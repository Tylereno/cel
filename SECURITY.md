# Security policy

CEL is a public vocabulary and schema project. It does not ingest live feeds,
store site data, evaluate consumer policy, or control equipment.

## Do not publish

Do not open a public issue or pull request containing:

- API keys, credentials, tokens, or private URLs
- customer names, sites, coordinates, or operational schedules
- unredacted live-feed payloads or deployment logs
- claims about an actual response, certification, or field deployment

Use synthetic fixtures and redacted examples.

## Reporting a vulnerability

Once the repository is transferred to the OpenLexicon organization, enable
GitHub private vulnerability reporting and use the repository Security tab.
Until then, contact the project maintainer privately through the GitHub account
that owns the repository. Do not put the details in a public issue.

## Scope

Security reports for a consumer, feed adapter, policy engine, or actuator belong
with that system's maintainers. CEL itself only owns the public vocabulary,
schemas, validators, and derived explorer.
