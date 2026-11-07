#!/usr/bin/env python3
"""
[FEAT-557] Reconciles lakehouse annual JSON files in Portfolio_Dev and www_deploy.
- Purges duplicated cloned anchors across 2008-2018 and 2019-2024.
- Injects authentic year-specific strategic anchors from parse_multi_year_focals.py.
- Sorts each year's events with strategic anchor at the top (rank 5).
"""

import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
from parse_multi_year_focals import parse_all_focal_anchors

DEV_DATA = os.path.join(BASE_DIR, "data")
DEPLOY_DATA = os.path.abspath(os.path.join(BASE_DIR, "../../www_deploy/data"))


def clean_and_update_year_file(filepath, year, anchor):
    if not os.path.exists(filepath):
        events = []
    else:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                events = json.load(f)
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            events = []

    # 1. Filter out all old [STRATEGIC_ANCHOR] items to purge clones
    cleaned_events = []
    for e in events:
        summary = str(e.get("summary", ""))
        # Drop old cloned anchors
        if "[STRATEGIC_ANCHOR]" in summary or e.get("rank") == 5:
            continue
        cleaned_events.append(e)

    # 2. Prepend authentic anchor if one exists for this year
    if anchor:
        cleaned_events.insert(0, anchor)

    # 3. Sort: Anchor first, then chronological date
    def sort_key(x):
        summary = str(x.get("summary", ""))
        is_anchor = 0 if "[STRATEGIC_ANCHOR]" in summary or x.get("rank") == 5 else 1
        date = str(x.get("date", "9999-99-99"))
        return (is_anchor, date)

    cleaned_events.sort(key=sort_key)

    with open(filepath + ".tmp", "w", encoding="utf-8") as f:
        json.dump(cleaned_events, f, indent=2)
    os.replace(filepath + ".tmp", filepath)
    print(f"  Updated {os.path.basename(filepath)} with {len(cleaned_events)} events (Anchor: {anchor['id'] if anchor else 'None'})")


def main():
    anchors = parse_all_focal_anchors()

    for data_dir in [DEV_DATA, DEPLOY_DATA]:
        if not os.path.exists(data_dir):
            continue
        print(f"\nProcessing {data_dir}...")
        for yr_int in range(2005, 2026):
            yr = str(yr_int)
            target_file = os.path.join(data_dir, f"{yr}.json")
            clean_and_update_year_file(target_file, yr, anchors.get(yr))

        # Also clean up range artifacts if present in deploy data
        for range_file in ["2008_2018.json", "2019_2024.json"]:
            rf_path = os.path.join(data_dir, range_file)
            if os.path.exists(rf_path):
                try:
                    with open(rf_path, "r", encoding="utf-8") as f:
                        rf_data = json.load(f)
                    rf_clean = [e for e in rf_data if "[STRATEGIC_ANCHOR]" not in str(e.get("summary", "")) and e.get("rank") != 5]
                    with open(rf_path, "w", encoding="utf-8") as f:
                        json.dump(rf_clean, f, indent=2)
                    print(f"  Cleaned range file {range_file}")
                except Exception as e:
                    print(f"  Error cleaning {range_file}: {e}")

    print("\n✅ Lakehouse reconciliation complete.")


if __name__ == "__main__":
    main()
