# 🚀 SPRINT PLAN 70.0: Live Conversational Ergonomics, Triage Squeeze & Swarm Delegation Shake-Down

**Sprint ID:** `SPR_70_0`  
**Theme:** Conversational Latency Optimization, Triage Context Isolation, and Bounded Swarm Delegation Execution  
**Status:** ACTIVE / IN PROGRESS  
**Parent Framework:** BKM-034 (Swarm Delegation & Tri-Loop Engine), BKM-043 (4-Anchor Standard), BKM-048 (Fingertips Protocol)  
**Hardware Nodes:** Windows RTX 4090 (Atlas L2), Apple M5 Air (Junior L3), Cloud Fallback Ladder (DeepSeek / Qwen)

---

## 🧭 Executive Summary & Architectural Contract

Sprint 70 directly addresses key friction points discovered during live conversational use and live telemetry audits:
1. **Hibernation Elimination:** Make VRAM hibernation strictly optional via a global config toggle, preserving pinned VRAM models indefinitely.
2. **Double Kickstart Remediation:** Solve the multi-layer race condition where cold engine warmup notices prematurely terminate triage turns and drop the initial greeting.
3. **Triage Context Isolation (400 Bad Request Fix):** Strip debate memories from the triage prompt, enforce a strict `max_tokens=128` boundary, and prevent multi-thousand token context overflows.
4. **Deterministic Triage Verification:** Build unit and integration tests forcing Pinky vs. Brain classifications to guarantee correct model routing.
5. **Dead Air Time & Liveliness Metric (5x5 Expansion):** Quantify latency stalls between actors with and without crosstalk, measuring how much heavy lifting inter-node banter provides.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ 🔮 LAYER 1: STRATEGIC GUARDIAN (AGY)                                            │
│ • Authors bounded 4-Anchor specifications for each story.                       │
│ • Monitors delegation heartbeats (1-minute initial check, 5-minute steady).     │
│ • Tri-Loop Escalation: Max 3 subagent remediation attempts before AGY takeover. │
└──────────────────────────────────────┬──────────────────────────────────────────┘
                                       │ (REST Port 4097 / delegate.py)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│ 🗺️ LAYER 2: BROAD ORCHESTRATOR (Atlas on Windows RTX 4090 / Ollama)             │
│ • Category: unspecified-low (routes to M5 Air via oh-my-openagent.json).        │
│ • Ingests bounded story spec and sequences micro-tasks (< 1,200 tokens).        │
└──────────────────────────────────────┬──────────────────────────────────────────┘
                                       │ (task(category="unspecified-low"))
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│ 🛠️ LAYER 3: SURGICAL WORKER (Sisyphus-Junior on Apple M5 Air / MLX)              │
│ • Executes bounded safe_patch edits within target function stubs.               │
│ • Zero repo-wide search/exploration; reports blockers immediately.             │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Granular Story Breakdown

### 🛡️ Story 70.1: Hibernation Master Switch (`[FEAT-517]`)
* **Status:** **COMPLETE / CERTIFIED**
* **Execution Mode:** Tri-Loop Swarm Delegation (Atlas $\rightarrow$ Junior safe_patch $\rightarrow$ AGY AST lint alignment).
* **Target Files:**
  * `HomeLabAI/config/infrastructure.json`
  * `HomeLabAI/src/v5/ignition/manager.py`
  * `HomeLabAI/src/v5/foyer/router.py`
  * `HomeLabAI/src/tests/test_hibernation_master_switch.py`
* **Delivered Artifacts:**
  1. `infrastructure.json`: Added top-level `"hibernation": {"enabled": false, "idle_timeout_seconds": 900}`.
  2. `manager.py`: Master Hibernation Gate in `_watchdog_loop` bypasses `stop_lab(reason="AFK_TIMEOUT")` when `enabled=False`.
  3. `router.py`: Suppresses `self.disconnect_timer` when `hibernation.enabled=False`.
  4. Verified via `pytest src/tests/test_hibernation_master_switch.py` (2/2 passed in 0.21s).
* **Specification:**
  1. Add master configuration schema in `infrastructure.json`:
     ```json
     "hibernation": {
       "enabled": false,
       "idle_timeout_seconds": 900
     }
     ```
  2. In `manager.py` (`_watchdog_loop` around line 500), load `hibernation.enabled`. If `False`, completely bypass `stop_lab(reason="AFK")`.
  3. In `router.py` (`[FEAT-412]` connection-aware idle check), respect `hibernation.enabled`.
  4. Ensure lab status remains `OPERATIONAL` and models remain pinned in VRAM indefinitely.
* **Verification:** Unit test asserting `manager._watchdog_loop` skips stop call when `enabled=False`.

---

### ⚡ Story 70.2: "Double Kickstart" Warmup Race Condition Remediation (`[FEAT-518]`)
* **Status:** **COMPLETE / CERTIFIED**
* **Execution Mode:** Direct AGY AST Remediation & Certification.
* **Target Files:**
  * `HomeLabAI/src/logic/cognitive_hub.py`
  * `HomeLabAI/src/logic/speculative_triage.py`
  * `HomeLabAI/src/tests/test_double_kickstart_remediation.py`
* **Root Cause & Forensic Discovery:**
  * In `cognitive_hub.py:623`, `bridge_signal_clean` checks if raw output is non-JSON prose (`len(clean_str) > 15`). If true, it synthesizes a fallback triage dict with `"addressed_to": "PINKY"`, `"vibe": "CASUAL"`, and `"importance": 0.5`.
  * When local engines wake from hibernation, `loader.py:432` yields `"The local engine is warming its anchors right now. Re-connecting momentarily!"`.
  * `bridge_signal_clean` did NOT exclude warming notifications. It treated the warming string as valid user prose, synthesized a fake valid triage JSON, and `SpeculativeTriageRelay._is_valid_triage` declared it a winner!
  * The hub then advanced to the execution phase on a cold engine that was still loading weights into VRAM. Downstream nodes aborted, the turn emitted `final: True`, and the first "Hi" was permanently dropped.
  * The user's second "Hi" worked because the engine had finished warming in the background.
* **Delivered Artifacts:**
  1. `cognitive_hub.py:621`: Added `is_warming` filter to `bridge_signal_clean`. Any string containing `"warming"`, `"warming its anchors"`, or `"re-connecting momentarily"` immediately returns `None` instead of synthesizing a fake triage object.
  2. `speculative_triage.py:207`: Hardened `_is_valid_triage` to reject any triage dict containing warming residue in `situation` or `hints`.
  3. Verified via `test_double_kickstart_remediation.py` (3/3 passing in 0.13s) and `test_triage_engine.py` (98/98 passing). The first "Hi" can never be silently dropped by transient warming strings again.

---

### 🧠 Story 70.3: Triage Context Squeeze & Token Cap (`[FEAT-519]`)
* **Status:** **COMPLETE / CERTIFIED**
* **Execution Mode:** Tri-Loop Swarm Delegation $\rightarrow$ AGY AST lint alignment & certification.
* **Target Files:**
  * `HomeLabAI/src/logic/cognitive_hub.py`
  * `HomeLabAI/src/nodes/loader.py`
  * `HomeLabAI/src/tests/test_triage_context_squeeze.py`
* **Delivered Artifacts:**
  1. `cognitive_hub.py`: Suppresses `self.round_table_memory` injection whenever `source_name` contains `"triage"`, preventing 7k+ token prompt inflation.
  2. `cognitive_hub.py`: Explicitly passes `max_tokens: 128 if is_triage else 1000` to `call_tool("think", ...)`.
  3. `loader.py`: Updated `think` tool signature with `max_tokens: int = 1000` parameter and forwarded directly into `generate_response(...)`.
  4. Verified via `test_triage_context_squeeze.py` (2/2 passing) and `test_triage_engine.py` (96/96 passing in 0.36s). Completely eliminates vLLM 400 Bad Request token overflow.

---

### 🎯 Story 70.4: Triage Routing Test Harness (`[FEAT-520]`)
* **Status:** **COMPLETE / CERTIFIED**
* **Execution Mode:** Direct AGY AST & Playwright Test Suite Development.
* **Target Files:**
  * `HomeLabAI/src/tests/test_triage_routing_forced.py`
* **Delivered Artifacts:**
  1. Unit Harness: `test_forced_triage_routing_pinky_unit` asserts deterministic dispatch to Pinky resident.
  2. Unit Harness: `test_forced_triage_routing_brain_unit` asserts deterministic dispatch to Brain resident.
  3. Playwright E2E: `test_playwright_forced_routing_dom_elements` launches headless Chromium, accesses `http://localhost:9001/intercom.html`, validates `#text-input`, and verifies `.msg-source.pinky` and `.msg-source.brain` DOM rendering.
  4. Verified via `pytest src/tests/test_triage_routing_forced.py` (3/3 passed in 1.55s).
* **Specification:**
  1. Implement deterministic test cases:
     * *Case A (Pinky Win):* Casual greetings and quips $\rightarrow$ assert `addressed_to == "PINKY"`, `vibe == "CASUAL"`, `importance <= 0.3`.
     * *Case B (Brain Win):* Telemetry / technical queries $\rightarrow$ assert `addressed_to in ["BRAIN", "MICE"]`, `vibe in ["TECHNICAL", "HISTORICAL"]`, `importance >= 0.7`.
  2. Verify JSON schema conformity and error-free execution on local vLLM/Kender mocks.

---

### 🛡️ Story 70.5: 5x5 "Dead Air Time" & Liveliness Benchmark Report (`[FEAT-521]`)
* **Execution Mode:** `[PURE AGY]`
* **Target Files:**
  * `HomeLabAI/src/debug/test_perf_5x5_timed.py`
  * `Portfolio_Dev/field_notes/reports/DEAD_AIR_LIVELINESS_REPORT.md`
* **Specification:**
  1. Update `test_perf_5x5_timed.py` to record precision timestamps for each turn:
     * $T_{\text{user}}$: User done speaking / prompt dispatched.
     * $T_{\text{crosstalk}}$: First crosstalk / preamble / triage event.
     * $T_{\text{token\_1}}$: First primary assistant response token.
     * $T_{\text{end}}$: Turn completely flushed.
  2. Compute:
     * $\text{Raw Dead Air} = T_{\text{token\_1}} - T_{\text{user}}$
     * $\text{Perceived Dead Air} = T_{\text{crosstalk}} - T_{\text{user}}$
     * $\text{Crosstalk Heavy Lifting Ratio} = (\text{Raw Dead Air} - \text{Perceived Dead Air}) / \text{Raw Dead Air}$
  3. Execute live 5x5 run and synthesize `DEAD_AIR_LIVELINESS_REPORT.md`.
* **Verification:** Formatted report with percentile distribution (p50, p90, p99).
