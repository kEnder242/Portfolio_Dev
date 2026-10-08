# 📋 SPRINT LOG 100.0: JIT Architecture, Parallel Orchestration & Lab Hardening

**Sprint ID:** `SPR_100_0`  
**Parent Framework:** `BKM-005` (Design Studio Alignment), `BKM-006` / `BKM-007` (Work Completion Report), `BKM-020` (High-Fidelity Sprint Documentation), `BKM-024` (Live Verification), `BKM-077` (ANCHOR_TRACK), `BKM-078` (One-Shot Surgical Contract), `BKM-079` (Speculative Triage Lead Calibration).  
**Date:** October 6–7, 2026  
**Status:** **ALL STORIES & HARDENING DELIVERABLES COMPLETED & CERTIFIED (100% GREEN)**  

---

## 📊 1. Story & Hardening Execution Matrix

| Story / Task ID | Owner | Mode | Target / Scope | Status | Evidence / Artifacts |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Story 100.1** | `[AGY:PRIMARY]` | Direct | GDM autologin, lockfile purge, intercom deploy | **COMPLETED & CERTIFIED** | Dead PID lockfile reaper in `standalone_accountability_watchdog.py` (`b384a15`); `intercom_v2.js` hash-guarded deploy. |
| **Story 100.2** | `[AGY:PRIMARY]` | Direct | `AcmeLab/src/clara_dna_mcp_server.py` | **COMPLETED & CERTIFIED** | FastMCP canonical `jit_*` tools registered (`jit_read`, `jit_locate`, `jit_stage`, `jit_research`, `jit_diagnose`, `jit_checkpoint`) with backward-compatible aliases. |
| **Story 100.3** | `[AGY:PRIMARY]` | Direct | `context_prewarmer.py`, `.jit_cache/` | **COMPLETED & CERTIFIED** | Context cache relocated from `/tmp` to `.jit_cache/`; file-scoped `mtime` invalidation and `safe_patch` targeted cache eviction active. |
| **Story 100.4** | `[AGY:PRIMARY]` | Direct | `oh-my-openagent.json`, `AGENTS_L2.md`, `AGENTS_L3.md` | **COMPLETED & CERTIFIED** | OpenCode permission profiles updated (`jit_read` allowed on L2, denied on L3); `test_subversive_prompt.py` verified 6/6 green. |
| **Story 100.5** | `[AGY:PRIMARY]` | Direct | `delegate.py`, `context_prewarmer.py` | **COMPLETED & CERTIFIED** | Sub-inference token receipts logged to `.jit_cache/sub_inference_ledger.jsonl` and aggregated into `delegate.py` telemetry. |
| **Story 100.6** | `[SWARM:LOCAL]` | Swarm Local | KENDER 4090 + M5 Air live shakedown | **COMPLETED & CERTIFIED** | Shakedown pass verified in 829.0s (`ses_eeb08d8f0ffes9iYH0Pe36rPed`); full `jit_*` toolchain executed without permission blocks. |
| **Story 100.7** | `[AGY:PRIMARY]` | Direct | `FEAT-655`, `BKM-078`, `AGENTS_L2.md`, `AGENTS_L3.md` | **COMPLETED & CERTIFIED** | Codified JIT One-Shot Surgical Contract: bounded iteration ($N \le 2$), mandatory AST line-range anchors, and anti-spiral conductor discipline. |
| **Hardening A** | `[AGY:PRIMARY]` | Direct | `field-notes-nightly.service` | **COMPLETED & CERTIFIED** | Expanded systemd `TimeoutStartSec` from 900s (15 min) to 21600s (6 hrs); verified un-killed multi-adapter LoRA training completion. |
| **Hardening B** | `[AGY:PRIMARY]` | Direct | `src/nodes/mlx_judge_node.py` | **COMPLETED & CERTIFIED** | Increased `MLX_TIMEOUT_SEC` from 15s to 45s; eliminated premature fallback to local standby stubs under deliberate evaluation load. |
| **Hardening C** | `[AGY:PRIMARY]` | Direct | `src/v5/ignition/manager.py` | **COMPLETED & CERTIFIED** | Added Smart-Reuse port 8088 probe in fallback & `main_loop`; prevents duplicate vLLM daemon collisions and protects VRAM residency. |
| **Hardening D** | `[AGY:PRIMARY]` | Direct | `standalone_accountability_watchdog.py` | **COMPLETED & CERTIFIED** | Full accountability audit certified: 7/7 checks green across power, Foyer, locks, forge, LoRA multi-adapter, dreaming gems, and live round table. |
| **Story 100.8** | `[AGY:PRIMARY]` | Direct | `speculative_triage.py`, `infrastructure.json`, `cognitive_hub.py` | **COMPLETED & CERTIFIED** | Calibrated speculative triage lead window to the parallel race differential ($W_{\text{lead}} = 400\text{ms}$, $t_{\text{warmed}} = 0.20\text{s}$); isolated EWMA estimators; 17/17 pytest green; live triage verified in 879ms. |

---

## 🛠️ 2. Detailed Execution Log: Session Hardening & Accountability Audit

### Hardening A: Nightly Forge Service Timeout Remediation
* **Forensic Finding:** During multi-adapter LoRA training sweeps, systemd terminated `field-notes-nightly.service` prematurely after 900 seconds (15 minutes), marking the service as `failed (Result: timeout)` despite active GPU gradient descent.
* **Remediation:**
  1. Updated `TimeoutStartSec=21600` (6 hours) in both `HomeLabAI/config/systemd/field-notes-nightly.service` and the active host unit `/etc/systemd/system/field-notes-nightly.service`.
  2. Executed `sudo systemctl daemon-reload`.
  3. Confirmed `HomeLabAI/run/nightly_forge_state.json` accurately reflects `status: COMPLETED` with valid age timestamps.

### Hardening B: MLX Judge Resilience & Timeout Expansion
* **Forensic Finding:** In `HomeLabAI/src/nodes/mlx_judge_node.py`, the remote MLX judge timeout was hardcoded to 15 seconds. High-context deliberate multi-agent round tables on M5 Air under load occasionally exceeded 15s, causing the node to prematurely fail over to `STANDBY_STUB` (`score: 0.0`), failing synthetic accountability probes.
* **Remediation:**
  1. Increased `MLX_TIMEOUT_SEC` from 15 to 45 seconds.
  2. Provided sufficient runway for full context evaluation on M5 Air without dropping genuine judicial oversight.

### Hardening C: Smart-Reuse Port 8088 Probe in Ignition Manager
* **Forensic Finding:** When Foyer or ignition manager restarted, the fallback loop and `main_loop` in `src/v5/ignition/manager.py` blindly attempted to re-ignite a fresh vLLM process on port 8088 without checking if a healthy resident vLLM process was already running. This risked port binding errors, duplicated GPU VRAM allocation, and process collisions.
* **Remediation:**
  1. Added non-blocking HTTP `/v1/models` socket probe targeting `127.0.0.1:8088` in both the fallback routine and `main_loop`.
  2. When the probe succeeds, ignition logs `[IGNITION] Existing healthy vLLM detected on port 8088 — adopting resident process` and skips re-launch, preserving GPU VRAM residency.

### Hardening D: Full 7/7 Standalone Accountability Audit Certification
* **Audit Execution:** Executed `standalone_accountability_watchdog.py` to audit all seven physical lab invariants:
  1. `GPU Power Clamp (165W)`: Verified 165.0W limit (max 170.0W) $\to$ **PASS**
  2. `Foyer Re-Ignition & Hot-Reload`: Verified state `OPERATIONAL`, status `ONLINE`, engine `UP` $\to$ **PASS**
  3. `Lockfile Cleanliness & Quiescence`: Verified all stale locks cleared in `/tmp/` and `/run/` $\to$ **PASS**
  4. `Nightly Forge Orchestration`: Verified state `COMPLETED` $\to$ **PASS**
  5. `LoRA Fine-Tuning Multi-Adapter Pass`: Verified 4/4 adapters active on `:8088` $\to$ **PASS**
  6. `Accountable Subconscious Dreaming`: Verified 4 active Gems in `memories.db` $\to$ **PASS**
  7. `Synthetic Morning Round Table Probe`: Verified greeting latency 2.11ms, triage routing `kender_online`, MLX Critic Score `0.95` $\to$ **PASS**
* **Certification:** Authoritative digest written to `daily_accountability_digest.json` (`overall_status: PASS`, 0 discrepancies).

---

## 🧭 3. Detailed Execution Log: Story 100.8 (Speculative Triage Calibration)

### The Forensic Finding (Because / Therefore)
* **Because** previous iterations in Sprint 71 (`FEAT-531`) conflated lightweight transport-layer TCP socket/probe latency (`t_warmed = 0.09` for a GET `/v1/models` check) with full structured LLM inference completion (~930ms for a 25-token triage JSON),
* **Therefore** the speculative head-start window was artificially truncated to $2 \times 0.09\text{s} = 0.18\text{s}$ (180ms).
* **Because** Apple M5 Air (`TokenAI-zer--Ternary-Bonsai-2-27B-MLX`) cannot generate a complete structured JSON in 180ms, Foyer prematurely launched local vLLM on every single query.
* **Because** vLLM completes execution in ~650ms, launching it at 180ms caused vLLM to cross the finish line at $180\text{ms} + 650\text{ms} = 830\text{ms}$, consistently undercutting warm M5 Air (930ms).
* **Furthermore, because** line 409 of `speculative_triage.py` observed the completion latency into the lead estimator (`deep_thought`) even when the racer (`vllm`) won, vLLM's fast duration poisoned Deep Thought's EWMA estimator, trapping M5 Air in a perpetual losing loop.

### The Parallel Differential Calculus
* Speculative racing does not require waiting for M5 Air to complete before launching backup compute. In a parallel race, the required lead window $W_{\text{lead}}$ only needs to offset the **execution differential**:
  $$W_{\text{lead}} > t_{\text{air}} - t_{\text{vllm\_exec}}$$
* Telemetry characterization from `Portfolio_Dev/field_notes/benchmarks_cache.json` and `foyer_stage_ledger.jsonl`:
  * Warm M5 Air ($P_{90}$): **~980 ms**
  * Local vLLM execution: **~650 ms**
  * Differential: $980\text{ms} - 650\text{ms} = \mathbf{330\text{ms}}$
* Adding a ~70ms buffer for OS scheduling and scheduling jitter yields:
  $$\mathbf{W_{\text{lead}} = 400\text{ms} \quad (t_{\text{warmed}} = 0.20\text{s})}$$

### Regime Comparison Table:

| Regime | $W_{\text{lead}}$ | $t_{\text{warmed}}$ ($W/2$) | Warm M5 Air Outcome (~930 ms) | Cold / Sluggish M5 Air (~3.0 s) | Parallelism |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Old Ping (Sprint 71)** | **180 ms** | 0.09 s | ❌ **vLLM wins at 830 ms** (steals turn) | ✅ vLLM wins at 830 ms | High, but undercuts warm reasoning |
| **Sequential Timeout** | **1,000 ms** | 0.50 s | ✅ **Air wins at 930 ms** (vLLM never launches) | ⚠️ vLLM wins at **1,680 ms** (waits 1.0s before launch) | Zero parallelism on warm turns |
| **Tight Speculative Race** | **400 ms** | **0.20 s** | ✅ **Air wins at 930 ms** (beats vLLM by 150 ms) | ⚡ **vLLM wins at 1,080 ms** (**600 ms faster!**) | **Optimal parallel overlap** |

### Outcomes at 400ms:
1. **Warm Steady State (~930 ms):** M5 Air starts at $t=0$, vLLM starts at $t=400\text{ms}$. vLLM would finish at $400 + 650 = 1,050\text{ms}$. M5 Air finishes at ~930ms and wins by ~120ms. vLLM is cancelled and discarded. Sovereign reasoning is preserved for >90% of turns.
2. **Cold Wake / Hibernation / Sluggishness (~3.0 s):** vLLM launches at $t=400\text{ms}$ and completes at $t=1,080\text{ms}$. Cold Air is cancelled. User latency drops from 3.0s down to **1.08s** (a 600ms improvement over sequential 1.0s timeouts).
3. **Offline Remote Seat:** Dual-check gate detects offline state in <50ms and dispatches local vLLM immediately with 0ms delay.

---

## 🛠️ 4. Implemented Code & Configuration Artifacts

1. **`HomeLabAI/config/infrastructure.json`:**
   * Updated `seats`: `M5_AIR`, `KENDER`, and `LOCAL` set to `t_warmed: 0.20` ($2 \times 0.20\text{s} = 0.40\text{s}$).
2. **`HomeLabAI/src/infra/engine_client.py`:**
   * Synchronized fallback seat definitions to `t_warmed: 0.20`.
3. **`HomeLabAI/src/logic/speculative_triage.py`:**
   * Constructor default updated to `t_warmed=0.20`.
   * Enforced dynamic floor: `lead_window()` returns $\max(2 \times t_{\text{warmed}},\, L_t + 4 \times J_t)$.
   * Estimator isolation fix: Recorded `t_racer = time.monotonic()` and updated each winner's isolated estimator (`self._estimators[winner]`), preventing vLLM wins from polluting Deep Thought's EWMA state.
4. **`HomeLabAI/src/logic/cognitive_hub.py`:**
   * Updated `SpeculativeTriageRelay` instantiation to `t_warmed=0.20`.
5. **Unit Tests:**
   * Updated `test_speculative_triage_seats.py` mock seats and assertion to `0.40s` head start.
   * Increased `mock_kender_slow` sleep to 1.5s in `test_speculative_triage.py` to properly model sluggish inference beyond the 0.40s window.
   * Fixed payload assertion in `test_kender_fast_gate.py` to handle `_finalize_payload` metadata.
   * **Full suite pass:** 17/17 tests passing green in 5.02s.

---

## 🔬 5. Live Verification & Ground Truth Audit (`BKM-024`)

* **Resident Hot-Reload:** `curl -X POST http://localhost:8765/reload_residents` returned `status: success`, commit `09a18e2`, `reconciled_silicon: true`.
* **Live Triage Timing (`foyer_stage_ledger.jsonl`):**
  * Request `c457d1b0`: `STARTED: 1791398329.176`, `COMPLETED: 1791398330.055` $\to$ **879.4 ms** total triage duration (`kender_online`).
  * Request `7a0c197d`: Verified triage routing to `kender_online`.
* **Live Deliberation Probe:** Ground-truth multi-agent deliberation probe executed live against Foyer `:8765`:
  * Greeting Latency: 2.11 ms
  * Triage Routing: `kender_online` (M5 Air)
  * Critic Score: **0.95 (ONLINE_EVALUATED by MLX Judge)**
  * Status: **PASS**

---

## 📚 6. Documentation & DNA Synchronization (`BKM-068`)

* **`Portfolio_Dev/field_notes/features.html`:** Updated `[FEAT-586]` Logic, Rationale, and Mechanism to formalize the parallel differential model ($W_{\text{lead}} > t_{\text{air}} - t_{\text{vllm}}$) and estimator state isolation.
* **`Portfolio_Dev/field_notes/triage_inference_calibration.md`:** Published field note capturing full telemetry benchmarks, regime comparison table, and lead-time equations.
* **`Portfolio_Dev/docs/sprints/active/SPRINT_PLAN_SPR_100_0.md`:** Updated `ANCHOR-12` as certified completed.

---

## 🧭 7. Forensic System Lineage: The Anatomy of a Cascading Regression & Restoration to Known-Good Architecture

### 7.1 Context & Motivation ("Staying Sane")
Every day we felt we were slipping backwards into regressions: thinking loops reappearing, context blowing up, and agents refusing to delegate. This log records the exact causal chain—applying the South Park rule (*"Because X, Therefore Y"*)—to serve as the definitive sanity anchor and prevent recurring amnesia across future sessions.

### 7.2 The Causal Chain of Breakdown

```
[Sprint 98-99 "Green Lie"] 
OpenCode ran /home/jallred/AcmeLab/src/clara_dna_mcp_server.py externally,
while tests imported in-tree copies.
   │
   ▼ (Because we needed a single source of truth...)
[Oct 6 23:37 PDT: Commit 9fdc567 / f60f75e]
Consolidated canonical MCP server into HomeLabAI/src/mcp/clara_dna_mcp_server.py
and symlinked AcmeLab.
   │
   ├─► Bug A (Context Dump): stage_research returned {"blueprint": patch_blueprint...}
   │                         echoing multi-KB plans back into Atlas's context on Turn 2.
   │
   └─► Bug B (Namespace Mismatch): Junior's permission in oh-my-openagent.json
                                   was set to safe_patch instead of clara-dna_safe_patch.
   │
   ▼ (Because Junior was blocked by OpenCode tool-namespacing and Atlas was bloated...)
[Oct 7 17:17 PDT: Panic Bypass Commit 124ec01]
Operators assumed Layer 2 -> Layer 3 delegation was fundamentally broken.
Therefore, "task" was added to disabled_tools, Atlas was set to "task": "deny",
and Atlas was forced into "DIRECT EXECUTION MODE" with safe_patch/write permissions.
   │
   ▼ (Because Atlas on KENDER 4090 was forced to read full files and write diffs directly...)
[The VRAM & Reasoning Collapse]
Atlas read full 200KB source files, exploding context from <3,000 tokens to 64,000+ tokens.
Therefore, KENDER 4090 stalled in 4-to-5 minute prompt-eval stalls, Ollama ignored
Anthropic thinking suppression on /v1/, and Qwen fell into infinite reasoning spirals.
```

### 7.3 The Forensic Discoveries

1. **The MCP Server Move Was Right, But Poisoned at the Seams:**
   Moving the MCP server inside `HomeLabAI/src/mcp/` and keeping `/home/jallred/AcmeLab/src/clara_dna_mcp_server.py` as a symlink was the correct architectural choice to end the "Green Lie". However, shipping untested return dictionaries (`"blueprint"` echo) directly broke Conductor context invariants.
2. **OpenCode Namespacing Is Inflexible:**
   FastMCP tools exposed by `clara-dna` MUST be matched in `oh-my-openagent.json` with their server prefix (`clara-dna_safe_patch`, `clara-dna_jit_stage`). Unprefixed entries cause silent runtime permission rejections.
3. **Panic Bypasses Warp Architecture:**
   When delegation failed, committing "Direct Execution Mode" (`124ec01`) broke `BKM-078: JIT_ONE_SHOT` and corrupted the bicameral model. Instead of fixing the 1-line tool permission on Junior, the entire delegation topology was dismantled.
4. **Ollama /v1/ vs. Headroom:**
   Ollama's native `/api/chat` respects `"think": false`, but its OpenAI-compatible `/v1/` endpoint does not reliably strip reasoning blocks. Headroom proxy (port 8787 / 8002) is mandatory to enforce thinking suppression and clean context boundaries on local silicon.

### 7.4 In-Flight Fixes Applied on `fork/sprint-100-run-b`

1. **Context Dump Stripped (`83855c5` in `HomeLabAI`):**
   `stage_research` in `clara_dna_mcp_server.py` now returns strictly `{"status": "staged", "file_path": file_path}`, restoring Turn 2 Conductor response payload to <10 tokens.
2. **Bicameral Separation Restored (`31f439f` in `Dev_Lab`):**
   - Removed `"task"` from `disabled_tools`.
   - Set `"task": "allow"` on Atlas; set `"write": "deny"`, `"edit": "deny"`, `"safe_patch": "deny"`, `"read": "deny"`. Atlas is once again a **Pure Conductor**.
   - Granted Junior `"clara-dna_safe_patch": "allow"` alongside `"safe_patch"`, keeping Junior terminal (`"task": "deny"`).
3. **Hardware Context Hardening (`31f439f` in `Dev_Lab`):**
   - Capped `atlas:27b` context to `32,768` tokens in `opencode.json` per `LAB-115`.
4. **Headroom Proxy Reactivated:**
   - Started and enabled `headroom-proxy.service` on `127.0.0.1:8787`.

### 7.5 Invariant Rule Going Forward
> [!CAUTION]
> **NO MORE PANIC BYPASSES:** When a worker fails to execute a task, do NOT disable `task` delegation or make Atlas a direct coder. Check the MCP namespace prefix in `oh-my-openagent.json`, verify the context return size in `clara_dna_mcp_server.py`, and inspect the Headroom proxy port. The bicameral model (Conductor on 4090 $\to$ Worker on M5 Air) is the law.

---

## 8. Phase 4 Execution & Delegation Maturation: The Hardening Sprints (100.8B - 100.11)

### 8.1 The Story Execution Trajectory

1. **Story 100.8B — Oracle Adversarial Pre-Pass (`[BKM-061]`/`[FEAT-640]`):**
   - Dispatched to Cloud Oracle (OpenRouter Nemotron-120B / Free Tier, 54k tokens).
   - Adversarially audited Stories 100.9–100.15, catching legacy Sprint 32 PECI/MSR scars in `_distill_strategic_brief()`, HyDE turn leakage, and triage policy drift.
   - Result: Blended findings committed to `ORACLE_REVIEW_SPRINT_100.md` with explicit remediation checklists.

2. **Story 100.9 — HyDE Multi-Turn Scope Isolation (`[FEAT-640]`/`[FEAT-437]`):**
   - Forensic defect: Pinky HyDE synthesis defaulted to `ContextScope.LONG`, injecting Turn 1 greetings (`[PREVIOUS_DEBATE]: User: hi`) into Stage 2 vector generation and causing false-positive casual classification.
   - Fix: Threaded explicit `request_id` and enforced `scope=ContextScope.TURN` in `cognitive_hub.py::resolve_hyde_vector`.
   - Verified 13/13 green in `test_feat437_resolve_hyde_vector.py`. Committed in HomeLabAI `bc38f7b`.

3. **Story 100.10 — Defeature CASUAL Vibe & 9-Vibe Taxonomy Alignment (`[FEAT-640]`):**
   - Forensic defect: Triage prompt offered CASUAL as an explicit LLM archetype choice, bypassing RAG on conversational greetings.
   - Fix: Commented out `CASUAL` line from `cognitive_hub.py#L1487` prompt string with `[DEFEATURED]` marker; updated fallback test assertions in `test_triage_engine.py` (L578, L632) from `CASUAL` to `SOCRATIC`; sanitized line 1490 to eliminate employer persona leakage.
   - Forensic lesson (BKM-049 reflection audit): The Oracle review suggested setting `"enabled": false` in `triage_policy.json`, which collided with `test_triage_policy_loader.py::test_production_has_all_nine_vibes` (which checks that all 9 vibes remain enabled in policy). Reconciled by keeping CASUAL enabled in policy while defeatured in prompt choices.
   - Verified 79/79 green in `test_triage_engine.py`. Committed in HomeLabAI `3b1972d`.

4. **Story 100.11 — Mandatory Stage 1 Brain Gatekeeper & Relic Excision (`[FEAT-635]`):**
   - Forensic defect: 68-sprint-old `_distill_strategic_brief()` hardcoded `"Extract specific platform anchors, validation targets, and known PECI/MSR scars."` Fallback when interest $< 0.70$ routed to `_run_brain_leg`, polluting Brain output with off-topic PECI/MSR text.
   - Attempt 1 (Law 6 Fast-Halt): Atlas inspected `cognitive_hub.py` via `jit_read`, discovered 4 call sites and 2 sibling test files dependent on `_run_brain_leg`, and strictly halted per Law 6 (Under-Specified Contract Blocker Mandate) to escalate to AGY.
   - Attempt 1b (BKM-049 Tri-Loop Remediation): AGY formulated the decoupled stub pattern—completely excise `_distill_strategic_brief()`, enforce Stage 1 Brain Gatekeeper (`_run_two_mice_handover`) on 100% of technical queries on the Brain lead branch, and preserve `_run_brain_leg` as a clean pass-through stub so sibling tests and `both`-branch calls stay functional.

### 8.2 What We Learned & Infrastructure Upgrades Built

1. **LiteLLM Native Ollama Acceleration (`think: false`):**
   - Discovered that Ollama `/api/chat` ignores `options: {"enable_thinking": false}` and strictly requires root `"think": false`.
   - Benchmarked on Kender RTX 4090: dropped turn latency from 1.80s (61 reasoning tokens) to 0.39s (5 tokens) with 0 reasoning chars.
   - Deployed standard `litellm` gateway daemon (`litellm-kender.service` on port 11435) with `extra_body.think: false`, delivering instant streaming without response-side censorship.

2. **The Psychological Escalation Protocol (`ask_oracle` / `[FEAT-656]`/`[BKM-080]`):**
   - Built `@mcp.tool() ask_oracle` in `clara_dna_mcp_server.py`.
   - Wired polling intercept in `delegate.py` that exits cleanly with code 3, logs diagnostic banner, and caches state in `.jit_cache/paused_session.json`.
   - Added `--feedback "<directive>"` flag for zero-friction resumption and live test monitoring.

3. **Strict Cache-Mediated IPC & Zero-Diff Task Ticket Mandate (`[FEAT-655]`):**
   - Solved the L2/L3 redundancy trap: when L2 inlined diffs into `task()`, L3 skipped `jit_research()`.
   - Codified strict invariant in `AGENTS_L2.md`: All blueprints, AST anchors, and diff directives live exclusively in `jit_stage()`. `task()` prompts are strictly compact tickets (<100 tokens). If conductor must put diffs in `task()`, it must halt and call `ask_oracle`.

4. **BKM-049 Handover Reflection Ingestion as Epistemic Bridge:**
   - Established that AGY must never ignore `[HANDOVER REFLECTION]` reports.
   - Reflections provide the empirical ground truth needed to detect spec collisions (Story 100.10) and under-specified contracts (Story 100.11), allowing smart outer-loop remediation instead of blind retry thrashing.


