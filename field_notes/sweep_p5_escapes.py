#!/usr/bin/env python3
"""[Story 112.140 / LOOP-006 / BKM-015] Resumable Read-Only P5 Escape Sweep.

Runs deterministic `sanitize_with_tripwire()` (<1s) plus batched read-only
P5_Hybrid_Semantic_Syntactic LLM escape detection over `20*.json` and
`public_benchmarks.json` without mutating source JSON files in-place.
"""

import argparse
import glob
import json
import os
import re
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DEFAULT_REPORT = os.path.join(DATA_DIR, "p5_escape_report.json")

sys.path.insert(0, BASE_DIR)
from ai_engine_v2 import get_engine_v2  # noqa: E402
from scrub_all_passwords import sanitize_with_tripwire  # noqa: E402


def iter_evidence_records():
    files = sorted(glob.glob(os.path.join(DATA_DIR, "20[0-2][0-9].json")))
    pb = os.path.join(DATA_DIR, "public_benchmarks.json")
    if os.path.exists(pb):
        files.append(pb)

    for fpath in files:
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue
        if not isinstance(data, list):
            continue
        fname = os.path.basename(fpath)
        for idx, rec in enumerate(data):
            if not isinstance(rec, dict):
                continue
            ev = rec.get("evidence", "")
            if isinstance(ev, str) and ev.strip():
                yield f"{fname}#{idx}", ev


def parse_llm_json(raw: str) -> list[dict]:
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if not m:
        return []
    try:
        obj = json.loads(m.group(0))
        escapes = obj.get("escapes", [])
        return escapes if isinstance(escapes, list) else []
    except Exception:
        return []


def main():
    parser = argparse.ArgumentParser(description="Resumable P5 + tripwire read-only escape sweep.")
    parser.add_argument("--batch-size", type=int, default=10)
    parser.add_argument("--limit", type=int, default=0, help="Max records to scan with LLM (0 = all)")
    parser.add_argument("--offset", type=int, default=0, help="Starting record offset")
    parser.add_argument("--tripwire-only", action="store_true", help="Skip LLM and run deterministic tripwire only")
    parser.add_argument("--report", default=DEFAULT_REPORT)
    args = parser.parse_args()

    records = list(iter_evidence_records())
    print(f"Total evidence records: {len(records)}")

    # 1. Deterministic backup tripwire across full corpus
    tripwire_hits = []
    for key, ev in records:
        _clean, esc, rules = sanitize_with_tripwire(ev)
        if esc:
            tripwire_hits.append({"key": key, "rules": rules})
    print(f"Deterministic tripwire hits: {len(tripwire_hits)}")

    llm_hits = []
    if not args.tripwire_only:
        slice_recs = records[args.offset :]
        if args.limit > 0:
            slice_recs = slice_recs[: args.limit]

        engine = get_engine_v2(mode="LOCAL")
        for start in range(0, len(slice_recs), args.batch_size):
            batch = slice_recs[start : start + args.batch_size]
            numbered = "\n".join(f"[{i}] ({k}): {ev[:400]}" for i, (k, ev) in enumerate(batch))
            prompt = (
                "[ROLE] Security escape auditor (read-only).\n"
                "[TASK] Inspect each numbered evidence string using P5 hybrid judgment:\n"
                "Look for high-entropy strings, password-like tokens, unredacted credential pairs "
                "(user:secret, scheme://user:secret@, --password/--token/--api-key <val>, Authorization/API-key headers).\n"
                "Ignore already-redacted placeholders like [REDACTED] or [REDACTED_PASSWORD], TCP ports, IPs, and hex registers.\n"
                'Return ONLY valid JSON: {"escapes": [{"index": int, "reason": "short", "suspect": "short_preview"}]}\n'
                'If none, return {"escapes": []}.\n\n'
                f"[EVIDENCE BATCH]\n{numbered}"
            )
            t0 = time.perf_counter()
            raw = engine.generate(prompt, options={"num_predict": 350})
            dt = time.perf_counter() - t0
            for item in parse_llm_json(raw):
                idx = item.get("index")
                suspect = str(item.get("suspect", ""))
                if isinstance(idx, int) and 0 <= idx < len(batch) and "[REDACTED" not in suspect:
                    llm_hits.append({
                        "key": batch[idx][0],
                        "reason": item.get("reason", ""),
                        "suspect": suspect[:60],
                    })
            print(f"  Batch {start//args.batch_size + 1} ({len(batch)} items, {dt:.1f}s) -> total llm_hits={len(llm_hits)}")

    report = {
        "total_records": len(records),
        "tripwire_hits": tripwire_hits,
        "llm_hits": llm_hits,
    }
    os.makedirs(os.path.dirname(args.report), exist_ok=True)
    with open(args.report, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"Wrote report -> {args.report}")


if __name__ == "__main__":
    main()
