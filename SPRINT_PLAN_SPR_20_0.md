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
- [x] **Task 1: Harmonize Hub Callbacks (ERR-05)**
    - Target: `cognitive_hub.py`. Replace `self.brain_online()` with `self.get_vram_status()` in `run_shadow`.
    - **Verify:** `python3 src/tests/test_hub_sprint20.py` (PASS)
- [x] **Task 2: Type-Agnostic Triage Parser (ERR-06)**
    - Target: `cognitive_hub.py`. Modify the triage loop to detect if `t_clean` is already a dictionary. Clean up unreachable code in `bridge_signal_clean`.
    - **Verify:** `python3 src/tests/test_hub_sprint20.py` (PASS)
- [x] **Task 3: Implement [FEAT-283] Neural Buffer**
    - Target: `acme_lab.py`. Create `self._neural_queue` and implement the "Wait-for-Wake" drainer.
    - **Verify:** `python3 src/tests/test_lab_sprint20.py` (PASS)
- [x] **Task 4: Attendant Status Resilience (ERR-08)**
    - Target: `lab_attendant_v4.py`. Extend the status wait window to 480s for heavy JIT swaps.
    - **Verify:** `python3 src/tests/test_attendant_sprint20.py` (PASS)
- [x] **Task 5: Refine Quiescent Hibernation (ERR-09)**
    - Target: `lab_attendant_v4.py`. Ensure `/sleep` REST call logs the full response.
    - **Verify:** Code Audit (PASS)
- [x] **Task 6: Graceful Client Deferral (Heartbeat Pause)**
    - Target: `acme_lab.py`. Implement heartbeat suppression during state transitions.
    - **Verify:** `python3 src/tests/test_lab_sprint20.py` (PASS)


### 🖇️ Continuous Improvement Stragglers
- [ ] **Verify Weight Mapping Timeline**: Ensure the 180s settle window is generous enough for a seamless user experience.
- [ ] **Activity Latch Audit [FEAT-287]**: Verify that active conversation naturally extends the residency window.
- [ ] **Ledger Integrity**: Confirm `active_pids.json` correctly reclaims ports after a hard service crash without leaving "Ghost Contexts."

---

## 🏛️ FORENSIC REPORT: THE ARCHITECTURAL GAP (April 13, 2026)

### 1. ERR-05: The `brain_online` Attribute Error
**The Trajectory (Sprints 17 -> 19):**
In Sprint 18/19, the initialization arguments in `acme_lab.py` were refactored from `brain_online_callback` to `get_vram_status` to support the **Waking State Machine [FEAT-265]**. However, the `run_shadow` function in `cognitive_hub.py` was not updated and continues to call `self.brain_online()`, which no longer exists as a method or attribute. This causes a fatal `AttributeError` during fallback scenarios.

### 2. ERR-06: The JSON Double-Parsing Triage Failure
**The Trajectory (Sprints 18 -> 19):**
The `bridge_signal_clean` method was hardened to return `json.loads(block)`, making its output a Python dictionary. However, the triage loop in `process_query` still calls `json.loads(t_clean)`, triggering a `TypeError` because it's attempting to parse an already-parsed object. This forces the Hub to fall back to a low-fuel default state, ignoring the Lab Node's semantic steering.

### 3. ERR-08/09: Heartbeat Collision (The Ghost Contexts)
**The Trajectory (Sprints 18 -> 19):**
We pivoted from forceful reaps to vLLM's `/sleep` mode. However, aggressive 10s heartbeats from the Hub are colliding with the 30s PCIe weight-offload window. This triggers a "Wake" event mid-sleep, leaving ~67% VRAM leaked in a resident "zombie" state. We must implement **Client Deferral** to silence the Hub during these transitions.

---
**Governing Standard:** [BKM-020] High-Fidelity Sprint Documentation & [BKM-023] Surgical Preservation Protocol.

---

## 🔬 Section 4: Post-Sprint Retrospective & Diagnostic Report (April 14, 2026)

### 1. System Telemetry & Crash State
Despite completing the sprint tasks, the Lab has entered a terminal failure loop (`RECOVERY` mode) with the following trace evidence:
*   **Intercom Sockets:** Disconnected. The `status.json` reports `foyer_up: false`, indicating the Hub process (PID `8438`) has crashed or exited, taking port `8765` offline.
*   **Stuck Services:** The Attendant Watchdog is caught in an auto-restart loop. It detects the Hub process ending, waits 5s, and triggers `mcp_start` repeatedly.
*   **Stuck VRAM (Ghost Contexts):** The vLLM engine remains inactive, yet `nvidia-smi` reports **7196MiB** used with no owning process listed. Approximately **6.6GB** of VRAM is stranded in a "Ghost Context," likely due to an abrupt process termination during an active weight mapping.

### 2. Immediate Stability Tasks (Sprint 21.0)
- [ ] **Task 7: Remove Misleading UI Default**
    - Target: `Portfolio_Dev/field_notes/intercom.html`.
    - Action: Remove the hardcoded `"⚡ Systems nominal."` from the `#crosstalk-bar` div.
- [ ] **Task 8: Redirect Misrouted Crosstalk Flows**
    - Target: `HomeLabAI/src/logic/cognitive_hub.py`.
    - Action: Convert `logging.info` and `print` statements for UPLINK, THINK MORE, and Triage into `await self.broadcast` events.
- [ ] **Task 9: Silicon De-fragmentation**
    - Target: Physical Hardware.
    - Action: Reclaim the 6.6GB stranded VRAM. (Requires Attendant service restart or physical driver reload).

---

## 🧪 Section 5: Systematic Testing Ledger & Roadmap

### Tier 1: Foundational Telemetry & VRAM (The Grounding Phase)
- [ ] **`src/debug/test_vllm_alpha.py` (VLLM Alpha)**
    - *Goal:* Connectivity check for vLLM REST API.
    - *Why:* If the engine can't talk, the Hub can't think. 
    - *Fix Needed:* Increase initial handshake timeout to 180s.
- [ ] **`src/test_liger.py` (Liger Test)**
    - *Goal:* Verify Triton kernel acceleration.
    - *Why:* Prevents CUDA kernel crashes during heavy inference.
    - *Fix Needed:* Update target model path to current AWQ base.
- [ ] **`src/debug/test_apollo_vram.py` (Apollo 11)**
    - *Goal:* Profile peak VRAM during Token Burn.
    - *Why:* Validates the 11GB budget headroom.

### Tier 2: Orchestration & State Machine (The Attendant Phase)
- [ ] **`src/debug/test_lifecycle_gauntlet.py` (Gauntlet)**
    - *Goal:* Stress test rapid connect/disconnect cycles.
    - *Why:* Proves socket resilience and prevents Hub crashes from UI refresh.
- [ ] **`src/test_shutdown.py` (Shutdown Flow)**
    - *Goal:* Validate clean exit and PID cleanup.
    - *Fix Needed:* Confirm Level 2 `/sleep` correctly unmaps weights from VRAM.

### Tier 3: Persona & Triage Logic (The Soul Phase)
- [ ] **`src/debug/test_live_fire_triage.py` (Live Fire Triage)**
    - *Goal:* Verify parallel turn-bundling and triage intent.
    - *Fix Needed:* Incorporate `ERR-06` type-agnostic dict handling.
- [ ] **`src/debug/test_contextual_echo.py` (Contextual Echo)**
    - *Goal:* Verify "Shadow Moat" Pinky-ism stripping.

### Tier 4: Holistic Validation (The Deep Smoke Phase)
- [ ] **`acme_lab.py --mode DEEP_SMOKE` (Deep Smoke)**
    - *Goal:* End-to-end state machine validation.
- [ ] **`src/tests/test_strategic_live_fire.py` (Strategic Live Fire)**
    - *Goal:* Definitive hardware validation of PMM routing.

---
### 🗑️ Redundant / Deprecated Tests (For Review)
*   **`Strategic Sentinel`**: Deprecated by Triage logic.
*   **`The Assassin`**: Deprecated by graceful `/sleep` offloading.
*   **`JSON Fix Experiment`**: Merged into `test_hub_sprint20.py`.


---

## 🔬 Section 4: Post-Sprint Retrospective & Diagnostic Report (April 14, 2026)

### 1. System Telemetry & Crash State
Despite completing the sprint tasks, the Lab has entered a terminal failure loop (`RECOVERY` mode) with the following trace evidence:
*   **Intercom Sockets:** Disconnected. The `status.json` reports `foyer_up: false`, indicating the Hub process (PID `8438`) has crashed or exited, taking port `8765` offline.
*   **Stuck Services:** The Attendant Watchdog is caught in an auto-restart loop. It detects the Hub process ending, waits 5s, and triggers `mcp_start` repeatedly.
*   **Stuck VRAM (Ghost Contexts):** The vLLM engine (PID `50280`) remains active, with VRAM stubbornly locked at `67.8%`. Because the Hub crashed abruptly, it failed to trigger its `AsyncExitStack` cleanup routines, leaving the vLLM prefix cache populated and the weights fully mapped in the 2080 Ti.

### 2. UI Refinement Tasks (Crosstalk Alignment)
During the diagnostic sweep, I identified several hardcoded UI assumptions and misrouted data flows that are actively polluting the console and providing false system state guarantees to the user.

- [ ] **Task 7: Remove Misleading UI Default**
    - Target: `Portfolio_Dev/field_notes/intercom.html`.
    - Action: Remove the hardcoded `"⚡ Systems nominal."` from the `#crosstalk-bar` div. Replace it with `Awaiting neural uplink...` or a blank placeholder to prevent the UI from lying to the user during an actual system failure.
- [ ] **Task 8: Redirect Misrouted Crosstalk Flows**
    - Target: `HomeLabAI/src/logic/cognitive_hub.py` and `HomeLabAI/src/acme_lab.py`.
    - Action: The following diagnostic logs are currently printing to standard output/Pinky's console and must be converted to `self.broadcast({"type": "crosstalk"...})` events for proper visibility:
        1. `[HUB] Action Tag: UPLINK via {source}` (`cognitive_hub.py`)
        2. `[HUB] Action Tag: THINK MORE via {source}` (`cognitive_hub.py`)
        3. `[HUB] Neural Signal detected: trigger_morning_briefing` (`cognitive_hub.py`)
        4. `[HUB] SILICON LOBOTOMY: Engine is returning garbage.` (`cognitive_hub.py`)

---

## 🧪 Section 5: Systematic Testing Ledger & Roadmap

To establish a verified baseline going forward, I have organized the `DIAGNOSTIC_SCRIPT_MAP.md` into a layered integration test plan.

### Tier 1: Foundational Telemetry & VRAM (The Grounding Phase)
*Goal: Ensure the 2080 Ti hardware can handle the exact memory curves required by the weight swaps.*
- [ ] **`src/debug/test_vllm_alpha.py` (VLLM Alpha)**
    - *Why:* Pure connectivity check for the vLLM OpenAI-compatible endpoint. If this fails, nothing else matters.
    - *Fix Needed:* Ensure the timeout accounts for the 180s cold-start JIT compilation delay on Turing architectures.
- [ ] **`src/test_liger.py` (Liger Test)**
    - *Why:* Verifies Liger-Kernels are physically accelerating the engine without throwing Triton configuration errors.
    - *Fix Needed:* Needs to be updated to target the current unified `Llama-3.2-3B-AWQ` base rather than older Gemma paths.
- [ ] **`src/debug/test_apollo_vram.py` (Apollo 11)**
    - *Why:* The definitive "Token Burn" test. It allocates the KV cache fully to ensure we don't hit OOM errors mid-generation.

### Tier 2: Orchestration & State Machine (The Attendant Phase)
*Goal: Ensure the Lab can boot, hibernate, and survive harsh process manipulation without leaving Zombie PID contexts.*
- [ ] **`src/debug/test_lifecycle_gauntlet.py` (Gauntlet)**
    - *Why:* Stress tests the Hub with rapid connect/disconnect cycles (e.g., the user spamming F5 on the Intercom). Essential for verifying `aiohttp` socket resilience.
- [ ] **`src/test_shutdown.py` (Shutdown Flow)**
    - *Why:* Validates the clean exit sequences and PID cleanup.
    - *Fix Needed:* Must be updated to confirm the new `mcp_hibernate` Level 2 offload logic behaves identically to the old `os.killpg` assassin pattern.
- [ ] **`src/test_intercom_flow.py` (Intercom Flow)**
    - *Why:* End-to-end local test of the Python CLI client to verify the WebSockets and handshakes are actually routing to the Brain.

### Tier 3: Persona & Triage Logic (The Soul Phase)
*Goal: Ensure the routing layer actually understands intent and maintains the "Lead Engineer" persona.*
- [ ] **`src/debug/test_live_fire_triage.py` (Live Fire Triage)**
    - *Why:* Rapid verification of parallel turn-bundling and hybrid (Pipe/JSON) triage.
    - *Fix Needed:* Ensure it incorporates the newly fixed `ERR-06` type-agnostic JSON parser.
- [ ] **`src/debug/test_contextual_echo.py` (Contextual Echo)**
    - *Why:* Verifies persona-aware echo behavior and ensures the "Shadow Moat" is actively stripping Pinky-isms (like "Narf!") from Sovereign output.
- [ ] **`src/tests/test_agentic_backtrack.py` (Agentic Backtrack)**
    - *Why:* Verifies the Strategic Pivot logic. If the Hub detects a hallucination, it must properly backtrack to Pinky.

### Tier 4: Holistic Validation (The Deep Smoke Phase)
*Goal: End-to-end integration proving the lab can function autonomously as a resident service.*
- [ ] **`acme_lab.py --mode DEEP_SMOKE` (Deep Smoke)**
    - *Why:* Full state-machine validation: Ingest -> Reason -> Dream -> Recall.
- [ ] **`src/tests/test_strategic_live_fire.py` (Strategic Live Fire)**
    - *Why:* The definitive physical hardware validation of the PMM routing and fidelity lifecycle.
    - *Fix Needed:* Requires verifying the "Neural Buffer" (Task 3) correctly queues requests while the engine handles the heavy `DEEP_SMOKE` reasoning.

---
### 🗑️ Redundant / Deprecated Tests (For Review)
*These tests are currently flagged in the ledger but are architecturally obsolete based on recent pivots.*
*   **`Iron Gate Audit` / `Strategic Sentinel`**: Flagged as STALE. The triage logic has entirely replaced the old Regex-based "Amygdala filtering."
*   **`The Assassin` / `Ghost Hunter`**: Deprecated. Sprint 19's pivot to vLLM's graceful REST `/sleep` offloading completely removes the need for `os.killpg` or `fuser -k` atomic reaping.
*   **`JSON Fix Experiment`**: Standalone sandbox code from Sprint 18. The `bridge_signal_clean` method is now fully integrated and unit-tested directly in `test_hub_sprint20.py`.

---

## 🧭 Section 6: Sprint 20 Retrospective & Strategic Consistency

### 1. What Helped in This Sprint
*   **Isolated Unit Testing (Pytest)**: Building `test_hub_sprint20.py` and running tests in a dedicated Python virtual environment allowed rapid validation of the JSON parser and Callback logic *without* suffering the 180s cold-start latency of the physical hardware.
*   **The Safe-Scalpel Protocol ([FEAT-198])**: Making targeted, lint-verified edits to `cognitive_hub.py` and `acme_lab.py` ensured that existing robust logic (like `asyncio.gather`) wasn't accidentally destroyed during the `brain_online` migration.
*   **Surgical Preservation ([BKM-023])**: Sticking to an "append-only" methodology in this document kept the forensic trace alive, allowing us to see *how* the errors evolved from previous sprints.

### 2. What Would Have Helped (If Paid Attention)
*   **The Diagnostic Ledger (`DIAGNOSTIC_SCRIPT_MAP.md`)**: The project *already had* a `test_live_fire_triage.py` script. If that had been consulted *before* refactoring the triage logic in Sprint 19, the `TypeError` caused by `json.loads` would have been caught instantly.
*   **Understanding Type Contracts**: A fundamental misunderstanding between the string-based outputs of Sprint 17 and the parsed dictionaries of Sprint 18 caused the core cognitive loop to fail. Paying closer attention to function signatures (`bridge_signal_clean`) would have prevented ERR-06.

### 3. Strategic Inconsistent Outliers (Conflicts & Lost Gems)
Across Sprints 11-20, several architectural philosophies began to conflict, creating "Ghost Contexts" and behavioral drift:

*   **[SPR-18 vs SPR-11.3] The Graceful Sleep vs The Assassin**: 
    *   *Origin*: In Sprint 11.3, `[FEAT-119] Socket-Aware Assassin` was built to aggressively reap processes (`os.killpg`) to free VRAM. 
    *   *Conflict*: In Sprint 18, `[FEAT-262] vLLM Sleep Mode` was introduced for graceful REST `/sleep` offloads. 
    *   *Result*: The system tried to do both, causing the Attendant to panic-reap the engine while it was trying to sleep, stranding 67% of the VRAM (ERR-09). The "Assassin" pattern must be formally deprecated in favor of Graceful Deferral.
*   **[SPR-19 vs SPR-17] The Disconnected Callback**: 
    *   *Origin*: Sprint 17 introduced robust Shadow Failover logic via `self.brain_online`. 
    *   *Conflict*: Sprint 19 migrated the initialization to `self.get_vram_status` to support `[FEAT-265] Waking State Machine`.
    *   *Result*: The `run_shadow` failover was never updated (ERR-05), effectively destroying the safety net exactly when we were trying to make the system more resilient.
*   **[SPR-18] The Lying UI**: 
    *   *Origin*: Deep server-side states (`WAKING`, `HIBERNATING`) were built in `acme_lab.py` `[FEAT-265]`. 
    *   *Conflict*: The frontend (`intercom.html`) retained a hardcoded `"⚡ Systems nominal."` default. 
    *   *Result*: Violates `[BKM-028] High-Fidelity State Machine Debugging`, as the UI happily reported "nominal" while the Hub was dead and the sockets were disconnected.

### Timeline of Architectural Drift
*   **Epoch 1 (Sprint 11-13)**: The Foundation. The "Assassin" pattern is born to enforce stability via brute force (kill processes to free VRAM).
*   **Epoch 2 (Sprint 14-17)**: The Soul. Robust failover (`run_shadow`), Larynx Gates, and Semantic Regex extracting are introduced. The system becomes "smart."
*   **Epoch 3 (Sprint 18-19)**: The Collision. Graceful `vLLM` hibernation and strict state machines are introduced. The old "Assassin" brute force conflicts with the new "Graceful Sleep," and the old `brain_online` boolean conflicts with the new telemetry callbacks.
*   **Epoch 4 (Sprint 20)**: The Healing. Applying `[FEAT-283]` Neural Buffers and Type-Agnostic parsers to bridge the gap between Epoch 2's "smartness" and Epoch 3's "gracefulness."


