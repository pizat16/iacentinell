from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from routes import auth, shield, forensics, audit, ai

load_dotenv()

app = FastAPI(
    title="IA CENTINELL v6.0",
    description="Enterprise Security Intelligence Platform",
    version="6.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(shield.router, prefix="/api/shield", tags=["shield"])
app.include_router(forensics.router, prefix="/api/forensics", tags=["forensics"])
app.include_router(audit.router, prefix="/api/audit", tags=["audit"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "6.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
