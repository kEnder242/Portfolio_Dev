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
*   [x] Execute the "Large Portion" of the test suite.
*   [x] **Rule:** Do not force passes. Report subjective results for ambiguous outcomes.
*   [x] **Goal:** Identify stability regressions, not 100% pass marks.

#### 📈 Stability Gauntlet Results (April 4, 2026)
| Instrument | Result | Subjective Observation |
| :--- | :--- | :--- |
| `test_attendant_sanity.py` | **PASS** | Heartbeat and state tracking are nominal. |
| `test_brain_smoke.py` | **PASS** | Primary engine core responding correctly to technical prompts. |
| `test_hibernation_cycle.py` | **PASS** | **CRITICAL:** Verified full cycle (Load -> Offload -> Reload -> Sync). |
| `test_broadcast_resilience.py`| **PASS** | Hub survives abrupt F5/Socket resets without crashing. |

### 📍 Phase 3: Forensic Hardening
*   [x] Fix identified stability bugs (Verify with re-run).
*   [x] Append Retrospective.

---

## 🏺 Session Retrospective (April 4, 2026)
**"The 50-Second Restoration"**

### 🧠 Strategic Synthesis
The primary discovery of this session was the "Restoration Illusion." We identified that the system was reporting `READY` based on socket availability, but failing when asked to *reason* because the model weights were still loading or the resident nodes hadn't finished their internal handshakes. By implementing **High-Fidelity Restoration [FEAT-265.8]**, we have mandated that the Lab only signals readiness *after* the engine passes a functional probe and all nodes report successful synchronization.

### 🩹 Scars & Technical Debt
*   **[SCAR] Hub Reaping:** The aggressive "Assassin" purges were occasionally killing the very Hub foyer that sparked them. The transition to **Conservative Reaping** (sparing the Hub port 8765) resolved this, but we must remain vigilant about "Ghost Hubs" that might survive a failed stop.
*   **[SCAR] Schema Drift:** The test suites revealed that several message paths (Cabinet, History Replay) lacked the `brain_source` field, causing parsing timeouts. We have hardened the `broadcast` method to enforce this schema at the root.

### 🚀 Next Steps
*   **MCP Instrument Audit:** The next session should focus on the `archive` and `browser` nodes, ensuring their specialized toolsets (listing files, reading web content) follow the new schema-hardened patterns.
*   **Induction Loop Verification:** Monitor the nightly Alarms to ensure the `WAKING` state handles automated triggers as reliably as manual handshakes.

**Status:** Sprint 19.0 Groundwork is **STABILIZED & VERIFIED**.

---
**Governing Standard:** [BKM-020] High-Fidelity Sprint Documentation & [BKM-023] Surgical Preservation Protocol.
