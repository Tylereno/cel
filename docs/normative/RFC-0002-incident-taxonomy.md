# RFC-0002 — Incident taxonomy (the CEL words)

**Status:** Accepted for CEL v0
**Spec:** 0.1.0
**Schema:** [`core_schemas/incident_taxonomy.json`](../../core_schemas/incident_taxonomy.json)
**Instance:** [`taxonomies/disasters.yaml`](../../taxonomies/disasters.yaml)
**Ingest catalog:** [`feeds/matrix.yaml`](../../feeds/matrix.yaml)

## The language is dotted English

Incident codes are dotted paths a person can read without a lookup table.
The tree covers disasters Sentinel **should** ingest, not only the adapters
that exist today.

```
disaster
├── fire (wildland, structure, industrial)
├── geophysical (earthquake, tsunami, volcano, landslide)
├── meteorological (severe_storm, tropical_cyclone, tornado,
│                   extreme_heat, extreme_cold, winter_storm, high_wind)
├── hydrological (flood, flash_flood, coastal_flood, storm_surge,
│                 drought, avalanche)
├── environmental (smoke, air_quality)
├── technological (dam_failure, hazmat, explosion, nuclear)
├── extraterrestrial (space_weather)
└── biological (disease_outbreak)
```

`disaster.fire.wildland` is both the identifier and the sentence. HIP
`EN0205` may be recorded on the leaf as a *profile*. It is not the CEL word.

This is not a 281-row HIP encyclopedia (no per-disease HIP dump). It is
also not clipped to USGS + WFIGS + NWS. Add a leaf when a real ingest
source needs a speakable word. Do not wait for a Sentinel UI mockup.

## Rules

1. Every non-root code has exactly one `parent`.
2. `children` on a parent MUST match codes that declare that parent.
3. Leaf codes are the values crosswalks and the feed matrix MAY emit.
4. Incident type is **not** a response state.
5. Optional `profiles` never replace `code`.
6. Sentinel observations become CEL words only through `crosswalks/`.
