from fastapi import APIRouter

router = APIRouter()


@router.get("/stats")
def get_dashboard_stats():
    return {
        "total_accounts": 0,
        "confirmed_accounts": 0,
        "possible_accounts": 0,
        "saved_password_accounts": 0,
        "email_evidence_accounts": 0,
        "phone_confirmed_accounts": 0,
        "recent_services": [],
        "forgotten_accounts": [],
        "accounts_needing_review": [],
        "demo_mode": True,
    }
