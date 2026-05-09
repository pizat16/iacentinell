from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    company: str
    role: str
    clearance_level: str
    is_admin: bool

class UserCreate(BaseModel):
    username: str
    password: str
    company: Optional[str] = None
    role: Optional[str] = "operator"
    clearance_level: Optional[str] = "LEVEL-1"
    is_admin: Optional[bool] = False

class UserResponse(BaseModel):
    id: int
    username: str
    company: Optional[str]
    role: str
    clearance_level: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    class Config:
        from_attributes = True
