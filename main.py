from fastapi import FastAPI
from app.routes.threats import router as threats_router
from app.routes.auth import router as auth_router
from app.database import init_db

app = FastAPI(
    title="Cyber Threat Intelligence API",
    description="API untuk mengelola dan mendeteksi ancaman siber",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to Cyber Threat API"}

app.include_router(threats_router, prefix="/api/threats", tags=["Threats"])
app.include_router(auth_router, prefix="/api", tags=["Authentication"])
