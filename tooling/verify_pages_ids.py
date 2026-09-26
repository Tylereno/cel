#!/usr/bin/env python3
"""Verify the published CEL identifier mapping.

A published `$id` is a promise: dereference it and you get that document. This
gate checks, before publication, that

  1. every `$id` under core_schemas/ is exactly BASE + the path we serve it from,
  2. every `$ref` naming BASE resolves to a schema this repository serves, and
  3. with --public, the staged artifact really contains a file per identifier
     and every internal link on the landing page lands on a staged file
     (Pages serves no directory listing, so a missing file is a 404 rather than
     a redirect, and the identifier silently stops resembling a URL).

Stdlib only. Exit status is the gate: non-zero fails the build.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

BASE = "https://tylereno.me/cel/schemas/"
SERVED_PREFIX = "schemas/"
ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "core_schemas"

EXTERNAL_HREF = ("http://", "https://", "mailto:", "data:", "#", "/", "..")


def served_path(path: Path) -> str:
    """Repository path -> its path relative to BASE."""
    return path.relative_to(SCHEMA_DIR).as_posix()


def walk_refs(node, found: list[str]) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "$ref" and isinstance(value, str):
                found.append(value)
            else:
                walk_refs(value, found)
    elif isinstance(node, list):
        for item in node:
            walk_refs(item, found)


def check_landing(artefact: Path, failures: list[str]) -> int:
    landing = artefact / "index.html"
    if not landing.is_file():
        failures.append("index.html: missing from the staged artifact")
        return 0
    checked = 0
    for href in re.findall(r'href="([^"]+)"', landing.read_text(encoding="utf-8")):
        if href.startswith(EXTERNAL_HREF):
            continue
        checked += 1
        target = artefact / href
        ok = target.is_file() or (href.endswith("/") and target.is_dir())
        if not ok:
            failures.append(f"index.html: link {href!r} has no file in the staged artifact")
    return checked


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public", help="staged artifact directory to check on disk")
    args = parser.parse_args()

    if not SCHEMA_DIR.is_dir():
        print(f"refusing to run: {SCHEMA_DIR} is missing", file=sys.stderr)
        return 2

    failures: list[str] = []
    published: list[tuple[str, str]] = []

    for path in sorted(SCHEMA_DIR.rglob("*.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        rel = path.relative_to(ROOT).as_posix()
        schema_id = document.get("$id")
        want = BASE + served_path(path)
        if schema_id != want:
            failures.append(f"{rel}: $id is {schema_id!r}, should be {want!r}")
        else:
            published.append((served_path(path), want))

        refs: list[str] = []
        walk_refs(document, refs)
        for ref in refs:
            if not ref.startswith(BASE):
                continue
            if not (SCHEMA_DIR / ref[len(BASE):]).is_file():
                failures.append(
                    f"{rel}: $ref {ref!r} has no schema at core_schemas/{ref[len(BASE):]}"
                )

    print(f"published identifiers: {len(published)}")
    for rel, schema_id in sorted(published):
        print(f"  {SERVED_PREFIX}{rel} -> {schema_id}")

    if args.public:
        artefact = Path(args.public)
        for rel, _ in sorted(published):
            if not (artefact / SERVED_PREFIX / rel).is_file():
                failures.append(f"{SERVED_PREFIX}{rel}: not present in the staged artifact")
        for extra in ("LICENSE", "index.html", "schemas/index.html", "schemas/manifest.json"):
            if not (artefact / extra).is_file():
                failures.append(f"{extra}: missing from the staged artifact")
        links = check_landing(artefact, failures)
        print(f"landing links checked: {links}")

    print(f"\nFAIL {len(failures)}")
    for failure in failures:
        print(f"  FAIL {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
