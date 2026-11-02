#!/usr/bin/env python3
"""
[FEAT-683] / [Story 109.10] Unit Tests for Gem Refiner Spatial Anchors & Chronology Excision.

Verifies:
1. resolve_gem_anchors() provides spatial_anchor and temporal_anchor schema.
2. Pre-2020 legacy gems NEVER receive 2024 or 06-01 guessing defaults.
3. Spatial lookup correctly associates line ranges with .map.json companion file.
4. Backward-compatible disentangle_chronology() wrapper functions without error.
"""

import sys
from pathlib import Path

FIELD_NOTES_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(FIELD_NOTES_DIR))

from refine_gem import resolve_gem_anchors, disentangle_chronology


def test_spatial_anchor_schema():
    gem = {
        "id": "GEM-001",
        "date": "2007-04-15",
        "summary": "ESB2 FW sustaining fix for Fox Cove network issue",
        "evidence": "Debugged network packets on Fox Cove",
        "line_start": 42,
        "line_end": 65,
        "source_file": "notes_2007_LAD.txt"
    }
    res = resolve_gem_anchors(gem)

    # Check spatial anchor
    assert "spatial_anchor" in res
    assert res["spatial_anchor"]["source_file"] == "notes_2007_LAD.txt"
    assert res["spatial_anchor"]["line_start"] == 42
    assert res["spatial_anchor"]["line_end"] == 65

    # Check temporal anchor
    assert "temporal_anchor" in res
    assert res["temporal_anchor"]["year"] == 2007
    assert res["temporal_anchor"]["era"] == "2007-04-15"
    assert res["temporal_anchor"]["quarter"] == "2007-Q2"
    assert res["temporal_anchor"]["precision"] == "EXACT"

    # Zero hallucinated 2024 or 06-01
    assert res["event_year"] == 2007
    assert res["event_year"] != 2024
    assert not res["event_era"].endswith("06-01")
    print("TEST_SPATIAL_ANCHOR_SCHEMA: PASSED")


def test_no_guessing_defaults_on_pre_2020_gems():
    test_cases = [
        {"file": "notes_2005_SSPD.txt", "date": "", "year": 2005},
        {"file": "notes_2006_EPSD.txt", "date": "2006-08-20", "year": 2006},
        {"file": "notes_2007_LAD.txt", "date": "", "year": 2007},
        {"file": "notes_2015_DSD.txt", "date": "2015-02-10", "year": 2015},
    ]

    for tc in test_cases:
        gem = {
            "source_file": tc["file"],
            "date": tc["date"],
            "summary": "Hardware triage and bring-up",
            "evidence": "Observed bus parity check"
        }
        res = resolve_gem_anchors(gem)
        assert res["event_year"] == tc["year"], f"Expected {tc['year']}, got {res['event_year']} for {tc['file']}"
        assert res["event_year"] != 2024, f"Hazardous 2024 fallback triggered for {tc['file']}"
        assert not str(res["event_era"]).endswith("-06-01"), f"Hazardous 06-01 fallback triggered: {res['event_era']}"
    print("TEST_NO_GUESSING_DEFAULTS_ON_PRE_2020_GEMS: PASSED")


def test_companion_map_integration():
    # notes_2005_SSPD.map.json exists and covers line 1-2700
    gem = {
        "source_file": "notes_2005_SSPD.txt",
        "line_start": 10,
        "line_end": 20,
        "summary": "SSPD initial test setup",
    }
    res = resolve_gem_anchors(gem)
    assert res["temporal_provenance"] == "companion_map"
    assert res["event_year"] == 2005
    assert res["event_quarter"] == "2005-Q1"
    print("TEST_COMPANION_MAP_INTEGRATION: PASSED")


def test_disentangle_chronology_wrapper():
    res = disentangle_chronology("Debug notes from 2006-11-04", "2006-11-04")
    assert res["event_year"] == 2006
    assert res["event_year"] != 2024
    print("TEST_DISENTANGLE_CHRONOLOGY_WRAPPER: PASSED")


if __name__ == "__main__":
    test_spatial_anchor_schema()
    test_no_guessing_defaults_on_pre_2020_gems()
    test_companion_map_integration()
    test_disentangle_chronology_wrapper()
    print("ALL GEM REFINER TESTS PASSED")
