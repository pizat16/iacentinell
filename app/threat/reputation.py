import re

MALICIOUS_IPS = {
    "203.0.113.42": {"score": 95, "category": "C2 Server"},
    "198.51.100.10": {"score": 88, "category": "Port Scanner"},
}
MALICIOUS_DOMAINS = {
    "malicious-c2.net": {"score": 99, "category": "Command & Control"},
    "phishing-update.com": {"score": 91, "category": "Phishing"},
}

def check_ip_reputation(ip):
    known = MALICIOUS_IPS.get(ip)
    if known:
        return {"indicator": ip, "type": "ip", "reputation_score": known["score"],
                "verdict": "MALICIOUS", "category": known["category"], "action": "BLOCK"}
    return {"indicator": ip, "type": "ip", "reputation_score": 5,
            "verdict": "CLEAN", "category": "Unknown", "action": "MONITOR"}

def check_domain_reputation(domain):
    known = MALICIOUS_DOMAINS.get(domain.lower())
    if known:
        return {"indicator": domain, "type": "domain",
                "reputation_score": known["score"], "verdict": "MALICIOUS",
                "category": known["category"], "action": "BLOCK"}
    return {"indicator": domain, "type": "domain", "reputation_score": 5,
            "verdict": "CLEAN", "category": "Unknown", "action": "ALLOW"}

def bulk_reputation_check(indicators):
    results = []
    for item in indicators:
        item = item.strip()
        if not item: continue
        if re.match(r"^(\d{1,3}\.){3}\d{1,3}$", item):
            results.append(check_ip_reputation(item))
        else:
            results.append(check_domain_reputation(item))
    return results
