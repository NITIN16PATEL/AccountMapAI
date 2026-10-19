# AI provider setup guide

The AI discovery layer is configurable and works in a local deterministic mode when no external API key is configured.

## Supported modes

- `local`: deterministic classification rules with no external provider required
- `openai` or similar provider: optional API-based classification behind a configured provider interface

## Environment configuration

Set the following values in a local `.env` file:

- `AI_PROVIDER=local`
- `AI_API_KEY=`

## Important guardrails

- Treat AI suggestions as estimates, not verified facts.
- Do not send raw inbox content to an external provider without explicit informed consent.
- Prefer minimal context and user-approved summarization windows.
