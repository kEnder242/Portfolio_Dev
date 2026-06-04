# Acme Lab Research Ledger

## 📖 Integrated Concepts

### Observational Memory (OM)
- **Source:** [VentureBeat: Observational Memory cuts AI agent costs 10x](https://venturebeat.com/data/observational-memory-cuts-ai-agent-costs-10x-and-outscores-rag-on-long)
- **Key Takeaway:** Treating memory as a stream of observations (compressed state) rather than a bag of retrieval chunks.
- **Application:** The **Continuous Burn** (Librarian/Nibbler) should transition from indexing to **State Summarization**. Instead of "where is the note about PCIe?", Pinky should have a "State of the PCIe Validation" memory.
- **Implementation:** Background synthesis of daily "Observations" into a `compressed_history.json`.

### Bicameral Mind (Psychology/AI)
- **Concept:** The breakdown of the bicameral mind (Julian Jaynes). 
- **Application:** The Hub (`acme_lab.py`) simulates the "hallucinated voice" (Brain) that Pinky (the reactive agent) hears and interprets. 

### Unified Diffs (Patching)
- **Concept:** Robust file editing using standard Unix diffs.
- **Application:** The `patch_file` tool for agents to modify workspace documents without brittle string matching.

### Ear Graph Re-compilation
- **Concept:** Pre-compiling CUDA graphs for ASR/TTS to restore performance lost by the "Sledgehammer" fix.
- **Task:** Investigate NeMo's graph caching mechanism for specific driver/GPU offsets.

### Bicameral Awareness (Handover)
- **Concept:** Brain being "aware" of Pinky's preceding interaction context.
- **Application:** Prepending Pinky's triage to Brain prompts to enable banter and personality continuity.

### Memo-Memory Model (LLM Upgrades)
- **Source:** [VentureBeat: Memo Memory Model](https://venturebeat.com/orchestration/memo-memory-model-teams-upgrade-llm-without-retraining)
- **Concept:** Decoupling memory from weights to allow model upgrades without retraining.
- **Application:** Sprint 32 Upgrade strategy. Ensures our 18-year archive remains the "Gold Standard" truth even as the serving engine (vLLM) and base models (Qwen 3.6) evolve.

### RAG Myth-Busting (Problem Space)
- **Source:** [Towards Data Science: RAG is not Machine Learning](https://towardsdatascience.com/rag-is-not-machine-learning-and-the-ml-toolkit-solves-the-wrong-problem/)
- **Concept:** RAG is an information retrieval and engineering problem, not an ML problem.
- **Application:** Focus Sprint 32 on the **Retrieval Layer** (precision) rather than the **Model Layer** (reasoning) to reduce PECISTRESSOR hallucinations.

### RAG Cost Control (Efficiency)
- **Source:** [GitHub: rag-cost-control-layer](https://github.com/Emmimal/rag-cost-control-layer)
- **Concept:** Gating heavy retrieval behind cost/token-aware layers.
- **Application:** Tiered Retrieval. Use lightweight "Keyword Pings" for Tier 3 context, and "Sovereign Deep Thought" only for Tier 1 strategic gems.

### Memory OS (Operating Memory)
- **Source:** [GitHub: memory-os](https://github.com/ClaudioDrews/memory-os)
- **Concept:** Treating memory as a system-level resource with allocation/eviction policies.
- **Application:** Hardening the 3-Tier Memory model. Implement an "Eviction Policy" for the RAG Clipboard to prevent context-window drowning.
