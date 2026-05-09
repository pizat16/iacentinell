from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user, require_admin, create_access_token
from app.auth.schemas import LoginRequest, TokenResponse, UserCreate, UserResponse
from app.auth.service import authenticate_user, create_user, get_all_users
from typing import List

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, body.username, body.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials")
    token = create_access_token({"sub": user.username, "role": user.role})
    return TokenResponse(access_token=token, username=user.username,
                         company=user.company or "", role=user.role,
                         clearance_level=user.clearance_level, is_admin=user.is_admin)

@router.get("/me", response_model=UserResponse)
async def get_me(current_user=Depends(get_current_user)):
    return current_user

@router.post("/users", response_model=UserResponse,
             dependencies=[Depends(require_admin)])
async def create_new_user(body: UserCreate, db: Session = Depends(get_db)):
    try:
        return create_user(db, **body.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users", response_model=List[UserResponse],
            dependencies=[Depends(require_admin)])
async def list_users(db: Session = Depends(get_db)):
    return get_all_users(db)
