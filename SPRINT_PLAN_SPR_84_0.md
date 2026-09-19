# 📋 Sprint Plan: [SPR-84.0] Resume Ingestion, The Synthesis Lens & Writing Studio Evolution

> **Sprint Type:** Live Collaborative Sprint & Architectural Alignment  
> **Status:** IN PLANNING (Items 0–18 Full Itemized Consensus)  
> **Date:** 2026-09-18  
> **Assigned Lead:** AGY + Sovereign Operator (Pair Programming)  
> **Applicable Operational Laws:** BKM-004 (QQ Protocol), BKM-020 (Intent Preservation), BKM-024 (Live Validation), BKM-040 (Git Discipline), BKM-049 (Owner Tag Mandate), BKM-060 (Polymorphic DNA Schema)

---

## 🧭 Executive Summary & Invariant Goals

Sprint 84 establishes the end-to-end knowledge cycle between raw career documents, polymorphic DNA decomposition, automated rubric grading, and structured round-trip publication. It delivers two major feature additions:
1. **`[FEAT-595]` Round-Trip Resume AST Decomposer & Google Docs Rich Formatter:** Ingests unstructured and rich resumes into a structured JSON AST (`PAPER-RESUME_v1.json`), decomposes career achievements into polymorphic `RESUME-xxx` DNA cards (following the all-inclusive "Subtractive CV" superset model), preserves layout styling metadata (`style_resume_v1.json`), updates the canonical text baseline (`raw_notes/Jason Allred resume 2026.txt`), and renders single-column ATS layouts back to Google Docs/PDF.
2. **`[FEAT-594]` Synthesis Lens Crafting & Automated Paper Grading Engine:** Ingests external guidance (e.g. the Farah Sharghi Recruiter Playbook) or job descriptions, compiles them into structured JSON rubrics (`/paper/craft_lens`), grades documents chunk-by-chunk to attach actionable `review_flags` (`/paper/grade_paper`), and enables discrete revision branching within `writer.html`.
3. **Writing Studio Ergonomics:** Implements agentic Arxiv/CLaRa citation discovery on `[TODO: ...]` markers (`/paper/expand_citations`), canvas paragraph splitting/insertion micro-actions, and outliner Arxiv badge previews.

---

## 🗺️ Consensus Trace & Verification Checklist (Itemized 0–18)

| Point | Phase & Topic | Status | Detailed Architectural Resolution & Specification |
| :---: | :--- | :---: | :--- |
| **0** | **Sprint 83 Clean Slate** | ✅ CERTIFIED | All pending changes committed cleanly (`Portfolio_Dev` @ `a301e54`, `HomeLabAI` @ `261db9d`). 10/10 pytests passing. Clean working tree verified. |
| **1** | **Resume Source Verification** | ✅ AGREED | Confirmed Google Doc precursor: [`Copy of Jason Allred Resume - Sept2026u`](https://docs.google.com/document/d/16yE02f-r1MfUcN3o3mLGe9EDeDTHb6lEv1bUCHy1hoY/) (Doc ID: `16yE02f-r1MfUcN3o3mLGe9EDeDTHb6lEv1bUCHy1hoY`). Local baseline: [`raw_notes/Jason Allred resume 2025.txt`](file:///home/jallred/Dev_Lab/Portfolio_Dev/raw_notes/Jason%20Allred%20resume%202025.txt). |
| **2** | **Source Delta & Subtractive CV Model** | ✅ AGREED | Decompose resume into structured `RESUME-xxx` / `CV` superset cards. Master resume is treated as an all-inclusive CV superset; specific 1–2 page resumes are generated via subtractive focus lenses rather than ad-hoc rewrites. |
| **3** | **Baseline = JSON AST + Text Sync** | ✅ AGREED | Canonical baseline stored as structured JSON AST (`data/papers/PAPER-RESUME_v1.json`) matching snapshot schema for direct tree diffing, paired with updated text baseline `raw_notes/Jason Allred resume 2026.txt`. |
| **4** | **Layout Schema (`style_schema`) Preservation** | ✅ AGREED | Capture ATS single-column structure, section header hierarchy, contact bar, line margins, and bold lead-in power verbs in `data/papers/style_resume_v1.json` before stripping formatting for baseline text. |
| **5** | **Round-Trip Import/Export Engine (`FEAT-595`)** | ✅ AGREED | Registered `[FEAT-595]`. Import: `[Doc/Text -> decompose_resume.py -> JSON AST + style_schema + DNA]`. Export: `[JSON AST + citations + style_schema -> export_paper_to_gdoc.py -> Google Docs API]`. |
| **6** | **Nomenclature Realignment: Review Flags** | ✅ AGREED | Standardize legacy "dirty flags" to **"Review Flags"** (`node.review_flags = [...]`). UI actions: `[🚨 Review Flag]`, `[✨ Apply Suggestion]`, `[📦 Archive Flag]`. |
| **7** | **DNA Palette Domain Synchronization** | ✅ AGREED | Ensure `writer.html` dynamically loads and filters all 8 polymorphic domains (`PHL`, `WIS`, `FEAT`, `BKM`, `SPRINT`, `DISC`, `RDNA`, `ART`) plus new `RESUME` collections from `dna_manifest.json`. |
| **8** | **DNA Collection & Census Manifest Sync** | ✅ AGREED | Auto-sync `data/dna_manifest.json` and ChromaDB vector store when new `RESUME-xxx` cards are ingested during decomposition. |
| **9** | **The Synthesis Lens Flow** | ✅ AGREED | Equation: `Candidate Revision = [Baseline AST + Citations - Review Flags]`. Applying a lens generates a discrete new candidate revision. |
| **10.1**| **Paper Grading Engine** | ✅ AGREED | LLM chunk-by-chunk pass evaluating paragraphs against a compiled rubric, attaching structured `review_flags` (`node_id`, `rubric_rule_id`, `severity`, `rationale`, `replacement_proposal`). |
| **10.2**| **Lens Crafting (Rubric Compiler)** | ✅ AGREED | Converts raw advice text (e.g. Farah Sharghi doc) or pasted Job Descriptions into structured JSON rubrics (`data/lenses/<lens_id>.json`). |
| **11** | **Lens Studio External UX in `writer.html`** | ✅ AGREED | Add `[🔍 Lens Studio]` toolbar: `[Active Lens Selector]`, `[+ Craft Lens]` drawer (JD/Doc input), `[📝 Grade Paper]` action, and version switcher (`[Base v1]`, `[v2 - Graded]`). |
| **12** | **Internal File Snapshots & JSON Baseline** | ✅ AGREED | Baseline and revisions stored as discrete JSON AST files (`data/papers/PAPER-001_<rev_id>.json`) for direct JSON tree diffing. |
| **13** | **Discrete Versioning & Revision Lifecycle** | ✅ AGREED | Deterministic `apply = new revision file` architecture. Clean provenance, zero merge conflict risk. |
| **14** | **Farah Sharghi Recruiter Lens Test Anchor** | ✅ AUDITED | Verified Doc `1mF3jVLyJP4Xb_MrKjD0hoIzujht02vKLdie2HTsupcQ`: First 3 words power verb, "So What?" drill, 3-tier metric hierarchy, 3-sentence summary hook, HERO behavioral framework. |
| **15** | **Agentic Research & `[🧠 Expand / Discover]` Pass** | ✅ AGREED | Live hook on `[TODO: ...]` markers triggering multi-source search (Arxiv API + CLaRa RDNA + `research.html`), rendering inline candidate bones with 1-click text/citation attachment. |
| **16** | **Review Flag Triage & Decision Persistence** | ✅ AGREED | Persistent human decision tracking in `data/paper_decisions.json` so approved/archived suggestions are never re-flagged across grading passes. |
| **17** | **Canvas Structural Controls: Add / Split Paragraphs** | ✅ AGREED | Inline micro-actions in `writer.html`: `[+ Add Paragraph]` to insert sibling nodes and `[✂️ Split]` to divide a block at the cursor. |
| **18** | **Tree View Arxiv Link Surfacing & Badging** | ✅ AGREED | Display badge icons for attached Arxiv / Research links directly in the sidebar tree outliner with 1-click preview tooltips. |

---

## 🏛️ Phase-by-Phase Technical Specifications

### Phase 1: Resume Ingestion & The Subtractive CV Model (`FEAT-595`)

#### 1.1 Source Reconciliation & Modernization
* **Precursor Analysis:** The Google Doc (`Copy of Jason Allred Resume - Sept2026u`) introduces modern 2025–2026 achievements:
  * Federated multi-agent AI infrastructure and local SLM residency (vLLM / FastEmbed / ChromaDB).
  * Simics pre-silicon model integration for Diamond Rapids and Oak Stream architectures.
  * Power/thermal telemetry envelopes and autonomous closed-loop test execution.
  * Professional 3rd-person technical framing replacing older 1st-person phrasing.
* **Sync Strategy:** Synchronize `raw_notes/Jason Allred resume 2026.txt` with these modern achievements while retaining full technical depth.

#### 1.2 The Subtractive CV Superset & DNA Card Schema
Instead of creating brittle, fragmented resume files for every application, the master resume is maintained as an **all-inclusive CV superset**. Tailored 1–2 page resumes are generated through *subtractive filtering* under a job-specific lens:
```json
{
  "id": "RESUME-042",
  "domain": "RESUME",
  "title": "Federated AI Lab Architecture & Local SLM Triage",
  "summary": "Engineered hybrid dual-engine cognitive routing reducing TTFT to sub-200ms.",
  "content": "Architected federated multi-agent execution pipeline combining local vLLM (RTX 4070) with Apple Silicon Deep Thought node, achieving 180ms TTFT intent classification.",
  "tags": ["#ai_infrastructure", "#vllm", "#slm", "#hybrid_compute"],
  "explicit_links": ["FEAT-586", "WIS-041"],
  "metadata": {
    "role": "Lead Architect & AI Systems Engineer",
    "company": "Federated Dev Lab",
    "period": "2024 - 2026",
    "metrics": {
      "ttft_ms": 180,
      "latency_reduction_pct": 45
    }
  }
}
```

#### 1.3 Document Baseline & Snapshot AST Schema
Both the canonical baseline and all derived revisions share a unified JSON AST schema (`data/papers/PAPER-RESUME_v1.json`):
```json
{
  "paper_id": "PAPER-RESUME",
  "revision_id": "v1_baseline",
  "title": "Jason Allred - Technical Resume & CV",
  "author": "Jason Allred",
  "created_at": "2026-09-18T15:30:00Z",
  "style_schema_ref": "data/papers/style_resume_v1.json",
  "sections": [
    {
      "section_id": "sec_summary",
      "heading": "Professional Summary",
      "nodes": [
        {
          "node_id": "node_sum_1",
          "type": "paragraph",
          "text": "Principal Systems Architect and AI Infrastructure Engineer with 12+ years...",
          "citations": ["FEAT-586", "FEAT-592"],
          "review_flags": []
        }
      ]
    },
    {
      "section_id": "sec_experience",
      "heading": "Professional Experience",
      "roles": [
        {
          "company": "Intel Corporation",
          "title": "Senior Systems Validation & Architecture Engineer",
          "period": "2018 - 2024",
          "context_line": "Led post-silicon validation and manageability architecture across Xeon server platforms.",
          "bullets": [
            {
              "node_id": "node_intel_b1",
              "text": "Architected autonomous validation suites for Xeon server power telemetry...",
              "citations": ["WIS-012"],
              "review_flags": []
            }
          ]
        }
      ]
    }
  ]
}
```

#### 1.4 Layout Schema (`data/papers/style_resume_v1.json`)
```json
{
  "layout_type": "ATS_SINGLE_COLUMN",
  "margins_inch": { "top": 0.5, "bottom": 0.5, "left": 0.6, "right": 0.6 },
  "typography": {
    "font_family": "Calibri",
    "body_size_pt": 10.5,
    "header_size_pt": 13,
    "line_spacing": 1.15
  },
  "rules": {
    "bold_lead_in_words": 3,
    "max_bullets_recent": 6,
    "max_bullets_older": 3,
    "context_line_italic": true
  }
}
```

#### 1.5 Round-Trip Export Engine
* **`scripts/export_paper_to_gdoc.py`**:
  1. `docs.create`: Creates a blank Google Doc titled `Jason Allred Resume - <Revision_Name>`.
  2. `docs.writeText`: Emits full structured text stream.
  3. `docs.formatText`: Applies `style_resume_v1.json` formatting passes (bolding header ranges, contact bar formatting, bullet formatting, italicizing context lines, bolding power verbs).

---

### Phase 2: The Synthesis Lens & Paper Grading Engine (`FEAT-594`)

#### 2.1 The Synthesis Lens Mathematical Flow
$$\text{Revision}_{k+1} = \mathcal{G}\left(\text{Revision}_k, \mathcal{L}_{\text{rubric}}\right) = [\text{Nodes}_k \oplus \text{Citations} \ominus \text{Flags}_{\text{applied}}]$$
Applying a lens compiles a candidate revision where review flags are staged or auto-resolved.

#### 2.2 Lens Crafter (`/paper/craft_lens`)
* **Endpoint:** `POST /paper/craft_lens`
* **Input Payload:**
  ```json
  {
    "lens_id": "farah_sharghi_recruiter_v1",
    "source_type": "google_doc" | "raw_text",
    "content": "1mF3jVLyJP4Xb_MrKjD0hoIzujht02vKLdie2HTsupcQ"
  }
  ```
* **Output:** Compiled `data/lenses/farah_sharghi_recruiter_v1.json`.

#### 2.3 Paper Grading Engine (`/paper/grade_paper`)
* **Endpoint:** `POST /paper/grade_paper`
* **Input Payload:**
  ```json
  {
    "paper_id": "PAPER-RESUME",
    "revision_id": "v1_baseline",
    "lens_id": "farah_sharghi_recruiter_v1"
  }
  ```
* **Grading Output:** Attaches structured `review_flags` to nodes and creates candidate revision `data/papers/PAPER-RESUME_v2_sharghi.json`.

#### 2.4 Farah Sharghi Recruiter Rubric Schema (`data/lenses/farah_sharghi_recruiter_v1.json`)
```json
{
  "lens_id": "farah_sharghi_recruiter_v1",
  "title": "Farah Sharghi Ex-Google Recruiter Lens",
  "source_doc_id": "1mF3jVLyJP4Xb_MrKjD0hoIzujht02vKLdie2HTsupcQ",
  "rubric_rules": [
    {
      "rule_id": "FIRST_3_WORDS_POWER_VERB",
      "target": "bullet_opening",
      "severity": "CRITICAL",
      "description": "Start every bullet with a high-impact power verb signaling ownership (Directed, Architected, Spearheaded, Standardized). Avoid passive openings like 'Responsible for', 'Worked on', or 'Helped'."
    },
    {
      "rule_id": "SO_WHAT_METRIC_DRILL",
      "target": "bullet_body",
      "severity": "HIGH",
      "description": "Every bullet must pass the 'So What?' test by tying the task to operational or business impact (Financial/Growth, Velocity/Efficiency, or Scale/Complexity metrics)."
    },
    {
      "rule_id": "CONTEXT_LINE_PURVIEW",
      "target": "role_header",
      "severity": "MEDIUM",
      "description": "Include a single 1-line context statement beneath title/company defining company scale, team mission, and direct purview before bullets appear."
    },
    {
      "rule_id": "THREE_SENTENCE_SUMMARY_HOOK",
      "target": "summary_section",
      "severity": "HIGH",
      "description": "Summary must be strictly 3 sentences: Sentence 1 (Identity & Purview), Sentence 2 (Differentiator / Superpower), Sentence 3 (Macro Career Proof Point)."
    },
    {
      "rule_id": "BULLET_DENSITY_CAP",
      "target": "section_structure",
      "severity": "MEDIUM",
      "description": "Recent roles: 4-6 bullets max. Roles 3-6 years ago: 3-4 bullets max. Older roles (>10 years): 1-2 bullets or collapsed into Early Career list without bullets."
    },
    {
      "rule_id": "HERO_FRAMEWORK_ALIGNMENT",
      "target": "story_narrative",
      "severity": "INFO",
      "description": "Structure technical achievements along HERO lines: Hook (15%), Execution (40%), Results (30%), Ownership & Learnings (15%)."
    }
  ]
}
```

---

### Phase 3: Writing Studio Augmentation & Agentic Research

#### 3.1 Agentic Research Pass: `[🧠 Expand / Discover]`
```
[ Canvas Paragraph Block in writer.html ]
"TODO: List of supporting documents and arxive links - Prior art on speculative multi-agent routing."
                      ┌──────────────────────────────────────┐
                      │  [🧠 Expand / Discover Citations]    │  <-- Click Trigger
                      └──────────────────────────────────────┘
                                         │
                                         ▼
                           REST POST /paper/expand_citations
       ┌─────────────────────────────────┼─────────────────────────────────┐
       ▼                                 ▼                                 ▼
 [Arxiv Search API]            [CLaRa ChromaDB RDNA]             [Local Research Hub]
 Top 3 preprint papers          Semantic match against            `data/research_entries.json`
 on speculative relay           Lab protocols & invariants        Verified internal papers
       │                                 │                                 │
       └─────────────────────────────────┼─────────────────────────────────┘
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ 📚 Candidate Citations Drawer (Inline in writer.html)                                       │
│                                                                                             │
│ 1. [arXiv:2401.12345] "Speculative Spec Execution in Dual-Engine LLM Topologies"            │
│    Relevance: 94% | Authors: DeepMind Labs | Link: https://arxiv.org/abs/2401.12345         │
│    [+ Attach Bone]  [✨ Synthesize & Replace TODO]  [Dismiss]                               │
│                                                                                             │
│ 2. [RDNA-014] "Asymmetric Lead Time & EWMA Latency Jitter Protocol"                         │
│    Relevance: 89% | Collection: rdna | Tags: #triage #speculative                           │
│    [+ Attach Bone]  [✨ Synthesize & Replace TODO]  [Dismiss]                               │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 3.2 Review Flag Triage & Persistent Human Decision Log
When an author reviews flags in `writer.html`, human approvals and dismissals are recorded in `data/paper_decisions.json`:
```json
{
  "paper_id": "PAPER-RESUME",
  "decisions": {
    "node_intel_b1::FIRST_3_WORDS_POWER_VERB": {
      "action": "APPROVED",
      "applied_text": "Spearheaded autonomous validation suites...",
      "timestamp": "2026-09-18T15:40:00Z"
    },
    "node_intel_b2::BULLET_DENSITY_CAP": {
      "action": "ARCHIVED",
      "rationale": "Retained for deep architectural context",
      "timestamp": "2026-09-18T15:41:00Z"
    }
  }
}
```

---

## 🗺️ Sprint 84 Story Breakdown & Delegation Matrix

### Story 84.1: Canonical Resume Reconciliation & Back-Porting
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Dispatch Mode:** Local In-Session
* **Input Files:** `raw_notes/Jason Allred resume 2025.txt`, Google Doc `16yE02f-r1MfUcN3o3mLGe9EDeDTHb6lEv1bUCHy1hoY`.
* **Tasks:**
  1. Extract full text from Google Doc `16yE02f-r1MfUcN3o3mLGe9EDeDTHb6lEv1bUCHy1hoY`.
  2. Reconcile differences: Back-port 2025–2026 AI infrastructure, Simics pre-silicon model achievements, and 3rd-person technical framing.
  3. Write updated canonical text file: `raw_notes/Jason Allred resume 2026.txt`.
* **Verification (`BKM-024`):** Confirm file exists and matches latest achievements.

### Story 84.2: Resume AST Decomposer & DNA Extractor (`FEAT-595`)
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Dispatch Mode:** Local Swarm (`delegate.py` on port 4097)
* **Target Script:** `scripts/decompose_resume.py`
* **Tasks:**
  1. Parse `raw_notes/Jason Allred resume 2026.txt` into structured `data/papers/PAPER-RESUME_v1.json`.
  2. Extract distinct career achievements into `RESUME-001` ... `RESUME-030` polymorphic DNA cards.
  3. Generate ATS layout companion file `data/papers/style_resume_v1.json`.
  4. Ingest new cards into `data/dna_manifest.json` and ChromaDB `resume` collection.
* **Verification (`BKM-024`):** Validate AST JSON syntax and confirm ChromaDB query returns top resume cards.

### Story 84.3: Round-Trip Google Docs Rich Formatter & Exporter (`FEAT-595`)
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Dispatch Mode:** Local In-Session
* **Target Script:** `scripts/export_paper_to_gdoc.py`
* **Tasks:**
  1. Implement two-stage export using Google Docs API (`docs.create` + `docs.writeText` + `docs.formatText`).
  2. Apply `style_resume_v1.json` rules: single-column margins, bold power-verb lead-ins, italicized context lines, and ATS clean headers.
  3. Export `PAPER-RESUME_v1.json` to live Google Doc and log Doc ID/URL.
* **Verification (`BKM-024`):** Verify Google Doc creation and formatting via MCP API.

### Story 84.4: Lens Crafter: Rubric Compiler Engine (`FEAT-594`)
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Dispatch Mode:** Local Swarm (`delegate.py` on port 4097)
* **Assigned Agent Seat:** `DEEP_THOUGHT` (M5_AIR) or `THE_BRAIN` (Kender); fast fallback `champion_reasoner` / `fast_worker` swarm alias.
* **Target Files:** `HomeLabAI/src/foyer/paper_service.py`, `data/lenses/`
* **Tasks:**
  1. Implement `POST /paper/craft_lens` endpoint in Foyer.
  2. Ingest raw advice text or Job Description $\rightarrow$ prompt analytical agent seat to extract structured `rubric_rules` JSON array.
  3. Compile and save test anchor `data/lenses/farah_sharghi_recruiter_v1.json`.
* **Verification (`BKM-024`):** Unit test `/paper/craft_lens` against Farah Sharghi doc and verify schema compliance.

### Story 84.5: Paper Grading Engine & Review Flag Generator (`FEAT-594`)
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Dispatch Mode:** Local Swarm (`delegate.py` on port 4097)
* **Assigned Agent Seat:** `PINKY` / `LOCAL_VLLM` (Localhost) or `DEEP_THOUGHT` (M5_AIR).
* **Target Files:** `HomeLabAI/src/foyer/paper_service.py`
* **Tasks:**
  1. Implement `POST /paper/grade_paper` endpoint.
  2. Iterate chunk-by-chunk through paper nodes and evaluate each paragraph/bullet against active rubric rules.
  3. Attach `review_flags` (`node_id`, `rubric_rule_id`, `severity`, `rationale`, `replacement_proposal`).
  4. Write staged candidate revision `data/papers/PAPER-RESUME_v2_sharghi.json`.
* **Verification (`BKM-024`):** Verify grading pass generates flags on passive verbs and missing metrics.

### Story 84.6: `writer.html` Lens Studio UX & Discrete Revision Controller
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Dispatch Mode:** Local Swarm (`delegate.py` on port 4097)
* **Target File:** `Portfolio_Dev/field_notes/writer.html`
* **Tasks:**
  1. Add `[🔍 Lens Studio]` toolbar and drawer.
  2. Add active lens selector dropdown and `[+ Craft Lens]` modal (JD paste / Doc input).
  3. Add `[📝 Grade Paper]` action button triggering `/paper/grade_paper`.
  4. Implement revision version switcher dropdown (`[Base v1]`, `[v2 - Graded by Farah Sharghi]`).
* **Verification (`BKM-024`):** UI test in browser; switch between revisions seamlessly.

### Story 84.7: Review Flags & Proposal Triage Realignment
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Dispatch Mode:** Local Swarm (`delegate.py` on port 4097)
* **Target Files:** `Portfolio_Dev/field_notes/writer.html`, `data/paper_decisions.json`
* **Tasks:**
  1. Update UI cards to display `[🚨 Review Flag (N)]` with red highlight styling.
  2. Add 1-click `[✨ Apply Suggestion]` (updates node text and marks flag `RESOLVED`).
  3. Add 1-click `[📦 Archive Flag]` (marks flag `ARCHIVED` and hides it).
  4. Persist decisions to `data/paper_decisions.json`.
* **Verification (`BKM-024`):** Verify approved suggestions update node text and decisions persist across page reloads.

### Story 84.8: Agentic Arxiv & Research Citation Expansion Engine
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Dispatch Mode:** Local Swarm (`delegate.py` on port 4097)
* **Assigned Agent Seat:** `PINKY` / `LOCAL_VLLM` (query distillation) $\rightarrow$ `THE_BRAIN` / `DEEP_THOUGHT` (multi-paper synthesis).
* **Target Files:** `HomeLabAI/src/foyer/paper_service.py`, `Portfolio_Dev/field_notes/writer.html`
* **Tasks:**
  1. Implement `POST /paper/expand_citations` endpoint in Foyer.
  2. Parse `[TODO: ...]` topic $\rightarrow$ query Arxiv API + CLaRa RDNA + `research_entries.json`.
  3. Build inline candidate citations drawer in `writer.html`.
  4. Implement `[+ Attach Bone]` and `[✨ Synthesize & Replace TODO]` actions.
* **Verification (`BKM-024`):** Test on Section 2 TODO marker; verify Arxiv results returned and attached.

### Story 84.9: Canvas Micro-Actions: Add & Split Paragraph Controls
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Dispatch Mode:** Local Swarm (`delegate.py` on port 4097)
* **Target File:** `Portfolio_Dev/field_notes/writer.html`
* **Tasks:**
  1. Add subtle hover control `[+ Add Paragraph]` between paragraph blocks.
  2. Add `[✂️ Split]` micro-action button allowing authors to split a paragraph at the cursor into two sibling nodes.
  3. Maintain AST tree integrity and node ID sequence.
* **Verification (`BKM-024`):** Test paragraph insertion and splitting in `writer.html`.

### Story 84.10: Tree Outliner Arxiv Badging & Citation Link Surfacing
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Dispatch Mode:** Local Swarm (`delegate.py` on port 4097)
* **Target File:** `Portfolio_Dev/field_notes/writer.html`
* **Tasks:**
  1. Inspect node citations in sidebar tree outliner.
  2. Render Arxiv badge pills (`[arXiv:2401.12345]`) and DNA badges (`[WIS-012]`) next to section nodes.
  3. Enable 1-click external link opening and hover preview tooltips.
* **Verification (`BKM-024`):** Verify badges appear in sidebar tree and links resolve correctly.

### 🔮 Sprint 85+ Long-Horizon Backlog & Ideographic DNA Vector Space

### 1. `[FEAT-596]` The DNA Forge 2D Connections Web (Neural Synapse View)
* **Goal:** Implement an interactive SVG/D3 force-directed knowledge graph in `dna_forge.html`.
* **Behavior:** Selecting any DNA card highlights its 1st-degree `explicit_links` and renders subtle dashed lines to top-3 semantic neighbors (via ChromaDB cosine distance). Allows the operator to click-traverse from an operational BKM $\rightarrow$ underlying Philosophy $\rightarrow$ related Feature $\rightarrow$ resume bullet point.

### 2. Multi-Tier Recommendation System (`PROSE`, `REFINEMENT`, `CONNECTION`)
* **Goal:** Formalize Review Flags into 3 distinct recommendation classes in `writer.html` / `paper_service.py`:
  1. `[✍️ Prose Recommendation]`: Power verbs, passive-to-active transformations, eye-fatigue fixes.
  2. `[📊 Refinement Recommendation]`: Metric injections, "So What?" operational impact, subtractive cuts.
  3. `[🔗 Connection Recommendation]`: Auto-suggesting related DNA cards (`[WIS-012]`) and arXiv preprint bones.

### 3. Voice Vector Space & Dynamic Register Refactoring Engine
* **Goal:** A meta-language for rapid paper and resume refactoring. Decouple semantic meaning (DNA noun/verb cores) from stylistic voice vectors ($\vec{v}_{\text{style}} = [\text{Voice}, \text{Tense}, \text{Register}, \text{Density}]$).
* **Interactive Demo:** Rapid voice toggle in `writer.html` allowing an author to switch a document between *Scientific Prose*, *Casual Tech Essay*, *Executive Brief*, and *ATS Recruiter Bullets* with zero loss of underlying semantic citations.

### 4. Canonical Definition: DNA = Domain-Named Artifacts
* **Codification:** Formally define DNA across `PHL-034` and `BKM-060` as **Domain-Named Artifacts** (encapsulating our 8 discrete polymorphic domains: `PHL`, `WIS`, `FEAT`, `BKM`, `SPRINT`, `DISC`, `RDNA`, `ART`, `RESUME`).

---

## 🧬 Feature & DNA Registry Entries (Pre-Registered)

### `[FEAT-594]` Synthesis Lens Crafting & Automated Paper Grading Engine
* **Sprint:** SPR-84.0
* **Status:** IN IMPLEMENTATION
* **Code:** `HomeLabAI/src/foyer/paper_service.py`, `Portfolio_Dev/field_notes/writer.html`, `data/lenses/`
* **Logic:** Ingests unstructured guidance or Job Descriptions via `/paper/craft_lens` and compiles structured JSON rubrics (`rubric_rules: [...]`). Executes chunk-by-chunk LLM evaluation via `/paper/grade_paper` against active paper ASTs, attaching actionable `review_flags` with concrete replacement proposals. Spawns staged candidate revision forks (`PAPER-001_<rev_id>.json`) viewable in the `writer.html` version dropdown.
* **Rationale:** Bridges high-level editorial and recruiting rubrics with surgical paragraph-level writing, enabling automated tailoring for specific job requisitions.
* **Mechanism:** Foyer REST API, FastEmbed vector scoring, discrete JSON revision snapshots, `data/paper_decisions.json`.

### `[FEAT-595]` Round-Trip Resume AST Decomposer & Google Docs Rich Formatter
* **Sprint:** SPR-84.0
* **Status:** IN IMPLEMENTATION
* **Code:** `Portfolio_Dev/scripts/decompose_resume.py`, `Portfolio_Dev/scripts/export_paper_to_gdoc.py`
* **Logic:** Decomposes resumes into structured JSON AST (`PAPER-RESUME_v1.json`) and polymorphic `RESUME-xxx` DNA cards (implementing the Subtractive CV model). Extracts ATS layout metadata into `style_resume_v1.json`. Re-exports structured papers back to Google Docs via a two-stage `docs.create` + `docs.formatText` formatting engine that enforces ATS single-column margins, bold lead-in power verbs, and clean section headers.
* **Rationale:** Unifies career knowledge management into the federated DNA architecture, allowing one master CV superset to generate tailored Google Docs/PDFs on demand.
* **Mechanism:** Python AST parser, Google Workspace MCP API, CLaRa ChromaDB resume collection.
