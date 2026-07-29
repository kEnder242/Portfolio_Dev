# 📜 SPRINT PLAN: Sprint 48.0 — RAG Matrix & Multi-Voice HyDE Synthesis Engine

**Session Focus**: Expand ChromaDB vector RAG collections, establish the `DNA vs. Work History` taxonomy (`career_ledger`, `artifact_vault`, `lab_journal`), synthesize Multi-Voice HyDE queries, and implement multi-collection cosine distance reranking.

---

## 🏛️ Architectural Context & Deep Dive

### 1. The RAG Architecture & HyDE Integration (Clarification)
*   **The 3-Tier RAG Engine (Intact & Active)**:
    *   **Tier 1 (Bedrock & Pre-Reflection)**: Micro Anchor Map (`career_compass.json` <300 tokens) + **HyDE Pre-Reflection** (150-token unified intent synthesis in `cognitive_hub.py`).
    *   **Tier 2 (Vector Discovery)**: ChromaDB (`chroma-server.service` on **Port 8001**).
    *   **Tier 3 (Physical Hydration)**: `[FEAT-407]` disk hydration opening physical JSON/MD files to extract un-truncated ground truth text.
*   **HyDE's Role**: HyDE operates at the **boundary of Tier 1 and Tier 2**. It uses Tier 1 LLM Pre-Reflection to generate a hypothetical answer string before querying Tier 2 ChromaDB vector collections.
*   **Current Ground Truth & Resume/Focal Gap**:
    *   Previously, `resume.txt` and focal goals were used as a **Synthesis Guide** (`synthesize_career_mesh()` in `mass_scan.py`) to enrich disk JSON files.
    *   However, `resume.txt` and `focal_goals.json` currently **lack direct, fine-grained vector RAG lookup** in ChromaDB.

---

### 2. FEAT Taxonomy: Agent DNA vs. User Work History (`[FEAT-440]`)

To maintain clean boundaries between **Agent Operational Mechanics** (AGY / OpenAgent) and **User Engineering History**:

| Domain Namespace | Target Scope | ChromaDB Collections (Port 8001) |
| :--- | :--- | :--- |
| **Agent System DNA** | Operational blueprints, BKMs, and feature specs for AGY & OpenAgent swarm. | `behavioral_dna` (`Protocols.md`)<br>`feature_dna` (`FeatureTracker.md`) |
| **User Work History** | 18-year validation engineering pedigree, focal goals, artifacts, and historical notes. | `career_ledger` (`resume.txt`, `focal_goals.json`)<br>`artifact_vault` (43 Diamond Artifacts & Drive IDs)<br>`lab_journal` (Chronological note gems) |

---

### 3. The Multi-Voice HyDE Compromise
Instead of forcing the triage engine to guess whether the user is asking about Silicon Validation, Strategic Goals, or SRE Scars, HyDE will generate a **3-Part Composite Hypothesis**: `[VALIDATION]: <silicon_term> | [STRATEGY]: <goal_impact> | [SRE]: <bkm_scar>`.

By querying ChromaDB's collections simultaneously, **ChromaDB's native cosine distance metric handles weighting automatically**—the highest relevance match naturally surfaces regardless of domain.

---

### 4. LoRA Adapter Decision: **TABLED**
*   **Decision**: Table LoRA fine-tuning for HyDE hypothesis generation.
*   **Rationale**: KENDER (Node 'Brain' / RTX 4090 running `qwen2.5-coder:14b` on port 11434) handles HyDE. Training a custom LoRA adapter for KENDER introduces significant dataset curation, fine-tuning, and model tag maintenance overhead. Structured prompt synthesis via FEAT-436 achieves >90% of the accuracy benefit with zero model retraining.

---

## 🎯 Stories & Tasks

### Story 1: Taxonomy Separation & ChromaDB Corpus Expansion (`career_ledger` & `artifact_vault`)
*   **Goal**: Create and populate `career_ledger` and `artifact_vault` collections on port 8001 under `[FEAT-440]`.
*   **Tasks**:
    1.  Write `src/forge/index_artifacts_to_rag.py`: Parse `field_notes/data/index/search_index.json`, extract titles, synopses, tags, and Google Drive links, and index them into `artifact_vault` on port 8001.
    2.  Write `src/forge/index_resume_to_rag.py`: Parse `resume.txt` and `focal_goals.json`, slice into semantic sections, and index into `career_ledger` on port 8001.
*   **Verification Gate**: `python3 src/tests/test_chroma_expansion.py` verifying vector query returns in `<50ms` from both `artifact_vault` and `career_ledger`.

---

### Story 2: Composite Multi-Voice HyDE Synthesis Engine (`cognitive_hub.py`)
*   **Goal**: Refactor FEAT-436 HyDE generation to produce multi-voice technical hypotheses.
*   **Tasks**:
    1.  Update `triage_mode_context` in `cognitive_hub.py` to prompt KENDER for a 3-part structured HyDE vector string: `[VALIDATION]: <silicon_term> | [STRATEGY]: <goal_impact> | [SRE]: <bkm_scar>`.
    2.  Ensure fallback HyDE cascades (vLLM AWQ -> raw query) preserve multi-voice structure.
*   **Verification Gate**: `pytest src/tests/test_hyde_plumbing.py` verifying multi-voice synthesis output schema.

---

### Story 3: Multi-Collection Cosine Distance Reranker (`archive_node.py`)
*   **Goal**: Query all 5 ChromaDB collections in parallel and rank by cosine distance.
*   **Tasks**:
    1.  Update `archive_node.get_context()` to execute parallel queries across `behavioral_dna`, `feature_dna`, `career_ledger`, `artifact_vault`, and `lab_journal`.
    2.  Implement a unified cosine similarity reranker (`distance < 0.45` threshold) returning top-k merged results with source metadata badges (e.g. `[ARTIFACT: Drive Link]`, `[CAREER: Optane AEP]`).
*   **Verification Gate**: `python3 src/tests/test_multi_collection_reranker.py` executing cross-domain queries.

---

### Story 4: FeatureTracker & Protocol Documentation Updates
*   **Goal**: Register `[FEAT-440]` and document the new RAG taxonomy.
*   **Tasks**:
    1.  Update `FeatureTracker.md` with `[FEAT-440] Taxonomy Separation: Agent DNA vs. User Work History` and `[FEAT-441] ChromaDB Multi-Collection Cosine Reranker`.
    2.  Update `Protocols.md` documenting the decision to table LoRA fine-tuning for HyDE.
*   **Verification Gate**: `git diff` review and ChromaDB pre-commit vector hook pass.

---

## 📊 Summary Checklist

- [ ] Story 1: `career_ledger` & `artifact_vault` ChromaDB Collections (`[FEAT-440]`)
- [ ] Story 2: Composite Multi-Voice HyDE Synthesis (`cognitive_hub.py`)
- [ ] Story 3: Multi-Collection Cosine Reranker (`archive_node.py`)
- [ ] Story 4: FeatureTracker & Protocol Documentation Updates
