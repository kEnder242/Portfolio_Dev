# GEMINI.md: Project Manifesto & State Machine
**Host:** Z87-Linux (Native) | **User:** Jason Allred | **Tier:** Lead Engineer Portfolio
**Global Status:** [./00_FEDERATED_STATUS.md](./00_FEDERATED_STATUS.md)

> [!CAUTION]
> **NOT THE SOURCE OF TRUTH:** This document is an active agent state machine, NOT the navigational bedrock. Refer to **[BOOTSTRAP_v4.3.md](../BOOTSTRAP_v4.3.md)** for orientation and **[00_FEDERATED_STATUS.md](./00_FEDERATED_STATUS.md)** for milestones and historical provenance.

---

## 🏺 CHRONOLOGICAL ARCHIVE (Remembrance of the Past)
*Historical progress for Phases 0 through 10. These entries are preserved for contextual grounding.*

### ✅ PHASE 0: INFRASTRUCTURE (Jan 2026)
- **Infrastructure Migration:** HomeLabAI_Dev moved from WSL -> Native Linux SSH.
- **Connectivity:** Tailscale MagicDNS active (z87-linux); passwordless SSH verified.
- **Access Layer:** Verified Cloudflare Tunnel hostnames (`code.jason-lab.dev`, `pager.jason-lab.dev`).

### ✅ PHASE 1: CORE REPOSITORY (Jan 2026)
- **Directory Integrity:** Confirmed `~/Portfolio_Dev` structure.
- **Binary Access:** Confirmed `python3` and `git` permissions.
- **Environment Isolation:** Established clean venv for portfolio synthesis.

### ✅ PHASE 2: FIELD NOTES IMPLEMENTATION (Feb 2026)
- **Security:** Cloudflare Access configured for Admin (Vault) and NVIDIA (Lobby).
- **Refinement (v2.0):** Added Quick-Filter, Permalinks, and simulated Status Indicators.
- **Search Index (v2.1):** Implemented `search_index.json` for "silent tag" filtering.
- **Timeline (v2.2):** Created `timeline.html` visualizing 18 years of technical data.
- **Access Layer (v2.3):** Configured "Access Request" (The "Knock" button) for guest entry.

### ✅ PHASE 3: OBSERVABILITY LAB (Feb 2026)
- **Scaffolding:** Docker stack created (Prometheus, Grafana, NodeExporter).
- **Telemetry:** RAPL-Sim custom exporter reading system thermal/load data.
- **Access:** `monitor.jason-lab.dev` mapped and secured (Admin Only).

### ✅ PHASE 4-9: AI-STATIC HYBRID & SYNTHESIS (Feb 2026)
- **Librarian/Nibbler:** Implemented dual-pipeline static synthesis for notes.
- **Research Hub:** Created `research.html` mapping AI papers to implementations.
- **Workbench UI:** Web Intercom with physical Report Writer sidebar.
- **Subconscious Dreaming:** Multi-host memory consolidation pipeline (Linux -> Windows 4090).

### ✅ PHASE 10: ARTIFACT SYNTHESIS (Feb 2026)
- **Artifact Map:** Built `files.html` with unified "ALL" view and Drive integration.
- **Cynical Ranking:** Implemented 0-4 "Showcase Value" scale (Rank 4 = Diamond).
- **Nuclear Search:** Isolated Mission Control from DOM filtering bugs.
- **Public Airlock (v3.1):** Deployed `www.jason-lab.dev`.

---

## 🚧 PHASE 11: SIGNATURE SYNTHESIS & SCALING (Active)
- [x] **Surgical Restoration Sprint**: [SPR-11-09] (COMPLETED) achieved 100% technical parity for Hardware Grounding, Tool Resurrection, and Agentic-R.
- [x] **vLLM 0.17 Optimization**: [FEAT-170] (Active) Lock in FlashInfer, Chunked Prefill, and Realtime Pipelining.
- [x] **Poor Man's MoE (PMM)**: [SPR-11-MoE] (COMPLETED) Implemented dynamic expert routing and backtracking.

- [ ] **Recruiter Deep Read:** [FEAT-168] (TODO) Implementation of Playwright scraping and Brain-driven semantic matching.
- [x] **3x3 CVT Builder:** Implemented signature career impact synthesis tool.
- [ ] **TTT-Discover:** Implement RL-based autonomous validation path discovery.

## 🎯 THE MISSION
To integrate the collection of technical notes and stories into a cohesive "Technical Dashboard." This is a full-spectrum integration—not a "best of" list. It reflects the rigor of a Validation Engineer.

## ⚖️ OPERATIONAL PROTOCOL (The "Cautious Design" Rule)
1. **Fact-Finding First:** The CLI must perform "discovery" on raw notes before suggesting a structure.
2. **Design Feedback Loop:** Reserve "heads-down" development for moments when specifically called out. Work with the user to gather requirements and build a detailed vision before moving forward. Some fact finding is allowed. Only dive into development once approved.
3. **Verification over Velocity:** Prioritize "Why" (the validation logic) over "What" (the finished text).
4. **[FEAT-075] Content Immutability:** Technical narrative assets (e.g., `stories.html`) are **Write-Protected** at the paragraph level. Structural UI updates are permitted, but technical story content must remain 100% word-faithful to the original engineering pedigree. No LLM-driven "summarization."

## ❄️ COLD-START PROTOCOL (Environment Discovery)
If the agent session is lost or restarted, refer to these anchors:
1.  **The Current State**: `HomeLabAI/docs/protocols/BKM_SILICON_UPGRADE_GAUNTLET.md` (Verified 0.17 stack).
2.  **The PMM Blueprint**: `HomeLabAI/docs/plans/LORA_MOE_SYNTHESIS.md` (The "Poor Man's MoE" roadmap).
3.  **Silicon Identity**: Kernel `6.14.0-36-generic`, Driver `580.126.09`. Wi-Fi requires `linux-modules-extra`.
4.  **Inference Ghost**: `.venv_vllm_017` is the active environment, but `vllm_server.log` currently reports version `0.15.1`. Investigate this discrepancy before starting FEAT-174.
5.  **Project Secrets**: `Portfolio_Dev/monitor/secrets.json` (Contains PagerDuty and Cloudflare IDs).
6.  **Runtime Safe-Zone**: `~/AcmeLab` is the production host; `~/Dev_Lab` is the workspace.

## 🤖 CLI INITIALIZATION COMMAND
> "I am acting as a Lead Engineer's thought partner. We are starting **Sprint [SPR-11-MoE]**. My first task is to resolve the vLLM version discrepancy in the 0.17 environment and then implement the **[FEAT-174.1] Pre-Gated Router** logic in `acme_lab.py`."

