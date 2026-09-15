# 🚀 Sprint 81 Plan: Sovereign Prose-First Wordsmithing & Deep Water-Level Palette

**Sprint ID:** `SPR_81_0`  
**Focus:** Sovereign Prose-First Layout, Unified Hover Toolbox, Deep Water-Level DNA Palette, and Collapsible Sys-Console  
**Target Files:** [`Portfolio_Dev/field_notes/writer.html`](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/writer.html), [`HomeLabAI/src/v5/foyer/router.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/v5/foyer/router.py)  
**Features Implemented:** **FEAT-590** *(Sovereign Prose-First Layout & Unified Hover Toolbox)*, **FEAT-591** *(Deep Water-Level DNA Palette & Collapsible Console Stream)*  
**Governance:** BKM-004 (QQ Protocol), BKM-006 / BKM-030 (Autonomy Gate), BKM-040 (Local Git Discipline), BKM-049 (Owner Tag Mandate)

---

## 🎯 Executive Summary & Architectural Vision

Sprint 81 delivers key ergonomic refinements to make `writer.html` a world-class, sovereign wordsmithing environment:
1. **Default Tab & Prose-First Layout (`FEAT-590`):** Sets `🌊 Writing View` as the default view. Author prose renders at the top of each paragraph container, with supporting citation epigraphs and anchors positioned directly below.
2. **Unified Hover Toolbox & Auto-Opening Wordsmithing Drawer (`FEAT-590`):** Eliminates duplicate buttons by consolidating into `.toolbox-hover-pill` (`[✍️ Wordsmith]`, `[🔍 Discover]`, `[↩️ Discard]`). Clicking `[✍️ Wordsmith]` or paragraph indicators auto-opens `#wordsmithing-drawer` with active context preloaded. Fixes `openCitationInspector` $\rightarrow$ `openInspector`.
3. **Deep Water-Level DNA Palette & Waterline Card Popover (`FEAT-591`):** Compiles a deep candidate pool of ~20 semantic hits from ChromaDB and bone co-members. Supports single-click `[+]` surface and `[✖]` submerge actions, cross-waterline micro-dragging, and clicking `#palette-waterline` pops up an elevated inspection card.
4. **Collapsible Sys-Console Footer (`FEAT-591`):** Adds a minimize/expand toggle button to `#sys-console`, collapsing to a 28px status bar (`🟢 Ready · 0 Errors`) with `localStorage` persistence.

---

## 📋 Story Breakdown & Delegation Matrix (BKM-049)

### **Story 81.1: Sovereign Prose-First Layout, Default Tab & Sentry Fix**
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Feature Anchor:** **FEAT-590**
* **Deliverables:**
  1. Set default `STATE.activeTab = 'writing'` and initialize `#write-view-panel` active on startup.
  2. In `renderWritingView`, append `prose` before `epigraphsWrap` so author text is on top.
  3. Fix ReferenceError on line 17094: change `openCitationInspector(c)` to `openInspector(c)`.

---

### **Story 81.2: Unified Hover Toolbox & Auto-Opening Wordsmithing Drawer**
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Feature Anchor:** **FEAT-590**
* **Deliverables:**
  1. Rename and consolidate `.hover-action-pill` into `.toolbox-hover-pill` with `[✍️ Wordsmith]`, `[🔍 Discover]`, and dynamic `[↩️ Discard]`.
  2. Remove redundant inline action buttons in `.dirty-banner`.
  3. Auto-open `#wordsmithing-drawer` (renamed from `#review-drawer`) on single-click of `[✍️ Wordsmith]` or paragraph focus.

---

### **Story 81.3: Deep Water-Level DNA Palette & Waterline Card Popover**
* **Assigned Owner:** `[SWARM:CLOUD]` via `delegate.py` on REST `:4097`
* **Feature Anchor:** **FEAT-591**
* **Deliverables:**
  1. Enhance Foyer `handle_paper_discover_citations` (`router.py`) to compile ~20 top related candidate citations.
  2. Implement elevated inspection card popover (`#palette-card-popover`) on top of sidebar palette when clicking `#palette-waterline`.
  3. Ensure seamless surface `[+]` and submerge `[✖]` gestures and dynamic attached/suggested counters.

---

### **Story 81.4: Collapsible Sys-Console Footer & Persistence**
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Feature Anchor:** **FEAT-591**
* **Deliverables:**
  1. Add minimize/expand chevron toggle to `#sys-console` header.
  2. Style 28px slim collapsed status bar (`🟢 Sys Console: Ready · 0 Errors · Click to Expand`).
  3. Persist collapsed state across page reloads via `localStorage`.

---

### **Story 81.5: Schema Invariants, LaTeX Sync, and Site Compilation**
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Feature Anchor:** **FEAT-590** / **FEAT-591**
* **Deliverables:**
  1. Verify `validate_paper_schema.py` passes 100% on `paper_jitc_intuition.json`.
  2. Run `scripts/build_writer.py` and `field_notes/build_site.py` with 0 code drift.
  3. Generate `docs/sprints/active/SPRINT_LOG_SPR_81.md` and commit locally.

---

### **Story 81.6: Attendant-Native 30-Minute Rolling Reset Engine**
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Feature Anchor:** **FEAT-537**
* **Deliverables:**
  1. Move the 30-minute quiet-window reset evaluator directly into `FoyerRouter.scheduled_tasks_loop` in `HomeLabAI/src/v5/foyer/router.py`.
  2. Implement native execution upon timer expiry (`now >= expiry_ts` and `pending_action != "NONE"`):
     - `SOFT_RELOAD`: Hot-reload resident nodes in-memory (`await self.residents.boot_all()`).
     - `DEEP_RESET`: Gracefully flush state and re-execute process in-place via `os.execv` (or clean restart).
  3. Cleanly clear `pending_reset.json` after execution.
  4. Update `HomeLabAI/src/infra/git_reset_hook.py` to remove stale supervisor invocation references.

---

### **Story 81.7: FeatureTracker FEAT-537 Documentation Alignment**
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Feature Anchor:** **FEAT-537**
* **Deliverables:**
  1. Update `FEAT-537` in `Portfolio_Dev/FeatureTracker.md` to document the Attendant-native rolling reset engine, git hook dirty queueing, and tiered soft/deep reset execution.
  2. Validate `verify_feature_links.py` and `build_site.py` pass cleanly.

