# Sprint Plan: [SPR-21.0] WD Actions (Watchdog Sovereignty)
**Status:** DRAFT | **Goal:** Rebuild the Lab Attendant's internal watchdog as a "Multi-Modal State Monitor" to ensure resilient hibernation and recovery.

---

## 🏛️ Section 1: Brainstorming & Architecture (The "Why")

**Core Problem:** A deep forensic review confirmed that the `vram_watchdog_loop` in `lab_attendant_v4.py` is an empty stub. More importantly, there's a fundamental architectural conflict between the old "liveness" model (always on) and the new "hibernation" model (resource efficiency). The watchdog must be rebuilt not just to detect crashes, but to **validate state transitions**.

**The Watchdog's New Purpose: The "Multi-Modal State Monitor"**
The internal watchdog must evolve from a simple "is it on?" checker to a true "State Machine Monitor." It runs as a background `asyncio` task on the same event loop as the Attendant's REST API, giving it direct, thread-safe access to internal state (`self.is_hibernating`, `self.current_lab_mode`).

**Proposed Flow (Multi-Modal Reconstruction):**
1.  **State-Aware Monitoring**: The watchdog checks intended state before probing. It respects a 60s `boot_grace_period` and a `MAINTENANCE_LOCK`.
2.  **Multi-Modal Detection Rubric**:
    *   **VRAM Truth**: Check `pynvml`. Declare failure if `is_hibernating` is true but VRAM > 2000MB (ERR-09).
    *   **Port Liveness**: Poll `:8765/heartbeat`. Declare failure if Hub is unresponsive for 3 cycles (ERR-05).
    *   **Forensic Log Scanning**: Use the **TraceMonitor** to scan `server.log`, `attendant.log`, and `vllm_server.log` for Python Tracebacks or CUDA kernel errors.
    *   **Observability Health**: Check status of Docker containers (Prometheus, Grafana). Restart if DOWN.
3.  **Tiered Recovery & Forensic Logging**:
    *   **On Failure**: Capture "Last Words" log snippet via TraceMonitor.
    *   **Recovery**: Execute `mcp_hibernate` (Level 1) or `mcp_stop -> mcp_start` (Level 2).
    *   **Interleaved Log**: Inject recovery actions into `pager_activity.json` for visibility in `status.html`.

---

## 🔗 Section 2: Architectural Alignment

This plan restores core DNA from the Feature Tracker and archived `v1` logic:
*   **[FEAT-036] VRAM Guard**: Physical VRAM thresholds (85% Warning, 95% Critical).
*   **[FEAT-249] VRAM Hibernation Matrix**: State-aware monitoring of transition windows.
*   **[FEAT-035] Zombie Port Recovery**: Hub heartbeat polling.
*   **[FEAT-043] Dead-Man's Switch**: Autonomous full restart on persistent unresponsiveness.
*   **[FEAT-151] Forensic Trace Monitor**: Expanded to include `vllm_server.log`.

---

### 🛠️ Section 3: Tasks & Tracking (WD Sovereignty)

- [x] **Task 1: Rebuild Multi-Modal Watchdog Logic**
    - **Mechanism**: Implement the state-aware rubric in `vram_watchdog_loop`. Add checks for VRAM thresholds, Hub liveness, and Docker container status.
- [x] **Task 2: Implement Tiered Recovery**
    - **Mechanism**: In the loop, call `self.mcp_hibernate()` for hibernation failures and `self.mcp_stop()` for DEAD Hubs.
- [x] **Task 3: Implement Forensic Log Injection (vLLM Aware)**
    - **Mechanism**: Expand `TraceMonitor` to include `/home/jallred/Dev_Lab/HomeLabAI/vllm_server.log`. Inject discovered errors into `self.log_event()`.
- [x] **Task 4: Gemini CLI BKM-018 Compliance**
    - **Mechanism**: Gemini CLI MUST use `lab_stop` / `lab_start` for all cleanup. Manual `pkill` is strictly forbidden.

---
## 🧪 Section 4: Detailed Implementation Plan

### **Task 1: Multi-Modal Detection Rubric**
*   **Location**: `lab_attendant_v4.py` -> `vram_watchdog_loop`.
*   **Sub-Task 1.1: State Gates**: Respect `MAINTENANCE_LOCK` and `boot_grace_period`.
*   **Sub-Task 1.2: VRAM Thresholds**: If `used > (total * 0.95)`, trigger `cleanup_silicon()`.
*   **Sub-Task 1.3: Docker Monitoring**: Check Prometheus/Grafana containers; restart via `subprocess` if not running.
*   **Sub-Task 1.4: Heartbeat Latency**: Measure `aiohttp` response time. If > 5s for 3 cycles, log "DEGRADED" status.

### **Task 2 & 3: Recovery and Logging**
*   **Sub-Task 2.1: Forensic Capture**:
    *   Call `self.trace_monitor.get_last_trace()`.
    *   Identify source (Hub, Attendant, or vLLM).
*   **Sub-Task 2.2: Log Interleaving**:
    *   `self.log_event(f"[WATCHDOG] Recovery triggered. Last words: {snippet}", "CRITICAL")`.
*   **Sub-Task 2.3: Reset Sequence**: `await self.mcp_stop()` -> `await asyncio.sleep(5)` -> `await self.mcp_start()`.

---

## 🧹 Section 5: Scrub Report & Unfinished Items (April 15, 2026)
*A final review of historical documents and sprint plans to ensure no intent is lost.*

### **Unfinished Items from Sprint 20:**
- **PENDING TEST: Contextual Echo**: Verify Pinky-ism stripping.
- **PENDING TEST: Deep Smoke**: Verify flow with Windows host online.
- **Carry-over Task: Activity Latch Audit [FEAT-287]**: Verify conversation extends residency.
- **Carry-over Task: Ledger Integrity**: Confirm `active_pids.json` port reclamation.

### **Refinement Report (Homework Analysis):**
- **vLLM Log Path**: Confirmed at `/home/jallred/Dev_Lab/HomeLabAI/vllm_server.log`.
- **v1 Lost Gems**: Re-integrated Docker monitoring and 95% VRAM critical threshold logic.
- **TraceMonitor**: Physically present in `v4` (imported); needs VLLM log added to target list.
- **State Mapping**: `self.is_hibernating` and `self.current_lab_mode` confirmed as the internal truth anchors.
- **Interleaved Schema**: Confirmed JSON list format in `pager_activity.json`.

---
**Governing Standard:** [BKM-020] High-Fidelity Sprint Documentation & [BKM-023] Surgical Preservation Protocol.
