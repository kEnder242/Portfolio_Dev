# 📜 SPRINT PLAN: SPR-51.0 (Conversational Polish, Deep Thought Refinement, & Mobile Crosstalk UI)

> **Sprint Goal**: Restore natural conversational flow to Acme Lab by eliminating persona leakage ("Narf" in Deep Thought), bypassing heavy HyDE/RAG pre-reflections on casual greetings ("hello"), un-blocking Deep Thought preamble latency, and routing `[SYSTEM]` messages into a compact scrolling Crosstalk Bar component for mobile.

---

## 🎯 Executive Summary & Architectural Focus

| Story | Feature ID | Target / Module | Description | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Story 1** | `FEAT-451` | `src/logic/cognitive_hub.py` | Persona Boundary Hardening: Remove Pinky tics ("Narf!", "Poit!") from Deep Thought / Brain preambles | **PLANNED** |
| **Story 2** | `FEAT-452` | `src/logic/cognitive_hub.py` | Casual Greeting Fast-Path: Bypass HyDE vector generation & heavy RAG on casual turns ("hello", "hey") | **PLANNED** |
| **Story 3** | `LAB-098` | `src/v5/foyer/router.py` | Deep Thought Latency Audit: Guarantee non-blocking async pre-reflection without waiting for heavy lab init | **PLANNED** |
| **Story 4** | `FEAT-453` | `field_notes/intercom_v2.js` / HTML | Mobile Crosstalk Bar: Route `[SYSTEM]` log floods into a dedicated scrolling Crosstalk tab component | **PLANNED** |
| **Story 5** | `FEAT-454` | Integration Gauntlet | End-to-End Sprint 51 Verification Suite & `/grill-me` Interactive Alignment | **PLANNED** |

---

## 📜 Detailed Story Specifications

### 🎭 Story 1: Persona Boundary Hardening (`FEAT-451`)
* **Problem**: Deep Thought pre-reflection output occasionally includes Pinky character tics like `"Narf!"`, causing persona bleed and unnatural dialogue.
* **Task Specification**:
  1. Audit `CognitiveHub` prompt templates and output parsers in `src/logic/cognitive_hub.py`.
  2. Enforce strict persona boundary constraints: Deep Thought = strategic/analytical; Pinky = cheerful/grounded; Brain = cerebral. Explicitly strip `"Narf!"`, `"Poit!"`, `"Zort!"` from Deep Thought outputs.
* **Target File**: [`HomeLabAI/src/logic/cognitive_hub.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py)
* **Verification Command**: `pytest HomeLabAI/src/tests/test_v5_stabilization.py`

---

### 💬 Story 2: Casual Greeting Fast-Path (`FEAT-452`)
* **Problem**: When a user says "hello" or "good morning", Deep Thought attempts to generate a complex 3-part HyDE vector and query ChromaDB RAG, producing overly formal or forced responses.
* **Task Specification**:
  1. Add a low-latency intent classifier in `src/logic/cognitive_hub.py` to immediately detect casual greetings/quips.
  2. For casual turns, bypass HyDE vector generation, set `hyde_vector_text = ""`, skip heavy RAG lookups, and route directly to Pinky/Brain fast-response templates.
* **Target File**: [`HomeLabAI/src/logic/cognitive_hub.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py)
* **Verification Command**: `pytest HomeLabAI/src/tests/test_qpr_hyde.py`

---

### ⚡ Story 3: Deep Thought Latency & Init Un-blocking Audit (`LAB-098`)
* **Problem**: Deep Thought pre-reflection was designed to stream space-filling thoughts instantly while vLLM wakes up. It appears to be waiting on heavy resident initialization or synchronous locks.
* **Task Specification**:
  1. Audit `waterfall_drainer` and `process_query` lock acquisition in `src/v5/foyer/router.py` & `cognitive_hub.py`.
  2. Ensure Deep Thought preamble fires asynchronously immediately upon WebSocket message receipt without waiting for resident wake locks.
* **Target Files**: [`HomeLabAI/src/v5/foyer/router.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/v5/foyer/router.py), [`HomeLabAI/src/logic/cognitive_hub.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py)
* **Verification Command**: `pytest HomeLabAI/src/tests/test_integration_foyer.py`

---

### 📱 Story 4: Mobile Crosstalk Bar System Message Routing (`FEAT-453`)
* **Problem**: `[SYSTEM]` messages (wake signals, heartbeats, status notices, judge logs) flood the main chat stream, crowding out actual dialogue on mobile screens.
* **Task Specification**:
  1. Update `field_notes/intercom_v2.js` and CSS layout to enhance the Crosstalk Bar with a scrollable event channel.
  2. Route all `[SYSTEM]` / `[REMOTE]` / `[HEARTBEAT]` messages directly to the Crosstalk Bar, keeping the main chat stream clean for out-loud dialogue.
* **Target Files**: `Portfolio_Dev/field_notes/intercom_v2.js`, `Portfolio_Dev/field_notes/intercom.html`
* **Verification Command**: `python3 field_notes/scan_librarian.py`

---

### 🧪 Story 5: Integration Gauntlet & Certification (`FEAT-454`)
* **Task Specification**:
  1. Execute unit and integration tests across Foyer, HyDE, and Memory Architecture.
  2. Conduct interactive `/grill-me` session to align on visual UI boundaries and persona nuances.
* **Verification Command**: `pytest HomeLabAI/src/tests/test_integration_foyer.py HomeLabAI/src/tests/test_memory_architecture.py`
