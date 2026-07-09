# Sprint 38 – OpenAgent Swarm Shakedown, RAG Temporal Alignment, Triage Hardening & UI Polish

## Active Stories & Task Ledger

### Story 1: OpenAgent Swarm Shakedown & Model Tuning
*   **Why**: Ensure OpenAgent's multi-agent orchestration and tools run cleanly on the RTX 4090 without prompt clobbering or VRAM resource exhaustion. We must restore agent-specific specialization by removing model-level overrides and verify tool delegation.
*   **Design**:
    *   Scrap model-level `systemPrompt` fields in `opencode.json` that clobber the default agent-specific system prompts from `oh-my-openagent` (restoring the "not alone" swarm delegation prompt).
    *   Draft a multi-agent shakedown task ("Role Call" verification) with Sisyphus and Prometheus to confirm they can plan and coordinate locally.
    *   Configure `devstral` with a reduced context window (e.g. 16K) in the backlog to test its viability as a backup worker.
*   **Tasks**:
    *   [x] Scrap model-level `systemPrompt` from `/home/jallred/.config/opencode/opencode.json` for Sisyphus / Qwen.
    *   [ ] Run a local OpenAgent shakedown test to verify name session persistence and tool delegation.
    *   [ ] Register `devstral:24b` with a 16K context limit as a backup alias in `opencode.json` and document the VRAM impact.

### Story 2: RAG Adaptive Temporal Compass & Context Poisoning Mitigation
*   **Why**: Prevent "Archive Silence" deadlocks and temporal data gaps (like the missing 2017 accomplishments) while maintaining strict year validation to avoid context leakage.
*   **Design**:
    *   Implement **Adaptive Temporal Windowing** in `archive_node.py`'s `get_context()`: If a strict year check returns fewer than 2 results, autonomously widen the search filter to a $\pm 1$ year window (e.g. 2016-2018 for 2017 queries) with Gaussian decay weighting, capturing adjacent career accomplishments.
    *   Add a `/reset` or `/topic` intent handler in `intercom_v2.js` and `cognitive_hub.py` to allow the user to clear the conversational history buffer, mitigating context poisoning.
*   **Tasks**:
    *   [x] Refactor strict year filtering in `/home/jallred/Dev_Lab/HomeLabAI/src/nodes/archive_node.py` to dynamically degrade to an adjacent year range ($\pm 1$ year) when the target year is "thin" (fewer than 2 matched entries). [REVISED: Implemented Year-Range parsing to match range-labeled files like 2016-2019 for target year 2017].
    *   [ ] Implement a `/reset` or `/topic` input handler in `intercom_v2.js` to clear `sessionStorage` history.
    *   [ ] Implement context memory clearing in `/home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py` when the reset token is received.

### Story 3: Vibe Alignment and Triage Rule Hardening
*   **Why**: Harden the triage sentinel to recognize self-referential debugging and meta-conversations (e.g. status of ChromaDB, agent behavior issues) and map them cleanly to the `META` vibe.
*   **Design**:
    *   Update `LAB_SYSTEM_PROMPT` in `lab_node.py` to add an explicit `META` intent classification rule.
    *   Update `cognitive_hub.py` to add explicit `vibe_tone` guidance mappings for `OPERATIONAL` and `ANALYTICAL` vibes.
*   **Tasks**:
    *   [x] Modify `/home/jallred/Dev_Lab/HomeLabAI/src/nodes/lab_node.py` to add the rule mapping self-diagnostics, context health, and ChromaDB queries to the `META` vibe.
    *   [x] Update `/home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py` to add specific tone guidance strings for `OPERATIONAL` and `ANALYTICAL` vibes.

### Story 4: Web Intercom JSON Pretty-Printing
*   **Why**: Format arbitrary JSON responses (e.g. tool output, critic scores, triage logs) inline within the console to improve developer readability without introducing nested scrollbars.
*   **Design**:
    *   Update `appendMsg` in `intercom_v2.js` to detect JSON strings. If valid, format the JSON with indentation in an inline `<pre class="json-pretty-print">` block with `white-space: pre-wrap;` and no nested scrolling.
*   **Tasks**:
    *   [x] Refactor `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/intercom_v2.js` to parse and render JSON blocks inline in a clean, non-scrollable monospace container.

---

## Sprint 38 Timeline & Delegation Plan

The work is structured sequentially to stabilize the local swarm first, evaluate model footprint, and then delegate codebase modifications to OpenAgent.

### Phase 1: Local Swarm Stabilization (AGY)
*   **Who:** AGY (Main Co-Pilot).
*   **Tasks:**
    *   Fix local prompt templates, resolve provider configurations (done).
    *   Initialize and connect to a named local session using the Playbook protocol (`opencode run "SESSION: ..."`).
*   **Target Date/Status:** Active.

### Phase 2: Role Call Shakedown (AGY + User)
*   **Who:** AGY initiates / User verifies.
*   **Tasks:**
    *   Execute a basic "Role Call" query in the session to verify that Sisyphus (`qwen3:14b`) and Prometheus coordinate and delegate tasks cleanly without crashing.
*   **Target Date/Status:** Next immediately.

### Phase 3: VRAM & Context Footprint Audit (AGY + User)
*   **Who:** AGY + User.
*   **Tasks:**
    *   Run `ollama ps` during and after active swarm calls.
    *   Examine prompt context lengths to see if we need to restrict the context window size (e.g. setting num_ctx to 8K/16K) to save GPU resources.
*   **Target Date/Status:** Scheduled.

### Phase 4: Model Evaluation & Quant Selection (AGY + User)
*   **Who:** AGY + User.
*   **Tasks:**
    *   Download and test alternative models (e.g., Qwen-2.5-Coder-14B vs. Qwen3-14B, or Devstral with smaller context limits) to find the optimum balance of speed, tool capability, and memory usage.
    *   Settle on a permanent model configuration for the `SISYPHUS` and `CONDUCTOR` aliases.
*   **Target Date/Status:** Scheduled.

### Phase 5: Swarm Delegation for remaining stories (OpenAgent)
*   **Who:** OpenAgent Swarm (Delegated by AGY).
*   **Tasks:**
    *   Implement Story 2's `/reset` memory-clearing tasks:
        *   Modify `intercom_v2.js` to clear `sessionStorage` on `/reset`.
        *   Modify `cognitive_hub.py` to clear short-term context.
*   **Verification Gate:** AGY reviews OpenAgent git diffs and logs before committing.
*   **Target Date/Status:** Scheduled (Deferred until model selection is stable).
