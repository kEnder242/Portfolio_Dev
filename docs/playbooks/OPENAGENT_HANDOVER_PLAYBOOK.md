# 📖 OpenAgent Handover & Co-Pilot Playbook

This playbook serves as the definitive reference guide for task allocation, model grounding, session management, and verification when coordinating between **Antigravity (AGY)** (Gemini-driven strategic co-pilot) and **OpenAgent** (autonomous coding swarm attached to port 4096).

---

## 0. Playbook Quick-Diagnostic Index & Routing Table

> [!IMPORTANT]
> **MANDATORY FULL-SYSTEM INTER-RETRY AUDIT (BKM-049 Step 4):**  
> Before formulating any diagnostic fix, retry prompt, or swarm escalation, the primary orchestrator (AGY) MUST perform a **comprehensive comparative audit**:
> 1. Audit this Playbook Index table (§0, lines 1–60) to match observed symptoms directly to authoritative rules.
> 2. Audit delegation code ([`delegate.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/tests/delegate.py)) vs active configuration files (`~/.config/opencode/oh-my-openagent.json`, `opencode.json`).
> 3. Audit target files, prompt anchors, and runtime environment (inference endpoints, socket states, service health) to eliminate discrepancies before re-dispatching.

| # | Playbook Section | Core Invariants & Rules | When to Consult (Diagnostic Symptoms) |
| :- | :--- | :--- | :--- |
| **§1** | [Model Allocation & Swarm Topology](#1-model-allocation--swarm-topology) | • Kender 4090: `Qwen3.8-27B`<br>• M5 Air MLX: `Ternary-Bonsai-2-27B`<br>• Cloud Tier: OpenRouter / OpenCode Free / Cohere 256k | Model selection, capacity bounds, local vs cloud routing |
| **§2** | [Session Lifecycle & Webview Visibility](#2-session-lifecycle--webview-visibility-bkm-034-point-12) | • Port 4097 REST API / Port 4096 Web UI<br>• `edit` is DENIED; `clara-dna_safe_patch` is MANDATORY<br>• Single-tenant zombie session nuke (`BKM-034`) | UI disconnects, 4097 port hangs, agent attempting forbidden `edit` tool |
| **§3** | [Context & Token Optimization](#3-context--token-optimization) | • Narrow `--dir` sub-project scoping<br>• Anti-Google-Starvation law (No Gemini in OpenAgent)<br>• Port 8002 Headroom Proxy KV compression (`BKM-047`)<br>• Subagent tool denial law (`BKM-051`) | Metal memory overflow (24GB cap), prompt token bloat (>2k tokens), KV cache thrashing |
| **§4** | [Swarm & Configuration Map](#4-swarm--configuration-map) | • Configuration Symlink Law (`~/.config/opencode/`)<br>• Dynamic Category Taxonomy (7 categories)<br>• Layer 3 Terminal Execution Law (`task: deny`) | Category routing errors, subagents failing to resolve model, nested delegation loops |
| **§5** | [Safety Gates & Troubleshooting Ledger](#5-safety-gates--troubleshooting-ledger) | • Mandatory Pre-Delegation Audit (`FEAT-477`)<br>• Git Ownership Gate (Workers never commit)<br>• Anti-Looping circuit breaker (`BKM-038`) | Verification failures, loop detection, uncommitted git drift |
| **§6** | [The Agent Cascade Architecture](#6-the-agent-cascade-architecture-context-isolated-swarms) | • 3-Tier Swarm Hierarchy (AGY $\rightarrow$ Atlas $\rightarrow$ Junior/Hephaestus)<br>• **Permission Matrix:** Atlas (`task`), Junior (`safe_patch`), Hephaestus (`write`, `safe_patch`) | Subagent tool permission rejections, Atlas attempting writes, Junior attempting bash |
| **§7** | [Operational Calibration Ledger](#7-operational-fix--calibration-ledger-bkm-049-tri-loop-inter-attempt-log) | • Historical root causes & verified calibrations across sprints | Repeated operational anomalies, historical regressions |

---

## 1. Model Allocation & Swarm Topology

Tasks are allocated based on engine roles to minimize API costs, prevent rate-limiting, and ensure high-fidelity coding execution:

| Role / Engine | Primary Function | Invocation Command Pattern |
| :--- | :--- | :--- |
| **Strategic Guardian (AGY)** | Master plan creation, architecture design, code review, git commits | AGY CLI Turn |
| **Sisyphus (Ultraworker & Autonomous Engineer)** | Primary Direct Autonomous Implementer for `delegate.py` story dispatches; directly executes safe_patch/bash | Dispatched via `delegate.py` (default) |
| **Atlas (Plan Executor & Swarm Conductor)** | Swarm orchestrator for multi-subagent task cascades (Windows 4090 / M5 Air) | Dispatched via `delegate.py --agent atlas` |
| **Prometheus (Planner & Diagnostic Investigator)** | Read-only strategic planner, pre-flight context auditor, diagnostic investigator | Dispatched via `delegate.py --mode plan/investigate` |
| **Primary Local Conductor & Verifier (KENDER)** | Node KENDER / Windows 4090 (Port 11434 Ollama: `hf.co/unsloth/Qwen3.8-27B-GGUF:UD-Q3_K_XL`) for 128k context architecture and verification | Subagent `task()` primary target (`atlas`, `librarian`, `momus`) |
| **Primary Local Reasoning Node (M5 Air)** | Mac M5 Air (Port 8002 Headroom Proxy → Port 8000 oMLX: `TokenAI-zer--Ternary-Bonsai-2-27B-MLX-oQ2-mtp`) for 128k context bounded surgical patching & greenfield | Subagent target for surgical edits (`sisyphus-junior`, `hephaestus`) |
| **Cloud Fallback Tier** | OpenCode (`opencode/big-pickle`) $\rightarrow$ OpenRouter Free (`openrouter/openrouter/free`) | Automatic runtime fallback (Zero Google, Zero Cohere) |

---

## 2. Session Lifecycle & Webview Visibility (BKM-034 Point 12)

### 2.1 Mandatory Shell Execution (Port 4096)
All tactical developer tasks delegated to OpenAgent must be launched via `delegate.py` attached to port 4096:
```bash
python3 HomeLabAI/src/tests/delegate.py --sprint XX --story YY --title "<Title>" --reference "<plan>" --target "<file>" --details "<specs>" --mode execute
```
> [!IMPORTANT]
> Never use internal `invoke_subagent` for developer/implementation tasks. `invoke_subagent` is strictly reserved for read-only research tasks. Attaching to port 4096 ensures all active worker sessions render live on the local TUI and webview dashboard at `http://192.168.1.238:4096/`.

### 2.2 Tooling Mandate: `clara-dna_safe_patch` vs. Hobbled `edit`
- **The Built-In `edit` Tool is Denied:** The native `edit` tool requires 100% exact character/whitespace matching and repeatedly fails on indentation drift. It has been hobbled via `"permission": { "edit": "deny" }` and `"disabled_tools": ["edit"]`.
- **Mandatory `safe_patch`:** All agents must use `clara-dna_safe_patch` with parameters `{ file_path, old_pattern, new_pattern, multi }`.
- **Emergency Fallback:** If `safe_patch` fails, agents use targeted `bash` scripts (Python/sed) or halt and surface the patch failure to the orchestrator rather than looping.

### 2.3 Socket-Activated Daemon Warm-Up
The OmO web UI proxy (`opencode-proxy.service`) is socket-activated via `opencode.socket` on `0.0.0.0:4096` with `StopWhenUnneeded=true`. Before launching any session, `delegate.py` calls `wake_web_ui()` which HTTP-GETs `http://127.0.0.1:4096/` — this TCP connect triggers the `opencode.socket` → `opencode-proxy.service` → `codex:4097` activation chain.

**Port separation:**
- `4097` = `codex serve` REST API (system-level service, always running). Used for session creation and message dispatch.
- `4096` = Web UI proxy (user-level, socket-activated, idle-stops after 5min). Required for browser access at `http://192.168.1.238:4096/`.

### 2.4 Unconditional Zombie Session Nuke & Single-Tenant Lifecycle ([BKM-034])
- **The Orphanage Failure Mode:** When `delegate.py` timed out or exited during offline silicon intervals, the background OpenCode daemon (`:4097`) retained in-flight child subagent sessions (`Sisyphus-Junior`, `explore`). These orphaned workers continued background polling loops against Node KENDER and Node Brain, keeping Ollama VRAM timers alive indefinitely.
- **The Sovereign Single-Tenant Nuke Policy:** Because the Federated Lab is a single-tenant environment, `delegate.py` enforces an unconditional total nuke across port 4097:
  1. **Pre-Flight Sweep:** Before creating any new dispatch session, `delegate.py` queries `GET /session` and issues `POST /session/<id>/abort` to all active sessions on the server.
  2. **Termination & Exit Nuke:** On any script exit, `SIGINT`, `SIGTERM`, error, or timeout, `_cleanup_active_session()` triggers `_nuke_all_sessions()`, ensuring all parent and child subagents are terminated immediately.

---

## 3. Context & Token Optimization

### 3.1 Narrow Workspace Scoping
- **The Rule:** Always set `--dir` to the narrowest sub-project directory (e.g. `--dir /home/jallred/Dev_Lab/HomeLabAI`).
- **The Pitfall:** Initializing OpenAgent at the parent root (`/home/jallred/Dev_Lab`) causes the server to index both sub-repositories, compiling large baseline token payloads on turn 1.
- **On-Demand Cross-Repo References:** Use `--reference` and `--target` args in `delegate.py` to pass specific file paths on-demand without indexing unneeded workspace trees.

### 3.2 Vector DNA Grounding (Port 8001)
- Instead of injecting full markdown files (`FeatureTracker.md` or `Protocols.md`) into prompt text, BKM and FEAT context is retrieved dynamically from ChromaDB vector collections (`behavioral_dna`, `feature_dna`) running on port 8001.

### 3.3 The Anti-Starvation Rule (Zero Google Gemini in OpenAgent)
- When AGY (Gemini Strategic Guardian) exhausts its API token quota, Google APIs are rate-limited for both systems.
- Therefore, **Google Gemini models are strictly prohibited from OpenAgent fallback chains**.
- OpenAgent fallbacks must route strictly through **OpenRouter Free $\rightarrow$ OpenCode Free $\rightarrow$ Cohere/Mistral $\rightarrow$ M5 Air MLX $\rightarrow$ Windows 4090**.

### 3.4 Local Silicon Token Overhead & Metal Memory Ceilings (Port 8002 Proxy)
- **The Physical Memory Constraint (24GB Apple Silicon):** Running `Qwen3.8-27B` (15.5 GB resident weights) without KV compression risks breaching macOS Metal's 24.46 GB wired allocation cap (`iogpu.wired_limit_mb`).
- **Mandatory Port 8002 Headroom Proxy:** All M5 Air inference requests MUST target `http://192.168.1.46:8002/v1` (never raw `:8000`) to dynamically compress KV cache and protect Metal prefill limits.
- **Context Configuration on Kender 4090:** Windows 4090 uses `qwen3:14b` with pinned 64k context in Ollama (`num_ctx 65536`), reserving VRAM for zero-thrash KV caching at 88 tok/s.

### 3.5 Subagent Tool Scoping & The ICM Ballast Tax ([BKM-051])
- **The 24.5k Token Ghost:** OpenCode automatically injects all registered MCP tool schemas into every subagent prompt, inflating baseline context to 24.5k tokens before reading code.
- **The Mandatory Tool Denial Law:** Execution workers (`atlas`, `sisyphus-junior`, `hephaestus`, `librarian`, `momus`, `daedalus`) MUST explicitly deny non-essential tools in `oh-my-openagent.json`:
  ```json
  "permission": {
    "edit": "allow",
    "icm_*": "deny",
    "websearch_*": "deny",
    "codegraph_*": "deny",
    "question": "deny"
  }
  ```
- **Resident Ambient Memory Micro-Bridge (FEAT-600 / LAB-019):** Programmatic dispatches via `delegate.py` query the resident `/ambient_recall` endpoint on Foyer (:8765) in <5ms, dynamically prepending relevant BKM protocols and FEAT anchors into Tier 2 dispatch payloads for cloud workers, while bypassing local-only leaf workers to preserve M5 Air / RTX 4090 prefill headroom.

---

## 4. Swarm & Configuration Map

### 4.1 Configuration Files & Symlink Invariant
- **Symlink Law:** OpenCode reads global configurations from `~/.config/opencode/`. Both configuration files MUST be symlinked to the version-controlled workspace repository:
  * `~/.config/opencode/opencode.json` $\rightarrow$ `/home/jallred/Dev_Lab/opencode.json`
  * `~/.config/opencode/oh-my-openagent.json` $\rightarrow$ `/home/jallred/Dev_Lab/oh-my-openagent.json`
- **MCP Absolute Path Rule:** Systemd user services (`opencode-core.service`) use default system `PATH` (`/usr/bin:/bin`). Commands in `opencode.json` (such as `icm`) MUST use absolute paths (`/home/jallred/.local/bin/icm`) to prevent silent `execvp` failures.
- **MCP Tool Bridge:** `HomeLabAI/.opencode.json` (OpenAgent) & `~/.gemini/config/mcp_config.json` (AGY)
- **Delegation Harness:** `HomeLabAI/src/tests/delegate.py`

### 4.2 Engine Hardware & Role Mapping Matrix

| Role | Hardware / Binding | Context Limit | Primary Purpose | Fallback Route |
| :--- | :--- | :--- | :--- | :--- |
| **Sisyphus (Lead)** | OpenCode Free (`opencode/big-pickle`) | 256K | Direct code edits, surgical refactoring | OpenRouter Free $\rightarrow$ Cohere $\rightarrow$ M5 MLX $\rightarrow$ 4090 |
| **Atlas / Prometheus** | OpenCode Free (`opencode/big-pickle`) | 256K | Swarm conduction, architectural planning | OpenRouter Free $\rightarrow$ Cohere $\rightarrow$ M5 MLX $\rightarrow$ 4090 |
| **Mac M5 Air (MLX)** | Node Brain / Mac M5 (Port 8002 Headroom $\rightarrow$ Port 8000 oMLX: `TokenAI-zer--Ternary-Bonsai-2-27B-MLX-oQ2-mtp`) | 128K / 8K out | Surgical patching (`sisyphus-junior`) & greenfield (`hephaestus`) | Windows 4090 (`Qwen3.8-27B`) |
| **Windows 4090 (Ollama)** | Node KENDER / Windows 4090 (Port 11434: `hf.co/unsloth/Qwen3.8-27B-GGUF:UD-Q3_K_XL`) | 128K | Conductor (`atlas`), Scout (`librarian`), Verifier (`momus`) | Cloud Free Tier |
| **Cloud Resiliency Tier** | Cohere (`command-a-plus-05-2026`) | 256K | Complex refactoring, emergency cloud fallback | M5 MLX / Windows 4090 |

### 4.3 Dynamic Category Taxonomy (Web GUI vs. Headless Dispatch)

When driving tasks interactively from the **Web GUI** (`http://192.168.1.238:4096/`), agents like Sisyphus decompose tasks and spawn background subagents via `task(category="...")`. In contrast to direct `delegate.py` dispatches (which bind to an agent identity), subagents resolve their model bindings strictly from the **`categories`** block in `oh-my-openagent.json`:

| Category | Typical Subagent Tasks | Primary Model Binding | Fallback Chain |
| :--- | :--- | :--- | :--- |
| **`coder`** | Surgical leaf patches, code editing | `my-m5-mlx/TokenAI-zer--Ternary-Bonsai-2-27B-MLX-oQ2-mtp` | OpenRouter Free $\rightarrow$ Cohere North $\rightarrow$ 4090 |
| **`ultrabrain`** | Deep architecture derivation, multi-file refactoring | `openrouter/free` (Meta-Router) | Cohere $\rightarrow$ OpenCode Big-Pickle $\rightarrow$ M5 MLX |
| **`deep`** | Complex local implementation, heavy coding | `openrouter/free` (Meta-Router) | Cohere $\rightarrow$ OpenCode Big-Pickle $\rightarrow$ Windows 4090 |
| **`writing`** | Documentation, docstrings, summaries, sprint logs | `my-m5-mlx/TokenAI-zer--Ternary-Bonsai-2-27B-MLX-oQ2-mtp` | OpenRouter Free $\rightarrow$ Windows 4090 |
| **`visual-engineering`** | Frontend HTML/CSS layout, UI rendering | `my-m5-mlx/TokenAI-zer--Ternary-Bonsai-2-27B-MLX-oQ2-mtp` | Windows 4090 |
| **`unspecified-high`** | General high-complexity fallback | `openrouter/free` (Meta-Router) | Cohere $\rightarrow$ OpenCode Big-Pickle $\rightarrow$ 4090 |
| **`unspecified-low`** | Verification and diagnostic helper tasks | `my-windows-4090/hf.co/unsloth/Qwen3.8-27B-GGUF:UD-Q3_K_XL` | M5 MLX |

### 4.4 The Layer 3 Terminal Execution Law ([BKM-049])
- **Terminal Execution Tier:** Layer 3 leaf workers (`sisyphus-junior`, `daedalus`, `hephaestus`, `momus`, `librarian`) represent the final execution tier of the swarm hierarchy.
- **Strict `task: deny` Tool Invariant:** All Layer 3 worker definitions in `oh-my-openagent.json` MUST enforce `"task": "deny"`. Layer 3 workers are strictly forbidden from spawning additional subagents or recursing down further delegation loops.
- **Direct Action Obligation:** Leaf workers receive bounded, spoon-fed 4-anchor instructions from Layer 2 (Atlas) and must apply atomic file edits directly via `clara-dna_safe_patch` and `write` without re-delegating.

> [!WARNING]
> If a category (such as `writing` or `unspecified-low`) is omitted from `oh-my-openagent.json`, `oh-my-openagent` falls back to its upstream hardcoded default (often Claude Opus or OpenRouter paid tier). This bypasses the free ladder and triggers immediate provider authorization or rate-limit failures. All 7 categories must remain explicitly mapped in `oh-my-openagent.json`.

---

## 5. Safety Gates & Troubleshooting Ledger

> [!IMPORTANT]
> **MANDATORY PRE-EXECUTION & PRE-REPAIR DELEGATION AUDIT (BKM-049 / FEAT-477):**  
> Before authorizing, diagnosing, or executing any fix-repair step in the Tri-Loop, the orchestrating agent MUST perform a live ledger audit across three anchors:
> 1. **Active Playbook Invariants:** Review Sections 1–4 of this document (Topology, Tool Ballast [BKM-051], Metal Headroom [BKM-047], Category Registry).
> 2. **Latest Retrospective Ledger:** Inspect [`DELEGATION_RETROSPECTIVE.md`](file:///home/jallred/Dev_Lab/DELEGATION_RETROSPECTIVE.md) (synthesized via `delegate.py --retrospective`) for recent sprint patterns.
> 3. **Live Runtime Failure Trace:** Inspect [`HomeLabAI/logs/delegation_failures.log`](file:///home/jallred/Dev_Lab/HomeLabAI/logs/delegation_failures.log) for raw upstream provider errors (e.g. argument mismatches, 429/500 ladders, socket drops).

```
  ┌────────────────────────────────────────────────────────────┐
  │ 1. Ground & Delegate (Antigravity / Gemini - AGY)          │
  │    - Mandatory Pre-Audit: Playbook + Failure Ledger        │
  │    - Master Plan entry in SPRINT_PLAN_SPR_XX_X.md          │
  │    - Dispatch via delegate.py to port 4097 (Sisyphus)      │
  └─────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
  ┌────────────────────────────────────────────────────────────┐
  │ 2. Execute & Verify (Sisyphus / Safe-Patch)                │
  │    - Code changes written via clara-dna_safe_patch         │
  │    - Pytest / verification scripts executed in-session     │
  │    - Workers prohibited from git commit                    │
  └─────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
  ┌────────────────────────────────────────────────────────────┐
  │ 3. Forensic Review & Gate (Antigravity / Gemini - AGY)     │
  │    - Inspect git diffs of modified files                   │
  │    - Verify test suite & assertion outputs                 │
  │    - Perform git add and git commit                        │
  └─────────────────────────────┘
```

### 5.1 Git Ownership & Review Gate
OpenAgent workers perform file edits and execute test suites locally, but are **strictly prohibited from executing `git commit`**. AGY (the Strategic Guardian) performs the git diff audit, verifies test results, and executes the git commit upon task certification.

### 5.2 Circuit Breaker & Anti-Looping (BKM-038)
- `opencode-core.service` is configured with `StartLimitIntervalSec=60s` and `StartLimitBurst=3`.
- If a worker process crashes or gets stuck in a loop, systemd halts the service after 3 bursts instead of spinning continuously.

### 5.3 Retrospective Ledger
- **Story 901 Reflection:** Exposed a declared-vs-actual model routing discrepancy where `delegate.py` hardcoded `opencode/big-pickle` instead of respecting configured personas. Resolved by harmonizing dispatch requests with configured models.
- **Story 1 Reflection:** Sprint plans must provide a one-line `ground_truth_summary` per anchor to make anchor transcription mechanical rather than requiring runtime knowledge authoring.
- **Story 2 Reflection:** Avoid guessing class export names in sprint specs; verify exact module exports via codegraph/grep before authoring story prompts.
- **Story 4 Reflection:** Provide exact grep snippets rather than approximate line ranges when referencing fast-moving codebase locations.
- **Sprint 54.10:** Replaced disabled `edit` tool with `clara-dna_safe_patch`, bound M5 Air to MLX port 8000 (`mlx-community--Qwen3.8-27B-4bit`), eliminated Google Gemini from OpenAgent fallbacks, and established the OpenRouter Free $\rightarrow$ OpenCode Free $\rightarrow$ Cohere $\rightarrow$ M5 Air MLX $\rightarrow$ Windows 4090 fallback chain.

### 5.4 Swarm Mechanics, Model Tool Limits & Upstream Bug Catalog
* **Model Tool-Calling Limits (Node KENDER)**:
  * `qwen2.5-coder:14b` does NOT emit OpenAI-compatible `tool_calls` through Ollama's `/v1` endpoint.
  * `qwen3-14b-16k:latest` DOES emit proper `tool_calls`. All KENDER categories route to `my-windows-4090/qwen3-14b-16k:latest`.
  * **Ollama Stream Interleaved Stalls:** Do NOT set `"interleaved": { "field": "reasoning_content" }` on Ollama provider models in `opencode.json` as it deadlocks the stream parser on tool calls.
* **OmO `task()` Internal Mechanics**:
  * Sisyphus only routes work to KENDER when it emits an explicit `task(category="quick", ...)` tool call. Prose instructions without `task()` result in Sisyphus doing all work itself.
  * Every `task()` prompt must include `## MUST DO: Use the edit/write tool to apply the change to <path>`.
* **Upstream OpenCode Bug Catalog**:
  * *Prompt-directed delegation* (upstream #3231): Handled via `agents.sisyphus.prompt_append`.
  * *`task` tool deferred behind ToolSearch* (upstream #3592): Kept visible with minimal MCP clutter.
  * *Empty delegation table* (upstream #2386): Resolved via PR #414 fix in installed plugin.

---

## 6. The Agent Cascade Architecture (Context-Isolated Swarms)

#### 6.1 The 3-Tier Bicameral Hierarchy (AGENTS_L1.md, AGENTS_L2.md, AGENTS_L3.md)
The Federated Lab operates under a streamlined **3-Tier Bicameral Hierarchy** designed to maximize 128k context utilization across silicon nodes while isolating terminal file mutation:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Tier 1 / Layer 1: Strategic Guardian & Master Conductor (AGY / Gemini)      │
│ - Authors master sprint plans, defines interface contracts, certifies git. │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ delegate.py dispatch
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Tier 2 / Layer 2: Tactical Conductor (Atlas on Node KENDER 4090 - 128k)      │
│ - Ingests sprint specs and inspects target code with read/grep/glob.       │
│ - Synthesizes bounded <2k token contracts and companion test assertions.   │
│ - Has write: deny and edit: deny. Dispatches to Layer 3 via task().         │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ task(prompt="[AGENTS_L3.md Contract]")
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Tier 3 / Layer 3: Surgical Execution Worker (Junior / Hephaestus on M5 Air) │
│ - Terminal execution tier (task: deny). Ingests bounded prompt contract.   │
│ - Applies edits strictly via clara-dna_safe_patch (or write for greenfield).│
│ - Executes pytest verification via bash and emits [HANDOVER REFLECTION].   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Handover Reflection Report
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Layer 1 Review & Certification: AGY audits diffs and commits locally.       │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Agent Permission Matrix in the Cascade
| Role / Persona | Silicon Seat | Tools Permitted | Tools Denied | Primary Mandate |
| :--- | :--- | :--- | :--- | :--- |
| **Atlas** (Layer 2 Conductor) | KENDER 4090 | `read`, `grep`, `glob`, `task` | `edit`, `write`, `safe_patch`, `bash`, `question`, `icm_*` | Ingest sprint plan, synthesize Layer 3 contracts |
| **Sisyphus-Junior** (Layer 3 Patcher) | Apple M5 Air (:8002) | `safe_patch`, `read`, `bash` | `edit`, `write`, `task`, `question`, `icm_*` | Surgical file edits and pytest verification |
| **Hephaestus** (Layer 3 Greenfield) | Apple M5 Air (:8002) | `write`, `safe_patch`, `read`, `bash` | `edit`, `task`, `question`, `icm_*` | Greenfield scaffolding and module creation |
| **Librarian** (Utility Scout) | KENDER 4090 | `read`, `grep`, `glob` | `write`, `edit`, `bash`, `task`, `icm_*` | Specialized code and symbol discovery |
| **Momus** (Utility Verifier) | KENDER 4090 | `bash`, `read` | `write`, `edit`, `safe_patch`, `task` | Isolated test traceback analysis |
| **Sisyphus-Junior** (Patcher)| M5 Air (:8000) | `clara-dna_safe_patch` | `bash`, `edit`, `write`, `icm_*`, `task`, `question` | Apply surgical code edits via exact AST diffs (<2k tokens) |
| **Hephaestus** (Scaffolder)| M5 Air (:8000) | `write`, `clara-dna_safe_patch`, `read` | `bash`, `edit`, `icm_*`, `task`, `question` | Greenfield module creation & full-file scaffolding |
| **Momus / Argus** (Verifier) | KENDER 4090 | `bash`, `read` | `write`, `edit`, `safe_patch`, `task`, `icm_*` | Run pytest / ruff check, parse tracebacks |

---

## 7. Operational Fix & Calibration Ledger (BKM-049 Tri-Loop Inter-Attempt Log)

This ledger records live operational calibration fixes, tool adjustments, and hardware alignments discovered between BKM-049 Tri-Loop retry attempts:

| Date / Sprint | Component / Layer | Root Cause / Friction | Operational Calibration / Fix Applied |
| :--- | :--- | :--- | :--- |
| 2026-09-13 (Spr 78.4) | Tool Schema / Token Bloat | Unscoped MCP tools injected 24.5k tokens per prompt | Added `icm_*`, `websearch_*`, `codegraph_*` denials in `oh-my-openagent.json` (`BKM-051`) |
| 2026-09-13 (Spr 78.4) | Ambient ICM Hooks | Ambient memory hook injected history into automated story prompts | Added programmatic skip in `icm_hook.py` when delegation header detected |
| 2026-09-13 (Spr 78.4) | Ollama Context Window | Default 2k/8k context truncated prompt payloads | Created and pinned `qwen3-14b-16k:latest` with `num_ctx 16384` across configs |
| 2026-09-13 (Spr 78.4) | Ollama Stream Deadlock | `"interleaved": { "field": "reasoning_content" }` caused stream stalls | Removed interleaved setting from `opencode.json` Ollama provider block |
| 2026-09-13 (Spr 78.4) | Silicon Port Routing | Direct `:8000` calls to M5 Air risked Metal wired memory overflow | Enforced Port 8002 Headroom Compression Proxy in all `opencode.json` M5 MLX definitions |
| 2026-09-13 (Spr 78.4) | Diagnostic Gate | Fix-repair steps skipped playbook guidance leading to config thrashing | Added mandatory Playbook Audit Step 4 to `BKM-049` protocol |
| 2026-09-16 (Spr 82.4) | Silicon Engine Upgrade | Qwen3.8-27B was high-latency (~18 tok/s) and constrained Metal VRAM | Swapped M5 resident model to `mlx-community--Qwen3.5-9B-4bit` (50–65 tok/s, 5.5GB VRAM, 65k context) |
| 2026-09-23 (Spr 88.0) | Top-Level Silicon Routing & Concurrency | `delegate.py` in `execute` mode bypassed KENDER 4090 and routed top-level session to M5 Air (MLX), causing single-concurrency recursive deadlock when M5 Air attempted nested subdelegation; stale 27B model references confused routing | Fixed `delegate.py` `local_only` top-level session to ALWAYS route to KENDER 4090 Atlas (`my-windows-4090`); scrubbed all stale 27B strings to reflect unified 9B MLX resident; aligned Atlas prompt to use strict category routing (`category="coder"` for Junior on M5 Air; `category="unspecified-low"` for Kender Momus/Librarian). |
| 2026-09-23 (Spr 88.0) | Anti-Pattern Elimination & Junior Lockdown | Hardcoded model dictionaries in `delegate.py` shadowed central configs; calling `sisyphus` instead of `sisyphus-junior` allowed tool roaming to ChromaDB; unguided patches caused structural AST nesting errors | Eliminated hardcoded model dictionaries in `delegate.py` (authoritative config delegated to `infrastructure.json` + `oh-my-openagent.json`); bound local execution explicitly to `sisyphus-junior` (strict tool jail); established mandatory 4-anchor spoon-feeding contract for `[SWARM:LOCAL]` stories. Certified via canary test. |
| 2026-09-23 (Spr 88.2) | Model Standardization & Local Delegation Fallback | `qwen3-14b-16k:latest` was hardcoded as a fallback in `delegate.py` and `infrastructure.json` had `"architect"` instead of `"reasoner"`, causing HTTP 500 Unknown Model error on Kender Ollama after tag consolidation to standard `qwen3:14b` (64k context). | Standardized all configs, `delegate.py`, and playbook references to generic `qwen3:14b`, unified `local_bicameral` reasoner/architect alias lookup, and verified clean dispatch to KENDER. |
| 2026-09-23 (Spr 88.2) | Cloud Topology Convergence & Model Decoupling | Groq 70B deprecation (403 Forbidden) and hardcoded fallback dictionaries inside `delegate.py` shadowed central configs, creating phantom model references; `big-pickle` silent-200 empty-part traps prevented clean cascades. | Decoupled `delegate.py` by eliminating all embedded model dicts (enforcing authoritative dynamic resolution from `infrastructure.json`), converged cloud categories onto `openrouter/free` meta-router with Cohere `command-a-plus-05-2026` as resilient 256k backstop. |
| 2026-09-29 (Spr 95.1) | Cloud Sisyphus Restoration & Dynamic Ladder Recovery | Fix-retry drift accidentally assigned `sisyphus` to local M5 Air silicon in `oh-my-openagent.json`, while `delegate.py` hardcoded `opencode/big-pickle`, bypassing `openrouter/free` and `cohere` fallbacks and causing 1400s remote connection dropouts during cloud tasks. | Restored `sisyphus` to `openrouter/free` (with `cohere` and `big-pickle` fallbacks) in `oh-my-openagent.json`, restored dynamic `infrastructure.json` swarm alias resolution in `delegate.py`, and synchronized `fast_worker` cloud ladders. |
| 2026-09-29 (Spr 95.1) | True Lightweight Shim & OpenAgent Decoupling | Automated fix-retry loops repeatedly drifted into programmatically resolving models and injecting `{"model": current_model}` overrides into `delegate.py`, subverting `oh-my-openagent.json` and disabling OpenCode's native fallback ladders. | Purged all programmatic model ladders from `delegate.py`, restored pure single-shot text dispatch, and re-anchored model routing, fallback ladders, and agent permissions 100% inside `oh-my-openagent.json`. Re-aligned Local Swarm to Atlas (KENDER 4090 conductor) + Sisyphus-Junior (M5 Air surgical worker) with 4-anchor contracts. |
| 2026-10-01 (Spr 96.0) | OpenRouter Tail-Only Rule & Stream Stall Trap | OpenRouter Free accepts connections but stalls mid-generation without throwing explicit HTTP error codes, preventing OpenCode's catch-block fallback handler from triggering and deadlocking the session. | Re-anchored OpenRouter Free strictly as the tail-end backup behind `opencode/big-pickle` in `oh-my-openagent.json`; never specify individual models on OpenRouter Free; zero Cohere and zero Google in OpenAgent fallback tier. |
| 2026-10-01 (Spr 96.0) | Loop DNA Invariant vs. Runtime Delegation Feedback | Conflating `LOOP_LEDGER.md` (human-curated architectural loop definitions) with runtime execution feedback led to prompt drift where Layer 1 was told to record operational friction in `LOOP_LEDGER.md`. | Enforced strict architectural distinction: `LOOP_LEDGER.md` / `loop_ledger.jsonl` are immutable Loop DNA specifications under `BKM-069`; runtime delegation feedback is ephemeral and streamed to stdout/terminal for AGY, with metrics recorded to `data/delegation_ledger.jsonl`. Delegation never writes to markdown or DNA files. |
| 2026-10-01 (Spr 96.0) | 3-Tier Swarm Hierarchy Invariant (Scrub 5-Stage) | Verbose 5-stage cascade prompts created greedy token attractor loops on local 27B GGUF weights, while unapproved roles bloated the cascade. | Standardized on canonical 3-Tier Bicameral Hierarchy (AGY Strategic Guardian $\rightarrow$ Atlas KENDER 4090 Tactical Conductor $\rightarrow$ Junior/Hephaestus M5 Air Surgical Worker); scrubbed all unapproved 5-stage cascade references across prompt and playbook. |
| 2026-10-01 (Spr 96.0) | Multi-Tier Backpressure Feedback Contract | Local workers lacked explicit backpressure escalation paths, leading to exploratory guessing and hallucinated file mutations. | Standardized backpressure contracts: Tier 3 pushes back on anchor mismatches via `[BLOCKER REPORT: ANCHOR_DRIFT_MISMATCH]`; Tier 2 relays blockers upward to Tier 1 without guessing; Tier 1 performs diagnostic retry/calibration under `BKM-049`. |
| 2026-10-01 (Spr 96.0) | Top-Level KENDER REST Binding & L2->L3 Category Routing | `delegate.py` and OpenCode defaulted top-level sessions to Sisyphus Ultraworker (Cloud/M5 Air) because `POST /session` lacked explicit model/agent bindings and `opencode.json` root pointed to Air; Atlas could not name Junior directly via `task()`. | 1) Bound `POST /session` in `delegate.py` explicitly to `agent: atlas` + `my-windows-4090` (KENDER 4090); 2) Kept `oh-my-openagent.json` neutral by removing global `default_run_agent` so cloud/local sessions both dispatch dynamically; 3) Aligned L2 $\rightarrow$ L3 delegation mechanics: Atlas uses `task(category="coder")` to route surgical edits to Junior on M5 Air. |
| 2026-10-01 (Spr 96.0) | Zero Fallback Bleed Invariant & Local Isolation | Local agents had cross-tier and cloud fallbacks, which caused silent cloud escalation, burned API quota, and leaked local code context during transient local stalls. | Enforced `"fallback_models": []` across all local agents (`atlas`, `junior`, `hephaestus`, `daedalus`) and local categories (`coder`, `unspecified-low`). Cloud fallbacks remain strictly on Cloud Ultraworker (`sisyphus`). |
| 2026-10-01 (Spr 96.0) | Dynamic Model Inheritance & Scrubbing Re-Baked Tags | Hardcoded model tag strings proliferated across every agent block in `oh-my-openagent.json`, making configs brittle to model updates on local hardware endpoints. | Decoupled endpoint definitions into `opencode.json` (single source of hardware truth) and omitted redundant `model` declarations in `oh-my-openagent.json` so agents dynamically inherit root/category models. |
| 2026-10-01 (Spr 96.0) | Scrubbing Legacy Momus & Librarian Stages | Intermediate Momus and Librarian agents added unnecessary prompt hops and tool permission complexity. | Officially purged Momus and Librarian from `oh-my-openagent.json`, `delegate.py`, and playbook permissions, locking in direct 2-tier local execution: Atlas (L2) $\to$ Junior (L3). |


