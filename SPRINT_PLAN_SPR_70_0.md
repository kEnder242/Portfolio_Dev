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

### ⏱️ Story 70.5: 5x5 "Dead Air Time" & Liveliness Benchmark Report (`[FEAT-521]`)
* **Status:** **COMPLETE / CERTIFIED**
* **Execution Mode:** Pure AGY Live Gauntlet Execution & Telemetry Reporting.
* **Target Files:**
  * `HomeLabAI/src/debug/test_perf_5x5_timed.py`
  * `Portfolio_Dev/field_notes/DEAD_AIR_LIVELINESS_REPORT.md`
* **Delivered Artifacts:**
  1. `test_perf_5x5_timed.py`: Added DOM-level live event tracking for each intermediate token/tic. Computes `dead_air_with_crosstalk`, `dead_air_without_crosstalk`, and `crosstalk_heavy_lifting_pct`.
  2. Executed 3-cycle live gauntlet across cold ignition and hot steady state.
  3. Authored [`DEAD_AIR_LIVELINESS_REPORT.md`](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/DEAD_AIR_LIVELINESS_REPORT.md) capturing empirical timing tables and SLA thresholds:
     * Cold-start First Crosstalk Acknowledgment: `+10.16s` (saves 10.16s of dead air, a 16.4% perceived latency lift).
     * Steady-State TTFT: `0.62s` (620 ms).
     * Steady-State Max Dead Air: `0.54s`.

---

## 🏆 Sprint 70.0 Completion Summary
* **Story 70.1 (`[FEAT-517]`):** Certified (Hibernation Master Switch).
* **Story 70.2 (`[FEAT-518]`):** Certified ("Double Kickstart" Warmup Race Condition Remediation).
* **Story 70.3 (`[FEAT-519]`):** Certified (Triage Context Squeeze & Token Cap).
* **Story 70.4 (`[FEAT-520]`):** Certified (Triage Routing Forced Playwright Test Harness).
* **Story 70.5 (`[FEAT-521]`):** Certified (5x5 Dead Air Time & Liveliness Benchmark Report).
* **All Sprint Verification Gates:** 100% Passing. Zero remote git pushes executed.

---

## 🔬 Deep Retrospective: Forensics, Root Causes & Architectural Lessons

### 1. The "Double Kickstart" Race Condition (`[FEAT-518]`)
* **Forensic Diagnosis:** When local engines wake from hibernation, `loader.py:432` yields: `"The local engine is warming its anchors right now. Re-connecting momentarily!"`.
* **The Glitch:** In `cognitive_hub.py:623`, `bridge_signal_clean` evaluated raw output: `if len(clean_str) > 15 and not ("Error:" in clean_str or "vLLM connection" in clean_str...)`. Because warming strings were not in the exclusion blacklist, the hub interpreted the notification as valid user prose and synthesized a fake triage payload:
  `{"inferred_intent": "The local engine is warming...", "addressed_to": "PINKY", "vibe": "CASUAL", "importance": 0.5}`.
* **The Cascade:** `SpeculativeTriageRelay._is_valid_triage` declared this fake triage JSON a winner because it contained `vibe`, `addressed_to`, and `importance`. The hub immediately advanced into the round-table phase on a cold engine that was still loading weights into VRAM. Downstream nodes aborted, the turn emitted `final: True`, and the user's first "Hi" was permanently dropped.
* **Why the Second "Hi" Worked:** By the time the user realized nothing happened and said "Hi" again, weights had finished loading in the background. Triage executed on a warm engine and succeeded.
* **Permanent Remediation:** 
  1. Filtered all warming phrases (`"warming"`, `"warming its anchors"`) in `bridge_signal_clean` to return `None`.
  2. Hardened `_is_valid_triage` in `speculative_triage.py` to reject any triage dict containing warming residue in `situation` or `hints`.

### 2. Triage Context Squeeze & Token Cap (`[FEAT-519]`)
* **Forensic Diagnosis:** Over multi-turn sessions, `self.round_table_memory` accumulated previous debate turns. `cognitive_hub.py:_process_node_stream` unconditionally prepended `round_table_memory` to the query, inflating triage prompts up to 7,193 tokens. Combined with default `max_tokens=1000`, this exceeded vLLM's 8,192 limit and threw `400 Bad Request`.
* **Permanent Remediation:** Suppressed `round_table_memory` during triage turns and passed `max_tokens=128` down to `generate_response`, keeping triage prompts strictly $< 300$ tokens total.

### 3. Swarm Single Task Law & Concurrency Deadlocks (`[LAB-515]`)
* **Forensic Diagnosis:** Apple M5 Air oMLX inference (`192.168.1.46:8000`) is strictly single-stream. When Atlas emitted multiple `task()` tool calls in a single turn, multiple OpenCode child sessions connected simultaneously. M5 Air exceeded its Metal wired memory limit (`iogpu.wired_limit_mb` 24.96GB) and rejected requests with `"Model is busy"`.
* **Harness Flaw:** `delegate.py` had contradictory prompt guidance: an invariant forbidding parallel calls juxtaposed against `"Prefer the 3-Task Micro-Pattern: Task A -> Task B -> Task C"`.
* **Permanent Remediation:** Enforced the **Single Task Law** in `delegate.py` and disabled `compaction.auto` in `opencode.json` for local subagent child sessions.

### 4. Systemic Tri-Loop Delegation Failure Post-Mortem
* **Why Delegation Fell Back to AGY:**
  * Iteration 1: Atlas emitted parallel tasks $\rightarrow$ M5 Air concurrency lock.
  * Iteration 2: Prompt invariant fixed task count, but OpenCode auto-compaction hijacked the session on local subagents.
  * Iteration 3: Auto-compaction disabled, `safe_patch` applied code, but local Qwen 27B entered an indentation error loop (`except Exception as e:\n pass` with misaligned whitespace).
* **The Operational Mistake:** Instead of pausing to deeply investigate the subagent execution logs and fix the underlying harness between iterations, the agent performed rapid prompt-level adjustments. True Tri-Loop discipline requires diagnosing the subagent's execution environment before re-firing.

---

---

## 🏷️ System Taxonomy Standard
* **`FEAT-xxx` (Software Features):** Application & cognitive architecture (CognitiveHub, Web Intercom, Foyer Router, Context Scoping, Blackboard Ledger, Telemetry UI).
* **`BKM-xxx` (Operational Protocols):** Agentic workflows, session discipline, delegation rules, and verification standards.
* **`LAB-xxx` (Hardware & Infrastructure):** Physical/virtual nodes, GPU/Metal memory constraints, systemd daemons (`lab-attendant.service`), ports, and environment plumbing.

---

## 🚀 Sprint 70.0 Phase 2: Follow-Up Stories & Tri-Loop Swarm Workstream

### 🛡️ Story 70.6: Direct-to-Online Boot Ignition & Manual Hibernation Hook Hardening (`[LAB-110B]`)
* **Status:** `[COMPLETE]` (Certified by `HomeLabAI/src/tests/test_direct_online_boot.py` — 3/3 passed in 0.21s)
* **Execution Forensics (Tri-Loop Protocol [BKM-049]):**
  * *Attempt 1 (M5 Air):* Failed due to oMLX prefill memory guard rejecting 24.5k tool schema context (`metal_cap ceiling 24.46 GB`).
  * *Attempt 2 (Kender 4090):* Execution succeeded on 4090 (309s) but subagent drifted into codegraph search due to unanchored `INFRA_CONFIG` object shape. Handover reflection provided exact remediation guidance.
  * *Attempt 3 (Kender 4090):* Subagent attempted file writes using `echo >` clobbering `manager.py`. Primary Agent (AGY) executed authorized takeover per Tri-Loop Law, applying surgical AST patch to `manager.py:main_loop()` and writing full 3-case pytest suite.
* **Target Files:**
  * `HomeLabAI/src/v5/ignition/manager.py` (L602–614: Direct-to-online boot check for `hibernation.enabled` and `PERMANENT_RESIDENT`)
  * `HomeLabAI/src/tests/test_direct_online_boot.py` (3 test cases: disabled hibernation, permanent residency, and on-demand bypass)
* **Verification Command:** `HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_direct_online_boot.py` (3 passed in 0.21s)

---

### 🧬 Story 70.7: Round Table Context Scoping & Blackboard Ledger DNA (`[FEAT-523]`)
* **Status:** `[COMPLETE]` (Certified by `HomeLabAI/src/tests/test_blackboard_dna.py` — 3/3 passed in 0.25s)
* **Execution Forensics (Tri-Loop Protocol [BKM-049]):**
  * *Attempt 1 (Local Swarm):* Junior completed symbolic exploration but committed an omission hallucination, marking todos as completed without writing files.
  * *Attempt 2 (Local Swarm):* Junior wrote `blackboard_ledger.py` after self-healing a bash quote syntax error, but truncated `cognitive_hub.py` via `echo >`. Primary Agent immediately restored clean file from git.
  * *Attempt 3 (Local Swarm):* Scoped strictly to `test_blackboard_dna.py`. Junior generated tests but hit import path naming ambiguities.
  * *AGY Takeover Gate:* Per Tri-Loop Law, Primary Agent (AGY) executed authorized takeover: enhanced `memory/blackboard_ledger.py` with `ContextScope` and `to_dict()`, wired `_process_node_stream` and turn finalization in `cognitive_hub.py`, and verified the full test suite.
* **Target Files:**
  * `HomeLabAI/src/memory/blackboard_ledger.py` (`ContextScope` enum, `BlackboardLedger` class)
  * `HomeLabAI/src/logic/cognitive_hub.py` (L29 import, L393 `blackboard_ledger` init, L730 `ContextScope` enforcement, L1415 turn recording)
  * `HomeLabAI/src/tests/test_blackboard_dna.py` (3 test cases: ledger operations, enum values, and CognitiveHub query isolation/enrichment)
* **Verification Command:** `HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_blackboard_dna.py` (3 passed in 0.25s)

---

### ⏱️ Story 70.8: The "Dead Air Delta" Benchmark Harness (`[FEAT-524]`)
* **Status:** `[COMPLETE]` (Certified by live silicon runs in `test_dead_air_delta.py` & `DEAD_AIR_DELTA_REPORT.md`)
* **Execution Mode:** `[PURE AGY]`
* **Empirical Silicon Results:**
  * *Operational Hot Steady-State:* Total Round Trip = **0.838s** (838 ms). $\Delta t_1$ (User $\rightarrow$ Triage) = **30 ms**, $\Delta t_5$ (Pinky synthesis delivery) = **808 ms**.
  * *Cold Boot Ignition:* Pre-flight VRAM 7,199 MB $\rightarrow$ 837 MB (`HIBERNATING`). $\Delta t_1$ (Kender Speculative Triage) = **1.247s**, First Crosstalk Bridge = **+10.23s** (`[SYSTEM] WAKING`), Full Ignition Complete = **+100.14s** (`[SYSTEM] OPERATIONAL`).
* **Target Files:**
  * `HomeLabAI/src/debug/test_dead_air_delta.py` (Playwright multi-condition harness tracking the 5 discrete actor handovers)
  * `Portfolio_Dev/field_notes/DEAD_AIR_DELTA_REPORT.md` (Detailed benchmark report with handover SLA targets)
  * `Portfolio_Dev/field_notes/data/dead_air_deltas.json` (Structured JSON telemetry records)
* **Verification Command:** `HomeLabAI/.venv/bin/python3 HomeLabAI/src/debug/test_dead_air_delta.py --condition hot`

---

### 📊 Story 70.9: Round Table Delta-T Telemetry & Blackboard Drawer UI (`[FEAT-525]`)
* **Status:** `[COMPLETE]` (Certified by Playwright DOM suite `HomeLabAI/src/tests/test_benchmarks_delta_t_ui.py`)
* **Execution Mode:** `[HYBRID AGY + SWARM]`
* **Implemented Features:**
  * Added 4th navigation tab `⏱️ ROUND TABLE DELTA-T` and `#tab-delta-t` pane in `benchmarks.html`.
  * Authored `benchmarks.js` rendering high-DPI canvas stacked waterfall chart `#delta-t-chart` with color-coded actor handover segments: Blue (Triage) $\rightarrow$ Pink (Pinky) $\rightarrow$ Red (Brain) $\rightarrow$ Purple (Deep Thought) $\rightarrow$ Green (Pinky Judgment).
  * Implemented `#blackboard-drawer` collapsible accordion with `toggleBlackboardDrawer()` function displaying historical turn summaries and 1-line consensus records.
* **Target Files:**
  * `Portfolio_Dev/field_notes/benchmarks.html` (Tab button, styles, tab pane, canvas, and accordion markup)
  * `Portfolio_Dev/field_notes/benchmarks.js` (Canvas waterfall renderer, drawer toggle, and DOM event wiring)
  * `HomeLabAI/src/tests/test_benchmarks_delta_t_ui.py` (Playwright DOM certification suite)
* **Verification Command:** `HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_benchmarks_delta_t_ui.py` (1 passed in 1.45s; 10/10 passed in sprint regression suite)

---

## 🏆 Sprint 70.0 Phase 2 Completion Matrix

| Story | Feature ID | Description | Mode | Certified By |
| :--- | :--- | :--- | :--- | :--- |
| **Story 70.6** | `[LAB-110B]` | Direct-to-Online Boot Ignition | Tri-Loop $\rightarrow$ AGY | `test_direct_online_boot.py` (3/3 pass) |
| **Story 70.7** | `[FEAT-523]` | Context Scoping & Blackboard Ledger DNA | Tri-Loop $\rightarrow$ AGY | `test_blackboard_dna.py` (3/3 pass) |
| **Story 70.8** | `[FEAT-524]` | Dead Air Delta Benchmark Harness | Pure AGY | `test_dead_air_delta.py` & `DEAD_AIR_DELTA_REPORT.md` |
| **Story 70.9** | `[FEAT-525]` | Round Table Delta-T & Blackboard Drawer UI | Pure AGY | `test_benchmarks_delta_t_ui.py` (1/1 pass) |

---

## 🚀 Sprint 70.0 Phase 3: Live Telemetry & Public Benchmark Decoupling

### 📋 Architectural Context & Master Blueprint (Turn 29362 Alignment)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PUBLIC / EXTERNAL (www.jason-lab.dev • GitHub Pages)                       │
│  "Federated Silicon Benchmarks"                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  [🔒 ACCESS LIVE LAB TELEMETRY]  (CTA Button linking to Zero Trust tunnel)   │
│                                                                             │
│  STATIC HARDWARE SEAT CARDS:                                                │
│  [ Apple M5 Air ]     [ Windows 4090 ]     [ Linux 2080 Ti ]   [ Cloud ]    │
│                                                                             │
│  TAB 1: PERFORMANCE ARENA        TAB 2: ENERGY & FINANCIAL ROI              │
│  ├─ Verified Max Throughput      ├─ Energy Efficiency (Tokens/Joule)        │
│  ├─ Warm TTFT Baseline           ├─ Electricity vs. Claude API Multiplier   │
│  └─ Model Residency Specs        ├─ CoT Reasoning Depth Ratio               │
│                                  └─ Interactive Cost Savings Calculator     │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  PRIVATE / INTERNAL (notes.jason-lab.dev:9001 • Cloudflare Access)          │
│  "Federated Model Telemetry"                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  Header: [Sync Pulse • Active Socket]  [📖 External Pedigree Benchmark Link] │
│                                                                             │
│  LIVE DYNAMIC HARDWARE SEATS:                                               │
│  (Real-time DCGM VRAM %, Watts draw, Sleep/Wake status, current resident)   │
│                                                                             │
│  TOP: DELTA-T TIME SERIES                                                   │
│  Cumulative stage lines across turns ($t_1 \rightarrow t_5$)                │
│                                                                             │
│  BOTTOM: MERGED UNIFIED LEDGER                                              │
│  Turn-level Blackboard DNA expanding to reveal discrete subagent runs       │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### Data Export & Push Protocol (Sticky Situation Governance)
1. **Strict Git Invariant:** All automated scripts write locally to `data/`. Automated processes NEVER push. The user alone initiates remote pushes.
2. **Sanitization Filter:** Private LAN IPs (`192.168.1.x`), raw session tokens, and local paths are stripped before export.
3. **Static Certification:** Public benchmarks are framed as *Certified Pedigree Benchmarks (Static)* with "Last Certified" timestamps, avoiding stale live claims.
4. **Shared Component Styling:** Public and internal surfaces share standard CSS classes to prevent UI drift.

---

### 📊 Pre-Story 70.9B: Safe-Patch Subagent Certification Harness (`[FEAT-529]`)
* **Status:** `[PENDING DELEGATION]`
* **Assigned Execution Mode:** `[TRI-LOOP LADDER: LOCAL (Atlas/Junior) -> CLOUD (DeepSeek/Cohere) -> AGY]` (via `delegate.py` on REST port 4097)
* **Objective:** Certify that subagents can invoke `clara-dna_safe_patch` (or AST patcher) to make surgical modifications to existing files without resorting to destructive bash `echo >` or `cat << 'EOF' >` overwrites.
* **Target Files:**
  * `HomeLabAI/src/tests/fixtures/patch_target.py` (Harness target file for patch mutations)
  * `HomeLabAI/src/tests/test_safe_patch_harness.py` (Test asserting safe_patch execution and AST validity)
  * `HomeLabAI/src/tests/delegate.py` (Prompt injection with explicit `clara-dna_safe_patch` few-shot tool schema)
* **Acceptance Criteria:**
  1. `delegate.py` payload includes explicit JSON tool call example for `clara-dna_safe_patch`.
  2. Subagent modifies `patch_target.py` surgically via tool call without clobbering surrounding code.
  3. `ruff check` passes with 0 syntax or AST errors.

---

### 📊 Story 70.10: Unified Nested Ledger (Turn Blackboard + Subagent Workload Stream) (`[FEAT-526]`)
* **Status:** `[PENDING DELEGATION]`
* **Assigned Execution Mode:** `[SWARM DELEGATION: ATLAS + JUNIOR]` (via `delegate.py` on REST port 4097)
* **Objective:** Merge the granular subagent execution stream directly inside the expandable Blackboard Turn details cards so each turn shows its own subagent runs, while background scans display as `[BATCH]` cards.
* **Target Files:**
  * `Portfolio_Dev/field_notes/benchmarks.js` (Unified ledger rendering logic)
  * `Portfolio_Dev/field_notes/benchmarks.html` (Markup container alignment)
  * `HomeLabAI/src/tests/test_unified_ledger_ui.py` (Playwright verification suite)
* **Acceptance Criteria:**
  1. Each turn `<details class="feature-details">` expands to show:
     - Distillation Bullets
     - 1-Line Consensus
     - Stage Delta Handover Telemetry
     - Nested Subagent Dispatches Table (Model, Tokens, Duration, Tok/s)
  2. Batch / non-interactive workloads render cleanly as `[BATCH] NIGHTLY_REFINEMENT` cards.
  3. Playwright DOM assertions verify nested structure and zero console errors.

---

### 📊 Story 70.11: Sanitized Public Benchmark Exporter (`[FEAT-527]`)
* **Status:** `[PENDING DELEGATION]`
* **Assigned Execution Mode:** `[SWARM DELEGATION: ATLAS + JUNIOR]` (via `delegate.py` on REST port 4097)
* **Objective:** Author an automated export script `Portfolio_Dev/field_notes/export_public_benchmarks.py` that ingests local telemetry and produces a clean, redacted `data/public_benchmarks.json` bundle.
* **Target Files:**
  * `Portfolio_Dev/field_notes/export_public_benchmarks.py` (Sanitizing export engine)
  * `HomeLabAI/src/infra/test_benchmark_sanitizer.py` (Unit test verifying zero LAN IP / token leakage)
* **Acceptance Criteria:**
  1. Regex scanner strips all `192.168.1.x` IPs, `ses_xxx` tokens, and `/home/jallred` paths.
  2. Generates valid `public_benchmarks.json` with hardware seats, throughput/TTFT averages, and ROI calculations.
  3. Unit test asserts 100% pass on leak-detection test vectors.

---

### 📊 Story 70.12: Public Showcase Surface on Airlock (`[FEAT-528]`)
* **Status:** `[PENDING DELEGATION]`
* **Assigned Execution Mode:** `[SWARM DELEGATION: ATLAS + JUNIOR]` (via `delegate.py` on REST port 4097)
* **Objective:** Deploy a clean, lightweight public showcase page `public_benchmarks.html` reading `public_benchmarks.json` with static cards, comparative bars, interactive ROI slider, and a zero-trust link button.
* **Target Files:**
  * `Portfolio_Dev/field_notes/public_benchmarks.html` (Standalone static showcase)
  * `HomeLabAI/src/tests/test_public_benchmarks_ui.py` (Playwright DOM verification)
* **Acceptance Criteria:**
  1. Header contains `🔒 ACCESS LIVE LAB TELEMETRY` button pointing to Zero Trust notes.
  2. Renders 4 static hardware seats, Throughput/TTFT bars, Tokens/Joule, and ROI calculator with zero external API/websocket dependencies.
  3. Playwright test confirms 100% offline static rendering in < 1.0s.


