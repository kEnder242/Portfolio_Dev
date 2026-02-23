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
- [x] **3x3 CVT Builder:** Implemented signature career impact synthesis tool.
- [x] **Internal Debate:** Deployed moderated consensus logic for high-stakes technical tasks.
- [x] **Diamond Dreams:** Multi-host memory consolidation pipeline active (Linux -> Windows 4090).
- [x] **MAXS Lookahead:** v1.0 active for instant wisdom retrieval.
- [x] **Expertise Hierarchy:** Created hierarchical BKM registry and Technical Architect persona.
- [x] **Bicameral Failover:** Implemented **Strategic Ping** (Generation Probe) for automatic Brain-to-Shadow failover.
- [x] **vLLM Assessment:** Officially **TABLED** for Turing (2080 Ti). Standardized on Ollama Unity Pattern.
- [ ] **Feature Tracker Deep Mapping:** (Next) Forensic review of Git/CLI history to map Scars to DNA.
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
1. **The Current State**: `HomeLabAI/docs/STABILIZATION_REPORT_FEB_13.md` (Crucial vLLM vs VRAM findings).
2. **The Safe Scalpel**: `HomeLabAI/src/debug/atomic_patcher.py`. Use for ALL code edits to ensure lint-verification.
3. **Infrastructure Secrets**: `~/.secrets/` (Contains `cloudflare_token` and other non-git keys).
4. **Project Secrets**: `Portfolio_Dev/monitor/secrets.json` (Contains PagerDuty and Cloudflare IDs).
5. **Maintenance Mode**: `Portfolio_Dev/field_notes/data/maintenance.lock`. If this file exists, external alerts (NTFY/PD) are suppressed. Remove this file to resume live alerting.
6. **Runtime Safe-Zone**: `~/AcmeLab` is the production host for background services.
7. **Dev Safe-Zone**: `~/Dev_Lab` is the primary workspace.
8. **Mandatory Start**: Run `HomeLabAI/src/debug/stability_marathon_v2.py` to verify the Mind before concluding any task.

## Personal notes from Jason:

1. **War Story notes** Here is a link to my document dealing wiht my work history.  I want to fill a dashboard with all the content in this doucment - I'd like to brainstorm ways to index and display this content as an interview dashboard

Link: https://docs.google.com/document/d/12Hu34Vv9y4e5mSfj98glCJ-1CJUVOYxKtWkxWMKyYk8/edit?usp=drive_link

2. **Travel Guide notes** - This is context for the environment we are working on, some of the info is old but it details the transition from HomeLabAI development in WSL to a Remote-to-Linux dev environment (here).  I'd like to leverage the website setup described here and implemented on this host.  A landing page pointing to home lab pages might be nice.  I'd like to brainstorm security options, maybe a guest login, and preserve existing work as well as possible./

Link: https://drive.google.com/file/d/1E7RYWn-WIkMkV6UmWML8_ZLzQRmuzlJY/view?usp=drive_link

3. **Strech goals** I want to learn promethius, graphana, and influxdb.  Please leave some room for these on a landing page and in our plans.  Integration to HomeLabAI_Dev might be useful - let's brainstorm as well.

## 🤖 CLI INITIALIZATION COMMAND
> "I am acting as a Lead Engineer's thought partner. My first task is to index all existing raw notes in  and propose a dashboard layout that highlights validation logic across the entire set."
