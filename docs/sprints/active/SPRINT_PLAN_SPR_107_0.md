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
