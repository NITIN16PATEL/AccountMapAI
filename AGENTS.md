# AccountMap AI agent instructions

This repository is a privacy-first account inventory and account-discovery MVP.

## Project goals
- Keep the app honest about what is verified versus demo-only.
- Prefer local deterministic logic unless real OAuth or AI credentials are configured.
- Protect user data and keep consent, retention, and audit logic explicit.
- Do not claim live Gmail, Microsoft, or AI integrations without real provider credentials and approvals.

## Working rules
- Use the existing local Python virtual environment in `backend/.venv` when running Python commands.
- Use `pytest` for backend validation and `npm run build` or `npm test -- --run` for frontend validation.
- Keep environment secrets in `.env` and never commit secrets.
- Favor small, verified fixes over broad speculation.
- If a feature depends on external credentials, implement the safe, configured/demo mode and document the missing step clearly.

## Local validation commands
- Backend tests: `cd backend; .\.venv\Scripts\python -m pytest -q`
- Frontend build: `cd frontend; npm run build`
- Frontend tests: `cd frontend; npm test -- --run`

## Important repo facts
- Backend app lives under `backend/app`.
- Frontend app lives under `frontend/src`.
- OAuth and provider configuration is environment-driven from `.env` and `Settings` in `backend/app/core/config.py`.
- Documentation is kept under the `docs` folder.
