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
