# 🚀 Sprint Plan SPR-63.0: Dual-Tier RAG Evaluation Modernization, Grounded Anchors & Live Cognitive Gauntlet

**Sprint:** 63.0  
**Date:** August 25, 2026  
**Status:** 🏗️ READY FOR DELEGATION / GREENLIGHT  
**Theme:** *Dual-Tier Evaluation Architecture (Vector Subsystem vs. Live Round Table), Epistemic Closed Loop (Gem Refinement in Reverse), AGY Reality Check & Purple Human-in-the-Loop Demarcation*

---

## 🧭 Executive Summary: Forensic Breakdown & The Epistemic Closed Loop

A rigorous forensic audit of `validation_anchors.json` and `validation_ledger.jsonl` revealed the exact root causes behind historical RAG evaluation failures:

### 1. The Multi-Collection Blind Spot (The Core Architectural Defect)
* **The Problem**: When `evaluate_rag.py` was constructed in July 2026, `ArchiveNode.get_context()` searched **only the 18-year career notes archive (`artifact_vault`)**.
* **The Failure**: When evaluated on queries regarding *"BKM-032"* or *"HomeLabAI setup guide"*, the engine searched legacy 2018 Intel notes rather than `behavioral_dna` (where BKMs live) or `feature_dna` (where lab modules live). Naturally, it retrieved unrelated TPMI/PAE files, and Kender rightfully failed the runs.
* **The Sprint 61/62 Foundation**: Sprint 61 delivered `LabDNARouter` and Sprint 62 delivered `TraversalDispatcher` (`[FEAT-117/467]`), establishing multi-collection scoping across `artifact_vault`, `behavioral_dna`, and `feature_dna`.

### 2. Synthetic & Outdated Evaluation Queries
* **The Problem**: `validation_anchors.json` contained only 5 synthetic questions with rigid, arbitrary keyword expectations (e.g., demanding the token `"montana"` on general telemetry queries).
* **The Failure**: The test set was disconnected from real-world validation experience, diamond-ranked gems, and low-level platform architecture.

### 3. Metric Pollution: Co-Pilot Human Corrections in the Automated Ledger
* **The Problem**: `[FEAT-456]` (Language-First Co-Pilot Feedback Loop) logs user conversational corrections (e.g., `"[ME] Wait, that's wrong, RAPL MSR 0x610 is PKG limit..."`) as `FAIL` entries to capture human ground truth.
* **The Failure**: On `status.html`, these human feedback traces were mixed into the same ledger table as automated RAG benchmark runs, painting the entire dashboard red.

### 4. Bypassing the Live Cognitive Stack (Isolated Unit Testing Trap)
* **The Problem**: `evaluate_rag.py` invoked `ArchiveNode.get_context()` directly in isolation.
* **The Failure**: It bypassed `TriageEngine` (vibe/domain classification), `LabDNARouter` (collection selection), `InterestLoop` (speculative pre-fetching and gating), `BrainNode` (reasoning synthesis), and `PinkyCritic` (factual grounding verification). It evaluated only raw vector recall, not end-to-end cognitive intelligence.

---

## 🔄 The Epistemic Closed Loop: "Gem Refinement in Reverse"

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                          THE EPISTEMIC CLOSED LOOP ARCHITECTURE                          │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  FORWARD PIPELINE (MassScan & Curator):                                                  │
│  [Raw Engineering Notes] ──► [Information Extraction] ──► [Diamond Gem: GEM-3582]       │
│                                                                  │                       │
│                                                  (Jeopardy Auto-Inversion [FEAT-161])    │
│                                                                  ▼                       │
│  REVERSE PIPELINE (RAG Evaluation):                              │                       │
│  [Grounding Verified] ◄── [Brain/Pinky Cognition] ◄── [Dynamic Eval Query Generated]     │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

1. **Fixed Golden Anchors (10 Core Queries)**: Acts as the permanent CI regression baseline across Silicon Validation, Platform Telemetry, and Operational BKMs.
2. **Dynamic Speculative Evals (Auto-Generated from Gems)**: As MassScan curates newly discovered Rank 4/5 gems, it auto-generates candidate query pairs into the pool, turning the lab into a self-testing, self-improving engine.
3. **Decoupled Local Evaluation**: Eliminates legacy network dependencies on remote KENDER (Ollama) by running evaluation locally via `Pinky Critic` (`[FEAT-470]`) and the deterministic `Epistemic 5-Question Battery` (`[FEAT-454]`).

---

## 🏛️ Dual-Tier Evaluation Architecture

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                         DUAL-TIER RAG EVALUATION ARCHITECTURE                            │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  TIER 1: SUBSYSTEM RETRIEVAL BENCHMARK (--mode vector)                                   │
│  - Purpose: Pure ChromaDB vector/lexical retrieval benchmark (isolated latency & recall) │
│  - Target: All 3 DNA collections (artifact_vault, behavioral_dna, feature_dna)           │
│  - Speed: Sub-second (~0.1s / query), offline, zero LLM dependency                       │
│                                                                                          │
│  TIER 2: END-TO-END LIVE COGNITIVE GAUNTLET (--mode live)                                │
│  - Purpose: Full round-trip evaluation over live WebSocket (ws://127.0.0.1:8765/)        │
│  - Stages Verified:                                                                      │
│    1. Triage Engine: Vibe & Domain classification (HISTORICAL, TECHNICAL, SUPERVISORY)  │
│    2. Traversal Dispatcher: Collection scoping & bidirectional (Topic vs Time) routing  │
│    3. Interest Loop: Speculative pre-fetch & context gating                              │
│    4. Brain Node: Accurate synthesis of technical facts/registers into response          │
│    5. Pinky Critic: Verification of grounding evidence & cartoon quip                   │
│                                                                                          │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 💎 Grounded Evaluation Anchor Portfolio (10 Real-World Validation Queries)

### Category A: Silicon Validation & Bring-Up (`artifact_vault`)
1. **PCIe AER Error Masks**: *"What are the PCIe AER uncorrectable error status mask register offsets and bit definitions?"*
2. **PECI / MCTP Commands**: *"How does the team interact with MCTP services on OpenBMC using peci_cmds and RdEndpointConfigPCILocal?"*
3. **Oakstream Platform Simulation**: *"What platform configuration and fmod was used for the Oakstream 1-socket simulation?"*
4. **Historical PAE Bring-Up**: *"What were the key challenges and deliverables during 2018 Intel Federal PAE bring-up?"*

### Category B: Platform Telemetry & Low-Level MSR (`artifact_vault` / `lab_infrastructure`)
5. **RAPL Energy Telemetry**: *"Which RAPL MSR register defines the Package Energy Status limit (MSR 0x610) vs DRAM energy (MSR 0x618)?"*
6. **DCGM Prometheus Metrics**: *"How does DCGM export RTX 2080 Ti GPU power draw, VRAM, and thermals to Prometheus on port 9400?"*
7. **Kernel USB BDI Throttle (`[LAB-111]`)**: *"How does Kernel BDI strict_limit=1 and max_ratio=1 prevent USB FAT32 writeback deadlocks?"*

### Category C: Lab Architecture & Operational BKMs (`behavioral_dna` / `feature_dna`)
8. **BKM-043 4-Anchor Delegation Standard**: *"What are the 4 mandatory prompt anchors required when delegating tasks via delegate.py?"*
9. **FEAT-472 Route Incubation Sandbox**: *"What is the three-tier lifecycle for mouse-owned candidate routes (Incubation, Evaluation, Solidification)?"*
10. **FEAT-467 Gated On-Demand RAG**: *"Why does the lab default to Zero Context for conversational/supervisory turns rather than default career history?"*

---

## 🎯 Master Delegation Specifications (BKM-043 Compliant)

### 📌 Story 63.1: Grounded Validation Anchor Bank Authoring
* **Target Workspace**: `/home/jallred/Dev_Lab/HomeLabAI`
* **File to Modify**: `config/validation_anchors.json` (Absolute: `/home/jallred/Dev_Lab/HomeLabAI/config/validation_anchors.json`)
* **Anchor 1: Imports**: N/A (Pure JSON configuration).
* **Anchor 2: Path Resilience**: Standard JSON file read by `evaluate_rag.py`.
* **Anchor 3: Signatures & Schema**: Array of 10 structured anchor objects.
* **Anchor 4: Concrete Output Template**:
  ```json
  [
    {
      "id": "VAL-01",
      "query": "What are the PCIe AER uncorrectable error status mask register offsets and bit definitions?",
      "domain": "exp_for",
      "target_collection": "artifact_vault",
      "expected_keywords": ["aer", "uncorrectable", "mask", "status"],
      "ground_truth_summary": "PCIe AER uncorrectable error mask and status registers define fatal/non-fatal hardware error reporting."
    },
    {
      "id": "VAL-02",
      "query": "How does the team interact with MCTP services on OpenBMC using peci_cmds and RdEndpointConfigPCILocal?",
      "domain": "exp_bkm",
      "target_collection": "artifact_vault",
      "expected_keywords": ["peci_cmds", "mctp", "openbmc", "rdendpointconfigpcilocal"],
      "ground_truth_summary": "Interaction with MCTP services on OpenBMC using peci_cmds and RdEndpointConfigPCILocal."
    },
    {
      "id": "VAL-03",
      "query": "What platform configuration and fmod was used for the Oakstream 1-socket simulation?",
      "domain": "exp_for",
      "target_collection": "artifact_vault",
      "expected_keywords": ["oakstream", "simulation", "pfrprot", "1_socket_ucc"],
      "ground_truth_summary": "Oakstream simulation targeting 1_socket_ucc-bmc-oobmsm-pfrprot-s3m with fmod pfrprot+oobmsm+s3m+bmc."
    },
    {
      "id": "VAL-04",
      "query": "What were the key deliverables during 2018 Intel Federal PAE bring-up?",
      "domain": "exp_bkm",
      "target_collection": "artifact_vault",
      "expected_keywords": ["pae", "bringup", "federal", "platform"],
      "ground_truth_summary": "Platform Enablement and Silicon Validation deliverables for Intel Federal PAE."
    },
    {
      "id": "VAL-05",
      "query": "Which RAPL MSR register defines the Package Energy Status limit vs DRAM energy?",
      "domain": "exp_tlm",
      "target_collection": "artifact_vault",
      "expected_keywords": ["rapl", "msr", "0x610", "package", "dram"],
      "ground_truth_summary": "MSR 0x610 is MSR_PKG_ENERGY_STATUS / PKG Power Limit, while 0x618 defines DRAM Energy Status."
    },
    {
      "id": "VAL-06",
      "query": "How does DCGM export RTX 2080 Ti GPU power draw and VRAM metrics to Prometheus on port 9400?",
      "domain": "exp_tlm",
      "target_collection": "feature_dna",
      "expected_keywords": ["dcgm", "prometheus", "9400", "gpu", "vram"],
      "ground_truth_summary": "DCGM exporter daemon exposes GPU power, thermals, and VRAM utilization on port 9400 for Prometheus scraping."
    },
    {
      "id": "VAL-07",
      "query": "How does Kernel BDI strict_limit=1 and max_ratio=1 prevent USB FAT32 writeback deadlocks?",
      "domain": "exp_bkm",
      "target_collection": "behavioral_dna",
      "expected_keywords": ["bdi", "usb", "strict_limit", "max_ratio", "flush"],
      "ground_truth_summary": "LAB-111 caps USB BDI dirty memory ratio to 1% to prevent dirty buffer accumulation from stalling system-wide sync()."
    },
    {
      "id": "VAL-08",
      "query": "What are the 4 mandatory prompt anchors required when delegating tasks via delegate.py under BKM-043?",
      "domain": "exp_bkm",
      "target_collection": "behavioral_dna",
      "expected_keywords": ["bkm-043", "anchors", "imports", "signatures", "template"],
      "ground_truth_summary": "BKM-043 specifies 4 anchors: Import Anchors, Path Resilience, Exact Signatures, and Concrete Output Templates."
    },
    {
      "id": "VAL-09",
      "query": "What is the three-tier lifecycle for mouse-owned candidate routes under FEAT-472?",
      "domain": "exp_bkm",
      "target_collection": "feature_dna",
      "expected_keywords": ["feat-472", "incubation", "evaluation", "solidification"],
      "ground_truth_summary": "FEAT-472 lifecycle: 1. Incubation (triage_supplement.json), 2. Evaluation (provenance telemetry), 3. Solidification (triage_policy.json promotion)."
    },
    {
      "id": "VAL-10",
      "query": "Why does the lab default to Zero Context for conversational turns rather than default career history under FEAT-467?",
      "domain": "exp_bkm",
      "target_collection": "feature_dna",
      "expected_keywords": ["feat-467", "zero context", "gated", "retrieval"],
      "ground_truth_summary": "FEAT-467 enforces Zero Context > Default Context to prevent models from hallucinating 2018 PAE history on general queries."
    }
  ]
  ```
* **Verification Command**:
  `python3 -c 'import json; d=json.load(open("/home/jallred/Dev_Lab/HomeLabAI/config/validation_anchors.json")); assert len(d)==10; print("✅ 10 Anchors Verified")'`

---

### 📌 Story 63.2: Multi-Collection Subsystem Evaluator (`evaluate_rag.py --mode vector`)
* **Target Workspace**: `/home/jallred/Dev_Lab/Portfolio_Dev`
* **File to Modify**: `field_notes/evaluate_rag.py` (Absolute: `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/evaluate_rag.py`)
* **Anchor 1: Imports**:
  ```python
  import argparse
  import asyncio
  import json
  import os
  import sys
  from pathlib import Path
  
  LAB_SRC = str(Path(__file__).resolve().parent.parent.parent / "HomeLabAI" / "src")
  if LAB_SRC not in sys.path:
      sys.path.insert(0, LAB_SRC)
  from nodes.lab_dna_router import LabDNARouter
  from logic.traversal_dispatcher import TraversalDispatcher
  from nodes.archive_node import ArchiveNode, get_context
  ```
* **Anchor 2: Path Resilience**:
  ```python
  DEV_LAB_ROOT = Path(__file__).resolve().parent.parent.parent
  CONFIG_PATH = DEV_LAB_ROOT / "HomeLabAI" / "config" / "validation_anchors.json"
  LEDGER_PATH = Path(__file__).resolve().parent / "data" / "validation_ledger.jsonl"
  RAG_RUNS_DIR = Path(__file__).resolve().parent / "data" / "rag_runs"
  ```
* **Anchor 3: Signatures & CLI**:
  - `parse_args()`: Adds `--mode` (`vector` or `live`, default `vector`). Purges legacy remote KENDER Ollama dependency in favor of local deterministic scoring (`[FEAT-454]`).
  - `async def run_vector_evaluation(anchors: list[dict]) -> list[dict]`: Iterates over anchors, dispatches to `ArchiveNode` / `LabDNARouter` for `target_collection`, calculates recall and vector distance.
  - `evaluate_keywords(text: str, expected: list[str]) -> dict`: Case-insensitive substring matching.
* **Anchor 4: Concrete Output Template**:
  ```python
  entry = {
      "timestamp": datetime.now(timezone.utc).isoformat(),
      "run_type": "AUTOMATED_BENCHMARK",
      "mode": "vector",
      "query": anchor["query"],
      "domain": anchor.get("domain", "exp_bkm"),
      "target_collection": anchor.get("target_collection", "artifact_vault"),
      "expected_keywords": anchor.get("expected_keywords", []),
      "retrieval_time_s": round(elapsed, 4),
      "sources": sources,
      "context_length_chars": len(context_text),
      "keyword_recall": recall,
      "keyword_hits": hits,
      "keyword_total": total_kws,
      "keyword_results": kw_dict,
      "verdict": "PASS" if recall >= 0.75 else "FAIL",
      "run_id": run_id,
  }
  ```
* **Verification Command**:
  `python3 /home/jallred/Dev_Lab/Portfolio_Dev/field_notes/evaluate_rag.py --mode vector`

---

### 📌 Story 63.3: End-to-End Live Cognitive RAG Gauntlet
* **Target Workspace**: `/home/jallred/Dev_Lab/HomeLabAI`
* **Files to Create/Modify**:
  - `src/tests/test_live_rag_eval.py` (Absolute: `/home/jallred/Dev_Lab/HomeLabAI/src/tests/test_live_rag_eval.py`)
  - `Portfolio_Dev/field_notes/evaluate_rag.py` (wire `--mode live`)
* **Anchor 1: Imports**:
  ```python
  import asyncio
  import json
  import os
  import sys
  import pytest
  import aiohttp
  from pathlib import Path
  ```
* **Anchor 2: Path Resilience & BKM-044 Priming**:
  - Reads `HomeLabAI/config/validation_anchors.json`.
  - Uses `wait_for_ready_and_vocal(STATUS_URL)` with a clean 30s timeout to verify lab liveness before starting.
* **Anchor 3: Signatures**:
  - `async def test_live_cognitive_rag_gauntlet()`: Sends the 10 grounded queries over WebSocket `ws://127.0.0.1:8765/ws`.
  - Captures streaming frames: `TRIAGE`, `BRAIN_STREAM`, `PINKY_CRITIC`, `INTEREST_SCORE`.
  - Asserts that:
    1. Triage emits non-empty `vibe` and `domain`.
    2. Brain output contains at least 1 grounded entity/offset.
    3. Pinky Critic emits valid quip and agreement summary.
* **Verification Command**:
  `PYTHONPATH=src pytest src/tests/test_live_rag_eval.py`

---

### 📌 Story 63.4: AGY Reality Check & Purple UI Demarcation
* **Target Workspace**: `/home/jallred/Dev_Lab/Portfolio_Dev`
* **Files to Modify**:
  - `field_notes/evaluate_rag.py` (Reality check audit logic)
  - `field_notes/status.html` (Absolute: `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/status.html`)
* **Anchor 1: AGY Forensic Assumption Audit**:
  - Audit actual vector chunks retrieved for all 10 anchor queries.
  - Weed out queries with invalid assumptions, rigid keyword mismatch, or hallucinated requirements.
* **Anchor 2: Purple UI Demarcation in `status.html`**:
  - Check `entry.source === 'CO_PILOT_FOURTH_WALL'` or `entry.ground_truth`:
    - Display Badge: **🟣 `HUMAN GROUND TRUTH`**
    - Styling: `background: rgba(163, 113, 247, 0.15); border: 1px solid #a371f7; color: #d2a8ff; font-weight: bold; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem;`
    - Subtitle: `Supervisor Coaching Trace • Fourth-Wall Feedback [FEAT-456]`
    - Flawed Output vs Ground Truth display.
  - Check Automated Runs (`entry.run_type === 'AUTOMATED_BENCHMARK'` or standard entry):
    - Display Badge: **🟢 `PASS`** (`#3fb950`) or **🔴 `FAIL`** (`#f85149`) with Recall % and Collection pill.
  - Add quick filter buttons: `[All Records]`, `[Automated Benchmarks]`, `[Human Corrections]`.
* **Verification Command**:
  `python3 /home/jallred/Dev_Lab/Portfolio_Dev/field_notes/build_site.py`

---

### 📌 Story 63.5: Dynamic Closed Loop & Certification
* **Target Workspace**: `/home/jallred/Dev_Lab`
* **Scope**:
  1. Wire MassScan Gem auto-inversion hook (`[FEAT-161]`) to dynamically suggest new eval queries.
  2. Execute `python3 Portfolio_Dev/field_notes/evaluate_rag.py --mode vector` (Verify 10/10 anchors pass with >80% recall).
  3. Execute `PYTHONPATH=src pytest src/tests/test_live_rag_eval.py` (Verify live cognitive gauntlet).
  4. Run `python3 Portfolio_Dev/field_notes/build_site.py` (Verify 0 link drift).
  5. Update `00_FEDERATED_STATUS.md` and feature tracking.
  6. Stage and commit across submodules.

---

## 🛡️ Definition of Done
1. `validation_anchors.json` contains 10 fully grounded queries with verified expectations.
2. `evaluate_rag.py --mode vector` executes in <2s with >80% keyword recall across multi-collection DNA.
3. `evaluate_rag.py --mode live` validates full Triage $\rightarrow$ Brain $\rightarrow$ Pinky Critic execution over WebSocket.
4. `status.html` cleanly demarcates Automated RAG Benchmarks from Co-Pilot Ground-Truth traces with Purple styling.
5. All regression tests pass (367/367), documentation is synchronized, and site builds with 0 link drift.
