# Changelog

All notable CEL changes are recorded here.

## [Unreleased]

- Prepare public contribution, governance, security, and Pages hosting
  scaffolding.
- Publish the format surface on GitHub Pages: every `$id` now resolves at
  `https://tylereno.me/cel/schemas/…` (the dead `openeno.dev` host is retired),
  the deployment ships the format tree rather than the explorer alone, and the
  schema index, identifier manifest, and corpus listing are generated from the
  same scan that the deploy gate checks.

## [0.1.0] - 2026-08-20

- Define the speakable incident taxonomy.
- Define site-level response machines for wildland fire, earthquake, and flood.
- Add USGS, GDACS, and NWS CAP crosswalks.
- Validate the 14-source feed matrix.
- Add a static read-only vocabulary explorer.

CEL does not ingest feeds, evaluate policy, issue alerts, or actuate equipment.
