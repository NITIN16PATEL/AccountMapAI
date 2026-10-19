from datetime import datetime, timedelta
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password
from app.db.session import get_db
from app.models import User, UserSession
from app.schemas import SessionToken, UserCreate, UserLogin

router = APIRouter()


@router.post("/register")
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if len(payload.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters.")

    email = payload.email.lower()
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(email=email, password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(str(user.id))
    db.add(
        UserSession(
            user_id=user.id,
            token_hash=token,
            expires_at=datetime.utcnow() + timedelta(days=7),
        )
    )
    db.commit()
    return {"status": "registered", "token": token, "user": {"email": user.email}, "access_token": token, "user_email": user.email}


@router.post("/login")
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(str(user.id))
    db.add(
        UserSession(
            user_id=user.id,
            token_hash=token,
            expires_at=datetime.utcnow() + timedelta(days=7),
        )
    )
    db.commit()
    return {"status": "ok", "token": token, "user": {"email": user.email}, "access_token": token, "user_email": user.email}


def _provider_demo_response(provider_name: str, instructions: str):
    return {
        "provider": provider_name,
        "status": "demo",
        "mode": "demo",
        "message": f"{provider_name.title()} OAuth is not configured. {instructions}",
    }


@router.get("/google/login")
def google_login():
    if not settings.gmail_client_id:
        return _provider_demo_response(
            "gmail",
            "Set GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, and GMAIL_REDIRECT_URI in the environment before enabling live Google OAuth.",
        )

    params = {
        "client_id": settings.gmail_client_id,
        "redirect_uri": settings.gmail_redirect_uri,
        "response_type": "code",
        "scope": "openid email profile https://www.googleapis.com/auth/gmail.readonly",
        "access_type": "offline",
        "prompt": "consent",
    }
    return {
        "provider": "gmail",
        "status": "configured",
        "mode": "configured",
        "authorization_url": f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}",
    }


@router.get("/google/callback")
def google_callback(
    code: str | None = Query(default=None),
    state: str | None = Query(default=None),
    error: str | None = Query(default=None),
):
    if error:
        return {"provider": "gmail", "status": "error", "mode": "demo", "message": f"Google callback returned an error: {error}"}

    if not settings.gmail_client_id:
        return _provider_demo_response(
            "gmail",
            "Google OAuth remains in demo mode until the required environment variables are filled in.",
        )

    return {
        "provider": "gmail",
        "status": "received",
        "mode": "configured",
        "message": "Google OAuth callback received. Exchange the code with the provider to complete login.",
        "code": code,
        "state": state,
    }


@router.get("/microsoft/login")
def microsoft_login():
    if not settings.microsoft_client_id:
        return _provider_demo_response(
            "microsoft",
            "Set MICROSOFT_CLIENT_ID, MICROSOFT_CLIENT_SECRET, and MICROSOFT_REDIRECT_URI in the environment before enabling live Microsoft OAuth.",
        )

    params = {
        "client_id": settings.microsoft_client_id,
        "response_type": "code",
        "redirect_uri": settings.microsoft_redirect_uri,
        "response_mode": "query",
        "scope": "openid profile email Mail.Read",
        "state": "accountmap-ai",
    }
    return {
        "provider": "microsoft",
        "status": "configured",
        "mode": "configured",
        "authorization_url": f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?{urlencode(params)}",
    }


@router.get("/microsoft/callback")
def microsoft_callback(
    code: str | None = Query(default=None),
    state: str | None = Query(default=None),
    error: str | None = Query(default=None),
):
    if error:
        return {"provider": "microsoft", "status": "error", "mode": "demo", "message": f"Microsoft callback returned an error: {error}"}

    if not settings.microsoft_client_id:
        return _provider_demo_response(
            "microsoft",
            "Microsoft OAuth remains in demo mode until the required environment variables are filled in.",
        )

    return {
        "provider": "microsoft",
        "status": "received",
        "mode": "configured",
        "message": "Microsoft OAuth callback received. Exchange the code with the provider to complete login.",
        "code": code,
        "state": state,
    }


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    sessions = db.query(UserSession).filter(UserSession.user_id == current_user.id).all()
    for session in sessions:
        session.revoked = True
    db.commit()
    return {"status": "logged_out"}


@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "consented": current_user.consented}
