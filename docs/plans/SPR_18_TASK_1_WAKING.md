# Agentic Plan: Task 1 - The Waking State Machine [FEAT-265]

## 🎯 Goal
Formalize the transition from `HIBERNATING` to `WAKING` to `READY` to prevent WebSocket disconnect loops when the engine is loading.

## 🧠 Context & "Why"
When a user handshakes the lab via `intercom.html` while it is `HIBERNATING`, `acme_lab.py` fires a background `spark_reload()` task but doesn't wait for it. The Hub immediately broadcasts its state to the client. Because the vLLM engine isn't up, the Hub reports a `None` state and drops the socket. This causes the UI to enter a "Disconnect/Reconnect" loop until the engine finally loads.
Additionally, the Crosstalk bar statically says "Systems nominal" even when offline or booting, which is discongruent.

## 📍 Pointers & Paths
*   **Hub Logic:** `/home/jallred/Dev_Lab/HomeLabAI/src/acme_lab.py` (Focus on `on_handshake` and `reflex_loop`).
*   **UI Status Bar:** `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/mission-control.js` and `status.html`.
*   **Feature Tracker:** `/home/jallred/Dev_Lab/Portfolio_Dev/FeatureTracker.md` (Update with FEAT-265).

## 🛠️ Implementation Steps
1.  **State Definition:** Introduce `self.status = "WAKING"` in `acme_lab.py` prior to initiating the `spark_reload()`.
2.  **WebSocket Gate:** In the `on_handshake` logic, if the state is `WAKING` or `HIBERNATING`, **await** an engine readiness check (with a timeout, e.g., 60s) before allowing resident nodes to anchor and broadcasting the state.
3.  **UI Updates:** Update `mission-control.js` to parse `HIBERNATING`, `QUIESCED`, `OFFLINE`, and `WAKING` from the status payload. Map these to distinct visual indicators (e.g., orange for waking/quiesced, gray for offline).
4.  **Feature Tracker Update:** Append `[FEAT-265] The Waking State Machine` under "State Management & Lifecycle" in `FeatureTracker.md`.

## 🧪 Testing Strategy
*   **Surgical Sleep:** Temporarily set `afk_timeout=30` in `acme_lab.py` to trigger rapid hibernation.
*   **Mock Engine:** Add a `--mock-engine` flag to `acme_lab.py` to bypass the actual vLLM wait, simulating a fast wake for UI testing.
*   **Console Stress:** Open multiple `intercom.html` tabs while hibernating to verify the WAKING state holds the connections open without crashing.