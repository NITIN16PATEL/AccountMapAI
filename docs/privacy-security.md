# Privacy and security design notes

## Data minimization

- Store only the data required for inventory review and user visibility.
- Do not persist raw passwords or email bodies beyond the minimum required for review.
- Use masked or partial identifiers for account records whenever possible.

## Consent and controls

- Consent records are tracked separately from account data.
- Users can review and update their privacy preferences.
- OAuth disconnection is supported at the application layer; provider-level revocation should be completed in the external service.

## Retention

The app defaults to a clear retention profile and supports future configuration for deletion windows. Records should be deleted automatically according to policy, and backups should be reviewed before any production rollout.

## Regulatory note

This project is designed with DPDP, 2023 principles in mind, but it is not legal counsel or a certification artifact. Legal review is still required before commercialization.
