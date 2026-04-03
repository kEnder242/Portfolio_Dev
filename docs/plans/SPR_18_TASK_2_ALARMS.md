# Agentic Plan: Task 2 - Alarm Restoration & Tiered Visibility [FEAT-266]

## 🎯 Goal
Restore the `scheduled_tasks_loop` in `acme_lab.py` and implement tiered logging to prevent UI spam while retaining critical execution records.

## 🧠 Context & "Why"
During a recent refactor, the alarm loop's trigger window (`is_window`) was hardcoded to `False`, effectively lobotomizing the system's ability to run nightly tasks (Recruiter, Forging) or background Nibbles. We need these tasks running, but they shouldn't spam the `interleaved system logs` with "Checking for work..." messages every few minutes. 

## 📍 Pointers & Paths
*   **Hub Logic:** `/home/jallred/Dev_Lab/HomeLabAI/src/acme_lab.py` (Focus on `scheduled_tasks_loop`).
*   **Feature Tracker:** `/home/jallred/Dev_Lab/Portfolio_Dev/FeatureTracker.md` (Update with FEAT-266).

## 🛠️ Implementation Steps
1.  **Re-enable Loop:** Modify `scheduled_tasks_loop` to remove the hardcoded `is_window = False` block. Implement dynamic time checks (e.g., 02:00 for Nightly Tasks).
2.  **Tiered Logging:**
    *   For Nightly Tasks: Log `[ALARM] Nothing to do` at `WARNING` level so it persists in the logs once per window.
    *   For Frequent (Nibble) Tasks: Only log on **Action Taken** or **Error** (silent on skips).
3.  **Resource Awareness:** Before triggering a wake from hibernation for an alarm, check if `MAINTENANCE_LOCK` exists or if `LORA_TRAINING` is active.
4.  **Feature Tracker Update:** Append `[FEAT-266] Alarm Restoration & Tiered Visibility` to `FeatureTracker.md`.

## 🧪 Testing Strategy
*   **Time-Warp Trigger:** Implement a file-watcher in the alarm loop for `~/trigger_nightly`. If this file exists, execute the nightly tasks immediately and delete the file. This avoids waiting for 2:00 AM.
*   **Hibernation Wake Test:** Ensure the file trigger successfully wakes the lab from `HIBERNATING` state.