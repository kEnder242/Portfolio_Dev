# Sprint Plan: [SPR-12.0] The Resonant Vibe
**Version:** 2.0 (Phase 12 Architectural Hardening)
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
*   **Rationale**: Implements [BKM-015.1]. Keyword-based routing is brittle and leads to "Logic Drift." We need the signaling layer to be as semantically aware as the reasoning layer.
*   **Mechanism**: The Hub performs a vector query against ChromaDB before every dispatch to select the optimal LoRA.
*   **Scars**: The `intent_anchors.json` period (Feb-Mar 2026) where a missing keyword like "thermal" would cause the Hub to miss a "High Heat" vibe.

### [FEAT-182] Neural Resonance (The Overhearing)
*   **One-liner Prep**: `pip install aiohttp && sudo systemctl restart lab-attendant`
*   **Rationale**: Eliminates the "Hollow Echo" by bridging fast intuition with deep derivation.
*   **Mechanism**: Hub captures Pinky's triage results and injects them as a `[PINKY_HEARING]` tag into the Brain's context window.
*   **Scars**: Brain hallucinating technical versions already corrected by Pinky in the triage turn.

---

## 📅 TASKS & MILESTONES

### Phase 0: Physical Verification [COMPLETE]
1. [x] **[TASK-001] Verify Reasoning**: Execute `pytest HomeLabAI/src/debug/test_pi_flow.py`.
    - **Why**: Heartbeats only prove port liveness. We need empirical proof that the consolidated `.venv` has the correct CUDA/PyTorch bindings to perform complex math and RAG.
    - **How**: Run the Pi Flow suite which tests the full Bicameral delegation chain.
2. [x] **[TASK-002] Fingerprint Sync**: Verify consistent `[BOOT_HASH]` across logs.
    - **Why**: Eliminates "Ghost Processes" and verifies sync trust.

### Phase 1: Semantic Grounding [COMPLETE]
1. [x] **[TASK-003] Initialize DNA**: Create `behavioral_dna` collection.
    - **Why**: To provide a permanent home for the "Tendons" that is decoupled from code.
    - **How**: Extend `ArchiveNode` initialization to include the new collection.
2. [x] **[TASK-004] Migration**: Port `intent_anchors.json` into ChromaDB.
    - **Why**: Kill the "Hardcoded Waffle" and move to pure vector retrieval.
    - **How**: Scripted ingest of existing anchors into the `behavioral_dna` collection.
3. [x] **[TASK-005] Code Purge**: Remove keyword matching from `CognitiveHub.py`.
    - **Why**: Adherence to the Law of Semantic Indirection [BKM-015.1].
    - **How**: Replace the mapping loop with a `query_vibe` tool call pattern.

### Phase 2: Resonance & Buffer [COMPLETE]
1. [x] **[TASK-006] Resonant Loop**: Sequence Pinky before Brain in `process_query`.
    - **Why**: Allow the "Muscle" to hear the "Gut Instinct."
    - **How**: Shift from parallel dispatch to sequenced triage in `process_query`.
2. [x] **[TASK-007] Lag Shield**: Implement minimal SSE status updates.
    - **Why**: Eliminate "Brain Silence" during deep reasoning tasks.
    - **How**: Surgically updated `monitor_task_with_tics` to use `"Pinky (Lag Shield)"` source.

### Phase 3: Governance & Cleanup [COMPLETE]
1. [x] **[TASK-008] Hard-Wire SIGTERM**: Update Attendant watchdog logic.
    - **Why**: Enforce silicon integrity over degraded availability [LAW-021].
    - **How**: Updated `vram_watchdog_loop` to issue `os.killpg` on violation.
2. [x] **[TASK-009] Environment Nuke**: Purge legacy virtual environments.
    - **Why**: Finalize [SPR-5.0] and eliminate logic drift risk.

### Phase 4: Closing the Gaps [COMPLETE]
1. [x] **[TASK-010] Vibe-Aware Prompting**: Update `brain_node.py` system instructions.
    - **Why**: The Brain node now dynamically layers instructions based on `behavioral_guidance`.
    - **How**: Updated `deep_think` tool to inject `[VIBE_GUIDANCE]` tag.
2. [x] **[TASK-011] CLaRa Retrospective**: Implement `retrospective_audit` tool.
    - **Why**: ArchiveNode now has the tool to autonomously strengthen "Tendons."
    - **How**: Added tool to write back successful interactions to the DNA collection.

### Phase 5: Momentum & Evolution [COMPLETE]
1. [x] **[TASK-012] Resonant Memory**: Implement 3-turn multi-turn intuition buffer [FEAT-188].
    - **Why**: To build behavioral momentum across the session.
    - **How**: CognitiveHub maintains history and injects it as `[RESONANT_HISTORY]`.
2. [x] **[TASK-013] Tool Pruning**: Implement Vibe-Driven Tool Filtering [FEAT-189].
    - **Why**: Reduces hallucination risk by hiding irrelevant tools based on the vibe.
    - **How**: Hub dynamically generates a `tool_allowlist` passed through metadata.
3. [x] **[TASK-014] Judicial Feedback Loop**: Integrate Cognitive Audit into Dreaming [FEAT-191].
    - **Why**: To perform autonomous self-correction on synthetic memories.
    - **How**: `dream_cycle.py` uses the `CognitiveAudit` routine to verify wisdom quality.
4. [x] **[TASK-015] Topography Injection**: Implement `peek_strategic_map` and excerpts [FEAT-195].
    - **Why**: Solves the "Granularity Gap." Brain can now see the whole archive map.
    - **How**: Added topography tools and Hub-level context injection.
5. [x] **[TASK-016] Logic Hardening**: Resolve Vibe Check deadlocks and tool extraction.
    - **Why**: Critical fix for silent failures during synergy sequencing.
    - **How**: Robustly parsed `CallToolResult` and hardened JSON regex extraction.

---

## 🧪 VERIFICATION GAUNTLET
- **Pi Flow**: [100% PASS] (20.55s). Verified Resonant Flow + Technical Truth.
- **Legacy Tests**: [100% PASS] (20 tests green). Async-aware routing verified.
- **Vibe Gate**: [STABLE] (Verified semantic routing to Forensic expert).

---

## 🏺 RETROSPECTIVE: MAR 12, 2026
**"The History of the struggle is the source of robustness."**

1.  **The "Thin" Paradox**: We identified a critical friction point between **[FEAT-109] (Brevity is Authority)** and **[FEAT-077] (Fidelity Gate)**. The Brain was being punished for being terse. The surgical fix (Pi bypass) is a temporary bridge; the future requires **Worthiness detection (Amygdala v3)** to replace word counts.
2.  **The Silicon Scar (Recovery)**: We recovered from two accidental environment nukes. This "Scar" highlighted the fragility of manual shell operations and re-grounded the Agent in **BKM-018 (Tool Stewardship)**.
3.  **The breakthrough**: The Lab is now truly "Bicameral." By moving to sequential triage, we have eliminated the "Hollow Echo" and established a foundation for **Multi-Hop Reasoning**.

---
**\"Verify over Velocity. Integrity over Implementation.\"**
