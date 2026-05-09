import re
from typing import List, Dict

MITRE_TECHNIQUES = {
    "T1059": "Command and Scripting Interpreter",
    "T1055": "Process Injection",
    "T1486": "Data Encrypted for Impact (Ransomware)",
    "T1566": "Phishing",
    "T1190": "Exploit Public-Facing Application",
    "T1078": "Valid Accounts",
    "T1082": "System Information Discovery",
    "T1041": "Exfiltration Over C2 Channel",
}

def extract_iocs(text: str) -> Dict:
    return {
        "ip": list(set(re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text)))[:20],
        "domain": list(set(re.findall(r"[a-zA-Z0-9\-]{2,}\.[a-zA-Z]{2,}", text)))[:20],
        "hash_sha256": list(set(re.findall(r"\b[a-fA-F0-9]{64}\b", text)))[:10],
        "cve": list(set(re.findall(r"CVE-\d{4}-\d{4,7}", text)))[:10],
        "url": list(set(re.findall(r"https?://[^\s]+", text)))[:20],
    }

def map_mitre_techniques(text: str) -> List[Dict]:
    found = []
    for tid, name in MITRE_TECHNIQUES.items():
        if tid in text.upper() or name.lower() in text.lower():
            found.append({"id": tid, "name": name})
    return found

def calculate_threat_score(iocs, techniques, verdict="CLEAN") -> int:
    score = 60 if verdict=="MALICIOUS" else 30 if verdict=="SUSPICIOUS" else 0
    score += min(len(iocs.get("ip",[])) * 5, 20)
    score += min(len(techniques) * 8, 40)
    return min(score, 100)
