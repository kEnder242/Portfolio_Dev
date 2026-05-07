# 🏛️ SPRINT 27: THE GOVERNOR'S GATE [RESOURCE HARDENING]
**Tier:** System Integrity | **Target:** vLLM 3B stability | **Window:** May 2026
## 🏛️ SPRINT 27: GOALS & OBJECTIVES

### 🎯 GOAL 1: MANAGED BACKGROUND WORKERS [FEAT-330]
- [x] **Task 1.1 (Refactor)**: Refactor `mass_scan.py` to register as a 'Resident Node'. (DONE)
- [x] **Task 1.2 (Signal)**: Implement `SIGUSR1` / `SIGUSR2` hooks in workers for remote Throttling. (VERIFIED: Signal reception confirmed).
- [x] **Task 1.3 (Unified)**: Update `refine_gem` to call the Hub's MCP `think` tool via `McpClient`. (DONE: 5GB RAM reduction verified).

### 🎯 GOAL 2: HARDENED LOCKDOWN [FEAT-331]
- [x] **Task 2.1 (Hub)**: Enforce `MAINTENANCE` gate in `acme_lab.py`. (VERIFIED: [ME] queries blocked during lockdown).
- [x] **Task 2.2 (ALARM)**: Audit all 2:00 AM tasks to ensure they call the `/lockdown` API. (DONE).
- [x] **Task 2.3 (Recovery)**: Implement an 'OOM Quiescence' window (240s) for kernel reclamation. (DONE).

### 🎯 GOAL 3: STABILITY GAUNTLET [TEST-45]
- [x] **Task 3.1 (Mock)**: Create a mock memory-pressure script `mock_worker.py`. (DONE).
- [x] **Task 3.2 (Hardening)**: Hardened Attendant to use edge-triggered signaling to prevent log spam. (DONE).
- [x] **Task 3.3 (Validation)**: Run `test_lockdown_enforcement.py` and `test_strategic_live_fire.py`. (PASS).

---

## 🤕 SCARS & RETROSPECTIVE [BKM-029]
- **The Telemetry Storm**: Initial governor implementation was pulse-triggered (every 2s). During the mock test, this caused a feedback loop of thousands of `RESUME` signals, truncating the CLI session.
- **Fix**: Re-implemented as **Edge-Triggered**. Signals are now only sent when crossing the 85% (Pause) or 70% (Resume) boundary.

---

## 🏗️ ARCHITECTURAL CONTEXT
- **Root Cause**: Anarchy between `mass_scan.py` (Refinement) and `acme_lab.py` (Foyer) on a shared 16GB RAM budget.
- **The Shift**: Moving from "Passive Observation" to "Active Governor." The Attendant must be able to `SIGSTOP` workers to save the Hub.
- **Model Efficiency**: Standardizing on the vLLM MCP tool for background tasks removes the 5GB Llama3-Ollama overhead.

## 🏺 REFERENCE ANCHORS
- **Physical BKM**: BKM-026 (RAM Contention Mitigation).
- **Test Template**: `HomeLabAI/src/tests/test_lifecycle_gauntlet.py`.
- **Scar Trace**: 02:17 AM Silent Hub Death (May 6, 2026).

---

## Phase 2: THE PHYSICIAN'S LENS [DIAGNOSTIC HARDENING]

### 🎯 GOAL 1: DYNAMIC STREAMING MODES [FEAT-332]
- [ ] **Task 1.1 (Hub)**: Implement a `/hub/config/streaming` endpoint.
    - *Reasoning*: Enables dynamic control to test if streaming interrupts cause prefix cache misalignment.
    - *Context*: Add to `acme_lab.py` around line 1800 near existing stream routes.
    - *Design*: Use a simple key-value store in the Hub to track per-node `pooling` vs `waterfall`.
- [ ] **Task 1.2 (Logic)**: Refactor `on_token` in `cognitive_hub.py` to check the dynamic `streaming_mode` state.
    - *Reasoning*: Decouples internal state from UI broadcasting, allowing for transparent "Pooling" when debugging.
    - *Context*: Modify `cognitive_hub.py` line 52.
    - *Design*: Buffer tokens in `self.session_buffers` but skip `broadcast` if `pooling == True`.
- [ ] **Task 1.3 (Test)**: Create `test_dynamic_streaming_toggle.py`.
    - *Reasoning*: Verifies that switching modes mid-stream behaves correctly without data loss.
    - *Context*: New file in `src/tests/`.
    - *Design*: Send a multi-token query, toggle mode mid-way, and verify UI output vs log output.

### 🎯 GOAL 2: INTERACTIVE TRIAGE HARNESS [FEAT-333]
- [ ] **Task 2.1 (Attendant Hooks)**: Add `/attendant/reset_cache` and `/attendant/update_prompt` endpoints.
    - *Reasoning*: Provides a "Path to Healing" without requiring a full Lab restart, saving critical debug time.
    - *Context*: Add to `lab_attendant_v4.py` using `register_route` (line 217).
    - *Design*: Calls `torch.cuda.empty_cache()` and vLLM's internal `/reset_prefix_cache`.
- [ ] **Task 2.2 (Harness)**: Implement `src/debug/triage_interactive_harness.py`.
    - *Reasoning*: Enables manual single-cycle iteration to prove Triage stability before scaling to automation.
    - *Context*: New file in `src/debug/`.
    - *Design*: Interactive CLI that wraps prompt updates, cache clearing, and triage triggering.
- [ ] **Task 2.3 (Study)**: Perform a manual "Stability Study."
    - *Reasoning*: Establifies a baseline of "5 consecutive stable queries" to prove the fix before regression testing.
    - *Context*: Manual process using the Task 2.2 harness.
    - *Design*: Record results in `triage_study.log` for future BKM derivation.

### 🎯 GOAL 3: PASSIVE PHYSICAL MAPPING [FEAT-334]
- [ ] **Task 3.1 (Audit Logic)**: Implement a `map_physical_memory()` function in the Attendant.
    - *Reasoning*: Provides ground-truth visibility into which processes (Accounting vs Ghosts) are consuming 16GB RAM.
    - *Context*: New method in `lab_attendant_v4.py` near `update_status_json` (line 1524).
    - *Design*: Uses `psutil` to iterate all processes and matches PIDs against the `ledger`.
- [ ] **Task 3.2 (Telemetry)**: Update the Attendant's `pulse_loop` to log the full map during pressure events.
    - *Reasoning*: Replaces "Aggressive Hibernation" with "Informed Governance" by logging forensic state before action.
    - *Context*: Modify `lab_attendant_v4.py` `pulse_loop` around line 320.
    - *Design*: Conditional trigger when `RAM > 90%` to write a memory snapshot to `attendant_forensic_day.log`.
- [ ] **Task 3.3 (Visibility)**: Expose this map via the `/status` API.
    - *Reasoning*: Transparently reflects the internal state mapping to the UI as requested.
    - *Context*: Update `update_status_json` in `lab_attendant_v4.py` (line 1524).
    - *Design*: Add a `memory_map` field to the status JSON containing the Accounted/Ghost PID lists.

---

### 💨 INITIAL SMOKE OUT PLAN
1.  **Concurrent Implementation**: Goals 1, 2, and 3 will be implemented together to minimize service restarts.
2.  **Harness Verification**: The `triage_interactive_harness.py` will be the first tool tested. It must successfully trigger Attendant-level cache flushes and prompt updates.
3.  **Stability Study**: Once the harness is verified, it will be used to prove Triage stability. This includes toggling `POOLING` vs `WATERFALL` mid-test to determine if internal streaming load impacts gibberish frequency.
4.  **Live Audit**: The Physical Memory Mapping will be monitored 'live' during the stability study to capture the silicon footprint as it crosses the 90% VRAM threshold.
