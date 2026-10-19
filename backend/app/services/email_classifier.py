import re
from typing import Any


def classify_email_evidence(subject: str, body: str = "") -> dict[str, Any]:
    text = f"{subject} {body}".lower()

    rules = {
        "welcome": ["welcome", "verify your email", "confirm your account", "activate your account"],
        "password_reset": ["reset your password", "password reset", "security code"],
        "security_alert": ["security alert", "suspicious login", "new device", "we noticed a sign-in"],
        "purchase": ["receipt", "invoice", "order confirmation", "subscription confirmed"],
        "subscription": ["subscription", "your plan", "trial started"],
    }

    for category, tokens in rules.items():
        if any(token in text for token in tokens):
            domain = extract_domain(subject, body)
            return {
                "service_name": infer_service_name(subject, body),
                "domain": domain,
                "category": category,
                "confidence": "high" if category in {"welcome", "password_reset"} else "medium",
                "rationale": f"Matched rule set for {category} evidence.",
            }

    domain = extract_domain(subject, body)
    return {
        "service_name": infer_service_name(subject, body),
        "domain": domain,
        "category": "unknown",
        "confidence": "low",
        "rationale": "No strong deterministic rule matched. Requires review.",
    }


def extract_domain(subject: str, body: str = "") -> str:
    text = f"{subject} {body}"
    matches = re.findall(r"@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", text)
    if matches:
        return matches[0]
    return "unknown-domain"


def infer_service_name(subject: str, body: str = "") -> str:
    text = f"{subject} {body}".strip()
    # Very conservative service extraction: use email sender-like clues from common service emails.
    service_hints = [
        ("dropbox", "Dropbox"),
        ("github", "GitHub"),
        ("linkedin", "LinkedIn"),
        ("netflix", "Netflix"),
        ("amazon", "Amazon"),
        ("google", "Google"),
        ("microsoft", "Microsoft"),
    ]
    lowered = text.lower()
    for key, value in service_hints:
        if key in lowered:
            return value
    return "Unidentified service"


def find_duplicate_candidates(records: list[dict]) -> list[dict]:
    seen: dict[str, dict] = {}
    duplicates = []
    for record in records:
        key = (record.get("service_name") or "").lower(), (record.get("domain") or "").lower()
        if key in seen:
            duplicates.append({"first_id": seen[key]["id"], "second_id": record.get("id"), "service_name": record["service_name"]})
        else:
            seen[key] = record
    return duplicates
