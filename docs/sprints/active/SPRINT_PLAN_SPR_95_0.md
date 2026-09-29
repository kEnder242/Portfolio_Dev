# Sprint Plan: SPR-95.0 — The Document Spine & Single-Node Proving Ground
**Date:** September 29, 2026  
**Goal:** Implement the Document Spine topology (`FEAT-626` / `BKM-073`), decompose the 3-resume corpus into canonical decoupled bone nodes (`FEAT-585`), refocus Projection Studio as the single-node R&D proving ground with interactive revision blending (`FEAT-627`), and build the offline job/target ingestion CLI (`FEAT-622`).

---

## 🎯 Architectural Mandates (BKM-073 / BKM-070 / BKM-049 / BKM-024 / BKM-060)
1. **SPINE & BONE DECOUPLING LAW (BKM-073 / INS-041):** Document hierarchy (`spine.json`) is strictly decoupled from node mutation history (`bones/<node_id>.json`). Structural operations (`MOVE`/`DELETE`) mutate the spine index only; textual operations (`REWORD`/`BLEND`) append to bone version stacks only.
2. **LENS LITMUS INVARIANT (FEAT-585 / BKM-070):** The active Lens is the ultimate judge for node recommendations. Later revisions are assumed to be better by default; recommending an older revision requires explicit lens-specific justification. Quality inversions must be flagged as warnings regardless of lens.
3. **MICRO-SCALE SANDBOX BOUNDARY (FEAT-627):** `projection_studio.html` is strictly a single-node testing proving ground for LLM editorial dialectics and revision blending before promoting changes to `writer.html`.
4. **HERMETIC INGESTION (FEAT-622 / BKM-070):** Job scraping and target rubric compilation live in an isolated offline CLI (`src/ops/job_ingest.py`) outputting frozen JSON fixtures. Core projection runtimes remain 100% offline.
5. **TRI-LOOP DELEGATION MANDATE (BKM-049):** Every story declares an assigned owner (`[SWARM:LOCAL]`, `[SWARM:CLOUD]`, or `[AGY:PRIMARY]`). Local stories execute via single-shot `delegate.py` with the Psychological Safety Contract (`FEAT-625`) and up to 3 diagnostic remediation rounds before cloud escalation.

---

## 📊 Delegation Matrix

| Story ID | Title | Assigned Owner | Tool / Runner | Success Criteria |
| :--- | :--- | :--- | :--- | :--- |
| **Story 95.1** | Document Spine & Bone Node Storage Engine | `[SWARM:LOCAL]` | `delegate.py --story 951 --local` | `spine.json` and `bones/<node_id>.json` storage classes |
| **Story 95.2** | 3-Resume Corpus Decomposition & Join Engine | `[SWARM:LOCAL]` | `delegate.py --story 952 --local` | Non-destructive AST join of v1/v2/resume_data |
| **Story 95.3** | Single-Node Proving Ground & Revision Carousel | `[SWARM:LOCAL]` | `delegate.py --story 953 --local` | `projection_studio.html` single-node workbench |
| **Story 95.4** | Editorial Dialogue Gutter & Mutation Blending | `[SWARM:CLOUD]` | `delegate.py --story 954 --cloud` | Conversational LLM revision blending endpoint |
| **Story 95.5** | Offline Job & Target Ingestion CLI | `[SWARM:LOCAL]` | `delegate.py --story 955 --local` | Standalone `src/ops/job_ingest.py` scraper/compiler |
| **Story 95.6** | Cloud Oracle Adversarial Audit & Live Certification | `[SWARM:CLOUD]` | `delegate.py --oracle` | Full audit report & 100% test pass rate |

---

## 📋 Story Cards (With Just-In-Time Context)

### Story 95.1: Document Spine & Bone Node Storage Engine
* **Assigned Owner:** `[SWARM:LOCAL]` (M5 Air: `Hephaestus` / `Junior`)
* **Target:** `HomeLabAI/src/projection/bones.py`, `HomeLabAI/src/projection/engine.py`, `HomeLabAI/src/tests/test_spine_engine_unit.py`
* **JITC Anchors:** `[FEAT-626]`, `[BKM-073]`, `[INS-041]`
* **Scope:**
  1. Implement `SpineManager` in `bones.py`:
     - Load and save `papers/<paper_id>/spine.json` (`paper_id`, `title`, `sections` array with ordered `node_ids`).
     - Provide atomic structural operators: `insert_node(node_id, section, pos)`, `move_node(node_id, new_pos)`, `delete_node(node_id)`.
  2. Implement `BoneNode` in `bones.py`:
     - Load and save `bones/<node_id>.json` (`node_id`, `base_text` $v_1$, `revisions` list [$v_1 \dots v_n$], `hyde_voice`, `dna_anchors`, `updated_at`).
     - Provide atomic mutation operators: `add_revision(text, lens_id, rationale, hyde_voice)`.
  3. Write exhaustive unit tests in `src/tests/test_spine_engine_unit.py`.
* **Success Criteria:** 100% passing unit tests; zero shared mutable state between spine and bone nodes.

---

### Story 95.2: 3-Resume Corpus Decomposition & Join Engine
* **Assigned Owner:** `[SWARM:LOCAL]` (Kender 4090: `Atlas` / `Kender`)
* **Target:** `HomeLabAI/src/curator/decompose_resume.py`, `Portfolio_Dev/field_notes/data/papers/paper_resume/`
* **JITC Anchors:** `[FEAT-585]`, `[FEAT-626]`, `[WIS-487]`, `[BKM-070]`
* **Scope:**
  1. Parse `paper_resume_v1.json`, `paper_resume_v2.json`, and `resume_data.json`.
  2. Establish `paper_resume/spine.json` representing the master career outline.
  3. Decompose all bullet points into atomic `bones/res_<company>_<role>_<idx>.json` records:
     - $v_1$: Initial baseline text from v1 / resume_data.
     - $v_2$: Refined overlay from v2.
     - Stamp HyDE voice tags (`"formal"`, `"ATS-optimized"`, `"metric-heavy"`) and DNA links.
  4. Enforce CP-5 numeric literal preservation and CP-1 token containment across all extracted bone nodes.
* **Success Criteria:** Complete decomposition generated on disk with zero lost metrics or bullets; verified via schema validator.

---

### Story 95.3: Single-Node Proving Ground & Revision Carousel
* **Assigned Owner:** `[SWARM:LOCAL]` (M5 Air: `Hephaestus` / `Junior`)
* **Target:** `Portfolio_Dev/field_notes/projection_studio.html`, `Portfolio_Dev/field_notes/style.css`
* **JITC Anchors:** `[FEAT-627]`, `[FEAT-584]`, `[FEAT-617]`
* **Scope:**
  1. Refactor `projection_studio.html` into a focused single-node sandbox:
     - Top bar: Paper selector (`paper_resume`, `paper_jitc`) $\rightarrow$ Spine Node dropdown.
     - Left pane: Node Revision Carousel ($v_1 \dots v_n$) with active lens compatibility score pills.
     - Center pane: Hoverable "Reason Why" explanation badge and Quality Inversion alerts.
     - Right pane: Active Lens selector & Rubric Rule checklist.
  2. Pure vanilla JS/CSS with zero framework overhead.
* **Success Criteria:** Interactive UI allowing seamless navigation through a node's version history and real-time lens scoring.

---

### Story 95.4: Editorial Dialogue Gutter & Synthetic Mutation Blending
* **Assigned Owner:** `[SWARM:CLOUD]` (Big-Pickle / OpenRouter Free 256k)
* **Target:** `HomeLabAI/src/projection/recommender.py`, `HomeLabAI/src/curator/lens_service.py`
* **JITC Anchors:** `[FEAT-627]`, `[FEAT-618]`, `[BKM-073]`
* **Scope:**
  1. Implement `recommender.blend_revisions(node_id, v_a, v_b, human_instruction, lens_id)`:
     - Formulate structured prompt to LLM judge instructing synthesis of candidate $v_{n+1}$ blending specified qualities of $v_a$ and $v_b$.
     - Verify candidate $v_{n+1}$ against CP-5 numeric preservation.
  2. Implement backend REST endpoint `/api/node/blend` and wire up conversational gutter in `projection_studio.html`.
  3. Implement `[Approve & Stamp v_{n+1}]` handler to persist approved blend directly to `bones/<node_id>.json`.
* **Success Criteria:** Multi-turn chat successfully produces valid blended revisions approved and stamped by human operator.

---

### Story 95.5: Offline Job & Target Ingestion CLI
* **Assigned Owner:** `[SWARM:LOCAL]` (Kender 4090: `Atlas`)
* **Target:** `HomeLabAI/src/ops/job_ingest.py`, `Portfolio_Dev/field_notes/data/jobs/`
* **JITC Anchors:** `[FEAT-622]`, `[BKM-070]`, `[WIS-487]`
* **Scope:**
  1. Create standalone CLI `src/ops/job_ingest.py` accepting `--url <URL>` or `--file <path>`.
  2. Single-shot structured LLM call extracts:
     - `tier_0_structural`: Required technical tokens, degree/cert keywords, density limits.
     - `tier_1_semantic`: Hiring manager persona, domain impact focus, leadership tenets.
  3. Invoke `craft_lens()` and `persist_lens()` to output compiled rubric `field_notes/data/lenses/job_<slug>.json` and save frozen posting `field_notes/data/jobs/<slug>.json`.
* **Success Criteria:** Standalone CLI compiles valid, sub-millisecond bounded job rubrics runnable completely offline.

---

### Story 95.6: Cloud Oracle Adversarial Audit & End-to-End Certification
* **Assigned Owner:** `[SWARM:CLOUD]` / `[AGY:PRIMARY]`
* **Target:** `Portfolio_Dev/docs/sprints/active/ORACLE_REVIEW_SPRINT_95.md`
* **JITC Anchors:** `[BKM-049]`, `[BKM-024]`, `[BKM-068]`
* **Scope:**
  1. Execute Cloud Oracle adversarial review on all Sprint 95 endpoints.
  2. Run comprehensive test suite across `HomeLabAI` and `Portfolio_Dev`.
  3. Verify live daemon synchronization (`POST http://127.0.0.1:8765/reload_residents`).
* **Success Criteria:** 100% unit and integration test pass rate, Oracle report saved, and git checkpoint committed.
