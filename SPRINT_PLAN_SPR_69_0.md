# 🚀 SPRINT PLAN 69.0: Local Bicameral Delegation Certification & Layered Swarm Validation

**Sprint ID:** `SPR_69_0`  
**Theme:** Sovereign Local Swarm Delegation Architecture (AGY $\rightarrow$ RTX 4090 Atlas $\rightarrow$ M5 Air Junior)  
**Status:** ACTIVE / IN PROGRESS  
**Parent Framework:** BKM-034 (Swarm Delegation), BKM-043 (4-Anchor Standard), BKM-047 (Local Silicon Memory Ceilings)  
**Certified KENDER Model:** `hf.co/unsloth/Qwen3-14B-GGUF:UD-Q4_K_XL` (9.16 GB, Verified Native Tool Calling)  

---

## 🧭 Executive Summary & Architecture

### The Hardware Reality & Topology Alignment
* **Node Kender (Windows RTX 4090 / Ollama):** Assigned as **Layer 2 (Atlas - Orchestrator)**. Ollama's flexible context management with graceful Host System RAM overflow makes it ideal for ingesting broad sprint documents, global project state, and task sequencing without choking on context boundaries.
  * **Model:** `hf.co/unsloth/Qwen3-14B-GGUF:UD-Q4_K_XL` (Unsloth Dynamic Q4_K_XL preserves critical attention and down-projection weights at higher precision while keeping 4-bit average size).
  * **Empirical Proof (2026-09-01):** Verified live against `192.168.1.26:11434/v1/chat/completions` emitting native `tool_calls` for `task(subagent_type="sisyphus-junior", prompt="...")`.
* **Node Brain (Apple M5 Air 32GB / oMLX with dflash):** Assigned as **Layer 3 (Sisyphus-Junior - Ground Execution Worker)** and **Deep Thought Primary**. With strict 16-bit KV cache constraints, M5 Air is protected from memory blowouts by receiving only isolated, bounded Stub-and-Fill contracts ($< 2\text{k}$ tokens), executing blazing-fast surgical code patches.
* **Strategic Guardian (AGY / Gemini):** Operates as **Layer 1**, authoring Interface-First Contracts, defining the Stub-and-Fill bounding boxes, and managing git commits.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ 🔮 LAYER 1: STRATEGIC GUARDIAN (AGY / Gemini)                                   │
│ • Static Rules: Enforce strict output schemas and immutable API boundaries.     │
│ • Dynamic Ingestion: High-level system requirements & finalized design specs.   │
│ • Downstream Hand-off: Discrete Interface-First Contracts & story bounds.       │
│ • Backpressure: Ingests blockers; amends specs rather than letting agents guess.│
└──────────────────────────────────────┬──────────────────────────────────────────┘
                                       │ (REST Port 4097 / delegate.py)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│ 🗺️ LAYER 2: BROAD ORCHESTRATOR (Atlas on Windows RTX 4090 / Ollama)             │
│ • Model: hf.co/unsloth/Qwen3-14B-GGUF:UD-Q4_K_XL                                │
│ • Static Rules: Pure routing, state tracking, and dispatch (NO CODE WRITING).   │
│ • Dynamic Ingestion: Full AGY sprint docs, global state, task sequencing.       │
│ • Downstream Hand-off: Passes isolated story blocks & target stubs to Junior.   │
│ • Backpressure: Relays Junior blockers upward to AGY without local mutation.    │
└──────────────────────────────────────┬──────────────────────────────────────────┘
                                       │ (task() Subagent Dispatch)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│ 🛠️ LAYER 3: FAST SURGICAL WORKER (Sisyphus-Junior on Apple M5 Air / oMLX dflash) │
│ • Model: mlx-community--Qwen3.8-27B-4bit / Qwen2.5-Coder-14B-4bit               │
│ • Static Rules: Anti-exploratory ("Research done; write only inside stub").     │
│ • Dynamic Ingestion: Active isolated file stubs & direct contract payloads.     │
│ • Execution: clara-dna_safe_patch + pytest execution within strict KV limits.   │
│ • Backpressure: Halts on missing types/context pressure; reports upward.        │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔀 The 3-Tier Task Routing Strategy & Fallback Hierarchy

To eliminate single-point-of-failure risks in OmO's subagent routing engine, we enforce a strict 3-tier dispatch ladder:

| Tier | Mechanism | Trigger Condition | Implementation |
| :--- | :--- | :--- | :--- |
| **Tier 1 (Primary)** | **Single-Parameter `subagent_type`** | Default for Atlas dispatches. | `task(subagent_type="sisyphus-junior", prompt="...")`<br>Resolves strictly via `agents["sisyphus-junior"]` $\rightarrow$ M5 Air MLX. Single-parameter invocation prevents schema parameter overlap conflicts. |
| **Tier 2 (Fallback)** | **Category-Only Dispatch** | Triggered if `subagent_type` fails to invoke or emits schema rejection. | `task(category="deep", prompt="...")`<br>Resolves strictly via `categories["deep"]` $\rightarrow$ M5 Air MLX. |
| **Tier 3 (Resilience)** | **Orchestrator Two-Step Cascade** | Triggered if OpenCode internal subagent execution deadlocks or hangs. | `delegate.py` executes a two-phase command sequence:<br>1. `--agent atlas --mode plan` (4090 generates contract)<br>2. `--agent sisyphus-junior --mode execute` (M5 Air executes patch). |

---

## 🔍 The Key Chokepoint Check (KENDER $\rightarrow$ M5 Air $\rightarrow$ KENDER Round-Trip)

To certify the delegation pipeline, Story 69.4 must pass the **4-Point Round-Trip Chokepoint Gate**:

```
[Point 1: Emission]        Atlas (4090) emits valid task(subagent_type="sisyphus-junior", prompt="...")
                                  │
                                  ▼
[Point 2: Target Binding]  OpenCode REST logs child runner starting on provider "my-m5-mlx" (M5 Air)
                                  │
                                  ▼
[Point 3: Return Value]    M5 Air executes safe_patch + pytest, returning completion string to Atlas
                                  │
                                  ▼
[Point 4: Atlas Synthesis] Atlas ingests return chunk and outputs final [HANDOVER REFLECTION] to REST log
```

---

## 🔁 The Closed-Loop Iteration & Remediation Plan

If a delegated execution fails, drifts, or encounters a blocker, we execute this automated recovery loop:

```
                  ┌───────────────────────────────┐
                  │ 1. Dispatch Canary to Atlas   │
                  │    (REST Port 4097)           │
                  └───────────────┬───────────────┘
                                  │
                                  ▼
                  ┌───────────────────────────────┐
                  │ 2. Atlas Spawns Junior        │
                  │    via task() on M5 Air       │
                  └───────────────┬───────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                           ▼
          [Success / Done]            [Error / Drift / Blocker]
                    │                           │
                    ▼                           ▼
        ┌───────────────────────┐   ┌───────────────────────────────────┐
        │ 3. Automated Check:   │   │ 4. Remediation Loop:              │
        │ • Target mtime diff   │   │ • Loop A: In-Session Re-fire with │
        │ • pytest execution    │   │   exact pytest/compiler trace     │
        │ • Telemetry capture   │   │ • Loop B: Tighten Junior stub     │
        └───────────┬───────────┘   │ • Loop C: Escalate Blocker to AGY │
                    │               └─────────────────┬─────────────────┘
                    ▼                                 │
        ┌───────────────────────┐                     │
        │ 5. Certify & Commit   │◄────────────────────┘ (Max 2 Iterations)
        └───────────────────────┘
```

* **Loop A (Fast In-Session Remediation):** If `pytest` fails on syntax or logic error, re-fire into the **same session** (`--session-id sprint-69-canary`) passing the exact pytest traceback without restarting the daemon.
* **Loop B (Anti-Drift Tightening):** If Junior attempts directory exploration instead of file editing, re-fire with an explicit diff snippet and hard file path anchor.
* **Loop C (Blocker Escalation):** If Junior emits `[BLOCKER REPORT: ...]`, Atlas and `delegate.py` bubble the blocker directly to the terminal for AGY contract amendment.

---

## 🔄 Recommended Step-by-Step Execution Sequence

```
  Step 1: Base Configuration Binding (Infrastructure, OpenCode Provider, Live Test)
     ↓
  Step 2: Topology Inversion & Task Schema Lockdown (Atlas 4090, Junior M5, Categories)
     ↓
  Step 3: Anti-Exploratory & Blocker Protocol (Junior Prompts + Regex Ingestion)
     ↓
  Step 4: Live Canary Gauntlet with Chokepoint & Iteration Gate (AGY → 4090 → M5 Air)
     ↓
  Step 5: Documentation & BKM-047 Authoring (Handover Playbook + Protocols.md)
```

---

## 📋 Stories Breakdown

### 🔬 Story 69.1: Model Cartography & Tool-Call Certification (`[FEAT-510]`)
* **Status:** **COMPLETE / CERTIFIED (2026-09-01)**
* **Findings:** `hf.co/unsloth/Qwen3-14B-GGUF:UD-Q4_K_XL` (9.16 GB) pulled and tested on KENDER. Redundant models purged. Verified native tool calling and `test_integration_kender.py` passed.

### 🛡️ Story 69.2: Topology Inversion & Anti-Exploratory Hardening (`[FEAT-511]`)
* **Status:** **COMPLETE / CERTIFIED (2026-09-01)**
* **Delivered Artifacts:**
  1. `opencode.json`: Registered `hf.co/unsloth/Qwen3-14B-GGUF:UD-Q4_K_XL` under `my-windows-4090`.
  2. `oh-my-openagent.json`: Inverted topology (`atlas` $\rightarrow$ 4090, `sisyphus-junior` $\rightarrow$ M5 Air). Rewired all categories (`deep`, `quick`, etc.) to `my-m5-mlx/mlx-community--Qwen3.8-27B-4bit` with local fallback to 4090.
  3. `infrastructure.json`: Inverted `swarm_aliases.local_bicameral` bindings (architect=4090, coder=M5 Air).
  4. `delegate.py`: Hardened mandate blocks to enforce `task(category="deep", prompt="...")` for deterministic subagent spawning without hallucinated parameters.

### 🔄 Story 69.3: Discrete Two-Way Backpressure & Blocker Escalation Protocol (`[FEAT-512]`)
* **Status:** **COMPLETE / CERTIFIED (2026-09-01)**
* **Delivered Artifacts:**
  1. `oh-my-openagent.json`: Hardened Junior system prompt with anti-exploratory rules and mandated `[BLOCKER REPORT: <CATEGORY>]` format.
  2. `delegate.py`: Added regex parsing for `[BLOCKER REPORT]` with critical log bubbling and automated ICM store triggers.
  3. `delegate.py`: **Smart Heartbeat Polling & Live Telemetry Tap** — Replaced passive 5s sleep with non-blocking `/session/:id/message` inspection, providing real-time state transition alerts (`LIVE_SWARM_STATE`) and instant fast-fail aborts upon encountering interactive `question` popups or quota traps. (Architectural analysis documented in `report_event_stream_vs_smart_polling.md`).

### 🧪 Story 69.4: End-to-End Live Local Delegation Validation Gauntlet (`[FEAT-513]`)
* **Status:** **COMPLETE / CERTIFIED (2026-09-01)**
* **Target Files:** `HomeLabAI/src/tests/test_delegation_canary.py`.
* **Validation & Chokepoint Criteria:**
  1. Dispatch `--agent atlas --local-only` to implement a controlled function stub.
  2. **Chokepoint Gate:** Atlas (4090) emitted `task(category="deep")`, M5 Air executed `compute_xor_checksum` stub fill, and `pytest` passed 3/3 test cases in 0.11s.
  3. **Identified Forensics:** Subagent ended turn invoking interactive `question` (Next Steps) popup rather than returning final text, causing `finish=unknown` and bypassing textual handover reflection.

### 🛡️ Story 69.6: Delegation Harness Resilience & Interactive Escalation Gate (`[FEAT-515]`)
* **Status:** **ACTIVE / PENDING IMPLEMENTATION**
* **Core Law:** *Fix the delegation infrastructure; do not manually finish the sprint.*
* **Tasks:**
  1. **Task 69.6.1 (Interactive Popup Breakout & Resumption):**
     - Modify `delegate.py` to intercept `waiting_for_input` / `question` tool calls immediately.
     - Extract question headers and numbered options, print clear instructions to the CLI, and exit cleanly with status code `2` (`AWAITING_INPUT`).
     - Implement `--resume <session_id> --answer <choice>` in `delegate.py` to seamlessly resume paused sessions via REST `POST /session/<id>/prompt`.
  2. **Task 69.6.2 (Silent Failure & Escalation Gate):**
     - Treat `finish=unknown` and empty text chunks as critical delegation harness failures.
     - Add `[ALERT: SILENT_DELEGATION_FAILURE]` telemetry and log unhandled session states to `HomeLabAI/logs/delegation_failures.log`.
     - Halt automated sprint progression when a delegation failure occurs so the harness can be diagnosed.
  3. **Task 69.6.3 (Dual-Mode Category Matrix Alignment):**
     - Wire `unspecified-low` to `my-m5-mlx` (M5 Air) with 4090 fallback for tightly bounded local bicameral execution.
     - Restore `deep`, `ultrabrain`, and `quick` in `oh-my-openagent.json` to cloud fallback ladders (DeepSeek-V4, Groq 70B, Cohere) for cloud strategic runs.
     - Update `delegate.py` prompt templates to use `unspecified-low` for `--local-only` and `deep` for cloud dispatches.
  4. **Task 69.6.4 (4-Pillars Executable Prompt Engineering):**
     - Embed the 4 Cardinal Pillars (`[STATIC RULES]`, `[DYNAMIC INGESTION]`, `[DOWNSTREAM HAND-OFF]`, `[BACKPRESSURE PROTOCOL]`) directly into `delegate.py` prompt templates for Atlas (L2) and Sisyphus/Junior (L3).

### 🔬 Story 69.7: Layered Context Shake-Down & Multi-Task Chain Validation (`[FEAT-516]`)
* **Status:** **PENDING Story 69.6**
* **Objective:** Certify cloud-scale fidelity on local silicon by stress-testing hierarchical context layering across multi-task story chains.
* **Tasks:**
  1. **Task 69.7.1 (Cloud Mode Co-Existence Shake-Down):**
     - Dispatch a strategic story using `--agent sisyphus` (verifying routing to Cloud DeepSeek/Groq via `deep` with working fallbacks).
  2. **Task 69.7.2 (Multi-Task Step Sequence Shake-Down):**
     - Decompose a real story into a 2-task micro-chain inside a single persistent session (`--session-id sprint-69-chain`):
       - *Task A (Contract & Signature):* Generate module interface and docstring anchors.
       - *Task B (Implementation & Verification):* Ingest Task A's output, implement logic, and verify with pytest.
     - Verify that context stays strictly $< 2\text{k}$ tokens per step and never trips M5 Air Metal memory ceilings.

### 📖 Story 69.5: Documentation Alignment & Tri-Loop Feedback Engine Authoring (`[FEAT-514]`)
* **Status:** **IN PROGRESS**
* **Target Files:** `Portfolio_Dev/OPENAGENT_HANDOVER_PLAYBOOK.md`, `HomeLabAI/docs/forensics/OPENAGENT_CONFIG_MAP.md`, `HomeLabAI/docs/Protocols.md`.
* **Tasks:**
  1. Update Handover Playbook and Config Map matrices (Scar #7 documented).
  2. Author `BKM-047: Local Silicon Memory Ceilings & Bicameral Swarm Topology` in `Protocols.md`.
  3. Expand `BKM-034` Section 4 into the **Tri-Loop Feedback & Remediation Engine** (Loop A: Fast In-Session Re-fire, Loop B: Anti-Drift Stub Tightening, Loop C: Blocker/Harness Escalation).
  4. Verified `BKM-048` (JIT Context Interleaving & Cloud-Scale Fidelity MO).

