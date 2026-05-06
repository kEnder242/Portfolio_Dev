# 🏛️ SPRINT 27: THE GOVERNOR'S GATE [RESOURCE HARDENING]
**Tier:** System Integrity | **Target:** vLLM 3B stability | **Window:** May 2026

## 🎯 GOAL 1: MANAGED BACKGROUND WORKERS [FEAT-330]
- [ ] **Task 1.1 (Refactor)**: Refactor `mass_scan.py` to register as a 'Resident Node' in the Attendant ledger.
- [ ] **Task 1.2 (Signal)**: Implement `SIGUSR1` / `SIGUSR2` hooks in workers for remote Throttling (Throttled by Attendant if RAM > 85%).
- [ ] **Task 1.3 (Unified)**: Update `refine_gem` to call the Hub's MCP `think` tool instead of launching standalone `llama3` processes.

## 🎯 GOAL 2: HARDENED LOCKDOWN [FEAT-331]
- [ ] **Task 2.1 (Hub)**: Enforce `MAINTENANCE` gate in `acme_lab.py`. If status is MAINTENANCE, return a silent "Dream Cycle in progress" instead of sparking ignition.
- [ ] **Task 2.2 (ALARM)**: Audit all 2:00 AM tasks to ensure they call the `/lockdown` API before starting.
- [ ] **Task 2.3 (Recovery)**: Implement an 'OOM Quiescence' window (120s) to allow kernel socket reclamation after silent deaths.

## 🎯 GOAL 3: STABILITY GAUNTLET [TEST-45]
- [ ] **Task 3.1 (Mock)**: Create a mock memory-pressure script to simulate the 2:17 AM OOM event.
- [ ] **Task 3.2 (Gauntlet)**: Adapt `test_lifecycle_gauntlet.py` into `test_background_stability.py`.
- [ ] **Task 3.3 (Validation)**: Verify that `[ME]` queries are gracefully rejected during active maintenance.

---

## 🏗️ ARCHITECTURAL CONTEXT
- **Root Cause**: Anarchy between `mass_scan.py` (Refinement) and `acme_lab.py` (Foyer) on a shared 16GB RAM budget.
- **The Shift**: Moving from "Passive Observation" to "Active Governor." The Attendant must be able to `SIGSTOP` workers to save the Hub.
- **Model Efficiency**: Standardizing on the vLLM MCP tool for background tasks removes the 5GB Llama3-Ollama overhead.

## 🏺 REFERENCE ANCHORS
- **Physical BKM**: BKM-026 (RAM Contention Mitigation).
- **Test Template**: `HomeLabAI/src/tests/test_lifecycle_gauntlet.py`.
- **Scar Trace**: 02:17 AM Silent Hub Death (May 6, 2026).
