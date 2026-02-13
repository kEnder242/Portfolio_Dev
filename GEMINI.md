# GEMINI.md: Project Manifesto & State Machine
**Host:** Z87-Linux (Native) | **User:** Jason Allred | **Tier:** Lead Engineer Portfolio
**Global Status:** [./00_FEDERATED_STATUS.md](./00_FEDERATED_STATUS.md)

> [!IMPORTANT]
> **THE TRUTH ANCHOR:** For the "God View" of project milestones, always defer to [00_FEDERATED_STATUS.md](./00_FEDERATED_STATUS.md).

## ✅ PHASE 0: ACCOMPLISHED (Gemini.google.com & Manual)
- [x] **Infrastructure Migration:** HomeLabAI_Dev moved from WSL -> Native Linux SSH (Success).
- [x] **Connectivity:** Tailscale MagicDNS active (z87-linux); passwordless SSH verified.
- [x] **Environment:** VS Code Desktop (Remote-SSH) + Zellij + Native Terminal active.
- [x] **Access Layer:** Verified Cloudflare Tunnel hostnames (`code.jason-lab.dev`, `pager.jason-lab.dev`).
- [x] **Strategy:** Initial brainstorming on "War Story" logic and technical dashboard intent.

## ✅ PHASE 1: ACCOMPLISHED (CLI Verification)
- [x] **Directory Integrity:** Confirmed `~/Portfolio_Dev` and subdirectories.
- [x] **Binary Access:** Confirmed `python3` and `git` access.
- [x] **Environment Isolation:** Confirmed operation within `Portfolio_Dev`.

## 📚 REFERENCE MATERIAL
- **Travel Guide:** `Travel_Guide_2026.md` (Local only, Git-ignored). Contains "Pinky" logic, infrastructure context, and credentials.
- **Pinky Location:** `~/HomeLabAI_Dev` (Dev) and `~/AcmeLab` (Runtime).
- **Google Workspace:** I have native access to Drive/Docs via the `google-workspace` extension.

## 🚧 PHASE 2: FIELD NOTES IMPLEMENTATION (Complete)
...
- [x] **Security:** Cloudflare Access configured for Admin (Vault) and NVIDIA (Lobby).
- [x] **Refinement (v2.0):** Added Quick-Filter, Permalinks, Print Mode (@media print), and simulated Status Indicators.
- [x] **Search Index (v2.1):** Implemented `search_index.json` for "silent tag" filtering.
- [x] **Timeline (v2.2):** Created `timeline.html` visualizing 18 years of "Pinky-scanned" data (Strategy vs. Tactics).
- [x] **Access Layer (v2.3):** Configured "Access Request" policy (The "Knock" button) for guest entry.

## ✅ PHASE 3: OBSERVABILITY LAB (Complete)
- [x] **Scaffolding:** Docker stack created (Prometheus, Grafana, NodeExporter).
- [x] **Telemetry:** RAPL-Sim custom exporter reading real system thermal/load data.
- [x] **Access:** `monitor.jason-lab.dev` mapped and secured (Admin Only).
- [x] **Visualization:** Grafana is live and measuring "Neural Uplink" load.

## ✅ PHASE 4-9: AI-STATIC HYBRID (Complete)
...
- [x] **Integration:** Defined the "Plays Nice" contract for HomeLabAI migration.

## ✅ PHASE 10: ARTIFACT SYNTHESIS & SCANNER ROBUSTNESS (Complete)
- [x] **Artifact Map:** Built `files.html` with a unified "ALL" view and Drive folder integration.
- [x] **Cynical Ranking:** Implemented 0-4 "Showcase Value" scale (Rank 4 = Star Power).
- [x] **Nuclear Search Fix:** Isolated Mission Control from search filtering.
- [x] **Robustness:** Implemented atomic writes and absolute path utility hardening.
- [x] **Public Airlock (v3.1):** Deployed `www.jason-lab.dev`.

## 🚧 PHASE 11: SIGNATURE SYNTHESIS & SCALING (Active)
- [x] **3x3 CVT Builder:** Implemented signature career impact synthesis tool.
- [x] **Internal Debate:** Deployed moderated consensus logic for high-stakes technical tasks.
- [x] **Diamond Dreams:** Multi-host memory consolidation pipeline active (Linux -> Windows 4090).
- [x] **MAXS Lookahead:** v1.0 active for instant wisdom retrieval.
- [x] **Expertise Hierarchy:** Created hierarchical BKM registry and Technical Architect persona.
- [x] **Report Writer Sidebar:** UI Shell integrated into Intercom v3.1.
- [ ] **vLLM Integration:** Transition from Ollama to vLLM (TABLED).
- [ ] **TTT-Discover:** Implement RL-based autonomous validation path discovery.

## 🎯 THE MISSION
To integrate the collection of technical notes and stories into a cohesive "Technical Dashboard." This is a full-spectrum integration—not a "best of" list. It reflects the rigor of a Validation Engineer.

## ⚖️ OPERATIONAL PROTOCOL (The "Cautious Design" Rule)
1. **Fact-Finding First:** The CLI must perform "discovery" on raw notes before suggesting a structure.
2. **Design Feedback Loop:** Reserve "heads-down" development for moments when specifically called out. Work with the user to gather requirements and build a detailed vision before moving forward. Some fact finding is allowed. Only dive into development once approved.
3. **Verification over Velocity:** Prioritize "Why" (the validation logic) over "What" (the finished text).

## ❄️ COLD-START PROTOCOL (Environment Discovery)
If the agent session is lost or restarted, refer to these anchors:
1. **The Soul of the Lab:** `Portfolio_Dev/docs/BICAMERAL_DISPATCH.md`.
2. **Infrastructure Secrets:** `~/.secrets/` (Contains `cloudflare_token` and other non-git keys).
2. **Project Secrets:** `Portfolio_Dev/monitor/secrets.json` (Contains PagerDuty and Cloudflare IDs).
3. **Maintenance Mode:** `Portfolio_Dev/field_notes/data/maintenance.lock`. If this file exists, external alerts (NTFY/PD) are suppressed. Remove this file to resume live alerting.
4. **Runtime Safe-Zone:** `~/AcmeLab` is the production host for background services.
4. **Dev Safe-Zone:** `~/Dev_Lab` is the primary workspace.
5. **Context Anchors:** `Travel_Guide_2026.md` contains the authoritative network topology.

## Personal notes from Jason:

1. **War Story notes** Here is a link to my document dealing wiht my work history.  I want to fill a dashboard with all the content in this doucment - I'd like to brainstorm ways to index and display this content as an interview dashboard

Link: https://docs.google.com/document/d/12Hu34Vv9y4e5mSfj98glCJ-1CJUVOYxKtWkxWMKyYk8/edit?usp=drive_link

2. **Travel Guide notes** - This is context for the environment we are working on, some of the info is old but it details the transition from HomeLabAI development in WSL to a Remote-to-Linux dev environment (here).  I'd like to leverage the website setup described here and implemented on this host.  A landing page pointing to home lab pages might be nice.  I'd like to brainstorm security options, maybe a guest login, and preserve existing work as well as possible./

Link: https://drive.google.com/file/d/1E7RYWn-WIkMkV6UmWML8_ZLzQRmuzlJY/view?usp=drive_link

3. **Strech goals** I want to learn promethius, graphana, and influxdb.  Please leave some room for these on a landing page and in our plans.  Integration to HomeLabAI_Dev might be useful - let's brainstorm as well.

## 🤖 CLI INITIALIZATION COMMAND
> "I am acting as a Lead Engineer's thought partner. My first task is to index all existing raw notes in  and propose a dashboard layout that highlights validation logic across the entire set."