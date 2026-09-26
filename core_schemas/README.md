# core_schemas — machine-readable CEL

JSON Schema Draft 2020-12 for CEL v0 artifacts. Layout follows OIDF
(`core_schemas/` as the contract surface) with **CEL semantics only**.

The schemas exist so the **same words** a human reads in the README can be
checked by a validator. They do not replace the language with HIP codes.

`$id` values use `https://tylereno.me/cel/schemas/…`, the published CEL surface.
Each identifier is a live URL that returns the schema it names, and the
[index](https://tylereno.me/cel/schemas/) and
[manifest](https://tylereno.me/cel/schemas/manifest.json) are generated from the
same scan as the schemas themselves.

That base is **frozen for v0**. An `$id` is the name implementations pin, so
moving hosts is a versioned migration, not an edit: do not change `$id` values
ad hoc. `tooling/verify_pages_ids.py` fails the build when a file and its
identifier disagree. If the OpenLexicon organization later takes over the
namespace, that is a deliberate v1 decision that aliases the v0 URLs — not a
silent rewrite.

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
