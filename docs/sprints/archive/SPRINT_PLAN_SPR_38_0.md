# Sprint 38 – OpenAgent Swarm Shakedown, RAG Temporal Alignment, Triage Hardening & UI Polish

## Active Stories & Task Ledger

### Story 1: OpenAgent Swarm Shakedown & Model Tuning [Sisyphus / quick]
*   **Why**: Ensure OpenAgent's multi-agent orchestration and tools run cleanly on the RTX 4090 without prompt clobbering or VRAM resource exhaustion. We must restore agent-specific specialization by removing model-level overrides and verify tool delegation.
*   **Design**:
    *   Scrap model-level `systemPrompt` fields in `opencode.json` that clobber the default agent-specific system prompts from `oh-my-openagent` (restoring the "not alone" swarm delegation prompt).
    *   Draft a multi-agent shakedown task ("Role Call" verification) with Sisyphus and Prometheus to confirm they can plan and coordinate locally.
    *   Configure `devstral` with a reduced context window (e.g. 16K) in the backlog to test its viability as a backup worker.
*   **Tasks**:
    *   [x] Scrap model-level `systemPrompt` from `/home/jallred/.config/opencode/opencode.json` for Sisyphus / Qwen.
    *   [x] Run a local OpenAgent shakedown test to verify name session persistence and tool delegation.
    *   [ ] Register `devstral:24b` with a 16K context limit as a backup alias in `opencode.json` and document the VRAM impact.
*   **Verification Gate**:
    *   [x] Execute `opencode session list` and confirm named session persists across successive tool invocations.
    *   [x] Audit VRAM usage via `ollama ps` during active swarm execution; verify context footprint is optimized and does not trigger OOM or severe swapping on the 4090.

### Story 2: RAG Adaptive Temporal Compass & Context Poisoning Mitigation [hephaestus / unspecified-high]
*   **Why**: Prevent "Archive Silence" deadlocks and temporal data gaps (like the missing 2017 accomplishments) while maintaining strict year validation to avoid context leakage.
*   **Design**:
    *   Implement **Adaptive Temporal Windowing** in `archive_node.py`'s `get_context()`: If a strict year check returns fewer than 2 results, autonomously widen the search filter to a $\pm 1$ year window (e.g. 2016-2018 for 2017 queries) with Gaussian decay weighting, capturing adjacent career accomplishments.
    *   Add a `/reset` or `/topic` intent handler in `intercom_v2.js` and `cognitive_hub.py` to allow the user to clear the conversational history buffer, mitigating context poisoning.
*   **Tasks**:
    *   [x] Refactor strict year filtering in `/home/jallred/Dev_Lab/HomeLabAI/src/nodes/archive_node.py` to dynamically degrade to an adjacent year range ($\pm 1$ year) when the target year is "thin" (fewer than 2 matched entries). [REVISED: Implemented Year-Range parsing to match range-labeled files like 2016-2019 for target year 2017].
    *   [x] Implement a `/reset` or `/topic` input handler in `intercom_v2.js` to clear `sessionStorage` history.
    *   [x] Implement context memory clearing in `/home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py` when the reset token is received.
*   **Verification Gate**:
    *   [x] **RAG Range Test:** Run a test script executing `get_context(query="2017 achievements")` and assert it successfully pulls anchors from range-labeled files like `2016_2019.json` instead of returning empty context.
    *   [x] **Backend Reset Integration Test:** Create a mock client script `tests/test_reset_flow.py` to assert that receiving the reset token clears the cognitive hub's short-term conversation context list.
    *   [x] **Frontend Session Clear Test:** Enter `/reset` in the browser console/chat input and verify browser `sessionStorage` keys are emptied and the message log is refreshed.

### Story 3: Vibe Alignment and Triage Rule Hardening [Sisyphus-Junior / quick]
*   **Why**: Harden the triage sentinel to recognize self-referential debugging and meta-conversations (e.g. status of ChromaDB, agent behavior issues) and map them cleanly to the `META` vibe.
*   **Design**:
    *   Update `LAB_SYSTEM_PROMPT` in `lab_node.py` to add an explicit `META` intent classification rule.
    *   Update `cognitive_hub.py` to add explicit `vibe_tone` guidance mappings for `OPERATIONAL` and `ANALYTICAL` vibes.
*   **Tasks**:
    *   [x] Modify `/home/jallred/Dev_Lab/HomeLabAI/src/nodes/lab_node.py` to add the rule mapping self-diagnostics, context health, and ChromaDB queries to the `META` vibe.
    *   [x] Update `/home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py` to add specific tone guidance strings for `OPERATIONAL` and `ANALYTICAL` vibes.
*   **Verification Gate**:
    *   [x] **Sentinel Dry-Run:** Run a dry-run test queries (e.g. *"is ChromaDB sync complete?"* or *"check the lab attendant status"*) and verify the triage JSON output maps `vibe` to `META` or `OPERATIONAL` rather than `TECHNICAL` or `CASUAL`.

### Story 4: Web Intercom JSON Pretty-Printing [Sisyphus-Junior / quick]
*   **Why**: Format arbitrary JSON responses (e.g. tool output, critic scores, triage logs) inline within the console to improve developer readability without introducing nested scrollbars.
*   **Design**:
    *   Update `appendMsg` in `intercom_v2.js` to detect JSON strings. If valid, format the JSON with indentation in an inline `<pre class="json-pretty-print">` block with `white-space: pre-wrap;` and no nested scrolling.
*   **Tasks**:
    *   [x] Refactor `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/intercom_v2.js` to parse and render JSON blocks inline in a clean, non-scrollable monospace container.
*   **Verification Gate**:
    *   [x] **JSON Inline Render:** Send a status check or query that outputs structured JSON in the Intercom browser UI; verify it displays pretty-printed with clean tab indentation and wraps words without generating a nested scrollbar.

---

## Sprint 38: Load-Balanced Swarm Strategy (Added 2026-07-09)
- **Strategy**: Leverage specialized swarm agents for RAG logic (`hephaestus`), UI/JS (`Sisyphus-Junior`), local integration compute (`atlas`), and quality gating (`momus`, `oracle`).
- **Objective**: Replace 'Sovereign' references and optimize delegation based on swarm capability mapping in `oh-my-openagent.json`.
- **Task Distribution**:
    - RAG Logic (`archive_node.py`): Delegated to `hephaestus` [unspecified-high].
    - UI Handler (`intercom_v2.js`): Delegated to `Sisyphus-Junior` [quick].
    - Verification/Test Execution: Delegated to `atlas` (Local 4090) [unspecified-high].
    - Codebase Sanitization ('Sovereign' removal): Parallelized `Sisyphus-Junior` task [quick].
    - Post-edit Workflow: Mandatory `build_site.py` execution for asset refresh.
