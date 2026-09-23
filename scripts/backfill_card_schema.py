#!/usr/bin/env python3
"""
[SPR-86 Story 8612] WIS and PHL Schema Backfill Migration
Addresses SPRINT_86_DEEP_DIVE_DEFICIENCY_REPORT.md Finding 15:
481 legacy WIS cards (and 34 PHL cards) have synthesis dicts lacking
'mutations'[] and 'revisions'[], making the mutation/revision UX invisible.

Behavior:
1. Load Portfolio_Dev/dna/wisdom_data.json and philosophy_data.json.
2. For every card, add 'mutations': [] and 'revisions': [] to synthesis
   ONLY when the key is missing (idempotent; safe to re-run).
3. Persist each file atomically (.tmp + os.replace) only if mutated.
4. Print final counts so the orchestrator can confirm 481 WIS + 34 PHL.

Class 1: standard library only, no external dependencies.
"""

import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent  # Portfolio_Dev/
DNA_DIR = REPO_ROOT / "dna"

TARGET_FILES = [
    ("wisdom_data.json", 481),
    ("philosophy_data.json", 34),
]

# Canonical insertion order used by newer cards (mutations then revisions).
MUTATIONS_DEFAULT = []
REVISIONS_DEFAULT = []


def backfill_synthesis(cards):
    """Return (modified_count, cards_with_mutations, cards_with_revisions)."""
    modified = 0
    with_mutations = 0
    with_revisions = 0
    for card in cards:
        if not isinstance(card, dict):
            continue
        synthesis = card.get("synthesis")
        if not isinstance(synthesis, dict):
            continue
        touched = False
        if "mutations" not in synthesis:
            synthesis["mutations"] = list(MUTATIONS_DEFAULT)
            touched = True
        if "revisions" not in synthesis:
            synthesis["revisions"] = list(REVISIONS_DEFAULT)
            touched = True
        if touched:
            modified += 1
        if isinstance(synthesis.get("mutations"), list):
            with_mutations += 1
        if isinstance(synthesis.get("revisions"), list):
            with_revisions += 1
    return modified, with_mutations, with_revisions


def atomic_write_json(path, data):
    """Persist data to path atomically via .tmp + os.replace."""
    tmp_path = str(path) + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp_path, path)
    return path.stat().st_size


def main():
    failures = []
    for filename, expected in TARGET_FILES:
        path = DNA_DIR / filename
        if not path.exists():
            print(f"[SKIP] {filename}: file not found at {path}", file=sys.stderr)
            failures.append(filename)
            continue

        with open(path, "r", encoding="utf-8") as f:
            cards = json.load(f)

        modified, with_mutations, with_revisions = backfill_synthesis(cards)
        size_before = path.stat().st_size

        if modified > 0:
            size_after = atomic_write_json(path, cards)
            action = f"PATCHED ({modified} cards mutated, {size_before}B -> {size_after}B)"
        else:
            action = "UNCHANGED (idempotent re-run)"

        print(
            f"[{path.name}] total={len(cards)} modified={modified} "
            f"mutations={with_mutations}/{len(cards)} revisions={with_revisions}/{len(cards)} -> {action}"
        )
        if len(cards) != expected or with_mutations != len(cards) or with_revisions != len(cards):
            failures.append(filename)

    if failures:
        print(f"\n[FAIL] Verification failed for: {', '.join(failures)}", file=sys.stderr)
        return 1
    print(f"\n[OK] All {len(TARGET_FILES)} files verified: every card carries mutations[] and revisions[].")
    return 0


if __name__ == "__main__":
    sys.exit(main())
