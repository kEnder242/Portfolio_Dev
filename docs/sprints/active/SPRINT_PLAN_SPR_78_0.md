# 🚀 SPRINT PLAN 78.0: The Composable Writer Studio & Paper Synthesis Pipeline
## Multi-Paper Dataset Architecture, Cross-DNA Citation Pointers, Structure-to-Synthesis Reflow & Inspector Ergonomics

**Sprint ID:** `SPR_78_0`  
**Theme:** Transitioning `writer.html` from a single-paper static view to a composable thought organizer managing discrete paper datasets (`Portfolio_Dev/papers/`); Cross-DNA citation resolution (`PHL`, `DISC`, `FEAT`, `ArXiv/Research`); Inspector side-panel using the single-card wisdom layout; and decoupled structure-to-synthesis reflow.  
**Status:** PROPOSED / READY FOR REVIEW (Planning Phase)  
**Parent Framework:** BKM-020 (High-Fidelity Sprint Documentation), BKM-046 (Fast-Path DNA Retrieval), BKM-024 (Live Verification), FEAT-564 (Writer Studio & LaTeX Pipeline), FEAT-581 (Paper Dataset Architecture & Storage), FEAT-582 (Cross-Collection DNA Citation Engine), FEAT-583 (Thought Organizer: Tree & Review Inspector), FEAT-584 (Synthesis Reflow & Revision Carousel).  
**Target Web Targets:** `Portfolio_Dev/field_notes/writer.html`, `Portfolio_Dev/scripts/build_writer.py`, `Portfolio_Dev/papers/`, `Portfolio_Dev/field_notes/wisdom.html`.  
**Target Silicon & DB:** ChromaDB Port 8001 (`philosophy_dna`, `feature_dna`, `discovery`, `sprint_dna`), Foyer REST Port 8765 (`/paper/*`), Local vLLM / Sovereign Engine.

---

## 🏛️ Foundational Architectural Invariants

Based on operator design directives and the Sprint 77 closeout:

### 1. 📄 The Unified Paper Paradigm (JITC + Intuition)
* **Single Unified Document (`PAPER-001`):** The *JITC Meta-Framework* and the *Intuition Paper (Sept 5 2026)* represent one singular foundational manuscript (`paper_jitc_intuition.json`). (Note: "Intuition" is an internal development label and can be dropped from public-facing titles).
* **3-Section Anatomy:**
  - **Section 1: JITC Framework & Core Concepts** (synthesizes human intuition and mental models into system design; cites `PHL-xxx` Philosophy DNA).
  - **Section 2: Academic References & Prior Art** (theoretical grounding; cites `RESEARCH_SYNTHESIS.md` / ArXiv anchors).
  - **Section 3: Lab Implementations & Empirical Proof** (working software; cites `FEAT-xxx` code anchors).
* **Storage Location:** `Portfolio_Dev/papers/manifest.json` indexes discrete papers stored as independent JSON documents in `Portfolio_Dev/papers/`.

### 2. 🧬 Taxonomy: The Role of Wisdom vs. Philosophy vs. Gems
* **Wisdom is the Overarching System:** "Wisdom" is the meta-system and framework for defining, linking, and managing all lab DNA—not an individual card prefix. The `WIS-XXX` tag prefix is formally **retired**.
* **`PHL-xxx` (Genuine Philosophy DNA):** High-level foundational mental models, epistemology, and engineering vectors extracted from *Philosophy and Learnings 2024.docx* (`1MH8W3jrhrny0xU46jK27J8nrUQurXk16`), *Philosophy and Learnings 2024–2026* (`1BTQUyUaJlU3P58rgiJiGfWdJNlSOmc7nfgQ9IGODlw0`), and Google Keep notes (`1n2HDfPeh8Cgp073P14VhCoIp3YBp78bv8Lt4wz0IdYQ`).
* **Gems (`GEM-xxx`):** The technical, code-level execution layer extracted from daily engineering logs.
* **No `PAPER-xxx` in ChromaDB:** Papers are composite prose documents that **cite** DNA; they are not atomic retrieval chunks.
* **Deprecate `writer` in `dna_manifest.json`:** Prune the redundant mirror collection.

### 3. 🦴 The "Bones" Model: Decoupling Structure from Wordsmithing
* The writing workflow is explicitly split into three decoupled operational layers:
  1. **Structural Bones (`FEAT-583` - Organization Tree View):** Drag-and-drop or slot lightweight citation chips (`[PHL-002]`, `[FEAT-104]`, `[ARXIV:2305.12345]`) into Section and Paragraph buckets.
  2. **Card Inspection (`FEAT-583` - Single-Card Review Inspector):** Clicking any citation chip opens a clean sidebar displaying that card's origin quote, synthesis narrative, and anchors using the exact `wisdom.html` layout.
  3. **Prose Reflow (`FEAT-584` - Synthesis View):** Hydrates paragraphs into continuous prose. Modifying citation associations in the tree marks the paragraph **`dirty`**, activating an actionable **[⚡ Revise / Re-synthesize]** button that triggers an LLM re-wordsmithing pass without touching adjacent paragraphs.
  4. **Revision History (`FEAT-584` - `< >` Carousel):** Paragraphs track up to `3 revisions` with navigation arrows inside the inspector/toolbar to step back and forth or restore an earlier version.

---

## 📋 Sprint 78 Phased Stories Breakdown

### 🟢 Phase 1: Core Foundation & Ergonomics (Low-Hanging Fruit / Unambiguous)

#### 🧬 Story 78.1: Discrete Paper Dataset Storage (`[FEAT-581]`)
* **Assigned Owner:** `[AGY:PRIMARY]` *(Status: COMPLETED during Housekeeping)*
* **Objective:** Establish the canonical `Portfolio_Dev/papers/` directory, configure `manifest.json`, and bootstrap `paper_jitc_intuition.json` with Section -> Paragraph UUID hierarchy and citation pointer lists.
* **Target Files:**
  - `Portfolio_Dev/papers/manifest.json`
  - `Portfolio_Dev/papers/paper_jitc_intuition.json`
* **Success Criteria:**
  1. `manifest.json` cleanly tracks `PAPER-001` (`jitc_intuition`) with status, author, and date.
  2. `paper_jitc_intuition.json` models Sections 1–3, paragraph UUIDs (`PAR-xxx`), citation arrays referencing `PHL-xxx`, `cached_words`, and `dirty` flags.

#### 🧬 Story 78.2: Cross-Collection Citation Pointer Engine (`[FEAT-582]`)
* **Assigned Owner:** `[SWARM:LOCAL]` *(Execution: delegate.py on REST :4097; Attempt 1)*
* **Objective:** Expand `Portfolio_Dev/scripts/build_writer.py` to resolve citation pointers across multiple collections (`philosophy`, `discovery`, `sprint`, and `RESEARCH_SYNTHESIS.md`).
* **Target Files:**
  - `Portfolio_Dev/scripts/build_writer.py`
  - `Portfolio_Dev/field_notes/data/dna_manifest.json`
* **Success Criteria:**
  1. Resolves citation IDs into human-readable epigraph quotes, code anchor links, and LaTeX `\cite{...}` entries.
  2. Compiles arXiv-ready `Portfolio_Dev/docs/whitepaper/main.tex` and `references.bib` dynamically from the active paper dataset.

#### 🧬 Story 78.3: Writer Studio Multi-Paper UI & Review Inspector Panel (`[FEAT-581]` / `[FEAT-583]`)
* **Assigned Owner:** `[SWARM:CLOUD]` *(Execution: delegate.py on REST :4097; Attempt 1/2)*
* **Objective:** Add paper selector dropdown to `writer.html` and build the single-card Review Inspector slide-out panel for inspecting citations in-place.
* **Target Files:**
  - `Portfolio_Dev/field_notes/writer.html`
* **Success Criteria:**
  1. Header dropdown allows switching papers dynamically.
  2. Clicking any `[PHL-xxx]`, `[DISC-xxx]`, or `[FEAT-xxx]` badge opens the side panel showing origin quote, synthesis text, and metadata matching `wisdom.html` card design.

#### 🧬 Story 78.4: Foyer REST Paper API Endpoints (`[FEAT-581]`)
* **Assigned Owner:** `[SWARM:LOCAL]` *(Execution: delegate.py on REST :4097; Attempt 1)*
* **Objective:** Implement `/paper/list`, `/paper/load`, and `/paper/save` in `HomeLabAI/src/v5/foyer/router.py`.
* **Target Files:**
  - `HomeLabAI/src/v5/foyer/router.py`
* **Success Criteria:**
  1. Browser UI saves paragraph adjustments and citation bindings atomically back to `Portfolio_Dev/papers/*.json`.
  2. Programmatic AGY draft imports can push updates over REST and trigger automated LaTeX verification.

---

### 🟡 Phase 2: Synthesis Reflow, Tag Drag-and-Drop & Revisions

#### 🧬 Story 78.5: Structural Tree View & DNA Tag Drag-and-Drop (`[FEAT-583]`)
* **Assigned Owner:** `[SWARM:CLOUD]` *(Execution: delegate.py on REST :4097)*
* **Objective:** Visual drag-and-drop or slotting interface for DNA citation chips between Section and Paragraph containers in `writer.html`.
* **Implementation:** Deploy lightweight `SortableJS` (~8KB local static script) for buttery, bug-free tag movement without DOM corruption. Moving a chip instantly marks the destination and origin paragraph containers `dirty = true`.

#### 🧬 Story 78.6: Cascade Synthesis Reflow & 3-Tier Revision Carousel (`[FEAT-584]`)
* **Assigned Owner:** `[SWARM:CLOUD]` *(Execution: delegate.py on REST :4097)*
* **Objective:** Implement the **[⚡ Revise / Re-synthesize]** flow to re-weave cached word collections when a paragraph's citation bones change, maintaining the last 3 revisions.
* **UI Controls:** `< >` revision navigator inside the inspector panel allowing the operator to step through recent revisions (timestamp, prompt hash, diff) and revert if needed.

---

### 🔵 Phase 3: Round Table Vocality, Multi-Doc PHL Ingestion & 5x5 Gauntlet

#### 🧬 Story 78.7: Multi-Doc PHL Extraction, Staged Ingestion & Schema Gate (`[FEAT-585]`)
* **Assigned Owner:** `[SWARM:CLOUD]` *(Execution: delegate.py on REST :4097)*
* **Objective:** Scrape and decompose primary documents into atomic `PHL-xxx` Philosophy DNA items and populate the active unified paper (`paper_jitc_intuition.json`).
* **Source Documents:**
  1. `Philosophy and Learnings 2024.docx` (`1MH8W3jrhrny0xU46jK27J8nrUQurXk16`)
  2. `Philosophy and Learnings 2024–2026` (`1BTQUyUaJlU3P58rgiJiGfWdJNlSOmc7nfgQ9IGODlw0`)
  3. `Intuition paper (Sept 5 2026)`
* **Backchannel & Validation:**
  - Automated schema validator (`validate_paper_schema.py`) enforcing paragraph UUIDs, immutable origin pointers, and citation arrays.
  - Internal backchannel allowing AGY to update paper datasets via Foyer REST `POST /paper/save` (`:8765`) or verified atomic disk writes.

#### 🧬 Story 78.8: Round Table Vocality, Non-Blocking Pre-Warm & Sub-Second Triage Fallback (`[FEAT-368]`, `[FEAT-486]`, `[FEAT-233]`)
* **Assigned Owner:** `[SWARM:CLOUD]` *(Execution: delegate.py on REST :4097)*
* **Baseline Anchor:** Historical Turn 1 at 20:19:45 (Sprint 70/71 round table baseline: Pinky <1s preamble $\rightarrow$ Brain/Deep Thought synthesis in ~3-5s).
* **Objective:** Resolve M5 Air cold-start stalls and restore non-blocking waterfall fallback.
* **Core Fixes:**
  1. **M5 Air Startup Pre-Warm Probe (`[FEAT-368]`):** Non-blocking background socket handshake and dummy token prefill on boot to eliminate initial 7-16s KV-cache allocation stalls.
  2. **Decoupled Waterfall Execution (`[FEAT-233]`):** Remove monolithic `asyncio.wait_for` blocking in `router.py`. If Deep Thought synthesis exceeds 2x threshold, immediately stream Pinky's conversational reply without throwing `"pipeline hit a snag"`, allowing Deep Thought to follow up or stream asynchronously.

#### 🧬 Story 78.9: Live 5x5 Timed Gauntlet Certification & Blackboard Ledger Stabilization (`BKM-010`, `BKM-050`, `[FEAT-501]`)
* **Assigned Owner:** `[AGY:PRIMARY]` *(Status: COMPLETED & CERTIFIED)*
* **Objective:** Execute the full live Playwright integration endurance test (`test_perf_5x5_timed.py --intervals 0`) against active running daemons (Foyer `:8765`, Intercom `:9001`, ChromaDB `:8001`, M5 Air OMLX `:8000`).
* **Certification Result:** Live Pinky Hyde response delivered in 17.81s with 0 unmanaged dead air, verified against boot commit `51cc129`.

---

### 🟣 Phase 3: Poly-Domain Citation Bundles, Interactive Tag DnD & Live Revision Carousel

#### 🧬 Story 78.10: Poly-Domain Citation Bundles in JITC Manuscript (`[FEAT-582]`, `[FEAT-585]`)
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Objective:** Cluster related concepts across all 4 operational tiers into loosely coupled **Poly-Domain Citation Bundles** (`PHL + BKM + FEAT + DISC`) in `paper_jitc_intuition.json`:
  1. **Dual-Channel JITC Memory Bundle:** `PHL-001` (Three Pillars) + `PHL-004` (JITC Cycle) + `BKM-046` (Fast-Path DNA) + `FEAT-546` (Semantic Intent) + `DISC-004` (JITC Lifecycle).
  2. **The Hippocampus & Prefrontal Architecture Bundle:** `PHL-002` (Hippocampus Model) + `PHL-003` (Intuition as Retrieval) + `BKM-046` + `FEAT-564` + `DISC-003` (Fast-Path RAG).
  3. **Feedback Backpressure & Closed-Loop Control Bundle:** `PHL-008` (Customer Service Model) + `PHL-009` (Handover Reflection) + `BKM-049` (Tri-Loop Delegation) + `FEAT-522` (Swarm Engine) + `DISC-008` (Handover Reflection Discovery).
  4. **The Bones Model & Knowledge Distillation Bundle:** `PHL-007` (Pearls of Wisdom) + `PHL-018` (Captured Insight) + `BKM-020` (Sprint Docs) + `FEAT-581` (Paper Storage) + `DISC-006` (Gem Refinement).
  5. **Ground-Truth Telemetry & Live Verification Bundle:** `PHL-010` (Live Data as God) + `PHL-015` (Reading Like a Robot) + `BKM-024` (Live Validation Mandate) + `FEAT-501` (Validation Ledger) + `DISC-002` (QQ Silence).
  6. **Sovereign Heterogeneous Silicon & Translation Layer Bundle:** `PHL-024` (The Translation Layer) + `PHL-025` (Class 1 Assumption Hazard) + `FEAT-233` (Decoupled Waterfall) + `FEAT-548` (Bicameral Harness) + `DISC-007` (Bicameral Silicon).
* **Target Files:**
  - `Portfolio_Dev/papers/paper_jitc_intuition.json`
  - `Portfolio_Dev/scripts/build_writer.py`

#### 🧬 Story 78.11: Cross-Paragraph SortableJS Citation Drag-and-Drop & Reactive Dirty State (`[FEAT-583]`)
* **Assigned Owner:** `[SWARM:CLOUD]`
* **Objective:** Enable interactive, bug-free drag-and-drop of citation chips across paragraph containers and sections in `writer.html`.
* **Implementation:**
  - Attach `SortableJS` instance with shared `group: 'citations'` across all `.citation-chips-container` elements.
  - On `onEnd` drop event:
    1. Extract new badge order and update source & destination paragraph `citation_ids` arrays in the client data model.
    2. Mark affected paragraphs as `dirty = true` with a glowing amber border and activate the `[⚡ Re-synthesize]` badge.
    3. Expose a searchable "+ Add Citation" quick-drawer to drop unattached DNA tags (`PHL`, `BKM`, `FEAT`, `DISC`, `ArXiv`) directly into paragraph buckets.
* **Target Files:**
  - `Portfolio_Dev/field_notes/writer.html`

#### 🧬 Story 78.12: 3-Tier Revision History `< >` Carousel & In-Place Restoration (`[FEAT-584]`)
* **Assigned Owner:** `[SWARM:CLOUD]`
* **Objective:** Equip every paragraph in `writer.html` and the Single-Card Review Inspector with a 3-tier revision carousel.
* **UI Controls & Schema:**
  - Paragraph schema tracks `revisions: [{ "version": 1, "text": "...", "timestamp": "...", "model": "..." }]` (capped at 3 items).
  - Paragraph header and side inspector render `< >` arrow buttons showing `Rev 2/3 (2026-09-14 00:45)`.
  - Clicking `<` or `>` previews past versions inline; clicking `[↺ Restore]` atomically reverts the active paragraph prose and updates the manuscript state.
* **Target Files:**
  - `Portfolio_Dev/field_notes/writer.html`
  - `Portfolio_Dev/papers/paper_jitc_intuition.json`

#### 🧬 Story 78.13: In-Browser Re-Synthesis Engine & Atomic Foyer REST Persistence (`[FEAT-581]`, `[FEAT-584]`)
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Objective:** Close the authoring loop with live in-browser paragraph re-synthesis and direct disk save.
* **Implementation:**
  1. **`[⚡ Re-synthesize]` Action:** Clicking the button sends a targeted prompt to Foyer REST `:8765/paper/synthesize` or local LLM, weaving the paragraph's updated citation bundle epigraphs into cohesive academic prose without disturbing adjacent paragraphs.
  2. **`[💾 Save Manuscript]` Button:** Top toolbar action sends the complete active paper JSON to Foyer `POST /paper/save`, writing atomically to `Portfolio_Dev/papers/paper_jitc_intuition.json` and triggering `build_writer.py` to compile LaTeX `main.tex` and `references.bib`.
* **Target Files:**
  - `Portfolio_Dev/field_notes/writer.html`
  - `HomeLabAI/src/v5/foyer/router.py`
  - `Portfolio_Dev/scripts/build_writer.py`

