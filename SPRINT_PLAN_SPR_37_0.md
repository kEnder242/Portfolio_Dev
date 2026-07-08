# Sprint 37 – Bicameral Validation, Benchmarking & Coherence Judge

## Active Stories & Task Ledger

### Story 1: Multi-Model Performance Benchmarking & Manifest Refinement
*   **Why**: Contrast latency and throughput performance across our heterogeneous model layout. We must measure the cost/benefit of vLLM (AWQ/LoRA) vs. Ollama fallback to optimize local VRAM allocation.
*   **Background / Historical Inspiration**:
    *   *The Blade Runner Forensic Audit* ([RETROSPECTIVE_BLADERUNNER_FORENSIC.md](file:///home/jallred/Dev_Lab/Portfolio_Dev/RETROSPECTIVE_BLADERUNNER_FORENSIC.md)): Retrospective of the 2026 hardware mismatch where vLLM failed to load Gemma 2 on the RTX 2080 Ti due to the lack of native `bfloat16` support (Compute 7.5). The discovery of `Llama-3.2-3B-AWQ` GGUF/AWQ blobs from the local Ollama store saved the VRAM budget (The Unity Pattern).
    *   *BKM Reproduction Log* ([docs/BKM_REPRODUCTION_LOG.md](file:///home/jallred/Dev_Lab/Portfolio_Dev/docs/BKM_REPRODUCTION_LOG.md)): Details the "Double Bind" where vLLM refuses `float16` for Gemma 2 and the 2080 Ti refuses `bfloat16`, forcing us to relegate Gemma 2 to Ollama (llama.cpp) for hybrid CPU/GPU fallback while Llama 3.2 remains our vLLM resident.
*   **Benchmarking Metrics (HF/vLLM Inspired Standards)**:
    *   **TTFT (Time to First Token)**: Latency in milliseconds between request submission and first generated token (interactive responsiveness indicator).
    *   **ITL (Inter-Token Latency)**: Average delay between subsequent tokens (readability speed indicator).
    *   **Throughput**: Generation speed in tokens/second.
    *   **VRAM Peak Footprint**: Active GPU memory overhead measured via NVML/DCGM telemetry during peak load.
*   **Design**:
    *   Draft a benchmarking script to measure TTFT, ITL, and throughput for:
        1.  `Llama-3.2-3B-AWQ` (vLLM Resident).
        2.  `Gemma-2-2B` (Ollama Fallback).
        3.  `Qwen-2.5-Coder-3B` (Ollama Fallback).
        4.  `Qwen-27B` (Remote Sovereign on KENDER).
    *   Update [benchmarks.html](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/benchmarks.html) to present a console-dense side-by-side comparison table using simple horizontal bar visualizations (Class 1 CSS flexboxes) to compare TTFT/Throughput.
*   **Tasks**:
    *   [x] Write a telemetry benchmarking runner `bench_models.py` inside `Portfolio_Dev/field_notes/` that communicates with the active local endpoints (vLLM on port 8088/8765, Ollama on port 11434, and KENDER remote gateway). It must respect Turing 7.5 launch constraints (e.g., calling endpoints under active environment flags: `NCCL_SOCKET_IFNAME=lo`, `NCCL_P2P_DISABLE=1`, `VLLM_ATTENTION_BACKEND=XFORMERS`).
    *   [x] Integrate local NVML checks to capture peak VRAM footprints during each model execution run, guarding against the "333MiB Wall" zombie VRAM deadlock.
    *   [x] Update the build pipeline in [build_site.py](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/build_site.py) to execute `bench_models.py` and output a JSON cache containing the performance metrics.
    *   [x] Redesign [benchmarks.html](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/benchmarks.html) to render these dynamic metrics.
    *   **Commit**: `443f426` — `feat(benchmarks): implement sprint-37 multi-model silicon performance benchmarking and dashboard`

### Story 2: RAG Evaluation Hardening & Drift Resolution
*   **Why**: Resolve the current collection drifts and de-duplication overlaps that are causing validation checks to fail in our Vector Store.
*   **Design**:
    *   Audit the ChromaDB index collection at `/home/jallred/AcmeLab/chroma_db` and identify misaligned boundaries.
    *   Implement structural fixes in `refine_gem.py` to prevent duplicate note clusters from diluting RAG recall.
*   **Root Cause Analysis**: The `validation_ledger.jsonl` shows keyword recall rates of 0.14 to 0.4, primarily because ChromaDB's `long_term_wisdom` collection contains loose semantic embeddings that match on general context rather than specific technical terms. The `archive_node.py` retrieval pipeline returns results from wrong years when the query lacks a strong temporal anchor. The user's commit `9ccc155` added strict year post-filtering (skip wrong year, skip undated items) to address the temporal drift.
*   **Tasks**:
    *   [x] Added strict year filtering to `archive_node.py` to skip results from wrong years when a specific temporal anchor is present in the query. (Commit: `9ccc155`)
    *   [ ] **Future Sprint**: Re-index the ChromaDB `long_term_wisdom` collection with higher-density embeddings (domain-tagged metadata) to improve keyword recall for domain-specific queries. This is a larger effort that requires running `bridge_burn_to_rag.py` with updated metadata tagging.
    *   [ ] **Future Sprint**: Expand `validation_anchors.json` test prompts to include domain-aware expected keywords that align with the current archive structure.

### Story 3: Pinky as the "Bicameral Foil" (Coherence Critic)
*   **Why**: Transition Pinky from a passive telemetry reader to an active strategic critic (The Foil), ensuring Brain's strategic output is grounded and free of conversational drift. This modernizes and extends **`[FEAT-356] Foil-Aware Memory (Unified Session Ledger)`**.
*   **Design**:
    *   Refactor Pinky's post-generation waterfall callback inside `cognitive_hub.py` to evaluate strategic thought coherence.
    *   If logic gaps or conversational slop are identified, Pinky interjects with a challenging retort, logging the feedback score directly to the RAG evaluation dataset.
*   **Tasks**:
    *   [x] Update `round_table_memory` handling in `cognitive_hub.py` to persist Pinky's evaluations under a new `.round_table_evals.json` ledger. (Commit: `9ccc155`)
    *   [x] Inject a coherence evaluator model prompt for Pinky's "Foil" mode inside `cognitive_hub.py`. The evaluator outputs a JSON block with `score`, `reasoning`, `slop_found`, and `retort` fields, using the `r'\{.*\}'` extraction pattern for robust JSON parsing. (Commit: `9ccc155`)
    *   [x] Record `turn_thought_trace` for Brain and Pinky responses, appending the full turn ledger to `round_table_memory` for persistent session context. (Commit: `9ccc155`)
    *   [x] Atomic write (`.tmp` + `os.replace`) for `.round_table_evals.json` per BKM-022. (Commit: `9ccc155`)
    *   [x] Fix `call_tool` keyword argument passing (`arguments=arguments`) to prevent positional arg mismatch errors. (Commit: `9ccc155`)
    *   [x] Extend triage JSON parsing to recognize `addressed_to` field for multi-party routing. (Commit: `9ccc155`)
    *   **Commit**: `9ccc155` — `feat: implement RAG evaluation strict year filtering and Coherence Judge critique log`

### Story 4: Interleaved Log Console & Scorecard Alignment
*   **Why**: Keep aggregate stats centralized while embedding granular execution details into the timeline, improving situational awareness without tab bloat.
*   **Design**:
    *   Retain the aggregate RAG evaluation scorecard (Precision/Recall rates) under the main dashboard tab.
    *   Move individual query evaluation events to the chronological System Logs console as collapsible rows.
    *   Provide dense, terminal-style details under each log event (raw query string, vector distance, retrieved file path).
*   **Tasks**:
    *   [x] Modified `pollPager()` in `status.html` to async-fetch both `pager_activity.json` and `validation_ledger.jsonl`, interleaving RAG evaluation entries into the chronological timeline. (Commit: `8a82eb8`)
    *   [x] Added `[+]`/`[-]` expand indicators to all alert rows, with correct toggle state preservation across poll refreshes. (Commit: `8a82eb8`)
    *   [x] Implemented detailed RAG evaluation expansion panel showing raw query, domain, retrieval time, keyword recall percentage, per-keyword hit/miss indicators, vector distance, retrieval source paths, and Kender Audit verdict with relevance/coverage scores. (Commit: `8a82eb8`)
    *   [x] Added `rag-eval` to both the artifact detection list and the Acme Lab source classification to ensure correct color-coding in the timeline. (Commit: `8a82eb8`)
    *   **Commit**: `8a82eb8` — `feat: interleave RAG query evaluations in status log console and implement +/- indicators`

### Story 5: Decoupled RAG Diagnostics & Ground Truth Chronology
*   **Why**: Resolve the low keyword recall rates (currently 14% to 40% in `validation_ledger.jsonl`) by upgrading the RAG retrieval pipeline to fetch actual raw note context, and eliminate dashboard latency by decoupling detailed evaluation logs from the main ledger.
*   **Historical Context & Current Baseline**:
    *   *RAG Recall Deficit*: Audit reports ([rag_search_pedigree.md](file:///home/jallred/.gemini/antigravity-cli/brain/d75e00e7-b3f5-4236-89ea-26c97eee308c/rag_search_pedigree.md)) indicate that while ChromaDB matches semantic categories (long-term wisdom Gems), the agent lacks specific technical details ("bones") because the acquisition stage in `get_context()` fails to fetch the raw note paragraphs for most matched entries.
    *   *MCP Status Hardening*: During Sprint 37, we resolved strategic profile loading failures by introducing a static [cv_3x3_summary.json](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/data/cv_3x3_summary.json) and implementing a dictionary-based defensive fallback in the `build_cv_summary` MCP tool (tested and passing in `test_tool_registry.py`).
    *   *Test Connectivity Fixes*: We corrected test connection failures in `test_memory_integration.py` and `test_mcp_integration.py` by transitioning connections to `localhost` (replacing the sluggish `z87-Linux.local` mDNS endpoint) and aligning the tests with V5 Foyer's immediate status-broadcasting handshake.
*   **Design & Architecture**:
    *   *Decoupled Diagnostic Storage*: Rather than writing the full retrieved context (up to 15KB per query) and the complete Kender audit conversation to the main `validation_ledger.jsonl`, `evaluate_rag.py` will write only a lightweight JSONL metadata row (timestamp, query, verdict, scores, and a new unique run file reference: `data/rag_runs/run_{timestamp}.json`). The heavy logs—including the full retrieved context, the expected keyword checklist, the hit/miss evaluation map, the complete Kender audit prompt, and Kender's raw API response—will be written to a dedicated JSON file in the gitignored `data/rag_runs/` directory.
    *   *Lazy-Load Expandable Dashboard Panel*: Refactor the `expandAlertDetail` Javascript function in `status.html` (lines 1153-1189) so that when a RAG log header is clicked, it dynamically performs a `fetch()` for the corresponding run JSON file, parsing and rendering the context and audit conversation in a beautiful, scrollable monospace panel. This preserves non-destructive timeline refreshes and prevents page-load latency.
    *   *Gems-to-Notes Ground Truth Connection*: In `archive_node.py`'s `get_context()`, the vector search collection (`long_term_wisdom`) acts as the "Discovery" index. Currently, when matches are found, the pipeline only inserts a reference string to the target file. We will modify `get_context()` so that for **all** retrieved candidates, it extracts the date (e.g. `2024-01-15`) and source file (e.g. `2024_01.json`), opens the raw JSON file, and copies the actual chronological text entry summary/details directly into the returned context string. This bridges the semantic-to-physical gap, providing the co-pilot with the actual ground truth notes.
    *   *Environment & Path Hardening*: Ensure all background tasks and tests run under the unified environment setup, setting `PYTHONPATH` explicitly (`export PYTHONPATH=$PYTHONPATH:$(pwd)/Portfolio_Dev/field_notes`) and utilizing absolute config paths to prevent execution failures in automated cron/nightly triggers.
*   **Tasks**:
    *   [x] **Task 5.1: Decoupled RAG Diagnostics Logging**
        *   *Why (Rationale)*: Storing full RAG query contexts and Kender audit interactions directly in `validation_ledger.jsonl` will bloat the file and slow down `status.html` page load. We must separate the heavy diagnostic logs from the main lightweight ledger.
        *   *How (Mechanism)*: Refactor `evaluate_rag.py` to generate a unique run ID (e.g. `run_YYYYMMDD_HHMMSS`), write only metadata to `validation_ledger.jsonl`, and write the full payload (retrieved context, expected keywords, keyword results mapping, Kender prompt/response) to a separate JSON file (`data/rag_runs/run_YYYYMMDD_HHMMSS.json`) using the Atomic File Swap Protocol (`.tmp` + `os.replace`).
        *   *Proof (Verification)*: Execute `evaluate_rag.py` and verify that a lightweight entry is added to `validation_ledger.jsonl`, and a detailed JSON file is created under `field_notes/data/rag_runs/` with valid JSON formatting.
    *   [x] **Task 5.2: Lazy-Load Expandable Dashboard Panel**
        *   *Why (Rationale)*: Expanding a RAG evaluation row currently only shows high-level metadata. To display the complete context and audit details without page-load lag, the UI must lazy-load the detailed logs only when requested.
        *   *How (Mechanism)*: Refactor the `expandAlertDetail` Javascript function in `status.html` (lines 1153-1189) so that for RAG logs, it performs an asynchronous `fetch()` to `data/rag_runs/run_YYYYMMDD_HHMMSS.json` and renders the context and audit response inside the expanded pre-formatted panel.
        *   *Proof (Verification)*: Load the dashboard in a browser, expand a RAG evaluation row, and verify that the browser fetches the specific JSON file and renders the full context text correctly.
    *   [x] **Task 5.3: Gems-to-Notes Ground Truth Connection**
        *   *Why (Rationale)*: Currently, `get_context()` only returns document anchors and references, leaving the resident models (Pinky/Brain) without the actual raw chronological note text. We must bridge the gap between vector semantic searches and raw date-based notes.
        *   *How (Mechanism)*: Refactor the raw acquisition stage of `get_context()` in `archive_node.py` (lines 789-828). For each retrieved candidate, extract the date/source, load the target JSON note file (e.g. `2024_01.json`), find the matching chronological entry, and inject its actual raw note text directly into the returned context string.
        *   *Proof (Verification)*: Run `pytest src/debug/test_tool_registry.py` and query the tool directly to verify the returned JSON context contains actual raw note paragraphs matching the candidate dates.
    *   [x] **Task 5.4: Environment & Path Hardening**
        *   *Why (Rationale)*: Background tasks and triggers fail if import paths or config targets are relative and context-dependent.
        *   *How (Mechanism)*: Refactor `evaluate_rag.py` to resolve configuration paths using absolute path utilities (`os.path.abspath`) instead of relative paths, and verify the PYTHONPATH requirements in execution scripts.
        *   *Proof (Verification)*: Execute `evaluate_rag.py` in a separate terminal shell without manual environment variables, verifying it runs and outputs successfully.

## Story 6: Resident Persona Polish & Triage Fidelity (Complete)
*   **Context (Why/How/Proof)**:
    *   *Lab Meta-Focus*: The topographical description in `IDENTITY_BEDROCK` dominated the attention of resident models (like Pinky). We reframed this positively to lead with the user's engineering domain, demoting topography to an operational footnote.
    *   *BANANA-5095 Hallucination*: Triage generated fake codes/projects. We constrained the triage `situation` field to paraphrase-only.
    *   *JSON Pretty-Printing*: Raw triage and critic JSON were streamed to the UI. We added frontend parsers to pretty-print them into compact system messages.
    *   *No-Sidebar Print Overrides*: We added a print media query to `style.css` to omit the sidebar, menu-toggle, and `#sys-console` in print output.
*   **Tasks**:
    *   [x] **Task 6.1: Persona Reframe (IDENTITY_BEDROCK)**
        *   *Why*: Reframing the topographical Bedrock stops models from narrating their own architecture when answering queries.
        *   *How*: Refactor `loader.py` to change `IDENTITY_BEDROCK` to focus on the platform telemetry engineering domain.
    *   [x] **Task 6.2: Constrain Triage Situation**
        *   *Why*: Prevents triage models from inventing hallucinated project or code references.
        *   *How*: Add grounding rule 6 to `LAB_SYSTEM_PROMPT` in `lab_node.py` to mandate paraphrase-only behavior for the `situation` field.
    *   [x] **Task 6.3: Frontend JSON Formatting & Print styling**
        *   *Why*: Removes raw JSON dumps from the chat console and allows printing `protocols.html` cleanly.
        *   *How*: Add guards to the crosstalk WebSocket handler in `intercom_v2.js` to parse and format triage and critic JSON. Add `@media print` overrides to `style.css` to hide `#sidebar` and `#sys-console` during printing.

---

### Story 7: ChromaDB DNA Integration for Swarm Context Efficiency
*   **Why**: The current OpenAgent delegation pattern (BKM-034) injects full text of `FeatureTracker.md` and `Protocols.md` into the context window of each session. For small local models (omnicoder-9b, gemma4:26b), this burns a significant fraction of the available KV cache before the first task token is generated. A local ChromaDB vector store can serve the same grounding data as concise, query-relevant snippets, reducing context pressure and improving task-following fidelity.
*   **Background / Reference**:
    *   [AGY_TO_OPENAGENT_PLAYBOOK.md §6](file:///home/jallred/Dev_Lab/Portfolio_Dev/AGY_TO_OPENAGENT_PLAYBOOK.md) documents the Dual-Collection architecture (`behavioral_dna` and `feature_dna`).
    *   The git pre-commit hook approach and Safe-Scalpel integration paths are already defined there.
*   **Design**:
    *   Implement `sync_chroma_dna.py` to parse and upsert `Protocols.md` (BKMs) into a `behavioral_dna` ChromaDB collection and `FeatureTracker.md` (FEATs) into a `feature_dna` collection, with metadata tags (`bkm_id`, `feat_id`, `status`, `tools`).
    *   Add a git pre-commit hook at `.git/hooks/pre-commit` to call `sync_chroma_dna.py` on every commit touching either source file.
    *   Modify the BKM-034 Surgical Handover Prompt Template to replace raw file references with a query call: `opencode run "query behavioral_dna: 'safe file patching' to retrieve relevant BKMs"`.
*   **Tasks**:
    *   [x] **Task 7.1: Write `sync_chroma_dna.py`**
        *   *Why*: Provides the ingestion pipeline to populate both ChromaDB collections from the markdown sources.
        *   *How*: Parse headers (`## BKM-XXX` and `## FEAT-XXX`) as chunk boundaries. Store full section text with `bkm_id`/`feat_id` metadata. Use `chromadb.PersistentClient` targeting `HomeLabAI/chroma_dna/`.
        *   *Proof*: Hook fired on commit `86d83aa` — 214 feature entries and 29 BKM entries synced successfully.
    *   [x] **Task 7.2: Install pre-commit hook**
        *   *Why*: Guarantees ChromaDB stays in sync with every protocol or feature edit without manual intervention.
        *   *How*: Write `.git/hooks/pre-commit` to conditionally run `sync_chroma_dna.py` only when `Protocols.md` or `FeatureTracker.md` are in the staged file set.
        *   *Proof*: Hook already active — fired on commit `86d83aa` and synced both collections without manual invocation.
    *   [ ] **Task 7.3: Update BKM-034 Handover Template**
        *   *Why*: Replaces verbose file injection with targeted ChromaDB retrieval queries in the handover prompt.
        *   *How*: Update `Protocols.md` BKM-034 step 5 template and `AGY_TO_OPENAGENT_PLAYBOOK.md` to show the ChromaDB-based retrieval pattern.
        *   *Proof*: Verify a sample handover prompt with ChromaDB query syntax retrieves the correct BKM sections when run against the populated collection.

