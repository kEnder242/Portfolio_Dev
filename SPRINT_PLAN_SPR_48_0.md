# 📜 SPRINT PLAN: Sprint 48.0 — RAG Matrix & Multi-Voice HyDE Synthesis Engine

**Session Focus**: Expand ChromaDB vector RAG collections, establish the `DNA vs. Work History` taxonomy (`career_ledger`, `artifact_vault`, `lab_journal`), synthesize Multi-Voice HyDE queries, implement multi-collection cosine distance reranking, and enforce Swarm Delegation Quality Gates.

---

## 🏛️ Architectural Context & Deep Dive

### 1. The RAG Architecture & HyDE Integration
*   **The 3-Tier RAG Engine (Intact & Active)**:
    *   **Tier 1 (Bedrock & Pre-Reflection)**: Micro Anchor Map (`career_compass.json` <300 tokens) + **HyDE Pre-Reflection** (150-token unified intent synthesis in `cognitive_hub.py`).
    *   **Tier 2 (Vector Discovery)**: ChromaDB (`chroma-server.service` on **Port 8001**).
    *   **Tier 3 (Physical Hydration)**: `[FEAT-407]` disk hydration opening physical JSON/MD files to extract un-truncated ground truth text.
*   **HyDE's Role**: HyDE operates at the **boundary of Tier 1 and Tier 2**. It uses Tier 1 LLM Pre-Reflection to generate a hypothetical answer string before querying Tier 2 ChromaDB vector collections on port 8001.

---

### 2. FEAT Taxonomy: Agent DNA vs. User Work History (`[FEAT-440]`)

To maintain clean boundaries between **Agent Operational Mechanics** (AGY / OpenAgent) and **User Engineering History**:

| Domain Namespace | Target Scope | ChromaDB Collections (Port 8001) | Primary Source Files |
| :--- | :--- | :--- | :--- |
| **Agent System DNA** | Operational blueprints, BKMs, and feature specs for AGY & OpenAgent swarm. | `behavioral_dna`<br>`feature_dna` | `HomeLabAI/docs/Protocols.md`<br>`Portfolio_Dev/FeatureTracker.md` |
| **User Work History** | 18-year validation engineering pedigree, focal goals, artifacts, and historical notes. | `career_ledger`<br>`artifact_vault`<br>`lab_journal` | `resume.txt`, `focal_goals.json`<br>`field_notes/data/index/search_index.json`<br>`raw_notes/*.txt` |

---

### 3. OpenAgent Swarm Governance & "Do Not Work Alone" Mandate
*   **Sequential Story Execution**: Execute Sprint 48.0 strictly one story at a time (Story 1 -> Story 2 -> Story 3 -> Story 4 -> Story 5).
*   **Swarm Delegation Mandate**: Sisyphus (Lead Manager in OpenAgent) is **strictly prohibited from working alone**. Sisyphus MUST delegate sub-tasks (code generation, syntax editing, test validation) to specialist subagents:
    *   `Sisyphus-Junior` (`qwen2.5-coder:14b` on Windows RTX 4090 / Node KENDER).
    *   `Prometheus` (`llama-3.3-70b` on Groq).
    *   `Hephaestus` (Verification and log checking).
*   **AGY Audit & Configuration Tuning Gate**:
    After each story completes, AGY (Strategic Co-pilot) will inspect OpenCode session logs to verify that subagents were invoked. If Sisyphus worked alone, AGY will tune the OpenCode prompt configuration or `--model` routing parameters in `delegate.py` before launching the next story.

---

## 🎯 Detailed Stories & Pre-Grounded Delegation Specs

### Story 1: Taxonomy Separation & ChromaDB Corpus Expansion (`career_ledger` & `artifact_vault`)
*   **Primary Target Files**:
    *   `src/forge/index_artifacts_to_rag.py` (New Script)
    *   `src/forge/index_resume_to_rag.py` (New Script)
    *   `src/tests/test_chroma_expansion.py` (New Integration Test)
*   **Context Anchors & Reference Files**:
    *   `field_notes/data/index/search_index.json` (Source of 43 Diamond Artifacts & Google Drive File IDs)
    *   `resume.txt` & `focal_goals.json` (Source of Work History Ground Truth)
    *   `src/bridge_burn_to_rag.py` (Reference ChromaDB HTTP client connection code on port 8001)
*   **Operational Requirements**:
    1.  **Artifact Indexer (`index_artifacts_to_rag.py`)**:
        *   Connect to ChromaDB HTTP server on `http://127.0.0.1:8001`.
        *   Create or get collection `artifact_vault`.
        *   Parse `field_notes/data/index/search_index.json`. For each artifact entry:
            *   Extract `id`, `title`, `synopsis`, `category`, `gdrive_id`, and `tags`.
            *   Formulate embedding text string: `f"Title: {title} | Synopsis: {synopsis} | Category: {category} | Tags: {', '.join(tags)}"`.
            *   Store metadata dictionary: `{"title": title, "category": category, "gdrive_id": gdrive_id, "type": "artifact"}`.
    2.  **Resume & Focal Indexer (`index_resume_to_rag.py`)**:
        *   Connect to ChromaDB HTTP server on `http://127.0.0.1:8001`.
        *   Create or get collection `career_ledger`.
        *   Parse `resume.txt` by section (Summary, Experience Era 1-6, Technical Skills).
        *   Parse `focal_goals.json` by goal category (Platform Telemetry, Validation Automation, Leadership).
        *   Index each chunk into `career_ledger` with metadata: `{"era": era_name, "domain": "career_pedigree"}`.
*   **Swarm Delegation Mandate**: Delegate initial indexer drafting to `Sisyphus-Junior` (KENDER 4090).
*   **Verification Gate Command**:
    ```bash
    python3 src/forge/index_artifacts_to_rag.py && python3 src/forge/index_resume_to_rag.py && python3 src/tests/test_chroma_expansion.py
    ```

---

### Story 2: Composite Multi-Voice HyDE Synthesis Engine (`cognitive_hub.py`)
*   **Primary Target Files**:
    *   `src/logic/cognitive_hub.py` (Lines 647–680: Unified Intent-HyDE Guided Decoding Schema & Prompt)
    *   `src/tests/test_hyde_plumbing.py` (Updated Unit/Integration Test Suite)
*   **Context Anchors & Reference Files**:
    *   `src/logic/cognitive_hub.py` (FEAT-436 Pre-Reflection Triage Schema)
    *   `FeatureTracker.md` (`[FEAT-436]`, `[FEAT-437]`)
*   **Operational Requirements**:
    1.  Update `triage_schema` in `cognitive_hub.py` to refine `hyde_vector_text` description to request 3-part multi-voice synthesis.
    2.  Update `triage_mode_context` string in `cognitive_hub.py`:
        ```python
        triage_mode_context = (
            "[MODE]: UNIFIED PRE-REFLECTION & TRIAGE\n"
            "Translate user intent ('I think the user is trying to say...').\n"
            "For technical, historical, or validation queries, synthesize a 3-part Composite HyDE Vector Query in hyde_vector_text following the exact format:\n"
            "[VALIDATION]: <silicon_term_or_pcie_ras> | [STRATEGY]: <focal_goal_or_leadership_impact> | [SRE]: <bkm_scar_or_shell_command>\n"
            "For casual quips or greetings, set addressed_to: PINKY, vibe: CASUAL, importance: 0.1, hyde_vector_text: ''."
        )
        ```
    3.  Ensure fallback HyDE cascades (`vLLM AWQ` on port 8088 -> raw query) preserve multi-voice tag structure.
*   **Swarm Delegation Mandate**: Delegate schema validation to `Prometheus` and code editing to `Sisyphus-Junior`.
*   **Verification Gate Command**:
    ```bash
    pytest src/tests/test_hyde_plumbing.py -v
    ```

---

### Story 3: Multi-Collection Cosine Distance Reranker (`archive_node.py`)
*   **Primary Target Files**:
    *   `src/nodes/archive_node.py` (`get_context()` function around lines 150–280)
    *   `src/tests/test_multi_collection_reranker.py` (New Integration Test)
*   **Context Anchors & Reference Files**:
    *   `src/nodes/archive_node.py` (Existing ChromaDB query & RAG context builder)
    *   `FeatureTracker.md` (`[FEAT-407] Physical File Hydration`)
*   **Operational Requirements**:
    1.  Update `archive_node.get_context(query_text, hyde_vector_text, top_k=5)`:
        *   Query all 5 ChromaDB collections in parallel on port 8001: `behavioral_dna`, `feature_dna`, `career_ledger`, `artifact_vault`, and `lab_journal`.
        *   Use `hyde_vector_text` if provided, falling back to `query_text`.
    2.  Implement a unified cosine similarity reranker:
        *   Flatten results from all 5 collections into a single candidate list.
        *   Sort candidates ascending by ChromaDB distance score (`distance < 0.45` relevance cutoff).
        *   Format top-k context payload with domain badges:
            *   `[ARTIFACT: Title]` (includes Google Drive Link if present)
            *   `[CAREER: Era/Skill]` (from `career_ledger`)
            *   `[BEHAVIORAL_DNA: BKM-ID]` (from `behavioral_dna`)
            *   `[FEATURE_DNA: FEAT-ID]` (from `feature_dna`)
            *   `[LAB_JOURNAL: Note-ID]` (from `lab_journal`)
*   **Swarm Delegation Mandate**: Delegate reranker algorithm implementation to `Sisyphus-Junior` and log check to `Hephaestus`.
*   **Verification Gate Command**:
    ```bash
    python3 src/tests/test_multi_collection_reranker.py
    ```

---

### Story 4: FeatureTracker & Protocol Documentation Updates
*   **Primary Target Files**:
    *   `Portfolio_Dev/FeatureTracker.md` (Add `[FEAT-440]` and `[FEAT-441]`)
    *   `HomeLabAI/docs/Protocols.md` (Add BKM section on `DNA vs. Work History` taxonomy & LoRA Tabling decision)
*   **Context Anchors & Reference Files**:
    *   `Portfolio_Dev/FeatureTracker.md` (Section tail around line 1490)
    *   `HomeLabAI/docs/Protocols.md` (BKM-034 / BKM-035 sections)
*   **Operational Requirements**:
    1.  Append `## [FEAT-440] Taxonomy Separation: Agent DNA vs. User Work History` and `## [FEAT-441] ChromaDB Multi-Collection Cosine Reranker` to `FeatureTracker.md`.
    2.  Update `Protocols.md` documenting:
        *   The separation of Agent DNA (`behavioral_dna`, `feature_dna`) vs. User Work History (`career_ledger`, `artifact_vault`, `lab_journal`).
        *   The architectural decision to table LoRA fine-tuning for HyDE in favor of structured prompt synthesis.
*   **Verification Gate Command**:
    ```bash
    git diff Portfolio_Dev/FeatureTracker.md HomeLabAI/docs/Protocols.md
    ```

---

### Story 5: End-to-End RAG Matrix & Swarm Delegation Capstone Test
*   **Primary Target Files**:
    *   `src/tests/test_integration_rag_matrix.py` (New Capstone Integration Test)
*   **Context Anchors & Reference Files**:
    *   `src/tests/test_integration_tri_node.py` (Reference end-to-end multi-node integration suite)
    *   `src/tests/test_integration_kender.py` (Reference KENDER inference test)
*   **Operational Requirements**:
    1.  Write `test_integration_rag_matrix.py`:
        *   Execute end-to-end query via `CognitiveHub` (`cognitive_hub.py`) -> `ArchiveNode` (`archive_node.py`) -> ChromaDB (`:8001`).
        *   Assert multi-voice HyDE vector is synthesized by KENDER or fallback cascade.
        *   Assert returned RAG payload contains merged context from `career_ledger`, `artifact_vault`, and `lab_journal`.
        *   Assert execution latency is `<1500ms`.
*   **Verification Gate Command**:
    ```bash
    python3 src/tests/test_integration_rag_matrix.py
    ```

---

## 📊 Delegation Ready Checklist

- [x] Story 1: `career_ledger` & `artifact_vault` ChromaDB Collections (`src/forge/index_*.py`)
- [x] Story 2: Composite Multi-Voice HyDE Synthesis (`src/logic/cognitive_hub.py`)
- [x] Story 3: Multi-Collection Cosine Reranker (`src/nodes/archive_node.py`)
- [x] Story 4: FeatureTracker & Protocol Documentation Updates
- [x] Story 5: End-to-End RAG Matrix Capstone Integration Suite (`test_integration_rag_matrix.py`)
