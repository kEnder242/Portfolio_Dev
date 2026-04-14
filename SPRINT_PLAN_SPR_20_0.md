# Sprint Plan: [SPR-20.0] Mind Healing & Stability
**Status:** PLANNED | **Goal:** Refine triage logic and restore cognitive continuity through graceful handling.

---

## 🏛️ Section 1: COGNITIVE STATE REPORT

#### 1. Analysis of the Interaction Gap
The conversation experienced a logical disconnect during the recent trial due to two interlocking refinements needed in `cognitive_hub.py`:

*   **[ERR-05] Uncaught Attribute: `brain_online`**: During the transition to a callback-driven health system, the `run_shadow` method remained aligned to an internal attribute. This caused the query task to yield during shadow interjections.
*   **[ERR-06] Triage Type Alignment**: The \`lab\` node, providing triage hints via the standard transport, occasionally returns a structured object (dictionary) where the Hub's parser expects a serialized string. This triggers a \`TypeError: JSON object must be str, bytes or bytearray, not dict\`, resulting in repeated triage attempts and a fallback to safe-mode status.

#### 2. Stability Ledger

| Error ID | Symbol / Message | Finding | Impact |
| :--- | :--- | :--- | :--- |
| **ERR-05** | `AttributeError` | Call site mismatch in `run_shadow`. | Query task yields unexpectedly. |
| **ERR-06** | `TypeError: JSON object...` | Hub-side double-parsing of node hints. | Triage falls back to default state. |
| **ERR-07** | `Cognitive processing failed` | Hub-side notification of task yielding. | Informational; provides user context. |
| **ERR-08** | `Wait-Ready request failed` | Attendant API reaching timeout during JIT. | Status sync lag during heavy compute. |
| **ERR-09** | `Hibernation Persistence` | Weights remaining resident after idle window. | Resource efficiency not fully optimized. |

---

## 🏗️ Section 2: Technical Refinement Architecture

### 1. Unified Health Callback (Resolving ERR-05)
*   **Path:** `HomeLabAI/src/logic/cognitive_hub.py`
*   **Objective:** Fully align the Hub to the `get_vram_status()` callback.
*   **Surgical Analysis:** Nearby code including the `asyncio.gather` and `_process_node_stream` calls is physically stable and should NOT be modified. We are only changing the Boolean source for the shadow failover check.

### 2. Polymorphic Triage Parser (Resolving ERR-06)
*   **Path:** `HomeLabAI/src/logic/cognitive_hub.py`
*   **Objective:** Enhance the triage loop to be type-agnostic. By gracefully accepting both dictionaries and strings, we ensure that varying transport layers do not interrupt the cognitive flow.

### 3. Graceful Intent Buffering [FEAT-283]
*   **Path:** `HomeLabAI/src/acme_lab.py`
*   **Objective:** Implement an \`asyncio.Queue\` in the \`client_handler\` to hold user intent during the brief "Waking" window. This provides a smoother experience where the Lab "hears" the user immediately and responds as soon as the mind is resident.

### 4. Quiescent Offload Refinement (Resolving ERR-09)
*   **Current Status:** VRAM has remained resident at **~67.6% (7.6GB)** for the last 12 hours across multiple reboots. The automatic 600s idle trigger is reaching the engine, but physical offloading is occasionally bypassed.
*   **Historical Context:** Level 2 REST Offload was proven functional via manual \`curl\`. We confirmed \`VLLM_SERVER_DEV_MODE=1\` is resident in the service environment.
*   **Elegance Strategy:** Instead of aggressive reaps, we will implement **Client Deferral**.
 The Hub will pause active foyer traffic and heartbeat probes *gracefully* during the 30s weight-swap window, ensuring the engine has 100% of the PCIe bandwidth required for a clean offload.

---

## 📝 Section 3: Tasks & Tracking

### 🛠️ New Sprint Tasks (Graceful Restoration)
- [ ] **Task 1: Harmonize Hub Callbacks (ERR-05)**
    - Target: `cognitive_hub.py`. Complete the migration to `get_vram_status()`.
- [ ] **Task 2: Type-Agnostic Triage Parser (ERR-06)**
    - Target: `cognitive_hub.py`. Update the triage loop to handle structured objects gracefully.
- [ ] **Task 3: Implement [FEAT-283] Neural Buffer**
    - Target: \`acme_lab.py\`. Create \`self._neural_queue\` and implement the "Wait-for-Wake" drainer.
- [ ] **Task 4: Attendant Status Resilience (ERR-08)**
    - Target: `lab_attendant_v4.py`. Extend the status wait window to accommodate physical hardware latency.
- [ ] **Task 5: Refine Quiescent Hibernation (ERR-09)**
    - Target: `lab_attendant_v4.py`. Verify the idle-gate triggers and the "Quiet Window" VRAM reclamation.
- [ ] **Task 6: Graceful Client Deferral**
    - Target: `acme_lab.py`. Implement a temporary pause in heartbeat probes during state transitions to ensure a smooth offload.

### 🖇️ Continuous Improvement Stragglers
- [ ] **Verify Weight Mapping Timeline**: Ensure the 180s settle window is generous enough for a seamless user experience.
- [ ] **Activity Latch Audit [FEAT-287]**: Verify that active conversation naturally extends the residency window.
- [ ] **Ledger Integrity**: Confirm \`active_pids.json\` correctly reclaims ports after a hard service crash without leaving "Ghost Contexts."

---
**Governing Standard:** [BKM-020] High-Fidelity Sprint Documentation & [BKM-023] Surgical Preservation Protocol.
