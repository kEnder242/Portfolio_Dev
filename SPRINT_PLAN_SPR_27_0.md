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
