# CEL — Core Emergency Language

**CEL is an OpenEno language.** Humans and machines share the same words.

You can say `disaster.fire.wildland` out loud. A schema can validate it. A
site can sit in `response.isolate_load` without anyone translating
`EN0205` or a CAP XML blob first.

Stewarded by [Tyler Eno](https://tylereno.me/). Anyone may implement it.
**CEL is not sold as a product.**

Planned landing: `openeno.dev` and an `openeno` GitHub org. Until that move,
this repository (`Tylereno/cel`) is the format source of truth.

## Why a new language

Alert formats and hazard encyclopedias already exist. They do not replace CEL.

| Existing standard | What it is | Why it is not CEL |
|---|---|---|
| **CAP 1.2** | Alert *message* (event, urgency, severity, certainty, area) | A payload about an observation, not a site response language |
| **UNDRR–ISC HIPs** | 281-hazard scientific taxonomy (`GH0101`, `EN0205`) | Canonical for research/interop; not speakable crew/edge vocabulary |
| **GDACS / GLIDE / EM-DAT** | Feed and loss-database codes | What those systems return; not what a VITO node should display as truth |
| **NIMS / ICS** | Human operations doctrine | Buyer language, not a JSON state machine |
| **OIDF** | Commissioning *evidence* states | Different question (see below) |

CEL is the gap those pieces leave: a **small, readable language** for
incident type + automated **response state**, with **crosswalks** into the
standards above.

```
USGS / CAP / GDACS observation
        ↓ crosswalks/
CEL words: disaster.geophysical.earthquake
        ↓ response_machines/
CEL words: response.monitor → response.escalate → response.isolate_load
        ↓ consumer policy (not CEL)
VITO may actuate; Sentinel never does
```

## Sibling of OIDF, not a part of it

CEL and [OIDF](https://github.com/Tylereno/oidf) are sibling OpenEno languages.
Same *shape* (vocabulary + state machine + JSON Schema). Different *domain*.
**Do not merge them.**

| Question | Language |
|---|---|
| Can this **asset** advance commissioning because the **evidence** is valid? | **OIDF** |
| What **incident** is this, and what **response state** may automated systems enter? | **CEL** |

Commissioning SAT gates, handoff ledgers, and energization evidence stay in
OIDF and [Keel](https://github.com/Tylereno/keel).

## v0 scope (finite, speakable)

```
cel/
  README.md
  docs/normative/          # human-readable contracts
  core_schemas/            # JSON Schema (OIDF-shaped layout, CEL semantics)
  taxonomies/              # the CEL incident words
  response_machines/       # the CEL response words + allowed transitions
  crosswalks/              # USGS / GDACS / CAP / HIP → CEL
  tooling/                 # schema + instance validation
```

v0 is mission-scoped to Sentinel-class feeds. It is **not** a 281-hazard
encyclopedia. HIP codes appear as *profiles on CEL leaves*, not as the
identifiers crews use.

### Incident words

```
disaster
├── fire.wildland
├── fire.structure
├── geophysical.earthquake
├── meteorological.severe_storm
└── hydrological.flood
```

### Response words (separate dimension)

A site may be `response.monitor` during `disaster.fire.wildland` proximity
and transition to `response.isolate_load` when **consumer policy** (not CEL)
says the threshold is met.

v0 states: `monitor`, `escalate`, `isolate_load`, `shelter`, `recover`.

## What this repo does not contain

- Runtime, ingest, correlation, or dashboards ([Sentinel](https://github.com/Tylereno/sentinel) / [VITO](https://github.com/Tylereno/ark-node))
- Commissioning SAT gates or equipment evidence (OIDF + Keel)
- A copy of the UNDRR HIP tree or a CAP message schema
- Hardware BOMs (Sunwave)
- A public `enotech.systems` nav item

## Consumers (later, not in this repo)

- **Sentinel** — maps open-feed observations to CEL incident words
- **VITO** — optional local policy on CEL response words
- **OIDF / Keel** — unchanged; commissioning only

## Validate locally

```bash
python3 -m pip install "jsonschema>=4.0" "pyyaml>=6.0"
python3 tooling/validate_cel.py
python3 -m unittest tooling.test_cel_v0 -v
```

## License

Apache 2.0 — see [`LICENSE`](./LICENSE). Repo remains **private** until the
founder flips visibility.
