#!/usr/bin/env python3
"""Unit checks for CEL v0 scaffold integrity."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml

from tooling import validate_cel

ROOT = Path(__file__).resolve().parents[1]


class CelV0ScaffoldTests(unittest.TestCase):
    def test_validator_accepts_checked_in_artifacts(self) -> None:
        self.assertEqual(validate_cel.main(), 0)

    def test_readme_states_openeno_stewardship_and_language(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("openeno", readme)
        self.assertIn("steward", readme)
        self.assertIn("not sold as a product", readme)
        self.assertIn("sibling", readme)
        self.assertIn("new language", readme)
        self.assertIn("disaster.fire.wildland", readme)
        self.assertIn("response.isolate_load", readme)
        self.assertIn("feed matrix", readme)
        self.assertIn("vito", readme)
        self.assertNotIn("just use hip", readme)
        self.assertNotIn("mission-scoped to sentinel-class feeds", readme)

    def test_response_machines_share_handout_states(self) -> None:
        expected_states = {
            "response.monitor",
            "response.escalate",
            "response.isolate_load",
            "response.shelter",
            "response.recover",
        }
        for name in (
            "wildland_proximity.json",
            "earthquake_proximity.json",
            "flood_proximity.json",
        ):
            machine = json.loads(
                (ROOT / "response_machines" / name).read_text(encoding="utf-8")
            )
            state_ids = {state["id"] for state in machine["states"]}
            self.assertEqual(state_ids, expected_states)
            self.assertEqual(machine["subject_kind"], "site")
            self.assertNotIn("evidence_requirements", machine)

    def test_earthquake_machine_targets_geophysical_earthquake(self) -> None:
        machine = json.loads(
            (ROOT / "response_machines" / "earthquake_proximity.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(machine["incident_types"], ["disaster.geophysical.earthquake"])

    def test_flood_machine_targets_hydrological_flood_codes(self) -> None:
        machine = json.loads(
            (ROOT / "response_machines" / "flood_proximity.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            machine["incident_types"],
            ["disaster.hydrological.flood", "disaster.hydrological.flash_flood"],
        )

    def test_response_machine_has_handout_states(self) -> None:
        machine = json.loads(
            (ROOT / "response_machines" / "wildland_proximity.json").read_text(
                encoding="utf-8"
            )
        )
        state_ids = {state["id"] for state in machine["states"]}
        self.assertEqual(
            state_ids,
            {
                "response.monitor",
                "response.escalate",
                "response.isolate_load",
                "response.shelter",
                "response.recover",
            },
        )
        self.assertEqual(machine["incident_types"], ["disaster.fire.wildland"])
        self.assertEqual(machine["subject_kind"], "site")
        self.assertNotIn("evidence_requirements", machine)

    def test_taxonomy_is_speakable_cel_not_hip(self) -> None:
        taxonomy = yaml.safe_load(
            (ROOT / "taxonomies" / "disasters.yaml").read_text(encoding="utf-8")
        )
        codes = {row["code"]: row for row in taxonomy["codes"]}
        for required in (
            "disaster.fire.wildland",
            "disaster.fire.structure",
            "disaster.geophysical.earthquake",
            "disaster.geophysical.volcano",
            "disaster.meteorological.severe_storm",
            "disaster.meteorological.tornado",
            "disaster.hydrological.flood",
            "disaster.hydrological.drought",
            "disaster.technological.dam_failure",
            "disaster.extraterrestrial.space_weather",
            "disaster.biological.disease_outbreak",
        ):
            self.assertIn(required, codes)
            self.assertTrue(
                validate_cel.spoken_matches_code(required, codes[required]["spoken"])
            )
        self.assertNotIn("response.monitor", codes)
        self.assertNotIn("GH0101", codes)
        self.assertNotIn("EN0205", codes)
        self.assertEqual(codes["disaster.geophysical.earthquake"]["profiles"]["undrr_hip"], "GH0101")
        self.assertEqual(codes["disaster.fire.wildland"]["profiles"]["undrr_hip"], "EN0205")

    def test_usgs_crosswalk_targets_cel_word(self) -> None:
        crosswalk = yaml.safe_load(
            (ROOT / "crosswalks" / "usgs_earthquake.yaml").read_text(encoding="utf-8")
        )
        targets = {rule["cel_code"] for rule in crosswalk["maps"]}
        self.assertIn("disaster.geophysical.earthquake", targets)
        self.assertTrue(all(not validate_cel.HIP_CODE.match(code) for code in targets))
        self.assertEqual(crosswalk["source"]["provider"], "usgs")
        quake = next(rule for rule in crosswalk["maps"] if rule["id"] == "usgs-type-earthquake")
        self.assertEqual(quake["profiles"]["undrr_hip"], "GH0101")

    def test_gdacs_crosswalk_targets_cel_words(self) -> None:
        crosswalk = yaml.safe_load(
            (ROOT / "crosswalks" / "gdacs_eventtype.yaml").read_text(encoding="utf-8")
        )
        by_event = {
            str(rule["match"]["equals"]): rule["cel_code"] for rule in crosswalk["maps"]
        }
        self.assertEqual(by_event["EQ"], "disaster.geophysical.earthquake")
        self.assertEqual(by_event["FL"], "disaster.hydrological.flood")
        self.assertEqual(by_event["TC"], "disaster.meteorological.tropical_cyclone")
        self.assertEqual(by_event["VO"], "disaster.geophysical.volcano")
        self.assertEqual(by_event["DR"], "disaster.hydrological.drought")

    def test_feed_matrix_names_all_implemented_sources(self) -> None:
        matrix = yaml.safe_load((ROOT / "feeds" / "matrix.yaml").read_text(encoding="utf-8"))
        by_id = {row["id"]: row for row in matrix["sources"]}
        self.assertEqual(len(by_id), 14)
        self.assertTrue(
            all(row["ingest_status"] == "implemented" for row in matrix["sources"])
        )
        self.assertEqual(by_id["usgs-earthquake-geojson"]["ingest_status"], "implemented")
        self.assertEqual(by_id["gdacs-rss"]["ingest_status"], "implemented")
        self.assertEqual(by_id["nhc-atlantic-rss"]["kind"], "rss")
        self.assertIn("disaster.extraterrestrial.space_weather", by_id["noaa-swpc-alerts"]["cel_codes"])

    def test_nws_cap_crosswalk_covers_tornado(self) -> None:
        crosswalk = yaml.safe_load(
            (ROOT / "crosswalks" / "nws_cap.yaml").read_text(encoding="utf-8")
        )
        by_event = {rule["match"]["equals"]: rule["cel_code"] for rule in crosswalk["maps"]}
        self.assertEqual(by_event["Tornado Warning"], "disaster.meteorological.tornado")
        self.assertEqual(by_event["Flash Flood Warning"], "disaster.hydrological.flash_flood")

    def test_commissioning_keys_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            validate_cel.reject_commissioning_keys(
                {"id": "x", "evidence_requirements": []},
                Path("synthetic.json"),
            )

    def test_hip_as_cel_code_is_rejected(self) -> None:
        codes = {
            "disaster.geophysical.earthquake": {
                "kind": "leaf",
                "profiles": {"undrr_hip": "GH0101"},
            }
        }
        with self.assertRaises(ValueError):
            validate_cel.validate_crosswalk(
                {
                    "maps": [
                        {
                            "id": "bad",
                            "cel_code": "GH0101",
                            "confidence": "authoritative",
                            "profiles": {},
                        }
                    ]
                },
                codes,
                Path("synthetic.yaml"),
            )


if __name__ == "__main__":
    unittest.main()
