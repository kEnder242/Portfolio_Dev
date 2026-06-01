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
    *   [ ] **Task 2.2 (Long-Form Shunt)**: Implement logic where `interest_score > 0.8` forces `max_tokens=2000`, allowing the Brain to perform exhaustive multi-node synthesis.
    *   [ ] **Task 2.3 (Native MCP Sampling)**: Enable nodes to request client-side LLM completions via the Hub (`sampling/createMessage`), allowing the Brain to "Ask the 4090" for help mid-turn.

---

## 🗄️ GOAL 3: THE MEMORY BRIDGE (Refinement & Persistence)
*Objective: Build a cumulative RAG context that survives hibernation without the 'Greed' of monolithic context.*

### 📋 Topical RAG Cache (The Clipboard)
*   **Pedigree & Intent**: *"RAG shouldn't be a one-shot lookup. We need to build up a 'mental clipboard' of context over several turns, refining the truth as the conversation deepens."* — Lead Engineer.
*   **Tasks**:
    *   [ ] **Task 3.1 (The Clipboard)**: Implement a session-scoped "Clipboard" in `ArchiveNode.py` that builds up RAG info turn-over-turn. Include **Neighborhood Expansion** logic to proactively look up related segments based on discovering new technical anchors.
    *   [ ] **Task 3.2 (RRF Implementation)**: Physically implement the **RRF Hybrid Retrieval** [BKM-032] to merge vector scores with exact-match frequency rankings for acronym precision (e.g., PECISTRESSOR).

### 📋 Workspace-as-Cache (Refinement)
*   [x] **Task 3.4 (The Collaborative Ledger)**: Implement `create_followup_file` in `ArchiveNode.py`. Trigger on Turn 2 of high-interest loops to instantiate physical `whiteboard/` files with Triage-derived names.
*   [ ] **Task 3.5 (Append-Only Mandate)**: Configure nodes to prefer the internal `patch_file` tool for updating Whiteboard files, ensuring evidence is built up without clobbering history.
*   [ ] **Task 3.6 (RAG Pointers)**: Use "RAG Pointers" (URIs/Line Anchors) in follow-up files instead of copying large text blocks to prevent context-window drowning.

### ❄️ The Hibernation Rule
*   **Pedigree & Intent**: *"Keep the conversation history, but discard the heavy context cache so we start the next session with a lean mind but a long memory."* — Lead Engineer.
*   **Tasks**:
    *   [ ] **Task 3.3 (Selective Persistence)**: Refactor `acme_lab.py` to persist `message_history` to disk, but explicitly discard the RAG Clipboard and heavy VRAM objects during H2 transitions.

---

## 📐 GOAL 4: THE APPLIANCE-GRADE DECOMPOSITION (V5 Architecture)
*Objective: Decompose the v4 monolith into a modular suite of services with 100% foyer uptime.*

### 🛠️ The Split Strategy: "The Zero-Downtime Handover"
*   **Pedigree & Intent**: *"The v4 monolith is a single point of failure. Breaking the Attendant into 'Appliance-Grade' services ensures that a failure in the router doesn't kill the ignition logic."* — Lead Engineer.
*   **Tasks**:
    *   [ ] **Task 4.1 (V5 Skeleton)**: Establish the `src/v5/` directory structure.
    *   [ ] **Task 4.2 (The Always-Online Foyer)**: Implement a standalone WebSocket/REST bridge that stays up 100% of the time, solving "Ghost Disconnects."
    *   [ ] **Task 4.3 (Disk-backed Holding Queue)**: Build a robust, disk-backed queue in the Foyer to hold user intent during hot-swaps of logic modules.
    *   [ ] **Task 4.4 (Larynx-Aware Ignition)**: Build the `attendant.ignition` module that uses the **Vocal Handshake** as a definitive readiness signal for the foyer.
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

*   **Phase A (The Hard Switch)**: [ ] Automated batch verify that all ports bind and the "Interest" scalar still calculates correctly.
*   **Phase B (The Voice Audit)**: [ ] Gemini CLI (AI Reviewer) reads the "Deep Thought" traces for persona alignment and interest decay naturalism.

---

### ⚖️ LEAD ENGINEER REVIEW REQUIRED
*This plan is an artifact for Sprint 31. No code changes have been made.*
