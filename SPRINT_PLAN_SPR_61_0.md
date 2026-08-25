# 🚀 Sprint Plan SPR-61.0: Epistemic Meta-Grounding & Triage Calibration

**Sprint:** 61.0  
**Date:** August 25, 2026  
**Status:** PLANNING & ARCHITECTURAL REVIEW  
**Theme:** *Epistemic Meta-Grounding: Connecting the Mice to the Lab's Internal DNA (`feature_dna` / `behavioral_dna`)*

---

## 🧭 Executive Summary & Co-Pilot Review

During recent live-fire co-pilot sessions across Sprints 59 and 60, four distinct units of real-world user feedback were surfaced and recorded in the system ledger. 

While the satellite refactoring in Sprint 60 successfully decoupled our background engines with 216/216 passing tests, live conversational analysis revealed a fundamental **Persona Grounding Disconnect**:
> *"The mice are trying too hard to talk about my experience rather than noting that I'm talking about the lab. I think this might be a good way to triage how vibe='meta' can be more effectively discovered."*

Currently, when the user discusses the Lab's internal systems, state, features (`FEAT-xxx`), or architecture, the resident models (Pinky/Brain) over-index on Jason's 18-year silicon validation career history (`raw_notes` / `career_ledger`) and fail to recognize that the prompt is a **Meta-Discussion about the Lab itself**.

Sprint 61.0 introduces **Epistemic Meta-Grounding**: calibrating the triage engine with `vibe="META"`, grafting internal Lab DNA (`feature_dna`, `behavioral_dna`, `LAB_INFRASTRUCTURE.md`) into context, and training the personas to cleanly separate *Jason's Silicon Validation Career* from *Acme Lab's Internal Architecture*.

---

## 📊 Review of 4 User Feedback Units (Coherence & Verification Ledger)

| Feedback Unit | Origin / Query | Coherence & Root Cause Analysis | System Action Taken & Status |
| :--- | :--- | :--- | :--- |
| **Unit 1: RAPL MSR 0x610 Domain Error** | `"[ME] Wait, that's wrong, RAPL MSR 0x610 is PKG limit, not DRAM."` | **High Coherence**: Live validation ground-truth correction. Highlighted that Fourth Wall interception must capture technical register semantics. | ✅ Intercepted by `feedback_interceptor.py`, appended FAIL record to `validation_ledger.jsonl`, weaved into Pinky intuition on next turn. |
| **Unit 2: Definition of Integration Testing** | *"When I say 'integration' test I mean we use the lab, live... if we didn't restart it, we didn't test the changed code."* | **High Coherence**: In-process mock tests verify unit isolation, but true integration testing requires restarting the live daemon and validating physical network/disk contracts. | ✅ Added Story 60.4 (Lab Stack Restart) and Story 60.5 (Live WebSocket Gauntlet) to all sprint architectures. Saved in ICM (`01M0XD63PMHXY3XZEKZ42JNTCV`). |
| **Unit 3: Intercom Transcript Prefix Collisions** | `"[ME] ..."` / `"[USER] ..."` transcript frames | **High Coherence**: Live Web Intercom prefixes speech turns with `[ME]`, breaking start-of-string regex anchors (`^(?:wait|no\b)`). | ✅ Added `re.sub(r"^\[(?:ME|USER)\]\s*", "", ...)` across `feedback_interceptor.py`, `floating_oracle.py`, and `override_parser.py`. |
| **Unit 4: Persona Over-Indexing on Career Experience vs. Lab Meta-Knowledge** | *"The mice are trying too hard to talk about my experience rather than noting that I'm talking about the lab."* | **High Coherence (Architectural Gap)**: Triage lacks a `vibe="META"` category. The Lab's internal DNA (`FeatureTracker.md`, `Protocols.md`) was synced to ChromaDB, but `ArchiveNode` prioritized `career_ledger` for queries lacking explicit `FEAT-` numbers. | 🎯 **Target of Sprint 61.0**: Introduce `vibe="META"` triage discovery, Lab DNA vector prioritization, and persona calibration. |

---

## 🏛️ Architectural Gap Analysis: Did We Intentionally Hide Lab Knowledge?

**No! The knowledge exists, but the routing pipeline lacked a meta-switch.**

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ CURRENT ROUTING: Over-indexing on Career Archive                                                  │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ User Query: "hey pinky, how is the audio pipeline behaving?"                                      │
│   ├── Triage: vibe="CASUAL", domain="exp_tlm"                                                    │
│   ├── ArchiveNode: Queries ChromaDB -> Returns [CAREER: 2018 PCIe Validation]                    │
│   └── Pinky Persona: "Back when Jason was validating PCIe Gen3 telemetry at Intel..." (WRONG!)   │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ SPRINT 61 TARGET: Epistemic Meta-Grounding                                                       │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ User Query: "hey pinky, how is the audio pipeline behaving?"                                      │
│   ├── Triage: vibe="META", domain="lab_internal"                                                 │
│   ├── ArchiveNode: Queries feature_dna / behavioral_dna -> Returns [FEATURE_DNA: FEAT-059]       │
│   └── Pinky Persona: "Narf! AudioPipeline (FEAT-059) is active with 24k sliding windows!" (CORRECT) │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Granular Refactoring Stories for Sprint 61.0

### **Story 61.1: [FEAT-457/TRIAGE-01] Triage Meta-Vibe & Lab Domain Discovery**
* **Status**: 🔲 **READY FOR IMPLEMENTATION**
* **Target Files**:
  * `HomeLabAI/src/logic/cognitive_hub.py`
  * `HomeLabAI/src/tests/test_triage_meta_vibe.py`
* **Scope**:
  * Expand Triage intent classifier prompt and parser to recognize `vibe="META"` and `domain="lab_internal"`.
  * Trigger keywords: `lab`, `foyer`, `pinky`, `brain`, `ear`, `pipeline`, `router`, `feature`, `bkm`, `override`, `status`, `health`, `vllm`, `attendant`.
  * Ensure HyDE vector text reflects system architecture rather than career validation terms.

---

### **Story 61.2: [FEAT-458/ARCHIVE-01] Lab DNA Priority Routing in Multi-Collection Reranker**
* **Status**: 🔲 **READY FOR IMPLEMENTATION**
* **Target Files**:
  * `HomeLabAI/src/nodes/archive_node.py`
  * `HomeLabAI/src/tests/test_archive_lab_dna_routing.py`
* **Scope**:
  * When query has `vibe="META"` or `domain="lab_internal"`, `ArchiveNode` boosts weights for `feature_dna`, `behavioral_dna`, and `lab_journal` collections.
  * Formats extracted context with direct `[FEATURE_DNA: FEAT-xxx]` and `[BKM: BKM-xxx]` tags.
  * Prevents `career_ledger` from polluting the context window during system operations.

---

### **Story 61.3: [FEAT-459/PERSONA-01] Persona Grounding & Identity Calibration**
* **Status**: 🔲 **READY FOR IMPLEMENTATION**
* **Target Files**:
  * `HomeLabAI/src/nodes/pinky_node.py`
  * `HomeLabAI/src/nodes/brain_node.py`
  * `HomeLabAI/src/tests/test_persona_grounding.py`
* **Scope**:
  * Update system prompt instructions for Pinky and Brain:
    1. **Personal Mode (Default)**: Discuss Jason's 18-year career history when answering questions about past validation, silicon engineering, and leadership.
    2. **Meta Mode (When `[FEATURE_DNA]` or `[BEHAVIORAL_DNA]` is present)**: Discuss Acme Lab's live software, pipelines, daemons, and architecture directly as active lab operators.

---

### **Story 61.4: [OPS-01] Mandatory Lab Stack Restart & Quiescence Validation**
* **Status**: 🔲 **PLANNED**
* **Scope**:
  * Restart `acme-lab.service` via `systemctl --user restart acme-lab`.
  * Respect [FEAT-136] Quiescence 60s stability window.
  * Verify `http://127.0.0.1:8765/version` reports `boot_commit == <HEAD>`.

---

### **Story 61.5: [TEST-01] Live-Fire Service Integration Suite (`test_live_sprint61_e2e.py`)**
* **Status**: 🔲 **PLANNED**
* **Scope**:
  * Connect over physical WebSockets (`ws://127.0.0.1:8765`).
  * Send meta query: `"[ME] Pinky, what is the status of our audio pipeline and thermal sweeper?"`
  * Verify Pinky responds with `FEAT-059` / `LAB-099` details without mentioning Intel/PCIe career history.
  * Send career query: `"[ME] Pinky, tell me about Jason's validation work on PCIe error bursts."`
  * Verify Pinky responds with career validation history.

---

## 🗺️ Existing Test Earmarks & Defeaturing Map

| Test Suite | Subsystem | Action | Target Story |
| :--- | :--- | :--- | :--- |
| `src/tests/test_multi_collection_reranker.py` | Multi-Collection Reranker | **ENHANCE** (Add meta-vibe collection weight assertions) | Story 61.2 |
| `src/tests/test_floating_oracle.py` | Shallow Turn & Casual Pool | **PRESERVE** (Ensure shallow meta queries aren't swallowed) | Story 61.1 |
| `src/tests/test_sprint60_integration.py` | Satellite Integration Baseline | **PRESERVE** (Core regression baseline) | Regression Suite |

---

## 🧭 Execution Order

1. **Story 61.1**: Triage Meta-Vibe Discovery (`cognitive_hub.py`).
2. **Story 61.2**: Lab DNA Collection Weight Boost (`archive_node.py`).
3. **Story 61.3**: Persona Grounding Calibration (`pinky_node.py` & `brain_node.py`).
4. **Story 61.4**: Lab Stack Bounce & Quiescence Validation (`acme-lab.service`).
5. **Story 61.5**: Live-Fire Service Integration Suite (`test_live_sprint61_e2e.py`).
6. **Feature Links & Docs**: Update `FeatureTracker.md` and rebuild Field Notes.
