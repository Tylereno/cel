# Normative CEL contracts

**Ownership:** OpenEno format steward (Tyler Eno)
**Role:** Human-readable contracts for the Core Emergency Language
**Spec:** CEL v0.1.0 (lab)

CEL is a **new language**. The words in `taxonomies/` and
`response_machines/` are the language. Existing standards are **profiled**,
not substituted.

Machine-readable schemas: [`../../core_schemas/`](../../core_schemas/).
Incident words: [`../../taxonomies/`](../../taxonomies/).
Response machines: [`../../response_machines/`](../../response_machines/).
Feed maps: [`../../crosswalks/`](../../crosswalks/).

CEL is an OpenEno language. It is **not** an EnoTech product SKU and **not**
a module of OIDF.

## Index

| Document | Title |
|---|---|
| [RFC-0001-scope.md](./RFC-0001-scope.md) | Language vs CAP/HIP/OIDF; what CEL is for |
| [RFC-0002-incident-taxonomy.md](./RFC-0002-incident-taxonomy.md) | Speakable incident words |
| [RFC-0003-response-machines.md](./RFC-0003-response-machines.md) | Speakable response states and transitions |

## v0 artifacts

| Artifact | Role |
|---|---|
| [`taxonomies/disasters.yaml`](../../taxonomies/disasters.yaml) | CEL incident language (finite) |
| [`response_machines/wildland_proximity.json`](../../response_machines/wildland_proximity.json) | First response FSM |
| [`crosswalks/usgs_earthquake.yaml`](../../crosswalks/usgs_earthquake.yaml) | USGS / CAP → CEL |
| [`crosswalks/gdacs_eventtype.yaml`](../../crosswalks/gdacs_eventtype.yaml) | GDACS → CEL (with HIP profile) |

No runtime belongs in this repository. Sentinel consumes CEL words; VITO may
apply policy; neither mints CEL identifiers here.
