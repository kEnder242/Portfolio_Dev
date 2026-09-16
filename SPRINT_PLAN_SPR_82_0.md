# 🗺️ SPRINT PLAN: SPR-82.0
## Generic Scoped Document Ingestion, Decoupled Two-Tier AST Palette & Anti-Embellishment Combinatorial Studio

> **Status:** PROPOSED / ARCHITECTURAL BLUEPRINT  
> **Session Anchor:** 2026-09-15 12:00 PDT  
> **Primary References:** [[BKM-024]], [[BKM-049]], [[BKM-055]], [[PHL-031]], [[WIS-010]], [[FEAT-581]], [[FEAT-582]], [[FEAT-585]], [[FEAT-588]]  

---

### 1. Executive Summary & Vision

Sprint 82.0 is the **unified, single AST sprint** that elevates Writer Studio (`writer.html`) from a single-manuscript editor into a generic, objective-driven document synthesizer and anti-embellishment career studio.

It combines two foundational breakthroughs:
1. **Functional Decoupling (The Anti-Embellishment Engine):** Traditional AI resume builders hallucinate buzzwords. Here, machine intelligence is strictly constrained to **combinatorial selection, relevance scoring, and auto-pruning** of verbatim human bullet points and tangible engineering citations (`FEAT`, `BKM`, `WIS`).
2. **Data Decoupling (The Self-Contained Two-Tier AST):** Opening sections, editing, and compiling LaTeX operate with **0ms latency and 100% offline portability** by embedding discovered candidate pools (`_candidate_pool[]`) and active citations (`bone_collection[]`) directly within the document AST, decoupling the studio from live database query loops.

---

### 2. Architectural Blueprint & The Tri-Phase Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│ 1. DISCOVER (ChromaDB Vector Lookup)                        │
│    • Ingests raw document via POST /paper/import            │
│    • Creates scoped collection: `paper_dna_<slug>`          │
│    • Queries global collections: PHL, WIS, FEAT, DISC       │
│    • Deposits discovered IDs into tier `_candidate_pool[]`   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. CURATE (Interactive Waterline & Objective Curation)      │
│    • Ingests Target Objective / Job Description (JD)        │
│    • Evaluates semantic alignment per bullet (0.0 – 1.0)    │
│    • Auto-Prunes low-match bullets below the Waterline      │
│    • Promotes approved bones into `bone_collection[]`       │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. GENERATE (Deterministic AST Assembly)                    │
│    • Compiles LaTeX, PDF, or HTML directly from AST bones   │
│    • 100% offline, reproducible, zero generative slop       │
└─────────────────────────────────────────────────────────────┘
```

---

### 3. Hierarchical AST Caching Schema (Document, Section, Paragraph)

```json
{
  "title": "Staff Infrastructure & AI Platforms Resume",
  "bone_collection": ["FEAT-181", "BKM-010", "WIS-042"],
  "_candidate_pool": ["FEAT-213", "BKM-024"],
  "sections": [
    {
      "id": "sec-01",
      "heading": "Distributed AI Infrastructure",
      "bone_collection": ["FEAT-452", "WIS-108"],
      "_candidate_pool": ["FEAT-450", "FEAT-451"],
      "paragraphs": [
        {
          "id": "p-01",
          "text": "Architected multi-model vLLM & Ollama fallback mesh...",
          "citations": ["FEAT-452"],
          "_candidate_pool": ["BKM-044", "FEAT-136"]
        }
      ]
    }
  ]
}
```

---

### 4. Sprint 82.0 Story Breakdown & Delegation Matrix

#### 📋 Story 82.1: Generic Document Ingestion & Two-Tier AST Schema (`/paper/import`)
- **Status:** ✅ COMPLETE
- **Assigned Owner:** `[SWARM:LOCAL]` $\rightarrow$ `[SWARM:CLOUD]` (Tri-Loop Handover)
- **Objective:** Build backend endpoint `POST /paper/import` that parses raw text, Markdown, or JSON into the canonical two-tier AST schema with `bone_collection[]` and `_candidate_pool[]` keys at Root, Section, and Bullet levels.
- **Verification:** Verified `pytest HomeLabAI/src/tests/test_paper_import.py` (38 passed, 0 failed).
- **Deliverable:** `HomeLabAI/src/v5/foyer/router.py` + `Portfolio_Dev/scripts/parse_document_to_ast.py` + `HomeLabAI/src/v5/foyer/validate_paper_schema.py` (commit `862a233` & `711e654`).

#### 📋 Story 82.2: Paper-Scoped ChromaDB DNA Collections
- **Assigned Owner:** `[SWARM:LOCAL]`
- **Objective:** Enhance ChromaDB sync and DNA query routers to support dynamic `paper_dna_<slug>` collections with collection-isolated indexing and cross-collection hybrid queries.
- **Deliverable:** Dynamic ChromaDB collection lifecycle in `HomeLabAI/src/curator/sync_sprint_dna.py` and `router.py`.

#### 📋 Story 82.3: Target Objective & JD Matching Engine (Joint Deep Design & Execution)
- **Assigned Owner:** `[AGY:PRIMARY]` (Joint Interactive Design) $\rightarrow$ `[SWARM:LOCAL]` (Execution)
- **Objective:** Build objective matching endpoint `POST /paper/evaluate_objective` that extracts semantic requirement vectors from a Job Description / CFP and calculates alignment scores against local AST bullets and Wisdom DNA.
- **Deliverable:** Architecture specification in design studio + `HomeLabAI/src/v5/foyer/router.py` endpoint (`POST /paper/evaluate_objective`).

#### 📋 Story 82.4: Objective Curation & Anti-Embellishment UI in `writer.html`
- **Assigned Owner:** `[SWARM:LOCAL]`
- **Objective:** Add `[Target Objective / JD]` curation drawer and two-tier palette waterline in `writer.html` showing:
  - Input drawer for Job Description / Requirement Brief.
  - Interactive per-bullet relevance badges (e.g., `92% Match [KEEP]`, `34% Match [PRUNE]`).
  - Action controls: `[Auto-Prune Low Matches]`, `[Sort by Alignment]`, `[Accept / Dismiss]`.
  - Zero-latency client-side drag-and-drop across the Waterline.
- **Deliverable:** `Portfolio_Dev/field_notes/writer.html` + `Portfolio_Dev/field_notes/style.css`.

#### 📋 Story 82.5: Deterministic AST-to-LaTeX & Web Document Compiler
- **Status:** ✅ COMPLETE
- **Assigned Owner:** `[SWARM:LOCAL]` $\rightarrow$ `[AGY:PRIMARY]`
- **Objective:** Upgrade `build_writer.py` to compile AST documents to pristine LaTeX, PDF, and static HTML entirely from cached `bone_collections`, requiring zero live database connectivity.
- **Verification:** Verified `python3 Portfolio_Dev/field_notes/build_writer.py --compile-all` successfully generates clean `paper.tex`, `references.bib`, and `index.html` from `paper_jitc_intuition.json` with 40 resolved citations.
- **Deliverable:** `Portfolio_Dev/field_notes/build_writer.py` (commit `f4cab42`).

---

### 5. Architectural Guardrails & Invariant Laws
1. **Zero Generative Embellishment (PHL-031):** The synthesis engine must only rank, filter, and organize verbatim human text. It must never fabricate experience or hallucinate achievements.
2. **Deterministic Portability (BKM-055):** Document editing and compilation must never stall or fail due to offline environments or unreachable database ports.
3. **AST Strictness:** All imported documents must validate against `validate_paper_schema.py` before saving to disk.
