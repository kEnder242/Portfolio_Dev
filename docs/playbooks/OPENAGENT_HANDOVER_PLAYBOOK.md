# 📖 OpenAgent Handover & Co-Pilot Playbook

This playbook serves as the definitive reference guide for task allocation, model grounding, session management, and verification when coordinating between **Antigravity (AGY)** (Gemini-driven strategic co-pilot) and **OpenAgent** (autonomous coding swarm attached to port 4096).

---

## 1. Model Allocation & Swarm Topology

Tasks are allocated based on engine roles to minimize API costs, prevent rate-limiting, and ensure high-fidelity coding execution:

| Role / Engine | Primary Function | Invocation Command Pattern |
| :--- | :--- | :--- |
| **Strategic Guardian (AGY)** | Master plan creation, architecture design, code review, git commits | AGY CLI Turn |
| **Sisyphus (Ultraworker & Autonomous Engineer)** | Primary Direct Autonomous Implementer for `delegate.py` story dispatches; directly executes safe_patch/bash | Dispatched via `delegate.py` (default) |
| **Atlas (Plan Executor & Swarm Conductor)** | Swarm orchestrator for multi-subagent task cascades (Windows 4090 / M5 Air) | Dispatched via `delegate.py --agent atlas` |
| **Prometheus (Planner & Diagnostic Investigator)** | Read-only strategic planner, pre-flight context auditor, diagnostic investigator | Dispatched via `delegate.py --mode plan/investigate` |
| **Primary Local Ground Worker (KENDER)** | Node KENDER / Windows 4090 (Port 11434 Ollama: `qwen3-14b-16k:latest`) for fast 88 tok/s code editing with 11.7 GB resident VRAM | Subagent `task()` primary target (`atlas`, `librarian`, `momus`) |
| **Primary Local Reasoning Node (M5 Air)** | Mac M5 Air (Port 8002 Headroom Proxy → Port 8000 oMLX: `mlx-community--Qwen3.8-27B-4bit`) for bounded surgical patching & architectural triage | Subagent target for surgical edits (`sisyphus-junior`) |
| **Cloud Fallback Tier** | OpenRouter Free -> OpenCode Free -> Cohere/Mistral (Non-Google) | Automatic runtime fallback |

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
- **Context Pinning on Kender 4090:** Windows 4090 uses `qwen3-14b-16k:latest` with pinned `num_ctx 16384` in Ollama Modelfile, reserving 14.8 GB VRAM for zero-thrash KV caching at 88 tok/s.

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
  This collapses worker prompt overhead from 24.5k down to **$< 1,500$ tokens**, reducing local silicon prefill time from 90s to 2s.
- **Ambient Memory Exemption:** Programmatic dispatches via `delegate.py` include delegation marker headers, allowing `icm_hook.py` to bypass ambient memory search injection and eliminate duplicate context tokens.

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
| **Sisyphus (Lead)** | OpenCode Free (`opencode/deepseek-v4-flash-free`) | 256K | Direct code edits, surgical refactoring | OpenRouter Free $\rightarrow$ Cohere $\rightarrow$ M5 MLX $\rightarrow$ 4090 |
| **Atlas / Prometheus** | OpenCode Free (`opencode/deepseek-v4-flash-free`) | 256K | Swarm conduction, architectural planning | OpenRouter Free $\rightarrow$ Cohere $\rightarrow$ M5 MLX $\rightarrow$ 4090 |
| **Mac M5 Air (MLX)** | Node Brain / Mac M5 (Port 8002 Proxy $\rightarrow$ Port 8000: `mlx-community--Qwen3.8-27B-4bit`) | 32K | Surgical patching (`sisyphus-junior`) & local reasoning | Windows 4090 (`qwen3-14b-16k:latest`) |
| **Windows 4090 (Ollama)** | Node KENDER / Windows 4090 (Port 11434: `qwen3-14b-16k:latest`) | 16K pinned | Conductor (`atlas`), Scout (`librarian`), Verifier (`momus`) | Cloud Free Tier |
| **Cloud Resiliency Tier** | Cohere (`command-a-plus-05-2026`) | 256K | Complex refactoring, emergency cloud fallback | M5 MLX / Windows 4090 |

### 4.3 Dynamic Category Taxonomy (Web GUI vs. Headless Dispatch)

When driving tasks interactively from the **Web GUI** (`http://192.168.1.238:4096/`), agents like Sisyphus decompose tasks and spawn background subagents via `task(category="...")`. In contrast to direct `delegate.py` dispatches (which bind to an agent identity), subagents resolve their model bindings strictly from the **`categories`** block in `oh-my-openagent.json`:

| Category | Typical Subagent Tasks | Primary Model Binding | Fallback Chain |
| :--- | :--- | :--- | :--- |
| **`ultrabrain`** | Deep architecture derivation, multi-file refactoring | `opencode/deepseek-v4-flash-free` | OpenRouter Free $\rightarrow$ Cohere $\rightarrow$ M5 MLX $\rightarrow$ 4090 |
| **`deep`** | Complex local implementation, heavy coding | `my-m5-mlx/mlx-community--Qwen3.8-27B-4bit` | DeepSeek $\rightarrow$ OpenRouter Free $\rightarrow$ 4090 $\rightarrow$ Cohere |
| **`writing`** | Documentation, docstrings, summaries, sprint logs | `opencode/deepseek-v4-flash-free` | OpenRouter Free $\rightarrow$ Cohere $\rightarrow$ M5 MLX |
| **`visual-engineering`** | Frontend HTML/CSS layout, UI rendering | `opencode/deepseek-v4-flash-free` | OpenRouter Free $\rightarrow$ Qwen 3.6 Plus |
| **`quick`** | Trivial lookups, file checks, regex queries | `opencode/longcat-2.0-free` | OpenRouter Free $\rightarrow$ DeepSeek $\rightarrow$ 4090 |
| **`unspecified-high`** | General high-complexity fallback | `opencode/deepseek-v4-flash-free` | OpenRouter Free $\rightarrow$ Cohere |
| **`unspecified-low`** | General low-complexity fallback | `opencode/longcat-2.0-free` | DeepSeek $\rightarrow$ OpenRouter Free $\rightarrow$ 4090 |

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

### 6.1 The Principle: Isolating Micro-Tasks to Preserve Small Contexts
When delegating to local silicon (Node KENDER RTX 4090 / M5 Air), forcing a single agent to plan, search, edit, and verify inevitably exhausts small context windows (Metal 24GB prefill guards or KV cache degradation). Conversely, forcing Layer 1 (AGY) to manually spoon-feed exact import paths, line numbers, and function stubs causes AGY's token consumption to eclipse the cost of writing the code directly.

The **Agent Cascade** solves this by establishing a turn-by-turn daisy-chain of specialized, context-isolated micro-agents orchestrated through OpenAgent's native `task()` tool:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Stage 1: The Tactical Planner (Atlas on Node KENDER 4090)                   │
│ - Ingests the high-level Story section from the sprint plan on disk.        │
│ - Formulates ordered, single-target execution steps (NO CODE EDITS).        │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼ task(category="unspecified-low")
┌─────────────────────────────────────────────────────────────────────────────┐
│ Stage 2: The Anchor & Import Resolver (Librarian / Scout on KENDER 4090)    │
│ - Reads the target file, grep searches symbols, and verifies live imports.  │
│ - Assembles the exact 4-anchor micro-patch payload (< 1,500 tokens).        │
│ - Flushes session context immediately upon task completion.                 │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼ task(category="unspecified-low")
┌─────────────────────────────────────────────────────────────────────────────┐
│ Stage 3: The Surgical Patcher (Sisyphus-Junior on M5 Air via Headroom)      │
│ - Ingests the spoon-fed 4-anchor patch payload.                             │
│ - Applies edits strictly via clara-dna_safe_patch (or write for greenfield).│
│ - Has ZERO bash and runs ZERO tests. Relays non-blocking lint feedback.    │
│ - Flushes session context immediately upon exit.                            │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼ task(category="unspecified-low")
┌─────────────────────────────────────────────────────────────────────────────┐
│ Stage 4: The Verification & Lint Runner (Argus / Momus on KENDER 4090)      │
│ - Receives the verification command (pytest, ruff check, python compile).   │
│ - Executes via bash, parses tracebacks, and returns pass/fail report.       │
│ - Isolates verbose pytest stack dumps away from Junior and the Planner.    │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Stage 5: Synthesis & Handover to AGY                                        │
│ - Atlas synthesizes a 2-line completion report to Layer 1 (AGY).            │
│ - AGY performs final git diff audit and commits to repository.              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Agent Permission Matrix in the Cascade
| Role / Persona | Silicon Seat | Tools Permitted | Tools Denied | Primary Mandate |
| :--- | :--- | :--- | :--- | :--- |
| **Atlas** (Lead Conductor) | KENDER 4090 | `read`, `task` | `edit`, `write`, `safe_patch`, `question`, `icm_*` | Ingest sprint plan, sequence tasks |
| **Librarian** (Scout) | KENDER 4090 | `read`, `grep`, `glob` | `write`, `edit`, `bash`, `task`, `icm_*` | Discover import paths and incumbent code |
| **Sisyphus-Junior** (Patcher)| M5 Air (:8002) | `clara-dna_safe_patch`, `write` | `bash`, `edit`, `icm_*`, `task`, `question` | Apply surgical code edits (<2k tokens) |
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
