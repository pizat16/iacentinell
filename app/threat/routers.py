from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.threat.scanner import scan_file
from app.threat.engine import extract_iocs, map_mitre_techniques, calculate_threat_score
from app.threat.reputation import bulk_reputation_check
from app.audit.models import Threat, Quarantine
from app.services.file_service import save_upload, get_mime_type
from app.services.alert_service import create_alert, log_audit
from app.core.websocket_manager import manager
from typing import List
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class IOCRequest(BaseModel):
    text: str

class ReputationRequest(BaseModel):
    indicators: List[str]

@router.post("/scan")
async def scan_file_endpoint(file: UploadFile = File(...),
                              db: Session = Depends(get_db),
                              current_user=Depends(get_current_user)):
    file_bytes = await file.read()
    if len(file_bytes) > 50 * 1024 * 1024:
        raise HTTPException(413, "File too large (max 50MB)")
    mime = get_mime_type(file_bytes, file.filename)
    result = scan_file(file_bytes, file.filename)
    saved = await save_upload(file_bytes, file.filename)
    threat = Threat(filename=file.filename, sha256=result["sha256"],
                    verdict=result["verdict"], risk_score=result["risk_score"],
                    details="\n".join(result["findings"]),
                    quarantined=result["verdict"]=="MALICIOUS")
    db.add(threat); db.commit(); db.refresh(threat)
    if result["verdict"] == "MALICIOUS":
        q = Quarantine(threat_id=threat.id, filename=file.filename,
                       sha256=result["sha256"], risk_level="HIGH",
                       threat_type=result.get("signature_match","Heuristic"),
                       status="QUARANTINED", auto_detected=True)
        db.add(q); db.commit()
        create_alert(db,"HIGH",f"Malware: {file.filename}",source="ThreatShield")
        await manager.broadcast_event("THREAT_DETECTED",
                                      {"filename":file.filename,"verdict":result["verdict"]})
    log_audit(db,"FILE_SCAN",f"{file.filename} -> {result['verdict']}",user_id=current_user.id)
    return {**result,"filename":file.filename,"size_bytes":len(file_bytes),
            "mime_type":mime,"threat_id":threat.id}

@router.post("/ioc-extract")
async def extract_ioc(body: IOCRequest, db: Session = Depends(get_db),
                      current_user=Depends(get_current_user)):
    iocs = extract_iocs(body.text)
    techniques = map_mitre_techniques(body.text)
    score = calculate_threat_score(iocs, techniques)
    log_audit(db,"IOC_EXTRACTION",f"Extracted IOCs",user_id=current_user.id)
    return {"iocs":iocs,"mitre_techniques":techniques,"threat_score":score}

@router.post("/reputation")
async def reputation_check(body: ReputationRequest, db: Session = Depends(get_db),
                            current_user=Depends(get_current_user)):
    results = bulk_reputation_check(body.indicators)
    malicious = [r for r in results if r["verdict"]=="MALICIOUS"]
    if malicious:
        create_alert(db,"HIGH",f"{len(malicious)} malicious indicators",source="ReputationEngine")
    log_audit(db,"REPUTATION_CHECK",f"Checked {len(body.indicators)}",user_id=current_user.id)
    return {"results":results,"total":len(results),"malicious_count":len(malicious)}

@router.get("/quarantine")
async def get_quarantine(db: Session = Depends(get_db),
                         current_user=Depends(get_current_user)):
    items = db.query(Quarantine).order_by(Quarantine.created_at.desc()).all()
    return [{"id":q.id,"filename":q.filename,"sha256":q.sha256,"risk_level":q.risk_level,
             "threat_type":q.threat_type,"status":q.status,"auto_detected":q.auto_detected,
             "created_at":q.created_at.isoformat() if q.created_at else None} for q in items]

@router.post("/quarantine/{qid}/clean")
async def clean_quarantine(qid: int, db: Session = Depends(get_db),
                            current_user=Depends(get_current_user)):
    q = db.query(Quarantine).filter(Quarantine.id == qid).first()
    if not q: raise HTTPException(404, "Not found")
    q.status = "CLEANED"; q.cleaned_at = datetime.utcnow(); db.commit()
    log_audit(db,"QUARANTINE_CLEAN",f"Cleaned: {q.filename}",user_id=current_user.id)
    return {"status":"cleaned","id":qid}
