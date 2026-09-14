#!/usr/bin/env python3
"""
[FEAT-559] Full DNA Manifest Synchronizer
Populates Portfolio_Dev/field_notes/data/dna_manifest.json with:
1. All 270+ features from FeatureTracker.md (feature collection)
2. All 50+ BKMs from HomeLabAI/docs/Protocols.md (behavioral collection)
3. All philosophy cards from philosophy_data.json
4. All wisdom cards from wisdom_data.json
5. All discovery events from timeline_data.json
6. All sprint plans from Portfolio_Dev/docs/sprints/
"""

import json
import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent
LAB_ROOT = REPO_ROOT.parent

FEATURE_TRACKER_MD = REPO_ROOT / "FeatureTracker.md"
PROTOCOLS_MD = LAB_ROOT / "HomeLabAI" / "docs" / "Protocols.md"
WISDOM_PATH = BASE_DIR / "data" / "wisdom_data.json"
PHILOSOPHY_PATH = BASE_DIR / "data" / "philosophy_data.json"
TIMELINE_PATH = BASE_DIR / "data" / "timeline_data.json"
MANIFEST_PATH = BASE_DIR / "data" / "dna_manifest.json"
SPRINTS_DIR = REPO_ROOT / "docs" / "sprints"

def parse_features():
    cards = []
    if not FEATURE_TRACKER_MD.exists():
        return cards
    content = FEATURE_TRACKER_MD.read_text(encoding="utf-8")
    sections = re.split(r'\n(?=## \[(?:FEAT|LAB)-)', content)
    for sec in sections:
        header = re.match(r'## \[((?:FEAT|LAB)-[A-Za-z0-9_\.\-]+)\]\s*(.*)', sec)
        if not header:
            continue
        fid = header.group(1).strip()
        title = header.group(2).strip()

        status_m = re.search(r'\*\*Status:\*\*\s*(.*)', sec)
        status = status_m.group(1).strip() if status_m else "ACTIVE"

        code_m = re.search(r'\*\*Code:\*\*\s*(.*)', sec)
        code_ref = code_m.group(1).strip() if code_m else ""

        logic_m = re.search(r'\*\*Logic:\*\*\s*(.*?)(?=\n\*\*[A-Za-z]+:\*\*|\n## |\Z)', sec, re.DOTALL)
        logic = logic_m.group(1).strip() if logic_m else ""

        rationale_m = re.search(r'\*\*Rationale:\*\*\s*(.*?)(?=\n\*\*[A-Za-z]+:\*\*|\n## |\Z)', sec, re.DOTALL)
        rationale = rationale_m.group(1).strip() if rationale_m else ""

        mechanism_m = re.search(r'\*\*Mechanism:\*\*\s*(.*?)(?=\n\*\*[A-Za-z]+:\*\*|\n## |\Z)', sec, re.DOTALL)
        mechanism = mechanism_m.group(1).strip() if mechanism_m else ""

        origin_text = rationale or logic or f"{fid}: {title}"
        narrative = f"{logic}\n\n{mechanism}".strip() if (logic or mechanism) else origin_text

        cards.append({
            "id": fid,
            "title": title or fid,
            "origin": {
                "author": "Federated Lab",
                "text": origin_text,
                "source": "FeatureTracker.md",
                "immutable": True
            },
            "synthesis": {
                "narrative_context": narrative,
                "lab_anchors": [code_ref] if code_ref else [],
                "review_notes": f"Status: {status}",
                "refinement_version": 1
            },
            "metadata": {
                "tags": ["feature", "code-anchor", status.lower()],
                "status": status,
                "bucket_id": "bucket_5_infra"
            }
        })
    return cards

def parse_protocols():
    cards = []
    if not PROTOCOLS_MD.exists():
        return cards
    content = PROTOCOLS_MD.read_text(encoding="utf-8")
    sections = re.split(r'\n(?=## BKM-)', content)
    for sec in sections:
        header = re.match(r'## (BKM-[0-9]+(?:\.[0-9]+)?):\s*(.*)', sec)
        if not header:
            continue
        bid = header.group(1).strip()
        title = header.group(2).strip()

        obj_m = re.search(r'\*\*Objective\*\*:\s*(.*?)(?=\n\n|\n\*|\Z)', sec, re.DOTALL)
        obj = obj_m.group(1).strip() if obj_m else ""

        origin_text = obj or f"{bid}: {title}"
        cards.append({
            "id": bid,
            "title": title or bid,
            "origin": {
                "author": "Federated Lab",
                "text": origin_text,
                "source": "HomeLabAI/docs/Protocols.md",
                "immutable": True
            },
            "synthesis": {
                "narrative_context": sec.strip(),
                "lab_anchors": ["HomeLabAI/docs/Protocols.md"],
                "review_notes": f"Operational Protocol {bid}",
                "refinement_version": 1
            },
            "metadata": {
                "tags": ["bkm", "behavioral-dna", "protocol"],
                "status": "APPROVED",
                "bucket_id": "bucket_4_rigor"
            }
        })
    return cards

def main():
    manifest = {}
    if MANIFEST_PATH.exists():
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                manifest = json.load(f)
        except Exception:
            manifest = {}

    # 1. Wisdom
    if WISDOM_PATH.exists():
        with open(WISDOM_PATH, "r", encoding="utf-8") as f:
            manifest["wisdom"] = json.load(f)

    # 2. Philosophy
    if PHILOSOPHY_PATH.exists():
        with open(PHILOSOPHY_PATH, "r", encoding="utf-8") as f:
            manifest["philosophy"] = json.load(f)

    # 3. Discovery / Timeline
    if TIMELINE_PATH.exists():
        with open(TIMELINE_PATH, "r", encoding="utf-8") as f:
            manifest["discovery"] = json.load(f)

    # 4. Features (Full extraction)
    feat_cards = parse_features()
    manifest["feature"] = feat_cards

    # 5. Behavioral BKMs (Full extraction)
    bkm_cards = parse_protocols()
    manifest["behavioral"] = bkm_cards

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"✅ Synced dna_manifest.json:")
    print(f"   - Wisdom cards:      {len(manifest.get('wisdom', []))}")
    print(f"   - Philosophy cards:  {len(manifest.get('philosophy', []))}")
    print(f"   - Feature DNA:       {len(manifest.get('feature', []))} (from FeatureTracker.md)")
    print(f"   - Behavioral BKMs:   {len(manifest.get('behavioral', []))} (from Protocols.md)")
    print(f"   - Discovery events:  {len(manifest.get('discovery', []))}")

if __name__ == "__main__":
    main()
