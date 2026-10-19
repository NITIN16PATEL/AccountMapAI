import csv
import io

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import AccountRecord, User
from app.schemas import DiscoveryClassificationRequest, DiscoveryClassificationResult
from app.services.email_classifier import classify_email_evidence, find_duplicate_candidates

router = APIRouter()


@router.post("/classify-message", response_model=DiscoveryClassificationResult)
def classify_message(payload: DiscoveryClassificationRequest):
    result = classify_email_evidence(payload.subject, payload.body)
    return DiscoveryClassificationResult(**result)


@router.get("/duplicates")
def duplicate_scan(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    records = db.query(AccountRecord).filter(AccountRecord.user_id == current_user.id).all()
    payload = [
        {
            "id": record.id,
            "service_name": record.service_name,
            "domain": record.domain,
        }
        for record in records
    ]
    return {"duplicates": find_duplicate_candidates(payload)}


@router.post("/import-demo")
def import_demo(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    sample_records = [
        {"service_name": "GitHub", "domain": "github.com", "category": "developer", "discovery_source": "email"},
        {"service_name": "Dropbox", "domain": "dropbox.com", "category": "storage", "discovery_source": "email"},
    ]

    for item in sample_records:
        exists = db.query(AccountRecord).filter(AccountRecord.user_id == current_user.id, AccountRecord.service_name == item["service_name"]).first()
        if not exists:
            db.add(AccountRecord(user_id=current_user.id, **item, masked_identifier="demo@accountmap.ai", confidence="medium", verification_status="pending", status="review"))
    db.commit()
    return {"status": "imported", "count": len(sample_records)}
