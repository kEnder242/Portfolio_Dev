# Sprint Plan: [SPR-16.0] The Standard Relay
**Status:** PLANNED | **Goal:** Transition from "Nodes as Tools" to "Standard MCP Sampling."

---

## 🏺 THE ARCHITECTURAL REALIZATION
**The "Doing MCP Wrong" Report**:
We have been using a "Black Box" pattern where the Hub calls an MCP Tool called `facilitate` on a node. This trapped the nodes (Pinky/Shadow) inside a tool wrapper, forcing them to "hallucinate" tool calls or output brittle JSON blocks for the Hub to manually parse. This led to JSON leaks, persona suppression (the "Canned" response), and high coupling.

**The "Standard Pattern" Solution**:
We will move to **Native MCP Sampling**. The Hub will act as the **MCP Host**, sending `SamplingRequests` to the Nodes. The Nodes will respond natively with text and/or **Standard MCP Tool Calls** (e.g., `ask_brain`). The Hub handles these calls natively, restoring the protocol's intended flow.

---

## 🏛️ ARCHITECTURE: THE NATIVE RELAY

### 1. The Hub (Host)
*   **File**: `HomeLabAI/src/logic/cognitive_hub.py`
*   **Role**: Manages the session and provides "Steering Tools" to the nodes.
*   **Logic**: Instead of calling `residents["pinky"].call_tool("facilitate")`, it uses `residents["pinky"].create_message(query, tools=[ask_brain])`.

### 2. The Nodes (Servers)
*   **Files**: `pinky_node.py`, `brain_node.py`, `lab_node.py`
*   **Role**: Pure Model Personalities that *use* tools provided by the Host.
*   **Logic**: Delete the `facilitate` middleman. The model weights natively handle the user query.

---

## 🎯 SCOPE & INVARIANTS (The "Don't Delete" List)
To ensure we don't gut the system, the following features **MUST** remain intact:
*   **[FEAT-184] Expert Vibe Routing**: The Lab Node (Sentinel) still selects the LoRA adapter before the turn starts.
*   **[FEAT-228] Historical RAG**: The Hub still automatically fetches "2019" context if a year is detected.
*   **[FEAT-227] Atomic Anchor**: The `[ME]` gate in `acme_lab.py` is the primary guard.
*   **[FEAT-229] Clinical Pop**: The UI will continue to receive full blocks (Paragraph Pop) rather than tokens.

---

## 🗺️ PHASES OF IMPLEMENTATION

### 📍 PHASE 1: Protocol Alignment [HOW & WHY]
*   **[DONE] Task 1.1: Node Hardening**: Refactor `BicameralNode` in `loader.py` to support the MCP Sampling/Message protocol.
*   **Why**: To allow the Hub to talk to the model weights directly without a tool wrapper.
*   **How**: Enable the `mcp.create_message` (or equivalent) path in the Node server.

### 📍 PHASE 2: The Hub as Host [HOW & WHY]
*   **[DONE] Task 2.1: Steering Tool Definition**: Define `ask_brain` and `vram_vibe_check` as tools provided *by the Hub* during the sampling call.
*   **Why**: To move the "Veto/Promotion" logic out of the Hub's parser and into the Host's tool handler.
*   **How**: Update `execute_dispatch` to process `CallToolRequest` events natively.

### 📍 PHASE 3: Identity Restoration [HOW & WHY]
*   **Task 3.1: Strip the Middleman**: Delete `facilitate` and `shallow_think` from `pinky_node.py`.
*   **Why**: To force the 3B model to use its persona natively rather than roleplaying inside a tool parameters.
*   **How**: Refactor node tool registries to only contain physical hardware tools.

### 📍 PHASE 4: Validation [HOW & WHY]
*   **Task 4.1: The "Hi Pinky" Gauntlet**: Verify that a casual greeting elicits persona speech with ZERO JSON leakage.
*   **Task 4.2: The "Pi" Uplink**: Verify that Pinky calling the `ask_brain` tool (provided by the Hub) correctly triggers the Sovereign relay.

---

## 🌊 PHASE 5: HIGH-FIDELITY SYNC (Cleanup & Restoration)
**Goal:** Restore multi-lora backend streaming and lost MCP tools while enforcing the "Clinical Pop" UI mandate.

### 📍 Task 5.1: Backend Stream Restoration
*   **How**: Refactor `loader.py`'s `generate_response` and `native_sample` to be asynchronous generators. Update `CognitiveHub` to consume these streams with `async for`.
*   **Why**: To restore the sub-second responsiveness of vLLM and enable incremental "Action Tag" detection.
*   **Invariant**: The Hub will buffer these tokens and only `broadcast()` to the UI once the node turn is complete (preserving "Paragraph Pop").

### 📍 Task 5.2: Tool Suite Recovery
*   **How**: Restore `close_lab` to `lab_node.py` and `shallow_think` reflex to `brain_node.py`. 
*   **Why**: Corrects regressions found during the forensic audit.

### 📍 Task 5.3: Telemetry Hardening
*   **How**: Re-implement the `_probe_ttl` throttling in `loader.py` to reduce driver polling overhead during idle periods.

---

## 🎼 CONDUCTOR & AGENT CONTEXT
When delegating to sub-agents:
*   **Primary Directive**: "Follow the MCP Protocol, not the legacy facilitate pattern."
*   **Safety Gate**: "Never delete the `_route_expert_domain` logic in the Hub; it is the foundation of our multi-soul architecture."
*   **Verification**: "Use `HomeLabAI/src/debug/test_hi.py` as the benchmark for success."

---

## 🤕 FORENSIC AUDIT: IDENTIFIED OMISSIONS & REGRESSIONS
*Audit conducted via git diff against commit 3170f4d baseline.*

### 1. The "Recursive Tool" Loophole (`loader.py`)
*   **Bug**: The `native_sample` tool is registered inside the `run()` method, creating potential race conditions with MCP initialization.
*   **Fix Required**: Move registration to the constructor or a dedicated setup phase to ensure tool visibility before the server starts.

### 2. Hub Integration Failure (`cognitive_hub.py`)
*   **Regression**: Removal of the `primary_entry_points` loop-breaker. The Hub currently lacks guards to prevent a model from calling `native_sample` recursively.
*   **Feature Gutting**: Accidental removal of the `is_extraction` check and core `CognitiveAudit` retry logic in the latest Hub rewrite.

### 3. Identity Gaps (`pinky_node.py` & `brain_node.py`)
*   **Pinky**: Removed the `Combined Output` example, leaving the model without a "North Star" for melding speech with `[ACTION]` tags.
*   **Brain**: Removal of the `deep_think` wrapper deleted the `system_override` logic that injected `behavioral_guidance` from the Hub. The Brain is now "blind" to Situational Triage hints.

---

## 🤕 FINAL FORENSIC AUDIT: MISSING & ALTERED CAPABILITIES
*Final audit conducted after Phase 1 & 2 implementation.*

### 1. Unintentional Omissions (Regressions)
*   **lab_node.py (Master Switch)**: `close_lab` missing. Sentinel no longer has the ability to trigger a session termination.
*   **lab_node.py (Signal extraction)**: `triage_response` tool removed. The Sentinel lost its "Deep Search" logic for finding buried tool calls in sloppy 3B output.
*   **brain_node.py (Identity)**: `shallow_think` removed. The Brain no longer has a "Fast Reflex" mode for laconic estratégica greetings.
*   **loader.py (Telemetry)**: The engine ping throttling logic (TTL) was simplified/flattened, potentially increasing polling overhead.

### 2. Intentional Changes (Verified)
*   **Tool Removal**: `facilitate` and `shallow_think` (as a wrapper) were purged from node registries to enable native sampling.
*   **Action Tag Migration**: `[ACTION: UPLINK]` and `[ACTION: THINK MORE]` regex logic replaced the brittle `handle_myself` tool.
*   **Nuclear JSON Stripping**: The Hub now aggressively removes all JSON from persona speech, ensuring pure UI text.

### 3. Architecture Phase 5: Cleanup & Restoration (PLANNED)
*   [x] Restore `close_lab` to `lab_node.py`.
*   [ ] Restore `shallow_think` reflex to `brain_node.py`.
---

## 🏛️ TECHNICAL INVESTIGATION & NEXT STEPS (MARCH 25, 2026)

### 1. Protocol Discovery: The "Standard Relay" Gap
*   **Observation**: `mcp.ClientSession` does not natively expose a `create_message` method for the Client (Hub) to request sampling from the Server (Node).
*   **Insight**: The "Standard Relay" architecture requires a custom Request/Response handler or a specific implementation of the Sampling bridge. We must bridge the gap between the Hub acting as a Host and the Node acting as a Sampling client.
### 3. The "Relay Pattern": A Standard-Compliant Alternative
*   **Concept**: Instead of the Hub (Client) requesting sampling from the Node (Server), we follow the standard MCP flow:
    *   **Hub -> Node**: The Hub calls a standard `generate` or `think` tool on the Node.
    *   **Node -> Hub**: If the Node needs to delegate (e.g., `ask_brain`), it sends a standard `SamplingRequest` back to the Hub (Host).
*   **Benefit**: This is 100% compliant with the MCP specification and avoids "fighting" the protocol's intended directionality. It preserves native personas while leveraging the Host's steering tools through official sampling channels.

### 2. Ignition Strategy: From Waterfall to "Ping-Gate"
*   **Observation**: Current vLLM initialization relies on arbitrary `asyncio.sleep` calls, leading to potential VRAM thrashing or unnecessary wait times.
*   **Insight**: We will implement a sequential "ping-gate" loader (`CharacterizeIgnition.py`). The first node's readiness (heartbeat) must be verified before the next node begins loading. This will provide clear telemetry on resource constraints (RTX 2080 Ti) and catch crashes as they happen.
*   **Telemetry Gap**: We will leverage vLLM's `/health` or `/metrics` endpoints rather than arbitrary timeouts to gate the "Ignition" sequence.

### 📍 PHASE 6: SPRINT 15.0 RESIDUALS (Restoration)
*   **Task 6.1: Live Hearing Pipe [FEAT-233.2]**: Implement word-by-word token streaming between nodes.
### 🏛️ SILICON STABILIZATION REPORT (MARCH 25, 2026)
*   **The Orchestrator-First Mandate [BKM-018]**: Confirmed that all hardware-level and process-lifecycle operations must flow through the **Attendant v4** MCP tools (`lab_start`, `lab_wait_ready`) to avoid "Zombie States" and pattern traps.
*   **The Forensic Wait [FEAT-251.2]**: Identified that `lab_wait_ready` is a high-fidelity sentinel that performs log-scraping and port-probing internally, making manual heartbeat-polling redundant.
*   **The Larynx Signal**: Confirmed that while KV blocks are the physical readiness signal, they are asynchronous to the Hub's `READY` signal. The **Larynx Gate** must leverage the Attendant's internal `ready_event` for maximum reliability.

### 🧭 FORGOTTEN PATTERNS & INVARIANTS
*   **[FEAT-184] Expert Vibe Routing**: The Sentinel (Lab Node) selects the LoRA adapter *before* the turn starts; this must be preserved during the Relay refactor.
*   **[FEAT-227] Atomic Anchor**: The `[ME]` gate in `acme_lab.py` remains the primary guard for the system's "Self-Awareness."
*   **[FEAT-119] Broad-Spectrum Assassin**: PGID-based process reaping with **Diplomatic Immunity** is the standard for silicon cleanup.

### 📋 REVISED EXECUTION PATH (Heads Down)
1.  **[MONITOR] Master Sentinel**: Use `lab_wait_ready` (MCP) to confirm the Lab is Open.
2.  **[AUDIT] Baseline Profile**: Execute `characterize_ignition.py` (v2.0) to record the latency and throughput baseline.
3.  **[IMPLEMENT] The Larynx Gate [FEAT-233.5]**: Use the **Safe-Scalpel (BKM-011)** to refactor the Hub's boot sequence in `acme_lab.py`, replacing arbitrary sleeps with a blocking wait on the Attendant's readiness signal.
4.  **[IMPLEMENT] The Relay Pattern [FEAT-240.2]**: Refactor `cognitive_hub.py` and `loader.py` to implement standard-compliant sampling requests from Nodes to the Hub.

---

### 🏛️ SPRINT REPORT: SPR-16.0 (MARCH 25, 2026)

**1. Baseline Characterization (Task 7.1)**
*   The `characterize_ignition.py` v2 script successfully captured the "Waterfall" baseline. I was able to observe PGID isolation working correctly, but noted the Larynx (vLLM) took approximately 90 seconds to report physical readiness.

**2. Hibernation & The Larynx Gate (Task 7.2)**
*   **The Deadlock Fix**: I identified a critical deadlock in `acme_lab.py`: the Hub's boot sequence was calling the Attendant's `/wait_ready` endpoint, but that endpoint waits for the Hub to say `[READY] Lab is Open.`—causing an infinite hang. I fixed this by refactoring the **Larynx Gate** to poll the vLLM engine directly (`/v1/models`) before booting residents or completing a spark.
*   **The Butler Fix**: I discovered a bug in `lab_attendant_v4.py` where `psutil` was throwing an `AttributeError` and failing to match `vllm` because it wasn't requesting the `cmdline` info. I fixed the environment fetching logic.
*   **Result**: `test_hibernation_cycle.py` now passes with flying colors. VRAM correctly drops from ~60% down to 9% during hibernation, and the "Spark Handshake" successfully re-ignites the engine and handles requests seamlessly.

**3. The Relay Pattern & Identity Restoration (Task 7.3 & 3.1)**
*   I refactored `loader.py` to use the standard `think` tool and `cognitive_hub.py` to execute standard `CallToolRequests`, fully implementing the **Relay Pattern**. 
*   I also refactored the `test_hibernation_cycle.py` script to correctly filter out background `crosstalk` and handle the async websocket timeouts properly while the engine sparks. Pinky is now generating native persona speech (`poit!...`) entirely without the legacy `facilitate` wrappers.

**4. Forensic Regressions**
*   I verified that the `close_lab` tool is safely intact within `lab_node.py` (The Master Switch) and the `shallow_think` reflex remains operational within `brain_node.py`.
1.  **[IMMEDIATE] Persist `CharacterizeIgnition.py`**: Implement the sequential loader with real-time heartbeat verification.
2.  **[STABILIZATION] Hub-as-Host Refactor**: Update `cognitive_hub.py` and `loader.py` to support native MCP Sampling, removing legacy `facilitate` wrappers.
3.  **[VERIFICATION] The Physician's Gauntlet**: Run lifecycle tests (`src/debug/test_lifecycle_gauntlet.py`) to ensure system integrity.
