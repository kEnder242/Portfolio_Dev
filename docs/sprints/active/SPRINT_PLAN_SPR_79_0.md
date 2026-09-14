# 🚀 SPRINT PLAN 79.0: The Decoupled Thought Organizer & Wordsmithing Studio
## Hierarchical Tree Outliner with Partitioned DNA Palette vs. High-Cohesion Wordsmithing View

**Sprint ID:** `SPR_79_0`  
**Theme:** Full Architectural Re-platforming of `writer.html`: replacing cluttered legacy single-canvas prototypes with a decoupled, tabbed **`[🌲 Tree View (with Palette)]`** vs. **`[🌊 Wordsmithing View]`** paradigm; Domain-partitioned DNA Palette with top bubble suggestions; and reactive dirty-highlighting across the synthesis pipeline.  
**Status:** PROPOSED / READY FOR REVIEW (Design Studio Phase)  
**Parent Framework:** BKM-005 (Design Studio Alignment), BKM-020 (High-Fidelity Sprint Documentation), BKM-046 (Fast-Path DNA Retrieval), BKM-024 (Live Verification), FEAT-581 (Paper Dataset Architecture), FEAT-582 (Cross-Collection DNA Citation Engine), FEAT-583 (Thought Organizer Tree & Palette), FEAT-584 (Synthesis Reflow & Revision Carousel).  
**Target Web Targets:** `Portfolio_Dev/field_notes/writer.html`, `Portfolio_Dev/scripts/build_writer.py`, `Portfolio_Dev/papers/`.  
**Target Silicon & DB:** ChromaDB Port 8001 (`philosophy_dna`, `feature_dna`, `discovery`, `sprint_dna`), Foyer REST Port 8765 (`/paper/*`).  

---

## 🏛️ Foundational Architectural Invariants

### 1. 🦴 The "Citation Bones" Architecture (Unifying Philosophy & Citations)
* **Invariant:** Citations are the immutable structural **"Bones"** of a manuscript. 
* Rather than maintaining separate vocabularies, the system formally adopts **"Citation Bones"** (`PHL-xxx`, `BKM-xxx`, `FEAT-xxx`, `DISC-xxx`, `ARXIV:xxx`). 
* The **Tree Outliner** organizes the bones; the **Wordsmithing Engine** weaves continuous academic prose around them.

### 2. 🗂️ Clean-Room DOM Rewrite of `writer.html` (Preserving URL & Build Integration)
* We preserve the canonical URL and file name `field_notes/writer.html` for bookmark stability and portfolio cross-linking.
* We scrape the bloated, nested legacy prototype JavaScript and inline DOM scripts, replacing them with a crisp, modular, reactive client runtime.

### 3. 📑 Tabbed Decoupling over Cramped Split-Pane
* Rather than crowding a small screen with side-by-side split panels, the studio features clean top-level tabs:
  1. **`[🌲 Tree View]`**: Structural Outliner canvas with Section/Paragraph AST containers, collapsible nodes, citation bone slotting, and docked DNA Palette Drawer.
  2. **`[🌊 Wordsmithing View]`**: Academic reader/synthesis canvas where paragraphs tagged `dirty` glow with amber highlights and actionable `[⚡ Re-synthesize]` prompts.

### 4. 🎨 Domain-Partitioned DNA Palette & Bubble Suggestions
* The 415+ `FEAT-xxx` items and 28 `PHL-xxx` items are segmented into categorical quick-filters:
  - **Bubble Suggestions:** Top contextual recommendations based on section keywords and adjacent paragraph citations.
  - **Domain Categories:** `[All]`, `[PHL: Philosophy]`, `[BKM: Governance]`, `[FEAT: Cognitive]`, `[FEAT: Silicon]`, `[FEAT: UI/Web]`, `[FEAT: Infra]`, `[DISC: Discoveries]`, `[ARXIV: Prior Art]`.

---

## 🎯 Active Stories Breakdown

### 🧬 Story 79.1: Clean-Room DOM & Modular Architecture for `writer.html` (`[FEAT-581]`, `[FEAT-583]`)
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Objective:** Cleanly refactor `Portfolio_Dev/field_notes/writer.html` into a maintainable, high-performance web app.
* **Implementation:**
  1. Strip duplicated and legacy script blocks.
  2. Implement a single, clean state controller (`__STUDIO_STATE__`) tracking active paper, active tab (`tree` vs `wordsmithing`), palette filter, and inspector target.
  3. Ensure `build_writer.py` hydrates the exact single context injection point without regex collision.
* **Target Files:**
  - `Portfolio_Dev/field_notes/writer.html`
  - `Portfolio_Dev/scripts/build_writer.py`

---

### 🧬 Story 79.2: Hierarchical Tree Outliner Canvas (`Paper > Section > Paragraph > Citation Bones`) (`[FEAT-583]`)
* **Assigned Owner:** `[SWARM:CLOUD]` *(Execution: delegate.py on REST :4097)*
* **Objective:** Implement the collapsible 3-tier AST Outliner view in `writer.html`.
* **Features:**
  1. Visual hierarchy with clear indentation: Paper Root $\rightarrow$ Section Nodes $\rightarrow$ Paragraph Nodes $\rightarrow$ Citation Bone Dropzones.
  2. Drag-and-drop re-ordering of sections and paragraphs using SortableJS.
  3. Inline chip removal (`×`), cross-paragraph dragging, and one-click `+ Add Paragraph` / `+ Add Section`.
  4. Moving or altering chips marks the paragraph `dirty = true`.
* **Target Files:**
  - `Portfolio_Dev/field_notes/writer.html`

---

### 🧬 Story 79.3: Domain-Partitioned DNA Palette Drawer & Bubble Suggestions (`[FEAT-583]`)
* **Assigned Owner:** `[SWARM:CLOUD]` *(Execution: delegate.py on REST :4097)*
* **Objective:** Provide a fast, searchable palette drawer for discovering and slotting citation bones.
* **Features:**
  1. Top **Bubble Suggestions** row rendering smart contextual recommendations (e.g., related `BKM` or `DISC` pairs).
  2. Domain partition pills (`[PHL]`, `[BKM]`, `[FEAT: Cognitive]`, `[FEAT: Silicon]`, `[FEAT: UI]`, `[FEAT: Infra]`, `[DISC]`, `[ArXiv]`).
  3. Instant typeahead search across titles, summaries, and IDs.
  4. Click-to-inspect opening the single-card Review Inspector without interrupting the drag flow.
* **Target Files:**
  - `Portfolio_Dev/field_notes/writer.html`
  - `Portfolio_Dev/field_notes/data/dna_manifest.json`

---

### 🧬 Story 79.4: Wordsmithing View with Reactive Dirty Highlighting (`[FEAT-584]`)
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Objective:** Render continuous academic prose with prominent dirty-card visual state when switching from Tree View.
* **Features:**
  1. Clean, arXiv-style continuous typesetting for unedited text.
  2. **Reactive Amber Dirty State:** Paragraphs modified in Tree View render with glowing amber left borders, an amber badge (`⚑ DIRTY — Bones Modified`), and an active `[⚡ Re-synthesize]` button.
  3. Inline 3-tier revision carousel (`< Rev X/Y >`) with `[↺ Restore]` rollback.
  4. Instant Foyer REST `POST /paper/synthesize` and atomic `POST /paper/save` execution.
* **Target Files:**
  - `Portfolio_Dev/field_notes/writer.html`

---

### 🧬 Story 79.5: Multi-Paper Manifest Selection & Live Compilation Verification (`[FEAT-581]`, `[FEAT-585]`, `BKM-024`)
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Objective:** Ensure seamless switching across papers in `Portfolio_Dev/papers/manifest.json` with live schema verification and automated LaTeX build test.
* **Verification Battery:**
  - `validate_paper_schema.py` (Zero errors).
  - `build_writer.py` (Full `main.tex` and `references.bib` generation).
  - `build_site.py` (Complete static airlock deployment).
