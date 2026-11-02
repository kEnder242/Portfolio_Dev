#!/usr/bin/env python3
"""
[FEAT-682] / [Story 109.8] Unit Tests for Density-Weighted Archive Queue Scheduler.

Verifies:
1. calculate_file_priorities() computes Priority = max(0.001, lines / (gems + 1)).
2. Empty files (0 lines) return floor priority 0.001 (preventing starvation).
3. Files with high lines and low/zero gems rank higher than saturated files.
4. Output is sorted descending by priority.
"""

import sys
import tempfile
import json
from pathlib import Path

# Add field_notes to path
FIELD_NOTES_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(FIELD_NOTES_DIR))

from scan_queue import calculate_file_priorities


def test_calculate_file_priorities_synthetic():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        raw_dir = temp_path / "raw"
        data_dir = temp_path / "data"
        raw_dir.mkdir()
        data_dir.mkdir()

        # 1. Create a large, unindexed gap file (1000 lines, 0 gems)
        gap_file = raw_dir / "notes_2005_SSPD.txt"
        gap_file.write_text("\n".join([f"Line {i}: test log entry" for i in range(1000)]))

        # 2. Create a saturated file (2000 lines, 100 gems in data/2024.json)
        sat_file = raw_dir / "notes_2024_PIAV.txt"
        sat_file.write_text("\n".join([f"Line {i}: test log entry" for i in range(2000)]))
        with open(data_dir / "2024.json", "w") as f:
            json.dump([{"id": f"gem_{i}", "source_file": "notes_2024_PIAV.txt"} for i in range(100)], f)

        # 3. Create an empty file (0 lines)
        empty_file = raw_dir / "notes_empty.txt"
        empty_file.write_text("")

        # 4. Create a moderate file (500 lines, 5 gems in chunk_state.json)
        mod_file = raw_dir / "notes_2007_LAD.txt"
        mod_file.write_text("\n".join([f"Line {i}: test log entry" for i in range(500)]))
        with open(data_dir / "chunk_state.json", "w") as f:
            state = {f"notes_2007_LAD.txt::bucket_{i}": f"hash_{i}" for i in range(5)}
            json.dump(state, f)

        priorities = calculate_file_priorities(raw_notes_dir=str(raw_dir), data_dir=str(data_dir))

        assert len(priorities) == 4, f"Expected 4 files, got {len(priorities)}"

        # Check keys
        for p in priorities:
            assert "filename" in p
            assert "lines" in p
            assert "gems" in p
            assert "priority" in p

        # Check sorted descending
        for i in range(len(priorities) - 1):
            assert priorities[i]["priority"] >= priorities[i + 1]["priority"], (
                f"Priority ordering failure: {priorities[i]} < {priorities[i+1]}"
            )

        p_map = {p["filename"]: p for p in priorities}

        # Empty file priority must be floor epsilon 0.001
        assert p_map["notes_empty.txt"]["lines"] == 0
        assert p_map["notes_empty.txt"]["priority"] == 0.001, (
            f"Expected epsilon floor 0.001, got {p_map['notes_empty.txt']['priority']}"
        )

        # Gap file (1000 lines, 0 gems) priority: 1000 / (0 + 1) = 1000.0
        assert p_map["notes_2005_SSPD.txt"]["lines"] == 1000
        assert p_map["notes_2005_SSPD.txt"]["gems"] == 0
        assert p_map["notes_2005_SSPD.txt"]["priority"] == 1000.0

        # Saturated file (2000 lines, 100 gems) priority: 2000 / (100 + 1) ~ 19.802
        assert p_map["notes_2024_PIAV.txt"]["lines"] == 2000
        assert p_map["notes_2024_PIAV.txt"]["gems"] == 100
        assert round(p_map["notes_2024_PIAV.txt"]["priority"], 2) == 19.80

        # Moderate file (500 lines, 5 gems) priority: 500 / (5 + 1) ~ 83.333
        assert p_map["notes_2007_LAD.txt"]["lines"] == 500
        assert p_map["notes_2007_LAD.txt"]["gems"] == 5
        assert round(p_map["notes_2007_LAD.txt"]["priority"], 2) == 83.33

        # Gap file must rank higher than Saturated file
        assert p_map["notes_2005_SSPD.txt"]["priority"] > p_map["notes_2024_PIAV.txt"]["priority"]

        print("TEST_CALCULATE_FILE_PRIORITIES_SYNTHETIC: PASSED")


def test_calculate_file_priorities_live():
    """Verify calculate_file_priorities against real knowledge_base and field_notes/data."""
    priorities = calculate_file_priorities()
    assert len(priorities) > 0, "Expected non-empty file priority list"
    assert priorities[0]["priority"] >= priorities[-1]["priority"]
    print(f"TEST_CALCULATE_FILE_PRIORITIES_LIVE: PASSED ({len(priorities)} files indexed)")
    for p in priorities[:5]:
        print(f"  - {p['filename']}: lines={p['lines']}, gems={p['gems']}, priority={p['priority']}")


if __name__ == "__main__":
    test_calculate_file_priorities_synthetic()
    test_calculate_file_priorities_live()
    print("ALL TESTS PASSED")
