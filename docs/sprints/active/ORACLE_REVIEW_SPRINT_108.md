# 🔮 Adversarial Oracle Audit Report: Sprint 108.0

**Sprint:** SPR-108.0 (Phase 1 Pre-Flight Architecture Audit)  
**Evaluator:** Tier 1 Strategic & Adversarial Architecture Oracle (`[SWARM:ORACLE]` / AGY)  
**Timestamp:** 2026-10-21T12:30:00-07:00  
**Target Document:** [`Portfolio_Dev/docs/sprints/active/SPRINT_PLAN_SPR_108_0.md`](file:///home/jallred/Dev_Lab/Portfolio_Dev/docs/sprints/active/SPRINT_PLAN_SPR_108_0.md)  
**Target Codebase:** `HomeLabAI` (branch `main`), `Portfolio_Dev` (branch `main`)  
**Governing BKMs & Invariants:** `[BKM-005]`, `[BKM-007]`, `[BKM-015]`, `[BKM-020]`, `[BKM-024]`, `[BKM-043]`, `[BKM-049]`, `[BKM-061]`, `[BKM-062]`, `[BKM-069]`, `[BKM-080]`, `[BKM-081]`, `[BKM-082]`, `[BKM-085]`, `[BKM-086]`, `[BKM-088]`, `[FEAT-058]`, `[FEAT-645]`, `[FEAT-672]`, `[LOOP-005]`, `[VIBE-013]`, `[VIBE-018]`, `[INS-047]` ("Live is King, History is Queen")  

---

## 1. Executive Assessment & Macro Architectural Verdict

### 🏛️ The Verdict: **APPROVED WITH 5 MANDATORY ADVERSARIAL SAFEGUARDS**
The Sprint 108.0 architecture—grounded in Cognitive Hydraulics (alternating Split/Sum cognitive pipeline), Keyed Evidence Filtering, the Positive/Negative Evidential Moat, Physical Node-Anchored Routing, the Elimination of "CRITIQUE" in favor of `FILTER` and `AUDIT`, and the Step-Trace Telemetry Loop (`[LOOP-005]`)—is **architecturally sound, mathematically elegant, and historically grounded**.

Forensic git archaeology and sprint lookback confirm that this architecture permanently closes the "Island of Green Illusion" and prevents the chronic "Brain Spoon-Feeding Trap" where 3B models were forced to regurgitate full RAG artifact bodies.

However, an exhaustive adversarial audit of the specifications reveals **five critical failure modes** that must be hardened in the concrete story specifications prior to execution.

---

## 2. Adversarial Peer Review & Edge-Case Analysis

| Risk Dimension | Oracle Finding / Failure Mode | Architectural Mitigation in Sprint 108 | Status |
| :--- | :--- | :--- | :--- |
| **1. Empty-RAG Moat Penalization Trap** | If a social primer or casual greeting produces 0 RAG candidate chunks ($N_{\text{CANDIDATES}} == 0$), strict evaluation of $N_{\text{KEEP}} == 0$ would trigger the damping penalty (`min(interest, 0.35)`), artificially suppressing conversational interest on harmless greetings. | **Neutral Bypass on Zero Candidates:** Evidential Moat damping applies **ONLY** if $N_{\text{CANDIDATES}} > 0$ and $N_{\text{KEEP}} == 0$. When $N_{\text{CANDIDATES}} == 0$, the moat is neutral: interest remains unmodified. | **MANDATED IN STORY 108.1** |
| **2. Keyed Filter Regex Brittle Match** | 3B quantized models (`Llama-3.2-3B-AWQ`) frequently omit brackets, alter capitalization, or format keys as `CHUNK 1: KEEP` or `- Chunk-1: DROP`. Rigid regex matching will fail, resulting in accidental zero-keep classifications. | **Permissive Parsing & Fallback:** Use `# [BKM-015:APPROVED_REGEX]` with `re.IGNORECASE` pattern `r"(?:\[|\b)CHUNK[-_\s]*(\d+)(?:\]|\b)[:\s]*(KEEP|DROP)"`. If 0 keys parse from a non-empty response, fail safe: retain all candidates and log an unparsed filter warning rather than silently dropping evidence. | **MANDATED IN STORY 108.1** |
| **3. Entailment Audit Latency Blocking** | Executing the Entailment Audit on Node KENDER (4090 Ollama) synchronously inside the turn loop introduces a 3–8 second blocking delay on the primary audio/conversational stream. | **Asynchronous Fire-and-Forget Dispatch:** The Entailment Audit is decoupled and dispatched out-of-band via `asyncio.create_task()`. The primary conversational turn streams and completes immediately. Deep Thought's audit results emit directly to Foyer telemetry and `[LOOP-005]` out-of-band. | **MANDATED IN STORY 108.2** |
| **4. Console Routing Multi-Key Conflict** | Discrepancies between `node` ("pinky"/"brain"), `seat` ("Linux 2080ti"/"M5 Air"), and `console` ("Left"/"Right") in WebSocket envelopes can cause client-side display misattribution. | **Canonical Envelope Standard:** The Python server computes `console: "Left" \| "Right"` once at emission based on immutable node ownership: Pinky/Triage $\to$ `Left`; Brain/Deep Thought $\to$ `Right`. Client binds strictly to `payload.console`. | **MANDATED IN STORY 108.3** |
| **5. Harness Telemetry Pollution** | Scaffolding `test_empirical_step_harness.py` could accidentally write test turn metrics to live `live_usage_stream.jsonl`, triggering false-alarm watchdog spikes or corrupting cumulative token ledgers. | **Strict Test Environment Sandboxing:** All test harness runs must mock or redirect `DATA_DIR` via `monkeypatch` / `tempfile.TemporaryDirectory()`. Offline CI tests must use pre-recorded synthetic fixtures (`tests/fixtures/synthetic_turn_fixtures.json`). | **MANDATED IN STORY 108.4** |

---

## 3. Story-by-Story Adversarial Directives

### Story 108.1: Brain Keyed Evidence Filter & Evidential Moat Logic
* **Failure Mode:** Brain hallucinates non-existent keys (e.g., outputs `[CHUNK-7]` when only 3 chunks were provided).
* **Directive:** Validate parsed chunk IDs against the actual input candidate set `0 <= chunk_id < len(candidates)`. Discard hallucinated chunk IDs.
* **Failure Mode:** Brain drops all chunks because the primer is casual banter.
* **Directive:** Do not trigger an error or retry. An empty keep list ($N_{\text{KEEP}} == 0$) when candidates exist is a valid epistemic judgment: it suppresses interest to $\le 0.35$ and prevents Deep Thought from waking up unnecessarily.

### Story 108.2: Decoupled Out-of-Band Entailment Audit & Elimination of "CRITIQUE"
* **Failure Mode:** Node KENDER 4090 is offline or Ollama `:11434` connection drops during audit dispatch.
* **Directive:** Implement explicit fail-soft exception handling in the background audit task (`except Exception as e: logger.warning(f"Entailment audit skipped: {e}")`). A failed out-of-band audit must **never** raise an exception that impacts the main conversational pipeline or corrupts session state.
* **Naming Excision:** Verify zero remaining occurrences of `step_grounding_critic`, `critic_verdict`, or `pinky_critic` in prompt keys, schemas, or variable names. All references must be `audit` / `entailment_audit` or `filter`.

### Story 108.3: Physical Node-Anchored Console Routing Hardening
* **Failure Mode:** Client re-rendering creates duplicate speech bubbles if a turn emits both an early token stream and a final audio URL.
* **Directive:** Ensure message deduplication in `intercom_v2.js` by checking `payload.request_id` or `payload.turn_id` before appending new DOM nodes.

### Story 108.4: BKM-088 Micro-Harness Test Rig Scaffolding
* **Failure Mode:** Harness modifies production configuration files (`config/triage_policy.json`).
* **Directive:** The harness operates on a cloned or in-memory policy object. It must never commit config mutations back to disk during prompt shootout runs.

---

## 4. Delegation & Anti-Bypass Matrix (`BKM-049`)

To strictly adhere to `BKM-049` (Anti-Bypass Guard) and prevent the **Self-Promotion Trap**:

| Story ID | Assigned Swarm Owner | Execution Mechanism | Architectural Justification |
| :--- | :--- | :--- | :--- |
| **Story 108.1** | `[SWARM:LOCAL]` | `delegate.py --mode local` | Local Python AST surgery on `cognitive_hub.py`. Atlas on 4090 executes surgical changes. |
| **Story 108.2** | `[SWARM:CLOUD]` | `delegate.py --mode cloud` | Broad AST surgery across 3,500-line `cognitive_hub.py` (purging "CRITIQUE" tokens and wiring async background task). High blast radius mandates 200k cloud context. |
| **Story 108.3** | `[AGY:PRIMARY]` | Direct AGY Execution | Multi-subsystem coordination spanning frontend DOM (`intercom_v2.js`) and backend router (`foyer/router.py`). |
| **Story 108.4** | `[SWARM:LOCAL]` | `delegate.py --mode local` | Test harness scaffolding in `src/tests/test_empirical_step_harness.py`. Atlas on 4090. |

---

## 5. Pre-Flight Verdict & Sign-Off

* **Verdict:** 🟢 **PRE-FLIGHT ADVERSARIAL AUDIT PASSED (WITH MITIGATIONS EMBEDDED)**
* **Action Required:** 
  1. Commit this audit document to `Portfolio_Dev/docs/sprints/active/ORACLE_REVIEW_SPRINT_108.md`.
  2. Embed the 5 mitigations directly into the Story specifications of `SPRINT_PLAN_SPR_108_0.md`.
  3. Formally check off the Pre-Flight Digital Checkbox Gate (`BKM-082 §GATE`).
