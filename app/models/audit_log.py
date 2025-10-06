from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.core.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(100), nullable=False) 
    user = Column(String(255), nullable=True)
    resource = Column(String(100), nullable=True)  
    details = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
