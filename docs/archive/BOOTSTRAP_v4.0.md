# 🧪 Dev_Lab: The Federated Silicon Environment
**The Immutable Bootloader [v4.0]**

Welcome, Agent. You are operating within a **Federated Lab** architecture.

## 🏛️ Project Architecture (Co-Equal Seats)
This environment consists of two primary, interdependent projects. Neither is secondary; they are the "Brain" and the "Face" of the same entity.

*   **[HomeLabAI/](./HomeLabAI/) (The Brain):** Heavy compute, NeMo STT, vLLM/Ollama inference, and RAG memory. This is the silicon-level logic center.
*   **[Portfolio_Dev/](./Portfolio_Dev/) (The Face):** The "Field Notes" static synthesis, professional dashboard, and public airlock. This is the strategic synthesis center.

## 📜 The Archival Process (Immutability Protocol)
This document is the **Immutable Bootloader**. To prevent accidental corruption, modification, or functional transformation (e.g., conversion into a script), we maintain a versioned history.

*   **Active Anchor:** The root `./BOOTSTRAP_vX.Y.md` is the primary entry point.
*   **Archive Location:** Every revision MUST be mirrored in **`Portfolio_Dev/docs/archive/`**.
*   **Modification Rule:** Never modify the bootloader without creating a new versioned snapshot in the archive first. This ensures agents can always "boot" from a known-good textual state.

---

## 🚀 Mandatory Ramp-Up Sequence
**PRIORITY 1: CONTEXTUALIZATION.** Do not jump to "Active Tasks" or "Phases" until you have verified the hardware and internalized the Law.

### 1. Orientation (The "Map Room")
Read **[Portfolio_Dev/00_MASTER_INDEX.md](./Portfolio_Dev/00_MASTER_INDEX.md)**.
This is your primary hub for navigating architectural blueprints and historical logs.

### 2. The God View (The "Truth Anchor")
Read **[Portfolio_Dev/00_FEDERATED_STATUS.md](./Portfolio_Dev/00_FEDERATED_STATUS.md)**.
This tracks global milestones across both projects. Ignore other status docs if they conflict.

### 3. Recent Learnings (The "Scars")
Read **[Portfolio_Dev/RETROSPECTIVE_FEB_11_2026.md](./Portfolio_Dev/RETROSPECTIVE_FEB_11_2026.md)**.
Essential for understanding recent stabilization efforts and environmental hangups.

### 4. Diagnostic Instruments (The "Physician's Ledger")
Read **[HomeLabAI/docs/DIAGNOSTIC_RUNDOWN.md](./HomeLabAI/docs/DIAGNOSTIC_RUNDOWN.md)**.
This is the index of all tests and profiling tools needed to verify Silicon stability.

### 5. The Strategy & Rules (The "Law")
Read **[Portfolio_Dev/DEV_LAB_STRATEGY.md](./Portfolio_Dev/DEV_LAB_STRATEGY.md)** and **[HomeLabAI/docs/Protocols.md](./HomeLabAI/docs/Protocols.md)**.
These define the Clean Room policy, Inter-Process Communication (IPC) rules, and operational shorthands (QQ, AFK).

---

## 🛠️ Global Execution Commands
*   **Start Lab**: `curl -X POST http://localhost:9999/start`
*   **Check Status**: `curl http://localhost:9999/status`
*   **Hard Reset**: `curl -X POST http://localhost:9999/hard_reset`
*   **Build Site**: `python3 Portfolio_Dev/field_notes/build_site.py`
