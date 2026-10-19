# AccountMap AI

AccountMap AI is a privacy-first digital-footprint organizer for discovering, reviewing, and cleaning up forgotten online accounts based on email, saved-password imports, and phone-associated evidence.

## Features

- Secure registration, login, logout, and demo session management
- Dashboard stats for discovered, confirmed, and review-needed accounts
- Email evidence classification with a deterministic rules engine
- Saved-password import preview and safe local processing
- Account inventory management and status tracking
- Privacy and security center for export, deletion, and audit trails
- AI suggestions behind a configurable provider interface with deterministic fallback
- Responsive React frontend and FastAPI backend

## Local setup

### 1. Backend

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend

```powershell
cd frontend
$env:Path = "C:\Program Files\nodejs;$env:Path"
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

## Public MVP launch path

The first production milestone is a public MVP using free services. The recommended path is:

- Frontend: Netlify or Cloudflare Pages
- Backend: Render or Railway
- Database: Supabase Postgres free tier
- Domain + SSL: Cloudflare
- Auth: Supabase Auth or a JWT setup aligned with the current app
- AI: keep in local/demo mode unless a free API key is configured

See [docs/public-mvp-launch.md](docs/public-mvp-launch.md) for the full step-by-step plan.

## Demo mode

The app ships in a documented demo mode with realistic sample data. It does not claim universal account discovery and clearly labels estimates as partial results.

## Security notes

- No raw passwords are stored or logged.
- Passwords are hashed with `passlib[bcrypt]`.
- Email content is treated as untrusted and never executed.
- OAuth and credential fields are expected to be provided via environment variables, not checked into source control.

## Known limitations

- Gmail and Microsoft live integrations are scaffolded and documented; live provider verification still requires credentials and provider approval.
- AI suggestions are optional and can run in local deterministic mode if no API key is configured.
- MySQL is supported in configuration, but SQLite is used by default for local development and testing.

## Documentation

See the docs folder for privacy, threat model, Gmail guidance, Microsoft Graph guidance, and operations notes.
