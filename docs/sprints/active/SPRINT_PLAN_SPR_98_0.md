# 🚀 SPRINT PLAN 98.0: Subversive Tool-Mediated Delegation & Empirical Trust Engineering

**Sprint ID:** `SPR_98_0`  
**Theme:** Subversive Tool-Mediated IPC (`research`), Empirical Prompt Trust Calibration, Diagnostic Whisperer (`failure_whisperer`), Clean Handoff (`handoff_checkpoint`), Path Resolver (`locate_path`), Pre-Warmed Session Resumption, and Zero-Wandering Local Swarm Execution (`FEAT-647`–`FEAT-649`)  
**Status:** **ACTIVE**  
**Parent Framework:** `[BKM-049]` (The Delegation Execution Rulebook), `[BKM-071]` (Delegation Playbook Index), `[INS-044]` (The "Trust-Me-Bro" Grounding Skepticism Law), `[DISC-012]` (Subversive Tool-Mediated Context Injection), `[BKM-072]` (Tool-as-IPC Swarm Delegation Protocol), `[BKM-060]` (Federated DNA Domains), `[BKM-024]` (Live Validation Mandate)  
**Target Silicon Nodes:** Node KENDER (RTX 4090 Ollama Conductor :11434), Node Brain (macOS M5 Air MLX :8002 via Headroom), ChromaDB Port 8001 (CLaRa-DNA)

---

## 🧭 Executive Summary & Architectural Contract

Sprint 98.0 directly attacks the fundamental failure mode of agentic delegation on small/medium reasoning models: **the "Trust-Me-Bro" exploration trap (`[INS-044]`)**. When prompt preambles assert that grounding has already been performed, models treat the assertion with skepticism and spend tokens in unconstrained exploratory loops.

Sprint 98.0 replaces static prompt spoon-feeding with **Subversive Tool-Mediated IPC (`[DISC-012]` / `[FEAT-647]`)**:
1. **`research` ("JITC Research tool"):** A dedicated tool bridge where workers query target files and receive pre-computed $L_2$ conductor patch notes formatted dynamically as "empirical findings."
2. **`failure_whisperer`:** Diagnostic fast lane sending failing `pytest` stack traces to M5 Air / local silicon for instant 2-line root-cause triage.
3. **`handoff_checkpoint`:** Subversive handoff tool logging completion reflection to `delegation_ledger.jsonl` and cleanly closing worker execution.
4. **`locate_path`:** Refined, enticing path locator and import resolver replacing `locate_grounding` to eliminate grep wandering.
5. **Empirical Trust Gradient Calibration:** Systematic tuning of $L_3$ prompts from naive assertion $\to$ forceful directive $\to$ subversive tool trigger.
6. **Pre-Warmed Session Resumption:** Reusing pre-warmed worker sessions on M5 Air that block on `research` rather than cold-starting fresh processes.
7. **Zero-Wander Local Swarm Certification:** Achieving $\le 3$ turns and $<60\text{s}$ execution per story on local silicon with zero unprompted `read`/`grep` wandering.

```mermaid
flowchart TD
    subgraph STAGE0 ["🔍 Pre-Flight"]
        S98_0["Story 98.0: Oracle Pre-Pass & Bedrock DNA Validation [SWARM:ORACLE]"]
    end
    subgraph STAGE1 ["🛠️ Subversive Tool Suite & State Cache"]
        S98_1["Story 98.1: Subversive Tool Suite (research, failure_whisperer, handoff_checkpoint, locate_path) [FEAT-647] [SWARM:LOCAL]"]
    end
    subgraph STAGE2 ["🎭 Prompt Trust Engineering"]
        S98_2["Story 98.2: Empirical Trust Gradient & Subversive L3 Prompt Calibration [DISC-012] [SWARM:LOCAL]"]
        S98_3["Story 98.3: Pre-Warmed Worker Session Resumption & Tool Blocking [FEAT-648] [SWARM:CLOUD]"]
    end
    subgraph STAGE3 ["🧪 Shakedown & Benchmark"]
        S98_4["Story 98.4: Zero-Wandering Local Swarm Certification on 4090 + M5 Air [BKM-072] [SWARM:LOCAL]"]
    end

    S98_0 --> S98_1
    S98_1 --> S98_2
    S98_2 --> S98_3
    S98_3 --> S98_4
```

---

## 📋 Granular Story Breakdown

### 🔍 Story 98.0: Oracle Pre-Pass on Sprint 98 & DNA Grounding
* **Assigned Owner:** `[SWARM:ORACLE]`
* **Feature Anchor:** `[FEAT-647]`
* **Status:** **PENDING EXECUTION**
* **Task Breakdown:**
  1. Adversarially audit Sprint 98.0 specifications against `[INS-044]`, `[DISC-012]`, and `[BKM-049]`.
  2. Verify tool schemas for `research`, `failure_whisperer`, `handoff_checkpoint`, and `locate_path` do not introduce MCP ballast tax (`[BKM-051]`).
  3. Emit structured review report to `Portfolio_Dev/docs/sprints/active/ORACLE_REVIEW_SPRINT_98.md`.

---

### 🛠️ Story 98.1: Subversive Tool Suite (`research`, `failure_whisperer`, `handoff_checkpoint`, `locate_path`) & Conductor Cache
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Feature Anchor:** `[FEAT-647]`
* **Status:** **PENDING EXECUTION**
* **Why & Root Cause:** $L_3$ workers ignore static prompt blueprints because of model skepticism. They need enticing, targeted tool endpoints that provide patch blueprints, test triage, and structured handoff on demand.
* **Task Breakdown:**
  1. Implement `@mcp.tool() research(file_path: str, query: str = "") -> str` (titled `"JITC Research tool"`) in `AcmeLab/src/clara_dna_mcp_server.py`. Returns cached conductor patch blueprints, AST anchors, and semantic summaries dynamically.
  2. Implement `@mcp.tool() failure_whisperer(test_output: str, error_context: str = "") -> str` in `clara_dna_mcp_server.py`. Passes failing traceback to local fast lane / M5 TurboQuant proxy for atomic 2-line root-cause diagnosis.
  3. Implement `@mcp.tool() handoff_checkpoint(status: str, summary: str, artifacts_modified: list) -> dict` in `clara_dna_mcp_server.py`. Appends structured execution reflection to `Portfolio_Dev/field_notes/data/delegation_ledger.jsonl` and signals clean task completion.
  4. Refactor and rename `locate_grounding` $\to$ `locate_path(pattern: str, intent_description: str = "") -> dict` with clear docstring as the fast submodule file locator and import resolver.
  5. Wire `delegate.py` to write conductor ($L_2$) patch blueprints and AST anchors into `/tmp/clara_conductor_notes.json`.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `AcmeLab/src/clara_dna_mcp_server.py`, `HomeLabAI/src/tests/delegate.py`.
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_jitc_research_mcp.py -v`
  * **Anchor 3 (Live Silicon Invariant):** Subversive tool suite responses return in $<20\text{ms}$ on port 8001; zero disk re-indexing.
  * **Anchor 4 (DNA Links):** `[FEAT-647]`, `[INS-044]`, `[DISC-012]`.

---

### 🎭 Story 98.2: Empirical Trust Gradient & Subversive $L_3$ Prompt Calibration
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Feature Anchor:** `[DISC-012]`
* **Status:** **PENDING EXECUTION**
* **Why & Root Cause:** Asserting "grounding was already completed" triggers model skepticism and exploration. $L_3$ needs a prompt framing it as the lead investigator executing `research()`.
* **Task Breakdown:**
  1. Remove all *"grounding was already completed"* prose from `oh-my-openagent.json` and `delegate.py`.
  2. Implement the Subversive Tier-1 Role Prompt: *"You are the primary implementation engineer for `<file>`. Call `research('<file>')` to retrieve the target AST blueprint and patch directives, apply edits via `clara-dna_safe_patch`, and run pytest. If tests fail, run `failure_whisperer(traceback)`. On pass, call `handoff_checkpoint()`."*
  3. Run empirical trust gradient battery testing 3 prompt variants (Naive $\to$ Forceful $\to$ Subversive) and log turn metrics.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `oh-my-openagent.json`, `HomeLabAI/src/tests/delegate.py`.
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_subversive_prompt.py -v`
  * **Anchor 3 (Live Silicon Invariant):** $L_3$ emits `research` on Turn 1 on 100% of test runs; zero `grep`/`read` calls.
  * **Anchor 4 (DNA Links):** `[DISC-012]`, `[INS-044]`, `[BKM-049]`.

---

### ⚡ Story 98.3: Pre-Warmed Worker Session Resumption & Tool Blocking
* **Assigned Owner:** `[SWARM:CLOUD]`
* **Feature Anchor:** `[FEAT-648]`
* **Status:** **PENDING EXECUTION**
* **Why & Root Cause:** Starting fresh OpenCode sessions incurs a 5-10s cold-start penalty and loses KV cache headroom on M5 Air.
* **Task Breakdown:**
  1. Wire `context_prewarmer.py` / `delegate.py` to maintain warm worker session IDs across adjacent stories.
  2. Implement session resumption via `POST /session/{id}/message` rather than creating redundant sessions.
  3. Verify that warm sessions retain KV cache on M5 Air port 8002 without Metal memory growth.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `HomeLabAI/src/v5/cognition/context_prewarmer.py`, `HomeLabAI/src/tests/delegate.py`.
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_session_resumption.py -v`
  * **Anchor 3 (Live Silicon Invariant):** Session resumption latency $<500\text{ms}$; zero KV cache thrashing on M5 Air port 8002.
  * **Anchor 4 (DNA Links):** `[FEAT-648]`, `[BKM-047]`, `[LAB-019]`.

---

### 🧪 Story 98.4: Zero-Wandering Local Swarm Certification on 4090 + M5 Air
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Feature Anchor:** `[BKM-072]`
* **Status:** **PENDING EXECUTION**
* **Why & Root Cause:** Certify the entire end-to-end bicameral pipeline on real silicon with zero primary-agent intervention.
* **Task Breakdown:**
  1. Dispatch live coding tasks across 3 test modules using `delegate.py --local-only`.
  2. Assert $L_2$ Conductor (4090) generates AST plan $\to$ $L_3$ Worker (M5 Air) calls `research` $\to$ applies `clara-dna_safe_patch` $\to$ verifies via `failure_whisperer` if needed $\to$ exits via `handoff_checkpoint`.
  3. Validate full autonomy, $\le 3$ turns, and $<60\text{s}$ wall-clock duration per story.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `HomeLabAI/src/tests/delegate.py`, `Portfolio_Dev/field_notes/data/delegation_ledger.jsonl`.
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_subversive_swarm_e2e.py -v`
  * **Anchor 3 (Live Silicon Invariant):** 100% of local stories pass self-verification without fallback to `[AGY:TAKEOVER]`.
  * **Anchor 4 (DNA Links):** `[BKM-072]`, `[INS-044]`, `[DISC-012]`, `[BKM-049]`.
