#!/usr/bin/env python3
# refine_wisdom.py [v1.0]
# [FEAT-562 / FEAT-563] Story 77.2 & 77.3: Automated Nightly Wisdom Synthesis Refiner & Deduplication Pass
# Target Silicon: macOS M5 Air (oMLX port 8000 / Headroom port 8002)
# Output: Updates Portfolio_Dev/field_notes/data/wisdom_data.json and pending_review.json

import argparse
import glob
import json
import logging
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
WISDOM_DATA_PATH = DATA_DIR / "wisdom_data.json"
PHILOSOPHY_DATA_PATH = DATA_DIR / "philosophy_data.json"
PENDING_REVIEW_PATH = DATA_DIR / "pending_review.json"
BUCKETS_PATH = DATA_DIR / "buckets.json"

logging.basicConfig(level=logging.INFO, format="[REFINE-WISDOM] %(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("refine_wisdom")


def cosine_similarity(a, b):
    import numpy as np
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def get_chroma_card_embeddings() -> dict:
    """Extract precomputed 384-dim embeddings from ChromaDB (port 8001) without in-process PyTorch."""
    embeddings = {}
    try:
        import chromadb
        client = chromadb.HttpClient(host="127.0.0.1", port=8001)
        client.heartbeat()
        coll = client.get_collection("philosophy_dna")
        res = coll.get(include=["embeddings", "metadatas"])
        if res and res.get("ids") and res.get("embeddings") is not None:
            for cid, emb in zip(res["ids"], res["embeddings"]):
                base_id = cid.split("_")[0]
                embeddings[base_id] = emb
        logger.info(f"Loaded {len(embeddings)} precomputed card embedding(s) from ChromaDB.")
    except Exception as e:
        logger.warning(f"ChromaDB precomputed embedding fetch failed: {e}")
    return embeddings


def compute_lightweight_vector(text: str, dim: int = 128) -> list:
    """Zero-torch deterministic word-token frequency vector for fallback similarity."""
    import math
    import re
    vec = [0.0] * dim
    words = re.findall(r"\w+", text.lower())
    if not words:
        return vec
    for w in words:
        idx = hash(w) % dim
        vec[idx] += 1.0
    norm = math.sqrt(sum(x * x for x in vec))
    if norm > 0:
        vec = [x / norm for x in vec]
    return vec


def run_deduplication(threshold: float = 0.82) -> list:
    """[FEAT-563] Detect duplicate thoughts across wisdom & philosophy cards without destructive merges."""
    logger.info("Running Semantic Deduplication Pass across wisdom collections (zero-torch host guard)...")
    chroma_embs = get_chroma_card_embeddings()

    cards = []
    if WISDOM_DATA_PATH.exists():
        with open(WISDOM_DATA_PATH, "r") as f:
            w_cards = json.load(f)
            if isinstance(w_cards, list):
                for c in w_cards:
                    c["_source_file"] = "wisdom_data.json"
                    cards.append(c)

    if PHILOSOPHY_DATA_PATH.exists():
        with open(PHILOSOPHY_DATA_PATH, "r") as f:
            p_cards = json.load(f)
            if isinstance(p_cards, list):
                for c in p_cards:
                    c["_source_file"] = "philosophy_data.json"
                    cards.append(c)

    if len(cards) < 2:
        logger.info("Fewer than 2 cards loaded. No duplicates possible.")
        return []

    # Prepare representations combining origin quote and narrative context
    vectors = []
    for c in cards:
        cid = c.get("id")
        if cid and cid in chroma_embs:
            vectors.append(("chroma", chroma_embs[cid]))
        else:
            orig = c.get("origin", {}).get("text") or c.get("origin", {}).get("verbatim") or ""
            narr = c.get("synthesis", {}).get("narrative_context") or ""
            txt = f"{orig}\n{narr}".strip()
            vectors.append(("hash", compute_lightweight_vector(txt)))

    flagged_pairs = []

    for i in range(len(cards)):
        for j in range(i + 1, len(cards)):
            if cards[i].get("id") == cards[j].get("id"):
                continue
            # Compare only matching vector types or fallback
            type_a, vec_a = vectors[i]
            type_b, vec_b = vectors[j]
            if type_a == type_b:
                sim = cosine_similarity(vec_a, vec_b)
            else:
                # Recalculate with lightweight vector for cross-comparison if types differ
                orig_a = cards[i].get("origin", {}).get("text") or cards[i].get("origin", {}).get("verbatim") or ""
                orig_b = cards[j].get("origin", {}).get("text") or cards[j].get("origin", {}).get("verbatim") or ""
                sim = cosine_similarity(compute_lightweight_vector(orig_a), compute_lightweight_vector(orig_b))
            if sim >= threshold:
                pair_report = {
                    "card_a": {
                        "id": cards[i].get("id"),
                        "title": cards[i].get("synthesis", {}).get("title"),
                        "source": cards[i].get("_source_file")
                    },
                    "card_b": {
                        "id": cards[j].get("id"),
                        "title": cards[j].get("synthesis", {}).get("title"),
                        "source": cards[j].get("_source_file")
                    },
                    "similarity": round(sim, 4),
                    "flagged_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                }
                flagged_pairs.append(pair_report)
                logger.info(f"🔎 Duplicate Candidate (sim={sim:.3f}): [{cards[i].get('id')}] '{cards[i].get('title', '')[:30]}' <-> [{cards[j].get('id')}] '{cards[j].get('title', '')[:30]}'")

    # Save to pending_review.json
    review_data = {}
    if PENDING_REVIEW_PATH.exists():
        try:
            with open(PENDING_REVIEW_PATH, "r") as pf:
                review_data = json.load(pf)
        except Exception:
            review_data = {}

    review_data["semantic_dedup_candidates"] = flagged_pairs
    review_data["last_dedup_scan_ts"] = int(time.time())

    tmp_path = str(PENDING_REVIEW_PATH) + ".tmp"
    with open(tmp_path, "w") as f:
        json.dump(review_data, f, indent=2)
    os.replace(tmp_path, PENDING_REVIEW_PATH)
    logger.info(f"💾 Recorded {len(flagged_pairs)} duplicate candidate(s) in {PENDING_REVIEW_PATH.name}")
    return flagged_pairs


def call_m5_air_qwen(prompt: str, system_msg: str = "You are the Senior Federated Lab Wisdom Architect.", timeout: int = 35) -> str:
    """Dispatches a low-temperature completion to local M5 Air Qwen 27B."""
    url = "http://192.168.1.46:8000/v1/chat/completions"
    payload = {
        "model": "mlx-community--Qwen3.8-27B-4bit",
        "temperature": 0.2,
        "max_tokens": 800,
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ]
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        res_json = json.loads(resp.read().decode("utf-8"))
        choices = res_json.get("choices", [])
        if choices:
            return choices[0].get("message", {}).get("content", "")
    return ""


def refine_wisdom_card(card: dict, dry_run: bool = False) -> bool:
    """Refines a single card's synthesis layer via M5 Air Qwen 27B."""
    cid = card.get("id", "UNKNOWN")
    origin = card.get("origin", {})
    orig_text = origin.get("text") or origin.get("verbatim", "")
    synthesis = card.get("synthesis", {})

    if not orig_text:
        logger.warning(f"Card {cid} has empty origin text. Skipping.")
        return False

    prompt = f"""[IMMUTABLE ORIGIN VERBATIM]
Author: {origin.get('author', 'jallred')}
Source: {origin.get('source', 'Unknown')}
Text: "{orig_text}"

[CURRENT SYNTHESIS]
Title: {synthesis.get('title', '')}
Narrative Context: {synthesis.get('narrative_context', '')}
Lab Anchors: {synthesis.get('lab_anchors', [])}
Review Notes: {synthesis.get('review_notes', '')}

[TASK]
Refine and tighten the synthesis layer for this immutable axiom.
Requirements:
1. Title: Crisp, authoritative 4-8 word title capturing the architectural insight.
2. Narrative Context: 2-3 precise sentences explaining the problem, the architectural insight, and the failure mode it prevents.
3. Lab Anchors: 2-3 specific Dev_Lab file paths or BKMs (e.g., 'HomeLabAI/src/tests/delegate.py', 'BKM-049', 'BKM-034', 'BKM-046').
4. Review Notes: 1 concise sentence summarizing how this axiom grounds active systems.
5. Tags: 4-5 semantic tags in kebab-case (e.g., ['jitc', 'token-golf', 'memory']).

Respond ONLY with a valid JSON object matching this schema:
{{
  "title": "...",
  "narrative_context": "...",
  "lab_anchors": ["..."],
  "review_notes": "...",
  "tags": ["..."]
}}"""

    logger.info(f"Dispatched refinement request for [{cid}] to M5 Air Qwen 27B...")
    try:
        raw_resp = call_m5_air_qwen(prompt)
        match = re.search(r'\{.*\}', raw_resp, re.DOTALL)
        if not match:
            logger.warning(f"Failed to parse JSON response from M5 Air for {cid}.")
            return False

        parsed = json.loads(match.group(0))
        new_title = parsed.get("title", synthesis.get("title"))
        new_narrative = parsed.get("narrative_context", synthesis.get("narrative_context"))
        new_anchors = parsed.get("lab_anchors", synthesis.get("lab_anchors", []))
        new_review = parsed.get("review_notes", synthesis.get("review_notes", ""))
        new_tags = parsed.get("tags", card.get("metadata", {}).get("tags", []))

        logger.info(f"✨ Refined [{cid}] '{new_title}':\n   Context: {new_narrative[:80]}...\n   Anchors: {new_anchors}")

        if dry_run:
            logger.info(f"[DRY-RUN] Would update {cid} without writing to disk.")
            return True

        # Apply updates
        card.setdefault("synthesis", {})
        card["synthesis"]["title"] = new_title
        card["synthesis"]["narrative_context"] = new_narrative
        card["synthesis"]["lab_anchors"] = new_anchors
        card["synthesis"]["review_notes"] = new_review
        card["synthesis"]["last_refined_by"] = "M5_AIR"
        card["synthesis"]["refinement_version"] = card["synthesis"].get("refinement_version", 1) + 1

        card.setdefault("metadata", {})
        card["metadata"]["tags"] = new_tags
        return True
    except Exception as e:
        logger.error(f"Refinement error for {cid}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Automated Wisdom Synthesis Refiner & Deduplication Pass")
    parser.add_argument("--dedup-only", action="store_true", help="Run semantic deduplication check only")
    parser.add_argument("--all", action="store_true", help="Refine all unrefined cards (refinement_version < 2)")
    parser.add_argument("--id", help="Refine a specific card by ID (e.g. WIS-001)")
    parser.add_argument("--dry-run", action="store_true", help="Simulate refinement without saving to disk")
    args = parser.parse_args()

    # Step 1: Semantic Deduplication Pass
    run_deduplication()

    if args.dedup_only:
        return

    # Step 2: Wisdom Card Refinement
    if not WISDOM_DATA_PATH.exists():
        logger.error(f"{WISDOM_DATA_PATH} not found.")
        sys.exit(1)

    with open(WISDOM_DATA_PATH, "r") as f:
        cards = json.load(f)

    if not isinstance(cards, list):
        logger.error("wisdom_data.json must be a list of cards.")
        sys.exit(1)

    modified_count = 0

    if args.id:
        target = next((c for c in cards if c.get("id") == args.id), None)
        if not target:
            logger.error(f"Card {args.id} not found in {WISDOM_DATA_PATH.name}")
            sys.exit(1)
        if refine_wisdom_card(target, dry_run=args.dry_run):
            modified_count += 1
    else:
        # Candidate search: unrefined cards (refinement_version < 2)
        candidates = [c for c in cards if c.get("synthesis", {}).get("refinement_version", 1) < 2]
        if not candidates:
            logger.info("All cards have reached refinement_version >= 2. Full polish certified.")
            return

        to_refine = candidates if args.all else [candidates[0]]
        for c in to_refine:
            if refine_wisdom_card(c, dry_run=args.dry_run):
                modified_count += 1

    if modified_count > 0 and not args.dry_run:
        tmp_file = str(WISDOM_DATA_PATH) + ".tmp"
        with open(tmp_file, "w") as f:
            json.dump(cards, f, indent=2)
        os.replace(tmp_file, WISDOM_DATA_PATH)
        logger.info(f"💾 Atomically saved {modified_count} refined card(s) to {WISDOM_DATA_PATH.name}")

        # Trigger rebuild of wisdom.html
        build_script = BASE_DIR / "wisdom_build.py"
        if build_script.exists():
            try:
                import subprocess
                res = subprocess.run([sys.executable, str(build_script)], capture_output=True, text=True, timeout=10)
                logger.info(f"Rebuilt wisdom.html: {res.stdout.strip()}")
            except Exception as be:
                logger.warning(f"Could not run wisdom_build.py: {be}")


if __name__ == "__main__":
    main()
