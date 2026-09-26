# Contributing to CEL

CEL is an open language/specification. Contributions should make incident and
response vocabulary more interoperable without adding an ingest runtime, policy
engine, dashboard product, or actuation path.

## Before you start

1. Read [`README.md`](./README.md) and [`GOVERNANCE.md`](./GOVERNANCE.md).
2. Search existing taxonomy, response-machine, crosswalk, and RFC files.
3. Open an issue before a semantic change so the compatibility impact is
   visible.
4. Never commit secrets, customer data, live coordinates, or unredacted feed
   payloads.

## Local setup

```bash
python3 -m pip install "jsonschema>=4.0" "pyyaml>=6.0"
python3 tooling/validate_cel.py
python3 -m unittest tooling.test_cel_v0 -v
python3 website/build_snapshot.py --check
node --check website/app.js
python3 -m http.server 8787 --directory website
```

If you change `taxonomies/` or `response_machines/`, regenerate the explorer
snapshot:

```bash
python3 website/build_snapshot.py
```

Commit the resulting `website/data.js` with the source change. CI rejects stale
generated data.

## Contribution types

- **Vocabulary:** new or changed `disaster.*` incident words.
- **Response:** new or changed `response.*` states and transitions.
- **Crosswalk:** mapping an external identifier to a CEL word.
- **Schema:** machine-readable contract changes.
- **Documentation:** examples, RFCs, or explorer copy.
- **Tooling:** validators or generated-snapshot tooling.

Every semantic change must describe compatibility, source provenance, and why
the change belongs in CEL rather than Sentinel, VITO, OIDF, or a consumer.

## Pull requests

- Use the pull request template.
- Keep one conceptual change per PR.
- Add or update tests for validator behavior.
- Do not edit generated `website/data.js` by hand.
- Do not add thresholds, recommendations, alerting, or actuator calls.
- Use the DCO sign-off in each commit:

```text
Signed-off-by: Your Name <your-email@example.com>
```

There is no CLA at this stage. Contributions are accepted under Apache-2.0
through the DCO sign-off and maintainer review.
