from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.auth.routes import router as auth_router
from app.threat.routes import router as threat_router
from app.network.routes import router as network_router
from app.guardian.routes import router as guardian_router
from app.audit.routes import router as audit_router
from app.websocket.routes import router as ws_router
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI(title="IA CENTINELL API", version="4.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(auth_router,     prefix="/auth",     tags=["Auth"])
app.include_router(threat_router,   prefix="/threat",   tags=["Threat"])
app.include_router(network_router,  prefix="/network",  tags=["Network"])
app.include_router(guardian_router, prefix="/guardian", tags=["Guardian"])
app.include_router(audit_router,    prefix="/audit",    tags=["Audit"])
app.include_router(ws_router,                           tags=["WebSocket"])
os.makedirs("app/uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="app/uploads"), name="uploads")

@app.get("/")
async def root():
    return {"platform": "IA CENTINELL", "version": "4.0.0", "status": "ONLINE"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
