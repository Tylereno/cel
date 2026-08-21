# CEL — Core Emergency Language

**CEL is an OpenLexicon language.** Humans and machines share the same words.

You can say `disaster.fire.wildland` out loud. A schema can validate it. A
site can sit in `response.isolate_load` without anyone translating
`EN0205` or a CAP XML blob first.

Stewarded by [Tyler Eno](https://tylereno.me/). Anyone may implement it.
**CEL is not sold as a product.**

Target stewardship: the `OpenLexicon` GitHub organization and a public
OpenLexicon documentation host selected by the founder. Until the repository
transfer is complete, this repository (`Tylereno/cel`) remains the source of
truth.

## Layers (do not collapse)

| Layer | Owns | Does not own |
|---|---|---|
| **CEL** | Incident words + response words | Ingest, UI, actuation |
| **Sentinel** | Observation matrix (RSS / Atom / CAP / GeoJSON / REST) | Decisions, suggestions, dashboards-as-product |
| **VITO** | Local decisions and suggestions from those observations | Minting CEL words; becoming a feed scraper |

```
many open feeds (RSS / CAP / GeoJSON)
        ↓ Sentinel (read, normalize, provenance)
CEL words: disaster.geophysical.earthquake
        ↓ VITO (policy, suggestions, optional actuation)
CEL words: response.monitor → response.escalate → response.isolate_load
```

Sentinel's current adapters are **not** the language ceiling. CEL names
disasters Sentinel should grow into. Sentinel should grow as a **feed matrix**,
not as a frontend project. VITO is the layer that decides and suggests.

## Why a new language

Alert formats and hazard encyclopedias already exist. They do not replace CEL.

| Existing standard | What it is | Why it is not CEL |
|---|---|---|
| **CAP 1.2** | Alert *message* | A payload, not a site language |
| **UNDRR–ISC HIPs** | 281-hazard scientific taxonomy | Profile on a CEL leaf; not the crew identifier |
| **GDACS / GLIDE / EM-DAT** | Feed and loss-database codes | Crosswalk source |
| **NIMS / ICS** | Human operations doctrine | Buyer language, not a JSON state machine |
| **OIDF** | Commissioning *evidence* states | Different question (see below) |

## Sibling of OIDF, not a part of it

| Question | Language |
|---|---|
| Can this **asset** advance commissioning because the **evidence** is valid? | **OIDF** |
| What **incident** is this, and what **response state** may automated systems enter? | **CEL** |

## Repository map

```
cel/
  taxonomies/              # the CEL incident words
  feeds/matrix.yaml        # sources Sentinel should ingest
  response_machines/       # the CEL response words + allowed transitions
  crosswalks/              # USGS / GDACS / NWS CAP / HIP → CEL
  core_schemas/            # JSON Schema (OIDF-shaped layout, CEL semantics)
  website/                 # read-only incident + response vocabulary explorer
  docs/normative/
```

HIP codes appear as *profiles on CEL leaves*, not as the identifiers crews
use. The taxonomy is speakable English, not a 281-row dump, and not clipped
to whatever Sentinel happens to poll this week.

### Incident words (excerpt)

```
disaster
├── fire.wildland / structure / industrial
├── geophysical.earthquake / tsunami / volcano / landslide
├── meteorological.severe_storm / tropical_cyclone / tornado / …
├── hydrological.flood / flash_flood / drought / …
├── environmental.smoke / air_quality
├── technological.dam_failure / hazmat / explosion / nuclear
├── extraterrestrial.space_weather
└── biological.disease_outbreak
```

See [`taxonomies/disasters.yaml`](./taxonomies/disasters.yaml) for the full
tree. See [`feeds/matrix.yaml`](./feeds/matrix.yaml) for the ingest matrix.

The [`website/`](./website/) directory contains a static, read-only explorer for
the incident taxonomy and response machines. It is a presentation surface, not a
runtime or policy engine.

### Response words (separate dimension)

v0 states: `monitor`, `escalate`, `isolate_load`, `shelter`, `recover`.
CAP urgency/severity/certainty describe an alert. They are not these states.

## What this repo does not contain

- Runtime, ingest, or dashboards (Sentinel / VITO)
- Commissioning SAT gates (OIDF + Keel)
- A copy of the UNDRR HIP tree or a forked CAP schema
- A runtime implementation or policy engine

## Public explorer and hosting

The [`website/`](./website/) directory is a generated-data, read-only explorer.
The future public host should deploy only the four explorer assets
(`index.html`, `styles.css`, `app.js`, and generated `data.js`) through GitHub
Pages. The source files, validators, and private operational material must not
be published as site content.

The Enotech site may link to the explorer as a company-facing presentation, but
the canonical source and contribution flow belong in this repository after the
OpenLexicon transfer.

## Contributing

Start with [`CONTRIBUTING.md`](./CONTRIBUTING.md), [`GOVERNANCE.md`](./GOVERNANCE.md),
and the pull request template. Proposals must keep CEL separate from Sentinel
ingest, consumer policy, OIDF commissioning, and actuation.

## Validate locally

```bash
python3 -m pip install "jsonschema>=4.0" "pyyaml>=6.0"
python3 tooling/validate_cel.py
python3 -m unittest tooling.test_cel_v0 -v
```

## License

Apache 2.0 — see [`LICENSE`](./LICENSE). Contributions are accepted under the
Apache-2.0 terms with DCO sign-off; there is no CLA at this stage.
