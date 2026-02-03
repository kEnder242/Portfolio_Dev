# Federated Lab - Next Steps & Status
**Status:** Feb 3, 2026
**Context:** The "Intercom Pivot" and the "Federated" Architecture.

## 1. The Intercom Pivot
We have officially deprecated the Python-based Desktop Client (`intercom.py`) in favor of a Browser-based Web Interface.

*   **Logic:** A Web UI is more portable, simpler to deploy (no client-side python deps), and integrates naturally with the Portfolio dashboard.
*   **Archive:** The legacy Python code (microphone handling, sync scripts) has been preserved in `HomeLabAI/src/archive/legacy_intercom/` for reference.
*   **Target Architecture:**
    *   **Server:** `AcmeLab` (Python/WebSockets) on Port 8765.
    *   **Client:** `intercom.html` (JS/WebSockets) hosted via `Portfolio_Dev` (or `HomeLabAI/web`).

## 2. Immediate Action Plan
1.  **Build `intercom.html`:** A lightweight "Class 1" interface (HTML/JS) that connects to `ws://localhost:8765`.
2.  **Verify Audio:** Test browser-based Microphone input (MediaStream API) vs the legacy PyAudio approach.
3.  **Bridge the Projects:** Ensure `Portfolio_Dev` documents can link to or embed this Intercom.

## 3. Environment Strategy (Recap)
*   **HomeLabAI:** Heavy ML Env (`.venv` w/ PyTorch).
*   **Portfolio_Dev:** Light Env (`.venv` w/ Requests).
*   **Communication:** Strictly via HTTP/WebSockets. No shared code imports.
