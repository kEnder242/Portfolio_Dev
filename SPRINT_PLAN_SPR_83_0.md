# 🗺️ SPRINT PLAN: SPR-83.0
## Technical Deep-Dive & Strategic Architecture: Multi-Curriculum LoRA Curation, Round Table Memory & Nightly Forge Pipeline

> **Status:** PROPOSED / ARCHITECTURAL BLUEPRINT  
> **Session Anchor:** 2026-09-15 12:00 PDT  
> **Primary References:** [[BKM-024]], [[BKM-049]], [[PHL-031]], [[WIS-010]], [[FEAT-160]], [[FEAT-204]], [[FEAT-213]], [[FEAT-246]], [[FEAT-452]]  

---

### 1. Executive Summary & Forensic Context

Sprint 83.0 focuses entirely on **Neural Pedigree Curation, Nightly Forge Restoration, and Round Table Memory Hygiene**. 

A forensic audit of the training pipeline revealed that on August 9, 2026 (`commit 881fcd58`), `nightly_forge.py` was hardcoded to train exclusively on `journal_ledger.jsonl` (the live runtime conversational scratchpad). Over several weeks, the nightly burns ceased training on the three curated foundation datasets and began fine-tuning on live conversational artifacts, unparsed bracket tokens, and raw critic loops.

Sprint 83.0 re-establishes the foundational training curriculum, repairs the automated nightly forge pipeline, enforces multi-curriculum dataset blending ratios, and implements round-table memory lifecycle controls.

---

### 2. Tri-Curriculum Foundation Architecture

The nightly Unsloth burn on the RTX 2080 Ti is restored to a deterministic, weighted blend across the 3 core foundations + distilled gems:

```
┌────────────────────────────────────────────────────────────────────────┐
│ master_forge_curriculum.jsonl (Unified Training Curriculum)            │
├────────────────────────────────────────────────────────────────────────┤
│ • 40% User Voice & Directives: cli_voice_training.jsonl [FEAT-204]     │
│   (Multi-year Gemini CLI prompt logs + engineer notes & cadence)       │
├────────────────────────────────────────────────────────────────────────┤
│ • 35% Engineering Pedigree & BKMs: lab_history_training.jsonl [FEAT-160]│
│   (18 years of catches, architectural post-mortems, and BKM laws)      │
├────────────────────────────────────────────────────────────────────────┤
│ • 15% Situational Awareness & Vibe Schema: lab_sentinel.jsonl [FEAT-246]│
│   (Triage classification, vibe vectors, and dynamic tool pruning)      │
├────────────────────────────────────────────────────────────────────────┤
│ • 10% Curated Rank 4 Pearls (Airlocked Distillation Gate)              │
│   (Deduplicated, high-coherence round-table gems from distill_gems.py) │
└────────────────────────────────────────────────────────────────────────┘
```

---

### 3. Sprint 83.0 Story Breakdown & Delegation Matrix

#### 📋 Story 83.1: Multi-Curriculum Dataset Blender (`build_lora_datasets.py`)
- **Status:** ✅ COMPLETE
- **Assigned Owner:** `[SWARM:LOCAL]` $\rightarrow$ `[AGY:TAKEOVER]` (Silicon Fallback)
- **Objective:** Upgrade `HomeLabAI/src/forge/build_lora_datasets.py` to assemble `master_forge_curriculum.jsonl` using the strict 40/35/15/10 ratio, applying schema validation and length gates.
- **Verification:** Verified 1,000 instruction-response pairs assembled with 40% Voice, 35% Pedigree, 15% Sentinel, and 10% Gems. Schema verified 100% clean.
- **Deliverable:** `HomeLabAI/src/forge/build_lora_datasets.py` (commit `ffe32f1`).

#### 📋 Story 83.2: Nightly Forge Pipeline & Dataset Re-Anchoring (`nightly_forge.py`)
- **Status:** ✅ COMPLETE
- **Assigned Owner:** `[SWARM:LOCAL]` $\rightarrow$ `[AGY:TAKEOVER]` (Silicon Fallback)
- **Objective:** Update `HomeLabAI/src/infra/nightly_forge.py` to point `DATASET_PATH` to `master_forge_curriculum.jsonl` and enforce pre-flight dataset health checks before claiming GPU VRAM.
- **Verification:** `nightly_forge.py` updated to point to `master_forge_curriculum.jsonl` with automatic pre-flight builder trigger.
- **Deliverable:** `HomeLabAI/src/infra/nightly_forge.py` (commit `ffe32f1`).

#### 📋 Story 83.3: Round Table Memory Persistence & Context Pruning
- **Assigned Owner:** `[SWARM:LOCAL]`
- **Objective:** Implement structured persistence and pruning for the blackboard ledger (`journal_ledger.jsonl`), ensuring resident models have a bounded context window (recent N turns) while archiving older turns into long-term ChromaDB recall.
- **Deliverable:** `HomeLabAI/src/memory/blackboard_ledger.py` + `HomeLabAI/src/nodes/cognitive_hub.py`.

#### 📋 Story 83.4: LoRA Fidelity & Pedigree Evaluation Suite
- **Assigned Owner:** `[SWARM:LOCAL]`
- **Objective:** Build an automated post-training evaluation suite that queries the newly forged adapter on canonical prompts (BKM recall, User Voice phrasing, Triage vibe check) and asserts coherence before hot-reloading into production vLLM.
- **Deliverable:** `HomeLabAI/src/tests/test_forge_fidelity.py`.

---

### 4. Delegation & Architectural Guardrails

1. **BKM-049 Tri-Loop Protocol:** All stories in Sprint 83.0 are assigned to `[SWARM:LOCAL]`. Local diagnostic retries (max 3) must be exhausted before cloud escalation.
2. **Pedigree Invariant (PHL-031 / BKM-055):** Never feed raw unfiltered chat logs into neural weights. Training data must remain decoupled from live runtime state.
3. **Hardware Safety (FEAT-452):** Hardware pacing (5s settling delay) and 165W power limit clamping remain strictly enforced during all Unsloth training runs.
