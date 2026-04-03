# Sprint Plan: [SPR-18.0] Silicon Stability & Restoration
**Role: [SPRINT] - High-Fidelity State Management**
**Date:** April 3, 2026
**Status:** PROPOSED

> [!IMPORTANT]
> **GOAL:** Resolve the "Laundry List" of system janks: stabilize the Hibernation Wake-up sequence, restore the missing Alarm tasks, and fix the "Remote Lab Control" auth failures.

---

## 🩹 [BKM-012] Scars Retrospective (Why v17.x Janted)
Before diving into the implementation, we must acknowledge the "Scars" from previous attempts:
1.  **[SCAR-01] Key Desync:** We previously relied on "Key Guessing" in `status.html` (scraping the DOM for a CSS hash). This failed because browser caches and race conditions between the static site and the dynamic Attendant caused `401 Unauthorized` rejections.
2.  **[SCAR-02] The Spark Race:** The `spark_reload()` task was non-blocking. The Hub would report "READY" before the vLLM engine was actually warm, causing Pinky's Console to disconnect repeatedly during the "Handshake Loop."
3.  **[SCAR-03] Log Hijacking:** Large refactors accidentally disabled the `is_window` flag in the Alarm loop, leading to a silent failure where the system appeared "Nominal" but was actually "Lobotimized" (no background tasks running).

---

## 🏗️ Phase 1: Remote Control "Discovery" [FEAT-267]
**Context:** Remote Lab Control has been failing due to CORS issues and "guessing" the Lab Key. This is the foundation for all remote verification.

### Tasks:
- [ ] **Internal Discovery:** Update the Attendant's `status.json` to include `vitals.style_key` (the CSS hash).
- [ ] **UI Unification:** Modify `status.html` to read the key directly from the `status.json` polling loop. No more DOM scraping.
- [ ] **CORS Preflight:** Update `lab_attendant_v4.py` middleware to return `200 OK` for all `OPTIONS` requests, satisfying Cloudflare's security handshake.
- [ ] **Informative Errors:** Fix the `Response.text` race condition in the JS `fetch` handler to provide detailed feedback (e.g., "Invalid Key" vs "Connection Refused").

---

## 🏗️ Phase 2: The Waking State Machine [FEAT-265]
**Context:** Once Remote Control is stable (Phase 1), we formalize the transition from HIBERNATING to WAKING to READY to stabilize the "Vibe."

### Tasks:
- [ ] **State Transition:** Introduce `status = "WAKING"` in `acme_lab.py`.
- [ ] **Crosstalk Integration:** Update `status.json` and the frontend `mission-control.js` to show `[IGNITION IN PROGRESS]` when the Hub is in the `WAKING` state. Map `HIBERNATING`, `QUIESCED`, and `OFFLINE` to distinct visual indicators.
- [ ] **The "Wait Ready" Gate:** Modify the WebSocket handshake to **await** `self.engine_ready` (with a 60s timeout) if the status is `WAKING`. This ensures Pinky's Console doesn't see a `None` state and disconnect.

---

## ⏰ Phase 3: Alarm Restoration & Tiered Visibility [FEAT-266]
**Context:** The "Alarm Clock" is the highest-level logic. It depends on a stable Waking State (Phase 2) to ensure background tasks don't crash trying to talk to a "None" engine.

### Tasks:
- [ ] **Enable Window:** Set `is_window = True` and calibrate the loop to run every 60s.
- [ ] **Tiered Logging:**
    - **Nightly (02:00/03:00):** Log "Nothing to do" at `WARNING` level so it appears in the Interleaved Logs once per window.
    - **Nibble (Frequent):** Log only on **Execution** or **Error** to keep the dashboard clean.
- [ ] **Hibernation Wake:** Ensure the Alarm loop can trigger a `wake_up` for the Nightly Dialogue if the Lab is hibernating. Skip if a `MAINTENANCE_LOCK` or `LORA_TRAINING` task is detected.

---

## 🔬 Investigation Report: The "Laundry List" Analysis
Based on the deliberate investigation conducted on April 3, 2026:
- **Wake State:** Confirmed a race condition in `on_handshake` where the background `spark_reload` is fired without awaiting readiness, causing the immediate `None` state broadcast.
- **Alarm Loop:** Confirmed the `is_window` kill-switch is hardcoded to `False` in `acme_lab.py` (Line 423), causing the disappearance of all `[ALARM]` logs since late February.
- **Remote Control:** Confirmed `401 Unauthorized` responses from the Attendant were due to CORS preflight failures (OPTIONS method rejection) and stale CSS hash guessing in `status.html`.

---

## 🧪 Phase 4: Verification & Testing Strategy
To avoid "waffling" and speed up verification, we will employ the following surgical testing methods:

### 1. The "Time-Warp" (Alarm Verification)
- **Method:** Create a manual trigger file (`~/trigger_nightly`). The alarm loop will check for this flag every 30s to execute the "Nightly" logic regardless of the current time.
- **Goal:** Verify the `run_full_induction_cycle()` still works with the new REST-based Attendant.

### 2. The "Surgical Sleep" (State Machine Speed)
- **Method:** Temporarily reduce the `afk_timeout` to **30 seconds**.
- **Debug Flag:** Implement `--mock-engine` in `acme_lab.py` to bypass the vLLM check, allowing rapid state-machine UI testing without waiting for GPU weight offloading.

### 3. The "Internal Mirror" (Remote Control Audit)
- **Method:** Tunnel `localhost:9999` to a local environment to test `status.html` directly, bypassing Cloudflare to isolate CORS logic from Networking logic.

### 4. Test Catalog (Existing vs New)
| Component | Existing Test | New Test Design |
| :--- | :--- | :--- |
| **Hibernation** | `test_hibernation_cycle.py` | `test_state_waking.py`: Verify WS wait-gate |
| **Alarms** | `test_alarm_clock.py` | `test_triggered_induction.py`: Verify file-trigger path |
| **Auth** | `test_key_handshake.py` | `test_options_preflight.py`: Verify 200 OK on OPTIONS |
| **UI** | N/A (Manual) | `ui_parity_check.py`: Selenium/Playwright check of crosstalk bar |

---

## 📝 Logging & Diagnostics
- **Internal:** Add a "Header-Dump" to the Attendant's middleware to log the full `X-Lab-Key` and `X-Forwarded-For` headers during 401 events to predict Cloudflare behavior.
- **External:** Implement detailed error strings in `status.html` that report the `Response.status` code and the first 60 chars of the error body for live test debugging.
