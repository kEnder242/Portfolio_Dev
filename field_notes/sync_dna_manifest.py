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

    # 1. Philosophy DNA (Authoritative RW Collection)
    if PHILOSOPHY_PATH.exists():
        with open(PHILOSOPHY_PATH, "r", encoding="utf-8") as f:
            manifest["philosophy"] = json.load(f)

    # 2. Wisdom Cards (Authoritative RW Collection from War Stories)
    if WISDOM_PATH.exists():
        with open(WISDOM_PATH, "r", encoding="utf-8") as f:
            manifest["wisdom"] = json.load(f)
    elif "philosophy" in manifest:
        manifest["wisdom"] = manifest["philosophy"]

    # 3. Discovery / Timeline
    if TIMELINE_PATH.exists():
        with open(TIMELINE_PATH, "r", encoding="utf-8") as f:
            manifest["discovery"] = json.load(f)

    # 4. Features (Full extraction from FeatureTracker.md)
    feat_cards = parse_features()
    manifest["feature"] = feat_cards

    # 5. Behavioral BKMs (Full extraction from Protocols.md)
    bkm_cards = parse_protocols()
    manifest["behavioral"] = bkm_cards

    # 6. Reverse DNA (RDNA) Questions
    rdna_path = BASE_DIR / "data" / "rdna_questions.json"
    if rdna_path.exists():
        try:
            with open(rdna_path, "r", encoding="utf-8") as f:
                raw_rdna = json.load(f)
                rdna_cards = []
                for item in raw_rdna:
                    rid = item.get("id", "RDNA-???")
                    target = item.get("target_dna", {})
                    variants = item.get("question_variants", [])
                    var_str = "\n".join([f"- {v}" for v in variants])
                    rdna_cards.append({
                        "id": rid,
                        "title": item.get("question", rid),
                        "origin": {
                            "author": "Reverse DNA Engine",
                            "text": f"Canonical: {item.get('question')}\n\nVariants:\n{var_str}",
                            "source": "rdna_questions.json",
                            "immutable": False
                        },
                        "synthesis": {
                            "narrative_context": f"Maps to {target.get('id', 'DNA')} ({target.get('title', '')}) in {target.get('collection', 'philosophy_dna')} with confidence floor {item.get('confidence_floor', 0.75)}.",
                            "lab_anchors": [target.get("id", "")] if target.get("id") else [],
                            "review_notes": f"Category: {item.get('intent_category', 'general')}",
                            "refinement_version": 1
                        },
                        "metadata": {
                            "tags": item.get("metadata", {}).get("tags", ["rdna", "resonant-question"]),
                            "status": "ACTIVE",
                            "bucket_id": "bucket_rdna"
                        }
                    })
                manifest["rdna"] = rdna_cards
        except Exception as e:
            print(f"Warning loading RDNA: {e}")

    # 7. Sprints extraction
    sprint_cards = []
    for sdir in [SPRINTS_DIR / "active", SPRINTS_DIR / "archive"]:
        if sdir.exists():
            for sfile in sorted(sdir.glob("*.md")):
                try:
                    s_text = sfile.read_text(encoding="utf-8")
                    first_line = s_text.splitlines()[0] if s_text.splitlines() else sfile.stem
                    s_title = re.sub(r'^[#\s]+', '', first_line).strip()
                    sprint_cards.append({
                        "id": sfile.stem,
                        "title": s_title or sfile.stem,
                        "origin": {
                            "author": "Federated Lab",
                            "text": s_text[:500] + "...",
                            "source": f"docs/sprints/{sdir.name}/{sfile.name}",
                            "immutable": True
                        },
                        "synthesis": {
                            "narrative_context": s_text[:1000],
                            "lab_anchors": [f"docs/sprints/{sdir.name}/{sfile.name}"],
                            "review_notes": f"Sprint document {sfile.stem}",
                            "refinement_version": 1
                        },
                        "metadata": {
                            "tags": ["sprint", "planning", sdir.name],
                            "status": "ARCHIVED" if sdir.name == "archive" else "ACTIVE",
                            "bucket_id": "bucket_sprints"
                        }
                    })
                except Exception:
                    pass
    if sprint_cards:
        manifest["sprint"] = sprint_cards

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"✅ Synced dna_manifest.json:")
    for k, v in manifest.items():
        print(f"   - {k.capitalize()} cards: {len(v)}")

if __name__ == "__main__":
    main()
