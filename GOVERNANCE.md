# CEL governance

## Project identity

CEL is an open, speakable language for incident and response vocabulary. It is
not a feed ingestor, policy engine, dashboard product, or actuator.

The project is being prepared for stewardship under the OpenLexicon GitHub
organization. Until a repository transfer is completed, `Tylereno/cel` remains
the source repository and Tyler Eno is the provisional maintainer.

OpenLexicon is an organizational/project identity, not by itself a nonprofit or
legal entity. Legal ownership, trademark ownership, and any fiscal sponsorship
will be documented separately if established.

## Normative authority

The source-of-truth order is:

1. `core_schemas/` and normative RFCs
2. `taxonomies/`, `response_machines/`, `crosswalks/`, and `feeds/`
3. validator tests and generated explorer snapshot
4. README, examples, and hosted presentation

The hosted explorer is derived documentation. It must never become a second
semantic source of truth.

## Change classes

### Editorial

Typos, examples, accessibility, and presentation-only changes may be reviewed
by a maintainer after CI passes.

### Compatibility-preserving

Additional profiles, crosswalk entries, and clarifying descriptions require
tests and a short compatibility note.

### Semantic or breaking

Changing a primary CEL code, response state, schema requirement, or transition
requires an RFC-style issue, version impact, migration note, and explicit
maintainer approval.

No response state may be added as an implicit command. Consumers own policy
thresholds and any authorized action.

## Decision process

1. Open a proposal issue with the affected files and use case.
2. Discuss the boundary and compatibility impact.
3. Submit a focused pull request with validators and tests.
4. A maintainer approves or requests changes.
5. CI must pass before merge.

As independent maintainers and adopters join, governance may move to a
maintainer council or a separate standards entity. Until then, the project
optimizes for transparent decisions and a small review surface.

## Trademark and naming

Apache-2.0 covers copyright and patent rights for the code and specification;
it does not grant permission to use OpenLexicon or CEL trademarks. Trademark
and logo use should be documented separately once those marks are selected.
