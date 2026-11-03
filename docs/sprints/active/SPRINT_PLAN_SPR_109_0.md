# 📑 SPRINT PLAN 109.0: Always-Live Multi-Node Projection Studio & 4-Tier Epistemic Memory Architecture

**Sprint ID:** `SPR_109_0`  
**Theme:** Full Restoration of the 4-Tier Epistemic Memory Architecture (`FEAT-683`), Density-Weighted Archive Queue Scheduling (`FEAT-682`), Non-Destructive Navigational Companion Mapping (`.map.json`), Automated Ripgrep Ground Truth Hydration (`FEAT-451`), Pre-Triage Focal Gravitational Steering (`FEAT-540`), Excision of `disentangle_chronology()` Guessing Fallbacks, and Always-Live Multi-Node Projection Studio (`FEAT-059` / `FEAT-673`).  
**Status:** 🟢 **COMPLETE (VERIFIED)**  
**Parent Frameworks:**
- [`BKM-086`]: The Paved-Path Sprint Protocol (AFK / Sovereign Execution)
- [`BKM-088`]: The Empirical Pipeline Step Judgment Protocol (Micro-Harness & Co-Pilot Loop)
- [`BKM-089`]: Resilient Ingestion & Multi-Format Temporal Normalization Protocol
- [`BKM-077`]: Conversational Anchor Tracking Protocol (ANCHOR_TRACK & 1:1 Swim Lanes)
- [`BKM-020`]: High-Fidelity Sprint Documentation & Pre-Lock Forensic Gap Audit
- [`BKM-015`]: Semantic Anchor Protocol (Anti-Hardcoding & Regex Governance)
- [`BKM-082`]: 5-Sprint Historical Lookback & Mistake Prevention
- [`INS-047`]: Live is King, History is Queen (Anti-Amnesia Sovereign Dyad)
- [`FEAT-059`]: Live Projection Studio Architecture (Always-Live, Zero-Stub Paradigm)
- [`FEAT-673`]: Multi-Node Real-Time Matrix Comparison View (Cross-Engine Lenses)
- [`FEAT-682`]: Density-Weighted Archive Queue Scheduler
- [`FEAT-683`]: 4-Tier Epistemic Memory Architecture (Bedrock, Focals, Gems, Raw Notes)
- [`FEAT-451`]: Autonomous Grep-Gated RiR Search Pivot / Ground Truth Hydration
- [`FEAT-540`]: CLaRa-DNA Fast Vector Similarity Pre-Triage Probe

**Target Silicon Nodes:**
- `z87-Linux`: Local RTX 2080 Ti (Llama-3.2-3B-AWQ on port 8088 / vLLM runtime / Pinky Reflex)
- `Node KENDER`: RTX 4090 Ollama Conductor :11434 (Qwen2.5-32B / Deep Thought Deliberation)
- `Node Brain`: macOS M5 Air MLX :8002 via Headroom (Ternary-Bonsai-2-27B / Semantic Mapper & Atlas)
- `ChromaDB`: Port 8001 (`focal_dna`, `long_term_wisdom`, `wisdom_dna`, `behavioral_dna`, `career_ledger`)
- `lab-attendant.service`: Port 8765 (Foyer WebSocket Gateway)

---

## 🛑 Pre-Flight Checklist Gate (`BKM-082 §GATE` / `BKM-086 §1.1`)
- [x] **1. 5-Sprint Lookback**: Reviewed SPR-104 through SPR-108 for traps, sentinels, and regression vectors (`BKM-082 §2.1` in §0.1).
- [x] **2. Mistakes-Avoided Ledger**: Enumerated 6 concrete historical mistakes avoided (`BKM-082 §2.4` in §0.2).
- [x] **3. Oracle Review**: Adversarial architecture review completed via `delegate.py --oracle` (`BKM-007`/`BKM-080`). Formally documented with 7 mitigations embedded in [`ORACLE_REVIEW_SPRINT_109.md`](file:///home/jallred/Portfolio_Dev/docs/sprints/active/ORACLE_REVIEW_SPRINT_109.md).
- [x] **4. Delegation Justification**: Swarm allocation evaluated `LOCAL`/`CLOUD` first per `Invariant 7` & `BKM-049`; documented rationale in §6 below.
- [x] **5. Risk Assessment**: `LOCAL` tasks evaluated for promotion to `CLOUD` (Stories 109.9 & 109.12 promoted to `CLOUD` due to multi-node/cross-file integration blast radius).

---

## 🛡️ Pre-Flight Mistakes Avoided Ledger (`BKM-081` / `BKM-082`)

### 0.1 5-Sprint Historical Lookback Summary (`BKM-082 §2.1`)
- **SPR-104**: Continuous Multiplier Token Pacing (`FEAT-523`). *Lesson:* Pacing must scale naturally with interest; forcing arbitrary floor tokens leads to hallucinated filler.
- **SPR-105**: Decoupled Tri-Anchor Alignment, RAG-First Ripgrep Expansion (`FEAT-451` / Story 105.6), and Natural Turn Completion (`FEAT-658`, `FEAT-659`). *Lesson:* Passing explicit `curated_anchors` to ripgrep prevents conversational stop-word flooding.
- **SPR-106**: Two-Dimensional Gem Epistemics (`refinement_level` vs `impact_level`). *Lesson:* Separating substance from topology eliminates paragraph distortion. Introduced `disentangle_chronology()` which, while well-intentioned, introduced hazardous `2024` and `06-01` guessing defaults.
- **SPR-107**: Active Staging Synthesis & Backward-Compatible Shims (`FEAT-665`). *Lesson:* Preserving legacy shims (e.g. symlinks) prevents immediate client amnesia.
- **SPR-108**: Cognitive Hydraulics, Node-Anchored Console Routing (`FEAT-058`), and Entailment Auditing. *Lesson:* Console routing must be anchored to physical hardware nodes, and ambiguous terminology ("CRITIQUE") must be eliminated.

### 0.2 Pre-Flight Mistakes Avoided for Sprint 109 (`BKM-082 §2.4`)
1. **The Whole-File `jit_read` Memory Trap**: Avoided attempting to read entire 15,000-line raw notes files through LLM prompts during interactive turns. Tier 3 Gems remain the high-density distilled signal; Ripgrep (`FEAT-451`) provides the bounded, surgical line-range ground truth.
2. **The In-Place Source Mutation Trap**: Avoided editing raw notes files where bracketed headers (`[DRA: VLV Visa debug tool]`) or log timestamps appear. Source text is preserved 100% pristine by using external **Navigational Companion Files (`.map.json`)**.
3. **The `FEAT-102` Collision**: Avoided recycling `FEAT-102` (which belongs to Nuclear Cache Busting from Sprint 10). Properly registered `FEAT-682` and `FEAT-683` at the top of the feature sequence.
4. **The Arbitrary 300-Token Bedrock Choke**: Avoided rigidly constraining Tier 1 Career Bedrock to 300 tokens, which artificially stripped verified platform achievements. Replaced with the **Completeness of Era Bedrock Standard**.
5. **The Regex Date Branching Explosion**: Avoided complicating scanner regexes across multiple scripts to handle `M-D-YY` notation. Replaced with a deterministic, single-pass date normalization pass on the files themselves.
6. **The `notes_2005` State Ghost Trap**: Avoided renaming `notes_2005.txt` without migrating `chunk_state.json`, which would have left orphaned ghost keys. Starting fresh by purging malformed keys ensures zero stale chunk contamination.

---

## ⚓ Conversational Anchor Tracking Ledger (`BKM-077`)

| Anchor ID | Origin Turn / Swim Lane | Topic Description | Target Milestone | State |
| :--- | :--- | :--- | :--- | :---: |
| `ANCHOR-01` | Topic 1 / 1.1 | `notes_2005_SSPD.txt` Fresh Start, State Purge & Symlink | Story 109.1 | 🟢 `STAGED` |
| `ANCHOR-02` | Topic 2 | Single-Pass Date Normalization (`2006`, `2007`, `2015` tail) | Story 109.2 | 🟢 `STAGED` |
| `ANCHOR-03` | Topic 2 / 5.1 | Navigational Companion Files (`.map.json`) & 3-Tier Pipeline | Story 109.3 | 🟢 `STAGED` |
| `ANCHOR-04` | Topic 4 | Restoration of 4-Tier Epistemic Memory Architecture (`FEAT-683`) | Story 109.4 | 🟢 `STAGED` |
| `ANCHOR-05` | Topic 4.1 | Ingestion of Annual Reviews into `focal_mesh.json` & `focal_dna` | Story 109.5 | 🟢 `STAGED` |
| `ANCHOR-06` | Topic 4.2 | Wiring `step_pre_triage` (`FEAT-540`) to `focal_dna` | Story 109.6 | 🟢 `STAGED` |
| `ANCHOR-07` | Topic 5.1.2 | `context_envelope` Scoped Exclusively to Gap Files | Story 109.7 | 🟢 `STAGED` |
| `ANCHOR-08` | Topic 5.2 | Density-Weighted Archive Queue Scheduler (`FEAT-682`) | Story 109.8 | 🟢 `STAGED` |
| `ANCHOR-09` | Topic 5.3 | Ground Truth Ripgrep Bridge (`FEAT-451`) & Path Verification | Story 109.9 | 🟢 `STAGED` |
| `ANCHOR-10` | Topic 5.4 | Excision of `disentangle_chronology()` in favor of Spatial Anchors | Story 109.10 | 🟢 `STAGED` |
| `ANCHOR-11` | Topic 5.5 | `FOCAL_DRAFT` Prompt Tagging & AGY Verification Probe | Story 109.11 | 🟢 `STAGED` |
| `ANCHOR-12` | Topic 0 | Always-Live Multi-Node Projection Studio (`FEAT-059` / `FEAT-673`) | Story 109.12 | 🟢 `STAGED` |

---

## 📖 Sprint Narrative: The Architectural Roll-Up

### 1. The Context & The Why
Across Sprints 47 through 54, the quest for sub-second conversational triage on local 3B weights led to the unintended flattening of the lab's knowledge architecture. The original vision of a **4-Tier Epistemic Memory Hierarchy** (Resume Bedrock $\to$ Strategic Focals $\to$ Technical Scars/Gems $\to$ Raw Ground Truth Notes) was crushed into a rigid <300 token prompt string (`career_compass.json`) and a flat vector search. Focals—the vital intermediate layer connecting daily engineering bugs to career deliverables—were reduced to an un-parsed 3 KB string slice in `scan_pinky.py`.

Simultaneously, our recent archaeological discovery of [`notes_2019_DPV.txt`](file:///home/jallred/knowledge_base/notes_2019_DPV.txt) and [`notes_2007_LAD.txt`](file:///home/jallred/knowledge_base/notes_2007_LAD.txt) closed the 2018–2019 transition gap and narrowed the pre-2012 void, but exposed acute limitations in our ingestion engines:
- Brittle slash-only date regexes completely blind the scanner to hyphenated entries (`7-23-07`, `1-18-12`).
- Sparse, tabular files (`notes_2005.txt`) get dumped into undifferentiated "Unknown" blobs.
- Refinement engines rely on post-hoc date guessing (`disentangle_chronology()`) that hallucinate arbitrary calendar days (`06-01` or `2024`).

### 2. The Core Solution
Sprint 109.0 executes a decisive, systemic overhaul:
1. **Restores `[FEAT-683]` (4-Tier Epistemic Memory)**: Tier 1 (Resume Bedrock), Tier 2 (`focal_mesh.json` / `focal_dna`), Tier 3 (Gems with line-range spatial anchors), and Tier 4 (Raw Notes on disk).
2. **Activates Pre-Triage Gravitational Steering (`[FEAT-540]`)**: Wires the sub-20ms vector probe in `step_pre_triage` to query `focal_dna`, seeding Pinky's triage with confirmed strategic milestones before HyDE synthesis.
3. **Non-Destructive Companion Navigation (`.map.json`)**: Preserves 100% of raw note text while providing external structural indices for tabular and sparsely dated gap files.
4. **Surgical Ripgrep Ground Truth (`[FEAT-451]`)**: Bridges curated technical tokens from Brain directly to physical disk lines, eliminating whole-file LLM context bloat.
5. **Always-Live Projection Studio (`[FEAT-059]` / `[FEAT-673]`)**: Purges stub modes and activates real-time side-by-side comparison across our physical heterogeneous silicon fleet.

---

## 🛠️ Phase 0: Pre-Execution Housekeeping

### Task 0.1: FeatureTracker Synchronization
- Register `[FEAT-682]` (Density-Weighted Archive Queue Scheduler) and `[FEAT-683]` (4-Tier Epistemic Memory Architecture) in `Portfolio_Dev/FeatureTracker.md`.
- Mark `[FEAT-410]` and `[FEAT-405]` as superseded by `[FEAT-683]`.

### Task 0.2: Knowledge Base Symlink Audit
- Ensure `knowledge_base/notes_2019_DPV.txt` and `knowledge_base/notes_2007_LAD.txt` are fully readable across `Portfolio_Dev/raw_notes/` and `Dev_Lab/HomeLabAI/`.

---

## 🗺️ Epic 1: Note Archaeology & Resilient Ingestion (`FEAT-682` / `FEAT-683`)

### 🧬 Story 109.1: `notes_2005_SSPD.txt` Fresh Start, State Purge & Symlink
- **Worker**: `[AGY:PRIMARY]`
- **Anchors**: `ANCHOR-01` / `BKM-089` / `FEAT-683`
- **Why It Broke & Root Cause**: `notes_2005.txt` had 90% of its content trapped in `notes_2005.txt::Unknown` because the slash parser found only 3 dates in 2,700 lines. The file was mis-tagged as `EPSD`. Attempting to preserve these 4 malformed chunks preserves low-quality data.
- **Mechanism**:
  1. Rename physical file: `mv /home/jallred/knowledge_base/notes_2005.txt /home/jallred/knowledge_base/notes_2005_SSPD.txt`.
  2. Create backward-compatible symlink: `ln -s notes_2005_SSPD.txt /home/jallred/knowledge_base/notes_2005.txt`.
  3. Purge malformed keys from `field_notes/data/chunk_state.json` (`notes_2005.txt::*`).
  4. Update `field_notes/data/file_manifest.json`: Set key `notes_2005_SSPD.txt`, tags to `["SSPD"]`, type `LOG`.
  5. Update `scan_pinky.py` `GAP_FILES` to cite `raw_notes/notes_2005_SSPD.txt`.
- **Literal Test Assertions & Verification**:
  ```bash
  python3 -c "
  import json, os
  assert os.path.exists('/home/jallred/knowledge_base/notes_2005_SSPD.txt')
  assert os.path.islink('/home/jallred/knowledge_base/notes_2005.txt')
  with open('/home/jallred/Portfolio_Dev/field_notes/data/file_manifest.json') as f:
      m = json.load(f)
      assert 'notes_2005_SSPD.txt' in m
      assert m['notes_2005_SSPD.txt']['tags'] == ['SSPD']
  with open('/home/jallred/Portfolio_Dev/field_notes/data/chunk_state.json') as f:
      c = json.load(f)
      assert not any(k.startswith('notes_2005.txt') for k in c)
  print('STORY 109.1 PASSED')
  "
  ```

### 🧬 Story 109.2: Single-Pass Date Normalization (`2006`, `2007`, `2015` Tail)
- **Worker**: `[AGY:PRIMARY]`
- **Anchors**: `ANCHOR-02` / `BKM-089`
- **Why It Broke & Root Cause**: `scan_queue.py` uses `^(\d{1,2})/(\d{1,2})/(\d{2,4})`. In 2006, 2007, and the 2012 tail of 2015, dates were written with hyphens (`7-23-07`, `1-18-12`), causing the scanner to drop 187+ journal entries into monolithic multi-month chunks.
- **Mechanism**:
  A deterministic normalization script parses line-initial `^(\d{1,2})-(\d{1,2})-(\d{2,4})$` and converts in-place to `M/D/YYYY`:
  - `notes_2006_EPSD.txt`: 151 entries normalized (`10-2-06` $\to$ `10/2/2006`).
  - `notes_2007_LAD.txt`: 36 entries normalized (`7-23-07` $\to$ `7/23/2007`).
  - `notes_2015_DSD.txt` (lines 18,000–26,313): 2012 dash entries normalized (`1-18-12` $\to$ `1/18/2012`).
- **Literal Test Assertions & Verification**:
  ```bash
  python3 -c "
  import re
  dash_re = re.compile(r'^\s*(\d{1,2})-(\d{1,2})-(\d{2,4})\b')
  for f in ['notes_2006_EPSD.txt', 'notes_2007_LAD.txt']:
      with open('/home/jallred/knowledge_base/' + f) as fp:
          lines = fp.readlines()
      assert not any(dash_re.match(l) for l in lines), f'Remaining unnormalized dash dates in {f}'
  print('STORY 109.2 PASSED')
  "
  ```

### 🧬 Story 109.3: Navigational Companion Files (`.map.json`) via 3-Tier Pipeline
- **Worker**: `[SWARM:LOCAL]` (`Node Brain` / M5 Air MLX) + `[AGY:PRIMARY]` (Judge)
- **Anchors**: `ANCHOR-03` / `BKM-015` / `BKM-088`
- **Why It Broke & Root Cause**: Tabular trackers (`notes_2005_SSPD.txt`) and tool traces in `notes_2015_DSD.txt` lack daily timestamps. Mutating original notes to inject dates violates documentation integrity.
- **Mechanism**:
  1. *Host Python Mechanical Slicer*: Slices `notes_2005_SSPD.txt` on 4+ newlines (`\n{4,}`) and ASCII dividers into candidate ranges `[line_start:line_end]`.
  2. *M5 Air Semantic Mapper*: Evaluates each slice to infer `section_title`, `platform` (e.g. `Harwich`), `implied_era` (`2005-Q1`), and `chunk_type` (`DEFECT_TRACKER`, `CVS_COMMIT`).
  3. *AGY Judge Probe*: Executes `probe_companion_map.py` to certify section boundaries and output `/home/jallred/knowledge_base/notes_2005_SSPD.map.json`.
- **Literal Test Assertions & Verification**:
  ```bash
  python3 -c "
  import json
  with open('/home/jallred/knowledge_base/notes_2005_SSPD.map.json') as f:
      data = json.load(f)
      assert 'sections' in data
      assert len(data['sections']) >= 90
      for s in data['sections']:
          assert 'line_start' in s and 'line_end' in s
          assert 'section_title' in s
          assert 'implied_era' in s
  print('STORY 109.3 PASSED')
  "
  ```

### 🧬 Story 109.7: Scoping `context_envelope` Exclusively to Gap Files
- **Worker**: `[AGY:PRIMARY]`
- **Anchors**: `ANCHOR-07` / `BKM-015`
- **Why It Broke & Root Cause**: Passing surrounding lines (`context_envelope`) to structured daily journals introduces bleed confusion (blending yesterday's issue with today's debug log). Gap files, however, require book-ended lines to resolve orphan tracker headers.
- **Mechanism**:
  In `field_notes/scan_queue.py` and `field_notes/refine_gem.py`:
  - Check `is_gap_file`: If True, attach `context_envelope = {"before": lines[s-5:s], "after": lines[e:e+5]}`.
  - If False, `context_envelope` is omitted.
  - The refinement prompt instructs: *"Use `[ENVELOPE_BEFORE]` only to resolve orphan headers or missing tracker IDs. Do NOT include envelope text in the core gem."*
- **Literal Test Assertions & Verification**:
  Verify via `test_context_envelope_scoping.py`: Gap files receive envelopes; standard files receive pure slices.

### 🧬 Story 109.8: Density-Weighted Archive Queue Scheduler (`FEAT-682`)
- **Worker**: `[AGY:PRIMARY]`
- **Anchors**: `ANCHOR-08` / `FEAT-682`
- **Why It Broke & Root Cause**: `scan_pinky.py` picked files via `random.shuffle(note_files)`. This caused heavily saturated files (`notes_2024_PIAV.txt` with 32,000 lines and hundreds of gems) to consume burn cycles while under-indexed files (`notes_2005_SSPD.txt`, `notes_2007_LAD.txt`) starved.
- **Mechanism**:
  Implement dynamic priority calculation in `field_notes/scan_queue.py`:
  $$\text{Priority} = \frac{\text{Total File Lines}}{\text{Indexed Gems in Archive} + 1}$$
  Sort the scan candidate queue descending by Priority before dispatching burn epochs.
- **Literal Test Assertions & Verification**:
  ```bash
  python3 -c "
  from field_notes.scan_queue import calculate_file_priorities
  p = calculate_file_priorities()
  assert p[0]['filename'] in ['notes_2005_SSPD.txt', 'notes_2007_LAD.txt', 'notes_2019_DPV.txt']
  print('STORY 109.8 PASSED')
  "
  ```

### 🧬 Story 109.10: Excision of `disentangle_chronology()` in Favor of Spatial Anchors
- **Worker**: `[AGY:PRIMARY]`
- **Anchors**: `ANCHOR-10` / `FEAT-683`
- **Why It Broke & Root Cause**: `disentangle_chronology()` attempted post-hoc date guessing on raw strings, hardcoding `doc_year = 2024` and hallucinating arbitrary dates (`06-01`). With companion maps and normalized dates, guessing is obsolete.
- **Mechanism**:
  1. Deprecate and remove `disentangle_chronology()` in `field_notes/refine_gem.py`.
  2. Require every gem candidate to receive its `spatial_anchor` (`line_start`, `line_end`) and `temporal_anchor` directly from chunk metadata or `.map.json`.
  3. If day precision is unavailable, store `precision: "QUARTER"` or `"ERA"` with zero artificial day padding.
- **Literal Test Assertions & Verification**:
  Run `pytest field_notes/tests/test_gem_refiner.py` confirming zero occurrences of fallback `06-01` or default `2024` dates on pre-2020 gems.

### 🧬 Story 109.11: `FOCAL_DRAFT` Prompt Tagging & AGY Verification Probe
- **Worker**: `[AGY:PRIMARY]`
- **Anchors**: `ANCHOR-11` / `BKM-015` / `BKM-088`
- **Why It Broke & Root Cause**: Engineers frequently draft performance self-assessments inside daily journals. Naive scanners extract these drafts as raw technical scars, creating circular RAG bloat. Hardcoding regexes like `(?:Focal):` violates `BKM-015`.
- **Mechanism**:
  1. Add semantic role instruction to `refine_gem.py`:
     *"If the chunk text represents a retrospective career summary, self-assessment, or focal draft, label its type as `FOCAL_DRAFT` and identify the corresponding Tier 2 milestone."*
  2. Build empirical probe `probe_focal_draft_detection.py` with an AGY judge asserting that draft entries in `notes_2018_PAE.txt` and `notes_2024_PIAV.txt` are tagged as `FOCAL_DRAFT`.
- **Literal Test Assertions & Verification**:
  `python3 field_notes/tests/probe_focal_draft_detection.py` returns score $\ge 0.90$.

---

## 🗺️ Epic 2: 4-Tier Epistemic Memory Architecture (`FEAT-683`)

### 🧬 Story 109.4: Formal Registration of `[FEAT-683]`
- **Worker**: `[AGY:PRIMARY]`
- **Anchors**: `ANCHOR-04` / `FEAT-683`
- **Why It Broke & Root Cause**: Historical multi-tier RAG (`FEAT-405`, `FEAT-410`, `FEAT-437`) was clobbered in Sprint 47 by a flat prompt string.
- **Mechanism**:
  Authoritatively document `[FEAT-683] 4-Tier Epistemic Memory Architecture` in `Portfolio_Dev/FeatureTracker.md` and `HomeLabAI/docs/Protocols.md`.
  - Tier 1: Resume & Career Bedrock (`Jason Allred resume 2026.txt` $\to$ `career_compass.json`).
  - Tier 2: Strategic Focals & Milestones (`focal_mesh.json` $\to$ ChromaDB `focal_dna`).
  - Tier 3: Technical Scars & Gems (`long_term_wisdom` with `spatial_anchor` line ranges).
  - Tier 4: Physical Raw Notes Ground Truth (`/home/jallred/knowledge_base/` on-demand via Ripgrep).
- **Literal Test Assertions & Verification**:
  Inspect `FeatureTracker.md` asserting presence of `[FEAT-683]` and deprecation pointers on `FEAT-405`/`FEAT-410`.

### 🧬 Story 109.5: Annual Reviews Ingestion into `focal_mesh.json` & `focal_dna`
- **Worker**: `[AGY:PRIMARY]`
- **Anchors**: `ANCHOR-05` / `FEAT-683`
- **Why It Broke & Root Cause**: 10 Annual Performance Review files (`2008.doc` through `2018.docx`) in `knowledge_base/` were never systematically parsed into a queryable layer.
- **Mechanism**:
  1. Author `field_notes/ingest_focals.py` using `docx2txt` / `antiword` / Python text extraction to parse each annual review.
  2. Extract: `focal_year`, `covered_period` (accounting for the 1-year lookback), `strategic_milestones`, `platforms`, and `impact_bullets`.
  3. Save consolidated JSON to `field_notes/data/focal_mesh.json`.
  4. Ingest into ChromaDB collection `focal_dna` (port 8001).
- **Literal Test Assertions & Verification**:
  ```bash
  /home/jallred/Dev_Lab/HomeLabAI/.venv/bin/python3 -c "
  import chromadb
  client = chromadb.HttpClient(host='localhost', port=8001)
  c = client.get_collection('focal_dna')
  assert c.count() >= 10, f'Expected >= 10 focal records, got {c.count()}'
  print('STORY 109.5 PASSED')
  "
  ```

### 🧬 Story 109.6: Wiring `step_pre_triage` (`FEAT-540`) to `focal_dna`
- **Worker**: `[AGY:PRIMARY]`
- **Anchors**: `ANCHOR-06` / `FEAT-540` / `FEAT-683`
- **Why It Broke & Root Cause**: `step_pre_triage` in `cognitive_hub.py` only probed agent DNA collections (`behavioral_dna`), missing the user's career context entirely.
- **Mechanism**:
  1. In `HomeLabAI/src/logic/cognitive_hub.py` (`step_pre_triage`), add `focal_dna` to the pre-triage probe target collections.
  2. When a user asks an architectural or historical question, `step_pre_triage` retrieves the parent strategic focal milestone in $<20\text{ms}$.
  3. The focal milestone is injected into `step_triage` as `vector_hint`, grounding Pinky's triage and HyDE query generation in verified career milestones.
- **Literal Test Assertions & Verification**:
  `pytest HomeLabAI/src/tests/test_pre_triage_focal.py` asserting that a query about "AEP Optane on Proton" returns the 2018 Proton SAT focal milestone as `vector_hint`.

### 🧬 Story 109.9: Ground Truth Ripgrep Bridge (`FEAT-451`) & Path Verification
- **Worker**: `[AGY:PRIMARY]`
- **Anchors**: `ANCHOR-09` / `FEAT-451`
- **Why It Broke & Root Cause**: `execute_grep_search_pivot()` in `archive_node.py` was treated as a desperate fallback when vector RAG failed, rather than an intentional Ground Truth Hydration Bridge.
- **Mechanism**:
  1. In `HomeLabAI/src/nodes/archive_node.py`, ensure `os.path.expanduser("~/knowledge_base")` is searched.
  2. Between Brain's filter step and Deep Thought's turn in `cognitive_hub.py`, automatically extract Brain's `curated_anchors` (`["Aurora", "0x610"]`).
  3. Execute `execute_grep_search_pivot(curated_anchors=curated_anchors, max_matches=5)`.
  4. Inject the raw matching lines into Deep Thought's prompt payload under `<ground_truth_exhaust>`.
- **Literal Test Assertions & Verification**:
  `pytest HomeLabAI/src/tests/test_ripgrep_hydration.py` passes with $<8\text{ms}$ execution latency.

---

## 🗺️ Epic 3: Always-Live Multi-Node Projection Studio (`FEAT-059` / `FEAT-673`)

### 🧬 Story 109.12: Live Engine Integration & Multi-Node Comparison Matrix
- **Worker**: `[AGY:PRIMARY]`
- **Anchors**: `ANCHOR-12` / `FEAT-059` / `FEAT-673`
- **Why It Broke & Root Cause**: The Projection Studio UI retained static mock/stub toggles, failing to deliver the "always-live" empirical testbed feel.
- **Mechanism**:
  1. Purge all static stub response paths in `Portfolio_Dev/field_notes/projection_studio.js` and server routes.
  2. Implement simultaneous dispatch of the same prompt/lens across the inference fleet:
     - `z87-Linux`: Local RTX 2080 Ti (vLLM 3B AWQ / Pinky Triage)
     - `Node KENDER`: RTX 4090 Ollama Conductor (Qwen2.5-32B / Deep Thought)
     - `Node Brain`: macOS M5 Air MLX (Ternary-Bonsai 27B / Atlas via Headroom)
  3. Render side-by-side comparative cards with live token-streaming, latency, and lens-alignment telemetry.
- **Literal Test Assertions & Verification**:
  Load Projection Studio in browser; verify live simultaneous completions stream from all reachable physical nodes without stub fallback.

---

## 📋 AFK Sprint Execution Protocol (`BKM-086`)

This sprint is certified for **immediate autonomous execution**:
1. **Phase 0**: Housekeeping and FeatureTracker updates.
2. **Batch 1 (Archaeology & Normalization)**: Execute Stories 109.1, 109.2, 109.8.
3. **Batch 2 (4-Tier Memory & Focals)**: Execute Stories 109.4, 109.5, 109.6.
4. **Batch 3 (Companion Maps & Ripgrep Bridge)**: Execute Stories 109.3, 109.7, 109.9, 109.10, 109.11.
5. **Batch 4 (Live Projection Studio)**: Execute Story 109.12.
6. **Sprint Certification**: Run full test battery and author `SPRINT_109_RETROSPECTIVE.md`.


---

## 📜 Sprint Append Ledger (Story 109.13: Multi-Year & Manifest Priority Bug Fixes)

### 🧬 Story 109.13: Multi-Year Span Aggregation & Manifest Gating in Scan Priority (`FEAT-682`)
* **Worker:** `[AGY:PRIMARY]`
* **Anchors:** `ANCHOR-08` / `FEAT-682` / `BKM-081`
* **Why It Broke & Root Cause**:
  1. *Multi-Year Single-Regex Flaw*: `calculate_file_priorities()` used `re.search(r"20\d{2}", filename)` to look up `gems_by_year`. For multi-year journals like `notes_2015_DSD.txt` (`year: "2011-2016"`), it only checked `gems_by_year["2015"]` (3 gems), completely ignoring the 27+ gems produced for 2011–2014.
  2. *Unfiltered Glob Hazard*: The scheduler globbed all `.txt` files in `knowledge_base/`, causing raw hardware trace dumps (e.g. `PECI_experiments_WW31.3_1.txt` with 83,254 lines) and prompt files (`prompt.txt`) to jump to Priority 83,254.0, drowning out real notes.
* **Mechanism**:
  1. Gated file discovery against `file_manifest.json`: included only files with `type in ("LOG", "META")` or matching `notes_*.txt` / `ras-*.txt`; excluded all `manual_review: true` entries.
  2. Multi-year span aggregation: parsed `year` ranges (e.g. `"2011-2016"`) in `manifest` and summed `gems_by_year` across all covered years (`sum(gems_by_year[y] for y in span_years)`).
* **Literal Test Assertions & Verification**:
  - `pytest field_notes/tests/test_scan_queue_priority.py` passed (2/2).
  - Live candidate queue verified: 100% pure engineering notes; `notes_2007_LAD.txt` (Priority 482.0), `notes_GIT.txt` (325.0), `notes_2016_MVE.txt` (307.0), `notes_2015_DSD.txt` (217.5), and `notes_2006_EPSD.txt` (197.2) now lead the queue. Zero raw hardware trace dumps.

---

### 🧬 Story 109.14: Evidence-Aware Semantic Deduplication & Environment Alignment (`FEAT-454` / `BUG-684`)
- **Worker**: `[AGY:PRIMARY]`
- **Status**: `PLANNED` (Scheduled for next implementation cycle)
- **Anchors**: `ANCHOR-08` / `FEAT-454` / `LOOP-004`
- **Why It Broke & Root Cause**:
  1. `2005_02.json` accumulated 5 redundant gems for a single raw log line because `nibble_v2.py:is_semantic_duplicate` uses character-by-character `SequenceMatcher > 0.85` strictly on `summary`, completely ignoring raw `evidence` quotes. LLM summary rephrasings scored 0.15–0.66, bypassing the filter.
  2. `gem_refinement_runner.py` invoked system `/usr/bin/python3` where `chromadb` and `sentence_transformers` are missing (they reside in `.venv`), causing `deduplicate_gems()` in `refine_gem.py` to silently abort without running semantic deduplication.
  3. `clean_duplicates.py` uses an exact compound string key `date|summary|evidence`, failing to collapse rephrased extractions of identical evidence.
- **Planned Mechanism**:
  1. **Evidence-Based Ingestion Gate**: Update `nibble_v2.py:is_semantic_duplicate()` to check normalized `evidence` string overlap (>75% token overlap or identical normalized evidence) on the same date/chunk, suppressing redundant facets.
  2. **Environment Alignment**: Configure `gem_refinement_runner.py` to explicitly execute `/home/jallred/Portfolio_Dev/.venv/bin/python3`, restoring live `chromadb` and `SentenceTransformer` vector deduplication.
  3. **Evidence-Cluster Consolidator**: Enhance `clean_duplicates.py` to identify multiple gems referencing the exact same raw evidence block on the same date/spatial anchor, consolidating them into the highest-impact single gem.
- **Literal Test Assertions & Verification**:
  - `pytest field_notes/tests/test_gem_deduplication.py` asserting redundant extractions from `2005_02.json` collapse from 5 to 1.

---

### 🧬 Story 109.15: Transition Scan Queue from Date Gates to Spatial Companion Map Offsets (`FEAT-683` / `ARCH-002`)
- **Worker**: `[AGY:PRIMARY]`
- **Status**: `COMPLETED`
- **Anchors**: `ANCHOR-03` / `ANCHOR-10` / `FEAT-683` / `BKM-089`
- **Why It Broke & Root Cause**:
  `scan_queue.py:parse_chunks()` used line-initial regex `^(\d{1,2}/\d{1,2}/\d{2,4})` to slice note files into date buckets. This caused two severe failures:
  1. Files with sparse dates (e.g. `notes_2005_SSPD.txt`) had 90%+ of their content trapped in `Unknown` or dropped.
  2. Single date lines surrounded by sparse context became tiny 1-line chunks (like February 2005), prompting LLMs to over-extract redundant facets from a single sentence.
- **Mechanism**:
  1. **Companion Map Slicing**: If `<filename>.map.json` exists in `knowledge_base/` or `Portfolio_Dev/raw_notes/`, slice chunks directly by spatial sections: `lines[section['line_start']:section['line_end']]`, assigning task bucket to `section.get('implied_era')` or section title.
  2. **Structural Paragraph Slicing (Unmapped Fallback)**: For files lacking a companion map, slice on paragraph breaks (`\n\n`) into cohesive spatial chunks of 2,500–3,500 characters, tracking chunk index and line boundaries.
  3. **Zero Date-Gating**: Completely remove the line-initial date regex as a chunk partitioner. Dates within chunks are extracted by the LLM as event properties, not used to slice the file.
- **Literal Test Assertions & Verification**:
  - `pytest field_notes/tests/test_spatial_scan_queue.py` verifying companion map sections are queued as discrete spatial tasks with line boundaries and zero regex date dependence.

---

### 🧬 Story 109.16: Canonical Temporal Lakehouse & Provenance-Decoupled Routing (`ARCH-003` / `BKM-060` / `FEAT-684`)
- **Worker**: `[AGY:PRIMARY]`
- **Status**: `READY` (Architecture double-check via Delegate Oracle)
- **Anchors**: `BKM-060` / `BKM-100` / `FEAT-683` / `ARCH-003`
- **Why It Broke & Root Cause (Whack-A-Mole Diagnosis)**:
  1. *Provenance-Coupled Storage*: `nibble_v2.py` sets the output filename directly from the ingestion task's chunk bucket: `clean_bucket_name = str(task["bucket"]).split("::")[0].replace("-", "_")` -> `DATA_DIR/{clean_bucket_name}.json`. Any event extracted from `notes_2015_DSD.txt` (task bucket `2015_05::SEC-1`)—even if explicitly dated `2013-05-12`—is saved into `2015_05.json`.
  2. *Fragmented Sub-Files & Blindspot Deduplication*: Legacy partitions (`2005_02.json`, `2015_05.json`, `2016_2019.json`, `2019_05.json`) caused cross-year contamination (e.g. `2023-02-20` sitting in `2015_05.json`). Deduplication only checked `same_date_events` inside the *current target sub-file*, leaving global duplicates invisible.
  3. *Prompting in a Temporal Vacuum*: LLMs prompted without document temporal context converted hostnames (`filt2023`) or bug IDs (`2204...`) into future dates, prompting fragile post-hoc regex clamping sentinels.
- **Architectural Design (The 4 Pillars)**:
  1. **Strict Decoupling of Provenance vs Temporal Home**: Provenance (`source_file`, `line_start`, `line_end`, `chunk_id`) is strictly gem metadata. Storage destination is a pure function of the event's validated date: `DATA_DIR / f"{event['date'][:4]}.json"`.
  2. **Unified Canonical Annual Store**: Deprecate fragmented sub-files (`YYYY_MM.json`, `YYYY_YYYY.json`) as write targets. The single authoritative storage layer is `data/{YYYY}.json`. Monthly/sub-views are strictly read-only projections.
  3. **Era Context Injection in Ingestion Prompt**: Pass the verified temporal envelope (`[TEMPORAL CONTEXT: Era YYYY-YYYY]`) from `file_manifest.json` into the extraction prompt to eliminate out-of-band date hallucinations at the source.
  4. **BKM-060 Global Re-Bucketing & Dedup Migration Pass**: Load all existing gems across fragmented files, route each gem to its genuine `data/{event_year}.json`, run global evidence/semantic deduplication, and purge cross-year contaminants.
- **Literal Test Assertions & Verification**:
  - `pytest field_notes/tests/test_temporal_lakehouse_routing.py` verifying:
    a) Extraction from a 2015 task with a 2013 event date routes strictly to `2013.json`.
    b) Global deduplication collapses identical evidence across legacy sub-file boundaries.
    c) Zero cross-year events exist in canonical `YYYY.json` stores.


