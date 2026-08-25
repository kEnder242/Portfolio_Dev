# 🚀 Sprint Plan SPR-61.0: Modular Triage Engine Refactoring, Epistemic Meta-Grounding & Conversational Flow

**Sprint:** 61.0  
**Date:** August 25, 2026  
**Status:** GREENLIGHT READY  
**Theme:** *Decoupled Triage Satellite, "Zero Context > Default Context" Gateway, Speaker Demarcation, and Cartoon/Summary Persona Dynamics*

---

## 🧭 Executive Summary & Architectural Consensus

Following the successful baseline of Sprint 60 and deep forensic review of live evaluation logs (`evaluation_batch_20260825_142951.log` and `152025.log`), we established clear consensus on the core root cause of conversational thrash:

> **The Core Consensus:**
> 1. **Defaults = Bad Assumptions**: When triage hit ambiguous inputs, hardcoded few-shot template placeholders (`<silicon_term_or_pcie_ras>`) were emitted literally, and `ArchiveNode` defaulted to dense 18-year career notes (`notes_2018_PAE.txt`). This default context actively misled the resident models into hallucinating 2018 Intel Federal PAE history for general lab status queries.
> 2. **Zero Context > Default Context (`[FEAT-467]`)**: When intent or domain is uncertain, the system must provide *zero context* (or minimal context) rather than injecting hallucinated career history.
> 3. **The Triage Engine Must Be Refactored Now (`[FEAT-468]`)**: In Sprint 60, we deferred Triage to protect async streaming stability. Live testing proved Triage is the exact epicenter of all persona confusion and echo-looping. We now tackle Triage as a dedicated, pure decision satellite with explicit concurrency boundaries.
> 4. **Multi-Agent Speaker Demarcation & Anti-Duplication Rule**:
>    * **Internal Only**: Speaker tags (`[USER: Jason]`, `[ASSISTANT: Brain]`, `[ASSISTANT: Pinky]`) are used *strictly inside the internal LLM prompt context*.
>    * **Zero Name Stacking**: Outgoing chat strings are strictly scrubbed of all `[PINKY]`, `Pinky:`, or `[ASSISTANT]` prefixes before WebSocket broadcast so the UI never prints duplicated names (e.g. `Pinky: [ASSISTANT: Pinky] Pinky says...`).
> 5. **DNA Scoping (`[FEAT-469]`)**: The mice receive `feature_dna` and `lab_infrastructure` to ground live lab operations, while `behavioral_dna` is strictly reserved for AGY development workflows.
> 6. **Authentic Pinky Critic Persona (`[FEAT-470]`)**: Replace robotic `"well-crafted response"` praise with a satirical Pinky cartoon quip reacting to Brain's complexity paired with an agreed 1-sentence technical summary.

---

## 🏛️ Architectural Boundary Definition (The Triage Refactor Contract)

To completely eliminate preemption and concurrency risks while extracting Triage:

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│ ARCHITECTURAL BOUNDARY PARTITION                                                         │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ WHAT STAYS IN COGNITIVE HUB (Orchestration & Streaming):                                 │
│  - Async WebSocket token streaming loop (_process_node_stream(), waterfall_queue)        │
│  - Resident ignition mutex & connection lifecycle management                             │
│  - Multi-stage Division of Labor execution and client disconnect handling                 │
│                                                                                          │
│ WHAT MOVES INTO TRIAGE ENGINE SATELLITE (Decision Logic & Sanitization):                 │
│  - Speaker-demarcated turn parsing (extract_latest_user_query, format_speaker_history)   │
│  - Lean 4-field JSON guided schema generator optimized for Llama-3.2-3B                  │
│  - HyDE template placeholder scrubber (<...>) & Zero Context fallback                    │
│  - Meta-lexicon classifier (mapping live lab modules to vibe="META")                     │
│  - Attribution of pre-reflection directly to Brain (Insight)                            │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛡️ Anti-Duplication & Prefix Scrubbing Contract

To prevent name stacking thrash:
* **The Rule**: Demarcation tags exist **only in the model's internal prompt memory**.
* **The Gatekeeper Function**: `sanitize_outgoing_chat_text(text: str) -> str`:
  ```python
  # Strips all internal role/name prefixes so UI renders only the clean message:
  clean = re.sub(r"^\[(?:ASSISTANT|USER|PINKY|BRAIN|ME|SYSTEM|DEEP THOUGHT)[^\]]*\]:?\s*", "", text, flags=re.IGNORECASE)
  clean = re.sub(r"^(?:Pinky|Brain|System|Deep Thought):\s*", "", clean, flags=re.IGNORECASE)
  ```
* **UI Output**: WebSocket frame contains `"brain_source": "Pinky"` and `"brain": "Poit! Looking good!"`. The browser renders `Pinky: Poit! Looking good!` (clean single attribution).

---

## 🛠️ Delegation BKM & Pathing Mandate

1. **Satellite Cleanliness**: All greenfield satellites use standard library imports and top-level absolute paths with zero relative-import ambiguity.
2. **Mandatory Lint & Test Gate**: Subagent dispatches in `delegate.py` enforce:
   `--verification "ruff check <target_files> && pytest <test_files> -v"`
3. **Mandatory Post-Delegation ICM Capture Protocol (BKM-034 Section 12)**:
   Immediately upon story completion and test certification, the Orchestrator executes an `icm store -t errors-resolved` capturing subagent reflection and resolutions before proceeding.

---

## 📋 Granular Story Breakdown & Delegation Matrix

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│ SPRINT 61 DELEGATION TOPOLOGY                                                            │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ Story 61.1: triage_engine.py        ──(OpenAgent Subagent)──> 25+ Unit Tests (Green)      │
│ Story 61.2: lab_dna_router.py      ──(OpenAgent Subagent)──> 20+ Unit Tests (Green)      │
│ Story 61.3: pinky_critic_persona.py──(OpenAgent Subagent)──> 20+ Unit Tests (Green)      │
│                                                                                          │
│ Story 61.4: Core Wiring & Onramps  ──(AGY Orchestrator)───> Hub / Router / ArchiveNode   │
│ Story 61.5: Stack Bounce & E2E     ──(AGY Orchestrator)───> ws://127.0.0.1:8765 Gauntlet │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### **Story 61.1: [FEAT-467/468] Decoupled Triage Engine Satellite (`triage_engine.py`)**
* **Status**: 🔲 **READY FOR DELEGATION**
* **Target Files**:
  * `HomeLabAI/src/logic/triage_engine.py`
  * `HomeLabAI/src/tests/test_triage_engine.py`
* **Satellite Responsibilities**:
  1. `extract_latest_user_query(turn_or_history: str) -> str`: Extracts exclusively the latest user command, stripping `[ME]`, `[USER]`, or speaker prefixes.
  2. `format_speaker_history(history_turns: List[Dict[str, str]]) -> str`: Formats internal prompt memory with `[USER: Jason]`, `[ASSISTANT: Brain]`, `[ASSISTANT: Pinky]` tags.
  3. `sanitize_outgoing_chat_text(text: str) -> str`: Strips all internal role/speaker prefixes from generated output so no duplicated name tags reach the UI.
  4. `scrub_hyde_vector(hyde_text: str) -> str`: Strips literal angle brackets (`<...>`) or zeroes out string if invalid (enforcing Zero Context rule).
  5. `is_meta_lexicon(query: str) -> bool`: Identifies live system component keywords (`audio_pipeline`, `maintenance_sweeper`, `override_parser`, `foyer`, `vllm`, `attendant`, `residents`, `features`, `bkm`).
  6. `classify_vibe_and_domain(query: str, parsed_json: Dict[str, Any]) -> Tuple[str, str]`: Enforces `vibe="META"` and `domain="lab_internal"` when lexicon matches.
  7. `TriageEngine` class with async `evaluate_triage(turn: str, history: List[Dict], resident_caller: Any) -> Dict[str, Any]`.
* **Delegation Command**:
  ```bash
  python3 HomeLabAI/src/tests/delegate.py --story 61.1 \
    --title "Build Decoupled Triage Engine Satellite (FEAT-467/468)" \
    --file "src/logic/triage_engine.py" \
    --details "Create a pure, decoupled satellite module src/logic/triage_engine.py implementing extract_latest_user_query, format_speaker_history, sanitize_outgoing_chat_text, scrub_hyde_vector, is_meta_lexicon, classify_vibe_and_domain, and the TriageEngine class. Ensure sanitize_outgoing_chat_text removes any leading [PINKY], [BRAIN], [ASSISTANT:...], or Pinky: prefixes from generated output to prevent name duplication in the UI. Ensure scrub_hyde_vector strips template angle brackets like <silicon_term_or_pcie_ras> and returns empty string on ambiguous input. Support resident_caller via call_tool('think', ...) or native think(). Create test_triage_engine.py with at least 25 unit tests covering all functions, edge cases, and dirty inputs." \
    --verification "ruff check src/logic/triage_engine.py src/tests/test_triage_engine.py && pytest src/tests/test_triage_engine.py -v" \
    --dir "/home/jallred/Dev_Lab/HomeLabAI"
  ```

---

### **Story 61.2: [FEAT-469] Lab DNA Router Satellite (`lab_dna_router.py`)**
* **Status**: 🔲 **READY FOR DELEGATION**
* **Target Files**:
  * `HomeLabAI/src/nodes/lab_dna_router.py`
  * `HomeLabAI/src/tests/test_lab_dna_router.py`
* **Satellite Responsibilities**:
  1. `get_collection_priorities(vibe: str, domain: str) -> List[str]`: For `vibe="META"` or `domain="lab_internal"`, returns `["feature_dna", "lab_infrastructure", "lab_journal"]` and strictly omits `career_ledger` and `behavioral_dna`. For `domain="lab_history"`, returns `["career_ledger", "artifact_vault"]`.
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
* **Satellite Responsibilities**:
  1. `build_critic_prompt(brain_brief: str, user_query: str) -> str`: Instructs Pinky to output JSON containing: `quip` (a witty/satirical cartoon reaction to Brain's complexity), `summary` (a crisp 1-sentence agreed takeaway), `score` (int 1-5), and `slop_found` (bool).
  2. `parse_critic_payload(raw_output: str) -> Dict[str, Any]`: Parses JSON payload, strips markdown fences, validates keys, and cleans up formatting.
  3. `format_chat_delivery(parsed_critic: Dict[str, Any]) -> str`: Returns combined quip and summary string for out-loud delivery, banning robotic boilerplate (`"A well-crafted response"`) and stripping leading persona tags so UI output is clean.
  4. `format_crosstalk_telemetry(parsed_critic: Dict[str, Any]) -> Dict[str, Any]`: Returns telemetry frame for internal `CROSSTALK` broadcast.
* **Delegation Command**:
  ```bash
  python3 HomeLabAI/src/tests/delegate.py --story 61.3 \
    --title "Build Pinky Critic Persona Satellite (FEAT-470)" \
    --file "src/nodes/pinky_critic_persona.py" \
    --details "Create a pure, decoupled satellite module src/nodes/pinky_critic_persona.py implementing build_critic_prompt, parse_critic_payload, format_chat_delivery, and format_crosstalk_telemetry. Ensure format_chat_delivery blends a witty cartoon quip with an agreed technical summary while rejecting robotic boilerplate like 'A well-crafted response' and stripping any leading speaker name prefixes. Create test_pinky_critic_persona.py with at least 20 unit tests." \
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
  * `HomeLabAI/src/nodes/brain_node.py`
  * `HomeLabAI/src/tests/test_sprint61_integration.py`
* **Scope**:
  1. Wire `triage_engine` into `CognitiveHub.process_query()` and `_process_turn()`.
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
     * Test 3: Pinky Critic $\rightarrow$ Verifies cartoon quip + summary without robotic praise or name duplication.
     * Test 4: Negative RAG Gating $\rightarrow$ Ambiguous query produces clean response with zero hallucinated career notes.

---

## 🧭 Execution Order

1. **Story 61.1**: Delegate `triage_engine.py` to OpenAgent $\rightarrow$ Run ICM Handover Capture.
2. **Story 61.2**: Delegate `lab_dna_router.py` to OpenAgent $\rightarrow$ Run ICM Handover Capture.
3. **Story 61.3**: Delegate `pinky_critic_persona.py` to OpenAgent $\rightarrow$ Run ICM Handover Capture.
4. **Story 61.4**: Core Orchestrator Wiring, Stream Demarcation & Integration Suite (`test_sprint61_integration.py`).
5. **Story 61.5**: Lab Stack Restart (`acme-lab.service`) & Live-Fire WebSocket Gauntlet (`test_live_sprint61_e2e.py`).
6. **Feature Links & Docs**: Update `FeatureTracker.md` and rebuild Field Notes.
