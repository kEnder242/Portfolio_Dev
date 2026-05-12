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

- [ ] **Task 1.8: LoRA Adapter Reset (The Purge)**
    - **Why**: Persistent silicon-level corruption in `lab_sentinel_v1` is causing "Token Storms" and blocking the Dream Pass. Rebuilding from a clean baseline is required.
    - **How**: 1) Full Lab Stop. 2) Set `lora_name` to `null` in `infrastructure.json`. 3) Delete `/speedy/models/adapters/lab_sentinel_v1/`. 4) Lab Restart.
    - **Proof**: Hub logs show successful boot without LoRA load, and triage reasoning returns to 100% alphanumeric density.

---

## Phase 3: LORA STABILITY PROOFING [MAY 10 22:45-23:45]
**Status:** COMPLETE | Reasoning Fidelity Verified across all personas.

### 🎯 GOAL 4: INDIVIDUAL ADAPTER CERTIFICATION [TEST-50]
- [x] **Task 4.1 (Pinky Audit)**: Force Hub to use `cli_voice_v1` and verify characterful response. (PASS: Responsive and physically sane).
- [x] **Task 4.2 (Shadow Audit)**: Force Hub to use `shadow_brain_v2` and verify complex reasoning stability. (PASS: Returned "Metadata-driven design system").
- [x] **Task 4.3 (History Audit)**: Force Hub to use `lab_history_v1` and verify archive-lookup reasoning. (PASS: Standard technical identity confirmed).
- [x] **Task 4.4 (Base-Mode Certification)**: Verify Hub can still function in "No-LoRA" mode with 100% fidelity. (PASS: Responded correctly as Llama 3.2).

---

## 🏛️ SPRINT 28.0: THE "DEEP BREATH" FINAL HARDENING
**Status:** COMPLETE | Silicon Integrity and Resilience Confirmed

### 🏆 Sprint Retrospective (Scars & Victories):
1.  **The H1 Trap**: We discovered that vLLM's Soft Sleep (Internal Offload) causes persistent physical VRAM corruption on the RTX 2080 Ti. **Verdict**: H1 is deprecated; H2 (Engine Restart) is now the primary stable hibernate state.
2.  **Autonomous Recovery**: The Hub can now detect "Screaming" and autonomously trigger an H2 reset.
3.  **Task Safety**: The new `ResidentLifecycleTask` has eliminated async scope crashes, providing a stable foundation for the Nightly Forge.
4.  **UI Visibility**: The new "LEDGER" tab in `status.html` provides the Lead Engineer with historical proof of system health.


---

## Phase 4: THE RUDE 5x5 CERTIFICATION [MAY 10 23:30-00:30]
**Status:** COMPLETE | Transition Stability Certified

### 🎯 GOAL 5: TRANSITION STABILITY CERTIFICATION [TEST-51]
- [x] **Task 5.1 (Rude Gauntlet Dev)**: Create `src/debug/test_rude_gauntlet.py`. (DONE: Accelerated 5x5 script developed).
- [x] **Task 5.2 (Rude Certification)**: Execute the gauntlet and achieve 5/5 "Rude Wins." (PASS: Hub successfully handled 5 concurrent "Wake-on-Intent" queries across 5 H2 cycles with 0 physical corruption or deadlocks).
- [x] **Task 5.3 (Final Resilience Audit)**: Verify vLLM status remains suppressed (no spam) and telemetry ledger records all transitions. (PASS: Verified via console audit and Ledger UI).

---

## 🏛️ SPRINT 28.0: THE "DEEP BREATH" FINAL HARDENING
**Status:** COMPLETE & CERTIFIED | Physically and Logically Robust

### 🏆 Sprint Retrospective (Scars & Victories):
1.  **The H1 Trap**: We identified and deprecated H1 (Soft Sleep) due to persistent VRAM corruption.
2.  **The Rude Win**: We proved the Lab can survive a 5-node concurrent storm even when waking from a cold state.
3.  **The Mute Fix**: Refactored `process_query` to eliminate the recursive lock deadlock identified in real-world usage.
4.  **The Spam Fix**: Suppressed vLLM throughput messages during operational status.
5.  **UI Transparency**: Historical resource accounting is now live via the Status Ledger.

