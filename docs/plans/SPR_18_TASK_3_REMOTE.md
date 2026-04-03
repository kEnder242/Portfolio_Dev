# Agentic Plan: Task 3 - Remote Control Discovery & CORS Fix [FEAT-267]

## 🎯 Goal
Resolve the `401 Unauthorized` and `Body has already been consumed` errors when using Remote Lab Control in `status.html`.

## 🧠 Context & "Why"
Remote commands fail because `status.html` tries to guess the Lab Key by scraping a CSS hash from its DOM, which is often stale due to browser caching. Furthermore, the requests are blocked by CORS preflight failures because the Attendant's middleware rejects `OPTIONS` requests with a 401.

## 📍 Pointers & Paths
*   **Attendant Middleware:** `/home/jallred/Dev_Lab/HomeLabAI/src/lab_attendant_v4.py` (Focus on `key_middleware`).
*   **UI Logic:** `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/status.html` (Focus on `triggerLabAction` and `pollStatus`).
*   **Feature Tracker:** `/home/jallred/Dev_Lab/Portfolio_Dev/FeatureTracker.md` (Update with FEAT-267).

## 🛠️ Implementation Steps
1.  **CORS Preflight Fix:** Modify `key_middleware` in `lab_attendant_v4.py` to immediately return `web.Response(status=200)` for any `request.method == "OPTIONS"`.
2.  **Key Discovery:** Update `status.html` to extract the `vitals.session` (or `vitals.style_key`) from the already-polled `status.json` and use it as the `X-Lab-Key`. Remove the CSS DOM scraping logic.
3.  **Robust Error Handling:** Fix the `response.text()` race condition in `status.html` fetch logic to cleanly display the first 60 characters of error responses.
4.  **Proactive Logging:** Add a "Header-Dump" in `lab_attendant_v4.py`'s 401 handler to log `X-Forwarded-For` and the received key to help debug Cloudflare tunnel stripping.
5.  **Feature Tracker Update:** Append `[FEAT-267] Remote Control Discovery` to `FeatureTracker.md`.

## 🧪 Testing Strategy
*   **Internal Mirror:** Use an SSH tunnel to `localhost:9999` and test `status.html` directly, proving the CORS and Key logic works before involving Cloudflare.
*   **External Cloudflare Test:** Trigger the action via `acme.jason-lab.dev` and check the Attendant's log for the Header-Dump to verify header preservation.