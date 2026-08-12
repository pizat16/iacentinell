from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import hashlib
import jwt
from datetime import datetime, timedelta
from config import settings

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str
    apiKey: str = None

class LoginResponse(BaseModel):
    token: str
    user: dict

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    # Demo authentication
    if request.username != "beacon" or request.password != "beacon2025":
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate JWT token
    payload = {
        "sub": request.username,
        "exp": datetime.utcnow() + timedelta(days=1),
        "iat": datetime.utcnow()
    }
    
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return {
        "token": token,
        "user": {
            "username": request.username,
            "company": "Beacon of the Eagle LLC",
            "role": "LEVEL-5 ADMIN"
        }
    }

@router.post("/logout")
async def logout():
    return {"message": "Logged out successfully"}
