#!/usr/bin/env python3
"""Validate CEL v0 schemas and instances.

Format-only checks. No feed ingest, no actuation, no OIDF commissioning.
The identifiers under test are speakable CEL words, not HIP/CAP codes.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import jsonschema
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "core_schemas"

FORBIDDEN_INSTANCE_KEYS = {
    "evidence_requirements",
    "sat_gate",
    "sat_gates",
    "handoff_ledger",
    "canonical_deployment_object",
    "cdo",
    "required_permission",
    "catalog_id",
    "baseline_id",
}

HIP_CODE = re.compile(r"^[A-Z]{2}[0-9]{4}$")
CEL_INCIDENT = re.compile(r"^disaster(\.[a-z][a-z0-9_]*)+$")
CEL_RESPONSE = re.compile(r"^response\.[a-z][a-z0-9_]*$")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def schema_registry() -> tuple[dict[str, dict[str, Any]], Registry]:
    schemas: dict[str, dict[str, Any]] = {}
    resources: list[tuple[str, Resource]] = []
    for path in sorted(SCHEMA_DIR.glob("*.json")):
        schema = load_json(path)
        Draft202012Validator.check_schema(schema)
        schema_id = schema.get("$id", "")
        if not str(schema_id).startswith("https://openeno.dev/cel/schemas/"):
            raise ValueError(f"{path}: $id must use the OpenEno CEL namespace, got {schema_id!r}")
        schemas[path.stem] = schema
        resources.append((schema_id, Resource.from_contents(schema)))
    return schemas, Registry().with_resources(resources)


def validate_instance(instance: Any, schema: dict[str, Any], registry: Registry, path: Path) -> None:
    Draft202012Validator(schema, registry=registry).validate(instance)


def collect_keys(value: Any, found: set[str]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            found.add(str(key))
            collect_keys(child, found)
    elif isinstance(value, list):
        for child in value:
            collect_keys(child, found)


def reject_commissioning_keys(instance: Any, path: Path) -> None:
    keys: set[str] = set()
    collect_keys(instance, keys)
    hit = sorted(keys & FORBIDDEN_INSTANCE_KEYS)
    if hit:
        raise ValueError(f"{path}: commissioning keys are not allowed in CEL instances: {hit}")


def spoken_matches_code(code: str, spoken: str) -> bool:
    expected = code.replace(".", " ").replace("_", " ")
    return " ".join(spoken.split()) == expected


def taxonomy_index(taxonomy: dict[str, Any], path: Path) -> dict[str, dict[str, Any]]:
    rows = taxonomy["codes"]
    codes = {}
    for row in rows:
        code = row["code"]
        if code in codes:
            raise ValueError(f"{path}: duplicate code {code}")
        if not spoken_matches_code(code, row["spoken"]):
            raise ValueError(f"{path}: spoken {row['spoken']!r} does not match code {code}")
        if HIP_CODE.match(code):
            raise ValueError(f"{path}: CEL codes must be speakable dotted words, not HIP ids ({code})")
        codes[code] = row
    if taxonomy["root"] not in codes:
        raise ValueError(f"{path}: taxonomy root is not in codes")
    if codes[taxonomy["root"]].get("kind") != "root":
        raise ValueError(f"{path}: taxonomy root kind must be root")
    for code, row in codes.items():
        parent = row.get("parent")
        if row.get("kind") == "root":
            if parent:
                raise ValueError(f"{code}: root must not declare parent")
            continue
        if parent not in codes:
            raise ValueError(f"{code}: parent {parent!r} is missing")
        if code not in (codes[parent].get("children") or []):
            raise ValueError(f"{code}: parent {parent} does not list this child")
        if not code.startswith(parent + "."):
            raise ValueError(f"{code}: must be a dotted child of {parent}")
        hip = (row.get("profiles") or {}).get("undrr_hip")
        if hip and not HIP_CODE.match(hip):
            raise ValueError(f"{code}: invalid HIP profile {hip}")
    for code, row in codes.items():
        for child in row.get("children") or []:
            if child not in codes:
                raise ValueError(f"{code}: child {child!r} is missing")
            if codes[child].get("parent") != code:
                raise ValueError(f"{child}: parent must be {code}")
    return codes


def validate_machine(machine: dict[str, Any], codes: dict[str, dict[str, Any]], path: Path) -> None:
    state_ids = [state["id"] for state in machine["states"]]
    if len(state_ids) != len(set(state_ids)):
        raise ValueError(f"{path}: duplicate state ids")
    if machine["initial_state"] not in state_ids:
        raise ValueError(f"{path}: initial_state is not in states")
    for state in machine["states"]:
        if not CEL_RESPONSE.match(state["id"]):
            raise ValueError(f"{path}: state id {state['id']} is not a CEL response word")
        if not spoken_matches_code(state["id"], state["spoken"]):
            raise ValueError(f"{path}: spoken {state['spoken']!r} does not match {state['id']}")
        if HIP_CODE.match(state["id"]):
            raise ValueError(f"{path}: response states must not be HIP codes")
    for incident in machine["incident_types"]:
        if incident not in codes:
            raise ValueError(f"{path}: incident_types references unknown code {incident}")
        if codes[incident].get("kind") != "leaf":
            raise ValueError(f"{path}: incident_types must be taxonomy leaves, got {incident}")
        if not CEL_INCIDENT.match(incident):
            raise ValueError(f"{path}: incident_types must be CEL words, got {incident}")
    for transition in machine["transitions"]:
        if transition["from"] not in state_ids or transition["to"] not in state_ids:
            raise ValueError(f"{path}: transition {transition['id']} references an unknown state")
        if transition["from"] == transition["to"]:
            raise ValueError(f"{path}: transition {transition['id']} is a self-loop")


def validate_crosswalk(crosswalk: dict[str, Any], codes: dict[str, dict[str, Any]], path: Path) -> None:
    for rule in crosswalk["maps"]:
        cel_code = rule["cel_code"]
        if HIP_CODE.match(str(cel_code)):
            raise ValueError(f"{path}: map {rule['id']} used a HIP code as cel_code; CEL words are required")
        if cel_code not in codes:
            raise ValueError(f"{path}: map {rule['id']} references unknown code {cel_code}")
        if codes[cel_code].get("kind") != "leaf":
            raise ValueError(f"{path}: map {rule['id']} must target a leaf code")
        if str(cel_code).startswith("response."):
            raise ValueError(f"{path}: crosswalks must not assign response states")
        hip = (rule.get("profiles") or {}).get("undrr_hip")
        leaf_hip = (codes[cel_code].get("profiles") or {}).get("undrr_hip")
        if hip and leaf_hip and hip != leaf_hip and rule["confidence"] == "authoritative":
            raise ValueError(
                f"{path}: map {rule['id']} HIP {hip} does not match leaf profile {leaf_hip}"
            )


def load_crosswalks() -> list[tuple[Path, dict[str, Any]]]:
    paths = sorted((ROOT / "crosswalks").glob("*.yaml"))
    return [(path, load_yaml(path)) for path in paths]


def validate_feed_matrix(matrix: dict[str, Any], codes: dict[str, dict[str, Any]], path: Path) -> None:
    seen: set[str] = set()
    for source in matrix["sources"]:
        source_id = source["id"]
        if source_id in seen:
            raise ValueError(f"{path}: duplicate source id {source_id}")
        seen.add(source_id)
        for cel_code in source["cel_codes"]:
            if HIP_CODE.match(cel_code):
                raise ValueError(f"{path}: source {source_id} used a HIP code as cel_code")
            if cel_code not in codes:
                raise ValueError(f"{path}: source {source_id} references unknown code {cel_code}")
            if codes[cel_code].get("kind") != "leaf":
                raise ValueError(f"{path}: source {source_id} must target a leaf code ({cel_code})")


def main() -> int:
    schemas, registry = schema_registry()

    taxonomy_path = ROOT / "taxonomies" / "disasters.yaml"
    taxonomy = load_yaml(taxonomy_path)
    reject_commissioning_keys(taxonomy, taxonomy_path)
    validate_instance(taxonomy, schemas["incident_taxonomy"], registry, taxonomy_path)
    codes = taxonomy_index(taxonomy, taxonomy_path)

    machine_paths = sorted((ROOT / "response_machines").glob("*.json"))
    if not machine_paths:
        raise ValueError("no response machines found")
    for machine_path in machine_paths:
        machine = load_json(machine_path)
        reject_commissioning_keys(machine, machine_path)
        validate_instance(machine, schemas["response_machine"], registry, machine_path)
        validate_machine(machine, codes, machine_path)

    crosswalks = load_crosswalks()
    if not crosswalks:
        raise ValueError("no crosswalks found")
    for path, crosswalk in crosswalks:
        reject_commissioning_keys(crosswalk, path)
        validate_instance(crosswalk, schemas["feed_crosswalk"], registry, path)
        validate_crosswalk(crosswalk, codes, path)

    matrix_path = ROOT / "feeds" / "matrix.yaml"
    matrix = load_yaml(matrix_path)
    reject_commissioning_keys(matrix, matrix_path)
    validate_instance(matrix, schemas["feed_matrix"], registry, matrix_path)
    validate_feed_matrix(matrix, codes, matrix_path)

    print("CEL v0 artifacts validated.")
    print(f"  taxonomy codes: {len(codes)}")
    print(f"  response machines: {len(machine_paths)}")
    print(f"  crosswalk files: {len(crosswalks)}")
    print(f"  feed matrix sources: {len(matrix['sources'])}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (jsonschema.ValidationError, ValueError, OSError) as exc:
        print(f"CEL validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
