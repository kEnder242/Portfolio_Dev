# Sprint Plan: [SPR-12.0] The Resonant Vibe
**Version:** 1.6 (Phase 12 Architectural Hardening)
**Goal:** Transition from rigid, keyword-based orchestration to an emergent synergy between Pinky and the Brain.

---

## 📖 THE STORY: FROM ECHO TO RESONANCE
For months, the Lab has operated in a state of **"Hollow Parallelism."** Pinky would intuit, the Brain would derive, and the Hub would bundle. But they were deaf to one another. Pinky’s fast assessment of a driver crash never reached the Brain’s deep reasoning window; instead, the Brain would start from zero, often missing the very clues Pinky had already identified. 

We attempted to fix this with "Intent Anchors," but we fell into the **"Hardcoded Waffle"** trap—replacing code-based `if/else` loops with JSON-based `if/else` loops. It was a static solution for a dynamic mind. 

With the breakthrough of the **Unified 3B Base**, we now have the VRAM headroom to stop "guessing" intent. We are moving from **Keywords to Vibes**. We are building the **Tendons**—the semantic connections that allow the **Muscle** (LLM) to finally feel the **Bones** (Data). This sprint is about making the Lab "Overhear" its own thoughts.

---

## 🚀 ACTIVE INITIATIVES

### [FEAT-181] Behavioral DNA Registry (The Tendons)
*   **BKM Protocol**:
    *   **One-liner Prep**: `ArchiveNode.call_tool("initialize_collection", {"name": "behavioral_dna"})`
    *   **Core Logic**: `vibe = chromadb.query(query_text).metadata['adapter_target']`
    *   **Trigger Points**: Entry into `CognitiveHub._route_expert_domain` during pre-gating.
    *   **Scars**: The `intent_anchors.json` period (Feb-Mar 2026) where a missing keyword like "thermal" would cause the Hub to miss a "High Heat" vibe, leading to standard routing instead of specialized telemetry handling.
*   **Rationale**: Implements [BKM-015.1]. Keyword-based routing is brittle and leads to "Logic Drift." We need the signaling layer to be as semantically aware as the reasoning layer.
*   **Mechanism**: Move `intent_anchors.json` logic into a `behavioral_dna` vector collection. The Hub performs a "Vibe Check" (semantic query) against this collection before every dispatch to select the optimal LoRA adapter.
*   **Proof**: `pytest src/tests/test_vibe_triggers.py` confirms routing to "Forensic" experts even when keywords like "history" or "search" are entirely absent.

### [FEAT-182] Neural Resonance (The Overhearing)
*   **BKM Protocol**:
    *   **One-liner Prep**: `pip install aiohttp && sudo systemctl restart lab-attendant`
    *   **Core Logic**: `brain_payload['system_prompt'] += f"[PINKY_HEARING]: {pinky_intuition}"`
    *   **Trigger Points**: Immediately following Pinky's `facilitate` completion and before Brain `deep_think` dispatch.
    *   **Scars**: The "Hollow Echo" of Phase 11 where the Brain would hallucinate technical versions that Pinky had already corrected in the triage turn, causing user confusion and loss of authority.
*   **Rationale**: Eliminates the "Hollow Echo Chamber" by ensuring Pinky's initial intuition informs the Brain's deep reasoning chain in real-time. Builds upon [FEAT-114] Sovereign Bridge and [FEAT-153] Resonant Chamber.
*   **Mechanism**: The Hub captures Pinky's `facilitate` result (Intuition) and injects it as a `[PINKY_HEARING]` block into the Brain's context window. This uses the [FEAT-172] Active Buffer mechanism to manage the "Silicon Gap" during high-latency derivations.
*   **Proof**: Brain's output explicitly acknowledges Pinky's insight (e.g., "I see Pinky's concern about the driver version, I will verify the RAPL registers specifically.")

### [FEAT-180] Graceful Resource Governance (Hard Stop)
*   **BKM Protocol**:
    *   **One-liner Prep**: `sudo sed -i 's/Restart=on-failure/Restart=always/' lab-attendant.service`
    *   **Core Logic**: `if vram_pct > 95: os.killpg(os.getpgrp(), signal.SIGTERM)`
    *   **Trigger Points**: Attendant `vram_watchdog_loop` (every 5 seconds).
    *   **Scars**: The "Logic Collapse" of Feb 13th where an Ollama fallback to a 1B model during a VRAM spike led to the Brain suggesting unstable shell commands due to reduced parameter count.
*   **Rationale**: Replaces [FEAT-069] Resilience Ladder. Fallbacks often result in "Logic Collapse." We prefer a clean "Hard Stop" to preserve system integrity as mandated by [LAW-021].
*   **Mechanism**: Hard-wires the Attendant's watchdog to trigger `SIGTERM` to the Lab Hub on VRAM/Load violation. This forces the Agent to resolve the bottleneck before proceeding.
*   **Proof**: Simulated resource spike triggers service termination and a 503 error to the client, verified via `journalctl`.

---

## 📅 TASKS & MILESTONES

### Phase 0: Physical Verification (The Gauntlet)
1. [ ] **[TASK-001] Verify Reasoning**: Execute `pytest HomeLabAI/src/debug/test_pi_flow.py`.
    - **Why**: Mandatory gate to ensure the consolidated `.venv` has the correct silicon bindings (CUDA/PyTorch).
    - **Proof**: 100% pass on the full Bicameral delegation chain.
2. [ ] **[TASK-002] Fingerprint Sync**: Verify consistent `[BOOT_HASH : COMMIT : ROLE]` across all logs.
    - **Why**: Eliminates "Ghost Processes" and verifies sync trust.
    - **Proof**: Heartbeat matches `attendant.log` entries word-for-word.

### Phase 1: Semantic Grounding (The Tendons)
1. [ ] **[TASK-003] Initialize DNA**: Create `behavioral_dna` collection in Archive Node.
    - **Why**: To provide a permanent home for the "Tendons" that is decoupled from code.
    - **How**: Extend `ArchiveNode` initialization to include the new collection.
2. [ ] **[TASK-004] Migration**: Port `intent_anchors.json` and `FEAT-069` thresholds into ChromaDB.
    - **Why**: Kill the "Hardcoded Waffle" and move to pure vector retrieval.
    - **How**: Scripted ingest of existing anchors as VIBE anchors.
3. [ ] **[TASK-005] Code Purge**: Remove keyword matching from `CognitiveHub.py`.
    - **Why**: Adherence to the Law of Semantic Indirection [BKM-015.1].
    - **How**: Replace mapping loop with a `query_vibe` tool call pattern.

### Phase 2: Resonance & Buffer (The Synergy)
1. [ ] **[TASK-006] Resonant Loop**: Modify Hub dispatch to sequence Pinky before Brain.
    - **Why**: Allow the "Muscle" to hear the "Gut Instinct."
    - **How**: Shift from parallel dispatch to sequenced triage in `process_query`.
2. [ ] **[TASK-007] Lag Shield**: Implement [FEAT-172] status updates.
    - **Why**: Eliminate "Brain Silence" during deep reasoning tasks.
    - **How**: Use the SSE `broadcast` mechanism to send Pinky's characterful status quips.

### Phase 3: Governance & Decommissioning (The Cleanup)
1. [ ] **[TASK-008] Hard-Wire SIGTERM**: Update Attendant watchdog logic.
    - **Why**: Enforce silicon integrity over degraded availability.
    - **How**: Modify `vram_watchdog_loop` to issue `os.killpg`.
2. [ ] **[TASK-009] Environment Nuke**: Remove legacy venvs (`.venv_vllm_017`, `HomeLabAI/.venv_legacy`).
    - **Why**: Finalize [SPR-5.0] and eliminate logic drift risk.
    - **Proof**: Disk usage reduction and confirmed removal of old binaries.

---

## 🌟 EMERGENT CONCEPTS

### [FEAT-184] Amygdala v2.1 (The Uncertainty Gate)
- **Rationale**: Keywords are a "Crutch." A true architect knows when a query is complex regardless of the specific words used.
- **Mechanism**: Use a tiny 1B model to score "Instructional Complexity." High scores trigger the Brain even if the Vibe retrieval is low-confidence.

### [FEAT-185] Alluring Instrumentation (Juicy Tooling)
- **Rationale**: LLMs are probabilistic. If a tool sounds like a "High-Precision Silicon Scalpel," the model is statistically more likely to use it accurately.
- **Mechanism**: Refactor all MCP tool descriptions to use "Validation Engineering" verbiage.

---

## 🧪 VERIFICATION GAUNTLET
- **Critical Gate**: `test_pi_flow.py` (Must pass before Phase 1).
- **Vibe Gate**: `test_vibe_triggers.py` (Verify semantic routing).
- **Resonance Gate**: `test_strategic_interjection.py` (Verify Brain overhears Pinky).

---
**\"Data should be the bones, LLM should be the muscle, and the flow that connects them the tendons.\"**
