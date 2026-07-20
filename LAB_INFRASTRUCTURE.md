# 🏗️ Lab Infrastructure & Configuration

This document tracks system-level infrastructure changes, configuration patterns, and physical deployment decisions that affect the Lab but are not inherently "software features" (FEAT).

## [LAB-001] Hibernate Lean (H2) Default
**Status:** ACTIVE
**Date:** May 2026

### Context
vLLM supports a "Soft Sleep" (H1) mode where model weights are temporarily offloaded to CPU RAM to free up VRAM without destroying the inference process. However, on specific consumer hardware (e.g., Turing architecture, RTX 2080 Ti), the transition back from H1 (re-mapping weights to VRAM) frequently causes physical memory corruption, resulting in the model outputting high-entropy garbage ("Screaming", e.g., `!!!!!!!!!!`).

### Decision
The default idle hibernation state for the Lab has been pivoted from **H1 (Soft Sleep)** to **H2 (Lean Sleep)**. 

### Mechanism
- **H2 (Lean Sleep)** involves a graceful SIGTERM of the vLLM engine process by the Lab Attendant, followed by an autonomous `Wake-on-Intent` re-ignition when the next query arrives.
- This guarantees a 100% clean silicon slate (VRAM purged and re-allocated) for every wake cycle, eliminating the risk of re-mapping corruption at the cost of a slightly longer wake latency (~15-20s vs ~5s).
- **Configuration**: This behavior is driven by the `vram_hibernation_level` key in `config/infrastructure.json` (Default: 2). The `--enable-sleep-mode` flag remains in the vLLM launch recipe to allow for future experimentation with H1 on newer vLLM builds or different hardware, but the Hub will not autonomously request H1 unless configured to do so.

---

## [LAB-002] ICM Hybrid Memory Pipeline (Daemon Embedding & Async Extraction)
**Status:** ACTIVE
**Date:** July 2026

### Context
During high-frequency OpenAgent developer subagent runs, the default CLI hook mechanism (`icm hook post`) cold-loaded ONNX/FastEmbed vector models on every tool turn. This resulted in 100%+ CPU spikes and 1.8GB-2.0GB RAM allocations per process spawn, thrashing system resources during rapid coding iterations.

### Decision
The Lab memory infrastructure has been updated to a **Hybrid Persistent Pipeline**:
1. **Daemon-Backed Vectorization:** Embedding calculations are offloaded to the resident ChromaDB/FastEmbed daemon, eliminating per-process ONNX model cold-starts and reducing idle RAM footprint to ~300MB.
2. **Deferred Async Extraction:** Synchronous per-tool-turn vector embeddings are replaced with an append-only JSONL event queue (`pending_queue.jsonl`). Event extraction and vector indexing are deferred to session pauses or `icm extract-pending` background sweeps.

### Mechanism
- Driven by `~/.config/icm/config.toml` (or OpenCode `icm` plugin configuration).
- Preserves 100% of persistent memory capabilities without impacting subagent execution speed or CPU/RAM budgets.

