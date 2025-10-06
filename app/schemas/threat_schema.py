from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ThreatBase(BaseModel):
    title: str
    description: Optional[str] = None
    threat_level: Optional[str] = None
    source: Optional[str] = None

class ThreatCreate(ThreatBase):
    pass

class ThreatResponse(ThreatBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
