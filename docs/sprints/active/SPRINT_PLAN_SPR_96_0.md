# 🚀 SPRINT PLAN 96.0: Brain Information Gatekeeper, LoRA Host Isolation & DNA Forge Split-Diff Workbench

**Sprint ID:** `SPR_96_0`  
**Theme:** Strict Information-Gatekeeping & Multi-Tier JITC, LoRA Resource Hardening, DNA Forge 4-Tab Architecture (`Recommendations` Split-Diff), and The Closed Flywheel Feedback Loop (`LOOP-001`–`LOOP-003`, `FEAT-632`–`FEAT-636`)  
**Status:** ACTIVE  
**Parent Framework:** `[BKM-064]` (Tracked Conversational Ledger), `[BKM-049]` (Owner Tag Mandate), `[BKM-060]` (Federated DNA Taxonomy), `[BKM-015]` (Semantic Intent Routing), `[BKM-020]` (Intent Preservation)  
**Target Hardware Nodes:** z87-Linux (RTX 2080 Ti Local vLLM 3B Base), KENDER (RTX 4090 Deep Thought), ChromaDB Port 8001 (CLaRa-DNA)

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
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Status:** READY FOR DISPATCH
* **Context & Mechanism:** Brain acts as an Information Gatekeeper. It evaluates candidates retrieved by Pinky, drops irrelevant items without showing negative clutter to Deep Thought, forwards approved bedrock text verbatim (no lossy rewrites), and appends high-leverage `💡 Curator Note: [ID] connects with [ID] on ...` annotations. Trims obsolete prior dialogue turns to eliminate conversational drag.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `HomeLabAI/src/nodes/brain_node.py`, `HomeLabAI/src/logic/cognitive_hub.py`, `HomeLabAI/src/tests/test_brain_gatekeeper.py`.
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_brain_gatekeeper.py -v`
  * **Anchor 3 (Live Silicon Invariant):** Deep Thought prompt context contains strictly approved candidate items + curator notes; zero dropped candidates present in prompt; full transcript retains dropped IDs for telemetry.
  * **Anchor 4 (DNA Links):** `[FEAT-584]`, `[FEAT-586]`, `[FEAT-635]`, `[INS-036]`.

---

### ✈️ Story 96.4: In-Flight Dynamic Retrieval Scope Override ("Direct Flight")
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Status:** READY FOR DISPATCH
* **Context & Mechanism:** Register and implement **`[FEAT-636]`**. If Brain detects that Triage misclassified a turn (e.g., historical query when the user was referring to earlier conversational dialogue), Brain has the authority to directly override the retrieval scope in-flight and fetch `blackboard_ledger_dna` without triggering an expensive 2-3s recursive re-triage loop.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `HomeLabAI/src/nodes/brain_node.py`, `HomeLabAI/src/logic/cognitive_hub.py`.
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_direct_flight_override.py -v`
  * **Anchor 3 (Live Silicon Invariant):** In-flight scope adjustments complete within the Brain node turn in $< 35\text{ms}$ without invoking re-triage.
  * **Anchor 4 (DNA Links):** `[FEAT-636]`, `[FEAT-584]`, `[BKM-015]`.

---

### 🔄 Story 96.5: Flywheel Closure: Thumbs Up/Down Telemetry & Loop DNA Collection
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Status:** READY FOR DISPATCH
* **Context & Mechanism:** Integrate frontend `👍 / 👎` rating buttons in the UI and wire to Foyer endpoint `POST /feedback`. Upvotes trigger Pinky coherence promotion into bedrock DNA (`FEAT-633`); downvotes generate negative foil shortcuts to suppress bad retrieval patterns (`FEAT-634`). Formalize `loop_dna` ChromaDB collection (`FEAT-632`).
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `Portfolio_Dev/dna_forge/js/dna_forge.js`, `HomeLabAI/src/v5/foyer/router.py`, `Portfolio_Dev/FeatureTracker.md`.
  * **Anchor 2 (Verification Command):** `curl -X POST http://127.0.0.1:8765/feedback -H "Content-Type: application/json" -d '{"turn_id": "test", "rating": "UP", "notes": "Grounded response"}'`
  * **Anchor 3 (Live Silicon Invariant):** Feedback packet persists to `foyer_feedback_ledger.jsonl` and updates `loop_dna` collection on Port 8001.
  * **Anchor 4 (DNA Links):** `[FEAT-632]`, `[FEAT-633]`, `[FEAT-634]`, `[LOOP-001]`, `[LOOP-002]`, `[LOOP-003]`.

---

### ⚖️ Story 96.6: DNA Forge 4-Tab Bar & In-Place Split-Diff Review Engine
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Status:** READY FOR DISPATCH
* **Context & Mechanism:** Upgrade DNA Forge to the 4-Tab architecture (`Drafting`, `Graph`, `Cards`, `Recommendations`). The `Recommendations` tab provides a full-width split-diff interface:
  - Left Pane: Original Bedrock DNA / Manuscript Text.
  - Right Pane: Editable Proposed Mutation Diff (Polish, New Links, Dupes, Drift, Proposed `AR-xxx`).
  - Action Bar: `[Accept Diff]`, `[Edit in Place]`, `[Reject / Dismiss]`.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `Portfolio_Dev/dna_forge/templates/dna_forge.html`, `Portfolio_Dev/dna_forge/js/dna_forge.js`, `Portfolio_Dev/dna_forge/css/dna_forge.css`.
  * **Anchor 2 (Verification Command):** `python3 Portfolio_Dev/dna_forge/dna_forge_build.py && test -f Portfolio_Dev/dna_forge/dna_forge.html`
  * **Anchor 3 (Live Silicon Invariant):** 4 tabs switch with 0ms client-side latency; in-place diff edits persist to `decisions.json` and ChromaDB on commit.
  * **Anchor 4 (DNA Links):** `[FEAT-593]`, `[FEAT-614]`, `[FEAT-582]`, `[FEAT-612]`.

---

### 🌙 Story 96.7: Automated Sprint DNA Nightly Ingestion
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Status:** READY FOR DISPATCH
* **Context & Mechanism:** Implement [`[FEAT-557]`](file:///home/jallred/Dev_Lab/Portfolio_Dev/FeatureTracker.md) in `Portfolio_Dev/sync_chroma_dna.py` and `HomeLabAI/src/infra/nightly_forge.py` Step 8 to parse all active and archived `SPRINT_PLAN_*.md` files and populate the `sprint_dna` ChromaDB collection automatically during the 2:00 AM maintenance sweep.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `Portfolio_Dev/sync_chroma_dna.py`, `HomeLabAI/src/infra/nightly_forge.py`.
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/python3 Portfolio_Dev/sync_chroma_dna.py --collection sprint_dna`
  * **Anchor 3 (Live Silicon Invariant):** ChromaDB Port 8001 reports `sprint_dna` collection count matching total historical sprint plans.
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
