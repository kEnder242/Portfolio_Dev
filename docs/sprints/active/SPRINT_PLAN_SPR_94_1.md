# Sprint Plan: SPR-94.1 — Projection Engine Hardening & Cognitive Swarm Architecture
**Date:** September 28, 2026  
**Goal:** Consolidate post-sprint architectural breakthroughs, finalize DNA taxonomy migration (PHL → INS), enforce the Anxiety & Cognitive Safety Invariant (`FEAT-625` / `LOOP-002`), restore full-fidelity 490-card wisdom manifest, and prepare the Grill-Me session for deferred complex engines.

---

## 🎯 Architectural Mandates (BKM-049 / BKM-060 / BKM-069 / BKM-072)
1. **PSYCHOLOGICAL SAFETY INVARIANT (INS-040 / FEAT-625):** Small/medium local models (27B) wander when bounds are ambiguous. Invariant contracts declare completeness, welcome naive starts, and guarantee outer-loop repair.
2. **PURE LAYER BOUNDARIES (AGENTS_L1 / L2 / L3):** L2 (`Atlas`) does NOT write to disk (`write: deny`). L2 constructs complete in-memory skeletons and companion tests in `task()` payloads. L3 (`Hephaestus`/`Junior`) executes Turn 1 physical file `write`.
3. **AUTHORITATIVE DNA DOMAINS (BKM-060):** `INS` (Inspiration / Applied Philosophy) replaces `PHL`. `philosophy_data.json` is purged; `sync_chroma_dna.py` and `dna_manifest.json` operate on genuine `INS` (38 cards) and `WIS` (490 cards).
4. **SESSION RESILIENCE & DEAD PID REAPING:** Headless OpenCode sessions on REST `:4097` track active PIDs via `/tmp/active_openagent_sessions.json` and auto-reap dead processes.

---

## 📊 Phase 2 Execution Matrix

| Story ID | Title | Assigned Owner | State | Deliverable / Target |
| :--- | :--- | :--- | :--- | :--- |
| **Story 94.8** | Full-Fidelity DNA Manifest Bridge | `[AGY:PRIMARY]` | ✅ **COMPLETED** | 490 WIS + 38 INS + 3 VIBE in `dna_manifest.json` |
| **Story 94.9** | Epistemic Anxiety Axiom & Contract FEAT | `[AGY:PRIMARY]` | ✅ **COMPLETED** | `INS-040`, `FEAT-625`, `LOOP-002` in `LOOP_LEDGER.md` |
| **Story 94.10** | PHL → INS Deprecation & ChromaDB Sync | `[AGY:PRIMARY]` | ✅ **COMPLETED** | `sync_chroma_dna.py` synced 38 INS to `:8001` |
| **Story 94.11** | OpenAgent Session Breadcrumb Supervisor | `[AGY:PRIMARY]` | ✅ **COMPLETED** | Dead PID reaper active in `delegate.py` |
| **Story 94.12** | 3-Resume AST Diffing & Multi-Document Join | `[GRILL-ME:PREP]` | ⏸️ **DEFERRED** | Needs design alignment on bone-ID join semantics |
| **Story 94.13** | Hiring Platform & ATS Scraper Strategy | `[GRILL-ME:PREP]` | ⏸️ **DEFERRED** | Needs requirements & compliance/ToS posture |

---

## 📋 Story Cards (Phase 2 & Hardening)

### Story 94.8: Full-Fidelity DNA Manifest Bridge
* **Status:** ✅ **COMPLETED**
* **Target:** `Portfolio_Dev/scripts/dna_manifest_bridge.py`, `Portfolio_Dev/field_notes/data/dna_manifest.json`
* **Artifact:** `dna_manifest_bridge.py` now ingests `wisdom_data.json` (490 cards), `inspiration_data.json` (38 cards), and `vibe_data.json` (3 cards).

### Story 94.9: Epistemic Anxiety Axiom & Contract Model Registration
* **Status:** ✅ **COMPLETED**
* **Target:** `Portfolio_Dev/dna/inspiration_data.json`, `Portfolio_Dev/FeatureTracker.md`, `Portfolio_Dev/field_notes/data/LOOP_LEDGER.md`
* **Artifact:** `INS-040` authored, `[FEAT-625]` registered, `[LOOP-002]` registered.

### Story 94.10: PHL → INS Deprecation & ChromaDB Sync
* **Status:** ✅ **COMPLETED**
* **Target:** `Portfolio_Dev/dna/philosophy_data.json` (deleted), `Portfolio_Dev/sync_chroma_dna.py`
* **Artifact:** ChromaDB `:8001` fully rebuilt with `inspiration_dna` and `wisdom_dna`.

### Story 94.11: OpenAgent Session Breadcrumb Supervisor
* **Status:** ✅ **COMPLETED**
* **Target:** `HomeLabAI/src/tests/delegate.py`
* **Artifact:** Dead PID breadcrumbs and orphan reaper verified in `delegate.py`.

---

## ⏸️ Deferred Items for Grill-Me Session

1. **Multi-Document AST Join Engine (Story 94.12):**
   - *Risk / TLC Need:* AST diffing across 3 disparate resumes requires a stable node-hash algorithm; naive line diffs cause structural corruption.
2. **External ATS / Hiring Platform Ingestion (Story 94.13):**
   - *Risk / TLC Need:* Scraping external sites without strict offline fixture boundaries risks flakiness and network-coupling in nightly pipelines.
