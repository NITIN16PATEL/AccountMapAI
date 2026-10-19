# Testing report

## Backend verification

Command run:

```powershell
cd "c:\Users\nitin\OneDrive\Desktop\AccountMapAI\backend"
.\.venv\Scripts\python -m pytest -q
```

Result: 4 passed in 4.77s.

## Frontend verification

Command run:

```powershell
cd "c:\Users\nitin\OneDrive\Desktop\AccountMapAI\frontend"
npm test -- --run
```

Result: 1 passed in 2.70s.

## Production build verification

Command run:

```powershell
cd "c:\Users\nitin\OneDrive\Desktop\AccountMapAI\frontend"
npm run build
```

Result: Vite production build succeeded.
