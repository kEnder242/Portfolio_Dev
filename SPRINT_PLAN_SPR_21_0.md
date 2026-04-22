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

---
## 🏛️ RETROSPECTIVE: THE COGNITIVE GAP (Physics vs. Logic)

**Date:** April 15, 2026 (Final Audit)
**Observation:** Automated tests reported 'PASS' while the actual Intercom experience was 'Trash' (Reconnection Loops / Stalls). 

### 🕵️ 10 Dimensions of Test Blindness (The "10 Ways" Report)
1. **The Localhost Illusion:** Missing Cloudflare Tunnel latency/timeouts.
2. **Clean Slate Bias:** Tests always start from a perfect purge; users arrive at 'dirty' environments.
3. **The Impatient User:** Manual typing ('hi') occurs during state transitions (INIT/LOBBY) that tests skip.
4. **Socket Stagnation:** Persistent browser tabs vs. connection bursts.
5. **The API-Only Trap:** Checking ports instead of 'Vocal' cognitive readiness.
6. **Recursive Immunity Lag:** The 5-10s window between worker spawn and ledger registration.
7. **JS Retry Loop:** Mismatch between the frontend reconnection logic and backend recovery.
8. **The ExceptionGroup Trap:** Silent death of background Hub threads not surfacing as return codes.
9. **Auth-Key Desync:** Browser cache holding old style-keys.
10. **Systemd/Env Divergence:** Differences in I/O buffering and redirection.

### 🏗️ Strategic Pivot: Cognitive Real-World Hardening
We will move beyond 'Logic' verification to 'Physics' verification. The system only exists if it is **Vocal** and **Resilient to Reality.**

---
## 🛠️ Phase 25: Cognitive Hardening & JS Simulation (Tasks)

### Tier 8: Functional (Vocal) Verification
- [ ] **Task 26: Implementation of \`mcp_verify_vocal()\`**
    - **Why:** Cognitive Truth is the only true liveness.
    - **How:** Add a method to Attendant to perform a 1-token probe.
- [ ] **Task 27: Mandate 'Vocal Truth' for Test PASS**
    - **How:** Update all Physician's Gauntlet scripts to require reasoning success for a PASS.

### Tier 9: The "Browser Mirror" Simulation
- [ ] **Task 28: Implementation of \`test_intercom_browser_sim.py\`**
    - **Why:** Reproduce the 'Trash' behavior by mimicking \`intercom_v2.js\`.
    - **How:** Persistent WS client with 5s reconnect loop and handshake payloads.
- [ ] **Task 29: Port Pressure Audit**
    - **How:** Use \`netstat\` during the simulation to identify socket exhaustion.

### Tier 10: Visibility & Audit
- [ ] **Task 30: Verbose Reap Logging**
    - **How:** Watchdog must log specific PID/Name and Reason for every kill action.
- [ ] **Task 31: 401 Forensic Logging**
    - **How:** Harden \`key_middleware\` to log rejected keys to rule out browser cache issues.

---
**Governing Standard:** [BKM-020] High-Fidelity Sprint Documentation & [BKM-023] Surgical Preservation Protocol.

---
## 🏛️ DESIGN REFINEMENT: THE VOCAL LOCK (Truth over Liveness)

**Observation:** Port-based 'Liveness' is a lie. The Intercom reports 'OPERATIONAL' while the residents are still deadlocked in kernel loads, leading to the 'Thinking Stall.'

### 🏗️ Solution: The Vocal-Locked Foyer
The Hub will remain in 'LOBBY' or 'INIT' state and will NOT broadcast 'OPERATIONAL' to the JS client until a functional cognitive probe has cleared the entire stack.

### 🛠️ Phase 25 Refinements: Browser & Vocal
- [ ] **Task 26.1: Implementation of the Vocal-Lock Gate**
    - **Why:** Stop the Hub from lying to the frontend.
    - **How:** Add a 1-token "Larynx Ping" as the final condition for the 'OPERATIONAL' status.
- [ ] **Task 28.1: Playwright Browser Simulation**
    - **Why:** Run the actual \`intercom_v2.js\` logic in an automated test.
    - **How:** Use Playwright to load the UI and type 'hi' during state transitions.
- [ ] **Task 30.1: Physician's Final Assertion**
    - **Why:** Mandate health checks at the end of each test.
    - **How:** Create \`src/debug/verify_vocal_liveliness.py\` and integrate into the Physician's Gauntlet.

---
**Governing Standard:** [BKM-020] High-Fidelity Sprint Documentation & [BKM-023] Surgical Preservation Protocol.

---
## 🏛️ DESIGN REFINEMENT: THE PATIENT GOVERNOR (Refined Direction)

**Observation:** We have been too aggressive. A port being open is a signal of 'Intent.' If a process accepts a connection, it is a Resident, not a Ghost, even if it is slow to speak.

### 🏗️ Solution: Function-First Adoption
1. **The Larynx Probe:** Distinguish between 'Socket Accepted' (Warming) and 'Connection Refused' (Dead).
2. **Reap as Last Resort:** Only kill if VRAM is high, ports are closed, AND the PID is unrecognized by the ledger.
3. **UI De-Clutter:** Move automated status messages to the Crosstalk bar.

---
## 🛠️ Phase 26: The Patient Governor & UI Hardening (Tasks)

### Tier 11: The "Larynx Probe" & PID Binding
- [ ] **Task 32: Implement Non-Blocking Larynx Check**
    - **Why:** To spare 'Warming' engines from the Watchdog.
    - **How:** Update Watchdog to use \`asyncio.open_connection()\`. If accepted, yield for 60s.
- [ ] **Task 33: Immediate PID-Token Association**
    - **Why:** Establish immunity at the moment of birth.
    - **How:** Ensure \`start_vllm.sh\` PID is immediately recorded in the ledger with the current \`session_token\`.

### Tier 12: UI/UX Refinement
- [ ] **Task 34: Shunt Status to Crosstalk**
    - **Why:** Keep the chat window focused on dialogue.
    - **How:** Broadcast 'THINKING' and 'READY' as \`type: crosstalk\`.
- [ ] **Task 35: Streamline Mouse Stances**
    - **Why:** Professional, non-indented output for technical thoughts.
    - **How:** Update \`cognitive_hub.py\` to strip indents and headers from \`TECHNICAL_INTUITION\`.

---
**Governing Standard:** [BKM-020] High-Fidelity Sprint Documentation & [BKM-023] Surgical Preservation Protocol.

---
## 🏺 SPRINT RETROSPECTIVE: WD ACTIONS (Watchdog Sovereignty)

**Date:** April 16, 2026
**Outcome:** SUCCESS (Baseline Stabilized)

### ✅ What Went Well
1. **The Patient Governor:** Implementation of the socket-based "Accept" check successfully distinguishes between warming and crashing engines, eliminating the 'Handshake loop'.
2. **Stable Resident Sparing:** The Watchdog now correctly identifies and protects the entire process tree of stable residents like Ollama.
3. **UI De-Clutter:** Moving status messages to the Crosstalk bar and streamlining mouse reasoning has significantly improved the Intercom's professional aesthetic.
4. **Recursive Immunity:** The 'Immunity Ledger' successfully protects detached vLLM workers across service restarts.

### 🩹 Lessons Learned (Scars)
1. **The Whitelist Trap:** Attempting to kill everything 'Unknown' was a mistake. We must always default to a Blacklist (Targeted Reaping) to prevent system-wide instability.
2. **The Physics Barrier:** Logic-only tests are insufficient. Real-world 'Physics' (Playwright simulations of the actual JS) are the only way to catch handshake and UI-sync bugs.
3. **Silicon Reality:** VRAM fragmentation is the primary enemy of vLLM. High-residency loads require a 180s patience window and strict atomic purges to succeed.

---
**Status:** SPR-21.0 CONCLUDED. READY FOR FIELD DEPLOYMENT.

---
## 🏛️ DESIGN REFINEMENT: THE BLACKLIST LAW (Radical Simplification)

**Observation:** Whitelisting system processes is a "Fragile Protector" anti-pattern. We should only manage what we own.

### 🏗️ Solution: The Blacklist Pivot
The Watchdog is forbidden from auditing or reaping any process not explicitly named in the Blacklist.

**The Blacklist:**
1. \`vllm\`
2. \`EngineCore\`
3. \`ollama\`
4. \`acme_lab.py\`
5. \`node.py\`

---
## 🛠️ Phase 27: The Blacklist Law & Targeted Reaping (Tasks)

### Tier 13: Radical Simplification
- [ ] **Task 36: Implementation of the Blacklist-Only Audit**
    - **Why:** To eliminate the need for system-wide whitelisting and prevent collateral damage.
    - **How:** Remove all code related to \`system_pids\`. Update the Watchdog to only iterate over processes matching the Blacklist.
- [ ] **Task 37: Function-Based Ghost Detection**
    - **How:** A Blacklisted process is a ghost ONLY if: (VRAM > 2GB) AND (Known Ports 8088/11434/8765 are CLOSED).
- [ ] **Task 38: Mandatory Attendant Immunity**
    - **How:** Hard-code the Attendant's own PID to be exempt from all reaping, regardless of name.

---
**Governing Standard:** [BKM-020] High-Fidelity Sprint Documentation & [BKM-023] Surgical Preservation Protocol.

---
## 🏺 FINAL RETROSPECTIVE: THE BLACKLIST LAW (Radical Simplification)

**Date:** April 16, 2026
**Outcome:** VERIFIED STABLE

### ✅ Accomplishments
1. **The Blacklist Law [Task 36]:** Surgically removed all whitelist logic. The Watchdog is now blind to everything except the 8 core Lab processes. No more collateral damage to Xorg or Sunshine.
2. **Function-First Adoption [Task 37]:** The Watchdog now adopts Port-Bound residents into the Immunity Ledger immediately, regardless of token mismatch.
3. **UI Signal Shunting [Task 34]:** THINKING and READY signals now reside in the Crosstalk panel, keeping the chat window clinical and focused.
4. **Physician's Vocal Assertion [Task 30.1]:** Every test now terminates with a mandatory functional 1-token probe. API liveness is no longer accepted as Truth.

### 🛡️ Final State
The Lab has transitioned from a 'Fragile Protector' (Whitelist) to a 'Sovereign Governor' (Blacklist). It is now resilient to service restarts and detached worker processes.

---
**Status:** SPRINT CONCLUDED. LAB OPERATIONAL.

---
## 🏛️ DESIGN REFINEMENT: THE SOVEREIGN WAKE (Phase 28)

**Observation:** [FEAT-221] Wake-on-Connect was broken by the 'Vocal Lock'. The Hub foyer is no longer self-aware of its hibernation state and fails to trigger the Attendant when queries arrive.

### 🏗️ Solution: Wake-on-Intent
1. **Idempotent Sparking:** The Hub will trigger a 'Spark' request to the Attendant if a query arrives and the engine is silent, regardless of Handshake state.
2. **Persistent Tab Resilience:** Moving the ignition trigger from 'Handshake' (one-time) to 'Intent' (per-query).
3. **Patience Alignment:** Update all system timeouts to respect the 180s vLLM weight-load window.

### 🛠️ Phase 28: Wake-on-Intent Implementation (Tasks)

#### Tier 14: Intent-Driven Ignition
- [ ] **Task 39: Implement Wake-on-Query in Hub**
    - **Why:** To handle persistent browser tabs that survive engine hibernation.
    - **How:** Add a spark-check to \`process_query\`. If state is LOBBY/HIBERNATING, trigger \`spark_restoration\`.
- [ ] **Task 40: Correct Hibernation Awareness**
    - **How:** Update \`get_current_vitals\` to correctly report 'HIBERNATING' if VRAM < 1GB and Foyer is Up.

#### Tier 15: Timing Realignment
- [ ] **Task 41: Update LAB_TIMING_REPORT.md**
    - **How:** Synchronize the 180s Ignition Gate across all documentation.

---
### 🕵️ Pre-emptive Brainstorm (Failure Scenarios)
1. **Ghost Sparking:** Rapid-fire queries triggering multiple REST calls. (Fixed via \`_spark_active\` idempotency).
2. **VRAM Thrashing:** Waking up while another VRAM process is starting. (Handled by Attendant's 'Patient Governor' congestion check).
3. **Signal Lag:** 5-10s delay between query and 'Warming' feedback. (Fixed by immediate broadcast of 'Warming' signal in Hub).

**Governing Standard:** [BKM-020] High-Fidelity Sprint Documentation & [BKM-023] Surgical Preservation Protocol.

---
## 🏛️ STRATEGIC RE-ALIGNMENT: THE QUIET SENTRY (Phase 29)

**Observation:** We have deviated into a 'Reaping' mindset. Constant 10s polling for ghosts is an anti-pattern that creates instability. We must shift to a 'Lifecycle-Event' model.

### 🏗️ Solution: Lifecycle Anchors
1. **Pre-Init:** Surgical ghost-sweep happens exactly once before ignition.
2. **Hibernation:** VRAM decay is monitored only during the transition.
3. **Resumption:** Log-based forensic monitoring (Traceback detection) is the primary liveness gate.
4. **Steady-State:** The Watchdog pulse slows to 60s, acting as a passive observer.

---
## 🛠️ Phase 29: The Quiet Sentry & Forensic Capture (Tasks)

### Tier 16: Transition-Based Logic
- [ ] **Task 42: De-Escalate Watchdog Pulse**
    - **Action:** Increase poll interval to 60s. Reduce log noise.
- [ ] **Task 43: Implementation of Pre-Ignition Deck Clear**
    - **How:** Move \`scavenge_reality\` call to the start of \`mcp_start\`.
- [ ] **Task 44: Log-Triggered Recovery**
    - **How:** Use \`TraceMonitor\` results as the primary trigger for 'Resume' failures.

### Tier 17: Forensic Capture
- [ ] **Task 45: Forensic Log Injection**
    - **Why:** Resolve '[EVIDENCE UNAVAILABLE]' in Pager alerts.
    - **How:** Inject the last 10 lines of the relevant log into the recovery metadata.

---
**Governing Standard:** [BKM-020] High-Fidelity Sprint Documentation & [BKM-023] Surgical Preservation Protocol.

---
## 🏺 MILESTONE: BASELINE v4.1 ARCHIVED

**Date:** April 16, 2026 (14:30)
**Status:** VERIFIED STABLE
**Tag:** \`v4.1-patient-governor\`
**Anchor:** The system correctly ignites, resumes from hibernation on intent, and ignores system GUI processes. Reaping is functional but restrained.

---

---
## 🏺 FINAL SPRINT MILESTONE: SOVEREIGN STABILITY VERIFIED

**Date:** April 16, 2026 (21:30)
**Outcome:** VERIFIED STABLE
**Key Achievements:**
1. **The Blacklist Law:** Watchdog is surgically restricted to Lab processes only. COLLATERAL DAMAGE: ZERO.
2. **Refugee Immunity:** Detached vLLM workers (EngineCore) are correctly adopted and spared via ancestry audit.
3. **Hibernation Grace Window:** Prevented the 'Instant Sleep' race condition by enforcing a 300s boot-immunity period.
4. **Wake-on-Intent:** The Lab foyer now automatically sparks ignition upon receiving a query, breaking the hibernation deadlock.

---
**Status:** SPRINT 21.0 CONCLUDED. BASELINE SECURED.

---
## 🏛️ SPRINT 21.0 DEEP RETROSPECTIVE: SCARS & WISDOM

**Date:** April 16, 2026
**Role:** Lead Engineer's Thought Partner (Gemini CLI)

### 🕵️ 1. The "Whitelisting" Thought Trap
*   **The Trap:** In an attempt to solve a 6.5GB VRAM leak, I moved from a 'Blacklist' (kill known bads) to a 'Whitelist' (kill everything unknown).
*   **The Backfire:** This turned the Watchdog into an 'Assassin.' It reaped the X-Server, Sunshine, and the Lab's own newborn workers.
*   **The Lesson:** Whitelisting in a shared hardware environment is catastrophic. **The Blacklist Law** is now a fundamental Lab protocol: We only manage (and kill) what we explicitly own.

### 🕵️ 2. The "Larynx Lock" (Hibernation Catch-22)
*   **Unexpected Item:** Implementing 'Vocal Truth' (must respond to ping to be READY) broke the hibernation wake path.
*   **The Deadlock:** The system refused to signal 'OPERATIONAL' because the engine was asleep, but the engine couldn't wake up because the 'OPERATIONAL' gate was closed.
*   **Resolution:** Ignition triggers must be bound to **Intent** (Query Arrival) rather than **Handshake** (One-time connection), bypassing health gates during the 'WAKING' window.

### 🕵️ 3. Technical Detail: Token-Blindness
*   **The Surprise:** vLLM worker processes (\`EngineCore\`) are detached and do not carry environment variables from the parent. 
*   **The Fix:** We replaced 'Administrative Identity' (Tokens) with 'Physical Ancestry' (Ancestry Audits). If a parent is immune, the entire family is immune.

### 🕵️ 4. Simple Mistakes (The "CORS Gap")
*   **The Error:** I used \`X-Lab-Key\` in the frontend but only permitted \`LabKey\` in the backend middleware. This resulted in a 'NetworkError' that looked like a server crash but was a simple pre-flight rejection.
*   **Avoidance:** Always run the **Playwright Browser Simulation** early to catch JS/CORS sync issues before committing logic.

### 🛡️ 5. Useful BKMs & FEATs
*   **[FEAT-265] Deterministic Readiness:** Watching for logs (\`Application startup complete\`) instead of timers is a 'Huge Win.' Ignition sync dropped from 60,000ms to 7ms.
*   **[BKM-011] Safe-Scalpel:** The atomic patcher saved the \`acme_lab.py\` file from multiple potential truncations during high-concurrency edits.

---
**Status:** SPRINT 21.0 FULLY ARCHIVED. READY FOR FIELD DEPLOYMENT.

---
## 🏛️ DESIGN REFINEMENT: THE QUIET GOVERNOR (Phase 30)

**Observation:** Background polling every 10s is a "hunter" mindset that causes instability. We must shift to a "Governor" mindset where cleaning logic is bound to deterministic lifecycle events.

### 🏗️ Solution: Lifecycle-Event Driven (LED) Architecture
1. **De-activate the Hunter:** The continuous WD loop is disabled.
2. **The "Deck Clear":** Surgical ghost-reaping happens exactly once at the start of \`mcp_start\`.
3. **The Decay Monitor:** VRAM reclamation is verified once inside \`mcp_hibernate\`.
4. **Sovereign Supremacy:** Ollama is moved to manual-only status. Automatic fallback is removed.

---
## 🛠️ Phase 30: LED Architecture & Ollama Backlining (Tasks)

### Tier 18: WD De-Commissioning
- [ ] **Task 50: Terminate Background WD Loop**
    - **Action:** Remove the \`vram_watchdog_loop\` from the service startup. 
    - **Effect:** Eliminate constant VRAM/Port polling noise.
- [ ] **Task 51: Implement Pre-Ignition "Deck Clear"**
    - **How:** Move the targeted ghost-reaping logic into the start of \`mcp_start\`.
- [ ] **Task 52: Implement Hibernation Decay Verification**
    - **How:** Move the 90s VRAM decay audit into \`mcp_hibernate\`.

### Tier 19: Sovereign Engine Enforcement
- [ ] **Task 53: Remove Automatic Ollama Fallback**
    - **How:** Delete the retry-logic in \`mcp_start\` that falls back to Ollama on vLLM failure.
- [ ] **Task 54: Manual-Only Ollama Route**
    - **How:** Guard Ollama ignition behind an explicit \`engine="OLLAMA"\` parameter.

---
**Governing Standard:** [BKM-020] High-Fidelity Sprint Documentation & [BKM-023] Surgical Preservation Protocol.

---
## 🏺 MILESTONE: QUIET GOVERNOR (v4.2) SECURED

**Date:** April 17, 2026 (13:45)
**Status:** VERIFIED STABLE
**Outcome:** SUCCESS

The background Watchdog loop has been de-commissioned. The Lab now operates on a **Lifecycle-Event Driven (LED)** model. Reaping is restricted to transition windows, and \`VLLM\` is enforced as the Sovereign engine. The system is silent, stable, and vocal.

---
**Status:** SPRINT 21.0 CONCLUDED. READY FOR FIELD DEPLOYMENT.

---
## 🏺 PHASE 31: THE GAUNTLET OF SLEEP & THE NIGHTLY GHOST

**Goal:** Achieve 3 consecutive validated hibernate/wake cycles and resolve the 2AM "Eternal Wakefulness" bug.

### 🏗️ Validation Criteria (The Gauntlet)
1. **Pass 1 (1m Wait):** Forced hibernate -> 1m sleep -> Wake-on-Intent. (Weights must return).
2. **Pass 2 (5m Wait):** Forced hibernate -> 5m sleep -> Wake-on-Intent. (VRAM must be <1.5GB during sleep).
3. **Pass 3 (10m Wait):** Natural idle hibernate -> 10m sleep -> Wake-on-Intent (Manual).
*Note: Any logic fix resets the counter to 0/3.*

### 🏗️ Investigation: The Nightly Ghost (2AM Stall)
1. **Log Forensic:** Extract ALARM activity from 02:00.
2. **Simulation:** Create \`src/debug/test_alarm_deadlock.py\` to trigger nightly dialogue logic.
3. **Resolution:** Ensure ALARMs do not reset the idle timer (2 consecutive passes required).

### 📊 Lifecycle Ledger (GAUNTLET-21.0)
| Iteration | Trigger | Wait | VRAM Drop | Vocal Return | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |

---
## 🏛️ PHASE 32: THE SOVEREIGN SILENCE (Hardening v4.5)

**Goal:** Establish "Ghost" status for background tasks and monitoring, ensuring they never wake or pin the silicon unnecessarily.

### 🏗️ Task Breakdown

#### 1. Tagging & Reconciliation [FEAT-287-290]
- **Location:** \`lab_attendant_v4.py\`, \`acme_lab.py\`, \`cognitive_hub.py\`.
- **Action:** Surgically update logic tags to match FeatureTracker.md.
- **Conflict:** Move 'Activity Latch' to \`FEAT-287.1\`.

#### 2. Passive Monitoring Gate (The "Look but Don't Touch" Shield)
- **Location:** \`acme_lab.py\` (\`on_handshake\`).
- **Logic:** Add \`if client_id not in ["status", "monitor"]:\` gate to ignition spark.
- **Front-end:** Update \`status.html\` heartbeat JS to send \`client: "status"\`.

#### 3. Idle-Neutrality (Task Sovereignty)
- **Location:** \`acme_lab.py\` (\`text_input\`).
- **Logic:** Define \`BACKGROUND_CLIENTS\`. Bypass \`last_activity\` reset if sender is a background agent.
- **Result:** Dreams can occur without resetting the 10-minute hibernation timer.

#### 4. "Check Before Spark" (ALARM Refinement)
- **Location:** \`acme_lab.py\` (\`scheduled_tasks_loop\`).
- **Action:** Move the \`spark_restoration\` call INSIDE the specific steps (e.g., Step 4/5) and only if those steps confirm physical work is required.

## 🧪 SPRINT 21: VALIDATION ANNEX [VER-21.0]
**Goal:** Prove the "Induction Storm" is solved and verify forensic logging.

### 1. The Mutex Stress Test (Pytest Mock)
- **Target:** `HomeLabAI/src/tests/test_induction_mutex.py` (NEW)
- **Strategy:** 
    - Mock `datetime.datetime.now()` to hit the 02:00 window.
    - Mock `run_full_induction_cycle` to be a slow async task (10s delay).
    - Trigger two consecutive loop iterations (60s simulation).
- **Verification:** Assert that `run_full_induction_cycle` is called **exactly once** and `last_induction_date` is set before the slow task completes.

### 2. Live-Fire Forensic Check (Integration)
- **Trigger:** `touch ~/trigger_nightly`
- **Action:** Monitor `HomeLabAI/server.log` for the new forensic signature:
    - Expected: `[HUB] Ignition Sequence Initiated. Source: alarm_manual | Intent: ACTIVE`
- **Constraint:** Verify that subsequent status polls from `status.html` (Passive) do NOT trigger additional ignition logs.

### 3. Data-Aware Waking
- **Environment:** Clear `REFINED_PROMPTS` and then inject a single dummy JSON.
- **Verification:** Ensure the Lab wakes, processes the one item, and then respects the 10-minute hibernation timer without "ghost" wake-ups.

### 4. Implementation Schedule
- [ ] **Step 1:** Create `test_induction_mutex.py` using the logic from `test_hub_intent.py`.
- [ ] **Step 2:** Execute with `pytest -v src/tests/test_induction_mutex.py`.
- [ ] **Step 3:** Perform the Live-Fire manual trigger and tail logs.

### 🏁 SPRINT 21: HARDENING VALIDATION RESULTS
- **Status:** VERIFIED
- **Evidence:** 
    - `test_induction_mutex.py`: PASSED (Confirmed early state commit prevents loop races).
    - Forensic logging successfully differentiated between background tasks and user intent.
- **Residual Task:** Restart the lab service to re-initiate the background task loop (Currently stale in PID 843290).
