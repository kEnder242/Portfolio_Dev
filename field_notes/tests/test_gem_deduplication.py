#!/usr/bin/env python3
"""
[Story 109.14 / FEAT-454] Unit Tests for Evidence-Aware Semantic Deduplication.
Verifies:
1. is_semantic_duplicate() collapses rephrased summaries sharing identical or overlapping raw evidence.
2. is_semantic_duplicate() respects distinct events with different evidence.
3. clean_duplicates() consolidates duplicate clusters, takes max rank, merges tags, and saves atomically.
"""

import json
import os
import sys
from pathlib import Path

FIELD_NOTES_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(FIELD_NOTES_DIR))

from nibble_v2 import is_semantic_duplicate
import clean_duplicates


def test_identical_evidence_different_summary():
    existing = [{
        "date": "2005-02-14",
        "summary": "Investigated memory board hot-add failure on Harwich system with error 0xCE.",
        "evidence": "Hot-add memory board fail with Harwich BIOS 0.90 error code 0xCE tracker 38099",
        "rank": 3,
        "tags": ["Harwich", "Memory"]
    }]

    new_event = {
        "date": "2005-02-14",
        "summary": "Tracker 38099 filed for board insertion failure encountering 0xCE post code.",
        "evidence": "Hot-add memory board fail with Harwich BIOS 0.90 error code 0xCE tracker 38099",
        "rank": 4,
        "tags": ["BIOS", "Validation"]
    }

    assert is_semantic_duplicate(new_event, existing) is True
    print("TEST_IDENTICAL_EVIDENCE_DIFFERENT_SUMMARY: PASSED")


def test_overlapping_evidence_substring_match():
    existing = [{
        "date": "2015-05-12",
        "summary": "PECI bus timeout during platform validation.",
        "evidence": "PECI command failure: timeout waiting for response from CPU socket 0 registers 0x4000",
        "rank": 3
    }]

    new_event = {
        "date": "2015-05-12",
        "summary": "Socket 0 failed to reply to PECI query.",
        "evidence": "timeout waiting for response from CPU socket 0 registers 0x4000",
        "rank": 4
    }

    assert is_semantic_duplicate(new_event, existing) is True
    print("TEST_OVERLAPPING_EVIDENCE_SUBSTRING_MATCH: PASSED")


def test_distinct_evidence_preserved():
    existing = [{
        "date": "2015-05-12",
        "summary": "PECI bus timeout during platform validation.",
        "evidence": "PECI command failure: timeout waiting for response from CPU socket 0 registers 0x4000",
        "rank": 3
    }]

    new_event = {
        "date": "2015-05-12",
        "summary": "Thermal trip observed on VRM bank 2.",
        "evidence": "VRM bank 2 telemetry exceeded 105C threshold, triggering PROCHOT assertion",
        "rank": 4
    }

    assert is_semantic_duplicate(new_event, existing) is False
    print("TEST_DISTINCT_EVIDENCE_PRESERVED: PASSED")


def test_clean_duplicates_cluster_consolidation(tmp_path, monkeypatch):
    test_json = tmp_path / "2005.json"
    raw_gems = [
        {
            "id": "GEM-001",
            "date": "2005-02-14",
            "summary": "Investigated memory board hot-add failure on Harwich system with error 0xCE.",
            "evidence": "Hot-add memory board fail with Harwich BIOS 0.90 error code 0xCE tracker 38099",
            "rank": 2,
            "tags": ["Harwich", "Memory"]
        },
        {
            "id": "GEM-002",
            "date": "2005-02-14",
            "summary": "Tracker 38099 filed for board insertion failure encountering 0xCE post code.",
            "evidence": "Hot-add memory board fail with Harwich BIOS 0.90 error code 0xCE tracker 38099",
            "rank": 4,
            "tags": ["BIOS", "Validation"]
        },
        {
            "id": "GEM-003",
            "date": "2005-02-14",
            "summary": "Memory hot add failure investigation.",
            "evidence": "Hot-add memory board fail with Harwich BIOS 0.90 error code 0xCE tracker 38099",
            "rank": 1,
            "tags": ["Memory"]
        },
        {
            "id": "GEM-004",
            "date": "2005-06-20",
            "summary": "Separate event on different date with distinct evidence.",
            "evidence": "PCIe AER root complex uncorrectable error logged on port 0x02",
            "rank": 3,
            "tags": ["PCIe"]
        }
    ]
    test_json.write_text(json.dumps(raw_gems, indent=2))

    monkeypatch.setattr(clean_duplicates, "DATA_DIR", str(tmp_path))
    clean_duplicates.clean_duplicates()

    # Load cleaned result
    cleaned = json.loads(test_json.read_text())
    assert len(cleaned) == 2, f"Expected 2 gems after deduplication, got {len(cleaned)}"

    # Check consolidated gem
    first = cleaned[0]
    assert first["date"] == "2005-02-14"
    assert first["rank"] == 4  # Promoted to max rank
    assert set(first["tags"]) == {"BIOS", "Harwich", "Memory", "Validation"}  # Merged tags
    assert "Separate event" in cleaned[1]["summary"]

    # Verify no dangling temp files
    assert not (tmp_path / "2005.json.tmp").exists()
    print("TEST_CLEAN_DUPLICATES_CLUSTER_CONSOLIDATION: PASSED")


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
