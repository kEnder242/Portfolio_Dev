# Sprint 37 – Bicameral Validation, Benchmarking & Coherence Judge

## Active Stories (Draft Stage)

### Story 1: Multi-Model Performance Benchmarking & Manifest Refinement
*   **Why**: Contrast latency and throughput performance across our heterogeneous model layout. We must measure the cost/benefit of vLLM (AWQ/LoRA) vs. Ollama fallback to optimize local VRAM allocation.
*   **Background / Historical Inspiration**:
    *   *The Blade Runner Forensic Audit* ([RETROSPECTIVE_BLADERUNNER_FORENSIC.md](file:///home/jallred/Dev_Lab/Portfolio_Dev/RETROSPECTIVE_BLADERUNNER_FORENSIC.md)): Retrospective of the 2026 hardware mismatch where vLLM failed to load Gemma 2 on the RTX 2080 Ti due to the lack of native `bfloat16` support (Compute 7.5). The discovery of `Llama-3.2-3B-AWQ` GGUF/AWQ blobs from the local Ollama store saved the VRAM budget (The Unity Pattern).
    *   *BKM Reproduction Log* ([docs/BKM_REPRODUCTION_LOG.md](file:///home/jallred/Dev_Lab/Portfolio_Dev/docs/BKM_REPRODUCTION_LOG.md)): Details the "Double Bind" where vLLM refuses `float16` for Gemma 2 and the 2080 Ti refuses `bfloat16`, forcing us to relegate Gemma 2 to Ollama (llama.cpp) for hybrid CPU/GPU fallback while Llama 3.2 remains our vLLM resident.
*   **Design**:
    *   Draft a benchmarking script to measure TTFT (Time to First Token) and overall tokens/sec for:
        1.  `Llama-3.2-3B-AWQ` (vLLM Resident).
        2.  `Gemma-2-2B` (Ollama Fallback).
        3.  `Qwen-2.5-Coder-3B` (Ollama Fallback).
        4.  `Qwen-27B` (Remote Sovereign on KENDER).
    *   Update [benchmarks.html](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/benchmarks.html) to present a side-by-side comparison matrix of these metrics.

### Story 2: RAG Evaluation Hardening & Drift Resolution
*   **Why**: Resolve the current collection drifts and de-duplication overlaps that are causing validation checks to fail in our Vector Store.
*   **Design**:
    *   Audit the ChromaDB index collection at `/home/jallred/AcmeLab/chroma_db` and identify misaligned boundaries.
    *   Implement structural fixes in `refine_gem.py` to prevent duplicate note clusters from diluting RAG recall.

### Story 3: Pinky as the "Bicameral Foil" (Coherence Critic)
*   **Why**: Transition Pinky from a passive telemetry reader to an active strategic critic (The Foil), ensuring Brain's strategic output is grounded and free of conversational drift.
*   **Design**:
    *   Refactor Pinky's post-generation waterfall callback inside `acme_lab.py`.
    *   Instruct Pinky to judge the coherence and factual grounding of the strategic thought.
    *   If logic holes are found, Pinky interjects with a challenging retort, logging the feedback score directly to the RAG evaluation dataset.

### Story 4: Interleaved Log Console & Scorecard Alignment
*   **Why**: Keep aggregate stats centralized while embedding granular execution details into the timeline, improving situational awareness without tab bloat.
*   **Design**:
    *   Retain the aggregate RAG evaluation scorecard (Precision/Recall rates) under the main dashboard tab.
    *   Move individual query evaluation events to the chronological System Logs console as collapsible rows.
    *   Provide dense, terminal-style details under each log event (raw query string, vector distance, retrieved file path).
