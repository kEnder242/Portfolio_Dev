# SPRINT 31: THE GREAT BRAIN AWAKENING [REFACTOR PLAN]
**Status:** PLANNING | NO EXECUTION PERMITTED

## 🎯 MISSION
Execute an architectural refactor to align the Lab's terminology and file structure with the Phase 15 "Neural Relay" reality. We will promote local reasoning to "The Brain," transform the 4090 into the "Deep Thought" action, and move from monolithic management to modular "Appliance-Grade" services.

---

## 🏗️ GOAL 1: NOMENCLATURE SHIFT & PHYSICAL FOUNDATIONS
*Objective: Stabilize the 'Hard Anchors' and align the file system with the mental model before logical shifts.*

### 🔬 Node Promotion: Shadow -> THE BRAIN
*   **Pedigree & Intent**: *"Shadow was originally a failover; the local 2080 Ti is now a primary participant in the Relay. Promoting it to THE BRAIN aligns our nomenclature with the new hierarchy of authority."* — Lead Engineer.
*   **Tasks**:
    *   [x] **Task 1.1 (Git Move)**: Physically rename `shadow_node.py` -> `brain_node.py` and update `infrastructure.json`.
    *   [x] **Task 1.2 (Prompt Sync)**: Update `BRAIN_SYSTEM_PROMPT` and `PINKY_SYSTEM_PROMPT` to reflect the new hierarchy ("The Brain" and "Deep Thought").
    *   [x] **Task 1.3 (Identity Bedrock)**: Update `IDENTITY_BEDROCK` labels in `cognitive_hub.py` to match the new naming gauntlet.
    *   [ ] **Task 1.5 (Lobby Residency)**: Ensure the "Deep Thought" action (4090) maintains model-awareness to minimize weight-swapping. Preserve the immediate fast-track response capability during local engine warm-ups.
    *   [ ] **Task 1.6 (Resilience Parity)**: [FEAT-069] Ensure the local Brain (2080 Ti) inherits the Sovereign toolset (RAG/Excerpts) during remote-offline failover to maintain Lab availability.

### 🔐 Physical Boundary Mitigation: VRAM Mutex
*   **Pedigree & Intent**: *"When Ignition becomes a separate service, in-memory locks will fail. We need a physical anchor to prevent silicon thrashing."* — Lead Engineer.
*   **Tasks**:
    *   [x] **Task 1.4 (File-based Mutex)**: Transition from `self._ignition_in_progress` memory flags to strict file-based locking (e.g., `fcntl` on `/tmp/lab_vram.lock`) to ensure only one process touches the GPU.

---

## 🧠 GOAL 2: THE CONSCIOUSNESS SHIFT (Logic & Communication)
*Objective: Move from 'Budgeting for cost' to 'Reasoning for Depth' using recursive linguistic resonance.*

### 📈 Metric Shift: Fuel -> INTEREST
*   **Pedigree & Intent**: *"We aren't budgeting for tokens anymore; we're reasoning for depth. If the Lab is genuinely 'interested' in a topic, it should have the autonomy to keep digging. Interest is the new fuel."* — Lead Engineer.
*   **Tasks**:
    *   [x] **Task 2.1 (The Recursive Scorer)**: Refactor `CognitiveHub.py` to derive `interest_score` from the semantic overlap and topical resonance (identifiable via grammar and repeated phrasing) between the current query and the `resonant_history`.
    *   [x] **Task 2.2 (Long-Form Shunt)**: Implement logic where `interest_score > 0.8` forces `max_tokens=2000`, allowing the Brain to perform exhaustive multi-node synthesis.
    *   [x] **Task 2.3 (Persona Stance)**: Update `_process_node_stream` to inject behavioral stances (ACADEMIC vs INTERFACE) based on the interest scalar.
    *   [x] **Task 2.4 (The Thought Trace)**: Update `execute_dispatch` to package the `<thought>` block of the local nodes into the context window of the remote node.
    *   [x] **Task 2.5 (Visible Consensus)**: Update UI (`style.css` and `intercom_v2.js`) to highlight where "Deep Thought" has refined the "Local Brain" intuition.
    *   [ ] **Task 2.6 (Native MCP Sampling)**: Enable nodes to request client-side LLM completions via the Hub (`sampling/createMessage`), allowing the Brain to "Ask the 4090" for help mid-turn.

---

## 🗄️ GOAL 3: THE MEMORY BRIDGE (Refinement & Persistence)
*Objective: Build a cumulative RAG context that survives hibernation without the 'Greed' of monolithic context.*

### 📋 Topical RAG Cache (The Clipboard)
*   **Pedigree & Intent**: *"RAG shouldn't be a one-shot lookup. We need to build up a 'mental clipboard' of context over several turns, refining the truth as the conversation deepens."* — Lead Engineer.
*   **Tasks**:
    *   [x] **Task 3.1 (The Clipboard)**: Implement a session-scoped "Clipboard" in `ArchiveNode.py` that builds up RAG info turn-over-turn. Include **Neighborhood Expansion** logic to proactively look up related segments based on discovering new technical anchors.
    *   [x] **Task 3.2 (RRF Implementation)**: Physically implement the **RRF Hybrid Retrieval** [BKM-032] to merge vector scores with exact-match frequency rankings for acronym precision (e.g., PECISTRESSOR).

### 📋 Workspace-as-Cache (Refinement)
*   [x] **Task 3.4 (The Collaborative Ledger)**: Implement `create_followup_file` in `ArchiveNode.py`. Trigger on Turn 2 of high-interest loops to instantiate physical `whiteboard/` files with Triage-derived names.
*   [x] **Task 3.5 (Append-Only Mandate)**: Configure nodes to prefer the internal `patch_file` tool for updating Whiteboard files, ensuring evidence is built up without clobbering history.
*   [x] **Task 3.6 (RAG Pointers)**: Use "RAG Pointers" (URIs/Line Anchors) in follow-up files instead of copying large text blocks to prevent context-window drowning.

### ❄️ The Hibernation Rule
*   **Pedigree & Intent**: *"Keep the conversation history, but discard the heavy context cache so we start the next session with a lean mind but a long memory."* — Lead Engineer.
*   **Tasks**:
    *   [x] **Task 3.3 (Selective Persistence)**: Refactor `acme_lab.py` to persist `message_history` to disk, but explicitly discard the RAG Clipboard and heavy VRAM objects during H2 transitions.

---

## 📐 GOAL 4: THE APPLIANCE-GRADE DECOMPOSITION (V5 Architecture)
*Objective: Decompose the v4 monolith into a modular suite of services with 100% foyer uptime.*

### 🛠️ The Split Strategy: "The Zero-Downtime Handover"
*   **Pedigree & Intent**: *"The v4 monolith is a single point of failure. Breaking the Attendant into 'Appliance-Grade' services ensures that a failure in the router doesn't kill the ignition logic."* — Lead Engineer.
*   **Tasks**:
    *   [x] **Task 4.1 (V5 Skeleton)**: Establish the `src/v5/` directory structure.
    *   [x] **Task 4.2 (The Always-Online Foyer)**: Implement a standalone WebSocket/REST bridge that stays up 100% of the time, solving "Ghost Disconnects."
    *   [x] **Task 4.3 (Disk-backed Holding Queue)**: Build a robust, disk-backed queue in the Foyer to hold user intent during hot-swaps of logic modules.
    *   [x] **Task 4.4 (Larynx-Aware Ignition)**: Build the `attendant.ignition` module that uses the **Vocal Handshake** as a definitive readiness signal for the foyer.
    *   [ ] **Task 4.5 (The Clean Cut)**: Deprecate `lab_attendant_v4.py` and promote the modular V5 orchestrator.

#### 🗺️ V5 Physical-to-Logical [FEAT] Map
| Module | Target Features |
| :--- | :--- |
| **`attendant.ignition`** | [FEAT-119] The Assassin (Port Reaping), [FEAT-254] VRAM Verification. |
| **`attendant.lifecycle`** | [FEAT-249] Hibernation Matrix, [FEAT-134] AFK Guarding. |
| **`attendant.router`** | [FEAT-233] Waterfall, [FEAT-234] Scalar Interest Triage. |
| **`attendant.forensics`**| [FEAT-151] Forensic Ledger (Wordy Log), [FEAT-318] Trace Monitor. |

---

## 🧪 GOAL 5: DEFERRED SEMANTIC CERTIFICATION
*Objective: Apply BKM-032 to certify the Refactor results.*

*   **Phase A (The Hard Switch)**: [x] Automated batch verify that all ports bind and the "Interest" scalar still calculates correctly.
---

## 📜 PHASE 1: REFACTOR REPORT [COMPLETE]
### 🏆 Milestone Completion Summary

#### 1. Goal 1: Physical Foundations & Nomenclature
*   **The Brain (Local)**: Promoted the 2080 Ti node to primary local participation.
*   **Deep Thought (Remote)**: Established the 4090 as the Sovereign strategic reasoning engine.
*   **VRAM Mutex**: Implemented `fcntl` locking on `/tmp/lab_vram.lock` in `acme_lab.py` to prevent silicon thrashing during ignition.
*   **Git Status**: SECURED. (Committed to `sprint-31` branch).

#### 2. Goal 2: The Consciousness Shift (Interest Scorer)
*   **Recursive Scalar**: Refactored `CognitiveHub.py` to use a dynamic **Interest Scalar**. The system now detects semantic resonance with `round_table_memory`, boosting interest on technical follow-ups to force Sovereign (4090) depth.
*   **Wait-for-Brain (Task 2.2)**: Implemented an **Interest Gate** (> 0.8) that forces the Hub to synchronize and wait for the remote synthesis before finalizing the turn.
*   **Persona Stance (Task 2.3)**: Added logic to inject `ACADEMIC` (dense, evidence-heavy) vs `INTERFACE` (brief, witty) stances into node guidance based on the Interest scalar.
*   **Thought Trace (Task 2.4)**: Explicitly extract `<thought>` blocks from local nodes and package them into the context window for **Deep Thought**, ensuring the Sovereign node knows the local "Intuition" before reasoning.
*   **Visible Consensus (Task 2.5)**: Updated `intercom_v2.js` and `style.css` to highlight **Sovereign Refinement** in the UI with a distinct gold border and background.

#### 3. Goal 3: The Memory Bridge (Implemented & Verified)
*   **The Clipboard (Task 3.1)**: Added session-scoped context storage to `ArchiveNode.py`.
*   **Neighborhood Expansion**: Refactored `get_context` to proactively fetch surrounding technical segments (+/- 1 entry) from JSON logs when a match is found, caching them in the session clipboard.
*   **Hybrid Retrieval (RRF) (Task 3.2)**: Implemented **Reciprocal Rank Fusion**. The Archive Node now merges Vector scores (ChromaDB) with Exact-match Frequency scores (Keyword Grep) to ensure acronyms like "PECISTRESSOR" are never missed.
*   **Selective Persistence (Task 3.3)**: `message_history` is now physically backed by `interaction_history.json`. RAG Clipboards are explicitly cleared during **H2 transitions** to maintain a lean context for the next session.

#### 4. Goal 4: Appliance-Grade Decomposition (Skeleton Established)
*   **V5 Skeleton (Task 4.1)**: Established the `src/v5/` directory structure with modular sub-services.
*   **Always-Online Foyer (Task 4.2/4.3)**: Created `v5/foyer/router.py`, a standalone WebSocket/REST bridge that implements a **Disk-backed Intent Queue** (`foyer_queue.jsonl`), ensuring user requests are secured even if logic nodes are offline.
*   **Larynx-Aware Ignition (Task 4.4)**: Created `v5/ignition/manager.py`, utilizing the physical **VRAM Mutex** and verifying readiness via the **Vocal Handshake** definitive signal.

### 🧪 Verification (BKM-032 / BKM-029)
*   **Conversation Ledger**: Successfully verified the multi-turn interest climb and thought-trace passage via `test_relay_interest_buildup.py`.
*   **RRF/Clipboard Trace**: Successfully verified hybrid retrieval and neighbor caching via `test_archive_clipboard.py` and `test_archive_rrf.py`.
*   **Persistence Audit**: Successfully verified history restoration and H2 rule enforcement via `test_hub_persistence.py`.

---

## 🚀 PHASE 2: AUTONOMOUS STABILIZATION & ALARM INTEGRATION
*Objective: Deprecate V4 monolith and certify V5 resilience for overnight ALARM tasks.*

### 🛠️ V4 Deprecation & V5 Promotion
*   **Pedigree & Intent**: *"We cannot have two captains. Moving the primary entry points to V5 ensures the 'Always-Online' Foyer is the definitive gate for all traffic."* — Lead Engineer.
*   **Tasks**:
    *   [x] **Task 2.1 (The Clean Cut)**: Physically move `acme_lab.py` logic into `v5/router.py` and rename the legacy script to `acme_lab_v4.py.bak`.
    *   [x] **Task 2.2 (V5 Transition Shim)**: Established a shim `acme_lab.py` that boots the V5 Foyer Router, ensuring backward compatibility with existing launch scripts.

### 🌙 ALARM Task Resilience (Dreaming & Refinement)
*   **Pedigree & Intent**: *"The mice shouldn't stop thinking when I'm away. Refactoring the ALARM loop to use the VRAM Mutex and Interest Scorer ensures continuous enhancement of the 18-year archive."* — Lead Engineer.
*   **Tasks**:
    *   [x] **Task 2.3 (Modular Dreaming)**: Update `internal_debate.py` and `dream_cycle.py` to respect the V5 nomenclature and use the physical VRAM Mutex.
    *   [x] **Task 2.4 (Continuous Burn)**: Implement a 'Quiet Refinement' loop in the Ignition Manager that triggers gem-refining tasks when VRAM pressure is low and user activity is idle.
    *   [x] **Task 2.5 (Search Parity)**: Ensure the 'Nightly Job Search' and 'Focal Connections' agents are updated to use the RRF Hybrid Retrieval for higher matching fidelity.


---

## 🛡️ PHASE 3: APPLIANCE STABILIZATION GAUNTLET
*Objective: Verify V5 modular resilience and ALARM task stability under physical stress.*

### ⛓️ Scenario A: The Busy Silicon Handshake (VRAM Mutex)
*   **Pedigree & Intent**: *"In a decoupled world, the Foyer must respect the physical VRAM lock held by background tasks without failing the user."* — Lead Engineer.
*   **Contextual Notes**: Repurpose `test_induction_mutex.py` logic to verify that when a background task (e.g., `dream_cycle.py`) holds `/tmp/lab_vram.lock`, the V5 Foyer correctly enqueues the user intent and provides a characterful "Silicon Busy" quip.
*   **Tasks (BKM-029)**:
    1.  [x] **Task 3.1.1 (Compare)**: Contrast `v5/ignition/manager.py` locking with legacy Attendant V4 behavior.
    2.  [x] **Task 3.1.2 (Save)**: Secure the `test_v5_mutex_collision.py` validator.
    3.  [x] **Task 3.1.3 (Strategic Inquiry)**: Brainstorm "Lock Hunger" traps where a background task might starvation the Foyer.
    4.  [x] **Task 3.1.4 (Verify)**: Physically simulate a 60s lock-hold and verify Foyer queue drainage.

### 👻 Scenario B: The Ghost Intent Recovery (Queue Durability)
*   **Pedigree & Intent**: *"Intent must survive the crash. If the Foyer dies, the queue stays."* — Lead Engineer.
*   **Contextual Notes**: Evolve `test_lifecycle_gauntlet.py` into a crash-consistency test. Verify that `foyer_queue.jsonl` is recovered and re-broadcasted to clients after a Foyer restart.
*   **Tasks (BKM-029)**:
    1.  [x] **Task 3.2.1 (Compare)**: Verify `foyer_queue.jsonl` schema against `IntentEvent` dataclass.
    2.  [x] **Task 3.2.2 (Save)**: Secure `test_v5_queue_recovery.py`.
    3.  [x] **Task 3.2.3 (Strategic Inquiry)**: Identify "Zombie Event" traps where a processed task is re-run after crash.
    4.  [x] **Task 3.2.4 (Verify)**: Kill Foyer with SIGKILL during active queueing and verify state restoration.

### 🌙 Scenario C: The Nightly No-Show (ALARM Self-Healing)
*   **Pedigree & Intent**: *"The Ignition Manager is the silent guardian. It must detect and restart failed ALARM loops."* — Lead Engineer.
*   **Contextual Notes**: Upgrade `test_goodnight_bounce.py` logic to verify that the `continuous_burn_loop` and `run_nightly_tasks` in the V5 Ignition Manager can detect subprocess failures (e.g., `refine_gem.py` crash) and re-initiate the sequence.
*   **Tasks (BKM-029)**:
    1.  [x] **Task 3.3.1 (Compare)**: Verify `v5/ignition/manager.py` subprocess monitoring against legacy watchdog logic.
    2.  [x] **Task 3.3.2 (Save)**: Secure `test_v5_alarm_healing.py`.
    3.  [x] **Task 3.3.3 (Strategic Inquiry)**: Brainstorm "VRAM Thrashing" traps during high-frequency restart loops.
    4.  [x] **Task 3.3.4 (Verify)**: Mock a `refine_gem.py` failure and verify Ignition Manager's 60s cooldown/restart logic.

### 💎 Scenario D: The Semantic Finality (Uber 5x5 Gauntlet)
*   **Pedigree & Intent**: *"Physical resilience is the skeleton; semantic fidelity is the soul. The 5x5 proves the system survives natural idle drift without logical decay."* — Lead Engineer.
*   **Contextual Notes**: Adapt `uber_5x5_hand_crank.py` to V5 nomenclature. Perform a 75-minute increasing stress test (5, 10, 15, 20, 25 mins) with natural idle drift.
*   **Tasks (BKM-029)**:
    1.  [ ] **Task 3.4.1 (Compare)**: Contrast `uber_5x5` search patterns with new V5 node names (**Deep Thought** / **The Brain**) and **Visible Consensus** DOM markers.
    2.  [ ] **Task 3.4.2 (Save)**: Secure the adapted `src/debug/uber_5x5_v5.py`.
    3.  [ ] **Task 3.4.3 (Strategic Inquiry)**: Audit **BKM-033 (Babysitting)** for real-time forensic oversight during the 75-minute run.
    4.  [ ] **Task 3.4.4 (Verify)**: Achieve 5/5 consecutive wins. Finalize with a **BKM-032 Wordy Audit** of the evaluation logs.

### ⚖️ LEAD ENGINEER REVIEW REQUIRED
*This plan is an artifact for Sprint 31. No code changes have been made.*


