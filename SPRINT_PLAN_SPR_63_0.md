# 🚀 Sprint Plan SPR-63.0: Dual-Tier RAG Evaluation Modernization, Grounded Anchors & Live Cognitive Gauntlet

**Sprint:** 63.0  
**Date:** August 25, 2026  
**Status:** 🏗️ PLANNING / INITIALIZED  
**Theme:** *Dual-Tier Evaluation Architecture (Vector Subsystem vs. Live Round Table), Grounded Hardware/BKM Anchors, Multi-Collection Routing, and Ledger Demarcation*

---

## 🧭 Executive Summary: Forensic Breakdown of Historical RAG EVAL Failures

A rigorous forensic audit of `validation_anchors.json` and `validation_ledger.jsonl` revealed the exact root causes behind historical RAG evaluation failures and why the pipeline felt disconnected from live lab reality:

### 1. The Multi-Collection Blind Spot (The Core Architectural Defect)
* **The Problem**: When `evaluate_rag.py` was originally constructed in July 2026, `ArchiveNode.get_context()` searched **only the 18-year career notes archive (`artifact_vault`)**.
* **The Failure**: When evaluated on queries regarding *"BKM-032"* or *"HomeLabAI setup guide"*, the engine searched legacy 2018 Intel notes rather than `behavioral_dna` (where BKMs live) or `feature_dna` (where lab modules live). Naturally, it retrieved unrelated TPMI/PAE files, and Kender rightfully failed the runs.
* **The Sprint 61/62 Foundation**: Sprint 61 delivered `LabDNARouter` and Sprint 62 delivered `TraversalDispatcher` (`[FEAT-117/467]`), establishing multi-collection scoping across `artifact_vault`, `behavioral_dna`, and `feature_dna`.

### 2. Synthetic & Outdated Evaluation Queries
* **The Problem**: `validation_anchors.json` contained only 5 synthetic questions with rigid, arbitrary keyword expectations (e.g., demanding the token `"montana"` on general telemetry queries).
* **The Failure**: The test set was disconnected from real-world validation experience, diamond-ranked gems, and low-level platform architecture.

### 3. Metric Pollution: Co-Pilot Human Corrections in the Automated Ledger
* **The Problem**: `[FEAT-456]` (Language-First Co-Pilot Feedback Loop) logs user conversational corrections (e.g., `"[ME] Wait, that's wrong, RAPL MSR 0x610 is PKG limit..."`) as `FAIL` entries to capture human ground truth.
* **The Failure**: On `status.html`, these human feedback traces were mixed into the same ledger table as automated RAG benchmark runs, creating the false visual impression of systemic RAG failure.

### 4. Bypassing the Live Cognitive Stack (Isolated Unit Testing Trap)
* **The Problem**: `evaluate_rag.py` invoked `ArchiveNode.get_context()` directly in isolation.
* **The Failure**: It bypassed `TriageEngine` (vibe/domain classification), `LabDNARouter` (collection selection), `InterestLoop` (speculative pre-fetching and gating), `BrainNode` (reasoning synthesis), and `PinkyCritic` (factual grounding verification). It evaluated only raw vector recall, not end-to-end cognitive intelligence.

---

## 🏛️ Architectural Consensus: Dual-Tier Evaluation Architecture

Sprint 63.0 formalizes a **Dual-Tier Evaluation Architecture**:

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

The evaluation suite is grounded in real 18-year validation history, platform telemetry registers, and lab operational BKMs:

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

## 🎯 Sprint Stories Breakdown

| Story | Subsystem | Description | Target Files |
| :--- | :--- | :--- | :--- |
| **63.1** | Config & Anchors | Author 10 grounded validation anchors with verified keyword sets and target collections. | `HomeLabAI/config/validation_anchors.json` |
| **63.2** | Subsystem Evaluator | Update `evaluate_rag.py` to route across multi-collection DNA (`LabDNARouter`) with `--mode vector`. | `Portfolio_Dev/field_notes/evaluate_rag.py` |
| **63.3** | Live Cognitive Gauntlet | Build live WebSocket end-to-end evaluation harness verifying Triage $\rightarrow$ Brain $\rightarrow$ Pinky Critic. | `HomeLabAI/src/tests/test_live_rag_eval.py`, `Portfolio_Dev/field_notes/evaluate_rag.py` |
| **63.4** | Ledger & UI Demarcation | Decouple automated RAG benchmarks from human co-pilot feedback in `validation_ledger.jsonl` & `status.html`. | `Portfolio_Dev/field_notes/status.html`, `Portfolio_Dev/field_notes/data/` |
| **63.5** | Gauntlet Verification | Execute Tier 1 Vector Benchmark (10/10) and Tier 2 Live Cognitive Gauntlet; compile site & certify. | `field_notes/build_site.py`, `00_FEDERATED_STATUS.md` |

---

## 🛡️ Definition of Done
1. `validation_anchors.json` contains 10 fully grounded queries with verified expectations.
2. `evaluate_rag.py --mode vector` executes in <2s with >90% keyword recall across multi-collection DNA.
3. `evaluate_rag.py --mode live` validates full Triage $\rightarrow$ Brain $\rightarrow$ Pinky Critic execution over WebSocket.
4. `status.html` cleanly demarcates Automated RAG Benchmarks from Co-Pilot Ground-Truth traces.
5. All tests pass, documentation is synchronized, and site builds with 0 link drift.
