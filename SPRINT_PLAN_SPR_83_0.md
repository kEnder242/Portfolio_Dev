# 🗺️ SPRINT PLAN: SPR-83.0
## Technical Deep-Dive & Strategic Architecture: Two-Tier Hybrid DNA Palette, Decoupled Document AST & Pedigree LoRA Curation

> **Status:** PROPOSED / ARCHITECTURAL BLUEPRINT  
> **Session Anchor:** 2026-09-15 11:18 PDT  
> **Primary References:** [[BKM-024]], [[BKM-049]], [[FEAT-160]], [[FEAT-204]], [[FEAT-246]], [[FEAT-581]], [[FEAT-582]], [[FEAT-585]], [[FEAT-588]]  

---

### 1. Architectural Deep Dive & Strategic Foundation

#### 1.1 Direct ChromaDB Backend vs. Decoupled Paper-Cached Lists

| Dimension | Direct ChromaDB Backend (`:8001` Live Query) | Decoupled AST-Cached Lists (Paper `.json`) |
| :--- | :--- | :--- |
| **Execution Path** | UI makes REST/WebSocket query on every section expand or click. | UI loads pre-computed DNA ID arrays directly from the paper's JSON AST. |
| **Latency & Feel** | 50–300ms vector search latency; potential UI flicker on navigation. | **Instant (0ms)** client-side hydration; butter-smooth UI transitions. |
| **Offline Portability** | Requires `chromadb` daemon & Python foyer running to view or edit. | **100% self-contained & portable**; works fully offline in browser or standalone CLI. |
| **Compilation** | `build_writer.py` / LaTeX compiler needs live DB connection to resolve citations. | Deterministic LaTeX/HTML builds directly from the static AST file. |
| **Version History** | Dynamic results can drift over time as ChromaDB updates or re-indexes. | **Immutable snapshots in Git**; paper preserves exact curated context at commit time. |

> **Strategic Architecture Decision:** Decoupling is the primary standard. Direct ChromaDB queries represent an explicit **Discovery action**, while day-to-day rendering, editing, and compilation read from **cached DNA ID lists embedded directly within each document's JSON AST**.

---

#### 1.2 Multi-Tier Hierarchical Caching (Root, Section, Paragraph)

Each AST tier maintains its own curated **"Bone Collection"** (Above Water / Active Citations) and **"Candidate Pool"** (Below Water / Discovered Suggestions):

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

* **Root Tier (Paper Scope):** Captures high-level themes, master archetypes (e.g., *Systems Validation*, *AI Telemetry*), and paper-wide citations.
* **Section Tier:** Captures domain-specific anchors relevant to that particular job chapter or paper section.
* **Paragraph / Bullet Tier:** Holds specific active evidence chips (`citations[]`) and local replacement suggestions (`_candidate_pool[]`).

---

#### 1.3 The Tri-Phase Document Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│ 1. DISCOVER (ChromaDB Vector Lookup)                        │
│    • Queries collections: PHL, WIS, FEAT, DISC, Paper-DNA  │
│    • Deposits discovered IDs into tier `_candidate_pool[]`   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. CURATE (Interactive Waterline & Objective Curation)      │
│    • User / Objective Engine moves IDs "Above Water"        │
│    • Promoted IDs stored in `bone_collection[]`/`citations[]│
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

### 2. Sprint 83.0 Story Breakdown & Delegation Matrix

#### 📋 Story 83.1: Two-Tier Decoupled Document AST Schema & Multi-Tier Caching
- **Assigned Owner:** `[SWARM:LOCAL]`
- **Objective:** Upgrade `paper.json` AST schema and validation engine to support explicit `bone_collection[]` (Above Water) and `_candidate_pool[]` (Below Water) arrays at the Document, Section, and Paragraph/Bullet levels.
- **Sub-tasks:**
  1. Update `validate_paper_schema.py` to enforce multi-tier bone collection and candidate pool keys.
  2. Implement AST migration utility `migrate_paper_v2.py` for backward compatibility with existing papers.
  3. Ensure `handle_paper_save` in `HomeLabAI/src/v5/foyer/router.py` preserves candidate pools and citation arrays without stripping.
- **Deliverable:** `Portfolio_Dev/field_notes/schemas/paper_ast_v2.json` + `Portfolio_Dev/scripts/validate_paper_schema.py`.

#### 📋 Story 83.2: Target Objective & JD Matching Engine (Joint Deep Design & Execution)
- **Assigned Owner:** `[AGY:PRIMARY]` (Joint Interactive Design) $\rightarrow$ `[SWARM:LOCAL]` (Execution)
- **Objective:** Build objective matching endpoint `POST /paper/evaluate_objective` that extracts semantic requirement vectors from a Job Description / CFP and calculates alignment scores against local AST bullets and Wisdom DNA.
- **Sub-tasks:**
  1. *Interactive Design Gate [AGY:PRIMARY]:* Align on requirement vector schema, bullet scoring formulas (TF-IDF + dense cosine blend), and Auto-Prune decision thresholds.
  2. Implement backend endpoint `POST /paper/evaluate_objective` in `HomeLabAI/src/v5/foyer/router.py`.
  3. Generate per-bullet relevance metadata (`score: 0.0-1.0`, `recommendation: KEEP | PRUNE | ENRICH`, `suggested_bones: [...]`).
- **Deliverable:** `HomeLabAI/src/v5/foyer/router.py` + unit tests in `HomeLabAI/src/tests/test_objective_evaluator.py`.

#### 📋 Story 83.3: Interactive Waterline & Objective Curation UI in `writer.html`
- **Assigned Owner:** `[SWARM:LOCAL]`
- **Objective:** Overhaul Writer Studio (`writer.html`) to render the two-tier palette, interactive waterline, and objective curation drawer.
- **Sub-tasks:**
  1. Implement collapsible `[Target Objective / JD]` sidebar drawer with input textarea and evaluation trigger.
  2. Render visual match badges on each bullet (e.g., `94% Match [KEEP]`, `32% Match [PRUNE]`).
  3. Add instant batch actions: `[Auto-Prune Low Matches]`, `[Sort by Alignment]`, `[Reset]`.
  4. Implement drag-and-drop / click-to-promote interaction across the Waterline separating `bone_collection` from `_candidate_pool`.
- **Deliverable:** `Portfolio_Dev/field_notes/writer.html` + `Portfolio_Dev/field_notes/style.css`.

#### 📋 Story 83.4: Tri-Curriculum LoRA Dataset Curation & Forge Blending Engine
- **Assigned Owner:** `[SWARM:LOCAL]`
- **Objective:** Rectify the nightly forge dataset pipeline by replacing the single-ledger ingestion with a balanced, multi-curriculum blend across the 3 historical foundations + curated ledger gems.
- **Sub-tasks:**
  1. Update `HomeLabAI/src/forge/build_lora_datasets.py` to produce a unified `master_forge_curriculum.jsonl` with fixed ratios:
     - **40% User Voice / Writing Style** (`cli_voice_training.jsonl` from multi-year Gemini CLI logs).
     - **35% Engineering Pedigree & BKMs** (`lab_history_training.jsonl` / `bkm_master_manifest.jsonl`).
     - **15% Situational Awareness & Vibe Schema** (`lab_sentinel_training.jsonl`).
     - **10% Curated Rank 4 Gems** (deduplicated, high-coherence round-table pearls, filtered from raw ledger).
  2. Update `HomeLabAI/src/infra/nightly_forge.py` to point `DATASET_PATH` to `master_forge_curriculum.jsonl` instead of raw `journal_ledger.jsonl`.
  3. Add pre-flight dataset schema and coherence verification before invoking Unsloth training.
- **Deliverable:** `HomeLabAI/src/forge/build_lora_datasets.py` + `HomeLabAI/src/infra/nightly_forge.py`.

#### 📋 Story 83.5: Deterministic AST-to-LaTeX & Web Document Compiler
- **Assigned Owner:** `[SWARM:LOCAL]`
- **Objective:** Upgrade `build_writer.py` to compile AST documents to pristine LaTeX, PDF, and static HTML entirely from cached `bone_collections`, requiring zero live database connectivity.
- **Sub-tasks:**
  1. Implement LaTeX template renderer for resumes, research papers, and technical briefs.
  2. Resolve all `\cite{...}` keys strictly from AST cached metadata.
  3. Verify offline compilation pass (`python3 build_writer.py --compile-all`).
- **Deliverable:** `Portfolio_Dev/field_notes/build_writer.py`.

---

### 3. Delegation & Architectural Guardrails

1. **BKM-049 Tri-Loop Protocol:**
   - Stories 83.1, 83.3, 83.4, 83.5 are assigned to `[SWARM:LOCAL]`. Local diagnostic retries (max 3) must be exhausted before cloud escalation.
   - Story 83.2 requires an explicit `[AGY:PRIMARY]` joint interactive design session before code execution.
2. **Zero Generative Embellishment:** Document synthesis operates strictly on combinatorial AST selection, ranking, and citation anchoring.
3. **Dataset Quality Over Recency:** LoRA training must anchor to curated foundations (Voice + History + Vibe) rather than drifting on raw recent chatter.
