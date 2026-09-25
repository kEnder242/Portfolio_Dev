# Sprint Plan: [SPR-90.0] The Applied Writer & Living Metabolism

**Version:** 1.0 (Phase 90 Architectural Sprint)  
**Goal:** Deliver the end-to-end Applied Writer studio workflow, unify Lens Projections with the Review Panel, establish Living Metabolism pruning mechanisms, and execute the polymorphic `PHL` $\to$ `INS` (Inspirations/Insights) domain migration.  
**Assigned Lead:** `[AGY:PRIMARY]` with Local Swarm Task Delegation  

---

## 🗺️ Tracked Sprint Vectors & DNA Mapping (Items 0 – 12)

| # | Sprint Vector / Objective | DNA Action | Target ID | Description |
|---|---------------------------|------------|-----------|-------------|
| **0** | **Remote Origin & CORS Handshake** | **None (Verified)** | `FEAT-582` | Foyer `:8765` `/paper/*` CORS preflight and remote origin handshake verified operational on `notes.jason-lab.dev`. |
| **1** | **Creative Flow & Voice Projections** | **Update** | `FEAT-594` / `FEAT-595` | Integrate Voice Vector math (axes) and Lenses (prompt contexts) directly into Writer Studio. |
| **2** | **Direct Markdown AST/Regex Backflow** | **New Protocol** | `BKM-065` | Direct Markdown AST/regex editing for BKM/FEAT/INS updates; preserve `NO HUMAN DOCS` and treat Bone collections as transient drafting scratchpads. |
| **3** | **Paragraph Hover Mutation Triggers** | **New Feature** | `FEAT-615` | Anchor mutation review triggers in `.par-hover-controls` on paragraph right margins. |
| **4** | **Offline Multi-View Publishing & Drift** | **New Feature** | `FEAT-616` | Static airlock export to `papers.html` with pre-baked view toggles and automated cross-view consistency drift detection. |
| **5** | **Review Panel: Mutation & Dialogue** | **New Feature** | `FEAT-614` | Right-hand interactive review gutter for conversational phrasing refinement, nightly mutations, and AST diff reconciliation. |
| **6** | **Unified Projection Toolbar** | **New Feature** | `FEAT-617` | Merge Lens Studio and Voice Vectors into a unified header projection drawer. |
| **7** | **Tracked Conversational Ledger** | **New Protocol** | `BKM-064` | Formalize numbered list tracking protocol across all agent pair-programming interactions (cross-linked to `INS-016`). |
| **7.1** | **Primary-Key Deduplication Engine** | **Update** | `FEAT-582` | Enforce strict primary-key deduplication in DNA Forge compiler to eliminate duplicate cards. |
| **8** | **Tracked Editorial Dialogue** | **New Feature** | `FEAT-618` | In-editor margin critique and multi-turn wording refinement ledger in the Review Panel. |
| **9** | **Living Metabolism & Continuous Pruning** | **New Vibe** | `VIBE-008` | Establish the architectural philosophy that knowledge bases require active feedback pressure and semantic pruning to prevent entropy. |
| **10** | **Associative Mice & Intuition Round Tables** | **New Wisdom** | `WIS-011` | Formalize Mice as low-latency vector retrieval probes whose associations are vetted and bound via human-in-the-loop round tables. |
| **11** | **Feedback Loops as Complexity Engines** | **New Vibe** | `VIBE-009` | Umbrella philosophy modeling feedback loops as the fundamental driver of emergent system complexity. |
| **11.1**| **The Logistic Map Principle** | **New Inspiration** | `INS-036` | Iterative mathematical feedback generates infinite fractal depth from simple deterministic functions. |
| **12** | **Polymorphic Domain Migration (`PHL` $\to$ `INS`)** | **Protocol Update** | `BKM-060` | Canonicalize `INS` (Inspirations / Insights) as first-class domain prefix with zero-downtime `PHL` backward-compatibility aliasing. |

---

## 🔬 Story Breakdown, Delegation & Oracle Audit Matrix

### Story 90.1: Unified Projection Toolbar & Review Panel (`[FEAT-614]`, `[FEAT-617]`)
- **Assigned Owner:** `[SWARM:LOCAL]` (Dispatch via `delegate.py --port 4097 --model local-unified-base`)
- **Diagnostic Retry Budget:** 3 attempts (`BKM-049`) before cloud fallback
- **Tasks & Execution Vectors**:
  - `Task 90.1.1`: Build top `.projection-toolbar` in `Portfolio_Dev/field_notes/writer.html` with Lens selector (Staff Architect, Executive, Casual) and Voice Vector sliders (Formality, Density, Register).
  - `Task 90.1.2`: Implement `#reviewPanel` gutter with multi-turn chat history, diff visualization, and "Accept Mutation" button.
  - `Task 90.1.3`: Wire `.par-hover-controls` on each paragraph to open specific paragraph discussion in Review Panel.
- **Validation Command**: `HomeLabAI/.venv/bin/python3 Portfolio_Dev/field_notes/build_site.py --no-verify`

### Story 90.2: Direct AST/Regex Markdown Backflow (`[BKM-065]`)
- **Assigned Owner:** `[SWARM:LOCAL]` (Dispatch via `delegate.py --port 4097 --model local-unified-base`)
- **Diagnostic Retry Budget:** 3 attempts (`BKM-049`)
- **Tasks & Execution Vectors**:
  - `Task 90.2.1`: Implement `/dna/edit_source` endpoint in `HomeLabAI/src/v5/foyer/router.py`.
  - `Task 90.2.2`: Create AST regex parser replacing BKM definitions in `HomeLabAI/docs/Protocols.md` and Features in `Portfolio_Dev/FeatureTracker.md`.
  - `Task 90.2.3`: Trigger local git commit checkpoint upon successful source mutation.
- **Validation Command**: `curl -s -X POST http://127.0.0.1:8765/dna/edit_source -d '{"id":"BKM-060","field":"content","val":"..."}'`

### Story 90.3: Polymorphic `PHL` $\to$ `INS` Aliasing & Migration (`[BKM-060]`)
- **Assigned Owner:** `[AGY:PRIMARY]` (Architectural Core)
- **Tasks & Execution Vectors**:
  - `Task 90.3.1`: Update `BKM-060` in `HomeLabAI/docs/Protocols.md` establishing `INS` as the canonical domain with `PHL` backward-compatibility alias.
  - `Task 90.3.2`: Implement prefix normalization in `clara_dna_mcp_server.py`, `synapse_graph.js`, `dna_forge.js`, and `dna_forge_build.py`.
  - `Task 90.3.3`: Generate `Portfolio_Dev/dna/inspiration_data.json` and register `INS-036` (*The Logistic Map Principle*).
- **Validation Command**: `python3 -c "import urllib.request; assert 'Pearls' in urllib.request.urlopen('http://127.0.0.1:8001/protocol?id=INS-007').read().decode()"`

### Story 90.4: Offline Multi-View Paper Publishing (`[FEAT-616]`, `[VIBE-008]`)
- **Assigned Owner:** `[SWARM:LOCAL]` (Dispatch via `delegate.py --port 4097 --model local-unified-base`)
- **Diagnostic Retry Budget:** 3 attempts (`BKM-049`)
- **Tasks & Execution Vectors**:
  - `Task 90.4.1`: Create `Portfolio_Dev/scripts/publish_paper.py` taking manuscript JSON AST and exporting standalone offline HTML.
  - `Task 90.4.2`: Bake client-side view tabs (`Formal`, `Executive`, `Story`) into exported paper.
  - `Task 90.4.3`: Implement cross-view consistency drift heuristic flagging divergent paragraphs.
- **Validation Command**: `HomeLabAI/.venv/bin/python3 Portfolio_Dev/scripts/publish_paper.py --paper Portfolio_Dev/papers/paper_jitc_intuition.json --out www_deploy/papers.html`

### Story 90.5: Oracle Architectural Review & Code Audit
- **Assigned Owner:** `[ORACLE:REVIEW]` via `delegate.py --port 4097`
- **Scope**:
  1. Audit Applied Writer AST mutations against Invariant Operational Law #1 (`NO HUMAN DOCS`).
  2. Review `PHL` $\to$ `INS` polymorphic alias resolution for broken references or split-brain vector indexing.
  3. Certify that all offline publication outputs (`papers.html`) require 0 live runtime API dependencies.

---

## 🎯 Verification Criteria
- [ ] `INS-xxx` search and graph navigation functions identically for both `INS` and legacy `PHL` identifiers across all UI tools.
- [ ] Review Panel successfully displays streaming paragraph mutation recommendations from local vLLM.
- [ ] Editing BKM/FEAT from Forge directly mutates Markdown source files with 0 syntax drift.
- [ ] `papers.html` renders completely offline with instant client-side view switching.
- [ ] Oracle Audit certifies 100% compliance with `NO HUMAN DOCS` and `BKM-049`.
