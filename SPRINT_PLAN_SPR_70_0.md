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

### 🛡️ Story 70.2: "Double Kickstart" Warmup Race Condition Remediation (`[FEAT-518]`)
* **Execution Mode:** `[DELEGATION: CLOUD SWARM]` (Sisyphus Cloud / DeepSeek via `delegate.py --agent sisyphus`)
* **Escalation Policy:** Monitored by AGY. Max 3 OpenAgent remediation attempts; if stalled/deadlocked, AGY takes over directly.
* **Target Files:**
  * `HomeLabAI/src/nodes/loader.py`
  * `HomeLabAI/src/logic/cognitive_hub.py`
* **Root Cause:** When `loader.py` yields `"The local engine is warming its anchors..."`, `cognitive_hub.py:bridge_signal_clean` misinterprets the non-JSON prose as a completed fallback triage payload, causing the turn to terminate before weights are warm.
* **Specification:**
  1. In `cognitive_hub.py:bridge_signal_clean`: Explicitly reject `"warming its anchors"` from fallback JSON synthesis. Return a distinct status `None` or `{"status": "WARMING"}`.
  2. In `_dispatch_vllm_triage`: If warming is detected, await true engine availability or allow the warming retry loop in `loader.py` to complete before returning triage metadata.
  3. Prevent premature `final=True` chat broadcasting from closing the turn.
* **Verification:** `HomeLabAI/src/tests/test_warming_anchor_handshake.py`.

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

### 🛡️ Story 70.4: Triage Routing Test Harness (Forced Pinky vs Brain) (`[FEAT-520]`)
* **Execution Mode:** `[DELEGATION: LOCAL SWARM]` (Atlas 4090 $\rightarrow$ Junior M5 Air via `--local-only`)
* **Target Files:**
  * `HomeLabAI/src/tests/test_triage_routing_forced.py`
* **Specification:**
  1. Implement deterministic test cases:
     * *Case A (Pinky Win):* Casual greetings and quips $\rightarrow$ assert `addressed_to == "PINKY"`, `vibe == "CASUAL"`, `importance <= 0.3`.
     * *Case B (Brain Win):* Telemetry / technical queries $\rightarrow$ assert `addressed_to in ["BRAIN", "MICE"]`, `vibe in ["TECHNICAL", "HISTORICAL"]`, `importance >= 0.7`.
  2. Verify JSON schema conformity and error-free execution on local vLLM/Kender mocks.
* **Verification:** `pytest HomeLabAI/src/tests/test_triage_routing_forced.py`.

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
