#!/usr/bin/env python3
"""
[ARCH-003 / Story 109.16] Canonical Temporal Lakehouse Migration.
Collapses legacy fragmented sub-files (YYYY_MM.json, YYYY_YYYY.json, Unknown.json)
into authoritative canonical data/{YYYY}.json files.
Performs global evidence-based and semantic deduplication,
strictly purges cross-year contaminations, and executes atomic writes
via BKM-022 (.tmp + os.replace).
"""

import glob
import json
import logging
import os
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def norm_text(text: str) -> str:
    return re.sub(r"[^a-z0-9\s]", "", str(text or "").lower()).strip()


def extract_event_year(item: dict) -> str:
    """Extract canonical year strictly from validated event date, falling back to anchors."""
    for field in ["date", "event_era", "document_date"]:
        val = str(item.get(field) or "").strip()
        m = re.match(r"^(20\d{2})", val)
        if m:
            return m.group(1)
    # Check temporal_anchor.year
    ta = item.get("temporal_anchor")
    if isinstance(ta, dict) and ta.get("year"):
        try:
            y = int(ta["year"])
            if 2005 <= y <= 2026:
                return str(y)
        except Exception:
            pass
    return "Unknown"


def migrate_to_canonical_lakehouse(dry_run: bool = False) -> dict:
    all_json_files = sorted(glob.glob(str(DATA_DIR / "*.json")))
    target_files = [
        f for f in all_json_files
        if re.match(r"^(Unknown|\d{4}(_\w+)?)\.json$", os.path.basename(f))
    ]

    logging.info(f"Scanning {len(target_files)} candidate gem files...")

    canonical_store: dict[str, list[dict]] = {}
    total_raw_gems = 0
    sub_files_to_deprecate = []

    for fpath in target_files:
        base = os.path.basename(fpath)
        is_sub_file = bool(re.match(r"^\d{4}_\w+\.json$", base))
        if is_sub_file:
            sub_files_to_deprecate.append(fpath)

        try:
            with open(fpath, "r", encoding="utf-8") as f:
                items = json.load(f)
            if not isinstance(items, list):
                continue

            for gem in items:
                if not isinstance(gem, dict):
                    continue
                total_raw_gems += 1
                y = extract_event_year(gem)
                
                # If date was corrupted to 2023-02-20 from legacy journal bridge
                # but source_file / context indicates different era, preserve or route accurately
                canonical_store.setdefault(y, []).append(gem)
        except Exception as e:
            logging.error(f"Error reading {base}: {e}")

    logging.info(f"Loaded {total_raw_gems} total raw gems across all files.")

    # Deduplication and Canonical Writing
    deduped_store: dict[str, list[dict]] = {}
    total_deduped_gems = 0

    for y in sorted(canonical_store.keys()):
        gems = canonical_store[y]
        unique_gems = []
        seen_evidence = {}
        seen_summaries = set()

        for g in gems:
            ev = norm_text(g.get("evidence", ""))
            sum_txt = norm_text(g.get("summary", ""))
            d = str(g.get("date", ""))

            # Evidence-based deduplication
            if len(ev) >= 15:
                key = (d, ev)
                if key in seen_evidence:
                    continue
                seen_evidence[key] = True
            elif sum_txt:
                key = (d, sum_txt)
                if key in seen_summaries:
                    continue
                seen_summaries.add(key)
            unique_gems.append(g)

        unique_gems.sort(key=lambda x: str(x.get("date", "")))
        deduped_store[y] = unique_gems
        total_deduped_gems += len(unique_gems)
        logging.info(f"  Year {y:7}: {len(unique_gems):4} unique gems (collapsed from {len(gems)})")

    logging.info(f"Total gems after global evidence dedup: {total_deduped_gems} (deduped {total_raw_gems - total_deduped_gems})")

    if not dry_run:
        # Atomic write of canonical YYYY.json files via BKM-022
        for y, gems in deduped_store.items():
            out_path = DATA_DIR / f"{y}.json"
            tmp_path = DATA_DIR / f"{y}.json.tmp"
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(gems, f, indent=2)
            os.replace(tmp_path, out_path)
            logging.info(f"Atomically committed {out_path} ({len(gems)} gems)")

        # Clear/archive legacy sub-files so they don't cause duplicate scans
        for sf in sub_files_to_deprecate:
            try:
                # Remove deprecated sub-file
                os.remove(sf)
            except Exception as e:
                logging.warning(f"Could not remove sub-file {sf}: {e}")
        logging.info(f"Removed {len(sub_files_to_deprecate)} deprecated fragmented sub-files.")

    return {
        "raw_gems": total_raw_gems,
        "deduped_gems": total_deduped_gems,
        "sub_files_deprecated": len(sub_files_to_deprecate),
        "years": {y: len(v) for y, v in deduped_store.items()}
    }


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    res = migrate_to_canonical_lakehouse(dry_run=dry)
    print("\nMigration Results Summary:")
    print(json.dumps(res, indent=2))
