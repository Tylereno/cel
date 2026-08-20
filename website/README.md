# CEL Explorer

Static, read-only vocabulary explorer for the CEL incident taxonomy and response
machines.

## Local preview

From the repository root:

```bash
python3 website/build_snapshot.py
python3 website/build_snapshot.py --check
python3 -m http.server 8787 --directory website
```

Open <http://localhost:8787>.

`data.js` is generated from `taxonomies/disasters.yaml` and the JSON files under
`response_machines/`. Edit those source files rather than the generated snapshot.

## Boundary

The explorer is a presentation surface only. CEL names incidents and allowed
response postures; it does not ingest feeds, evaluate consumer policy, issue
alerts, or actuate equipment. The future public landing destination is
OpenEno/openeno.dev, pending a domain and visibility decision.
