# 🚀 SPRINT PLAN 101.0: 02:00 AM Nightly Stability, Ignition Guardrails & Historical Grounding Hardening

**Sprint ID:** `SPR_101_0`  
**Theme:** 02:00 AM Nightly Task Stabilization, Morning Ignition 30-Minute Timeout & Kill Guardrail, LoRA Multi-Adapter Payload Calibration, Post-Training vLLM Profiling Settle Gate, Dedicated Sprint DNA Curator Engine Reconnection, Canonical Single-Home Wisdom Path Alignment, and Pre-Ignition Hygiene Cleanups  
**Status:** **PROPOSED & AWAITING OPERATOR GREENLIGHT**  
**Parent Framework:** `[BKM-005]` (Design Studio Alignment), `[BKM-006]` / `[BKM-007]` (Work Completion Protocol), `[BKM-020]` (High-Fidelity Sprint Gates & Phase 0 Housekeeping), `[BKM-024]` (Live Validation Mandate), `[BKM-048]` (JIT Fingertips Protocol), `[BKM-049]` (Owner Tag Mandate), `[BKM-066]` / `[BKM-067]` (Decoupled Accountability), `[BKM-077]` (ANCHOR_TRACK Ledger), `[BKM-082]` (Sprint Grounding Run Mandate), `[LAB-103]` / `[LAB-107]` / `[LAB-110]` (Host Memory & Power Sentinels), `[FEAT-160]` (Hardware Pacing), `[FEAT-213]` (VRAM Handover), `[FEAT-361]` (Token Transparency), `[FEAT-416]` (05:00 AM Work Window Cutoff), `[FEAT-557]` (Sprint DNA Curator Engine), `[FEAT-562]` (Wisdom Refiner), `[FEAT-629]` (Phase-Isolated Decoupled Nightly Architecture), `[FEAT-659]` (Sprint Grounding Protocol)  
**Target Silicon Nodes:** `z87-Linux` (RTX 2080 Ti Local vLLM 3B Base :8088), Node KENDER (RTX 4090 Ollama Conductor :11434), Node Brain (macOS M5 Air MLX :8002 via Headroom), ChromaDB Port 8001 (CLaRa-DNA)

---

## 🧭 Executive Summary & Core Invariants

Sprint 101.0 addresses the operational breakdown discovered during the 02:00 AM – 08:30 AM log horizon audit of October 8, 2026. The 2:00 AM nightly tasks made significant progress (successfully completing multi-adapter fine-tuning across 4 adapters), but degraded due to resource tightness, concurrency races, argument drift, and missing ignition guardrails.

Per **`[BKM-082]`**, every story embeds the full forensic context and cautions re-framed into **positive execution directives** ("Do Y because Z context guides you to do it this way"), ensuring that future agents operate with zero amnesia and full respect for physical hardware sentinels.

Furthermore, this sprint formalizes **Phase 0: Documentation Fortification & Housekeeping**, paying documentation debt forward before story execution begins.

---

## ⚓ BKM-077: ANCHOR_TRACK Ledger

| Anchor ID | Target Scope | Origin / Defect | State | Resolution Milestone |
| :--- | :--- | :--- | :---: | :--- |
| **ANCHOR-101.0** | Documentation & Maps | Argument drift & stale path pointers | `COMPLETED` | Phase 0: Fortify `DIAGNOSTIC_SCRIPT_MAP.md`, `FeatureTracker.md`, `BOOTSTRAP_v4.5.md`, `LAB_INFRASTRUCTURE.md`. |
| **ANCHOR-101.1** | `HomeLabAI/run/vllm.pid` | Dead PID file left on disk; port 8088 down | `PROPOSED` | Story 101.1: Pre-ignition hygiene; remove dead `vllm.pid` & purge orphan processes (`FEAT-119`). |
| **ANCHOR-101.2** | `HomeLabAI/src/logic/cognitive_hub.py` | Residual dialogue abort event flags | `PROPOSED` | Story 101.2: Ensure clean reset of turn abort flags on new turn initiation (`FEAT-227`). |
| **ANCHOR-101.3** | `HomeLabAI/src/nodes/loader.py` | Unexecuted Carry-Over Story 100.15: `internal=True` token suppression | `PROPOSED` | Story 101.3: Remove `stream_source = None` gag in `loader.py:210` per `FEAT-361`. |
| **ANCHOR-101.4** | `HomeLabAI/config/infrastructure.json` | LoRA training ran 208m (28m over 180m budget) | `PROPOSED` | Story 101.4: Trim steps 450 $\to$ 350 (~22% reduction) to fit under 04:30 AM (`FEAT-657`). |
| **ANCHOR-101.5** | `HomeLabAI/src/v5/ignition/manager.py` | 5-minute timeout leaves hanging vLLM process; no hard-kill | `PROPOSED` | Story 101.5: 30-min timeout + active process kill on timeout (`FEAT-656`). |
| **ANCHOR-101.6** | `field-notes-nibbler.service` | Mass scanning overrunning past 05:00 AM | `PROPOSED` | Story 101.6: Enforce 05:00 AM hard cutoff gate in nibbler per `FEAT-416`. |
| **ANCHOR-101.7** | `HomeLabAI/src/infra/nightly_forge.py` | vLLM memory profiling race with concurrent Subconscious Dreaming | `PROPOSED` | Story 101.7: 30s settling delay + blocking probe gate before Step 5 (`FEAT-658`). |
| **ANCHOR-101.8** | `HomeLabAI/src/infra/nightly_forge.py` | Argument drift calling `sync_chroma_dna.py --collection sprint_dna` | `PROPOSED` | Story 101.8: Rewire to dedicated `src/curator/sync_sprint_dna.py` (`FEAT-557`). |
| **ANCHOR-101.9** | `Portfolio_Dev/field_notes/refine_wisdom.py` | Path mismatch looking in `field_notes/data/wisdom_data.json` | `PROPOSED` | Story 101.9: Target canonical `Portfolio_Dev/dna/wisdom_data.json` (`FEAT-562`). |
| **ANCHOR-101.10** | `HomeLabAI/src/infra/nightly_forge.py` | Subprocess timeout (60s) prematurely cuts probe (75s wait) | `PROPOSED` | Story 101.10: Expand timeout to 120s (`FEAT-608`). |
| **ANCHOR-101.11** | Cgroup Telemetry (`/sys/fs/cgroup`) | Lack of swap peak monitoring during nightly heavy load | `PROPOSED` | Story 101.11: Add swap peak telemetry to watchdog & digest (`LAB-110`). |
| **ANCHOR-101.12** | Silicon & Daemons (`:8088`, `:8765`) | Foyer in OFFLINE standby; vLLM dead; digest graded FAIL | `PROPOSED` | Story 101.12: Physical restoration & 7/7 watchdog certification pass (`BKM-024`). |

---

## 📚 Phase 0: Documentation Fortification & Housekeeping (COMPLETED)

*Objective: Immunize future agents and subagents against argument guessing, path drift, and stale infrastructure pointers BEFORE touching code.*

### Story 101.0A: Fortify `DIAGNOSTIC_SCRIPT_MAP.md` Tool & CLI Arguments
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Status:** `COMPLETED`
* **Feature Anchor:** `[FEAT-659]` / `[BKM-082]` / `[BKM-020]`
* **Positive Context Guidance:**  
  *Document exact CLI arguments, inputs, and canonical dataset locations for `probe_round_table_accountability.py`, `sync_sprint_dna.py`, and `refine_wisdom.py` in [`DIAGNOSTIC_SCRIPT_MAP.md`](file:///home/jallred/Dev_Lab/HomeLabAI/docs/DIAGNOSTIC_SCRIPT_MAP.md), because future autonomous workers rely on the script map to execute tools without hallucinating CLI parameters.*

### Story 101.0B: Fortify `FeatureTracker.md` Feature Lineage & Code Mappings
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Status:** `COMPLETED`
* **Feature Anchor:** `[FEAT-659]` / `[BKM-082]`
* **Positive Context Guidance:**  
  *Update `FEAT-227` (spliced chunk uncoupling), `FEAT-407` (AST line link to L1077), `FEAT-557`, `FEAT-562`, `FEAT-160`, and register `FEAT-656`–`FEAT-659` in [`FeatureTracker.md`](file:///home/jallred/Dev_Lab/Portfolio_Dev/FeatureTracker.md), because the Feature Tracker is the primary DNA truth anchor used by CLaRa MCP tools during JITC lookups.*

### Story 101.0C: Correct `BOOTSTRAP_v4.5.md` Path & Port Navigation Table
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Status:** `COMPLETED`
* **Feature Anchor:** `[FEAT-659]` / `[BKM-001]`
* **Positive Context Guidance:**  
  *Roll `BOOTSTRAP_v4.4.md` to `BOOTSTRAP_v4.5.md` per archival protocol, because `OPENAGENT_HANDOVER_PLAYBOOK.md` resides in `Portfolio_Dev/docs/playbooks/` and port `:8000` serves Prometheus metrics rather than Foyer REST endpoints.*

### Story 101.0D: Fortify `LAB_INFRASTRUCTURE.md` Daemon Timeout & Nightly Map
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Status:** `COMPLETED`
* **Feature Anchor:** `[FEAT-659]` / `[LAB-112]`
* **Positive Context Guidance:**  
  *Update the Transport Layer and Nightly Service topology in [`LAB_INFRASTRUCTURE.md`](file:///home/jallred/Dev_Lab/HomeLabAI/docs/LAB_INFRASTRUCTURE.md), because port `:8000` is Prometheus hardware metrics and port `:8765` is the dual Foyer REST / WebSocket coordination plane.*

---

## 🧹 Phase 1: Pre-Ignition Hygiene & Mindful Cleanups

*Objective: Establish clean filesystem and process baselines before attempting daemon re-ignition or nightly script execution.*

### 🛡️ Story 101.1: Dead `vllm.pid` & Orphan Sentry Cleanup
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Feature Anchor:** `[FEAT-119]` / `[LAB-112]`
* **Positive Context Guidance:**  
  *Inspect `HomeLabAI/run/vllm.pid` and verify PID liveness using `kill -0 <pid>` before executing ignition or health probes, because an unlinked dead PID file tricks watchdogs into believing a zombie daemon is active when the port is closed.*
* **Task Breakdown:**
  1. Inspect `HomeLabAI/run/vllm.pid`. If process is dead, cleanly remove the file.
  2. Verify no orphan processes matching `vllm.entrypoints.openai.api_server` or `VLLM::EngineCore` occupy GPU memory.
  3. Ensure port 8088 is cleanly free (`ss -tulpn | grep 8088` returns empty).
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `HomeLabAI/run/vllm.pid`.
  * **Anchor 2 (Verification Command):** `test ! -f HomeLabAI/run/vllm.pid || kill -0 $(cat HomeLabAI/run/vllm.pid)`
  * **Anchor 3 (Live Silicon Invariant):** Zero stale PID lockfiles; port 8088 unencumbered.
  * **Anchor 4 (DNA Links):** `[FEAT-119]`, `[LAB-112]`.

---

### 🛡️ Story 101.2: Residual Dialogue Abort Event Clearing
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Feature Anchor:** `[FEAT-227]` / `[FEAT-407]`
* **Positive Context Guidance:**  
  *Explicitly clear and reset any residual `turn_aborted` flags or pending interruption events in [`cognitive_hub.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py) at the start of each new dispatch turn, because stale abort flags from previously interrupted runs cause subsequent conversational turns to silently abort before generating tokens.*
* **Task Breakdown:**
  1. In `HomeLabAI/src/logic/cognitive_hub.py`, locate turn initiation and ensure `turn_aborted.clear()` is called unconditionally on new input arrival.
  2. Verify in unit tests that an abort on turn $N$ does not leak into turn $N+1$.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `HomeLabAI/src/logic/cognitive_hub.py`.
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_cognitive_hub_unit.py -k test_abort_reset -v`
  * **Anchor 3 (Live Silicon Invariant):** Subsequent turns execute cleanly after an abort signal.
  * **Anchor 4 (DNA Links):** `[FEAT-227]`, `[FEAT-407]`.

---

### 🛡️ Story 101.3: Carry-Over Story 100.15 — Abolish Vestigial `internal=True` Censorship Masking
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Feature Anchor:** `[FEAT-361]` (Token Transparency Mandate)
* **Positive Context Guidance:**  
  *Abolish `stream_source = None` suppression in `nodes/loader.py#L210` and route intermediate/diagnostic tokens to dedicated stream channels (`crosstalk`, `insight`), because `FEAT-361` strictly forbids black-hole token silencing and mandates 100% telemetry visibility.*
* **Task Breakdown:**
  1. In `HomeLabAI/src/nodes/loader.py#L210`, replace `stream_source = self.name if not internal else None` with channel-tagged routing:
     `stream_source = self.name` and tag metadata with `is_internal=internal`.
  2. Verify that `self._broadcast_token` is never bypassed.
  3. Run existing unit test `test_visibility_truth.py`.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `HomeLabAI/src/nodes/loader.py`.
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_visibility_truth.py -v`
  * **Anchor 3 (Live Silicon Invariant):** 100% of tokens emitted by resident nodes are visible to the UI/websocket plane.
  * **Anchor 4 (DNA Links):** `[FEAT-361]`.

---

## ⚙️ Phase 2: Nightly Cascade & Watchdog Defenses

*Objective: Stabilize the 02:00 AM – 06:00 AM compute cycle, eliminate memory profiling races, and calibrate workloads to guaranteed SLA windows.*

### ⏱️ Story 101.4: Multi-Adapter LoRA Training Payload & Step Calibration
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Feature Anchor:** `[FEAT-160]` / `[FEAT-657]` / `[FEAT-416]` / `[LAB-103]` / `[LAB-107]`
* **Positive Context Guidance:**  
  *Maintain the mandatory 5.0s `HardwarePacingCallback` inter-step delay and micro-batching (`batch_size=1`, `grad_accum=4`) because `FEAT-160` and `SCAR-035` prove that host motherboard VRMs, PSU capacitors, and GDDR6 power rails require inter-step settling to eliminate electrical $di/dt$ power trips; calibrate `default_steps` down to 350 to achieve the desired ~155-minute training window and guarantee completion before 04:30 AM.*
* **Task Breakdown:**
  1. In `HomeLabAI/config/infrastructure.json#L105`, calibrate `forge.default_steps` from 450 to 350 (~22.2% reduction).
  2. Total 4-adapter training duration drops from 208 minutes down to ~155–160 minutes (~2.6 hours). Training finishes by ~04:35 AM, leaving a clean 25-minute buffer before the strict 05:00 AM cutoff (`[FEAT-416]`).
  3. Preserve all micro-batching parameters and `HardwarePacingCallback` (5.0s) per `FEAT-160` and `LAB-107`.
  4. Verify in `HomeLabAI/src/tests/test_nightly_lora_training.py` that step resolution cleanly loads 350 steps from `infrastructure.json`.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `HomeLabAI/config/infrastructure.json`, `HomeLabAI/src/infra/nightly_lora_training.py`, `HomeLabAI/src/tests/test_nightly_lora_training.py`.
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_nightly_lora_training.py -k test_step_resolution -v`
  * **Anchor 3 (Live Silicon Invariant):** 4-adapter training completes within $\le 165\text{ minutes}$, concluding before 04:45 AM.
  * **Anchor 4 (DNA Links):** `[FEAT-160]`, `[FEAT-657]`, `[FEAT-416]`, `[LAB-103]`, `[LAB-107]`, `[SCAR-035]`.

---

### 🛡️ Story 101.5: Morning Ignition 30-Minute Timeout & Hard-Kill Guardrail
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Feature Anchor:** `[FEAT-656]` / `[LAB-112]` / `[BKM-024]` / `[FEAT-119]`
* **Positive Context Guidance:**  
  *Expand the readiness probe loop to 360 iterations (30 minutes) and execute active process termination (`_kill_stale_vllm`) if port 8088 fails to bind, because `FEAT-119` (Parallel Assassin) requires ensuring that hung background subprocesses and dead port bindings are aggressively purged to prevent silent degradation into an `OFFLINE` standby trap.*
* **Task Breakdown:**
  1. In `HomeLabAI/src/v5/ignition/manager.py#L274`, change `range(60)` to `range(360)` (30 minutes at 5s polling intervals).
  2. Implement `_kill_stale_vllm(self)`:
     - Read PID from `HomeLabAI/run/vllm.pid` and execute `kill -9 <pid>`.
     - Execute `pkill -9 -f "vllm.entrypoints.openai.api_server"` and `pkill -9 -f "VLLM::EngineCore"`.
     - Remove `HomeLabAI/run/vllm.pid` and verify port 8088 is released.
  3. When `not api_ready` after 360 iterations, invoke `_kill_stale_vllm()`, release the VRAM mutex, transition state to `ERROR`, and emit a `CRITICAL` pager milestone.
  4. Add unit test `test_ignition_manager_kill_guardrail` in `HomeLabAI/src/tests/test_ignition_manager.py`.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `HomeLabAI/src/v5/ignition/manager.py`, `HomeLabAI/src/tests/test_ignition_manager.py`.
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_ignition_manager.py -k test_ignition_manager_kill_guardrail -v`
  * **Anchor 3 (Live Silicon Invariant):** Zero orphan/zombie vLLM processes remaining after timeout expiration; port 8088 released in $<3\text{s}$.
  * **Anchor 4 (DNA Links):** `[FEAT-656]`, `[LAB-112]`, `[FEAT-119]`, `[BKM-024]`.

---

### ⏱️ Story 101.6: Tail Mass Scan 05:00 AM Hard Cutoff Gate
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Feature Anchor:** `[FEAT-416]` (05:00 AM Quiet Hours Mandate)
* **Positive Context Guidance:**  
  *Enforce a strict 05:00 AM check within `field-notes-nibbler` and related note indexing sweeps because `FEAT-416` requires total system quiescence between 05:00 AM and 06:00 AM to give memory buffers time to drain before morning sentry audits.*
* **Task Breakdown:**
  1. In `Portfolio_Dev/field_notes/nibbler.py` (or note scanning sweep), add an explicit time gate checking current local hour.
  2. If local time reaches 05:00 AM, pause or yield execution cleanly, saving indexing checkpoints.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `Portfolio_Dev/field_notes/nibbler.py`.
  * **Anchor 2 (Verification Command):** Code inspection and unit test verifying 05:00 AM cutoff logic.
  * **Anchor 3 (Live Silicon Invariant):** Zero background disk scans or indexing activity active between 05:00 AM and 06:00 AM.
  * **Anchor 4 (DNA Links):** `[FEAT-416]`.

---

### 🛡️ Story 101.7: vLLM Re-Ignition Isolation & VRAM Profiling Settle Gate
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Feature Anchor:** `[FEAT-213]` / `[FEAT-658]` / `[FEAT-629]` / `[SCAR-036]`
* **Positive Context Guidance:**  
  *Enforce a 30s settling delay and block on polling `:8088/v1/models` until the engine is confirmed healthy and vocal before initiating Subconscious Dreaming, because vLLM's memory profiler requires exclusive GPU memory stability during its 17-second initialization to avoid `AssertionError` memory snapshot discrepancies.*
* **Task Breakdown:**
  1. In `HomeLabAI/src/infra/nightly_forge.py`, update `re_ignite_vllm()`:
     - Increase post-training thermal cooldown from 15s to 30s.
     - Call `torch.cuda.empty_cache()` and `gc.collect()` to ensure full VRAM quiescence.
     - Issue `POST /wake` and `POST /status_update {"state": "OPERATIONAL"}` to Foyer.
     - **Add a blocking probe gate**: Poll `http://127.0.0.1:8088/v1/models` for up to 180 seconds until the local unified base responds with 200 OK.
     - Only once vLLM is confirmed UP on port 8088 does `re_ignite_vllm()` return `True`, unblocking Step 5 (Subconscious Dreaming).
  2. Add unit test `test_re_ignite_vllm_blocking_gate` in `HomeLabAI/src/tests/test_nightly_forge.py`.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `HomeLabAI/src/infra/nightly_forge.py`, `HomeLabAI/src/tests/test_nightly_forge.py`.
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_nightly_forge.py -k test_re_ignite_vllm -v`
  * **Anchor 3 (Live Silicon Invariant):** Zero concurrent memory churn during vLLM initialization; vLLM memory profiling passes without `AssertionError`.
  * **Anchor 4 (DNA Links):** `[FEAT-213]`, `[FEAT-658]`, `[FEAT-629]`, `[SCAR-036]`.

---

### 🧬 Story 101.8: Dedicated Sprint DNA Curator Engine Reconnection
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Feature Anchor:** `[FEAT-557]` / `[BKM-060]`
* **Positive Context Guidance:**  
  *Directly invoke `HomeLabAI/src/curator/sync_sprint_dna.py` because `FEAT-557` established it as the dedicated curator for `sprint_dna` with Level 1/2 chunking, recency curves, and `sprint_data.json` compilation, while `sync_chroma_dna.py` is reserved exclusively for static DNA files.*
* **Task Breakdown:**
  1. In `HomeLabAI/src/infra/nightly_forge.py#run_sprint_dna_sync()`, update the script target:
     - Point to `HomeLabAI/src/curator/sync_sprint_dna.py`.
     - Remove unsupported `--collection sprint_dna` argument (the script targets `sprint_dna` by default).
  2. Verify that running `python3 HomeLabAI/src/curator/sync_sprint_dna.py --dry-run` executes cleanly and exits code 0.
  3. Add test assertion in `test_nightly_forge.py`.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `HomeLabAI/src/infra/nightly_forge.py`, `HomeLabAI/src/curator/sync_sprint_dna.py`.
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/python3 HomeLabAI/src/curator/sync_sprint_dna.py --dry-run` (Assert exit 0).
  * **Anchor 3 (Live Silicon Invariant):** `sprint_dna` collection and `sprint_data.json` updated with 0 argument errors.
  * **Anchor 4 (DNA Links):** `[FEAT-557]`, `[BKM-060]`.

---

### 📚 Story 101.9: Canonical Wisdom DNA Path Resolution in Refiner
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Feature Anchor:** `[FEAT-562]` / `[FEAT-558]` / `[FEAT-637]`
* **Positive Context Guidance:**  
  *Target canonical `Portfolio_Dev/dna/wisdom_data.json` because `FEAT-637` (Single-Home Runtime Data Law) mandates a single canonical home in `dna/` to prevent split-brain state drift across submodules.*
* **Task Breakdown:**
  1. In `Portfolio_Dev/field_notes/refine_wisdom.py`, update `WISDOM_DATA_PATH` resolution:
     - First check `Portfolio_Dev/dna/wisdom_data.json` (the canonical DNA home per Sprint 97 Single-Home Law `[FEAT-637]`).
     - Fallback to `DATA_DIR / "wisdom_data.json"` if present.
  2. Verify `python3 Portfolio_Dev/field_notes/refine_wisdom.py --dry-run` executes cleanly, loads cards from ChromaDB and `dna/wisdom_data.json`, and exits 0.
  3. Ensure no duplicate copies of `wisdom_data.json` are created in `field_notes/data/`.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `Portfolio_Dev/field_notes/refine_wisdom.py`, `Portfolio_Dev/dna/wisdom_data.json`.
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/python3 /home/jallred/Dev_Lab/Portfolio_Dev/field_notes/refine_wisdom.py --dry-run` (Assert exit 0).
  * **Anchor 3 (Live Silicon Invariant):** Zero duplicate `wisdom_data.json` files; single canonical home in `dna/`.
  * **Anchor 4 (DNA Links):** `[FEAT-562]`, `[FEAT-558]`, `[FEAT-637]`.

---

### ⏱️ Story 101.10: Round Table Accountability Probe Timeout Alignment
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Feature Anchor:** `[FEAT-608]` / `[FEAT-651]` / `[BKM-062]`
* **Positive Context Guidance:**  
  *Configure the subprocess timeout to 120s because `probe_round_table_accountability.py`'s internal deliberation circuit requires up to 75s to complete genuine multi-stage deliberation across Triage, Pinky, Brain, M5 Air, and Pinky Critic.*
* **Task Breakdown:**
  1. In `HomeLabAI/src/infra/nightly_forge.py#run_round_table_probe()`, increase the subprocess `timeout` parameter from 60 to 120 seconds.
  2. Provides adequate buffer for the probe's 75s deliberation deadline plus greeting check and socket connections.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `HomeLabAI/src/infra/nightly_forge.py`.
  * **Anchor 2 (Verification Command):** Code inspection and unit test verifying `timeout=120`.
  * **Anchor 3 (Live Silicon Invariant):** Deliberation probe given full 75s runway without outer wrapper clipping.
  * **Anchor 4 (DNA Links):** `[FEAT-608]`, `[FEAT-651]`, `[BKM-062]`.

---

### 📊 Story 101.11: Cgroup Swap Peak & Memory Pressure Telemetry Sentinel
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Feature Anchor:** `[LAB-110]` / `[FEAT-619]` / `[BKM-066]`
* **Positive Context Guidance:**  
  *Read `/sys/fs/cgroup/memory.swap.peak` (or `memory.swap.current`) within `standalone_accountability_watchdog.py` and record it into `daily_accountability_digest.json`, because swap thrashing during overnight training is a primary root cause of morning ignition latency and must be tracked empirically.*
* **Task Breakdown:**
  1. In `HomeLabAI/src/infra/standalone_accountability_watchdog.py`, add vector reading cgroup swap metrics (`memory.swap.peak` / `memory.swap.current` or `/proc/meminfo` SwapTotal/SwapFree).
  2. Emit `swap_peak_mb` and `swap_utilization_pct` in `daily_accountability_digest.json`.
  3. Flag a `WARNING` if peak swap exceeds 80% during the overnight cycle.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `HomeLabAI/src/infra/standalone_accountability_watchdog.py`.
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_standalone_accountability_watchdog.py -k test_swap_telemetry -v`
  * **Anchor 3 (Live Silicon Invariant):** `swap_peak_mb` populated in `daily_accountability_digest.json`.
  * **Anchor 4 (DNA Links):** `[LAB-110]`, `[FEAT-619]`, `[BKM-066]`.

---

## 🧪 Phase 3: Live Silicon Certification & Verification

*Objective: Certify 100% operational health across all reachable endpoints and achieve 7/7 green marks on the physical watchdog digest.*

### 🏥 Story 101.12: Physical Lab Live Recovery & 7/7 Accountability Certification
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Feature Anchor:** `[BKM-024]` / `[BKM-066]` / `[FEAT-619]`
* **Positive Context Guidance:**  
  *Verify against the running live daemons (`:8088`, `:8765`) and certify 7/7 checks green via `standalone_accountability_watchdog.py` because `BKM-024` mandates that final certification requires matching Git HEAD on active silicon.*
* **Task Breakdown:**
  1. Verify clean daemon startup via Foyer `/wake` or `start_vllm.sh`.
  2. Verify port 8088 responds with `{"object": "list"}` on `/v1/models` and confirms all 4 LoRA adapters loaded.
  3. Verify Foyer port 8765 reports `"state": "OPERATIONAL"` and `"engine_up": true`.
  4. Run `standalone_accountability_watchdog.py` and certify 7/7 checks pass green (`overall_status: PASS`, 0 discrepancies).
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `Portfolio_Dev/field_notes/data/status.json`, `Portfolio_Dev/field_notes/data/daily_accountability_digest.json`.
  * **Anchor 2 (Verification Command & Literal Test Battery):**  
    `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/python3 HomeLabAI/src/infra/standalone_accountability_watchdog.py`
  * **Anchor 3 (Live Silicon Invariant):** 7/7 checks green in `daily_accountability_digest.json`; Foyer `OPERATIONAL`; vLLM `UP`.
  * **Anchor 4 (DNA Links):** `[BKM-024]`, `[BKM-066]`, `[FEAT-619]`.

---

## 🚫 Pre-Flight Mistake Ledger (Mistakes Avoided by Grounding)

1. **Mistake Avoided: Adding `--collection` to `sync_chroma_dna.py`**  
   * *What would have happened:* Attempting to patch `Portfolio_Dev/sync_chroma_dna.py` to add `--collection sprint_dna`.  
   * *Why it's wrong:* Grounding in Sprint 76.3 (`FEAT-557`) and `FeatureTracker.md` revealed that `HomeLabAI/src/curator/sync_sprint_dna.py` is the dedicated, purpose-built curator for sprint documentation (with Level 1/Level 2 chunking and recency curves). `sync_chroma_dna.py` is for core DNA files only. Modifying `sync_chroma_dna.py` would have corrupted its single responsibility and left `sync_sprint_dna.py` orphaned.
2. **Mistake Avoided: Duplicating `wisdom_data.json` into `field_notes/data/`**  
   * *What would have happened:* Copying `Portfolio_Dev/dna/wisdom_data.json` to `Portfolio_Dev/field_notes/data/wisdom_data.json` to silence the file-not-found error.  
   * *Why it's wrong:* Violates the **Single-Home Runtime Data Law (`[FEAT-637]`)** established in Sprint 97.1. Duplicating files across directories causes split-brain edits and stale state drift. The correct fix is teaching `refine_wisdom.py` to read from the canonical `dna/` directory.
3. **Mistake Avoided: Disabling or Reducing the Hardware Pacing Delay in `train_expert.py`**  
   * *What would have happened:* Reducing or removing the 5.0-second delay between training steps to make LoRA training run faster.  
   * *Why it's wrong:* Grounding in `[FEAT-160]` and `[SCAR-035]` proved that the 5.0s delay with `torch.cuda.empty_cache()` is an invariant physical law required to prevent thermal exhaustion and electrical di/dt power trips on the 11-year-old Z87 motherboard power rails. Pacing must be preserved; the step budget is what must be calibrated.
4. **Mistake Avoided: Assuming vLLM Failed from Out-Of-Memory (OOM)**  
   * *What would have happened:* Assuming the 2080 Ti ran out of VRAM and modifying GPU memory utilization fractions.  
   * *Why it's wrong:* Log horizon inspection proved that VRAM utilization was low (7.57 GiB free). The crash was an assertion failure in `gpu_worker.py:434` triggered because Subconscious Dreaming was executing concurrently and released 100 MB of VRAM during vLLM's memory profiling. Serializing re-ignition completely resolves the race.
5. **Mistake Avoided: Modifying Critic Prompts for Round Table Failure**  
   * *What would have happened:* Tuning prompts or personas in `pinky_critic_persona.py`.  
   * *Why it's wrong:* The probe failed simply because the outer subprocess timeout in `nightly_forge.py` was 60 seconds, which abruptly killed the probe before its internal 75-second multi-stage deliberation timeout could finish.
6. **Mistake Avoided: Blindly Committing Code Without Process Quiescence**  
   * *What would have happened:* Attempting to run unit tests while background subagents or zombie vLLM PIDs linger.  
   * *Why it's wrong:* Residual process table entries can cause port collisions and memory leaks during pytest runs. Pre-ignition hygiene (Stories 101.1–101.3) ensures total quiescence before testing.

---

## 🧭 Grounding Gap Audit

- **Audit Result:** **100% Grounded.**
- Every single story in Sprint 101.0 is tied to specific historical sprints, existing DNA features (`FEAT-119`, `FEAT-160`, `FEAT-213`, `FEAT-227`, `FEAT-361`, `FEAT-407`, `FEAT-416`, `FEAT-557`, `FEAT-562`, `FEAT-608`, `FEAT-619`, `FEAT-629`, `FEAT-656`), physical hardware scars (`SCAR-035`, `SCAR-036`), and verified codebase paths.
- **Zero ungrounded items remain.**
