# Sprint Plan: SPR-93.0 — Writing with Projections, Mice DNA Empowerment & Multi-Paper Publishing
**Date:** September 27, 2026  
**Goal:** Empower local mice with CLaRa-DNA retrieval, reposition the Projection Toolbar in `writer.html`, establish the multi-paper selection and publication purgatory pipeline in `papers.html`, synthesize the Chained Projections & Lens Crafting protocol via Cloud Oracle, and scaffold the lightweight Projection Studio sandbox.

---

## 🎯 Invariant Operational Laws (BKM-049 / BKM-024 / BKM-009)
1. **DELEGATION OWNER TAG MANDATE (BKM-049):** Every story declares an assigned owner (`[SWARM:LOCAL]`, `[SWARM:CLOUD]`, or `[AGY:PRIMARY]`). `[SWARM:*]` stories MUST be executed via `delegate.py` with 3 diagnostic retries for local before any cloud escalation.
2. **LIVE VALIDATION MANDATE (BKM-024):** Verify against active running daemons and reachable silicon endpoints.
3. **SOVEREIGN LOCAL PERSISTENCE (BKM-009 / BKM-040):** Checkpoint state via local `git commit`; strictly zero remote pushes.
4. **DNA & TRACEABILITY MANDATE (BKM-068):** Keep `FeatureTracker.md` and CLaRa-DNA synchronized with code modifications.

---

## 📋 Story Cards

### Story 93.1: Unblock DNA Retrieval Tools for Atlas & Mice Swarm Guidance
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Scope:** 
  1. Update `oh-my-openagent.json` to allow `clara-dna_query_dna`, `clara-dna_get_protocol`, and `clara-dna_list_collections` for `Atlas` (keeping `safe_patch: deny`).
  2. Update prompt instructions for `Atlas` and `Sisyphus-Junior` to query DNA specifications on demand.
* **Success Criteria:** Atlas configuration allows CLaRa-DNA MCP tools; configuration syntax is valid JSON.

### Story 93.2: Reposition Projection Toolbar in Writer Studio
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Target:** `Portfolio_Dev/field_notes/writer.html`
* **Scope:**
  1. Relocate `.projection-toolbar` from inside `<section id="write-view-panel">` to `<main class="studio-workspace">`, positioned directly below `<header class="studio-header">` and above `<div class="studio-viewport">`.
  2. Ensure the toolbar is a persistent fixture across both Tree View and Writing View modes.
  3. Verify flexbox layout so `.studio-viewport` scrolls cleanly without content clipping.
* **Verification Command:** `grep -n "projection-toolbar" Portfolio_Dev/field_notes/writer.html`
* **Success Criteria:** `.projection-toolbar` is rendered immediately following `<header class="studio-header">`.

### Story 93.3: Multi-Paper Selector & Publishing Purgatory in Papers Viewer
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Target:** `Portfolio_Dev/field_notes/papers.html`, `Portfolio_Dev/www_deploy/mission-control.js`
* **Scope:**
  1. Add a Paper Selector dropdown UI component at the top of `papers.html` below the title/mission-control header.
  2. Implement client-side paper dataset switching to load and render different published paper ASTs (e.g. `paper_jitc_intuition.json`, `PAPER-002_SEMANTIC_PACKING.json`, `PAPER-RESUME_v1.json`) from `data/papers/` with 0ms client-side projection tabs.
  3. Ensure `papers.html` is accessible and linked under `[Publications & Wisdom]` in `mission-control.js` for internal staging (`notes.jason-lab.dev`).
* **Verification Command:** `grep -n "paper-select" Portfolio_Dev/field_notes/papers.html`
* **Success Criteria:** Dropdown switches papers client-side; `papers.html` is accessible in internal navigation.

### Story 93.4: Cloud Oracle Synthesis on Chained Projections & Dynamic Lens Crafting Protocol
* **Assigned Owner:** `[SWARM:CLOUD]`
* **Scope:** Dispatch `delegate.py --mode oracle --cloud-only` to synthesize the architectural specification for:
  1. Moving beyond static lens presets to prompt-rubric driven Lens Crafting.
  2. Applying DNA cards (Philosophies, Vibes, BKMs) as stylistic and structural projection lenses.
  3. Mathematical invariants for Chained Projections ($P = f(B_{\text{canonical}}, L_{\text{local}}, L_{\text{global}})$) preventing serial generative decay.
* **Success Criteria:** Synthesis report written to `Portfolio_Dev/docs/sprints/active/ORACLE_REVIEW_SPRINT_93.md`.

### Story 93.5: Standalone Projection Studio Sandbox Scaffolding
* **Assigned Owner:** `[SWARM:CLOUD]`
* **Target:** `Portfolio_Dev/field_notes/projection_studio.html`
* **Scope:**
  1. Create a lightweight standalone sandbox page `field_notes/projection_studio.html` utilizing `<mission-control>` and `style.css`.
  2. Implement interactive UI: Text/Bone Input Gutter, Dynamic Lens Selector / Prompt Rubric Editor, and Real-Time Synthesis Preview Panel.
  3. Wire client-side mock/live Foyer `/paper/*` transform simulation with side-by-side diffing.
  4. Link `projection_studio.html` in `mission-control.js` under `[Publications & Wisdom]`.
* **Verification Command:** `test -f Portfolio_Dev/field_notes/projection_studio.html`
* **Success Criteria:** Clean standalone HTML sandbox rendering text-to-lens-to-synthesis testbed.

### Story 93.6: Intercom Triage Context Isolation & Sprint Certification
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Scope:**
  1. Audit `HomeLabAI/src/logic/cognitive_hub.py` and `triage_engine.py` to isolate turn intent classification from deep conversation memory.
  2. Execute unit and shakedown tests.
  3. Update `SPRINT_LOG_SPR_93.md` and feature tracking records.
* **Success Criteria:** 100% tests passing, clean local Git commit.
