# 🚀 Sprint Plan SPR-65.0: Two-Mice Streaming Handover, Triage-as-Primer Vocality, Semantic Feedback Interception, and Role-Slot Isolation

**Sprint:** 65.0  
**Date:** August 27, 2026  
**Status:** 🟡 PLANNED & READY FOR EXECUTION  
**Theme:** *Live Triage Vocality Verification & Fast Socket Gate, Semantic Meta-Triage Feedback Interception (BKM-035), Clean Role-Slot Prompt Segregation, and Sequential Two-Mice Distillation Pipeline*

---

## 🧭 Executive Summary & Architectural Contract

Sprint 65.0 addresses the critical findings and regressions surfaced during interactive co-pilot validation:

1. **Triage-as-Primer Live Vocality Check & Fast Socket Gate (`[FEAT-486]`)**:
   - **Fast 200ms Socket Probe**: Wire `_probe_tcp("192.168.1.26", 11434, 0.2)` at the front gate of `SpeculativeTriageRelay` and `FoyerRouter`. If the port is closed/unreachable, immediately lock Sovereignty to `SHADOW` and skip the 2.5s speculative head-start window with **zero delay**.
   - **Triage as Living Vocal Check**: Eliminate redundant "dumb" generation pings (`{"prompt": "ping"}`) in the background health loop. The real triage prompt dispatched during the speculative race serves as the definitive test of Kender residency and vocality.
   - **Short-Circuit Downstream Timeouts**: Ensure downstream stages (`[STAGE 4/5] Strategic Synthesis`) check Sovereignty state and skip 60s timeout loops when Kender is unreachable.

2. **Semantic Meta-Triage Feedback Interceptor (`[FEAT-487] / BKM-035`)**:
   - **BKM-015 Semantic Classification**: Replace brittle, hardcoded regex pattern matching (`_CRITIQUE_PATTERNS`) with model-driven semantic triage.
   - **Triage Taxonomy Expansion**: Register `vibe: "META"`, `domain: "feedback"`, and `addressed_to: "SYSTEM"` in `config/triage_policy.json` and triage system prompts to catch natural supervisory feedback, bug reports, tone adjustments, and Fourth-Wall critiques.
   - **Fast Control-Plane Intercept**: Intercept `vibe == "META"` turns immediately at Stage 1. Bypass RAG retrieval, interest boosts, and resident model debates. Atomically record the feedback to `validation_ledger.jsonl` ([`BKM-035`](file:///home/jallred/Dev_Lab/HomeLabAI/docs/Protocols.md#BKM-035)) and emit a crisp in-character confirmation from Pinky.
   - **Repurposed Test Battery**: Implement `test_feedback_semantic_triage.py` asserting that natural feedback phrases (e.g. `"feedback: rag echo"`, `"Wait, that's wrong"`, `"Pinky, note that..."`, `"Too verbose"`) reliably trigger the `META` intercept.

3. **Role-Slot System Instruction Isolation & Anti-Bleed Stream Guardrail (`[FEAT-488]`)**:
   - **Strict Chat Role Segregation**: Move `GROUNDING_PROTOCOL`, `[STANCE]`, and behavioral rules out of concatenated user/context message payloads in `cognitive_hub.py` and pass them strictly into the `system` role slot of the chat completions API.
   - **Eliminate Prompt Echoes**: Prevent 3B base models (`Llama-3.2-3B-AWQ`) from misinterpreting capitalized prompt headers as markdown section templates to reproduce.
   - **Stream Sanitizer Guardrail**: Implement a post-stream cleaner in `CognitiveHub._stream_message_to_ui` to strip any rogue protocol tags (`GROUNDING_PROTOCOL:`, `[STANCE]:`, `[ROUTE]`) before tokens reach the Intercom WebSocket.

4. **Two-Mice Sequential Streaming Handover & Distillation Pipeline (`[FEAT-489]`)**:
   - **The Distillation Funnel**: Transition from uncoordinated parallel essays to a sequential handover:
     * **Step 1 (Brain - Right Console)**: Acts as the deep technical fact extractor. Absorbs raw RAG context and streams 3–4 dense, structured bullet points (platforms, tools, registers, scars) with zero conversational filler.
     * **Step 2 (Pinky - Left Console / TTS)**: Acts as the conversational co-pilot. Receives Brain's extracted bullet points, acknowledges Brain in character (*"Narf! Brain dug up the firmware logs..."*), and delivers a punchy 2-sentence conversational TL;DR directly to Jason.
   - **The 3 Prompt Pillars**: Ground prompts with (1) Common Lab/Environment Foundation (`[FEAT-140/467]`), (2) Interest Loop Awareness (`[FEAT-403]`), and (3) Stage in Turn Sequence (`[FEAT-236]`).
   - **Critic Persona Hardening**: Fix the `retort` vs `cartoon_retort` key coercion bug in `pinky_critic_persona.py` and align the critic to provide an in-character topic TL;DR rather than a wooden code-linter score.

---

## 📋 Granular Story Breakdown & Delegation Topology

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ SPRINT 65 DELEGATION & COLLABORATION MATRIX                                                            │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ PHASE 1: TELEMETRY, GATING & INTERCEPTION                                                              │
│ Story 65.1: Kender Fast Gate & Triage Vocality      ──(OpenAgent Subagent)──> [FEAT-486] Unit Tests    │
│ Story 65.2: Semantic Feedback Interceptor (BKM-035) ──(OpenAgent Subagent)──> [FEAT-487] Unit Tests    │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ PHASE 2: PROMPT HYGIENE & CONVERSATIONAL DISTILLATION                                                  │
│ Story 65.3: Role-Slot Isolation & Anti-Bleed Guard  ──(OpenAgent Subagent)──> [FEAT-488] Unit Tests    │
│ Story 65.4: Two-Mice Sequential Streaming Handover  ──(OpenAgent Subagent)──> [FEAT-489] Unit Tests    │
├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ PHASE 3: INTEGRATION CERTIFICATION & LEDGER LOCK                                                       │
│ Story 65.5: Full-Lab E2E Verification & Feature Map ──(AGY Orchestrator)───> 384/384 Verified Links   │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### **Story 65.1: [FEAT-486] Triage-as-Primer Live Vocality Check & Kender Fast Socket Gate**

#### 🔍 Why It Broke & Root Cause
When Remote Kender (`192.168.1.26:11434`) is offline, `SpeculativeTriageRelay` still waited for the 2.5s `head_start_window`, and downstream stages (e.g. `[STAGE 4/5] Strategic Synthesis`) blocked for 60s on HTTP connection timeouts. Furthermore, running a separate "dumb" `{"prompt": "ping"}` generate pass forced Ollama into redundant dual-inference passes.

#### 📌 Existing / Buried Code Pointers
1. **Pre-built Socket Probe:** [`HomeLabAI/src/tests/test_integration_tri_node.py:L63-79`](file:///home/jallred/Dev_Lab/HomeLabAI/src/tests/test_integration_tri_node.py#L63) — Reusable, non-blocking `_probe_tcp(host, port, timeout=0.2)`.
2. **Speculative Relay Loop:** [`HomeLabAI/src/logic/speculative_triage.py:L23-55`](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/speculative_triage.py#L23) — The `head_start_window` wait to be short-circuited.
3. **Background Health Probe:** [`HomeLabAI/src/v5/foyer/router.py:L480-598`](file:///home/jallred/Dev_Lab/HomeLabAI/src/v5/foyer/router.py#L480) — Redundant heavy generation prime to be eliminated.

#### 🛠️ Implementation Details
1. In `speculative_triage.py`, import `_probe_tcp` (or implement a 200ms socket check for `192.168.1.26:11434`).
2. At the entry of `SpeculativeTriageRelay.relay()`, check Kender reachability. If offline:
   * Immediately dispatch `_run_vllm()` with **0ms wait**.
   * Skip `_run_kender()` and head-start timeout completely.
   * Return `(result, "vllm")`.
3. In `v5/foyer/router.py`, eliminate the redundant background generation ping (`{"prompt": "ping"}`) in `check_thought_health()`. Rely on the fast 200ms TCP probe + `/api/tags` status check. The live triage prompt dispatched during `SpeculativeTriageRelay` acts as the living vocality verification.
4. In `foyer/router.py` and `cognitive_hub.py`, ensure `[STAGE 4/5] Strategic Synthesis` checks Sovereignty state and bypasses remote calls when Kender is `SHADOW`.

#### ✅ Verification & Test Contract
* Create `test_kender_fast_gate.py` asserting:
  1. When Kender TCP port is unreachable, `relay()` returns in `<50ms` (no 2.5s head-start delay).
  2. Local vLLM wins the race immediately.
  3. No 60s timeout hangs occur in Foyer downstream stages.

---

### **Story 65.2: [FEAT-487] Semantic Meta-Triage Feedback Interceptor (BKM-035)**

#### 🔍 Why It Broke & Root Cause
[`_CRITIQUE_PATTERNS`](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/feedback_interceptor.py#L25) used brittle hardcoded regex that checked for conversational objections (`"Wait, that's wrong"`, `"Actually..."`), but had a 100% blind spot for explicit prefixes like `"feedback:"`, `"regression:"`, or natural tone corrections. The feedback fell through triage into the resident LLMs as regular user queries, causing hallucinated essays instead of logging to the validation ledger.

#### 🛠️ Implementation Details
1. In `config/triage_policy.json`, add the canonical `META` policy entry:
   ```json
   "META": {
     "description": "User is giving supervisory feedback, pointing out bugs/regressions, correcting factual errors, requesting tone/verbosity adjustments, or issuing Fourth-Wall operational commands.",
     "vibe": "META",
     "domain": "feedback",
     "addressed_to": "SYSTEM",
     "importance": 0.0,
     "rag": null
   }
   ```
2. In `triage_engine.py`, update `build_triage_prompt()` to instruct the triage model:
   * *"META / FEEDBACK: If the user is giving feedback on a previous answer, pointing out an error or regression, asking to tweak verbosity/tone, or issuing system corrections (e.g. 'feedback: ...', 'that was wrong', 'stop echoing', 'too verbose', 'kender should have a ping gate'), classify as vibe: META, domain: feedback, addressed_to: SYSTEM."*
3. In `cognitive_hub.py`, update the Stage 1 Triage handler:
   ```python
   if t_parsed.get("vibe") == "META" or t_parsed.get("domain") == "feedback":
       flawed_output = self.turn_thought_trace.get("pinky") or (self.round_table_memory[-1] if self.round_table_memory else "")
       record_feedback(query=turn, user_correction=turn, flawed_output=flawed_output)
       await self.broadcast({
           "type": "thought_stream",
           "source": "Pinky (Feedback)",
           "token": "Narf! Feedback logged to the validation ledger.",
           "final": True,
           "request_id": request_id
       })
       return  # Short-circuit: Zero debate, zero RAG, zero latency
   ```
4. In `feedback_interceptor.py`, maintain `record_feedback()` and `_DEFAULT_LEDGER_PATH` for atomic write, while deprecating regex pattern matching.

#### 🧪 Grounded 11-Phrase Test Battery
Create `HomeLabAI/src/tests/test_feedback_semantic_triage.py` asserting that each of the following 11 inputs classifies to `vibe: "META"`, `domain: "feedback"`, and appends an entry to `validation_ledger.jsonl`:
```python
FEEDBACK_TEST_BATTERY = [
    "feedback: 1) rag echo 2) verbosity should be tweaked",
    "feedback: KENDER should have a ping check gate",
    "Wait, that's wrong, the register offset is 0x610 not 0x618",
    "Actually, in 2016 I worked on ESB2 server management, not Optane",
    "Pinky, note that we deprecated InfluxDB in Phase 3",
    "Brain, your dates are off by two years",
    "This is way too verbose, give me just the bullet points",
    "Regression: the coherence critic is failing every turn with score 1",
    "I disagree with that summary, check the 2019 logs again",
    "Correction: the host rebooted due to hung_task_panic on USB sync",
    "Can you be more concise? Stop giving me 5-page essays"
]
```

---

### **Story 65.3: [FEAT-488] Role-Slot System Instruction Isolation & Anti-Bleed Stream Sanitizer**

#### 🔍 Why It Broke & Root Cause
In `cognitive_hub.py:L574-575`, operational rules like `GROUNDING_PROTOCOL: Formulate your response EXCLUSIVELY...` and `[STANCE]: ACADEMIC` were concatenated directly into the `user` message text above `<historical_record>`. Llama-3.2-3B perceives capitalized instruction tags in user space as few-shot output formatting examples, printing `**GROUNDING PROTOCOL**` and `**CONVERSATIONAL ACKNOWLEDGMENT**` verbatim in chat.

#### 🛠️ Implementation Details
1. In `cognitive_hub.py:L574-575`, **never concatenate operational directives into `query` or `context` strings**. Pass them strictly via `behavioral_guidance`.
2. In `nodes/brain_node.py` and `nodes/loader.py`, ensure the OpenAI chat completions payload places all behavioral guidance strictly inside the `{"role": "system", "content": ...}` slot:
   ```python
   messages = [
       {"role": "system", "content": f"{system_prompt}\n\n[BEHAVIORAL_GUIDANCE]: {behavioral_guidance}"},
       {"role": "user", "content": user_payload}
   ]
   ```
3. In `cognitive_hub.py`, implement `sanitize_stream_chunk(text: str) -> str` to strip any rogue markers (`GROUNDING_PROTOCOL:`, `[STANCE]:`, `[ROUTE]`, `RAW CONTEXT APPEND`) before emitting tokens to `_stream_message_to_ui`.

#### ✅ Verification & Test Contract
* Create `test_prompt_isolation_guardrail.py` verifying:
  1. System prompt parameters are routed to the `system` role slot.
  2. Simulated model responses containing leaked protocol markers are sanitized cleanly without losing technical content.

---

### **Story 65.4: [FEAT-489] Two-Mice Sequential Streaming Handover & Distillation Pipeline**

#### 🔍 Why It Broke & Root Cause
Brain and Pinky ran as uncoordinated parallel competitors. Brain generated a 500-word essay from the raw RAG dump, and then Pinky was invoked on the **same original user query and raw RAG dump**, ignoring Brain entirely. Furthermore, in `pinky_critic_persona.py:L217`, `_coerce_result` looked only for `"cartoon_retort"`; when the LLM returned `"retort"`, it defaulted to `"Narf! The retort went missing."` and scored the turn 1/5.

#### 🏛️ The 3 Prompt Engineering Pillars
1. **Shared Lab/Environment Foundation (`[FEAT-140/467]`):**
   Both mice share a bedrock system prompt establishing physical hardware awareness (z87-Linux, RTX 2080 Ti) and residency. Neither mouse roleplays in a generic vacuum.
2. **Interest Loop Awareness (`[FEAT-403]`):**
   * Low Interest (`< 0.4`): Casual banter; Pinky answers directly with high brevity; Brain remains dormant.
   * High Interest (`>= 0.7`): Distillation Funnel active; Brain extracts facts $\rightarrow$ Pinky distills to user.
3. **Stage in Turn Sequence (`[FEAT-236]`):**
   * **Stage 1 (Brain - Right Console)**: System Prompt: *"You are Brain. Jason asked a technical question. Extract the exact technical ground truth (platforms, firmware, tools, scars) from <historical_record> in 3-4 dense bullet points. Provide pure technical signal for Pinky."*
   * **Stage 2 (Pinky - Left Console / TTS)**: System Prompt: *"You are Pinky. Brain has reviewed the archives and extracted: {brain_extracted_bullets}. Acknowledge Brain in character ('Narf! Brain dug up the firmware logs...') and deliver a 2-sentence conversational TL;DR directly to Jason."*

#### 📡 Dual-Console WebSocket Routing Contract
Ensure WebSocket telemetry packets carry explicit console channel tags:
* **Brain Extraction Stream:** `{"type": "thought_stream", "channel": "insight", "source": "Brain (Archive)", "console": "Right"}`
* **Pinky Voice Stream:** `{"type": "thought_stream", "channel": "pinky", "source": "Pinky (Voice)", "console": "Left"}`

#### 🛠️ Critic Persona Fix
In `pinky_critic_persona.py:L215-240`, support both `"retort"` and `"cartoon_retort"` keys in `_coerce_result()`. Refactor the critic prompt from a static formatting grader into an active conversational participant summarizing Brain's technical points.

#### ✅ Verification & Test Contract
* Create `test_two_mice_handover.py` asserting:
  1. Brain outputs 3–4 structured bullets on `channel: "insight"` (Right Console).
  2. Pinky receives Brain's bullets and emits an in-character acknowledgment and concise TL;DR on `channel: "pinky"` (Left Console).
  3. Critic parses `"retort"` cleanly with zero missing-retort fallback crashes.

---

### **Story 65.5: Full-Lab E2E Verification & Feature Map Sync**
* **Goal:** Verify all test suites pass, update `FeatureTracker.md` with FEAT-486 through FEAT-489, compile `features.html`, verify 0 link drift, and update status ledgers.
* **Target Files:**
  - `Portfolio_Dev/FeatureTracker.md`
  - `Portfolio_Dev/field_notes/features.html`
  - `Portfolio_Dev/00_FEDERATED_STATUS.md`
  - `HomeLabAI/ProjectStatus.md`
* **Verification:**
  - `python3 Portfolio_Dev/field_notes/verify_feature_links.py` $\rightarrow$ 384/384 Code fields verified, 0 drift.
  - `pytest` across all new and existing test suites $\rightarrow$ 100% PASS.

---

## 🔒 Verification & Exit Criteria

1. **Kender Offline Resilience:** When `192.168.1.26:11434` is stopped, interactive queries resolve in local vLLM in `<2s` with zero 60s timeout errors.
2. **Feedback Capture:** User feedback prefixed with `"feedback:"` or phrased conversationally is 100% captured into `validation_ledger.jsonl` without triggering RAG debates.
3. **Zero Prompt Bleed:** No `GROUNDING_PROTOCOL` or `[STANCE]` headers appear in Intercom chat responses.
4. **Two-Mice Handover:** Brain outputs structured technical bullets on the Right Console; Pinky acknowledges Brain and delivers a conversational TL;DR on the Left Console.
5. **DNA Fast-Path Adherence:** All subagent operations consult `clara-dna` MCP or `icm recall` without reading 200KB+ files.
