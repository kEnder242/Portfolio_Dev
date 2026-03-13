# Sprint Plan: [SPR-12.0] The Resonant Vibe
**Version:** 1.8 (Phase 12 Architectural Hardening)
**Goal:** Transition from rigid, keyword-based orchestration to an emergent synergy between Pinky and the Brain.

---

## 📖 THE STORY: FROM ECHO TO RESONANCE
For months, the Lab has operated in a state of **"Hollow Parallelism."** Pinky would intuit, the Brain would derive, and the Hub would bundle. But they were deaf to one another. Pinky’s fast assessment of a driver crash never reached the Brain’s deep reasoning window; instead, the Brain would start from zero, often missing the very clues Pinky had already identified. 

We attempted to fix this with "Intent Anchors," but we fell into the **"Hardcoded Waffle"** trap—replacing code-based `if/else` loops with JSON-based `if/else` loops. It was a static solution for a dynamic mind. 

With the breakthrough of the **Unified 3B Base**, we now have the VRAM headroom to stop "guessing" intent. We are moving from **Keywords to Vibes**. We are building the **Tendons**—the semantic connections that allow the **Muscle** (LLM) to finally feel the **Bones** (Data). This sprint is about making the Lab "Overhear" its own thoughts.

---

## 🚀 ACTIVE INITIATIVES (BKM PROTOCOL)

### [FEAT-181] Behavioral DNA Registry (The Tendons)
*   **One-liner Prep**: `ArchiveNode.call_tool("initialize_collection", {"name": "behavioral_dna"})`
*   **Rationale**: Implements [BKM-015.1]. Semantic signaling over rigid keyword matching.
*   **Mechanism**: The Hub performs a vector query against ChromaDB before every dispatch to select the optimal LoRA.
*   **Scars**: routing failures when specific keywords (e.g., "thermal") were missing.

### [FEAT-182] Neural Resonance (The Overhearing)
*   **One-liner Prep**: `pip install aiohttp && sudo systemctl restart lab-attendant`
*   **Rationale**: Eliminates the "Hollow Echo" by bridging fast intuition with deep derivation.
*   **Mechanism**: Injects `[PINKY_HEARING]` into the Brain's context window.
*   **Scars**: Brain hallucinating technical versions already corrected by Pinky.

---

## 📅 TASKS & MILESTONES

### Phase 0: Physical Verification [COMPLETE]
1. [x] **[TASK-001] Verify Reasoning**: Execute `pytest HomeLabAI/src/debug/test_pi_flow.py`.
    - **Why**: Mandatory gate to ensure the consolidated `.venv` has the correct silicon bindings (CUDA/PyTorch).
    - **How**: Run the Pi Flow suite which tests the full Bicameral delegation chain.
2. [x] **[TASK-002] Fingerprint Sync**: Verify consistent `[BOOT_HASH]` across logs.
    - **Why**: Eliminates "Ghost Processes" and verifies sync trust.

### Phase 1: Semantic Grounding [COMPLETE]
1. [x] **[TASK-003] Initialize DNA**: Create `behavioral_dna` collection.
    - **Why**: To provide a permanent home for the "Tendons" that is decoupled from code.
2. [x] **[TASK-004] Migration**: Port `intent_anchors.json` into ChromaDB.
    - **Why**: Kill the "Hardcoded Waffle" and move to pure vector retrieval.
3. [x] **[TASK-005] Code Purge**: Remove keyword matching from `CognitiveHub.py`.
    - **Why**: Adherence to the Law of Semantic Indirection [BKM-015.1].

### Phase 2: Resonance & Buffer [COMPLETE]
1. [x] **[TASK-006] Resonant Loop**: Sequence Pinky before Brain in `process_query`.
    - **Why**: Allow the "Muscle" to hear the "Gut Instinct."
2. [x] **[TASK-007] Lag Shield**: Implement minimal SSE status updates.
    - **Why**: Eliminate "Brain Silence" during deep reasoning tasks.

### Phase 3: Governance & Cleanup [COMPLETE]
1. [x] **[TASK-008] Hard-Wire SIGTERM**: Update Attendant watchdog logic.
    - **Why**: Enforce silicon integrity over degraded availability.
2. [x] **[TASK-009] Environment Nuke**: Purge legacy virtual environments.
    - **Why**: Finalize [SPR-5.0] and eliminate logic drift risk.

### Phase 4: Closing the Gaps [COMPLETE]
1. [x] **[TASK-010] Vibe-Aware Prompting**: Update `brain_node.py` system instructions.
    - **Why**: The Brain node now dynamically layers instructions based on `behavioral_guidance`.
2. [x] **[TASK-011] CLaRa Retrospective**: Implement `retrospective_audit` tool.
    - **Why**: ArchiveNode now has the tool to autonomously strengthen "Tendons."

### Phase 5: Momentum & Evolution [ACTIVE]
1. [ ] **[TASK-012] Resonant Memory**: Implement multi-turn intuition buffer [FEAT-188].
    - **Why**: To build behavioral momentum across the session.
    - **How**: CognitiveHub maintains a 3-turn history of Pinky's assessments and injects them as a `[RESONANT_HISTORY]` block.
2. [ ] **[TASK-013] Tool Pruning**: Implement Vibe-Driven Tool Filtering [FEAT-189].
    - **Why**: Reduces hallucination risk by hiding irrelevant tools based on the vibe.
    - **How**: Hub dynamically generates a `tool_allowlist` for the Brain based on the retrieved vibe.
3. [ ] **[TASK-014] Judicial Feedback Loop**: Integrate Cognitive Audit into Dreaming [FEAT-191].
    - **Why**: To perform autonomous self-correction on synthetic memories.
    - **How**: `dream_cycle.py` uses the `CognitiveAudit` routine to verify "Diamond Wisdom" candidates before committing them.

---

## 🧪 VERIFICATION GAUNTLET
- **Pi Flow**: [HEARING VERIFIED] (Sequencing is correct, latency timeout observed).
- **Legacy Tests**: [REPAIRED] (All intent/routing tests are green).
- **Vibe Gate**: [STABLE] (Verified semantic routing to Forensic expert).

---
**\"Verify over Velocity. integrity over Implementation.\"**
