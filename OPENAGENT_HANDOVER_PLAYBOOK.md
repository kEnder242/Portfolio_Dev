# 📖 OpenAgent Handover & Co-Pilot Playbook

This playbook serves as the definitive reference guide for task allocation, model grounding, session management, and verification when coordinating between **Antigravity (AGY)** (Gemini-driven strategic co-pilot) and **OpenAgent** (autonomous coding swarm attached to port 4096).

---

## 1. Model Allocation & Swarm Topology

Tasks are allocated based on model strengths to minimize API costs, prevent rate-limiting, and ensure high-fidelity coding execution:

| Role / Engine | Provider / Model | Primary Function | Invocation Command Pattern |
| :--- | :--- | :--- | :--- |
| **Strategic Guardian** | `google/gemini-2.5-flash` / `pro` | Master plan creation, architecture design, code review, git commits | AGY CLI Turn |
| **Sisyphus (Lead Worker)** | `mistral-large-latest` (via OpenCode) | Primary developer subagent for complex refactoring and multi-file logic | `opencode run --dir <dir> --attach http://127.0.0.1:4096/ "SESSION: ..."` |
| **Sisyphus-Junior (Ground Worker)** | `qwen2.5-coder:14b` (Windows 4090) | High-speed local code generation, syntax editing, line-by-line diffs | `opencode run -m my-windows-4090/qwen2.5-coder:14b "task"` |
| **Prometheus (Planner / Reviewer)** | `groq/llama-3.3-70b-versatile` | Parallel test suites, fast code reviews, independent verification | `opencode run -m groq/llama-3.3-70b-versatile "task"` |
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
The OpenAgent daemon (`opencode-core.service`) is socket-activated on port 4096 with `StopWhenUnneeded=true`. Before launching a heavy turn, AGY sends a fast socket ping (`curl -I http://127.0.0.1:4096/`) to wake the server from hibernation.

---

## 3. Context & Token Optimization

### 3.1 Narrow Workspace Scoping
- **The Rule:** Always set `--dir` to the narrowest sub-project directory (e.g. `--dir /home/jallred/Dev_Lab/HomeLabAI`).
- **The Pitfall:** Initializing OpenAgent at the parent root (`/home/jallred/Dev_Lab`) causes the server to index both sub-repositories, compiling 40K+ baseline tokens on turn 1 and exhausting cloud TPM limits.
- **On-Demand Cross-Repo References:** To reference files outside the target workspace (like `Portfolio_Dev/SPRINT_PLAN_SPR_42_0.md`), include absolute markdown links using the `file://` scheme in the prompt. OpenAgent will fetch that specific file on-demand without indexing the rest of the repository.

### 3.2 Vector DNA Grounding (Port 8001)
- Instead of injecting full markdown files (`FeatureTracker.md` or `Protocols.md`) into prompt text, BKM and FEAT context is retrieved dynamically from ChromaDB vector collections (`behavioral_dna`, `feature_dna`) running on port 8001.
- **Semantic Translation:** Translate conversational user prompts into precise domain keywords (e.g., `"atomic write"`, `"safe file patch"`, `"circuit breaker"`) before querying vector collections.

### 3.3 Explicit Blueprint Prompting
Cloud orchestrators (Gemini) must compile exact HTML/CSS blocks, BeautifulSoup scripts, or shell templates directly inside the prompt's `[TARGET SPECIFICATION]` section. This minimizes local model reasoning drift, prevents path hallucinations, and allows code inspection inside the sprint plan before execution.

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

### 4.3 Common Failure Recovery
1. **`Session too large to compact`:** Verify `.opencodeignore` exists in the target directory and excludes `.venv/` and `node_modules/`.
2. **`HttpClient connection failed` (ChromaDB):** All refactored scripts include a failover handler (`try HttpClient(port=8001) except Exception: PersistentClient(...)`), ensuring disk fallback if port 8001 is offline.

---

## 5. Historical Evolution & Sprint Retrospective Wins

- **Sprint 36:** Established basic model matrix (Gemini orchestrator + Qwen local ground worker).
- **Sprint 38:** Added session naming conventions (`SESSION: Sprint XX Story YY`) and Ollama concurrency fixes.
- **Sprint 40:** Integrated real-time Grafana/Prometheus telemetry and socket-activated server hibernation.
- **Sprint 42:** Standardized BKM-034 Point 12 (mandatory shell execution on port 4096 for webview visibility), implemented ICM persistent memory hybrid offloading (BKM-037), and established daemon circuit breakers (BKM-038).
