# 📋 Sprint Plan: [SPR-86.0] The DNA Dropped Ball — End-to-End Audit, Flow Hardening & Adapter Synthesis

> **Sprint Type:** Core Architectural Audit, Deep Flow Hardening & LoRA Adapter Alignment  
> **Status:** ACTIVE & HEADS-DOWN  
> **Date:** September 2026  
> **Assigned Lead:** AGY + Autonomous Swarm  
> **Applicable Operational Laws:** BKM-004 (QQ Protocol), BKM-009 (Checkpoint Protocol), BKM-020 (Intent Preservation), BKM-024 (Live Silicon Validation), BKM-034 (Strict Task Delegation), BKM-040 (Git Discipline), BKM-041 (Automagic DNA Injection), BKM-049 (Owner Tag Mandate), BKM-060 (Polymorphic DNA Schema), PHL-035 (Invariant Truth & Fluid Projection), PHL-036 (Dense Token Hypothesis)

---

## 🧭 Executive Summary & Core Objectives

This sprint executes an exhaustive, end-to-end audit and refactoring of the entire DNA lifecycle across the Federated Lab. We audit every link in the chain—from automated nightly mutation generation, persistence, UX rendering, interactive revision promotion, bidirectional sync, database kickstart, to LoRA adapter alignment.

### The 8 Invariant DNA Flow Pillars Under Audit:
1. **Flow 1: Nightly Mutation Recommendation & Archival (`[FEAT-598]`)**
   - Automated nightly run scans lab activity, discovers mutation candidates, and writes them with structured status (`CANDIDATE`/`ARCHIVED`) to both disk JSON (`Portfolio_Dev/dna/`) and ChromaDB vector collections.
2. **Flow 2: UI Presentation of Mutations in DNA Forge & Writer**
   - `dna_forge.html` displays mutation cards with visual diff indicators, confidence scores, and source provenance.
3. **Flow 3: Interactive Mutation Certification & Promotion Flow**
   - 1-click promotion button triggering `POST /dna/certify_mutation` or `POST /dna/promote_draft`, upgrading mutations into numbered revisions with author stamp.
4. **Flow 4: Atomic Revision Persistence (File + DB Invariant)**
   - Double-write guarantee: newly approved revisions save back to `Portfolio_Dev/dna/*.json` and trigger instant ChromaDB collection upsert (`wisdom_dna`, `philosophy_dna`, `rdna`).
5. **Flow 5: Cold-Start / DB Kickstart from Original Source (`BKM-041`)**
   - 1-command complete reconstruction of ChromaDB from disk source (`Portfolio_Dev/dna/`, `FeatureTracker.md`, `Protocols.md`) via `sync_chroma_dna.py` with zero data loss.
6. **Flow 6: Revision History & UX Card Selection**
   - Card drawer in `dna_forge.html` allowing operators to browse chronological revisions ($v1 \dots vN$), select active projection, and review mutation lineage.
7. **Flow 7: Bidirectional Wordsmithing in `writer.html` (Both Tabs)**
   - Both tabs in `writer.html` (Document Editor & Voice Vector Switcher) seamlessly load revisions, allow manual edits to original source revisions in writer/forge, and save back to disk and DB.
8. **Flow 8: LoRA Adapter Training & Idiographic Stamp / Reverse DNA Alignment**
   - `build_lora_datasets.py` and `nightly_lora_training.py` generate training datasets from all DNA domains (`PHL`, `WIS`, `FEAT`, `BKM`, `RDNA`), training the model to think with idiographic stamps (`[BKM-xxx]`, `[PHL-xxx]`) and answer Reverse DNA questions directly.

---

## 🗺️ Sprint 86 Story Breakdown & Delegation Matrix

| Story | Title | Owner | Dispatch Mode | Key Deliverables & Target Files |
| :--- | :--- | :---: | :---: | :--- |
| **86.1** | Flow 1 Audit: Nightly Mutation Ingestion & Multi-Domain Archival | `[SWARM:CLOUD]` | Cloud Swarm / AGY Fallback | Audit & harden `HomeLabAI/src/infra/nightly_forge.py` and `HomeLabAI/src/curator/draft_decomposer.py`. Ensure candidate mutations write cleanly to `Portfolio_Dev/dna/*.json` and ChromaDB. |
| **86.2** | Flow 2 & 3 Audit: Mutation UI Presentation & Promotion REST Endpoint | `[AGY:PRIMARY]` | Local In-Session | Audit `HomeLabAI/src/v5/foyer/router.py` (`/dna/certify_mutation`, `/dna/promote_draft`) and `Portfolio_Dev/field_notes/dna_forge_build.py`. Verify 1-click promotion creates verified revision. |
| **86.3** | Flow 4 & 5 Audit: Atomic Disk + ChromaDB Persistence & Cold-Start Kickstart | `[AGY:PRIMARY]` | Local In-Session | Audit `Portfolio_Dev/sync_chroma_dna.py`, git pre-commit hooks, and Foyer save endpoints. Verify zero-data-loss cold start from `Portfolio_Dev/dna/`. |
| **86.4** | Flow 6 & 7 Audit: Multi-Revision Selection UX & `writer.html` Bidirectional Wordsmithing | `[AGY:PRIMARY]` | Local In-Session | Audit `Portfolio_Dev/field_notes/writer.html` and `dna_forge.html`. Verify revision switching, editing in place, and atomic save to disk + DB across both writer tabs. |
| **86.5** | Flow 8 Audit: LoRA Dataset Pipeline for Idiographic Stamps & Reverse DNA | `[SWARM:CLOUD]` | Cloud Swarm / AGY Fallback | Audit & expand `HomeLabAI/src/forge/build_lora_datasets.py` and `HomeLabAI/src/infra/nightly_lora_training.py` to ingest all DNA domains, idiographic stamps, and RDNA question bank. |
| **86.6** | Live Validation Suite & Sprint 86 Certification (`BKM-024`) | `[AGY:PRIMARY]` | Local In-Session | Run end-to-end integration tests, verify against live vLLM silicon and ChromaDB port 8001, produce live audit report. |

---

## 📊 Live Verification Gates
- [ ] Gate 1: `Portfolio_Dev/dna/*.json` files are tracked in git and trigger ChromaDB sync on commit.
- [ ] Gate 2: `sync_chroma_dna.py` cold-starts 100% of collections (`philosophy_dna`, `wisdom_dna`, `rdna`, `behavioral_dna`, `feature_dna`) from scratch without error.
- [ ] Gate 3: `POST /dna/promote_draft` and `POST /dna/certify_mutation` update disk JSON and ChromaDB atomically.
- [ ] Gate 4: `writer.html` bidirectional edits persist to disk and DB.
- [ ] Gate 5: `build_lora_datasets.py` generates verified training examples for idiographic stamps and RDNA queries.
