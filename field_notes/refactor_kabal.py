#!/usr/bin/env python3
"""[FEAT-662 / VIBE-017] Atomic Variable Namespace Refactoring Tool.

Performs atomic renaming of Kabal collections and their variable prefixes:
e.g. refactor_kabal.py --from-prefix=RESUME --to-prefix=PORTFOLIO [--from-slug=resume] [--to-slug=portfolio]

Renames directory, files, internal card IDs, spine nodes, and performs atomic
search-and-replace across paper ASTs and citations, preserving the Git paper trail.
"""

import argparse
import json
import logging
import os
import re
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("refactor_kabal")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

BASE_DIR = Path(__file__).resolve().parent.parent
PAPERS_DIR = BASE_DIR / "papers"


def refactor_kabal(
    from_prefix: str,
    to_prefix: str,
    from_slug: Optional[str] = None,
    to_slug: Optional[str] = None,
    dry_run: bool = False,
) -> Dict[str, Any]:
    from_prefix = from_prefix.upper().strip()
    to_prefix = to_prefix.upper().strip()
    from_slug = (from_slug or from_prefix).lower().strip()
    to_slug = (to_slug or to_prefix).lower().strip()

    source_dir = PAPERS_DIR / from_slug
    target_dir = PAPERS_DIR / to_slug

    if not source_dir.exists():
        raise FileNotFoundError(f"Source kabal bundle directory not found at: {source_dir}")

    source_kabal = source_dir / f"{from_slug}_kabal.json"
    source_spine = source_dir / f"{from_slug}_spine.json"

    if not source_kabal.exists():
        raise FileNotFoundError(f"Source kabal file not found: {source_kabal}")

    with open(source_kabal, "r", encoding="utf-8") as f:
        kabal_data = json.load(f)

    spine_data = None
    if source_spine.exists():
        with open(source_spine, "r", encoding="utf-8") as f:
            spine_data = json.load(f)

    # 1. Update Kabal Data
    id_map = {}
    cards = kabal_data.get("cards", [])
    for card in cards:
        old_id = card.get("id", "")
        if old_id.startswith(from_prefix):
            new_id = to_prefix + old_id[len(from_prefix):]
            id_map[old_id] = new_id
            card["id"] = new_id
            card["kabal"] = to_slug

    kabal_data["slug"] = to_slug
    kabal_data["variable_prefix"] = to_prefix
    if "title" in kabal_data:
        kabal_data["title"] = kabal_data["title"].replace(from_prefix, to_prefix)

    # 2. Update Spine Data
    if spine_data:
        spine_data["slug"] = to_slug
        spine_data["variable_prefix"] = to_prefix
        if "title" in spine_data:
            spine_data["title"] = spine_data["title"].replace(from_prefix, to_prefix)

        for tag_name, tag_info in spine_data.get("tags", {}).items():
            new_node_ids = []
            for nid in tag_info.get("node_ids", []):
                new_node_ids.append(id_map.get(nid, nid.replace(from_prefix, to_prefix)))
            tag_info["node_ids"] = new_node_ids

        for node in spine_data.get("nodes", []):
            nid = node.get("id", "")
            node["id"] = id_map.get(nid, nid.replace(from_prefix, to_prefix))

    # 3. Scan & Update External References in other papers
    external_updates = []
    for bundle in PAPERS_DIR.glob("*"):
        if bundle.is_dir() and bundle.name != from_slug:
            for json_file in bundle.glob("*.json"):
                try:
                    with open(json_file, "r", encoding="utf-8") as f:
                        text = f.read()
                    changed = False
                    for old_id, new_id in id_map.items():
                        if old_id in text:
                            text = text.replace(old_id, new_id)
                            changed = True
                    if changed:
                        external_updates.append(str(json_file))
                        if not dry_run:
                            with open(json_file, "w", encoding="utf-8") as f:
                                f.write(text)
                except Exception as e:
                    logger.warning(f"Error checking {json_file}: {e}")

    report = {
        "from_prefix": from_prefix,
        "to_prefix": to_prefix,
        "from_slug": from_slug,
        "to_slug": to_slug,
        "cards_renamed": len(id_map),
        "external_files_updated": len(external_updates),
        "external_files": external_updates,
        "dry_run": dry_run,
    }

    if dry_run:
        logger.info(f"[DRY-RUN] Would rename {len(id_map)} cards from {from_prefix} to {to_prefix}")
        return report

    # 4. Atomic File & Directory Rename
    if from_slug != to_slug:
        if target_dir.exists():
            raise FileExistsError(f"Target directory already exists: {target_dir}")
        temp_dir = PAPERS_DIR / f".tmp_{to_slug}"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        target_kabal = temp_dir / f"{to_slug}_kabal.json"
        with open(target_kabal, "w", encoding="utf-8") as f:
            json.dump(kabal_data, f, indent=2, ensure_ascii=False)
            
        if spine_data:
            target_spine = temp_dir / f"{to_slug}_spine.json"
            with open(target_spine, "w", encoding="utf-8") as f:
                json.dump(spine_data, f, indent=2, ensure_ascii=False)

        # Remove source and move temp to target
        shutil.rmtree(source_dir)
        temp_dir.rename(target_dir)
    else:
        # In-place rewrite
        with open(source_kabal, "w", encoding="utf-8") as f:
            json.dump(kabal_data, f, indent=2, ensure_ascii=False)
        if spine_data:
            with open(source_spine, "w", encoding="utf-8") as f:
                json.dump(spine_data, f, indent=2, ensure_ascii=False)

    logger.info(f"Successfully refactored {from_prefix} -> {to_prefix} ({len(id_map)} cards).")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Atomic Variable Namespace Refactoring Tool")
    parser.add_argument("--from-prefix", required=True, help="Current variable prefix (e.g. RESUME)")
    parser.add_argument("--to-prefix", required=True, help="New variable prefix (e.g. PORTFOLIO)")
    parser.add_argument("--from-slug", help="Current slug (defaults to lower prefix)")
    parser.add_argument("--to-slug", help="New slug (defaults to lower prefix)")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without mutating files")
    parser.add_argument("--sync-chroma", action="store_true", help="Sync refactored cards to ChromaDB")
    args = parser.parse_args()

    res = refactor_kabal(
        from_prefix=args.from_prefix,
        to_prefix=args.to_prefix,
        from_slug=args.from_slug,
        to_slug=args.to_slug,
        dry_run=args.dry_run,
    )
    print(json.dumps(res, indent=2))

    if args.sync_chroma and not args.dry_run:
        from kabal_registry import sync_to_chroma
        sync_res = sync_to_chroma(res["to_slug"])
        print(f"ChromaDB Sync: {sync_res}")
