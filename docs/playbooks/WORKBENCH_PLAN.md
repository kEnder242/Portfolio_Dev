# WORKBENCH_PLAN.md: The Acme Lab Evolution (v3.3)

## 🎯 Vision: The Collaborative Engineering Workbench
Transitioning from a "Search & Chat" interface to a stateful, dual-hemisphere engineering environment where AI and human collaborate on a persistent canvas.

---

## 🧱 1. The Context Moat (Grounding)
*   **The Problem**: AI confusing historical validation notes with real-time system state.
*   **The Soft Moat**: Instead of a binary block, the Archive is treated as a **Gated Resource**. 
    *   **[LIVE_SENSORS]**: The default reality. (DCGM/Prometheus).
    *   **[PERSONAL_HISTORY]**: Pinky avoids this by default unless the query implies a need for historical grounding.
*   **Behavioral Guardrail**: Pinky is an **Observer** of history, not an Author. He is strictly prohibited from modifying or "organizing" the `archive/` directory.

---

## ⚪ 2. The Whiteboard (Functional Canvas)
*   **Concept**: A persistent "Notepad-Fidelity" workspace (`whiteboard.md`) that represents the Brain's active reasoning.
*   **Functionality over Minimalism**:
    *   benchmark: `notepad.exe` (Undo, Edit, Select, Save).
    *   **Live Stream**: The Brain must use the Whiteboard actively for complex thoughts to prevent it from feeling like a "static report."
*   **Human-in-the-Loop**: The user can edit or paste content directly into the Whiteboard for the Brain to analyze or refine.

---

## 📁 3. The Filing Cabinet (Archive Navigator)
*   **Concept**: A navigable tree of `~/AcmeLab` with explicit permission zones.
*   **Structure**:
    *   `archive/`: **READ-ONLY**. (The Moat).
    *   `drafts/`: **READ-WRITE**. Brain's output for new BKMs/Docs.
    *   `workspace/`: **READ-WRITE**. Home of `whiteboard.md`.
*   **UI Implementation**: Functional directory tree in the sidebar (collapsible folders).

---

## 🛠️ 4. Tool Evolution (Modular Rigor)
*   **De-coupling the BKM**:
    1.  `start_draft`: Hits the Whiteboard with initial outline.
    2.  `refine_draft`: Brain iterates on the Whiteboard based on chat feedback.
    3.  `commit_to_archive`: Saves the result to the `drafts/` or `archive/` folder.
*   **Extension Tools**: 
    *   `web_search`: [TABLED] For market data (e.g., "Intel stock").
    *   `file_management`: Ability to add/remove files in `drafts/`.

---

## 🚦 5. Roadmap & Tabled Ideas
- [x] DCGM high-fidelity telemetry integration.
- [x] Modular Web Component navigation (v1.3).
- [ ] **Next**: Implement "Notepad-Fidelity" (Editable Whiteboard) in `lab.html`.
- [ ] **Next**: Fix Filing Cabinet index loading & Folder support.
- [ ] **Next**: Update Brain logic to use Whiteboard *during* reasoning.
- [ ] **Tabled**: Web Search API integration.
- [ ] **Tabled**: Multi-file "Project Context" for Brain.

---

## 💡 User Insights (Diff)
*   "The Whiteboard is a portal into the Brain's reasoning, not just a static report."
*   "benchmark: notepad.exe, not vscode. Functionality (undo/edit) is priority over minimalism."
*   "Archive is Read-Only; Workspace is Read-Write. Pinky must not be an aggressive architect of the past."