# Sprint Plan: [SPR-24.0] Dream Refinement & Hibernation Stability
**Status:** ACTIVE | **Baseline:** Sprint 23 Goal 3 [VER-23.3]

---

## 🏛️ RETROSPECTIVE: THE REAPING WAFFLE (Context & Scars)
**The Problem:** Over multiple sprints (20-22), the Lab has oscillated between an "Assassin" mindset (aggressive background reaping) and a "Governor" mindset (graceful deferral). 

### 🏺 Historical Scars:
1.  **The Assassin [SPR-18/11.3]**: Aggressive heartbeats collided with the 30s PCIe weight-offload window during sleep, triggering "false wakes" and stranding 67% of VRAM in zombie states.
2.  **The 'Adopted Hibernate' Failure [SPR-21]**: Despite LED architecture, the Watchdog remained "Token-Blind," misidentifying legitimate background workers as ghosts and reaping the entire family every 20s.
3.  **The Larynx Lock [SPR-22]**: Resume attempts triggered hangs during Brain synchronization, leading to a "Self-Reaping" death loop where the Lab died every 30s.
4.  **The FEAT-325 Regression [SPR-24]**: The "Nuclear Port Purge" implemented to fix Ollama zombies was too aggressive. It executed at the start of `mcp_start`, reaping port 8088 and 8765 **before** the Fast Wake path could trigger. This effectively killed hibernation by murdering the sleeping process before it could wake.

### 🕵️ Investigation Findings (May 5):
- **Assassin Overreach**: `cleanup_silicon(mode="GHOSTS")` reaps port 8765 (Hub) even when `engine_only=True` was requested. This causes the Hub to die during any engine-only recovery.
- **Wake Deadlock**: `mcp_start` reaps the "Deck" before checking `current_lab_mode == "HIBERNATING"`. This guarantees a cold start every time, wasting silicon cycles and time.
- **The Mandate**: Resuming from hibernation MUST wake the lab from sleep rather than "Pre-Reaping". 

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

---

### Forensic Report: Adopting the "Physician's Ledger" & Recognizing Old Traps

I have taken a step back and performed a deep audit of `DIAGNOSTIC_SCRIPT_MAP.md`, the git history, and the internal routines of `lab_attendant_v4.py`. I have identified several "Old Traps" I fell into today and realized I was re-implementing logic that has been hardened over months of Sprints.

#### 🕵️ Recognition of "Old Traps" & Waffling

1.  **The "Hunter" Regression (Today's nuclear reaping)**: 
    *   **The Trap**: I implemented a "Nuclear Port Purge" today at the start of ignition.
    *   **The History**: **Sprint 21 (April 16-17)** explicitly established the **"Blacklist Law"** and the **"Quiet Governor"** pattern. This was designed to stop exactly what I did: broad-spectrum port nuking that causes "silicon thrashing" and kills hibernating engines. 
    *   **The Waffle**: By re-introducing `fuser -k` at the start of `mcp_start`, I reverted the system to the **"Assassin"** mindset we spent two sprints (20 & 21) deprecating.

2.  **Redundant Tooling (Blindness to the Map)**:
    *   **The Trap**: I created `test_stability_fixed.py` and `vram_hog.py`.
    *   **The Adoption**: `DIAGNOSTIC_SCRIPT_MAP.md` already contains:
        *   **VRAM Guard**: `src/test_vram_guard.py` (Validation of >95% limits).
        *   **Attendant Sanity**: `src/debug/test_attendant_sanity.py` (API verification).
        *   **Resilient Wake**: `src/debug/test_wakeup.py` (Already exists to verify FEAT-315).
        *   **Dream Test**: `src/test_dream.py` (Already exists to validate the pipeline).

3.  **The "Vitals" Circular Wait**:
    *   **The Frustration**: I noted a frustration with "Cache Lag" in `_get_current_vitals`. 
    *   **The Reality**: This was already addressed in `FEAT-259.7` (Non-Blocking Readiness) and `FEAT-318.11` (Dynamic Reflex). I was fighting a battle that had already been won, but I was using the tools incorrectly.

#### 🧱 Forensic Audit of `lab_attendant_v4.py` (Overlooked Routines)

I discovered several routines in the Attendant that I should have utilized instead of coding new logic:
*   `scavenge_reality()`: This is the "God Move." It reconstructs the state of the silicon upon boot. I should have called this to resolve the Ollama zombie issue rather than a manual fuser.
*   `sync_family_ledger()`: This recursively authorizes child processes. It is the core of the "Governor" pattern.
*   `FEAT-262` Fast Wake Path: This was already there, but my "Nuclear" change today was executing *before* it, making it unreachable.

#### 😤 What is Frustrating Me (The "Catch")

The primary "catch" in the system right now is **Cognitive Truth Lag**. 
The Hub reports `status="HIBERNATING"`, but the Attendant's `_get_current_vitals` uses a **30s TTL** cache for the engine. If we wake the engine, there is a 30s window where the Attendant still "thinks" the engine is down. If a second request comes in during this window, the Attendant sees `engine_up=False` and triggers a **Full Ignition**, which reaps the freshly-woken engine.

#### 🎯 Refined Path: Adoption over Re-Implementation

I am pivoting Goal 2 and 4 to use the **hardened tools** from the map.

1.  **Stop Coding, Start Running**: I will use `src/debug/test_hibernation_wake.py` (already found on disk) and `src/debug/verify_vocal_liveliness.py` to verify the Lab.
2.  **Surgical Fix to TTL**: Instead of a "In-Flight Guard," I will simply **clear the `_last_engine_check` cache** whenever a Wake or Start is triggered. This is a one-line change that solves the 30s lag without adding new complexity.
3.  **Respect the Blacklist Law**: I will remove the "Nuclear" port-based reaping and instead rely on the existing `scavenge_reality()` and ledger-based `cleanup_silicon()`.
