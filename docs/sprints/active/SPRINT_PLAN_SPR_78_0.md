# 🚀 SPRINT PLAN 78.0: The Composable Writer Studio & Paper Synthesis Pipeline
## Multi-Paper Dataset Architecture, Cross-DNA Citation Pointers, Structure-to-Synthesis Reflow & Inspector Ergonomics

**Sprint ID:** `SPR_78_0`  
**Theme:** Transitioning `writer.html` from a single-paper static view to a composable thought organizer managing discrete paper datasets (`Portfolio_Dev/papers/`); Cross-DNA citation resolution (`WIS`, `PHL`, `DISC`, `FEAT`, `ArXiv/Research`); Inspector side-panel using the single-card wisdom layout; and decoupled structure-to-synthesis reflow.  
**Status:** PROPOSED / READY FOR REVIEW (Planning Phase)  
**Parent Framework:** BKM-020 (High-Fidelity Sprint Documentation), BKM-046 (Fast-Path DNA Retrieval), BKM-024 (Live Verification), FEAT-564 (Writer Studio & LaTeX Pipeline), FEAT-580 (Paper Dataset Architecture), FEAT-581 (Kanban Thought Organizer), FEAT-582 (Cross-Collection DNA Citations), FEAT-583 (Paragraph Synthesis Engine), FEAT-584 (Paper Voice Control).  
**Target Web Targets:** `Portfolio_Dev/field_notes/writer.html`, `Portfolio_Dev/scripts/build_writer.py`, `Portfolio_Dev/papers/`, `Portfolio_Dev/field_notes/wisdom.html`.  
**Target Silicon & DB:** ChromaDB Port 8001 (`wisdom`, `philosophy_dna`, `feature_dna`, `discovery`, `sprint_dna`), Foyer REST Port 8765 (`/paper/*`), Local vLLM / Sovereign Engine.

---

## 🏛️ Foundational Architectural Invariants

Based on operator design directives and the Sprint 77 closeout:

### 1. 📂 Discrete File Storage over Monolithic Datasets
* Individual papers reside as discrete JSON documents under **`Portfolio_Dev/papers/`**:
  - `Portfolio_Dev/papers/manifest.json`: Top-level index of papers, active drafts, metadata, and status.
  - `Portfolio_Dev/papers/paper_jitc_framework.json`: The foundational JITC paper.
  - `Portfolio_Dev/papers/paper_intuition_2026.json`: The "Intuition paper (Sept 5 2026)" draft.
* Eliminates concurrent-write clobbering between human operators and agentic draft assistants.

### 2. 🧬 Pointers, Not Copies (DNA as Citations)
* Papers are **compositional documents**, not raw DNA cards.
* Papers own their hierarchical structure (Sections and Paragraphs) and prose ("cached word collections").
* DNA items are referenced strictly as **citation pointers** (`["WIS-001", "FEAT-564", "ARXIV:2305.12345"]`).
* Pointers resolve dynamically at render/compile time from `dna_manifest.json` and `RESEARCH_SYNTHESIS.md`.

### 3. 🦴 The "Bones" Model: Decoupling Structure from Wordsmithing
* **Level 1: Section & Paragraph Bones (Tree / Kanban View):** Operator drags lightweight DNA tags (`[WIS-002]`, `[FEAT-104]`) between structural buckets.
* **Level 2: Review Inspector Panel:** Selecting any citation tag opens an in-place inspector using the single-card card layout from `wisdom.html`.
* **Level 3: Synthesis Reflow (Synthesis View):** Switching views surfaces cached word collections. Paragraphs with altered citation associations are marked dirty with a **[Revise / Re-synthesize]** action, triggering surgical LLM re-wordsmithing without breaking adjacent paragraphs.

---

## 📋 Sprint 78 Phased Stories Breakdown

### 🟢 Phase 1: Core Foundation & Ergonomics (Low-Hanging Fruit / Unambiguous)

#### 🧬 Story 78.1: Multi-Paper Storage & Schema (`[FEAT-580]`)
* **Objective:** Establish the canonical `Portfolio_Dev/papers/` directory, create `manifest.json`, and bootstrap `paper_jitc_framework.json` with Section -> Paragraph UUID hierarchy.
* **Target Files:**
  - `Portfolio_Dev/papers/manifest.json`
  - `Portfolio_Dev/papers/paper_jitc_framework.json`
* **Success Criteria:**
  1. `manifest.json` correctly indexes all papers with ID, title, status, and file pointers.
  2. JITC framework paper successfully migrated with clean paragraph UUID hashes and citation pointer arrays.

#### 🧬 Story 78.2: Cross-Collection DNA Citation Resolution (`[FEAT-582]`)
* **Objective:** Build the citation resolution engine in `build_writer.py` resolving pointers across `wisdom`, `philosophy`, `discovery`, `sprint`, and `RESEARCH_SYNTHESIS.md`.
* **Target Files:**
  - `Portfolio_Dev/scripts/build_writer.py`
  - `Portfolio_Dev/field_notes/data/dna_manifest.json`
* **Success Criteria:**
  1. Resolves citation keys into human-readable epigraph quotes and LaTeX `\cite{...}` keys.
  2. Generates updated `references.bib` containing cross-collection anchors.

#### 🧬 Story 78.3: Writer Studio Multi-Paper UI & Inspector Panel (`[FEAT-580]` / `[FEAT-582]`)
* **Objective:** Add paper selector switcher to `writer.html` header and implement the single-card Review Inspector panel when clicking citation tags.
* **Target Files:**
  - `Portfolio_Dev/field_notes/writer.html`
* **Success Criteria:**
  1. Dropdown permits switching between `JITC Framework` and other active drafts.
  2. Clicking any `[WIS-xxx]` or `[DISC-xxx]` badge opens a sidebar inspector displaying origin quote, synthesis context, and source anchors using the `wisdom.html` single-card styling.

#### 🧬 Story 78.4: Foyer REST Paper Endpoints (`[FEAT-580]`)
* **Objective:** Add `/paper/list`, `/paper/load`, and `/paper/save` routes in Foyer `router.py` enabling both web UI saves and programmatic AGY draft imports.
* **Target Files:**
  - `HomeLabAI/src/v5/foyer/router.py`
* **Success Criteria:**
  1. Surgical atomic saves to individual paper JSON files without clobbering adjacent files.
  2. Automatic trigger of `build_writer.py` upon paper save.

---

### 🟡 Phase 2: Synthesis Reflow & Advanced Thought Organization (Tagged for Research / Deferral)

#### 🧬 Story 78.5: Kanban DNA Citation Drag-and-Drop (`[FEAT-581]`) [RISK: MEDIUM]
* **Objective:** Implement visual drag-and-drop for DNA citation badges across Section/Paragraph columns.
* **Research Flag:** Evaluate `SortableJS` (~8KB local static script) vs native HTML5 DnD for multi-bucket tag slotting.

#### 🧬 Story 78.6: Cascade Paragraph Synthesis & Revision History (`[FEAT-583]` / `[FEAT-584]`) [RISK: HIGH]
* **Objective:** Implement the [Revise / Re-synthesize] flow via sovereign engine to re-weave cached word collections based on modified DNA bone associations, storing up to 3 prior revisions per paragraph.
* **Research Flag:** Requires verifying sovereign engine connection (`X-Lab-Key`) and testing prompt fidelity on paragraph re-weaving.
