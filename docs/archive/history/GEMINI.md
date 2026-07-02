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

## 🚧 SPRINT 33: ALIGNMENT & IDENTITY (Active)
- [x] **Task 18.1 (Identity Grounding)**: Update `IDENTITY_BEDROCK` in `cognitive_hub.py` to clarify Acme Lab's resident relationship.
- [x] **Task 18.2 (Quip Refinement)**: Update priming persona to naive, arrogant, and hesitant deep thought quips.
- [x] **Task 18.3 (Pinky Un-gagging)**: Fix Pinky wordiness using synthesis mode over raw RAG log dumping.
- [x] **Task 18.4 (Triage De-duplication)**: Consolidate redundant triage broadcast in `cognitive_hub.py`.
- [x] **Task 18.5 (Nightly Task Audit)**: Verify Continuous Burn and log paths.
- [x] **Harden V5 Recovery**: Port `[FEAT-302]` (recovery backoff) and `[FEAT-323]` (backoff telemetry) to V5.

## 🎯 THE MISSION
To integrate the collection of technical notes and stories into a cohesive "Technical Dashboard." This is a full-spectrum integration—not a "best of" list. It reflects the rigor of a Validation Engineer.

## ⚖️ OPERATIONAL PROTOCOL (The "Cautious Design" Rule)
1. **Fact-Finding First:** The CLI must perform "discovery" on raw notes before suggesting a structure.
2. **Design Feedback Loop:** Reserve "heads-down" development for moments when specifically called out. Work with the user to gather requirements and build a detailed vision before moving forward. Some fact finding is allowed. Only dive into development once approved.
3. **Verification over Velocity:** Prioritize "Why" (the validation logic) over "What" (the finished text).
4.  **[FEAT-075] Content Immutability**: Technical narrative assets (e.g., `stories.html`) are **Write-Protected** at the paragraph level. Structural UI updates are permitted, but technical story content must remain 100% word-faithful to the original engineering pedigree. No LLM-driven "summarization."
5.  **[FEAT-205] Authority of Time**: If the Sovereign Brain (Windows 4090) is confirmed **RESIDENT** (`PRIMARY_LOCKED`), the Hub must yield to the long-tail latency (up to 180s). The Hub is forbidden from performing a "Panic Pivot" to local models based strictly on response time. 
6.  **[FEAT-198] Safe-Scalpel Protocol (Mandatory):**

    - **Primary Path (MCP):** Use the `archive` node's `safe_scalpel` MCP tool for all edits. This is the gold standard for high-fidelity, verified patching.
    - **Fallback (Standalone):** Only if the Lab is **OFFLINE**, use the `HomeLabAI/src/debug/atomic_patcher.py` script directly via the shell. Ensure `ruff` is present in the `.venv`.
    - **CRITICAL:** Do not confuse this protocol with standard `write_file` or generic `replace` calls. It is a strictly gated, lint-verified surgical tool and **never** requires the Lab to be active when using the standalone script.

## ❄️ COLD-START PROTOCOL (Environment Discovery)
If the agent session is lost or restarted, refer to these anchors:
1.  **The Current State**: `HomeLabAI/docs/protocols/BKM_SILICON_UPGRADE_GAUNTLET.md` (Verified 0.17 stack).
2.  **The PMM Blueprint**: `HomeLabAI/docs/plans/LORA_MOE_SYNTHESIS.md` (The "Poor Man's MoE" roadmap).
3.  **Silicon Identity**: Kernel `6.14.0-36-generic`, Driver `580.126.09`. Wi-Fi requires `linux-modules-extra`.
4.  **Watchdog Check**: The `vram_watchdog_loop` is active but requires verification of its "Auto-Restart" logic for defunct processes.
5.  **Project Secrets**: `Portfolio_Dev/monitor/secrets.json` (Contains PagerDuty and Cloudflare IDs).
6.  **Runtime Safe-Zone**: `~/AcmeLab` is the production host; `~/Dev_Lab` is the workspace.

## 🤖 CLI INITIALIZATION COMMAND
> "I am acting as a Lead Engineer's thought partner. We are wrapping up **Sprint 33 (Alignment & Identity)** by porting `[FEAT-302]` and `[FEAT-323]`, stabilizing Pinky's repetition penalty, and documenting feature integrity."

