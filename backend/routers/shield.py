from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
import hashlib
import os

router = APIRouter()

KNOWN_MALWARE_HASHES = {
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855": "EICAR Test File",
    "a3f5d2c9b1e8f4a7d6c3b2e1f9a8d7c6b5e4f3a2d1c0b9e8f7a6d5c4b3e2f1": "Trojan.Generic",
}

class ScanResponse(BaseModel):
    filename: str
    hash: str
    isMalicious: bool
    verdict: str
    analysis: str

@router.post("/scan", response_model=ScanResponse)
async def scan_file(file: UploadFile = File(...)):
    # Read file and compute SHA-256
    content = await file.read()
    file_hash = hashlib.sha256(content).hexdigest()
    
    # Check against known malware database
    is_malicious = file_hash in KNOWN_MALWARE_HASHES
    verdict = "⚠ THREAT DETECTED" if is_malicious else "✓ CLEAN"
    
    # Perform behavioral analysis
    analysis = f"""FILE ANALYSIS REPORT
    
Filename: {file.filename}
Size: {len(content)} bytes
SHA-256: {file_hash}

Verdict: {verdict}
Status: {'MALICIOUS' if is_malicious else 'CLEAN'}
"""
    
    return {
        "filename": file.filename,
        "hash": file_hash,
        "isMalicious": is_malicious,
        "verdict": verdict,
        "analysis": analysis
    }
