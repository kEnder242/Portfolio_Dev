# Sprint Plan: [SPR-28.0] Lab Sleep States & Resilience Strategy
**Status:** DRAFT | **Theme:** "The Deep Breath" | **Target:** Zero-OOM Gaming Readiness

## 🧪 EXECUTIVE SUMMARY: THE "WAKE DEBT" ARCHITECTURE
Sprint 27 succeeded in achieving **Persistent Residency [FEAT-337]**, delivering sub-second wake times. However, this established a high **"Used RAM" Floor (~11GB)**, leaving insufficient headroom for high-performance external applications (Games). 

Sprint 28 introduces the **"Lab Sleep States" (H1-H3)**, a tiered degradation model that allows the user to trade wake-time for physical RAM headroom without losing remote orchestration.

---

## 🏛️ SECTION 1: THE HIBERNATION STATES (H-STATES)

| State | Name | Wake Time | RAM Gain | Action | Context |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **H1** | **Standby** | **< 1s** | **0 MiB** | Standard Level 2 Sleep | Baseline (Persistent Residents). |
| **H2** | **Lean Sleep**| **~20s** | **~3.1 GiB** | **STOP vLLM**, Keep Nodes | Trading weights for RAM headroom. |
| **H3** | **Deep Sleep**| **~60s** | **~4.5 GiB** | **STOP vLLM & Nodes** | **Game Mode**. Minimal footprint. |

### **Experimental Flexibility [RESEARCH-09]**
We will implement an **Independent Unloading** mechanism. Instead of rigid levels, the Attendant will support targeted killing of Lab-controlled groups (Engine vs. Foyer) to allow for H2-Partial experimentation (e.g., Keeping only the Archive node resident).

---

## 🏗️ SECTION 2: INDEPENDENT UNLOADING (WAKE DEBT ANALYSIS)

To optimize recovery, we must understand the "Wake Debt" of our components:

1.  **vLLM Engine (~3.1 GiB RAM / ~40s Debt)**:
    *   **The Weight**: Loading 3.2B weights from NVMe and initializing the KV Cache in VRAM.
    *   **The Gain**: Stopping vLLM is the single largest "Nice" RAM reclamation action.
2.  **Resident Nodes (~1.4 GiB RAM / ~20s Debt)**:
    *   **The Weight**: Spawning 7 Python processes and loading `SentenceTransformers` (Archive).
    *   **Outlier**: The **Archive Node** is the heavy init outlier (~10s). Keeping it resident while killing other nodes is a viable "Low Debt" strategy.

---

## 🛡️ SECTION 3: THE INCREMENTAL WATCHDOG [FEAT-341]

Recent unresponsiveness (May 09, 7pm) revealed that a crashed Hub leads to "Remote Blindness." We need a non-intrusive recovery loop.

### **Architecture: "The Gentle Nudge"**
1.  **Interleaved Logging**: The Attendant records Hub status (UP/DOWN/STALL) into the shared `telemetry_ledger.jsonl`.
2.  **Backoff Recovery**: If the Hub dies, re-ignition attempts occur at **1m / 5m / 15m** intervals.
3.  **Physical Guard**: Watchdog must verify **RAM < 90%** before recovery to prevent "Ignition Death Spirals" during high system load (Games).

---

## 🗓️ SPRINT 28: TASKS

### 🎯 GOAL 1: MULTI-LEVEL HIBERNATION [FEAT-340]
- [ ] **Task 1.1: Multi-Level API**
    - **Why**: Enable flexible state switching from `status.html`.
    - **How**: Update `mcp_hibernate` in `lab_attendant_v4.py` to accept `level=[1,2,3]`.
    - **Proof**: `curl /status` reports the correct target H-State.
- [ ] **Task 1.2: H2-Lean Implementation (vLLM Stop)**
    - **Why**: Reclaim 3GB RAM while keeping nodes alive for a 20s "Warmish" wake.
    - **How**: Update `cleanup_silicon(engine_only=True)` to forcefully terminate the vLLM APIServer and EngineCore.
    - **Proof**: `hog_report.py` confirms `Lab Controlled` drops by ~3.1GB while 7 nodes remain.
- [ ] **Task 1.3: H3-Full Implementation (Game Mode)**
    - **Why**: Absolute RAM recovery (4.5GB) for modern gaming.
    - **How**: Implement a sequential stop of the Hub followed by vLLM. Hub must handle `SIGTERM` gracefully via the new Lifecycle Task.
    - **Proof**: `free -h` shows system returning to the **7.2 GiB Floor**.

### 🎯 GOAL 2: RESILIENCE & VISIBILITY [FEAT-341]
- [ ] **Task 2.1: Incremental Watchdog**
    - **Why**: Autonomous recovery without thrashing silicon during OOM events.
    - **How**: Implement an `ExponentialBackoff` class in the Attendant pulse loop.
    - **Proof**: Logged timestamps in `journalctl` show increasing gaps between restart attempts.
- [ ] **Task 2.2: Event Logging (Nominal vs Crash)**
    - **Why**: Distinguish between "User stopped lab for a game" vs "Lab crashed on its own."
    - **How**: Add an `event_type` field to the telemetry ledger. `mcp_stop` tags as `NOMINAL`; Watchdog tags as `UNEXPECTED_FAILURE`.
    - **Proof**: `telemetry_ledger.jsonl` displays distinct tags for different shutdown reasons.
- [ ] **Task 2.3: UI Visibility (Status Ledger)**
    - **Why**: Expose the last 5 events to `status.html` for remote forensic auditing.
    - **How**: Update the `/status` endpoint to return the tail of the telemetry ledger.
    - **Proof**: The "Diagnostics" section of `status.html` shows a chronological list of state changes.

---

## 🛠️ ONBOARDING & POINTERS FOR NEW SESSIONS
*   **Primary Tool**: `src/debug/hog_report.py` (The Resource Balance Sheet).
*   **Validation**: `src/debug/test_warm_wake.py` (Benchmark latency).
*   **Mandate**: Follow **BKM-029** (4-Step Loop) for all state-machine modifications.
*   **Caution**: Avoid the "Reaping Trap"—focus only on processes identified in the **Lab Controlled** category.
