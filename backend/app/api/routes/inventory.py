from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import AccountRecord, User
from app.schemas import AccountRecordCreate, AccountRecordUpdate

router = APIRouter()


@router.get("/")
def list_accounts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    query = db.query(AccountRecord).filter(AccountRecord.user_id == current_user.id)
    total = query.count()
    rows = query.offset(skip).limit(limit).all()
    return {"items": [record_to_dict(r) for r in rows], "total": total}


@router.get("/{account_id}")
def get_account(account_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record = db.query(AccountRecord).filter(AccountRecord.user_id == current_user.id, AccountRecord.id == account_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Account not found")
    return record_to_dict(record)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_account(payload: AccountRecordCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record = AccountRecord(user_id=current_user.id, **payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record_to_dict(record)


@router.put("/{account_id}")
def update_account(account_id: int, payload: AccountRecordUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record = db.query(AccountRecord).filter(AccountRecord.user_id == current_user.id, AccountRecord.id == account_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Account not found")
    for field, value in payload.model_dump().items():
        setattr(record, field, value)
    db.commit()
    return record_to_dict(record)


@router.delete("/{account_id}")
def delete_account(account_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record = db.query(AccountRecord).filter(AccountRecord.user_id == current_user.id, AccountRecord.id == account_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Account not found")
    db.delete(record)
    db.commit()
    return {"deleted": True, "id": account_id}


def record_to_dict(record: AccountRecord):
    return {
        "id": record.id,
        "service_name": record.service_name,
        "domain": record.domain,
        "category": record.category,
        "masked_identifier": record.masked_identifier,
        "phone_association": record.phone_association,
        "discovery_source": record.discovery_source,
        "evidence_type": record.evidence_type,
        "confidence": record.confidence,
        "verification_status": record.verification_status,
        "status": record.status,
        "notes": record.notes,
        "management_url": record.management_url,
        "deletion_url": record.deletion_url,
    }
