# 📋 SPRINT PLAN 113.0: Inter-Node Waterfall Streaming Restoration & Decoupled Edge Pop Governance

**Parent Frameworks:** `BKM-015` (Prompt Engineering & Formatting), `BKM-018` (Orchestrator-First Mandate), `BKM-024` (Live Verification), `BKM-062` (Ground Truth Verification), `BKM-081` (In-Tree Append Ledger), `BKM-082` (Historical Grounding & 5-Sprint Lookback), `BKM-086` (Paved-Path Sprint Protocol / AFK), `BKM-095` (UI Atomic Turn Dispatch), `BKM-102` (Internal Pipe vs. Edge Pop Invariant), `[FEAT-233]` (Inter-Node Token Waterfall & Live Hearing Pipe), `[FEAT-361]` (Token Transparency Mandate), `[FEAT-439]` (Async Sanity Judge Protocol), `[FEAT-457]` (Speculative Context Pre-fetch), `[FEAT-489]` (Two-Mice Sequential Handover), `[FEAT-684]` (Pre-Streaming Waterfall Routing).  
**Sprint Horizon:** November 18, 2026 – November 22, 2026  
**Status:** 🚀 ACTIVE / PLANNING  
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
- [x] **3. Oracle / Architectural Audit**: Pre-flight review completed and certified with zero blockers by Cloud Oracle (`ses_e0f316788ffeSQjEBGquvHnI9I` in [`Portfolio_Dev/docs/sprints/active/ORACLE_REVIEW_SPRINT_113.md`](file:///home/jallred/Dev_Lab/Portfolio_Dev/docs/sprints/active/ORACLE_REVIEW_SPRINT_113.md)). Validated decoupling boundaries against `BKM-095`, `BKM-102`, `FEAT-233`, and `FEAT-361`. Inter-node backend streaming and user-facing atomic balloon delivery are orthogonal concerns that must never be conflated.
- [x] **4. Delegation Gate (`BKM-049` / `BKM-086 §Pillar 3`)**: Story assignments declared: Leaf plumbing and unit test assertions assigned to `[SWARM:LOCAL]`; cross-module routing and protocol codification assigned to `[SWARM:CLOUD]`; physical silicon certification and daemon lifecycle assigned to `[AGY:PRIMARY]`.
- [x] **4.1 Sole-Owner & Zero-Delegation Tripwire (`BKM-049 §3.4` / `BKM-086 §Pillar 3`)**: Verified non-homogeneous allocation across stories. AGY is NOT sole owner across 100% of tasks.
- [x] **5. Risk Assessment**: Evaluated blast radius of modifying `_run_two_mice_handover` token pipes and Foyer WebSocket egress filtering. Zero risk to database schemas or GPU hardware topology; fully verified via unit test mocks and live accountability probes.
- [x] **6. BKM Invariant & Anti-Bypass Audit**: Verified plan against `BKM-095` (Edge Pop), `BKM-101` (Live Shakedown), `BKM-024` (Live Silicon Gate), and `BKM-084` (Dropped Threads Governance).

---

## 🚦 Interactive Execution Checklist (`BKM-086 §1.1`)

### 🧭 Track 1: Edge Egress Decoupling & Unit Test Correction
- [ ] **Story 113.10: Surgical Unit Test Realignment & Egress Filtering (`[BKM-095]` / `[FEAT-361]`)**:
  - **Assigned Owner:** `[SWARM:LOCAL]`
  - [ ] Task 113.10.1: Refactor `HomeLabAI/src/tests/test_two_mice_handover.py:547`: replace global `assert len(token_packets) == 0` with channel-scoped assertion asserting zero streaming tokens on user-facing channels (`channel in ("chat", "pinky", "voice")`).
  - [ ] Task 113.10.2: Update `v5/foyer/router.py`: enforce `BKM-095` atomic pop suppression strictly at the WebSocket egress layer for conversational bubbles, while allowing diagnostic and internal channels (`"internal_stream"`, `"insight"`, `"crosstalk"`) to stream freely.
  - [ ] Task 113.10.3: Verify test suite runs 100% green with streaming enabled internally.

### ⚡ Track 2: Inter-Node Waterfall Streaming Restoration
- [ ] **Story 113.20: Pipelined Relay from Deep Thought to Pinky (`[FEAT-233.2]` / `[FEAT-489]`)**:
  - **Assigned Owner:** `[SWARM:CLOUD]`
  - [ ] Task 113.20.1: In `cognitive_hub.py:3887-4140`, replace monolithic `await self.step_deep_thought()` with a pipelined async generator / queue.
  - [ ] Task 113.20.2: Connect Pinky's `step_pinky_voice()` prefill buffer to consume Deep Thought's token stream incrementally as chunks arrive from Kender/M5 Air.
  - [ ] Task 113.20.3: Verify Pinky begins prompt evaluation before Deep Thought finishes generating, collapsing 5–10s of trailing circuit turnaround latency.

- [ ] **Story 113.30: Concurrent Pre-Hydration of the Sovereign Critic (`[FEAT-439]` / `[FEAT-608]`)**:
  - **Assigned Owner:** `[SWARM:CLOUD]`
  - [ ] Task 113.30.1: In `cognitive_hub.py:4140`, decouple `step_entailment_audit` from post-Pinky execution; trigger judicial context pre-warming on M5 Air concurrently during Stage 3/5 generation.
  - [ ] Task 113.30.2: Forward query, Brain's `RAW_KEEP_CHUNKS`, and Deep Thought synthesis to the Critic to pre-fill its KV cache before Pinky speaks.
  - [ ] Task 113.30.3: Benchmark post-turn Quorum evaluation latency, verifying reduction to < 1.0 second.

- [ ] **Story 113.40: Shared Root Prefix Standardization for Local Slot-0 KV Cache Reuse (`[LAB-122]`)**:
  - **Assigned Owner:** `[SWARM:LOCAL]`
  - [ ] Task 113.40.1: Standardize a static 500-token `<cluster_root>` prefix identical across Pinky and Brain system prompts.
  - [ ] Task 113.40.2: Probe `http://127.0.0.1:8088/slots` during handover, verifying `n_prompt_tokens_cache > 0` and `f_keep > 0.50` on slot 0.

### 🛡️ Track 3: Permanent DNA Codification & Guardrails
- [ ] **Story 113.50: Codification of BKM-102 & Code Comment Annotation**:
  - **Assigned Owner:** `[AGY:PRIMARY]`
  - [ ] Task 113.50.1: Codify `[BKM-102] / [FEAT-233.8] (Internal Pipe vs. Edge Pop Invariant)` into `HomeLabAI/docs/Protocols.md`.
  - [ ] Task 113.50.2: Annotate all internal streaming pipes in `cognitive_hub.py`, `loader.py`, and `router.py` with `# [PROTECTED_PIPE: FEAT-233 / BKM-102] DO NOT BUFFER INTO MONOLITHIC STRING.`
  - [ ] Task 113.50.3: Update `FeatureTracker.md` registering `FEAT-233.8` as ACTIVE.

### 🏁 Track 4: Live Silicon Certification & Gauntlet
- [ ] **Story 113.60: Multi-Topic Silicon Shakedown & Quorum Certification (`[BKM-024]` / `[BKM-101]`)**:
  - **Assigned Owner:** `[AGY:PRIMARY]`
  - [ ] Task 113.60.1: Execute `probe_round_table_accountability.py` on active physical silicon.
  - [ ] Task 113.60.2: Verify end-to-end circuit latency improvement below the 60.0s floor while certifying `sovereign_quorum: true` and `critic_score >= 0.90`.
  - [ ] Task 113.60.3: Run `standalone_accountability_watchdog.py` certifying 9/9 PASS.

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
