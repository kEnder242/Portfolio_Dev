# 🚀 Sprint Plan SPR-61.0: Epistemic Calibration, Conversational Flow & Defaults Audit

**Sprint:** 61.0  
**Date:** August 25, 2026  
**Status:** GREENLIGHT READY  
**Theme:** *Eliminating False Defaults ("Zero Context > Default Context"), Speaker Demarcation, and Cartoon/Summary Persona Dynamics*

---

## 🧭 Executive Summary & Core Architectural Principles

During our live co-pilot session review on August 25, 2026, a deep inspection of both conversational turns and raw evaluation logs revealed why the system thrashed into irrelevant career history and robotic loops.

### 🏛️ Core Principles & Insights

1. **"Zero Context is Better than Default Context" (`[FEAT-467]`)**:
   * Injecting *no context* (or minimal context) allows resident models to reason cleanly or ask for clarification.
   * Injecting *default context* (e.g. falling back to 2018 Intel PAE notes when a query is ambiguous) actively misleads models and triggers severe hallucinations.
   * **Rule**: When intent or domain is uncertain, `hyde_vector_text` is empty (`""`), and `ArchiveNode` returns zero context.

2. **Speaker Demarcation in Triage Memory (`[FEAT-468]`)**:
   * **The Catch**: Pinky repeated *"You're feeling a bit off... checking vital signs"* because Triage ingested conversation history without speaker filtering and mistook Pinky's previous turn for the user's intent.
   * **Rule**: Triage MUST strictly evaluate the latest `[USER]` turn, never mistaking assistant dialogue for user intent, while preserving self-awareness of what Pinky and Brain stated in previous turns.

3. **Scoping the DNA (`[FEAT-469]`)**:
   * **`feature_dna` & `lab_infrastructure`**: Given to the Mice (Pinky/Brain) to ground discussions about live software modules (`AudioPipeline`, `MaintenanceSweeper`, `OverrideParser`, daemons, ports).
   * **`behavioral_dna`**: Reserved strictly for Orchestrator/AGY development workflows. Mice do not roleplay commit rules.
   * **`career_ledger`**: Suppressed during live system operations; queried only for explicit personal career questions.

4. **Cartoon Roleplay Critic & Actionable Technical Summary (`[FEAT-470]`)**:
   * Raw JSON diagnostic dictionaries (`{"score": 5, "slop_found": false}`) stay in `CROSSTALK`.
   * Pinky delivers a satirical cartoon quip reacting to Brain's complexity + a 1-sentence agreed takeaway directly to `CHAT`.

---

## 🛠️ Delegation BKM & Pathing Guidelines (Learnings from Sprint 60)

1. **Pathing & Import Cleanliness**:
   * All greenfield satellites must use standard library imports and top-level absolute paths (`from typing import ...`, `import json`, `import re`).
   * No brittle relative imports inside satellites.
2. **Strict Verification Command Gate**:
   * In `delegate.py`, the `--verification` flag must mandate both linting and testing:
     `--verification "ruff check <target_files> && pytest <test_files> -v"`
   * OpenAgent must satisfy zero lint errors and 100% green unit tests before concluding.
3. **Decoupled Greenfield Satellites**:
   * Subagents build pure, self-contained satellite classes and unit suites.
   * AGY orchestrator performs core wiring into `CognitiveHub`, `router.py`, and `ArchiveNode`.

---

## 📋 Granular Story Breakdown & Delegation Matrix

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│ SPRINT 61 DELEGATION TOPOLOGY                                                            │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ Story 61.1: triage_gateway.py      ──(OpenAgent Subagent)──> 25+ Unit Tests (Green)      │
│ Story 61.2: lab_dna_router.py      ──(OpenAgent Subagent)──> 20+ Unit Tests (Green)      │
│ Story 61.3: pinky_critic_persona.py──(OpenAgent Subagent)──> 20+ Unit Tests (Green)      │
│                                                                                          │
│ Story 61.4: Core Wiring & Onramps  ──(AGY Orchestrator)───> Hub / Router / ArchiveNode   │
│ Story 61.5: Stack Bounce & E2E     ──(AGY Orchestrator)───> ws://127.0.0.1:8765 Gauntlet │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### **Story 61.1: [FEAT-467/468] Triage Gateway Satellite (`triage_gateway.py`)**
* **Status**: 🔲 **READY FOR DELEGATION**
* **Target Files**:
  * `HomeLabAI/src/logic/triage_gateway.py`
  * `HomeLabAI/src/tests/test_triage_gateway.py`
* **Satellite Functions**:
  1. `format_speaker_history(history_turns: List[Dict[str, str]]) -> str`: Formats turns with `[USER: Jason]`, `[ASSISTANT: Brain]`, `[ASSISTANT: Pinky]` tags.
  2. `extract_latest_user_query(turn_or_history: str) -> str`: Extracts exclusively the latest user command, stripping `[ME]` or `[USER]` prefixes.
  3. `scrub_hyde_vector(hyde_text: str) -> str`: Strips literal angle brackets (`<...>`), template placeholders, or zeroes out string if invalid.
  4. `is_meta_lexicon(query: str) -> bool`: Checks if query mentions live lab components (`audio_pipeline`, `sweeper`, `override`, `foyer`, `vllm`, `attendant`, `residents`, `features`, `bkm`).
  5. `classify_vibe_and_domain(query: str, parsed_json: Dict[str, Any]) -> Tuple[str, str]`: Enforces `vibe="META"` and `domain="lab_internal"` when lexicon matches.
* **Delegation Command**:
  ```bash
  python3 HomeLabAI/src/tests/delegate.py --story 61.1 \
    --title "Build Triage Gateway Satellite (FEAT-467/468)" \
    --file "src/logic/triage_gateway.py" \
    --details "Create a pure, decoupled satellite module src/logic/triage_gateway.py implementing format_speaker_history, extract_latest_user_query, scrub_hyde_vector, is_meta_lexicon, and classify_vibe_and_domain. Ensure scrub_hyde_vector strips template angle brackets like <silicon_term_or_pcie_ras> and returns empty string on ambiguous input. Create test_triage_gateway.py with at least 25 unit tests covering all functions, edge cases, and dirty inputs." \
    --verification "ruff check src/logic/triage_gateway.py src/tests/test_triage_gateway.py && pytest src/tests/test_triage_gateway.py -v" \
    --dir "/home/jallred/Dev_Lab/HomeLabAI"
  ```

---

### **Story 61.2: [FEAT-469] Lab DNA Router Satellite (`lab_dna_router.py`)**
* **Status**: 🔲 **READY FOR DELEGATION**
* **Target Files**:
  * `HomeLabAI/src/nodes/lab_dna_router.py`
  * `HomeLabAI/src/tests/test_lab_dna_router.py`
* **Satellite Functions**:
  1. `get_collection_priorities(vibe: str, domain: str) -> List[str]`: Returns collection search priority. For `vibe="META"` or `domain="lab_internal"`, returns `["feature_dna", "lab_infrastructure", "lab_journal"]` and strictly omits `career_ledger` and `behavioral_dna`. For `domain="lab_history"`, returns `["career_ledger", "artifact_vault"]`.
  2. `filter_candidate_context(candidates: List[Dict[str, Any]], vibe: str, domain: str, max_distance: float = 0.50) -> List[Dict[str, Any]]`: Implements "Zero Context > Default Context". If top candidate distance > max_distance, returns empty list.
  3. `format_lab_dna_tag(coll: str, metadata: Dict[str, Any], doc: str) -> str`: Formats extracted context with `[FEATURE_DNA: FEAT-xxx]` and `[INFRA: component]` tags.
* **Delegation Command**:
  ```bash
  python3 HomeLabAI/src/tests/delegate.py --story 61.2 \
    --title "Build Lab DNA Router Satellite (FEAT-469)" \
    --file "src/nodes/lab_dna_router.py" \
    --details "Create a pure, decoupled satellite module src/nodes/lab_dna_router.py implementing get_collection_priorities, filter_candidate_context, and format_lab_dna_tag. Implement the Zero Context rule: if top candidate distance > max_distance, return empty list. For meta vibes, prioritize feature_dna and lab_infrastructure and suppress career_ledger. Create test_lab_dna_router.py with at least 20 unit tests." \
    --verification "ruff check src/nodes/lab_dna_router.py src/tests/test_lab_dna_router.py && pytest src/tests/test_lab_dna_router.py -v" \
    --dir "/home/jallred/Dev_Lab/HomeLabAI"
  ```

---

### **Story 61.3: [FEAT-470] Pinky Critic Persona Satellite (`pinky_critic_persona.py`)**
* **Status**: 🔲 **READY FOR DELEGATION**
* **Target Files**:
  * `HomeLabAI/src/nodes/pinky_critic_persona.py`
  * `HomeLabAI/src/tests/test_pinky_critic_persona.py`
* **Satellite Functions**:
  1. `build_critic_prompt(brain_brief: str, user_query: str) -> str`: Constructs prompt instructing Pinky to output JSON containing: `quip` (a witty/satirical cartoon reaction to Brain's complexity), `summary` (a crisp 1-sentence agreed takeaway), `score` (int 1-5), and `slop_found` (bool).
  2. `parse_critic_payload(raw_output: str) -> Dict[str, Any]`: Parses JSON payload, strips markdown fences, validates keys, and cleans up formatting.
  3. `format_chat_delivery(parsed_critic: Dict[str, Any]) -> str`: Returns the combined quip and summary string for out-loud delivery. Banned phrases (`"A well-crafted response"`, `"well crafted"`) are stripped or rejected.
  4. `format_crosstalk_telemetry(parsed_critic: Dict[str, Any]) -> Dict[str, Any]`: Returns the telemetry frame for internal `CROSSTALK` broadcast.
* **Delegation Command**:
  ```bash
  python3 HomeLabAI/src/tests/delegate.py --story 61.3 \
    --title "Build Pinky Critic Persona Satellite (FEAT-470)" \
    --file "src/nodes/pinky_critic_persona.py" \
    --details "Create a pure, decoupled satellite module src/nodes/pinky_critic_persona.py implementing build_critic_prompt, parse_critic_payload, format_chat_delivery, and format_crosstalk_telemetry. Ensure format_chat_delivery blends a witty cartoon quip with an agreed technical summary while rejecting robotic boilerplate like 'A well-crafted response'. Create test_pinky_critic_persona.py with at least 20 unit tests." \
    --verification "ruff check src/nodes/pinky_critic_persona.py src/tests/test_pinky_critic_persona.py && pytest src/tests/test_pinky_critic_persona.py -v" \
    --dir "/home/jallred/Dev_Lab/HomeLabAI"
  ```

---

### **Story 61.4: [CORE/ORCH] Core Wiring, Conversational Onramps & Stream Demarcation**
* **Status**: 🔲 **PLANNED (AGY Orchestrator)**
* **Target Files**:
  * `HomeLabAI/src/logic/cognitive_hub.py`
  * `HomeLabAI/src/nodes/archive_node.py`
  * `HomeLabAI/src/v5/foyer/router.py`
  * `HomeLabAI/src/nodes/pinky_node.py`
  * `HomeLabAI/src/tests/test_sprint61_integration.py`
* **Scope**:
  1. Wire `triage_gateway` into `CognitiveHub.process_query()` and `_process_turn()`.
  2. Wire `lab_dna_router` into `ArchiveNode.get_context()`.
  3. Wire `pinky_critic_persona` into `CognitiveHub.run_division_of_labor()` and `PinkyNode`.
  4. Demarcate Deep Thought operational handshakes in `router.py` (`_spawn_deep_thought_preamble`) to `type="crosstalk"`.
  5. Add conversational onramp templates (*"While you were away..."*, *"By the way, we had a failure in..."*) to `pinky_node.py` and `brain_node.py`.
  6. Create in-process integration test suite `test_sprint61_integration.py` verifying full regression.

---

### **Story 61.5: [OPS-01] Mandatory Lab Stack Restart & Live-Fire Gauntlet**
* **Status**: 🔲 **PLANNED (AGY Orchestrator)**
* **Target Files**:
  * `HomeLabAI/src/tests/test_live_sprint61_e2e.py`
* **Scope**:
  1. Restart `acme-lab.service` via `systemctl --user restart acme-lab`.
  2. Respect [FEAT-136] Quiescence 60s stability window.
  3. Execute `test_live_sprint61_e2e.py` on `ws://127.0.0.1:8765`:
     * Test 1: Live Meta Query (*"Pinky, what is the status of our audio pipeline and sweeper?"*) $\rightarrow$ Verifies `FEAT-059` / `LAB-099` details with zero Intel PAE mentions.
     * Test 2: Deep Thought Handshake $\rightarrow$ Verifies received in `CROSSTALK`, not `CHAT`.
     * Test 3: Pinky Critic $\rightarrow$ Verifies cartoon quip + summary without robotic praise.
     * Test 4: Negative RAG Gating $\rightarrow$ Ambiguous query produces clean response with zero hallucinated career notes.

---

## 🧭 Execution Order

1. **Story 61.1**: Delegate `triage_gateway.py` to OpenAgent.
2. **Story 61.2**: Delegate `lab_dna_router.py` to OpenAgent.
3. **Story 61.3**: Delegate `pinky_critic_persona.py` to OpenAgent.
4. **Story 61.4**: Core Orchestrator Wiring, Stream Demarcation & Integration Suite (`test_sprint61_integration.py`).
5. **Story 61.5**: Lab Stack Restart (`acme-lab.service`) & Live-Fire WebSocket Gauntlet (`test_live_sprint61_e2e.py`).
6. **Feature Links & Docs**: Update `FeatureTracker.md` and rebuild Field Notes.
