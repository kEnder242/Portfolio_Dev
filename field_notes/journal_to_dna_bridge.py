#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[FEAT-592] Historical Journal to DNA Manifest Ingestion Bridge (journal_to_dna_bridge.py)
Purpose: Scans data/journal_ledger.jsonl and historical gem archives for Rank 4/5 entries,
         transforms them into standard polymorphic DNA cards (WIS / DISC), and merges them
         into wisdom_data.json and dna_manifest.json without duplicate clobbering.
"""

import os
import sys
import json
import time
import re
import hashlib
import datetime
import argparse
import logging
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
LEDGER_PATH = DATA_DIR / "journal_ledger.jsonl"
WISDOM_DATA_PATH = DATA_DIR / "wisdom_data.json"
MANIFEST_PATH = DATA_DIR / "dna_manifest.json"
DNA_BUILD_SCRIPT = BASE_DIR / "dna_forge_build.py"
CHROMA_SYNC_SCRIPT = BASE_DIR.parent / "sync_chroma_dna.py"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [JOURNAL->DNA BRIDGE] %(message)s")
logger = logging.getLogger("journal_bridge")


def get_gem_fingerprint(text: str) -> str:
    """Deterministic hash for deduplicating dialogue or milestone findings."""
    cleaned = re.sub(r"\s+", " ", text.strip().lower())
    return hashlib.md5(cleaned.encode("utf-8")).hexdigest()[:12]


def map_theme_and_bucket(text: str, tags: list = None) -> tuple[str, str]:
    """Classifies theme and bucket_id based on keywords."""
    combined = (text + " " + " ".join(tags or [])).lower()
    if any(k in combined for k in ["security", "rakp", "rmcp", "cve", "auth", "vulnerability", "cert"]):
        return "Security & Manageability", "bucket_security_manageability"
    elif any(k in combined for k in ["peci", "i2c", "ipmi", "sensor", "telemetry", "sideband", "bmc", "hardware"]):
        return "Silicon Validation Methodology", "bucket_silicon_validation"
    elif any(k in combined for k in ["framework", "automation", "pytest", "script", "library", "tool", "sdk", "api"]):
        return "Systems Architecture & Automation", "bucket_systems_architecture"
    elif any(k in combined for k in ["team", "leadership", "mentorship", "process", "culture", "strategy"]):
        return "Engineering Leadership", "bucket_engineering_leadership"
    return "Systems Architecture & Automation", "bucket_systems_architecture"


def extract_title_and_narrative(dialogue: str) -> tuple[str, str, str]:
    """Parses dialogue entry into trigger/question, milestone title, and evidence."""
    lines = [l.strip() for l in dialogue.split("\n") if l.strip()]
    trigger = ""
    finding = ""
    evidence = ""

    for line in lines:
        if line.startswith("User:"):
            trigger = line.replace("User:", "").strip()
        elif line.startswith("Pinky:"):
            finding = line.replace("Pinky:", "").strip()
        elif line.startswith("Evidence:"):
            evidence = line.replace("Evidence:", "").strip()

    # Extract title from finding or trigger
    clean_finding = re.sub(r"^In \d{4}(-\d{2})*, the milestone was:\s*", "", finding, flags=re.IGNORECASE).strip()
    title = clean_finding[:80].rstrip(".") if clean_finding else (trigger[:80].rstrip(".") if trigger else "Validation Finding")
    narrative = clean_finding if clean_finding else (evidence if evidence else dialogue[:200])

    return title, narrative, evidence


def run_bridge(dry_run: bool = False, min_rank: int = 4) -> int:
    """Executes the ingestion bridge from journal_ledger.jsonl to wisdom_data.json."""
    if not LEDGER_PATH.exists():
        logger.warning(f"Journal ledger not found at {LEDGER_PATH}. Nothing to bridge.")
        return 0

    # 1. Load existing wisdom cards & decisions
    existing_cards = []
    if WISDOM_DATA_PATH.exists():
        try:
            with open(WISDOM_DATA_PATH, "r", encoding="utf-8") as f:
                existing_cards = json.load(f)
        except Exception as e:
            logger.error(f"Error loading existing wisdom_data.json: {e}")
            existing_cards = []

    decisions = {}
    decisions_file = DATA_DIR / "dna_decisions.json"
    if decisions_file.exists():
        try:
            with open(decisions_file, "r", encoding="utf-8") as f:
                decisions = json.load(f).get("decisions", {})
        except Exception:
            pass

    # Map existing fingerprints and IDs
    existing_fps = set()
    highest_id_num = 0

    for card in existing_cards:
        card_id = card.get("id", "")
        m = re.search(r"WIS-(\d+)", card_id)
        if m:
            highest_id_num = max(highest_id_num, int(m.group(1)))

        origin_text = card.get("origin", {}).get("text", "")
        title = card.get("synthesis", {}).get("title", "")
        if origin_text:
            existing_fps.add(get_gem_fingerprint(origin_text))
        if title:
            existing_fps.add(get_gem_fingerprint(title))

    # Add recorded decisions to fingerprints to prevent re-ingesting rejected/archived items
    for dec_id, dec_info in decisions.items():
        if dec_info.get("decision") in ("REJECTED", "ARCHIVED"):
            existing_fps.add(dec_id)
            if "fingerprint" in dec_info:
                existing_fps.add(dec_info["fingerprint"])

    logger.info(f"Loaded {len(existing_cards)} existing wisdom cards (Highest ID: WIS-{highest_id_num:03d}, {len(decisions)} tracked decisions).")


    # 2. Read journal_ledger.jsonl
    newly_harvested = []
    next_seq = highest_id_num + 1

    with open(LEDGER_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
            except Exception:
                continue

            rank = entry.get("rank", 3)
            if rank < min_rank:
                continue

            dialogue = entry.get("dialogue", "")
            if not dialogue:
                continue

            fp = get_gem_fingerprint(dialogue)
            if fp in existing_fps:
                continue

            title, narrative, evidence = extract_title_and_narrative(dialogue)
            if not title:
                continue

            # Check secondary fingerprint on title
            if get_gem_fingerprint(title) in existing_fps:
                continue

            theme, bucket_id = map_theme_and_bucket(dialogue)
            date_str = str(entry.get("date") or "Historical")
            created_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

            new_card = {
                "id": f"WIS-{next_seq:03d}",
                "theme": theme,
                "paper_order": next_seq,
                "origin": {
                    "author": "jallred",
                    "text": narrative,
                    "source": f"Historical Journal Ledger ({date_str})",
                    "evidence": evidence or "Historical validation telemetry log.",
                    "immutable": False,
                    "created_at": created_iso
                },
                "synthesis": {
                    "title": title,
                    "narrative_context": narrative,
                    "lab_anchors": [
                        "FEAT-592",
                        "BKM-060"
                    ],
                    "review_notes": f"Harvested via [FEAT-592] journal_to_dna_bridge from journal_ledger.jsonl (Rank {rank}).",
                    "last_refined_by": "AGY_BRIDGE",
                    "refinement_version": 1
                },
                "metadata": {
                    "tags": [
                        bucket_id.replace("bucket_", "").replace("_", "-"),
                        "historical-gem",
                        f"rank-{rank}"
                    ],
                    "explicit_links": [
                        "FEAT-592",
                        "BKM-060"
                    ],
                    "aliases": [f"gem_{fp}"],
                    "status": "APPROVED",
                    "bucket_id": bucket_id,
                    "rank": rank
                }
            }

            existing_fps.add(fp)
            existing_fps.add(get_gem_fingerprint(title))
            newly_harvested.append(new_card)
            next_seq += 1

    logger.info(f"✨ Bridge Analysis: Identified {len(newly_harvested)} new high-rank candidate DNA cards.")

    if not newly_harvested:
        logger.info("No new cards to merge. Wisdom DNA is up to date.")
        return 0

    if dry_run:
        logger.info("[DRY RUN] Would write new cards to wisdom_data.json. Exiting cleanly.")
        return len(newly_harvested)

    # 3. Atomic write to wisdom_data.json
    all_cards = existing_cards + newly_harvested
    tmp_path = str(WISDOM_DATA_PATH) + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(all_cards, f, indent=2)
    os.replace(tmp_path, WISDOM_DATA_PATH)
    logger.info(f"💾 Updated {WISDOM_DATA_PATH} ({len(all_cards)} total wisdom cards).")

    # 4. Rebuild DNA Forge site and manifest
    venv_python = BASE_DIR.parent.parent / "HomeLabAI" / ".venv" / "bin" / "python3"
    py_exec = str(venv_python) if venv_python.exists() else sys.executable

    if DNA_BUILD_SCRIPT.exists():
        logger.info("🔨 Triggering dna_forge_build.py to refresh HTML and manifest...")
        try:
            import subprocess
            res = subprocess.run([py_exec, str(DNA_BUILD_SCRIPT)], capture_output=True, text=True, timeout=60)
            if res.returncode == 0:
                logger.info("✅ dna_forge_build.py completed successfully.")
            else:
                logger.warning(f"⚠️ dna_forge_build.py returned code {res.returncode}: {res.stderr}")
        except Exception as e:
            logger.warning(f"⚠️ Error running dna_forge_build.py: {e}")

    # 5. Sync ChromaDB vector collections if script available
    if CHROMA_SYNC_SCRIPT.exists():
        logger.info("📡 Triggering sync_chroma_dna.py to update vector collections...")
        try:
            import subprocess
            res = subprocess.run([py_exec, str(CHROMA_SYNC_SCRIPT)], capture_output=True, text=True, timeout=120)
            if res.returncode == 0:
                logger.info("✅ ChromaDB DNA sync completed successfully.")
            else:
                logger.warning(f"⚠️ ChromaDB DNA sync returned code {res.returncode}: {res.stderr}")
        except Exception as e:
            logger.warning(f"⚠️ Error running ChromaDB DNA sync: {e}")

    return len(newly_harvested)



def main():
    parser = argparse.ArgumentParser(description="[FEAT-592] Historical Journal to DNA Ingestion Bridge")
    parser.add_argument("--dry-run", action="store_true", help="Scan and report candidates without writing files.")
    parser.add_argument("--min-rank", type=int, default=4, help="Minimum gem rank to ingest (default: 4).")
    args = parser.parse_args()

    count = run_bridge(dry_run=args.dry_run, min_rank=args.min_rank)
    logger.info(f"Bridge execution finished ({count} cards processed).")


if __name__ == "__main__":
    main()
