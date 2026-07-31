#!/usr/bin/env python3
"""[FEAT-444] Judicial Backpressure Ledger Compiler.

Reads field_notes/data/judge_backpressure.jsonl (written by the Foyer router
M5 Judge hook) and compiles JUDGE_FIELD_LEDGER.md + a machine-readable
judge_ledger.json. Class-1 pattern: stdlib only, atomic writes (.tmp + replace).
"""
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
BACKPRESSURE_PATH = os.path.join(DATA_DIR, "judge_backpressure.jsonl")
LEDGER_JSON = os.path.join(DATA_DIR, "judge_ledger.json")
LEDGER_MD = os.path.join(DATA_DIR, "JUDGE_FIELD_LEDGER.md")


def load_entries():
    entries = []
    if not os.path.exists(BACKPRESSURE_PATH):
        return entries
    with open(BACKPRESSURE_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def compile_ledger(entries):
    refusals = [e for e in entries if e.get("refusal")]
    drifts = [e for e in entries if e.get("factual_drift_detected")]
    return {
        "total_evaluations": len(entries),
        "refusal_count": len(refusals),
        "factual_drift_count": len(drifts),
        "latest": entries[-1] if entries else None,
        "sources": sorted({e.get("source", "unknown") for e in entries}),
    }


def atomic_write(path, text):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        f.write(text)
    os.replace(tmp, path)


def main():
    entries = load_entries()
    ledger = compile_ledger(entries)
    atomic_write(LEDGER_JSON, json.dumps(ledger, indent=2, default=str) + "\n")
    lines = [
        "# Judicial Field Ledger [FEAT-444]",
        "",
        f"- Total evaluations: {ledger['total_evaluations']}",
        f"- Refusals (PREMISE_MISMATCH): {ledger['refusal_count']}",
        f"- Factual drift flags: {ledger['factual_drift_count']}",
        f"- Sources: {', '.join(ledger['sources']) or 'none'}",
    ]
    if ledger["latest"]:
        latest = ledger["latest"]
        lines += [
            "",
            "## Latest entry",
            f"- request_id: {latest.get('request_id')}",
            f"- source: {latest.get('source')}",
            f"- status: {latest.get('status')} | score: {latest.get('score')}",
            f"- refusal: {latest.get('refusal')} ({latest.get('refusal_reason')})",
            f"- timestamp: {latest.get('iso_timestamp')}",
        ]
    atomic_write(LEDGER_MD, "\n".join(lines) + "\n")
    print(f"[FEAT-444] Ledger compiled: {ledger['total_evaluations']} evaluations -> {LEDGER_MD}")


if __name__ == "__main__":
    main()
