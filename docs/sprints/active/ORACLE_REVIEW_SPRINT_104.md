# 🔍 ORACLE ADVERSARIAL REVIEW: Sprint 104.0 (Pre-Execution Audit)

**Reviewer:** `[SWARM:ORACLE]` (Strategic Architectural Adversary / AGY)  
**Date:** 2026-10-16  
**Target Specifications:** [`SPRINT_PLAN_SPR_104_0.md`](file:///home/jallred/Dev_Lab/Portfolio_Dev/docs/sprints/active/SPRINT_PLAN_SPR_104_0.md)  
**Target Repositories:** `HomeLabAI` (branch `sprint-104`), `Portfolio_Dev` (branch `main`)  
**Governing BKMs & Invariants:** `[BKM-004]`, `[BKM-006]`, `[BKM-015]`, `[BKM-020]`, `[BKM-024]`, `[BKM-030]`, `[BKM-039]`, `[BKM-043]`, `[BKM-049]`, `[BKM-061]`, `[BKM-080]`, `[BKM-081]`, `[BKM-082]`, `[BKM-083]`, `[FEAT-233]`, `[FEAT-234]`, `[FEAT-238]`, `[FEAT-418]`, `[FEAT-489]`, `[FEAT-523]`, `[FEAT-635]`, `[FEAT-645]`

---

## 1. Executive Assessment & Macro Architectural Verdict

### 🏛️ The Verdict: **APPROVED WITH 4 CRITICAL ADVERSARIAL SAFEGUARDS**
The proposal to eradicate the bifurcated casual path (`lead_node = "both"`) and unify 100% of turns into the **Council of Hemispheres** is **architecturally imperative**. Forensic git archaeology (`f9ec302` $\to$ `FEAT-542`) confirmed that the casual bypass was an artificial band-aid that directly spawned "The Island of Green Illusion", muted Deep Thought, and broke vector retrieval on informal queries ("Aurora Miss").

However, executing this unification without categorical shortcuts introduces four distinct edge cases that must be mitigated by concrete code contracts:

---

## 2. Adversarial Peer Review & Edge-Case Analysis

| Risk Dimension | Oracle Finding / Failure Mode | Architectural Mitigation in Sprint 104 | Status |
| :--- | :--- | :--- | :--- |
| **1. Greeting Latency Explosion** | Routing simple greetings (*"hi"*) through a 4-node sequential handover could explode latency from $<1.5\text{s}$ to $>6.0\text{s}$ if nodes spin up unneeded prompts or wait for remote GPUs. | **A.** Gated zero-ChromaDB dispatch: When `len(target_domains) == 0` and `search_terms == ""`, RAG returns in $0.0\text{ms}$ with zero DB queries.<br/>**B.** Deep Thought dormancy: If `current_interest < 0.30`, DT budget is 0 tokens and stage returns immediately ($0.0\text{ms}$).<br/>**C.** Pacing floors: Pinky quip is paced to $\sim 15-35$ tokens. Total greeting turn latency remains $<2.5\text{s}$. | **MANDATED IN STORY SPECS** |
| **2. Pinky Dual-Vocal Clash** | In the Council, Pinky speaks in Stage 2 (opening HyDE take) and Stage 6 (Critic verdict). For a simple greeting (*"hi"*), having Pinky speak twice in the same 3-second turn sounds redundant and jarring. | **Adaptive Critic Pass**: In Stage 6 (`step_grounding_critic`), if `current_interest < 0.25` and Brain delivered a simple greeting quip, Pinky's Critic turn is either a single micro-quip or gracefully yields, preventing double-talking on trivial greetings. | **MANDATED IN STORY SPECS** |
| **3. Upvote Race Condition** | Pinky's `upvote: true` in Stage 2 boosts interest from e.g. $0.06$ to $0.36$. If Deep Thought's budget was evaluated *before* Pinky's upvote, Deep Thought would stay dormant even though the alarm was pulled. | **Strict Sequential Causality**: Triage initial interest feeds Pinky $\to$ Pinky's upvote applies immediately to `self.current_interest` $\to$ Brain and Deep Thought evaluate budget against the *post-boosted* interest. | **MANDATED IN STORY SPECS** |
| **4. LoRA vs Base Adapter Drift** | Casual Pinky previously relied on `cli_voice_v1` LoRA weights for personality, while HyDE uses `local-unified-base`. Merging them must not sanitize Pinky into a wooden corporate assistant. | **Persona Preservation in JSON**: `HYDE_SYNTHESIS_PROMPT` behavioral guidance explicitly commands Pinky's authentic voice and wit in `spoken_take`, using few-shot character banter examples in the prompt to preserve persona without needing LoRA grammar clashing. | **MANDATED IN STORY SPECS** |

---

## 3. Delegation Matrix & Invariant Allocations (`BKM-049`)

To strictly avoid the **Self-Promotion Trap** (`BKM-049` / Rule 7):
* **`[SWARM:CLOUD]` (Nemotron / DeepSeek)**: Delegated all heavy AST refactoring and code pruning in `cognitive_hub.py` (deleting the `lead_node == "both"` branch, excising casual prompt assembly, and wiring the unified staged handover).
* **`[SWARM:LOCAL]`**: Delegated deterministic contract execution (`test_multi_stage_replay_pipeline.py`) and fast unit test verification.
* **`[ORACLE]`**: Delegated post-stage contract audits (`BKM-061`).
* **`[AGY:PRIMARY]`**: Restricted to orchestration, git boundaries (atomic commits per story), AST review, and live silicon validation against the running daemon on port 8765.
