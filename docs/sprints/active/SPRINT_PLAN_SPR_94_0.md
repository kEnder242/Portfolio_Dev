# Sprint Plan: SPR-94.0 — The Projection Engine: Backend Organization & Core Use Cases
**Date:** September 28, 2026  
**Goal:** Transition from UI/UX scaffolding to backend organization and use case execution. Implement the DNA Manifest Bridge (`FEAT-621`), partition Symbolic vs Semantic rubric detectors (`FEAT-622`), enforce the Paper AST Schema v2 dynamic scoping gate (`FEAT-623`), and harden the nightly GPU compute envelope.

---

## 🎯 Architectural Mandates (BKM-049 / BKM-070 / BKM-024)
1. **D-1 RE-ANCHORING LAW (BKM-070):** All projections project from immutable certified bones ($\pi(\mathcal{C})$) in diamond topologies; serial compounding chains are forbidden.
2. **SYMBOLIC PARTITIONING (WIS-051 / FEAT-622):** Deterministic truth invariants (CP-1, CP-4, CP-5, CP-7) are enforced strictly by sub-millisecond symbolic code; semantic LLM detectors are isolated for asynchronous styling.
3. **DELEGATION OWNER TAG MANDATE (BKM-049):** Every story declares an assigned owner (`[SWARM:LOCAL]`, `[SWARM:CLOUD]`, or `[AGY:PRIMARY]`). Local stories execute via `delegate.py` with 3 diagnostic retries before escalation.
4. **DOUBLE-WRITE & SYNCHRONIZATION (BKM-068):** Keep `FeatureTracker.md` and ChromaDB `:8001` synchronized with all changes.

---

## 📋 Story Cards

### Story 94.1: DNA Manifest Bridge for VIBE & INSPIRATION Domains
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Target:** `Portfolio_Dev/scripts/dna_manifest_bridge.py`, `Portfolio_Dev/field_notes/data/dna_manifest.json`
* **Scope:**
  1. Create `dna_manifest_bridge.py` to ingest `dna/vibe_data.json` and inspiration records into `dna_manifest.json`.
  2. Populate titles for all PHL and VIBE cards so they render descriptive names in Writer Studio and Projection Studio dropdowns.
  3. Ensure `load_dna_index()` in `publish_paper.py` resolves VIBE and INSPIRATION cards with valid text bodies.
* **Success Criteria:** `dna_manifest.json` contains non-empty `vibe` and `inspiration` lists with populated titles.

### Story 94.2: Symbolic vs Semantic Detector Budgeting in Rubric Engine
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Target:** `HomeLabAI/src/curator/lens_service.py`
* **Scope:**
  1. Refactor `lens_service.py:craft_lens` to enforce total function compilation: emit valid bound rules with `UNSAFE_TO_CRAFT` refusal branch when input is invalid (`WIS-054`).
  2. Partition rules into `tier_0_structural` (symbolic: regex, numeric subset CP-5, token containment CP-1) and `tier_1_semantic` (LLM-judge).
  3. Add `detector_budget` limits to prevent blocking execution loops.
* **Success Criteria:** `craft_lens` handles edge cases without silent default fallback; unit tests pass.

### Story 94.3: Paper AST Schema v2 & Dynamic Scoping Gate
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Target:** `HomeLabAI/src/curator/validate_paper_schema.py`, `HomeLabAI/src/curator/lens_service.py`
* **Scope:**
  1. Fix the cross-paper output overwrite in `lens_service.py:grade_paper` so it dynamically writes to `PAPER-<paper_id>_v2_<lens>.json` instead of hardcoding `PAPER-RESUME_v2_*.json`.
  2. Create `validate_paper_schema.py` to validate Lens v2 and Rubric v2 JSON schemas against CP-1, CP-5, and CP-7 invariants.
* **Success Criteria:** `grade_paper` respects dynamic `paper_id`; schema validator passes on all canonical paper ASTs.

### Story 94.4: Cloud Oracle Adversarial Audit on Backend Projection Endpoints
* **Assigned Owner:** `[SWARM:CLOUD]`
* **Target:** `Portfolio_Dev/docs/sprints/active/ORACLE_REVIEW_SPRINT_94.md`
* **Scope:**
  1. Dispatch `delegate.py --mode oracle --cloud-only` to review backend projection schemas, error models, and merge operators ($M$).
  2. Synthesize recommendations for multi-document AST consolidation and preference ledger recording (`WIS-056`).
* **Success Criteria:** Oracle synthesis report recorded with zero code regressions.

### Story 94.5: Nightly LoRA GPU Thermal/Power Tuning & End-to-End Certification
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Target:** `HomeLabAI/src/infra/nightly_lora_training.py`, `HomeLabAI/src/infra/nightly_forge.py`
* **Scope:**
  1. Audit GPU power-clamp and batch pacing in `nightly_lora_training.py` (adjust step limits and enforce persistent 165W clamp across subprocesses to prevent hardware reset trips during sustained backpropagation).
  2. Verify clean execution of unit and shakedown tests.
  3. Commit local changes per BKM-009 / BKM-040.
* **Success Criteria:** 100% test suite passing, clean local git checkpoint.
