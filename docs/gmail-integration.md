# Gmail integration guide

## Development status

The project includes an extensible email discovery layout and deterministic classification helper for Gmail-style evidence. Live Google OAuth requires a real Google Cloud project and an approved OAuth client.

## Required setup

1. Create a Google Cloud project.
2. Enable the Gmail API.
3. Create OAuth 2.0 credentials.
4. Add the redirect URI: `http://localhost:8000/api/auth/google/callback`
5. Set `MAIL_CLIENT_ID`, `MAIL_CLIENT_SECRET`, and `MAIL_REDIRECT_URI` in the environment.

## Permission model

Use the smallest Gmail scope required for metadata-only discovery first. Do not request full message-body access unless a user is informed and the review path explicitly requires it.

## Local mock mode

If credentials are not configured, the app continues in demo mode and displays deterministic sample evidence rather than pretending the live Gmail API is connected.
