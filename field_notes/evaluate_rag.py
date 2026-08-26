"""
Goal 4: RAG Evaluation Pipeline.

Loads validation anchors from HomeLabAI/config/validation_anchors.json,
# [FEAT-228] Agnostic Context Engine (get_context)
invokes the ArchiveNode get_context() RAG pipeline for each anchor,
evaluates keyword recall, routes output to KENDER (remote Ollama) for
BKM-032 qualitative audit, and appends results atomically to the
validation ledger.
"""

import asyncio
import json
import os
import sys
import time
import traceback
from datetime import datetime, timezone

# --- Path Resolution ---
HOME = os.path.expanduser("~")
LAB_SRC = os.path.join(HOME, "Dev_Lab", "HomeLabAI", "src")
CONFIG_PATH = os.path.join(HOME, "Dev_Lab", "HomeLabAI", "config", "validation_anchors.json")
LEDGER_PATH = os.path.join(HOME, "Dev_Lab", "Portfolio_Dev", "field_notes", "data", "validation_ledger.jsonl")

# Ensure we can import the ArchiveNode module
sys.path.insert(0, LAB_SRC)

from nodes.archive_node import get_context
from nodes.lab_dna_router import get_collection_priorities, filter_candidate_context

# --- [FEAT-454] Local Deterministic Scoring (replaces KENDER) ---
# KENDER Ollama config retained for --mode live fallback only
KENDER_URL = os.environ.get("KENDER_URL", "http://127.0.0.1:11434/api/generate")
KENDER_MODEL = os.environ.get("KENDER_MODEL", "llama3.2:3b")
KENDER_TIMEOUT = int(os.environ.get("KENDER_TIMEOUT", "60"))


def local_scoring(kw_result: dict) -> dict:
    """[FEAT-454] Local deterministic scoring — zero network, zero LLM.
    Calculates recall and coverage from keyword evaluation results.
    Verdict is PASS if recall >= 0.75, else FAIL.
    """
    recall = kw_result["keyword_recall"]
    hits = kw_result["keyword_hits"]
    total = kw_result["keyword_total"]
    coverage = min(1.0, hits / max(1, total))
    verdict = "PASS" if recall >= 0.75 else "FAIL"
    return {
        "relevance": round(recall, 3),
        "coverage": round(coverage, 3),
        "issues": [] if verdict == "PASS" else [f"Recall {recall:.1%} below 0.75 threshold"],
        "verdict": verdict,
    }


async def call_kender(context_text: str, query: str) -> tuple[dict, str, str]:
    """Route RAG output to KENDER for BKM-032 qualitative audit.
    DEPRECATED: Retained for --mode live only. Use local_scoring() for vector mode.
    """
    import aiohttp

    prompt = (
        "[BKM-032 AUDIT] Evaluate the following RAG retrieval quality.\n\n"
        f"ORIGINAL QUERY: {query}\n\n"
        f"RETRIEVED CONTEXT:\n{context_text[:4000]}\n\n"
        "You MUST respond in raw JSON format ONLY. Do NOT wrap the output in markdown code fences, and do NOT include conversational text. Output only the raw JSON object.\n\n"
        "JSON Schema:\n"
        "{\n"
        '  "relevance": 0.0,\n'
        '  "coverage": 0.0,\n'
        '  "issues": ["description of issues or none"],\n'
        '  "verdict": "PASS"\n'
        "}\n\n"
        "JSON:"
    )

    payload = {
        "model": KENDER_MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.0, "num_predict": 1024},
    }

    try:
        async with aiohttp.ClientSession(trust_env=False) as session:
            async with session.post(
                KENDER_URL, json=payload, timeout=KENDER_TIMEOUT
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    raw_response = data.get("response", "")
                    return _parse_kender_response(raw_response), prompt, raw_response
                else:
                    err_res = {
                        "relevance": 0.0,
                        "coverage": 0.0,
                        "issues": [f"KENDER HTTP {resp.status}"],
                        "verdict": "ERROR",
                    }
                    return err_res, prompt, f"HTTP {resp.status}"
    except asyncio.TimeoutError:
        err_res = {
            "relevance": 0.0,
            "coverage": 0.0,
            "issues": ["KENDER timeout"],
            "verdict": "ERROR",
        }
        return err_res, prompt, "TimeoutError"
    except Exception as e:
        err_res = {
            "relevance": 0.0,
            "coverage": 0.0,
            "issues": [f"KENDER error: {e}"],
            "verdict": "ERROR",
        }
        return err_res, prompt, f"Error: {e}"


def _parse_kender_response(raw: str) -> dict:
    """Extract JSON from KENDER's response (handles markdown fences)."""
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1]
        cleaned = cleaned.rsplit("```", 1)[0].strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned.removeprefix("```json").strip()
        cleaned = cleaned.rsplit("```", 1)[0].strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {
            "relevance": 0.0,
            "coverage": 0.0,
            "issues": [f"Unparseable KENDER response: {raw[:200]}"],
            "verdict": "ERROR",
        }


def evaluate_keywords(context_text: str, expected_keywords: list[str]) -> dict:
    """Check presence of expected keywords in the retrieved context.

    Returns keyword-level hit/miss map and aggregate recall.
    """
    text_lower = context_text.lower()
    results = {}
    hits = 0
    for kw in expected_keywords:
        found = kw.lower() in text_lower
        results[kw] = found
        if found:
            hits += 1

    total = len(expected_keywords)
    return {
        "keyword_results": results,
        "keyword_hits": hits,
        "keyword_total": total,
        "keyword_recall": hits / total if total > 0 else 0.0,
    }


def append_ledger_atomic(entry: dict) -> None:
    """Append a JSON line to the validation ledger.
    
    Uses standard robust append to commit the line.
    """
    os.makedirs(os.path.dirname(LEDGER_PATH), exist_ok=True)
    line = json.dumps(entry, default=str) + "\n"
    
    with open(LEDGER_PATH, "a") as f:
        f.write(line)


# [FEAT-023] The Stoic Strategist (Identity Anchor)
async def evaluate_single_anchor(anchor: dict, mode: str = "vector") -> dict:
    """Run a single validation anchor through the full evaluation pipeline.
    Supports --mode vector (local deterministic scoring) and --mode live (KENDER LLM).
    """
    query = anchor["query"]
    domain = anchor["domain"]
    target_collection = anchor.get("target_collection", "artifact_vault")
    expected_keywords = anchor.get("expected_keywords", [])

    print(f"\n{'='*70}")
    print(f"  QUERY: {query}")
    print(f"  DOMAIN: {domain}")
    print(f"  TARGET COLLECTION: {target_collection}")
    print(f"  MODE: {mode}")
    print(f"  EXPECTED: {expected_keywords}")
    print(f"{'='*70}")

    # Stage 1: RAG Retrieval — route across target_collection
    t0 = time.monotonic()
    try:
        raw_result = await get_context(query=query, n_results=3, domain=domain)
        elapsed = time.monotonic() - t0
        try:
            parsed = json.loads(raw_result)
            if isinstance(parsed, dict):
                context_text = parsed.get("text", raw_result)
                sources = parsed.get("sources", [])
            else:
                context_text = str(raw_result)
                sources = []
        except Exception:
            context_text = str(raw_result)
            sources = []
    except Exception as e:
        elapsed = time.monotonic() - t0
        context_text = ""
        sources = []
        error_detail = traceback.format_exc()
        print(f"  ❌ RAG RETRIEVAL ERROR: {e}\n{error_detail}")

    print(f"  RETRIEVAL TIME: {elapsed:.2f}s")
    print(f"  SOURCES: {sources}")
    print(f"  CONTEXT LENGTH: {len(context_text)} chars")

    # Stage 2: Keyword Evaluation
    kw_result = evaluate_keywords(context_text, expected_keywords)
    recall = kw_result["keyword_recall"]
    hit_list = [kw for kw, found in kw_result["keyword_results"].items() if found]
    miss_list = [kw for kw, found in kw_result["keyword_results"].items() if not found]
    print(f"  KEYWORD RECALL: {recall:.2%} ({kw_result['keyword_hits']}/{kw_result['keyword_total']})")
    if hit_list:
        print(f"  HITS: {hit_list}")
    if miss_list:
        print(f"  MISSES: {miss_list}")

    # Stage 3: Scoring — local deterministic (vector) or KENDER LLM (live)
    if mode == "vector":
        audit_result = local_scoring(kw_result)
        audit_source = "local_scoring"
    else:
        audit_result, _, _ = await call_kender(context_text[:4000], query)
        audit_source = "kender_llm"
    print(f"  AUDIT VERDICT: {audit_result.get('verdict', 'UNKNOWN')} ({audit_source})")
    print(f"  AUDIT RELEVANCE: {audit_result.get('relevance', 0.0)}")
    print(f"  AUDIT COVERAGE: {audit_result.get('coverage', 0.0)}")

    # Generate unique run ID and save diagnostic details decoupled
    import hashlib
    query_hash = hashlib.md5(query.encode('utf-8')).hexdigest()[:8]
    run_id = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{query_hash}"

    # Save the detailed diagnostic logs using Atomic File Swap Protocol
    rag_runs_dir = os.path.join(os.path.dirname(LEDGER_PATH), "rag_runs")
    os.makedirs(rag_runs_dir, exist_ok=True)
    run_payload = {
        "query": query,
        "context": context_text,
        "expected_keywords": expected_keywords,
        "keyword_results": kw_result["keyword_results"],
        "audit_source": audit_source,
        "audit_result": audit_result
    }

    # Atomic write to rag_runs directory
    from infra.atomic_io import atomic_write_json
    run_file_path = os.path.join(rag_runs_dir, f"{run_id}.json")
    atomic_write_json(run_file_path, run_payload)
    print(f"  Diagnostic log written to {run_file_path}")

    # Assemble result entry
    hits = kw_result["keyword_hits"]
    total_kws = kw_result["keyword_total"]
    verdict = "PASS" if recall >= 0.75 else "FAIL"
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "run_type": "AUTOMATED_BENCHMARK",
        "mode": mode,
        "query": query,
        "domain": domain,
        "target_collection": target_collection,
        "expected_keywords": expected_keywords,
        "retrieval_time_s": round(elapsed, 4),
        "sources": sources,
        "context_length_chars": len(context_text),
        "keyword_recall": recall,
        "keyword_hits": hits,
        "keyword_total": total_kws,
        "keyword_results": kw_result["keyword_results"],
        "verdict": verdict,
        "run_id": run_id,
    }

    return entry


async def main(mode: str = "vector"):
    print("=" * 70)
    print("  GOAL 4: RAG EVALUATION PIPELINE")
    print(f"  Config: {CONFIG_PATH}")
    print(f"  Ledger: {LEDGER_PATH}")
    print(f"  Mode: {mode.upper()}")
    if mode == "live":
        print(f"  KENDER: {KENDER_URL} ({KENDER_MODEL})")
    else:
        print("  Scoring: Local Deterministic [FEAT-454]")
    print("=" * 70)

    # Load validation anchors
    if not os.path.exists(CONFIG_PATH):
        print(f"\n  ❌ Config not found: {CONFIG_PATH}")
        sys.exit(1)

    with open(CONFIG_PATH, "r") as f:
        anchors = json.load(f)

    total = len(anchors)
    print(f"\n  Loaded {total} validation anchors.\n")

    results = []
    for i, anchor in enumerate(anchors, 1):
        print(f"\n--- Anchor {i}/{total} ---")
        entry = await evaluate_single_anchor(anchor, mode=mode)
        results.append(entry)

        # Append atomically after each anchor (crash-safe)
        append_ledger_atomic(entry)
        print("  ✅ Appended to ledger.")

    # --- Summary Report ---
    print(f"\n{'='*70}")
    print("  EVALUATION SUMMARY")
    print(f"{'='*70}")
    recalls = [r["keyword_recall"] for r in results]
    avg_recall = sum(recalls) / len(recalls) if recalls else 0.0

    passed = sum(1 for r in results if r.get("verdict") == "PASS")
    failed = sum(1 for r in results if r.get("verdict") == "FAIL")

    print(f"  Total Anchors:     {total}")
    print(f"  Mode:              {mode.upper()}")
    print(f"  Avg Keyword Recall: {avg_recall:.2%}")
    print("  Verdicts:")
    print(f"    PASS:      {passed}")
    print(f"    FAIL:      {failed}")

    for i, r in enumerate(results, 1):
        print(f"\n  [{i}] {r['query'][:60]}...")
        print(f"      Domain: {r['domain']}  Collection: {r['target_collection']}  "
              f"Recall: {r['keyword_recall']:.0%}  "
              f"Verdict: {r.get('verdict', '?')}  "
              f"Time: {r['retrieval_time_s']:.1f}s")

    print(f"\n{'='*70}")
    print(f"  Results appended to: {LEDGER_PATH}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="RAG Evaluation Pipeline")
    parser.add_argument(
        "--mode",
        choices=["vector", "live"],
        default="vector",
        help="Scoring mode: 'vector' for local deterministic [FEAT-454], 'live' for KENDER LLM (default: vector)"
    )
    args = parser.parse_args()
    asyncio.run(main(mode=args.mode))
