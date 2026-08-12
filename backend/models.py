from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    company = Column(String)
    role = Column(String, default="USER")
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    scans = relationship("FileScan", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")

class FileScan(Base):
    __tablename__ = "file_scans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String)
    file_hash = Column(String, index=True)
    verdict = Column(String)  # CLEAN, SUSPICIOUS, MALICIOUS
    analysis = Column(Text)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="scans")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String)
    details = Column(Text)
    ip_address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="audit_logs")

class ThreatIndicator(Base):
    __tablename__ = "threat_indicators"
    
    id = Column(Integer, primary_key=True, index=True)
    indicator_type = Column(String)  # HASH, IP, DOMAIN, URL
    indicator_value = Column(String, index=True, unique=True)
    threat_level = Column(String)  # LOW, MEDIUM, HIGH, CRITICAL
    description = Column(Text)
    source = Column(String)
    added_at = Column(DateTime, default=datetime.utcnow)
