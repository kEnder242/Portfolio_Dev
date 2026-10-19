#!/usr/bin/env python3
"""[FEAT-662 / FEAT-665] Migrate legacy paper_jitc_intuition.json and notes_jitc_bones.json
into the canonical atomic bundle: Portfolio_Dev/papers/jitc_intuition/
  - jitc_kabal.json
  - jitc_spine.json
"""

import datetime
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PAPERS_DIR = BASE_DIR / "papers"
BUNDLE_DIR = PAPERS_DIR / "jitc_intuition"
OLD_PAPER_PATH = PAPERS_DIR / "paper_jitc_intuition.json"
OLD_BONES_PATH = BASE_DIR / "field_notes/data/bones/notes_jitc_bones.json"


def migrate():
    os.makedirs(BUNDLE_DIR, exist_ok=True)
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # Load old paper AST
    old_paper = {}
    if OLD_PAPER_PATH.exists():
        with open(OLD_PAPER_PATH, "r", encoding="utf-8") as f:
            old_paper = json.load(f)

    # Load old bones
    old_bones = {}
    if OLD_BONES_PATH.exists():
        with open(OLD_BONES_PATH, "r", encoding="utf-8") as f:
            old_bones = json.load(f)

    cards = []
    spine_node_ids = []
    spine_nodes = []
    counter = 0

    def add_card(sub_ns: str, title: str, text: str, citations: list, tags: list, style: str = "paragraph", raw_source: str = "paper_jitc_intuition.json"):
        nonlocal counter
        counter += 1
        num_str = f"{counter:03d}"
        card_id = f"JITC.{sub_ns.upper()}-{num_str}"
        card = {
            "id": card_id,
            "local_id": num_str,
            "sub_namespace": sub_ns.upper(),
            "kabal": "jitc_intuition",
            "origin": {
                "author": old_paper.get("author", "Jason Allred"),
                "source": raw_source,
                "raw_text": text.strip()
            },
            "synthesis": {
                "title": title.strip(),
                "summary": text.strip(),
                "citations": citations
            },
            "metadata": {
                "tags": tags,
                "style": style,
                "created_at": now_iso
            }
        }
        cards.append(card)
        spine_node_ids.append(card_id)
        spine_nodes.append({
            "id": card_id,
            "style": style,
            "sub_namespace": sub_ns.upper()
        })
        return card_id

    # 1. Paper Header / Title
    title = old_paper.get("title", "Just in time context retrieval and synthesis")
    subtitle = old_paper.get("subtitle", "Applied armchair philosophy")
    add_card("HEADER", title, f"{title} — {subtitle}", old_paper.get("citations", []), ["header", "jitc", "philosophy"], style="heading")

    # 2. Iterate sections and paragraphs
    for sec in old_paper.get("sections", []):
        sec_heading = sec.get("heading", f"Section {sec.get('id', '')}")
        sec_citations = sec.get("citations", [])
        add_card("SEC", sec_heading, sec_heading, sec_citations, ["section", "jitc"], style="heading")

        for p_idx, para in enumerate(sec.get("paragraphs", [])):
            para_text = para.get("text", "") if isinstance(para, dict) else str(para)
            para_cits = para.get("citations", []) if isinstance(para, dict) else []
            p_title = f"{sec_heading} — Paragraph {p_idx + 1}"
            add_card("PARA", p_title, para_text, para_cits, ["paragraph", "jitc"], style="paragraph")

    # 3. Add historical bone cards from notes_jitc_bones.json as companion cards
    bone_node_ids = []
    for b in old_bones.get("bones", []):
        b_id = b.get("id", f"WIS-{counter:03d}")
        b_title = b.get("title", "Historical Bone Note")
        b_raw = b.get("origin_verbatim", "")
        card_id = add_card("BONE", f"Historical Bone: {b_title}", b_raw, [b_id], ["bone-legacy", "adr-008", "jitc"], style="callout", raw_source="notes_jitc_bones.json")
        bone_node_ids.append(card_id)

    # 4. Write jitc_intuition_kabal.json
    kabal_payload = {
        "slug": "jitc_intuition",
        "variable_prefix": "JITC",
        "title": "JITC Intuition Kabal Knowledge Group",
        "source_document": "paper_jitc_intuition.json",
        "created_at": now_iso,
        "updated_at": now_iso,
        "cards": cards
    }
    kabal_out = BUNDLE_DIR / "jitc_intuition_kabal.json"
    with open(kabal_out, "w", encoding="utf-8") as f:
        json.dump(kabal_payload, f, indent=2)
    print(f"✅ Generated {kabal_out} with {len(cards)} cards")

    # 5. Write jitc_intuition_spine.json
    spine_payload = {
        "slug": "jitc_intuition",
        "variable_prefix": "JITC",
        "title": "Just in Time Context Retrieval and Synthesis Narrative Spine",
        "source_document": "paper_jitc_intuition.json",
        "active_tag": "@master",
        "created_at": now_iso,
        "updated_at": now_iso,
        "tags": {
            "@master": {
                "name": "@master",
                "description": "Canonical JITC manuscript sections, paragraphs, and citations",
                "created_at": now_iso,
                "node_ids": [nid for nid in spine_node_ids if not nid.startswith("JITC.BONE")]
            },
            "@with_bones": {
                "name": "@with_bones",
                "description": "JITC manuscript including historical companion bone notes",
                "created_at": now_iso,
                "node_ids": spine_node_ids
            }
        },
        "nodes": spine_nodes
    }
    spine_out = BUNDLE_DIR / "jitc_intuition_spine.json"
    with open(spine_out, "w", encoding="utf-8") as f:
        json.dump(spine_payload, f, indent=2)
    print(f"✅ Generated {spine_out} with {len(spine_nodes)} nodes and tags: {list(spine_payload['tags'].keys())}")

    # 6. Update manifest.json
    manifest_path = PAPERS_DIR / "manifest.json"
    if manifest_path.exists():
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        for p in manifest.get("papers", []):
            if p.get("slug") == "jitc_intuition":
                p["bundle_path"] = "papers/jitc_intuition"
                p["kabal_file"] = "jitc_intuition_kabal.json"
                p["spine_file"] = "jitc_intuition_spine.json"
                p["status"] = "KABAL_BUNDLE_CONVERTED"
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
        print(f"✅ Updated {manifest_path}")

if __name__ == "__main__":
    migrate()
