#!/usr/bin/env python3
"""
[FEAT-454/FEAT-458] Extract Latest Distilled Gems for Status Dashboard
Parses the most recently synthesized year archive (e.g. 2024.json) and extracts
the top Rank 4/5 technical gems, commands, and evidence into latest_synthesis_gems.json.
"""

import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"


def _parse_year_from_key(key):
    """Extract 4-digit year from trailing '::YYYY-MM' or '::YYYY-YYYY' part of a chunk key."""
    date_part = key.split("::")[-1]
    m = re.search(r"(20\d{2})-", date_part)
    if m:
        return m.group(1)
    m = re.search(r"(20\d{2})", date_part)
    return m.group(1) if m else None


def _year_rank_gems(year_file):
    try:
        with open(year_file, "r") as f:
            items = json.load(f)
        return sum(1 for it in items if isinstance(it, dict) and it.get("rank", 0) >= 4)
    except Exception:
        return 0


def _resolve_target_year():
    """[Story 105.12] Dynamically resolve target year: chunk_state.json > queue.json > latest rank>=4 year."""
    last_file = "unknown"
    state_file = DATA_DIR / "chunk_state.json"
    if state_file.exists():
        try:
            with open(state_file, "r") as f:
                state = json.load(f)
            keys = [k for k in state.keys() if "::" in k]
            if keys:
                def recency(k):
                    m = re.search(r"::(\d{4}-\d{2})$", k)
                    return m.group(1) if m else k.rsplit("::", 1)[-1]
                latest_key = max(keys, key=recency)
                last_file = latest_key.split("::")[0]
                year = _parse_year_from_key(latest_key)
                if year:
                    return last_file, year
        except Exception as e:
            print(f"⚠️ chunk_state.json unreadable: {e}")
    queue_file = DATA_DIR / "queue.json"
    if queue_file.exists():
        try:
            with open(queue_file, "r") as f:
                queue = json.load(f)
            if isinstance(queue, list) and queue:
                task = queue[-1]
                if isinstance(task, dict):
                    last_file = task.get("last_file") or task.get("filename") or last_file
                    for field in ("bucket", "last_file", "filename"):
                        val = task.get(field, "")
                        if isinstance(val, str):
                            m = re.search(r"(20\d{2})-\d{2}", val)
                            if m:
                                return last_file, m.group(1)
                            m = re.search(r"(20\d{2})$", val)
                            if m:
                                return last_file, m.group(1)
        except Exception as e:
            print(f"⚠️ queue.json unreadable: {e}")
    year_files = sorted(
        (p for p in DATA_DIR.glob("20*.json") if re.match(r"20\d{2}\.json$", p.name)),
        reverse=True,
    )
    for p in year_files:
        if _year_rank_gems(p) >= 4:
            return last_file, p.stem
    if year_files:
        return last_file, year_files[0].stem
    return last_file, "2024"


def extract_latest_gems(max_gems=4):
    last_file, target_year = _resolve_target_year()

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
                ranked.sort(
                    key=lambda x: (x.get("rank", 0), x.get("date", "")), reverse=True
                )
                for it in ranked[:max_gems]:
                    gems.append(
                        {
                            "id": it.get("id", "GEM-???"),
                            "rank": it.get("rank", 4),
                            "date": it.get("date", ""),
                            "summary": it.get("summary", ""),
                            "evidence": it.get("evidence", ""),
                            "tags": it.get("tags", [])[:4],
                            "source_file": last_file,
                        }
                    )
        except Exception as e:
            print(f"Error reading {year_file}: {e}")

    out_file = DATA_DIR / "latest_synthesis_gems.json"
    payload = {
        "source_file": last_file,
        "year": target_year,
        "total_gems_extracted": len(gems),
        "gems": gems,
    }

    with open(out_file, "w") as f:
        json.dump(payload, f, indent=2)

    print(
        f"✅ Extracted {len(gems)} Rank 4/5 gems from {year_file.name} to {out_file.name}"
    )
    return payload


if __name__ == "__main__":
    extract_latest_gems()
