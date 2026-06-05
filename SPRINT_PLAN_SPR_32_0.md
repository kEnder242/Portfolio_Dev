# SPRINT 32: THE RETRIEVAL RENAISSANCE
**Status:** PLANNING | NO EXECUTION PERMITTED

## 🎯 MISSION
Upgrade the Lab's serving core to vLLM 0.21.x, integrate the Qwen 3.6 family, and shift focus from *Inference Reason* to *Retrieval Precision*. We will move beyond "Monolithic RAG" into a sophisticated "Orchestration Memory" (OM) model.

---

## 🏗️ GOAL 1: SILICON MODERNIZATION (vLLM v0.21.0)
*Objective: Stabilize the latest serving stack to leverage native reasoning parsers and MRv2 latency gains.*

### 🛠️ The Serving Core
*   **Pedigree & Intent**: *"vLLM v0.21.x natively supports Qwen 3.6 and deep-integrated reasoning blocks. Upgrading eliminates our custom regex hacks for <think> extraction and increases throughput."* — Lead Engineer.
*   **Tasks**:
    *   [x] **Task 1.1 (The Upgrade)**: Upgrade the production `.venv` to vLLM 0.21.0 and Python 3.12 (Local 2080 Ti host only).
    *   [x] **Task 1.2 (Local Qwen 3.6)**: Migrate the 3B Unified Base (2080 Ti) to Qwen 3.6 FP8. Maintain "Lazy Adaptive" selection for the Sovereign (4090) to leverage whatever high-fidelity model is currently resident on Kender.
    *   [x] **Task 1.3 (Native Thinking)**: Enable `--reasoning-parser qwen3` (Local only) to allow the engine to handle internal reasoning blocks without breaking tool-calling streams.

---

## 🧠 GOAL 2: ORCHESTRATION MEMORY (OM & RAG)
*Objective: Apply the "RAG is not ML" philosophy [BKM-032] to build an Engineering Layer for Truth.*

### 📋 Context Precision (The High-Fidelity Brief)
*   **Pedigree & Intent**: *"The 4090 is a 'free' sovereign resource. We won't gate its thinking; we will feed it better context. By using the local Brain to distill RAG chunks into high-density memos, we minimize network latency and prevent context-window drowning."* — Lead Engineer.
*   **Tasks**:
    *   [ ] **Task 2.1 (Memo Layer)**: Implement a "Memo" caching layer that stores high-fidelity synthesized observations (OM) derived from nightly ALARM tasks.
    *   [ ] **Task 2.2 (Context Distillation)**: Implement the "Sovereign Brief" pattern. If the local Brain identifies relevant context, it distills it into a dense summary *before* dispatching to the 4090, ensuring the Sovereign node starts with high-fidelity technical anchors.
    *   [ ] **Task 2.3 (Memory-OS)**: Implement system-level eviction policies for the session RAG clipboard to prevent context-window "Drowning" in long sessions.

---

## 🧪 GOAL 3: SEMANTIC HARMONY
*Objective: Implement the "Mice Calling Each Other Out" pattern for autonomous self-correction.*

### ⚖️ The Inter-Node Audit
*   [ ] **Task 3.1 (Qualitative Vibe Scores)**: Refactor `cognitive_audit.py` to output [VIBE_RESONANCE] scalars rather than binary Pass/Fail.
*   [ ] **Task 3.2 (Neural Correction)**: Enable nodes to interject with "Off-Vibe" corrections in the chat, informing the next link in the Waterfall.

---

## ❄️ GOAL 4: STABLE HIBERNATION (VRAM Hygiene)
*Objective: Restore high-fidelity hibernation using the modular V5 architecture.*

### 🛠️ The Deep Sleep Cycle
*   **Pedigree & Intent**: *"Hibernation in V4 was a source of zombies. V5's decoupled architecture allows us to reap models and release VRAM safely while the Foyer remains online."* — Lead Engineer.
*   **Tasks**:
    *   [ ] **Task 4.1 (Subprocess Reaping)**: Implement strict subprocess termination in the Ignition Manager for AFK periods (>30 mins).
    *   [ ] **Task 4.2 (VRAM Vacuum)**: Verify that `vLLM` releases all GPU memory upon SIGTERM and that the `lab-vram.lock` is cleared.
    *   [ ] **Task 4.3 (Instant Wake)**: Ensure the Foyer can reliably trigger a fresh ignition upon the next user intent.

---

## 💎 STRETCH GOALS
*   [ ] **Neural Pager v2**: Use `memory-os` logic to alert on "Memory Fragmentation" (logical contradictions in retrieval).
*   [ ] **MTP Speculative Decoding**: Enable Multi-Token Prediction for Qwen 3.6 to reduce TPOT.
