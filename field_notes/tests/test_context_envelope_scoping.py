#!/usr/bin/env python3
"""
[FEAT-683] / [Story 109.7] Unit Tests for Context Envelope Scoping.

Verifies:
1. is_gap_file() correctly identifies gap files (notes_2005_SSPD.txt, notes_2006_EPSD.txt, etc.)
   and rejects standard journal files (notes_2024_PIAV.txt, notes_2018_PAE.txt).
2. parse_chunks(..., return_envelopes=True) attaches context_envelope strictly to gap files.
3. parse_chunks(..., return_envelopes=True) produces None envelopes for standard files.
4. Envelopes contain "before" and "after" slices with up to 5 lines of boundary context.
"""

import sys
from pathlib import Path

FIELD_NOTES_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(FIELD_NOTES_DIR))

from scan_queue import is_gap_file, parse_chunks


def test_is_gap_file():
    # Gap files
    assert is_gap_file("notes_2005_SSPD.txt") is True
    assert is_gap_file("notes_2005.txt") is True
    assert is_gap_file("notes_2006_EPSD.txt") is True
    assert is_gap_file("Performance review 2008-2018.txt") is True

    # Standard non-gap files
    assert is_gap_file("notes_2024_PIAV.txt") is False
    assert is_gap_file("notes_2018_PAE.txt") is False
    assert is_gap_file("notes_2019_DPV.txt") is False
    assert is_gap_file("ras-2019-11.txt") is False
    print("TEST_IS_GAP_FILE: PASSED")


def test_gap_file_envelope_attached():
    sample_gap_text = "\n".join([
        "Header 1: Pre-incident diagnostic context",
        "Header 2: Server configuration",
        "Header 3: Initial boot",
        "Header 4: Baseline check",
        "Header 5: Entering loop",
        "1/15/2005",
        "Debug entry for socket 0",
        "Registers: 0x4000 0x8000",
        "2/20/2005",
        "Second incident debug",
        "Follow-up actions",
        "Trailing log line 1",
        "Trailing log line 2",
    ])

    chunks, envelopes = parse_chunks(
        sample_gap_text,
        filename="notes_2005_SSPD.txt",
        file_type="LOG",
        return_envelopes=True
    )

    assert "2005-01" in chunks
    assert "2005-02" in chunks
    assert envelopes["2005-01"] is not None
    assert "before" in envelopes["2005-01"]
    assert "after" in envelopes["2005-01"]

    # Before envelope must contain preceding lines
    before_lines = envelopes["2005-01"]["before"]
    assert len(before_lines) <= 5
    assert any("Header" in line for line in before_lines)

    print("TEST_GAP_FILE_ENVELOPE_ATTACHED: PASSED")


def test_standard_file_pure_slice_no_envelope():
    sample_std_text = "\n".join([
        "1/10/2024",
        "Regular daily standup and bug triage",
        "1/11/2024",
        "Completed PECI validation pass",
    ])

    chunks, envelopes = parse_chunks(
        sample_std_text,
        filename="notes_2024_PIAV.txt",
        file_type="LOG",
        return_envelopes=True
    )

    assert "2024-01" in chunks
    # Envelope must be None for standard file (pure slices mandate)
    assert envelopes["2024-01"] is None
    print("TEST_STANDARD_FILE_PURE_SLICE_NO_ENVELOPE: PASSED")


if __name__ == "__main__":
    test_is_gap_file()
    test_gap_file_envelope_attached()
    test_standard_file_pure_slice_no_envelope()
    print("ALL CONTEXT ENVELOPE TESTS PASSED")
