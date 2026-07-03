"""
Goal 4: RAG Evaluation Pipeline.

Loads validation anchors from HomeLabAI/config/validation_anchors.json,
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

# --- KENDER Ollama Configuration ---
KENDER_URL = os.environ.get("KENDER_URL", "http://192.168.1.26:11434/api/generate")
KENDER_MODEL = os.environ.get("KENDER_MODEL", "llama3:latest")
KENDER_TIMEOUT = int(os.environ.get("KENDER_TIMEOUT", "60"))


async def call_kender(context_text: str, query: str) -> dict:
    """Route RAG output to KENDER for BKM-032 qualitative audit.

    Sends the retrieved context + original query to the remote LLM
    and requests a structured quality assessment.
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
                    return _parse_kender_response(raw_response)
                else:
                    return {
                        "relevance": 0.0,
                        "coverage": 0.0,
                        "issues": [f"KENDER HTTP {resp.status}"],
                        "verdict": "ERROR",
                    }
    except asyncio.TimeoutError:
        return {
            "relevance": 0.0,
            "coverage": 0.0,
            "issues": ["KENDER timeout"],
            "verdict": "ERROR",
        }
    except Exception as e:
        return {
            "relevance": 0.0,
            "coverage": 0.0,
            "issues": [f"KENDER error: {e}"],
            "verdict": "ERROR",
        }


def _parse_kender_response(raw: str) -> dict:
    """Extract JSON from KENDER's response (handles markdown fences)."""
    # Strip markdown code fences if present
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


async def evaluate_single_anchor(anchor: dict) -> dict:
    """Run a single validation anchor through the full evaluation pipeline."""
    query = anchor["query"]
    domain = anchor["domain"]
    expected_keywords = anchor["expected_keywords"]

    print(f"\n{'='*70}")
    print(f"  QUERY: {query}")
    print(f"  DOMAIN: {domain}")
    print(f"  EXPECTED: {expected_keywords}")
    print(f"{'='*70}")

    # Stage 1: RAG Retrieval
    t0 = time.monotonic()
    try:
        raw_result = await get_context(query=query, n_results=3, domain=domain)
        elapsed = time.monotonic() - t0
        parsed = json.loads(raw_result)
        context_text = parsed.get("text", "")
        sources = parsed.get("sources", [])
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

    # Stage 3: KENDER BKM-032 Audit
    print(f"  Routing to KENDER ({KENDER_MODEL}) for BKM-032 audit...")
    kender_result = await call_kender(context_text[:4000], query)
    print(f"  KENDER VERDICT: {kender_result.get('verdict', 'UNKNOWN')}")
    print(f"  KENDER RELEVANCE: {kender_result.get('relevance', 0.0)}")
    print(f"  KENDER COVERAGE: {kender_result.get('coverage', 0.0)}")

    # Assemble result entry
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "query": query,
        "domain": domain,
        "expected_keywords": expected_keywords,
        "retrieval_time_s": round(elapsed, 3),
        "sources": sources,
        "context_length_chars": len(context_text),
        "keyword_recall": recall,
        "keyword_hits": kw_result["keyword_hits"],
        "keyword_total": kw_result["keyword_total"],
        "keyword_results": kw_result["keyword_results"],
        "kender_audit": kender_result,
    }

    return entry


async def main():
    print("=" * 70)
    print("  GOAL 4: RAG EVALUATION PIPELINE")
    print(f"  Config: {CONFIG_PATH}")
    print(f"  Ledger: {LEDGER_PATH}")
    print(f"  KENDER: {KENDER_URL} ({KENDER_MODEL})")
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
        entry = await evaluate_single_anchor(anchor)
        results.append(entry)

        # Append atomically after each anchor (crash-safe)
        append_ledger_atomic(entry)
        print(f"  ✅ Appended to ledger.")

    # --- Summary Report ---
    print(f"\n{'='*70}")
    print(f"  EVALUATION SUMMARY")
    print(f"{'='*70}")
    recalls = [r["keyword_recall"] for r in results]
    avg_recall = sum(recalls) / len(recalls) if recalls else 0.0

    passed = sum(
        1 for r in results if r["kender_audit"].get("verdict") == "PASS"
    )
    failed = sum(
        1 for r in results if r["kender_audit"].get("verdict") == "FAIL"
    )
    borderline = sum(
        1 for r in results if r["kender_audit"].get("verdict") == "BORDERLINE"
    )
    errors = sum(
        1 for r in results if r["kender_audit"].get("verdict") == "ERROR"
    )

    print(f"  Total Anchors:     {total}")
    print(f"  Avg Keyword Recall: {avg_recall:.2%}")
    print(f"  KENDER Verdicts:")
    print(f"    PASS:      {passed}")
    print(f"    BORDERLINE: {borderline}")
    print(f"    FAIL:      {failed}")
    print(f"    ERROR:     {errors}")

    for i, r in enumerate(results, 1):
        print(f"\n  [{i}] {r['query'][:60]}...")
        print(f"      Domain: {r['domain']}  Recall: {r['keyword_recall']:.0%}  "
              f"Verdict: {r['kender_audit'].get('verdict', '?')}  "
              f"Time: {r['retrieval_time_s']:.1f}s")

    print(f"\n{'='*70}")
    print(f"  Results appended to: {LEDGER_PATH}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    asyncio.run(main())
