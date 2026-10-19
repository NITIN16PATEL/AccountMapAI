# Microsoft Graph integration guide

The project is structured to support a second provider adapter for Microsoft Graph. This is scaffolded to help future live integrations without forcing provider credentials into source code.

## Required setup

1. Register an app in Microsoft Entra ID.
2. Add Microsoft Graph permissions appropriate to the minimum required metadata flow.
3. Configure the OAuth redirect URI for local development.
4. Store credentials in environment variables rather than in source files.

## Scope guidance

Prefer a metadata-only or message-header flow before requesting broad mail-content permissions. Message content should be treated as untrusted and only used when a user explicitly consents and the workflow requires it.
