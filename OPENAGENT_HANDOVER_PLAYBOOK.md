# 📖 OpenAgent Handover & Co-Pilot Playbook

This playbook serves as the definitive reference guide for task allocation, model grounding, session management, and verification when coordinating between **Antigravity (AGY)** (Gemini-driven strategic co-pilot) and **OpenAgent** (autonomous coding swarm attached to port 4096).

---

## 1. Model Allocation & Swarm Topology

Tasks are allocated based on model strengths to minimize API costs, prevent rate-limiting, and ensure high-fidelity coding execution:

| Role / Engine | Provider / Model | Primary Function | Invocation Command Pattern |
| :--- | :--- | :--- | :--- |
| **Strategic Guardian** | `google/gemini-2.5-flash` / `pro` | Master plan creation, architecture design, code review, git commits | AGY CLI Turn |
| **Sisyphus (Lead Orchestrator)** | `opencode/deepseek-v4-flash-free` | Lead worker & orchestrator for task delegation, diff auditing, and state tracking | `opencode run --dir <dir> --attach http://127.0.0.1:4096/ "SESSION: ..."` |
| **Atlas (Plan Executor)** | `groq/llama-3.3-70b-versatile` | Plan Executor for `delegate.py` story dispatches; blocked from direct file edits (`disabled_tools`) | `opencode run -m groq/llama-3.3-70b-versatile "task"` |
| **Prometheus (Planner / Reviewer)** | `groq/llama-3.3-70b-versatile` | Strategic planner, pre-flight context auditor, test suite verifier | `opencode run -m groq/llama-3.3-70b-versatile "task"` |
| **Sisyphus-Junior (Ground Worker)** | `my-windows-4090/qwen3:14b` (Windows 4090) | High-speed local code generation, syntax editing, line-by-line diffs (native `tool_calls`) | `opencode run -m my-windows-4090/qwen3:14b "task"` |
| **Triage / Utility** | `opencode/deepseek-v4-flash-free` | Fast text processing, status parsing, lightweight search | `opencode run -m opencode/deepseek-v4-flash-free "task"` |

---

## 2. Session Lifecycle & Webview Visibility (BKM-034 Point 12)

### 2.1 Mandatory Shell Execution (Port 4096)
All tactical developer tasks delegated to OpenAgent must be launched via the shell-based `opencode` CLI attached to port 4096:
```bash
/home/jallred/.opencode/bin/opencode run --dir <target_dir> --attach http://127.0.0.1:4096/ "SESSION: Sprint XX Story YY — <Title>..."
```
> [!IMPORTANT]
> Never use internal `invoke_subagent` for developer/implementation tasks. `invoke_subagent` is strictly reserved for read-only research tasks. Attaching to port 4096 ensures all active worker sessions render live on the local TUI and webview dashboard at `http://192.168.1.238:4096/`.

### 2.2 Named Sessions & Persistence
- **Session Declaration:** The first prompt of a new session must explicitly start with `SESSION: Sprint XX Story YY — <Title>`. This guarantees the session is indexed with a clear title on the web dashboard instead of generic titles like "New session".
- **Resuming Sessions:** To continue work in an existing session, use `--session <session_id>` or `-c`:
  ```bash
  opencode run --dir <dir> --attach http://127.0.0.1:4096/ --session ses_XXXX "Next task prompt..."
  ```
- **Forking Context:** Use `--fork` when branching from a known stable state without dirtying the parent session.

### 2.3 Socket-Activated Daemon Warm-Up
The OmO web UI proxy (`opencode-proxy.service`) is socket-activated via `opencode.socket` on `0.0.0.0:4096` with `StopWhenUnneeded=true`. Before launching any session, `delegate.py` calls `wake_web_ui()` which HTTP-GETs `http://127.0.0.1:4096/` — this TCP connect triggers the `opencode.socket` → `opencode-proxy.service` → `codex:4097` activation chain.

**Port separation (do not confuse):**
- `4097` = `codex serve` REST API (system-level service, always running). Used for session creation and message dispatch.
- `4096` = Web UI proxy (user-level, socket-activated, idle-stops after 5min). Required for browser access at `http://192.168.1.238:4096/`.

---

## 3. Context & Token Optimization

### 3.1 Narrow Workspace Scoping
- **The Rule:** Always set `--dir` to the narrowest sub-project directory (e.g. `--dir /home/jallred/Dev_Lab/HomeLabAI`).
- **The Pitfall:** Initializing OpenAgent at the parent root (`/home/jallred/Dev_Lab`) causes the server to index both sub-repositories, compiling 40K+ baseline tokens on turn 1 and exhausting cloud TPM limits.
- **On-Demand Cross-Repo References:** To reference files outside the target workspace (like `Portfolio_Dev/SPRINT_PLAN_SPR_42_0.md`), include absolute markdown links using the `file://` scheme in the prompt. OpenAgent will fetch that specific file on-demand without indexing the rest of the repository.

### 3.2 Vector DNA Grounding (Port 8001)
- Instead of injecting full markdown files (`FeatureTracker.md` or `Protocols.md`) into prompt text, BKM and FEAT context is retrieved dynamically from ChromaDB vector collections (`behavioral_dna`, `feature_dna`) running on port 8001.
- **Semantic Translation:** Translate conversational user prompts into precise domain keywords (e.g., `"atomic write"`, `"safe file patch"`, `"circuit breaker"`) before querying vector collections.

### 3.3 Clean Delegation Prompting
Cloud orchestrators compile concise prompt specifications focused on target files and functional requirements. Avoid hyper-verbose negative constraints or role roleplay—Atlas orchestrates work naturally when provided a clean specification:

```markdown
SESSION: Sprint XX Story YY — <Title>

[CONTEXT & TARGET SPECIFICATION]
- Sprint Plan Reference: file://<path_to_sprint_plan>.md#Story-YY
- Target Files: <absolute_path_to_target_file_1>, <absolute_path_to_target_file_2>

[FUNCTIONAL REQUIREMENTS]
1. <Requirement 1>
2. <Requirement 2>

[NOTE]
Apply code modifications only. Silicon validation and testing will be performed post-dispatch by the orchestrator.
```

---


## 4. Safety Gates & Troubleshooting Ledger

```
  ┌────────────────────────────────────────────────────────────┐
  │ 1. Ground & Delegate (Antigravity / Gemini)                │
  │    - Master Plan entry in SPRINT_PLAN_SPR_XX_X.md          │
  │    - Launch opencode CLI attached to port 4096              │
  └─────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
  ┌────────────────────────────────────────────────────────────┐
  │ 2. Execute & Verify (OpenAgent Swarm)                      │
  │    - Code changes written to local target directory        │
  │    - Pytest / verification scripts executed in-session     │
  │    - Worker prohibited from git commit                     │
  └─────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
  ┌────────────────────────────────────────────────────────────┐
  │ 3. Forensic Review & Gate (Antigravity / Gemini)           │
  │    - Inspect git diffs of modified files                   │
  │    - Verify test suite & assertion outputs                 │
  │    - Perform git add and git commit                        │
  └────────────────────────────────────────────────────────────┘
```

### 4.1 Git Ownership & Review Gate
OpenAgent workers perform file edits and execute test suites locally, but are **strictly prohibited from executing `git commit`**. AGY (the Strategic Guardian) performs the git diff audit, verifies test results, and executes the git commit upon task certification.

### 4.2 Circuit Breaker & Anti-Looping (BKM-038)
- `opencode-core.service` is configured with `StartLimitIntervalSec=60s` and `StartLimitBurst=3`.
- If a worker process crashes or gets stuck in a loop, systemd halts the service after 3 bursts instead of spinning continuously.
- On completion, AGY verifies zero established sockets (`ss -tp | grep 11434`) remain connected to remote compute nodes (Node KENDER).

### 4.4 Token Behavior & Provider Quota Matrix
To prevent rate-limit crashes and manage cloud token budgets effectively:

- **Google Gemini Free Tier (`google/gemini-2.5-flash`)**: 250,000 Input Tokens/Min (TPM) capacity with 20 Requests/Min (RPM) limit. Primary model for OpenAgent orchestration.
- **Groq (`groq/llama-3.3-70b-versatile`)**: Strict 12,000 TPM limit. Ideal for concise sub-task planning or verification prompts (<10k tokens). Cannot accept heavy OpenCode initial payloads (80k+ tokens).
- **DeepSeek Free Tier (`opencode/deepseek-v4-flash-free`)**: Generous free tier for text processing, status checks, and triage.
- **Node KENDER (`my-windows-4090/qwen2.5-coder:14b`)**: **Strict Isolation Mandate.** KENDER's local Ollama instance is reserved exclusively for live Round Table integration tests and high-speed local code generation (`Sisyphus-Junior`). It MUST NOT be used for top-level OpenAgent orchestration to avoid compute and VRAM resource contention during automated test runs.

### 4.5 Delegation Helper Scripts
All CLI delegations are routed through:
- **`delegate.py`**: `/home/jallred/Dev_Lab/HomeLabAI/src/tests/delegate.py`
  - Calls `wake_web_ui()` to activate port 4096 socket chain.
  - Creates session via `POST http://127.0.0.1:4097/session`.
  - Dispatches prompt via `POST http://127.0.0.1:4097/session/<id>/message` (headless REST, no TUI required).
  - **Do NOT use `opencode run --attach` from scripts** — it is a blocking foreground TUI and hangs when the webview is down.

### 4.6 Orchestrator Non-Coding Mandate
The Strategic Guardian (**Antigravity / Gemini**) is strictly an **architect, planner, and git reviewer**. The orchestrator MUST NOT directly write code, implement features, or generate unit test files itself when an OpenAgent developer swarm is available. All code writing, test file creation, and refactoring MUST be delegated to OpenAgent.

---

## 5. Historical Evolution & Sprint Retrospective Wins

- **Sprint 36:** Established basic model matrix (Gemini orchestrator + Qwen local ground worker).
- **Sprint 38:** Added session naming conventions (`SESSION: Sprint XX Story YY`) and Ollama concurrency fixes.
- **Sprint 40:** Integrated real-time Grafana/Prometheus telemetry and socket-activated server hibernation.
- **Sprint 42:** Standardized BKM-034 Point 12 (mandatory shell execution on port 4096 for webview visibility), implemented ICM persistent memory hybrid offloading (BKM-037), and established daemon circuit breakers (BKM-038).
- **Sprint 47.1:** Enforced Submodule `.opencodeignore` context isolation, established the Pre-Grounded Blueprint template, documented model token quota ceilings, and added `scratch_delegate.py` helper script mapping.
- **Sprint 48 (RAG Matrix):** Discovered critical delegation gap: prose "delegate to Sisyphus-Junior" directives do NOT invoke the OmO `task()` tool — Sisyphus must emit explicit `task(agent="sisyphus-junior", ...)` tool calls for KENDER to receive work. Fixed `delegate.py` to use headless REST POST dispatch instead of blocking `subprocess.run(opencode run --attach)`. Fixed port 4096 socket wakeup via `wake_web_ui()`. Audit gate added: verify `providerID=my-windows-4090` in session message log after each story.
