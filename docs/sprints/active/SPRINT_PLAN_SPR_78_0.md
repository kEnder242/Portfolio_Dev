# 🚀 SPRINT PLAN 78.0: The Composable Writer Studio & Paper Synthesis Pipeline
## Multi-Paper Dataset Architecture, Cross-DNA Citation Pointers, Structure-to-Synthesis Reflow & Inspector Ergonomics

**Sprint ID:** `SPR_78_0`  
**Theme:** Transitioning `writer.html` from a single-paper static view to a composable thought organizer managing discrete paper datasets (`Portfolio_Dev/papers/`); Cross-DNA citation resolution (`WIS`, `PHL`, `DISC`, `FEAT`, `ArXiv/Research`); Inspector side-panel using the single-card wisdom layout; and decoupled structure-to-synthesis reflow.  
**Status:** PROPOSED / READY FOR REVIEW (Planning Phase)  
**Parent Framework:** BKM-020 (High-Fidelity Sprint Documentation), BKM-046 (Fast-Path DNA Retrieval), BKM-024 (Live Verification), FEAT-564 (Writer Studio & LaTeX Pipeline), FEAT-581 (Paper Dataset Architecture & Storage), FEAT-582 (Cross-Collection DNA Citation Engine), FEAT-583 (Thought Organizer: Tree & Review Inspector), FEAT-584 (Synthesis Reflow & Revision Carousel).  
**Target Web Targets:** `Portfolio_Dev/field_notes/writer.html`, `Portfolio_Dev/scripts/build_writer.py`, `Portfolio_Dev/papers/`, `Portfolio_Dev/field_notes/wisdom.html`.  
**Target Silicon & DB:** ChromaDB Port 8001 (`wisdom`, `philosophy_dna`, `feature_dna`, `discovery`, `sprint_dna`), Foyer REST Port 8765 (`/paper/*`), Local vLLM / Sovereign Engine.

---

## 🏛️ Foundational Architectural Invariants

Based on operator design directives and the Sprint 77 closeout:

### 1. 📄 The Unified Paper Paradigm (JITC + Intuition)
* **Single Unified Document (`PAPER-001`):** The *JITC Meta-Framework* and the *Intuition Paper (Sept 5 2026)* represent one singular foundational manuscript (`paper_jitc_intuition.json`). (Note: "Intuition" is an internal development label and can be dropped from public-facing titles).
* **3-Section Anatomy:**
  - **Section 1: JITC Framework & Core Concepts** (synthesizes engineering intuition into system design; cites `WIS-xxx` and `PHL-xxx`).
  - **Section 2: Academic References & Prior Art** (theoretical grounding; cites `RESEARCH_SYNTHESIS.md` / ArXiv anchors).
  - **Section 3: Lab Implementations & Empirical Proof** (working software; cites `FEAT-xxx` code anchors).
* **Storage Location:** `Portfolio_Dev/papers/manifest.json` indexes discrete papers stored as independent JSON documents in `Portfolio_Dev/papers/`.

### 2. 🧬 Taxonomy: What Lives in DNA vs. What Lives in Papers
* **`WIS-xxx` (Retained & Primary):** Battle-tested operational engineering heuristics (e.g. *Token Golf*, *10x Debt & Whiplash*, *The Handover Reflection*). Fully maintained in `wisdom_data.json` and ChromaDB `:8001`.
* **`PHL-xxx` (Genuine Philosophy DNA):** High-level foundational mental models and epistemology extracted from *Philosophy and Learnings 2024–2026* (`1BTQUyUaJlU3P58rgiJiGfWdJNlSOmc7nfgQ9IGODlw0`) and Google Keep notes (`1n2HDfPeh8Cgp073P14VhCoIp3YBp78bv8Lt4wz0IdYQ`). The raw philosophy dumps are **not** the paper; they are reference sources for `PHL-DNA`.
* **No `PAPER-xxx` in ChromaDB:** Papers are composite prose documents that **cite** DNA; they are not atomic retrieval chunks.
* **Deprecate `writer` in `dna_manifest.json`:** Remove the redundant clone of `WIS-001..008`.

### 3. 🦴 The "Bones" Model: Decoupling Structure from Wordsmithing
* The writing workflow is explicitly split into three decoupled operational layers:
  1. **Structural Bones (`FEAT-583` - Organization Tree View):** Drag-and-drop or slot lightweight citation chips (`[WIS-002]`, `[FEAT-104]`, `[ARXIV:2305.12345]`) into Section and Paragraph buckets.
  2. **Card Inspection (`FEAT-583` - Single-Card Review Inspector):** Clicking any citation chip opens a clean sidebar displaying that card's origin quote, synthesis narrative, and anchors using the exact `wisdom.html` layout.
  3. **Prose Reflow (`FEAT-584` - Synthesis View):** Hydrates paragraphs into continuous prose. Modifying citation associations in the tree marks the paragraph **`dirty`**, activating an actionable **[⚡ Revise / Re-synthesize]** button that triggers an LLM re-wordsmithing pass without touching adjacent paragraphs.
  4. **Revision History (`FEAT-584` - `< >` Carousel):** Paragraphs track up to `3 revisions` with navigation arrows inside the inspector/toolbar to step back and forth or restore an earlier version.

---

## 📋 Sprint 78 Phased Stories Breakdown

### 🟢 Phase 1: Core Foundation & Ergonomics (Low-Hanging Fruit / Unambiguous)

#### 🧬 Story 78.1: Discrete Paper Dataset Storage (`[FEAT-581]`)
* **Objective:** Establish the canonical `Portfolio_Dev/papers/` directory, configure `manifest.json`, and bootstrap `paper_jitc_intuition.json` with Section -> Paragraph UUID hierarchy and citation pointer lists.
* **Target Files:**
  - `Portfolio_Dev/papers/manifest.json`
  - `Portfolio_Dev/papers/paper_jitc_intuition.json`
* **Success Criteria:**
  1. `manifest.json` cleanly tracks `PAPER-001` (`jitc_intuition`) with status, author, and date.
  2. `paper_jitc_intuition.json` models Sections 1–3, paragraph UUIDs (`par_xxxxxx`), citation arrays, `cached_words`, and `dirty` flags.

#### 🧬 Story 78.2: Cross-Collection Citation Pointer Engine (`[FEAT-582]`)
* **Objective:** Expand `Portfolio_Dev/scripts/build_writer.py` to resolve citation pointers across multiple collections (`wisdom`, `discovery`, `sprint`, and `RESEARCH_SYNTHESIS.md`).
* **Target Files:**
  - `Portfolio_Dev/scripts/build_writer.py`
  - `Portfolio_Dev/field_notes/data/dna_manifest.json`
* **Success Criteria:**
  1. Resolves citation IDs into human-readable epigraph quotes, code anchor links, and LaTeX `\cite{...}` entries.
  2. Compiles arXiv-ready `Portfolio_Dev/docs/whitepaper/main.tex` and `references.bib` dynamically from the active paper dataset.

#### 🧬 Story 78.3: Writer Studio Multi-Paper UI & Review Inspector Panel (`[FEAT-581]` / `[FEAT-583]`)
* **Objective:** Add paper selector dropdown to `writer.html` and build the single-card Review Inspector slide-out panel for inspecting citations in-place.
* **Target Files:**
  - `Portfolio_Dev/field_notes/writer.html`
* **Success Criteria:**
  1. Header dropdown allows switching papers dynamically.
  2. Clicking any `[WIS-xxx]`, `[DISC-xxx]`, or `[FEAT-xxx]` badge opens the side panel showing origin quote, synthesis text, and metadata matching `wisdom.html` card design.

#### 🧬 Story 78.4: Foyer REST Paper API Endpoints (`[FEAT-581]`)
* **Objective:** Implement `/paper/list`, `/paper/load`, and `/paper/save` in `HomeLabAI/src/v5/foyer/router.py`.
* **Target Files:**
  - `HomeLabAI/src/v5/foyer/router.py`
* **Success Criteria:**
  1. Browser UI saves paragraph adjustments and citation bindings atomically back to `Portfolio_Dev/papers/*.json`.
  2. Programmatic AGY draft imports can push updates over REST and trigger automated LaTeX verification.

---

### 🟡 Phase 2: Synthesis Reflow, Tag Drag-and-Drop & Revisions (Tagged for Research / Deferral)

#### 🧬 Story 78.5: Structural Tree View & DNA Tag Drag-and-Drop (`[FEAT-583]`) [RISK: MEDIUM]
* **Objective:** Visual drag-and-drop or slotting interface for DNA citation chips between Section and Paragraph containers.
* **Research Focus:** Evaluate lightweight `SortableJS` (~8KB local static script) vs native HTML5 DnD to ensure buttery, bug-free tag movement without DOM corruption.
* **Dirty Marking:** Moving a chip instantly marks the destination and origin paragraph containers `dirty = true`.

#### 🧬 Story 78.6: Cascade Synthesis Reflow & 3-Tier Revision Carousel (`[FEAT-584]`) [RISK: HIGH]
* **Objective:** Implement the **[⚡ Revise / Re-synthesize]** flow to re-weave cached word collections when a paragraph's citation bones change, maintaining the last 3 revisions.
* **UI Controls:** `< >` revision navigator inside the inspector panel allowing the operator to step through recent revisions (timestamp, prompt hash, diff) and revert if needed.
* **Pre-flight Requirement:** Verify sovereign engine communication (`X-Lab-Key` auth) before activating automated wordsmithing.
