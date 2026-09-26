# OpenLexicon organization setup

This is an operational checklist for moving CEL under the new GitHub
organization. Creating a GitHub organization does not create a nonprofit or
transfer copyright by itself.

## Founder actions in GitHub

1. Create the public organization profile repository:
   `OpenLexicon/.github`.
2. Add the organization profile README from
   [`OPENLEXICON-ORG-PROFILE.md`](./OPENLEXICON-ORG-PROFILE.md).
3. Transfer `Tylereno/cel` to `OpenLexicon/cel`, or rename the canonical public
   repository if the transfer UI presents that option.
4. Keep issues, pull requests, releases, and history during the transfer.
5. Configure public repository settings:
   - protect `main`;
   - require pull request review and passing CI;
   - enable Discussions;
   - enable private vulnerability reporting;
   - keep Actions permissions at least privilege.
6. Set the Pages source to GitHub Actions and attach the selected OpenLexicon
   domain only after DNS and TLS are ready. Pages is **already enabled** on
   `Tylereno/cel` (Actions source) and serves <https://tylereno.me/cel/>, a
   free subpath of an already-owned domain. Two account facts to carry over: a
   Pages project path follows the repository name, and Pages paths are
   **case-sensitive** — which is why the repository is lowercase `cel` while its
   `$id` base is `/cel/`.
7. Add an `@OpenLexicon/maintainers` team and update `CODEOWNERS` after the
   team exists.

## Before transfer

- Confirm copyright ownership and any assignment needed from Tyler Eno or
  EnoTech.
- Confirm the OpenLexicon and CEL trademark policy with counsel.
- Review repository history for secrets, private URLs, customer data, and
  deployment details.
- Decide whether the current `openeno.dev` v0 schema namespace remains a
  legacy identifier or receives a versioned migration. **Settled 2026-09-26:**
  `openeno.dev` is a dead host, so identifiers now resolve at
  `https://tylereno.me/cel/schemas/…` and that base is frozen for v0. An
  OpenLexicon namespace is a versioned v1 migration with v0 URLs aliased, never
  an in-place rewrite of `$id` values.

## Canonical source rule

OpenLexicon/CEL should own the schemas, taxonomy, response machines,
crosswalks, validators, and generated explorer data. EnoTech may link to or
mirror the explorer for company-facing discovery, but it must not become a
second manually edited source.

## Funding decision

Do not form a nonprofit merely to publish CEL. Revisit fiscal sponsorship or a
separate nonprofit/standards entity only when the project has external
maintainers, funding, or a public governance requirement that justifies the
administrative cost.
