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
- [x] **Task 1.1**: Refactor `reflex_loop` in `acme_lab.py` to allow hibernation based strictly on `idle_time`, ignoring client count. (DONE)
- [x] **Task 1.2**: Update `client_handler` to support the `heartbeat=30.0` parameter in `WebSocketResponse`. (DONE)
- [x] **Task 1.3**: Verify that incoming `[ME]` queries from an open lobby correctly trigger a "Fast Wake" without dropping the socket. (VERIFIED via logic path)

### 🎯 GOAL 2: SOVEREIGNTY DEBOUNCING [FEAT-328]
- [x] **Task 2.1**: Implement state-aware broadcasting for "Strategic Sovereignty" to prevent spam. (DONE)
- [x] **Task 2.2**: Move the initial status report to happen EXACTLY once per handshake. (DONE)

### 🎯 GOAL 3: REMOTE BRAIN COOL-DOWN [FEAT-329]
- [x] **Task 3.1**: Refactor `check_brain_health` to respect the `idle_time`. (DONE)
- [x] **Task 3.2**: Suspend health probes to KENDER if the Lab has been idle for > 5 minutes. (DONE)
- [x] **Task 3.3**: Resume probes immediately upon `text_input` or `user_typing`. (DONE)

---

## 🛠️ PHYSICAL STATE (Baseline)
- **Status**: OPERATIONAL.
- **VRAM**: 7.2GB / 11GB.
- **Hub Socket**: Persistent.
- **Remote Brain**: PROBING.
