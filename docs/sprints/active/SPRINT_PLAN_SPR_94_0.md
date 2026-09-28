# Sprint Plan: SPR-94.0 — The Projection Engine: Backend Organization & Core Use Cases
**Date:** September 28, 2026  
**Goal:** Transition from UI/UX scaffolding to backend organization and use case execution. Consolidate the Projection Engine package (`Story 94.6`), implement the DNA Manifest Bridge (`Story 94.1`), partition Symbolic vs Semantic rubric detectors (`Story 94.2`), enforce the Paper AST Schema v2 dynamic scoping gate (`Story 94.3`), and harden the nightly GPU compute envelope (`Story 94.5`).

---

## 🎯 Architectural Mandates (BKM-049 / BKM-015 / BKM-070 / BKM-024 / BKM-071)
1. **D-1 RE-ANCHORING LAW (BKM-070):** All projections project from immutable certified bones ($\pi(\mathcal{C})$) in diamond topologies; serial compounding chains are forbidden.
2. **BKM-015 ANTI-REGEX & STRUCTURAL PARTITIONING (BKM-015 / WIS-487 / FEAT-622):** Deterministic truth invariants (CP-1, CP-7) are enforced strictly by structural AST/schema traversal; semantic criteria (power-verbs, numeric assertion equivalence, style) are evaluated via LLM-judge. Custom regex matching for natural language evaluation is strictly banned.
3. **TRI-LOOP DELEGATION MANDATE (BKM-049):** Every story declares an assigned owner (`[SWARM:LOCAL]`, `[SWARM:CLOUD]`, or `[AGY:PRIMARY]`). Local stories execute via single-shot `delegate.py` dispatches with AGY-driven outer diagnostic loop (up to 3 diagnostic attempts) before cloud escalation. Direct takeover (`[AGY:TAKEOVER]`) is strictly forbidden without prior failed execution attempts.
4. **DNA DE-DUPLICATION & MERGE LAW (BKM-071):** Vector search ChromaDB `:8001` before adding DNA; merge >85% similar records.
5. **DOUBLE-WRITE & SYNCHRONIZATION (BKM-068):** Keep `FeatureTracker.md` and ChromaDB `:8001` synchronized with all changes.

---

## 📊 Delegation Matrix

| Story ID | Title | Assigned Owner | Tool / Runner | Success Criteria |
| :--- | :--- | :--- | :--- | :--- |
| **Story 94.4** | Cloud Oracle Adversarial Audit | `[SWARM:CLOUD]` | `delegate.py --mode oracle` | ✅ **COMPLETED** (`ORACLE_REVIEW_SPRINT_94.md`) |
| **Story 94.6** | Consolidated Projection Engine Backend | `[SWARM:LOCAL]` | `delegate.py --story 946` | Unified `HomeLabAI/src/projection/` package |
| **Story 94.1** | DNA Manifest Bridge (Vibe & Inspiration) | `[SWARM:LOCAL]` | `delegate.py --story 941` | Manifest populated with VIBE/INSPIRATION titles |
| **Story 94.2** | Symbolic vs Semantic Detector Budgeting | `[SWARM:LOCAL]` | `delegate.py --story 942` | `UNSAFE_TO_CRAFT` refusal branch + sub-ms filters |
| **Story 94.3** | Paper AST Schema v2 & Dynamic Scoping | `[SWARM:LOCAL]` | `delegate.py --story 943` | Dynamic `paper_id` scoping in `lens_service.py` |
| **Story 94.5** | Nightly GPU Thermal / Pacing Certification | `[AGY:PRIMARY]` | Native test runner | 100% test pass on final consolidated code |

---

## 📋 Story Cards

### Story 94.4: Cloud Oracle Adversarial Audit on Backend Projection Endpoints
* **Status:** ✅ **COMPLETED**
* **Assigned Owner:** `[SWARM:CLOUD]`
* **Target:** `Portfolio_Dev/docs/sprints/active/ORACLE_REVIEW_SPRINT_94.md`
* **Artifact:** Full audit report saved to `ORACLE_REVIEW_SPRINT_94.md`.

### Story 94.6: Consolidated Projection Engine Backend Package
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Target:** `HomeLabAI/src/projection/` (`__init__.py`, `engine.py`, `bones.py`, `lenses.py`, `recommender.py`)
* **Scope:**
  1. Create `HomeLabAI/src/projection/` consolidating scattered projection and recommendation logic:
     - `engine.py`: Core projection lifecycle (bone extraction, lens binding, AST transforms).
     - `bones.py`: Generic document AST parser, revision tagging, and diff/reconciliation operators.
     - `lenses.py`: Lens compiler, rule validator, and symbolic rubric detectors.
     - `recommender.py`: Topic triage adapter router, alignment matrix, mutation proposals, and cover letter synthesis.
  2. Implement unit test suite `HomeLabAI/src/tests/test_projection_engine_unit.py`.
* **Success Criteria:** Unified Python API callable by both CLI and web endpoints; 100% unit test pass rate.

### Story 94.1: DNA Manifest Bridge for VIBE & INSPIRATION Domains
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Target:** `Portfolio_Dev/scripts/dna_manifest_bridge.py`, `Portfolio_Dev/field_notes/data/dna_manifest.json`
* **Scope:**
  1. Create `dna_manifest_bridge.py` to ingest `dna/vibe_data.json` and inspiration records into `dna_manifest.json`.
  2. Populate titles for all PHL and VIBE cards so they render descriptive names in Writer Studio and Projection Studio dropdowns.
  3. Bar `RDNA` / `RESUME` from acting as lenses (`WIS-484`).
* **Success Criteria:** `dna_manifest.json` contains non-empty `vibe` and `inspiration` lists with populated titles.

### Story 94.2: Symbolic vs Semantic Detector Budgeting in Rubric Engine
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Target:** `HomeLabAI/src/projection/lenses.py`
* **Scope:**
  1. Refactor `craft_lens` to enforce total function compilation: emit valid bound rules with `UNSAFE_TO_CRAFT` refusal branch when input is invalid (`WIS-487`).
  2. Partition rules strictly into:
     - `tier_0_structural` (Deterministic AST node traversal: schema integrity, CP-1 token containment, CP-7 section isolation). **ZERO brittle regex matching for natural language / power verbs / numeric diffing (`BKM-015`).**
     - `tier_1_semantic` (LLM-judge with temperature=0 and JSON schema output for power-verb evaluation, style, and semantic assertion equivalence).
  3. Add `detector_budget` limits to prevent blocking execution loops.
* **Success Criteria:** `craft_lens` handles edge cases without silent default fallback; zero regex in semantic rubrics; unit tests pass.

### Story 94.3: Paper AST Schema v2 & Dynamic Scoping Gate
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Target:** `HomeLabAI/src/curator/validate_paper_schema.py`, `HomeLabAI/src/projection/`
* **Scope:**
  1. Fix the cross-paper output overwrite in grading so it dynamically writes to `PAPER-<paper_id>_v2_<lens>.json` instead of hardcoding `PAPER-RESUME_v2_*.json`.
  2. Create `validate_paper_schema.py` to validate Lens v2 and Rubric v2 JSON schemas against CP-1, CP-5, and CP-7 invariants.
* **Success Criteria:** Dynamic `paper_id` scoping respected; schema validator passes on all canonical paper ASTs.

### Story 94.5: Nightly LoRA GPU Thermal/Power Tuning & End-to-End Certification
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Target:** `HomeLabAI/src/infra/nightly_lora_training.py`, `HomeLabAI/src/infra/nightly_forge.py`
* **Scope:**
  1. Audit GPU power-clamp and batch pacing in `nightly_lora_training.py` (enforce persistent 165W clamp and inter-step CUDA cache purging via consolidated `[FEAT-160]`).
  2. Verify clean execution of unit and shakedown tests across the entire consolidated codebase.
  3. Commit local changes per BKM-009 / BKM-040.
* **Success Criteria:** 100% test suite passing, clean local git checkpoint.

---

## ⏸️ Deferred Items (Marked for Future Dedicated Sprints)
* **3-Resume AST Diffing & Multi-Document Join**: Deferred pending formal bone-ID derivation spec and merge operator ($M$) join semantics.
* **HiringCafe / ATS Scraper Integration**: Deferred pending structured requirements and ToS / legal posture alignment.

---

## 🛠️ Delegation & Quality Checklist (BKM-049 / BKM-024)
- [x] Every story has explicit assigned owner (`[SWARM:LOCAL]`, `[SWARM:CLOUD]`, `[AGY:PRIMARY]`).
- [ ] Subagent dispatches use REST `delegate.py` on port 4097 (no interactive CLI attachments).
- [ ] 3-attempt diagnostic retry gauntlet enforced before escalating local failures to cloud.
- [ ] Pre-flight AST and syntax validation (`python3 -m py_compile`, `node --check`).
- [ ] Fast unit tests verify isolated logic; live daemon verification confirms HEAD match.
- [ ] Double-write and local git checkpoint commits executed cleanly without remote push.
