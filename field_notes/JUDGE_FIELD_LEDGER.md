# JUDGE_FIELD_LEDGER.md — Judicial Backpressure Digest

_Generated: 2026-07-30 19:54:12 UTC_
_Source: `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/data/judge_backpressure.jsonl`_

---

## Executive Summary

| Metric | Value |
|---|---|
| **Total Evaluations** | 5 |
| **Valid Scores** | 4 |
| **Average Score** | 0.8550 |
| **High Scores (>= 0.8)** | 3 |
| **Low Scores (< 0.5)** | 1 |
| **Refusals (Premise Mismatch)** | 1 |
| **Factual Drift Detected** | 1 |

### Status Breakdown

- **VERIFIED_PASS**: 4
- **ONLINE_EVALUATED**: 1

### Source Breakdown

- **Deep Thought**: 3
- **Pinky (Response)**: 2

---

## Detailed Evaluation Log

### [1] request=default / source=Deep Thought

| Field | Value |
|---|---|
| **Timestamp** | 2026-07-30 19:52:57 UTC |
| **Request ID** | default |
| **Source** | Deep Thought |
| **Status** | VERIFIED_PASS |
| **Score** | 0.99 |
| **Context Eval Length** | 329 chars |
| **Factual Drift** | NO :white_check_mark: |
| **Route Factual** | CHROMADB_PORT_8001 |
| **Route Persona** | CLI_VOICE_V1_LORA |

**Critique:**

> Coherent technical alignment with 18-year career bedrock.

---

### [2] request=5f16b56c / source=Deep Thought

| Field | Value |
|---|---|
| **Timestamp** | 2026-07-30 19:53:01 UTC |
| **Request ID** | 5f16b56c |
| **Source** | Deep Thought |
| **Status** | VERIFIED_PASS |
| **Score** | 0.99 |
| **Context Eval Length** | 620 chars |
| **Factual Drift** | NO :white_check_mark: |
| **Route Factual** | CHROMADB_PORT_8001 |
| **Route Persona** | CLI_VOICE_V1_LORA |

**Critique:**

> Coherent technical alignment with 18-year career bedrock.

---

### [3] request=5f16b56c / source=Pinky (Response)

| Field | Value |
|---|---|
| **Timestamp** | 2026-07-30 19:53:15 UTC |
| **Request ID** | 5f16b56c |
| **Source** | Pinky (Response) |
| **Status** | VERIFIED_PASS |
| **Score** | 0.99 |
| **Context Eval Length** | 126 chars |
| **Factual Drift** | NO :white_check_mark: |
| **Route Factual** | CHROMADB_PORT_8001 |
| **Route Persona** | CLI_VOICE_V1_LORA |

**Critique:**

> Coherent technical alignment with 18-year career bedrock.

---

### [4] request=SYNTH_refusal_001 / source=Deep Thought

| Field | Value |
|---|---|
| **Timestamp** | 2026-07-30 19:53:01 UTC |
| **Request ID** | SYNTH_refusal_001 |
| **Source** | Deep Thought |
| **Status** | ONLINE_EVALUATED |
| **Refusal** | `true` — PREMISE_MISMATCH |
| **Context Eval Length** | 4352 chars |
| **Route Factual** | CHROMADB_PORT_8001 |
| **Route Persona** | CLI_VOICE_V1_LORA |

**Critique:**

> Response contains premise mismatch — user asked about VRAM work at Intel which does not appear in any context documents.

---

### [5] request=SYNTH_lowscore_002 / source=Pinky (Response)

| Field | Value |
|---|---|
| **Timestamp** | 2026-07-30 19:54:01 UTC |
| **Request ID** | SYNTH_lowscore_002 |
| **Source** | Pinky (Response) |
| **Status** | VERIFIED_PASS |
| **Score** | 0.45 |
| **Context Eval Length** | 1792 chars |
| **Factual Drift** | YES :warning: |
| **Route Factual** | CHROMADB_PORT_8001 |
| **Route Persona** | CLI_VOICE_V1_LORA |

**Critique:**

> Low score due to incomplete context. Response omitted key technical detail on GPU thermal throttling mitigations.


---

_End of report — 5 evaluation(s) total._
