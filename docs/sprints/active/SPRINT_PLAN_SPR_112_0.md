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

## 🧭 7. Dropped Threads Ledger (`BKM-084`)

* **A: Story 112.10 & 112.20 Execution**: Grounding of the Sovereign Judge transitioning from Dropped Thread #A into primary sprint execution.
* **B: Foyer Maintenance Quiescence Gate**: Ready to gate Foyer `/inject` with HTTP 503 when `maintenance.lock` is active to prevent overnight 02:00–05:00 AM warmup failures.
* **C: Git Push Invariant**: All local commits remain strictly unpushed per Law 0.
