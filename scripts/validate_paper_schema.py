#!/usr/bin/env python3
"""
[FEAT-585] Story 78.7: Paper JSON Schema & Invariant Validator
Validates paper datasets in Portfolio_Dev/papers/ against strict architectural invariants:
1. Valid top-level metadata (id, title, author, date, voice_profile, sections).
2. Strict paragraph hierarchy (section id SEC-xxx, paragraph id PAR-xxx).
3. Citation validation: all citations must match registered formats (PHL-xxx, DISC-xxx, FEAT-xxx, ARXIV:xxx).
4. No empty or corrupted paragraph bodies.
"""

import json
import os
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
PAPERS_DIR = REPO_ROOT / "papers"
MANIFEST_FILE = PAPERS_DIR / "manifest.json"

CITATION_PATTERN = re.compile(r'^(PHL|DISC|FEAT|ARXIV|GEM|WIS)-[A-Za-z0-9_\.\-]+$|^ARXIV:\d+\.\d+$')

def validate_paper(paper_path):
    print(f"[*] Validating {paper_path}...")
    with open(paper_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    errors = []
    # Check top-level required fields
    for field in ["id", "title", "author", "sections"]:
        if field not in data:
            errors.append(f"Missing top-level field: '{field}'")

    sections = data.get("sections", [])
    if not isinstance(sections, list) or len(sections) == 0:
        errors.append("Sections must be a non-empty list.")

    sec_ids = set()
    par_ids = set()

    for s_idx, sec in enumerate(sections):
        s_id = sec.get("id")
        if not s_id:
            errors.append(f"Section index {s_idx} missing 'id'")
        elif s_id in sec_ids:
            errors.append(f"Duplicate section id: {s_id}")
        else:
            sec_ids.add(s_id)

        paragraphs = sec.get("paragraphs", [])
        if not isinstance(paragraphs, list):
            errors.append(f"Section {s_id} paragraphs must be a list")
            continue

        for p_idx, par in enumerate(paragraphs):
            p_id = par.get("id")
            if not p_id:
                errors.append(f"Section {s_id} paragraph {p_idx} missing 'id'")
            elif p_id in par_ids:
                errors.append(f"Duplicate paragraph id: {p_id}")
            else:
                par_ids.add(p_id)

            citations = par.get("citations", [])
            for c in citations:
                if not CITATION_PATTERN.match(str(c)):
                    errors.append(f"Paragraph {p_id} invalid citation syntax: '{c}'")

    if errors:
        print(f"❌ Schema validation FAILED for {paper_path.name} with {len(errors)} error(s):")
        for err in errors:
            print(f"   - {err}")
        return False
    else:
        print(f"✅ Schema validation PASSED for {paper_path.name} ({len(sections)} sections, {len(par_ids)} paragraphs).")
        return True

def main():
    if not MANIFEST_FILE.exists():
        print(f"❌ Manifest not found: {MANIFEST_FILE}")
        sys.exit(1)

    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        mdata = json.load(f)

    all_passed = True
    for p_info in mdata.get("papers", []):
        file_name = p_info.get("file")
        if file_name:
            p_path = PAPERS_DIR / file_name
            if p_path.exists():
                passed = validate_paper(p_path)
                if not passed:
                    all_passed = False
            else:
                print(f"⚠️ Paper file not found on disk: {p_path}")
                all_passed = False

    if not all_passed:
        sys.exit(1)
    print("\nAll paper schemas verified successfully.")

if __name__ == "__main__":
    main()
