# 🚀 SPRINT PLAN 77.0: The Federated Wisdom System
## Universal DNA Workbench, Nightly Synthesis Refinement, Semantic Bucketing & `writer.html` Thought Organizer

**Sprint ID:** `SPR_77_0`  
**Theme:** Iterative Evolution of the Gem System into the Universal Wisdom Framework; Generic DNA Editor (`wisdom.html`); Automated Nightly Synthesis Refinement (`refine_wisdom.py`); Semantic Bucketing & Deduplication; Thought Organizer Transition (`paper.html` $\rightarrow$ `writer.html`); and Backpressure / WYWO Feedback Architecture.  
**Status:** PROPOSED / READY FOR REVIEW  
**Parent Framework:** BKM-020 (High-Fidelity Sprint Documentation), BKM-046 (Fast-Path DNA Retrieval), BKM-024 (Live Verification), FEAT-558 (Wisdom Schema WIS-001), FEAT-559 (Wisdom Studio), FEAT-560 (Paper Studio & LaTeX Pipeline), FEAT-416 (Nightly Refinement Sweeper).  
**Target Web Targets:** `Portfolio_Dev/field_notes/wisdom.html`, `Portfolio_Dev/field_notes/wisdom_build.py`, `Portfolio_Dev/field_notes/writer.html`, `Portfolio_Dev/field_notes/data/wisdom_data.json`, `Portfolio_Dev/scripts/build_paper.py`.  
**Target Silicon & DB:** ChromaDB Port 8001 (`philosophy_dna`, `long_term_wisdom`, `feature_dna`, `behavioral_dna`, `sprint_dna`, `blackboard_ledger_dna`), M5 Air MLX `:8000` (Qwen 27B / TurboQuant), Local Nightly Forge (`HomeLabAI/src/infra/nightly_forge.py`).

---

## 🏛️ Approved Context & Strategic Invariants (From "Wisdom system" Google Doc)

During the Sprint 77.0 synthesis of the human operator's *"Wisdom system"* design document, the following core principles, constraints, and architecture boundaries were established:

### 1. 🛡️ The Dual-Channel Invariant: Immutable Origin vs. Refinable Synthesis
* **Origin (The Human Sovereign Anchor):** Personal historical notes, verbatim voice dumps, Keep logs, and career journals (`author: "jallred"`, `immutable: true`).
  - *Absolute Law:* Machine agents, background loops, and LLMs are strictly forbidden from modifying, rewriting, or hallucinating within `origin`.
* **Synthesis (The Collaborative Backpressure Layer):** Machine scaffolding, narrative framing, lab anchors, and review notes (`narrative_context`, `lab_anchors`, `review_notes`, `refinement_version`).
  - *Evolution Rule:* Automated nightly passes and agentic peers can iteratively refine, cross-link, and polish this layer.

### 2. 🎛️ Generic DNA Editor Vision (`wisdom.html`)
* `wisdom.html` serves as a generic viewer/editor across the Federated Lab's DNA collections in ChromaDB and local JSON stores.
* **Access Control:**
  - **Read-Only:** `feature_dna`, `behavioral_dna` (BKM/BKC), `sprint_dna`, `career_ledger`, `artifact_vault`.
  - **Interactive / Read-Write:** `wisdom_data.json` (Wisdom DNA) and `writer.html` (Paper DNA).
  - **Top-Level Dropdown:** Provides immediate switching across collections while enforcing read-only locks on structural lab DNA.

### 3. 🌙 Folding Wisdom with Gems: Nightly Synthesis Refinement
* Wisdom refinement is the philosophical equivalent of Technical Gem refinement (`refine_gem.py`).
* An automated nightly pass (`refine_wisdom.py`) executes during the off-peak 03:00–05:00 AM maintenance window (`nightly_forge.py`).
* Candidate cards with unpolished or low-version synthesis are analyzed against the untouched `origin` to generate sharper narrative context, tag associations, and codebase anchors.

### 4. 🗂️ Semantic Bucketing over Time-Decay Tiers
* Notes/Gems historically relied on 3-tier recency decay (time-based: active, recent 5, archive).
* Wisdom and philosophical engineering thoughts transcend chronological dates. They belong in **Semantic Buckets** (e.g. *Memory & JITC*, *Stability & Backpressure*, *The Human-AI Interface*, *Engineering Rigor & Vectors*).
* Buckets are discovered dynamically during refactoring passes and refined through tagging and visual canvas organization.

### 5. ✍️ Evolution from `paper.html` to `writer.html`
* `paper.html` transitions into `writer.html` as a dedicated **Organizer of Thoughts**.
* Functions at the domain level: visual bucket arrangement, paragraph ordering, DNA sequence slotting, and drafting with co-authoring assistance.

### 6. 📄 Intuition Paper Ingestion Strategy (Google Doc "Intuition paper (Sept 5 2026)")
* **Levels of Buckets (Hierarchy):** Rather than forcing prose essays into single cards, the hierarchy is:
  $$\text{Document Section} \rightarrow \text{Semantic Bucket} \rightarrow \text{Discrete Card (Epigraph/Anchor)} \rightarrow \text{Synthesis Text}$$
* **Prior Art & Citations:** Prior art is not crammed into wisdom cards. It leverages the existing **`research_dna`** domain (`research.html` / `references.bib`), allowing `writer.html` to slot citation pointers (`[CITE: key]`) that compile cleanly to LaTeX `\cite{...}`.
* **Diagram Action Cards:** Architecture workflows (e.g. JITC Cycle diagram) are represented as reminder action cards with a `[DIAGRAM PLACEHOLDER]` tag that render framed diagram boxes in LaTeX drafts until graphic assets are provided.
* **Staged Import vs Immediate DB Fill (Avoiding the Chicken-and-Egg Trap):** Do *not* prematurely mass-populate `wisdom_data.json` before the schema and bucket validators are wired. Prepare clean ingestion staging specs first so schema iterations do not require manual DB migration churn.

---

## 🧬 Sprint 77 Detailed Story Specifications

### 🧬 Story 77.1: Multi-DNA Collection Selector in `wisdom.html` (Core / Low-Hanging Fruit)
* **Feature Anchor:** `[FEAT-561]` / `[FEAT-559]`  
* **Objective:** Expand `wisdom.html` and `wisdom_build.py` with a top-level collection dropdown selector allowing the operator to inspect all lab DNA stores from a single unified UI.
* **Target Files:**
  - `Portfolio_Dev/field_notes/wisdom.html`
  - `Portfolio_Dev/field_notes/wisdom_build.py`
  - `Portfolio_Dev/field_notes/data/dna_manifest.json`
* **Success Criteria:**
  1. Top-level dropdown selector provides options: `Wisdom DNA` (default, RW), `Paper/Writer DNA` (RW), `Feature DNA` (RO), `Behavioral DNA (BKM)` (RO), `Sprint DNA` (RO), `Philosophy DNA` (RO).
  2. Selecting a read-only DNA collection switches the card view to display the respective items with a visible `[READ-ONLY SYSTEM DNA]` badge, locking all edit controls.
  3. Selecting `Wisdom DNA` restores the live in-place Workbench editing of `synthesis.narrative_context` and `synthesis.review_notes`.
  4. **Direct REST Save Endpoint:** Implement `POST /wisdom/save` on Foyer daemon (`:8765`), allowing `wisdom.html` "Save" button to write directly to `Portfolio_Dev/field_notes/data/wisdom_data.json` on disk with atomic JSON schema validation, eliminating manual clipboard exports.
  5. Build pipeline (`wisdom_build.py`) bundles DNA summary manifests without bloating browser load times.

---

### 🧬 Story 77.2: Automated Nightly Wisdom Synthesis Refiner (`refine_wisdom.py`) (Core / Low-Hanging Fruit)
* **Feature Anchor:** `[FEAT-562]` / `[FEAT-416]`  
* **Objective:** Create `Portfolio_Dev/field_notes/refine_wisdom.py` modeled after `refine_gem.py` to automatically polish unrefined wisdom cards during the nightly forge maintenance window.
* **Target Files:**
  - `Portfolio_Dev/field_notes/refine_wisdom.py`
  - `HomeLabAI/src/infra/nightly_forge.py`
  - `Portfolio_Dev/field_notes/data/wisdom_data.json`
* **Success Criteria:**
  1. Identifies candidate wisdom cards with `refinement_version < 2` or unpopulated `lab_anchors` / `narrative_context`.
  2. Dispatches a bounded, low-temperature prompt to local silicon (M5 Air Qwen 27B or Daedalus) presenting the immutable `origin.text`.
  3. Produces structured output: concise `title`, tightened `narrative_context`, relevant `lab_anchors` (verified file paths/BKMs), and 3–5 semantic `tags`.
  4. Atomically updates `wisdom_data.json`, increments `refinement_version`, sets `last_refined_by: "M5_AIR"`, and preserves `origin.text` verbatim with zero byte drift.
  5. Wired into `nightly_forge.py` as a non-blocking step executing within the 03:00–05:00 AM window.

---

### 🧬 Story 77.3: Semantic Bucketing & Deduplication Engine (Core / Low-Hanging Fruit)
* **Feature Anchor:** `[FEAT-563]`  
* **Objective:** Establish a first-class "Bucket" taxonomy in the wisdom schema and build an automated semantic similarity pass to detect duplicate thoughts and cluster cards.
* **Target Files:**
  - `Portfolio_Dev/field_notes/data/wisdom_data.json`
  - `Portfolio_Dev/field_notes/wisdom_build.py`
  - `Portfolio_Dev/field_notes/data/buckets.json`
* **Success Criteria:**
  1. Seed initial standard buckets extracted from Sprint 74 & 76:
     - `Bucket 1: Memory & JITC`
     - `Bucket 2: Stability & Backpressure`
     - `Bucket 3: Human-AI Interface & The Perfect Foil`
     - `Bucket 4: Engineering Rigor & Vectors`
     - `Bucket 5: Architecture & Infrastructure`
  2. Add `bucket_id` to `wisdom_data.json` card metadata.
  3. Nightly deduplication pass: calculates cosine similarity across embeddings in `philosophy_dna` collection; flags pairs with similarity > 0.82 in a `pending_review.json` ledger for human review rather than destructive auto-merging.

---

### 🧬 Story 77.4: Thought Organizer Transition (`paper.html` -> `writer.html`) (Core / Low-Hanging Fruit)
* **Feature Anchor:** `[FEAT-564]` / `[FEAT-560]`  
* **Objective:** Cleanly rebrand and evolve `paper.html` into `writer.html` as a structured thought organizer that maps visual buckets into draft chapters and exports clean LaTeX, performing a complete workspace-wide rename with zero symlinks.
* **Target Files:**
  - `Portfolio_Dev/field_notes/writer.html` (renamed from `paper.html`)
  - `Portfolio_Dev/scripts/build_writer.py` (renamed from `build_paper.py`)
  - `Portfolio_Dev/field_notes/mission-control.js`
  - `www_deploy/mission-control.js`
  - `Portfolio_Dev/field_notes/build_site.py`
* **Success Criteria:**
  1. Complete workspace search-and-replace: all occurrences of `paper.html`, "Paper Studio", and `build_paper.py` migrated cleanly to `writer.html`, "Writer Studio", and `build_writer.py` across `Portfolio_Dev`, `www_deploy`, and documentation. Zero symlinks created.
  2. `writer.html` deployed with visual bucket columns (or swimlanes) allowing drag-and-drop or sequential re-ordering of wisdom cards.
  3. Preserves dual-view functionality: Solidified Reader View (rendered essay / academic draft) + Interactive Organizer Workbench.
  4. Updated `build_writer.py` compiles the ordered bucket sequences into `Portfolio_Dev/docs/whitepaper/main.tex` and triggers automated PDF verification.

---

### 🧬 Story 77.5: Silicon Division-of-Labor Clarification Loop & Human Reflection Queue (Core Architecture Blueprint)
* **Feature Anchor:** `[FEAT-565]`  
* **Objective:** Establish the two-tier silicon division of labor for generating and ranking ambiguity questions, track human vs machine feedback in the data structure, and integrate an in-place human reflection queue in `wisdom.html` and WYWO.
* **Architecture & Division of Labor:**
  1. **Tier 1 Question Generation (Local vLLM / 2080 Ti):** Scans candidate wisdom cards for high semantic ambiguity, missing boundaries, or implicit assumptions and generates 2–3 targeted clarification questions.
  2. **Tier 2 Merit Ranking (M5 Air Qwen 27B / TurboQuant):** Evaluates candidate questions on a 0.0–1.0 merit scale: *"Does answering this question resolve high architectural/philosophical ambiguity, or is it trivial pedantry?"* Filters out low-merit questions.
  3. **Data Structure Feedback Separation:** Cards maintain an explicit `clarifications` array distinguishing machine-generated inquiry from sovereign human answers:
     ```json
     {
       "id": "CQ-01",
       "question": "Does 'Token Golf' apply to system prompts or subagent handovers?",
       "merit_score": 0.94,
       "generated_by": "VLLM",
       "ranked_by": "M5_AIR",
       "status": "PENDING_HUMAN",
       "human_answer": null,
       "answered_via": "WISDOM_HTML" | "WYWO_CONSENSUS"
     }
     ```
  4. **Human Reflection Interfaces:**
     - **Discrete UI (`wisdom.html`):** Cards float the top-ranked pending ambiguity question with a simple answer prompt for human reflection.
     - **Semi-Automatic Flow (WYWO Consensus):** Deliberation sessions or async WYWO summaries surface top-ranked questions for conversational human answers.
  5. **Closing the Loop (Synthesis Re-Wordsmithing):** When the human provides raw answers, M5 Air is re-triggered to ingest the human answer and weave it into `synthesis.narrative_context` (Human provides the raw truth; LLM does what it does best with wordsmithing).

---

---

## 🏛️ Phase 2: Novel Ideas Evolutionary Timeline (`timeline.html`)

**Feature Anchor:** `[FEAT-566]`  
**Target Web Targets:** `Portfolio_Dev/field_notes/timeline.html`, `Portfolio_Dev/field_notes/timeline_build.py`, `Portfolio_Dev/field_notes/data/timeline_data.json`, `Portfolio_Dev/field_notes/data/timeline_outliers.json`.  
**Intent:** Track and showcase the original art, discovery timeline, and organic engineering evolution of the Dev_Lab. Serves as the evolutionary companion to `research.html` and the historical backbone for the Intuition whitepaper.

### 1. Data Taxonomy & Naming Convention: The `discovery` Schema
We adopt **`discovery`** (or **`timeline_event`**) as the canonical data item:
```json
{
  "id": "DISC-001",
  "title": "Subconscious Dreaming Cycle",
  "conception_date": "2026-01-14",
  "implementation_date": "2026-01-19",
  "bucket_id": "distillation",
  "lane": "JITC: Distillation & Consolidation",
  "origin_artifact": "VIBE-005 / FEAT-067",
  "sprint_ref": "SPRINT_PLAN_SPR_52_0.md",
  "code_anchors": ["HomeLabAI/src/infra/dream_cycle.py", "field_notes/mass_scan.py"],
  "arxiv_inspiration": null,
  "summary": "Automated off-peak synthesis converting raw daily notes into Rank 4/5 diamond gems.",
  "status": "ACTIVE"
}
```

### 2. UI Layout & Visual Design
* **Header / Navigation:** Standard Hamburger sidebar (`mission-control.js`) with responsive drawer.
* **Top Half: Interactive Gantt Chart:**
  * **X-Axis:** Scrollable / pannable time scale showing `[conception -> implementation]` span.
  * **Y-Axis:** Semantic Buckets / Swimlanes (Race tracks). Items with minimal overlap share lanes to maximize vertical density.
  * **Interactivity:** Hover tooltip (quick summary, dates), Click event (locks list focus and highlights interconnected nodes).
* **Bottom Half: Reactive Detail List:**
  * Rendered from static `timeline_data.json`.
  * Filters reactively when a Gantt bar or lane is clicked.
  * Rich detail cards: Clickable links to specific Sprint Markdown files, Git code anchors, ArXiv inspiration pointers (cross-linked to `research.html`), and BKM/FEAT numbers.

### 3. Lane / Bucket Definitions (Cognitive Flow Pipeline: Option B)
> 🎨 **Paper Figure Stand-in:** `Triage Classification -> Ambient Hooks -> (Inside LLM: Context -> Attention -> Reply ) -> Distillation -> Storage`  
> *(Author Pen & Paper Blueprint Anchor — represents the living reflex arc of the Federated Lab and serves as the conceptual architecture graphic for the forthcoming publication).*

* **Lane 1: Triage & Classification** (`triage`): Informational inquiry gates, QQ protocol (BKM-004), autonomy gating (BKM-006/030), model selection routing via Foyer.
* **Lane 2: Ambient Hooks & Monitors** (`ambient_hooks`): Invisible background watchdogs, filesystem monitors, `git_reset_hook.py`, quiescence telemetry timers (FEAT-318), and AST memory guards.
* **Lane 3: LLM Kernel (Context · Attention · Reply)** (`llm_kernel`):
  * *Context:* Runtime dynamic anchor injection, Token Golf (BKM-051), 3-Tier RAG packing.
  * *Attention:* Multi-agent swarm delegation (`delegate.py`), CoT preservation, tool orchestration.
  * *Reply:* Structured output parsing, safe patching (`clara-dna_safe_patch`), live WebSocket streaming.
* **Lane 4: Distillation & Synthesis** (`distillation`): Post-turn synthesis, subconscious dreaming (VIBE-005), blackboard gem refinement, and error-to-protocol crystallization.
* **Lane 5: Memory & Substrate Storage** (`storage`): ChromaDB vector vaults, persistent ICM SQLite episodic recall, git commit/branch ledger, and zero-torch precomputed caches.


### 4. Scraping, Ingestion & Consolidation Pipeline
* **Multi-Tier Harvest:**
  * **AGY / Author Pre-Seed:** Bootstrap initial canonical milestones (Dreaming, QQ, 3-Tier RAG, JITC, Gem Refinement).
  * **Cloud Swarm Sweep (Prometheus / Oracle):** Broad initial pass across `FeatureTracker.md`, `docs/Protocols.md`, and archived `SPRINT_PLAN_*.md` to populate candidate `conception_date` and `implementation_date` spans.
  * **Local Nightly Dreaming Sweep:** Ingest newly closed sprint stories and git commits, tagging bucket associations automatically.
* **The Outlier Review Pipeline (`timeline_outliers.json`):**
  * Items with low confidence bucket alignment ($< 0.65$ embedding similarity) are written to an `[outliers list]`.
  * Outliers are surfaced in `timeline.html` / `wisdom.html` for human consideration $\rightarrow$ prompting the operator to confirm or declare a new bucket category.

---

## 📊 Verification Ledger

| Story ID | Verification Method | Silicon Target | Sign-off Status |
| :--- | :--- | :--- | :--- |
| **77.1** | UI dropdown switching, RW/RO badge, & Foyer `/wisdom/save` REST endpoint | Foyer `:8765` / Chromium | **SIGNED OFF (Live Verified)** |
| **77.2** | Standalone execution of `refine_wisdom.py` & M5 Air zero-torch refiner | M5 Air `:8000` / Local | **SIGNED OFF (Live Verified)** |
| **77.3** | Bucket schema validation & zero-torch precomputed ChromaDB dedup test | ChromaDB `:8001` | **SIGNED OFF (Live Verified)** |
| **77.4** | `writer.html` DOM rendering, section re-ordering & `main.tex` compile | Local Python / pdflatex | PENDING |
| **77.5** | Architectural review & WYWO prototype rubric evaluation | Design Review / BKM-005 | PENDING |
| **77.6** | Gantt SVG rendering, lane click-filter, outlier ledger & airlock deploy | Python / Chromium / Airlock | **SIGNED OFF (Live Verified)** |

---

## 🗺️ Scope & Risk Management: Low-Hanging Fruit vs. Stretch Goals

> 📜 **Cloud Oracle Swarm Review:** Full adversarial review and scalability audit saved in [`Portfolio_Dev/docs/sprints/active/ORACLE_REVIEW_SPRINT_77.md`](file:///home/jallred/Dev_Lab/Portfolio_Dev/docs/sprints/active/ORACLE_REVIEW_SPRINT_77.md).

| Track | Tier | Complexity | Risk | Rationale & Oracle Mitigation Gate |
| :--- | :--- | :--- | :--- | :--- |
| **Multi-DNA Dropdown in `wisdom.html`** | Low-Hanging Fruit | Low | Minimal | UI-only read-only locking; reuses existing ChromaDB and manifest structures. |
| **Nightly `refine_wisdom.py`** | Low-Hanging Fruit | Low-Med | Low | Adapts proven `refine_gem.py` pattern; strictly touches `synthesis` only. |
| **Initial 5 Buckets & Tagging** | Low-Hanging Fruit | Low | Minimal | Formalizes Sprint 74 themes; provides immediate structural clarity. |
| **`writer.html` Rebranding & Canvas** | Low-Hanging Fruit | Med | Low | Renames `paper.html` and adds card/paragraph ordering controls. **Oracle Invariant:** Keep editor contenteditable/DOM-first; strictly avoid heavy real-time browser IDE features. |
| **`timeline.html` Gantt & List View** | Core Deliverable | Med | Low | Canvas/SVG Gantt chart + reactive detail list from static `timeline_data.json`. High visual ROI. |
| **Discovery Harvester & Outlier List** | Core Deliverable | Med | Low | Scrapes BKMs, FEATs, and Sprints for date ranges; routes unclassified items to `timeline_outliers.json`. |
| **Atomic Card Granularity Gate** | **Scope Guard** | Med | **High** | **Oracle Warning #1 (Card Explosion):** Capping cards to core axioms/pearls only (~10-25 cards). Connective narrative remains in section paragraphs, preventing a 200-card combinatorial sprawl. |
| **Ambiguity Drift Firewall** | **Scope Guard** | Med | **High** | **Oracle Warning #2 (Prompt Drift):** Ground vLLM question generation with strict boundary prompt. Human answer stage acts as hard context reset before M5 Air re-synthesis. |
| **Automated Markdown "Rebuild"** | **Stretch / Design** | High | **High** | Reverse-syncing machine synthesis into human markdown risks format corruption and git thrash. Unidirectional export only. |
| **WYWO Clarification Loop** | **Stretch / Design** | Med-High | Med | Requires async queue, question ranking model, and user prompt injection. Blueprint first. |
| **Legacy Gem/BKM Full Migration** | **Future Phase** | High | Med-High | Deferred until Wisdom System proves stable across multiple nightly cycles. |

---

## 🛠️ Phase 3: Post-Execution Forensic Hardening & Navigation Alignment

### 1. Navigation Scoping & Public Airlock Censorship Fix
* **The Issue:** Censoring "Publications & Wisdom" previously swallowed all of `<section id="mission-control">` on the public airlock (`www.jason-lab.dev`), hiding internal navigation links (Artifact Files, Lab Status, AI Intercom, Feature Tracker, Model Benchmarks).
* **The Resolution:** Refactored `field_notes/mission-control.js`:
  * `<section id="mission-control">` is preserved on the public airlock.
  * `<section id="publications-wisdom">` (Wisdom Studio, Writer Studio, Novel Ideas Timeline) is strictly hidden from public airlock and only rendered on internal `notes.jason-lab.dev`.

### 2. Forensic Resolution of Blank Sidebar on `protocols.html`
* **The Root Cause:** In `HomeLabAI/docs/Protocols.md` line 752, an unbalanced code fence inverted all downstream code blocks. An ASCII diagram containing `HomeLabAI/src/tests/delegate.py ... --title "<Title>"` was rendered as unescaped raw HTML.
* **The Browser Trap:** Web browsers parse `<Title>` as an HTML `<title>` element (case-insensitive), immediately switching to RCDATA plain-text mode. This swallowed the entire bottom of `protocols.html`—including `<script src="mission-control.js"></script>`—preventing `customElements.define` from executing.
* **The Fix:**
  1. Balanced the code fence in `HomeLabAI/docs/Protocols.md`.
  2. Standardized BKM headers (BKM-020, BKM-049, BKM-051, BKM-052, BKM-053).
  3. Hardened `field_notes/protocols_build.py` regex with resilient heading parsing.
  4. Verified via Playwright headless browser test: DOM parsed cleanly, `mission-control.js` executed, and `#sidebar` rendered 2,680 bytes of navigation HTML.

---

## 🏛️ Phase 4: Cognitive Flow Pipeline Alignment & Zero-Torch Policy

### 1. Dual-Anchor Invariant Registration
* **`BKM-054: Zero In-Process PyTorch on Orchestrator Host`**: Registered in `HomeLabAI/docs/Protocols.md`. Governs agent behavior and test harnesses against importing PyTorch or SentenceTransformers on the 16GB z87 host. Embeddings must be offloaded to remote silicon endpoints (M5 Air / vLLM) or read from precomputed JSON caches.
* **`FEAT-567: Orchestrator Memory Guard & AST Import Linter`**: Registered in `Portfolio_Dev/FeatureTracker.md`. Enforces automated AST linting and assertion gates against host OOM and session resets.

### 2. Cognitive Flow Pipeline (Option B) & Paper Graphic Anchor
* **The Living Reflex Arc:** Replaced static software silos with the 5-stage cognitive lifecycle drawn from the author's pen & paper notes:
  $$\text{Triage Classification} \longrightarrow \text{Ambient Hooks} \longrightarrow \left(\text{Inside LLM: Context} \longrightarrow \text{Attention} \longrightarrow \text{Reply}\right) \longrightarrow \text{Distillation} \longrightarrow \text{Storage}$$
* **Whitepaper Integration:** Tagged as the official conceptual architecture graphic stand-in for the federated autonomous lab paper.

### 3. Nomenclature & Visual Identity
* **Prefix & Identifier:** Retained `DISC-xxx` as the compact machine and schema identifier.
* **User-Facing Terminology:** Standardized all UI presentation on **"Innovations"** (e.g. *Innovations Matrix*, *Lab Innovations Timeline*, *Filter Innovations*).

---

## 🏛️ Phase 5: In-Place Wisdom Ergonomics & Host Telemetry Loop Hardening

### 1. New Feature Anchors Registered
* **`[FEAT-568]` In-Place Single-Card Surgical Save & Fast-Path ChromaDB Sync:** Replaces bulk page saves with per-card unlocking and atomic single-document ChromaDB upsert (`POST /wisdom/save_card`).
* **`[FEAT-569]` Reactive Semantic Bucket Selector & Dynamic Theme Assignment:** Direct `<select>` dropdown binding to the 5 canonical buckets in `buckets.json`, updating card accent border and ChromaDB metadata.
* **`[FEAT-570]` Daemon Exporter Heartbeat Throttling & Port-Busy Resilience:** Persistent daemon loop in `bench_models.py` with 60s sleep and socket reuse (`SO_REUSEADDR`) to permanently eliminate the 10-second systemd restart loop (counter 569+).

### 2. Forensic Crash Fix & Systemd Remediation
* **Root Cause:** 7.4 GB sudden memory allocation during `lab-attendant` cold boot coupled with process churn from `bench-models-exporter.service` (respawning every 10s due to clean exit without persistent loop).
* **Fix Plan:**
  1. Refactor `bench_models.py` to run an internal persistent sleep loop (60s cycle), avoiding repeated process exits and restarts.
  2. Implement socket `SO_REUSEADDR` to eliminate port 8011 `TIME_WAIT` collisions.
  3. Reload `systemctl --user daemon-reload && systemctl --user restart bench-models-exporter.service`.

### 3. Wisdom Studio In-Place Refactor Plan
* **Card Unlock Flow:**
  - Default: `[ 🔓 Edit ]` on top-right of card header.
  - Active: Enables `contenteditable="true"` on narrative, title, notes, tags, and activates the bucket dropdown. Action morphs to `[ 💾 Save ]` &bull; `[ ✖ Discard ]`.
  - Discard restores snapshot; Save posts to `/wisdom/save_card` and performs instant ChromaDB single-document upsert.
* **Markdown Backflow Stub:**
  - RO items (`behavioral`, `feature`, `sprint`) display `[ 🔒 Markdown Origin (Git Anchored) - SafePatch Backflow Stubbed ]`.

---

## 🏛️ Phase 6: Universal Data Bridge — Sprint DNA Manifest & Read-Write Innovations (`DISC`) & Gems

### 1. Architectural Intent
1. **Automated Sprint DNA Distillation (`[FEAT-557]`):**
   - Update `HomeLabAI/src/curator/sync_sprint_dna.py` to compile Level 2 Sprint Overviews into a canonical `sprint_data.json` and inject all 77 sprints into `dna_manifest.json["sprint"]`.
   - Wire `sync_sprint_dna.py` into the nightly maintenance flow so new and updated sprint documents stay synchronized automatically with zero manual churn.
2. **Read-Write Innovations (`DISC` / Novel Ideas):**
   - Implement `POST /timeline/save_card` in `router.py` to allow in-place surgical editing and saving of `timeline_data.json` directly from `wisdom.html`.
   - Update `wisdom.html` collection switcher to make `discovery` (`DISC`) Read-Write (`dna-badge rw`).
3. **Technical Gems Living Layer (`GEM-xxx`):**
   - Treat `YYYY.json` as the derived synthesis layer of engineering logs: manual refinements in `career_notes.html` or `wisdom.html` save into `YYYY.json` without modifying or clobbering immutable raw notes.




