# RFC-0002 — Incident taxonomy (the CEL words)

**Status:** Accepted for CEL v0
**Spec:** 0.1.0
**Schema:** [`core_schemas/incident_taxonomy.json`](../../core_schemas/incident_taxonomy.json)
**Instance:** [`taxonomies/disasters.yaml`](../../taxonomies/disasters.yaml)

## The language is dotted English

Incident codes are dotted paths a person can read without a lookup table.

```
disaster
├── fire
│   ├── wildland
│   └── structure
├── geophysical
│   ├── earthquake
│   └── tsunami
├── meteorological
│   ├── severe_storm
│   ├── tropical_cyclone
│   └── extreme_heat
└── hydrological
    └── flood
```

`disaster.fire.wildland` is both the identifier and the sentence. That is
the point of CEL. HIP `EN0205` may be recorded on the leaf as a *profile*
so Sentinel can interoperate. It is not the CEL word.

v0 stays finite and mission-scoped (USGS, WFIGS/FIRMS-class fire, GDACS,
NWS-class weather). Do not grow this into a global all-hazards ontology.

## Rules

1. Every non-root code has exactly one `parent`.
2. `children` on a parent MUST match codes that declare that parent.
3. Leaf codes are the values crosswalks MAY emit as `cel_code`.
4. Incident type is **not** a response state. Do not encode `monitor` or
   `shelter` in the taxonomy.
5. Optional `profiles` (UNDRR HIP, GLIDE, CAP event) are aliases for
   implementers. They never replace `code`.
6. Sentinel `hazard_type` strings (`earthquake`, `wildfire`, …) are
   observations. They become CEL words only through `crosswalks/`.
