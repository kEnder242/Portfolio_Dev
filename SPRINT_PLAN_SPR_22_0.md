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
