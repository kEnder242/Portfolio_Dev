# Sprint 36 – ROLE TOKEN & RAG Synthesis

## Overview
This sprint captures the design discussion around the **waterfall template**, **KV‑cache strategy**, the introduction of a **ROLE TOKEN** to enable seamless Multi‑LoRA personality switching, and the integration of advanced retrieval patterns (KV-Cache Routing, Static GraphRAG, and Semantic Compass).

## Background
- The waterfall model prefixes a static prompt segment (e.g., *Mission Control*) before each user turn. This gives a reliable KV‑cache but forces a cache‑miss when the personality prefix changes.
- Introducing a single **ROLE TOKEN** (e.g., `<|PINKY|>`) inserted **after** the `PREVIOUS STAGE OUTPUT` and **before** the `USER PROMPT` allows the hub to switch LoRA adapters on‑the‑fly while preserving the cached static prefix.
- The token is mapped to a LoRA adapter in `loader.py`; during request processing the hub loads the corresponding adapter prior to generation.

## Research Integration & Synthesis Plan
Based on architectural evaluation under our local 11GB VRAM (2080 Ti) and static synthesis constraints, the following research anchors are integrated into this sprint's roadmap:

### 1. KV-Cache Routing (ArXiv 2606.32032)
- **Concept:** Share prefix context window caches across different LoRA/persona swaps.
- **Implementation:** Align vLLM's `--enable-prefix-caching` with prompt structures. The base model prefix (`[IDENTITY_BEDROCK] + [PREVIOUS STAGE OUTPUT]`) must be token-identical. The LoRA adapter is dynamically applied after encountering the `<|ROLE_TOKEN|>` boundary, preventing prefix cache invalidation.

### 2. Static GraphRAG
- **Concept:** Enrich semantic vector search with explicit relational edges.
- **Implementation:** Relationships are extracted by the AI Worker (`nibble_v2.py`) during note ingestion and stored inside monthly/yearly JSONs under `field_notes/data/`. A fast compilation pass in the index merging script (`merge_indices.py`) aggregates these pre-extracted relations into a static `graph_relations.json` lookup map. This ensures zero CPU/LLM runtime overhead and keeps the build pipeline lightweight.

### 3. Semantic Compass (MCompassRAG)
- **Concept:** Metadata-guided navigation using temporal anchors and relevance scoring.
- **Implementation & Fuzzy Date Handling:** 
  - *Concern:* Notes are grouped by calendar file year (e.g., `YYYY/MM.json`), but internal events often bridge calendar boundaries (e.g., a late-December note referencing early-January activities). Hard year filters cause retrieval blind spots.
  - *Mitigation:* The Semantic Compass will implement a **weighted temporal window**. The query parser will extract date hints and construct a target date anchor with an adjustable boundary (e.g., Target +/- 60 days). Candidates will be scored using a temporal decay function based on the event's *internal* date granularity rather than strict file boundaries.

## Implementation Tasks & Goals
The following detailed tasks are established to execute these features:

### Goal 1: KV-Cache Routing & Role Tokens
- **Why:** Swapping persona LoRAs typically causes vLLM to invalidate or bypass the prefix cache. We must isolate the dynamic weight adjustment so that the base model's prefix KV-cache remains shared and warm across all persona handovers.
- **Tasks:**
  - [ ] Implement `role_tokens.json` mapping file to pair special tokens (e.g., `<|PINKY|>`) with LoRA weight files.
  - [ ] Refactor the prompt builder to place the role token immediately after the static history segment.
  - [ ] Update `loader.py` to intercept the prompt, detect the role token, and issue the corresponding `lora_request` payload to the vLLM completion API.
  - [ ] Create benchmark tests measuring TTFT (Time-to-First-Token) to verify prefix cache hit rate remains > 95% across consecutive persona swaps.
- **Verification Plan:**
  - Create `field_notes/tests/test_role_token_cache.py` (referenced in [DIAGNOSTIC_RUNDOWN.md](file:///home/jallred/Dev_Lab/HomeLabAI/docs/DIAGNOSTIC_RUNDOWN.md)).
  - **BKM-015.1 Compliance Check:** Audit `loader.py` to ensure it implements dynamic mapping lookup via `role_tokens.json` registry. Hardcoded `if/else` or case switch blocks mapping special tokens to adapter paths in Python logic are strictly prohibited.
  - Script must trigger successive vLLM completions on a shared prefix containing alternative role tokens (e.g., `<|PINKY|>` then `<|BRAIN|>`).
  - Assert that the TTFT of the second prompt remains under 50ms, proving that the shared system prefix remained cached in vLLM's memory while dynamic LoRA switching was initiated.

### Goal 2: Relational Ingestion & GraphRAG Compilation
- **Why:** Simple keyword or vector searches cannot capture structural connections (e.g. "which sprint resolved this scar?"). Mapping these explicit edges resolves queries along engineering pedigree lines without external runtime graph databases.
- **Tasks:**
  - [ ] Update the AI worker prompts in `nibble_v2.py` to extract relationships as entity-relation triples (e.g., `[FEAT-030] -> consolidates -> [FEAT-172]`) and append them to event metadata.
  - [ ] Modify `merge_indices.py` to compile all extracted triples from `field_notes/data/*.json` into a single lookup file `field_notes/data/graph_relations.json`.
  - [ ] Add relationship traversal functions to `archive_node.py` that query the graph index to append related context (e.g. adjacent features or design documents) to the retrieval payload.
- **Verification Plan:**
  - Create `field_notes/tests/test_graph_compilation.py`.
  - **BKM-032 Structural Gate:** The automated script must validate only JSON structure and presence of relational nodes (e.g., checking that the compiled dictionary is valid JSON and contains adjacency keys). String-matching assertions on specific technical facts or names are forbidden in unit test assertions to preserve LLM flexibility.
  - Ingest a mock event with explicit relations, run `merge_indices.py`, and assert `graph_relations.json` compiles the edge list correctly.
  - Call `archive_node.py`'s `get_context` to request the mock event and verify that structurally adjacent entities are successfully retrieved and appended as context.
  - **BKM-032 Semantic Audit:** Capture the complete LLM reasoning trace of a GraphRAG retrieval output and execute a qualitative manual/AI audit using `semantic_audit_template.md` to verify that graph-traversed relationships improve factual synthesis without introducing semantic hallucinations.

### Goal 3: Fuzzy Temporal Compass Routing
- **Why:** Strict year filters miss events that bridge calendar transitions. We must perform date-aware scoring using the internal timestamps of individual logs rather than relying on file-system boundaries.
- **Tasks:**
  - [ ] Extend the search query parser in `archive_node.py` to identify fuzzy date anchors (e.g., "early 2025" or "late 2024").
  - [ ] Implement a temporal weight decay algorithm in `get_context` that scores candidate events based on their internal `date` attribute proximity to the anchor date.
  - [ ] Update RAG search to retrieve candidates from adjacent years and apply this decay factor to rank the final context payload.
- **Verification Plan:**
  - Create `field_notes/tests/test_fuzzy_temporal.py`.
  - **BKM-032 Mathematical/Structural Gate:** Automated assertions are restricted to verifying relative mathematical scoring (e.g., asserting that Candidate A's calculated weight is strictly greater than Candidate B's score due to chronological proximity). No string-matching on facts or raw summaries is permitted in the Python test.
  - Seed dummy entries in `data/2024.json` (dated `2024-12-28`) and `data/2025.json` (dated `2025-01-05`).
  - Query `get_context` with a "January 2025" temporal anchor.
  - Assert that both entries are retrieved, and verify that the closer date (`2025-01-05`) receives a higher ranking score than the boundary-spanning event (`2024-12-28`).
  - **BKM-032 Semantic Audit:** Verify that boundary-spanning context remains chronologically sound during synthesis. Confirm the LLM does not suffer from temporal displacement (e.g., asserting a future Jan 2025 event occurred prior to Dec 2024).

## Acceptance Criteria (Planning & Design Phase)
- [ ] Document token-to-adapter mappings in `role_tokens.json`.
- [ ] Implement prototype token injection inside the request processing pipeline.
- [ ] Verify prefix cache hit rate remains > 95% in vLLM when switching active LoRAs via the role token.
- [ ] Design the schema for the offline entity-relation map (`graph_relations.json`).
- [ ] Update `scan_pinky.py` and `scan_librarian.py` to extract relationships (e.g., `consolidated_by`, `milestone_of`) during static scanning.
- [ ] Refactor `archive_node.py`'s `get_context` to parse temporal boundaries and apply fuzzy weighted scoring based on internal event date granularity.
- [ ] Add unit tests verifying neighborhood retrieval accuracy for events spanning year-end boundaries.
- [ ] Conduct a manual/AI **BKM-032 Semantic Audit** on the output of both GraphRAG and Fuzzy Temporal Compass retrievals, saving the logs to the validation ledger before certification.

## OpenAgent Hybrid Execution (Verification Gate)
- [ ] Delegate the tokenizer extension and prototype unit tests to OpenAgent:
  * Execution: Run `opencode play feature/role-token-prototype` using the DeepSeek/Ollama parallel mapping.
  * Verification: Verify OpenAgent successfully implements and verifies the test suite without using Google Gemini tokens.

---

## Phase 2: The Semantic Annealing Pipeline
This phase integrates background self-evaluation with online/offline human feedback, creating a continuous improvement loop to refine retrieval accuracy and event data quality without manual test overhead.

### 1. The Core Design: Semantic Annealing
- **Subconscious Burn (The Ingestion & Consolidation):** Daily log scans (`nibble_v2.py`) and nightly consolidation (`dream_cycle.py`) create raw summaries and metadata.
- **Verification Pass (The Validation):** A background worker (`evaluate_rag.py`) runs queries against the RAG system and uses the Sovereign node (27B) to audit outputs, storing results in `validation_ledger.jsonl`.
- **Crystallization (The Feedback & Overrides):** Corrections from user chat (Online Review) or dashboard flags (Offline Review) write persistent override rules to `overrides.json`, which are applied during nightly aggregations to correct history.

### 2. Implementation Tasks & Goals

#### Goal 4: The Evaluation Worker & Validation Ledger
- **Why:** To run structural and qualitative evaluations of our retrieval methods (GraphRAG, Fuzzy Compass) passively in the background without locking developer resources.
- **Tasks:**
  - [ ] Create `field_notes/evaluate_rag.py` to execute queries from `config/validation_anchors.json` against the active RAG stack.
  - [ ] Update `evaluate_rag.py` to route retrieval traces to the KENDER (4090) Sovereign Node for BKM-032 auditing.
  - [ ] Implement atomic writing for `field_notes/data/validation_ledger.jsonl` to append structural scoring, cache hit rates, and audit logs.
  - [ ] Hook the evaluation worker into the `mass_scan.py` loop to run once per idle epoch.
- **Verification Plan:**
  - Execute `python3 field_notes/evaluate_rag.py` manually.
  - Verify `validation_ledger.jsonl` is written atomically and contains score metrics and qualitative notes.
  - Verify KENDER correctly processes the audit payload and logs findings.

#### Goal 5: Online & Offline Feedback Loop (Expert Overrides)
- **Why:** To capture real-world user corrections during chat sessions and persist them into the data collection without manually modifying historical JSON files.
- **Tasks:**
  - [ ] Create `field_notes/data/overrides.json` to store user-defined correction rules (e.g., matching a unique ID like `[GEM-x7f2]` to specific dates or tags).
  - [ ] Refactor the Hub's triage step in `cognitive_hub.py` to detect correction intent (e.g., *"GEM-x7f2 has the wrong year"*) and parse the ID and content.
  - [ ] Write the override writer in the Foyer to append the correction to `overrides.json`.
  - [ ] Update `aggregate_years.py` to load `overrides.json` and apply corrections to the calendar JSON files during the nightly compile.
- **Verification Plan:**
  - Inject a mock correction via the Intercom chat interface: *"that's not right! GEM-test has the wrong tag!"*
  - Assert that the Hub extracts the correction, and verify `overrides.json` is updated with the override rule.
  - Run `aggregate_years.py` and verify the output event matches the corrected metadata.

#### Goal 6: Semantic Merging (Anti-Exhaustion)
- **Why:** Continuous scan cycles will eventually exhaust raw notes, causing duplicate generation and database bloat. We must merge similar insights into existing records instead of writing duplicates.
- **Tasks:**
  - [ ] Implement a semantic similarity check (threshold > 0.85) inside `refine_gem.py` to compare new/recent insights with existing gems.
  - [ ] Write the merge logic to layer new evidence (e.g., additional files, verification runs) into the matching gem's JSON record, upgrading its rank to Diamond (4) instead of appending a new file.
- **Verification Plan:**
  - Seed an event in `data/2024.json`.
  - Trigger `refine_gem.py` with a highly similar mock insight (similarity > 0.85).
  - Verify that no duplicate event is appended, and assert that the existing event's evidence field is successfully enriched.

#### Goal 7: Dashboard Integration (status.html Panel)
- **Why:** To provide the user with a centralized, non-intrusive offline review space to inspect recent background insights and RAG validation metrics.
- **Tasks:**
  - [ ] Add a new panel in `field_notes/status.html` to display recent entries from `validation_ledger.jsonl` and pending insights.
  - [ ] Display unique reference IDs (e.g. `[GEM-xxxx]`) next to all draft insights to facilitate online voice/chat corrections.
- **Verification Plan:**
  - Open `status.html` in the browser.
  - Verify the validation metrics (cache hit rate, temporal accuracy) are rendered dynamically from `validation_ledger.jsonl`.
  - Verify draft insights render their unique reference IDs correctly.

---

## Acceptance Criteria (Phase 2)
- [ ] Create the RAG validation worker `field_notes/evaluate_rag.py`.
- [ ] Ensure `validation_ledger.jsonl` compiles and appends metrics atomically.
- [ ] Implement the `overrides.json` schema and Foyer parser for intent-driven corrections.
- [ ] Update `aggregate_years.py` to enforce expert overrides on compile.
- [ ] Refactor `refine_gem.py` with the 0.85 similarity merge gate.
- [ ] Update `status.html` to display validation health and draft gem IDs.
- [ ] Certify the entire Semantic Annealing pipeline via a round-trip test (mock ingestion -> automated evaluation -> simulated user correction -> override validation).

*No tasks are created yet; this file serves as the sprint narrative and reference for upcoming work.*




