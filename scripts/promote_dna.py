#!/usr/bin/env python3
"""
[FEAT-628 / BKM-060 / BKM-071] Document-Scoped DNA Promotion Gate & Sync Pipeline

Graduates quarantined document-level DNA (DOC-<paper>-<idx>) from PAPER-<id>_spine.json
into master global lab memory (WIS-xxx or INS-xxx in Portfolio_Dev/dna/).
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PORTFOLIO_DIR = os.path.dirname(SCRIPT_DIR)
DEFAULT_DNA_DIR = os.path.join(PORTFOLIO_DIR, "dna")
DEFAULT_PAPERS_DIR = os.path.join(PORTFOLIO_DIR, "field_notes", "data", "papers")


def atomic_write_json(path: str, data: any):
    """Atomically write JSON data to disk."""
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    tmp_path = f"{path}.tmp.{os.getpid()}"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp_path, path)


def get_next_global_id(items: list, prefix: str) -> tuple[str, int]:
    """Calculate the next sequential ID (e.g. WIS-490 or INS-042)."""
    max_num = 0
    pattern = re.compile(rf"^{prefix}-(\d+)$")
    for item in items:
        item_id = item.get("id", "")
        match = pattern.match(item_id)
        if match:
            num = int(match.group(1))
            if num > max_num:
                max_num = num
    next_num = max_num + 1
    if prefix == "INS":
        formatted_id = f"{prefix}-{next_num:03d}"
    else:
        formatted_id = f"{prefix}-{next_num}"
    return formatted_id, next_num


def promote_document_dna(
    paper_id: str,
    doc_dna_id: str,
    target_domain: str = "WIS",
    dna_dir: str = None,
    papers_dir: str = None,
    dry_run: bool = False,
    run_sync: bool = True,
) -> dict:
    """
    Promote a quarantined document DNA record into global lab memory.
    """
    dna_dir = dna_dir or DEFAULT_DNA_DIR
    papers_dir = papers_dir or DEFAULT_PAPERS_DIR
    target_domain = target_domain.upper()

    if target_domain not in ("WIS", "INS"):
        raise ValueError(f"Invalid target domain '{target_domain}'. Must be 'WIS' or 'INS'.")

    # Clean paper_id
    clean_paper = paper_id.replace("PAPER-", "")
    spine_file = os.path.join(papers_dir, f"PAPER-{clean_paper}_spine.json")

    if not os.path.exists(spine_file):
        raise FileNotFoundError(f"Spine file not found at: {spine_file}")

    with open(spine_file, "r", encoding="utf-8") as f:
        spine_data = json.load(f)

    doc_dna_list = spine_data.get("document_dna", [])
    target_record = None
    target_idx = -1

    for idx, rec in enumerate(doc_dna_list):
        if rec.get("doc_dna_id") == doc_dna_id:
            target_record = rec
            target_idx = idx
            break

    if target_record is None:
        raise KeyError(f"Document DNA '{doc_dna_id}' not found in {spine_file}")

    if target_record.get("promoted_to_global"):
        existing_id = target_record["promoted_to_global"]
        raise ValueError(f"Document DNA '{doc_dna_id}' is already promoted to '{existing_id}'")

    # Load target global dataset
    if target_domain == "WIS":
        global_file = os.path.join(dna_dir, "wisdom_data.json")
        prefix = "WIS"
        default_theme = "Career Engineering & Technical Wisdom"
    else:
        global_file = os.path.join(dna_dir, "inspiration_data.json")
        prefix = "INS"
        default_theme = "Systems Architecture & Design Philosophy"

    if not os.path.exists(global_file):
        raise FileNotFoundError(f"Global DNA file not found: {global_file}")

    with open(global_file, "r", encoding="utf-8") as f:
        global_items = json.load(f)

    new_global_id, next_num = get_next_global_id(global_items, prefix)
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # Extract clean tags from theme string
    theme_str = target_record.get("theme", "")
    tags = [t.strip("#").lower() for t in theme_str.split() if t.strip()]
    tags.extend(["promoted-doc-dna", f"paper-{clean_paper.lower()}"])
    tags = sorted(list(set(tags)))

    citations = target_record.get("citations", [])

    new_card = {
        "id": new_global_id,
        "theme": theme_str if theme_str else default_theme,
        "paper_order": next_num,
        "origin": {
            "author": "jallred",
            "text": target_record.get("text", ""),
            "source": f"PAPER-{clean_paper} ({target_record.get('origin_node_id', 'unknown')}) -> {doc_dna_id}",
            "immutable": True,
            "created_at": now_iso,
        },
        "synthesis": {
            "title": target_record.get("title", f"Promoted DNA from PAPER-{clean_paper}"),
            "narrative_context": target_record.get("text", ""),
            "lab_anchors": citations if citations else [f"FEAT-{clean_paper}"],
            "review_notes": f"Graduated from document-scoped DNA {doc_dna_id} in PAPER-{clean_paper}.",
            "last_refined_by": "AGY",
            "refinement_version": 1,
            "mutations": [],
            "revisions": [],
        },
        "metadata": {
            "tags": tags,
            "explicit_links": citations,
            "aliases": [doc_dna_id],
            "status": "APPROVED",
            "bucket_id": f"bucket_promoted_{target_domain.lower()}",
        },
    }

    if not dry_run:
        # 1. Append to global dataset
        global_items.append(new_card)
        atomic_write_json(global_file, global_items)

        # 2. Update spine document DNA record
        doc_dna_list[target_idx]["promoted_to_global"] = new_global_id
        doc_dna_list[target_idx]["promoted_at"] = now_iso
        spine_data["document_dna"] = doc_dna_list
        spine_data["updated_at"] = now_iso
        atomic_write_json(spine_file, spine_data)

        # 3. Trigger ChromaDB sync if requested
        if run_sync:
            sync_script = os.path.join(PORTFOLIO_DIR, "sync_chroma_dna.py")
            venv_python = os.path.expanduser("~/Dev_Lab/HomeLabAI/.venv/bin/python3")
            if os.path.exists(sync_script) and os.path.exists(venv_python):
                try:
                    subprocess.run(
                        [venv_python, sync_script],
                        check=True,
                        capture_output=True,
                        text=True,
                    )
                except Exception as e:
                    print(f"⚠️ [WARN] ChromaDB sync failed (non-fatal): {e}", file=sys.stderr)

    return {
        "status": "success",
        "global_id": new_global_id,
        "doc_dna_id": doc_dna_id,
        "paper_id": f"PAPER-{clean_paper}",
        "target_domain": target_domain,
        "dry_run": dry_run,
        "card": new_card,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Promote document-scoped DNA into global lab memory."
    )
    parser.add_argument("--paper", required=True, help="Paper ID (e.g. RESUME)")
    parser.add_argument("--doc-dna", required=True, help="Document DNA ID (e.g. DOC-RESUME-001)")
    parser.add_argument(
        "--target-domain",
        default="WIS",
        choices=["WIS", "INS", "wis", "ins"],
        help="Target global DNA domain (WIS or INS)",
    )
    parser.add_argument("--data-dir", default=None, help="Path to field_notes/data")
    parser.add_argument("--dna-dir", default=None, help="Path to dna/ directory")
    parser.add_argument("--dry-run", action="store_true", help="Simulate promotion without writing")
    parser.add_argument("--no-sync", action="store_true", help="Skip ChromaDB sync after write")

    args = parser.parse_args()

    papers_dir = None
    if args.data_dir:
        papers_dir = os.path.join(args.data_dir, "papers")

    try:
        res = promote_document_dna(
            paper_id=args.paper,
            doc_dna_id=args.doc_dna,
            target_domain=args.target_domain,
            dna_dir=args.dna_dir,
            papers_dir=papers_dir,
            dry_run=args.dry_run,
            run_sync=not args.no_sync,
        )
        print(
            f"✅ Successfully promoted {res['doc_dna_id']} -> {res['global_id']} (Domain: {res['target_domain']})"
        )
        if res["dry_run"]:
            print("🔍 [DRY RUN] No files modified.")
    except Exception as e:
        print(f"❌ Promotion failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
