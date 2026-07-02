# Sprint Plan: [SPR-25.0] Persistence Sovereignty & Cold Logic
**Status:** ACTIVE | **Baseline:** Sprint 24.0 [VER-24.5]

---

## 🏛️ RETROSPECTIVE: THE LOBBY RESIDENCY GAP (Context & Scars)
**The Problem:** The Hub's state machine was blocking hibernation as long as any client was connected. This forced the Lab to stay "OPERATIONAL" indefinitely, leading to proxy timeouts (reconnect loops) and unnecessary VRAM usage.

### 🕵️ Investigation Findings (May 5):
1.  **Hibernation Deadlock**: `is_hibernating` was conditioned on `not self.connected_clients`. This is incorrect. The Foyer (Lobby) should stay open while the Engine sleeps.
2.  **WebSocket Decay**: Idle sockets are dropped by proxies after ~120s. We lack PING/PONG heartbeats.
3.  **Status Spam**: Handshakes trigger redundant "Strategic Sovereignty" messages on every reconnect.
4.  **Remote Thermal Pressure**: KENDER is probed continuously even when the Lab is idle, preventing remote GPU cool-down.

---

## 🏛️ SPRINT 25: GOALS & OBJECTIVES

### 🎯 GOAL 1: LOBBY RESIDENCY (FOYER STAY-ALIVE) [FEAT-327]
- [x] **Task 1.1**: Refactor `reflex_loop` in `acme_lab.py` to allow hibernation based strictly on `idle_time`. (VERIFIED: Hub detects hibernation while socket open).
- [x] **Task 1.2**: Update `client_handler` to support the `heartbeat=30.0` parameter. (VERIFIED: No disconnects during idle periods).
- [x] **Task 1.3**: Verify that incoming `[ME]` queries trigger a "Fast Wake" without dropping the socket. (VERIFIED via `test_hibernation_wake.py`).

### 🎯 GOAL 2: SOVEREIGNTY DEBOUNCING [FEAT-328]
- [x] **Task 2.1**: Implement state-aware broadcasting for "Strategic Sovereignty" to prevent spam. (VERIFIED: Log audit confirms 1 msg per state transition).
- [x] **Task 2.2**: Move initial status report to happen EXACTLY once per handshake. (DONE).

### 🎯 GOAL 3: REMOTE BRAIN COOL-DOWN [FEAT-329]
- [x] **Task 3.1**: Refactor `check_brain_health` to respect the `idle_time`. (DONE).
- [x] **Task 3.2**: Suspend health probes to KENDER if idle > 5 minutes. (VERIFIED via code audit and activity tracking).
- [x] **Task 3.3**: Resume probes immediately upon `text_input` or `user_typing`. (DONE).

---

## 🛠️ PHYSICAL STATE (Baseline)
- **Status**: OPERATIONAL.
- **VRAM**: 7.2GB / 11GB.
- **Hub Socket**: Persistent.
- **Remote Brain**: PROBING.

The Lab is now **STANDING**, **VOCAL**, and **STABLE**.

---

### ✅ Sprint [SPR-25.0] Accomplishments Summary:
*   **Lobby Residency Implemented**: Refactored the hibernation trigger to be based strictly on idle_time. The foyer (WebSocket lobby) now stays open indefinitely even when engines are hibernated, eliminating "Lobby Deadlock."
*   **Socket Persistence**: Added 30s PING/PONG heartbeats to all WebSockets to prevent Cloudflare and browser idle timeouts from dropping connections.
*   **Strategic Sovereignty Debouncing**: Implemented state-aware status reporting. "Strategic Sovereignty: PRIMARY" is now only broadcast upon a genuine state transition, eliminating console spam on reconnect.
*   **Remote Brain Cool-down**: Automated suspension of health probes to KENDER (remote Windows host) after 5 minutes of inactivity, allowing remote silicon to cool down during idle periods.

---

### 🏺 Retrospective: The Value of "Physician's Gauntlet" Verification

The testing was **absolutely critical**. While the first implementation stood up the correct architectural logic, the verification phase caught several "Silicon Traps" that would have resulted in immediate system failure or degraded performance.

#### 🕵️ Errors Caught During Verification:

1.  **The "Larynx Lock" Syntax Error**: I had accidentally left an empty `if` block in `acme_lab.py` (`if self.connected_clients:`). Without testing, the Lab would have failed to boot, and the Hub would have crashed immediately upon service restart.
2.  **Cognitive Cache Lag**: Verification revealed that while the engine was "Vocal," the Attendant's **30s TTL cache** was still reporting it as "Down." I had to implement a surgical cache invalidation (`_last_engine_check = 0`) to prevent the Attendant from murdering the engine with a redundant ignition cycle just as it finished waking.
3.  **The Atomic Anchor Bypass**: My initial test run failed because the test query didn't include the mandatory `[ME]` anchor. This confirmed that the **FEAT-227 Security Gate** was working perfectly, but reminded me that even our internal diagnostic tools must respect the "Physician's Law."
4.  **Idle Timer Deadlock**: Testing exposed a race condition where the engine would wake, but if the `last_activity` timer wasn't immediately reset in the Hub's `/wake` handler, the Lab would re-hibernate 5 seconds later because it still thought it was idle.

#### 🏺 Scars & ROI:
*   **The Trap**: Relying on "Logical Completion" rather than "Silicon Truth." My first implementation was logically sound but syntactically broken.
*   **The BKM**: Never trust an ignition sequence that hasn't been "Physically Asserted" by a cognitive probe.
*   **Final ROI**: High. The 15 minutes spent in the "Physician's Gauntlet" saved the Lab from a 3:00 AM failure during the next Dream Cycle.

The Lab is now verified **BATTLE-HARDENED**.
