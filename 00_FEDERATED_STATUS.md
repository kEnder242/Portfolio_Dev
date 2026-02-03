# Federated Lab Status: The "God View"
**Date:** Feb 3, 2026
**Scope:** Architecture, Bridges, and Public Infrastructure.

## 🧭 Navigation
*   **🧠 The Brain (Backend):** [HomeLabAI/ProjectStatus.md](../HomeLabAI/ProjectStatus.md)
*   **📂 The Face (Frontend):** [GEMINI.md](./GEMINI.md)
*   **📜 The Rules:** [DEV_LAB_STRATEGY.md](./DEV_LAB_STRATEGY.md)

## 🎯 Active Initiative: "The Web Intercom" (Phase 8)
**Goal:** Connect the static Portfolio (`notes`) to the active Brain (`acme`) via WebSockets, replacing the legacy Python client.
*   **Server:** `AcmeLab` (Port 8765) -> Needs to serve WebSocket API.
*   **Client:** `intercom.html` (Hosted on Portfolio) -> Needs to implement JS WebSocket client.
*   **Bridge:** `cloudflared` Tunnel mapping `acme.jason-lab.dev` -> `localhost:8765`.

## ✅ Global Milestones (Feb 2026)
1.  **Federated Architecture:**
    *   Defined "Shared Nothing" env policy (PyTorch vs Requests).
    *   Created `DEV_LAB_STRATEGY.md`.
2.  **Public Airlock (v3.1):**
    *   Deployed `www.jason-lab.dev` (GitHub Pages).
    *   Implemented "Systems Nominal" cross-site ping.
3.  **Security Layer:**
    *   Implemented "Knock" (Access Requests) for `notes.jason-lab.dev`.
    *   Documented BKM in `Portfolio_Dev/FIELD_NOTES_ARCHITECTURE.md`.

## 🔮 The Roadmap
*   **[TODO] Web Intercom:** Build `intercom.html` + `script.js`.
*   **[TODO] Voice Input:** Research MediaStream API for browser-based STT.
*   **[TODO] Sandbox:** Docker-based code execution for the Brain.
