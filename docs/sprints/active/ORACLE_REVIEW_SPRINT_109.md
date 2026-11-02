# 🔮 Adversarial Oracle Audit Report: Sprint 109.0

**Sprint:** SPR-109.0 (Pre-Flight Adversarial Architecture Audit)  
**Evaluator:** Tier 1 Strategic & Adversarial Architecture Oracle (`[SWARM:ORACLE]` / AGY)  
**Timestamp:** 2026-11-02  
**Target Document:** [`Portfolio_Dev/docs/sprints/active/SPRINT_PLAN_SPR_109_0.md`](file:///home/jallred/Dev_Lab/Portfolio_Dev/docs/sprints/active/SPRINT_PLAN_SPR_109_0.md)  
**Target Codebase:** `HomeLabAI` (branch `main`), `Portfolio_Dev` (branch `main`)  
**Governing BKMs & Invariants:** `[BKM-005]`, `[BKM-007]`, `[BKM-015]`, `[BKM-020]`, `[BKM-024]`, `[BKM-043]`, `[BKM-049]`, `[BKM-061]`, `[BKM-062]`, `[BKM-069]`, `[BKM-080]`, `[BKM-081]`, `[BKM-082]`, `[BKM-085]`, `[BKM-086]`, `[BKM-088]`, `[BKM-089]`, `[FEAT-059]`, `[FEAT-451]`, `[FEAT-540]`, `[FEAT-673]`, `[FEAT-682]`, `[FEAT-683]`, `[INS-047]` ("Live is King, History is Queen")

---

## 1. Executive Assessment & Macro Architectural Verdict

### 🏛️ The Verdict: **CONDITIONALLY APPROVED WITH 7 MANDATORY ADVERSARIAL SAFEGUARDS**

The Sprint 109.0 architecture—grounded in the restoration of the 4-Tier Epistemic Memory Hierarchy (`FEAT-683`), Density-Weighted Archive Queue Scheduling (`FEAT-682`), Non-Destructive Navigational Companion Mapping (`.map.json`), Automated Ripgrep Ground Truth Hydration (`FEAT-451`), Pre-Triage Focal Gravitational Steering (`FEAT-540`), Excision of `disentangle_chronology()` Guessing Fallbacks, and Always-Live Multi-Node Projection Studio (`FEAT-059` / `FEAT-673`)—is **architecturally necessary and directionally correct**.

Forensic git archaeology and sprint lookback confirm this sprint permanently closes the "Flattened Prompt String" regression from Sprint 47 and the "Date Guessing Hallucination" introduced in Sprint 106.

However, an exhaustive adversarial audit of the specifications against the **actual current codebase state** reveals **seven critical failure modes** and **three spec-to-implementation drift gaps** that must be hardened in the concrete story specifications prior to execution.

---

## 2. Adversarial Peer Review & Edge-Case Analysis

| Risk Dimension | Oracle Finding / Failure Mode | Architectural Mitigation Required | Status |
| :--- | :--- | :--- | :--- |
| **1. `focal_dna` Wiring Drift (FEAT-540 → FEAT-683)** | Sprint Plan Story 109.6 claims: *"In `HomeLabAI/src/logic/cognitive_hub.py` (`step_pre_triage`), add `focal_dna` to the pre-triage probe target collections."* **Reality:** `step_pre_triage` delegates to `probe_clara_dna_sync()` in `vector_pre_triage.py`, which uses `PRE_TRIAGE_COLLECTIONS` list. `focal_dna` is **absent** from this list. The fix location is `vector_pre_triage.py:21-32`, not `cognitive_hub.py`. | **Mandate:** Update `PRE_TRIAGE_COLLECTIONS` in `vector_pre_triage.py` to include `"focal_dna"`. Verify ChromaDB collection `focal_dna` exists (Story 109.5 dependency). Add integration test asserting `probe_clara_dna_sync("AEP Optane")` returns `focal_dna` match. | **MANDATED IN STORY 109.6** |
| **2. `calculate_file_priorities()` Missing Implementation (FEAT-682)** | Story 109.8 test asserts `from field_notes.scan_queue import calculate_file_priorities`. **Reality:** `scan_queue.py` has **no such function**. The priority formula `Total File Lines / (Indexed Gems + 1)` requires: (a) line counting of raw notes files, (b) gem counting from ChromaDB `long_term_wisdom` + monthly JSONs, (c) sorting logic. Division-by-zero guarded by `+1`, but **empty files (0 lines) yield priority 0** — starves them permanently. | **Mandate:** Implement `calculate_file_priorities()` in `scan_queue.py` with: (1) `wc -l` on raw notes, (2) gem count via `long_term_wisdom` query + JSON scan, (3) floor priority `epsilon=0.001` for empty files, (4) unit test for 0-line edge case. | **MANDATED IN STORY 109.8** |
| **3. `.map.json` Companion Pipeline — Zero Implementation Exists** | Story 109.3 specifies 3-tier pipeline: Host Python Slicer → M5 Air Semantic Mapper → AGY Judge Probe → `probe_companion_map.py`. **Reality:** `probe_companion_map.py` **does not exist**. `notes_2005_SSPD.map.json` **does not exist**. The mechanical slicer (4+ newlines / ASCII dividers) is unspecified in code. Test asserts `len(sections) >= 90` — arbitrary without knowing file structure. | **Mandate:** (1) Implement `slice_gap_file()` in `scan_queue.py` or new `companion_map.py` using `\n{4,}` and `^={3,}$` regex. (2) Create `probe_companion_map.py` that loads slices, calls M5 Air MLX endpoint (`:8002`) for semantic labeling, writes `.map.json`. (3) Test must derive expected section count from actual file analysis, not magic number. | **MANDATED IN STORY 109.3** |
| **4. `context_envelope` Scoping — No Implementation in `scan_queue.py` or `refine_gem.py`** | Story 109.7: *"In `field_notes/scan_queue.py` and `field_notes/refine_gem.py`: Check `is_gap_file`... attach `context_envelope`."* **Reality:** Neither file has `context_envelope` logic. `scan_queue.py` produces queue tasks with `content` but no envelope. `refine_gem.py` processes gems but has no envelope parameter. `test_context_envelope_scoping.py` **does not exist**. | **Mandate:** (1) Add `is_gap_file` detection to `scan_queue.py` (reuse `GAP_FILES` logic from `scan_pinky.py`). (2) Add `context_envelope` field to queue task schema: `{"before": lines[s-5:s], "after": lines[e:e+5]}`. (3) Modify `refine_gem.py` refinement prompt to accept envelope and emit `[ENVELOPE_BEFORE]`/`[ENVELOPE_AFTER]` tags. (4) Create `test_context_envelope_scoping.py` with gap vs. standard file fixtures. | **MANDATED IN STORY 109.7** |
| **5. Ripgrep Bridge — `curated_anchors` Extraction Not Wired** | Story 109.9: *"Between Brain's filter step and Deep Thought's turn in `cognitive_hub.py`, automatically extract Brain's `curated_anchors`... Execute `execute_grep_search_pivot(curated_anchors=curated_anchors)`."* **Reality:** `cognitive_hub.py` has **no extraction of `curated_anchors`** from Brain's Stage 1 output. `execute_grep_search_pivot` exists in `archive_node.py` and accepts `curated_anchors` parameter, but the pipeline integration is missing. The test `test_ripgrep_hydration.py` **does not exist**. | **Mandate:** (1) In `cognitive_hub.py` Stage 1→2 handover, parse Brain's `[BEDROCK SELECTION]` kept chunks for hardware anchors (regex: `0x[0-9a-f]+`, `[A-Z]{3,}`, `\w+\.(py|sh|c|h)`). (2) Pass extracted anchors to `archive_node.execute_grep_search_pivot()` via MCP tool call. (3) Inject results into Deep Thought's prompt as `<ground_truth_exhaust>`. (4) Create `test_ripgrep_hydration.py` with mocked Brain output. | **MANDATED IN STORY 109.9** |
| **6. `disentangle_chronology()` Excision — Function Exists with Hardcoded Fallbacks** | Story 109.10: *"Deprecate and remove `disentangle_chronology()` in `field_notes/refine_gem.py`."* **Reality:** Function exists at lines 96-197 with **hardcoded `doc_year = 2024` default (line 100)** and **`06-01` fallback (line 158)**. It is **actively called** at lines 560-564 and 717-722 in `RotationalRefinementEngine.populate_queue_from_archive()` and `advance_gem_pass()`. Removal requires replacing all call sites with spatial anchor logic from `.map.json` (Story 109.3 dependency). | **Mandate:** (1) Add `spatial_anchor` (`line_start`, `line_end`) and `temporal_anchor` fields to gem schema. (2) Modify `populate_queue_from_archive()` and `advance_gem_pass()` to read anchors from `.map.json` (when available) or chunk metadata. (3) Only after all call sites migrated, delete `disentangle_chronology()`. (4) Test: `pytest field_notes/tests/test_gem_refiner.py` asserting zero `06-01` or `2024` defaults on pre-2020 gems. | **MANDATED IN STORY 109.10** |
| **7. Projection Studio — File Does Not Exist; No Multi-Node Dispatch Logic** | Story 109.12: *"Purge all static stub response paths in `Portfolio_Dev/field_notes/projection_studio.js` and server routes."* **Reality:** `projection_studio.js` **does not exist**. No server routes for multi-node dispatch exist. The test assertion is manual browser verification — **not automatable**. | **Mandate:** (1) Create `projection_studio.js` with WebSocket client connecting to Foyer (`:8765`) and three node endpoints. (2) Implement `/api/projection/dispatch` route in `foyer/router.py` that fans out to: `z87-Linux:8088` (vLLM), `KENDER:11434` (Ollama), `Node Brain:8002` (MLX). (3) Add error handling: node timeout → show "Node Unreachable" card; partial results → render available cards. (4) Replace manual test with Playwright test asserting 3 concurrent streams. | **MANDATED IN STORY 109.12** |

---

## 3. Spec-to-Implementation Drift Gaps (Missing Artifacts)

| Story | Missing Artifact | Required Action |
| :--- | :--- | :--- |
| **109.5** | `field_notes/ingest_focals.py` | Create script parsing 10 annual review `.doc`/`.docx` files using `docx2txt`/`antiword`, outputting `focal_mesh.json` and ingesting to ChromaDB `focal_dna`. |
| **109.11** | `field_notes/probe_focal_draft_detection.py` | Create empirical probe with AGY judge asserting `FOCAL_DRAFT` tagging on `notes_2018_PAE.txt` and `notes_2024_PIAV.txt`. Add `FOCAL_DRAFT` logic to `refine_gem.py` refinement prompt. |
| **109.3** | `probe_companion_map.py` + `.map.json` schema | Define `.map.json` schema: `{sections: [{line_start, line_end, section_title, platform, implied_era, chunk_type}]}`. Implement 3-tier pipeline. |
| **109.7** | `test_context_envelope_scoping.py` | Create test with gap file fixture (expects envelope) and standard file fixture (expects no envelope). |
| **109.8** | `calculate_file_priorities()` in `scan_queue.py` | Implement with line counting, gem counting, epsilon floor. |
| **109.9** | `test_ripgrep_hydration.py` | Create test with mocked Brain curated_anchors, verify grep pivot execution <8ms. |
| **109.10** | `test_gem_refiner.py` | Create test asserting no `06-01`/`2024` fallbacks on pre-2020 gems. |
| **109.12** | `projection_studio.js` + `/api/projection/dispatch` route | Create frontend + backend dispatch with error handling. |

---

## 4. Story-by-Story Adversarial Directives

### Story 109.1: `notes_2005_SSPD.txt` Fresh Start, State Purge & Symlink
* **Failure Mode:** Symlink `notes_2005.txt` → `notes_2005_SSPD.txt` breaks `scan_pinky.py` `GAP_FILES` which references `raw_notes/notes_2005_SSPD.txt` but the symlink is in `knowledge_base/`.
* **Directive:** Update `scan_pinky.py:22-26` `GAP_FILES` to use `knowledge_base/notes_2005_SSPD.txt` (symlink target) or ensure `raw_notes/` is a symlink to `knowledge_base/`. Verify both paths resolve.

### Story 109.2: Single-Pass Date Normalization
* **Failure Mode:** Regex `^(\d{1,2})-(\d{1,2})-(\d{2,4})\b` misses dates with leading whitespace or tabs. `notes_2015_DSD.txt` lines 18,000–26,313 range is hardcoded — fragile if file changes.
* **Directive:** Use `^\s*(\d{1,2})-(\d{1,2})-(\d{2,4})\b`. For 2015 tail, detect year transition programmatically (scan for first `2012` dash date) rather than hardcoding line numbers.

### Story 109.3: Navigational Companion Files (`.map.json`) via 3-Tier Pipeline
* **Failure Mode:** M5 Air MLX endpoint (`:8002`) may be unreachable. Pipeline must fail-soft with local heuristic fallback (platform regex from `PLATFORM_ERA_MAP` in `refine_gem.py`).
* **Directive:** Implement `probe_companion_map.py` with timeout + fallback. `.map.json` must include `source_file_hash` for invalidation detection.

### Story 109.4: Formal Registration of `[FEAT-683]`
* **Failure Mode:** `FeatureTracker.md` currently has `[FEAT-102]` (Nuclear Cache Busting) at line 466. Sprint plan claims "Avoided recycling `FEAT-102`" but it **already exists** in FeatureTracker. `FEAT-683` and `FEAT-682` must be appended, not replace.
* **Directive:** Append `FEAT-682` and `FEAT-683` entries to `FeatureTracker.md`. Add deprecation pointers on `FEAT-405`/`FEAT-410` (Multi-Stage Retrieval / Adaptive Temporal RAG) as "Superseded by FEAT-683".

### Story 109.5: Annual Reviews Ingestion into `focal_mesh.json` & `focal_dna`
* **Failure Mode:** `focal_ledger.json` already exists with 5 focal gems (2009, 2015, 2018, 2019×2). Annual reviews (2008-2018) may duplicate. ChromaDB `focal_dna` collection **does not exist** — must be created.
* **Directive:** `ingest_focals.py` must deduplicate against `focal_ledger.json` by `event_era` + `summary` similarity. Create `focal_dna` collection via `chromadb.HttpClient`. Test asserts `count() >= 10` — but only 10 annual reviews exist; some years may yield 0 focals. Relax to `>= 5` new focals.

### Story 109.6: Wiring `step_pre_triage` (`FEAT-540`) to `focal_dna`
* **Failure Mode:** As documented in Risk #1, the wiring point is `vector_pre_triage.py:21-32` `PRE_TRIAGE_COLLECTIONS`, not `cognitive_hub.py`. Also, `focal_dna` collection must exist (Story 109.5 dependency).
* **Directive:** Add `"focal_dna"` to `PRE_TRIAGE_COLLECTIONS`. In `probe_clara_dna_sync()`, add `elif best_col == "focal_dna": hint += " Contains Career Strategic Milestones."; suggested_vibe = "CHRONICLE"`. Update test to assert `AEP Optane` query returns `focal_dna` match.

### Story 109.7: Scoping `context_envelope` Exclusively to Gap Files
* **Failure Mode:** `scan_queue.py` has no concept of `is_gap_file`. `refine_gem.py` has no envelope parameter. The refinement prompt instruction `"*Use [ENVELOPE_BEFORE] only to resolve orphan headers...*"` must be injected into the actual prompt template.
* **Directive:** Add `is_gap_file` detection to `scan_queue.py` (reuse `scan_pinky.py` logic). Extend queue task schema with optional `context_envelope`. Modify `RotationalRefinementEngine.advance_gem_pass()` to pass envelope to refinement prompt.

### Story 109.8: Density-Weighted Archive Queue Scheduler (`FEAT-682`)
* **Failure Mode:** Priority formula `Total File Lines / (Indexed Gems + 1)` — "Indexed Gems" definition ambiguous: ChromaDB `long_term_wisdom` count? Monthly JSON gem count? Both? Also, `notes_2024_PIAV.txt` (32K lines) with hundreds of gems yields low priority — correct. But `notes_2005_SSPD.txt` (2,700 lines) with 0 gems yields priority 2700 — correct. **Edge case:** New file with 0 lines → priority 0 (starved). **Fix:** `max(epsilon, lines / (gems + 1))`.
* **Directive:** Implement `calculate_file_priorities()` returning sorted list of `{"filename", "priority", "lines", "gems"}`. Use `wc -l` for lines. Count gems from monthly JSONs (rank >= 2) + `long_term_wisdom` query. Unit test for 0-line file.

### Story 109.9: Ground Truth Ripgrep Bridge (`FEAT-451`) & Path Verification
* **Failure Mode:** `execute_grep_search_pivot()` searches `~/Dev_Lab/Portfolio_Dev/field_notes/data` and `~/knowledge_base`. But `cognitive_hub.py` has **no call** to this function. The "Brain's filter step" (Stage 1) produces `[BEDROCK SELECTION]` kept chunks — anchors must be extracted from these.
* **Directive:** In `cognitive_hub.py` `step_triage()` or new `step_ground_truth_hydration()`, parse Brain's kept chunks for hardware anchors. Call `archive_node.execute_grep_search_pivot(curated_anchors=anchors)` via MCP. Inject into Deep Thought prompt. Create `test_ripgrep_hydration.py`.

### Story 109.10: Excision of `disentangle_chronology()` in Favor of Spatial Anchors
* **Failure Mode:** Function called in two places in `RotationalRefinementEngine`. `.map.json` (Story 109.3) must exist first. Spatial anchor schema: `{"line_start": int, "line_end": int, "source_file": str}`. Temporal anchor: `{"era": "2005-Q1", "precision": "QUARTER"}`.
* **Directive:** Sequence: (1) Story 109.3 delivers `.map.json`. (2) Add `spatial_anchor`/`temporal_anchor` to gem schema. (3) Migrate `populate_queue_from_archive()` and `advance_gem_pass()` to read anchors. (4) Delete `disentangle_chronology()`. (5) Test asserts no fallback dates.

### Story 109.11: `FOCAL_DRAFT` Prompt Tagging & AGY Verification Probe
* **Failure Mode:** `refine_gem.py` refinement prompt has no `FOCAL_DRAFT` instruction. `probe_focal_draft_detection.py` does not exist. AGY judge probe requires `probe_focal_draft_detection.py` to exist and return score ≥ 0.90.
* **Directive:** Add to `refine_gem.py` refinement prompt: `*If the chunk text represents a retrospective career summary, self-assessment, or focal draft, label its type as FOCAL_DRAFT and identify the corresponding Tier 2 milestone.*` Create probe script with test fixtures from `notes_2018_PAE.txt` and `notes_2024_PIAV.txt`.

### Story 109.12: Live Engine Integration & Multi-Node Comparison Matrix
* **Failure Mode:** `projection_studio.js` does not exist. No `/api/projection/dispatch` route. Three node endpoints have different APIs: vLLM (`/v1/completions`), Ollama (`/api/generate`), MLX (`/v1/chat/completions` via Headroom). Unified dispatch requires adapter layer.
* **Directive:** Create `projection_studio.js` with three WebSocket connections or Server-Sent Events. Backend route fans out to node adapters. Handle: node timeout (5s), partial results, stream synchronization. Playwright test: load page, send prompt, assert 3 streaming cards appear within 10s.

---

## 5. Delegation & Anti-Bypass Matrix (`BKM-049`)

| Story ID | Assigned Swarm Owner | Execution Mechanism | Architectural Justification |
| :--- | :--- | :--- | :--- |
| **Story 109.1** | `[AGY:PRIMARY]` | Direct AGY Execution | File ops + symlink + manifest update — low blast radius, high precision. |
| **Story 109.2** | `[AGY:PRIMARY]` | Direct AGY Execution | Deterministic regex normalization — no LLM needed. |
| **Story 109.3** | `[SWARM:LOCAL]` + `[AGY:PRIMARY]` | `delegate.py --mode local` (Atlas on M5 Air) + AGY Judge | 3-tier pipeline: Python slicer (local) → M5 Air semantic labeling → AGY certification. |
| **Story 109.4** | `[AGY:PRIMARY]` | Direct AGY Execution | Documentation update only. |
| **Story 109.5** | `[AGY:PRIMARY]` | Direct AGY Execution | Doc parsing + ChromaDB ingestion — sequential, deterministic. |
| **Story 109.6** | `[SWARM:LOCAL]` | `delegate.py --mode local` | Surgical edit to `vector_pre_triage.py` `PRE_TRIAGE_COLLECTIONS` + hint logic. |
| **Story 109.7** | `[SWARM:LOCAL]` | `delegate.py --mode local` | `scan_queue.py` + `refine_gem.py` modifications — bounded context. |
| **Story 109.8** | `[SWARM:LOCAL]` | `delegate.py --mode local` | New function in `scan_queue.py` with math — Atlas on 4090. |
| **Story 109.9** | `[SWARM:CLOUD]` | `delegate.py --mode cloud` | Cross-file integration: `cognitive_hub.py` → `archive_node.py` MCP call — high blast radius. |
| **Story 109.10** | `[AGY:PRIMARY]` | Direct AGY Execution | Depends on Story 109.3 `.map.json` — sequential migration. |
| **Story 109.11** | `[AGY:PRIMARY]` | Direct AGY Execution | Prompt engineering + probe script — low blast radius. |
| **Story 109.12** | `[SWARM:CLOUD]` | `delegate.py --mode cloud` | Full-stack: frontend JS + backend router + 3 node adapters — maximum blast radius. |

---

## 6. Pre-Flight Verdict & Sign-Off

* **Verdict:** 🟡 **PRE-FLIGHT ADVERSARIAL AUDIT PASSED CONDITIONALLY (WITH 7 MITIGATIONS EMBEDDED + 3 DRIFT GAPS DOCUMENTED)**
* **Action Required:** 
  1. Commit this audit document to `Portfolio_Dev/docs/sprints/active/ORACLE_REVIEW_SPRINT_109.md`.
  2. Embed the 7 mitigations directly into the Story specifications of `SPRINT_PLAN_SPR_109_0.md`.
  3. Create the 7 missing implementation artifacts (ingest_focals.py, probe_companion_map.py, calculate_file_priorities(), context_envelope logic, curated_anchors extraction, projection_studio.js, FOCAL_DRAFT probe).
  4. Formally check off the Pre-Flight Digital Checkbox Gate (`BKM-082 §GATE`).

---

## 7. Escalation Triggers (Conditions Warranting Architecture Revision)

| Trigger | Condition | Escalation Path |
| :--- | :--- | :--- |
| **M5 Air MLX Unreachable** | `:8002` Headroom proxy fails health check for >5 min | Fallback to local heuristic slicer only; defer semantic labeling to AGY Judge. |
| **ChromaDB `focal_dna` Ingestion Fails** | `ingest_focals.py` cannot create collection or insert docs | Use `focal_ledger.json` as Tier 2 fallback; defer vector pre-triage wiring. |
| **Projection Studio Node Adapter Incompatibility** | vLLM/Ollama/MLX APIs diverge beyond adapter capacity | Reduce to 2-node comparison (vLLM + Ollama); defer MLX to Sprint 110. |
| **`disentangle_chronology()` Call Sites > 2** | Discovery reveals more call sites than `populate_queue_from_archive()` and `advance_gem_pass()` | Full grep audit before excision; may require phased deprecation. |

---

## 8. Alternative Sketch: Phased Execution (If Resources Constrained)

If full parallel execution is infeasible, execute in **4 Phases** with hard gates:

**Phase 1 (Foundation — Stories 109.1, 109.2, 109.4, 109.5):** File ops, date normalization, FEAT registration, focal ingestion. **Gate:** `focal_dna` collection exists with ≥5 records.

**Phase 2 (Memory Architecture — Stories 109.3, 109.6, 109.7, 109.8):** Companion maps, pre-triage wiring, context envelopes, queue scheduler. **Gate:** `calculate_file_priorities()` passes unit test; `context_envelope` test passes.

**Phase 3 (Ground Truth & Excision — Stories 109.9, 109.10, 109.11):** Ripgrep bridge, chronology excision, FOCAL_DRAFT tagging. **Gate:** `disentangle_chronology()` deleted; grep hydration test <8ms.

**Phase 4 (Projection Studio — Story 109.12):** Multi-node dispatch. **Gate:** Playwright test passes with 3 concurrent streams.

---

**Oracle Seal:** This review is grounded in empirical codebase inspection (cognitive_hub.py, vector_pre_triage.py, archive_node.py, scan_queue.py, refine_gem.py, scan_pinky.py, FeatureTracker.md, focal_ledger.json) and sprint archaeology (SPR-104 through SPR-108). All findings are traceable to specific line numbers and file paths. No speculative assertions.

**End of Adversarial Oracle Audit Report.**
