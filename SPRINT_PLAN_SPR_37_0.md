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
    *   [ ] Write a telemetry benchmarking runner `bench_models.py` inside `Portfolio_Dev/field_notes/` that communicates with the active local endpoints (vLLM on port 8088/8765, Ollama on port 11434, and KENDER remote gateway). It must respect Turing 7.5 launch constraints (e.g., calling endpoints under active environment flags: `NCCL_SOCKET_IFNAME=lo`, `NCCL_P2P_DISABLE=1`, `VLLM_ATTENTION_BACKEND=XFORMERS`).
    *   [ ] Integrate local NVML checks to capture peak VRAM footprints during each model execution run, guarding against the "333MiB Wall" zombie VRAM deadlock.
    *   [ ] Update the build pipeline in [build_site.py](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/build_site.py) to execute `bench_models.py` and output a JSON cache containing the performance metrics.
    *   [ ] Redesign [benchmarks.html](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/benchmarks.html) to render these dynamic metrics.

### Story 2: RAG Evaluation Hardening & Drift Resolution
*   **Why**: Resolve the current collection drifts and de-duplication overlaps that are causing validation checks to fail in our Vector Store.
*   **Design**:
    *   Audit the ChromaDB index collection at `/home/jallred/AcmeLab/chroma_db` and identify misaligned boundaries.
    *   Implement structural fixes in `refine_gem.py` to prevent duplicate note clusters from diluting RAG recall.
*   **Tasks**:
    *   [ ] Scan the existing ChromaDB collection schema and identify corrupted indexes or relative path mappings.
    *   [ ] Update `refine_gem.py` to enforce absolute path sanitization and ignore calendar-day de-duplication overlaps beneath the 0.85 similarity threshold.
    *   [ ] Re-run the RAG evaluation suite and verify all baseline checks pass.

### Story 3: Pinky as the "Bicameral Foil" (Coherence Critic)
*   **Why**: Transition Pinky from a passive telemetry reader to an active strategic critic (The Foil), ensuring Brain's strategic output is grounded and free of conversational drift. This modernizes and extends **`[FEAT-356] Foil-Aware Memory (Unified Session Ledger)`**.
*   **Design**:
    *   Refactor Pinky's post-generation waterfall callback inside `acme_lab.py` to evaluate strategic thought coherence.
    *   If logic gaps or conversational slop are identified, Pinky interjects with a challenging retort, logging the feedback score directly to the RAG evaluation dataset.
*   **Tasks**:
    *   [ ] Update `round_table_memory` handling in `cognitive_hub.py` to persist Pinky's evaluations under a new `.round_table_evals.json` ledger.
    *   [ ] Inject a coherence evaluator model prompt for Pinky's "Foil" mode inside `acme_lab.py`.
    *   [ ] Validate the transition from single-turn amnesia to active coherence debate via unit tests in `src/debug/test_persona_bugs.py`.

### Story 4: Interleaved Log Console & Scorecard Alignment
*   **Why**: Keep aggregate stats centralized while embedding granular execution details into the timeline, improving situational awareness without tab bloat.
*   **Design**:
    *   Retain the aggregate RAG evaluation scorecard (Precision/Recall rates) under the main dashboard tab.
    *   Move individual query evaluation events to the chronological System Logs console as collapsible rows.
    *   Provide dense, terminal-style details under each log event (raw query string, vector distance, retrieved file path).
*   **Tasks**:
    *   [ ] Modify the status backend to output chronological interleaved logs (combining server status events, system alerts, and individual RAG query scores).
    *   [ ] Update [status.html](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/status.html) to render these log entries as collapsible [+] and [-] table rows.
    *   [ ] Verify the unified UI presentation across the Zero Trust local webserver.
