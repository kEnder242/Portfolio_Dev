#!/usr/bin/env python3
"""[FEAT-595 / FEAT-662 / FEAT-663] Document & Resume Decomposer to Kabal + Replayable Spine.

Imports structured documents (e.g. Jason Allred Resume - Jan 2026.txt) into:
  - Portfolio_Dev/papers/<slug>/<slug>_kabal.json (Substantive DNA cards)
  - Portfolio_Dev/papers/<slug>/<slug>_spine.json (Narrative topology & @master tag)
"""

import argparse
import datetime
import json
import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("decompose_document")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

BASE_DIR = Path(__file__).resolve().parent.parent
PAPERS_DIR = BASE_DIR / "papers"


def parse_resume_text(text: str, prefix: str = "RESUME") -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Parses resume text into atomic Kabal cards and an ordered spine sequence."""
    lines = [l.rstrip() for l in text.splitlines()]
    cards = []
    spine_nodes = []
    
    current_sub = "HEADER"
    local_counter = 0

    def add_card(sub_ns: str, title: str, raw_text: str, tags: List[str], style: str = "paragraph") -> str:
        nonlocal local_counter
        local_counter += 1
        card_num_str = f"{local_counter:03d}"
        card_id = f"{prefix.upper()}.{sub_ns.upper()}-{card_num_str}"
        
        card = {
            "id": card_id,
            "local_id": card_num_str,
            "sub_namespace": sub_ns.upper(),
            "kabal": prefix.lower(),
            "origin": {
                "author": "jallred",
                "source": "Jason Allred Resume - Jan 2026.txt",
                "raw_text": raw_text.strip(),
            },
            "synthesis": {
                "title": title.strip(),
                "summary": raw_text.strip(),
                "citations": [],
            },
            "metadata": {
                "tags": tags,
                "style": style,
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            }
        }
        cards.append(card)
        spine_nodes.append({
            "id": card_id,
            "style": style,
            "sub_namespace": sub_ns.upper(),
        })
        return card_id

    # 1. Contact / Header Block
    header_lines = []
    idx = 0
    while idx < len(lines) and lines[idx].strip():
        header_lines.append(lines[idx].strip())
        idx += 1
    
    if header_lines:
        add_card("HEADER", "Contact Information", " | ".join(header_lines), ["contact", "header"], style="header")
    
    # Process remaining sections
    current_section = "GENERAL"
    i = idx
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        
        # Section Header Detection
        if line in ("System Validation & Platform Telemetry Engineer", "Technical Skills", "Addressing the Giant LLM in the Room", "Experience", "Education"):
            current_section = line
            i += 1
            continue
        
        # Section: Summary / Target Title
        if current_section == "System Validation & Platform Telemetry Engineer":
            add_card("SUMMARY", "Platform Telemetry & Validation Summary", line, ["summary", "telemetry", "validation"], style="callout")
            i += 1
            continue

        # Section: Technical Skills
        if current_section == "Technical Skills":
            if ":" in line:
                category, items = line.split(":", 1)
                add_card("SKILL", f"Skills: {category.strip()}", items.strip(), ["skills", category.lower().strip()], style="bullet")
            else:
                add_card("SKILL", "Technical Skills", line, ["skills"], style="bullet")
            i += 1
            continue

        # Section: Addressing LLM
        if current_section == "Addressing the Giant LLM in the Room":
            add_card("LLM", "Agentic Workflow & AI Tooling Philosophy", line, ["ai", "llm", "workflows", "tooling"], style="callout")
            i += 1
            continue

        # Section: Education
        if current_section == "Education":
            add_card("EDU", "Academic Credentials", line, ["education", "degree"], style="bullet")
            i += 1
            continue

        # Section: Experience
        if current_section == "Experience":
            # Check for Role / Company Header
            if "|" in line or " - " in line and ("20" in line or "19" in line or "Present" in line):
                role_header = line
                # Gather description lines if any
                desc_lines = []
                j = i + 1
                while j < len(lines) and lines[j].strip() and not lines[j].strip().startswith("-") and not ("|" in lines[j] and ("20" in lines[j] or "19" in lines[j])):
                    desc_lines.append(lines[j].strip())
                    j += 1
                desc_text = " ".join(desc_lines)
                role_full = f"{role_header}\n{desc_text}".strip()
                add_card("EXP", f"Role: {role_header[:50]}", role_full, ["experience", "role_overview"], style="heading")
                i = j
                continue
            
            # Check for Bullet point
            if line.startswith("-"):
                bullet_text = line.lstrip("- ").strip()
                # Derive thematic tags
                tags = ["experience", "bullet"]
                if any(w in bullet_text.lower() for w in ["peci", "mctp", "ipmi", "redfish", "bmc"]):
                    tags.append("manageability")
                if any(w in bullet_text.lower() for w in ["telemetry", "power", "ras"]):
                    tags.append("telemetry")
                if any(w in bullet_text.lower() for w in ["python", "c++", "tcl", "perl"]):
                    tags.append("automation")
                if any(w in bullet_text.lower() for w in ["simics", "simulation"]):
                    tags.append("simulation")
                
                title_sample = bullet_text[:60] + "..." if len(bullet_text) > 60 else bullet_text
                add_card("EXP", title_sample, bullet_text, tags, style="bullet")
                i += 1
                continue
            
            # Free paragraph within experience
            add_card("EXP", "Experience Narrative", line, ["experience"], style="paragraph")
            i += 1
            continue

        # Default fallback
        add_card("BODY", "Manuscript Content", line, ["body"], style="paragraph")
        i += 1

    return cards, spine_nodes


def decompose_file(file_path: str, slug: str = "resume", prefix: str = "RESUME", dry_run: bool = False) -> Dict[str, Any]:
    """Decomposes a source document file into a Kabal bundle directory."""
    path = Path(file_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Source file not found at: {file_path}")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    cards, spine_nodes = parse_resume_text(content, prefix=prefix)
    node_ids = [n["id"] for n in spine_nodes]
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    kabal_payload = {
        "slug": slug.lower(),
        "variable_prefix": prefix.upper(),
        "title": f"{slug.title()} Kabal Knowledge Group",
        "source_document": path.name,
        "source_path": str(path),
        "created_at": timestamp,
        "updated_at": timestamp,
        "cards": cards,
    }

    spine_payload = {
        "slug": slug.lower(),
        "variable_prefix": prefix.upper(),
        "title": f"{slug.title()} Narrative Spine",
        "source_document": path.name,
        "active_tag": "@master",
        "created_at": timestamp,
        "updated_at": timestamp,
        "tags": {
            "@master": {
                "name": "@master",
                "description": "Original full imported document verbatim",
                "created_at": timestamp,
                "node_ids": node_ids,
            }
        },
        "nodes": spine_nodes,
    }

    bundle_dir = PAPERS_DIR / slug.lower()
    kabal_dest = bundle_dir / f"{slug.lower()}_kabal.json"
    spine_dest = bundle_dir / f"{slug.lower()}_spine.json"

    if dry_run:
        logger.info(f"[DRY-RUN] Would create {len(cards)} cards in {kabal_dest} and spine {spine_dest}")
        return {"cards": len(cards), "nodes": len(spine_nodes), "kabal_dest": str(kabal_dest), "spine_dest": str(spine_dest)}

    bundle_dir.mkdir(parents=True, exist_ok=True)
    with open(kabal_dest, "w", encoding="utf-8") as f:
        json.dump(kabal_payload, f, indent=2, ensure_ascii=False)
    with open(spine_dest, "w", encoding="utf-8") as f:
        json.dump(spine_payload, f, indent=2, ensure_ascii=False)

    logger.info(f"Successfully decomposed {path.name} into {len(cards)} Kabal cards -> {kabal_dest}")
    logger.info(f"Successfully initialized narrative spine with @master tag -> {spine_dest}")

    return {
        "slug": slug.lower(),
        "cards_created": len(cards),
        "spine_nodes": len(spine_nodes),
        "kabal_path": str(kabal_dest),
        "spine_path": str(spine_dest),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decompose document to Kabal + Spine")
    parser.add_argument("--file", required=True, help="Path to input text/markdown document")
    parser.add_argument("--slug", default="resume", help="Manuscript slug identifier (e.g. resume)")
    parser.add_argument("--prefix", default="RESUME", help="Variable namespace prefix (e.g. RESUME)")
    parser.add_argument("--dry-run", action="store_true", help="Inspect decomposition without writing files")
    parser.add_argument("--sync-chroma", action="store_true", help="Sync resulting cards to ChromaDB")
    args = parser.parse_args()

    result = decompose_file(args.file, slug=args.slug, prefix=args.prefix, dry_run=args.dry_run)
    print(json.dumps(result, indent=2))

    if args.sync_chroma and not args.dry_run:
        from kabal_registry import sync_to_chroma
        sync_res = sync_to_chroma(args.slug)
        print(f"ChromaDB Sync: {sync_res}")
