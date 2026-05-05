# Sprint Plan: [SPR-24.0] Dream Refinement & Hibernation Stability
**Status:** ACTIVE | **Baseline:** Sprint 23 Goal 3 [VER-23.3]

---

## 🏛️ RETROSPECTIVE: THE REAPING WAFFLE (Context & Scars)
**The Problem:** Over multiple sprints (20-22), the Lab has oscillated between an "Assassin" mindset (aggressive background reaping) and a "Governor" mindset (graceful deferral). 

### 🏺 Historical Scars:
1.  **The Assassin [SPR-18/11.3]**: Aggressive heartbeats collided with the 30s PCIe weight-offload window during sleep, triggering "false wakes" and stranding 67% of VRAM in zombie states.
2.  **The 'Adopted Hibernate' Failure [SPR-21]**: Despite LED architecture, the Watchdog remained "Token-Blind," misidentifying legitimate background workers as ghosts and reaping the entire family every 20s.
3.  **The Larynx Lock [SPR-22]**: Resume attempts triggered hangs during Brain synchronization, leading to a "Self-Reaping" death loop where the Lab died every 30s.
4.  **The Current Mandate [SPR-24]**: Resuming from hibernation MUST wake the lab from sleep rather than "Pre-Reaping" (killing and restarting). Pre-reaping is a time-sink and silicon-thrashing anti-pattern.

---

## 🏛️ SPRINT 24: GOALS & OBJECTIVES

### 🎯 GOAL 1: REFACTOR DIAMOND DREAM CYCLE [FEAT-067.2]
**Problem**: `dream_cycle.py` contains hardcoded Ollama ports (11434) and direct HTTP calls that bypass the Lab Attendant's VRAM guards.
- [ ] **Task 1.1**: Refactor `dream_cycle.py` to use the `BicameralNode` base class for model interaction.
- [ ] **Task 1.2**: Replace hardcoded `localhost:11434` with dynamic URI resolution from the Attendant API (`:9999/status`).
- [ ] **Task 1.3**: Implement "Attendant-Aware" ignition: Dreaming must request an engine start via the Attendant to ensure VRAM gates are respected.

### 🎯 GOAL 2: TEST SUITE - DREAMING INTEGRITY
- [ ] **Task 2.1**: Create `tests/test_dreaming.py` to verify end-to-end memory synthesis.
- [ ] **Task 2.2**: Verify that background Dreaming does NOT trigger a hibernation cycle mid-task.

### 🎯 GOAL 3: POST-DREAMING LIVELINESS
- [ ] **Task 3.1**: Verify the Lab is "Vocal" - responsive to API ping AND returns actual "Vocal" responose to a prompt (See "Vocal" in tools and docs) - immediately after a Dream Cycle finishes.
- [ ] **Task 3.2**: Ensure no zombie ports or PIDs are left behind after the Dream transition.

### 🎯 GOAL 4: HIBERNATION-TO-WAKE PRIORITY [FEAT-262.2]
- [ ] **Task 4.1**: Implement `tests/test_hibernation_wake.py`.
- [ ] **Task 4.2**: **CRITICAL**: Verify that the Lab uses the "Fast Wake Path" (HTTP `/wake_up`) instead of the "Pre-Reap Path" (SIGKILL + Restart).
- [ ] **Task 4.3**: Benchmark the "Wake" vs "Restart" time to confirm <10s availability.

---

## 🛠️ PHYSICAL STATE (Baseline)
- **Status**: STABLE (v4.1 Guardian active).
- **VRAM**: 1.0GB / 11GB.
- **Port 11434**: CLEAN (Reaped).
- **Port 8088**: STANDBY.
