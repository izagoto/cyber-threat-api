from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.threat_model import Threat
from app.schemas.threat_schema import ThreatCreate, ThreatResponse
from typing import List
from app.services.analysis import detect_types_and_score
from app.models.audit_log import AuditLog
from app.logger import logger
from app.database import get_db
from app.auth import get_current_user  

router = APIRouter()


@router.post("/", response_model=ThreatResponse)
def create_threat(
    threat: ThreatCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)):

    analysis = detect_types_and_score(threat.title, threat.description)
    new_threat = Threat(**threat.dict())
    new_threat.threat_level = analysis["severity_label"]
    new_threat.analysis_score = analysis["severity_score"]
    new_threat.detected_types = ",".join(analysis["detected_types"])
    log = AuditLog(action="create_threat", user=current_user.username, resource=f"threats:{new_threat.id}",
               details=f"score={new_threat.analysis_score}, types={new_threat.detected_types}")
    db.commit()
    db.add(log)
    logger.info(f"User={current_user.username} created threat id={new_threat.id} severity={new_threat.threat_level}")
    db.refresh(new_threat)
    return new_threat


@router.get("/", response_model=List[ThreatResponse])
def get_threats(db: Session = Depends(get_db)):
    return db.query(Threat).all()

@router.get("/{threat_id}", response_model=ThreatResponse)
def get_threat(threat_id: int, db: Session = Depends(get_db)):
    threat = db.query(Threat).filter(Threat.id == threat_id).first()
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    return threat

@router.put("/{threat_id}", response_model=ThreatResponse)
def update_threat(threat_id: int, updated: ThreatCreate, db: Session = Depends(get_db)):
    threat = db.query(Threat).filter(Threat.id == threat_id).first()
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    for key, value in updated.dict().items():
        setattr(threat, key, value)
    db.commit()
    db.refresh(threat)
    return threat

@router.delete("/{threat_id}")
def delete_threat(threat_id: int, db: Session = Depends(get_db)):
    threat = db.query(Threat).filter(Threat.id == threat_id).first()
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    db.delete(threat)
    db.commit()
    return {"message": f"Threat with ID {threat_id} deleted successfully"}
