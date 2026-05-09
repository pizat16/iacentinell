from sqlalchemy.orm import Session
from datetime import datetime
from app.auth.models import User
from app.core.security import hash_password, verify_password

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    user.last_login = datetime.utcnow()
    db.commit()
    return user

def create_user(db: Session, username: str, password: str, company: str = None,
                role: str = "operator", clearance_level: str = "LEVEL-1",
                is_admin: bool = False):
    user = User(username=username, password_hash=hash_password(password),
                company=company, role=role, clearance_level=clearance_level,
                is_admin=is_admin)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_all_users(db: Session):
    return db.query(User).filter(User.is_active == True).all()
