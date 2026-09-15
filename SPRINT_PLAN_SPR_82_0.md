# 🗺️ SPRINT PLAN: SPR-82.0
## Generic Scoped Document Ingestion, Objective-Driven AST Combinatorial Studio & Anti-Embellishment Synthesis

> **Status:** PROPOSED / BRAINSTORMING ARCHITECTURE  
> **Session Anchor:** 2026-09-15 10:25 PDT  
> **Primary References:** [[BKM-024]], [[BKM-049]], [[FEAT-581]], [[FEAT-582]], [[FEAT-585]], [[FEAT-588]]  

---

### 1. Executive Summary & Vision

In Sprints 78–81, Writer Studio (`writer.html`) established a decoupled AST architecture for technical manuscripts, featuring:
- **Two-tier outliner & writing view** with atomic section/paragraph JSON schemas.
- **DNA Palette with Waterline semantics** ("Above Water" attached citations vs. "Below Water" suggested pool).
- **Cross-collection citation weaving** (`PHL`, `WIS`, `FEAT`, `DISC`, `ArXiv`) compiling directly to LaTeX and Web views.

**Sprint 82.0 expands Writer Studio from a single-manuscript editor into a generic, objective-driven document synthesizer**:
1. **Generic Document Ingestion (`[Import / Open]`):** Parse arbitrary structured text, Markdown, or JSON (including master CVs, research drafts, and technical briefs) into atomic, citation-anchored AST nodes and a dedicated paper-scoped ChromaDB collection (`paper_dna_<slug>`).
2. **Objective / Target Spec Parsing (`[Parse Job Description / Objective]`):** Ingest target requirements (e.g., a Staff AI SRE job description or academic CFP) to calculate dense semantic similarity vectors against both document-local nodes and the federated Wisdom DNA pool.
3. **The Anti-Embellishment Combinatorial Studio (`[Flag / Accept / Reject / Refine]`):**
   - **The Problem:** LLM-assisted resume generation fabricates buzzwords, hallucinates accomplishments, and creates generic corporate slop.
   - **The Solution:** The model is strictly constrained to **combinatorial selection and ranking** of verbatim human bullet points and real engineering citations.
   - **The Workflow:** The system suggests:
     - **Auto-Pruning:** Dropping low-relevance bullets ("Below Water").
     - **Evidence Anchoring:** Attaching real lab features (`FEAT-213`, `FEAT-452`, `BKM-010`) to corroborate experience bullets.
     - **Relevance Reordering:** Sequencing bullet points by mathematical alignment with the target role.

---

### 2. Forensic Review of Legacy Resume Assets

| Asset | Location | Evaluation & Practicality |
| :--- | :--- | :--- |
| **`index_resume_to_rag.py`** | [`HomeLabAI/src/forge/index_resume_to_rag.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/forge/index_resume_to_rag.py) | **Deprecated / Inflexible:** Monolithic 1,000-char regex chunker. Splits text arbitrarily across sentence boundaries and destroys atomic bullet identity. *Verdict: Do not revive script; replace with atomic AST parser.* |
| **`cv_3x3_summary.json`** | [`Portfolio_Dev/field_notes/data/cv_3x3_summary.json`](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/data/cv_3x3_summary.json) | **Useful Seed Archetype:** Well-distilled 3-pillar focal points (*System Validation*, *Platform Telemetry*, *Distributed AI Infra*). *Verdict: Retain as pre-curated candidate themes/pillars.* |
| **Work Stories & Catches** | [`Portfolio_Dev/field_notes/stories.html`](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/stories.html) | **High-Value Raw DNA:** Contains rich, factual narrative history (RAKP CVE catches, VISA signal-tracing, platform telemetry automation). *Verdict: Ingestible directly into the master `career_ledger`.* |

---

### 3. Architectural Blueprint & Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Raw Document Ingestion ([Import / Open])                 │
│    • Ingests raw_resume.md / draft_paper.txt / cv.json      │
│    • Decomposes into atomic paragraph / bullet AST nodes    │
│    • Creates/Updates scoped collection: `paper_dna_<slug>`  │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Target Objective Ingestion ([Parse Job Description / CFP])│
│    • Extracts core skills, domains, and requirement vectors │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Dual-Layer Semantic Scoring Engine                       │
│    A. Scoped Document DNA: Scores local bullets (0.0 – 1.0) │
│    B. Global Wisdom DNA: Finds relevant FEAT/BKM/WIS anchors │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Writer Studio Interactive Curation Canvas (`writer.html`)│
│    • Visual Relevance Heatmap per bullet                    │
│    • Auto-Prune Recommendations (Flag low-scoring bullets)  │
│    • Suggested Evidence Chips from Lab Wisdom DNA           │
│    • Clean Decision Bar: [Accept All] [Reject] [Refine]     │
│    • Verbatim Human Prose Guaranteed (Zero Generative Slop) │
└─────────────────────────────────────────────────────────────┘
```

---

### 4. Sprint 82.0 Story Breakdown (High-Level Proposals)

#### 📋 Story 82.1: Generic Document-to-AST Ingestion Engine (`/paper/import`)
- **Assigned Owner:** `[SWARM:LOCAL]`
- **Objective:** Build backend endpoint `POST /paper/import` that takes raw text, Markdown, or JSON and parses it into compliant AST schema (`structure[]`, `sections[]`, `paragraphs[]` with atomic bullet IDs).
- **Deliverable:** `HomeLabAI/src/v5/foyer/router.py` + `Portfolio_Dev/scripts/parse_document_to_ast.py`.

#### 📋 Story 82.2: Paper-Scoped ChromaDB DNA Collections
- **Assigned Owner:** `[SWARM:LOCAL]`
- **Objective:** Enhance ChromaDB sync and DNA query routers to support dynamic `paper_dna_<slug>` collections with collection-isolated indexing and cross-collection hybrid queries.
- **Deliverable:** Dynamic ChromaDB collection lifecycle in `HomeLabAI/src/curator/sync_sprint_dna.py` and `router.py`.

#### 📋 Story 82.3: Target Objective Vectorizer & Relevance Scorer
- **Assigned Owner:** `[SWARM:LOCAL]`
- **Objective:** Implement `POST /paper/evaluate_objective` which accepts a target job description or prompt, embeds it, and computes similarity scores against document paragraphs and global Wisdom DNA.
- **Deliverable:** `HomeLabAI/src/v5/foyer/router.py` + embedding scorer.

#### 📋 Story 82.4: Objective Curation & Anti-Embellishment UI in `writer.html`
- **Assigned Owner:** `[SWARM:LOCAL]`
- **Objective:** Add `[Target Objective]` drawer in `writer.html` showing:
  - Input box for Job Description / Requirement Brief.
  - Interactive per-bullet relevance badges (e.g., `92% Match`, `34% Match - Prune Recommended`).
  - Action buttons: `[Auto-Prune Low Matches]`, `[Sort by Alignment]`, `[Accept / Dismiss]`.
  - Evidence chip injector pulling relevant `FEAT` and `BKM` anchors into bullet tooltips.
- **Deliverable:** `Portfolio_Dev/field_notes/writer.html` + `Portfolio_Dev/field_notes/style.css`.

---

### 5. Architectural Guardrails & Invariant Laws
1. **Zero Generative Embellishment:** The synthesis engine must only rank, filter, and organize verbatim human text. It must never fabricate experience or hallucinate achievements.
2. **Deterministic Provenance:** Every bullet and suggested evidence link must point to a tangible file, story, or feature ID in the repository.
3. **AST Schema Strictness:** All imported documents must validate against `validate_paper_schema.py` before saving to disk.
