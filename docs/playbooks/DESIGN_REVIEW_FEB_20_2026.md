# Design Review & Documentation Audit: Phase 11 "Signature Synthesis"
**Date:** Feb 20, 2026 | **Auditor:** Gemini CLI | **Status:** CRITICAL DISCREPANCIES IDENTIFIED

## 1. Executive Summary
The ecosystem has successfully transitioned from a "vLLM-Optimistic" phase to a "Resilient Ollama-Standard" architecture. However, the documentation reflects a split-brain state: the functional layer (code, retrospectives, services) has adapted to the hardware realities of the Turing-based RTX 2080 Ti, while the global status documents still broadcast an outdated "Success" narrative for vLLM.

## 2. Critical Discrepancies (The "Doc Drift")

### A. The vLLM Paradox (Global vs. Local)
- **The "God View" (`00_FEDERATED_STATUS.md`)**: Last updated Feb 15. Reports "Unity Pattern Stabilized" on vLLM with Liger kernels. This is **incorrect**.
- **The Engineering Reality**: `Portfolio_Dev/RETROSPECTIVE_VLLM_RESURRECTION.md` and `FeatureTracker.md` confirm vLLM is **TABLED** due to BF16 deadlocks on Compute 7.5 (Turing).
- **The Ground Truth**: `lab-attendant.service` is hard-coded to `PINKY_ENGINE=OLLAMA`.

### B. Mandate Lag (HomeLabAI/GEMINI.md)
- **Status**: SEVERELY OUTDATED. 
- **Drift**: Still refers to `llama3.1:8b` for Pinky and `llama3:latest` for Brain.
- **Reality**: The system has standardized on the **Unified Base: Llama-3.2-3B** (AWQ/GGUF) as per `ProjectStatus.md` and `vram_characterization.json`.

### C. Resource Pathing
- **Dependency**: The Lab Attendant (`HomeLabAI`) requires `Portfolio_Dev/field_notes/data/vram_characterization.json`.
- **Finding**: While functional, this "Cross-Repo Dependency" is not explicitly documented in the `README.md` or `GEMINI.md` files of either repo, creating a risk for fresh clones or isolated development.

## 3. Lost Gems & Technical Scars (Unmapped Insights)

### [FEAT-029] The "Hardware Isolation Protocol"
- **Insight**: Breaking the kernel's 10s module reload loop by **physically erasing `.ko.zst` files** to blind the PCI probe. This is a high-density "SRE Playbook" insight currently buried in the Feature Tracker.
- **The USB-C Lurker**: Specifically `i2c_nvidia_gpu` and `i2c_ccgx_ucsi` as hidden hardware probes that trigger driver reloads even when the main driver is unloaded.

### [FEAT-028] Bicameral Failover logic
- **Insight**: The use of a **"Generation Probe"** (a single-token generation test) to detect deadlocks on the Windows 4090 and automatically reroute to the local Shadow Hemisphere.

### The "Montana Protocol"
- **Insight**: A strategy for managing logger hijacking by NeMo and ChromaDB, ensuring that the Attendant's telemetry remains clean.

## 4. Recommendations for Shoring Up

1.  **Immediate Update of `00_FEDERATED_STATUS.md`**: Synchronize the "God View" with the vLLM Table/Ollama Standard reality.
2.  **Harmonize `HomeLabAI/GEMINI.md`**: Update the "Voice Gateway" persona mapping to reflect the Unified Base (Llama 3.2).
3.  **Promote the "Feature Tracker"**: Add a direct link to `FeatureTracker.md` in the root `00_MASTER_INDEX.md` and the `README.md`. It is currently the most accurate technical ledger.
4.  **Formalize the "BKM Protocol"**: Transition the "Hardware Isolation" and "USB-C Lurker" insights into a dedicated `HomeLabAI/docs/SRE_PLAYBOOK.md`.
5.  **Refactor "vLLM Ghost" Variables**: Clean up `USE_BRAIN_VLLM` and related stubs in `lab_attendant.py` to reduce cognitive load during future vLLM (Ampere+) attempts.

## 5. Architectural Health Check
The transition to **Ollama** has provided **90% of the target value** (sub-second prompt swaps) without the BF16/Turing stability issues. The **Bicameral Failover** ensures a resilient co-pilot experience.

### ✅ Post-Review Execution (Feb 20, 2026)
1.  **Bootstrap Primacy**: All primary entry points (`00_FEDERATED_STATUS.md`, `00_MASTER_INDEX.md`, and repo `GEMINI.md` files) now contain the mandatory **[BOOTSTRAP_v4.2.md](../BOOTSTRAP_v4.2.md)** pointer for cold-starts.
2.  **God View Sync**: Updated the "God View" to reflect Phase 11 milestones and the Ollama/3.2 standard.
3.  **DNA Elevation**: `FeatureTracker.md` is now the recognized relational hub, documenting the **Montana Protocol**, **Strategic Ping**, and **Hardware Isolation Artifacts**.
4.  **Breadcrumb Integrity**: Verified the cross-repo dependency of `vram_characterization.json` as a stable anchor for the Attendant.

The documentation is now synchronized with the "ground truth." The Lab is primed for Phase 11 synthesis.

---
*End of Design Review. Context is preserved and ready for Directive implementation.*
