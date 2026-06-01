# SPRINT 31: THE GREAT BRAIN AWAKENING [REFACTOR PLAN]
**Status:** PLANNING | NO EXECUTION PERMITTED

## 🎯 MISSION
Execute an architectural refactor to align the Lab's terminology and file structure with the Phase 15 "Neural Relay" reality. We will promote local reasoning to "The Brain," transform the 4090 into the "Deep Thought" action, and move from monolithic management to modular "Appliance-Grade" services.

---

## 🧠 1. THE CONSCIOUSNESS SHIFT (Metric Promotion)

### 📈 Metric Shift: Fuel -> INTEREST
*   **Pedigree & Intent**: *"We aren't budgeting for tokens anymore; we're reasoning for depth. If the Lab is genuinely 'interested' in a topic, it should have the autonomy to keep digging. Interest is the new fuel."* — Lead Engineer.
*   **Strategies**:
    *   **A: Static Keyword List**: Maintain a list of "High-Value" words to trigger deep thinking (Rejected: High drift risk).
    *   **B: JSON-based Interest Anchors**: Use `intent_anchors.json` to map interest scores to specific domains (Rejected: Too rigid).
    *   **C: Recursive Topic Scoring (Linguistic Resonance)**: Derive interest from the semantic overlap between the current query, the `resonant_history`, and established technical domains. (**Selected: Best**).
*   **Implementation**: 
    *   Purge `intent_anchors.json` and all hardcoded keyword list dependencies.
    *   Refactor `CognitiveHub.py`: `self.current_fuel` -> `self.interest_score`.
    *   Logic: The Brain evaluates the `interest_score` via linguistic resonance. If the score is high, it triggers multi-turn refinement. If low, it yields to high-fidelity brevity.

### 📚 Retrieval Shift: RRF Implementation
*   **Pedigree & Intent**: *"Exact technical matches (like PECISTRESSOR) are often lost in a purely semantic vector search. We need the rigor of Reciprocal Rank Fusion to ensure both the 'Vibe' and the 'Fact' surface correctly."* — Lead Engineer.
*   **Strategies**:
    *   **A: Pure Vector Search**: Continue relying on ChromaDB semantic similarity (Rejected: Lost acronym precision).
    *   **B: Keyword-Only Search**: Revert to BM25/Grep for technical terms (Rejected: Lost semantic context).
    *   **C: RRF Hybrid Retrieval [BKM-032]**: Merge vector scores with exact-match frequency rankings to surface "Star" technical artifacts. (**Selected: Best**).

---

## 🗄️ 2. THE MEMORY BRIDGE (Refinement & Persistence)

### 📋 Topical RAG Cache (The Clipboard)
*   **Pedigree & Intent**: *"RAG shouldn't be a one-shot lookup. We need to build up a 'mental clipboard' of context over several turns, refining the truth as the conversation deepens. It's about cumulative synthesis, not isolated pings."* — Lead Engineer.
*   **Strategies**:
    *   **A: Stateless RAG**: Every turn performs a fresh, isolated search (Rejected: Loss of refinement).
    *   **B: Permanent Whiteboard**: Save all search results to `whiteboard.md` (Rejected: Too much noise for the primary reasoning path).
    *   **C: Topical RAG Cache (Clipboard)**: Implement a session-scoped "Clipboard" in `ArchiveNode.py` that allows refining and building up RAG info Turn-over-Turn, flushed only on major topic shifts. (**Selected: Best**).

### ❄️ The Hibernation Rule
*   **Pedigree & Intent**: *"When the Lab goes to sleep (H2), I don't want to lose the thread of where we were. Keep the conversation history, but discard the heavy context cache so we start the next session with a lean mind but a long memory."* — Lead Engineer.
*   **Strategies**:
    *   **A: Full Session Persistence**: Persist the entire VRAM state and cache during sleep (Rejected: High resource overhead/thrashing).
    *   **B: Complete State Wipe**: Clear all history and buffers on hibernation (Rejected: Loss of cognitive thread).
    *   **C: Selective Persistence**: Preserve `message_history` in `acme_lab.py`, but discard the heavy RAG Clipboard and trigger `clear_thoughts()` on the thinking node. (**Selected: Best**).

---

## 📐 3. MODULAR ARCHITECTURE (Foundation Pillars)

### 🔬 Node Promotion: Shadow -> THE BRAIN
*   **Pedigree & Intent**: *"Shadow was originally a failover; the local 2080 Ti is now a primary participant in the Relay. Promoting it to THE BRAIN aligns our nomenclature with the new hierarchy of authority."* — Lead Engineer.
*   **Strategies**:
    *   **A: Maintain "Shadow" Terminology**: (Rejected: Misleading relative to current authority).
    *   **B: "Local Mind" Name**: (Rejected: Too clinical, lacks character resonance).
    *   **C: THE BRAIN Promotion**: Deprecate "Shadow." The local reasoning node is now **THE BRAIN**. The 4090 is accessed via the **Deep Thought** action. (**Selected: Best**).

### 🛠️ The v5 Appliance Split (Lab Attendant)
*   **Pedigree & Intent**: *"The v4 monolith is a single point of failure. Breaking the Attendant into 'Appliance-Grade' services ensures that a failure in the router doesn't kill the ignition logic."* — Lead Engineer.
*   **Strategies**:
    *   **A: Patch V4 Monolith**: (Rejected: Increasing technical debt).
    *   **B: Full Rewrite from Scratch**: (Rejected: Extreme regression risk).
    *   **C: Decomposed v5 Split**: Break logic into `ignition`, `lifecycle`, `router`, and `forensics` modules with stable API boundaries. (**Selected: Best**).

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
