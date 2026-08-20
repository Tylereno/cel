# RFC-0001 — Scope: CEL is a language

**Status:** Accepted for CEL v0
**Spec:** 0.1.0

## One sentence

CEL is a small language that humans can speak and machines can validate:
incident words (`disaster.fire.wildland`) and response words
(`response.isolate_load`).

## Why not “just use HIP / CAP”

Those systems are real and CEL **profiles** them. They are not the language.

| Standard | Human-readable as a site language? | CEL relationship |
|---|---|---|
| CAP 1.2 alert | Partially (event text), but the contract is a message envelope | Ingest via Sentinel; crosswalk into CEL words. Do not fork CAP. |
| UNDRR HIP `EN0205` | No. Scientific identifier, 281-hazard encyclopedia | Profile on the CEL leaf. Do not make HIP the identifier crews use. |
| GDACS `EQ` / GLIDE | Short, but foreign to edge products | Crosswalk source. |
| NIMS / ICS | Human doctrine, not a state machine | Buyer docs only. |
| OIDF | Yes, but for commissioning evidence | Sibling format. Do not merge. |

The gap CEL fills is the missing **readable response layer** for automated
edge systems, plus a **readable incident layer** those machines can share
with people.

## OpenEno vs EnoTech

| Layer | What | Sold? |
|---|---|---|
| **OpenEno** | Format languages (OIDF, CEL) | No. Stewarded by Tyler Eno. Anyone may implement. |
| **EnoTech** | Products and buyer programs (Keel, Sunwave, VITO, Sentinel) | Yes, as products/programs. |

Do not add a sixth `enotech.systems` nav product until a published
normative doc **and** at least one consumer exist.

## Sibling formats (do not collapse)

| Format | Repo | Question |
|---|---|---|
| OIDF | `Tylereno/oidf` | Can this **asset** advance commissioning because the **evidence** is valid? |
| CEL | `Tylereno/cel` | What **incident** is this, and what **response state** may automated systems enter? |

Forbidden in this repository:

- SAT gates, evidence catalogs, handoff ledgers, CDO, energization sequences
- Feed polling, correlation runtime, dashboards
- A rebuilt 281-row HIP encyclopedia copied into git
- A forked CAP / EDXL schema
- Hardware BOMs and sourcing

## Response vs commissioning state

An OIDF equipment machine (Procured → Energized) and a CEL response machine
(`monitor` → `isolate_load`) are different state spaces. A site may be
OIDF-energized and CEL-`response.shelter` at the same time. Consumers must
not treat a CEL transition as commissioning evidence, or an OIDF gate as an
emergency response directive.

## Consumers

| Product | Allowed use of CEL | Must not do |
|---|---|---|
| Sentinel | Map observations to CEL incident words via `crosswalks/` | Mint new CEL words; decide actuation |
| VITO | Apply local policy that *fires* named CEL transitions | Redefine the taxonomy or machine |
| Keel / OIDF | Ignore CEL, or read it only as unrelated site context | Import CEL states into SAT / ledger semantics |
