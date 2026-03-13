# Sprint Plan: [SPR-13.0] Silicon Stability & Forensic Clarity
**Status:** ACTIVE | **Goal:** Resolve VRAM instability, implement Split Status Model, and harden Forensic Ledger.

## 🎯 THE MISSION
To stabilize the **Unified 3B Base** on the 2080 Ti (11GB) following the vLLM 0.17 transition and the recent 02:40 AM "Silicon Scrub" crash. This sprint hardens the **Forensic Ledger [FEAT-151]**, implements the **Split Status Model [FEAT-045]**, and decouples the **EarNode** from nightly background tasks to preserve VRAM headroom.

---

## 🏗️ ARCHITECTURAL MANDATES

### 1. The Atomic File Swap Protocol [BKM-022]
*   **Purpose:** Ensure filesystem atomicity for all file updates.
*   **Mechanism:** Standardize on `.tmp` + `os.replace` for all state snapshots (e.g., yearly JSONs) and the **Forensic Ledger**.
*   **Intent:** Protect UIs and workers from reading partially written files without overwriting chronological history.

### 2. The Split Status Model [FEAT-045/151]
*   **Volatile Status (Liveness):** Real-time system health and indicators (e.g. VRAM pressure) retrieved directly from the Lab Attendant API (:9999/heartbeat).
*   **Forensic Ledger (History):** An append-only, atomic-write-protected chronological record (`pager_activity.json`) that preserves all historical alerts and state transitions.

### 3. Cumulative Synthesis [FEAT-127]
*   **Mandate:** Archive refinement must layer new technical insights onto existing history.
*   **Gate:** Enforce strict semantic de-duplication (0.85 similarity) within the same calendar day to prevent redundant narratives while ensuring no previous work is lost.

---

## 🧪 FORENSIC TRIAGE & REPRODUCTION (The 02:40 AM Crash)

### 1. Crash Analysis (Post-Mortem)
*   **Trigger:** Critical System Load (VRAM/Load) at 02:40 AM on March 13.
*   **Forensic Evidence:** `HomeLabAI/attendant.log` confirms a Watchdog SIGTERM.
*   **Hypothesis:** Concurrent execution of the **Nightly Recruiter** and **Slow Burn Scanner** exceeded the 11GB VRAM budget, potentially due to the **EarNode** residency and vLLM 0.17 KV cache allocation.

### 2. Reproduction [LIVE FIRE]
*   **Tool:** `HomeLabAI/src/debug/test_apollo_vram.py`.
*   **Action:** Run "Token Burn" with vLLM 0.17 and EarNode active to identify the physical peak.
*   **Goal:** Determine if `gpu_memory_utilization` in `infrastructure.json` needs adjustment (currently 0.5-0.6).

---

## 🏗️ SPRINT PHASES

### PHASE 1: Forensic Hardening (The Ledger)
- [ ] **Implementation (Generalist):** Refactor `lab_attendant_v2.py` and `acme_lab.py` to use the **Atomic File Swap Protocol [BKM-022]** for `pager_activity.json`.
    - *BKM Detail:* Use `open("file.tmp", "w")` -> `json.dumps()` -> `os.replace("file.tmp", "file")`.
- [ ] **Implementation (Generalist):** Implement the **Forensic Ledger [FEAT-151]** logic to capture raw log deltas using the `TraceMonitor` and append them to the ledger during state transitions.

### PHASE 2: VRAM Optimization & EarNode Decoupling
- [ ] **Characterization:** Run `test_apollo_vram.py` on vLLM 0.17 to verify the "333MiB Breakthrough" and characterize the KV cache footprint.
- [ ] **Decoupling [FEAT-145]:** Update `acme_lab.py` and `mass_scan.py` to allow disabling the **EarNode** during heavy background tasks.
    - *Logic:* If `disable_ear=True` is passed, the Hub must skip `self.sensory.load()`.
- [ ] **Watchdog Refinement:** Adjust the **VRAM Watchdog [FEAT-036]** to trigger a "Downshift" (Tier 2/3) instead of an immediate "Hard Stop" during moderate pressure, reserving "Hard Stop" for true critical thresholds (>98%).

### PHASE 3: Watchdog Recovery & Resilience
- [ ] **Recovery Logic:** Implement "Auto-Restart" in the Lab Attendant's watchdog. 
    - *Behavior:* If the Lab is found "Dead" (no heartbeat) but no Maintenance Lock exists, the Attendant should attempt **One (1) Autonomous Ignition** before alerting the Pager.
- [ ] **UI Visibility:** Update `status.html` to pull "Liveness" from the heartbeat API and "History" from the ledger, implementing the **Split Status Model**.

### PHASE 4: Resilience Ladder Restoration [FEAT-069/148]
- [ ] **Historical Review:** Re-integrate the "Downshift" logic removed in commit `0441f45`.
- [ ] **Tiered Governance:** 
    - **Tier 1 (vLLM):** Primary high-throughput mode.
    - **Tier 2 (Ollama Fallback):** Auto-restart into Ollama with a 1B/3B model if VRAM pressure is >85% but <95%.
    - **Tier 3 (Hard Stop):** SIGTERM only when VRAM > 98% or load > 12.0.
- [ ] **Document Update:** Refine **FEAT-180** in `FeatureTracker.md` to be "Optional/Configurable" rather than a mandatory mandate.

---

## 🛠️ BKM PROTOCOLS (The Implementation Law)

### [BKM-REPRO] VRAM Crash Reproduction
*   **One-liner:** `python3 HomeLabAI/src/debug/test_apollo_vram.py --engine vLLM --burn`
*   **Core Logic:** Allocates max context window to force VRAM fragmentation and KV cache spill.
*   **Trigger:** VRAM usage > 10.5GB on 2080 Ti.
*   **Scars:** Previous tests failed to account for EarNode's 1.2GB static footprint.

### [BKM-PATCH] Atomic Ledger Write
*   **One-liner:** `python3 HomeLabAI/src/debug/run_scalpel.py --file pager_activity.json --atomic`
*   **Core Logic:** `tempfile.NamedTemporaryFile` + `shutil.move` for atomic replacement of the JSON ledger.
*   **Trigger:** Every `CRITICAL` or `WARNING` alert generation.

---

## 🎼 ORCHESTRATION (The Conductor)
*   **Conductor Role:** Track the sprint milestones in `Portfolio_Dev/conductor/tracks/spr-13-0/plan.md`.
*   **Generalist Role:** Execute the surgical Python refactors for `lab_attendant_v2.py` and `mass_scan.py`.
*   **DNA Guard:** Main Agent verifies all changes against `FeatureTracker.md` before final sign-off.

---
*Reference: [BKM-018] Orchestrator-First Mandate*
