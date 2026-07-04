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
