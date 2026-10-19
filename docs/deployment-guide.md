# Deployment guide

## Local development

Backend:

```powershell
cd "c:\Users\nitin\OneDrive\Desktop\AccountMapAI\backend"
.\.venv\Scripts\python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Frontend:

```powershell
cd "c:\Users\nitin\OneDrive\Desktop\AccountMapAI\frontend"
$env:Path = "C:\Program Files\nodejs;C:\Program Files\Git\cmd;$env:Path"
npm run dev -- --host 0.0.0.0 --port 5173
```

## Production notes

- Use environment variables for secret configuration.
- Prefer a managed MySQL instance over SQLite for production.
- Keep OAuth credentials and AI keys outside source control.
- Require HTTPS and secure cookies in deployment.
- Review retention, consent, and legal disclosures before wider launch.
