#!/usr/bin/env python3
# Copyright 2025-2026 Jason Allred
# SPDX-License-Identifier: Apache-2.0
"""
[Story 112.170 / VIBE-008 / LOOP-006 / FEAT-683]
Targeted Focal/Coaching Draft Mapping & Precision Drift Excision Engine.

Executes:
1. Focal Audit & Inventory across /home/jallred/knowledge_base/ (2007-2024)
2. Dual-Bucket Anchor Separation:
   - Positive Anchors (Preserve & Amplify): Deliverables, accomplishments, platform bring-ups
   - Negative Anchors (Tripwire Sentinel & Scrub): Managerial developmental critique, coaching, HR rating verbiage
3. ClaraDB (ChromaDB :8001) Negative Vector Similarity Query (distance < 0.35)
4. Lakehouse Scan across Portfolio_Dev/field_notes/data/ and www_deploy/data/
5. Generation of focal_draft_mapping.json tracking multi-year windows
6. Surgical Hybrid Scrub on mapped gems (Drop pure coaching / excise critique phrases from technical gems)
7. ChromaDB cleanup of tainted artifacts
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PORTFOLIO_ROOT = BASE_DIR.parent
DATA_DIR = BASE_DIR / "data"
WWW_DATA_DIR = PORTFOLIO_ROOT.parent / "www_deploy" / "data"
KB_DIR = Path("/home/jallred/knowledge_base")

# Import ChromaDB if available
try:
    import chromadb
    CHROMA_CLIENT = chromadb.HttpClient(host="127.0.0.1", port=8001)
except Exception as e:
    CHROMA_CLIENT = None
    print(f"[WARN] ChromaDB not available: {e}")

def load_negative_patterns():
    """Loads generic structural rules and merges external private sentinels (LAB-125)."""
    patterns = [
        (r"\bAREAS FOR IMPROVEMENT\b", "areas_for_improvement"),
        (r"\bAREAS FOR DEVELOPMENT\b", "areas_for_development"),
        (r"\bImprovement/Development Areas\b", "improvement_dev_areas"),
        (r"\bEVALUATION:\s*DEVELOPMENT AREAS\b", "eval_dev_areas"),
        (r"\bResults Coaching\b", "results_coaching"),
        (r"\bBehaviors Coaching\b", "behaviors_coaching"),
        (r"\bPerformance Summary with Rating\b", "perf_summary_rating"),
        (r"\bSuccessful performance rating\b", "successful_perf_rating"),
        (r"\brated\s+successful\b", "rated_successful"),
        (r"\bRating:\s*(?:Successful|Needs Improvement|Exceeds)\b", "rating_header"),
    ]
    ext_path = Path.home() / ".config/homelab/focal_negative_anchors.json"
    if ext_path.exists():
        try:
            ext_data = json.loads(ext_path.read_text(encoding="utf-8"))
            for idx, pat in enumerate(ext_data.get("negative_patterns", [])):
                regex = pat if pat.startswith(r"\b") else rf"\b{pat}\b"
                patterns.append((regex, f"ext_negative_pattern_{idx}"))
        except Exception:
            pass
    return patterns

NEGATIVE_PATTERNS = load_negative_patterns()


def audit_review_documents():
    """Task 112.170.1: Extract authoritative positive and negative anchors."""
    print("=== [1] AUDITING AUTHORITATIVE REVIEW ARCHIVE ===")
    review_txt = KB_DIR / "Performance review 2008-2018.txt"
    insights_txt = KB_DIR / "11066402 Insights 2019-2024.txt"

    positive_anchors = []
    negative_anchors = []

    if review_txt.exists():
        text = review_txt.read_text(encoding="utf-8", errors="ignore")
        # Split review sections
        sections = re.split(r"\n(?=(?:Review Period|Job Title[:\s]|Oct`2007))", text)
        for sec in sections:
            if not sec.strip():
                continue
            # Extract year
            y_m = re.search(r"\b(20\d{2})\b", sec)
            year = int(y_m.group(1)) if y_m else 2008

            # Extract Deliverables / Accomplishments (Positive)
            acc_m = re.search(r"(?:Key Accomplishments|KEY ACCOMPLISHMENTS|Deliverables)(.*?)(?=\n(?:Strengths|Evaluation|AREAS|EVALUATION:\s*DEV|Improvement|PERFORMANCE|$))", sec, re.DOTALL | re.IGNORECASE)
            if acc_m:
                paras = [p.strip() for p in acc_m.group(1).split("\n\n") if len(p.strip()) > 30]
                for p in paras:
                    header = p.splitlines()[0][:80]
                    positive_anchors.append({
                        "era": str(year),
                        "type": "accomplishment",
                        "anchor_title": header,
                        "text_snippet": p[:250]
                    })

            # Extract Areas for Improvement / Development (Negative)
            dev_m = re.search(r"(?:AREAS FOR IMPROVEMENT|EVALUATION:\s*DEVELOPMENT AREAS|Improvement/Development Areas)(.*?)(?=\n(?:PERFORMANCE|Job Title|Review Period|$))", sec, re.DOTALL | re.IGNORECASE)
            if dev_m:
                paras = [p.strip() for p in dev_m.group(1).split("\n\n") if len(p.strip()) > 30]
                for p in paras:
                    header = p.splitlines()[0][:80]
                    negative_anchors.append({
                        "era": str(year),
                        "type": "coaching_critique",
                        "anchor_title": header,
                        "text_snippet": p[:250]
                    })

    if insights_txt.exists():
        text = insights_txt.read_text(encoding="utf-8", errors="ignore")
        sections = re.split(r"\n(?=(?:Q[1-4]\s+20\d{2}|\d{1,2}/\d{1,2}/20\d{2}))", text)
        for sec in sections:
            if not sec.strip():
                continue
            y_m = re.search(r"\b(20\d{2})\b", sec)
            year = int(y_m.group(1)) if y_m else 2024

            # Positive: Results Feedback & Behaviors Feedback
            rf_m = re.search(r"Results Feedback:?(.*?)(?=(?:Results Coaching|Behaviors Feedback|Behaviors Coaching|$))", sec, re.DOTALL | re.IGNORECASE)
            if rf_m:
                lines = [l.strip() for l in rf_m.group(1).splitlines() if len(l.strip()) > 20]
                for l in lines:
                    positive_anchors.append({
                        "era": str(year),
                        "type": "results_feedback",
                        "anchor_title": l[:60],
                        "text_snippet": l
                    })

            # Negative: Results Coaching & Behaviors Coaching
            rc_m = re.search(r"(?:Results Coaching|Behaviors Coaching):?(.*?)(?=(?:Results Feedback|Behaviors Feedback|Q[1-4]|$))", sec, re.DOTALL | re.IGNORECASE)
            if rc_m:
                lines = [l.strip() for l in rc_m.group(1).splitlines() if len(l.strip()) > 15 and not l.strip().startswith("(TBD)")]
                for l in lines:
                    negative_anchors.append({
                        "era": str(year),
                        "type": "coaching_directive",
                        "anchor_title": l[:60],
                        "text_snippet": l
                    })

    print(f"  Cataloged {len(positive_anchors)} Positive Anchors (Deliverables).")
    print(f"  Cataloged {len(negative_anchors)} Negative Anchors (Coaching/Critique).")
    return positive_anchors, negative_anchors


def query_claradb_sentinels(negative_anchors):
    """Task 112.170.5: Query ClaraDB vector collections for negative coaching similarity (distance < 0.35)."""
    print("=== [2] CLARADB VECTOR PROXIMITY AUDIT (ChromaDB :8001) ===")
    if not CHROMA_CLIENT:
        return []

    flagged_artifacts = []
    ext_path = Path.home() / ".config/homelab/focal_negative_anchors.json"
    query_texts = [
        "AREAS FOR IMPROVEMENT: Performance evaluation and coaching review feedback.",
        "Results Coaching: Quarterly deliverable and milestones coaching.",
        "Behaviors Coaching: Communication and process improvement feedback.",
        "Successful performance rating Performance Summary.",
    ]
    if ext_path.exists():
        try:
            ext_data = json.loads(ext_path.read_text(encoding="utf-8"))
            custom_queries = ext_data.get("vector_negative_queries", [])
            if custom_queries:
                query_texts = custom_queries
        except Exception:
            pass

    for col_name in ["wisdom_dna", "long_term_wisdom"]:
        try:
            col = CHROMA_CLIENT.get_collection(col_name)
            res = col.query(query_texts=query_texts, n_results=5)
            for q_idx, q in enumerate(query_texts):
                ids = res["ids"][q_idx]
                dists = res["distances"][q_idx]
                docs = res["documents"][q_idx]
                metas = res["metadatas"][q_idx]
                for doc_id, dist, doc, meta in zip(ids, dists, docs, metas):
                    # Flag hits with high proximity (distance < 0.38) or containing explicit rating text
                    is_rating = any(r in doc for r in ["Successful performance rating", "Performance Summary: Successful", "Performance Summary with Rating"])
                    if dist < 0.35 or is_rating:
                        flagged_artifacts.append({
                            "collection": col_name,
                            "id": doc_id,
                            "distance": round(float(dist), 4),
                            "matched_query": q[:50],
                            "document": doc,
                            "metadata": meta,
                            "is_pure_rating": is_rating
                        })
        except Exception as e:
            print(f"  [WARN] Failed to query {col_name}: {e}")

    # Deduplicate by (collection, id)
    seen = set()
    deduped = []
    for a in flagged_artifacts:
        k = (a["collection"], a["id"])
        if k not in seen:
            seen.add(k)
            deduped.append(a)

    print(f"  ClaraDB identified {len(deduped)} proximity hits (distance < 0.35 or explicit rating).")
    for d in deduped:
        print(f"    -> [{d['collection']}] {d['id']} (dist={d['distance']}): {repr(d['document'][:80])}")
    return deduped


def scan_and_map_lakehouse():
    """Task 112.170.2: Scan lakehouse datasets and construct focal_draft_mapping.json."""
    print("=== [3] SCANNING LAKEHOUSE FOR DRAFT WINDOWS & ESCAPES ===")
    mappings = []

    for fpath in sorted(DATA_DIR.glob("20*.json")):
        fname = fpath.name
        try:
            events = json.loads(fpath.read_text(encoding="utf-8"))
            if not isinstance(events, list):
                continue
            for idx, ev in enumerate(events):
                summary = str(ev.get("summary", ""))
                evidence = str(ev.get("evidence", ""))
                txt = f"{summary} {evidence}"

                matched_neg = []
                for pat, rule_tag in NEGATIVE_PATTERNS:
                    if re.search(pat, txt, re.IGNORECASE):
                        # Verify word boundary against false positives like "generated successfully"
                        if rule_tag == "rated_successful":
                            if not re.search(r"\brated\s+successful\b", txt, re.IGNORECASE):
                                continue
                        matched_neg.append(rule_tag)

                # Check if this event contains Results Feedback or Key Accomplishments
                has_positive_marker = bool(re.search(r"\b(?:Results Feedback|Key Accomplishments|Strategic Anchor)\b", txt, re.IGNORECASE))

                if matched_neg or has_positive_marker:
                    # Decide disposition
                    # If it has technical commands or registers, do surgical suture; if purely HR/rating, drop
                    has_tech_scars = bool(re.search(r"\b(?:curl|python|pci|setpci|0x[0-9a-f]+|mctp|peci|ipmi|simics|reg|cfg)\b", txt, re.IGNORECASE))
                    if matched_neg:
                        disposition = "SURGICAL_SUTURE" if has_tech_scars else "DROP"
                    else:
                        disposition = "PRESERVE_POSITIVE_ANCHOR"

                    mapping_entry = {
                        "mapping_id": f"MAP-{fname.replace('.json', '')}-{idx:04d}",
                        "source_lakehouse_file": fname,
                        "event_index": idx,
                        "gem_id": ev.get("id"),
                        "date": ev.get("date"),
                        "event_era": ev.get("event_era"),
                        "matched_negative_rules": matched_neg,
                        "has_positive_marker": has_positive_marker,
                        "disposition": disposition,
                        "summary_snippet": summary[:120],
                        "evidence_snippet": evidence[:150]
                    }
                    mappings.append(mapping_entry)
        except Exception as e:
            print(f"  [ERROR] Reading {fpath}: {e}")

    mapping_file = DATA_DIR / "focal_draft_mapping.json"
    mapping_file.write_text(json.dumps(mappings, indent=2), encoding="utf-8")
    print(f"  Generated {mapping_file} with {len(mappings)} mapped windows.")
    return mappings


def execute_precision_hybrid_scrub(mappings, claradb_hits):
    """Task 112.170.3: Execute surgical scrub across Portfolio_Dev/field_notes/data/ and www_deploy/data/."""
    print("=== [4] EXECUTING TARGETED HYBRID SCRUB ===")
    scrub_count = 0
    drop_count = 0

    # 1. Scrub Lakehouse JSONs
    # Group mappings by file
    by_file = {}
    for m in mappings:
        if m["disposition"] in ["DROP", "SURGICAL_SUTURE"]:
            by_file.setdefault(m["source_lakehouse_file"], []).append(m)

    target_dirs = [DATA_DIR, WWW_DATA_DIR]
    for d in target_dirs:
        if not d.exists():
            continue
        print(f"  Scrubbing directory: {d}")
        for fname, file_mappings in by_file.items():
            fpath = d / fname
            if not fpath.exists():
                continue
            events = json.loads(fpath.read_text(encoding="utf-8"))
            new_events = []
            modified = False

            # Set of gem IDs or indices to drop/suture
            drop_indices = {m["event_index"] for m in file_mappings if m["disposition"] == "DROP"}
            suture_indices = {m["event_index"] for m in file_mappings if m["disposition"] == "SURGICAL_SUTURE"}

            for idx, ev in enumerate(events):
                if idx in drop_indices:
                    drop_count += 1
                    modified = True
                    print(f"    [DROP] {fname}[{idx}] id={ev.get('id')}: {ev.get('summary', '')[:60]}")
                    continue

                if idx in suture_indices:
                    # Surgically excise negative phrases
                    modified = True
                    scrub_count += 1
                    for fld in ["summary", "evidence"]:
                        if fld in ev and isinstance(ev[fld], str):
                            orig = ev[fld]
                            for pat, _ in NEGATIVE_PATTERNS:
                                orig = re.sub(pat, "", orig, flags=re.IGNORECASE)
                            # Clean extra whitespace
                            ev[fld] = re.sub(r"\s+", " ", orig).strip()
                    print(f"    [SUTURE] {fname}[{idx}] id={ev.get('id')}: {ev.get('summary', '')[:60]}")

                new_events.append(ev)

            if modified:
                fpath.write_text(json.dumps(new_events, indent=2), encoding="utf-8")
                print(f"    -> Updated {fpath} ({len(events)} -> {len(new_events)} items)")

    # 2. Scrub ClaraDB Vector Collections
    if CHROMA_CLIENT and claradb_hits:
        print("  Scrubbing ClaraDB vector collections...")
        for h in claradb_hits:
            if h.get("is_pure_rating"):
                try:
                    col = CHROMA_CLIENT.get_collection(h["collection"])
                    col.delete(ids=[h["id"]])
                    print(f"    [CHROMA_DELETE] Deleted {h['collection']}:{h['id']} ({h['document'][:60]})")
                except Exception as e:
                    print(f"    [WARN] Failed to delete {h['id']}: {e}")

    print(f"=== SCRUB COMPLETE: {drop_count} items dropped, {scrub_count} items sutured ===")


if __name__ == "__main__":
    pos, neg = audit_review_documents()
    claradb_hits = query_claradb_sentinels(neg)
    mappings = scan_and_map_lakehouse()
    execute_precision_hybrid_scrub(mappings, claradb_hits)
