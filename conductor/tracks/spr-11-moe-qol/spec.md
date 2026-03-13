# Specification: MoE Synthesis Phase 4-5

## Overview
This track implements the Quality-of-Life (QoL) improvements and the Engine Enhancement logic defined in the extended [SPR-11-MoE] sprint.

## Requirements

### 📍 Quality-of-Life Hardening
- **[FEAT-172] Hemispheric Interjection**: Enable Pinky to fire WebSocket interjections ("Thinking...") while Brain processes.
- **[FEAT-171] Intelligent Socket Logic**: Implement mode-aware idle timers in `acme_lab.py` to prevent rebooting on disconnects.
- **[WYWO] Intent Gate**: Transition morning briefings to a prompt-triggered "Passive Mode."
- **Atomic Write Audit**: Enforce `.tmp` + `os.replace` for JSON reports in `recruiter.py` and `internal_debate.py`.

### 📍 Engine Enhancement (Forensic RAG)
- **[FEAT-175] BKM Sentinel**: Librarian logic to prioritize "Silicon Scars" (BKMs/RCA docs).
- **[FEAT-176] Deep-Connect Epoch**: Reverse RAG flow using Focal Wins as search seeds to harvest 50-100 word technical blocks.
- **[FEAT-177] DNA Uplink**: Route harvested data into `expertise/bkm_master_manifest.jsonl`.
- **[FEAT-181] Semantic Map Injection**: Plumb `semantic_map.json` into Brain's `deep_think` context.
- **[FEAT-179] Hallway Protocol (Agentic-R)**: Real-time "Deep Retrieval" triggered by failed Strategic Pivots.

## Success Criteria
- All features verified with automated tests.
- Zero 0-byte or corrupted JSONs after atomic write audit.
- BKM dataset density increased to at least 50 high-fidelity technical pairs.
- No linting regressions.
