#!/usr/bin/env python3
"""Re-point CEL identifiers from the planned host to the host that serves them.

Every `$id` in core_schemas/ named a planned host (`openeno.dev`) that does not
resolve, so no identifier in this repository could be dereferenced. GitHub Pages
serves this repository at https://tylereno.me/cel/, so the published identifiers
must name that host.

Only scheme'd URLs are rewritten. Bare host mentions in prose are reported for a
human to fix: a blind substring replace leaves prose asserting a host that no
longer serves the format.

Dry run by default; pass --apply to write.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

OLD = "https://openeno.dev/cel"
NEW = "https://tylereno.me/cel"

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__", "public"}
TEXT_SUFFIXES = {".json", ".md", ".py", ".yaml", ".yml", ".html"}
BARE_MARKERS = ("openeno.dev", "openeno.github.io", "openeno.io")


def iter_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.resolve() == SELF:
            continue  # never rewrite this script's own OLD/NEW constants
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="write changes (default: dry run)")
    parser.add_argument("--old", default=OLD)
    parser.add_argument("--new", default=NEW)
    args = parser.parse_args()

    if not (ROOT / "core_schemas").is_dir():
        print(f"refusing to run: {ROOT} does not look like the CEL repo root", file=sys.stderr)
        return 2

    changed = 0
    manual = 0
    for path in iter_files(ROOT):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT).as_posix()
        hits = text.count(args.old)
        if hits:
            changed += 1
            print(f"{'rewrite    ' if args.apply else 'would write'} {rel}: {hits} occurrence(s)")
            if args.apply:
                path.write_text(text.replace(args.old, args.new), encoding="utf-8")
            text = text.replace(args.old, args.new)
        for marker in BARE_MARKERS:
            if marker in text:
                manual += 1
                print(f"  MANUAL     {rel}: prose still mentions {marker!r}")

    verb = "rewritten" if args.apply else "to rewrite"
    print(f"\n{changed} file(s) {verb}; {manual} prose mention(s) need a human")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
