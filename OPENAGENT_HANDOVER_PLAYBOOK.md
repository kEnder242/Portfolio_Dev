# 📖 OpenAgent Handover & Co-Pilot Playbook

This playbook serves as the definitive reference guide for task allocation, model grounding, session management, and verification when coordinating between **Antigravity (AGY)** (Gemini-driven strategic co-pilot) and **OpenAgent** (autonomous coding swarm attached to port 4096).

---

## 1. Model Allocation & Swarm Topology

Tasks are allocated based on engine roles to minimize API costs, prevent rate-limiting, and ensure high-fidelity coding execution:

| Role / Engine | Primary Function | Invocation Command Pattern |
| :--- | :--- | :--- |
| **Strategic Guardian (AGY)** | Master plan creation, architecture design, code review, git commits | AGY CLI Turn |
| **Sisyphus (Ultraworker & Autonomous Engineer)** | Primary Direct Autonomous Implementer for `delegate.py` story dispatches; directly executes safe_patch/bash | Dispatched via `delegate.py` (default) |
| **Atlas (Plan Executor & Swarm Conductor)** | Swarm orchestrator for multi-subagent task cascades (M5 Air / Windows 4090) | Dispatched via `delegate.py --agent atlas` |
| **Prometheus (Planner & Diagnostic Investigator)** | Read-only strategic planner, pre-flight context auditor, diagnostic investigator | Dispatched via `delegate.py --mode plan/investigate` |
| **Primary Local MLX Node** | Mac M5 Air (Port 8000 MLX: `Qwen3.8-27B-4bit`) for high-speed local inference | Subagent target / primary local compute |
| **Primary Local Ground Worker** | Node KENDER / Windows 4090 (Port 11434 Ollama: `qwen2.5-coder:14b`) | Subagent `task()` target / local backup |
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

---

## 4. Swarm & Configuration Map

### 4.1 Configuration Files
- **OpenAgent Core Config:** `~/.config/opencode/oh-my-openagent.json`
- **MCP Tool Bridge:** `HomeLabAI/.opencode.json` (OpenAgent) & `~/.gemini/config/mcp_config.json` (AGY)
- **Delegation Harness:** `HomeLabAI/src/tests/delegate.py`

### 4.2 Engine Hardware & Role Mapping Matrix

| Role | Hardware / Binding | Context Limit | Primary Purpose | Fallback Route |
| :--- | :--- | :--- | :--- | :--- |
| **Sisyphus (Lead)** | OpenCode Free (`opencode/deepseek-v4-flash-free`) | 256K | Direct code edits, surgical refactoring | OpenRouter Free $\rightarrow$ Cohere $\rightarrow$ M5 MLX $\rightarrow$ 4090 |
| **Atlas / Prometheus** | OpenCode Free (`opencode/deepseek-v4-flash-free`) | 256K | Swarm conduction, architectural planning | OpenRouter Free $\rightarrow$ Cohere $\rightarrow$ M5 MLX $\rightarrow$ 4090 |
| **Mac M5 Air (MLX)** | Node Brain / Mac M5 (Port 8000: `Qwen3.8-27B-4bit`) | 32K | High-speed local reasoning & code generation | Windows 4090 (`qwen2.5-coder:14b`) |
| **Windows 4090 (Ollama)** | Node KENDER / Windows 4090 (Port 11434) | 16K–32K | Local ground worker code edits, offline execution | Cloud Free Tier |
| **Cloud Resiliency Tier** | Cohere (`command-a-plus-05-2026`) | 256K | Complex refactoring, emergency cloud fallback | M5 MLX / Windows 4090 |

### 4.3 Dynamic Category Taxonomy (Web GUI vs. Headless Dispatch)

When driving tasks interactively from the **Web GUI** (`http://192.168.1.238:4096/`), agents like Sisyphus decompose tasks and spawn background subagents via `task(category="...")`. In contrast to direct `delegate.py` dispatches (which bind to an agent identity), subagents resolve their model bindings strictly from the **`categories`** block in `oh-my-openagent.json`:

| Category | Typical Subagent Tasks | Primary Model Binding | Fallback Chain |
| :--- | :--- | :--- | :--- |
| **`ultrabrain`** | Deep architecture derivation, multi-file refactoring | `opencode/deepseek-v4-flash-free` | OpenRouter Free $\rightarrow$ Cohere $\rightarrow$ M5 MLX $\rightarrow$ 4090 |
| **`deep`** | Complex local implementation, heavy coding | `my-m5-mlx/mlx-community/Qwen3.8-27B-4bit` | DeepSeek $\rightarrow$ OpenRouter Free $\rightarrow$ 4090 $\rightarrow$ Cohere |
| **`writing`** | Documentation, docstrings, summaries, sprint logs | `opencode/deepseek-v4-flash-free` | OpenRouter Free $\rightarrow$ Cohere $\rightarrow$ M5 MLX |
| **`visual-engineering`** | Frontend HTML/CSS layout, UI rendering | `opencode/deepseek-v4-flash-free` | OpenRouter Free $\rightarrow$ Qwen 3.6 Plus |
| **`quick`** | Trivial lookups, file checks, regex queries | `opencode/longcat-2.0-free` | OpenRouter Free $\rightarrow$ DeepSeek $\rightarrow$ 4090 |
| **`unspecified-high`** | General high-complexity fallback | `opencode/deepseek-v4-flash-free` | OpenRouter Free $\rightarrow$ Cohere |
| **`unspecified-low`** | General low-complexity fallback | `opencode/longcat-2.0-free` | DeepSeek $\rightarrow$ OpenRouter Free $\rightarrow$ 4090 |

> [!WARNING]
> If a category (such as `writing` or `unspecified-low`) is omitted from `oh-my-openagent.json`, `oh-my-openagent` falls back to its upstream hardcoded default (often Claude Opus or OpenRouter paid tier). This bypasses the free ladder and triggers immediate provider authorization or rate-limit failures. All 7 categories must remain explicitly mapped in `oh-my-openagent.json`.

---

## 5. Safety Gates & Troubleshooting Ledger

```
  ┌────────────────────────────────────────────────────────────┐
  │ 1. Ground & Delegate (Antigravity / Gemini - AGY)          │
  │    - Master Plan entry in SPRINT_PLAN_SPR_XX_X.md          │
  │    - Dispatch via delegate.py to port 4097 (Sisyphus)      │
  └─────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
  ┌────────────────────────────────────────────────────────────┐
  │ 2. Execute & Verify (Sisyphus / Safe-Patch)                │
  │    - Code changes written via clara-dna_safe_patch         │
  │    - Pytest / verification scripts executed in-session     │
  │    - Workers prohibited from git commit                     │
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
- **Sprint 54.10:** Replaced disabled `edit` tool with `clara-dna_safe_patch`, bound M5 Air to MLX port 8000 (`Qwen3.8-27B-4bit`), eliminated Google Gemini from OpenAgent fallbacks, and established the OpenRouter Free $\rightarrow$ OpenCode Free $\rightarrow$ Cohere $\rightarrow$ M5 Air MLX $\rightarrow$ Windows 4090 fallback chain.

### 5.4 Swarm Mechanics, Model Tool Limits & Upstream Bug Catalog
* **Model Tool-Calling Limits (Node KENDER)**:
  * `qwen2.5-coder:14b` does NOT emit OpenAI-compatible `tool_calls` through Ollama's `/v1` endpoint (returns plain text tool calls that the harness never executes).
  * `qwen3:14b` DOES emit proper `tool_calls`. All OmO categories in `~/.config/opencode/oh-my-openagent.json` route to `my-windows-4090/qwen3:14b`.
* **OmO `task()` Internal Mechanics**:
  * Sisyphus only routes work to KENDER when it emits an explicit `task(category="quick", ...)` tool call. Prose instructions without `task()` result in Sisyphus doing all work itself.
  * Every `task()` prompt must include `## MUST DO: Use the edit/write tool to apply the change to <path>`.
* **Upstream OpenCode Bug Catalog**:
  * *Prompt-directed delegation* (upstream #3231): Handled via `agents.sisyphus.prompt_append`.
  * *`task` tool deferred behind ToolSearch* (upstream #3592): Kept visible with minimal MCP clutter.
  * *Empty delegation table* (upstream #2386): Resolved via PR #414 fix in installed plugin.
