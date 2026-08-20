# RFC-0003 — Response machines (the CEL words)

**Status:** Accepted for CEL v0
**Spec:** 0.1.0
**Schema:** [`core_schemas/response_machine.json`](../../core_schemas/response_machine.json)
**State schema:** [`core_schemas/response_state.json`](../../core_schemas/response_state.json)
**Instance:** [`response_machines/`](../../response_machines/) (wildland, earthquake, flood)

## Separate dimension

Response state is independent of incident type. CEL names the **allowed**
states and transitions in the same speakable dialect as the taxonomy.
Consumers decide **when** a named event fires.

v0 states (always prefixed `response.`):

| State | Spoken | Meaning |
|---|---|---|
| `response.monitor` | response monitor | Watch the incident; no extra posture implied |
| `response.escalate` | response escalate | Elevated attention; review / notify per policy |
| `response.isolate_load` | response isolate load | Non-life-safety load isolation is an allowed posture |
| `response.shelter` | response shelter | Life-safety / shelter posture |
| `response.recover` | response recover | Hazard receding; return path toward monitor |

CAP urgency/severity/certainty describe an **alert**. They are not these
states. A “Severe” CAP message does not put a site into
`response.isolate_load`. Consumer policy does.

## Transition vocabulary

Each edge has a stable `event` id (for example
`wildland.proximity_detected`). Events are names, not actuators. CEL does
not shed load, page crews, or trip breakers.

## What a machine must not contain

- `evidence_requirements`, SAT gates, or commissioning permissions
- Distance, acreage, or magnitude thresholds (those are consumer policy)
- Sentinel feed URLs or polling intervals
- HIP or CAP identifiers as the state names

The first v0 machine is **wildland proximity** bound to
`disaster.fire.wildland`. Additional v0 machines reuse the same response
states for earthquake and flood:

| Machine | Incident types |
|---|---|
| [`wildland_proximity.json`](../../response_machines/wildland_proximity.json) | `disaster.fire.wildland` |
| [`earthquake_proximity.json`](../../response_machines/earthquake_proximity.json) | `disaster.geophysical.earthquake` |
| [`flood_proximity.json`](../../response_machines/flood_proximity.json) | `disaster.hydrological.flood`, `disaster.hydrological.flash_flood` |
