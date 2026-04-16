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

- [ ] **Task 5: Fix Log Collation Format**
    - **Context**: The watchdog logs in `lab_attendant_v4.py` use an ISO 'T' separator (e.g., 2026-04-15T17:00:00), which breaks the frontend's day-grouping logic. 
    - **Action**: Revert to the legacy space-separated format (YYYY-MM-DD HH:MM:SS) to restore collation in `status.html`.

- [ ] **Task 6: Resolve Asynchronous Shutdown Race**
    - **Reproduction**: Start vLLM, then immediately restart the service. Verify if the engine survives the Attendant's exit.
    - **Fix**: Implement a synchronous SIGTERM handler in `lab_attendant_v4.py` that waits for `cleanup_silicon()` to complete before exit.


---
## 🏛️ FORENSIC REPORT: THE GOVERNOR'S PARADOX (Service Stability Audit)

**Date:** April 15, 2026
**Observation:** The Lab Attendant currently functions as a 'Volatile Process' rather than a 'Stable Service.' Frequent 'systemctl restarts' to apply logic changes result in 'Session Amnesia,' where the new Attendant instance disowns the AI engine processes spawned by its predecessor, leading to 'Ghost Contexts' and VRAM fragmentation.

### 🕵️ Core Stability Flaws
1. **Volatile Identity:** The `session_token` is a random UUID generated on boot. Child processes (vLLM/Hub) carry the token of their parent. When the parent restarts, it generates a new token and views its own children as 'unrecognized orphans.'
2. **Ledger Fragility:** The `active_pids.json` is the sole source of truth. If it becomes corrupted or out-of-sync during a crash, the Attendant is 'blind' to reality until the Watchdog performs a physical truth audit.
3. **Shutdown Race:** Detached children (spawned with `start_new_session=True`) often outlive the Attendant during a SIGTERM window, especially if the `cleanup_silicon` task is interrupted by the systemd timeout.

### 🏗️ Strategic Shift: The 'Adopt-on-Restart' Architecture
We must transition the Attendant to a 'Continuous Governor' model. A service restart should be a 'Logic Refresh,' not a 'State Reset.' The Attendant must be capable of 'scavenging' the machine on boot to recognize and adopt its existing family.

---
## 🛠️ Phase 22: Service Continuity & Adoption (Tasks)

### Tier 1: Persistent Identity
- [x] **Task 7: Disk-Persisted Session Token**
    - **Why:** To ensure the 'Immunity Signal' survives a service restart.
    - **Where:** `lab_attendant_v4.py` -> `__init__`.
    - **How:** Check for `run/session.token`. If exists, load it; otherwise, generate and save. Use this for all `LAB_IMMUNITY_TOKEN` environment variables.

- [x] **Task 8: Stable Boot Hash**
    - **Why:** Provide a secondary 'Epoch' marker that persists across restarts but resets on a 'Hard Reset.'
    - **Where:** Global state in `lab_attendant_v4.py`.

### Tier 2: Physical Scavenging (The 'Detective' Boot)
- [x] **Task 9: Implementation of `scavenge_reality()`**
    - **Why:** To identify what is *actually* running before we look at the ledger.
    - **Where:** `LabAttendantV4` class.
    - **How:** Execute `sudo fuser` on ports 8765, 8088, and 11434. Cross-reference results with `psutil` to find process start times and command lines.

- [x] **Task 10: Process Adoption Protocol**
    - **Why:** To re-link the Attendant with healthy existing nodes.
    - **Where:** Startup sequence in `run_bilingual()`.
    - **How:** Compare discovered PIDs against the `active_pids.json` and the persisted `session_token`. If a healthy node matches, update the live `self.active_pids` and skip spawning.

- [x] **Task 11: State Machine Reconstruction**
    - **Why:** Ensure the `current_lab_mode` and `is_hibernating` flags reflect reality on boot.
    - **Where:** `mcp_heartbeat` and `update_status_json`.
    - **How:** If a vLLM process is found on 8088 but is not responding to a cognitive probe, set `is_hibernating = True`.

### Tier 3: Hardening & Verification
- [x] **Task 12: Synchronous SIGTERM Handler**
    - **Why:** Prevent the 'Shutdown Race' where children outlive the parent.
    - **Where:** `lab_attendant_v4.py` signal registration.
    - **How:** Implement a handler that uses `asyncio.run(self.cleanup_silicon(mode="SESSION"))` before final exit.

- [x] **Task 13: Ledger Integrity (Self-Healing)**
    - **Why:** Ensure the disk ledger is never out of sync with physical reality.
    - **Where:** `vram_watchdog_loop`.
    - **How:** Add a task to periodically overwrite `active_pids.json` with the 'Physical Truth' found during the VRAM audit.

- [x] **Task 14: The 'Graceful Restart' Test**
    - **Action:** Start the Lab (VLLM), then `sudo systemctl restart lab-attendant`.
    - **Success:** The new Attendant instance should adopt the existing vLLM PID without triggering a second ignition or reaping the healthy engine.

- [x] **Task 15: The 'Adopted Hibernate' Test**
    - **Action:** Hibernate the Lab, then restart the Attendant.
    - **Success:** The new instance should correctly identify the state as `HIBERNATING` based on VRAM/Process checks.

- [x] **Task 16: Standard Operating Procedure (Gemini CLI)**
    - **Action:** Formally document the 'Orchestrator-First' mandate. Gemini CLI (me) is forbidden from manual intervention unless the Attendant's scavenging fails.

---
**Governing Standard:** [BKM-020] High-Fidelity Sprint Documentation & [BKM-023] Surgical Preservation Protocol.


---
## 🏛️ RETROSPECTIVE: THE RECURSIVE BLIND SPOT (Why it's still breaking)

**Date:** April 15, 2026 (Late Session)
**Observation:** Despite implementing 'Adopt-on-Restart,' the Lab remained trapped in a 'Recovery Loop.' The Watchdog continued to reap the vLLM engine every 20 seconds.

### 🕵️ The "Smoking Gun" Discovery
vLLM spawns a family of worker processes to handle inference. While the **Parent PID** (the API Server) correctly carries the `LAB_IMMUNITY_TOKEN`, its **Child Worker PIDs** (the ones actually holding the VRAM) do not. 
The Watchdog's 'VRAM Truth' audit saw these 'Token-Blind' workers, misidentified them as ghosts, and reaped the entire engine family.

### 🏗️ Solution: The 'Family Ledger' (Tier 4)
We will move from 'Identity Probing' (checking environments) to 'Family Tracking' (recording the tree). The Attendant will maintain a disk-persisted table of authorized PIDs.

---
## 🛠️ Phase 23: Family Sovereignty & Signal Unification (Tasks)

### Tier 4: The Immunity Ledger
- [ ] **Task 17: Schema Extension (`family_pids`)**
    - **Why:** Provide a single source of truth for all authorized GPU consumers.
    - **Where:** `active_pids.json`.
    - **How:** Add a `family_pids` list to the JSON structure.

- [ ] **Task 18: Implementation of `sync_family_ledger()`**
    - **Why:** Authorize vLLM workers and Hub residents recursively.
    - **Where:** `LabAttendantV4` class.
    - **How:** Use `psutil.Process(parent).children(recursive=True)` to populate the ledger. Call this immediately after ignition and during the Watchdog loop.

- [ ] **Task 19: Family-Aware VRAM Audit**
    - **Why:** Prevent the Watchdog from 'murdering' recognized children.
    - **Where:** `vram_watchdog_loop` -> Step 4.
    - **How:** Replace the environment token-scrape with a simple `p_pid in self.active_pids['family_pids']` check.

### Tier 5: Signal Alignment & Verification
- [ ] **Task 20: Purge Legacy 'READY' Signals**
    - **Why:** The Attendant is waiting for 'READY' while the Hub is sending 'OPERATIONAL.'
    - **Where:** `log_monitor_loop` and `mcp_wait_ready`.
    - **How:** Standardize all readiness checks to look for the Hub's `Mind is OPERATIONAL` and the Engine's `is VOCAL` signals.

- [ ] **Task 21: Family-Aware Gauntlet Test**
    - **Action:** Update `test_lifecycle_gauntlet.py` to verify that the *entire family* (workers included) is protected during restarts.

---
**Governing Standard:** [BKM-020] High-Fidelity Sprint Documentation & [BKM-023] Surgical Preservation Protocol.

---
## 🏛️ DESIGN REFINEMENT: THE SOVEREIGN BINDING (Token-PID Association)

**Observation:** A list of PIDs without a linked token is 'unauthenticated.' If the session token changes (e.g., after a Hard Reset), the Attendant must know which PIDs are disowned to prevent unauthorized GPU occupancy.

### 🏗️ Solution: Unified Sovereign Ledger
The \`active_pids.json\` will be upgraded to include an \`authority\` header containing the current \`session_token\`. This binds the process tree to a specific identity.

### 🛠️ Phase 23 Additions: Linkage & Purge
- [ ] **Task 17.1: Implementation of Authority Header**
    - **Why:** Bind PIDs to a verifiable session identity.
    - **How:** Add \`"authority": {"token": "..."}\` to the ledger schema.
- [ ] **Task 22: Stale Identity Purge**
    - **Why:** Clear survivors from invalidated sessions.
    - **How:** If boot-time scavenging finds a token mismatch in the ledger, treat the entire \`family_pids\` list as a kill-list.

---
**Governing Standard:** [BKM-020] High-Fidelity Sprint Documentation & [BKM-023] Surgical Preservation Protocol.

---
## 🏛️ HISTORICAL REPORT: THE RESILIENCE DNA (Reclaiming the Blacklist)

**Date:** April 15, 2026 (Night Session)
**Observation:** We have deviated from established resilience laws. The move toward 'Whitelisting' (killing unrecognized processes) has turned the Watchdog into a threat to system stability.

### 🏺 Historical Successes (The DNA)
1. **The Assassin [FEAT-119]:** Originally used a strict **Blacklist** of names (\`vllm\`, \`ollama\`, \`acme_lab.py\`). It never touched unknown VRAM consumers.
2. **Port-Strict Reaping:** Used \`fuser -k\` only on specific Lab ports (8765, 8088, 11434).
3. **Script Supremacy:** Standardized on \`bash start_vllm.sh\` to prevent Python FD 'bullying.'

### 🩹 How we Lost it (The Scars)
The 'v4 Over-Reach' attempted to solve the persistent 6.5GB VRAM leak by auditing all GPU PIDs. This bypassed the 'Blacklist' law and resulted in the 'Murderous Protector' bug, where the Watchdog killed newborn engines and system processes.

---
## 🛠️ Phase 24: Blacklist Restoration & Intercom Stability (Tasks)

### Tier 6: The Blacklist Law
- [ ] **Task 23: Implementation of strict Blacklist Reaping**
    - **Why:** Adhere to the 'Only Kill What We Know' mandate.
    - **How:** Revert \`cleanup_silicon\` to use the \`targets\` list from \`v1\`. Remove all broad physical-PID killing.
- [ ] **Task 24: Port-Bound VRAM Audit**
    - **Why:** Narrow the Watchdog's focus to prevent collateral damage.
    - **How:** Watchdog only audits PIDs that are physically bound to ports 8088, 8765, or 11434.

### Tier 7: Stress Validation
- [ ] **Task 25: Intercom Stress Test (The 'Cray Ports' Fix)**
    - **Action:** Run \`src/debug/test_intercom_flood.py\`.
    - **Success:** 50 consecutive WebSocket connections without a single Hub crash or Watchdog recovery.

---
**Governing Standard:** [BKM-020] High-Fidelity Sprint Documentation & [BKM-023] Surgical Preservation Protocol.
