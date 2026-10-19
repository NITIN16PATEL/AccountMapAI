import csv
import io

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import AccountRecord, ImportJob, User

router = APIRouter()


@router.post("/validate-csv")
def validate_csv(file: UploadFile, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    content = file.file.read()
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="CSV file is empty")

    text = content.decode("utf-8", errors="ignore")
    reader = csv.DictReader(io.StringIO(text))
    rows = []
    for row in reader:
        cleaned = {key: (value or "").strip() for key, value in row.items()}
        if cleaned.get("service") or cleaned.get("website") or cleaned.get("name"):
            rows.append(cleaned)

    job = ImportJob(user_id=current_user.id, source_type="saved_password_csv", status="validated", rows_processed=len(rows))
    db.add(job)
    db.commit()
    return {"valid": True, "message": "CSV format supported", "rows": rows[:10], "job_id": job.id}


@router.post("/process-preview")
def process_preview(file: UploadFile, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    content = file.file.read()
    rows = []
    for row in csv.DictReader(io.StringIO(content.decode("utf-8", errors="ignore"))):
        service = (row.get("service") or row.get("website") or row.get("name") or "Unknown").strip()
        domain = (row.get("domain") or service).strip()
        rows.append({
            "service_name": service,
            "domain": domain,
            "masked_identifier": "masked-user",
            "discovery_source": "saved_password",
            "confidence": "medium",
        })

    for item in rows:
        db.add(
            AccountRecord(
                user_id=current_user.id,
                service_name=item["service_name"],
                domain=item["domain"],
                category="import",
                masked_identifier=item["masked_identifier"],
                discovery_source=item["discovery_source"],
                confidence=item["confidence"],
                verification_status="pending",
                status="review",
                evidence_type="saved_password_import",
            )
        )
    db.commit()
    return {"processed": len(rows), "message": "Imported records have been added to the inventory."}
