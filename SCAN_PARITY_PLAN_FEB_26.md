# SCAN_PARITY_PLAN_FEB_26.md
**Goal:** Restore the Nightly Scan (Slow Burn) pipeline to a safe, polite, and functional state following raw_notes recovery.

## 1. 🏗️ Infrastructure: Mutex & Lock Hardening
Currently, the "Scanner" (Portfolio_Dev) and the "Hub" (HomeLabAI) are looking at different paths for the session lock.

*   **Action 1: Path Unification.** Force both `HomeLabAI/src/acme_lab.py` and `Portfolio_Dev/field_notes/utils.py` to use a single, absolute path for the lock file.
    *   Target: `/home/jallred/Dev_Lab/HomeLabAI/round_table.lock` (Standardizing on the Brain's location).
*   **Action 2: Smart Mutex Logic.** Update `acme_lab.py` to only release the lock when `len(self.connected_clients) == 0`.
*   **Action 3: API Mutex Endpoint.** Add a `/mutex` endpoint to `lab_attendant.py`.
    *   **GET /mutex**: Returns `{ "yielding": true }` if either the file lock exists OR the Hub's heartbeat indicates a session.
    *   **Why:** This allows the scanner to perform a single, non-blocking check via the Attendant rather than brittle file-watching.

## 2. 🛡️ Scanner Politeness (Slow Burn Recovery)
*   **Action 4: Librarian Protection.** Wrap `scan_librarian.py` in the `can_burn()` logic from `utils.py`. The Librarian is currently "loud" and ignores locks/load.
*   **Action 5: Utils Refit.** Update `field_notes/utils.py` to:
    1.  Check the Attendant's `/mutex` API first.
    2.  Fallback to checking the unified file-lock.
    3.  Continue using `os.getloadavg()` or Prometheus for silicon cooling.

## 3. ⚡ Processing Modes (Fast & One-Time)
*   **One-Time Burn (Debug Mode):** I have identified `field_notes/nudge_2024.py` as the existing "one-time" debug script. I will verify it is correctly re-chunking the 2024 data and running a fixed-count of `nibble.py` turns.
*   **Fast Burn:** I have identified `field_notes/force_feed.py` as the "Fast Burn" script.
    *   **Fix:** `force_feed.py` currently uses `nibble.py` (v1.5). It needs to be updated to call `nibble_v2.py` (v2.0) with a `--fast` flag that ignores `SLEEP_INTERVAL`.
*   **Backlog Sanitation:** I will run the Librarian once to re-classify the 1130 "Unknown" items in `queue.json` before starting the first burn.

## 4. 🔬 Validation Scenarios
1.  **Barge-In:** Start a "Slow Burn" (mass_scan), then connect to the Intercom. Verify the scanner detects the mutex and logs `[LOCK] Round Table Active. Entering Low-Power Wait...`.
2.  **Silicon Safety:** Start a heavy task (e.g. `nemo` or `vLLM`) and verify the scanner yields due to `MAX_LOAD`.
3.  **One-Time Recovery:** Run `nudge_2024.py` and verify it clears specific chunk state without wiping the entire `chunk_state.json`.

## 5. 🧬 Feature Tracker Alignment
*   **[FEAT-125] API-First Mutex:** (New) Transitioning from file-locks to Attendant API for background orchestration.
*   **[FEAT-126] Refined PGID Cleanup:** Ensuring `lab_attendant` successfully reaps the entire process tree of a yielded scanner if a "Force Start" is requested.

---
**Awaiting Buy-in.** I will document any additions or alterations to the FEAT and VIBE trackers in `FeatureTracker.md` as part of Step 1 once approved.
