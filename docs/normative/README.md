# Normative CEL contracts

**Ownership:** OpenLexicon project stewardship (transfer pending; Tyler Eno is provisional maintainer)
**Role:** Human-readable contracts for the Core Emergency Language
**Spec:** CEL v0.1.0 (lab)

CEL is a **new language**. The words in `taxonomies/` and
`response_machines/` are the language. Existing standards are **profiled**,
not substituted.

## Index

| Document | Title |
|---|---|
| [RFC-0001-scope.md](./RFC-0001-scope.md) | Language vs CAP/HIP/OIDF |
| [RFC-0002-incident-taxonomy.md](./RFC-0002-incident-taxonomy.md) | Speakable incident words |
| [RFC-0003-response-machines.md](./RFC-0003-response-machines.md) | Response states and transitions |
| [RFC-0004-ingest-vs-decision.md](./RFC-0004-ingest-vs-decision.md) | Sentinel reads; VITO decides |

## v0 artifacts

| Artifact | Role |
|---|---|
| [`taxonomies/disasters.yaml`](../../taxonomies/disasters.yaml) | CEL incident language |
| [`feeds/matrix.yaml`](../../feeds/matrix.yaml) | Sources Sentinel should ingest (14/14 implemented) |
| [`response_machines/`](../../response_machines/) | Response FSMs (wildland, earthquake, flood) |
| [`crosswalks/`](../../crosswalks/) | USGS, GDACS, NWS CAP → CEL |

Sentinel consumes CEL words. VITO applies policy. Neither mints CEL
identifiers here.
