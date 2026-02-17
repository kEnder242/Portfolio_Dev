# Federated Lab Status: The "God View"
**Date:** Feb 15, 2026
**Scope:** Architecture, Bridges, and Public Infrastructure.

## 🧭 Navigation
*   **🧠 The Brain (Backend):** [HomeLabAI/ProjectStatus.md](../HomeLabAI/ProjectStatus.md)
*   **📂 The Face (Frontend):** [GEMINI.md](./GEMINI.md)

## 🎯 Active Initiative: "Bicameral Dispatch" (Phase 9.5)
**Goal:** High-fidelity persona concurrency and strategic career matching.

## 🚧 High-Priority Bridge: The Map Room
*   **[ACTIVE] Feature Tracker Forensic Buildup**:
    *   **Goal:** Construct `FeatureTracker.md` based on `FeatureTrackerDesign.md`.
    *   **Task:** Mine current session context for the "Initial Identity" draft before context-drift occurs.
    *   **Mandate:** Map the "Why" behind the Unity Pattern, Shadow Dispatch, and Bicameral Triage.

## ✅ Global Milestones (Feb 2026)
1.  **Unity Pattern Stabilized**: Unified the Lab nodes on Llama-3.2-3B-AWQ via vLLM with Liger kernels.
2.  **Silicon Headroom Verified**: Characterized 11GB VRAM budget with full stack + EarNode resident (~9.8GB peak).
3.  **Attendant Resilience**: Hardened Lab Attendant against zombie processes and non-blocking vLLM initialization.
4.  **Strategic Retrieval**: Connected Pinky to the 18-year archive via the Strategic Map integration.
5.  **Shadow Dispatch Prototype**: Integrated predictive intent detection into the transcription engine.

## 🔮 The Roadmap
*   **[ACTIVE] Unity Stabilization (v4.2)**:
    *   **Goal:** Harden the Unified Base and implement advanced sensory logic.
    *   **Current Focus:** **Amygdala v3 (Contextual interjection logic) & Shadow Dispatch.**
    *   **Scar (Feb 15 evening):**
        *   [HALT] System crash (z87) reported after Gauntlet run. Investigating OOM vs. Kernel Panic.
        *   [TODO] Hardened model resolution in `loader.py` pending verification after reboot.
        *   [TODO] Complete Phase 3 Barge-In verification and VRAM Heartbeat.
*   **[TODO] Phase 4: The Hierarchical Mind**: Connect Pinky as a **Consumer** of the Semantic Map.
*   **[TODO] Phase 5: Refined Persona**: Implement **Strategic Vibe Check** validation logic.
*   **[BACKLOG] Observability & Resilience Expansion**:
    *   **Deep Status Watchdog**: **(PRIORITY)** Replace brittle PID-based monitoring in Attendant with active port-binding verification (8765) and Pinky pings. PID check currently reports "Online" for zombie processes.
    *   **Autonomous Recovery**: Implement auto-restart and automated Downshift (vLLM -> Ollama) if Pinky fails health checks.
*   **[BACKLOG] Telemetry Resilience (Graphs Offline)**:
    *   **Root Cause Analysis**: Investigate recurring Prometheus Exit 255 (suspect WAL corruption or volume pressure).
    *   **Robust Recovery**: Add a watchdog task to the Attendant to monitor Docker container health (`field_prometheus`, `field_grafana`) and trigger `docker start` on failure.
    *   **Degraded Status**: Update `status.html` / `status.json` to report a "Degraded" state when telemetry is unreachable, rather than just masking the failure.

---

## 🛠️ Operational Protocols
### Website Build (Cache-Busting)
To force-clear browser caches after UI changes, run the automated build script:
`python3 field_notes/build_site.py`

### Diagnostic Instruments
Refer to **[HomeLabAI/docs/DIAGNOSTIC_RUNDOWN.md](../HomeLabAI/docs/DIAGNOSTIC_RUNDOWN.md)** for silicon verification and test suites.
