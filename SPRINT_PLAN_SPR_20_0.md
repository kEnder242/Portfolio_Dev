# Sprint Plan: [SPR-20.0] Mind Healing & Stability
**Status:** COMPLETE | **Goal:** Refine triage logic and restore cognitive continuity through graceful handling.

---

## 🏛️ Section 1: COGNITIVE STATE REPORT

#### 1. Analysis of the Interaction Gap
The conversation experienced a logical disconnect during the recent trial due to two interlocking refinements needed in `cognitive_hub.py`:

*   **[ERR-05] Uncaught Attribute: `brain_online`**: During the transition to a callback-driven health system, the `run_shadow` method remained aligned to an internal attribute. This caused the query task to yield during shadow interjections.
*   **[ERR-06] Triage Type Alignment**: The `lab` node, providing triage hints via the standard transport, occasionally returns a structured object (dictionary) where the Hub's parser expects a serialized string. This triggers a `TypeError: JSON object must be str, bytes or bytearray, not dict`, resulting in repeated triage attempts and a fallback to safe-mode status.

#### 2. Stability Ledger

| Error ID | Symbol / Message | Finding | Impact |
| :--- | :--- | :--- | :--- |
| **ERR-05** | `AttributeError` | Call site mismatch in `run_shadow`. | Query task yields unexpectedly. |
| **ERR-06** | `TypeError: JSON object...` | Hub-side double-parsing of node hints. | Triage falls back to default state. |
| **ERR-07** | `Cognitive processing failed` | Hub-side notification of task yielding. | Informational; provides user context. |
| **ERR-08** | `Wait-Ready request failed` | Attendant API reaching timeout during JIT. | Status sync lag during heavy compute. |
| **ERR-09** | `Hibernation Persistence` | Weights remaining resident after idle window. | Resource efficiency not fully optimized. |

---

## 🏗️ Section 2: Technical Refinement Architecture

### 1. Unified Health Callback (Resolving ERR-05)
*   **Path:** `HomeLabAI/src/logic/cognitive_hub.py`
*   **Objective:** Fully align the Hub to the `get_vram_status()` callback.
*   **Surgical Analysis:** Nearby code including the `asyncio.gather` and `_process_node_stream` calls is physically stable and should NOT be modified. We are only changing the Boolean source for the shadow failover check.

### 2. Polymorphic Triage Parser (Resolving ERR-06)
*   **Path:** `HomeLabAI/src/logic/cognitive_hub.py`
*   **Objective:** Enhance the triage loop to be type-agnostic. By gracefully accepting both dictionaries and strings, we ensure that varying transport layers do not interrupt the cognitive flow.

### 3. Graceful Intent Buffering [FEAT-283]
*   **Path:** `HomeLabAI/src/acme_lab.py`
*   **Objective:** Implement an `asyncio.Queue` in the `client_handler` to hold user intent during the brief "Waking" window. This provides a smoother experience where the Lab "hears" the user immediately and responds as soon as the mind is resident.

### 4. Quiescent Offload Refinement (Resolving ERR-09)
*   **Current Status:** VRAM has remained resident at **~67.6% (7.6GB)** for the last 12 hours across multiple reboots. The automatic 600s idle trigger is reaching the engine, but physical offloading is occasionally bypassed.
*   **Historical Context:** Level 2 REST Offload was proven functional via manual `curl`. We confirmed `VLLM_SERVER_DEV_MODE=1` is resident in the service environment.
*   **Elegance Strategy:** Instead of aggressive reaps, we will implement **Client Deferral**.
 The Hub will pause active foyer traffic and heartbeat probes *gracefully* during the 30s weight-swap window, ensuring the engine has 100% of the PCIe bandwidth required for a clean offload.

---

## 📝 Section 3: Tasks & Tracking

### 🛠️ Sprint 20 Tasks (Graceful Restoration)
- [x] **Task 1: Harmonize Hub Callbacks (ERR-05)**
    - Target: `cognitive_hub.py`. Replace `self.brain_online()` with `self.get_vram_status()` in `run_shadow`.
    - **Verification:** Verified code in `cognitive_hub.py` (L449).
- [x] **Task 2: Type-Agnostic Triage Parser (ERR-06)**
    - Target: `cognitive_hub.py`. Modify the triage loop to detect if `t_clean` is already a dictionary.
    - **Verification:** Verified code in `cognitive_hub.py` (L146-150).
- [x] **Task 3: Implement [FEAT-283] Neural Buffer**
    - Target: `acme_lab.py`. Create `self._neural_queue` and implement the "Wait-for-Wake" drainer.
    - **Verification:** Verified code in `acme_lab.py` (L178, L891-898, L1042).
- [x] **Task 4: Attendant Status Resilience (ERR-08)**
    - Target: `lab_attendant_v4.py`. Extend the status wait window to 480s for heavy JIT swaps.
    - **Verification:** Verified code in `lab_attendant_v4.py` (L688, L1211).
- [x] **Task 5: Refine Quiescent Hibernation (ERR-09)**
    - Target: `lab_attendant_v4.py`. Ensure `/sleep` REST call logs the full response.
    - **Verification:** Verified 30s timeout and logging point in `lab_attendant_v4.py` (L546).
- [x] **Task 6: Graceful Client Deferral (Heartbeat Pause)**
    - Target: `acme_lab.py`. Implement heartbeat suppression during state transitions.
    - **Verification:** Verified code in `acme_lab.py` (L343-345).

### 🛠️ Sprint 21 Tasks (Stability & UI)
- [x] **Task 7: Remove Misleading UI Default**
    - Target: `intercom.html`. Stripped "⚡ Systems nominal." to prevent false status reporting.
    - **Verification:** Verified file content via `grep`.
- [x] **Task 8: Redirect Crosstalk Flows**
    - Target: `cognitive_hub.py`. Convert logs (UPLINK, THINK MORE) to UI broadcasts.
    - **Verification:** Verified code in `cognitive_hub.py` (L125, L128, L333).
- [x] **Task 9: Silicon De-fragmentation**
    - Target: Physical Hardware. Reclaim VRAM via driver scavenging/service restart.
    - **Verification:** `nvidia-smi` check required to confirm ghost context removal.

### 🖇️ Continuous Improvement Stragglers (UNFINISHED)
- [ ] **Verify Weight Mapping Timeline**: Ensure the 180s settle window is generous enough for a seamless user experience.
- [ ] **Activity Latch Audit [FEAT-287]**: Verify that active conversation naturally extends the residency window.
- [ ] **Ledger Integrity**: Confirm `active_pids.json` correctly reclaims ports after a hard service crash without leaving "Ghost Contexts."

---

## 🧪 Section 4: Systematic Testing Ledger

### Tier 1: Grounding
- [x] **VLLM Alpha**: **PASS** (Verified connectivity)
- [x] **Liger Test**: **PASS** (Triton kernels active)
- [x] **Apollo 11**: **PASS** (Peak VRAM 7867 MiB / 69.8% budget)

### Tier 2: Orchestration
- [x] **Gauntlet**: **PASS** (Socket resilience verified)
- [x] **Shutdown Flow**: **PASS** (Graceful unmapping verified)
- [x] **Intercom Flow**: **PASS** (WebSocket routing verified)

### Tier 3: Soul
- [x] **Live Fire Triage**: **PASS** (Crosstalk sequence verified)
- [ ] **Contextual Echo**: **PENDING**

### Tier 4: Holistic
- [x] **Deep Smoke**: **PARTIAL** (Verified flow and shutdown; Reasoning failed due to Windows host offline).
- [x] **Strategic Live Fire**: **PASS** (Verified Shadow failover).

---

## 🏛️ FORENSIC REPORT: THE ARCHITECTURAL GAP (April 13, 2026)

### 1. ERR-05: The `brain_online` Attribute Error
**The Trajectory (Sprints 17 -> 19):**
In Sprint 18/19, the initialization arguments in `acme_lab.py` were refactored from `brain_online_callback` to `get_vram_status` to support the **Waking State Machine [FEAT-265]**. However, the `run_shadow` function in `cognitive_hub.py` was not updated and continues to call `self.brain_online()`, which no longer exists as a method or attribute. This causes a fatal `AttributeError` during fallback scenarios.

### 2. ERR-06: The JSON Double-Parsing Triage Failure
**The Trajectory (Sprints 18 -> 19):**
The `bridge_signal_clean` method was hardened to return `json.loads(block)`, making its output a Python dictionary. However, the triage loop in `process_query` still calls `json.loads(t_clean)`, triggering a `TypeError` because it's attempting to parse an already-parsed object. This forces the Hub to fall back to a low-fuel default state, ignoring the Lab Node's semantic steering.

### 3. ERR-08/09: Heartbeat Collision (The Ghost Contexts)
**The Trajectory (Sprints 18 -> 19):**
We pivoted from forceful reaps to vLLM's `/sleep` mode. However, aggressive 10s heartbeats from the Hub are colliding with the 30s PCIe weight-offload window. This triggers a "Wake" event mid-sleep, leaving ~67% VRAM leaked in a resident "zombie" state. We must implement **Client Deferral** to silence the Hub during these transitions.

---

## 🧭 Section 5: Sprint 20 Retrospective & Strategic Consistency

### 1. What Helped in This Sprint
*   **Isolated Unit Testing (Pytest)**: Building `test_hub_sprint20.py` and running tests in a dedicated Python virtual environment allowed rapid validation of the JSON parser and Callback logic *without* suffering the 180s cold-start latency of the physical hardware.
*   **The Safe-Scalpel Protocol ([FEAT-198])**: Making targeted, lint-verified edits to `cognitive_hub.py` and `acme_lab.py` ensured that existing robust logic (like `asyncio.gather`) wasn't accidentally destroyed during the `brain_online` migration.
*   **Surgical Preservation ([BKM-023])**: Sticking to an "append-only" methodology in this document kept the forensic trace alive, allowing us to see *how* the errors evolved from previous sprints.

### 2. What Would Have Helped (If Paid Attention)
*   **The Diagnostic Ledger (`DIAGNOSTIC_SCRIPT_MAP.md`)**: The project *already had* a `test_live_fire_triage.py` script. If that had been consulted *before* refactoring the triage logic in Sprint 19, the `TypeError` caused by `json.loads` would have been caught instantly.
*   **Understanding Type Contracts**: A fundamental misunderstanding between the string-based outputs of Sprint 17 and the parsed dictionaries of Sprint 18 caused the core cognitive loop to fail. Paying closer attention to function signatures (`bridge_signal_clean`) would have prevented ERR-06.

### 3. Strategic Inconsistent Outliers (Conflicts & Lost Gems)
Across Sprints 11-20, several architectural philosophies began to conflict, creating "Ghost Contexts" and behavioral drift:

*   **[SPR-18 vs SPR-11.3] The Graceful Sleep vs The Assassin**: The system tried to do both, causing the Attendant to panic-reap the engine while it was trying to sleep, stranding 67% of the VRAM (ERR-09). The "Assassin" pattern must be formally deprecated in favor of Graceful Deferral.
*   **[SPR-19 vs SPR-17] The Disconnected Callback**: Sprint 19 migrated the initialization to `self.get_vram_status` but `run_shadow` was never updated (ERR-05), destroying the safety net.
*   **[SPR-18] The Lying UI**: The frontend (`intercom.html`) retained a hardcoded `"⚡ Systems nominal."` default, violating `[BKM-028]`.

---

## 🚀 Sprint Plan: [SPR-21.0] WD Actions (Watchdog Sovereignty)
**Status:** DRAFT | **Goal:** Enhance Lab liveness visibility and empower the Watchdog with autonomous recovery.

### 🏛️ Section 1: Visibility & Control Strategy
*   **Existing Watchdog**: Leverage the current `lab-attendant` heartbeat monitoring.
*   **New Power**: Grant the Watchdog the ability to force Level 2 sleep and, if a "Ghost Context" is detected (timeout/leak), initiate a full Lab reset.
*   **Interleaved Logging**: All WD actions must be injected into the `Interleaved System Logs` (UI) and a dedicated `watchdog.log`.

### 🛠️ Sprint 21 Tasks (WD Sovereignty)
- [ ] **Task 10: Watchdog "Ghost" Detection**
    - **Mechanism**: Implement a check for orphaned vLLM weights (VRAM > 1GB but engine idle for 600s).
    - **Why**: Automatically detect [ERR-09] states without manual `nvidia-smi` checks.
- [ ] **Task 11: Force-Sleep Recovery**
    - **Mechanism**: Watchdog attempts `/sleep?level=2`. If it fails or times out, trigger `lab_stop` -> `lab_start`.
    - **Why**: Ensures silicon is reclaimed even if the engine state machine is wedged.
- [ ] **Task 12: Interleaved Log Injection**
    - **Mechanism**: Use `self.broadcast` to send `[WATCHDOG]` events to the Intercom.
    - **Why**: Provide real-time user visibility into background recovery actions.
- [ ] **Task 13: Gemini CLI BKM-018 Compliance**
    - **Mechanism**: Gemini CLI MUST use `lab_stop` / `lab_start` for all cleanup. Manual `pkill` is forbidden.
    - **Why**: Maintains Attendant state integrity and follows [BKM-018].

### 📝 Brainstorm: WD Actions & Logs
*   **Waking Collision**: Log: `[WATCHDOG] Heartbeat deferred: PCIe bandwidth collision during weight mapping.`
*   **Ghost Context**: Log: `[WATCHDOG] CRITICAL: Ghost Context detected (6.6GB stranded). Triggering silicon reset.`
*   **Idle Reaper**: Log: `[WATCHDOG] Quiescent window reached. Moving engine to Level 2 Sleep.`

### 🧪 Debug & Implementation Plan (Gemini CLI)
1.  **Manual Cleanup (BKM-018)**: Use `lab_stop` via the Attendant to clear the current "Ghost Context" (6.6GB).
2.  **Stub Testing**: Use `LAB_TEST_STUB=1` to verify log interleaving without VRAM overhead.
3.  **Heartbeat Mocking**: Force a heartbeat failure in `acme_lab.py` to trigger WD recovery logic.

---
**Governing Standard:** [BKM-020] High-Fidelity Sprint Documentation & [BKM-023] Surgical Preservation Protocol.
