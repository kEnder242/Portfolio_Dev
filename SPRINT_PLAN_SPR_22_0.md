# Sprint Plan: [SPR-22.0] - The Sovereign Bridge
**Status:** ACTIVE | **Baseline:** Sprint 21 Hardening [VER-21.0]

## 🧬 RETROSPECTIVE: SPRINT 21 (Hardening v4.5)
**Goal:** Stabilize the "Sovereign Silence" by eliminating the 2-minute induction storm.

### 📍 Steps Taken (The Path of Precision)
1.  **Atomic Induction Mutex [FEAT-289]**: Moved the `last_induction_date` update to the *start* of the task loop. This fixed the race condition where slow model ignition would allow the next 60s loop to trigger a redundant spark.
2.  **Dream Guard [FEAT-292]**: Implemented a `pgrep` process check in the induction cycle to ensure `dream_voice.py` never spawns redundant instances.
3.  **Forensic Ignition [FEAT-294]**: Enhanced `spark_restoration` logging to include `Source` (e.g., `alarm_manual`) and `Intent` (`ACTIVE` vs `PASSIVE`).
4.  **Subprocess Logging**: Updated the Hub to capture and log the stdout/stderr of background tasks (Harvest/Dream) for better visibility.

### 🤕 Scars (The Mis-Steps)
- **The Accidental Amputation**: During a surgical `replace` call, I accidentally removed the `await self.run_full_induction_cycle()` call. This caused the manual trigger to be consumed without actually starting the work.
- **Mangled Logic**: A missing newline during an edit merged an `await` call with an `elif` block, causing a syntax error that required a second patch.
- **The Case-Sensitivity Ghost**: `dream_voice.py` was ignoring valid responses because it was looking for the literal string "Brain" while the Hub was sending "brain".
- **Tool Desync**: The `facilitate` tool had been removed from the nodes, but `InternalDebate` and the `Larynx Check` were still calling it, leading to silent "Unknown Tool" failures.

---

## 🎯 THE MISSION [SPR-22.0]
To harden the **Cross-Node Communication** (The Bridge) and ensure that the "Shadow" failover logic is as robust as the primary Sovereign path.

## 🛠️ TASK LIST

### 1. The Tooling Parity [FEAT-295]
- [ ] **Standardize `think`**: Ensure all nodes (Pinky, Brain, Archive, Lab) support the standardized `think` and `deep_think` interfaces to prevent "Unknown Tool" regressions.
- [ ] **Larynx Hardening**: Move the Larynx check to a dedicated class method that verifies *all* residents, not just the local Lab node.

### 2. The Passive Peeking [FEAT-291]
- [ ] **Status.html Alignment**: Update the frontend to handshake with `client="status"`.
- [ ] **Silent Heartbeat**: Ensure the Hub ignores "status" handshakes for ignition but still returns health metrics.

### 3. Integrated Stress Test
- [ ] **Queue Refactor**: Implement a "Fast Forward" flag for `dream_voice.py` to allow immediate processing of the last-added prompt without iterating through 6,000 skipped items.
- [ ] **Failure Mode Audit**: Simulate a primary node disconnect and verify the "Shadow" take-over timing.

---

## 🧪 VERIFICATION GAUNTLET
1.  **Run `test_induction_mutex.py`**: Verify baseline hardening still holds.
2.  **Trigger `status.html`**: Ensure it does NOT wake a hibernating lab.
3.  **Force-Fail Primary**: Monitor the transition to Shadow in the logs.

Critical Review of Centralized Hub Control

  I have reviewed the diff from 912176d to HEAD (today's "Centralization" arc). Here is my technical audit of the refactors:

  1. Necessary Refactors (The Wins)
   * [FEAT-289] Atomic Induction Gate: Moving self.last_induction_date = today to the top of the trigger block was Necessary. Without this, the 2-minute "Induction Storm" would always
     recur on slow model loads.
   * [FEAT-292] Dream Guard: The pgrep check is Necessary defensive coding to prevent VRAM thrashing by multiple dream_voice.py processes.
   * Subprocess Logging: Capturing stdout/stderr is Necessary for server-side forensics (previously, background task errors were completely invisible).

  2. Superfluous Refactors (The Bloat)
   * Forensic Ignition Log [FEAT-294]: While the intent is good, adding a new log signature without bridging it to the existing pager_activity.json (The UI) makes it Superfluous from a
     user perspective. It only adds noise to the internal server.log while the dashboard remains silent.

  3. Harmful Refactors (The Regressions)
   * Blocking Subprocesses: Using await proc.communicate() inside the scheduled_tasks_loop is Harmful.
       * Impact: The main loop is the heartbeat of the Lab. By awaiting a 2-hour Dream Pass, I effectively killed the Watchdog and the Hibernation Timer for that entire duration. The
         Lab could not check if it was idle because it was stuck waiting for a subprocess.
   * Logic Amputation (Manual Trigger): My accidental deletion of await self.run_full_induction_cycle() in commit 51d9788 was Harmful. It turned the manual trigger into a "Dead Man's
     Switch" that cleared the flag but did no work.
   * Fire-and-Forget Forge [FEAT-297]: This refactor is Harmful to state traceability. By moving the Forge turn to an asyncio.create_task, the Hub now logs "Induction Cycle Complete"
     while the physical GPU might be entering a 1-hour training lockdown. This creates a "Lying Status" anomaly.

  📋 Audit of Lost Features (Identified via Diff)

  ┌──────────────┬──────────────────────┬────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┬──────────┐
  │ ID           │ Feature              │ Note on Loss                                                                                                               │ Status   │
  ├──────────────┼──────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼──────────┤
  │ [FEAT-045]   │ Interleaved Forensic │ SUPERSEDE ERROR: The Hub took over tasks from standalone scripts but did not adopt their trigger_pager logic. Resulted in  │ LOST     │
  │              │ Ledger               │ UI silence after 3:05 PM.                                                                                                  │          │
  │ [FEAT-249]   │ Watchdog Heartbeat   │ THREAD BLOCK: await proc.communicate() blocked the heartbeat during Step 5. The watchdog was effectively dead for 2 hours. │ DEGRADED │
  │ [FEAT-265.1] │ Vocal Truth (Larynx  │ TOOL DESYNC: Replaced facilitate with think in code but not in all logic paths. Resulted in "Unknown Tool" errors in Step  │ BROKEN   │
  │              │ Check)               │ 1.                                                                                                                         │          │
  └──────────────┴──────────────────────┴────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┴──────────┘

  🕵️ Unknown Lost Feature: "The IDLE_GAUGE"
  I discovered a formerly unknown loss: [FEAT-249.2] Linear Idle Countdown.
  In the baseline, [IDLE_GAUGE] would log every 60s to show the countdown to hibernation. By using communicate() in the same loop, I broke the linearity of this gauge. It would
  "freeze" at 100s and then suddenly jump to 7200s, likely triggering a panic hibernation immediately after the task finished, or missing the window entirely if the model was still
  resident.

  📍 Corrective Recommendation
  I have been "over-optimizing" for the Python runtime while ignoring the Silicon/User interface. To fix this, I must:
   1. Non-Blocking Tasks: All background steps (1-6) must run in their own tasks, or use asyncio.wait_for with the heartbeat loop preserved.
   2. Restore the Pager: Port the "Hard-Won" trigger_pager logic from the Recruiter directly into the Hub's core.


