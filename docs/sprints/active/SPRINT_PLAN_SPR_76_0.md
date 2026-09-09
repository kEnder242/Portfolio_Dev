# 🚀 SPRINT PLAN 76.0: The Wisdom Architecture & JITC Whitepaper
## Swarm Hardening, Decoupled Origin/Synthesis, Dual-View Workbench, Sprint DNA & arXiv Pipeline

**Sprint ID:** `SPR_76_0`  
**Theme:** OpenAgent Swarm Hardening & Oracle Mode, Wisdom Architecture (`origin` vs. `synthesis`), Native Dual-View Workbench (`philosophy.html` & `paper.html`), Dedicated `sprint_dna` ChromaDB Collection with Smart Archiving Trigger, and JITC arXiv Synthesis Pipeline  
**Status:** ACTIVE / IN PROGRESS  
**Parent Framework:** BKM-020 (High-Fidelity Sprint Documentation), BKM-049 (Tri-Loop Delegation), BKM-040 (Git Discipline), BKM-024 (Live Verification), BKM-029 (Heads-Down Loop)  
**Target Web Targets:** `Portfolio_Dev/field_notes/philosophy.html`, `Portfolio_Dev/field_notes/paper.html`, `Portfolio_Dev/field_notes/data/wisdom_data.json`  
**Target Silicon & DB:** ChromaDB Port 8001 (`sprint_dna`, `long_term_wisdom`, `philosophy_dna`), M5 Air MLX `:8000`, ICM SQLite (`wisdom-philosophy`, `agent-discipline`)  

---

## 🏛️ Approved Context & Strategic Invariants (Grill-Me Alignment)

During the Sprint 76.0 alignment sessions, the following fundamental design decisions and operational laws were approved:

### 1. 🛡️ The Wisdom Card Law: Decoupled `origin` vs. `synthesis`
* **`origin` (Human Sovereign)**: Contains verbatim, unmodified quotes, voice dumps, and thoughts authored by `jallred`.
  - *Invariant Rule*: AGY, mice, and delegated models are strictly FORBIDDEN from altering, overwriting, or hallucinating within `origin`. Only the human operator modifies this field.
* **`synthesis` (Agent Collaborative)**: Contains machine scaffolding, contextual narrative, touched codebase anchors, academic literature connections, and review critique.
  - *Collaborative Rule*: AGY, local silicon (M5 Air/Atlas), and cloud reviewer models can iteratively draft, refine, and grade the synthesis block.
* **Relations & Graph**:
  - `explicit_links`: Hard-coded relationship IDs (`WIS-001` connects to `WIS-018`).
  - `tags`: Soft semantic vectors for ChromaDB querying.

### 2. 🎛️ The Native Dual-View Workbench Pattern (`philosophy.html` & `paper.html`)
* **Solidified Default / Reader View**: By default, pages present clean, solidified, publication-ready views:
  - `philosophy.html`: High-density philosophical essays, theme filters, quote callouts matching `stories.html`.
  - `paper.html`: Academic paper format, section hierarchy, equations, figures, and epigraphs.
* **Interactive Workbench Mode (`?edit=1` or Admin Toggle)**:
  - In-place editing of human `origin` thoughts vs agent `synthesis` scaffolding.
  - Drag-and-drop section and card re-ordering.
  - Semantic tag editor and explicit ID relationship connector.
  - Action buttons to trigger local silicon refinement or compile directly to LaTeX/PDF.

### 3. 🗄️ `sprint_dna` Hybrid Ingestion & Recency Decay
* **Hybrid Chunking**: Level 1 (Story Cards with prompt triggers, touched files, lessons learned) + Level 2 (Sprint Overview with high-level themes, metrics, and retros).
* **Discrete 3-Tier Recency Curve**:
  - **Active Sprint**: Weight `1.0`
  - **Past 5 Sprints**: Weight `0.85`
  - **Older Archived Sprints**: Weight `0.30`
* **Targeted Ambient Hook Gate**: `icm_hook.py` queries `sprint_dna` strictly when prompt contains keyword anchors (`SPR-xx`, `Story xx`, `sprint`, `plan`, `retro`, `sprint_dna`) with a 150ms fail-open timeout.
* **Smart Archiving Trigger & Single-Worker Batch**: Moving a sprint to `docs/sprints/archive/` enqueues single-sprint distillation to M5 Air sovereign engine with execution duration telemetry.

### 4. 🛑 Operational Discipline, Anti-Starvation & Swarm Hardening
* **No Parallel Delegation**: Parallel subagent swarms cause thrashing and context fragmentation. Dispatches are strictly serialized (ICM memory `01M21GZE1CNKQHRW4B1ZE6TEVH`).
* **The Anti-Starvation Rule (Zero Google Gemini in OpenAgent)**: AGY is Layer 1 Strategic Guardian. Google/Gemini is strictly prohibited in OpenAgent fallback chains (`disabled_providers: ["google", "mistral"]`).
* **Dedicated Oracle Dispatch Mode**: Cloud models (Nemotron-120B, Command-A+, Llama 3.3 70B) are dispatched strictly in read-only Oracle mode for high-context clustering, outline proposal, and adversarial critique.
* **BKM-040**: Stage and commit locally only, never push.
* **New Addition**: Integrated swarm validation gates now enforce ICM memory consistency checks before any dispatch, ensuring no context fragmentation across serialized operations.

---

## 🧬 Sprint 76 Detailed Story Specifications

### 🧬 Story 76.0: OpenAgent Swarm Vetting, Oracle Mode & Canary Certification
* **Feature Anchor:** `[FEAT-556]` / `[BKM-034]`  
* **Objective:** Harden OpenAgent swarm configuration with live vetted free/cloud models, add first-class `--mode oracle` support to `delegate.py`, and certify REST dispatch with live canary tests.
* **Target Files:**
  - `Dev_Lab/oh-my-openagent.json`
  - `HomeLabAI/src/tests/delegate.py`
  - `HomeLabAI/src/tests/test_delegation_canary.py`
* **Success Criteria:**
  1. `oh-my-openagent.json` mapped to verified active models (`nvidia/nemotron-3-super-120b-a12b:free`, `nvidia/nemotron-3.5-lightning:free`, `cohere/north-mini-code:free`).
  2. `delegate.py` implements `--mode oracle` with structured prompt contracts for clustering, outlines, and review.
  3. Canary test passes with 0 interactive popups and sub-2s tool latency.

---

### 🧬 Story 76.1: Wisdom Schema & Dual-Channel Ingestion Pipeline
* **Feature Anchor:** `[FEAT-558]`  
* **Objective:** Establish the canonical Wisdom Card schema (`WIS-xxx`) with decoupled `origin` and `synthesis` fields. Ingest existing Keep dumps, Philosophy papers, and Google Drive notes into `wisdom_data.json` while syncing vector collections.
* **Target Files:**
  - `Portfolio_Dev/field_notes/data/wisdom_data.json`
  - `Portfolio_Dev/docs/philosophy/PHL-*.md`
  - `HomeLabAI/src/curator/sync_chroma_dna.py`
* **Success Criteria:**
  1. JSON schema strictly enforces `origin.immutable: true` and isolates `synthesis` block.
  2. Initial batch of 8+ core engineering philosophy cards ingested from Drive/Keep notes without altering human origin text.
  3. ChromaDB collection `long_term_wisdom` / `philosophy_dna` on `:8001` indexed and queryable.

---

### 🧬 Story 76.2: Dual-View Wisdom Studio (`wisdom.html` & `wisdom_build.py`)
* **Feature Anchor:** `[FEAT-559]`  
* **Objective:** Build `Portfolio_Dev/field_notes/wisdom.html` featuring a solidified public reader view and an in-place interactive workbench mode for curating wisdom cards.
* **Target Files:**
  - `Portfolio_Dev/field_notes/wisdom.html`
  - `Portfolio_Dev/field_notes/wisdom_build.py`
  - `Portfolio_Dev/field_notes/data/wisdom_data.json`
  - `Portfolio_Dev/field_notes/data/philosophy_data.json`
* **Key Capabilities:**
  1. Solidified Reader View: Theme filtering (Memory, Stability, Human-AI, Vectors), dark-mode typography matching `stories.html`.
  2. In-Place Workbench Mode: Live `origin` quote editing, `synthesis` inspection, explicit link connector.
  3. JSON data pipeline compiled via `wisdom_build.py` with backward-compatible `philosophy.html` symlink.

---

### 🧬 Story 76.3: `sprint_dna` Smart Archiving Trigger & Distillation Engine
* **Feature Anchor:** `[FEAT-557]`  
* **Objective:** Implement dedicated `sprint_dna` ChromaDB collection with hybrid chunking, 3-tier recency decay, smart archiving queue, and targeted ambient hook integration.
* **Target Files:**
  - `HomeLabAI/src/curator/sync_sprint_dna.py`
  - `HomeLabAI/config/hooks/icm_hook.py`
  - `HomeLabAI/src/engine_client.py`
* **Success Criteria:**
  1. All 56 archived sprint plans in `Portfolio_Dev/docs/sprints/archive/` ingested into `sprint_dna` with hybrid story/sprint embeddings and discrete recency weights (`1.0`, `0.85`, `0.30`).
  2. Archiving a sprint file triggers a single-worker M5 Air background distillation job logging elapsed execution time.
  3. `icm_hook.py` injects relevant sprint DNA when prompt contains sprint keywords within 150ms.

---

### 🧬 Story 76.4: Interactive Paper Studio & arXiv LaTeX Pipeline (`paper.html`)
* **Feature Anchor:** `[FEAT-560]`  
* **Objective:** Build `Portfolio_Dev/field_notes/paper.html` with in-place section re-ordering and an automated LaTeX compilation pipeline to produce an arXiv-ready whitepaper on the JITC Meta-Framework.
* **Target Files:**
  - `Portfolio_Dev/field_notes/paper.html`
  - `Portfolio_Dev/scripts/build_paper.py`
  - `Portfolio_Dev/docs/whitepaper/main.tex`
  - `Portfolio_Dev/docs/whitepaper/references.bib`
* **Success Criteria:**
  1. `paper.html` provides dual-view: solidified academic paper preview + interactive section re-order/quote slotting workbench.
  2. `build_paper.py` reads ordered cards from `wisdom_data.json`, embeds `origin` quotes as epigraphs/blockquotes, and weaves `synthesis` explanatory text.
  3. Compiles to clean LaTeX document adhering to arXiv formatting standards with automated PDF artifact generation.
  4. Zero drift of human origin voice throughout compilation.

---

## 📊 Verification Ledger

| Story ID | Verification Method | Silicon Target | Sign-off Status |
| :--- | :--- | :--- | :--- |
| **76.0** | Swarm model ping & Canary delegation suite | REST `:4097` / OpenRouter | PASSED |
| **76.1** | Schema unit tests & ChromaDB query probe | ChromaDB `:8001` | PASSED |
| **76.2** | UI DOM interaction & LocalStorage sync test | M5 Air TurboQuant `:8000` | PASSED |
| **76.3** | Archive ingestion benchmark & M5 Air distillation timing | ChromaDB `:8001` / M5 Air | PASSED |
| **76.4** | `build_paper.py` compile run & LaTeX syntax check | Local Python / PDF | PASSED |

---

## 📌 Top of Backlog: Upcoming Architectural Tracks

### 🏛️ [BACKLOG-01] The Agent Cascade Architecture (Context-Isolated Swarms)
* **Core Problem Solved:** Eliminates the AGY spoon-feeding overhead trap. If Layer 1 (AGY) has to hand-curate exact import paths, line numbers, and function signatures for every dispatch, the orchestrator's token expenditure eclipses direct AST implementation. The solution is an **Agent Cascade**—a daisy-chain of specialized, small-context local micro-agents that isolate token burdens into independent ephemeral sessions.
* **The 4-Stage Sovereign Cascade Pipeline:**
  1. **Stage 1: Planner / Sequencer (Atlas on KENDER 4090):** Ingests the high-level story and acceptance criteria. Emits an execution plan with ordered sub-tasks. (No code editing).
  2. **Stage 2: Anchor & Import Resolver (Librarian / Scout on KENDER 4090):** Uses `read`, `grep`, and LSP symbols to discover the real incumbent import paths, target lines, and incumbent code blocks. Assembles the exact 4-anchor micro-patch payload.
  3. **Stage 3: Surgical Patcher (Sisyphus-Junior on M5 Air via Headroom):** Receives the resolved micro-payload (<2,000 tokens). Applies edits strictly via `clara-dna_safe_patch` (or `write` for greenfield files). Has **zero bash** and runs **zero tests**. Context is flushed immediately upon exit.
  4. **Stage 4: Verification & Lint Runner (Argus / Momus on KENDER 4090):** Dedicated test runner with `bash`. Runs `pytest`, `ruff check`, parses stack traces, and reports clean pass/fail or diff corrections back to Atlas without polluting Junior's or the Planner's memory windows.
* **Key Benefits:**
  - True sovereign self-healing without AGY intervention.
  - Keeps each local agent's prefill footprint well under hardware caps (<3k tokens).
  - Maximizes OpenAgent's native architectural design for lean context workflows.
