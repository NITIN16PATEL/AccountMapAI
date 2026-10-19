from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


def _provider_summary(name: str, client_id: str, redirect_uri: str) -> dict:
    configured = bool((client_id or "").strip())
    return {
        "name": name,
        "status": "configured" if configured else "demo",
        "mode": "configured" if configured else "demo",
        "enabled": configured,
        "redirect_uri": redirect_uri,
        "requires_credentials": True,
    }


@router.get("/status")
def provider_status():
    return {
        "message": "Provider capabilities are environment-driven and credential-safe.",
        "providers": [
            _provider_summary("gmail", settings.gmail_client_id, settings.gmail_redirect_uri),
            _provider_summary("microsoft", settings.microsoft_client_id, settings.microsoft_redirect_uri),
        ],
        "ai": {
            "provider": settings.ai_provider,
            "configured": bool((settings.ai_api_key or "").strip()),
            "mode": "configured" if settings.ai_provider and settings.ai_provider.lower() != "local" and bool((settings.ai_api_key or "").strip()) else "local",
        },
    }
