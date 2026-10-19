# Threat model

The application is designed as a privacy-first account inventory for evidence-based discovery. The highest-risk areas are OAuth, email processing, password imports, and data export.

## Threats addressed

- Unauthorized access to user records through missing authentication or user scoping
- Brute-force sign-in attempts against the auth endpoints
- Raw password retention during CSV import or email processing
- Untrusted inbox content influencing app actions or automation
- Token or session leakage from missing secure session handling
- Lack of consent auditing and retention controls

## Controls in place

- Authentication and per-user scoping on API endpoints
- Password hashing using `passlib[bcrypt]`
- Local-only demo and import preview flow for CSV processing
- Deterministic classification rules for email evidence, never executing email attachments or messages
- Environment-based secret configuration stored outside source control
- Audit events for consent and deletion actions

## Remaining legal and operational review

- Provider-specific OAuth review, consent wording, and token retention choices should be approved by the product owner before live production use.
- Actual production compliance review for DPDP, 2023 and sector-specific needs is a legal responsibility, not a technical guarantee.
