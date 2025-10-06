from app.core.database import Base, engine, SessionLocal
from app.models import threat_model  # pastikan model diimpor setelah Base
from sqlalchemy.orm import Session

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
