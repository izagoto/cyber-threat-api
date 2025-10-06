from typing import Dict, Any
import re

KEYWORD_MAP = {
    "phishing": ["phish", "credential", "login", "password", "bank", "invoice"],
    "malware": ["trojan", "ransom", "malware", "virus", "payload", "exploit"],
    "brute_force": ["failed login", "invalid password", "too many attempts", "brute force"],
    "ddos": ["ddos", "flood", "traffic spike", "syn flood"],
}

SEVERITY_SCORE = {
    "low": 10,
    "medium": 50,
    "high": 90
}

def normalize_text(text: str) -> str:
    return re.sub(r"\W+", " ", (text or "").lower())

def detect_types_and_score(title: str, description: str) -> Dict[str, Any]:
    text = normalize_text(f"{title} {description}")
    scores = {}
    for t, keywords in KEYWORD_MAP.items():
        count = sum(1 for kw in keywords if kw in text)
        if count > 0:
            scores[t] = count
 
    total_hits = sum(scores.values())
    if total_hits >= 4:
        severity = "high"
    elif total_hits >= 2:
        severity = "medium"
    elif total_hits == 1:
        severity = "low"
    else:
        severity = "low"

    numeric_score = SEVERITY_SCORE[severity]
    return {
        "detected_types": list(scores.keys()),
        "hits": scores,
        "severity_label": severity,
        "severity_score": numeric_score
    }
