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
*   **Task 1.1: Node Hardening**: Refactor `BicameralNode` in `loader.py` to support the MCP Sampling/Message protocol.
*   **Why**: To allow the Hub to talk to the model weights directly without a tool wrapper.
*   **How**: Enable the `mcp.create_message` (or equivalent) path in the Node server.

### 📍 PHASE 2: The Hub as Host [HOW & WHY]
*   **Task 2.1: Steering Tool Definition**: Define `ask_brain` and `vram_vibe_check` as tools provided *by the Hub* during the sampling call.
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

### 4. Sentinel Logic Gaps (`lab_node.py`)
*   **Regression**: Removal of `triage_response`. This tool contained the "Deep Search" safety net for identifying tool names inside sloppy 3B JSON values. The current Hub is too reliant on rigid regex for these signals.
