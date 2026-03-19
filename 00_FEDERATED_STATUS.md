# Federated Lab Status: The "God View"
**Date:** March 6, 2026
**Scope:** Architecture, Bridges, and Public Infrastructure.

> [!IMPORTANT]
> **BOOTSTRAP PROTOCOL:** For environment orientation and cold-starts, always begin with **[BOOTSTRAP_v4.3.md](../BOOTSTRAP_v4.3.md)**.

## 🧭 Navigation
*   **🧠 The Brain (Backend):** [HomeLabAI/ProjectStatus.md](../HomeLabAI/ProjectStatus.md)
*   **📂 The Face (Frontend):** [GEMINI.md](./GEMINI.md)
*   **🗺️ The Map Room:** [00_MASTER_INDEX.md](./00_MASTER_INDEX.md)
*   **🧬 The DNA:** [FeatureTracker.md](./FeatureTracker.md)
*   **🎼 The Conductor:** [Registry](./conductor/tracks.md) | [Product](./conductor/product.md) | [Workflow](./conductor/workflow.md)

## 🏗️ Conductor: Active Tracks
| ID | Phase | Feature Focus | Status |
| :--- | :--- | :--- | :--- |
| **spr-15-0-relay** | 2. Implementation | Neural Relay & Token Waterfall | **ACTIVE** |
| **spr-13-0-stability** | 3. Foundation | Long-Tail Stability | **COMPLETED** |

## 🎯 Active Initiative: "The Neural Relay" (Sprint SPR-15.0)
**Goal:** Transition from a linear "Ping-Pong" state machine into a high-throughput **Relay Race** with parallel inference and token-aware yielding.

## ✅ Global Milestones (March 2026)
1.  **Neural Relay [SPR-15.0]**: ACTIVE. Parallelized local inference implemented. Waterfall pipe in logic phase.
2.  **Long-Tail Stability [SPR-13.0]**: COMPLETED. Resolving Windows 4090 latency misalignment and implementing Serial Capture (v12).
3.  **Strategic Induction [SPR-13.0]**: COMPLETED. Implemented the Decoupled Pipeline (Capture/Refine) and Bicameral Bridge refactor.
4.  **Silicon Stability [SPR-13.0]**: COMPLETED. Hardened the Resilience Ladder (Auto-Restart/Downshift), implemented the Split Status Model, and established the Forensic Ledger.

## 🔮 The Roadmap

### [ACTIVE] Phase 15: The Neural Relay (Sprint SPR-15.0)
*   [x] **Parallel Local Fan-out [FEAT-229.1]**: Spark Pinky and Shadow nodes simultaneously.
*   [x] **Incremental Triage [FEAT-233.1]**: Hub proceeds once intent is parsed from streaming Lab Node output.
*   [x] **Scalar Fuel Routing [FEAT-231]**: Multiplicative fuel function for emergent routing decisions.
*   [x] **Loopback Protection [FEAT-227]**: Atomic Anchor ([ME]) gate active.
*   [ ] **Live Hearing Pipe [FEAT-233.2]**: Implement word-by-word token streaming between nodes (In Progress).
*   [ ] **Calibration UI [FEAT-232]**: Add relay feedback buttons to the Intercom.

### [COMPLETE] Phase 13.1: Silicon Induction & The Living Ledger
*   [x] **Neural Shock [FEAT-201]**: Logic-based mental reset feedback loop for tool hallucinations.
*   [x] **Semantic Map (v2)**: Implemented 3-layer strategic hierarchy (Strategic, Analytical, Tactical).
*   [ ] **Curriculum Distillation**: Formatting BKMs into instruction-tuning pairs.
*   [ ] **LoRA Induction**: Fine-tuning the `lab_sentinel_v1` native expert.

### [COMPLETE] Phase 13.2: Silicon Stability & Forensic Clarity
*   [x] **Forensic Ledger [FEAT-151]**: Structured silicon logging with physical trace evidence.
*   [x] **Split Status Model [FEAT-045]**: Bifurcated health (API) from logical persona (status.json).
*   [x] **Resilience Ladder [FEAT-069]**: Autonomous Tiered Governance (Unified -> Large -> Emergency Stop).
*   [x] **Operational Modes**: Verified DEBUG_PINKY filtering and auto-shutdown for non-service modes.


### [COMPLETE] Phase 12: The Resonant Vibe (Sprint SPR-12.0)
*   [x] **Behavioral DNA [FEAT-181]**: Semanticexpert routing via ChromaDB.
*   [x] **Neural Resonance [FEAT-182]**: Inter-agent overhearing logic.
*   [x] **Safe-Scalpel [FEAT-198]**: Atomic, lint-gated code patching via MCP.
*   [x] **Judicial Feedback [FEAT-191]**: Peer-review integrated into dreaming.
2.  **vLLM 0.16.0 Breakthrough**: Successfully bypassed the "333MiB Wall" on Turing (2080 Ti) using `lo` loopback handshakes. vLLM is now the **Active Production Engine** for the Unified 3B Base.
3.  **Unified 3B Base Established**: Standardized on Llama 3.2 / Qwen 2.5 for 2080 Ti residency via the **Unity Pattern [FEAT-030]**.
4.  **Historical Pivot (Feb 2026)**: vLLM was briefly **TABLED** due to Ray/NCCL deadlocks; Ollama served as the bridge during characterization.
5.  **Sovereign Ultra (27B)**: Claude-distilled Qwen resident on KENDER (4090).
6.  **Resonant Chamber [FEAT-153]**: Implemented multi-agent coordination via "overhearing" strategic intent.
7.  **Forensics Archive Established**: Relocated "Silicon Scars" to `HomeLabAI/docs/forensics/` to preserve pedigree.

## 🔮 The Roadmap (The Restoration Hub)

### [ACTIVE] Phase 11: Signature Synthesis & Scaling (Sprint SPR-11-07)
*   [x] **Bilingual Attendant (V2)**: Integrated REST and MCP toolsets.
*   [x] **Sovereign Ultra (27B)**: Claude-distilled Qwen resident on KENDER (4090).
*   [x] **Resonant Chamber**: Multi-agent coordination via "overhearing" [FEAT-153].
*   [x] **Resident Handshake Gate**: Implemented initialization barrier for resident nodes [FEAT-165].
*   [ ] **Architect LoRA**: Distill BKM Protocol into a specialized `architect_v1` adapter.

*   **[COMPLETE] Phase 11.5: Poor Man's MoE (PMM)** (Sprint SPR-11-MoE)
    *   [x] **Pre-Gated Router**: Intent-based expert domain routing [FEAT-174.1].
    *   [x] **vLLM Multi-Adapter Bridge**: Dynamic hot-swapping via lora_request [FEAT-174.2].
    *   [x] **Expert Forge**: Archive distillation and Unsloth training infra [FORGE-01/02].
    *   [x] **Strategic Pivot**: Fidelity-aware backtracking and recursive retry [FEAT-173].

*   **[COMPLETE] Phase 11.4: Semantic Re-Mapping** (Sprint SPR-11-05)
    *   [x] **Strategic Anchoring**: Implemented [FEAT-128] extraction logic and verified on `2011.json`.
    *   [x] **Robust Extraction**: Implemented [FEAT-131] regex-based JSON parsing for chatty LLMs.
    *   [x] **Archaeological Logic**: Integrated role-based team anchors (DSD, MVE, PIAV) into the Librarian.
    *   [x] **Yearly Injection**: Implement [FEAT-127] for anchor-aware yearly aggregation.

*   **[COMPLETE] Phase 11.3: The Ghost Hunter** (Sprint SPR-11-04)
    *   [x] **Lab Fingerprint**: Implemented [FEAT-121] Boot Hash and Git-Commit tracing.
    *   [x] **Proc Title**: Implemented [FEAT-122] kernel-level process renaming.
    *   [x] **Process Group Cleanup**: Refactored Attendant to use `os.killpg()` for total tree termination.
    *   [x] **Socket-Aware Assassin**: Implemented [FEAT-119] to purge port 8765 before boot.
    *   [x] **Local Truth Sentry**: Implemented [FEAT-124] to prevent archive hallucinations.

*   **[COMPLETE] Phase 11.2: Authority of Synthesis** (Sprint SPR-11-03)
    *   [x] **Synthesis of Authority**: Implemented [FEAT-109] laconic synthesis prompts for the Brain.
    *   [x] **The Shadow Moat**: Implemented [FEAT-110] post-generation post-sanitization for persona isolation.
    *   [x] **Identity Lock**: Implemented [FEAT-111] hard constraints for local failover nodes.

*   **[ACTIVE] Continuous Burn**: Indefinite refinement of technical gems.
    *   [DONE] **Burn Progress Tracking**: Update `mass_scan.py` to report completion % to `status.json`.

*   **[ACTIVE] Semantic Sentinel**: Refine Sentinel logic into a true "Semantic Intent" gate using a tiny local model.
*   **[ACTIVE] Job Search Integration**: Connect the Recruiter node to external search APIs or local web-scrapes.

### [BACKLOG]
*   [BACKLOG] **Windows Voice Upgrade**: Research and test **Kani-TTS-2** (400M Param) on the Windows host for local voice cloning and low-latency speech generation.
*   [BACKLOG] **The Tracing Checklist**: Build a Meta-style mandatory checklist pass into the Brain's code-patching prompt to improve line-by-line verification accuracy.
*   [BACKLOG] **GPU Fractioning Research**: Investigate NVIDIA Run:ai or similar software partitioning to enforce strict VRAM quotas for concurrent resident nodes.
*   [BACKLOG] **Adversarial Internal Debate**: Experiment with an adversarial reviewer node (Byzantine Consensus) to force the Brain to defend technical logic more rigorously.
*   [BACKLOG] **Hemispheric Interjection**: [FEAT-172] Transform Pinky into an "Active Buffer" that provides pre-emptive clarifying questions while the Brain is thinking.
*   [BACKLOG] **Intelligent Socket Logic**: [FEAT-171] Implement mode-aware shutdown triggers. Debug modes use a 5-minute idle timer on disconnect; Service mode ignores disconnects.
*   [BACKLOG] **Airlock Redundancy Audit**: Check if `notes.jason-lab.dev/research.html` is redundant vs the static `www.jason-lab.dev` variant.
*   [BACKLOG] **Hot Swap LoRA Strategy**: Plan for building and swapping adapters (mice glasses) tailored to journals, code, and notes.
*   [BACKLOG] **WYWO Intent Gate**: Adjust "While You Were Out" to trigger only on user prompt ("What's up?") rather than connection.
*   [BACKLOG] **Integrated News Cycle**: Expand WYWO to include recruiter results, lab status, and service health briefings.
*   [BACKLOG] **Service Management via Pinky**: Research a safe execution flow for Pinky to monitor and potentially restart services (e.g., Jellyfin).
*   [BACKLOG] **vLLM 0.17.0 Optimization**: [FEAT-170] Lock in FlashInfer, Chunked Prefill, and Realtime WebSocket Pipelining.
*   [BACKLOG] **Recruiter "Deep Read"**: [FEAT-168] Implement Playwright scraping and Brain-driven semantic scoring for real-world job URLs.
*   [BACKLOG] **Status.html Navigation**: Port "Blue Tree" logic to Lab Status to enable log/report reading.
*   [BACKLOG] **Readability Overhaul**: Implement bold conclusions and bullets in Brain's system prompt.
*   [BACKLOG] **Atomic Write Audit**: Enforce .tmp write-and-rename pattern for all report generation.
*   [BACKLOG] **Subconscious Sanitization**: Review dreaming/debate prompts to remove personal professional anchors.
*   [BACKLOG] **Lazy-Load Protection**: Protect Hub stability by moving node-specific imports to local blocks.
*   [BACKLOG] **Liger-Standard Test**: Bench-test Viger-Kernels for Ollama VRAM efficiency.
*   [BACKLOG] **MAXS Utility Logic**: Implement "Value of Information" lookahead for Brain tasks.

*   **[COMPLETE] Phase 11.1: Resilient Responsiveness** (Sprint SPR-11-01)
    *   [x] **Tiered Brain Response**: [FEAT-086] WITTY preamble active.
    *   [x] **Intelligent Priming**: [FEAT-087] handshake priming verified.
    *   [x] **Recruiter Dashboard**: [FEAT-088] reporting active.
    *   [x] **Telemetry Watchdog**: Watching Docker health and reporting to Pager.

---

## 🏺 Chronological Archive (The Bedrock)
*Historical milestones for Phases 0 through 10.*

*   **[COMPLETE] Phase 10: Artifact Synthesis** (Feb 2026)
    *   [x] **Artifact Map**: Built `files.html` with unified "ALL" view.
    *   [x] **Cynical Ranking**: Implemented 0-4 showcase value scale.
    *   [x] **Nuclear Search**: Isolated navigation from DOM filtering.

### ✅ PHASE 0: INFRASTRUCTURE (Jan 2026)
- **Infrastructure Migration:** HomeLabAI_Dev moved from WSL -> Native Linux SSH.
- **Connectivity:** Tailscale MagicDNS active (z87-linux); passwordless SSH verified.
- **Access Layer:** Verified Cloudflare Tunnel hostnames (`code.jason-lab.dev`, `pager.jason-lab.dev`).

### ✅ PHASE 1-2: FIELD NOTES
- **Security:** Cloudflare Access configured (Admin/Lobby).
- **Static Synthesis:** Implemented `search_index.json` and `timeline.html`.
- **Access Layer:** Configured "Access Request" policy for guest entry.

### ✅ PHASE 3: OBSERVABILITY LAB
- **Scaffological Scaffolding:** Docker stack created (Prometheus, Grafana, NodeExporter).
- **Telemetry:** RAPL-Sim custom exporter reading system thermal/load data.
- **Access:** `monitor.jason-lab.dev` mapped and secured.

### ✅ PHASE 4-9: SYNTHESIS & ROBUSTNESS
- **Librarian/Nibbler:** Implemented dual-pipeline static synthesis.
- **Artifact Map:** Built `files.html` with Cynical Ranking (0-4).
- **Public Airlock (v3.1):** Deployed `www.jason-lab.dev`.


---

## 🛠️ Operational Protocols
### Website Build (Cache-Busting)
To force-clear browser caches after UI changes, run the automated build script:
`python3 field_notes/build_site.py`

### Diagnostic Instruments
Refer to **[HomeLabAI/docs/DIAGNOSTIC_SCRIPT_MAP.md](../HomeLabAI/docs/DIAGNOSTIC_SCRIPT_MAP.md)** for silicon verification and test suites.
