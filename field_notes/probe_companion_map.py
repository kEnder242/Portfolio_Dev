#!/usr/bin/env python3
"""
[FEAT-683] / [Story 109.3] AGY Verification Probe for Navigational Companion Files (.map.json).

Audits:
1. Integrity & Schema of notes_2005_SSPD.map.json.
2. Source hash match against physical notes_2005_SSPD.txt on disk.
3. Strict monotonicity and contiguous line coverage (line 1 to EOF).
4. Full semantic metadata presence (platform, implied_era, chunk_type).
"""

import sys
import json
import hashlib
from pathlib import Path

DATA_DIR = Path("/home/jallred/Portfolio_Dev/field_notes/data")
RAW_NOTES_DIR = Path("/home/jallred/knowledge_base")
MAP_FILE = DATA_DIR / "notes_2005_SSPD.map.json"
SOURCE_FILE = RAW_NOTES_DIR / "notes_2005_SSPD.txt"


def probe_companion_map():
    assert MAP_FILE.exists(), f"Companion map file missing: {MAP_FILE}"
    assert SOURCE_FILE.exists(), f"Source notes file missing: {SOURCE_FILE}"

    with open(MAP_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. Root schema checks
    assert data.get("source_file") == "notes_2005_SSPD.txt", f"Unexpected source_file: {data.get('source_file')}"
    assert "source_file_hash" in data, "source_file_hash missing"

    with open(SOURCE_FILE, "r", encoding="utf-8", errors="replace") as f:
        src_text = f.read()
    expected_hash = hashlib.md5(src_text.encode("utf-8", errors="replace")).hexdigest()
    assert data["source_file_hash"] == expected_hash, f"Hash mismatch: {data['source_file_hash']} != {expected_hash}"

    sections = data.get("sections", [])
    assert len(sections) >= 90, f"Expected >= 90 sections, found {len(sections)}"
    assert data.get("total_sections") == len(sections), "total_sections count mismatch"

    # 2. Section schema and boundary coverage
    prev_end = 0
    for idx, sec in enumerate(sections):
        assert "section_id" in sec, f"Missing section_id in section {idx}"
        assert "line_start" in sec, f"Missing line_start in section {idx}"
        assert "line_end" in sec, f"Missing line_end in section {idx}"
        assert "section_title" in sec and len(sec["section_title"]) > 0, f"Empty title in section {idx}"
        assert "platform" in sec and len(sec["platform"]) > 0, f"Missing platform in section {idx}"
        assert "implied_era" in sec and "2005" in sec["implied_era"], f"Invalid implied_era in section {idx}"
        assert "chunk_type" in sec and len(sec["chunk_type"]) > 0, f"Missing chunk_type in section {idx}"

        l_start = sec["line_start"]
        l_end = sec["line_end"]
        assert l_start <= l_end, f"Inverted range in section {idx}: {l_start} > {l_end}"

        # Contiguity check
        assert l_start == prev_end + 1, f"Gap detected before section {idx}: expected {prev_end + 1}, got {l_start}"
        prev_end = l_end

    total_lines = len(src_text.splitlines())
    assert prev_end == total_lines, f"EOF coverage mismatch: covered up to {prev_end}, file has {total_lines} lines"

    print(f"PROBE PASSED: {MAP_FILE.name} verified with {len(sections)} sections covering lines 1-{total_lines} seamlessly.")
    print("Sample mapped sections:")
    for s in sections[:4]:
        print(f"  - [{s['section_id']}] Lines {s['line_start']}-{s['line_end']} | {s['platform']} | {s['chunk_type']} | {s['section_title']}")
    return True


if __name__ == "__main__":
    if probe_companion_map():
        sys.exit(0)
    sys.exit(1)
