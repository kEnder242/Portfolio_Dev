# 📑 SPRINT PLAN 107.0: The Active Staging Synthesis & Bone Collection Retirement

**Sprint ID:** `SPR_107_0`  
**Theme:** Retirement of the Legacy ADR-008 "Bone Collection" Nomenclature, Transition to "+ Stage" & Active Kabal Staging Shelf, JITC Paper Bundle Migration (`papers/jitc_intuition/`), AST Reconciliation Re-Anchoring, and Full Public Airlock Deployment (`www_deploy`).  
**Status:** 🏁 **COMPLETE & CERTIFIED**  
**Parent Frameworks:**
- [`BKM-086`]: The Paved-Path Sprint Protocol (AFK / Sovereign Execution)
- [`BKM-043`]: Master 4-Anchor Prompt Standard (Surgical Line & Grep Anchors)
- [`BKM-062`]: Fail-Fast & Explicit Failure Propagation Mandate ("Green-Lie Prevention")
- [`BKM-070`]: The Re-Anchoring Law (Bones/Spine as Immutable AST Anchors)
- [`BKM-081`]: Pre-Flight Mistake Avoidance Ledger
- [`BKM-082`]: 5-Sprint Historical Lookback & Mistake Prevention
- [`BKM-085`]: Historical Pre-Regression Correlation Protocol
- [`FEAT-662`]: The Kabal: Emergent Ingestion Clusters & Manuscript Working Groups
- [`FEAT-663`]: Spine Version Tagging & Deterministic Snapshot Projections
- [`FEAT-664`]: Multi-Corpus Knowledge Ingestion in Applied Writer
- [`INS-048`]: The Bone Collection as the Skeletal Predecessor to the Kabal
- [`INS-049`]: Dam Building: The Law of Epistemic Hydraulics and Paved Flow

**Target Silicon Nodes:**
- `z87-Linux`: Local RTX 2080 Ti (Llama-3.2-3B-AWQ base on port 8088 / `cli_voice_v1` LoRA)
- `ChromaDB`: Port 8001 (`behavioral_dna`, `kabal_dna`, `inspiration_dna`, `philosophy_dna`)
- `lab-attendant.service`: Port 8765

---

## 🛡️ Pre-Flight Mistakes Avoided Ledger (`BKM-081` / `BKM-082`)

### 0.1 5-Sprint Historical Lookback Summary (`BKM-082 §2.1`)
- **SPR-102**: Decoupled Nightly Architecture & passive telemetry over synthetic benchmarking. *Historical Lesson:* Separate presentation shelves from raw background database schemas.
- **SPR-103**: Decouple-and-Stitch Architecture (`BKM-083`) & Multi-Stage Replay Pipeline (`FEAT-645`). *Historical Lesson:* Discrete stage isolation prevents cascading failures.
- **SPR-104**: Continuous Multiplier Token Pacing (`FEAT-523`) & Brain Information Gatekeeper. *Historical Lesson:* Fuel must exhaust naturally without artificial lower-bound token bloat.
- **SPR-105**: Decoupled Tri-Anchor Waterfall & Gem Intake Rollback (`FEAT-658`, `FEAT-659`, `INS-019`). *Historical Lesson:* Intake must remain a lossless net; never prune raw operational exhaust.
- **SPR-106**: Two-Dimensional Gem Epistemics (`refinement_level` L0–L3 vs `impact_level` Imp 1–4) & Polymorphic Kabal/Spine Architecture (`FEAT-662..664`, `INS-048`, `INS-049`). *Historical Lesson:* Decoupling substance (`_kabal.json`) from structural topology (`_spine.json`) eliminates destructive paragraph reorderings and premature static ID binding.

### 0.2 Pre-Flight Mistakes Avoided (`BKM-082 §2.4`)
1. **The Destructive Logic Deletion Trap**: Avoided deleting `HomeLabAI/src/projection/bones.py` simply because it had "bones" in the filename. Its `reconcile_diff` and AST normalization functions are pure mathematical algorithms essential for overlay comparison. We re-anchor it to `ast_reconciliation.py` while providing backward-compatibility shims.
2. **The LocalStorage Amnesia Trap**: Avoided breaking users' existing browser session staging by changing localStorage keys abruptly. The new staging code seamlessly migrates existing `dna_active_bone_rack` items into `dna_active_staging_shelf`.
3. **The Unanchored Orphan Bundle Trap**: When migrating `notes_jitc_bones.json` into `papers/jitc_intuition/`, we must generate both `jitc_kabal.json` and `jitc_spine.json` adhering strictly to `kabal_registry.py` invariants.
4. **Hardcoded Build Paths Trap**: Ensured all builders resolve templates relative to `Path(__file__).resolve().parent` to avoid path breakage during `build_site.py`.

---

## 🏛️ Executive Summary & Master Narrative

Sprint 107.0 completes the architectural evolution started in ADR-008 and formalized in FEAT-662:
1. **From "Bones" to "Kabal & Staging"**: We excise the archaic skeletal metaphor ("Bone Collection", "+ Rack", "Bone Rack") across all UI surfaces in favor of the active, actionable concept: **`+ Stage`** and the **`📑 Active Kabal Staging Shelf`**. Docking cards across domains is an intentional editorial act of assembling an emergent caucus before sending it to a manuscript or creating a named Kabal.
2. **Canonical Paper Bundling**: We migrate historical standalone files (`notes_jitc_bones.json` and `paper_jitc_intuition.json`) into the official atomic bundle structure under `Portfolio_Dev/papers/jitc_intuition/` (`jitc_kabal.json` + `jitc_spine.json`), officially retiring the `field_notes/data/bones/` directory.
3. **Core AST Re-Anchoring**: We re-anchor `HomeLabAI/src/projection/bones.py` to `ast_reconciliation.py`, preserving pure document normalization, spine snapshot management, and diff reconciliation without naming pollution.
4. **Site & Deployment Synchronization**: We compile all updated HTML views and deploy the sanitized state to the public airlock (`www_deploy`).

---

## 🚦 AFK Execution Checklist & Stories (`BKM-086`)

### Phase 1: External UI Refactoring (DNA Forge & Applied Writer)
- [ ] **Story 107.1**: Card Button Renaming (`+ Rack` $\to$ `+ Stage`) across `dna_forge_build.py`, templates, and CSS.
- [ ] **Story 107.2**: Rebrand Top Shelf in `dna_forge.html` to `📑 ACTIVE KABAL STAGING` with `dna_active_staging_shelf` migration and "Send to Writer" / "Export Kabal" actions.
- [ ] **Story 107.3**: Tab 1 Drafting & Decomposition terminology alignment (`Decompose into Kabal Cards & Spine`).
- [ ] **Story 107.4**: Applied Writer (`writer.html`) canvas cleanup (retire vestigial `.bone-*` classes, prioritize multi-corpus citation chips).

### Phase 2: Internal Data & Paper Migration
- [ ] **Story 107.5**: Migrate `notes_jitc_bones.json` and `paper_jitc_intuition.json` into canonical bundle: `Portfolio_Dev/papers/jitc_intuition/`.
- [ ] **Story 107.6**: Archive legacy `field_notes/data/bones/` to `field_notes/data/archive/bones/` and deprecate `bone_collections.json`.
- [ ] **Story 107.7**: Re-anchor `HomeLabAI/src/projection/bones.py` to `ast_reconciliation.py` with backwards-compatibility aliases, and retire obsolete `refine_bones.py`.

### Phase 3: Silicon Gauntlet, Compilation & Deployment
- [ ] **Story 107.8**: Recompile `dna_forge_build.py` and run `build_site.py --no-verify` to deploy to `www_deploy`.
- [ ] **Story 107.9**: Execute complete test suite (HomeLabAI + Portfolio_Dev 24/24), hot-reload live daemons, verify live `:8765` health.
- [ ] **Story 107.10**: Update `FeatureTracker.md`, register `SPR-107.0` in `sprint_data.json`, and certify sprint completion.

---

## 📋 Story Specifications (`BKM-043` 4-Anchor Standard)

#### 📊 Story 107.1: DNA Card Button Renaming (`+ Rack` $\to$ `+ Stage`)
* **Objective**: Rename the primary docking button on all DNA cards in DNA Forge from `+ Rack` to `+ Stage`, updating titles and CSS affordances.
* **Target Files**:
  - `Portfolio_Dev/dna_forge/dna_forge_build.py`
  - `Portfolio_Dev/field_notes/dna_forge_build.py`
  - `Portfolio_Dev/dna_forge/css/dna_forge.css`
  - `Portfolio_Dev/dna_forge/js/dna_forge.js`
* **4-Anchor Specification**:
  - **Anchor 1**: `dna_forge_build.py` line 397: replace `<button class="btn-card-rack"...>+ Rack</button>` with `<button class="btn-card-stage" data-cid="{escape_html(cid)}" title="Stage into Active Working Kabal">+ Stage</button>`.
  - **Anchor 2**: In `dna_forge.js`, bind click listener to `.btn-card-stage` (with fallback to `.btn-card-rack`).
  - **Anchor 3**: CSS rule `.btn-card-stage` with modern cyan border `#38bdf8` and subtle background tint.
  - **Anchor 4**: Verification via `python3 dna_forge_build.py`.

#### 📊 Story 107.2: Active Kabal Staging Shelf & Actions
* **Objective**: Upgrade the floating top shelf in `dna_forge.html` from `🦴 BONE COLLECTION BUILDER` to `📑 ACTIVE KABAL STAGING`. Migrate localStorage key from `dna_active_bone_rack` to `dna_active_staging_shelf`. Add direct "✍️ Open in Writer" action.
* **Target Files**:
  - `Portfolio_Dev/dna_forge/templates/dna_forge.html`
  - `Portfolio_Dev/dna_forge/js/dna_forge.js`
  - `Portfolio_Dev/dna_forge/css/dna_forge.css`
* **4-Anchor Specification**:
  - **Anchor 1**: `dna_forge.html` lines 196–212: update badge to `📑 ACTIVE KABAL STAGING`, input placeholder to `Kabal Working Title...`.
  - **Anchor 2**: In `dna_forge.js`, add migration `localStorage.getItem('dna_active_staging_shelf') || localStorage.getItem('dna_active_bone_rack')`.
  - **Anchor 3**: Add button `#btnStageToWriter`: opens `writer.html?staging=true` or attaches staged card IDs.
  - **Anchor 4**: Verification via browser DOM inspection and build script.

#### 📊 Story 107.3: Tab 1 Drafting Terminology Alignment
* **Objective**: Refactor Tab 1 Drafting copy and DOM IDs to refer to Kabal Cards and Spines rather than bones.
* **Target Files**:
  - `Portfolio_Dev/dna_forge/templates/dna_forge.html`
  - `Portfolio_Dev/dna_forge/js/dna_forge.js`
* **4-Anchor Specification**:
  - **Anchor 1**: Update button text to `⚡ Decompose into Kabal Cards & Spine`.
  - **Anchor 2**: Update section title to `📑 Suggested Kabal Track Scaffold`.
  - **Anchor 3**: In `dna_forge.js`, update promotion notification to reflect Kabal registration.
  - **Anchor 4**: Verification via `dna_forge_build.py`.

#### 📊 Story 107.4: Applied Writer Canvas & CSS Cleanup
* **Objective**: Deprecate vestigial `.bone-*` classes in `writer.html` and clean up demo AST structures to emphasize multi-corpus citation chips.
* **Target Files**:
  - `Portfolio_Dev/field_notes/writer.html`
  - `Portfolio_Dev/field_notes/js/writer.js`
* **4-Anchor Specification**:
  - **Anchor 1**: In `writer.html`, alias `.tier-bones-container` to `.tier-staging-container` and `.bone-collection-badge` to `.citation-cluster-badge`.
  - **Anchor 2**: Verify multi-corpus search drawer chips seamlessly attach citation anchors (`[RESUME.EXP-042]`, `[WIS-xxx]`).
  - **Anchor 3**: Ensure zero rendering regressions on existing paper view.
  - **Anchor 4**: Verification via syntax check and browser inspection.

#### 📊 Story 107.5: JITC Legacy Bone Migration to Canonical Kabal Bundle
* **Objective**: Convert `Portfolio_Dev/field_notes/data/bones/notes_jitc_bones.json` and `paper_jitc_intuition.json` into canonical atomic bundle: `Portfolio_Dev/papers/jitc_intuition/jitc_kabal.json` and `jitc_spine.json`.
* **Target Files**:
  - `Portfolio_Dev/papers/jitc_intuition/jitc_kabal.json`
  - `Portfolio_Dev/papers/jitc_intuition/jitc_spine.json`
  - `Portfolio_Dev/papers/manifest.json`
* **4-Anchor Specification**:
  - **Anchor 1**: Run `decompose_document_to_kabal.py` or bespoke conversion script to emit valid Kabal cards with prefix `JITC`.
  - **Anchor 2**: Generate `jitc_spine.json` with `@master` snapshot tag and section ordering.
  - **Anchor 3**: Update `papers/manifest.json` pointing to `papers/jitc_intuition/`.
  - **Anchor 4**: Verify replay with `python3 field_notes/replay_paper.py --slug=jitc_intuition --tag=@master`.

#### 📊 Story 107.6: Internal Legacy Bone Archival
* **Objective**: Move `field_notes/data/bones/` to `field_notes/data/archive/bones/` and mark `bone_collections.json` as legacy reference.
* **Target Files**:
  - `Portfolio_Dev/field_notes/data/archive/bones/`
  - `Portfolio_Dev/field_notes/data/bone_collections.json`
* **4-Anchor Specification**:
  - **Anchor 1**: `mkdir -p Portfolio_Dev/field_notes/data/archive/bones/` and move legacy files.
  - **Anchor 2**: Add `"status": "ARCHIVED_SUPERSEDED_BY_KABAL"` in `bone_collections.json`.
  - **Anchor 3**: Ensure build scripts gracefully handle absence of unarchived `bones/` folder.
  - **Anchor 4**: Verify `dna_forge_build.py` runs without error.

#### 📊 Story 107.7: Projection Engine Re-Anchoring
* **Objective**: Re-anchor `HomeLabAI/src/projection/bones.py` to `HomeLabAI/src/projection/ast_reconciliation.py`, preserving `reconcile_diff`, `DocumentAST`, `normalize_ast`, and `SpineManager`. Leave `bones.py` as an alias redirect for backwards-compatibility.
* **Target Files**:
  - `HomeLabAI/src/projection/ast_reconciliation.py`
  - `HomeLabAI/src/projection/bones.py`
  - `HomeLabAI/src/forge/refine_bones.py`
* **4-Anchor Specification**:
  - **Anchor 1**: Copy `bones.py` $\to$ `ast_reconciliation.py`.
  - **Anchor 2**: In `bones.py`, import all symbols from `ast_reconciliation` with deprecation note.
  - **Anchor 3**: Mark `refine_bones.py` as deprecated.
  - **Anchor 4**: Verify unit tests in HomeLabAI pass cleanly.

#### 📊 Story 107.8: DNA Forge Compilation & Full Site Deployment
* **Objective**: Recompile all dynamic pages with `dna_forge_build.py` and run `build_site.py --no-verify` to deploy to `www_deploy`.
* **Target Files**:
  - `Portfolio_Dev/field_notes/build_site.py`
  - `Dev_Lab/www_deploy/`
* **4-Anchor Specification**:
  - **Anchor 1**: Run `python3 dna_forge_build.py`.
  - **Anchor 2**: Run `python3 build_site.py --no-verify`.
  - **Anchor 3**: Verify git status of `www_deploy`.
  - **Anchor 4**: Clean commit in `Portfolio_Dev` and `www_deploy`.

#### 📊 Story 107.9: Silicon Gauntlet & Live Daemon Validation
* **Objective**: Run unit test suites (HomeLabAI + Portfolio_Dev 24/24), verify live daemon health on port 8765, and ensure zero regression.
* **Target Files**:
  - `Portfolio_Dev/field_notes/tests/`
  - `HomeLabAI/src/tests/`
* **4-Anchor Specification**:
  - **Anchor 1**: `pytest field_notes/tests/`.
  - **Anchor 2**: `pytest src/tests/test_accountability_matrix_unit.py`.
  - **Anchor 3**: Query `curl -s "http://127.0.0.1:8765/status?timeout=5"`.
  - **Anchor 4**: Confirm physical endpoint response is nominal.

#### 📊 Story 107.10: Sprint Certification & Registration
* **Objective**: Register `SPR-107.0` in `sprint_data.json`, update `FeatureTracker.md`, and stamp sprint plan complete.
* **Target Files**:
  - `Portfolio_Dev/field_notes/data/sprint_data.json`
  - `Portfolio_Dev/FeatureTracker.md`
  - `Portfolio_Dev/docs/sprints/active/SPRINT_PLAN_SPR_107_0.md`
* **4-Anchor Specification**:
  - **Anchor 1**: Add `SPR-107.0` entry to `sprint_data.json`.
  - **Anchor 2**: Update `FeatureTracker.md` with FEAT-665 ("Active Kabal Staging & Bone Retirement").
  - **Anchor 3**: Mark all checklist items in `SPRINT_PLAN_SPR_107_0.md` complete.
  - **Anchor 4**: Final Git commit.

---

## 🏁 Story Completion & Certification Matrix

- [x] **Story 107.1: DNA Forge Card Staging Refactor (`+ Stage`)**: Fully refactored `.btn-card-stage`, cyan `#38bdf8` active styling, badge counting.
- [x] **Story 107.2: Floating Active Kabal Staging Shelf**: `📑 ACTIVE KABAL STAGING` floating shelf (`#btnStageToWriter`) with `dna_active_staging_shelf` persistence and `writer.html?staged=ID1,ID2` handoff.
- [x] **Story 107.3: DNA Forge Tab 1 Drafting Decomposer Alignment**: Clean terminology alignment to `⚡ Decompose into Kabal Cards & Spine`.
- [x] **Story 107.4: Applied Writer Review Drawer Staging Integration**: URL parameter `?staged=...` ingestion, CSS aliasing `.tier-staging-container` and `.citation-cluster-badge`.
- [x] **Story 107.5: JITC Legacy Bone Migration to Canonical Kabal Bundle**: Created `papers/jitc_intuition/jitc_intuition_kabal.json` (20 cards) and `jitc_intuition_spine.json` (tags `@master` and `@with_bones`). 100% verified via `replay_paper.py`.
- [x] **Story 107.6: Internal Legacy Bone Archival**: Archived `field_notes/data/bones/` to `field_notes/data/archive/bones/`, deprecated `bone_collections.json` (`ARCHIVED_SUPERSEDED_BY_KABAL`), updated compiler fallbacks.
- [x] **Story 107.7: Projection Engine Re-Anchoring**: Re-anchored to `HomeLabAI/src/projection/ast_reconciliation.py`. Replaced `bones.py` with backward-compatible alias deprecation module. All 216 unit tests passing.
- [x] **Story 107.8: DNA Forge Compilation & Full Site Deployment**: Compiled via `dna_forge_build.py` and deployed to `www_deploy` via `build_site.py --no-verify`.
- [x] **Story 107.9: Silicon Gauntlet & Live Daemon Validation**: All 24 unit tests in `Portfolio_Dev/field_notes/tests/` passed. `test_accountability_matrix_unit.py` passed. Lab Attendant daemon (port 8765) verified OPERATIONAL.
- [x] **Story 107.10: Sprint Certification & Registration**: Registered `SPR-107.0` in `sprint_data.json` and `FEAT-665` in `FeatureTracker.md`.

---

# 🚀 SPRINT 107.0 (PHASE 2): Live Silicon Grounding & Self-Dialogue Circuit Breaker

**Phase Theme:** Direct Real-Time Hardware Grounding (`FEAT-557`), Self-Dialogue Sanitizer Circuit Breaker (`FEAT-558`), and Triage Feedback Snapping (`FEAT-559`).  
**Status:** 📋 **PLANNED / READY FOR REVIEW**  
**Parent Frameworks:**
- [`BKM-081` §4]: The Sprint Append Ledger Protocol (Phased Sprint Architecture Invariant)
- [`BKM-086`]: The Paved-Path Sprint Protocol (AFK / Sovereign Execution)
- [`FEAT-557`]: Live Host Telemetry Node & Real-Time Hardware Grounding
- [`FEAT-558`]: Self-Dialogue Sanitizer Circuit Breaker
- [`FEAT-559`]: Triage Feedback Domain Snapping & Prompt Interception

### 🏛️ Phase 2 Executive Summary & Narrative
Phase 2 builds directly upon Sprint 107.0's epistemic staging stability to resolve two runtime cognitive issues identified in `copilot_mice_feedback_forensics_report.md`:
1. **Physical Grounding over Historical Memory (`FEAT-557`)**: The lab frequently answers inquiries about live memory, GPU temperature, or hardware headroom using outdated documentation retrieved via RAG. We wire `live_telemetry.get_host_vitals()` directly into `CognitiveHub`, snapping telemetry inquiries to live silicon metrics.
2. **Auto-Regressive Health & Circuit Breaking (`FEAT-558`)**: Multi-turn conversations degrade when model reasoning artifacts (`<thought>` tags, internal prompts) leak into conversation history buffers. We establish a strict multi-turn sanitizer circuit breaker that strips internal monologues from prior turns before context construction.
3. **Feedback Intent Snapping (`FEAT-559`)**: User corrective turns (*"stop hallucinating"*, *"feedback: you missed the point"*) snap immediately to `domain: feedback` / `vibe: CRITIQUE`, suppressing standard RAG in favor of direct corrective reflection.

### 🎯 Phase 2 Stories & 4-Anchor Specifications

#### 📊 Story 107.11: Live Host Telemetry Tool & Context Injection (`FEAT-557`)
* **Objective**: Connect `live_telemetry.get_host_vitals()` into `CognitiveHub` so live hardware questions receive deterministic physical metrics (GPU VRAM, RAM, CPU load, active model).
* **Target Files**:
  - `HomeLabAI/src/logic/cognitive_hub.py`
  - `HomeLabAI/src/infra/live_telemetry.py`
* **4-Anchor Specification**:
  - **Anchor 1**: `live_telemetry.py`: Ensure `get_host_vitals()` returns structured dictionary with sub-5ms latency and graceful non-NVIDIA fallback.
  - **Anchor 2**: `cognitive_hub.py`: Introduce `inject_live_telemetry_context(domain, query)` during waterfall context construction.
  - **Anchor 3**: Suppress historical hardware spec RAG injection when live hardware intent is detected.
  - **Anchor 4**: Verification via unit tests asserting physical memory values in prompt context.

#### 📊 Story 107.12: Hardware Intent Routing in Semantic Triage (`FEAT-557`)
* **Objective**: Ensure queries asking about current VRAM, RAM, GPU, or model state classify into `domain: infra` / `intent: live_telemetry` without falling through to generic tech RAG.
* **Target Files**:
  - `HomeLabAI/src/logic/triage_engine.py`
  - `HomeLabAI/src/logic/traversal_dispatcher.py`
* **4-Anchor Specification**:
  - **Anchor 1**: In `triage_engine.py`, add live telemetry trigger patterns ("how much vram", "current memory", "hardware status", "silicon vitals").
  - **Anchor 2**: Set high confidence routing to `domain: infra` with metadata flag `is_live_telemetry: True`.
  - **Anchor 3**: Verify fast-path routing bypasses heavy vector search.
  - **Anchor 4**: Unit tests in `test_fast_triage_harness.py`.

#### 📊 Story 107.13: Multi-Turn Conversation History Sanitizer Circuit Breaker (`FEAT-558`)
* **Objective**: Enforce multi-turn history sanitization in `CognitiveHub` before prompt compilation, excising prior `<thought>` blocks, internal tags, and self-speaker prefixes.
* **Target Files**:
  - `HomeLabAI/src/logic/cognitive_hub.py`
  - `HomeLabAI/src/nodes/loader.py`
* **4-Anchor Specification**:
  - **Anchor 1**: In `cognitive_hub.py`, pipe all prior assistant turns in `recent_history` through `sanitize_spoken_dialogue()`.
  - **Anchor 2**: Strip multiline `<thought>.*?</thought>` and `<role>.*?</role>` artifacts.
  - **Anchor 3**: Remove redundant leading speaker prefixes (e.g. `Brain: Brain:`, `Pinky:`) from multi-turn accumulation.
  - **Anchor 4**: Unit tests asserting clean multi-turn prompt generation with zero thought leakage.

#### 📊 Story 107.14: Triage Feedback Domain Snapping (`FEAT-559`)
* **Objective**: Automatically classify explicit user critique and feedback phrases into `domain: feedback` / `vibe: CRITIQUE` with priority prompt steering.
* **Target Files**:
  - `HomeLabAI/src/logic/triage_engine.py`
  - `HomeLabAI/src/logic/cognitive_hub.py`
* **4-Anchor Specification**:
  - **Anchor 1**: In `triage_engine.py`, map critique keywords (*"stop hallucinating"*, *"you missed"*, *"incorrect"*, *"feedback"*) to `vibe: CRITIQUE`.
  - **Anchor 2**: In `cognitive_hub.py`, apply corrective framing when `vibe == "CRITIQUE"`.
  - **Anchor 3**: Suppress repetitive previous verbiage and inject self-correction prompt constraints.
  - **Anchor 4**: Verification via `test_feedback_semantic_triage.py`.

#### 📊 Story 107.15: Anti-Self-Echo & Live Silicon Gauntlet Validation
* **Objective**: Run full unit test gauntlets across `HomeLabAI` and `Portfolio_Dev`, perform live query validation against the attendant daemon, and certify zero regression.
* **Target Files**:
  - `HomeLabAI/src/tests/test_feedback_semantic_triage.py`
  - `HomeLabAI/src/tests/test_integrated_fast.py`
  - `Portfolio_Dev/field_notes/tests/`
* **4-Anchor Specification**:
  - **Anchor 1**: All 9 tests in `test_feedback_semantic_triage.py` passing.
  - **Anchor 2**: `pytest field_notes/tests/` passing (24/24).
  - **Anchor 3**: Live query probe: `curl` query verifying live VRAM returns actual hardware value.
  - **Anchor 4**: Commit and update documentation.

#### 📊 Story 107.16: Triage vs. Pinky Actual LLM Stopwatch Decoupling (Item 0)
* **Objective**: Distinctly measure Pinky's actual local LLM generation duration ($\sim 3\text{s}$) rather than conflating it with the $0.03\text{s}$ event-loop reflex or aliasing it to triage elapsed time in `blackboard_ledger.py`, while strictly preserving the `"Initiating..."` handshake prints.
* **Target Files**:
  - `HomeLabAI/src/logic/cognitive_hub.py`
  - `HomeLabAI/src/infra/blackboard_ledger.py`
* **4-Anchor Specification**:
  - **Anchor 1**: Strictly preserve all `"Initiating {source_name} intuition..."` broadcast prints across `_process_node_stream()`, maintaining unbroken handshake telemetry.
  - **Anchor 2**: In `resolve_hyde_vector()` and `step_pinky_voice()`, wrap physical generation with a dedicated high-resolution stopwatch (`time.perf_counter()`), recording the genuine LLM token inference duration ($t_{\text{pinky\_llm}}$).
  - **Anchor 3**: In `cognitive_hub.py#L1808-L1815`, record distinct elapsed times in `blackboard_ledger.py` ($t_{\text{triage}} \ne t_{\text{pinky}}$) so the ledger reflects true physical silicon reality.
  - **Anchor 4**: Unit tests in `test_two_mice_handover.py` and `test_fast_triage_harness.py` asserting non-identical, positive delta timings.

#### 📊 Story 107.17: Zero-Streaming UI Restoration, Paragraph Pop Primacy & Persona Theming (Item 1)
* **Objective**: Re-affirm the Sprint 32 "Clinical Paragraph Pop" mandate and eliminate the Sprint 103 streaming regression. Simple implementation: completely silence `thought_stream` WebSocket chatter to the intercom, letting `router.py:waterfall_drainer` be the single authority delivering complete, popped thoughts with canonical headers, colors, and physical truth.
* **Target Files**:
  - `HomeLabAI/src/logic/cognitive_hub.py`
  - `HomeLabAI/src/v5/foyer/router.py`
  - `Portfolio_Dev/field_notes/intercom_v2.js`
  - `Portfolio_Dev/field_notes/intercom.html`
* **4-Anchor Specification**:
  - **Anchor 1 (Zero Streaming to Intercom)**: Silence `thought_stream` packet emission to the Web Intercom, ending mid-stream token flicker and dual-stream duplication. Internal pipeline nodes stream for execution speed, but UI delivery relies 100% on the single Waterfall Drainer Pop.
  - **Anchor 2 (Single Waterfall Pop Authority)**: In `router.py` (`_waterfall_consumer`), broadcast exactly one finalized `type: "chat"` frame upon `final: True`, mapping sources to user-preferred display names (`[Pinky (Voice)]` and `[Brain (Archive)]`) and logging sovereign telemetry (`[FEAT-498]`).
  - **Anchor 3 (Canonical Styling & Physical Truth)**: In `intercom_v2.js` and `intercom.html`, fix CSS token class matching so `[Pinky (Voice)]` maps to `.msg-source.pinky` (cyan `#58a6ff`) and `[Brain (Archive)]` maps to `.msg-source.brain` (red `#f85149`), appending live `[SID: ...] [PID: ...]`.
  - **Anchor 4 (Anti-Regex Formatting Mandate)**: Preserve intentional newlines and list spacing in `sanitize_spoken_dialogue()`. Inject system prompt guidance (`[FORMATTING]: Use clean markdown with single newlines between bullet items.`) rather than fighting the LLM with regex.

#### 📊 Story 107.18: Additive Waterfall HyDE & Triage First-Class Data Type (Item 2)
* **Objective**: Refactor pre-RAG HyDE prompt synthesis to use additive waterfall composition instead of branching `if/elif/else` ladders, trusting the structured `triage` dict directly as a first-class data type.
* **Target Files**:
  - `HomeLabAI/src/logic/cognitive_hub.py`
  - `Portfolio_Dev/field_notes/intercom_v2.js`
* **4-Anchor Specification**:
  - **Anchor 1 (Additive HyDE Waterfall)**: Base HyDE synthesis (`search_terms`, `upvote`, `spoken_take`) always runs. If `triage.get("addressed_to") == "BRAIN"`, additively append the overhearing directive. If `triage.get("domain")` indicates historical/career records, additively append era indexing guidance.
  - **Anchor 2 (Direct Triage Consumption)**: Excise synthetic boolean wrappers (e.g. `is_historical`). Check `triage["domain"]` and `triage["vibe"]` directly, enabling RAG search across all topics (infra, telemetry, non-gem DNA).
  - **Anchor 3 (Right Console RAG Drawer)**: In `intercom_v2.js`, route `type: "rag_eval"` frames to `insightConsole` (`channel='insight'`) with full `<details class="rag-eval-card">` interactive `+`/`-` drawer above Brain's evidentiary grounding.
  - **Anchor 4**: Unit tests in `test_rag_cache.py`, `test_two_mice_handover.py`, and `test_feedback_semantic_triage.py` passing cleanly.

#### 📊 Story 107.19: Brain Gatekeeper Scope & Negative Constraint Filter (Item 3)
* **Objective**: Invert the Brain-Pinky hierarchy in Stage 1 so Brain acts as a sovereign Gatekeeper and Exclusion Filter on Pinky's output and candidate records, actively pruning negative constraints (e.g., "not IPMI or PECI") without regex tampering.
* **Target Files**:
  - `HomeLabAI/src/logic/cognitive_hub.py`
  - `HomeLabAI/src/tests/test_two_mice_handover.py`
* **4-Anchor Specification**:
  - **Anchor 1**: In `build_two_mice_stage_prompt(stage=1)`, inject the canonical `[GATEKEEPER SCOPE & EXCLUSION FILTER]` directive into Brain's instructions.
  - **Anchor 2**: Explicitly instruct Brain to treat Pinky's stance as an unvetted associative hunch, using Jason's primer as a selective sieve to filter noise and discard candidate chunks touching excluded terms.
  - **Anchor 3**: Strictly forbid Brain from validating, conversing with, or parroting excluded topics, focusing exclusively on the surviving technical core.
  - **Anchor 4**: Unit tests in `test_two_mice_handover.py` asserting Brain's prompt embeds the exclusion filter specification.

---

### 🏁 Phase 2 Verification Checklist

- [x] Story 107.11: Live Host Telemetry Tool & Context Injection (`FEAT-557`)
- [x] Story 107.12: Hardware Intent Routing in Semantic Triage (`FEAT-557`)
- [x] Story 107.13: Multi-Turn Conversation History Sanitizer Circuit Breaker (`FEAT-558`)
- [x] Story 107.14: Triage Feedback Domain Snapping (`FEAT-559`)
- [x] Story 107.15: Anti-Self-Echo & Live Silicon Gauntlet Validation
- [x] Story 107.16: Triage vs. Pinky Actual LLM Stopwatch Decoupling (Item 0)
- [x] Story 107.17: Zero-Streaming UI Restoration, Paragraph Pop Primacy & Persona Theming (Item 1)
- [x] Story 107.18: Additive Waterfall HyDE & Triage First-Class Data Type (Item 2)
- [x] Story 107.19: Brain Gatekeeper Scope & Negative Constraint Filter (Item 3)

---

## 📜 Sprint Log: In-Flight Execution Narrative & Epistemic Alignment Ledger (`[BKM-081]`)

### 🛠️ Execution Trace: Sidebar Shortcut Navigation Alignment (Oct 19, 2026)

#### 1. Action Summary
* **User Directive**: Quick pivot to rename the `https://notes.jason-lab.dev/benchmarks.html` shortcut to **"Model Telemetry"** in the Mission Control sidebar, identify corresponding DNA alignment adjustments, and log the execution narrative into the active sprint plan.
* **Target Files Modified**:
  - `Portfolio_Dev/field_notes/mission-control.js` (line 35): Renamed anchor text from `Model Benchmarks` to `Model Telemetry`.
  - `www_deploy/mission-control.js` (line 35): Synchronized deployed airlock component with canonical source.
  - `Portfolio_Dev/FeatureTracker.md` (`[FEAT-494]`): Upgraded title to `[FEAT-494] [CONSOLIDATED] benchmarks.html 3-Tab Federated Silicon Workbench (Model Telemetry)` and documented navigation alignment.

#### 2. DNA Consistency & Architectural Rationale
* **The Epistemic Shift from Synthetic Benchmarks to Continuous Telemetry**:
  - The historical nomenclature *"Model Benchmarks"* was a legacy artifact from Sprints 35–43 when synthetic nightly probe sweeps (`FEAT-495`) actively burned tokens to measure static throughput.
  - In Sprint 102 (`Story 102.20`), synthetic sweeps were decoupled and retired (`FEAT-495`) in favor of continuous passive execution telemetry harvested from authentic production multi-seat workloads (`FEAT-496`).
  - The underlying workbench `benchmarks.html` operates 100% on empirical live telemetry: Tab 1 (`FEAT-525` live deliberation elapsed time / blackboard ledger), Tab 2 (`FEAT-496` real-time task generation throughput waterfall), and Tab 3 (`FEAT-552` authentic sovereign token ledger and realized dollar savings).
  - Renaming the navigation entry point from **"Model Benchmarks"** to **"Model Telemetry"** accurately describes the surface to human operators and autonomous agents alike, eliminating cognitive drift.
* **Relevant DNA Cards Identified & Adjusted**:
  - `[FEAT-494]`: Updated title and logic to designate `Model Telemetry` as the official sidebar entry point for `benchmarks.html`.
  - `[FEAT-496]` (*Passive Real-Time Swarm Telemetry Stream*): Primary operational anchor for `benchmarks.html`; taxonomy is now 100% congruent.
  - `[FEAT-495]` (*Dynamic Auto-Discovery Benchmark Engine & Service De-escalation*): Retired card providing the historical rationale for deprecating synthetic "benchmarks" in favor of passive "telemetry".
  - `[FEAT-557]` (*Live Host Telemetry Node & Real-Time Hardware Grounding*): Sprint 107.0 Phase 2 feature bridging live backend physical host telemetry (`live_telemetry.py`) with frontend telemetry representations.

#### 3. Verification & Silicon Health
* `pytest Portfolio_Dev/field_notes/tests/`: 24/24 unit tests passed (0.71s).
* Verified component rendering logic across both `Portfolio_Dev/field_notes/mission-control.js` and `www_deploy/mission-control.js`.

### 🛠️ Execution Trace: Phase 2 Sovereign Deliberation & UI Restoration (Oct 19, 2026)

#### 1. Stories Executed & Certified
* **Story 107.16: Triage vs. Pinky Actual LLM Stopwatch Decoupling (Item 0)**:
  - Preserved unbroken `"Initiating..."` handshake telemetry.
  - Wrapped Pinky's physical LLM generation in `resolve_hyde_vector` with a high-resolution stopwatch (`time.perf_counter()`).
  - Decoupled `t_pinky_elapsed` from `t_triage_elapsed` ($t_{\text{pinky\_elapsed}} = t_{\text{triage}} + d_{\text{hyde}}$), resolving the identical timestamp bug in `round_table_deltas.json`.
* **Story 107.17: Zero-Streaming UI Restoration, Paragraph Pop Primacy & Persona Theming (Item 1)**:
  - Re-affirmed Sprint 32 "Clinical Paragraph Pop" mandate: silenced mid-stream token broadcasting over WebSockets. Internal pipeline nodes stream for execution speed; the UI receives finalized, complete thoughts.
  - Silenced duplicate monolithic broadcasts in `router.py:_waterfall_consumer` for handover personas, while preserving `log_telemetry_event()` for sovereign accounting (`[FEAT-498]`).
  - Fixed CSS token matching in `intercom_v2.js` and `intercom.html`: removed `text-transform: uppercase`, mapped base class to `.pinky` (cyan `#58a6ff`) and `.brain` (red `#f85149`), preserving Title Case (`[Pinky (Voice)]` and `[Brain (Archive)]`) alongside physical truth signatures (`[SID: ...] [PID: ...]`).
  - Excised destructive `re.sub(r"\s+", " ", ...)` whitespace collapsing in `sanitize_spoken_dialogue()`, preserving markdown formatting and intentional newlines.
* **Story 107.18: Additive Waterfall HyDE & Triage First-Class Data Type (Item 2)**:
  - Replaced branching `if/elif/else` ladders with additive waterfall prompt composition: Base HyDE synthesis (`search_terms`, `upvote`, `spoken_take`) always runs. If `addressed_to == "BRAIN"`, additively append the overhearing directive; if historical/career, additively append era indexing guidance.
  - Consumed `triage` directly as a first-class structured dictionary, eliminating lossy `is_historical` boolean wrappers and unlocking multi-corpus RAG.
  - Routed expandable `rag_eval` drawers directly to `insightConsole` (Right Console) above Brain's evidentiary grounding.
* **Story 107.19: Brain Gatekeeper Scope & Negative Constraint Filter (Item 3)**:
  - Inverted the Brain-Pinky hierarchy: injected `[GATEKEEPER SCOPE & EXCLUSION FILTER]` into Brain's Stage 1 prompt in `build_two_mice_stage_prompt`.
  - Directed Brain to treat Pinky's stance as an unvetted associative hunch, using Jason's primer as a selective sieve to filter noise, reject baited tangents (e.g. "not IPMI or PECI"), and strictly refrain from validating or parroting excluded topics.
  - Upheld `BKM-015`: Zero regex tampering in pre-retrieval; Brain exercises sovereign gatekeeper authority natively.

#### 2. Physical Silicon Health & Gauntlet Certification
* **Unit Test Gauntlet**:
  - `pytest Portfolio_Dev/field_notes/tests/`: 24/24 PASSED (0.71s).
  - `pytest HomeLabAI/src/tests/test_two_mice_handover.py`: 17/17 PASSED.
  - `pytest HomeLabAI/src/tests/test_feedback_semantic_triage.py`: 9/9 PASSED.
  - `pytest HomeLabAI/src/tests/test_censorship_memory_tri_node.py`: 4/4 PASSED.
  - Total: 54/54 automated tests green.
* **Daemon Hot-Reload**:
  - `POST http://127.0.0.1:8765/reload_residents`: `{"status": "success", "message": "Resident nodes hot-reloaded successfully. vLLM VRAM preserved."}`
* **Public Airlock Deployment**:
  - Synchronized `intercom_v2.js` and `intercom.html` to `Dev_Lab/www_deploy/`.

---

## 🔬 Phase 3: Empirical Telemetry Grounding & Synthetic Benchmark Regression Audit (`BKM-085` / `FEAT-496` / `FEAT-498`)

### 1. Architectural & Historical Problem Statement
During a live review of the **Model Telemetry** surface (`benchmarks.html`), the operator observed that **Throughput is always flatlined at exactly 35.0 tok/s**.

A focused historical regression analysis adhering to `BKM-085` traced this anomaly back to **Commit `cbce247` (August 31, 2026 - Sprint 66.5 / FEAT-498)**:
* When wiring the Intercom sovereign token tap in `HomeLabAI/src/v5/foyer/router.py`, a placeholder estimation was introduced:
  ```python
  toks = max(1, int(len(content) / 3.8))
  duration_seconds = max(1.0, toks / 35.0)  # Synthetic duration forced to 35 tps
  raw_throughput_tok_s = 35.0               # Hardcoded 35.0 tok/s mock!
  ```
* Because `duration_seconds` was derived as `toks / 35.0` and `raw_throughput_tok_s` was hardcoded to `35.0`, `log_telemetry_event()` logged `throughput_tok_s: 35.0` and `workflow_velocity_tok_s: 35.0` on every single Mice turn (Pinky, Brain, Deep Thought, Lab) into `live_usage_stream.jsonl`.
* Meanwhile, the true physical telemetry engine in `src/nodes/loader.py:880-900` was already measuring ground-truth `token_count`, `duration_s = time.time() - t0`, and `ttft_ms` and posting to `router.py:handle_telemetry_ingest`, but that handler only updated internal DCGM structures without updating `log_telemetry_event()`.

### 2. Stories Executed & Certified

#### 📊 Story 107.20: Empirical Model Throughput Telemetry Grounding (`FEAT-496` / `FEAT-498`) &mdash; [COMPLETED & CERTIFIED]
* **Implementation Details**:
  1. In `HomeLabAI/src/v5/foyer/router.py:handle_telemetry_ingest`:
     - Rewired handler to capture physical generation telemetry emitted by `src/nodes/loader.py`: `total_tokens`, `duration_s`, and `ttft_ms`.
     - Calculated real observed speed: `raw_tp = round(total_tokens / duration_s, 2)`.
     - Mapped emitting node name dynamically to physical seat (`Windows 4090RTX`, `Linux 2080ti`, `Apple M5 Air`).
     - Invoked `log_telemetry_event()` directly with ground-truth parameters.
  2. In `HomeLabAI/src/v5/foyer/router.py:waterfall_drainer`:
     - Completely excised lines 4870-4895 containing the synthetic `toks / 35.0` duration and `raw_throughput_tok_s = 35.0` mock tap.
  3. Added regression verification unit tests in `HomeLabAI/src/tests/test_telemetry_grounding.py` (2/2 PASSED).

#### 📊 Story 107.21: Historical Benchmark Synthetic Data Regression Audit & Scrub (`BKM-085` / `FEAT-494`) &mdash; [COMPLETED & CERTIFIED]
* **Implementation Details**:
  1. **Stream Scrub**:
     - Backed up `Portfolio_Dev/field_notes/data/live_usage_stream.jsonl` to `*.bak_spr107_pre_scrub`.
     - Purged 859 synthetic 35.0 tok/s Intercom entries, preserving all 121 authentic production multi-seat dispatches from `delegate.py`.
     - Synchronized scrubbed stream to `Dev_Lab/www_deploy/data/live_usage_stream.jsonl`.
  2. **Cumulative Sovereign Ledger Recalculation**:
     - Recalculated `Portfolio_Dev/field_notes/data/cumulative_tokens.json` strictly from the 121 authentic dispatches (110,851 tokens, 2.099 kWh consumed).
     - Reset `web_intercom` counters to 0 until new metered receipts arrive from `handle_telemetry_ingest`.
     - Synchronized updated ledger to `Dev_Lab/www_deploy/data/cumulative_tokens.json`.
  3. **Public Airlock Grounding & Zero-Fallback N/A Display**:
     - Overhauled `Portfolio_Dev/field_notes/public_benchmarks.html`: replaced static hardcoded bars (35.4 tok/s, 75.0 tok/s, 280.0 tok/s) with authentic live measurements (`m5_air` 3.98 tok/s, `z87_2080ti` 23.9 tok/s) and explicit `— (N/A)` / `OFFLINE` indicators for unmeasured/offline tiers (`Windows 4090`, `Cloud Swarm`).
     - Injected client-side `syncPublicBenchmarks()` script to dynamically bind to `benchmarks_cache.json`.
     - Synchronized updated `public_benchmarks.html` and `data/benchmarks_cache.json` to `Dev_Lab/www_deploy/`.

#### 📊 Story 107.22: Silicon Gauntlet, Daemon Reload & Airlock Deployment &mdash; [COMPLETED & CERTIFIED]
* **Unit Test Gauntlet**:
  - `pytest Portfolio_Dev/field_notes/tests/`: 24/24 PASSED (0.74s).
  - `pytest HomeLabAI/src/tests/` (two_mice, triage, censorship, telemetry_grounding): 32/32 PASSED (2.62s).
  - Total: 56/56 automated unit tests green.
* **Daemon Hot-Reload**:
  - `POST http://127.0.0.1:8765/reload_residents`: `{"status": "success", "message": "Resident nodes hot-reloaded successfully (commit: 9ee48f1). vLLM VRAM preserved."}`
* **Public Airlock Deployment**:
  - Verified synchronized deployment across `Dev_Lab/www_deploy/` (`public_benchmarks.html`, `data/live_usage_stream.jsonl`, `data/cumulative_tokens.json`, `data/benchmarks_cache.json`).

#### 📊 Story 107.23: Pass 2 Scrub, Universal Timeline Canvas Overlay & 2080 Ti Pinky Backfill (`FEAT-494` / `FEAT-496`) &mdash; [COMPLETED & CERTIFIED]
* **Implementation Details**:
  1. **Pass 2 Stream Scrub (Synthetic Test Blended Telemetry)**:
     - Identified 23 mock `"Test Blended Telemetry"` entries (200 tokens, 5.0s, 40.0 tok/s) originating from test loops in Sprint 100.5 (`delegate.py`).
     - Excised all 23 mock records from `Portfolio_Dev/field_notes/data/live_usage_stream.jsonl`.
  2. **Model Throughput Canvas Universal Timeline Overlay**:
     - Diagnosed horizontal "chaining" in `field_notes/benchmarks.js`: `allPoints = seatNames.flatMap(s => bySeat[s])` partitioned seats side-by-side (`Cloud -> M5 Air -> Kender`) using array index `idx / (n - 1)`.
     - Refactored `renderThroughputLiveChart(records)`: unified stream sorted chronologically by epoch `timestamp`, mapping `getX(ts) = padLeft + ((ts - minTime) / timeSpan) * chartW`.
     - Rendered multi-series curves and scatter points for each seat across the shared universal time domain, adding 5 periodic date/time gridlines (`MM/DD HH:mm`) and seat value badges.
     - Updated canvas subtitle in `field_notes/benchmarks.html` to reflect universal timeline overlay.
  3. **Linux 2080 Ti Pinky Deliberation Backfill**:
     - Harvested 20 authentic physical receipts from `round_table_deltas.json` (Turns 30–51), mapping exact Pinky deliberation token counts (`(X tokens)` in `distillation_bullets`) and stopwatch elapsed durations (`pinky_judgment` in `deltas_elapsed_s`).
     - Backfilled 20 authentic `Linux 2080ti` records (0.9 to 13.3 tok/s) into `live_usage_stream.jsonl`.
     - Verified full federated lab representation across all 4 tiers: Windows 4090RTX (50), Cloud Swarm (34), Linux 2080ti (20), Apple M5 Air (14) &mdash; total 118 authentic empirical records.
  4. **Cumulative Ledger & Deployment Sync**:
     - Recalculated `cumulative_tokens.json`: 109,429 lifetime tokens (42,661 sovereign local, 66,768 cloud swarm, 2.09959 kWh consumed).
     - Synchronized `benchmarks.js`, `benchmarks.html`, `live_usage_stream.jsonl`, and `cumulative_tokens.json` to `Dev_Lab/www_deploy/`.

#### 📊 Story 107.24: Metric 1 Decoupling, Macro Task N/A Display & Telemetry Engine Hardening &mdash; [COMPLETED & CERTIFIED]
* **Implementation Details**:
  1. **Telemetry Grounding (Metric 1 Standard)**:
     - In `HomeLabAI/src/infra/cumulative_telemetry.py:log_telemetry_event`: decoupled hardware generation throughput (`throughput_tok_s`) from macro task workflow velocity (`workflow_velocity_tok_s`).
     - Hardened the logging engine so that if `raw_throughput_tok_s` is not explicitly provided by a pure generation stopwatch, `throughput_tok_s` is stored as `null` (`N/A`) rather than falling back to dividing tokens by total multi-minute agent wall-clock time.
  2. **Historical Stream Retrospective Cleanse**:
     - Evaluated all 118 records in `Portfolio_Dev/field_notes/data/live_usage_stream.jsonl`.
     - Preserved true physical decode benchmarks: 20 Pinky 2080 Ti deliberation rounds (0.9–13.3 tok/s), bulk 8K 4090 runs (13.6–14.1 tok/s), and verified LLM runs on M5 Air (15.8 tok/s) and Cloud (7.7–39.0 tok/s).
     - Converted 83 macro agent coding stories (where duration measured test runs and tool execution loops) to `throughput_tok_s: null`, honestly reporting `— (N/A)` in the live stream table.
  3. **Canvas & Table UI Grounding**:
     - In `Portfolio_Dev/field_notes/benchmarks.js`: updated `loadLiveUsageStream()` to render `<span style="color:#8b949e;">— (N/A)</span>` for records lacking physical generation stopwatches, preventing false ~0.15 tok/s flatlines from pulling down silicon velocity lines.
     - Updated `renderThroughputLiveChart()` to plot only authentic non-null Metric 1 points on the canvas.
  4. **Future Telemetry Pipeline Hardening**:
     - In `HomeLabAI/src/tests/delegate.py`: updated `record_swarm_telemetry` to extract true generation timing (`info.timing.eval_duration`) from upstream providers if present, passing `None` when only macro session wall time is known.
     - Bumped cache buster in `field_notes/benchmarks.html` to `?v=spr107_metric1_na` and synchronized all assets to `Dev_Lab/www_deploy/`.
     - Hot-reloaded resident daemons via `POST http://127.0.0.1:8765/reload_residents`.





