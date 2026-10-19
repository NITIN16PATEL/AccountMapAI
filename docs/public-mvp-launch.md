# Public MVP launch plan

This is the first production step: launch the app publicly using free or low-cost services without paying for infrastructure upfront.

## Recommended deployment stack

### Frontend
- Netlify or Cloudflare Pages
- Free build and hosting for the React app
- Use the production build output from `frontend/dist`

### Backend
- Render or Railway
- Deploy the FastAPI service as a Python app
- Set environment variables securely in the hosting dashboard

### Database
- Supabase Postgres free tier for the public MVP
- Keep SQLite only for local development and testing

### Domain and security
- Cloudflare free DNS and SSL
- Use HTTPS only
- Keep secrets in environment variables and never in source control

## Recommended architecture

- Frontend: static React SPA served from Netlify or Cloudflare Pages
- API: FastAPI backend on Render or Railway
- Database: Supabase Postgres
- Auth: Supabase Auth or a JWT setup aligned with the current app
- AI assistant: keep it in local/demo mode until a free API key is available

## Why this is the right first step

- Keeps the app real and accessible to users
- Avoids paying for hosting before demand is proven
- Uses free services that are common and easy to maintain
- Keeps the project honest about demo-only capabilities

## Free-tier limits and data safety

- Render free web services sleep after 15 minutes without traffic and have an ephemeral filesystem. Never store production data in SQLite on Render.
- Supabase free projects include 500 MB of database storage and pause after one week of inactivity. Confirm the current plan limits before launch.
- Render's free Postgres databases expire after 30 days, so use Supabase Postgres instead if remaining on the free tier.
- Treat this combination as a public demo/pilot only. Do not invite users to store sensitive account inventories until authentication, authorization, backups, migrations, and production security have been reviewed.

## Production requirements before public launch

1. Move from SQLite to a public database like Supabase Postgres.
2. Put all secrets in environment variables.
3. Update CORS to include the public frontend URL.
4. Ensure JWT secret and database URLs are not committed.
5. Add HTTPS-only deployment and secure cookie settings.
6. Turn off demo-only assumptions in public production mode.
7. Keep the chatbot in local demo mode unless you add a real AI API key.

## Recommended deployment checklist

### Frontend checklist
- Run `npm run build`
- Upload the `frontend/dist` folder to Netlify or Cloudflare Pages
- Set `VITE_API_BASE_URL` to the live backend URL

### Backend checklist
- Deploy the `backend` project to Render or Railway
- Set up environment values for:
  - `APP_NAME`
  - `SECRET_KEY`
  - `DATABASE_URL`
  - `JWT_ALGORITHM`
  - `ACCESS_TOKEN_EXPIRE_MINUTES`
  - `DEMO_MODE`
  - `AI_PROVIDER`
  - `AI_API_KEY`
  - provider credential variables if enabled

### Database checklist
- Create a Supabase Postgres instance
- Copy its connection string directly into Render's `DATABASE_URL` environment setting. Do not paste the connection string into chat or commit it.
- Run the same schema creation flow used locally
- Confirm migration or auto-table creation works in the new environment

## Account and secret handling

Create and sign in to provider accounts yourself. Never send account passwords, database connection strings, API keys, or verification codes in chat. Add secrets directly to the provider dashboards. The deployment cannot be completed until the repository is pushed to GitHub and the provider accounts and project have been created.

## Free tools to use first

- GitHub for source control
- Netlify or Cloudflare Pages for frontend
- Render or Railway for backend
- Supabase for database and auth
- Cloudflare for domain + SSL
- Plausible or PostHog for analytics

## Monetization path after launch

- Freemium plan for limited account records
- Premium AI features
- Team workspaces
- Export and review reports
- Paid higher-tier privacy and cleanup features

## Recommended next milestone

After the public MVP is live, the next step should be:
- add real auth to production
- replace demo data with real user data flows
- add a strong onboarding flow
- test the core sign-up and inventory journey end to end
