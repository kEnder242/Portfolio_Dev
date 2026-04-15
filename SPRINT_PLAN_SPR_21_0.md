# Sprint Plan: [SPR-21.0] WD Actions (Watchdog Sovereignty)
**Status:** DRAFT | **Goal:** Rebuild the Lab Attendant's internal watchdog as a "State Machine Monitor" to ensure resilient hibernation and recovery.

---

## 🏛️ Section 1: Brainstorming & Architecture (The "Why")

**Core Problem:** A deep forensic review confirmed that the `vram_watchdog_loop` in `lab_attendant_v4.py` is an empty stub. More importantly, there's a fundamental architectural conflict between the old "liveness" model (always on) and the new "hibernation" model (resource efficiency). The watchdog must be rebuilt not just to detect crashes, but to **validate state transitions**.

**The Watchdog's New Purpose: The "Sleep Monitor"**
The internal watchdog must evolve from a simple "is it on?" checker to a true "State Machine Monitor." It runs as a background `asyncio` task on the same event loop as the Attendant's REST API, giving it direct, thread-safe access to the Attendant's internal state (`self.is_hibernating`, etc.). Its job is to ensure the Lab doesn't get stuck *between* states.

**Proposed Flow (Reconstruction):**
1.  **State-Aware Monitoring**: The `vram_watchdog_loop` will be state-aware. It will check the Attendant's intended state (`current_lab_mode`, `is_hibernating`) before performing checks.
2.  **Hibernation Failure Detection**:
    *   **Trigger**: The Attendant sets `is_hibernating = True` and attempts to unload the AI engine.
    *   **Watchdog Check**: The watchdog sees the `is_hibernating` flag. After a grace period (e.g., 60s), it checks VRAM.
    *   **Failure Condition**: If `is_hibernating` is true but VRAM usage is still high, the watchdog declares a "Hibernation Failure."
3.  **Liveness Failure Detection**:
    *   **Trigger**: The Lab is supposed to be `ONLINE`.
    *   **Watchdog Check**: The watchdog polls the Hub's heartbeat endpoint (`:8765`).
    *   **Failure Condition**: If the endpoint is unresponsive for several cycles, the watchdog declares a "DEAD Hub."
4.  **Tiered Recovery & Forensic Logging**:
    *   **On Hibernation Failure**: Log a `CRITICAL` event (`[WATCHDOG] Hibernation failed. VRAM remains allocated.`) and trigger a forceful `mcp_stop` to guarantee silicon release.
    *   **On DEAD Hub**: Use the **TraceMonitor** to grab the last few lines from `server.log`. Log a `CRITICAL` event (`[WATCHDOG] Hub unresponsive. Last words: "..."`) and trigger the `mcp_stop` -> `mcp_start` cycle.
    *   All logs will use `self.log_event()` to ensure they appear in the "Interleaved System Logs" on `status.html`.

---

## 🔗 Section 2: Architectural Alignment

This plan directly implements and restores several core features documented in the `FeatureTracker`:
*   **[FEAT-036] VRAM Guard**: The VRAM monitoring logic is the core of this feature.
*   **[FEAT-249] VRAM Hibernation Matrix**: The state-aware monitoring directly supports this feature.
*   **[FEAT-035] Zombie Port Recovery**: The Hub liveness probe directly addresses this.
*   **[FEAT-043] Dead-Man's Switch**: The "DEAD Hub Recovery" is the implementation of this switch.
It also adheres to **[BKM-018] (Orchestrator-First)** and **[BKM-022] (Atomic IO)** for logging.

---

### 🛠️ Section 3: Tasks & Tracking (WD Sovereignty)

- [ ] **Task 1: Rebuild State-Aware Watchdog Logic**
    - **Mechanism**: Implement the state-aware VRAM and Port monitoring logic in the `vram_watchdog_loop` in `lab_attendant_v4.py`. This involves checking internal state flags like `self.is_hibernating` before probing hardware or ports.
- [ ] **Task 2: Implement Tiered Recovery**
    - **Mechanism**: In the watchdog loop, call the appropriate recovery MCP methods (`mcp_hibernate`, `mcp_stop`) based on the detected failure mode.
- [ ] **Task 3: Implement Forensic Log Injection**
    - **Mechanism**: Before triggering a recovery, use the existing `TraceMonitor` instance to read the last few lines from `server.log` and `attendant.log`. Inject any discovered `Traceback` or error into the `self.log_event()` message to provide a rich forensic record in `status.html`.

---
## 🧪 Section 4: Detailed Implementation Plan

### **Task 1: Rebuild State-Aware Watchdog Logic**
*   **Location**: `lab_attendant_v4.py`, inside the `vram_watchdog_loop` method.
*   **Sub-Task 1.1: State Initialization**: Initialize `failure_count = 0` and `boot_grace_period = 6` at the top of the loop.
*   **Sub-Task 1.2: State-Aware Gates**:
    *   Add `if os.path.exists(MAINTENANCE_LOCK): continue`.
    *   Add a grace period for booting: `if boot_grace_period > 0: boot_grace_period -= 1; continue`.
*   **Sub-Task 1.3: Hibernation Check**:
    *   `if is_hibernating:`
    *   Check VRAM. If `used > 2000` after a grace period, trigger **Hibernation Failure Recovery**.
*   **Sub-Task 1.4: Liveness Check**:
    *   `elif current_lab_mode != "OFFLINE":`
    *   Poll `http://127.0.0.1:8765/heartbeat`. On failure, increment `failure_count`.
    *   If `failure_count > 3`, trigger **DEAD Hub Recovery**. On success, reset `failure_count`.

### **Task 2 & 3: Recovery and Logging**
*   **Location**: `lab_attendant_v4.py`, inside `vram_watchdog_loop`.
*   **Sub-Task 2.1: Hibernation Failure Recovery**:
    *   `self.log_event("Hibernation failed; VRAM not released. Forcing stop.", "CRITICAL")`.
    *   `await self.mcp_stop()`.
*   **Sub-Task 2.2: DEAD Hub Recovery**:
    *   Use `self.trace_monitor` to get the last lines from `server.log`.
    *   `self.log_event(f"Hub unresponsive. Triggering full restart. Last words: {log_snippet}", "CRITICAL")`.
    *   `await self.mcp_stop()`.
    *   `await asyncio.sleep(5)`.
    *   `await self.mcp_start(reason="WATCHDOG_RECOVERY")`.

---

## 🧹 Section 5: Scrub Report & Unfinished Items (April 15, 2026)
*A final review of historical documents and sprint plans to ensure no intent is lost.*

### **Unfinished Items from Sprint 20:**
- **PENDING TEST: Contextual Echo**: The Tier 3 "Soul" test for verifying Pinky-ism stripping was not run.
- **PENDING TEST: Deep Smoke**: This test was only partially completed.
- **Carry-over Task: Verify Weight Mapping Timeline**: Ensure the 180s settle window is generous enough.
- **Carry-over Task: Activity Latch Audit [FEAT-287]**: Verify active conversation extends the residency window.
- **Carry-over Task: Ledger Integrity**: Confirm `active_pids.json` correctly reclaims ports after a hard service crash.

### **Lost Gems Recovered:**
- **Docker Container Monitoring**: The `lab_attendant_v1.py` watchdog included logic to monitor essential Docker containers. This should be restored in a future sprint.

---
**Governing Standard:** [BKM-020] High-Fidelity Sprint Documentation & [BKM-023] Surgical Preservation Protocol.
