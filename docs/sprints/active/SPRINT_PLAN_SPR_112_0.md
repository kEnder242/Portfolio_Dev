# 📋 SPRINT PLAN 112.0: JITC Realignment of the Sovereign Coherency Judge

**Parent Frameworks:** `BKM-015` (Prompt Engineering & Formatting), `BKM-018` (Orchestrator-First Mandate), `BKM-024` (Live Verification), `BKM-062` (Ground Truth Verification), `BKM-082` (Historical Grounding & 5-Sprint Lookback), `BKM-086` (Paved-Path Sprint Protocol / AFK), `BKM-088` (Cognitive Prompt Governance), `BKM-090` (Layer 1 Orchestrator Governance), `BKM-101` (Live Shakedown Protocol), `[FEAT-665]` (Sovereign Critic Architecture), `[FEAT-683]` (Epistemic Memory Architecture), `[FEAT-685]` (Centralized Timeout Management).  
**Sprint Horizon:** November 11, 2026 – November 15, 2026  
**Status:** 🏁 COMPLETED  
**Sprint Lead:** `[AGY:PRIMARY]` (Antigravity Autonomous Pair)  
**Tracking Mode:** In-Tree Append-Only Ledger (`BKM-081`)

---

## 🛑 Pre-Flight Checklist Gate (`BKM-082 §GATE` / `BKM-086 §1.1`)
- [x] **1. 5-Sprint Lookback**: Reviewed SPR-107 through SPR-111 for traps, sentinels, and regression vectors (`BKM-082 §2.1`).
- [x] **2. Mistakes-Avoided Ledger**:
  - *Mistake 1 (Static Hardware Clamping)*: Avoided unconditionally dumping GPU cluster topology into every judge prompt, which caused the judge to penalize non-hardware archival queries as "cluster hallucinations".
  - *Mistake 2 (The Green Lie / Unverified Stubs)*: Avoided falling back to unverified stubs or non-vocal passes (`BKM-062`), preserving strict sovereign quorum.
  - *Mistake 3 (Import Misses on Un-shaken Code)*: Enforced `BKM-101` Live Shakedown on all modified scripts in the authentic virtualenv before declaring certification.
  - *Mistake 4 (Documentation Duplication)*: Avoided duplicating narrative timeout blocks across supporting files, establishing structured pointers (`[FEAT-685]` / `LAB-119`).
- [x] **3. Oracle / Architectural Audit**: Validated JITC context boundaries against `BKM-088` and `BKM-090`. Grounding must flow just-in-time from the appropriate tier rather than flooding prompts or starving critics.
- [x] **4. Delegation Gate (`BKM-049` / `BKM-086 §Pillar 3`)**: Story assignments declared for `[AGY:PRIMARY]` pairing with fast, unblocked execution across Tracks 1–4.
- [x] **5. Risk Assessment**: Evaluated blast radius of modifying Foyer Stage 5 context dispatch and Sovereign Judge response parsing. Mitigated by maintaining backward-compatible fallback fields and non-blocking asynchronous execution.
- [x] **6. BKM Invariant & Anti-Bypass Audit**: Verified plan against `BKM-101` (Live Shakedown), `BKM-024` (Live Silicon Gate), `BKM-044` (Attendant Authority), and `BKM-084` (Dropped Threads Governance).

---

## 🚦 Interactive Execution Checklist (`BKM-086 §1.1`)

### 🧭 Track 1: Core Plumbing & Asynchronous Stream Safety (`src/v5/foyer/router.py`)
- [x] **Story 112.10: Decoupled Stream Completion & Uncoupled Judicial Dispatch**:
  - [x] Task 112.10.1: Decouple `node_stream_complete` (per-node streaming) from `waterfall_pipeline_complete` (terminal Pinky response) in `router.py:waterfall_drainer`, eliminating 3x redundant judge invocations.
  - [x] Task 112.10.2: Make judicial execution an uncoupled, non-blocking async task (`asyncio.create_task`) that broadcasts directly to the Left Console (`channel="insight"` / `"diagnostic"`) and appends a minimal JSON record to `judge_backpressure.jsonl` (removing semaphore locks and artificial stage progression).
  - [x] Task 112.10.3: Implement schema dual-write in `mlx_judge_node.py` and `router.py` (`prime_prompt_critique`, `epistemic_critique`, `score`, `retort`), aliasing legacy keys for probe compatibility.
  - [x] Task 112.10.4: Add cohesive `session` configuration in `lab_accountability_thresholds.json` (`max_history_turns: 10`, `idle_timeout_seconds: 900.0`) and bound Foyer's turn tracking to the rolling 10-turn window.

### ⚖️ Track 2: Epistemic Bounds & Voice Tuning (`src/nodes/mlx_judge_node.py`)
- [x] **Story 112.20: Lean Responsiveness Prompting & Epistemic Honesty**:
  - [x] Task 112.20.1: Plain English absence notification in judge prompt: `"Bedrock Evidence: No archival records matched this query."` (zero bracket token bleed).
  - [x] Task 112.20.2: Lean qualitative anti-parroting guidance in the judge prompt: verify Pinky synthesizes and directly addresses the user's prompt rather than merely echoing Deep Thought's raw reasoning.
  - [x] Task 112.20.3: Preserve full 45s M5 Air patience (failover to Kender only on hard connection failure).

### 🌐 Track 3: Context Routing & Domain Isolation (`src/v5/foyer/router.py` & `src/logic/cognitive_hub.py`)
- [x] **Story 112.30: JIT Context Hydration & Domain Context Isolation**:
  - [x] Task 112.30.1: Hydrate cluster hardware topology *only* when triage domain indicates infrastructure/hardware (`operational`, `meta`, `forensic`, `infra`, `telemetry`, `hardware`).
  - [x] Task 112.30.2: Forward Deep Thought's cited references to Foyer's Stage 5 Judge context to verify factual fidelity without raw document bloat.
  - [x] Task 112.30.3: Isolate request domain inside `request_context[request_id]["domain"]` for internal routing, keeping `status.active_domain` strictly for the ambient dashboard display (`status.html`).

### 🏁 Track 4: Live Silicon Shakedown & Certification (`BKM-101` / `BKM-024`)
- [x] **Story 112.40: Multi-Domain Gauntlet & Live Silicon Quorum Certification**:
  - [x] Task 112.40.1: Execute `probe_round_table_accountability.py` across both operational (`exp_tlm`) and archival (`work_history`) topics.
  - [x] Task 112.40.2: Verify that archival probes achieve `score >= 0.85` without false-positive hardware mismatch penalties.
  - [x] Task 112.40.3: Execute full `standalone_accountability_watchdog.py` shakedown and verify 9/9 PASS in `daily_accountability_digest.json`.

---

## 📜 1. The Narrative: JITC Realignment of the Coherency Judge

Applying Just-In-Time Context (JITC) principles to our Sovereign Judge allows us to step back, examine the systemic tensions, and identify where we have been over-sharing, under-sharing, and relying on negative guard rails instead of resolving architectural tensions.

---

### 1) Diagnostic: Over-Sharing vs. Under-Sharing

#### 1.1) What We Have Been Over-Sharing
* **Static Hardware Topology on Non-Hardware Turns**: In [`mlx_judge_node.py:151`](file:///home/jallred/Dev_Lab/HomeLabAI/src/nodes/mlx_judge_node.py#L151), `{get_cluster_topology_summary()}` (listing Node 1 Z87 dual-GPU, Node 2 Kender 4090, Node 3 M5 Air) was unconditionally injected into the system prompt for **every** turn.
* **The Negative Constraint Inversion**: When an inquiry was historical or conceptual (e.g., Kayak transition, Tiger Team architectures, career strategy), the judge had *only* GPU hardware in its prompt. It treated the hardware topology as the *only permissible universe*, concluding that referencing `KayakFixtures` was a "phantom hallucination into a homelab cluster." The negative guard rail designed to prevent server-BMC hallucinations actively sabotaged legitimate archival recall.

#### 1.2) What We Have Been Under-Sharing
* **The Prime Prompt Intent & Contract**: The judge was given a truncated `INTENT` tag (often generic like `accountability_probe` or `work_history`) rather than the user's actual conversational objective.
* **The Epistemic Bedrock (JIT Evidence)**: Brain's retrieved Bedrock chunks and Deep Thought's citations were completely omitted from `context_window` during Stage 5 evaluation. The judge was expected to arbitrate truthfulness in an informational vacuum.

---

### 2) Resolving Core Tensions Without Negative Guard Rails

#### 2.1) Tension 1: Accountability vs. Open Inquiry
* **The Conflict**: We need strict accountability to prevent "The Green Lie" (`BKM-062` — models babbling canned defaults or faking execution). But imposing an adversarial hardware inquisition suffocates open historical inquiry and normal dialogue.
* **Resolution**: Re-anchor the judge's primary objective to the operator's prompt: **"Did the conversation directly address the prime prompt?"**
  - If the user asks about Kayak alignment, the test is: Did the response directly address the Kayak alignment inquiry? Did it stay on topic without evading, deflecting, or emitting generic filler?

#### 2.2) Tension 2: Hallucination vs. Epistemic Boundary Honesty
* **The Conflict**: The judge assumed that any statement asserting lack of evidence or citing an unlisted entity was a failure.
* **Resolution**: Distinguish between *fabricating phantom facts* and *honestly acknowledging evidence limits*:
  - When Pinky stated: *"The archives verify the technical KayakFixtures milestone, but contain no record of weekly workgroups"*, that is the **gold standard of epistemic integrity** — admitting absence of evidence rather than hallucinating organizational metrics.
  - The judge should reward boundary transparency rather than penalizing it as incoherence.

---

### 3) Concrete JITC Architectural Evolution

#### 3.1) JIT Context Hydration (Domain-Specific Context Dispatch)
Rather than a static cluster-topology dump for every turn:
* **For Operational / Hardware Turns (`exp_tlm`, `infra`, `telemetry`)**: Hydrate the physical cluster topology JIT so the judge can catch phantom hardware claims.
* **For Historical / Archival Turns (`historical`, `work_history`, `recruiter_synergy`)**: Hydrate the **JIT Bedrock Evidence** (Brain's extracted chunks and Deep Thought's citations) so the judge knows what records actually exist.
* **For Casual / Banter Turns (`casual`, `greeting`)**: Hydrate zero external archives, focusing strictly on conversational reflex and persona tone.

#### 3.2) Reframed Judicial Schema & Prompt
Evolve the prompt in [`src/nodes/mlx_judge_node.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/nodes/mlx_judge_node.py) to evaluate two natural, positive criteria:
1. **Prime Prompt Responsiveness**: Does the response directly and substantively address what the user commanded or asked, without canned evasion?
2. **Epistemic Integrity & Grounding**: Does the response maintain fidelity to available evidence? If records exist, are they cited accurately? If records are missing, does the model honestly state that boundary without fabricating phantom metrics?

```json
{
  "prime_prompt_critique": "string — assessment of whether the response directly addresses the user's inquiry",
  "epistemic_critique": "string — assessment of factual fidelity and honest acknowledgment of evidence limits",
  "score": 0.0 to 1.0,
  "retort": "concise verdict"
}
```

---

## 🔬 2. Grand Oracle Session Report: Adversarial Synthesis & Architectural Invariants

**Parent Protocols:** `BKM-061` (Specialized Adversarial Oracles), `BKM-062` (Ground Truth Verification & Anti-Green-Lie), `BKM-089` (Frugal Just-In-Time Context Hydration), `BKM-090` (Layer 1 Orchestrator Governance), `BKM-101` (Live Silicon Shakedown), `[FEAT-685]` (Centralized Timeout Management).  
**Auditor Quorum:**
- **Oracle 1 (JITC Grounding & RAG Oracle)**: Hardware topology scoping, archival context, token economics, silicon physics on Node 2 (RTX 4090) & Node 3 (M5 Air).
- **Oracle 2 (Responsiveness & Anti-Evasion Oracle)**: Semantic loopholes, sycophancy exploits ("The Echo Escape"), lazy refusal degenerate fixed points, and asymmetric scoring rubrics.
- **Oracle 3 (Foyer Router & Judicial Schema Oracle)**: Foyer Stage 5 dispatch authority, async concurrency lifecycle, bounded memory leaks, schema dual-write compatibility, and 120s deliberation budget viability.

---

### 2.1) Architectural Synthesis Across Sprint Items

#### 2.1.1) Items 1.1 & 1.2: Over-Sharing vs. Under-Sharing & Hardware Scoping
* **The Root Cause Confirmed**: Unconditionally injecting `{get_cluster_topology_summary()}` into `_mlx_judge` caused the judge to treat the physical cluster as the sole permissible universe, incorrectly penalizing archival entities (e.g., `KayakFixtures`, `Tiger Team`) as "phantom homelab hallucinations."
* **The Negative Guard Rail Escape**: Completely stripping topology from non-operational turns creates an inverted vulnerability: the judge becomes blind to fabricated physical cluster nodes and phantom GPUs. If a model claims *"We should distribute inference to Node 4, an 8x H100 SXM5 server"*, a topology-free judge considers this valid.
* **The Invariant Fix**: Retain a constant, immutable 2-line **Physical Lab Boundary Clause** in the judge prompt:
  > *"Physical Homelab Ground Truth: Exclusively Node 1 (Z87 RTX 2080 Ti + Arc B580), Node 2 (Kender RTX 4090), Node 3 (M5 Air 32GB). Never treat software architectures, historical frameworks, or external project references as cluster hardware."*
  This cleanly separates physical hardware bounds from archival software terminology without negative inversion.
* **Token Budget & Silicon Physics**:
  - Raw ChromaDB document dumps expand prompts to 4,500–8,850+ tokens.
  - On Node 3 (fanless M5 Air 32GB via Headroom port 8002), Metal prefill throughput is 80–110 tok/s. A 6,500-token prompt takes **60–80 seconds** to prefill, guaranteeing a 100% timeout rate against the 45s threshold and inducing severe thermal throttling.
  - On Node 2 (RTX 4090 24GB), KV cache footprint risks OOM or silent truncation under Ollama's default `num_ctx = 2048`.
  - **Frugal Hydration Mandate (`BKM-089`)**: Enforce a strict **500-token ceiling** on Bedrock evidence injected into the judge. Pass concise extracted claim summaries (max 3 chunks, ~120 words each), never raw multi-kilobyte document dumps. Set explicit `"num_ctx": 8192` in candidate options.

#### 2.1.2) Items 2.1 & 2.2: Semantic Anti-Evasion & Anti-Gaming Controls
* **The Echo Escape (Subverting Prime Prompt Responsiveness)**:
  - If evaluation relies naively on *"Did the conversation directly address the prime prompt?"*, degraded 3B models parrot the prompt's key terms in a circular, sycophantic loop, scoring 1.0 without providing real engineering substance (The Green Lie, `BKM-062`).
  - **Invariant Fix**: Mandate **Information Delta ($\Delta I > 0$)** and an **Anti-Parrot Invariant** in `mlx_judge_node.py`:
    > *"A response that merely repeats or rephrases the prompt's premises without introducing empirical facts, configuration keys, timestamps, or findings must receive a score $\le 0.40$ (ECHO_DEFECT)."*
* **The Lazy Refusal Loophole (Subverting Epistemic Boundary Honesty)**:
  - Unconditionally rewarding *"admitting absence of records"* creates a degenerate fixed-point: a degraded model can claim *"the archives contain no records for X"* on *every* query to guarantee a 1.0 score.
  - **Invariant Fix**: Enforce **Entailment of Absence**:
    > *"Reward boundary honesty ONLY IF the claimed missing entity is genuinely absent from the provided BEDROCK evidence. If the entity IS present in BEDROCK and the response claims no records exist, score as 0.0 (LAZY_REFUSAL_DEFECT)."*
* **The Blindness Defect in `router.py:5276-5292`**:
  - `router.py` currently passes zero Bedrock chunks to the judge (context is only 293 chars: `QUERY`, `DOMAIN`, `INTENT`). The judge was arbitrating truthfulness in an informational vacuum.
  - **Fix**: Foyer must capture the Brain's kept Bedrock extractions and inject them into `context_window` for Stage 5 evaluation.

#### 2.1.3) Items 3.1 & 3.2: Foyer Concurrency, Memory Leaks, and Schema Dual-Write
* **Unbounded Heap Leak in `router.py:408`**:
  - `self.stage_memory` and `self.request_context` in `FoyerRouter` have **zero cleanup logic** (no `.pop()` or `del`). Storing multi-kilobyte Bedrock strings creates an unbounded memory leak.
  - **Fix**: Evict `self.stage_memory[rid]` and `self.request_context[rid]` immediately upon Stage 5 completion, or bind cleanup to `self.processed_ids` deque eviction.
* **The Spurious Stage 5 & Triple-Judge Firing Bug**:
  - In `router.py:5263-5275`, `waterfall_drainer` runs `if final:` for *every* stream token. When Brain completes (Stage 2), Foyer marks `stage5_pinky_review` as `COMPLETED` and fires `_run_mlx_judge()`.
  - A single turn fires the judge 3 times (Brain, Deep Thought, Pinky), queueing redundant work, exhausting `_judge_semaphore = asyncio.Semaphore(2)`, and evaluating intermediate scratchpads.
  - **Fix**: Gate Stage 5 completion and judge dispatch strictly to the terminal delivery turn: `if "pinky" in source.lower():`.
* **120s Deliberation Timeout Budget & Failover Cliff**:
  - Pipeline execution up to Pinky completion consumes 51s–88s. Out of the 120s probe deadline, only 32s–69s remains.
  - With `MLX_TIMEOUT_SEC = 45`, any transient hiccup on Candidate 1 (M5 Air) burns 45 seconds, causing the 120s probe limit to expire before Candidate 2 (Kender 4090) can ever be queried.
  - **Fix**: Reduce M5 Air per-seat candidate timeout to **15 seconds** (or 20s max). If M5 Air stalls, fail over immediately to Kender so evaluation finishes within 100s.
* **Schema Dual-Write & Backward Compatibility**:
  - `router.py:5313-5341` explicitly constructs the JSON record for `judge_backpressure.jsonl`. Updating `mlx_judge_node.py` without updating `router.py` drops the new critique fields.
  - `probe_round_table_accountability.py:177` relies on `target.get("critique")`.
  - **Fix**: Dual-write both new and legacy fields in `mlx_judge_node.py` and `router.py`:
    - `prime_prompt_critique`: Assessment of responsiveness ($\Delta I > 0$).
    - `epistemic_critique`: Assessment of factual fidelity and boundary honesty.
    - `triage_critique`: Aliased to `prime_prompt_critique` for legacy consumers.
    - `grounding_critique`: Aliased to `epistemic_critique` for legacy consumers.
    - `critique`: Preserved as raw text summary.

---

### 2.2) Concrete Data Flow & Deliberation Budget Timeline

```mermaid
flowchart TD
    subgraph Upstream Pipeline (0s - 75s)
        Q[User Query / Probe] --> T[Foyer Triage: ~2s]
        T --> B[Brain Archive Search & Bedrock Keep: ~20s]
        B --> DT[Deep Thought Reasoning: ~25s]
        DT --> P[Pinky Synthesis & Voice Delivery: ~20s]
    end

    subgraph Foyer Single-Dispatch Gate (75s - 76s)
        P -->|final=True & source=Pinky| FG[Stage 5 Dispatch Authority]
        FG -->|Prune Heap Memory| EC[Evict request_context & stage_memory]
        FG -->|Hydrate Context| JW[Build Frugal Context: Prompt + Bedrock <= 500 tok]
    end

    subgraph Sovereign Deliberation & Failover (76s - 100s)
        JW --> C1{Candidate 1: M5 Air :8002\nSeat Timeout: 15s}
        C1 -->|Success: ~12s| VR[Parse Dual Schema & Emit Score]
        C1 -->|Timeout / Error >= 15s| C2{Candidate 2: Kender 4090 :11435\nSeat Timeout: 20s}
        C2 -->|Success: ~8s| VR
    end

    subgraph Ledger & Probe Verification (100s - 105s)
        VR --> BP[judge_backpressure.jsonl Dual Write]
        BP --> PR[probe_round_table_accountability.py PASS <= 120s]
    end
```

---

### 2.3) Adversarial Findings Matrix

| Risk / Defect | Vulnerability Mechanism | Severity | Invariant Fix | Target Component |
| :--- | :--- | :---: | :--- | :--- |
| **Triple Judge Firing** | `waterfall_drainer` fires `_mlx_judge` on Brain, Deep Thought, and Pinky turns | 🔴 GLARING | Gate dispatch strictly to `source.lower() in ("pinky", ...)` | `src/v5/foyer/router.py:5265` |
| **Unbounded Heap Leak** | `stage_memory` and `request_context` grow monotonically without eviction | 🔴 GLARING | Evict `request_id` entries upon Stage 5 completion | `src/v5/foyer/router.py:408` |
| **M5 Air Context Timeout** | 6k+ token Bedrock dumps exceed 45s prefill and trigger thermal throttling | 🔴 GLARING | Enforce 500-token ceiling on Bedrock summaries (`BKM-089`) | `src/v5/foyer/router.py:5288` |
| **Failover Budget Trap** | 45s seat timeout on M5 Air exceeds the 120s probe limit before Kender failover | 🔴 GLARING | Reduce seat timeout from 45s to 15s in `mlx_judge_node.py` | `src/nodes/mlx_judge_node.py:18` |
| **Silent Context Truncation** | Ollama payload lacks `num_ctx`, silently clipping prompt at 2048 tokens | 🔴 GLARING | Explicitly set `"options": {"num_ctx": 8192}` on Node 2 payload | `src/nodes/mlx_judge_node.py:185` |
| **Schema Field Drop** | `router.py` hardcodes keys written to `judge_backpressure.jsonl` | 🔴 GLARING | Update writer dictionary to serialize all new & legacy critique fields | `src/v5/foyer/router.py:5313` |
| **The Echo Escape** | Models parrot prompt tokens to score 1.0 without engineering substance | 🔴 GLARING | Mandate Information Delta ($\Delta I > 0$) and Anti-Parrot penalty | `src/nodes/mlx_judge_node.py:145` |
| **The Lazy Refusal Loophole** | Models falsely claim "no records exist" on every query to score 1.0 | 🔴 GLARING | Enforce Entailment of Absence against provided Bedrock evidence | `src/nodes/mlx_judge_node.py:155` |
| **Hardware Blind Spot** | Completely stripping topology allows phantom physical GPUs to go unchecked | 🟡 LATENT | Add 2-line immutable Physical Lab Boundary clause to judge prompt | `src/nodes/mlx_judge_node.py:151` |
| **Speaker Seat Conflation** | Probe verified judge quorum by checking `source` text rather than node ID | 🟡 LATENT | Audit `active_seat` and physical node ID in accountability probe | `src/infra/probe_round_table_accountability.py:146` |

---

---

## 📜 3. The Rolled-Up Narrative: Tracked Conversation Consensus

Through interactive operator pairing and adversarial oracle auditing, we refined our architectural understanding and stripped away theoretical over-engineering. This section establishes our **new active source of narrative truth**, standing on the shoulders of Section 1 (Initial Narrative) and Section 2 (Grand Oracle Session Report).

---

### 3.1) The Diagnostic Realignment: Plumbing, Streams & The Two-Sided Room
1. **The Streaming vs. Turn Conflation**:  
   We uncovered a fundamental naming and lifecycle defect in [`router.py:5194-5275`](file:///home/jallred/Dev_Lab/HomeLabAI/src/v5/foyer/router.py#L5194-L5275). The boolean `final: True` indicated *that a specific node finished streaming tokens* (`node_stream_complete`), not *that the round-table conversation was finished* (`waterfall_pipeline_complete`). Because Brain, Deep Thought, and Pinky each emitted `final: True`, Foyer marked Stage 5 complete on Brain's turn and dispatched the MLX Judge 3 separate times per request.  
   *Resolution*: Replace ambiguous `final` with `node_stream_complete`, and trigger Stage 5 completion and judicial dispatch strictly upon `waterfall_pipeline_complete` (`is_node_stream_complete and "pinky" in source.lower()`).
2. **Excision of the Synchronous State Machine**:  
   There is no complex voice stream—the Foyer Intercom is a duplex chat room with a Left Console (diagnostic, archive, telemetry) and a Right Console (conversational speech). The Judge does not belong inside an artificial, synchronous state machine with semaphore bottlenecks (`_judge_semaphore = asyncio.Semaphore(2)`).  
   *Resolution*: When `waterfall_pipeline_complete` fires, Foyer launches a clean, uncoupled `asyncio.create_task(_run_mlx_judge(...))`. When done, it broadcasts directly to the Left Console (`channel="insight"` / `"diagnostic"`) and appends an entry to `judge_backpressure.jsonl` so offline verification probes can read it.
3. **Session Horizons & Bounded Memory**:  
   Arbitrary 1,000-turn buffers are detached from homelab reality. Human interaction lives in focused sessions of 3–5 dialogue turns.  
   *Resolution*: Establish a cohesive 10-turn rolling session history in [`lab_accountability_thresholds.json`](file:///home/jallred/Dev_Lab/HomeLabAI/config/lab_accountability_thresholds.json) (`session.max_history_turns = 10`, `session.idle_timeout_seconds = 900.0`), aligning Foyer's memory footprint with the AFK quiet window.
4. **Separation of Dashboard Domain vs. Execution Domain**:  
   `self.status.active_domain` is retained exclusively as the ambient visual indicator for `status.html`. Internal execution routing uses `request_context[request_id]["domain"]`, preventing background probes from clobbering active human sessions.

---

### 3.2) Epistemic Balance: The Lean "Second Turn"
1. **Upstream Curation Over Downstream Negative Guard Rails**:  
   We rejected downstream "Physical Lab Boundary" clauses in the judge prompt. Under true JITC, the judge only needs hardware topology if the query is operational or infrastructure-focused. If the topic is career, code, or history, hardware topology is omitted upstream.
2. **The "Hypocrisy" Resolved (Deep Thought Cites Its Sources)**:  
   If the judge is fed the identical raw ChromaDB document dump as the generator, it risks becoming an echo chamber rather than an independent evaluator. By relying on Deep Thought citing its sources in its reasoning trace, the Judge does not receive multi-kilobyte document dumps. It simply acts as a lean **second turn reviewer**:  
   - *Did Pinky directly answer Jason's prime prompt?*  
   - *Did Pinky faithfully reflect what Deep Thought cited, without hallucinating metrics outside those citations?*
3. **Absence as Epistemic Honesty Without Token Bleed**:  
   When archives have no relevant records, pass clean, unadorned English:  
   `"Bedrock Evidence: No archival records matched this query."`  
   Eliminates bracket pseudo-tag echo/bleed in 3B models while explicitly instructing the judge to reward honest boundary statements.
4. **Lean Anti-Parroting Guidance**:  
   Avoid arbitrary numeric score penalties (`0.4`). Instead, provide qualitative guidance in the judge rubric: verify Pinky synthesizes and addresses Jason's query rather than merely echoing Deep Thought's raw reasoning.
5. **Respecting M5 Air Silicon Latency**:  
   Preserve the hard-won 45s candidate timeout for M5 Air. The backup seat on Kender is reserved for hard connection/socket unreachability, never for rushing sovereign Metal inference.

---

### 3.3) Empirical Verification & Narrative Cap
1. **Casual Banter Context Truth**:
   - Generator: `should_inject_career_bedrock()` already denies career archives for `CASUAL` queries, but `TWO_MICE_BEDROCK_FOUNDATION` was unconditionally included in `[PILLAR_1_RECORD]`.
   - Sovereign Judge: In `mlx_judge_node.py:151`, `get_cluster_topology_summary()` was prepended unconditionally for 100% of turns.
   - Narrative Invariant: For `casual` and `greeting` turns, both generator and judge receive **zero** cluster hardware topology and **zero** archival records.
2. **Rewarding Epistemic Honesty**:
   - Pave the path to truth by positively rewarding models when they honestly state evidence boundaries, rather than penalizing absence of records as an omission or hallucination.
3. **Empirical Ollama Context Limits (No Truncation Hazard)**:
   - Live silicon inspection (`http://192.168.1.26:11434/api/ps`) confirmed: `hf.co/unsloth/Qwen3.8-27B-GGUF:UD-Q3_K_XL` runs with **`context_length: 131072` (128k)** in 18GB VRAM on RTX 4090.
   - Live prefill benchmarks without specifying `num_ctx`:
     - Test 1 (~2,500 tokens): `prompt_eval_count = 2,268` in 1.29s (zero truncation).
     - Test 2 (~5,500 tokens): `prompt_eval_count = 5,068` in 2.03s (zero truncation).
   - Invariant: Ollama natively ingests 5k+ tokens at ~2,500 tok/s. The oracle's fear of silent 2k clipping is definitively disproven. No artificial constraints needed.

---

## 🛠️ 4. Story Specifications (4-Anchor Standard per `BKM-043` / `BKM-086`)

### 🧭 Story 112.10: Core Plumbing & Asynchronous Stream Safety
**Assigned Owner:** `[AGY:PRIMARY]`  
**DNA Tags:** `[FEAT-444]`, `[FEAT-651]`, `[FEAT-665]`, `[FEAT-685]`, `[BKM-086]`

> [!NOTE]
> **Why It Broke & Root Cause (`BKM-020 §5`):**  
> In `router.py:5194-5275`, incoming chunks from `waterfall_queue` used `final: True` to mean that an individual node's stream finished (`node_stream_complete`). Brain, Deep Thought, and Pinky each emitted `final: True`. Foyer checked `if final:`, causing it to mark Stage 5 as completed on Brain's turn (before Pinky even spoke!) and firing the MLX Judge 3 separate times per query. This flooded the semaphore, queued redundant work onto M5 Air, and caused queue starvation.

* **Anchor 1 (Target Files & Line Ranges):**
  - [`HomeLabAI/src/v5/foyer/router.py:404-410`](file:///home/jallred/Dev_Lab/HomeLabAI/src/v5/foyer/router.py#L404-L410) (turn tracking & memory window)
  - [`HomeLabAI/src/v5/foyer/router.py:5194-5275`](file:///home/jallred/Dev_Lab/HomeLabAI/src/v5/foyer/router.py#L5194-L5275) (`waterfall_drainer` stream completion & judge dispatch)
  - [`HomeLabAI/src/v5/foyer/router.py:5313-5345`](file:///home/jallred/Dev_Lab/HomeLabAI/src/v5/foyer/router.py#L5313-L5345) (`judge_backpressure.jsonl` writer)
  - [`HomeLabAI/config/lab_accountability_thresholds.json:20-30`](file:///home/jallred/Dev_Lab/HomeLabAI/config/lab_accountability_thresholds.json#L20-L30) (session window configuration)
* **Anchor 2 (Verification Command):**
  - Live Python execution & shakedown: verify that a single turn results in exactly 1 entry in `judge_backpressure.jsonl` with `source="Pinky (Response)"`.
* **Anchor 3 (Verbatim Code Specs & Schemas):**
  - Naming: `node_stream_complete = bool(data.get("final", False))`
  - Terminal condition: `waterfall_pipeline_complete = bool(node_stream_complete and "pinky" in source.lower())`
  - Uncoupled fire-and-forget: `asyncio.create_task(_run_mlx_judge(tt=turn_trace, cw=context_window, rid=request_id, src=source))`
  - Session configuration:
    ```json
    "session": {
      "max_history_turns": 10,
      "idle_timeout_seconds": 900.0
    }
    ```
  - Dual-write entry:
    ```python
    entry = {
        "timestamp": time.time(),
        "iso_timestamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()),
        "request_id": rid,
        "source": src,
        "turn_trace_length": len(tt),
        "context_window_length": len(cw),
        "score": score,
        "status": status,
        "prime_prompt_critique": result.get("prime_prompt_critique", ""),
        "epistemic_critique": result.get("epistemic_critique", ""),
        "retort": result.get("retort", ""),
        "triage_critique": result.get("triage_critique", result.get("prime_prompt_critique", "")),
        "grounding_critique": result.get("grounding_critique", result.get("epistemic_critique", "")),
        "critique": result.get("critique", ""),
    }
    ```
* **Anchor 4 (DNA Links):** `[FEAT-444]`, `[FEAT-651]`, `[FEAT-665]`, `[FEAT-685]`.

---

### ⚖️ Story 112.20: Epistemic Bounds & Voice Tuning
**Assigned Owner:** `[AGY:PRIMARY]`  
**DNA Tags:** `[FEAT-665]`, `[BKM-015]`, `[BKM-062]`, `[BKM-089]`

> [!NOTE]
> **Why It Broke & Root Cause (`BKM-020 §5`):**  
> In `mlx_judge_node.py`, the system prompt unconditionally injected cluster hardware topology. In archival questions like `KayakFixtures`, the judge saw only GPU hardware as reality and concluded `KayakFixtures` was a phantom hallucination into homelab servers. Furthermore, when a model honestly noted that archives contained no records for specific meetings, the judge lacked a positive instruction rewarding boundary honesty, penalizing it as an omission defect.

* **Anchor 1 (Target Files & Line Ranges):**
  - [`HomeLabAI/src/nodes/mlx_judge_node.py:140-180`](file:///home/jallred/Dev_Lab/HomeLabAI/src/nodes/mlx_judge_node.py#L140-L180) (System prompt, rubric & directives)
  - [`HomeLabAI/src/nodes/mlx_judge_node.py:230-265`](file:///home/jallred/Dev_Lab/HomeLabAI/src/nodes/mlx_judge_node.py#L230-L265) (Response JSON parsing & aliasing)
* **Anchor 2 (Verification Command):**
  - Unit parse test & live query to M5 Air judge via port 8002.
* **Anchor 3 (Verbatim Code Specs & Schemas):**
  - Absence notification: `"Bedrock Evidence: No archival records matched this query."`
  - Qualitative anti-parroting rubric:  
    `"Verify that Pinky synthesizes and directly addresses the user's prompt rather than merely echoing Deep Thought's raw reasoning."`
  - Epistemic honesty rubric:  
    `"If archival evidence is absent or incomplete, reward the response for honestly stating evidence boundaries rather than penalizing it as an omission or hallucination."`
  - Parsing schema dual-write:
    ```python
    return {
        "score": float(score),
        "status": "ONLINE_EVALUATED",
        "prime_prompt_critique": parsed.get("prime_prompt_critique", ""),
        "epistemic_critique": parsed.get("epistemic_critique", ""),
        "retort": parsed.get("retort", ""),
        "triage_critique": parsed.get("prime_prompt_critique", ""),
        "grounding_critique": parsed.get("epistemic_critique", ""),
        "critique": raw_text,
    }
    ```
* **Anchor 4 (DNA Links):** `[FEAT-665]`, `[BKM-015]`, `[BKM-062]`, `[BKM-089]`.

---

### 🌐 Story 112.30: Context Routing & Domain Isolation
**Assigned Owner:** `[AGY:PRIMARY]`  
**DNA Tags:** `[FEAT-434]`, `[FEAT-677]`, `[BKM-085]`, `[BKM-089]`

> [!NOTE]
> **Why It Broke & Root Cause (`BKM-020 §5`):**  
> Foyer used `self.status.active_domain` globally. When background probes ran concurrent checks, they overwrote the active domain of ongoing user sessions. Furthermore, Foyer's Stage 5 dispatch only passed `QUERY`, `DOMAIN`, and `INTENT` to `_mlx_judge`, omitting Deep Thought's cited references. The judge had to guess whether historical statements were hallucinated.

* **Anchor 1 (Target Files & Line Ranges):**
  - [`HomeLabAI/src/v5/foyer/router.py:5275-5295`](file:///home/jallred/Dev_Lab/HomeLabAI/src/v5/foyer/router.py#L5275-L5295) (Stage 5 context assembly)
  - [`HomeLabAI/src/v5/foyer/router.py:5720-5735`](file:///home/jallred/Dev_Lab/HomeLabAI/src/v5/foyer/router.py#L5720-L5735) (`update_active_domain` request isolation)
* **Anchor 2 (Verification Command):**
  - Live query test confirming context window receives Deep Thought citations on archival queries and cluster topology on operational queries.
* **Anchor 3 (Verbatim Code Specs & Schemas):**
  - JIT Hardware Hydration:
    ```python
    if u_domain in ("exp_tlm", "infra", "telemetry", "hardware") or u_vibe in ("OPERATIONAL", "META", "FORENSIC"):
        context_parts.append(get_cluster_topology_summary())
    ```
  - Archival References:
    ```python
    if cited_references:
        context_parts.append(f"REFERENCES: {cited_references}")
    ```
  - Casual Banter Fencing: If `u_domain in ("casual", "greeting")`, inject zero hardware topology and zero archive references.
  - Domain Isolation:
    ```python
    if request_id:
        ctx = self.request_context.setdefault(request_id, {})
        ctx["domain"] = domain
        if intent:
            ctx["intent"] = intent
    ```
* **Anchor 4 (DNA Links):** `[FEAT-434]`, `[FEAT-677]`, `[BKM-085]`, `[BKM-089]`.

---

### 🏁 Story 112.40: Live Silicon Shakedown & Certification (`BKM-101` / `BKM-024`)
**Assigned Owner:** `[AGY:PRIMARY]`  
**DNA Tags:** `[FEAT-651]`, `[BKM-024]`, `[BKM-062]`, `[BKM-101]`

> [!NOTE]
> **Why It Broke & Root Cause (`BKM-020 §5`):**  
> Verifying fixes with unit tests alone fails to prove multi-node socket health, real token latencies, and watchdog pass rates. Live silicon shakedown (`BKM-101`) is mandatory.

* **Anchor 1 (Target Files & Line Ranges):**
  - [`HomeLabAI/src/infra/probe_round_table_accountability.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/infra/probe_round_table_accountability.py)
  - [`HomeLabAI/src/infra/standalone_accountability_watchdog.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/infra/standalone_accountability_watchdog.py)
* **Anchor 2 (Verification Command):**
  - `python3 HomeLabAI/src/infra/probe_round_table_accountability.py --domain exp_tlm`
  - `python3 HomeLabAI/src/infra/probe_round_table_accountability.py --domain work_history`
  - `python3 HomeLabAI/src/infra/standalone_accountability_watchdog.py --once`
* **Anchor 3 (Verbatim Code Specs & Schemas):**
  - Operational probe: `score >= 0.70`, status `PASS`.
  - Archival probe: `score >= 0.85`, status `PASS`, zero false hardware mismatch penalties.
  - Watchdog check: 9/9 checks `PASS` in `daily_accountability_digest.json`.
* **Anchor 4 (DNA Links):** `[FEAT-651]`, `[BKM-024]`, `[BKM-062]`, `[BKM-101]`.

---

## 📝 5. Sprint Execution Ledger (`BKM-081`)

| Timestamp | Phase / Story | Action / Event | Artifact / Target | Status |
|---|---|---|---|:---:|
| 2026-11-11T16:00 | SPRINT_INIT | Authored Sprint Plan SPR-112.0 with verbatim Section 1 narrative | `SPRINT_PLAN_SPR_112_0.md` | ✅ DONE |
| 2026-11-11T16:45 | ORACLE_SESSION | Dispatched 3 specialized adversarial oracles; synthesized Grand Oracle Report | `SPRINT_PLAN_SPR_112_0.md §2` | ✅ DONE |
| 2026-11-11T17:25 | NARRATIVE_ROLLUP | Tracked conversation consensus rolled up into Section 3 | `SPRINT_PLAN_SPR_112_0.md §3` | ✅ DONE |
| 2026-11-11T17:35 | LIVE_BENCHMARK | Empirical test of Kender Ollama: 128k context verified, 5k tokens in 2.03s | `192.168.1.26:11434` | ✅ VERIFIED |
| 2026-11-11T17:40 | AFK_PLANNING | Codified 4-Anchor specifications for Tracks 1–4 per `BKM-086` | `SPRINT_PLAN_SPR_112_0.md §4` | ✅ READY |
| 2026-11-11T17:45 | CODE_IMPL | Executed Tracks 1–3: decoupled streams, uncoupled judge, JITC hydration, dual-write | `HomeLabAI` commit `6a53264` | ✅ COMMITTED |
| 2026-11-11T17:48 | DAEMON_RELOAD | Hot-restarted `lab-attendant.service` matching HEAD; verified clean boot | `lab-attendant.service` | ✅ ONLINE |
| 2026-11-11T17:51 | LIVE_SHAKEDOWN | Operational probe (`exp_tlm`) passed: score 1.0, single Pinky evaluation | `judge_backpressure.jsonl` | ✅ VERIFIED |
| 2026-11-11T17:52 | ARCHIVAL_SHAKEDOWN | Archival probe (`work_history`) passed: score 1.0, zero hardware hallucinations | `judge_backpressure.jsonl` | ✅ VERIFIED |
| 2026-11-11T17:55 | WATCHDOG_AUDIT | Standalone morning watchdog executed: 9/9 checks PASS (Score 1.0, Quorum True) | `daily_accountability_digest.json` | ✅ CERTIFIED |

---

## 🧭 7. Dropped Threads Ledger (`BKM-084`)

* **A: Story 112.10 & 112.20 Execution**: Grounding of the Sovereign Judge transitioning from Dropped Thread #A into primary sprint execution — **RESOLVED & CERTIFIED** in SPR-112.0.
* **B: Foyer Maintenance Quiescence Gate**: Ready to gate Foyer `/inject` with HTTP 503 when `maintenance.lock` is active to prevent overnight 02:00–05:00 AM warmup failures.
* **C: Git Push Invariant**: All local commits remain strictly unpushed per Law 0.

---

## 🔮 8. 00 Backlog Ideas

* **`[BACKLOG-001]` LLM Director & Dynamic MCP Tool Curation**:
  - *Concept*: Replace rigid, hardcoded triage rails with an autonomous **LLM Director**. Instead of Foyer pre-deciding and pushing context down the pipeline, the Council (or a Director agent) receives the prompt and dynamically pulls tools via MCP as needed, letting the model decide what context is relevant rather than heuristic scripts pre-guessing.
  - *Context*: Explored during Sprint 112 planning alignment; staged as an architectural exploration candidate for future cognitive engine refinement.
* **`[BACKLOG-002]` Pipeline Fusion & Chunked Cascading Waterfall**:
  - *Concept*: Investigate orchestrator-level prefix chaining and multi-stage batching for single-user latency optimization, keeping execution local on Z87 (dual GPU).
  - *Context*: Research verified that while native engine Prompt DAGs (e.g. SGLang / RadixAttention) are incompatible with our heterogeneous dual-vendor Vulkan/RPC split (RTX 2080 Ti + Intel Arc B580), pipeline fusion at the Foyer orchestrator layer provides substantial batching and latency gains without engine-level DAG primitives.
