# 🚀 Sprint Plan SPR-63.0: Dual-Tier RAG Evaluation Modernization, Grounded Anchors & Live Cognitive Gauntlet

**Sprint:** 63.0  
**Date:** August 25, 2026  
**Status:** 🏗️ IN PROGRESS (Stories 63.1 & 63.2 Complete, 63.3 In Flight)  
**Theme:** *Dual-Tier Evaluation Architecture (Vector Subsystem vs. Live Round Table), Epistemic Closed Loop (Gem Refinement in Reverse), 4-Tier Exception Resilience Ladder, AGY Reality Check & Purple Human-in-the-Loop Demarcation*

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

## 🎯 Surgical Master Delegation Specifications (BKM-043 Compliant)

### 📌 Story 63.1: Grounded Validation Anchor Bank Authoring
* **Status**: ✅ COMPLETE (`commit a3f0b3b`)
* **Target Workspace**: `/home/jallred/Dev_Lab/HomeLabAI`
* **File Modified**: `config/validation_anchors.json` (Absolute: `/home/jallred/Dev_Lab/HomeLabAI/config/validation_anchors.json`)
* **Verification Command**:
  `python3 -c 'import json; d=json.load(open("/home/jallred/Dev_Lab/HomeLabAI/config/validation_anchors.json")); assert len(d)==10; print("✅ 10 Anchors Verified")'`

---

### 📌 Story 63.2: Multi-Collection Subsystem Evaluator (`evaluate_rag.py --mode vector`)
* **Status**: ✅ COMPLETE (`commit 5947820`)
* **Target Workspace**: `/home/jallred/Dev_Lab/Portfolio_Dev`
* **File Modified**: `field_notes/evaluate_rag.py` (Absolute: `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/evaluate_rag.py`)
* **Output Template**:
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
* **Status**: ⏳ IN FLIGHT
* **Target Workspace**: `/home/jallred/Dev_Lab/HomeLabAI`
* **Files to Create/Modify**:
  - `src/tests/test_live_rag_eval.py` (Absolute: `/home/jallred/Dev_Lab/HomeLabAI/src/tests/test_live_rag_eval.py`)
* **Grep Anchors**:
  - In `test_live_rag_eval.py`, new file using `wait_for_ready_and_vocal(STATUS_URL)` (grep: `wait_for_ready_and_vocal`).
* **Assertions**:
  1. Triage emits valid non-null `vibe` and `domain`.
  2. Brain stream outputs at least 1 grounded register/entity token.
  3. Pinky Critic emits valid quip and agreement summary.
* **Verification Command**:
  `PYTHONPATH=src pytest src/tests/test_live_rag_eval.py`

---

### 📌 Story 63.4: 4-Tier Exception Resilience & Quarantine Sweep
* **Target Workspace**: `/home/jallred/Dev_Lab/Portfolio_Dev`
* **Files to Modify**:
  - `field_notes/utils.py` (Absolute: `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/utils.py`)
  - `field_notes/aggregate_years.py` (Absolute: `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/aggregate_years.py`)
  - `field_notes/mass_scan.py` (Absolute: `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/mass_scan.py`)
* **Scope & Mechanics (The 4-Tier Resilience Ladder)**:
  1. **Tier 4 (Quarantine Fallback Pattern)**: In `aggregate_years.py` and `mass_scan.py`, when a JSON line or record fails parsing, write the offending record to `<file>.quarantine.jsonl` with timestamp and error message instead of silently dropping data (`except: pass`).
  2. **Tier 3 (Neural Pager Relay Hooks)**: In `mass_scan.py` and `nibble_v2.py`, emit warning telemetry to the Neural Pager (`infra.pager_relay`) on batch parsing anomalies.
  3. **Tier 2 (Structured Diagnostic Logging)**: In `utils.py` (`safe_load_json`, `parse_date`), replace bare `except: pass` with explicit `except (json.JSONDecodeError, OSError, ValueError) as e: logger.warning(f"Error parsing {filepath}: {e}")`.
  4. **Tier 1 (Fail-Fast Hard Gates)**: Ensure all build scripts (`build_site.py`, `verify_feature_links.py`) halt with `sys.exit(1)` on compilation exceptions.
* **Grep Anchors**:
  - In `utils.py`, grep: `except: pass` (L43, L82, L179).
  - In `aggregate_years.py`, grep: `except: pass` (L51, L60, L154).
  - In `mass_scan.py`, grep: `except: pass` (L118).
* **Verification Command**:
  `python3 -c 'import sys; from field_notes.utils import safe_load_json; print("✅ Utils verified")'`

---

### 📌 Story 63.5: AGY Reality Check & Purple UI Demarcation
* **Target Workspace**: `/home/jallred/Dev_Lab/Portfolio_Dev`
* **File to Modify**: `field_notes/status.html` (Absolute: `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/status.html`)
* **Grep Anchor**: Inside `showRagEval()` / RAG log renderer around line 1344 (grep: `RAG EVALUATION METRICS`).
* **Surgical Delta**:
  - Check `entry.source === 'CO_PILOT_FOURTH_WALL'` or `entry.ground_truth`:
    - Display Badge: **🟣 `HUMAN GROUND TRUTH`**
    - Styling: `background: rgba(163, 113, 247, 0.15); border: 1px solid #a371f7; color: #d2a8ff; font-weight: bold; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem;`
    - Subtitle: `Supervisor Coaching Trace • Fourth-Wall Feedback [FEAT-456]`
  - Check Automated Runs (`entry.run_type === 'AUTOMATED_BENCHMARK'` or standard entry):
    - Display Badge: **🟢 `PASS`** (`#3fb950`) or **🔴 `FAIL`** (`#f85149`) with Recall % and Collection pill.
  - Add quick filter buttons: `[All Records]`, `[Automated Benchmarks]`, `[Human Corrections]`.
* **Verification Command**:
  `python3 /home/jallred/Dev_Lab/Portfolio_Dev/field_notes/build_site.py`

---

### 📌 Story 63.6: Dynamic Closed Loop & Certification
* **Target Workspace**: `/home/jallred/Dev_Lab`
* **Grep Anchor**: In `Portfolio_Dev/field_notes/mass_scan.py`, inside post-scan step around line 180 (grep: `latest_synthesis_gems.json`).
* **Surgical Delta**:
  1. Trigger `extract_latest_gems.py` to keep candidate eval pool synchronized with newly discovered gems.
  2. Run `python3 Portfolio_Dev/field_notes/evaluate_rag.py --mode vector` (Verify 10/10 anchors pass with >80% recall).
  3. Run `python3 Portfolio_Dev/field_notes/build_site.py` (Verify 0 link drift).
  4. Update `00_FEDERATED_STATUS.md` and feature tracking.
  5. Stage and commit across submodules.

---

## 🛡️ Definition of Done
1. `validation_anchors.json` contains 10 fully grounded queries with verified expectations.
2. `evaluate_rag.py --mode vector` executes in <2s with >80% keyword recall across multi-collection DNA.
3. `evaluate_rag.py --mode live` validates full Triage $\rightarrow$ Brain $\rightarrow$ Pinky Critic execution over WebSocket.
4. 4-Tier Exception Resilience Ladder applied: Quarantine pattern in note aggregators, Neural Pager alerts on batch anomalies, and bare `except: pass` purged.
5. `status.html` cleanly demarcates Automated RAG Benchmarks from Co-Pilot Ground-Truth traces with Purple styling.
6. All regression tests pass (367/367), documentation is synchronized, and site builds with 0 link drift.
