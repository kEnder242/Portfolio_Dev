# Sprint Plan: [SPR-19.0] The Stability Gauntlet
**Role: [SPRINT] - Lab Stabilization & Test Auditing**
**Date:** April 4, 2026
**Status:** ACTIVE

> [!IMPORTANT]
> **GOAL:** Transition the Lab from "Fragile Resident" to "Tested Professional." This sprint focuses on resolving visual ambiguity, implementing fail-safe resets for LLM garbage, and conducting a full audit of existing test suites to ensure long-term stability.

## 🏛️ Session Summary (April 4, 2026 Morning)
**Objective:** Restore visibility and implement protective gates for broken inference.

### ✅ Completed Tasks
1.  **[FEAT-221.1] Forensic Quips:** Enabled server-side logging for all UI broadcasts (`[BROADCAST]` tags in `server.log`).
2.  **[FEAT-271] Active Reasoning UI:** Implemented the `WORKING` state. The Intercom now displays **"🧠 THINKING..."** during inference.
3.  **[FEAT-270] Lobotomy Gate:** Integrated a **Gibberish Detector** in `CognitiveHub`. Detects binary garbage and triggers a Nuclear Reset (`os._exit(1)`) to clear broken CUDA states.
4.  **[FEAT-272] Sovereignty Clarity:** Refined status messages to distinguish between **PRIMARY** (4090) and **SHADOW** (2080 Ti) models.
5.  **[HYGIENE]:** Purged the hardcoded "Systems nominal" default from the frontend and archived stale logs.

---

## 🧪 The Stability Gauntlet (Active Task)
**Role:** [AUDIT] - Comprehensive Test Execution & Reporting

### 📍 Phase 1: Test Discovery & Mapping
*   [x] Inventory all existing tests in `HomeLabAI/src/tests`, `debug/`, and root.
*   [x] Categorize by: Smoke, Unit, Integration, and Hardware-Dependent.
*   [ ] Map tests to current [FEAT] IDs.

#### 📊 Test Inventory Map
| Category | Primary Instruments | Purpose |
| :--- | :--- | :--- |
| **Smoke** | `test_attendant_sanity.py`, `test_liveliness.py`, `test_brain_smoke.py` | Verify basic port bindings and engine presence. |
| **System** | `test_lab_integration.py`, `test_mcp_integration.py`, `test_lifecycle_gauntlet.py` | End-to-end flow from Intercom to Node response. |
| **Stability** | `test_hibernation_cycle.py`, `test_vram_guard.py`, `test_assassin_regression.py` | Validate VRAM reclamation and process sparing. |
| **Forensic** | `test_live_fire_triage.py`, `test_forensic_logging.py`, `test_grounding_fidelity.py` | Audit LLM output quality and logging integrity. |

### 📍 Phase 2: Execution & Subjective Reporting
*   [ ] Execute the "Large Portion" of the test suite.
*   [ ] **Rule:** Do not force passes. Report subjective results for ambiguous outcomes.
*   [ ] **Goal:** Identify stability regressions, not 100% pass marks.

### 📍 Phase 3: Forensic Hardening
*   [ ] Fix identified stability bugs (Verify with re-run).
*   [ ] Append Retrospective.

---
**Governing Standard:** [BKM-020] High-Fidelity Sprint Documentation & [BKM-023] Surgical Preservation Protocol.
