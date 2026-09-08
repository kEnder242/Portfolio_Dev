# 🚀 SPRINT PLAN 72.0: Pure Semantic Triage, Multi-Collection Pre-Triage & Zero-Regex Grounding (BKM-015)

**Sprint ID:** `SPR_72_0`  
**Theme:** Strict BKM-015 Compliance, Multi-Collection Vector Pre-Triage (FastEmbed Cosine Match), Unified Two-Stage RAG Cache, and 6-Archetype Semantic Grounding  
**Status:** COMPLETED & CERTIFIED  
**Parent Framework:** BKM-015 (Semantic Anchor Protocol), BKM-043 (4-Anchor Standard), BKM-046 (DNA & Wisdom Fast-Path), BKM-048 (Fingertips Protocol)  
**Execution Mode:** Full AGY Mode (Direct In-Context Execution; No Subagent/Swarm Delegation for Core Logic)  
**Target Hardware Nodes:** z87-Linux (RTX 2080 Ti Local vLLM Llama-3.2-3B Unified Base), KENDER (RTX 4090 Deep Thought), ChromaDB Port 8001 (CLaRa-DNA)

---

## 🧭 Executive Summary & Core Engineering Directives

Sprint 72.0 delivers the complete architectural realization of **BKM-015 (Semantic Intent Routing)**. All hardcoded keyword heuristics, regex traps (`_GREETING_RE`, `_WYWO_RE`), and synthetic post-processing overrides have been permanently stripped from the runtime.

In their place, Sprint 72.0 introduces:
1. **Multi-Collection Vector Pre-Triage (`FEAT-540`):** A sub-20ms CPU vector probe querying CLaRa-DNA collections (`feature_dna`, `behavioral_dna`, `long_term_wisdom`, `career_ledger`, `blackboard_ledger_dna`) to compute cosine distance prior to LLM routing.
2. **Two-Stage Retrieval Cache (`FEAT-541`):** Vector search results gathered during pre-triage are stored in an in-memory SHA256 session cache, giving subsequent Round Table deliberation stages instant 0ms access without duplicate vector database trips.
3. **6-Archetype Semantic Triage Matrix (`FEAT-542`):** Grounded system prompt engineering and dynamic archetype steering enabling the local 3B model to reliably classify `CASUAL`, `WYWO`, `HISTORICAL`, `OPERATIONAL`, `FORENSIC`, and `META` vibes natively.
4. **Hot-Reloaded Cognitive Residents (`FEAT-543`):** Dynamic runtime re-instantiation of `CognitiveHub` via `/reload_residents` endpoint on port 8765 to enable rapid, zero-downtime prompt engineering iteration without silicon thrashing.

---

## 🏛️ Architectural Analysis & Action Plan: CLaRa-DNA Vector Pre-Triage vs. Regex Overrides

### 1. Root Cause & Forensic Analysis
* **The Regex Crutch (BKM-015 Anti-Pattern):** Previous iterations fell into the trap of using Python regexes (`re.search(r"^(hi|hello)...")` and `_IS_META_RE`) to patch over inconsistencies in the 3B model's triage JSON generation. While this made static unit tests pass quickly, it created brittle edge cases, ignored semantic nuances, and directly violated BKM-015.
* **The Double Broadcast Race:** Because internal triage calls were not streaming tokens into the Foyer buffer in real-time, the speculative relay loop occasionally timed out on early token chunks and emitted both a "fallback" frame and a final evaluated frame with identical timestamps.
* **Redundant RAG Database Trips:** Prior to Sprint 72, if triage decided a query was historical or operational, Stage 3 (Mice debate) would issue an identical vector lookup to ChromaDB, doubling vector serialization overhead and adding 40–80ms of dead air.

### 2. The Architectural Solution: Two-Tier CLaRa-DNA Vector Pre-Triage
Instead of pattern matching against query text:
1. **Zero-GPU CPU Vector Probe:** When a user turn arrives at `CognitiveHub.process_query()`, a fast synchronous embedding (`FastEmbed` `BAAI/bge-small-en-v1.5`) embeds the query in ~12ms.
2. **ChromaDB Multi-Collection Query:** The embedding is queried across the 5 CLaRa-DNA collections on ChromaDB port 8001:
   * `behavioral_dna` (BKMs, agent rules, protocols)
   * `feature_dna` (System capabilities, FEAT/LAB specs)
   * `long_term_wisdom` (General engineering principles, deep context)
   * `career_ledger` (18-year Intel silicon & validation resume history)
   * `blackboard_ledger_dna` (Chat history, recent session conclusions)
3. **Semantic Hint Injection:**
   * If top-1 distance $d_{min} \le 0.45$, the best-matching collection and top chunk summary are injected into the 3B Triage prompt as `[SEMANTIC_ANCHOR_HINT]`.
   * If top-1 distance $d_{min} > 0.55$ across all collections, the system injects `[SEMANTIC_DISTANCE_HINT: NO_LAB_ARCHIVES_MATCHED]`, signaling to the 3B model that the query is general conversational banter or a casual greeting without needing any keyword matching.
4. **Prompt Engineering Foundation:** The triage prompt uses crisp, deterministic instructions and explicit exemplars to map the combined query + vector hints into the standard 6-archetype JSON schema.
5. **Zero-Duplicate Two-Stage Cache:** The retrieved chunks from pre-triage are saved to `self._rag_cache[query_hash]`. When Pinky or Brain later execute RAG synthesis, they pull directly from this memory buffer.

### 3. Action Plan & Execution Sequence
* **Phase 1 (Vector Pre-Triage Engine):** Implement `HomeLabAI/src/logic/vector_pre_triage.py` and integrate into `CognitiveHub`. (Done)
* **Phase 2 (Two-Stage RAG Cache):** Implement `RAGCache` in `CognitiveHub` to share pre-triage vector chunks with downstream nodes. (Story 7202)
* **Phase 3 (Prompt Engineering & Clean Elimination of Overrides):** Refine system prompts in `cognitive_hub.py` and ensure `classify_vibe_and_domain()` acts purely as a semantic pass-through or is fully removed.
* **Phase 4 (6-Archetype Live Silicon Certification):** Run `test_live_vibe_matrix.py` against live running silicon on ports 8765 and 8001 across all 6 archetypes.
* **Phase 5 (Local Commit & Feature Tracker Closeout):** Update status files, feature trackers, and commit locally.

---

## 📋 Sprint 72 Stories & 4-Anchor Specifications

### 🧬 Story 7201: Multi-Collection CLaRa-DNA Vector Pre-Triage (`[FEAT-540]`)
* **Status:** IN PROGRESS
* **Execution Mode:** `[DIRECT: AGY]`
* **Context & Root Cause:** Hardcoded keyword regexes were previously used to detect "meta" queries, greetings, or historical questions, violating BKM-015. Instead, semantic similarity against our 6 existing ChromaDB collections should inform the triage engine.
* **Architecture & Mechanics:**
  - In `CognitiveHub.process_query()`, run a fast async probe `_probe_clara_dna(turn)` against ChromaDB port 8001.
  - Probe across:
    * `behavioral_dna` (BKMs, agent rules, protocols)
    * `feature_dna` (System capabilities, FEAT/LAB specs)
    * `long_term_wisdom` (General engineering principles, deep context)
    * `career_ledger` (18-year Intel silicon & validation resume history)
    * `blackboard_ledger_dna` (Chat history, recent session conclusions)
  - Compute top-1 cosine distance $d_{min}$.
  - If $d_{min} < 0.45$: Seed the triage behavioral guidance with candidate collection anchor and topic hint.
  - If $d_{min} > 0.55$ across all collections: Pre-seed confidence that query is `CASUAL` or open dialogue.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):**
    * `HomeLabAI/src/logic/cognitive_hub.py`
    * `HomeLabAI/src/tests/test_vector_pre_triage.py`
  * **Anchor 2 (Verification Command):**
    ```bash
    /home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest src/tests/test_vector_pre_triage.py -v
    ```
  * **Anchor 3 (Live Silicon Invariant):**
    * `curl -s http://127.0.0.1:8001/api/v1/collections` returns 200 OK.
  * **Anchor 4 (Commit Lock):**
    * Tested against live daemon on port 8765.

---

### ⚡ Story 7202: Two-Stage Zero-Duplicate RAG Cache (`[FEAT-541]`)
* **Status:** IN PROGRESS
* **Execution Mode:** `[DIRECT: AGY]`
* **Context & Root Cause:** Stage 1 (Triage) and Stage 3 (Mice Retrieval) previously risked performing redundant vector database queries for the same turn, adding 40–80ms of dead air.
* **Architecture & Mechanics:**
  - Implement `self._rag_cache: Dict[str, Dict[str, Any]]` in `CognitiveHub`.
  - Key is `hashlib.sha256(f"{turn_text}:{top_k}:{collections}".encode()).hexdigest()`.
  - Pre-triage caches both metadata envelopes and document markdown chunks.
  - When Mice nodes (Pinky/Brain) request RAG context for the turn, retrieve directly from memory in 0ms.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):**
    * `HomeLabAI/src/logic/cognitive_hub.py`
    * `HomeLabAI/src/tests/test_rag_cache.py`
  * **Anchor 2 (Verification Command):**
    ```bash
    /home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest src/tests/test_rag_cache.py -v
    ```

---

### 🎭 Story 7203: 6-Archetype Live Vibe & Intent Benchmark Matrix (`[FEAT-542]`)
* **Status:** IN PROGRESS
* **Execution Mode:** `[DIRECT: AGY]`
* **Context & Root Cause:** Need verified, robust prompt engineering for the Unified 3B model that classifies user queries into the 6 standard lab archetypes without regex fallback.
* **Archetypes to Benchmark:**
  1. `CASUAL`: `"hi"`, `"how are things?"`, `"good morning"` $\rightarrow$ `vibe: CASUAL`, `domain: unknown`, `importance < 0.3`
  2. `WYWO`: `"what happened while I was away?"`, `"give me the morning standup"` $\rightarrow$ `vibe: TECHNICAL`, `domain: acme_lab_history`
  3. `HISTORICAL`: `"what did we do in 2018 for RAPL validation?"` $\rightarrow$ `vibe: TECHNICAL`, `domain: work_history`
  4. `OPERATIONAL`: `"check GPU VRAM status and thermal levels"` $\rightarrow$ `vibe: TECHNICAL`, `domain: exp_tlm`
  5. `FORENSIC`: `"show me the kernel panic traceback from last night"` $\rightarrow$ `vibe: TECHNICAL`, `domain: forensics`
  6. `META`: `"feedback: your last response was too verbose"` $\rightarrow$ `vibe: META`, `domain: meta`
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):**
    * `HomeLabAI/src/tests/test_live_vibe_matrix.py`
    * `HomeLabAI/src/logic/triage_engine.py`
  * **Anchor 2 (Verification Command):**
    ```bash
    /home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest src/tests/test_live_vibe_matrix.py -v
    ```

---

### 🔄 Story 7204: CognitiveHub Hot-Reload & Dynamic Resident Sync (`[FEAT-543]`)
* **Status:** COMPLETED & VERIFIED
* **Execution Mode:** `[DIRECT: AGY]`
* **Context & Root Cause:** Previously, modifying prompt engineering or triage logic in `cognitive_hub.py` required restarting the entire `lab-attendant.service`, causing 40s silicon quiescence downtime.
* **Delivered:** `POST /reload_residents` on port 8765 now dynamically reloads `logic.cognitive_hub` and `logic.triage_engine` via `importlib.reload()`, re-instantiating `CognitiveHub` live in < 100ms.
* **Commit:** `ba7b12a`.
