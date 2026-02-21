# 🧪 Dev_Lab: The Federated Silicon Environment
**The Immutable Bootloader [v4.3]**

> [!CAUTION]
> **IMMUTABILITY PROTOCOL:** This document is a navigational primer. Do NOT modify this file to track sprints, mandates, or features. 
> 
> **ROUTING PROTOCOL:** Always refer to the **Document Role Routing Table** below to ensure your contributions and queries are targeted to the correct "Truth Anchor." Avoid creating new files for existing categories.

Welcome, Agent. You are operating within a **Federated Lab** architecture.

## 🏛️ Project Architecture (Co-Equal Seats)
*   **[HomeLabAI/](./HomeLabAI/) (The Brain):** Heavy compute, NeMo STT, and RAG memory.
*   **[Portfolio_Dev/](./Portfolio_Dev/) (The Face):** Static synthesis, professional dashboard, and public airlock.

## 🧭 Document Role Routing Table
| If you are looking for... | Go to... | Role |
| :--- | :--- | :--- |
| **Global Context & Cold Start** | `BOOTSTRAP.md` | **The Bootloader** |
| **Operational Protocols**| `Protocols.md` | **The Law (BKM-001+)** |
| **Diagnostic Rundown** | `DIAGNOSTIC_RUNDOWN.md` | **The Physician's Ledger** |
| **Active Tasks & Agent State** | `GEMINI.md` | **The State Machine** |
| **Milestones & Success History** | `00_FEDERATED_STATUS.md` | **The God View** |
| **Architecture "Why" & Mission** | `ENGINEERING_PEDIGREE.md`| **The Philosophy/Laws** |
| **Feature DNA & Code Mapping** | `FeatureTracker.md` | **The Relational Matrix** |

## 📜 The Archival Process
Every revision of this bootloader MUST be mirrored in **`Portfolio_Dev/docs/archive/`**.

**MODIFICATION PROTOCOL:**
To update this "Immutable" file:
1.  **Snapshot:** Copy the current root `BOOTSTRAP_vX.Y.md` to the archive.
2.  **Increment:** Create a new `BOOTSTRAP_vX.Z.md` in the root.
3.  **Sync:** Update all cross-document pointers (GEMINI.md, 00_MASTER_INDEX.md) to the new version.
4.  **Cleanup:** Remove the previous version from the root directory.

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
