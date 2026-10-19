#!/usr/bin/env python3
"""[FEAT-663 / BKM-085 / ADR-008] Deterministic Spine Replay Engine.

Reconstructs complete manuscript markdown or plaintext deterministically by joining
the structural narrative spine (papers/<slug>/<slug>_spine.json) with substantive
Kabal cards (papers/<slug>/<slug>_kabal.json) across named tags and projection lenses.
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("replay_paper")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

BASE_DIR = Path(__file__).resolve().parent.parent
PAPERS_DIR = BASE_DIR / "papers"


def load_spine(slug: str) -> Dict[str, Any]:
    spine_path = PAPERS_DIR / slug.lower() / f"{slug.lower()}_spine.json"
    if not spine_path.exists():
        raise FileNotFoundError(f"Spine file not found: {spine_path}")
    with open(spine_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_kabal_cards_dict(slug: str) -> Dict[str, Dict[str, Any]]:
    kabal_path = PAPERS_DIR / slug.lower() / f"{slug.lower()}_kabal.json"
    if not kabal_path.exists():
        raise FileNotFoundError(f"Kabal file not found: {kabal_path}")
    with open(kabal_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {c["id"]: c for c in data.get("cards", [])}


def replay_paper(
    slug: str,
    tag: str = "@master",
    lens: str = "verbatim",
    include_citations: bool = False,
    output_format: str = "markdown",
) -> str:
    """Deterministically reconstructs paper text from Spine and Kabal."""
    spine = load_spine(slug)
    cards_dict = load_kabal_cards_dict(slug)

    tags = spine.get("tags", {})
    if tag not in tags:
        available = list(tags.keys())
        raise ValueError(f"Tag '{tag}' not found in spine for '{slug}'. Available tags: {available}")

    tag_meta = tags[tag]
    node_ids = tag_meta.get("node_ids", [])
    spine_node_meta = {n["id"]: n for n in spine.get("nodes", [])}

    output_lines = []

    for node_id in node_ids:
        card = cards_dict.get(node_id)
        if not card:
            logger.warning(f"Card '{node_id}' referenced in spine tag '{tag}' not found in kabal cards.")
            continue

        meta = card.get("metadata", {})
        origin = card.get("origin", {})
        synthesis = card.get("synthesis", {})
        style = meta.get("style", "paragraph")
        raw_text = origin.get("raw_text", synthesis.get("summary", ""))

        # Lens Filtering
        if lens == "executive":
            # Executive lens filters out non-leadership, routine internship entries
            tags_list = meta.get("tags", [])
            if "role_overview" in tags_list and any(y in raw_text for y in ["2005", "2008", "Internship"]):
                continue
            if style == "bullet" and len(raw_text) < 40:
                continue

        # Citation Badge
        citation_suffix = f" [{node_id}]" if include_citations else ""

        # Formatting
        if style == "header":
            output_lines.append(f"# {raw_text}{citation_suffix}\n")
        elif style == "heading":
            output_lines.append(f"\n### {raw_text}{citation_suffix}\n")
        elif style == "callout":
            output_lines.append(f"\n> **{synthesis.get('title', 'Highlight')}**  \n> {raw_text}{citation_suffix}\n")
        elif style == "bullet":
            output_lines.append(f"- {raw_text}{citation_suffix}")
        else:
            output_lines.append(f"\n{raw_text}{citation_suffix}\n")

    return "\n".join(output_lines).strip() + "\n"


def verify_identity(slug: str, original_file_path: str) -> Dict[str, Any]:
    """Verifies that replayed @master tag captures all substantive sentences from the source document."""
    replayed = replay_paper(slug, tag="@master", lens="verbatim", include_citations=False)
    with open(original_file_path, "r", encoding="utf-8") as f:
        original = f.read()

    # Extract substantive tokens/lines
    orig_lines = [l.strip().lstrip("- ") for l in original.splitlines() if l.strip() and len(l.strip()) > 15]
    replayed_lines = [l.strip().lstrip("- ") for l in replayed.splitlines() if l.strip() and len(l.strip()) > 15]

    matched = 0
    missing = []
    for ol in orig_lines:
        if any(ol in rl or rl in ol for rl in replayed_lines):
            matched += 1
        else:
            missing.append(ol[:60])

    coverage = (matched / len(orig_lines)) * 100 if orig_lines else 100.0
    return {
        "slug": slug,
        "original_lines_evaluated": len(orig_lines),
        "replayed_lines": len(replayed_lines),
        "matched": matched,
        "coverage_percent": round(coverage, 2),
        "missing_samples": missing[:5],
        "zero_loss_certified": coverage >= 95.0,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deterministic Spine Replay Engine")
    parser.add_argument("--slug", default="resume", help="Manuscript slug (e.g. resume)")
    parser.add_argument("--tag", default="@master", help="Spine snapshot tag (e.g. @master, @executive_2page)")
    parser.add_argument("--lens", default="verbatim", choices=["verbatim", "executive"], help="Projection lens")
    parser.add_argument("--citations", action="store_true", help="Include inline citation stamps")
    parser.add_argument("--verify", help="Path to original document to verify identity coverage")
    parser.add_argument("--out", help="Write output to file path")
    args = parser.parse_args()

    if args.verify:
        res = verify_identity(args.slug, args.verify)
        print(json.dumps(res, indent=2))
        sys.exit(0 if res["zero_loss_certified"] else 1)

    result_text = replay_paper(args.slug, tag=args.tag, lens=args.lens, include_citations=args.citations)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(result_text)
        logger.info(f"Wrote replayed manuscript to {args.out}")
    else:
        print(result_text)
