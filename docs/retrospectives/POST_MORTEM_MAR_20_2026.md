# Post-Mortem: SPR-16.0 Architectural Shift & Feature Audit
**Date:** Friday, March 20, 2026
**Subject:** Forensic Analysis of Native MCP Sampling Impact & Regressions

## 🕵️ EXECUTIVE SUMMARY
The transition to **SPR-16.0 (The Standard Relay)** successfully aligned the Lab with native MCP sampling protocols, eliminating the brittle `facilitate` wrappers. However, this "Standardization" introduced several critical regressions, primarily due to path inconsistencies and protocol-level buffering, resulting in the loss of specialized persona depth and real-time responsiveness.

---

## 🏛️ RANK 1: OBVIOUS REGRESSIONS & CRITICAL FAILURES
*These items represent clear bugs, broken paths, or missing implementations that require immediate recovery.*

### 1. The "Broken Bridge" (Path Inconsistency in `loader.py`)
*   **The Issue**: `src/nodes/loader.py` incorrectly calculates `LAB_DIR` using only two `os.path.dirname` calls.
*   **The Impact**: Nodes (Pinky, Shadow, Lab) fail to load `infrastructure.json`. They default to `localhost` and **fail to load their LoRA adapters** (e.g., `lab_history_v1`, `cli_voice_v1`). 
*   **The Scar**: This is the root cause of the reported "lost features" and "regression." The Brain is being run locally on a generic 3B model instead of on the Sovereign 4090 with its specialized 18-year archive DNA.

### 2. The Streaming Paradox (Buffering in `native_sample`)
*   **The Issue**: The new `native_sample` tool in `loader.py` exhausts the async generator and returns a full string block.
*   **The Impact**: The "Live Feedback" and "Waterfall Flow" (SPR-15.0) are dead at the Hub level. The UI only receives "Paragraph Pops," significantly increasing perceived latency.
*   **Recovery**: Refactor `native_sample` to be a streaming-aware tool or implement a "Native Sampling" protocol that supports `async for` tokens.

### 3. The "Silent" Morning Briefing (Missing Hub Logic)
*   **The Issue**: The `trigger_morning_briefing` tool is listed in `CognitiveHub.known_hub_tools` but is **not implemented** in the `execute_dispatch` logic.
*   **The Impact**: Nodes can request a debrief, but the Hub silently ignores the request. The "Dreaming Debrief" feature is currently a ghost capability.

---

## 🏛️ RANK 2: AMBIGUOUS & DUBIOUS CHANGES
*These items are functional but represent a drift from original requirements or introduce new risks.*

### 1. The "Veto" Trap (`shallow_think` as Kill-Switch)
*   **The Change**: Hub now treats any `shallow_think` call from Pinky/Shadow as a "Veto" signal (Fuel = 0.0).
*   **The Risk**: If the 3B model hallucinations this tool name (e.g., in a technical explanation), it kills the strategic relay. This is a "brittle-by-design" steerage mechanism that conflicts with persona-driven interjections.

### 2. The "Echo Chamber" Blindness (Collective Address)
*   **The Change**: The Sentinel's triage rules in `lab_node.py` were refactored to focus on individual addresses ('Brain', 'Pinky').
*   **The Loss**: There is no explicit logic for addressing "Everyone" or the "Mice." Collective greetings currently fall back to standard scalar fuel logic, often silencing the higher reasoning nodes during group interactions.

### 3. Audit Bias (Marking Your Own Homework)
*   **The Change**: `dream_cycle.py` uses the same remote model to both synthesize and audit its own "Diamond Wisdom."
*   **The Risk**: This violates the Judicial Feedback Loop [FEAT-191] and risks propagating high-fidelity hallucinations into the permanent archive.

---

## 🏛️ RANK 3: LOST CAUSES & DEFEATURED
*These items were intentionally removed or are technically unfeasible in the current stack.*

### 1. The Live Hearing Pipe ([FEAT-233.2])
*   **Status**: **DEFEATURED**.
*   **Rationale**: Confirmed unfeasible over standard MCP/REST transport. Inter-node token synchronization is tabled until custom transport layers are developed.

### 2. The "Facilitate" Wrapper
*   **Status**: **PURGED**.
*   **Rationale**: Replaced by `native_sample` for better protocol alignment.

---

## 🏺 TL;DR SUMMARY
The Lab is currently running "Blind" due to a one-line path error in `loader.py`, causing the Sovereign Brain to be bypassed and LoRA adapters to be ignored. While the new **MCP Sampling Bridge** is a step forward in protocol hygiene, its implementation has effectively **killed real-time streaming** and orphaned several high-value features like the **Morning Briefing**.

**Immediate Actions Recommended:**
1. Fix the `LAB_DIR` path in `src/nodes/loader.py` (Add 3rd `dirname`).
2. Implement the missing `trigger_morning_briefing` logic in `CognitiveHub.py`.
3. Restore true streaming to the Hub by refactoring the `native_sample` bridge.
