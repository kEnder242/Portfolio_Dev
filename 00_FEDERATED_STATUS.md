# Federated Lab Status: The "God View"
**Date:** July 8, 2026
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
| **spr-39-0-moe-research** | 1. Planning | Federated Routing & "MoE+" Research | **ACTIVE** |
| **spr-38-0-alignment** | 2. Implementation | Swarm Shakedown & Temporal Calibration | **COMPLETED** |
| **spr-37-0-validation** | 2. Implementation | Bicameral Validation & RAG Diagnostics | **COMPLETED** |
| **spr-34-0-telemetry** | 2. Implementation | Semantic Retrieval & GPU Telemetry | **ACTIVE** |
| **spr-15-0-relay** | 2. Implementation | Neural Relay & Token Waterfall | **ACTIVE** |
| **spr-13-0-stability** | 3. Foundation | Long-Tail Stability | **COMPLETED** |

## 🎯 Active Initiative: "Federated Routing & "MoE+" Research" (Sprint SPR-39.0)
**Goal:** Design and benchmark a federated inference architecture (MoE+) utilizing lightweight routing, model specialization, and latency-hiding background workflows. **[STATUS: ACTIVE]**

## ✅ Global Milestones (July 2026)
1.  **Federated Routing & "MoE+" Research [SPR-39.0]**: **ACTIVE**. Sprint Plan drafted and double-written to workspace and brain cache, defining Stories for latency-hiding pre-gated pipelines, router accuracy evaluation, and stage-by-stage benchmark KPI tracking.
2.  **Swarm Shakedown & Temporal Calibration [SPR-38.0]**: **COMPLETE**. All 4 Stories completed. Story 1 (OpenAgent Shakedown and Model Concurrency Deadlock Fixes) done; Story 2 (RAG Adaptive Temporal Compass and /reset mitigation) done; Story 3 (Vibe Triage Meta rule) done; Story 4 (JSON Pretty-Printing in Intercom) done. protocols.md, AGY_TO_OPENAGENT_PLAYBOOK.md, and OPENAGENT_HANDOVER_PLAYBOOK.md updated with swarm category mappings, Ollama deadlock mitigations, and protocol pain points (lint-gating, DNA grounding, named sessions).
3.  **Bicameral Validation & RAG Diagnostics [SPR-37.0]**: **COMPLETE**. All 7 Stories done and committed. Story 7 (ChromaDB DNA Integration) finalized this session: `behavioral_dna` (29 BKMs) and `feature_dna` (214 FEATs) collections live, synced via pre-commit hook on every DNA file change. BKM-034 handover template updated to use ChromaDB query syntax instead of raw file injection. Sisyphus upgraded to `devstral:24b` (SWE-bench ~68%, ~19GB VRAM Q4) with omnicoder-9b as fallback. Cloudflare app renamed from 'Jason Lab - Sovereign' to 'Jason Lab - Strategic'; `panasonic.aero` added to Lobby Access policy.
2.  **Semantic & Telemetry [SPR-34.0]**: COMPLETE. Goal 1 (Hierarchical Semantic Map, MCompassRAG domain filtering/fallback, V5 dreaming, and client disconnect auto-shutdown) complete and verified. Phase 2 (Live Telemetry) and Phase 3 (Benchmarking Page) complete. Phase 4 (CORS Remediation, Tiered Idle Verification [FEAT-374], and Baseline Eval) complete. Phase 5 (Cognitive Taxonomy, Cache Alignment, positive peer-to-peer prompting, Foyer native logs viewer, and LoRA training restoration) complete.
3.  **Alignment & Identity [SPR-33.0]**: COMPLETE. Corrected Acme Lab grounding, refined Deep Thought naive/hesitant persona, un-gagged Pinky RAG summaries, consolidated triage broadcasts, and verified Continuous Burn logs. Ported V4 recovery backoff [FEAT-302] and telemetry [FEAT-323] to V5.
2.  **GPU Core Upgrade [SPR-32.0]**: COMPLETE. Stabilized vLLM 0.21.0 Turing stack, multi-LoRA concurrent resident nodes, and VRAM hibernation.

## ✅ Global Milestones (May 2026)
1.  **Governor's Gate [SPR-27.0]**: ACTIVE. Implementing resource coordination between background workers and the Lab Hub to prevent OOM events.
2.  **Mind Healing [SPR-26.0]**: COMPLETE. Restored Internal Waterfall Cascade [FEAT-233] and resolved high-fidelity triage deadlocks.

## ✅ Global Milestones (April 2026)
1.  **Mind Healing [SPR-20.0]**: COMPLETE. Implemented Neural Buffer [FEAT-283] for WAKING state queuing, type-agnostic triage parsing [ERR-06], and Heartbeat Deferral [FEAT-283.2] to prevent weight-swap collisions.
2.  **Stability Gauntlet [SPR-19.0]**: COMPLETED. Verified vLLM V0 stability on 2080 Ti and established PID Ledger for port reclamation.
3.  **Engine Stability [SPR-18.0]**: COMPLETED. Resolved Hibernation Wake-up traps and established Remote Lab Control auth discovery.
4.  **Neural Relay [SPR-15.0]**: COMPLETED. Parallelized local inference and scalar fuel routing verified.

## ✅ Global Milestones (March 2026)
1.  **Neural Relay [SPR-15.0]**: ACTIVE. Parallelized local inference implemented. Waterfall pipe in logic phase.
2.  **Long-Tail Stability [SPR-13.0]**: COMPLETED. Resolving Windows 4090 latency misalignment and implementing Serial Capture (v12).
3.  **Strategic Induction [SPR-13.0]**: COMPLETED. Implemented the Decoupled Pipeline (Capture/Refine) and Bicameral Bridge refactor.
4.  **Engine Stability [SPR-13.0]**: COMPLETED. Hardened the Resilience Ladder (Auto-Restart/Downshift), implemented the Split Status Model, and established the Forensic Ledger.

## 🔮 The Roadmap

### [ACTIVE] Phase 16: Federated Routing & "MoE+" Research (Sprint SPR-39.0)
*   [ ] **Latency-Hiding Pre-Gating [FEAT-MOE01]**: Overlap intent classification, RAG retrieval, and model warming to hide load times.
*   [ ] **Lightweight Router Calibration [FEAT-MOE02]**: Benchmark routing/escalation accuracy of 3B local models.
*   [ ] **Multi-Stage Workflow Benchmarking [FEAT-MOE03]**: Record and display metrics for each pipeline stage (TTFT, warm-up, tool call) on `benchmarks.html`.

### [ACTIVE] Phase 15: The Neural Relay (Sprint SPR-15.0)
*   [x] **Parallel Local Fan-out [FEAT-229.1]**: Spark Pinky and Shadow nodes simultaneously.
*   [x] **Incremental Triage [FEAT-233.1]**: Hub proceeds once intent is parsed from streaming Lab Node output.
*   [x] **Scalar Fuel Routing [FEAT-231]**: Multiplicative fuel function for emergent routing decisions.
*   [x] **Loopback Protection [FEAT-227]**: Atomic Anchor ([ME]) gate active.
*   [ ] **Live Hearing Pipe [FEAT-233.2]**: Implement word-by-word token streaming between nodes (In Progress).
*   [ ] **Calibration UI [FEAT-232]**: Add relay feedback buttons to the Intercom.

### [COMPLETE] Phase 13.1: Archive Ingestion & The Living Ledger
*   [x] **Neural Shock [FEAT-201]**: Logic-based mental reset feedback loop for tool hallucinations.
*   [x] **Semantic Map (v2)**: Implemented 3-layer strategic hierarchy (Strategic, Analytical, Tactical).
*   [ ] **Curriculum Distillation**: Formatting BKMs into instruction-tuning pairs.
*   [ ] **LoRA Induction**: Fine-tuning the `lab_sentinel_v1` native expert.

### [COMPLETE] Phase 13.2: Engine Stability & Forensic Clarity
*   [x] **Forensic Ledger [FEAT-151]**: Structured engine logging with physical trace evidence.
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
7.  **Forensics Archive Established**: Relocated "Technical Scars" to `HomeLabAI/docs/forensics/` to preserve pedigree.

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
Refer to **[HomeLabAI/docs/DIAGNOSTIC_SCRIPT_MAP.md](../HomeLabAI/docs/DIAGNOSTIC_SCRIPT_MAP.md)** for hardware verification and test suites.

### ✅ PHASE 15: THE NEURAL RELAY
- **Stabilization Sweep [SPR-32]**: (Complete) Modernized inference core to vLLM 0.21.0. Resolved Turing JIT linker fragmentation and dependency wars.
- **Multi-LoRA Baseline**: Re-certified Llama 3.2 3B AWQ with concurrent Voice, Brain, and History adapters.
- **Orchestration Memory**: Implemented Token-Aware Eviction and Sovereign Context Distillation.
- **VRAM Hibernation**: Verified 100% memory release during natural AFK drift.
- **Closed-Loop & Adaptive LoRAs [SPR-35]**: (Active) Integrated automated dataset distillation, vibe-grouping schema, and hemispheric sandbox tool isolation. Completed Task 1.5 (Fidelity & Telemetry Restoration) and Task 1.6 (Waterfall & Direct Routing Path Refactor) to resolve routing/handover deviations while preserving direct Brain routing exceptions, unifying interest terminology, and enabling peer-vote interest boosting.
