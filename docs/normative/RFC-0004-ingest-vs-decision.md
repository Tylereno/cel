# RFC-0004 — Ingest vs decision

**Status:** Accepted for CEL v0
**Spec:** 0.1.0
**Feed matrix:** [`feeds/matrix.yaml`](../../feeds/matrix.yaml)

## Three layers

| Layer | Question it answers |
|---|---|
| **CEL** | What words do humans and machines share for this incident and this response posture? |
| **Sentinel** | What did open feeds just say, with provenance and uncertainty? |
| **VITO** | Given those observations, what should this site do or suggest? |

Sentinel **reads**. VITO **decides and suggests**. CEL **names**.

## Sentinel is a feed matrix, not a frontend

Priority for Sentinel is many important open inputs (RSS, Atom, CAP,
GeoJSON, REST), normalized onto CEL words. A map UI may consume that
matrix later. The UI is not the product.

`feeds/matrix.yaml` is the CEL-side catalog of those inputs. `ingest_status:
implemented` means Sentinel already has an adapter. `planned` means CEL
already has the word and the source — Sentinel should grow into it. v0 of
this catalog is **14/14 implemented**; key-gated feeds (FIRMS, ReliefWeb,
AirNow) skip live pull when their env vars are unset.

Do not shrink the CEL taxonomy to match today's Sentinel adapters.

## VITO is the suggestion / decision layer

CAP severity does not put a site into `response.isolate_load`. Sentinel
must not emit recommended actions or actuation. VITO (or another consumer
policy engine) binds:

- CEL incident word
- observation confidence / geometry / validity
- local policy thresholds

to a named CEL response transition.

## What stays out of CEL

- Feed polling, RSS parsers, dashboards
- Suggestion copy, paging, load-shed, breaker trips
- OIDF SAT gates
