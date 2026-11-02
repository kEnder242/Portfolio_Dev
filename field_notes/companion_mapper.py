#!/usr/bin/env python3
"""
[FEAT-683] / [Story 109.3] 3-Tier Pipeline for Navigational Companion Files (.map.json).

Pipeline:
1. Mechanical Python Slicer: Slices gap files on dividers (====, ----, [ERR, and empty line clusters).
2. Semantic Mapper: Classifies each section (title, platform, era, chunk_type) using M5 Air MLX :8002
   with local deterministic heuristic fail-soft fallback.
3. Serializes companion map to Portfolio_Dev/field_notes/data/<basename>.map.json.
"""

import os
import sys
import json
import re
import hashlib
import time
import urllib.request
import urllib.error
from pathlib import Path

DATA_DIR = Path("/home/jallred/Portfolio_Dev/field_notes/data")
RAW_NOTES_DIR = Path("/home/jallred/knowledge_base")
MLX_ENDPOINT = os.getenv("MLX_ENDPOINT", "http://192.168.1.46:8002/v1/chat/completions")


def compute_hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8", errors="replace")).hexdigest()


def slice_file(filepath: Path) -> list[dict]:
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    sections = []
    current_start = 1
    current_title = "Header / Environment Overview"
    pattern = re.compile(r"^(?:={3,}|-{4,}|\[ERR|\*{3,}|_{3,})")

    for idx, line in enumerate(lines, 1):
        m = pattern.match(line.strip())
        is_gap = False
        if idx > 3 and all(lines[i - 1].strip() == "" for i in range(idx - 2, idx + 1)):
            is_gap = True

        # Bounded slice interval (minimum 10 lines or major divider)
        if (m or is_gap) and (idx - current_start >= 10 or (m and idx - current_start >= 5)):
            title = line.strip().strip("=-* _") if m else "Log Section"
            if not title:
                title = f"Section at line {idx}"
            sections.append({
                "line_start": current_start,
                "line_end": idx - 1,
                "raw_sample": "".join(lines[current_start - 1:min(idx - 1, current_start + 8)]),
                "section_title": current_title[:70]
            })
            current_start = idx
            current_title = title

    sections.append({
        "line_start": current_start,
        "line_end": len(lines),
        "raw_sample": "".join(lines[current_start - 1:min(len(lines), current_start + 8)]),
        "section_title": current_title[:70]
    })

    return sections, len(lines)


def classify_section_heuristic(title: str, sample: str) -> tuple[str, str, str]:
    """Heuristic fallback when MLX is unreachable or slow."""
    t_lower = (title + " " + sample).lower()
    platform = "SSPD"
    era = "2005-Q1"
    chunk_type = "diagnostic_log"

    if "watchdog" in t_lower:
        chunk_type = "watchdog_telemetry"
        platform = "IPMI/BMC"
    elif "pef" in t_lower:
        chunk_type = "pef_configuration"
        platform = "IPMI"
    elif "sighting" in t_lower or "tracker" in t_lower or "#41879" in t_lower:
        chunk_type = "sighting_tracker"
        platform = "SSPD"
    elif "selftest" in t_lower or "self test" in t_lower:
        chunk_type = "self_test_log"
        platform = "BMC"
    elif "chassis" in t_lower or "enclosure" in t_lower:
        chunk_type = "chassis_status"
        platform = "IPMI"
    elif "err-" in t_lower or "error" in t_lower:
        chunk_type = "error_diagnostic"
    elif "header" in t_lower:
        chunk_type = "hardware_setup"

    return platform, era, chunk_type


def classify_with_mlx(title: str, sample: str) -> tuple[str, str, str]:
    """Classify section using M5 Air MLX endpoint with timeout."""
    payload = {
        "model": "bonsai2",
        "messages": [
            {"role": "system", "content": "You are a hardware telemetry classifier. Output single line JSON: {\"platform\": \"...\", \"implied_era\": \"2005-Q1\", \"chunk_type\": \"...\"}"},
            {"role": "user", "content": f"Title: {title}\nSample:\n{sample[:300]}"}
        ],
        "max_tokens": 60,
        "temperature": 0.1
    }
    req = urllib.request.Request(
        MLX_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            content = data["choices"][0]["message"]["content"]
            m = re.search(r"\{.*?\}", content, re.DOTALL)
            if m:
                parsed = json.loads(m.group(0))
                return (
                    parsed.get("platform", "SSPD"),
                    parsed.get("implied_era", "2005-Q1"),
                    parsed.get("chunk_type", "diagnostic_log")
                )
    except Exception:
        pass
    return classify_section_heuristic(title, sample)


def generate_companion_map(filename: str = "notes_2005_SSPD.txt") -> Path:
    filepath = RAW_NOTES_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Source notes file not found: {filepath}")

    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        full_text = f.read()

    file_hash = compute_hash(full_text)
    raw_sections, total_lines = slice_file(filepath)
    print(f"Slicing complete: {len(raw_sections)} sections detected across {total_lines} lines.")

    mapped_sections = [None] * len(raw_sections)
    print(f"Beginning concurrent semantic mapping across {len(raw_sections)} sections (max 6 workers)...")

    from concurrent.futures import ThreadPoolExecutor, as_completed

    def process_idx(idx):
        s = raw_sections[idx]
        sec_id = f"SEC-{idx + 1:03d}"
        platform, era, chunk_type = classify_with_mlx(s["section_title"], s["raw_sample"])
        return idx, {
            "section_id": sec_id,
            "line_start": s["line_start"],
            "line_end": s["line_end"],
            "section_title": s["section_title"],
            "platform": platform,
            "implied_era": era,
            "chunk_type": chunk_type
        }

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = [executor.submit(process_idx, i) for i in range(len(raw_sections))]
        done_count = 0
        for f in as_completed(futures):
            idx, res = f.result()
            mapped_sections[idx] = res
            done_count += 1
            if done_count % 25 == 0 or done_count == len(raw_sections):
                print(f"Mapped {done_count}/{len(raw_sections)} sections...")

    map_payload = {
        "version": "1.0.0",
        "description": "Navigational Companion Map for Gap Notes File (FEAT-683)",
        "source_file": filename,
        "source_file_hash": file_hash,
        "total_lines": total_lines,
        "total_sections": len(mapped_sections),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "sections": mapped_sections
    }

    out_file = DATA_DIR / f"{Path(filename).stem}.map.json"
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(map_payload, f, indent=2)

    print(f"Companion map generated successfully: {out_file} ({len(mapped_sections)} sections)")
    return out_file


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "notes_2005_SSPD.txt"
    generate_companion_map(target)
