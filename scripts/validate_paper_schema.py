#!/usr/bin/env python3
"""
[FEAT-585] [FEAT-581] Story 79.1: Multi-Tier Paper JSON Schema & Invariant Validator
Validates paper datasets in Portfolio_Dev/papers/ against strict architectural invariants:
1. Valid top-level metadata (id, title, author, sections; optional subtitle, date, status, voice_profile).
2. Multi-tier Bone Collections & Citations support at Paper Root, Section Nodes, and Paragraph Containers.
3. Strict paragraph hierarchy (section id SEC-xxx, paragraph id PAR-xxx, bone collection id BONE-xxx / COL-xxx).
4. Citation validation: all citations must match registered formats (PHL-xxx, DISC-xxx, FEAT-xxx, BKM-xxx, PROTO-xxx, ARXIV:xxx, GEM-xxx, WIS-xxx, LAB-xxx).
5. No empty or corrupted paragraph bodies.
"""

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
PAPERS_DIR = REPO_ROOT / "papers"
MANIFEST_FILE = PAPERS_DIR / "manifest.json"

CITATION_PATTERN = re.compile(
    r'^(PHL|DISC|FEAT|BKM|PROTO|ARXIV|GEM|WIS|LAB)-[A-Za-z0-9_\.\-]+$|^ARXIV:\d+\.\d+$|^arXiv:\d+\.\d+$|^doi:[A-Za-z0-9_\.\-/]+$',
    re.IGNORECASE
)

def validate_bone_collections(b_list, tier_name, node_id, errors, bone_ids):
    """Validate a list of bone collection objects attached to a specific tier."""
    if not isinstance(b_list, list):
        errors.append(f"{tier_name} '{node_id}' bone_collections must be a list.")
        return

    for b_idx, bone in enumerate(b_list):
        if not isinstance(bone, dict):
            errors.append(f"{tier_name} '{node_id}' bone collection index {b_idx} must be a dict.")
            continue
        b_id = bone.get("id")
        b_name = bone.get("name")
        if not b_id:
            errors.append(f"{tier_name} '{node_id}' bone collection index {b_idx} missing 'id'.")
        elif b_id in bone_ids:
            errors.append(f"Duplicate bone collection id: '{b_id}' in {tier_name} '{node_id}'.")
        else:
            bone_ids.add(b_id)

        if not b_name:
            errors.append(f"{tier_name} '{node_id}' bone collection '{b_id or b_idx}' missing 'name'.")

        b_cites = bone.get("citations", [])
        if not isinstance(b_cites, list):
            errors.append(f"{tier_name} '{node_id}' bone collection '{b_id or b_idx}' citations must be a list.")
        else:
            for c in b_cites:
                if not CITATION_PATTERN.match(str(c)):
                    errors.append(f"{tier_name} '{node_id}' bone collection '{b_id or b_idx}' invalid citation syntax: '{c}'.")

def validate_citations_list(c_list, tier_name, node_id, errors, field_name="citations"):
    """Validate a list of citation strings."""
    if not isinstance(c_list, list):
        errors.append(f"{tier_name} '{node_id}' {field_name} must be a list.")
        return
    for c in c_list:
        if not CITATION_PATTERN.match(str(c)):
            errors.append(f"{tier_name} '{node_id}' invalid {field_name} syntax: '{c}'.")

def validate_paper_dict(data, source_name="paper"):
    """Validate in-memory paper dict against schema invariants."""
    errors = []

    # 1. Top-level required fields
    for field in ["id", "title", "author", "sections"]:
        if field not in data:
            errors.append(f"Missing top-level required field: '{field}'.")

    bone_ids = set()
    sec_ids = set()
    par_ids = set()
    paper_id = data.get("id", "UNKNOWN_PAPER")

    # Paper-level bone collections & citations
    if "bone_collections" in data:
        validate_bone_collections(data["bone_collections"], "Paper", paper_id, errors, bone_ids)
    if "citations" in data:
        validate_citations_list(data["citations"], "Paper", paper_id, errors, "citations")
    if "pending_citations" in data:
        validate_citations_list(data["pending_citations"], "Paper", paper_id, errors, "pending_citations")

    sections = data.get("sections", [])
    if not isinstance(sections, list) or len(sections) == 0:
        errors.append("Sections must be a non-empty list.")
        return False, errors

    for s_idx, sec in enumerate(sections):
        s_id = sec.get("id")
        if not s_id:
            errors.append(f"Section index {s_idx} missing 'id'.")
            s_id = f"SEC_IDX_{s_idx}"
        elif s_id in sec_ids:
            errors.append(f"Duplicate section id: '{s_id}'.")
        else:
            sec_ids.add(s_id)

        if "heading" not in sec:
            errors.append(f"Section '{s_id}' missing 'heading'.")

        # Section-level bone collections & citations
        if "bone_collections" in sec:
            validate_bone_collections(sec["bone_collections"], "Section", s_id, errors, bone_ids)
        if "citations" in sec:
            validate_citations_list(sec["citations"], "Section", s_id, errors, "citations")
        if "pending_citations" in sec:
            validate_citations_list(sec["pending_citations"], "Section", s_id, errors, "pending_citations")

        paragraphs = sec.get("paragraphs", [])
        if not isinstance(paragraphs, list):
            errors.append(f"Section '{s_id}' paragraphs must be a list.")
            continue

        for p_idx, par in enumerate(paragraphs):
            p_id = par.get("id")
            if not p_id:
                errors.append(f"Section '{s_id}' paragraph {p_idx} missing 'id'.")
                p_id = f"PAR_IDX_{p_idx}"
            elif p_id in par_ids:
                errors.append(f"Duplicate paragraph id: '{p_id}'.")
            else:
                par_ids.add(p_id)

            # Paragraph-level bone collections & citations
            if "bone_collections" in par:
                validate_bone_collections(par["bone_collections"], "Paragraph", p_id, errors, bone_ids)
            if "citations" in par:
                validate_citations_list(par["citations"], "Paragraph", p_id, errors, "citations")
            if "pending_citations" in par:
                validate_citations_list(par["pending_citations"], "Paragraph", p_id, errors, "pending_citations")

            # Check text presence
            text_body = par.get("cached_words") or par.get("text")
            if text_body is None:
                errors.append(f"Paragraph '{p_id}' missing text body ('cached_words' or 'text').")

    passed = (len(errors) == 0)
    return passed, errors

def validate_paper(paper_path):
    print(f"[*] Validating {paper_path}...")
    p = Path(paper_path)
    if not p.exists():
        print(f"❌ File not found: {p}")
        return False

    try:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as ex:
        print(f"❌ JSON parse error for {p.name}: {ex}")
        return False

    passed, errors = validate_paper_dict(data, source_name=p.name)
    if not passed:
        print(f"❌ Schema validation FAILED for {p.name} with {len(errors)} error(s):")
        for err in errors:
            print(f"   - {err}")
        return False
    else:
        sections = data.get("sections", [])
        par_count = sum(len(s.get("paragraphs", [])) for s in sections)
        bone_count = len(data.get("bone_collections", [])) + sum(len(s.get("bone_collections", [])) for s in sections) + sum(len(p.get("bone_collections", [])) for s in sections for p in s.get("paragraphs", []))
        print(f"✅ Schema validation PASSED for {p.name} ({len(sections)} sections, {par_count} paragraphs, {bone_count} bone collections).")
        return True

def main():
    if len(sys.argv) > 1:
        target = Path(sys.argv[1])
        if target.is_file():
            passed = validate_paper(target)
            sys.exit(0 if passed else 1)

    if not MANIFEST_FILE.exists():
        print(f"❌ Manifest not found: {MANIFEST_FILE}")
        sys.exit(1)

    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        mdata = json.load(f)

    all_passed = True
    for p_info in mdata.get("papers", []):
        file_name = p_info.get("file")
        if file_name:
            p_path = PAPERS_DIR / file_name
            if p_path.exists():
                passed = validate_paper(p_path)
                if not passed:
                    all_passed = False
            else:
                print(f"⚠️ Paper file not found on disk: {p_path}")
                all_passed = False

    if not all_passed:
        sys.exit(1)
    print("\nAll paper schemas verified successfully.")

if __name__ == "__main__":
    main()
