# Known limitations and roadmap

## Current MVP status

This workspace includes a working local MVP for the core product experience, including:

- FastAPI backend with demo auth routes and user-scoped inventory logic
- SQLite-backed local data model for development and testing
- Vite + React UI with dashboard and account inventory sections
- Deterministic classification logic for email evidence
- CSV import preview workflow
- Privacy and consent scaffolding

## Known limitations

- Live Gmail and Microsoft Graph provider integrations require real credentials, provider approval, and consent flows.
- No production-grade MySQL migration strategy has been executed yet.
- AI classification is optional and local-by-default.
- The app currently emphasizes an honest demo and review-oriented workflow rather than full provider automation.

## Recommended next milestone

1. Add a final MySQL migration and production security hardening pass.
2. Implement provider adapters and OAuth callback flows with explicit consent UI.
3. Expand inventory and cleanup workflows with richer evidence review and request drafting.
4. Add browser E2E coverage for the core user journey.
