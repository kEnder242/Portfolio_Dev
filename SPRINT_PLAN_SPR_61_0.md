# 🚀 Sprint Plan SPR-61.0: Modular Triage Engine Refactoring, Epistemic Meta-Grounding & Conversational Flow

**Sprint:** 61.0  
**Date:** August 25, 2026  
**Status:** ✅ DELIVERED & VERIFIED  
**Theme:** *Decoupled Triage Satellite, "Zero Context > Default Context" Gateway, Speaker Demarcation, and Cartoon/Summary Persona Dynamics*

---

## 🧭 Executive Summary & Architectural Consensus

Following the successful baseline of Sprint 60 and deep forensic review of live evaluation logs (`evaluation_batch_20260825_142951.log` and `152025.log`), we established clear consensus on the core root cause of conversational thrash:

> **The Core Consensus:**
> 1. **Defaults = Bad Assumptions**: When triage hit ambiguous inputs, hardcoded few-shot template placeholders (`<silicon_term_or_pcie_ras>`) were emitted literally, and `ArchiveNode` defaulted to dense 18-year career notes (`notes_2018_PAE.txt`). This default context actively misled the resident models into hallucinating 2018 Intel Federal PAE history for general lab status queries.
> 2. **Zero Context > Default Context (`[FEAT-467]`)**: When intent or domain is uncertain, the system must provide *zero context* (or minimal context) rather than injecting hallucinated career history.
> 3. **The Triage Engine Must Be Refactored Now (`[FEAT-468]`)**: In Sprint 60, we deferred Triage to protect async streaming stability. Live testing proved Triage is the exact epicenter of all persona confusion and echo-looping. We now tackle Triage as a dedicated, pure decision satellite with explicit concurrency boundaries.
> 4. **Dynamic Speaker Demarcation & Anti-Duplication (`SpeakerRegistry`)**:
>    * **Structural Primary (Option 2)**: Formats history as native chat message envelopes (`{"role": "assistant", "name": "Pinky", ...}`) so LLMs generate pure content without persona self-tagging.
>    * **Dynamic Registry Fallback (Option 1)**: Employs a runtime-compiled `SpeakerRegistry` that dynamically generates prefix-scrubbing patterns from active registered personas, eliminating hardcoded regex tech debt.
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
│  - SpeakerRegistry dynamic runtime sanitizer (strips leading prefixes automatically)     │
│  - Lean 4-field JSON guided schema generator optimized for Llama-3.2-3B                  │
│  - HyDE template placeholder scrubber (<...>) & Zero Context fallback                    │
│  - Meta-lexicon classifier (mapping live lab modules to vibe="META")                     │
│  - Attribution of pre-reflection directly to Brain (Insight)                            │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛡️ Dynamic Speaker Registry Pattern (`SpeakerRegistry`)

To eliminate regex maintenance debt:
```python
class SpeakerRegistry:
    """Dynamic speaker sanitizer that scales automatically with registered personas."""
    def __init__(self, names: list[str] | None = None):
        self.names = names or [
            "Pinky", "Brain", "Deep Thought", "Archive", "Lab",
            "Jason", "User", "Assistant", "System", "Me"
        ]
        escaped_names = "|".join(re.escape(n) for n in self.names)
        self._pattern = re.compile(
            rf"^(?:\[(?:{escaped_names})(?::[^\]]*)?\]|\b(?:{escaped_names})\b:)\s*",
            flags=re.IGNORECASE,
        )

    def sanitize(self, text: str) -> str:
        if not text:
            return ""
        prev: str | None = None
        curr = text.strip()
        while prev != curr:
            prev = curr
            curr = self._pattern.sub("", curr).strip()
        return curr
```

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
│ SPRINT 61 DELEGATION TOPOLOGY (ALL DELIVERED & VERIFIED)                                 │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ Story 61.1: triage_engine.py        ──(OpenAgent Subagent)──> 67 Unit Tests (PASS)       │
│ Story 61.2: lab_dna_router.py      ──(OpenAgent Subagent)──> 32 Unit Tests (PASS)       │
│ Story 61.3: pinky_critic_persona.py──(OpenAgent Subagent)──> 45 Unit Tests (PASS)       │
│ Story 61.4: Core Wiring & Onramps  ──(AGY Orchestrator)───> 15 Integration Tests (PASS) │
│ Story 61.5: Stack Bounce & E2E     ──(AGY Orchestrator)───> ws://127.0.0.1:8765 (PASS)   │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### **Story 61.1: [FEAT-467/468] Decoupled Triage Engine Satellite (`triage_engine.py`)**
* **Status**: ✅ **DELIVERED & VERIFIED (67/67 Tests Green)**
* **Target Files**:
  * `HomeLabAI/src/logic/triage_engine.py`
  * `HomeLabAI/src/tests/test_triage_engine.py`
* **Satellite Responsibilities**:
  1. `SpeakerRegistry`: Implements dynamic runtime regex compiler from persona list to sanitize outgoing text.
  2. `extract_latest_user_query(turn_or_history: str) -> str`: Extracts exclusively the latest user command, stripping `[ME]`, `[USER]`, or speaker prefixes via `SpeakerRegistry`.
  3. `format_speaker_history(history_turns: List[Dict[str, str]]) -> str`: Formats internal prompt memory with `[USER: Jason]`, `[ASSISTANT: Brain]`, `[ASSISTANT: Pinky]` tags.
  4. `scrub_hyde_vector(hyde_text: str) -> str`: Strips literal angle brackets (`<...>`) or zeroes out string if invalid (enforcing Zero Context rule).
  5. `is_meta_lexicon(query: str) -> bool`: Identifies live system component keywords (`audio_pipeline`, `maintenance_sweeper`, `override_parser`, `foyer`, `vllm`, `attendant`, `residents`, `features`, `bkm`).
  6. `classify_vibe_and_domain(query: str, parsed_json: Dict[str, Any]) -> Tuple[str, str]`: Enforces `vibe="META"` and `domain="lab_internal"` when lexicon matches.
  7. `TriageEngine` class with async `evaluate_triage(turn: str, history: List[Dict], resident_caller: Any) -> Dict[str, Any]`.

---

### **Story 61.2: [FEAT-469] Lab DNA Router Satellite (`lab_dna_router.py`)**
* **Status**: ✅ **DELIVERED & VERIFIED (32/32 Tests Green)**
* **Target Files**:
  * `HomeLabAI/src/nodes/lab_dna_router.py`
  * `HomeLabAI/src/tests/test_lab_dna_router.py`
* **Satellite Responsibilities**:
  1. `get_collection_priorities(vibe: str, domain: str) -> List[str]`: For `vibe="META"` or `domain="lab_internal"`, returns `["feature_dna", "lab_infrastructure", "lab_journal"]` and strictly omits `career_ledger` and `behavioral_dna`. For `domain="lab_history"`, returns `["career_ledger", "artifact_vault"]`.
  2. `filter_candidate_context(candidates: List[Dict[str, Any]], vibe: str, domain: str, max_distance: float = 0.50) -> List[Dict[str, Any]]`: Implements "Zero Context > Default Context". If top candidate distance > max_distance, returns empty list.
  3. `format_lab_dna_tag(coll: str, metadata: Dict[str, Any], doc: str) -> str`: Formats extracted context with `[FEATURE_DNA: FEAT-xxx]` and `[INFRA: component]` tags.

---

### **Story 61.3: [FEAT-470] Pinky Critic Persona Satellite (`pinky_critic_persona.py`)**
* **Status**: ✅ **DELIVERED & VERIFIED (45/45 Tests Green)**
* **Target Files**:
  * `HomeLabAI/src/nodes/pinky_critic_persona.py`
  * `HomeLabAI/src/tests/test_pinky_critic_persona.py`
* **Satellite Responsibilities**:
  1. `build_critic_prompt(brain_brief: str, user_query: str) -> str`: Instructs Pinky to output JSON containing: `cartoon_retort`, `critique_suggestions`, and `banned_phrases`.
  2. `parse_critic_payload(raw_output: str) -> CriticResult`: Parses JSON payload, strips markdown fences, validates keys, and cleans up formatting.
  3. `format_chat_delivery(cartoon_retort: str, technical_summary: str) -> str`: Returns combined quip and summary string for out-loud delivery, banning robotic boilerplate (`"A well-crafted response"`) and sanitizing via `SpeakerRegistry`.
  4. `format_crosstalk_telemetry(...) -> Dict[str, Any]`: Returns telemetry frame for internal `CROSSTALK` broadcast.

---

### **Story 61.4: [CORE/ORCH] Core Wiring, Conversational Onramps & Stream Demarcation**
* **Status**: ✅ **DELIVERED & VERIFIED (15/15 Integration Tests Green)**
* **Target Files**:
  * `HomeLabAI/src/logic/cognitive_hub.py`
  * `HomeLabAI/src/nodes/archive_node.py`
  * `HomeLabAI/src/v5/foyer/router.py`
  * `HomeLabAI/src/nodes/pinky_node.py`
  * `HomeLabAI/src/nodes/brain_node.py`
  * `HomeLabAI/src/tests/test_sprint61_integration.py`
* **Accomplishments**:
  1. Integrated `triage_engine` into `CognitiveHub.process_query()`, attributing pre-reflection to `Brain (Insight)` and routing meta queries to `vibe="META"` / `domain="lab_internal"`.
  2. Integrated `lab_dna_router` into `ArchiveNode.get_context()`, prioritizing `feature_dna` and `lab_infrastructure` and enforcing the Zero Context gate.
  3. Integrated `pinky_critic_persona` into `CognitiveHub.evaluate_grounding()`, broadcasting critic telemetry to `crosstalk` and sending witty cartoon quips + crisp summaries to `chat`.
  4. Demarcated Deep Thought operational handshakes in `router.py` (`_spawn_deep_thought_preamble`) to `type="crosstalk"`.
  5. Added conversational onramp directives to `pinky_node.py` and `brain_node.py`.
  6. Verified complete suite: **159/159 tests passing in < 8s**.

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

---

## 🔬 Post-Sprint Architecture Addendum: Meta Taxonomy & Supervisory Feedback Grammar

### 1. Structural Distinction: System Infrastructure vs. Meta-Cognitive Supervisory Guidance

```
                                  USER INPUT
                                      │
               ┌──────────────────────┴──────────────────────┐
               ▼                                             ▼
     [INFRASTRUCTURE META]                         [SUPERVISORY / FEEDBACK META]
  "What is the audio pipeline state?"            "The critic phase needs tuning; 
  "Is the vLLM engine running?"                   use Pinky cartoon quips instead."
               │                                             │
               ▼                                             ▼
  Queries CLaRa Vector Store                     Intercepted by Feedback Engine
  (feature_dna, lab_infrastructure)              Updates Session Memory / Whiteboard
  Zero Career Notes. No hallucination.           Acknowledges architectural coaching.
```

- **`lab_internal` (CLaRa Retrieval)**: Ground truth repository of the lab’s code and hardware (`feature_dna`, `lab_infrastructure`, `lab_journal`). Retrieves feature specs with Zero Context fallback.
- **`META` (Conversational Vibe)**: Conversational mode indicating the user is speaking about the lab's operating environment, actors, or conversational cadence (not external silicon or historical PAE projects).

### 2. The Supervisory Feedback Grammar

| Characteristic | Linguistic Indicators | Intended System Action |
|:---|:---|:---|
| **Actor Referencing** | *"the critic phase"*, *"Pinky"*, *"Brain"*, *"Deep Thought"*, *"triage"* | Directs specific personas rather than requesting external research. |
| **Language of Expectation & Normative Steering** | *"I think you need to"*, *"needs some tuning"*, *"less useful than"*, *"should belong in"*, *"would be more ideal"*, *"makes the cadence work better"* | Establishes architectural intent and behavioral constraints (SOP/BKM coaching). |
| **Stream & Cadence Awareness** | *"in crosstalk"*, *"Brain's insight"*, *"introduce it naturally"*, *"cadence"*, *"prompted"* | Meta-evaluates user experience and WebSocket flow. |
| **Feedback Loop Closure** | Direct critique of an immediately preceding assistant turn | Calibrates prompt/persona alignment in real time. |

### 3. The 6-Part Vibe Taxonomy

1. **WYWO ("While You Were Out")**: Queries subconscious consolidation, dreaming, and background crystallization from short-term memory.
2. **Provenance / Self-Awareness**: Checks turn ledger and session context to explain *why* an actor spoke.
3. **Live Telemetry & Interleaved System Health**: Live NVML thermals, GPU VRAM, and summary of system logs.
4. **Multi-Agent Dynamics**: Reads `round_table_memory` and `crosstalk` buffer to inspect Pinky and Brain's debate.
5. **Sprints vs. Features**: Sprints are orchestrator/AGY agile concepts; residents interact with `feature_dna` and `lab_infrastructure`.
6. **Supervisory Feedback**: Direct architectural coaching from the Lab Director, acknowledging guidance and adjusting behavior without triggering external RAG.

