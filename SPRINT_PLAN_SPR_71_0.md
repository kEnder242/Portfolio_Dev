# 🚀 SPRINT PLAN 71.0: Conversational Stability, Semantic Triage Decoupling & RAG Zero-Noise Hardening

**Sprint ID:** `SPR_71_0`  
**Theme:** Real-Time Dialogue Liveliness, Semantic Vibe-First Triage (BKM-015), Zero-Context RAG Precision, and Telemetry Convergence  
**Status:** ACTIVE / IN PROGRESS  
**Parent Framework:** BKM-015 (Semantic Anchor Protocol), BKM-034 (Swarm Delegation), BKM-043 (4-Anchor Standard), BKM-048 (Fingertips Protocol)  
**Target Hardware Nodes:** z87-Linux (RTX 2080 Ti Local vLLM), KENDER (RTX 4090 Deep Thought / Atlas), M5 Air (Speculative Candidate)

---

## 🧭 Executive Summary & Core Engineering Mandates

Sprint 71 addresses the root causes of conversational latency and incoherence observed during live co-pilot dialogue ("hello pinky"):
1. **Dynamic Deep Thought Head-Start Window (Sub-1s Liveliness):** Replace static 10s wait loops with an adaptive socket-probed head-start window ($2 \times t_{\text{warm}} \approx 180\text{ms}$). If remote Deep Thought is unresponsive, failover immediately to local vLLM.
2. **Semantic Vibe-First Triage (BKM-015 Compliance):** Deprecate rigid static greeting lists (`raw_lower in [...]`) and hardcoded keyword filters. Ground intent routing in vector similarity via ChromaDB `behavioral_dna` and prompt-guided semantic classification.
3. **Empty/Sparse Query RAG Suppression (Zero-Hallucination Floor):** Prevent RAG from returning legacy historical records on casual greetings or ungrounded turns. When intent is CASUAL or query terms have 0 semantic domain overlap, return an empty HyDE vector and bypass ChromaDB.
4. **Console Broadcast De-duplication:** Eliminate double-printing in UI/Web Intercom by unifying crosstalk and chat telemetry payloads.
5. **Two-Mice Mutual Exclusion Gate:** Prevent Brain from executing redundant dual responses (Strategic Brief + Secondary Reflection) when addressed as lead node.
6. **Critic Deterministic Scoring & Sampling Hygiene:** Lower critic sampling temperature ($T=0.0$) and enforce atomic regex JSON extraction to eliminate whitespace stutter and malformed token outputs (`"{"` and `"P 1"`).
7. **Web Intercom & Benchmarks Session Synchronization:** Ensure all live conversational turns stream to `round_table_deltas.json` and properly bind the active session ID (`SID`).

---

## 📋 Sprint 71 Stories & 4-Anchor Specifications

### ⏱️ Story 7101: Adaptive Speculative Triage Head-Start & Cold-Socket Sentinel (`[FEAT-531]`)
* **Objective:** Ensure triage completes in $< 150\text{ms}$ by probing remote socket health before dispatching, and clamping the speculative head-start window from 10.0s to $2 \times t_{\text{warm}}$ (~180ms).
* **Target Files:**
  * `HomeLabAI/src/logic/speculative_triage.py`
  * `HomeLabAI/src/tests/test_speculative_triage_headstart.py`
* **Acceptance Criteria:**
  1. If KENDER or M5 Air is unresponsive, local vLLM takes over in $< 150\text{ms}$.
  2. Speculative race terminates instantly upon first valid winner.

---

### 🎭 Story 7102: Semantic Vibe-First Triage Grounding (BKM-015 Restoration) (`[FEAT-532]`)
* **Objective:** Eliminate static list-matching (`raw_lower in [...]`) in `CognitiveHub` and restore dynamic vector/prompt-guided semantic classification per BKM-015. "Hello Pinky" must evaluate to `addressed_to: PINKY, vibe: CASUAL` purely from prompt semantics.
* **Target Files:**
  * `HomeLabAI/src/logic/cognitive_hub.py`
  * `HomeLabAI/src/logic/triage_engine.py`
  * `HomeLabAI/src/tests/test_semantic_vibe_triage.py`
* **Acceptance Criteria:**
  1. Zero hardcoded greeting lists in `cognitive_hub.py`.
  2. Salutations directed to Pinky route cleanly with `addressed_to: PINKY`.

---

### 🛡️ Story 7103: Empty & Low-Information Query RAG Suppression Floor (`[FEAT-533]`)
* **Objective:** When queries are casual greetings or sparse ("hello pinky", "what's up"), enforce an explicit zero-context floor. ChromaDB RAG must be bypassed completely to prevent dumping stale silicon validation history from days ago.
* **Target Files:**
  * `HomeLabAI/src/logic/cognitive_hub.py`
  * `HomeLabAI/src/nodes/archive_node.py`
  * `HomeLabAI/src/tests/test_rag_suppression_floor.py`
* **Acceptance Criteria:**
  1. Casual greetings return `hyde_vector_text = ""` and bypass ChromaDB retrieval.
  2. No unsolicited 18-year archive briefs on conversational turns.

---

### 📢 Story 7104: Console Telemetry De-Duplication & Two-Mice Single-Turn Gate (`[FEAT-534]`)
* **Objective:** Unify triage broadcasts into a single clean payload and fix the execution loop in `CognitiveHub` so Brain never executes two separate reply legs for a single user turn.
* **Target Files:**
  * `HomeLabAI/src/logic/cognitive_hub.py`
  * `HomeLabAI/src/tests/test_two_mice_single_execution.py`
* **Acceptance Criteria:**
  1. Triage emits exactly ONE broadcast event per turn.
  2. Lead node executes exactly once per turn.

---

### 🎯 Story 7105: Critic Sampling Hygiene & Deterministic JSON Parser (`[FEAT-535]`)
* **Objective:** Root-cause critic token malformation (`"{"` / whitespace padding). Enforce $T=0.0$ greedy decoding and robust regex extraction for critic telemetry.
* **Target Files:**
  * `HomeLabAI/src/nodes/pinky_critic_persona.py`
  * `HomeLabAI/src/logic/cognitive_hub.py`
  * `HomeLabAI/src/tests/test_critic_sampling_hygiene.py`
* **Acceptance Criteria:**
  1. Critic output parses valid JSON score/reasoning 100% of the time.
  2. Zero runaway whitespace token padding.

---

### 📊 Story 7106: Live Turn Telemetry Socket & Session Synchronization (`[FEAT-536]`)
* **Objective:** Ensure live Web Intercom turns consistently record stage timings to `round_table_deltas.json` and resolve active socket session IDs (`SID`).
* **Target Files:**
  * `HomeLabAI/src/logic/cognitive_hub.py`
  * `Portfolio_Dev/field_notes/data/benchmarks.js`
  * `HomeLabAI/src/tests/test_live_telemetry_socket_sync.py`
* **Acceptance Criteria:**
  1. Every live dialogue turn increments `round_table_deltas.json`.
  2. Web Intercom and `benchmarks.html` reflect current session stats in real time.
