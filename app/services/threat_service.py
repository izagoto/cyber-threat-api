from app.models.threat_model import Threat

def get_all_threats():
    return [
        Threat(id=1, type="Malware", description="Trojan detected", level="High"),
        Threat(id=2, type="Phishing", description="Suspicious email", level="Medium")
    ]
