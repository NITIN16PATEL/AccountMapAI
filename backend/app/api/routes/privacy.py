from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import AccountRecord, AuditEvent, ConsentRecord, User

router = APIRouter()


@router.get("/settings")
def settings(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return {
        "retention_days": 365,
        "data_export_enabled": True,
        "demo_mode": True,
        "email_discovery_consent": bool(current_user.consented),
    }


@router.post("/consent")
def save_consent(payload: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    consent = ConsentRecord(
        user_id=current_user.id,
        purpose=payload.get("purpose", "email-discovery"),
        consented=bool(payload.get("consented", False)),
        consent_text=payload.get("consent_text", "I consent to discovery processing."),
    )
    db.add(consent)
    current_user.consented = bool(payload.get("consented", False))
    db.add(AuditEvent(user_id=current_user.id, event_type="consent_updated", message="Consent preference updated"))
    db.commit()
    return {"status": "saved"}


@router.get("/export")
def export_data(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    accounts = db.query(AccountRecord).filter(AccountRecord.user_id == current_user.id).all()
    consent_records = db.query(ConsentRecord).filter(ConsentRecord.user_id == current_user.id).all()
    audit_events = db.query(AuditEvent).filter(AuditEvent.user_id == current_user.id).all()
    return {
        "user_email": current_user.email,
        "accounts": [
            {
                "id": item.id,
                "service_name": item.service_name,
                "domain": item.domain,
                "status": item.status,
                "verification_status": item.verification_status,
            }
            for item in accounts
        ],
        "consent_records": [{"purpose": item.purpose, "consented": item.consented} for item in consent_records],
        "audit_events": [{"event_type": item.event_type, "message": item.message} for item in audit_events],
    }


@router.post("/delete-account")
def delete_account(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.query(AccountRecord).filter(AccountRecord.user_id == current_user.id).delete()
    db.query(ConsentRecord).filter(ConsentRecord.user_id == current_user.id).delete()
    db.query(AuditEvent).filter(AuditEvent.user_id == current_user.id).delete()
    db.delete(current_user)
    db.commit()
    return {"status": "deleted", "user_email": current_user.email}
