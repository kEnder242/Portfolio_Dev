# 🚀 Sprint Plan SPR-65.0: Two-Mice Streaming Handover, Triage-as-Primer Vocality, Semantic Feedback Interception, and Role-Slot Isolation

**Sprint:** 65.0  
**Date:** August 27, 2026  
**Status:** 🟡 PLANNED & READY FOR REVIEW  
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
* **Goal:** Eliminate 60s timeout hangs and 2.5s speculative head-start delays when Remote Kender (`192.168.1.26:11434`) is unreachable, unifying vocality checks into the live triage prompt.
* **Target Files:**
  - `HomeLabAI/src/logic/speculative_triage.py`
  - `HomeLabAI/src/v5/foyer/router.py`
  - `HomeLabAI/src/logic/cognitive_hub.py`
  - `HomeLabAI/src/tests/test_speculative_triage.py`
  - `HomeLabAI/src/tests/test_kender_fast_gate.py`
* **Implementation Details:**
  1. In `speculative_triage.py`, import `_probe_tcp` (or implement 200ms socket check for `192.168.1.26:11434`).
  2. At the entry of `SpeculativeTriageRelay.relay()`, check Kender reachability. If offline:
     * Immediately dispatch `_run_vllm()` with `0ms` wait.
     * Skip `_run_kender()` and head-start timeout.
     * Return `(result, "vllm")`.
  3. In `v5/foyer/router.py`, remove redundant background dumb generate ping (`{"prompt": "ping"}`) and update `check_thought_health` to use TCP probe + API status.
  4. In `foyer/router.py` and `cognitive_hub.py`, ensure `[STAGE 4/5] Strategic Synthesis` checks Sovereignty state and bypasses remote calls when Kender is `SHADOW`.
* **Verification:**
  - Create `test_kender_fast_gate.py` verifying that when Kender is offline, `relay()` returns in `<50ms` (no 2.5s sleep), local vLLM wins, and no 60s timeout occurs.

---

### **Story 65.2: [FEAT-487] Semantic Meta-Triage Feedback Interceptor (BKM-035)**
* **Goal:** Replace brittle regex with model-based semantic classification (`vibe: "META"`, `domain: "feedback"`, `addressed_to: "SYSTEM"`) to intercept supervisory turns directly into `validation_ledger.jsonl`.
* **Target Files:**
  - `HomeLabAI/config/triage_policy.json`
  - `HomeLabAI/src/logic/triage_engine.py`
  - `HomeLabAI/src/logic/feedback_interceptor.py`
  - `HomeLabAI/src/logic/cognitive_hub.py`
  - `HomeLabAI/src/tests/test_feedback_semantic_triage.py`
* **Implementation Details:**
  1. In `config/triage_policy.json`, add the canonical `META` policy:
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
  2. In `triage_engine.py`, update `build_triage_prompt()` to include `META / FEEDBACK` classification guidance.
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
         return
     ```
  4. In `feedback_interceptor.py`, keep `record_feedback()` and `_DEFAULT_LEDGER_PATH` for atomic write, while deprecating brittle regex in favor of triage classification.
* **Verification:**
  - Create `test_feedback_semantic_triage.py` testing the 11-phrase feedback battery, verifying 100% classification to `vibe: "META"` and atomic write to `validation_ledger.jsonl`.

---

### **Story 65.3: [FEAT-488] Role-Slot System Instruction Isolation & Anti-Bleed Stream Sanitizer**
* **Goal:** Eliminate prompt echoing and RAG bleed in small models by isolating behavioral directives in the `system` role slot and adding a stream output cleaner.
* **Target Files:**
  - `HomeLabAI/src/logic/cognitive_hub.py`
  - `HomeLabAI/src/nodes/base_resident.py`
  - `HomeLabAI/src/nodes/archive_node.py`
  - `HomeLabAI/src/tests/test_prompt_isolation_guardrail.py`
* **Implementation Details:**
  1. In `cognitive_hub.py:L574-575`, do NOT append `GROUNDING_PROTOCOL:` or `[STANCE]:` to the user query/context string. Pass them strictly via `behavioral_guidance`.
  2. In `nodes/base_resident.py`, ensure OpenAI chat completion messages place `behavioral_guidance` into `{"role": "system", "content": ...}`.
  3. In `cognitive_hub.py`, add `sanitize_stream_chunk(text)` to strip any rogue markers (`GROUNDING_PROTOCOL:`, `[STANCE]:`, `[ROUTE]`, `RAW CONTEXT APPEND`) before UI emission.
* **Verification:**
  - Run `test_prompt_isolation_guardrail.py` verifying that simulated model outputs containing prompt tokens are stripped cleanly without data loss.

---

### **Story 65.4: [FEAT-489] Two-Mice Sequential Streaming Handover & Distillation Pipeline**
* **Goal:** Implement the true streaming two-mice distillation dialogue (Brain Extract $\rightarrow$ Pinky Distill & TL;DR) and fix the critic retort bug.
* **Target Files:**
  - `HomeLabAI/src/logic/cognitive_hub.py`
  - `HomeLabAI/src/nodes/pinky_critic_persona.py`
  - `HomeLabAI/src/tests/test_two_mice_handover.py`
* **Implementation Details:**
  1. In `cognitive_hub.py`, implement sequential streaming handover for high-interest historical turns:
     * **Turn 1 (Brain - Archive)**: Invoked on raw RAG context with prompt instructing pure technical fact extraction (3–4 bullets, platforms, firmware, tools, scars). Streams to Right Console.
     * **Turn 2 (Pinky - Voice)**: Invoked with Brain's extracted bullets passed as context. System prompt instructs Pinky to acknowledge Brain in character and deliver a 2-sentence conversational TL;DR directly to Jason on the Left Console.
  2. In `pinky_critic_persona.py:L215-240`:
     * Support both `"retort"` and `"cartoon_retort"` keys in `_coerce_result()` so `CriticResult.retort` is never overridden with `"Narf! The retort went missing."`.
     * Update critic prompt to provide an in-character topic TL;DR acknowledging Brain's synthesis.
* **Verification:**
  - Create `test_two_mice_handover.py` asserting that Pinky receives Brain's extraction, acknowledges Brain, and emits a concise TL;DR.

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
