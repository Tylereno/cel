## Summary

## Contract impact

- [ ] Touches `core_schemas/`
- [ ] Touches `taxonomies/`, `response_machines/`, or `crosswalks/`
- [ ] Touches normative docs
- [ ] Touches validation tooling
- [ ] Docs-only

## Boundary

- [ ] No OIDF commissioning SAT / ledger / evidence semantics were added
- [ ] No ingest runtime, dashboard, or actuation logic was added
- [ ] CEL remains a sibling of OIDF (not a submodule or merged vocabulary)
- [ ] Primary identifiers stay speakable CEL words (`disaster.*`, `response.*`), not HIP/CAP codes

## Validation

- [ ] `python3 tooling/validate_cel.py`
- [ ] `python3 -m unittest tooling.test_cel_v0 -v`
- [ ] `python3 website/build_snapshot.py --check`
- [ ] `node --check website/app.js`

## Contribution agreement

- [ ] Commits are signed off under the DCO (`Signed-off-by`)
- [ ] Generated `website/data.js` is current
- [ ] No secrets, customer data, live coordinates, or unredacted operational payloads were added
