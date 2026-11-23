# Sprint 115: IP Mothball & Personal IP Protection Plan

**Status:** ACTIVE (Heads-Up Planning & Iterative Execution)  
**Target Cutoff Date:** `2026-11-22` (Signing Date: `2026-11-23`)  
**Owner:** Jason Allred  
**Format:** Narrative Sprint Document (BKM-081 Unified Plan & Running Log)

---

## 1. Mission & Legal Context
Prepare the Federated Lab ecosystem (`Dev_Lab`, `HomeLabAI`, `Portfolio_Dev`, and `www_deploy`) for upcoming employment in an overlapping technical domain (AI agents, RAG, distributed inference, developer tooling). The operator resides in **Oregon** and the prospective employer may be based in **California** (Cal. Lab. Code § 2870 / PIIA Exhibit A context).

The core objective is **creative control and clear prior-invention provenance**:
- Establish **Apache License 2.0** across the 4 core repositories with explicit attribution to **Jason Allred** (`LICENSE`, `NOTICE`, SPDX headers, and README IP notices dated `2026-11-22`).
- Produce a **private, 1-page Tiered Exhibit A** (`PRIOR_INVENTIONS_EXHIBIT_A.md` in `Dev_Lab`, backed up to Google Docs / PDF) so pre-existing architectures cannot be absorbed as work-made-for-hire, while leaving a clean path for the author to license his own IP separately if ever desired.
- Evolve `timeline.html` into a clean, static, `2026-11-22`-bounded visual record of innovation provenance ("Exhibit A in itself").
- Establish an off-GitHub backup mirror (**Bitbucket**, per `[LAB-108]`) and a reversible **`close_shop.sh`** script to mothball GitHub credentials when ready.

---

## 2. Agreed Architectural & Operational Decisions

### 2.1 Licensing, READMEs & Header Injection Script (Track 1 & 2.1)
- **License:** **Apache License 2.0** (`SPDX-License-Identifier: Apache-2.0`) with root `LICENSE` and `NOTICE` files in all 4 repositories (`Dev_Lab`, `HomeLabAI`, `Portfolio_Dev`, `www_deploy`).
- **READMEs:** All 4 repositories carry a standardized **License, Authorship & Intellectual Property Notice** citing `Copyright 2025–2026 Jason Allred`, the `2026-11-22` IP snapshot date, and the `v2026.11.22-ip-snapshot` tag. *(Completed in Sprint Log below.)*
- **Header Injection Script Design (`scripts/apply_license_headers.py` — Planned):**
  - **Scope:** Targets git-tracked source files (`git ls-files`) across the 4 repos matching `.py`, `.js`, `.sh`, `.css`, `.html`.
  - **Exclusions:** Third-party/vendor assets, generated minified bundles, `.json`, `.md`, and files already containing `SPDX-License-Identifier`.
  - **Idempotency & Safety Rules:**
    1. Preserves line 1 shebangs (`#!/usr/bin/env ...`, `#!/bin/bash`) and Python encoding cookies (`# -*- coding: ...`) by inserting the 3-line header immediately after them.
    2. Uses language-appropriate comment syntax (`#` for `.py`/`.sh`, `//` for `.js`, `/* */` for `.css`, `<!-- -->` for `.html`).
    3. Header format:
       ```text
       Copyright 2025-2026 Jason Allred
       SPDX-License-Identifier: Apache-2.0
       ```
    4. Supports `--dry-run` (default), `--apply`, and `--verify`.
  - **Testing Plan:**
    1. Unit tests on synthetic fixtures (file with shebang, file without shebang, HTML `<!DOCTYPE html>`, already-headed file verifying zero diff on second run).
    2. `--dry-run` audit across all 4 repos to confirm file counts and zero unintended mutations.
    3. Post-apply syntax verification (`python3 -m py_compile` on all touched `.py` files, `bash -n` on `.sh` files, `git diff --stat` review).

### 2.2 Ancillary Repositories & Disk Hygiene (Track 2.2)
- **`M5-Local-oMLX`** and **`decky-trailers`**: 1-line summary entries in Exhibit A (no heavy sprint work; `M5-Local-oMLX` is mostly deployment notes + small shell/API configs; `decky-trailers` is a standalone Steam Deck plugin).
- **`openbmc-lab`**: Safe to delete from disk and ignore.
- **`DeepAgent`**: Upstream fork; safe to delete from disk and GitHub.
- **`jason_leetcode`**, **`binary_2-27`**, **`Navidrome-Server`**, Jellyfin configs: Toy/media repos; no TLC required.

### 2.3 Exhibit A Strategy & Tiered Prior Inventions Document (Track 3.1)
- **Storage:** Private file in `Dev_Lab/PRIOR_INVENTIONS_EXHIBIT_A.md` (private repo), converted to clean PDF / backed up in Google Docs for HR/Legal submission.
- **Tiered Structure (Standard Practice):**
  - **Tier 1 (≤ 250-char Workday/Portal Field):** Crisp pointer referencing the attached 1-page Exhibit A PDF, date cutoff (`2026-11-22`), and freeze tag (`v2026.11.22-ip-snapshot`).
  - **Tier 2 (1-Page Exhibit A PDF):** 4–5 broad functional architectural umbrellas (covering code, protocols, workflows, and concepts without disclosing employer-sensitive secrets) + compact table of repositories, date range (`2025–2026-11-22`), and commit SHAs.
  - **Tier 3 (Immutable Backing Evidence — Retained by Author):** Annotated git tags, git history, `timeline.html`, `papers.html`, and `NOTICE`/`LICENSE` files.

### 2.4 DNA Taxonomy, `DISC-xxx` Backfill & `wisdom.html` Deprecation (Track 3.2, 3.4, 3.5)
- **Taxonomy Clarification (`BKM-060`):** `INS-xxx` = philosophical first principles (`inspiration_data.json`); `DISC-xxx` = concrete novel inventions/discoveries (`timeline_data.json`).
- **`wisdom.html` Careful Deprecation Plan:** `wisdom.html` is a redundant mirror of `dna_forge.html`. Before removing it, audit all navigation links (`mission-control.js`, `index.html`, `build_site.py`, `www_deploy/`) and replace or redirect references cleanly so zero 404s are introduced.
- **New `DISC-xxx` Inventions to Backfill into `timeline_data.json` & Exhibit A:**
  1. Waterfall & Waterfall Streaming / Multi-LoRA Feedback Streaming
  2. Living Cognitive DNA & Morphology Architecture (`clara-dna` MCP + ChromaDB)
  3. Ambient Hooks & Sub-600ms Grounding Transparency
  4. Heterogeneous Cross-Vendor GPU Pooling (`llama.cpp` CUDA + Vulkan/ReBAR + Apple Silicon oMLX)
  5. Automated Benchmark Gauntlet & Nightly Accountability Watchdog (`uber_5x5`)
  6. Tracked Conversational Lanes & Dropped Threads Ledger (`BKM-064` / `BKM-077` / `BKM-084`)
  7. Heads-Up / Heads-Down (AFK) Swarm Governance & Sprint Methodology (`BKM-006` / `BKM-086`)
  8. Dynamic Multi-View Paper Projection & Consistency Drift Engine (`FEAT-616` / `papers.html`)

### 2.5 Evolutionary Timeline (`timeline.html`) & Public Airlock Readiness (Track 3.3.1 & 3.3.2)
- **Root Cause Identified:** `timeline_build.py` hardcoded `maxTime = '2026-04-15'`, clamping every Sep–Nov 2026 discovery (`DISC-011`..`DISC-020`) onto the right edge (`ratio = 1.0`), creating the tail-heavy pileup.
- **Visual Direction:** Bound axis cleanly to `2025-10-15` → `2026-11-22` (with dashed gold `11/22 Freeze` cutoff line). Render each discovery as a **horizontal evolution line** (same lane color) with **vertical revision ticks** at conception, first build, and major revisions, stacked cleanly in dynamic sub-rows so lines never collide.
- **Airlock / Public Presentation:** `timeline.html` inlines all `DISCOVERIES` and `OUTLIERS` JSON at build time (zero backend API calls). Candidate for direct public exposure (`public_timeline.html` or un-gated `timeline.html` on `kEnder242.github.io`) once `DISC-xxx` backfill and revision dates are complete.

### 2.6 Git Freeze, Credential Mothballing, Bitbucket Mirror & Static Site (Track 4 & 5)
- **Git Freeze Tag:** Annotated tag `v2026.11.22-ip-snapshot` across all 4 repos after licenses, headers, and timeline updates land.
- **Credential Mothballing:** Reversible `close_shop.sh` script (logs out `gh`, clears GitHub credentials from `git-credential-manager`, sets push URL to `no_push`) — executed only when operator is ready.
- **Bitbucket Backup (`[LAB-108]`):** API token stored securely outside git at `~/.secrets/bitbucket_token` (`chmod 600`). Requires Bitbucket repository/workspace scopes before wiring dual-push remotes.
- **Static Site (`www_deploy` / `kEnder242.github.io`):** Migration off `github.io` tabled (Cloudflare already in place). Focus strictly on Apache 2.0 copyright/attribution footer injection and static `timeline.html` sync.

---

## 🧭 Roll-Up Audit & Authoritative ANCHOR_TRACK (BKM-097)

*Conducted `2026-11-22` via adversarial line-by-line reconciliation of the tracked Sprint 115 conversation against this unified sprint document (`BKM-081` / `BKM-020` / `BKM-097`). Existing narrative sections above are preserved verbatim (Absolute Append).*

### Gaps & Drift Surfaced During Audit (Now Reconciled)
1. **Track `3` (Clickable Git History & Broken Sprint Links)** was previously logged only in Sprint Log bullet #5; promoted here into full specification:
   - *Why*: `timeline_build.py` line 1146 hardcoded `docs/sprints/archive/${item.sprint_ref}`, breaking **11 of 17** sprint links (`DISC-007`..`010` are in `active/`, and `DISC-011`..`020` use short labels like `SPR-108.0`).
   - *How*: Resolve `sprint_ref` in Python at build time against `docs/sprints/active/` and `docs/sprints/archive/`; make Code Anchor pills clickable to GitHub `blob/main/<path>` plus a compact `⏱` history link (`commits/main/<path>`); add a single 1-line `Git:` meta-row (`First: <sha> • Latest: <sha>`) to `discovery-card` only (leaving common `dna_forge.html` cards untouched).
   - *Proof*: Rebuild `timeline.html` and assert 0 unresolved sprint URLs and 0 live backend `fetch`/`WebSocket` calls.
2. **Track `2.2` (Disk & Repo Cleanup Actions)** explicitly separated from Exhibit A 1-liners: `openbmc-lab` (local delete) and `DeepAgent` (local delete + user-owned GitHub deletion) + local untracked `Dev_Lab/unsloth_compiled_cache/` cleanup.
3. **Track `4.3` (GitLab Audit)** and **Tracks `C` / `D`** formally closed out in `ANCHOR_TRACK` below so zero conversational threads remain unanchored.
4. **Track `5.1` (Bitbucket Workspace Slug)** explicitly flagged as the sole open input needed to wire `[LAB-108]` private mirror remotes.

### Authoritative `ANCHOR_TRACK` Reconciliation Table

| Lane | Origin Prompt / Topic | Agreed Technical Architecture & Forensic Scope | Mapped Section | Status |
| :--- | :--- | :--- | :--- | :--- |
| **1 / 1.1** | License choice & OR/CA IP control | **Apache License 2.0** (`LICENSE` + `NOTICE` preserving "Jason Allred" attribution + patent grant/retaliation); OR residence + CA § 2870 context; Exhibit A protects ownership while keeping author's separate licensing path open. | §2.1 | `DONE` |
| **2.1** | Code headers, `11/22/2026` date & 4 READMEs | All 4 repos (`Dev_Lab`, `HomeLabAI`, `Portfolio_Dev`, `www_deploy`) updated with `README.md` IP notice, `LICENSE` + `NOTICE`, and idempotent `scripts/apply_license_headers.py` (`--self-test` + `--apply` across 739 files + `py_compile`/`bash -n` verified). | §2.1 | `DONE` |
| **2.2** | Ancillary repos & local disk hygiene | `M5-Local-oMLX` & `decky-trailers` = 1-liners in Exhibit A; `openbmc-lab` & `Dev_Lab/unsloth_compiled_cache` deleted locally; `DeepAgent` GitHub fork left for user UI delete; toy/media repos no TLC. | §2.2 | `DONE` *(local)* |
| **3** | Clickable git history, code anchors & sprint links | Graph → `discovery-card` (isolated from `dna_forge.html`) → clickable Code Anchors (`blob` + `⏱` `commits` link) + compact 1-line `Git: First / Latest` row; build-time fix for 11/17 broken sprint links (`unresolved_sprints=0`). | §2.5 & Roll-Up | `DONE` |
| **3.1** | Private Exhibit A document | Private `Dev_Lab/PRIOR_INVENTIONS_EXHIBIT_A.md` (Tier 1: 215-char Workday field; Tier 2: 1-page PDF / Google Docs backup with 5 architectural pillars + repo/SHA table + attestation; Tier 3: git tags/history/timeline/papers). | §2.3 | `DONE` |
| **3.2** | `INS` vs `DISC` taxonomy & `wisdom.html` | `BKM-060`: items 1–7 registered in `DISC-xxx` (`timeline_data.json`); redundant `wisdom.html` removed from `Portfolio_Dev`, `www_deploy`, and `build_site.py` (0 broken nav links). | §2.4 | `DONE` |
| **3.3.1** | Evolutionary Timeline visual & backfill | Fixed `maxTime = '2026-04-15'` tail-clamping bug → `2025-10-15..2026-11-22` with `11/22 Freeze` line, horizontal evolution lines & vertical revision ticks; 25 discoveries enriched with real git provenance. | §2.5 | `DONE` |
| **3.3.2** | Move `timeline.html` outside airlock | Verified `timeline.html` is 100% static (0 live calls); promoted to `PUBLIC_AIRLOCK_HTML` in `build_site.py` and deployed to `www_deploy/timeline.html`. | §2.5 | `DONE` |
| **3.4** | `papers.html` (JITC & Dynamic Projections) | Dynamic Multi-View Paper Projection & Consistency Drift Engine (`[FEAT-616]`, `papers.html`, `paper_jitc_intuition.json`) registered as `DISC-028` and included in Exhibit A. | §2.4 | `DONE` |
| **3.5** | Tracked Conversations | Tracked Conversational Lanes & Dropped Threads Ledger (`BKM-064` / `BKM-077` / `BKM-084`) registered as `DISC-026` and included in Exhibit A. | §2.4 | `DONE` |
| **4.1** | Git freeze tag | Annotated tag `v2026.11.22-ip-snapshot` applied locally across all 4 repos (`HomeLabAI`, `Portfolio_Dev`, `www_deploy`, `Dev_Lab`); push left to operator (Law 0). | §2.6 | `DONE` *(local tags)* |
| **4.2** | Credential mothball script | Reversible `Dev_Lab/scripts/close_shop.sh` built and `--dry-run` verified; awaiting operator execution after final pushes. | §2.6 | `DONE` *(script ready)* |
| **4.3** | GitLab vs GitHub check | Verified zero GitLab remotes, configs, or SSH keys locally; only 4 legacy links already cleaned in Sprint 64. | Sprint Log | `DONE` |
| **5.1** | Bitbucket backup mirror (`[LAB-108]`) | Scoped API token stored outside git at `~/.secrets/bitbucket_token` (`chmod 600`) and verified live as `kender242` (`Jason Allred`). **Open blocker:** needs Bitbucket workspace slug to wire private mirror remotes. | §2.6 | `BLOCKED ON WORKSPACE SLUG` |
| **5.2 / 5.3** | Static site (`kEnder242.github.io`) | Migration off `github.io` & sync script rewrites **TABLED** (Cloudflare already in place). Injected Apache 2.0 copyright/attribution footers onto 8 public pages + synced `timeline.html`. | §2.6 | `DONE` *(Migration DEFERRED)* |
| **C** | Strata Sprint 114 / DNA docs | Explicitly dismissed by operator ("dropped long ago when we dropped the engine experiment"). | — | `DROPPED` |
| **D** | Confirm `Portfolio_Dev` push & delete backup | Confirmed `origin/main` = `9d70132` (filtered `HEAD`); deleted `/home/jallred/Portfolio_Dev_pre_filter_git_backup`. | Sprint Log | `DONE` |

---

## 📜 Sprint Log

### 2026-11-22 — Session 1 (Planning, Verification & Timeline Iteration 1)
1. **Verified `Portfolio_Dev` Force-Push & Cleaned Backup (Track D):**
   - Confirmed `Portfolio_Dev` local `HEAD` (`9d7013204d0485d8eb8958a2349914fa2e3dd1c7`) matches `origin/main` on GitHub (`git ls-remote`).
   - Deleted pre-filter `.git` backup `/home/jallred/Portfolio_Dev_pre_filter_git_backup` per operator authorization.
2. **Stored Bitbucket Token & Tested Access (Track 5.1):**
   - Stored token outside git at `~/.secrets/bitbucket_token` (`chmod 600`, alongside `cloudflare_token` and `hf_token`).
   - Tested against `https://api.bitbucket.org/2.0/user` and `/2.0/workspaces`: Atlassian returned `API Token provided has no Bitbucket scopes.` Flagged for operator to issue a Bitbucket-scoped token.
3. **Updated All 4 Repository READMEs (Track 2.1):**
   - Created `Dev_Lab/README.md` and appended the **Apache 2.0 / 2026-11-22 IP Snapshot Notice** to `HomeLabAI/README.md`, `Portfolio_Dev/README.md`, and `www_deploy/README.md`.
4. **Fixed `timeline_build.py` Tail-Clamping Bug & Built Iteration 1 (Track 3.3.1 & 3.3.2):**
   - Root cause: `maxTime` was hardcoded to `2026-04-15`, clamping all Sep–Nov discoveries to the right edge.
   - Refactored `renderGanttChart()` in `Portfolio_Dev/field_notes/timeline_build.py`:
     - Extended axis to `2025-10-15` → `2026-11-22` with all 13 monthly gridlines and a dashed gold `11/22 Freeze` line.
     - Replaced overlapping rectangles with dynamic sub-row **horizontal evolution lines** + **vertical revision ticks** (`conception_date`, `implementation_date`, optional `revisions[]`, and `last_evolved_date`).
   - Rebuilt `Portfolio_Dev/field_notes/timeline.html` and verified static independence.
5. **Bitbucket Auth Verified & Timeline Card/Sprint Link Audit (Track 3 & 5.1):**
   - Updated `~/.secrets/bitbucket_token` with scoped Atlassian/Bitbucket token; verified live API authentication as `kender242` (`Jason Allred`). Awaiting Bitbucket workspace slug to wire `[LAB-108]` backup remotes.
   - Audited `timeline_build.py` card rendering (`discovery-card`, isolated from common `dna_forge.html` cards) and `timeline_data.json` sprint links: found **11 of 17 sprint links broken (404)** because `timeline_build.py` hardcoded `docs/sprints/archive/${item.sprint_ref}` while `DISC-007`..`010` live in `active/` and `DISC-011`..`020` use short labels (`SPR-97.0`, `SPR-108.0`). Planned build-time path resolution + clickable code anchors + compact 1-line `Git:` (first/latest commit) provenance row.
6. **Roll-Up Audit Executed (BKM-097):**
   - Reconciled all 17 tracked conversation lanes (`1` through `5.3`, `C`, `D`) into the authoritative `ANCHOR_TRACK` table above, promoting Track `3` (clickable git history & broken sprint links) and Track `2.2` disk cleanup out of log bullets into tracked scope, and closing out `4.3`, `C`, and `D`.

### 2026-11-22 — Session 2 (`AGY:PRIMARY` Phase Promotion & Core Execution)
- **Delegation Override (Single-Phase):** Operator promoted Sprint 115 stories to `AGY:PRIMARY` for this mothball/IP phase (future sprints continue to enforce `AGENTS.md` Law 7 / `BKM-006` / `BKM-007`).
- **Delegation IP Verification:** Confirmed top-level delegation architecture is anchored in `DISC` (`DISC-008` Handover Reflection, `DISC-010` Tri-Loop Diagnostic Delegation Ladder, `DISC-012` Subversive Tool-Mediated Context Injection) and DNA (`BKM-017`, `BKM-034`, `BKM-042`, `BKM-049`, `FEAT-477`, `FEAT-552`, `LOOP-001`), and elevated to Pillar #1 of Exhibit A.
1. **Apache 2.0 `LICENSE` & `NOTICE` (Track 1 / 2.1):** Wrote verbatim Apache 2.0 `LICENSE` (11,358 B) and customized `NOTICE` files to all 4 repos (`Dev_Lab`, `HomeLabAI`, `Portfolio_Dev`, `www_deploy`).
2. **Header Injection & Close-Shop Scripts (Track 2.1 / 4.2):**
   - Built `Dev_Lab/scripts/apply_license_headers.py` (`--self-test` PASSED on 7 fixtures: shebang, encoding cookie, bash, JS, CSS, HTML DOCTYPE, idempotency, `py_compile`, `bash -n`). Dry-run counts: `HomeLabAI=571`, `Portfolio_Dev=141`, `www_deploy=29`, `Dev_Lab=0` (untracked scripts).
   - Built reversible `Dev_Lab/scripts/close_shop.sh` (verified `--dry-run`; not executed yet).
3. **Private Exhibit A Drafted (Track 3.1):** Created `Dev_Lab/PRIOR_INVENTIONS_EXHIBIT_A.md` with Tier 1 (215-char Workday field), Tier 2 (1-page 5-pillar Exhibit A including Delegation, JITC/Ambient Hooks, Distillation/Dynamic Papers, Heterogeneous GPU Pooling, and `M5-Local-oMLX`/`decky-trailers` 1-liners), repo/SHA table, and attestation.
4. **Timeline Iteration 2 Built (Track 3 / 3.2 / 3.3.1 / 3.4 / 3.5):**
   - Backfilled 8 new discoveries (`DISC-021`..`DISC-028`) into `Portfolio_Dev/dna/timeline_data.json` (25 total) and mined real git `first_commit`, `last_commit`, `last_evolved_date`, and monthly `revisions[]` bounded `<= 2026-11-22`.
   - Upgraded `Portfolio_Dev/field_notes/timeline_build.py` with build-time `active/`/`archive/` sprint link resolution, clickable Code Anchor pills (`blob` + `⏱ commits` history), compact 1-line `Git: First • Latest` provenance row, and Apache 2.0 footer.
   - Recompiled `Portfolio_Dev/field_notes/timeline.html` (25 discoveries, `unresolved_sprints=0`).
5. **AFK Heads-Down Execution & Freeze Certification (BKM-086 / BKM-024):**
   - Pre-flight verified (`lab-attendant.service` active; `/home` 146G free; `/speedy` 36G free).
   - Ran `apply_license_headers.py --apply` across all 4 repos (`HomeLabAI: 570`, `Portfolio_Dev: 140`, `www_deploy: 29`), verified 100% idempotency (`to_update=0` on re-run) and syntax (`py_compile` 644/647 ok with only 3 pre-existing legacy debug files, `bash -n` 31/31 ok).
   - Deprecated redundant `wisdom.html` (15.6 MB freed across `Portfolio_Dev` & `www_deploy`), promoted `timeline.html` to `PUBLIC_AIRLOCK_HTML` in `build_site.py`, synced `timeline.html` to `www_deploy`, and injected Apache 2.0 copyright footers into 8 public `www_deploy` pages.
   - Deleted local `/home/jallred/openbmc-lab` and untracked `/home/jallred/Dev_Lab/unsloth_compiled_cache`.
   - Committed all 4 repos cleanly and applied annotated tag `v2026.11.22-ip-snapshot` locally (zero `git push` per Law 0).

