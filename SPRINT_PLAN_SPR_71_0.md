# 🚀 SPRINT PLAN 71.0: Conversational Stability, Declarative Engine Seats & Semantic RAG Decoupling

**Sprint ID:** `SPR_71_0`  
**Theme:** Real-Time Dialogue Liveliness, Declarative Multi-Seat Resolution, Semantic Triage (BKM-015), and Zero-Noise RAG Floors  
**Status:** ACTIVE / IN PROGRESS  
**Parent Framework:** BKM-015 (Semantic Anchor Protocol), BKM-034 (Swarm Delegation), BKM-043 (4-Anchor Standard), BKM-048 (Fingertips Protocol)  
**Target Hardware Nodes:** z87-Linux (RTX 2080 Ti Local vLLM), KENDER (RTX 4090 Deep Thought / Atlas), M5 Air (Speculative Candidate)

---

## 🧭 Executive Summary & Core Engineering Directives

Sprint 71 converts the live co-pilot dialogue audit into ten structured, tracked work items. It eliminates hardcoded latency traps, restores strict BKM-015 compliance, decouples conversational tone from data retrieval, and hardens inter-node consensus.

### 🏛️ Execution Assignments
* **Strategic Direct (AGY):** Large refactors, architectural policy decoupling, and core engine orchestration.
* **Swarm Delegation (Atlas L2 + Junior L3):** Bounded, surgical implementation stories adhering to the 4-Anchor Standard (BKM-043) with line pointers and interface-first verification.

---

## 📋 Sprint 71 Stories, Sub-Tasks & Forensic Mapping

### ⏱️ Topic 1 & 1.1 / Story 7101: Config-Driven Declarative Engine Seats & 2x Timing Standard (`[FEAT-531]`)
* **Status:** `[VERIFIED 100% PASS ON LIVE SILICON]`
* **Assigned Execution Mode:** `[DIRECT: AGY]` (Architectural Refactor across Config + Core Logic)
* **Context & Root Cause:** M5 Air timed out because `_probe_m5_air_vocal` had a hardcoded 0.3s timeout while cold M5 Air took 0.83s. Deep Thought was hardcoded with a 10s cold-start window.
* **Consensus & Design:** 
  1. Rename $t_{\text{warm}} \rightarrow t_{\text{warmed}}$ to reflect post-warmup TTFT.
  2. Implement the **2x Rule**:
     - Probe Timeout: $t_{\text{probe}} = 2 \times t_{\text{cold}} \approx 1.7\text{s}$.
     - Speculative Race Head-Start: $t_{\text{headstart}} = 2 \times t_{\text{warmed}} \approx 180\text{ms}$.
  3. Refactor `infrastructure.json` to define declarative `seats` array (`M5_AIR`, `KENDER`, `LOCAL`). Replace bespoke probe functions with a single generic loop in `speculative_triage.py`.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):**
    * `HomeLabAI/config/infrastructure.json` (Declarative seats definition)
    * `HomeLabAI/src/logic/speculative_triage.py` (Generic seat iterator & 2x timing engine)
    * `HomeLabAI/src/tests/test_speculative_triage_seats.py` (Unit verification harness)
  * **Anchor 2 (Verification Command):**
    ```bash
    /home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest src/tests/test_speculative_triage_seats.py -v
    ```
* **Sub-Tasks:**
  - `[STAGE 1: INTERFACE_CONTRACT_STUB]` Define `SeatConfig` schema in `infrastructure.json` and declare `resolve_active_seat()`.
  - `[STAGE 2: TEST_HARNESS_CREATION]` Author `test_speculative_triage_seats.py` with mock 2x probe and race timings.
  - `[STAGE 3: CALLER_INTEGRATION_WIRING]` Replace `resolve_active_deep_thought_target()` in `speculative_triage.py` with generic seat iterator.
  - `[STAGE 4: FULL_SILICON_CONVERGENCE]` Validate against live M5 Air (:8000), KENDER (:11434), and Local (:8088).

---

### 📢 Topic 2 / Story 7102: Telemetry Console Broadcast Consolidation (`[FEAT-532]`)
* **Status:** `[PENDING IMPLEMENTATION]`
* **Assigned Execution Mode:** `[SWARM DELEGATION: ATLAS + JUNIOR]` (via `delegate.py`)
* **Context & Root Cause:** Triage double-printed to the console by emitting back-to-back `crosstalk` summary and raw `chat` JSON broadcasts.
* **Consensus & Design:** Consolidate into a single telemetry chat broadcast payload per turn.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):**
    * `HomeLabAI/src/logic/cognitive_hub.py` (Lines 1150–1175)
    * `HomeLabAI/src/tests/test_telemetry_broadcast_dedup.py`
  * **Anchor 2 (Verification Command):**
    ```bash
    /home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest src/tests/test_telemetry_broadcast_dedup.py -v
    ```
* **Sub-Tasks:**
  - `[STAGE 1]` Stub unified `_broadcast_triage_telemetry()` method.
  - `[STAGE 2]` Create mock test verifying exactly 1 broadcast packet emitted during triage completion.
  - `[STAGE 3]` Replace dual `broadcast` calls in `cognitive_hub.py`.
  - `[STAGE 4]` Live integration verify against Web Intercom stream.

---

### 🎭 Topic 3 / Story 7103: Semantic Triage Grounding & BKM-015 Restoration (`[FEAT-533]`)
* **Status:** `[VERIFIED 100% PASS ON LIVE SILICON]`
* **Assigned Execution Mode:** `[SWARM DELEGATION: ATLAS + JUNIOR]` (via `delegate.py`)
* **Context & Root Cause:** Sprint 47 introduced `raw_lower in [...]` rigid string matching. "Hello pinky" fell through, got misclassified as `exp_tlm`, and routed to `BRAIN`.
* **Consensus & Design:** Rip out hardcoded greeting list. Restore pure prompt-guided semantic classification with explicit few-shot rules for direct resident salutations. Add cautionary BKM-015 header tags.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):**
    * `HomeLabAI/src/logic/cognitive_hub.py` (Lines 1040–1110)
    * `HomeLabAI/src/tests/test_fast_triage_harness.py` (Lightweight LLM hook test)
  * **Anchor 2 (Verification Command):**
    ```bash
    /home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest src/tests/test_fast_triage_harness.py -v
    ```
* **Sub-Tasks:**
  - `[STAGE 1]` Add `# [BKM-015-GUARD]` comment tag and update Guided Decoding schema.
  - `[STAGE 2]` Build `test_fast_triage_harness.py` verifying direct name salutations route to `addressed_to: PINKY` via local vLLM.
  - `[STAGE 3]` Remove `raw_lower in [...]` block in `cognitive_hub.py`.
  - `[STAGE 4]` Run test against live local vLLM port 8088.

---

### 🛡️ Topic 4 & 5 / Story 7104: The Domain–Vibe Decoupling & Zero-Noise RAG Floor (`[FEAT-534]`)
* **Status:** `[PENDING IMPLEMENTATION]`
* **Assigned Execution Mode:** `[DIRECT: AGY]` (Deep Policy Architecture)
* **Context & Root Cause:** `config/triage_policy.json` forced `TECHNICAL` $\rightarrow$ `exp_tlm` and `FORENSIC` $\rightarrow$ `exp_for`, causing RAG to dump 2013 historical notes on conversational questions.
* **Consensus & Design:**
  1. Decouple `domain` (Data Source) from `vibe` (Tone).
  2. Add `unknown` to `domain: enum ["lab_history", "exp_bkm", "exp_tlm", "dream_stream", "unknown"]`.
  3. Default all conversational vibes to `domain: "unknown"`.
  4. Enforce **True RAG Rule**: If `domain == "unknown"` or cosine similarity $< 0.65$, return empty HyDE vector and skip ChromaDB.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):**
    * `HomeLabAI/config/triage_policy.json`
    * `HomeLabAI/src/logic/cognitive_hub.py` (`resolve_hyde_vector` & `_fetch_rag_context`)
    * `HomeLabAI/src/tests/test_rag_suppression_floor.py`
  * **Anchor 2 (Verification Command):**
    ```bash
    /home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest src/tests/test_rag_suppression_floor.py -v
    ```
* **Sub-Tasks:**
  - `[STAGE 1]` Update `triage_policy.json` schema to decouple default domains and add `unknown`.
  - `[STAGE 2]` Create unit test asserting no RAG context returned for `domain == "unknown"`.
  - `[STAGE 3]` Wire cosine threshold check ($0.65$) in `resolve_hyde_vector()`.
  - `[STAGE 4]` Verify on live silicon.

---

### 👥 Topic 6 / Story 7105: Two-Mice Single-Execution Gate (`[FEAT-535]`)
* **Status:** `[PENDING IMPLEMENTATION]`
* **Assigned Execution Mode:** `[SWARM DELEGATION: ATLAS + JUNIOR]` (via `delegate.py`)
* **Context & Root Cause:** In `cognitive_hub.py`, when `lead_node == "brain"`, a failed two-mice handover fell through to the `else:` branch, executing Brain a second time.
* **Consensus & Design:** Enforce mutual exclusion in `lead_node == "brain"` flow so Brain speaks once and only once.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):**
    * `HomeLabAI/src/logic/cognitive_hub.py` (Lines 1334–1365)
    * `HomeLabAI/src/tests/test_two_mice_single_execution.py`
  * **Anchor 2 (Verification Command):**
    ```bash
    /home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest src/tests/test_two_mice_single_execution.py -v
    ```
* **Sub-Tasks:**
  - `[STAGE 1]` Patch `lead_node == "brain"` conditional branch to prevent secondary execution.
  - `[STAGE 2]` Create mock test verifying single execution invocation for Brain-addressed turns.
  - `[STAGE 3]` Integrate into `cognitive_hub.py`.
  - `[STAGE 4]` Live test turn execution.

---

### 🧬 Topic 7 / Retrospective 7107: Critic Context Collapse & Sampling Hygiene
* **Status:** `[RESOLVED & GROUNDED IN RETROSPECTIVE]` (No action code needed beyond Story 7105 fix)
* **Consensus Finding:** The critic token malformation (`"{"` and `"P 1"`) was caused by Topic 6 (Brain talking twice left Pinky's response buffer empty, malforming the judge's prompt context). Enforcing single-turn execution in Story 7105 and greedy decoding ($T=0.0$) permanently resolves critic stability.

---

### 📊 Topic 8 / Retrospective 7108: Dialogue Turn vs Round Table Consensus
* **Status:** `[RESOLVED & GROUNDED IN ARCHITECTURE]`
* **Consensus Finding:** 
  - Direct 1-on-1 turns (`addressed_to: BRAIN` or `addressed_to: PINKY`) are recorded to `journal_ledger.jsonl`.
  - Multi-node collaborative turns record sub-second stage deltas to `round_table_deltas.json` and persist to Clara-DNA blackboard memory.

---

### 🔌 Topic 9 / Story 7106: Dynamic `SID` DOM Healing on Connection Handshake (`[FEAT-536]`)
* **Status:** `[PENDING IMPLEMENTATION]`
* **Assigned Execution Mode:** `[DIRECT: AGY]` (Frontend JS Lifecycle)
* **Context & Root Cause:** Initial messages rendered during the first 1–2 seconds display `[SID: Unknown]` because the socket ID hasn't yet arrived from the server.
* **Consensus & Design:** Tag early DOM elements with `data-needs-sid="true"`. Upon receiving the WebSocket `handshake` / `status` frame, dynamically heal all pending DOM tags with the true session ID.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):**
    * `Portfolio_Dev/field_notes/intercom_v2.js` (Lines 195–205 and 480–490)
    * `Portfolio_Dev/field_notes/data/benchmarks.js`
  * **Anchor 2 (Verification Command):**
    ```bash
    grep -n "data-needs-sid" Portfolio_Dev/field_notes/intercom_v2.js
    ```
* **Sub-Tasks:**
  - `[STAGE 1]` Add `data-needs-sid` attribute to initial DOM renders.
  - `[STAGE 2]` Add auto-healing sweep inside `ws.onmessage` upon receiving `session_token` / `socket_id`.
  - `[STAGE 3]` Test via browser reload.

---

### 🕒 Topic 10 / Retrospective 7110: Browser History Timestamp Normalization
* **Status:** `[RESOLVED & GROUNDED IN RETROSPECTIVE]`
* **Consensus Finding:** Identical timestamps (`12:48:27`) occur only when re-rendering un-timestamped messages from `sessionStorage` upon browser refresh. Live message stream generates accurate wall-clock timestamps.

---

## 🔬 Pre-Retrospective: The Domain–Vibe Coupling Audit

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                          THE DOMAIN–VIBE DECOUPLING CONTRACT                                │
├──────────────────────────────┬────────────────────────────────┬─────────────────────────────┤
│ Dimension                    │ Old Coupled State (Broken)     │ New Decoupled State (Clean) │
├──────────────────────────────┼────────────────────────────────┼─────────────────────────────┤
│ VIBE (Conversational Tone)   │ Forced default_domain + RAG    │ Pure Tone (CASUAL, TECH,    │
│                              │ (e.g. TECH -> exp_tlm)         │ FORENSIC, HISTORICAL)       │
├──────────────────────────────┼────────────────────────────────┼─────────────────────────────┤
│ DOMAIN (Knowledge Base)      │ Auto-selected by Vibe          │ Explicit Data Target or     │
│                              │                                │ "unknown"                   │
├──────────────────────────────┼────────────────────────────────┼─────────────────────────────┤
│ RAG RETRIEVAL TRIGGER        │ Fired automatically on Vibe    │ Fired ONLY if domain !=     │
│                              │                                │ "unknown" & Cosine >= 0.65  │
└──────────────────────────────┴────────────────────────────────┴─────────────────────────────┘
```

---

## 🧭 Orchestration Sequence & Live Silicon Verification Strategy

```
  ┌────────────────────────────────────────────────────────┐
  │ 1. Story 7101 (Topic 1 & 1.1) [DIRECT: AGY]            │
  │    Config-Driven Engine Seats & 2x Probe/Race Timings  │
  └──────────────────────────┬─────────────────────────────┘
                             │  🧪 Verify: test_speculative_triage_seats.py
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │ 2. Story 7103 (Topic 3)       [SWARM: ATLAS+JR]        │
  │    Semantic Triage Grounding (BKM-015 Cleanup)         │
  └──────────────────────────┬─────────────────────────────┘
                             │  🧪 Verify: test_fast_triage_harness.py
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │ 3. Story 7104 (Topic 4 & 5)   [DIRECT: AGY]            │
  │    Domain-Vibe Decoupling & 'unknown' RAG Floor        │
  └──────────────────────────┬─────────────────────────────┘
                             │  🧪 Verify: test_rag_suppression_floor.py
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │ 4. Story 7105 (Topic 6 & 7)   [SWARM: ATLAS+JR]        │
  │    Two-Mice Single-Turn Gate (Fixes Brain Double-Talk) │
  └──────────────────────────┬─────────────────────────────┘
                             │  🧪 Verify: test_two_mice_single_execution.py
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │ 5. Story 7102 (Topic 2)       [SWARM: ATLAS+JR]        │
  │    Console Broadcast De-Duplication                    │
  └──────────────────────────┬─────────────────────────────┘
                             │  🧪 Verify: test_telemetry_broadcast_dedup.py
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │ 6. Story 7106 (Topic 9)       [DIRECT: AGY]            │
  │    Frontend SID Auto-Healing in intercom_v2.js         │
  └──────────────────────────┬─────────────────────────────┘
                             │  🧪 Verify: Live Web Intercom turn check
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │ 🏁 FINAL LIVE SMOKE TEST: Full Silicon Turn Check      │
  │    "Hello Pinky!" -> Sub-800ms, Clean Pinky Voice,    │
  │    0s Dead Air, No RAG Spam, Accurate SID in UI        │
  └────────────────────────────────────────────────────────┘
```
