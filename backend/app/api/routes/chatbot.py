from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import settings

router = APIRouter()


class ChatbotRequest(BaseModel):
    message: str


def _infer_reply(message: str) -> str:
    normalized = (message or '').strip().lower()

    if not normalized:
        return 'Please ask a question about account review, risks, or cleanup steps.'

    if 'suspicious' in normalized or 'risk' in normalized or 'review' in normalized:
        return (
            'Start by checking evidence quality: look for welcome emails, password-reset notices, and confirmed account creation events. '
            'If the source is weak or inconsistent, mark it as pending review and avoid deleting anything until you confirm it.'
        )

    if 'password' in normalized:
        return (
            'Password imports should be treated as hints, not proof. Review the site name, the import date, and whether the entry appears in a real account list. '
            'Never store the raw password payload beyond the preview step.'
        )

    if 'gmail' in normalized or 'microsoft' in normalized or 'google' in normalized:
        return (
            'For Gmail or Microsoft sources, prefer metadata and consented evidence first. Only access message content when the user explicitly approves the workflow.'
        )

    if 'privacy' in normalized or 'consent' in normalized:
        return (
            'The safest approach is to keep consent as a separate audit record, minimize the data retained, and only act on evidence after the user reviews it.'
        )

    if 'cleanup' in normalized or 'delete' in normalized or 'remove' in normalized:
        return (
            'Use the official service management page, not just a guessed deletion URL. Confirm the account is truly inactive, then delete it and record the action in the audit log.'
        )

    return (
        'I can help you assess suspicious accounts, explain how inventory evidence is ranked, and suggest safe next steps for cleanup or privacy review.'
    )


@router.post('/message')
def chatbot_message(payload: ChatbotRequest):
    reply = _infer_reply(payload.message)
    provider_mode = 'configured' if bool((settings.ai_api_key or '').strip()) else 'local'
    return {
        'reply': reply,
        'mode': provider_mode,
        'provider': settings.ai_provider,
    }
