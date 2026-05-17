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
