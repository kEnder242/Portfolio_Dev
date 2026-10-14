# 🚀 SPRINT PLAN 102.0: Continuous Interest Multiplier Pacing, Brain Epistemic Gatekeeper & Narrative Steering, Sideband Consensus, and Meta-Vocabulary Prompt Decoupling

**Sprint ID:** `SPR_102_0`  
**Theme:** Continuous Scalar Interest Multiplier Pacing (`FEAT-523` Redefinition), Brain Epistemic Gatekeeper & Unrelated RAG Filtering (`FEAT-635`), Two-Mice Sideband Consensus (`VIBE-015`), Prompt Meta-Vocabulary Decoupling (Intent Cleanliness), and Adversarial Oracle Pre-Grounding  
**Status:** **COMPLETED & CERTIFIED (8/8 WATCHDOG GREEN)**  
**Parent Framework:** `[BKM-005]` (Design Studio Alignment), `[BKM-020]` (Intent Preservation & Phase Gates), `[BKM-024]` (Live Validation Mandate), `[BKM-039]` (Pure Interest Cascade Protocol), `[BKM-049]` (Owner Tag Mandate), `[BKM-061]` (Adversarial Oracle Audit), `[BKM-064]` (Tracked Conversational Ledger), `[BKM-077]` (1:1 Numbered Swim Lane Rule), `[BKM-080]` (Ask-Oracle Delegation Protocol), `[BKM-081]` (Pre-Flight Mistakes Avoided), `[BKM-082]` (Sprint Grounding Run Mandate), `[FEAT-234]` (Pure Scalar Fuel), `[FEAT-238]` (Council of Hemispheres), `[FEAT-418]` (Symmetrical Interest Cascade), `[FEAT-523]` (Continuous Multiplier Token Pacing), `[FEAT-635]` (Brain Information Gatekeeper), `[VIBE-015]` (Sideband Interest Consensus)  
**Target Silicon Nodes:** `z87-Linux` (RTX 2080 Ti Local vLLM 3B Base :8088), Node KENDER (RTX 4090 Ollama Conductor :11434), Node Brain (macOS M5 Air MLX :8002 via Headroom), ChromaDB Port 8001 (CLaRa-DNA)

---

## 🏛️ Master Consensus Narrative & Executive Report

### Background & Genesis
Sprint 102.0 emerges from an intensive architectural alignment session between L0 (Human Operator) and AGY:PRIMARY. The core realization resolves a long-standing operational anomaly across the Federated Lab: **why Deep Thought answers were consistently perceived as jarringly massive and runaway, while the interest loop felt unresponsive.**

Forensic inspection of `HomeLabAI/src/logic/cognitive_hub.py#L1104-L1118` unmasked the root defect:
```python
# [FEAT-523] Token Budget: Clamp casual/low-interest turns to 150 tokens to prevent runaway loops
token_budget = (
    max_tokens if max_tokens is not None
    else (128 if is_triage else (150 if getattr(self, "current_interest", 0.5) < 0.3 or getattr(self, "current_vibe", "TECHNICAL") == "CASUAL" else 1500))
)
```
Instead of functioning as a continuous gradient, `current_interest` was locked behind a coarse binary step function: any turn with interest $\ge 0.3$ was unconditionally granted a massive 1,500-token allocation. This coarse clamp directly contradicted the original design intent of **Scalar Fuel (`FEAT-234`)** and the **Symmetrical Interest Cascade (`FEAT-418`)**.

Interest was never meant to be a static token bucket—**interest is a continuous multiplier** ($0.0 \dots 1.0$) that smoothly throttles output verbosity. When interest is $0.76$, with a base multiplier of 100, the model receives a tight, focused budget of ~76 tokens. Low interest means nodes talk less, on a smooth gradient down to terseness and silence. This mathematical clarity unlocks generous routing limits: heavy compute nodes (Deep Thought and Brain) can be safely invited into conversation without the operator fearing a wall of text.

Simultaneously, the architectural division of labor between the Two Mice is crystallized:
- **Pinky:** The optimistic associative scout and personification of Hypothetical Document Embeddings (HyDE). Pinky retrieves wide candidate vectors and offers an initial enthusiastic hypothesis.
- **Brain:** The cynical epistemic gatekeeper and narrative steerer. Brain does not simply downvote or kill turns; Brain inspects retrieved RAG against human intent, filters out unrelated distraction clutter, and steers the dialogue toward grounded reality.
- **Deep Thought:** The heavy compute distillation engine, protected from prompt pollution, receiving only high-density curated facts and generating answers proportional to interest.

---

## 🏊‍♂️ The 8 Tracked Conversational Swim Lanes (`BKM-077`)

Per `BKM-077` (amended herein), the tracked numbers $1 \dots 8$ **are** the immutable swim lanes. They are neither merged nor collapsed, and preserve 1:1 parity with the architectural dialogue:

### Swim Lane 1: Phased Execution, Git Checkpoints & L0 Circuit Breaker
* **Origin Directive:** *"Good. Let's organize this into phases. Git commit between phases, as phases. Testing gives us a time to pause and evaluate what is practical and needed. Bake a re-evaluation between each phase in the plan as well. I think an oracle would do. Express permission to cancel a heads down if recommendations deviate significantly or drastically less work is apparently needed, I want to ensure you consult me, as L0, don't get trapped into thinking you can do this just like L2 and L3 often do. Agree that interest and prompt tweaking can be phase 1, Monologue and side-band are nuanced enough to deserve attention later as phase 2. Plan it in the sprint doc."*
* **Architectural Consensus:**
  - Execute sequentially across strict phase boundaries:
    - **Phase 0:** Pre-Grounding Audit, 5-Sprint Lookback, DNA Ledger, and Cloud Adversarial Oracle Pre-Pass.
    - **Phase 1 (Plumbing):** Continuous Interest Multiplier Token Budgeting (`cognitive_hub.py`, `infrastructure.json`), RAG Filtering, and Generous Routing Decoupling.
    - **Phase 2 (Narrative & Voice):** Brain First-Person Cynical Voice Calibration, Narrative Steering Prompts, Two-Mice Sideband Consensus (`VIBE-015`), and Short-Circuit Replay Harness.
    - **Phase 3 (Certification):** Live Silicon Validation (`BKM-024`) across M5 Air and KENDER 4090, Watchdog Audit Certification.
  - **The L0 Circuit Breaker:** Autonomous subagents are prohibited from expanding scope or rationalizing deviation. If the adversarial Oracle or live testing indicates that significantly less work is required, or that the design must pivot, execution immediately pauses to consult L0.
  - **Git Boundary Rule:** Clean, atomic `git commit` checkpoints between each phase.

### Swim Lane 2: Executive Consensus Narrative & Sprint Plan Elevation
* **Origin Directive:** *"Please consider adding a section at the top that is on the same level as your consensus reports. I want our narrative to survive as I think it's the most crucial part of the design process. Of course stories, anchors, hooks, details, context and tasks need to be grounded as well, but they don't paint the big picture. Each sprint has one or more of these big picture reports. I believe there is a BKM describing this way to create a sprint as well?"*
* **Architectural Consensus:**
  - Codified in accordance with `BKM-005` (Design Studio Alignment), `BKM-020` (High-Fidelity Sprint Gates), `BKM-030` (Document Hierarchy), `BKM-081` (Pre-Flight Mistakes-Avoided), and `BKM-082` (Sprint Grounding Run Mandate).
  - The Sprint Master Plan elevates the Executive Consensus Narrative to Section 0. Technical specifications and 4-anchor story cards derive their rationale directly from this narrative anchor.

### Swim Lane 3: Pre-Grounding Audit, Adversarial Oracle Gate & Historical Lookback
* **Origin Directive:** *"Sure, let's add a Phase 0 for pre-grounding. Does this mean oracle goes into phase 0 or 1? Fine either way. I touched on some re-evaluation steps in #1, consider this as well. Once we see the whole plan you should be able to review that it's consistent with our tracked conversation. Historical look back is going to be essential. Recommend checking the titles in 5 sprints prior to 97 to see if we have additional background. IIRC sprint 96 might be a key, and even the sprint where we invented the interest loop. Keep a mini report of the sprints and how they map in our sprint and in text to me. I'd like to see what you dig up."*
* **Architectural Consensus:**
  - Place Cloud Adversarial Oracle Audit (`delegate.py --oracle`) squarely in **Phase 0**. The Oracle stress-tests the planned continuous multiplier formula and Brain filtering contracts *before* modifying production hub logic.
  - Conduct a forensic 5-Sprint Historical Lookback (Sprints 92–96) plus the Sprint 31/FEAT-418 genesis. Document findings in a dedicated sprint ledger.

### Swim Lane 4: Sideband Consensus, Narrative Steering & VIBE-015
* **Origin Directive:** *"brain can also choose to steer the narrative to reality rather than simply veto. In fact, I may go back and consider removing the brain downvote/gating feature and simply keep brain as a filter of unrelated information... Good VIBE. Save it. Now, is it practical? how do we USE the idea? I think this idea only gets practical in the middle, when brain has 'sideband' to read and curate. It's essentially explaining why. But I guess Pinky needs to produce a coherent reply. QQ: is pinky still mostly just personifying HyDe? Then Brain personifies the Interest Consensus using pinky's initial reply as an initial side-band reason for the interest level. --- Does this flow track as a practical application of the vibe? What could be ambiguous? idea: this vibe also tracks well with pinky's post-evaluation. Let's tag pinky's critique for review as well."*
* **Architectural Consensus:**
  - **Register `VIBE-015`:** *"Two-Mice Sideband Interest Consensus"*.
  - **Mechanism:**
    1. Pinky personifies HyDE / Associative Scouting: generates an enthusiastic first take and wide vector retrieval.
    2. Brain personifies Reality Grounding & Narrative Steering: inspects retrieved vectors, prunes irrelevant chunks (zero negative clutter passed to Deep Thought), and writes a brief sideband rationale explaining *why* the conversation has merit or where it must pivot.
    3. Brain does not downvote interest into oblivion or stall the pipeline; Brain filters noise and steers the narrative back to reality.
    4. Pinky Critic (`FEAT-406` / `FEAT-470`) evaluates the turn end-to-end and proposes continuous calibration.

### Swim Lane 5: Continuous Interest Multiplier Pacing (`FEAT-523` Redefinition)
* **Origin Directive:** *"OMG! excellent find, I expected interest to be a gradient form day one! a hard baked 1500 is WHY I felt interest was broken for so long! To be clear, interest is not a bucket of tokens, it's a multiplier. If interest is .76 and the multiplier is 100 we could suggest a 76 token budget. Fuzzy of course. I was often jarred by how huge deep thought would always reply as. This also means we can be more generous with the routing limits when deep thought or even Brain gets a low interest. Low interest means they talk less, on a smooth gradient to not replying at all. Does this re-define a FEAT?"*
* **Architectural Consensus:**
  - **Redefines `FEAT-523`** (Round Table Token Budgeting & Context Pacing) and augments `FEAT-234` (Pure Scalar Fuel) and `FEAT-418` (Symmetrical Interest Cascade).
  - Abolish the binary clamp (`< 0.3 -> 150, >= 0.3 -> 1500`).
  - Implement continuous scalar pacing:
    $$\text{token\_budget} = \operatorname{clamp}\left(\operatorname{int}(\text{current\_interest} \times \text{multiplier}), \text{min\_floor}, \text{max\_ceiling}\right)$$
    - Configurable in `config/infrastructure.json`:
      - `interest_token_multiplier`: `150` (or `100`–`200` per operator calibration).
      - `min_token_floor`: `32` (or `0` for complete silence / bypass).
      - `max_token_ceiling`: `1500` (reserved strictly for near-1.0 interest deep distillation).
  - Unlocks generous routing: lower interest queries can safely ignite Brain or Deep Thought without generating verbose diatribes.

### Swim Lane 6: BKM-077 1:1 Numbered Swim Lane Rule
* **Origin Directive:** *"I meant swim lanes 1-8. Keep the tracked numbers. Don't make new lanes, relate them, don't combine them. Does this change your BKM update suggestion? ... Disagree. As mentioned above, swim lanes ARE tracked numbers, so we just add a simple rule to stay within the tracked numbers and not munch or group them. tracked numbers can peter out, they have a lifetime, like when we are in agreement."*
* **Architectural Consensus:**
  - Amend `BKM-077` (Tracked Ledger Protocol) with the **1:1 Numbered Swim Lane Invariant**:
    - Tracked dialogue items $1 \dots N$ established during alignment are the canonical swim lanes.
    - Agents are strictly prohibited from consolidating, merging, or munching tracked numbers into generalized thematic buckets (e.g. Lane A/B/C).
    - Swim lanes maintain their individual numbering until they naturally achieve full consensus and peter out.

### Swim Lane 7: Brain Cynical Voice, Narrative Monologue & Replay Harness
* **Origin Directive:** *"I don't think we can find the medium right now. Plan to test this. Brain is thinking out loud, but the voice should be as a critique or agreement with pinky's hot take. I think we need to focus on getting the right voice; first second third person, passive/active, cynical, etc. Also, the gritty details might get muddy here, do we need to rely on Brian to output valid JSON to capture the vote? Do we already have the plumbing in place to do this? Do we FORCE certain outputs to be filled like we do in triage? IIRC this was done, but I want to double check."*
* **Architectural Consensus:**
  - **Voice & Persona:** Brain speaks in 1st person active voice—cynical, rigorous, academically protective, critiquing Pinky's associative leap and pruning irrelevant DNA.
  - **Structured JSON Plumbing:** Confirmed existing in `cognitive_hub.py` and `brain_node.py` (`curator_notes`, `approved_candidate_ids`, `dropped_candidate_ids`).
  - **Short-Circuit Replay Harness:** In Phase 2, develop a focused standalone test harness (`test_brain_voice_replay.py`) to feed historical turns into Brain's prompt, empirically testing voice fidelity, narrative steering, and filtering precision without spinning up full multi-node websocket sessions.

### Swim Lane 8: DNA Governance, Verbatim Provenance & Clean Prompt Engineering
* **Origin Directive:** *"Epistemic Governor, Second derivative Intent bias, merit, interest loop - and any other topics in our conversation that deserve to be saved - we should be capturing this as sprint documentation as well as DNA or DNA updates. Let's avoid making multiple entries for a single idea, and favor updating existing DNA when it fits well. I want to avoid unnecessary DNA creep while still tracking new ideas. Name the ideas we are adding and recommend where they might land in FEAT/INS/BKM/DISC etc. ... Please include original text where applicable, I'd like you to capture where my ideas came from."*
* **Architectural Consensus:**
  - Enforce verbatim provenance tracking: embed user directive text in `quotes: [...]` and `Origin Directive:` headers across all sprint story cards and DNA records.
  - Clean Prompt Engineering Mandate: Eliminate meta-intent words ("fluff", "casual") from semantic intent detection prompts (`FBK_1791400074_4d41d3`). Prompts must evaluate objective semantic alignment between query and evidence, not subjective characterizations.
  - Maintain the consolidated DNA Delta Mapping Table.

---

## 📜 5-Sprint Historical Lookback & Provenance Ledger

| Sprint ID | Theme & Relevant Architectural Discoveries | Connection to Sprint 102.0 |
| :--- | :--- | :--- |
| **SPR-31 / SPR-32** | **Genesis of Interest Loop & Pure Interest Cascade (`feda60a` / `a51d669`)**<br>Origin of `FEAT-234` (Scalar Fuel), `FEAT-418` (Symmetrical Interest Cascade), and `BKM-039`. Established that unaddressed queries default to `NONE`, Pinky takes Turn 1, and escalating interest ignites the Round Table. | Proves that interest was mathematically defined as a continuous scalar fuel, and that the binary clamp (`< 0.3 -> 150 : 1500`) in `cognitive_hub.py` was an implementation drift that subverted the original law. |
| **SPR-92.0** | **Accountability Watchdog & Test Isolation**<br>Hardened standalone verification and health gates across resident nodes. | Provides the rock-solid 8/8 green baseline (`standalone_accountability_watchdog.py`) required for live certification. |
| **SPR-93.0** | **DNA Retrieval Tooling & Swarm Guidance**<br>Unblocked CLaRa-DNA MCP tools for local workers while preserving security fences. | Ensures local workers on KENDER and M5 Air can query DNA without hallucinating requirements. |
| **SPR-94.0** | **Symbolic vs Semantic Rubric Detectors (`BKM-015` / `FEAT-622`)**<br>Partitioned strict schema/AST validation from LLM-Judge semantic evaluation; barred regex from semantic grading. | Directly informs our **Clean Prompt Engineering Mandate**: intent classification must evaluate semantic alignment, never regex meta-keywords. |
| **SPR-95.0** | **Document Spine & Single-Node Proving Ground**<br>Established self-contained version files over fragmented micro-files; verified isolation. | Guides our replay harness design: self-contained prompt fixtures rather than volatile distributed state. |
| **SPR-96.0** | **Brain Information Gatekeeper & Triage Decoupling (`FEAT-540` / `FEAT-635`)**<br>Story 96.2 decoupled Triage and added `target_domains`. Story 96.3 transformed Brain into Information Gatekeeper evaluating Pinky's vectors and pruning clutter. | Direct ancestor of Sprint 102.0. Sprint 96 established the gatekeeper plumbing; Sprint 102 perfects narrative steering and replaces the binary token gate with continuous multiplier pacing. |

---

## 🧬 DNA Delta & Governance Table

| Item / Idea | Classification | Target Location | Action | Verbatim Operator Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Continuous Multiplier Token Pacing** | `FEAT` | `Portfolio_Dev/FeatureTracker.md#FEAT-523` | **Redefine** | *"To be clear, interest is not a bucket of tokens, it's a multiplier. If interest is .76 and the multiplier is 100 we could suggest a 76 token budget... Low interest means they talk less, on a smooth gradient to not replying at all."* |
| **Brain Epistemic Gatekeeper & Narrative Steering** | `FEAT` | `Portfolio_Dev/FeatureTracker.md#FEAT-635` | **Update** | *"Brain can also choose to steer the narrative to reality rather than simply veto. In fact, I may go back and consider removing the brain downvote/gating feature and simply keep brain as a filter of unrelated information."* |
| **Two-Mice Sideband Interest Consensus** | `VIBE` | `Portfolio_Dev/field_notes/dna/vibe_dna.json` (`VIBE-015`) | **New** | *"Sideband - interest isn't just a high/medium/low, it's tracking a live consensus... Pinky personifies HyDE, Brain personifies Interest Consensus using pinky's initial reply as an initial side-band reason."* |
| **1:1 Numbered Swim Lane Rule** | `BKM` | `HomeLabAI/docs/Protocols.md#BKM-077` | **Update** | *"Swim lanes ARE tracked numbers, so we just add a simple rule to stay within the tracked numbers and not munch or group them. Tracked numbers can peter out... when we are in agreement."* |
| **Meta-Vocabulary Intent Decoupling** | `BKM` | `HomeLabAI/docs/Protocols.md#BKM-015` | **Update** | *"Words like fluff are meta intents when we design, but we should be very cautious about embedding a bias by mixing words used to guide the intent detection with actual intent detection."* |
| **L0 Heads-Down Circuit Breaker** | `BKM` | `AGENTS.md` / `BKM-006` | **Affirm** | *"Express permission to cancel a heads down if recommendations deviate significantly or drastically less work is apparently needed, I want to ensure you consult me, as L0."* |

---

## 🚦 Phased Implementation Roadmap

```mermaid
flowchart TD
    subgraph P0 ["🔬 Phase 0: Pre-Grounding Audit & Adversarial Oracle Gate"]
        P0_1["Story 102.0: 5-Sprint Lookback & Pre-Flight Ledger"]
        P0_2["Story 102.1: Cloud Oracle Adversarial Pre-Pass (delegate.py --oracle)"]
        P0_3["Story 102.2: L0 Checkpoint & Consensus Review"]
    end

    subgraph P1 ["🔧 Phase 1: Plumbing & Continuous Multiplier Pacing"]
        P1_1["Story 102.3: Configurable Multiplier Token Budget in infrastructure.json"]
        P1_2["Story 102.4: CognitiveHub Multiplier Pacing & Routing Decoupling"]
        P1_3["Story 102.5: Clean Prompt Meta-Vocabulary Purge (cognitive_hub.py)"]
        P1_4["Story 102.6: Phase 1 Atomic Git Checkpoint & Oracle Audit"]
    end

    subgraph P2 ["🎭 Phase 2: Narrative Steering, Voice & Replay Harness"]
        P2_1["Story 102.7: Brain Cynical Voice & Narrative Steering Prompt (brain_node.py)"]
        P2_2["Story 102.8: Two-Mice Sideband Consensus & RAG Filter Logic (VIBE-015)"]
        P2_3["Story 102.9: Standalone Brain Voice & Replay Test Harness"]
        P2_4["Story 102.10: Phase 2 Atomic Git Checkpoint & Oracle Audit"]
    end

    subgraph P3 ["🛡️ Phase 3: Live Silicon Certification & Watchdog Verification"]
        P3_1["Story 102.11: Multi-Turn Conversation Live Certification (M5 Air + KENDER 4090)"]
        P3_2["Story 102.12: Standalone Watchdog 8/8 Green Certification"]
        P3_3["Story 102.13: Final Phase 3 Git Checkpoint & Sprint Completion"]
    end

    P0_1 --> P0_2 --> P0_3
    P0_3 -->|L0 Approval| P1_1
    P1_1 --> P1_2 --> P1_3 --> P1_4
    P1_4 -->|Oracle Pass| P2_1
    P2_1 --> P2_2 --> P2_3 --> P2_4
    P2_4 -->|Oracle Pass| P3_1
    P3_1 --> P3_2 --> P3_3
```

---

## 🏛️ Delegation Governance Matrix & Tier Assignment Criteria (`BKM-049`)

### Criteria for Delegation Tiers
In adherence to `BKM-049` (Tri-Loop Delegation) and `BKM-080` (Ask-Oracle Protocol), tasks are partitioned across three tiers based on strict architectural criteria:

| Tier | Assigned Runner / Silicon Node | Task Characteristics & Assignment Criteria |
| :--- | :--- | :--- |
| **`[SWARM:LOCAL]`** | Node KENDER (RTX 4090 :11434) / Node Brain (Apple M5 Air :8002) via `delegate.py --mode local` | **Surgical & Deterministic Implementation:**<br>• Clear 4-anchor contracts (known target file, line bounds, and expected input/output).<br>• JSON configuration updates, isolated Python method refactors, and prompt string updates.<br>• Local pytest execution and offline replay harness development.<br>• Zero cloud API spend; sovereign local iteration. |
| **`[SWARM:CLOUD]`** | Frontier Cloud Models (Nemotron-120B / Claude / GPT-4o) via `delegate.py --oracle` or `--mode cloud` | **Adversarial Auditing & High-Ambiguity Synthesis:**<br>• Adversarial review gates: stress-testing edge cases, mathematical formulas, regression analysis, and circular dependency checks.<br>• Complex multi-file state machines where local models exceed context or ambiguity ceilings.<br>• Fallback escalation if `[SWARM:LOCAL]` exhausts the 3-attempt diagnostic retry loop (`BKM-049`). |
| **`[AGY:PRIMARY]`** | Antigravity Orchestrator (L1 / Primary Agent) | **Orchestration, Governance & Physical Certification:**<br>• Pre-grounding audits, sprint plan authoring, and architectural alignment with L0.<br>• Atomic `git commit` checkpoint enforcement between sprint phases.<br>• Final Live Validation Mandate (`BKM-024`): running against active resident daemons and physical silicon ports (`:8088`, `:8002`, `:8000`), which containerized subagents cannot perform.<br>• Consultations and pause gates with the Human Operator (L0). |

---

### Sprint 102 Delegation Matrix

| Story ID | Story Title | Assigned Owner | Tool / Runner | Success Criteria |
| :--- | :--- | :--- | :--- | :--- |
| **Story 102.0** | 5-Sprint Historical Lookback & Pre-Flight Ledger | `[AGY:PRIMARY]` | Direct Analysis | Lookback synthesized into sprint plan |
| **Story 102.1** | Cloud Oracle Adversarial Pre-Pass | `[SWARM:CLOUD]` | `delegate.py --oracle` | `ORACLE_REVIEW_SPRINT_102.md` generated |
| **Story 102.2** | L0 Checkpoint & Consensus Review | `[AGY:PRIMARY]` | L0 Consultation | Operator greenlight before Phase 1 |
| **Story 102.3** | Configurable Multiplier & Node Profiles in Config | `[SWARM:LOCAL]` | `delegate.py --mode local` | Valid `infrastructure.json` with pacing keys |
| **Story 102.4** | CognitiveHub Multiplier Pacing & Vibe Decoupling | `[SWARM:LOCAL]` | `delegate.py --mode local` | `test_cognitive_hub.py` passes 100% green |
| **Story 102.5** | Clean Prompt Meta-Vocabulary Purge | `[SWARM:LOCAL]` | `delegate.py --mode local` | `test_vector_pre_triage.py` passes 5/5 green |
| **Story 102.6** | Phase 1 Atomic Git Checkpoint & Re-Evaluation | `[AGY:PRIMARY]` | Git CLI & Oracle Check | Clean working tree; atomic commit |
| **Story 102.7** | Brain Cynical Voice & Narrative Steering Prompt | `[SWARM:LOCAL]` | `delegate.py --mode local` | `test_brain_gatekeeper.py` passes green |
| **Story 102.8** | Two-Mice Sideband Consensus & RAG Filter Logic | `[SWARM:LOCAL]` | `delegate.py --mode local` | `test_two_mice_handover.py` passes 16/16 green |
| **Story 102.9** | Standalone Brain Voice & Replay Test Harness | `[SWARM:LOCAL]` | `delegate.py --mode local` | `test_brain_voice_replay.py` executes in <2s |
| **Story 102.10** | Phase 2 Atomic Git Checkpoint & Re-Evaluation | `[AGY:PRIMARY]` | Git CLI & Oracle Check | Clean working tree; atomic commit |
| **Story 102.11** | Multi-Turn Live Silicon Validation (`BKM-024`) | `[AGY:PRIMARY]` | Live Daemon Probe | Live turns exhibit proportional token pacing |
| **Story 102.12** | Standalone Watchdog 8/8 Green Certification | `[AGY:PRIMARY]` | Watchdog Runner | `standalone_accountability_watchdog.py` PASS |
| **Story 102.13** | Final Sprint 102 Certification & DNA Sync | `[AGY:PRIMARY]` | ChromaDB & Git Sync | `FeatureTracker.md` and ChromaDB synchronized |

---

## 📋 Sprint Stories & 4-Anchor Specifications

### 🔬 Phase 0: Pre-Grounding Audit & Adversarial Oracle Gate

#### Story 102.0: 5-Sprint Historical Lookback & Pre-Flight Mistakes-Avoided Ledger
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Status:** `READY FOR EXECUTION`
* **Context & Mechanism:** Conduct an in-depth audit across Sprints 92–96 and Sprint 31/FEAT-418. Synthesize historical failure modes (e.g. `FBK_1791400074_4d41d3` meta-intent leakage, Sprint 96 triage coupling) into the pre-flight ledger.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `Portfolio_Dev/docs/sprints/active/SPRINT_PLAN_SPR_102_0.md`.
  * **Anchor 2 (Verification Command):** `test -f Portfolio_Dev/docs/sprints/active/SPRINT_PLAN_SPR_102_0.md && grep -q "Historical Lookback" Portfolio_Dev/docs/sprints/active/SPRINT_PLAN_SPR_102_0.md`.
  * **Anchor 3 (Silicon Invariant):** Zero stale assumptions; 100% verified historical commit anchors.
  * **Anchor 4 (DNA Links):** `[BKM-081]`, `[BKM-082]`, `[INS-047]`.

#### Story 102.1: Cloud Oracle Adversarial Pre-Pass
* **Assigned Owner:** `[SWARM:CLOUD]`
* **Status:** `READY FOR EXECUTION`
* **Context & Mechanism:** Execute `python3 delegate.py --oracle` against the proposed Sprint 102 plan. The Oracle evaluates edge cases in the continuous multiplier formula, potential deadlocks in Brain RAG filtering, and prompt regression risks.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `Portfolio_Dev/docs/sprints/active/ORACLE_REVIEW_SPRINT_102.md`.
  * **Anchor 2 (Verification Command):** `python3 /home/jallred/Dev_Lab/delegate.py --oracle`.
  * **Anchor 3 (Silicon Invariant):** Cloud model completes comprehensive adversarial review; output saved to disk.
  * **Anchor 4 (DNA Links):** `[BKM-061]`, `[BKM-080]`.

#### Story 102.2: L0 Checkpoint & Consensus Review
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Status:** `GATE (PAUSE FOR USER REVIEW)`
* **Context & Mechanism:** Present Oracle findings and Pre-Grounding audit to L0. If Oracle recommendations deviate significantly or work simplifies drastically, consult L0 before entering Phase 1.

---

### 🔧 Phase 1: Plumbing & Continuous Multiplier Pacing

#### Story 102.3: Configurable Multiplier Token Budget & Node Profiles in `infrastructure.json`
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Status:** `PENDING PHASE 0`
* **Context & Mechanism:** Add declarative configuration keys for continuous interest token budgeting and node generation profiles in `HomeLabAI/config/infrastructure.json`:
  ```json
  "interest_pacing": {
    "enabled": true,
    "token_multiplier": 150,
    "min_token_floor": 32,
    "max_token_ceiling": 1500
  },
  "node_pacing_profiles": {
    "pinky": { "default_temp": 0.7, "terse_temp": 0.4, "repetition_penalty": 1.15 },
    "brain": { "default_temp": 0.3, "repetition_penalty": 1.12 },
    "thought": { "default_temp": 0.2, "repetition_penalty": 1.10 }
  }
  ```
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `HomeLabAI/config/infrastructure.json`.
  * **Anchor 2 (Verification Command):** `python3 -c "import json; d=json.load(open('HomeLabAI/config/infrastructure.json')); assert 'interest_pacing' in d and 'node_pacing_profiles' in d"`.
  * **Anchor 3 (Silicon Invariant):** Valid JSON syntax; zero daemon reload failure.
  * **Anchor 4 (DNA Links):** `[FEAT-523]`, `[FEAT-234]`.

#### Story 102.4: CognitiveHub Multiplier Pacing & String Vibe Decoupling
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Status:** `PENDING PHASE 0`
* **Context & Mechanism:** Refactor `HomeLabAI/src/logic/cognitive_hub.py` to decouple hardcoded string branches (`"CASUAL"` / `"TECHNICAL"`):
  1. **Token Budgeting (L1104–L1118):** Replace binary ternary clamp with continuous multiplier:
     ```python
     # [FEAT-523] Continuous Multiplier Pacing
     pacing_cfg = getattr(self, "config", {}).get("interest_pacing", {})
     multiplier = pacing_cfg.get("token_multiplier", 150)
     min_floor = pacing_cfg.get("min_token_floor", 32)
     max_ceiling = pacing_cfg.get("max_token_ceiling", 1500)
     current_interest = getattr(self, "current_interest", 0.5)

     token_budget = max_tokens if max_tokens is not None else (
         128 if is_triage else max(min_floor, min(max_ceiling, int(current_interest * multiplier)))
     )
     ```
  2. **RAG Prefetch Decoupling (L1928–L1934):** Replace `and vibe != "CASUAL"` with `len(getattr(self, "current_target_domains", [])) > 0`. Gate prefetch on domain relevance, not vibe strings.
  3. **Generation Parameters Decoupling (L1894–L1895, L1937–L1938):** Replace hardcoded Python ternaries (`p_temp = 0.4 if vibe == "CASUAL" else 0.7`) by reading values from `node_pacing_profiles` in `infrastructure.json`.
  4. **Runaway Loop Decoupling:** Enforce stop tokens (`\n\n`, user turn tokens) and calibrated repetition penalties rather than coarse token truncation.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `HomeLabAI/src/logic/cognitive_hub.py`.
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_cognitive_hub.py -v`.
  * **Anchor 3 (Silicon Invariant):** Turns scale token budget smoothly with `current_interest`; zero string checks on `"CASUAL"` for RAG prefetch or token budgets.
  * **Anchor 4 (DNA Links):** `[FEAT-523]`, `[FEAT-234]`, `[FEAT-418]`, `[FEAT-457]`.

#### Story 102.5: Clean Prompt Meta-Vocabulary Purge
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Status:** `PENDING PHASE 0`
* **Context & Mechanism:** Audit and sanitize prompt strings in `HomeLabAI/src/logic/cognitive_hub.py` and `HomeLabAI/src/logic/speculative_triage.py`. Remove meta-intent labels ("fluff", "casual chatter") that artificially bias regex/intent classification (`FBK_1791400074_4d41d3`). Prompts evaluate semantic alignment against facts only.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `HomeLabAI/src/logic/cognitive_hub.py`, `HomeLabAI/src/logic/speculative_triage.py`.
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_vector_pre_triage.py -v`.
  * **Anchor 3 (Silicon Invariant):** Zero false-positive casual classifications on technical regex queries.
  * **Anchor 4 (DNA Links):** `[BKM-015]`, `[WIS-487]`.

#### Story 102.6: Phase 1 Atomic Git Checkpoint & Oracle Audit
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Status:** `PENDING PHASE 1`
* **Context & Mechanism:** Run local tests, verify clean git status, and execute an atomic `git commit` checkpoint: `feat(hub): implement continuous interest multiplier pacing and vibe decoupling [FEAT-523]`. Trigger an intermediate Oracle review if necessary.

---

### 🎭 Phase 2: Narrative Steering, Voice & Replay Harness

#### Story 102.7: Brain Cynical Voice & Narrative Steering Prompt
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Status:** `PENDING PHASE 1`
* **Context & Mechanism:** Update `BRAIN_SYSTEM_PROMPT` in `HomeLabAI/src/nodes/brain_node.py`. Brain's role is refined: 1st person cynical evaluator who critiques Pinky's take, steers the narrative back to reality, and filters unrelated RAG without downvoting or killing the turn.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `HomeLabAI/src/nodes/brain_node.py`.
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_brain_gatekeeper.py -v`.
  * **Anchor 3 (Silicon Invariant):** Brain outputs valid structured JSON containing narrative steering commentary and filtered ID lists.
  * **Anchor 4 (DNA Links):** `[FEAT-635]`, `[VIBE-015]`.

#### Story 102.8: Two-Mice Sideband Consensus & RAG Filter Logic (`VIBE-015`)
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Status:** `PENDING PHASE 1`
* **Context & Mechanism:** Wire Brain's narrative steering and filtered RAG IDs directly into Deep Thought's prompt assembly in `cognitive_hub.py`. Filtered/unrelated chunks are strictly excluded from Deep Thought's context, eliminating negative clutter. Brain's sideband rationale is logged in telemetry and attached as a high-density curator note.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `HomeLabAI/src/logic/cognitive_hub.py`.
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_two_mice_handover.py -v`.
  * **Anchor 3 (Silicon Invariant):** Deep Thought prompt contains 0% dropped candidate tokens; receives verified bedrock and steering notes.
  * **Anchor 4 (DNA Links):** `[VIBE-015]`, `[FEAT-635]`, `[FEAT-489]`.

#### Story 102.9: Standalone Brain Voice & Replay Test Harness
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Status:** `PENDING PHASE 1`
* **Context & Mechanism:** Build `HomeLabAI/src/tests/test_brain_voice_replay.py`. Create a lightweight offline harness that feeds sample multi-turn queries and Pinky responses to Brain, evaluating voice cynicism, narrative steering, and filtering precision without full websocket overhead.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `HomeLabAI/src/tests/test_brain_voice_replay.py`.
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_brain_voice_replay.py -v`.
  * **Anchor 3 (Silicon Invariant):** Replay harness executes in $< 1.5\text{s}$ for local mock passes.
  * **Anchor 4 (DNA Links):** `[BKM-024]`, `[FEAT-635]`.

#### Story 102.10: Phase 2 Atomic Git Checkpoint & Oracle Audit
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Status:** `PENDING PHASE 2`
* **Context & Mechanism:** Verify all unit tests pass, commit Phase 2 atomically: `feat(brain): implement narrative steering and sideband consensus [VIBE-015] [FEAT-635]`.

---

### 🛡️ Phase 3: Live Silicon Certification & Watchdog Verification

#### Story 102.11: Multi-Turn Conversation Live Certification
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Status:** `PENDING PHASE 2`
* **Context & Mechanism:** Run live multi-turn test session against active running daemons across Node Brain (M5 Air oMLX) and Node KENDER (RTX 4090 Deep Thought). Verify continuous token scaling, Brain narrative steering, and absence of runaway 1500-token diatribes.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `HomeLabAI/run/foyer_journal.jsonl`.
  * **Anchor 2 (Verification Command):** `python3 HomeLabAI/src/tests/probe_round_table_accountability.py`.
  * **Anchor 3 (Silicon Invariant):** Live responses complete with smooth token counts matching interest; zero daemon crash.
  * **Anchor 4 (DNA Links):** `[BKM-024]`, `[FEAT-523]`.

#### Story 102.12: Standalone Watchdog 8/8 Green Certification
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Status:** `PENDING PHASE 2`
* **Context & Mechanism:** Execute `standalone_accountability_watchdog.py`. Verify 8/8 checks pass GREEN with 0 failures or stale states.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `HomeLabAI/run/watchdog_report.json`.
  * **Anchor 2 (Verification Command):** `python3 HomeLabAI/src/tests/standalone_accountability_watchdog.py`.
  * **Anchor 3 (Silicon Invariant):** 8/8 checks report PASS; `overall_status: PASS`.
  * **Anchor 4 (DNA Links):** `[BKM-024]`, `[BKM-066]`.

#### Story 102.13: Final Phase 3 Git Checkpoint & Sprint Completion
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Status:** `COMPLETED`
* **Context & Mechanism:** Final sync of `FeatureTracker.md` and ChromaDB DNA. Atomic commit: `chore(sprint): complete Sprint 102.0 certification`. Update sprint status to `COMPLETED & CERTIFIED`.

---

### 🌐 Phase 4: Telemetry Synthesis, Dashboard Unification & Clean Delegation Tracking

#### Story 102.14: Dual Live & Deploy Feed Publisher Hook in `delegate.py` and `build_site.py` (`[FEAT-552]` / `[FEAT-064]`)
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Status:** `READY FOR EXECUTION`
* **Context & Mechanism:**
  1. In `HomeLabAI/src/tests/delegate.py`, invoke `export_web_telemetry()` immediately upon writing to `delegation_ledger.jsonl`. This gives zero-delay live updates whenever local, cloud, or oracle runs complete.
  2. In `Portfolio_Dev/field_notes/build_site.py`, call `export_web_telemetry()` right before `deploy_to_airlock()`, guaranteeing the feed is freshly compiled and synced to `www_deploy/data/delegation_runs.json`.
  3. Update `FeatureTracker.md` under `[FEAT-552]` to document this dual publisher pattern.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `HomeLabAI/src/tests/delegate.py`, `Portfolio_Dev/field_notes/build_site.py`, `Portfolio_Dev/FeatureTracker.md`.
  * **Anchor 2 (Verification Command):** `python3 Portfolio_Dev/field_notes/build_site.py --no-verify --no-js-lint && test -f www_deploy/data/delegation_runs.json`.
  * **Anchor 3 (Silicon Invariant):** Zero-delay update to `delegation_runs.json` upon delegate completion; airlock receives identical payload.
  * **Anchor 4 (DNA Links):** `[FEAT-552]`, `[FEAT-064]`, `[BKM-049]`.

#### Story 102.15: Tab Nomenclature Cleanup, Compact Button Styling & ROI Slider Purge
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Status:** `READY FOR EXECUTION`
* **Context & Mechanism:**
  1. In `Portfolio_Dev/field_notes/benchmarks.html`, clean and compact the tab names:
     - `Live Round Table` (was `⏱️ LIVE ROUND TABLE ELAPSED TIME`)
     - `Model Throughput` (was `🏛️ SILICON ARENA & WORKLOAD`)
     - `Sprint Delegation` (was `🐝 SWARM DELEGATION & SOVEREIGN GAINS`)
  2. In `Portfolio_Dev/field_notes/style.css`, squish tab button padding (`6px 12px`, `font-size: 0.8rem`, `letter-spacing: normal`).
  3. Purge Tab 3 (`#tab-roi` and Hypothetical Scaling Calculator) from `benchmarks.html` and `benchmarks.js`.
  4. Mark `[FEAT-426]` in `Portfolio_Dev/FeatureTracker.md` as `DEFEATURED (Sprint 102) — Superseded by [FEAT-525]`.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `Portfolio_Dev/field_notes/benchmarks.html`, `Portfolio_Dev/field_notes/benchmarks.js`, `Portfolio_Dev/field_notes/style.css`, `Portfolio_Dev/FeatureTracker.md`.
  * **Anchor 2 (Verification Command):** `node --check Portfolio_Dev/field_notes/benchmarks.js && ! grep -q "tab-roi" Portfolio_Dev/field_notes/benchmarks.html`.
  * **Anchor 3 (Silicon Invariant):** Clean DOM layout without JS errors; 3 unified tabs active.
  * **Anchor 4 (DNA Links):** `[FEAT-525]`, `[FEAT-426]`, `[FEAT-494]`.

#### Story 102.16: Codify BKM-049 §8 (Canonical Story Argument Law) & Multi-Format Ingestion in `sprint_telemetry.py`
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Status:** `READY FOR EXECUTION`
* **Context & Mechanism:**
  1. In `HomeLabAI/docs/Protocols.md`, codify `BKM-049 §8` mandating canonical dotted story IDs (`--story 102.1`, `--story 102.9`) across all dispatch commands and JIT checkpoint calls.
  2. In `HomeLabAI/src/infra/sprint_telemetry.py`, harden `export_web_telemetry()`:
     - Normalize story keys across both dotted (`102.9`) and un-dotted (`1029`) formats so JIT checkpoint stubs match authoritative `delegate.py` records.
     - Suppress unpopulated stub records when an authoritative record with matching story exists.
     - Extract clean story, sprint, and titles for all historical entries.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `HomeLabAI/docs/Protocols.md`, `HomeLabAI/src/infra/sprint_telemetry.py`.
  * **Anchor 2 (Verification Command):** `python3 HomeLabAI/src/infra/sprint_telemetry.py --export-web && python3 -c "import json; d=json.load(open('Portfolio_Dev/field_notes/data/delegation_runs.json')); s102=[r for r in d['runs'] if r['sprint']=='102']; assert all(r['title'] and r['tier'] for r in s102), 'Blank stubs detected in Sprint 102'; print('PASS: All Sprint 102 runs decorated clean')"`
  * **Anchor 3 (Silicon Invariant):** Zero un-decorated JIT stubs; 100% clean story, title, tier, and token metrics.
  * **Anchor 4 (DNA Links):** `[BKM-049]`, `[BKM-081]`, `[FEAT-552]`.

#### Story 102.17: Delegation Table Mobile Optimization & Blackboard Header Ergonomics
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Status:** `READY FOR EXECUTION`
* **Context & Mechanism:**
  1. In `Portfolio_Dev/field_notes/benchmarks.js`:
     - Collapse `Mode / Tier` column to strictly `Tier` (`r.tier || '—'`).
     - In `renderBlackboardLedger()`, replace redundant static badges (`[FULL ROUND TABLE]`, `[CONTEXT_SCOPE_LONG]`) with a clean timestamp including date (`YYYY-MM-DD HH:MM:SS` from `turn.timestamp`) and turn duration.
  2. In `Portfolio_Dev/field_notes/style.css`:
     - Add responsive styles for `#delegation-runs-table` (`@media (max-width: 768px)` hides chevron and duration, allows title wrapping).
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `Portfolio_Dev/field_notes/benchmarks.js`, `Portfolio_Dev/field_notes/style.css`.
  * **Anchor 2 (Verification Command):** `node --check Portfolio_Dev/field_notes/benchmarks.js && ! grep -q "CONTEXT_SCOPE_LONG" Portfolio_Dev/field_notes/benchmarks.js`.
  * **Anchor 3 (Silicon Invariant):** Clean, date-stamped accordion headers; responsive table layout on mobile.
  * **Anchor 4 (DNA Links):** `[FEAT-525]`, `[FEAT-526]`.

#### Story 102.18: Model Throughput Live Telemetry Planning & Swarm Specification
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Status:** `READY FOR EXECUTION`
* **Context & Mechanism:** Document architectural specification in `Portfolio_Dev/docs/sprints/active/SPRINT_PLAN_SPR_102_0.md` detailing how `live_usage_stream.jsonl` will feed real observed Tok/s and TTFT into a multi-seat Canvas trend graph in a subsequent sprint story, replacing synthetic `bench_models.py` pings.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `Portfolio_Dev/docs/sprints/active/SPRINT_PLAN_SPR_102_0.md`.
  * **Anchor 2 (Verification Command):** `grep -q "Model Throughput Live Telemetry Specification" Portfolio_Dev/docs/sprints/active/SPRINT_PLAN_SPR_102_0.md`.
  * **Anchor 3 (Silicon Invariant):** Formal spec approved for local swarm delegation.
  * **Anchor 4 (DNA Links):** `[FEAT-495]`, `[FEAT-494]`, `[INS-047]`.
