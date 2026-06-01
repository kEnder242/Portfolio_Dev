# SPRINT 31: THE GREAT BRAIN AWAKENING [REFACTOR PLAN]
**Status:** PLANNING | NO EXECUTION PERMITTED

## 🎯 MISSION
Execute an architectural refactor to align the Lab's terminology and file structure with the Phase 15 "Neural Relay" reality. We will promote local reasoning to "The Brain," transform the 4090 into the "Deep Thought" action, and move from monolithic management to modular "Appliance-Grade" services.

---

## 🧠 1. THE CONSCIOUSNESS SHIFT (Metric Promotion)

### 📈 Metric Shift: Fuel -> INTEREST
*   **Pedigree & Intent**: *"We aren't budgeting for tokens anymore; we're reasoning for depth. If the Lab is genuinely 'interested' in a topic, it should have the autonomy to keep digging. Interest is the new fuel."* — Lead Engineer.
*   **Strategy: Recursive Topic Scoring (Linguistic Resonance)**: Derive interest from the semantic overlap between the current query, the `resonant_history`, and established technical domains.
*   **Implementation**: 
    *   Purge `intent_anchors.json` and all hardcoded keyword list dependencies.
    *   Refactor `CognitiveHub.py`: `self.current_fuel` -> `self.interest_score`.
    *   Logic: The Brain evaluates the `interest_score` via linguistic resonance. If the score is high, it triggers multi-turn refinement. If low, it yields to high-fidelity brevity.

### 📚 Retrieval Shift: RRF Implementation
*   **Pedigree & Intent**: *"Exact technical matches (like PECISTRESSOR) are often lost in a purely semantic vector search. We need the rigor of Reciprocal Rank Fusion to ensure both the 'Vibe' and the 'Fact' surface correctly."* — Lead Engineer.
*   **Strategy: RRF Hybrid Retrieval [BKM-032]**: Merge vector scores with exact-match frequency rankings to surface "Star" technical artifacts.

---

## 🗄️ 2. THE MEMORY BRIDGE (Refinement & Persistence)

### 📋 Topical RAG Cache (The Clipboard)
*   **Pedigree & Intent**: *"RAG shouldn't be a one-shot lookup. We need to build up a 'mental clipboard' of context over several turns, refining the truth as the conversation deepens. It's about cumulative synthesis, not isolated pings."* — Lead Engineer.
*   **Strategy: Topical RAG Cache (Clipboard)**: Implement a session-scoped "Clipboard" in `ArchiveNode.py` that allows refining and building up RAG info Turn-over-Turn, flushed only on major topic shifts.

### ❄️ The Hibernation Rule
*   **Pedigree & Intent**: *"When the Lab goes to sleep (H2), I don't want to lose the thread of where we were. Keep the conversation history, but discard the heavy context cache so we start the next session with a lean mind but a long memory."* — Lead Engineer.
*   **Strategy: Selective Persistence**: Preserve `message_history` in `acme_lab.py`, but discard the heavy RAG Clipboard and trigger `clear_thoughts()` on the thinking node.

---

## 📐 3. THE APPLIANCE-GRADE DECOMPOSITION (V5 Architecture)
*   **Pedigree & Intent**: *"Transform the 'Stable Monolith' into a modular suite of services. Objective: Decouple physical silicon management (Ignition) from logical intent (The Brain) to achieve zero-downtime persona transitions and eliminate state-machine race conditions."* — Lead Engineer.

### 🔬 Node Promotion: Shadow -> THE BRAIN
*   **Strategy**: Deprecate "Shadow." The local reasoning node is now **THE BRAIN**. The 4090 is accessed via the **Deep Thought** action. 

### 🛠️ The Four Physical Boundaries
Based on forensic analysis of the v38 baseline (where `acme_lab.py` and `lab_attendant_v4.py` exceed 2,000 lines), the system will be split along four natural boundaries:
1.  **The Ignition Boundary (`attendant.ignition`)**: Strictly silicon. Port checking, weight loading, process reaping. Zero cognitive logic.
2.  **The Foyer Boundary (`attendant.foyer`)**: Always-online WebSocket/REST bridge. Solves "WebSocket Jitter" and the "Silent Ledger" bug by staying up even when the Brain is "Dreaming" or "Resetting."
3.  **The Logic Boundary (`lab.brain` / `lab.sentinel`)**: All "Interest" and "Resonance" logic moves to a dedicated Brain Engine, independent of physical server routing.
4.  **The Forensic Boundary (`attendant.forensics`)**: Pulse logging and trace monitoring.

### 🛡️ The Versioning Strategy: "The Zero-Downtime Handover"
*   **Step 1: The v5 Skeleton**: Create a new directory structure `HomeLabAI/src/v5/`.
*   **Step 2: Component Extraction**: Extract one module at a time (e.g., `ignition.py`), rather than a "Big Bang" refactor.
*   **Step 3: The Alias Layer**: Rename `shadow_node.py` -> `brain_node.py` physically first, then let the V4 monolith call the V5 Brain module.
*   **Step 4: The Clean Cut**: Once verified via parallel run, deprecate `lab_attendant_v4.py` and promote the V5 orchestrator.

### ⚠️ Forensic Recovery: Missed Requirements
*   **Context Synchronization**: A shared state ledger (e.g., `.v5_state.json`) is required so modular components don't experience amnesia during handovers.
*   **Larynx-Awareness**: The new modular Ignition needs a direct health-link to the Foyer, using the Vocal Handshake as a definitive readiness signal (not just guessing).
*   **Log Compatibility**: Renaming `fuel` to `interest` requires a "Legacy Parser" or a clean cut-over point to ensure old `evaluation_batch_*.log` files don't break during replay.

---

## 🧪 4. DEFERRED SEMANTIC CERTIFICATION
*Applying BKM-032 to the Refactor.*

1.  **Phase A (The Hard Switch)**: Automated batch verify that all ports bind and the "Interest" scalar still calculates correctly (0.2/0.6 logic).
2.  **Phase B (The Voice Audit)**: Gemini CLI (AI Reviewer) reads the "Deep Thought" traces. 
    *   **Check**: Does Pinky address the local node as "Brain" correctly?
    *   **Check**: Does the "Interest Decay" feel natural vs. the old "Fuel" jitter?
    *   **Check**: Does the system stay vocal during the H2 -> V5 startup?

---

### ⚖️ LEAD ENGINEER REVIEW REQUIRED
*This plan is an artifact for Sprint 31. No code changes have been made.*
