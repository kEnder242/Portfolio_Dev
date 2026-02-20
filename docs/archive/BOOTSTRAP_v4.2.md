# 🧪 Dev_Lab: The Federated Silicon Environment
**The Immutable Bootloader [v4.2]**

> [!CAUTION]
> **IMMUTABILITY PROTOCOL:** This document is a navigational primer, NOT a notepad for design details. Do NOT modify this file to track sprints, mandates, or features. 
> 
> **BREADCRUMB PROTOCOL:** Session-specific documentation, retrospectives, and technical milestones must be indexed in **[Portfolio_Dev/00_MASTER_INDEX.md](./Portfolio_Dev/00_MASTER_INDEX.md)** (The Map Room) rather than this bootloader.

Welcome, Agent. You are operating within a **Federated Lab** architecture.

## 🏛️ Project Architecture (Co-Equal Seats)
This environment consists of two primary, interdependent projects. Neither is secondary; they are the "Brain" and the "Face" of the same entity.

*   **[HomeLabAI/](./HomeLabAI/) (The Brain):** Heavy compute, NeMo STT, vLLM/Ollama inference, and RAG memory. This is the silicon-level logic center.
*   **[Portfolio_Dev/](./Portfolio_Dev/) (The Face):** The "Field Notes" static synthesis, professional dashboard, and public airlock. This is the strategic synthesis center.

## 📜 The Archival Process
Every revision of this bootloader MUST be mirrored in **`Portfolio_Dev/docs/archive/`**. Never modify the root bootloader without creating a new versioned snapshot in the archive first.

---

## 🚀 Mandatory Ramp-Up Sequence
**PRIORITY 1: CONTEXTUALIZATION.** Do not jump to "Active Tasks" until you have verified the hardware and internalized the Law.

### 1. The Design Pedigree (The "Why")
Read **[HomeLabAI/docs/ENGINEERING_PEDIGREE.md](./HomeLabAI/docs/ENGINEERING_PEDIGREE.md)**.
**CRITICAL.** This document contains the Invariant Laws (Silicon Mandates, Memory Bridge, Unitary Tasks) that prevent catastrophic regressions.

### 2. Orientation (The "Map Room")
Read **[Portfolio_Dev/00_MASTER_INDEX.md](./Portfolio_Dev/00_MASTER_INDEX.md)**.
This is your primary hub for navigating architectural blueprints and historical logs. **Check this file for recent session breadcrumbs and retrospectives.**

### 3. The God View (The "Truth Anchor")
Read **[Portfolio_Dev/00_FEDERATED_STATUS.md](./Portfolio_Dev/00_FEDERATED_STATUS.md)**.
This tracks global milestones across both projects. Ignore other status docs if they conflict.

### 4. Diagnostic Instruments (The "Physician's Ledger")
Read **[HomeLabAI/docs/DIAGNOSTIC_RUNDOWN.md](./HomeLabAI/docs/DIAGNOSTIC_RUNDOWN.md)** and **[HomeLabAI/docs/TOOL_RUNDOWN.md](./HomeLabAI/docs/TOOL_RUNDOWN.md)**.
Index of all tests, profiling tools, and agentic capabilities needed to verify Silicon stability.

### 5. Operational Protocols (The "Law")
Read **[HomeLabAI/docs/Protocols.md](./HomeLabAI/docs/Protocols.md)** and **[Portfolio_Dev/DEV_LAB_STRATEGY.md](./Portfolio_Dev/DEV_LAB_STRATEGY.md)**.
Defines the Cold-Start procedure, Clean Room isolation, and the Resilience Ladder.

---

## 🛠️ Global Execution Commands
*   **Start Lab**: `curl -X POST http://localhost:9999/start`
*   **Check Status**: `curl http://localhost:9999/status`
*   **Hard Reset**: `curl -X POST http://localhost:9999/hard_reset`
*   **Build Site**: `python3 Portfolio_Dev/field_notes/build_site.py`
