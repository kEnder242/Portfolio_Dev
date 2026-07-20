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

---

## [LAB-007] ChromaDB HTTP Vector Daemon (Port 8001)
**Status:** ACTIVE
**Date:** July 2026

### Context
Cold-loading PyTorch and SentenceTransformers in-process on every git pre-commit hook (`sync_chroma_dna.py`) was causing 15–20s commit delays.

### Decision
Established **`chroma-server.service`** as a systemd user daemon running on port 8001 (`ExecStart=chroma run --path ~/AcmeLab/chroma_db --port 8001`).

### Mechanism
- Configured with `MemoryHigh=1G`, `MemoryMax=1.5G`, and systemd circuit breaker limits (`StartLimitIntervalSec=60s`, `StartLimitBurst=3` per BKM-038).
- Reduces git pre-commit hook and vector retrieval latency from ~20s to **66ms**.
- All client scripts (`sync_chroma_dna.py`, `archive_node.py`, `refine_gem.py`) implement a graceful `try HttpClient(port=8001) except Exception: PersistentClient(...)` failover.

---

## [LAB-008] Headroom Token Optimization Proxy (Port 8787)
**Status:** ACTIVE
**Date:** July 2026

### Context
`headroom proxy --port 8787` was previously launched manually in the background, making it vulnerable to process termination or unmonitored memory drift.

### Decision
Established **`headroom-proxy.service`** as a systemd user daemon running on port 8787.

### Mechanism
- Configured with `MemoryHigh=500M`, `MemoryMax=1000M`, and circuit breaker caps (`StartLimitBurst=3` per BKM-038).
- Intercepts LLM tool outputs to compress context by 60–90% automatically.

---

## [LAB-009] Field Notes Nightly Subconscious Timer (2:00 AM)
**Status:** ACTIVE
**Date:** July 2026

### Context
The subconscious scanner (`field_notes/nibble.py`) required manual invocation or ad-hoc timers to process raw notes.

### Decision
Established **`field-notes-nibble.timer`** as a systemd user timer scheduled for `02:00:00` daily.

### Mechanism
- Triggers `field-notes-nibble.service` oneshot execution using `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/python`.
- Automates off-peak historical note indexing and summary synthesis.



