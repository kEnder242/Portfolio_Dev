# 🚀 SPRINT PLAN 96.0: Brain Information Gatekeeper, LoRA Host Isolation & DNA Forge Split-Diff Workbench

**Sprint ID:** `SPR_96_0`  
**Theme:** Strict Information-Gatekeeping & Multi-Tier JITC, LoRA Resource Hardening, DNA Forge 4-Tab Architecture (`Recommendations` Split-Diff), and The Closed Flywheel Feedback Loop (`LOOP-001`–`LOOP-003`, `FEAT-632`–`FEAT-636`)  
**Status:** ACTIVE  
**Parent Framework:** `[BKM-064]` (Tracked Conversational Ledger), `[BKM-049]` (Owner Tag Mandate), `[BKM-060]` (Federated DNA Taxonomy), `[BKM-015]` (Semantic Intent Routing), `[BKM-020]` (Intent Preservation)  
**Target Hardware Nodes:** z87-Linux (RTX 2080 Ti Local vLLM 3B Base), KENDER (RTX 4090 Deep Thought), ChromaDB Port 8001 (CLaRa-DNA)

## 📝 Operator Directives & Mid-Flight Guidance
- **BKM-049 Owner Tag Mandate**: Every sprint story MUST declare an Assigned Owner (`[SWARM:LOCAL]`, `[SWARM:CLOUD]`, or `[AGY:PRIMARY]`).
- **Strict Delegation Rule**: When a story is tagged `[SWARM:LOCAL]`, direct primary-agent code edits are strictly forbidden without prior failed execution attempts via `delegate.py --mode local` on Port 4097.
- **Tri-Loop Diagnostic Protocol**: Follow the 3-attempt local diagnostic retry loop, cloud escalation if local fails, and mandatory `OPENAGENT_HANDOVER_PLAYBOOK.md` audit before any AGY fix-repair or takeover.

---

## 🧭 Executive Summary & Architectural Roadmap

Sprint 96.0 formalizes the **Roundtable Flywheel** by transforming the local Brain node into an **Active Information Gatekeeper**, eliminating prompt pollution/hallucinations in Deep Thought, isolating nightly LoRA training resources to protect host stability, and delivering a dedicated **4th Tab (`Recommendations`)** in the DNA Forge for in-place split-diff reviews.

```mermaid
flowchart TD
    subgraph STAGE1 ["🛡️ Foundation & Host Hardening"]
        S96_1["Story 96.1: LoRA Systemd Cgroups & Host Memory Sentinels [LAB-103/107/110/111]"]
    end
    subgraph STAGE2 ["🧠 The Roundtable Flywheel & Information Gatekeeper"]
        S96_2["Story 96.2: Triage Decoupling & Target Domain Routing [FEAT-540/542]"]
        S96_3["Story 96.3: Brain Coherence Gate & Curator Synergy Annotations [FEAT-584/586/635]"]
        S96_4["Story 96.4: In-Flight Dynamic Scope Override 'Direct Flight' [FEAT-636]"]
        S96_5["Story 96.5: Flywheel Closure: Thumbs Up/Down & Loop DNA Collection [FEAT-632/633/634]"]
    end
    subgraph STAGE3 ["⚖️ DNA Forge Review Workbench"]
        S96_6["Story 96.6: DNA Forge 4-Tab Bar & In-Place Split-Diff Review Engine [FEAT-593/614]"]
    end
    subgraph STAGE4 ["🧹 Nightly Maintenance & Sprint Ingestion"]
        S96_7["Story 96.7: Automated Sprint DNA Nightly Ingestion [FEAT-557]"]
    end

    S96_1 --> S96_2 --> S96_3 --> S96_4 --> S96_5 --> S96_6 --> S96_7
```

---

## 🎭 Roles & Responsibilities in the Roundtable Flywheel

| Actor | Tier | Architectural Role | Core Mechanism |
| :--- | :--- | :--- | :--- |
| **Human** | External | Intent Provider & Evaluator | Prompts system; gives `👍/👎` feedback to close the loop (`FEAT-633`/`FEAT-634`). |
| **Triage** | 3B CPU/Local | Classification & Routing | Maps prompt to categorical vibe and `target_domains: List[str]` (`[]` for ZERO DNA). |
| **Pinky** | FastEmbed/Chroma | Collection & Candidate Retrieval | Gathers candidate DNA vectors from requested domains; avoids unrequested collections. |
| **Brain** | 3B Local | Information & Conversational Gatekeeper | Coherence pass: Drops ungrounded junk, forwards exact text, appends Curator Notes, trims stale turns. |
| **Deep Thought** | 70B / 4090 | Pure Distillation & Insight | Single IN $\to$ OUT reasoning engine; receives high-density curated facts with zero negative clutter. |
| **Pinky** | Evaluator | Dialogue Grader & Promoter | Evaluates turn coherence, proposes DNA additions, records telemetry for human up/down vote. |

---

## 📋 Sprint 96 Stories & 4-Anchor Specifications

### 🛡️ Story 96.1: LoRA Systemd Cgroups & Host Memory Sentinels
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Status:** **COMPLETED & CERTIFIED**
* **Context & Mechanism:** Enforce strict systemd cgroups and allocator parameters to guarantee nightly LoRA fine-tuning cannot trigger kernel thrashing or crash resident daemons.
* **Accomplished:**
  1. Updated [`[LAB-103]`](file:///home/jallred/Dev_Lab/Portfolio_Dev/FeatureTracker.md) with `field-notes-nightly.service` resource limits (`MemoryHigh=8.5G`, `MemoryMax=10.0G`, `MemorySwapMax=1.5G`, `CPUQuota=600%`).
  2. Updated [`[LAB-107]`](file:///home/jallred/Dev_Lab/Portfolio_Dev/FeatureTracker.md) with `PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True,max_split_size_mb:128"` and `dataloader_num_workers=0` (in-process fork protection).
  3. Registered **`[LAB-110]`** (Host RAM Pre-Flight Gate): `psutil.virtual_memory().available >= 3.0 GB` check before spawning `train_expert.py` subprocesses.
  4. Registered **`[LAB-111]`** (`SWAP_ARCHITECTURE_PLAYBOOK.md` tracking): Documented fast zram (`pri=100`) + swap-on-zvol deadlock prevention invariants.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `/etc/systemd/system/field-notes-nightly.service`, `HomeLabAI/src/infra/nightly_lora_training.py`, `Portfolio_Dev/FeatureTracker.md`.
  * **Anchor 2 (Verification Command):** `systemctl cat field-notes-nightly.service && /home/jallred/Dev_Lab/HomeLabAI/.venv/bin/python3 -c "import psutil; print(f'RAM Available: {psutil.virtual_memory().available / 1024**3:.2f} GB')"`
  * **Anchor 3 (Live Silicon Invariant):** Host available DRAM remains $> 3.0\text{ GB}$ during adapter switches; zero zombie CUDA context leaks across subprocess runs.
  * **Anchor 4 (DNA Links):** `[LAB-103]`, `[LAB-107]`, `[LAB-110]`, `[LAB-111]`, `[SCAR-035]`.

---

### 🧭 Story 96.2: Triage Decoupling & Target Domain Routing
* **Assigned Owner:** `[AGY:TAKEOVER]` (Tri-Loop Complete: Local Attempt 1-2 & Cloud Timeout)
* **Status:** **COMPLETED & CERTIFIED**
* **Root Cause & Architectural Flaw Discovered:**
  1. `vector_pre_triage.py` was unconditionally probing all 10 ChromaDB collections synchronously for *every* query *before* Triage even ran.
  2. Triage outputted only `vibe`, but never emitted or used `target_domains: List[str]` to constrain downstream retrieval. As a result, downstream nodes (Pinky/Brain) were either unconstrained or forced to consume arbitrary top-1 chunks that won an unconstrained 10-collection race.
* **Task Breakdown & Deliverables:**
  1. **Task 96.2.1:** Updated Triage schema in `cognitive_hub.py` to output `target_domains: List[str]` (`["BKM"]`, `["FEAT"]`, `["WIS"]`, `["RESUME"]`, or `[]` for ZERO DNA) evaluated against collection scope descriptors.
  2. **Task 96.2.2:** Updated `vector_pre_triage.py` (`probe_clara_dna_sync`) to accept `collections: Optional[List[str]]`. Immediate 0ms bypass for `collections=[]` returning `[ZERO_DNA]` semantic hint; filtered probes restrict vector search to requested collections.
  3. **Task 96.2.3:** Wired `target_domains` into `CognitiveHub` routing (`self.current_target_domains`).
  4. **Task 96.2.4:** Added unit tests in `test_vector_pre_triage.py` (`test_zero_dna_probe_bypass`, `test_filtered_collections_probe`). All 5/5 unit tests passed green.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `HomeLabAI/src/logic/vector_pre_triage.py`, `HomeLabAI/src/logic/cognitive_hub.py`, `HomeLabAI/src/tests/test_vector_pre_triage.py`.
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_vector_pre_triage.py -v` (5/5 PASSED, 1.77s).
  * **Anchor 3 (Live Silicon Invariant):** Zero-DNA turns complete in $< 15\text{ms}$ with 0 ChromaDB lookups; domain-targeted turns restrict vector search strictly to listed collections.
  * **Anchor 4 (DNA Links):** `[FEAT-540]`, `[FEAT-542]`, `[BKM-015]`, `[BKM-060]`. Commit: `87e185f`.

---

### 🧠 Story 96.3: Brain Coherence Gate & Curator Synergy Annotations
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Status:** **COMPLETED & CERTIFIED**
* **Context & Mechanism:** Brain acts as an Information Gatekeeper. It evaluates candidates retrieved by Pinky, drops irrelevant items without showing negative clutter to Deep Thought, forwards approved bedrock text verbatim (no lossy rewrites), and appends high-leverage `💡 Curator Note: [ID] connects with [ID] on ...` annotations. Trims obsolete prior dialogue turns to eliminate conversational drag.
* **Accomplished:**
  1. Updated `BRAIN_SYSTEM_PROMPT` in `brain_node.py` with Directive #8 (`[FEAT-635] Information Gatekeeper & Curator Synergy`).
  2. Updated `build_two_mice_stage_prompt` Stage 1 prompt builder in `cognitive_hub.py` with explicit Information Gatekeeper and Curator Note evaluation instructions.
  3. Created `test_brain_gatekeeper.py` unit test suite (3/3 tests passing, verified alongside `test_two_mice_handover.py` 16/16 tests green).
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `HomeLabAI/src/nodes/brain_node.py`, `HomeLabAI/src/logic/cognitive_hub.py`, `HomeLabAI/src/tests/test_brain_gatekeeper.py`.
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_brain_gatekeeper.py HomeLabAI/src/tests/test_two_mice_handover.py -v` (16/16 PASSED, 0.59s).
  * **Anchor 3 (Live Silicon Invariant):** Deep Thought prompt context contains strictly approved candidate items + curator notes; zero dropped candidates present in prompt; full transcript retains dropped IDs for telemetry.
  * **Anchor 4 (DNA Links):** `[FEAT-584]`, `[FEAT-586]`, `[FEAT-635]`, `[INS-036]`. Commit: `0d59142`.

---

### ✈️ Story 96.4: In-Flight Dynamic Retrieval Scope Override ("Direct Flight")
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Status:** **COMPLETED & CERTIFIED**
* **Context & Mechanism:** Register and implement **`[FEAT-636]`**. If Brain detects that Triage misclassified a turn (e.g., historical query when the user was referring to earlier conversational dialogue), Brain has the authority to directly override the retrieval scope in-flight and fetch `blackboard_ledger_dna` without triggering an expensive 2-3s recursive re-triage loop.
* **Accomplished:**
  1. Added `@mcp.tool() direct_flight_override` in `HomeLabAI/src/nodes/brain_node.py` calling `probe_clara_dna_sync`.
  2. Implemented greenfield test suite `HomeLabAI/src/tests/test_direct_flight_override.py` (2/2 PASSED in 0.25s).
  3. Dispatched and certified via Layer 2 Atlas on Node KENDER RTX 4090 and Layer 3 Junior on M5 Air (Commit `000c6e1`).
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files & Line Anchors):**
    - `HomeLabAI/src/nodes/brain_node.py` (`direct_flight_override` MCP tool)
    - `HomeLabAI/src/tests/test_direct_flight_override.py` (greenfield pytest suite)
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_direct_flight_override.py -v` (2/2 PASSED)
  * **Anchor 3 (Silicon Invariant):** In-flight scope adjustments complete within the Brain node turn in $< 35\text{ms}$ without invoking re-triage.
  * **Anchor 4 (DNA Links):** `[FEAT-636]`, `[FEAT-584]`, `[BKM-015]`.

---

### 🔄 Story 96.5: Flywheel Closure: Thumbs Up/Down Telemetry & Loop DNA Collection
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Status:** **COMPLETED & CERTIFIED**
* **Context & Mechanism:** Integrate frontend `👍 / 👎` rating buttons in the UI and wire to Foyer endpoint `POST /feedback`. Upvotes trigger Pinky coherence promotion into bedrock DNA (`FEAT-633`); downvotes generate negative foil shortcuts to suppress bad retrieval patterns (`FEAT-634`). Formalize `loop_dna` ChromaDB collection (`FEAT-632`).
* **Accomplished:**
  1. Registered `POST /feedback` and `POST /attendant/feedback` in `HomeLabAI/src/v5/foyer/router.py` appending to `foyer_feedback_ledger.jsonl`.
  2. Integrated `COLLECTION_LOOP = "loop_dna"` in `Portfolio_Dev/sync_chroma_dna.py` with `parse_feedback_ledger()`.
  3. Created `HomeLabAI/src/tests/test_foyer_feedback.py` unit test suite (2/2 PASSED).
  4. Updated `[FEAT-632]`, `[FEAT-633]`, `[FEAT-634]` to ACTIVE in `Portfolio_Dev/FeatureTracker.md`.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files & Line Anchors):**
    - `HomeLabAI/src/v5/foyer/router.py` (add `POST /feedback` endpoint handler appending to `foyer_feedback_ledger.jsonl`)
    - `Portfolio_Dev/sync_chroma_dna.py` (add `loop_dna` collection definition and sync logic)
    - `Portfolio_Dev/FeatureTracker.md` (register `[FEAT-632]`, `[FEAT-633]`, `[FEAT-634]`)
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_foyer_feedback.py -v` (2/2 PASSED)
  * **Anchor 3 (Silicon Invariant):** Feedback packet persists to `foyer_feedback_ledger.jsonl` in $< 10\text{ms}$.
  * **Anchor 4 (DNA Links):** `[FEAT-632]`, `[FEAT-633]`, `[FEAT-634]`, `[LOOP-001]`, `[LOOP-002]`, `[LOOP-003]`.

---

### ⚖️ Story 96.6: DNA Forge 4-Tab Bar & In-Place Split-Diff Review Engine
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Status:** **COMPLETED & CERTIFIED**
* **Context & Mechanism:** Upgrade DNA Forge to the 4-Tab architecture (`Drafting`, `Graph`, `Cards`, `Recommendations`). The `Recommendations` tab provides a full-width split-diff interface:
  - Left Pane: Original Bedrock DNA / Manuscript Text.
  - Right Pane: Editable Proposed Mutation Diff (Polish, New Links, Dupes, Drift, Proposed `AR-xxx`).
  - Action Bar: `[Accept Diff]`, `[Edit in Place]`, `[Reject / Dismiss]`.
* **Accomplished:**
  1. Updated `Portfolio_Dev/dna_forge/templates/dna_forge.html` with 4-tab bar switcher and `#tab-recommendations-view` split-diff container.
  2. Enhanced `Portfolio_Dev/dna_forge/js/dna_forge.js` with 4-tab switching router and action handlers (`btnAcceptDiff`, `btnEditDiff`, `btnRejectDiff`).
  3. Added split-diff grid layout styling in `Portfolio_Dev/dna_forge/css/dna_forge.css`.
  4. Verified build pipeline via `python3 Portfolio_Dev/dna_forge/dna_forge_build.py`.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files & Line Anchors):**
    - `Portfolio_Dev/dna_forge/templates/dna_forge.html` (tab bar navigation: `<button class="tab-btn" data-tab="recommendations">Recommendations</button>`)
    - `Portfolio_Dev/dna_forge/js/dna_forge.js` (render split-diff pane and action bar handlers)
    - `Portfolio_Dev/dna_forge/css/dna_forge.css` (split diff two-column grid layout styles)
  * **Anchor 2 (Verification Command):** `python3 Portfolio_Dev/dna_forge/dna_forge_build.py && test -f Portfolio_Dev/dna_forge/dna_forge.html` (PASSED)
  * **Anchor 3 (Silicon Invariant):** 4 tabs switch with 0ms client-side latency; in-place diff edits persist to `decisions.json` and ChromaDB on commit.
  * **Anchor 4 (DNA Links):** `[FEAT-593]`, `[FEAT-614]`, `[FEAT-582]`, `[FEAT-612]`.

---

### 🌙 Story 96.7: Automated Sprint DNA Nightly Ingestion
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Status:** **COMPLETED & CERTIFIED**
* **Context & Mechanism:** Implement [`[FEAT-557]`](file:///home/jallred/Dev_Lab/Portfolio_Dev/FeatureTracker.md) in `Portfolio_Dev/sync_chroma_dna.py` and `HomeLabAI/src/infra/nightly_forge.py` Step 8 to parse all active and archived `SPRINT_PLAN_*.md` files and populate the `sprint_dna` ChromaDB collection automatically during the 2:00 AM maintenance sweep.
* **Accomplished:**
  1. Implemented `sync_sprint_dna()` in `Portfolio_Dev/sync_chroma_dna.py` vectorizing active and archived sprint plans into `sprint_dna`.
  2. Added `--collection` argument filter in `sync_chroma_dna.py`.
  3. Updated `HomeLabAI/src/infra/nightly_forge.py` Step 8 `run_sprint_dna_sync()` to invoke `sync_chroma_dna.py --collection sprint_dna`.
  4. Verified via `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/python3 Portfolio_Dev/sync_chroma_dna.py --collection sprint_dna` (64 sprint plans indexed into ChromaDB Port 8001).
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files & Line Anchors):**
    - `Portfolio_Dev/sync_chroma_dna.py` (lines 140–200: `sync_sprint_dna(client)` function parsing `Portfolio_Dev/docs/sprints/active/*.md` and `Portfolio_Dev/docs/sprints/archive/*.md`)
    - `HomeLabAI/src/infra/nightly_forge.py` (lines 684–705: Step 8 invoking `sync_chroma_dna.py --collection sprint_dna`)
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/python3 Portfolio_Dev/sync_chroma_dna.py --collection sprint_dna` (64 sprint plans indexed)
  * **Anchor 3 (Silicon Invariant):** ChromaDB Port 8001 reports `sprint_dna` collection count matching total historical sprint plans.
  * **Anchor 4 (DNA Links):** `[FEAT-557]`, `[BKM-060]`.

---

## 📦 Backlog Ledger Updates & Allocations

| Item ID | Title & Scope | Connection / Parent FEAT | Target Phase |
| :--- | :--- | :--- | :--- |
| **`TODO-006`** | **ATS Boolean Scraper & Hiring Pipeline:** Multi-platform ATS lead extractor (Ashby, Greenhouse, Lever, Workday) with automated skill matching. | Connects to [`[FEAT-595]`](file:///home/jallred/Dev_Lab/Portfolio_Dev/FeatureTracker.md) (Resume AST Decomposer). | Phase 20 (Backlog) |
| **`TODO-007`** | **3-Revision Resume AST Decomposition Test:** Stress-test [`[FEAT-595]`](file:///home/jallred/Dev_Lab/Portfolio_Dev/FeatureTracker.md) round-trip fidelity across 3 resume revisions. | [`[FEAT-595]`](file:///home/jallred/Dev_Lab/Portfolio_Dev/FeatureTracker.md) | Phase 20 (Backlog) |
| **`TODO-008`** | **`writer.html` 'Manic Phases of an Agent' Evaluation:** Creative prose authoring trial on [`[FEAT-583]`](file:///home/jallred/Dev_Lab/Portfolio_Dev/FeatureTracker.md) / [`[FEAT-587]`](file:///home/jallred/Dev_Lab/Portfolio_Dev/FeatureTracker.md). | [`[FEAT-583]`](file:///home/jallred/Dev_Lab/Portfolio_Dev/FeatureTracker.md) | Phase 20 (Backlog) |
| **`FEAT-444`** | **Judicial Backpressure Ledger:** Clean up/archive — core handover feedback is dialed in via [`[BKM-049]`](file:///home/jallred/Dev_Lab/AGENTS.md) and [`OPENAGENT_HANDOVER_PLAYBOOK.md`](file:///home/jallred/Dev_Lab/OPENAGENT_HANDOVER_PLAYBOOK.md). | [`[FEAT-444]`](file:///home/jallred/Dev_Lab/Portfolio_Dev/FeatureTracker.md#L88) | Groomed / Archived |
| **`FEAT-606`** | **File-to-DB Dynamic Round-Trip Invariant Matrix:** Drop continuous polling loop; rely on event-driven Git pre-commit hooks and nightly verification. | [`[FEAT-606]`](file:///home/jallred/Dev_Lab/Portfolio_Dev/FeatureTracker.md) | Groomed / Event-Driven |

---

## 🔬 Swarm Retrospective: Local Execution, Output Token Limits & AGY Benchmark

### 1. Output Token Limits: Physical Constraint vs. Runaway Protection
* **Physical & Compute Mechanics:**
  - In autoregressive decoding, generating tokens is strictly sequential (memory-bandwidth bound at 25–35 t/s). Emitting 8,192 tokens takes 4–5 minutes of continuous GPU tensor-core saturation.
  - While modern context windows support 32k–131k *input tokens* in parallel prefill, the *generation output limit* (`max_tokens` / `num_predict`) is defaulted to 8,192 tokens in Ollama/OpenCode harnesses.
* **Runaway Reasoning Protection:**
  - Reasoning-distilled models (Qwen-3.8 / DeepSeek derivatives) can enter self-reinforcing debate loops in their `<think>` chains if given unlimited output space. 
  - An 8k ceiling guards against infinite `<think>` lockups and thermal throttling.
* **Architectural Conduction Alignment (`BKM-049`):**
  - Layer 2 Conductor (Atlas) is designed for high-leverage tactical decomposition (200–500 token bounded contracts), not authoring full implementations in internal thought blocks. When Atlas attempted to simulate the retired 4-stage cascade (Librarian/Momus), it generated 33,088 characters of thought and breached the ceiling.
  - Once streamlined to lean 2-tier conduction, Atlas emitted only 1,019 output tokens, operating comfortably within budget.

### 2. Quality Benchmark: Local Swarm vs. Frontier AGY
* **Surgical Code Implementation (BKM-043 Anchor 3 Compliance):**
  - When provided with explicit Anchor 3 verbatim code templates and test fixtures, **Local Swarm code quality is on par with AGY (95–98% structural fidelity)**. Junior (M5 Air) implemented the exact tool decorator, error handling, JSON serialization, and unit tests on the first try without syntax drift (Story 96.4 passed 2/2 tests in 0.25s).
* **Ambiguity Tolerance & Problem Solving:**
  - **AGY (Cloud Frontier):** Superior at resolving underspecified, multi-file architectural constraints from scratch, reading between lines, and self-recovering from complex external errors.
  - **Local Swarm (Atlas 27B + Junior 27B):** Lower ambiguity ceiling. Requires crisp 4-anchor contracts. If line numbers drift or anchors are missing, local models risk getting bogged down in repetitive file scans.
* **Latency & Wall-Clock Profile:**
  - **AGY:** Fast parallel generation (~100 t/s) with near-instant prefill.
  - **Local Swarm:** Story 96.4 completed in 718s (~11m wall-clock) across Node KENDER (RTX 4090) and Apple M5 Air (oMLX TurboQuant 4-bit KV).
* **Sovereignty & Economics:**
  - **Local Swarm:** 100% sovereign, zero external telemetry leakage, zero recurring cloud API spend.

