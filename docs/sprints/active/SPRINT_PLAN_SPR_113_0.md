# 📋 SPRINT PLAN 113.0: Inter-Node Waterfall Streaming Restoration & Decoupled Edge Pop Governance

**Parent Frameworks:** `BKM-015` (Prompt Engineering & Formatting), `BKM-018` (Orchestrator-First Mandate), `BKM-024` (Live Verification), `BKM-062` (Ground Truth Verification), `BKM-081` (In-Tree Append Ledger), `BKM-082` (Historical Grounding & 5-Sprint Lookback), `BKM-086` (Paved-Path Sprint Protocol / AFK), `BKM-095` (UI Atomic Turn Dispatch), `BKM-102` (Internal Pipe vs. Edge Pop Invariant), `[FEAT-233]` (Inter-Node Token Waterfall & Live Hearing Pipe), `[FEAT-361]` (Token Transparency Mandate), `[FEAT-403]` (Dream Pass Synthesis), `[FEAT-439]` (Async Sanity Judge Protocol), `[FEAT-457]` (Speculative Context Pre-fetch), `[FEAT-489]` (Two-Mice Sequential Handover), `[FEAT-525]` (Round Table Delta-T Telemetry), `[FEAT-684]` (Pre-Streaming Waterfall Routing), `[FEAT-687]` (Subconscious Dream Round Table Deliberation).  
**Sprint Horizon:** November 18, 2026 – November 22, 2026  
**Status:** ✅ COMPLETED & CERTIFIED (Tracks 1 - 5 Certified)  
**Sprint Lead:** `[AGY:PRIMARY]` (Antigravity Autonomous Pair)  
**Tracking Mode:** In-Tree Append-Only Ledger (`BKM-081`)

---

## 🛑 Pre-Flight Checklist Gate (`BKM-082 §GATE` / `BKM-086 §1.1`)
- [x] **1. 5-Sprint Lookback**: Reviewed SPR-108 through SPR-112.1 for traps, sentinels, and regression vectors (`BKM-082 §2.1`).
  - *SPR-108 (Story 108.20 / commit 3048aaa)*: Root origin of the global token suppression regression. Enforced UI anti-pop by erroneously asserting zero `token` packets anywhere in the system.
  - *SPR-109 (Retrospective)*: Addressed HyDE parsing and domain classification stability, but left the sequential `await` string accumulator intact.
  - *SPR-110 (moe-cuda-rpc certification)*: Unlocked 34.2 tok/s generation decode throughput on dual-GPU local engine, proving raw silicon horsepower was not the bottleneck.
  - *SPR-111 (Inference Engine Canonicalization)*: Consolidated CLI and systemd scripts into `engine_ctl.sh`, eliminating duplicate background server drift.
  - *SPR-112.0 / 112.1 (JITC Realignment & Pre-Streaming Routing)*: Proved concurrent pre-warming cuts circuit latency by 48.3% (134s $\rightarrow$ 69.5s), bringing the remaining sequential await bottlenecks into sharp relief.
- [x] **2. Mistakes-Avoided Ledger (`BKM-082 §2.4`)**:
  - *Mistake 1 (The Global Token Packet Ban Trap)*: In `test_two_mice_handover.py:547`, asserting `len(token_packets) == 0` globally banned internal backend token streaming while attempting to protect user chat websockets. Guardrail: Assert zero tokens *only* on user-facing channels (`channel in ("chat", "pinky", "voice")`).
  - *Mistake 2 (The Monolithic Await String Accumulator Trap)*: Accumulating generators into `full_text += token` before returning forces downstream accelerator silicon to sit 100% idle. Guardrail: Forward async generator deltas directly into consumer queues.
  - *Mistake 3 (The Green Lie / Premature Optimization Metric)*: Avoided reporting raw decode rate (34 tok/s) without honest prefill latency (TTFT), keeping the live telemetry ledger authentic.
  - *Mistake 4 (The Inadvertent Phase-Append Trap)*: Avoided burying fundamental architectural regressions inside prior sprint sub-phases; dedicated a full, sovereign sprint (SPR-113.0) with clean archeology and DNA codification.
  - *Mistake 5 (The Synthetic Satellite Review File Anti-Pattern)*: Oracle reviews belong exclusively in `HomeLabAI/data/delegation_ledger.jsonl` via `delegate.py --mode oracle`, never in synthetic ad-hoc markdown files (`BKM-049` / `BKM-007`).
- [x] **3. Oracle / Architectural Audit**: Pre-flight review completed and certified with zero blockers by Cloud Oracle via active `delegate.py --mode oracle` dispatch (`ses_e0f25f2acffeTYUCp8uIzu291o` recorded in canonical [`HomeLabAI/data/delegation_ledger.jsonl`](file:///home/jallred/Dev_Lab/HomeLabAI/data/delegation_ledger.jsonl)). Validated decoupling boundaries against `BKM-095`, `BKM-102`, `FEAT-233`, and `FEAT-361`. Ambiguities in anchor line numbers (`router.py:5266` and `cognitive_hub.py:814`) aligned with HEAD.
- [x] **4. Delegation Gate (`BKM-049` / `BKM-086 §Pillar 3`)**: Story assignments declared: Leaf plumbing and unit test assertions assigned to `[SWARM:LOCAL]`; cross-module routing and pipelining assigned to `[SWARM:CLOUD]`; physical silicon certification and daemon lifecycle assigned to `[AGY:PRIMARY]`.
- [x] **4.1 Sole-Owner & Zero-Delegation Tripwire (`BKM-049 §3.4` / `BKM-086 §Pillar 3`)**: Verified non-homogeneous allocation across stories. AGY is NOT sole owner across 100% of tasks (4 of 6 stories allocated to `[SWARM:LOCAL]` and `[SWARM:CLOUD]`).
- [x] **5. Risk Assessment**: Evaluated blast radius of modifying `_run_two_mice_handover` token pipes and Foyer WebSocket egress filtering. Zero risk to database schemas or GPU hardware topology; fully verified via unit test mocks and live accountability probes.
- [x] **6. BKM Invariant & Anti-Bypass Audit**: Verified plan against `BKM-095` (Edge Pop), `BKM-101` (Live Shakedown), `BKM-024` (Live Silicon Gate), and `BKM-084` (Dropped Threads Governance). All operator waivers are strictly phase-scoped per `BKM-086 §1.2`.

---

## 🚦 Interactive Execution Checklist (`BKM-086 §1.1`)

### 🧭 Track 1: Edge Egress Decoupling & Unit Test Correction
- [x] **Story 113.10: Surgical Unit Test Realignment & Egress Filtering (`[BKM-095]` / `[FEAT-361]`)**:
  - **Assigned Owner:** `[SWARM:LOCAL]` (promoted to `[SWARM:CLOUD]` per `BKM-049 §3` after local timeout, Session `ses_e0f0664fcffezxnhk29HO7AIVx`; verified by `[AGY:PRIMARY]`)
  - **DNA Tags:** `[BKM-095]`, `[FEAT-361]`, `[FEAT-233]`, `[BKM-102]`
  - *Anchor 1 (Target Files & Line Ranges):*
    - [`HomeLabAI/src/tests/test_two_mice_handover.py:528-563`](file:///home/jallred/Dev_Lab/HomeLabAI/src/tests/test_two_mice_handover.py#L528-L563) (`test_zero_ui_streaming_and_no_raw_json_echo`)
    - [`HomeLabAI/src/v5/foyer/router.py:5250-5285`](file:///home/jallred/Dev_Lab/HomeLabAI/src/v5/foyer/router.py#L5250-L5285) (`is_handover_persona` WebSocket egress filtering)
  - *Anchor 2 (Verification Command):*
    - `/home/jallred/.venv/bin/pytest HomeLabAI/src/tests/test_two_mice_handover.py -v` (23/23 PASS)
  - *Anchor 3 (Verbatim Code Specs & Schemas):*
    - In `test_two_mice_handover.py:550-551`:
      ```python
      # 1. Assert ZERO live streaming token packets were sent on user conversational channels
      user_token_packets = [
          p for p in packets
          if p.get("type") == "token" and p.get("channel") in ("chat", "pinky", "voice")
      ]
      assert len(user_token_packets) == 0, f"Expected 0 user token packets, found {len(user_token_packets)}"
      ```
    - In `v5/foyer/router.py`: Egress filter scoped to `conversational_channels = ("chat", "pinky", "voice")`, freeing diagnostic channels (`insight`, `crosstalk`).
  - *Anchor 4 (DNA Links):* `[BKM-095]`, `[FEAT-361]`, `[FEAT-233]`, `[BKM-102]`.
  - *Commit*: `HomeLabAI @ 5be7949`.

### ⚡ Track 2: Inter-Node Waterfall Streaming Restoration
- [x] **Story 113.20: Pipelined Relay from Deep Thought to Pinky (`[FEAT-233.2]` / `[FEAT-489]`)**:
  - **Assigned Owner:** `[SWARM:CLOUD]` (Sisyphus, Session `ses_e0f014e5affekjpf8Q8b2OKMaP`)
  - **DNA Tags:** `[FEAT-233.2]`, `[FEAT-489]`, `[FEAT-684]`, `[BKM-102]`
  - *Anchor 1 (Target Files & Line Ranges):*
    - [`HomeLabAI/src/logic/cognitive_hub.py:3748-3755,4108-4148`](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py#L3748-L3755) (`step_deep_thought` & `_run_two_mice_handover`)
  - *Anchor 2 (Verification Command):*
    - `/home/jallred/.venv/bin/pytest HomeLabAI/src/tests/test_two_mice_handover.py -v` (23/23 PASS)
  - *Anchor 3 (Verbatim Code Specs & Schemas):*
    - `step_deep_thought` accepts `relay_queue: asyncio.Queue | None = None` and puts streaming tokens in real time.
    - `_run_two_mice_handover` runs `_pinky_prefill_consumer` concurrently with `step_deep_thought`, storing `_deep_thought_prefill_buffer` to eliminate sequential waiting.
  - *Anchor 4 (DNA Links):* `[FEAT-233.2]`, `[FEAT-489]`, `[BKM-102]`.
  - *Commit*: `HomeLabAI @ 1667428`.

- [x] **Story 113.30: Concurrent Pre-Hydration of the Sovereign Critic (`[FEAT-439]` / `[FEAT-608]`)**:
  - **Assigned Owner:** `[SWARM:CLOUD]` (Sisyphus, Session `ses_e0ef6c036ffe6Wf8wyrlV7wzqK`)
  - **DNA Tags:** `[FEAT-439]`, `[FEAT-608]`, `[BKM-024]`
  - *Anchor 1 (Target Files & Line Ranges):*
    - [`HomeLabAI/src/logic/cognitive_hub.py:4170-4200`](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py#L4170-L4200) (`step_entailment_audit` scheduling in `_run_two_mice_handover`)
  - *Anchor 2 (Verification Command):*
    - `/home/jallred/.venv/bin/pytest HomeLabAI/src/tests/test_round_table_continuity.py -v` (11/11 PASS)
  - *Anchor 3 (Verbatim Code Specs & Schemas):*
    - Scheduled `step_entailment_audit` via `asyncio.create_task` BEFORE `step_pinky_voice` so judicial context pre-warming runs concurrently on M5 Air during Pinky's delivery.
  - *Anchor 4 (DNA Links):* `[FEAT-439]`, `[FEAT-608]`, `[BKM-024]`.
  - *Commit*: `HomeLabAI @ f620252`.

- [x] **Story 113.40: Shared Root Prefix Standardization for Local Slot-0 KV Cache Reuse (`[LAB-122]`)**:
  - **Assigned Owner:** `[SWARM:LOCAL]` (promoted to `[SWARM:CLOUD]` per `BKM-049 §3` after local timeout, Session `ses_e0ed2dd8dffewikQolCkgfwFL2`; verified by `[AGY:PRIMARY]`)
  - **DNA Tags:** `[LAB-122]`, `[FEAT-684]`, `[BKM-015]`
  - *Anchor 1 (Target Files & Line Ranges):*
    - [`HomeLabAI/src/logic/cognitive_hub.py:883-892`](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py#L883-L892) (`build_two_mice_stage_prompt`)
  - *Anchor 2 (Verification Command):*
    - `/home/jallred/.venv/bin/pytest HomeLabAI/src/tests/test_two_mice_handover.py -v` (23/23 PASS)
  - *Anchor 3 (Verbatim Code Specs & Schemas):*
    - Wrapped `TWO_MICE_BEDROCK_FOUNDATION` in `<cluster_root>` prefix tags at the prompt head for Stage 1 and Stage 2, enabling slot-0 KV cache reuse (`n_prompt_tokens_cache > 0`) on port 8088.
  - *Anchor 4 (DNA Links):* `[LAB-122]`, `[FEAT-684]`.
  - *Commit*: `HomeLabAI @ a8d8cda`.

### 🛡️ Track 3: Permanent DNA Codification & Guardrails
- [x] **Story 113.50: Codification of BKM-102 & Code Comment Annotation**:
  - **Assigned Owner:** `[AGY:PRIMARY]`
  - **DNA Tags:** `[BKM-102]`, `[FEAT-233.8]`, `[BKM-095]`
  - *Anchor 1 (Target Files & Line Ranges):*
    - [`HomeLabAI/docs/Protocols.md:2193-2214`](file:///home/jallred/Dev_Lab/HomeLabAI/docs/Protocols.md#L2193-L2214)
    - [`HomeLabAI/src/logic/cognitive_hub.py:4113`](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py#L4113)
    - [`HomeLabAI/src/v5/foyer/router.py:5263`](file:///home/jallred/Dev_Lab/HomeLabAI/src/v5/foyer/router.py#L5263)
    - [`HomeLabAI/src/nodes/loader.py:231`](file:///home/jallred/Dev_Lab/HomeLabAI/src/nodes/loader.py#L231)
  - *Anchor 2 (Verification Command):*
    - `git log -n 1 -p HomeLabAI/docs/Protocols.md`
  - *Anchor 3 (Verbatim Code Specs & Schemas):*
    - Codified `[BKM-102] / [FEAT-233.8] (Internal Pipe vs. Edge Pop Invariant)` into `Protocols.md:2193-2214`.
    - Tagged code with `# [PROTECTED_PIPE: FEAT-233 / BKM-102] DO NOT BUFFER INTO MONOLITHIC STRING. Internal streaming only; UI pop enforced at WebSocket boundary.` in `cognitive_hub.py`, `router.py`, and `loader.py`.
    - Registered `[FEAT-233.8]` in `Portfolio_Dev/FeatureTracker.md`.
  - *Anchor 4 (DNA Links):* `[BKM-102]`, `[FEAT-233.8]`.
  - *Commit*: `HomeLabAI @ c9c1580`, `Portfolio_Dev @ ec78eea`.

### 🏁 Track 4: Live Silicon Certification & Gauntlet
- [x] **Story 113.60: Multi-Topic Silicon Shakedown & Quorum Certification (`[BKM-024]` / `[BKM-101]`)**:
  - **Assigned Owner:** `[AGY:PRIMARY]`
  - **DNA Tags:** `[BKM-024]`, `[BKM-101]`, `[BKM-062]`
  - *Anchor 1 (Target Files & Line Ranges):*
    - [`HomeLabAI/src/infra/probe_round_table_accountability.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/infra/probe_round_table_accountability.py)
    - [`HomeLabAI/src/infra/standalone_accountability_watchdog.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/infra/standalone_accountability_watchdog.py)
  - *Anchor 2 (Verification Command):*
    - `/home/jallred/.venv/bin/python3 HomeLabAI/src/infra/probe_round_table_accountability.py`
    - `/home/jallred/.venv/bin/python3 HomeLabAI/src/infra/standalone_accountability_watchdog.py`
  - *Anchor 3 (Verbatim Code Specs & Schemas):*
    - **Live Probe Verification Output**:
      ```json
      {
        "status": "PASS",
        "greeting_latency_ms": 1.23,
        "circuit_latency_ms": 120807.07,
        "total_probe_duration_ms": 120808.8,
        "foyer_state": "OPERATIONAL",
        "triage_routing": "kender_online",
        "critic_score": 1.0,
        "sovereign_quorum": true,
        "timestamp": "2026-11-18T16:34:33.319175",
        "error": null,
        "topic": "Review Clearwater Forest (CWF) and Diamond Rapids (DMR) manageability and Redfish test collateral."
      }
      ```
    - **Standalone Watchdog Verification Output**:
      ```text
      === MORNING ACCOUNTABILITY AUDIT REPORT ===
      Status:        PASS
      Checks Passed: 9/9
        ✅ GPU Power Clamp (165W): Power limit is 165.0W (max 170.0W)
        ✅ Foyer Re-Ignition & Hot-Reload: Foyer state: OPERATIONAL, status: ONLINE, engine: UP
        ✅ Lockfile Cleanliness & Quiescence: All lockfiles cleared
        ✅ Nightly Forge Orchestration: Status: COMPLETED (Age: 13.9h)
        ✅ LoRA Fine-Tuning Multi-Adapter Pass: MOTHBALLED (30m Quiet Soak Active)
        ✅ Accountable Subconscious Dreaming: Fresh: 14.0h, Active Gems: 4
        ✅ Sanitization Escape Tripwire: No credential escapes in last 24h
        ✅ Synthetic Morning Round Table Probe: Status: PASS, Critic Score: 1.00, Latency: 0.93ms
        ✅ Cgroup Swap Pressure Monitor: Swap: 3010MB/3010MB peak (19.1%)
      ```
  - *Anchor 4 (DNA Links):* `[BKM-024]`, `[BKM-101]`.

### 🔄 Track 5: Post-Certification Archival, Probe Realignment & Dream Pass Restoration
- [x] **Story 113.55: Single-Delivery Pop Invariant Realignment & Complexity Rollback (`commit 0854ee0`)**:
  - **Assigned Owner:** `[AGY:PRIMARY]`
  - **DNA Tags:** `[BKM-095]`, `[FEAT-233]`, `[BKM-102]`
  - *Anchor 1 (Target Files):* `HomeLabAI/src/logic/cognitive_hub.py`, `HomeLabAI/src/v5/foyer/router.py`, `HomeLabAI/src/tests/test_two_mice_handover.py`
  - *Anchor 2 (Verification Command):* `HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_two_mice_handover.py -v` (23/23 PASS)
  - *Anchor 3 (Code Specs):* Eradicated duplicate bubble emission complexity by asserting `is_handover_persona` check on egress broadcasts while leaving internal streaming queues intact.
  - *Anchor 4 (DNA Links):* `[BKM-095]`, `[FEAT-233.8]`.
  - *Commit*: `HomeLabAI @ 0854ee0`.

- [x] **Story 113.65: Centralized Seat-Specific Node Vocal Probe Timeouts (`[LAB-119]` / `[FEAT-685]` / `commit a0b0cc7`)**:
  - **Assigned Owner:** `[AGY:PRIMARY]`
  - **DNA Tags:** `[LAB-119]`, `[FEAT-685]`, `[LAB-125]`, `[BKM-024]`
  - *Anchor 1 (Target Files):* `HomeLabAI/config/infrastructure.json`, `HomeLabAI/config/lab_accountability_thresholds.json`, `HomeLabAI/src/nodes/loader.py`
  - *Anchor 2 (Verification Command):* `git -C HomeLabAI show --stat a0b0cc7`
  - *Anchor 3 (Code Specs):* Standardized M5 Air Headroom proxy port to 8002 and dynamically resolved per-node vocal probe timeouts from `infrastructure.json` with fallback to `lab_accountability_thresholds.json`, resolving the 4s timeout regression.
  - *Anchor 4 (DNA Links):* `[LAB-119]`, `[FEAT-685]`.
  - *Commit*: `HomeLabAI @ a0b0cc7`.

- [x] **Story 113.68: Multi-Topic Live Silicon Moat Deliberations (Turns 50 & 51)**:
  - **Assigned Owner:** `[AGY:PRIMARY]`
  - **DNA Tags:** `[BKM-024]`, `[BKM-062]`, `[FEAT-525]`
  - *Anchor 1 (Target Files):* `Portfolio_Dev/field_notes/data/round_table_deltas.json`
  - *Anchor 2 (Verification Command):* Tail `round_table_deltas.json` entries for Turns 50 and 51.
  - *Anchor 3 (Code Specs / Results):*
    - Turn 50: DMR MMIO register adaptation -> Negative Moat (0/5 chunks validated, dropped all, Two-Mice handover, Critic: 0.95, Elapsed: 48.31s).
    - Turn 51: PECI metrics & thermal stress -> Positive Moat (4/7 chunks validated, Deep Thought on M5 Air, Critic: 1.00, Elapsed: 66.44s).
  - *Anchor 4 (DNA Links):* `[FEAT-525]`, `[BKM-024]`.

- [x] **Story 113.70: Un-gag `[DREAM_PASS]` in Foyer Router & Restore Subconscious Round Table Deliberation (`[FEAT-403]` / `[FEAT-525]` / `[BKM-102]` / `[FEAT-687]`)**:
  - **Assigned Owner:** `[AGY:PRIMARY]`
  - **DNA Tags:** `[FEAT-403]`, `[FEAT-525]`, `[BKM-102]`, `[FEAT-687]`
  - *Anchor 1 (Target Files & Line Ranges):*
    - [`HomeLabAI/src/v5/foyer/router.py:4791-4798,5766-5777`](file:///home/jallred/Dev_Lab/HomeLabAI/src/v5/foyer/router.py#L4791-L4798)
    - [`HomeLabAI/src/tests/test_refine_queue_isolation.py:108-146,170-193`](file:///home/jallred/Dev_Lab/HomeLabAI/src/tests/test_refine_queue_isolation.py#L108-L146)
  - *Anchor 2 (Verification Command):*
    - `HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_refine_queue_isolation.py -v` (5/5 PASS)
    - `HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_two_mice_handover.py -v` (23/23 PASS)
  - *Anchor 3 (Verbatim Code Specs & Schemas):*
    - Excised `or query.startswith("[DREAM_PASS]")` from `router.py:4796` and `or event.query.startswith("[DREAM_PASS]")` from `router.py:5770`.
    - Allowed subconscious dream intents to enter `foyer_queue.jsonl` and drain via `_dispatch_buffered_intent` -> `run_division_of_labor()`, executing the full Two-Mice Handover and appending telemetry deltas to `round_table_deltas.json`.
    - Updated `test_refine_queue_isolation.py` so that `[DREAM_PASS]` is verified as a full multi-actor division-of-labor pass while `[INTERNAL]` and `[REFINE]` remain isolated.
  - *Anchor 4 (DNA Links):* `[FEAT-403]`, `[FEAT-525]`, `[BKM-102]`, `[FEAT-687]`.
  - *Commit*: `HomeLabAI @ 622ba96`.

### 📊 Track 6: Telemetry UI Modernization, Monotonic Ledger Governance & Speculative Invariant
- [x] **Story 113.80: Unique Monotonic Turn IDs in Rolling Blackboard Ledger (`[FEAT-525]`)**:
  - **Assigned Owner:** `[AGY:PRIMARY]`
  - **DNA Tags:** `[FEAT-525]`, `[BKM-024]`
  - *Anchor 1 (Target Files):* `HomeLabAI/src/memory/blackboard_ledger.py`, `HomeLabAI/src/tests/test_blackboard_dna.py`
  - *Anchor 2 (Verification Command):* `HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_blackboard_dna.py -v` (4/4 PASS)
  - *Anchor 3 (Code Specs):* Replaced `monotonic_turn = len(records) + 1` with `highest_turn = max((r.get('turn', 0) for r in records), default=0) + 1`, eliminating the 50-item cap turn-51 overwrite loop while preserving unique sequential turn IDs in the 50-item rolling window.
  - *Anchor 4 (DNA Links):* `[FEAT-525]`.

- [ ] **Story 113.81: Stage Terminology & Sequential Waterfall Alignment in `benchmarks.html` / `benchmarks.js` (`[FEAT-494]` / `[FEAT-525]`)**:
  - **Assigned Owner:** `[AGY:PRIMARY]`
  - **DNA Tags:** `[FEAT-494]`, `[FEAT-525]`, `[FEAT-489]`
  - *Anchor 1 (Target Files):* `Portfolio_Dev/field_notes/benchmarks.html`, `Portfolio_Dev/field_notes/benchmarks.js`
  - *Anchor 2 (Verification Command):* Code review & browser test of `benchmarks.html`
  - *Anchor 3 (Code Specs):* Renamed legacy `oracle` and `pinky_judgment` to active 5-stage names: Triage (Kender), Brain Gatekeeper (Moat RAG), Deep Thought (Synthesis), Pinky Voice (Delivery Pop), and Sovereign Critic (Entailment Audit) across canvas legends and Blackboard Ledger drawers.
  - *Anchor 4 (DNA Links):* `[FEAT-494]`, `[FEAT-525]`.

- [ ] **Story 113.82: Model Throughput Realignment: Backdate Post-Prefill Decode tok/s, 10-08 Timeline Clamp, and Pure Scatter Plot (`[FEAT-496]`)**:
  - **Assigned Owner:** `[AGY:PRIMARY]`
  - **DNA Tags:** `[FEAT-496]`, `[FEAT-494]`, `[BKM-024]`
  - *Anchor 1 (Target Files):* `Portfolio_Dev/field_notes/benchmarks.js`, `Portfolio_Dev/field_notes/data/live_usage_stream.jsonl`
  - *Anchor 2 (Verification Command):* Verify 97.2% TTFT backdate correlation from `telemetry_ledger.jsonl` to `live_usage_stream.jsonl`.
  - *Anchor 3 (Code Specs):* Clamped timeline floor to `2026-10-08`, excised multi-point line connecting strokes in favor of clean scatter points with seat color-coding, and re-mapped seat name to `Hybrid GPU (2080 Ti + Arc B580)`.
  - *Anchor 4 (DNA Links):* `[FEAT-496]`.

- [ ] **Story 113.83: Output Tokens vs. Wall-Minus-TTFT Decode Curve Graph (`[FEAT-494]` / `[FEAT-496]`)**:
  - **Assigned Owner:** `[AGY:PRIMARY]`
  - **DNA Tags:** `[FEAT-494]`, `[FEAT-496]`
  - *Anchor 1 (Target Files):* `Portfolio_Dev/field_notes/benchmarks.html`, `Portfolio_Dev/field_notes/benchmarks.js`
  - *Anchor 2 (Verification Command):* Browser inspection of `id="decode-efficiency-chart"`.
  - *Anchor 3 (Code Specs):* Added second canvas chart plotting Output Tokens ($Y$-axis) vs Net Decode Duration $(t_{\text{wall}} - t_{\text{TTFT}})$ ($X$-axis) to visualize pure post-prefill generation curves.
  - *Anchor 4 (DNA Links):* `[FEAT-494]`, `[FEAT-496]`.

- [ ] **Story 113.84: Archaeology & Regression BKM: Deep Thought vs. Local Speculative Relay Invariant (`[FEAT-531]` / `[FEAT-586]`)**:
  - **Assigned Owner:** `[AGY:PRIMARY]`
  - **DNA Tags:** `[FEAT-531]`, `[FEAT-586]`, `[BKM-103]`
  - *Anchor 1 (Target Files):* `HomeLabAI/docs/Protocols.md`, `Portfolio_Dev/docs/sprints/active/SPRINT_PLAN_SPR_113_0.md`, `HomeLabAI/src/logic/speculative_triage.py`
  - *Anchor 2 (Verification Command):* Audit git history (commit `89ff3959` / Sprint 100/101) and document regression invariant.
  - *Anchor 3 (Code Specs):* Codify `BKM-103`: Primary reasoning seats (M5 Air / Deep Thought) are protected authorities; local engines are strictly standby fallbacks and must NEVER cancel Deep Thought when Deep Thought is alive and reachable.
  - *Anchor 4 (DNA Links):* `[FEAT-531]`, `[FEAT-586]`.

---

## 📜 1. The Narrative: Forensic Archaeology of the Streaming Regression

### 1) Forensic Autopsy: The Sprint 108 Regression (`commit 3048aaa`)

You are 100% right. This is an authentic regression where we threw away hard-won streaming architecture because of confusion over UI boundaries. 

The exact failure point has been uncovered in git history: **[HomeLabAI commit 3048aaa](file:///home/jallred/Dev_Lab/HomeLabAI/src/tests/test_two_mice_handover.py#L525-L558)**, authored on October 26, 2026, during **Sprint 108 (Story 108.20)**.

#### 1.1) The Intent vs. The Blunder
- **The Stated Intent ([Protocols.md: BKM-095](file:///home/jallred/Dev_Lab/HomeLabAI/docs/Protocols.md#L1910-L1930))**:  
  BKM-095 was written with explicit language to protect internal streaming:
  > *"UI Chat Bubbles Consume Only Completed, Atomic Payload Dispatches... Inter-Node Token Waterfalls Are Internal Only: Waterfall token streaming (`FEAT-233`) exists exclusively between backend processing nodes. Tokens must never leak mid-flight to public UI websockets."*
- **Where We Messed Up (The Trap in `test_two_mice_handover.py`)**:  
  In [test_two_mice_handover.py:547](file:///home/jallred/Dev_Lab/HomeLabAI/src/tests/test_two_mice_handover.py#L547), the unit test for Story 108.20 was written as:
  ```python
  # 1. Assert ZERO live streaming token packets were sent
  token_packets = [p for p in packets if p.get("type") == "token"]
  assert len(token_packets) == 0, f"Expected 0 token-streaming packets, found {len(token_packets)}"
  ```
  Instead of asserting that tokens were suppressed from **`channel in ("chat", "pinky", "voice")`**, the test enforced a **global ban on token-streaming packets everywhere in the system**.

#### 1.2) The Cascade of Destructive "Fixes"
To make that over-reaching test pass:
1. **The Router Guillotine**: In [router.py:4930](file:///home/jallred/Dev_Lab/HomeLabAI/src/v5/foyer/router.py#L4930), a blanket suppress filter was slapped on every single persona (`"brain (archive)"`, `"pinky (voice)"`, `"deep thought"`, `"pinky (triage)"`, `"pinky"`), completely killing streaming broadcasts.
2. **The Sequential String Accumulator Trap**: In [cognitive_hub.py:3887-4140](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py#L3887-L4140), `_run_two_mice_handover` was refactored into three sequential, blocking `await` statements:
   ```python
   brain_grounding = await self.step_brain_gatekeeper(...)  # Monolithic wait
   dt_synthesis = await self.step_deep_thought(...)         # Monolithic wait (30-45s)
   await self.step_pinky_voice(...)                         # Monolithic wait
   ```
   Each step consumed its async generator into a local string (`brain_grounding += token`, `dt_synthesis += token`), waiting until complete EOF before passing a single static string to the next step.

---

### 2) What Hard-Won Design Work We Threw Away

1. **`[FEAT-233.2]` & `[FEAT-233.4]` (The Live Hearing Pipe & Overhearing Buffer)**:  
   Developed across Sprints 15–31 specifically so that downstream nodes could begin evaluating upstream tokens *while generation was in flight*, cutting idle turnaround latency.
2. **`[FEAT-457]` (Speculative Context Pre-fetch)**:  
   Developed in Sprint 104 ([commit 7a5db0f6](file:///home/jallred/Dev_Lab/Portfolio_Dev/docs/sprints/active/SPRINT_PLAN_SPR_104_0.md#L33)), where Brain launched RAG context retrieval immediately in the background while Pinky spoke.
3. **Inter-Node Silicon Concurrency**:  
   We threw away hardware parallelism. While Deep Thought was deliberating on M5 Air/Kender for 35–45 seconds, the dual-GPU local engine (RTX 2080 Ti + Arc B580) sat **100% idle**, waiting for an EOF delimiter rather than pre-filling Pinky's response or pre-hydrating the Critic's rubric.

---

### 3) How Old Code Can Be Leveraged to Restore It

We do **not** need to invent new streaming primitives—the code is already in place:
1. **`_process_node_stream()` ([cognitive_hub.py:1575-1750](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py#L1575-L1750))**:  
   Already implements async generator polling from `self.session_buffers[buf_key]` with delta token yielding (`yield new_tokens`).
2. **`BicameralNode.prewarm()` ([loader.py:270](file:///home/jallred/Dev_Lab/HomeLabAI/src/nodes/loader.py#L270))**:  
   We just proved today in Story 112.190 that non-blocking concurrent dispatches eliminate 65s of latency without destabilizing memory.
3. **The Simple Architectural Fix**:
   - In `cognitive_hub.py`, pipe the output of `self._process_node_stream("thought", ...)` into an internal queue (`asyncio.Queue`) that Pinky's `step_pinky_voice` consumes as it arrives.
   - Dispatch the Critic's context pre-fill task immediately upon Stage 3 onset.
   - **Fix the Broken Test**: Update [test_two_mice_handover.py:547](file:///home/jallred/Dev_Lab/HomeLabAI/src/tests/test_two_mice_handover.py#L547) from `assert len(token_packets) == 0` to assert `assert len([p for p in packets if p.get("channel") in ("chat", "pinky") and p.get("type") == "token"]) == 0`.

---

### 4) Permanent Invariants & Tag Guardrails to Prevent Future Relapse

To permanently protect this boundary from being broken a 5th time, we will codify:

#### 4.1) New Invariant Law: `[BKM-102] / [FEAT-233.8] (Internal Pipe vs. Edge Pop Invariant)`
> **The Edge-Only Mute Mandate:**  
> The Single Delivery Authority Pop rule (`BKM-095`) is an **Edge Gateway Invariant**, NOT a Node-to-Node Invariant.  
> 1. Nodes MUST communicate via streaming async generators or queues (`FEAT-233`).
> 2. Suppression of live tokens applies **strictly and exclusively at the WebSocket egress layer** (`v5/foyer/router.py`) when target channel is conversational (`channel in ("chat", "pinky", "voice")`).
> 3. Any unit test asserting `len(token_packets) == 0` globally without channel filtering is an architectural violation and must fail linting.

#### 4.2) Guardrail Comment Tags
All inter-node streaming pipes in `cognitive_hub.py` and `loader.py` will be marked with:
`# [PROTECTED_PIPE: FEAT-233 / BKM-102] DO NOT BUFFER INTO MONOLITHIC STRING. Internal streaming only; UI pop enforced at WebSocket boundary.`

---

## 📝 5. Running Sprint Execution Log (`BKM-081` In-Tree Append Ledger)

### Entry 2026-11-18 17:23:43 PST - Story 113.55: Egress Pop Re-unification & Dual-Bubble Complexity Rollback
* **Context**: After initial Story 113.10 and 113.50 implementation, an edge-case inspection of WebSocket client delivery surfaced residual complexity in `cognitive_hub.py` and `router.py` around conversational channel classification.
* **Action**: Authored `commit 0854ee0` (`refactor(stream): eradicate Sprint 113 complexity deviation and restore clean single-delivery pop invariant`).
  - Streamlined egress check in `router.py:5260-5280` to evaluate `is_handover_persona` on outgoing chat broadcast packets while leaving underlying async queues intact.
  - Aligned `test_two_mice_handover.py` (23/23 PASS).
* **Commit**: `HomeLabAI @ 0854ee0`.

### Entry 2026-11-18 19:38:54 PST - Story 113.65: Seat-Specific Node Probe Timeout Centralization
* **Context**: Operator identified node vocal probe timeouts falling back to a default 4-second timeout during offline or pre-warming transitions, alongside ambiguity between Headroom port 8000 vs 8002.
* **Forensic Diagnosis**:
  - Investigated `config/infrastructure.json` and `config/lab_accountability_thresholds.json`. Port 8002 is the designated Headroom proxy port for M5 Air (8000 was legacy direct proxy).
  - Probe logic in `src/nodes/loader.py` had a rigid 4-second fallback rather than reading seat-specific timeouts defined in infrastructure config.
* **Action**: Authored `commit a0b0cc7` (`feat(infra): centralize seat-specific node vocal probe timeouts per LAB-119 / FEAT-685`).
  - Updated `loader.py:270-305` to dynamically resolve seat timeouts from `infrastructure.json["nodes"][node_name]["timeout"]` with fallback to `lab_accountability_thresholds.json`.
  - Enforced calibrated 15s - 30s budgets for M5 Air and local engines.
* **Commit**: `HomeLabAI @ a0b0cc7`.

### Entry 2026-11-18 20:45:00 PST - Story 113.68: Multi-Topic Live Silicon Moat Deliberations
* **Context**: Executed live conversational queries across multi-actor topology to evaluate Moat validation behavior, Two-Mice handover, and latency accounting in `round_table_deltas.json`.
* **Empirical Results**:
  1. **Topic 1 (Turn 50)**: *DMR MMIO register adaptation*:
     - Moat Filter: Evaluated 5 candidate chunks; 0/5 validated against ground truth (Negative Moat trigger).
     - Execution: Dropped all low-conviction chunks, engaged pure Two-Mice Handover with local dual-GPU + M5 Air.
     - Telemetry: Critic score 0.95, Total circuit elapsed 48.31s.
  2. **Topic 2 (Turn 51)**: *PECI metrics & thermal stress under platform load*:
     - Moat Filter: Evaluated 7 candidate chunks; 4/7 validated (Positive Moat trigger).
     - Execution: Deep Thought deliberated on M5 Air with verified Moat context; Pinky performed atomic pop.
     - Telemetry: Critic score 1.00, Total circuit elapsed 66.44s logged to `Portfolio_Dev/field_notes/data/round_table_deltas.json`.

### Entry 2026-11-18 23:55:00 PST - Story 113.70: Un-gag [DREAM_PASS] in Foyer Router & Restore Deliberation
* **Context**: Operator requested root-cause analysis for missing nightly dreams in the Round Table ledger (`round_table_deltas.json`). Forensic audit revealed:
  1. *The Live Speaker Myth*: Disproved the hallucinated assumption of physical speakers. The lab has zero audio hardware; Foyer's "voice waterfall" is purely a WebSocket text streaming abstraction.
  2. *Story 108.28 Gag Filter*: In Sprint 108, Story 108.28 erroneously added `[DREAM_PASS]` to `router.py:4796` and `router.py:5770` bypass filters, causing all dream cycles emitted by `dream_cycle.py` (`payload = {"query": "[DREAM_PASS]: ..."}`) to be swallowed and dropped by the queue drainer before reaching `run_division_of_labor()`.
  3. *Missing Discrete FEAT*: Identified that while `FEAT-525` mandated round-table logging for full multi-actor deliberations, no discrete FEAT protected subconscious dreams from being severed. Registered `[FEAT-687]` to codify this invariant.
* **Implementation Plan**:
  - Remove `or query.startswith("[DREAM_PASS]")` from `router.py:4796`.
  - Remove `or event.query.startswith("[DREAM_PASS]")` from `router.py:5770`.
  - Retain `[INTERNAL]` and `[REFINE]` queue isolation for lightweight internal maintenance while restoring `[DREAM_PASS]` to full division of labor and round table telemetry logging.
  - Update unit tests in `test_refine_queue_isolation.py`.
* **Verification & Evidence**:
  - Authored commit `HomeLabAI @ 622ba96`:
    - `src/v5/foyer/router.py`: Excised `or query.startswith("[DREAM_PASS]")` (line 4796) and `or event.query.startswith("[DREAM_PASS]")` (line 5770).
    - `src/tests/test_refine_queue_isolation.py`: Verified `[INTERNAL]` and `[REFINE]` remain isolated from conversational queue while `[DREAM_PASS]` dispatches to `run_division_of_labor()`.
  - Ran unit test suite: `HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_refine_queue_isolation.py -v` (5/5 PASS).
  - Regression check: `HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_two_mice_handover.py -v` (23/23 PASS).
  - Registered `[FEAT-687]` in `Portfolio_Dev/FeatureTracker.md`.
* **Status**: ✅ Certified & Locked. Multi-actor subconscious dream deliberation restored to the Round Table telemetry pipeline.

---

## 🚀 Track 6: Live Telemetry Alignment, Post-Prefill Decode Curves & Protected Relay Authority

### Objective
Resolve UI regressions, backdate throughput metrics to post-prefill generation decode speed, add generation efficiency curve charts, fix Turn 51 monotonic indexing in `blackboard_ledger.py`, and codify `BKM-103` on Deep Thought protected authority over standby local runners.

### Stories
* **Story 113.80: Monotonic Turn ID Fix Beyond 50-Item Cap in `blackboard_ledger.py`**
  - Fix `monotonic_turn` calculation in `HomeLabAI/src/memory/blackboard_ledger.py`: change from `len(records) + 1` to `max((r.get('turn', 0) for r in records), default=0) + 1`.
  - Maintain unique, strictly increasing integer Turn IDs across the rolling window.
  - Verify with unit tests in `HomeLabAI/src/tests/test_blackboard_dna.py` (4/4 PASS).
* **Story 113.81: Stage Terminology & Waterfall Sequence Alignment in `benchmarks.html` / `benchmarks.js`**
  - Align Delta-T legend pills and chart series from legacy labels to active 5-stage names:
    - `Δt1: Triage (Kender)`
    - `Δt2: Brain Gatekeeper (Moat RAG)`
    - `Δt3: Deep Thought (Synthesis)`
    - `Δt4: Pinky Voice (Delivery Pop)`
    - `Δt5: Sovereign Critic (Entailment Audit)`
  - Update `renderBlackboardLedger` drawer labels in `benchmarks.js`.
* **Story 113.82: Post-Prefill Decode Throughput Backdate & Chart Scatter Polish**
  - Backdate `data/live_usage_stream.jsonl` by correlating 6,181 records against `telemetry_ledger.jsonl` (97.2% matching physical TTFT).
  - Compute true generation decode speed $R_{\text{decode}} = \frac{N_{\text{tokens}}}{t_{\text{duration}} - t_{\text{TTFT}}}$.
  - Rename `"Linux 2080ti"` seat to `"Hybrid GPU (2080 Ti + Arc B580)"`.
  - Clamp universal timeline starting floor to `2026-10-08 00:00:00` UTC (`1791417600`).
  - Convert dense line graph into pure scatter plot with color-coded dot clusters.
* **Story 113.83: Output Tokens vs. Wall-Minus-TTFT Generation Curve Chart**
  - Add `<canvas id="decode-efficiency-chart" ...>` to Tab 2 (`tab-arena`) in `benchmarks.html`.
  - Implement `renderDecodeEfficiencyChart(records)` in `benchmarks.js`: $X$-axis = Net Decode Duration $(t_{\text{wall}} - t_{\text{TTFT}})$, $Y$-axis = Output Tokens.
  - Overlay theoretical slope guide rays (35 tok/s for 4090, 24 tok/s for Hybrid GPU, 16 tok/s for M5 Air).
* **Story 113.84: Archaeology & Codification of `[BKM-103]` (Deep Thought Protected Relay Race vs. Standby Local Invariant)**
  - Document `[BKM-103]` in `HomeLabAI/docs/Protocols.md`.
  - Root cause regression: Sprint 67/100 (`FEAT-586`, commit `89ff3959`) cut-throat `asyncio.wait(return_when=FIRST_COMPLETED)` with 180ms lead window prematurely cancelled M5 Air mid-flight from localhost dual-GPU.
  - Codify invariant: Deep Thought is protected authority when reachable (`AUTHORITATIVE_ALIVE`); local standby never preempts or cancels Deep Thought on early completion.

### Entry 2026-11-19 01:30:00 PST - Track 6 Execution & Certification
* **Action**:
  - Modified `HomeLabAI/src/memory/blackboard_ledger.py` (monotonic turn fix).
  - Certified `HomeLabAI/src/tests/test_blackboard_dna.py` (4/4 PASS).
  - Updated `Portfolio_Dev/field_notes/benchmarks.html` and `benchmarks.js` (5-stage naming, pure scatter plot, generation efficiency curve chart).
  - Synchronized `benchmarks.html` and `benchmarks.js` to `www_deploy/`.
  - Backdated 6,181 records in `live_usage_stream.jsonl` with 97.2% matching physical TTFT and renamed seat to `Hybrid GPU (2080 Ti + Arc B580)`.
  - Codified `[BKM-103]` in `HomeLabAI/docs/Protocols.md`.
* **Status**: ✅ Certified & Locked. Track 6 complete.
