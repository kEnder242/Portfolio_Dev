#!/usr/bin/env python3
"""
[FEAT-444] Judicial Backpressure Ledger Compiler

Reads judge_backpressure.jsonl from the field_notes data directory and
compiles JUDGE_FIELD_LEDGER.md — a curated design critique digest for
human/architect review.

Usage:
    python3 field_notes/generate_judge_ledger.py

Output:
    field_notes/JUDGE_FIELD_LEDGER.md
"""

import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone

HOME = os.path.expanduser("~")
DATA_DIR = os.path.join(HOME, "Dev_Lab", "Portfolio_Dev", "field_notes", "data")
JUDGE_JSONL = os.path.join(DATA_DIR, "judge_backpressure.jsonl")
OUTPUT_MD = os.path.join(os.path.dirname(DATA_DIR), "JUDGE_FIELD_LEDGER.md")

REPORT_TITLE = "JUDGE_FIELD_LEDGER.md — Judicial Backpressure Digest"


def load_judge_entries():
    if not os.path.exists(JUDGE_JSONL):
        print(f"[FEAT-444] No judge ledger found at {JUDGE_JSONL}")
        return []

    entries = []
    with open(JUDGE_JSONL, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"[WARN] Skipping malformed JSONL line: {e}")

    return entries


def format_timestamp(entry):
    iso = entry.get("iso_timestamp", "")
    if iso:
        try:
            dt = datetime.fromisoformat(iso)
            return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        except (ValueError, TypeError):
            pass
    ts = entry.get("timestamp", 0)
    if isinstance(ts, (int, float)) and ts > 0:
        dt = datetime.fromtimestamp(ts)
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    return "Unknown"


def compile_markdown(entries):
    total = len(entries)
    if total == 0:
        return (
            f"# {REPORT_TITLE}\n\n"
f"_Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC_\n\n"
        f"## Summary\n\n"
        f"**No judge evaluations recorded yet.**\n\n"
            f"The ledger at `{JUDGE_JSONL}` is empty or does not exist.\n"
            f"Trigger a turn trace through the Lab UI to generate entries.\n"
        )

    refusals = [e for e in entries if e.get("refusal")]
    non_refusals = [e for e in entries if not e.get("refusal")]

    scores = [e.get("score", 0) for e in non_refusals if isinstance(e.get("score"), (int, float))]
    avg_score = sum(scores) / len(scores) if scores else 0.0
    high_scores = sum(1 for s in scores if s >= 0.8)
    low_scores = sum(1 for s in scores if s < 0.5)
    drift_count = sum(1 for e in non_refusals if e.get("factual_drift_detected"))
    statuses = Counter(e.get("status", "UNKNOWN") for e in entries)
    sources = Counter(e.get("source", "unknown") for e in entries)

    lines = [
        f"# {REPORT_TITLE}",
        "",
        f"_Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC_",
        f"_Source: `{JUDGE_JSONL}`_",
        "",
        "---",
        "",
        "## Executive Summary",
        "",
        f"| Metric | Value |",
        f"|---|---|",
        f"| **Total Evaluations** | {total} |",
        f"| **Valid Scores** | {len(scores)} |",
        f"| **Average Score** | {avg_score:.4f} |",
        f"| **High Scores (>= 0.8)** | {high_scores} |",
        f"| **Low Scores (< 0.5)** | {low_scores} |",
        f"| **Refusals (Premise Mismatch)** | {len(refusals)} |",
        f"| **Factual Drift Detected** | {drift_count} |",
        "",
        "### Status Breakdown",
        "",
    ]
    for status, count in statuses.most_common():
        lines.append(f"- **{status}**: {count}")
    lines.append("")

    if sources:
        lines.append("### Source Breakdown")
        lines.append("")
        for src, count in sources.most_common():
            lines.append(f"- **{src}**: {count}")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## Detailed Evaluation Log",
        "",
    ])

    for i, entry in enumerate(entries, 1):
        ts = format_timestamp(entry)
        rid = entry.get("request_id", "?")
        src = entry.get("source", "?")
        status = entry.get("status", "UNKNOWN")
        score = entry.get("score", "N/A")
        is_refusal = entry.get("refusal", False)
        refusal_reason = entry.get("refusal_reason", "")
        context_len = entry.get("context_eval_length", 0)
        drift = entry.get("factual_drift_detected")
        critique = entry.get("critique") or entry.get("style_critique", "")
        route_feedback = entry.get("route_feedback", {})

        lines.append(f"### [{i}] request={rid} / source={src}")
        lines.append("")
        lines.append(f"| Field | Value |")
        lines.append(f"|---|---|")
        lines.append(f"| **Timestamp** | {ts} |")
        lines.append(f"| **Request ID** | {rid} |")
        lines.append(f"| **Source** | {src} |")
        lines.append(f"| **Status** | {status} |")

        if is_refusal:
            lines.append(f"| **Refusal** | `true` — {refusal_reason} |")
        else:
            lines.append(f"| **Score** | {score} |")

        lines.append(f"| **Context Eval Length** | {context_len} chars |")

        if drift is not None:
            drift_str = "YES :warning:" if drift else "NO :white_check_mark:"
            lines.append(f"| **Factual Drift** | {drift_str} |")

        ft = route_feedback.get("factual_target", "")
        pt = route_feedback.get("persona_target", "")
        if ft or pt:
            lines.append(f"| **Route Factual** | {ft or 'N/A'} |")
            lines.append(f"| **Route Persona** | {pt or 'N/A'} |")

        lines.append("")

        if critique:
            lines.append("**Critique:**")
            lines.append("")
            lines.append(f"> {critique}")
            lines.append("")

        if i < total:
            lines.append("---")
            lines.append("")

    lines.extend([
        "",
        "---",
        "",
        f"_End of report — {total} evaluation(s) total._",
        "",
    ])

    return "\n".join(lines)


def main():
    print(f"[FEAT-444] Loading judge entries from {JUDGE_JSONL}")
    entries = load_judge_entries()
    print(f"[FEAT-444] Loaded {len(entries)} evaluation(s)")

    markdown = compile_markdown(entries)

    os.makedirs(os.path.dirname(OUTPUT_MD), exist_ok=True)
    with open(OUTPUT_MD, "w") as f:
        f.write(markdown)

    print(f"[FEAT-444] Report written to {OUTPUT_MD}")
    print(f"[FEAT-444] Done.")


if __name__ == "__main__":
    main()
