# Sprint 108 Phase 3 Retrospective: Empirical Silicon Probing & Prompt MO Calibration

**Feature Anchor:** `[FEAT-668]` / `[BKM-087]` / `[BKM-088]` / `[BKM-089]` / `[BKM-090]` / `[FEAT-675]`  
**Date:** 2026-10-26  
**Authors:** Jason Allred & Antigravity (`[AGY:PRIMARY]`)  
**Scope:** Interactive Co-Pilot Prompt Engineering & Modus Operandi Calibration across Stages 0–6 of the Two-Mice Waterfall on Live Physical Silicon (`:8088` local vLLM RTX 2080 Ti, `:8001` ChromaDB HTTP, `:8000` M5 Air oMLX, `:11434` Kender RTX 4090).

---

## 1. Executive Summary & Epistemic Transformation

Sprint 108 Phase 3 achieved a fundamental paradigm shift in how Acme Lab engineers and certifies its cognitive pipeline: **from theoretical prompt speculation and brittle keyword regexes to empirical, live-silicon calibration backed by Modus Operandi (MO) criteria and $N=5$ stochastic verification.**

Over 400 live inference calls were executed across the Two-Mice Waterfall. Instead of guessing how models behave, we observed real failure modes under temperature ($T=0.7$) and causal token generation, uncovering profound subtle breaking points that could never be caught by static unit tests:
1. **The Causal Token-Order Phenomenon in Gatekeeping**: When asked to output verdict-first (`- CHUNK-1: KEEP/DROP — reason`), causal 3B models emit `KEEP` first and then post-hoc hallucinate evidence (`"matches Kubernetes"`) to justify their early token. Inverting the token order to **Evidence-Before-Verdict** (`Anchor Match: ...; Anchor Missing: ... => KEEP|DROP`) forced deterministic truth evaluation (`5/5` `0/3 KEEP` on missing technology).
2. **The Temporal Ambiguity Collision on `WYWO`**: When an overnight standup presented a past 2021 platform milestone without explicit temporal framing, 27B models refused to answer (`"2021 != overnight"`), while 3B models hallucinated that the team integrated 2021 hardware last night. Explicitly framing the event as *reading and indexing a past archive memory during last night's dream cycle* resolved both failure modes simultaneously.
3. **The Addressee Inversion Trap**: Directing Pinky to speak *"alongside your partner The Brain"* caused 3B models to turn around and address Brain in the 2nd person (`"Okay, Brain..."`) instead of addressing Jason. Enforcing strict 2nd-person Jason / 3rd-person Brain framing restored proper console delivery.
4. **Mental-Math Hallucinations on Numeric Summaries**: Instructing a 3B voice model to paraphrase quantitative trade-offs caused it to fabricate mathematical ratios (`"saving 57 times the energy"`) and cross-attribute metrics (attributing the 2080 Ti's 150ms TTFT to the M5 Air). Constraining the prompt to contrast exact cited metric pairs eliminated all numerical hallucinations.
5. **The Entailment Capability Cliff**: Live probing revealed that 3B local models cannot reliably function as out-of-band entailment judges (`0%` specificity; pedantic false-positive alarms on rounding and punctuation). In contrast, Sovereign 27B models (`M5_AIR` / `KENDER`) achieved `12/12` (`100%`) precision and recall, establishing the rule that Entailment Auditing runs strictly on warm 27B silicon and stays completely silent on faithful turns.

---

## 2. Stage-by-Stage Empirical Discoveries & Prompt Invariants

### Stage 1: Triage Engine (`triage_engine.py` & `triage_policy.json`)
* **Live Discovery**: Unadorned nouns (`"Telemetry."`) caused `OPERATIONAL` queries to over-trigger on historical architecture notes (e.g. Purley 2018 PECI/RAPL notes). Hardcoded regexes (`_GREETING_RE`, `_WYWO_RE`, `_META_KEYWORDS`) violated `BKM-015` and masked model behavior.
* **Calibrated Solution**:
  * Established canonical **9-Vibe Master Taxonomy**: `CASUAL`, `UNCLEAR`, `WYWO`, `HISTORICAL`, `OPERATIONAL`, `FORENSIC`, `META`, `TECHNICAL`, `SOCRATIC`.
  * Evicted all regex short-circuits into `test_empirical_step_harness.py` as standalone Primer-Context Generators.
  * Injected `Current Year: 2026` temporal anchor into the Stage 1 system prompt, establishing explicit precedence for past hardware eras (2005–2025) over telemetry nouns (`5/5` historical routing on Purley 2018).

### Stage 2: HyDE Synthesis & Short-Exit (`cognitive_hub.py`)
* **Live Discovery**: Free-form string generation for `search_terms` in `PINKY_HYDE_SCHEMA` caused 3B models to enter repetitive string loops, truncating output at 180 tokens. Injecting full lab topology maps into Pinky's Stage 2 prompt bled into her conversational voice.
* **Calibrated Solution**:
  * **3-Axis Dynamic Prompt Compiler**:
    * `domain` $\to$ purely RAG substrate routing (`TraversalDispatcher`); never alters Pinky's prompt.
    * `vibe` $\to$ dynamically scoped `vibe_bedrock` (`career_compass` strictly on `HISTORICAL`; `lab_seats` on `META`/`OPERATIONAL`/`FORENSIC`; `current_date` on `CASUAL`/`WYWO`/`META`/`OPERATIONAL`).
    * `addressed_to` $\to$ dynamic speaker/listener framing (`"Jason addressed you directly"` vs `"Jason asked you and Brain"`).
  * `search_terms` constrained as a bounded JSON array (`maxItems: 6`), eliminating truncation loops (`0/36` truncations).
  * `CASUAL` and `UNCLEAR` short-exit immediately at Stage 2 with zero RAG attachment (`rag: null`).

### Stage 3: Brain Gatekeeper & Evidential Moat (`cognitive_hub.py` & `brain_node.py`)
* **Live Discovery**: The legacy two-block structure (`[ANALYSIS]` + `[BEDROCK SELECTION]`) caused 3B models to contradict themselves by dropping chunks in analysis and then re-listing them in selection. Furthermore, verdict-first formatting triggered causal hallucination on strict conjunction queries (`"Did we run Kubernetes on the 2012 Nehalem cluster?"`).
* **Calibrated Solution**:
  * Single `[ANALYSIS]` block with **Evidence-Before-Verdict** token order:
    `- CHUNK-N: Anchor Match: <terms>; Anchor Missing: <terms> => KEEP|DROP`.
  * **Strict Conjunction Gate**: If the primary queried subject is in `Anchor Missing:`, conclude `=> DROP` even if the hardware era matches (`5/5` `0/3 KEEP` on Nehalem Kubernetes).
  * **Pristine Payload Forwarding**: Parse `KEEP` IDs directly from `[ANALYSIS]` and forward only pristine kept chunks into `[BEDROCK_PAYLOAD]`; completely isolate Brain's raw `DROP` lines from Deep Thought.
  * **0/N Negative Moat**: When 0 chunks are kept, advance cleanly to Stage 5 with `[ZERO_CONTEXT]` sentinel and `vibe="ZERO_CONTEXT"` (skipping Deep Thought).
  * **`WYWO` Topic Anchor**: Substitute `gems[0]["summary"]` (`[STRATEGIC_ANCHOR]`) from `latest_synthesis_gems.json` as both the ChromaDB RAG query and Brain's `[EVALUATION_ANCHOR]`, filtering raw ticket stubs (`HSD-ES: 22013940445`) `5/5`.

### Stage 4: Deep Thought Strategic Synthesis (`thought_node.py`)
* **Live Discovery**: When presented with an archival gem from 2021 under a prompt asking *"What did I miss overnight?"*, M5 Air 27B Bonsai refused to answer (`"I'm not sure I can answer that"` / `"no recorded detail on the specific overnight gap"`), while 3B models hallucinated that the team integrated 2021 platforms last night.
* **Calibrated Solution**:
  * Explicit temporal labeling in `[BEDROCK_PAYLOAD]`: `Overnight Dream Excavation (from <year> archive)` vs `Overnight Lab Runtime (2026)`.
  * Deep Thought system prompt updated to distinguish present runtime telemetry from past career memories excavated during nightly dreaming (`5/5` clean passes on M5 Air with 0 refusals).
  * Omit nominal `status.json` metrics (`VRAM 61.2%`, `GPU 62.3W`) from `WYWO` payload to prevent models from cross-blending present GPU metrics with past silicon power validation.

### Stage 5: Pinky Spoken Voice & Contextual-Prompts (`cognitive_hub.py` & `triage_policy.json`)
* **Live Discovery**:
  * 3x context injection (prompt text, `[BRAIN_GROUNDING]`, and `_process_node_stream` context arg) bloated KV cache.
  * Static `"Brain dug up firmware logs"` framing caused archive hallucinations on live operational queries.
  * Conditional prompt text (`"flag any degraded watchdog alert if present"`) primed 3B models to invent degraded alerts on nominal nights.
  * Paraphrasing metrics caused mental-math fabrication (`57x energy savings`, `0.65 J/token`).
* **Calibrated Solution**:
  * Single `[BRAIN_NOTES]` block; Pinky speaks to Jason in 2nd person and refers to Brain in 3rd person.
  * Strict grounding fence: *"Ground every fact strictly in [BRAIN_NOTES] — never invent events, dates, numbers, or alerts absent from [BRAIN_NOTES]."*
  * `WYWO` static prompt kept strictly nominal (`"what old career note Brain read and indexed into memory overnight"`), crediting 2021 work to Jason's history (`5/5` zero time-travel). Python deterministically appends a 1-line degraded heads-up *only* when Watchdog == `DEGRADED`.
  * `TECHNICAL` directive instructs model to contrast exact cited metric pairs without computing new ratios (`5/5` zero math errors).
  * Cartoon mannerisms (`Narf!`, `Poit!`) kept strictly in `[BACKLOG-CLI-VOICE]` LoRA tuning; internal prompts maintain clean, warm, grounded engineering voice.

### Stage 6: Entailment Audit & Adversarial Intercom Continuation (`Protocols.md` & `cognitive_hub.py`)
* **Live Discovery**:
  * Local 3B base models are incapable of nuanced entailment auditing (`0%` specificity: JSON collapsed to 100% false-negatives, while text collapsed to 100% false-positive alarms over trivial capitalization or rounding).
  * The literal `BKM-089 §3` runtime prompt (`[MODE]: ADVERSARIAL_CONTINUATION...`) caused 3B models to echo `[MODE]` verbatim, roleplay Jason, or blame Jason for Brain's slip.
* **Calibrated Solution**:
  * **Half A (Silent Entailment Gate)**: Runs causal `CLAIM_CHECK:` $\to$ `VERDICT: PASS|MISMATCH` strictly on warm Sovereign 27B silicon (`M5_AIR` / `KENDER`, `12/12` accuracy). Stays **100% silent** on `PASS` (zero redundant chat messages). If only local 3B is online, the audit is skipped.
  * **Half B (Adversarial Continuation — `CONT_SYS_V3`)**: Fires only on `MISMATCH`. Prompts Pinky to chime in immediately on the Intercom to Jason (2nd person) calling out Brain's slip (3rd person) with the true bedrock detail, using plain `Jason asked:` / `Brain's mix-up:` / `Actual lab fact:` inputs without mode headers or quoted opener examples (`10/10` natural spoken corrections).

---

## 3. The Golden Laws of Live-Silicon Prompt Engineering (BKM-089 Codification)

From these 400+ empirical runs, we codify five invariant laws for small and quantized model prompt engineering:

1. **The Causal Evidence-First Law**: In classification or gatekeeping tasks on causal autoregressive models, the supporting evidence must always precede the decision token (`Evidence -> Decision`). Never place the verdict at the beginning of the line.
2. **The Frugal HOW / Rich WHY Law (`BKM-089`)**: Prompts explain HOW (format boundaries, roleplay channel, sentence limits). Prompt MOs explain WHY (epistemic motive, evaluation criteria). Never cram design justifications or negative edge-case rules into runtime prompts.
3. **The Anti-Quotation Invariant**: Never put quoted example phrases (e.g. `(like 'Hold on, Jason—')` or `Start with 'Narf!'`) in runtime prompts for small models. The model will treat the example as a mandatory verbatim prefix in 100% of generations.
4. **The Deterministic State vs. Generative Language Boundary**: Never ask an LLM to evaluate boolean system state conditionally inside a prompt (e.g. `"mention watchdog only if degraded"`). Evaluate the boolean state deterministically in Python, and conditionally inject the language directive only when the state is active.
5. **The Persona Grounding Fence**: Creative or playful character personas must be bounded by an explicit epistemic fence (`"Ground every fact strictly in [INPUT_BLOCK] — never invent events absent from [INPUT_BLOCK]"`). Without this fence, small models interpret character cues as an invitation to confabulate fictional scenarios.
