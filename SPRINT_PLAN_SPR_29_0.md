# SPRINT 29: THE PERFORMANCE FRONTIER [MAY 19 12:00]
**Status:** ACTIVE | 90% COMPLETE (Pending Qwen Adapter Forge)

## 🎯 MISSION
To verify and maximize the performance of the Acme Lab's multi-LoRA routing architecture. We aim for 100% KV-cache prefix hits between Triage and Persona phases to minimize Time-to-First-Token (TTFT).

---

## 🚨 FORENSIC DISCOVERY: RAG BYPASS [HIGH SEVERITY]
- **Root Cause**: Investigation of `CognitiveHub.py` reveals that the `intent` variable was being initialized to `"STRATEGIC"` in triage exception blocks, overwriting `RECALL`.
- **Status**: [x] **FIXED**. Initialized as `None` and preserved through retry loops.

---

## 🛠️ SPRINT GOALS

### 🎯 GOAL 18: WAKE-ON-INTENT HARDENING [STABL-001]
*Objective: Eliminate the "Chaotic Wake-up" race conditions.*

- [x] **Task 20.0.1 (Wait-for-Ready Lock)**: Port-8088 ping loop moved to `_synchronize_and_probe` to prevent triage before binding.
- [x] **Task 20.0.2 (Cached Lobby Relay)**: Bypassed local boot wait if Brain is online for instant responses (0.8s TTFT).

### 🎯 GOAL 19: SHELL-SIDE RECIPE HARDENING [PERF-001]
*Objective: Stabilize vLLM flags and prevent Python GC interference.*

- [x] **Task 20.1 (Move Flags to start_vllm.sh)**: Port all vLLM optimization flags (`--enable-prefix-caching`, `--max-loras`, `--gpu-memory-utilization`) directly into the shell script to avoid Python GC deaths and flag parsing issues.
- [x] **Task 20.2 (Attendant Simplification)**: Update `lab_attendant_v4.py` to rely on the script for the "Bulletproof Recipe," passing only the `model_path` and `venv` as arguments.

### 🎯 GOAL 20: THE PHYSICAL BEDROCK (AGENTIC PREAMBLE) [FEAT-351]
*Objective: Achieve 100% stable prefix-cache hits for repeated or related queries via BKM-015.*

- [x] **Task 20.3 (Identity Bedrock Implementation - BKM-015)**: Create a shared constant string describing the Lab's 3-tier memory topography (Diamond/Archive/Raw), RAG capabilities, and resident roles (Pinky/Shadow/Brain). 
    - **Constraint**: Describe the *locations* and *capabilities* only. No hard-coded telemetry values or fuel metrics (BKM-015 compliance).
- [x] **Task 20.4 (Prompt-Engineering Routing)**: Shift triage from Python logic to "Agentic Routing" within the shared identity preamble.
- [x] **Task 20.5 (Context Displacement)**: Move all dynamic "Fuel/Route" data to the *tail* of the prompt or a trailing user message role to preserve the Bedrock prefix hash.
- [x] **Task 20.6 (Throughput Benchmarking)**: Develop `src/debug/bench_vllm_cache.py` to physically measure the latency difference between a cold prefill and a prefix-cached hit.

### 🎯 GOAL 21: THE QWEN PIVOT [FEAT-352]
*Objective: Standardize on Qwen2.5-3B for superior tool-calling and performance.*

- [x] **Task 20.7 (Qwen Transition)**: Update `infrastructure.json` to set `qwen2.5-3b-awq` as the `unified-base`.
- [x] **Task 20.8 (Adapter Legacy Preservation)**: Move existing Llama LoRAs to `/speedy/models/adapters/llama_legacy`.
- [x] **Task 20.9 (Nightly Task Adaptation)**: Update the Nightly Dream Pass and Training scripts to generate Qwen-compatible adapters.

---

## 🛠️ EXECUTION SEQUENCE (BKM-029)
1. **Priority 1**: RAG Bypass Cleanup (Stability). [COMPLETE]
2. **Priority 2**: Shell-Side Hardening (GC Shielding). [COMPLETE]
3. **Priority 3**: Physical Bedrock Implementation (Cache Optimization). [COMPLETE]
4. **Priority 4**: The Qwen Pivot (Intelligence Upgrade). [IN PROGRESS]

---

## 🧪 PROPOSED VERIFICATION TESTS

### 1. The "Throughput Ghost" Test
**Method**: Send the same 1000-token technical prompt twice.
**Assertion**: The second request must have a TTFT < 50ms (Cache Hit).
**Status**: [x] **PASSED**. 75-min gauntlet (5x5) verified **0.01s TTFT** consistently.

### 2. The "Triage-to-Persona" Handover
**Method**: Send a query that triggers Triage -> Shadow -> Brain.
**Assertion**: shadow_node must report a prefix-cache hit on the shared user input tokens.
**Status**: [x] **PASSED**. 0.01s TTFT confirmed during multi-node transitions.

### 3. RAG Sincerity Check
**Method**: Ask "What did I do with RAPL in the past?"
**Assertion**: Verify Hub logs show intent: RECALL and the archive node is physically invoked.
**Status**: [x] **PASSED**. Forensic logs confirm **RECALL** intent firing without year regex.

---


---

## 🔬 RESEARCH RECOVERY & MODERNIZATION REPORT [BKM-023]
**Date:** May 20, 2026 | **Status:** PROPOSED

### 🎯 Restoration Summary
Following a forensic audit of `research.html` and `RESEARCH_SYNTHESIS.md`, we have restored the high-fidelity ArXiv-centric architecture. Internal `FEAT` markers have been subordinated to their theoretical anchors to maintain a professional "Research Ledger" appearance.

### 🧬 ArXiv Mapping & Pedigree Correlation
| Research Anchor | ArXiv ID | Implementation Milestone | Status |
| :--- | :--- | :--- | :--- |
| **FS-Researcher** | 2602.01566 | [FEAT-095] Static Synthesis | Live |
| **Agentic-R** | 2601.11888 | [FEAT-080] Learning to Retrieve | Active |
| **TTCS / Curriculum**| 2601.22628 | [FEAT-114] Sovereign Bridge | Live |
| **Apple CLaRa** | 2511.18659 | [FEAT-073] Semantic Condenser | Live |
| **Liger Kernel** | 2410.10989 | [FEAT-137] Triton Optimization | Live |
| **Byzantine ToM** | 2603.00142 | [FEAT-071] Internal Debate | Live |
| **AT2QA** | 2603.01853 | [FEAT-173] Autonomous Pivot | Design |
| **Memex (RL)** | 2603.04257 | [FEAT-067] Diamond Dreaming | Live |
| **TTT-Discover** | 2601.16175 | N/A | Planned |
| **MAXS** | 2601.12538 | N/A | Planned |

### 🛠️ Actions Taken [BKM-023 Compliance]
1.  **Surgical Update**: `RESEARCH_SYNTHESIS.md` updated with explicit ArXiv IDs.
2.  **Noise Filtering**: Cleaned up "Tabled & Future" items in the source markdown.
3.  **Demo Creation**: `field_notes/research_demo.html` generated (not committed) for UI comparison. 
4.  **BKM-023 Adherence**: All edits performed via `replace` to preserve surrounding engineering context.

### 🔮 Next Steps
- [x] Review `research_demo.html`.
- [x] Perform the Google Keep brain dump for Epoch 2 research.
- [x] Sync the refined ledger to the public airlock (`sync_research.sh`).

---

## 🔬 PHASE 2: THE BICAMERAL DEBATE [MAY 20]
**Status:** DRAFT | PENDING LEAD ENGINEER GREENLIGHT

### 🎯 MISSION
Evolve the Lab's reasoning architecture from "Sequential Overhearing" to **Visible Consensus (TTCS)**. We will implement a persistent **Unified Session Ledger** and force explicit **Visible Debate** between nodes to eliminate historical amnesia and hallucinations when navigating the 18-year archive.

### 🧠 STRATEGIC RATIONALE (Why)
*   **The Goldfish Gap**: Currently, the Hub clears the `session_buffers` every turn. Pinky cannot "remember" the Brain's critiques from previous turns, causing cyclical errors during deep archival probes.
*   **The Banter Evolution**: We are pivoting from "Banter as side-chatter" to "Banter as the primary reasoning trace" [TTCS - 2601.22628]. The nodes must act as adversarial foils *before* presenting a final narrative to the user.
*   **The Silicon Constraint**: To hold this expanding context, we must implement Apple's Stochastic KV Routing [2604.22782] to fit the multi-turn debate onto 11GB of VRAM.

---

### 🛠️ SPRINT GOALS

#### 🎯 GOAL 22: OPEN DEBATE TTCS (Visible Consensus) [FEAT-355]
*Objective: Transform inter-node talk from "side-chatter" into the reasoning bedrock where nodes foil each other to reach historical truth.*

- [ ] **Task 22.1 (Thought Tagging)**: Update `execute_dispatch` in `cognitive_hub.py` and the node prompts to enforce the use of `<thought>` tags for all inter-node communication prior to user delivery.
    *   **BKM-017 Delegation**: Repetitive prompt string updates across `shadow_node.py`, `pinky_node.py`, and `brain_node.py` are candidates for `generalist` execution.
- [ ] **Task 22.2 (Adversarial Prompts)**: Modify `pinky_node.py` & `brain_node.py` system prompts to explicitly mandate critiquing each other's historical retrieval (e.g., "Check the dates").
- [ ] **Task 22.3 (Consensus Gate)**: Implement logic in `_process_node_stream` that prevents final user delivery until a consensus is reached or fuel runs out.
    *   **Logic Flow**: Triage -> Round Table -> `<thought>` (Pinky) -> `<thought>` (Shadow/Brain) -> Final Delivery.

**Implementation Details**:
*   **Where**: `HomeLabAI/src/logic/cognitive_hub.py` and individual node prompt files.
*   **Test Strategy**: Create `src/tests/test_debate_logic.py` (Mock) to verify the Hub doesn't skip the critique phase when "Fuel" is high.

#### 🎯 GOAL 23: FOIL-AWARE MEMORY (Unified Session Ledger) [FEAT-356]
*Objective: Eliminate amnesia by giving Pinky a persistent view of the Brain's strategic logic from previous turns.*

- [ ] **Task 23.1 (Persistent Ledger)**: Replace `session_buffers.clear()` in `cognitive_hub.py` with an append-only `round_table_memory` (deque, maxlen=5) that survives across turns.
    *   **Why**: Current amnesia prevents Pinky from learning from the Brain's corrections in real-time.
- [ ] **Task 23.2 (Ledger Injection)**: Prepend the `[PREVIOUS_DEBATE]` block to node context on every turn so they retain historical corrections.
- [ ] **Task 23.3 (Pruning Strategy)**: Implement rolling window management to prevent context bloat before KV Routing is finalized.
    *   **BKM-017 Delegation**: Surgical insertion of deque logic into `__init__` and `process_query` will be delegated to ensure context amnesia for the Main Agent is avoided.

**Implementation Details**:
*   **Where**: `HomeLabAI/src/logic/cognitive_hub.py` (`__init__` and `process_query`).
*   **Test Strategy**: Use `src/tests/test_memory_drill_down.py` (Forensic) to verify Turn-1 corrections are visible in Turn-2 prompts.

#### 🎯 GOAL 24: STOCHASTIC KV ROUTING (The VRAM Multiplier) [FEAT-357]
*Objective: Enable deep, multi-turn RAG conversations on the 2080 Ti by optimizing context caching.*

- [ ] **Task 24.1 (vLLM Parameter Injection)**: Update `lab_attendant_v4.py` (`_run_engine`) to include `--enable-chunked-prefill` and `--max-num-batched-tokens` optimized for memory sharing.
    *   **BKM-017 Delegation**: Shell command flag verification and update delegated to `generalist`.
- [ ] **Task 24.2 (Context Anchoring)**: Ensure `IDENTITY_BEDROCK` (Goal 20) remains locked in the prefix cache while the `round_table_memory` cycles dynamically.

**Implementation Details**:
*   **Where**: `HomeLabAI/src/lab_attendant_v4.py`.
*   **Test Strategy**: Use `src/debug/test_apollo_vram.py` to profile VRAM delta before/after enabling optimized prefill.

---

### 🔄 THE 4-STEP HEADS-DOWN IMPLEMENTATION LOOP
For each goal, I will follow this rigorous cycle:
1.  **REPRODUCE/MOCK**: Create a failing test case to establish the baseline failure.
2.  **SURGICAL ACT**: Apply the code change using the **Safe-Scalpel [FEAT-198]**.
3.  **UNIT VALIDATE**: Run specific tests (e.g., `pytest src/tests/test_debate_logic.py`).
4.  **INTEGRATION GAUNTLET**: Execute the **Physician's Gauntlet** (`src/debug/verify_sprint.py`).

---

### 🧪 THE ULTIMATE RAG VERIFICATION: "THE 2023 PROBE"
**Objective:** Prove the mice can debate and win on historical ground truth.
*   **Prompt**: "[ME] What was my primary focus in early 2023?"
*   **Success Criteria**: 
    1. **Trace**: Pinky finds "PECISTRESSOR" or "Telemetry Scripts."
    2. **Foil**: Shadow critiques the "raw data" to extract "Strategic Intent."
    3. **Memory**: Pinky answers a follow-up correctly using the Turn-1 debate context.

---

---

## 🔬 PHASE 3: RESTORATION HARDENING [MAY 21]
**Status:** ACTIVE | HEADS-DOWN EXECUTION

### 🎯 MISSION
Evolve the Lab's reasoning architecture to **100% Transparency**. We will physically remove the architectural barriers (is_internal, FRAME_ONLY) that caused the "Silence" failures and implement granular system reporting to eliminate the "Black Box" ignition problem.

### 🧠 STRATEGIC RATIONALE (Why)
*   **The Transparency Gap**: Phase 2 introduced flags (`is_internal`) that inadvertently hid thoughts from the Intercom. We are moving to a "Validation-First" mode where every inter-node whisper is visible.
*   **The Streaming Synergy**: Transparent thinking eliminates the need for blocking buffers. We will stream thoughts in real-time while using buffers strictly for background context.
*   **The Ignition Visibility**: Users must see the "Silicon Life" during the 5-minute warming window to ensure the system hasn't hung.

---

### 🛠️ SPRINT GOALS

#### 🎯 GOAL 28: NUKE INTERNAL MASKING (100% Transparency) [FEAT-361]
*Objective: Remove the ability for any node to be silenced or hidden from the user.*

- [ ] **Task 28.1 (API Purge)**: Remove `is_internal` and `internal` parameters from `execute_dispatch`, `_dispatch_plain_text`, and `_process_node_stream`.
- [ ] **Task 28.2 (Logic Removal)**: Delete `mute_pinky`, `mute_shadow`, and `FRAME_ONLY` mode hints from `cognitive_hub.py`.
- [ ] **Task 28.3 (Broadcast Enforcement)**: Ensure the "Handshake Tic" is always broadcast to the user.

#### 🎯 GOAL 29: NON-BLOCKING WATERFALL BUFFERS [FEAT-362]
*Objective: Ensure real-time streaming of all node dialogue.*

- [ ] **Task 29.1 (Token Priority)**: Refactor `on_token` to ensure the broadcast to the user is the high-priority task.
- [ ] **Task 29.2 (Context Decoupling)**: Ensure `session_buffers` are populated in the background without delaying the user-facing stream.

#### 🎯 GOAL 30: PHYSICAL WARMING VISIBILITY [FEAT-363]
*Objective: Provide real-time status updates during the restoration window.*

- [ ] **Task 30.1 (Attendant Milestones)**: Update `lab_attendant_v4.py` to log specific "Step 1, 2, 3" milestones to the event ledger.
- [ ] **Task 30.2 (Polling Task)**: Implement a 2s polling task in `acme_lab.py` to broadcast these ledger items as `[SYSTEM]` messages.

#### 🎯 GOAL 31: UI TRUTH VERIFICATION (Playwright) [FEAT-364]
*Objective: Physically prove that thoughts are visible in the browser.*

- [ ] **Task 31.1 (Visibility Test)**: Create `src/tests/test_visibility_truth.py` using Playwright.
- [ ] **Task 31.2 (DOM Assertion)**: Assert that `<thought>` blocks and `[SYSTEM]` stages are present in the Intercom DOM.

---

---

---

## 🔬 PHASE 4: RAG DEEP SEARCH & BKM-015 CLEANUP [MAY 22]
**Status:** DRAFT | PENDING LEAD ENGINEER REVIEW

### 🎯 MISSION
Transition the Lab from a "Year-Sticky" searcher into a semantic "Researcher." We will eliminate hardcoded temporal triggers (BKM-015), implement autonomous retry logic (Agentic Backtracking), and restore **Semantic Career Recall (FEAT-088)** to ensure the Lab Node can detect historical queries by intent rather than rigid regex.

### 🧠 STRATEGIC RATIONALE (Why)
*   **The BKM-015 Violation**: Currently, the system often relies on hardcoded regex for "2023" or "2019" to trigger RAG. This is brittle and violates the Law of Semantic Indirection. We must use the **Lab Node's Intent (RECALL)** as the sole authority.
*   **The Search Trap**: A single "thin" RAG result often leads to hallucinations. **Agentic Backtracking** allows the Lab to say "I found nothing, let me look at the surrounding years" autonomously.
*   **The Core Mind (FEAT-088)**: The Lab Node exists to perceive the *nature* of your query. By restoring FEAT-088, we empower the "Receptionist" to recognize when you are asking about the past, even if you don't provide a specific year.

---

### 🛠️ SPRINT GOALS

#### 🎯 GOAL 32: BKM-015 CLEANUP & FEAT-088 (Semantic Recall)
*Objective: Replace hardcoded triggers with semantic intent detection.*

- [ ] **Task 32.1 (Trigger Refactor)**: Remove hardcoded year-regex from `acme_lab.py` and `cognitive_hub.py`. Ensure `intent == "RECALL"` is the sole authority for triggering `archive.get_context`.
    *   **Where**: `HomeLabAI/src/logic/cognitive_hub.py` (lines 620-630).
- [ ] **Task 32.2 (FEAT-088 Intent Hardening)**: Update the `lab_node.py` (Sentinel) prompt to recognize temporal queries like "My time at Intel" or "Early career" and map them to `intent: RECALL`.
- [ ] **Task 32.3 (Agnostic Retrieval)**: Update `archive_node.py` to handle `get_context` calls without an explicit year, defaulting to a broader semantic search across the `long_term_wisdom` collection.

#### 🎯 GOAL 33: AGENTIC BACKTRACKING [RE-FEAT-173]
*Objective: Allow nodes to autonomously refine their search if initial results are thin.*

- [ ] **Task 33.1 (Fidelity Check)**: In `CognitiveHub`, implement a check after `get_context`. If `historical_context` is < 150 characters or contains "No relevant artifacts," trigger a secondary attempt.
- [ ] **Task 33.2 (Recursive Retrieval)**: Grant the `ArchiveNode` the authority to widen the temporal window (e.g., +/- 1 year) if the primary year yields low signal.

#### 🎯 GOAL 34: MULTI-YEAR NEIGHBORHOOD SEARCH
*Objective: Provide "temporal on-ramps" by peeking at surrounding context.*

- [ ] **Task 34.1 (Temporal Neighborhoods)**: Update `archive.get_context` to always retrieve 1 year before a confirmed temporal anchor to provide narrative continuity.
- [ ] **Task 34.2 (Strategic Summary Grafting)**: Ensure the high-level `[STRATEGIC_ANCHOR]` from the previous year is always included in the context when starting a new temporal probe.

#### 🎯 GOAL 35: STANDARDIZED 3-TIER MAP INJECTION
*Objective: Orient the mice with the full topography of the 18-year archive.*

- [ ] **Task 35.1 (Topographical Preamble)**: Ingest the `semantic_map.json` and prepend its topographical anchors (Theme vs Year ranges) to the `IDENTITY_BEDROCK` in `CognitiveHub`.

---

### 🧪 VERIFICATION: THE "RECALL PROBE" (v3.0)
**Objective:** Prove semantic intent and multi-year grounding.
*   **Prompt**: "[ME] Look into the early months of my NVIDIA career. What was the transition like?"
*   **Success Criteria**:
    1.  **Intent**: Hub logs show `intent: RECALL` triggered without the user saying "2024" or a specific year.
    2.  **Backtracking**: If NVIDIA starts in Jan, and the search finds nothing, the log must show a backtracking retry to Dec of the previous year.
    3.  **Continuity**: The final answer must reference context from both the anchor year and its neighborhood.

---

### ⚖️ LEAD ENGINEER REVIEW REQUIRED
*Per BKM-030, Phase 4 execution is paused pending review of these goals.*

