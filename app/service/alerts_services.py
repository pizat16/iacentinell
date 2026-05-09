from sqlalchemy.orm import Session
from app.audit.models import Alert, AuditLog
from datetime import datetime

def create_alert(db, severity, title, description=None, source=None):
    alert = Alert(severity=severity, title=title,
                  description=description, source=source)
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert

def log_audit(db, event_type, details=None, user_id=None, ip_address=None):
    entry = AuditLog(user_id=user_id, event_type=event_type,
                     details=details, ip_address=ip_address,
                     created_at=datetime.utcnow())
    db.add(entry)
    db.commit()
    return entry
