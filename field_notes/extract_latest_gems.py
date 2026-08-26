#!/usr/bin/env python3
"""
[FEAT-454/FEAT-458] Extract Latest Distilled Gems for Status Dashboard
Parses the most recently synthesized year archive (e.g. 2024.json) and extracts
the top Rank 4/5 technical gems, commands, and evidence into latest_synthesis_gems.json.
"""

import json
import os
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"

def extract_latest_gems(max_gems=4):
    status_file = DATA_DIR / "status.json"
    last_file = "notes_2024_PIAV.txt"
    target_year = "2024"

    if status_file.exists():
        try:
            with open(status_file, "r") as f:
                s = json.load(f)
                last_file = s.get("last_file", last_file)
                m = re.search(r"20\d{2}", last_file)
                if m:
                    target_year = m.group(0)
        except Exception:
            pass

    year_file = DATA_DIR / f"{target_year}.json"
    if not year_file.exists():
        year_files = sorted(DATA_DIR.glob("20*.json"), reverse=True)
        if year_files:
            year_file = year_files[0]
            target_year = year_file.stem

    gems = []
    if year_file.exists():
        try:
            with open(year_file, "r") as f:
                items = json.load(f)
                ranked = [it for it in items if it.get("rank", 0) >= 4]
                ranked.sort(key=lambda x: (x.get("rank", 0), x.get("date", "")), reverse=True)
                for it in ranked[:max_gems]:
                    gems.append({
                        "id": it.get("id", "GEM-???"),
                        "rank": it.get("rank", 4),
                        "date": it.get("date", ""),
                        "summary": it.get("summary", ""),
                        "evidence": it.get("evidence", ""),
                        "tags": it.get("tags", [])[:4],
                        "source_file": last_file
                    })
        except Exception as e:
            print(f"Error reading {year_file}: {e}")

    out_file = DATA_DIR / "latest_synthesis_gems.json"
    payload = {
        "source_file": last_file,
        "year": target_year,
        "total_gems_extracted": len(gems),
        "gems": gems
    }

    with open(out_file, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"✅ Extracted {len(gems)} Rank 4/5 gems from {year_file.name} to {out_file.name}")
    return payload

if __name__ == "__main__":
    extract_latest_gems()
