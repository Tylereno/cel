# core_schemas — machine-readable CEL

JSON Schema Draft 2020-12 for CEL v0 artifacts. Layout follows OIDF
(`core_schemas/` as the contract surface) with **CEL semantics only**.

The schemas exist so the **same words** a human reads in the README can be
checked by a validator. They do not replace the language with HIP codes.

`$id` values currently use `https://openeno.dev/cel/schemas/…` as the legacy v0
namespace. The OpenLexicon host and any namespace migration are not selected
yet; do not change `$id` values ad hoc. That host is not a live HTTP registry
in v0. Pin this git commit (or a future annotated tag) rather than fetching
schemas by URL.

| File | Role |
|---|---|
| [`incident_taxonomy.json`](./incident_taxonomy.json) | Speakable incident catalogs (`taxonomies/*.yaml`) |
| [`response_state.json`](./response_state.json) | One response-state vocabulary entry |
| [`response_machine.json`](./response_machine.json) | Emergency response FSMs (`response_machines/*.json`) |
| [`feed_crosswalk.json`](./feed_crosswalk.json) | External feed → CEL word maps (`crosswalks/*.yaml`) |
| [`feed_matrix.json`](./feed_matrix.json) | Ingest source catalog (`feeds/matrix.yaml`) |

**Spec:** CEL `0.1.0` (lab)

These schemas MUST NOT describe commissioning evidence, SAT gates, handoff
ledgers, CDOs, or equipment energization. Those contracts live in
[`Tylereno/oidf`](https://github.com/Tylereno/oidf).

They MUST NOT copy OASIS CAP or the UNDRR HIP SKOS graph. Profile those
systems in `crosswalks/` and optional `profiles` fields.
