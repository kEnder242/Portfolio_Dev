# 📋 SPRINT PLAN 112.0: JITC Realignment of the Sovereign Coherency Judge

**Parent Frameworks:** `BKM-015` (Prompt Engineering & Formatting), `BKM-018` (Orchestrator-First Mandate), `BKM-024` (Live Verification), `BKM-062` (Ground Truth Verification), `BKM-082` (Historical Grounding & 5-Sprint Lookback), `BKM-086` (Paved-Path Sprint Protocol / AFK), `BKM-088` (Cognitive Prompt Governance), `BKM-090` (Layer 1 Orchestrator Governance), `BKM-101` (Live Shakedown Protocol), `[FEAT-665]` (Sovereign Critic Architecture), `[FEAT-683]` (Epistemic Memory Architecture), `[FEAT-685]` (Centralized Timeout Management).  
**Sprint Horizon:** November 11, 2026 – November 15, 2026  
**Status:** 🚀 ACTIVE (In Planning / Execution)  
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
- [ ] **4. Delegation Gate (`BKM-049` / `BKM-086 §Pillar 3`)**: Story assignments staged for `[SWARM:LOCAL]` (`KENDER 4090`) and `[AGY:PRIMARY]` pairing.
- [x] **5. Risk Assessment**: Evaluated blast radius of modifying Foyer Stage 5 context dispatch and Sovereign Judge response parsing. Mitigated by maintaining backward-compatible fallback fields and non-blocking asynchronous execution.
- [x] **6. BKM Invariant & Anti-Bypass Audit**: Verified plan against `BKM-101` (Live Shakedown), `BKM-024` (Live Silicon Gate), `BKM-044` (Attendant Authority), and `BKM-084` (Dropped Threads Governance).

---

## 🚦 Interactive Execution Checklist (`BKM-086 §1.1`)

### 🧭 Phase 1: JIT Context Hydration & Domain-Specific Context Dispatch
- [ ] **Story 112.10: Domain-Specific Context Dispatch in Foyer (`src/v5/foyer/router.py`)**:
  - [ ] Task 112.10.1: Instrument Foyer Stage 5 dispatch to capture Brain's finalized Bedrock chunks (`[BEDROCK SELECTION]`) and Deep Thought's citations for the active `request_id`.
  - [ ] Task 112.10.2: For historical/archival queries (`historical`, `work_history`, `recruiter_synergy`), inject JIT Bedrock evidence into `context_window` sent to `_mlx_judge`.
  - [ ] Task 112.10.3: For operational queries (`exp_tlm`, `infra`, `telemetry`), inject JIT cluster hardware topology.
  - [ ] Task 112.10.4: For casual/banter queries (`casual`, `greeting`), inject minimal conversational context with zero external bloat.

### ⚖️ Phase 2: Reframed Judicial Schema & Prime Prompt Responsiveness
- [ ] **Story 112.20: Sovereign Critic Prompt & Schema Re-Architecture (`src/nodes/mlx_judge_node.py`)**:
  - [ ] Task 112.20.1: Refactor Sovereign Judge prompt to center on Prime Prompt Responsiveness: "Did the conversation directly address the prime prompt?"
  - [ ] Task 112.20.2: Update JSON response schema to output `prime_prompt_critique`, `epistemic_critique`, `score`, and `retort`.
  - [ ] Task 112.20.3: Reward honest boundary statements (admitting absence of unlogged records) as high epistemic integrity rather than penalizing as hallucinations.
  - [ ] Task 112.20.4: Update response parsing in `mlx_judge_node.py` to handle reframed critique schema with full backward-compatibility for legacy fields.

### 🏁 Phase 3: Live Silicon Shakedown & Certification (`BKM-101` / `BKM-024`)
- [ ] **Story 112.30: Multi-Domain Gauntlet & Live Silicon Quorum Certification**:
  - [ ] Task 112.30.1: Execute `probe_round_table_accountability.py` across both operational (`exp_tlm`) and archival (`work_history`) topics.
  - [ ] Task 112.30.2: Verify that archival probes achieve `score >= 0.85` without false-positive hardware mismatch penalties.
  - [ ] Task 112.30.3: Execute full `standalone_accountability_watchdog.py` shakedown and verify 9/9 PASS in `daily_accountability_digest.json`.

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

## 🧭 7. Dropped Threads Ledger (`BKM-084`)

* **A: Story 112.10 & 112.20 Execution**: Grounding of the Sovereign Judge transitioning from Dropped Thread #A into primary sprint execution.
* **B: Foyer Maintenance Quiescence Gate**: Ready to gate Foyer `/inject` with HTTP 503 when `maintenance.lock` is active to prevent overnight 02:00–05:00 AM warmup failures.
* **C: Git Push Invariant**: All local commits remain strictly unpushed per Law 0.
