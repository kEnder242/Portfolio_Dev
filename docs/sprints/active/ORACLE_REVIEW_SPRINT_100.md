# 🔍 ORACLE ADVERSARIAL REVIEW: Sprint 100.0 (Phase 4 Cognitive Pipeline Hardening & Legacy Regression Excision)

**Reviewer:** `[SWARM:ORACLE]` (Cloud / High-Density Architectural Adversary)  
**Oracle Engine:** `openrouter/nvidia/nemotron-3-super-120b-a12b:free` (Session `ses_ee7ce694effequXShiSXcZD0cN`, 54,632 tokens, 5,386 reasoning tokens)  
**Date:** 2026-10-07  
**Target Specifications:** [`SPRINT_PLAN_SPR_100_0.md`](file:///home/jallred/Dev_Lab/Portfolio_Dev/docs/sprints/active/SPRINT_PLAN_SPR_100_0.md) (Stories 100.9 – 100.15)  
**Governing Laws:** `[BKM-061]` (Adversarial Oracle Protocol), `[BKM-062]` (Zero-Mock Anti-Green-Lie Mandate), `[BKM-015]` (Semantic Anchor Protocol), `[FEAT-361]` (Nuke Internal Masking), `[FEAT-640]` (Multi-Turn Turn Isolation), `[FEAT-635]` (Stage 1 Brain Information Gatekeeper), `[FEAT-406/470]` (Pinky Critic Scorecard)

---

## 1. Executive Summary & Findings Matrix

| Story ID | Focus Area | Current Defect / Legacy Regression Vector | Severity | Required Architectural Mitigation | Clearance Gate |
| :--- | :--- | :--- | :---: | :--- | :---: |
| **Story 100.9** | **HyDE Turn Isolation** | `resolve_hyde_vector` omits `scope=ContextScope.TURN` and `request_id`, defaulting to `ContextScope.LONG`. In multi-turn dialogues, `_process_node_stream` injects `[PREVIOUS_DEBATE]` (e.g. Turn 1 "hi"), poisoning HyDE synthesis into hallucinating `{"is_casual": true, "hyde_vector": ""}`. | **CRITICAL (`[FEAT-640]`)** | Explicitly pass `scope=ContextScope.TURN` and `request_id=request_id` in `cognitive_hub.py#L2469-L2477`. Update caller `_fetch_rag_context` to pass `request_id`. | **APPROVED WITH SPEC** |
| **Story 100.10** | **Defeature `CASUAL` Vibe & Persona Sanitize** | Active triage prompt (`triage_mode_context`) explicitly offers `1. CASUAL: Conversational pleasantries...`, triggering false-positive RAG bypass. Furthermore, line 1489 hardcodes `"past Intel/career projects"`, violating the Operator Persona Quarantine Directive. | **HIGH (`[FEAT-640]`)** | Comment out `CASUAL` in `cognitive_hub.py#L1486` prompt string while retaining Python enum fast-path. Sanitize line 1489 to `"past career / hardware projects"`. | **APPROVED WITH SPEC** |
| **Story 100.11** | **Mandatory Stage 1 Brain Gatekeeper & Relic Excision** | 68-sprint-old dinosaur `_distill_strategic_brief` (Sprint 32, commit `15b4705`) hardcodes `"Extract specific platform anchors, validation targets, and known PECI/MSR scars."` Turn dispatch falls back to `_run_brain_leg` when `interest < 0.70`, bypassing the modern Sprint 96 Brain Gatekeeper and emitting ungrounded PECI/MSR text. | **CRITICAL (`[FEAT-635]`)** | Completely delete `_distill_strategic_brief()` and retire `_run_brain_leg()`. Make Stage 1 Brain Information Gatekeeper (`_run_two_mice_handover`) mandatory on 100% of technical queries, routing fallback directly to `Brain (Archive)` extraction. | **APPROVED WITH SPEC** |
| **Story 100.12** | **Pinky Critic Scorecard (WHY + Retort)** | Severe schema mismatch: `build_critic_prompt()` requests `cartoon_retort` and `critique_suggestions`, while `eval_schema` enforces `score`, `reasoning`, `slop_found`, and `retort`. Lacking semantic guidance, the 3B model treated `reasoning` and `retort` as boolean string flags, emitting `"No\n\nNo"`. | **HIGH (`[FEAT-406]`)** | Harmonize `build_critic_prompt` output schema and `eval_schema`. Preserve debug scalar `{ "score": ... }` while eliciting substantive technical `reasoning` (the WHY) and spoken in-character `retort`. | **APPROVED WITH SPEC** |
| **Story 100.13** | **Cloud Delegation Baseline & Model Probe** | Risk of local execution silently substituting for cloud workers without verifiable cloud invocation, masking configuration regressions in OpenRouter/Cohere endpoints. | **HIGH (`[BKM-071]`)** | Implement pre-flight smoke test invoking `delegate.py --mode cloud`. Babysit logs at 30s intervals (`delegation_ledger.jsonl`, journalctl). Ground strictly in `OPENAGENT_HANDOVER_PLAYBOOK.md` §7 if fixes are needed. | **APPROVED WITH SPEC** |
| **Story 100.14** | **Triage Voting & In-Line Hover UI** | `intercom_v2.js` regex `/pinky|brain|insight|thought|resident|shadow/i` excludes `triage`, preventing voting. Feedback buttons are appended below message body, consuming an extra vertical line. | **MEDIUM (`[FEAT-638]`)** | Inject `voteable_sources` list from `infrastructure.json` via `build_site.py`. Relocate `.resp-fb` into `.msg-header` adjacent to timestamp with hover reveal (0 extra vertical lines). | **APPROVED WITH SPEC** |
| **Story 100.15** | **Re-Purge Vestigial `internal=True` Masking** | `nodes/loader.py#L210` sets `stream_source = self.name if not internal else None`. When `internal=True`, `self._broadcast_token` is skipped entirely, re-creating the Sprint 32 Censorship Waffle and gagging node telemetry. | **CRITICAL (`[FEAT-361]`)** | Abolish `stream_source = None` suppression. Route diagnostic/intermediate tokens to dedicated channels (`crosstalk`, `insight`) rather than silencing tokens into a black hole. | **APPROVED WITH SPEC** |

---

## 2. Invariant & Architecture Audit Details

### A. Story 100.9: Multi-Turn Turn Isolation & HyDE Synthesis
- **Forensic Verification:** In `HomeLabAI/src/logic/cognitive_hub.py#L1001-L1028`, `_process_node_stream` defaults to `ContextScope.LONG` unless `source_name` contains `"triage"` or `"deep"`. Because `resolve_hyde_vector` passed `source_name="Pinky (HyDE)"`, `scope` evaluated to `ContextScope.LONG`, appending all entries from `self.round_table_memory`.
- **Mitigation Directive:**
  1. Pass `scope=ContextScope.TURN` explicitly in `cognitive_hub.py#L2476`.
  2. Pass `request_id=request_id` from `_fetch_rag_context` $\to$ `resolve_hyde_vector` $\to$ `_process_node_stream`.
  3. Validate with `pytest HomeLabAI/src/tests/test_feat437_resolve_hyde_vector.py HomeLabAI/src/tests/test_triage_context_squeeze.py -v`.

### B. Story 100.10: `CASUAL` Vibe Defeaturing & Persona Quarantine
- **Forensic Verification:** `cognitive_hub.py#L1486` lists `1. CASUAL: Conversational pleasantries...`. Line 1489 additionally contains `'4. HISTORICAL: Questions on past Intel/career projects...'`. Furthermore, the Cloud Oracle identified that `HomeLabAI/config/triage_policy.json` retains `CASUAL: { "enabled": true }`, which could cause declarative policy drift if not synchronized.
- **Mitigation Directive:**
  1. Comment out line 1486 in `triage_mode_context`.
  2. Set `"enabled": false` for `CASUAL` in `HomeLabAI/config/triage_policy.json`.
  3. Sanitize line 1489 to read `'4. HISTORICAL: Questions on past career / hardware projects...'`.
  4. Retain Python dictionary mappings and fast-path handlers in `cognitive_hub.py` so no runtime exceptions occur if legacy vectors appear.

### C. Story 100.11: Excision of Sprint 32 Brief & Mandatory Brain Gatekeeper
- **Forensic Verification:** `_distill_strategic_brief` at `cognitive_hub.py#L2298-L2339` is the sole origin of the `"PECI/MSR scars"` text. It is invoked exclusively by `_run_brain_leg()#L2718`. In turn dispatch (`#L1843-L1885`), if `current_interest < TWO_MICE_FUNNEL_INTEREST` (0.70), execution falls back to `_run_brain_leg`, bypassing the modern Sprint 96 Brain Gatekeeper.
- **Mitigation Directive:**
  1. Make Stage 1 Brain Information Gatekeeper mandatory for ALL technical inquiries in `process_message`.
  2. Completely delete `_distill_strategic_brief()`.
  3. Completely delete `_run_brain_leg()`.
  4. Ensure any fallback path streams directly to `Brain (Archive)` without legacy distillation.
  5. Assert zero references to `_distill_strategic_brief` exist across the entire workspace.

### D. Story 100.12: Pinky Critic Scorecard Alignment
- **Forensic Verification:** `build_critic_prompt` in `pinky_critic_persona.py#L135-L138` requested:
  ```json
  "output_schema": {
      "cartoon_retort": "string — a witty, in-character one-liner",
      "critique_suggestions": "list[string] — actionable improvement notes"
  }
  ```
  While `evaluate_grounding` in `cognitive_hub.py#L2180-L2188` enforced:
  ```json
  "properties": {
      "score": {"type": "integer", "minimum": 1, "maximum": 5},
      "reasoning": {"type": "string"},
      "slop_found": {"type": "boolean"},
      "retort": {"type": "string"}
  }
  ```
- **Mitigation Directive:**
  Update `build_critic_prompt` to declare the exact schema enforced by vLLM:
  - `score` (1-5 scalar, visible debug backpressure).
  - `reasoning` (technical WHY analyzing factual alignment).
  - `retort` (spoken in-character judge reply).
  - `slop_found` (bool).
  Ensure `format_chat_delivery` weaves `reasoning` + `retort` for clear conversational presentation.

### E. Story 100.13: Cloud Delegation Smoke Test & Playbook Grounding
- **Forensic Verification:** Cloud models must be actively verified to prevent silent degradation into local execution or broken API pipes.
- **Mitigation Directive:**
  1. Execute a pre-flight probe using `delegate.py --sprint 100 --story 100.13 --mode cloud`.
  2. Verify that provider endpoints (OpenRouter/Cohere) emit tokens in `delegation_ledger.jsonl`.
  3. Enforce that any cloud fixes are preceded by reading `Portfolio_Dev/OPENAGENT_HANDOVER_PLAYBOOK.md` and logging entries in §7 Calibration Ledger.

### F. Story 100.14: Triage Up/Down Voting & In-Line Hover UI
- **Forensic Verification:** `intercom_v2.js#L347` checks `/pinky|brain|insight|thought|resident|shadow/i` and appends `.resp-fb` at the bottom of the card (`#L427`).
- **Mitigation Directive:**
  1. Add `"voteable_sources": ["pinky", "brain", "insight", "thought", "resident", "shadow", "triage"]` in `infrastructure.json`.
  2. Bake this list into `intercom_v2.js` via `build_site.py`.
  3. Relocate `${respFbHtml}` inside `<div class="msg-header">` with CSS `margin-left: auto; opacity: 0;` revealing on header hover.

### G. Story 100.15: Re-Purge Vestigial `internal=True` Censorship Waffle
- **Forensic Verification:** `nodes/loader.py#L210` sets `stream_source = self.name if not internal else None`. If `internal=True`, line 237 suppresses token broadcasting.
- **Mitigation Directive:**
  1. Remove `stream_source = None` token suppression.
  2. Route internal or intermediate tokens to `channel="crosstalk"` or `channel="insight"` rather than gagging them.
  3. Fully uphold `FEAT-361` (100% transparency; zero silent nodes).
  4. Perform a global workspace search across all resident node files (`loader.py`, `ear_node.py`, etc.) to verify zero remaining instances of silent `stream_source = None` token gags.

---

## 3. Certification & Gate Clearance

The adversarial Oracle audit confirms:
1. All 7 target stories (100.9 through 100.15) have precise, empirical root-cause verifications.
2. The legacy regressions (68-sprint-old `_distill_strategic_brief`, PECI/MSR scars, and `internal=True` gagging) have been definitively isolated and scheduled for complete excision.
3. The stories are **CERTIFIED AND CLEARED FOR EXECUTION**.

**Oracle Verdict: PROCEED TO AUTONOMOUS HEADS-DOWN IMPLEMENTATION.**
