# Sprint Plan: [SPR-23.0] Documentation Alignment & Daily Induction
**Status:** DRAFT | **Baseline:** Sprint 22 Stability [VER-22.5]

---

## 🏛️ Section 1: DOCUMENTATION AUDIT & REVIEW
**Scope:** Comprehensive review of foundational ledgers to align with Phase 15 Neural Relay and v6.0 Eternal Forge architectures.

### 📍 Current Gaps identified:
1.  **PROTOCOLS**: Lacks instructions for the new `quiescence_remaining` telemetry. Does not reflect the Non-Blocking Ignition strategy (still implies a sequential wait).
2.  **FEDERATED_STATUS**: Last updated April 13. Does not mention [FEAT-317] Absolute Foyer or the successful 5x5 Stability Gauntlet.
3.  **GEMINI.md**: Lifecycle states (WAKING vs BOOTING) are inconsistent with the latest `lab_attendant_v4.py` implementation.
4.  **FeatureTracker**: [FEAT-310] through [FEAT-318] are undocumented or partially documented.

### 🛠️ Recommended Update Plan:
- **Phase 1: Foundation Alignment**
    - [ ] Update `Protocols.md` to include surgical debugging BKMs for the log tailer.
    - [ ] Sync `00_FEDERATED_STATUS.md` with the VER-22.5 stability baseline.
- **Phase 2: Feature Pedigree**
    - [ ] Formalize [FEAT-313] through [FEAT-318] in `FeatureTracker.md`.
    - [ ] Document the "Hand-Crank" 5x5 verification protocol as a standard for high-fidelity silicon audits.
- **Phase 3: Operational Hardening**
    - [ ] Verify the 2:00 AM ALARM trigger and document the daily induction cycle logic in a new `DAILY_INDUCTION_BKM.md`.

---

## 🏛️ SPRINT 23: GOAL 1 - ALARM MONITORING & INDUCTION VERIFICATION
**Active Goal:** Verify the automated 2:00 AM daily induction cycle.
**Status**: [PENDING]

### 📍 Why & How
- **The Why**: To ensure the Lab correctly transitions from IDLE/HIBERNATING to OPERATIONAL at the scheduled hour without manual intervention.
- **The How**: 
    1.  Observe logs between 01:55 AM and 02:05 AM.
    2.  Verify `[ALARM]` trigger in `acme_lab.py`.
    3.  Verify the Attendant accepts the ignition request and successfully sparks the engine.

### 🛠️ Task List
21. **[ ] Goal 1: Alarm Verification**:
    - [ ] **21.1 [Watch] Pre-Alarm State**: Ensure Lab is HIBERNATING by 01:50 AM.
    - [ ] **21.2 [Verify] Alarm Spark**: Confirm signal 0xALARM is processed.
    - [ ] **21.3 [Verify] Induction Stability**: Confirm full operational state by 02:10 AM.

---

## 🏛️ SPRINT 23: LOST/NEUTERED FEATURES LEDGER
**Scope:** Forensic identification of architectural drift and lost timing fidelity.

### 📍 Findings:
1.  **[REGRESSION] Absolute Foyer Recovery missing Adaptive Backoff**
    *   **Code**: `lab_attendant_v4.py` (~line 376)
    *   **Finding**: `FEAT-317` (Absolute Foyer check) triggers `FOYER_RECOVERY` immediately via `asyncio.create_task` without consulting or incrementing `self.recovery_attempts`.
    *   **Impact**: Causes a 60-second ignition loop (governed only by the `_last_ignition_time` gate) instead of the intended 2m/4m/6m exponential backoff.
2.  **[REGRESSION] Premature Backoff Reset (The 2-Minute Trap)**
    *   **Code**: `lab_attendant_v4.py` (~line 1434)
    *   **Finding**: `recovery_attempts` is reset to 0 the moment `[OPERATIONAL] Hub foyer is fully synchronized.` is seen in the logs.
    *   **Impact**: If the Lab crashes shortly after sync but before stabilization, the backoff never "tapers off" past the first 125s (2m) step.
3.  **[INCONSISTENCY] Incorrect Intent on Physical Hub Failure**
    *   **Code**: `lab_attendant_v4.py` (~line 1423)
    *   **Finding**: When `foyer_alive` is False (Hub dead), recovery is triggered with `engine_only=True`.
    *   **Impact**: Incorrect intent; a dead Hub requires a full spark (`engine_only=False`) to restore the management layer.
4.  **[DOCUMENTATION] FEAT-302/318 Orphaned Status**
    *   **Finding**: `[FEAT-302] Adaptive Cooldown Tracking` and `[FEAT-318] Quiescence Telemetry` are active in code but missing from `FeatureTracker.md`.

### 🛠️ Restoration Strategy:
- **Task 22.1**: Refactor `mcp_start` to centralize the `recovery_attempts` increment and cooldown sleep logic.
- **Task 22.2**: Implement a **Stability Latch**: Only reset `recovery_attempts` if the Lab has maintained `OPERATIONAL` status for >300s.
- **Task 22.3**: Unify all recovery triggers (`VLLM_CRASH`, `FOYER_DEAD`, `REST_RECOVERY`) under the centralized backoff controller.
- **Task 22.4**: Sync `FeatureTracker.md` with the current state of Phase 15.

---

## 🏛️ RESOLUTION REPORT: Adaptive Recovery Cooldown [VER-23.1]
**Scope:** Forensic audit and restoration of the adaptive backoff system.

I identified and restored three critical regressions and one documentation gap that were causing the ignition loops you observed:

1.  **[FIX] Absolute Foyer Recovery Backoff**:
    *   **The Regression**: The new `Absolute Foyer` check (`FEAT-317`) was triggering recoveries instantly upon port failure, bypassing the `recovery_attempts` backoff logic.
    *   **Resolution**: Unified the foyer check under a new centralized `_trigger_adaptive_recovery` controller. It now correctly respects the 2m/4m/6m exponential backoff.
2.  **[FIX] The "2-Minute Trap" (Stability Latch)**:
    *   **The Regression**: `recovery_attempts` was being reset to 0 the moment the Hub reported initial synchronization. If the Lab crashed shortly after sync, the next recovery would start at 125s (2m) again, creating a perpetual loop.
    *   **Resolution**: Implemented **[FEAT-302] Stability Latch**. The recovery counter now only resets if the Lab maintains an `OPERATIONAL` status for at least **300 seconds (5 minutes)**. 
3.  **[FIX] Intent Inconsistency**:
    *   **The Regression**: Log monitor recoveries were using `engine_only=True` even when the Hub foyer was physically dead.
    *   **Resolution**: Corrected the recovery intent. If the management process (Hub) is confirmed ended, a full spark (`engine_only=False`) is now mandated.
4.  **[SYNC] Feature Tracker Alignment**:
    *   Formally documented **[FEAT-302] Adaptive Cooldown Tracking** and **[FEAT-318] Quiescence Telemetry** in the `FeatureTracker.md` ledger.

### 🛠️ PHYSICAL STATE (Restored)
- **Status**: STABLE.
- **Recovery Latch**: ARMED. (Backoff will reset if stable for 5 minutes).

---

## 🏛️ SPRINT 23: GOAL 2 - 5x5 STABILITY CERTIFICATION [FEAT-319]
**Active Goal:** Achieve 5 consecutive wins in the 5x5 gauntlet under BKM-029.
**Status**: [COMPLETE] | **Resolution**: [VER-23.2]

### 🛠️ Task List (Heads Down)
22. **[x] Goal 2: 5x5 Stability Certification**:
    - [x] **22.1 [Run] Win 1**: 5-minute idle. COMPLETE.
    - [x] **22.2 [Run] Win 2**: 10-minute idle. COMPLETE.
    - [x] **22.3 [Run] Win 3**: 15-minute idle. COMPLETE.
    - [x] **22.4 [Run] Win 4**: 20-minute idle. COMPLETE.
    - [x] **22.5 [Run] Win 5**: 25-minute idle. COMPLETE.

**[VERIFY] Hand-Crank Success**: ACHIEVED 5/5 WINS.
- **Stability**: Verified that the **Stability Latch [FEAT-302]** correctly manages the recovery backoff reset. 
- **Persistence**: Hub foyer (Port 8765) remained responsive through all cycles.
- **Log Fidelity**: **Crosstalk [FEAT-221]** rendering verified in UI for all engine logs.
- **Autonomous Recovery**: Verified that the Attendant correctly handles physical Hub failures with a full spark (`engine_only=False`) and respects the adaptive cooldown.

**Verdict**: The Lab is physically healthy and production-stable as of 08:15 PM.
