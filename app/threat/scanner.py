import re
from app.services.hash_service import sha256_bytes

KNOWN_SIGNATURES = {
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855": "EICAR Test File",
    "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592": "Ransomware.WannaCry",
}

HIGH_RISK_EXTENSIONS = {"exe","dll","bat","cmd","vbs","ps1","scr","com","pif","jar","msi","hta","wsf"}

SUSPICIOUS_PATTERNS = [
    r"powershell\s+-enc", r"cmd\.exe\s+/c", r"reg\s+add\s+HKLM",
    r"wget\s+https?://", r"curl\s+-O\s+https?://", r"base64_decode",
    r"CreateRemoteThread", r"VirtualAllocEx", r"WScript\.Shell",
]

def scan_file(file_bytes: bytes, filename: str) -> dict:
    file_hash = sha256_bytes(file_bytes)
    if file_hash in KNOWN_SIGNATURES:
        return {"sha256": file_hash, "verdict": "MALICIOUS", "risk_score": 95,
                "signature_match": KNOWN_SIGNATURES[file_hash],
                "findings": [f"KNOWN SIGNATURE: {KNOWN_SIGNATURES[file_hash]}"],
                "method": "signature"}
    findings, risk = [], 0
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext in HIGH_RISK_EXTENSIONS:
        findings.append(f"HIGH-RISK EXTENSION: .{ext}"); risk += 25
    try:
        text = file_bytes.decode("utf-8", errors="ignore")
        for pat in SUSPICIOUS_PATTERNS:
            if re.search(pat, text, re.IGNORECASE):
                findings.append(f"PATTERN: {pat}"); risk += 15
    except Exception:
        pass
    verdict = "CLEAN"
    if risk >= 70: verdict = "MALICIOUS"
    elif risk >= 35: verdict = "SUSPICIOUS"
    return {"sha256": file_hash, "verdict": verdict, "risk_score": min(risk, 100),
            "signature_match": None,
            "findings": findings if findings else ["No threats detected"],
            "method": "heuristic"}
