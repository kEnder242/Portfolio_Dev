# WORKBENCH_PLAN.md: The Acme Lab Evolution (v3.3)

## 🎯 Vision: The Collaborative Engineering Workbench
Transitioning from a "Search & Chat" interface to a stateful, dual-hemisphere engineering environment where AI and human collaborate on a persistent canvas.

---

## 🧱 1. The Temporal Moat (Grounding)
*   **The Problem**: AI confusing historical validation notes with real-time system state.
*   **The Fix**: Explicit "moat" logic in Pinky's triage layer.
    *   **[LIVE_SENSORS]**: Default for "today," "now," or hardware queries. (DCGM/Prometheus).
    *   **[PERSONAL_HISTORY]**: Requires a **Temporal Key** (e.g., "In 2019", "Check archives").
*   **Persona Calibration**: Pinky (Llama 3.1 8B) as the "Aware Gateway," Brain (Llama 3.1 70b/8b) as the "Grounded Architect."

---

## ⚪ 2. The Whiteboard (Stateful Canvas)
*   **Concept**: A persistent file-backed workspace (`whiteboard.md`) that represents the "Active Mind" of the Brain.
*   **UI Implementation**:
    *   A dedicated panel in `lab.html`.
    *   **Styling**: Engineering Canvas (Soft Dim Grey/Blue, not blinding white).
    *   **Flexibility**: Brain can "pin" thoughts, drafts, or code snippets here so they don't scroll away.
*   **Human-in-the-Loop**: Ability for the user to edit or paste into the whiteboard for the Brain to analyze.

---

## 📁 3. The Filing Cabinet (Archive Navigator)
*   **Concept**: A navigable tree of `~/AcmeLab`.
*   **Permission Model**:
    *   `archive/`: **READ-ONLY**. Bridge via `access_personal_history`.
    *   `drafts/`: **READ-WRITE**. Brain's output for new documents.
    *   `workspace/`: **READ-WRITE**. Location of `whiteboard.md`.
*   **UI Implementation**: Collapsible directory tree in the sidebar using pure HTML/CSS.

---

## 🛠️ 4. Tool Evolution (Modular Rigor)
*   **De-coupling the BKM**:
    1.  `start_draft`: Writes initial synthesis to the Whiteboard.
    2.  `refine_draft`: Brain iterates on the Whiteboard content based on user feedback.
    3.  `commit_to_archive`: Permanently saves the finalized draft to the Filing Cabinet.
*   **Telemetery Tools**: `vram_vibe_check` and `get_lab_health` (High-fidelity DCGM).
*   **Extension Tools**: `web_search` for current market or technical data outside the archive.

---

## 🚦 5. Phase 11 Roadmap (Active)
- [x] DCGM high-fidelity telemetry integration.
- [x] Modular Web Component navigation (v1.3).
- [x] Basic Whiteboard / Filing Cabinet scaffolding in `lab.html`.
- [ ] **Next**: Split BKM tool into `start_draft` and `commit_to_archive`.
- [ ] **Next**: Revert Whiteboard UI to "Engineering Canvas" theme.
- [ ] **Next**: Fix Filing Cabinet index loading in `lab.html`.
- [ ] **Future**: Implement multi-file "Workspace" context for the Brain.
