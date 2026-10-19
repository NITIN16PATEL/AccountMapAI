from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class SessionToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_email: str


class AccountRecordBase(BaseModel):
    service_name: str
    domain: str
    category: str = "general"
    masked_identifier: Optional[str] = None
    phone_association: Optional[str] = None
    discovery_source: str = "manual"
    evidence_type: str = "email"
    confidence: Literal["low", "medium", "high"] = "medium"
    verification_status: Literal["pending", "confirmed", "rejected"] = "pending"
    status: Literal["active", "unused", "review", "closed"] = "review"
    notes: Optional[str] = None
    management_url: Optional[str] = None
    deletion_url: Optional[str] = None


class AccountRecordCreate(AccountRecordBase):
    pass


class AccountRecordUpdate(AccountRecordBase):
    pass


class AccountRecordOut(AccountRecordBase):
    id: int

    class Config:
        from_attributes = True


class DiscoveryClassificationRequest(BaseModel):
    subject: str
    body: str = ""


class DiscoveryClassificationResult(BaseModel):
    service_name: str
    domain: str
    category: str
    confidence: str
    rationale: str


class CSVImportPreview(BaseModel):
    file_name: str
    rows: list[dict]
    valid: bool
    message: str


class ConsentRecordCreate(BaseModel):
    purpose: str
    consented: bool
    consent_text: str


class PrivacyExport(BaseModel):
    user_email: str
    accounts: list[dict]
    consent_records: list[dict]
    connected_sources: list[dict]
    audit_events: list[dict]


class HealthStatus(BaseModel):
    status: str = "ok"
    app: str = "AccountMap AI"
