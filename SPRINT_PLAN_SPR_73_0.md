# 🚀 SPRINT PLAN 73.0: Triage Rubric Health, Scalar Decoupling, BKM/Ledger DNA & Discourse Intent Grounding

**Sprint ID:** `SPR_73_0`  
**Theme:** Triage Schema & Rubric Hygiene, Scalar Continuous Decoupling, Multi-Collection BKM/Blackboard Vector Probe, and Discourse-Aware Meta Intent Grounding  
**Status:** PROPOSED / DRAFT  
**Parent Framework:** BKM-015 (Semantic Anchor Protocol), BKM-035 (Feedback Capture), BKM-046 (CLaRa-DNA Fast-Path)  
**Execution Mode:** Full AGY Mode (Direct In-Context Execution)  
**Target Hardware Nodes:** z87-Linux (RTX 2080 Ti Local vLLM Llama-3.2-3B Unified Base), KENDER (RTX 4090 Deep Thought), ChromaDB Port 8001 (CLaRa-DNA)

---

## 🧭 Executive Summary & Core Engineering Directives

Sprint 73.0 targets the root causes of triage bias, scalar clamping, and missed feedback discovered during live conversational validation:
1. **Scalar Decoupling & Continuous Guidance (`FEAT-544`):** Replace rigid single-point exemplar numbers (`casual=0.9, intrigue=0.1`) with continuous 3-tier semantic rubrics so the 3B model scores along a spectrum rather than snapping to binary extremes.
2. **CLaRa-DNA Vector Expansion (`FEAT-545`):** Expand `vector_pre_triage.py` to query `behavioral_dna` (BKMs / Protocols) and `blackboard_ledger_dna` (live conversation history) to close the "BKM is META" gap and recognize previous-turn references.
3. **Discourse-Aware Intent & Semantic Meta Grounding (`FEAT-546`):** Ground `inferred_intent` as a concise semantic action phrase and explicitly recognize implicit supervisory feedback, prompt tuning, and turn-referential comments without requiring the literal `"feedback:"` keyword.
4. **Brain Generation Clamp & Anti-Recursion Stop Tokens (`FEAT-547`):** Clamp recursive `<thought>` loops and add stop-token boundaries to eliminate runaway "Visible Consensus" spam.

---

## 📊 Triage Schema & Rubric Health Matrix

| Triage Field | Type | Health | Current Failure Mode | Root Cause | Proposed Sprint 73 Fix |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **`vibe`** | Enum (`CASUAL`, `WYWO`, `HISTORICAL`, `OPERATIONAL`, `FORENSIC`, `META`, `TECHNICAL`) | ⚠️ **POOR** | Snaps to `CASUAL` on conversational feedback or meta discussions about prompting. | Coupled to `PINKY` and `casual=0.9` in prompt examples. Lacks implicit feedback exemplars. | Decouple from addressee. Add explicit criteria for implicit feedback / meta lab discussion. |
| **`domain`** | Enum (`work_history`, `acme_lab_history`, `exp_tlm`, `exp_for`, `feedback`, `lab_internal`, etc.) | ⚠️ **FAIR** | Defaults to `unknown` or `standard` when query is conversational. | Tightly coupled with `vibe` in prompt templates. | Decouple domain so a `CASUAL` vibe can target `work_history`, and a `META` vibe can target `lab_internal`. |
| **`addressed_to`** | Enum (`PINKY`, `BRAIN`, `MICE`, `SYSTEM`, `NONE`) | ⚠️ **POOR** | Over-biases to `PINKY` on almost all conversational queries. | Model treats `addressed_to` as synonymous with `vibe` (Casual $\rightarrow$ Pinky, Tech $\rightarrow$ Brain). | Clarify role definitions: `PINKY` (Interface/Dialogue), `BRAIN` (Deep RAG/Analysis), `SYSTEM` (Control Plane / Meta). |
| **`casual`** | Float (`0.0–1.0`) | ❌ **CRITICAL** | Model outputs only `0.9` or `0.1` (binary snap). | Hardcoded exemplar values in prompt caused few-shot pattern copying. | Define a 3-tier continuous scoring guide (High $\ge 0.8$, Mid $0.4–0.6$, Low $\le 0.2$). |
| **`intrigue`** | Float (`0.0–1.0`) | ❌ **CRITICAL** | Defaults to `0.0` or `0.1` unless historical keyword present. | "Intrigue" is undefined in prompt; model treats it as "is historical". | Define as conceptual novelty / depth of inquiry (e.g. meta-reflections and architectural queries = High intrigue). |
| **`importance`** | Float (`0.0–1.0`) | ⚠️ **FAIR** | Skewed low ($0.1$) on conversational feedback. | Inherits low importance from `CASUAL` classification. | Tie importance to operational and supervisory impact. |
| **`inferred_intent`** | Freeform String | ⚠️ **POOR** | Model outputs generic single words (`"greeting"`, `"query"`, `"inform"`). | Undefined schema semantics; downstream code only checks for `"morning_briefing"`. | Define as a concise 3–6 word action phrase (e.g. `"adjust_triage_scalars"`, `"critique_verbosity"`). |

---

## 🧬 Sprint 73 Stories & Specifications

### 🧬 Story 7301: Continuous Scalar Rubrics & Axis Decoupling (`[FEAT-544]`)
* **Objective:** Decouple `vibe`, `domain`, `addressed_to`, and scalars (`casual`, `intrigue`, `importance`) into independent orthogonal dimensions.
* **Mechanism:**
  - Remove coupled exemplars from `triage_mode_context` and `LAB_SYSTEM_PROMPT`.
  - Provide continuous tier guidelines for scalars:
    - **`casual`:** 0.8–1.0 (pure pleasantry), 0.4–0.7 (conversational engineering/meta banter), 0.0–0.3 (direct diagnostic commands/queries).
    - **`intrigue`:** 0.7–1.0 (architectural exploration, systemic feedback, novel connections), 0.4–0.6 (standard retrieval), 0.0–0.3 (simple status checks/greetings).
    - **`importance`:** 0.8–1.0 (supervisory feedback, errors, critical telemetry), 0.4–0.7 (technical queries), 0.0–0.3 (casual banter).

### 🧬 Story 7302: Multi-Collection CLaRa Vector Probe Expansion (`[FEAT-545]`)
* **Objective:** Include `behavioral_dna` (BKMs / Protocols) and `blackboard_ledger_dna` (chat/turn history) in `vector_pre_triage.py`.
* **Mechanism:**
  - Update `PRE_TRIAGE_COLLECTIONS = ["behavioral_dna", "feature_dna", "long_term_wisdom", "career_ledger", "blackboard_ledger_dna"]`.
  - When a query matches BKMs or recent conversation turns, inject `[SEMANTIC_ANCHOR_HINT: BKM_PROTOCOL]` or `[SEMANTIC_ANCHOR_HINT: RECENT_CONVERSATION_TURN]`, preventing the false `No internal lab match -> Likely casual` suppression trap.

### 🧬 Story 7303: Discourse-Aware Semantic Meta Grounding (`[FEAT-546]`)
* **Objective:** Ground implicit supervisory feedback, prompt discussions, and previous-turn references without requiring literal keyword prefixes.
* **Mechanism:**
  - Add explicit discourse rules to Triage prompt:
    - Critiques of assistant style, verbosity, repetition, or hallucination $\rightarrow$ `vibe: "META"`, `domain: "feedback"`, `addressed_to: "SYSTEM"`.
    - Discussions regarding prompt engineering, scalars, JIT, or lab routing $\rightarrow$ `vibe: "META"`, `domain: "lab_internal"`.
    - Turn-referential statements (*"you didn't catch that"*, *"in the previous turn"*) $\rightarrow$ inspect `blackboard_ledger_dna` and route to `lab_internal` / `feedback`.

### 🧬 Story 7304: Brain Generation Clamp & Consensus Anti-Recursion (`[FEAT-547]`)
* **Objective:** Terminate runaway recursive `<thought>` loops in Brain node responses.
* **Mechanism:**
  - Add strict stop tokens to Brain generation requests: `["\n\nUser:", "\n\nPinky:", "\n\n[BRAIN]", "\n---\n\n**Visible Consensus**"]`.
  - Enforce max response token bounding and repetition penalty on Brain resident node.

