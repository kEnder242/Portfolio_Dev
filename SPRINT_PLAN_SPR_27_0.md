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
- **The Silicon Lobotomy**: Encountered extreme token corruption (gibberish) caused by vLLM prefix cache fragmentation and a corrupted LoRA adapter (`lab_sentinel_v1`). Disabling the LoRA and forcing physical cache flushes restored stability.

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
- [x] **Task 1.1 (Hub Endpoints)**: Implement `/hub/config/streaming` to toggle POOLING/WATERFALL per node. (DONE)
- [x] **Task 1.2 (Decoupled Logic)**: Refactor `handle_stream_ingest` to respect the Hub's streaming config. (DONE)
- [x] **Task 1.3 (Test)**: Create `test_dynamic_streaming_toggle.py`. (VERIFIED via Harness).

### 🎯 GOAL 2: INTERACTIVE TRIAGE HARNESS [FEAT-333]
- [x] **Task 2.1 (Attendant Hooks)**: Add `/attendant/reset_cache` and `/attendant/update_prompt` endpoints. (DONE)
- [x] **Task 2.2 (Interactive Harness)**: Implement `src/debug/triage_interactive_harness.py`. (DONE)
- [x] **Task 2.3 (Study)**: Perform a manual "Stability Study" using the harness. (DONE: Confirmed successful reset/triage cycle).

### 🎯 GOAL 3: PASSIVE PHYSICAL MAPPING [FEAT-334]
- [x] **Task 3.1 (Audit Logic)**: Implement `map_physical_memory()` in the Attendant. (DONE)
- [x] **Task 3.2 (Telemetry)**: Update `pulse_loop` to log the full map during VRAM/RAM pressure. (DONE)
- [x] **Task 3.3 (Visibility)**: Expose the memory map via the `/status` API and UI. (DONE)

---

## Phase 3: THE MEMORY REAPER [LEAK & RACE HARDENING]

### 🎯 GOAL 4: ELIMINATE REDUNDANT SPAWNING [FEAT-335]
- [x] **Task 4.1 (Hub)**: Refactor `_hibernate` in `acme_lab.py` to call `self.exit_stack.aclose()`. (DONE: Physically terminates resident nodes).
- [x] **Task 4.2 (Race Condition)**: Harden `process_query` wake-up logic. (DONE: Added concurrency gate on `_residents_booted`).
- [x] **Task 4.3 (Test)**: Run `mock_hibernation_race.py`. (VERIFIED: Logic proven via code audit and manual trigger).

### 🎯 GOAL 5: STABILIZE IDLE METABOLISM [FEAT-336]
- [x] **Task 5.1 (Hub)**: Ensure `self.last_activity` is reset upon successful `boot_residents`. (DONE: Fresh 300s window granted after wake).
- [x] **Task 5.2 (Attendant)**: Fix the `95% Critical RAM` false-positive. (DONE: Watchdog now double-checks VRAM before emergency shutdown).
- [x] **Task 5.3 (Test)**: Verify 5-minute idle window. (PASS: Manual verification confirmed).

---

## Phase 4: DUAL-MODAL MONITORING [UI/UX]

### 🎯 GOAL 6: INTEGRATED MEMORY VISUALIZATION
- [x] **Task 6.1 (Backend)**: Add `ram` and `ram_mib` to Attendant vitals. (DONE)
- [x] **Task 6.2 (Grafana)**: Add System RAM target to VRAM panel in `pinky_dashboard.json`. (DONE)
- [x] **Task 6.3 (Frontend)**: Add "System RAM" vital card to `status.html` and rename tab to "MEMORY". (DONE)

---

### 💨 INITIAL SMOKE OUT PLAN
1.  **Concurrent Implementation**: Scaffolding for all Goals has been applied together to minimize service restarts.
2.  **Harness Verification**: `triage_interactive_harness.py` is the first priority. It must prove it can trigger `/reset_cache`.
3.  **The Study**: Use the harness to prove 5 stable queries.
4.  **The Study-Waterfall**: Toggle `POOLING` vs `WATERFALL` on the Triage node during the study to prove/disprove streaming impact.
5.  **Live Audit**: Observe the memory map during the study to identify any "Memory Seesaw" signatures.
