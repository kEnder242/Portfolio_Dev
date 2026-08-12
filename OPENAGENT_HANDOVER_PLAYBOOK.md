# 📖 OpenAgent Handover & Co-Pilot Playbook

This playbook serves as the definitive reference guide for task allocation, model grounding, session management, and verification when coordinating between **Antigravity (AGY)** (Gemini-driven strategic co-pilot) and **OpenAgent** (autonomous coding swarm attached to port 4096).

---

## 1. Model Allocation & Swarm Topology

Tasks are allocated based on engine roles to minimize API costs, prevent rate-limiting, and ensure high-fidelity coding execution:

| Role / Engine | Primary Function | Invocation Command Pattern |
| :--- | :--- | :--- |
| **Strategic Guardian (AGY)** | Master plan creation, architecture design, code review, git commits | AGY CLI Turn |
| **Atlas (Plan Executor & Task Orchestrator)** | Primary Task Orchestrator and Plan Executor for `delegate.py` story dispatches; emits `task()` calls | Dispatched via `delegate.py` |
| **Prometheus (Planner & Diagnostic Investigator)** | Read-only strategic planner, pre-flight context auditor, diagnostic investigator | Dispatched via `delegate.py --mode plan/investigate` |
| **Primary Local Ground Worker** | High-speed local code generation, syntax editing, line-by-line diffs (native `tool_calls`) | Subagent `task()` target (default) |
| **Heavy-Logic Local Node** | Local reasoning and complex analysis capped to strict 8K context limit | Subagent `task()` target |
| **Cloud Fallback Tier** | Context overflow escape hatch (HTTP 400 trigger) | Automatic runtime fallback |

---

## 2. Session Lifecycle & Webview Visibility (BKM-034 Point 12)

### 2.1 Mandatory Shell Execution (Port 4096)
All tactical developer tasks delegated to OpenAgent must be launched via `delegate.py` attached to port 4096:
```bash
python3 HomeLabAI/src/tests/delegate.py --sprint XX --story YY --title "<Title>" --reference "<plan>" --target "<file>" --details "<specs>" --mode execute
```
> [!IMPORTANT]
> Never use internal `invoke_subagent` for developer/implementation tasks. `invoke_subagent` is strictly reserved for read-only research tasks. Attaching to port 4096 ensures all active worker sessions render live on the local TUI and webview dashboard at `http://192.168.1.238:4096/`.

### 2.2 Named Sessions & Persistence
- **Session Declaration:** The first prompt of a new session automatically formats `Sprint XX Story YY — <Title>`. This guarantees the session is indexed with a clear title on the web dashboard.
- **Resuming Sessions:** Headless dispatch on port 4097 supports session reuse via REST session IDs.

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

### 3.3 Dynamic Task Routing & Sparse Trapdoors
- **Category Parameter Mandate:** When Atlas emits `task()` calls, it should **omit the `category` parameter** for all standard tasks. Omitting `category` allows OpenAgent to naturally route work to the **primary local ground worker**.
- **Sparse Trapdoors:** Explicit categories (e.g. `category="quick"`) act as sparse trapdoors reserved exclusively for targeted micro-edits.

### 3.4 The Context Escape Hatch (Frugal Matrix VRAM Safety Net)
- **Local Context Ceiling:** The heavy-logic local node is clamped to a strict **8K context limit** to preserve GPU VRAM budget.
- **HTTP 400 Overflow Fallback:** If a prompt/session context overflows the 8K ceiling, the local engine throws an HTTP 400 error.
- **Runtime Fallback Chain:** The `runtime_fallback` chain catches the HTTP 400 and seamlessly hands off execution:
  1. Primary Local Ground Worker (8K limit, zero API cost)
  2. Cloud Reasoning Model (262K context window, preserves reasoning format)
  3. Cloud Escape Hatch (1M-token ceiling)

---

## 4. Swarm & Configuration Map

This map defines the configuration files, hardware bindings, and fallback matrix:

### 4.1 Configuration Files
- **OpenAgent Core Config:** `~/.config/opencode/oh-my-openagent.json`
- **MCP Tool Bridge:** `HomeLabAI/.opencode.json` (OpenAgent) & `~/.gemini/config/mcp_config.json` (AGY)
- **Delegation Harness:** `HomeLabAI/src/tests/delegate.py`

### 4.2 Engine Hardware & Role Mapping Matrix

| Role | Hardware / Binding | Context Limit | Primary Purpose | Fallback Route |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Local Ground Worker** | Node KENDER / Windows 4090 | 8K | High-speed file writes, syntax edits, line-by-line diffs | Cloud Reasoning Tier |
| **Heavy-Logic Local Node** | Node Brain / Mac M5 | 8K | Local reasoning, heavy multi-file logic & architecture | Cloud Reasoning Tier |
| **Cloud Reasoning Model** | Cloud API | 262K | Complex refactoring, heavy context analysis | 1M Cloud Escape Hatch |
| **Cloud Escape Hatch** | Cloud API | 1M | Emergency mega-context payload processing | Terminal Alert |

### 4.3 Delegation Map (Category Routing Intent & Destination)

| Category / Workload | Internal Intent | Hardware Destination |
| :--- | :--- | :--- |
| **`quick`** | Micro-edits, typos, single line fixes | Cloud Fast Inference (Groq) |
| **`ultrabrain` / `deep`** | Heavy multi-file logic & architecture | Local Heavy Compute Node (Mac M5) |
| **`visual-engineering`** | UI, CSS, and layout work | Vision / Cloud Tier |
| *(Unspecified / Default)* | Standard daily coding & feature implementation | Primary Local Ground Worker (Windows 4090) |

---

## 5. Safety Gates & Troubleshooting Ledger

```
  ┌────────────────────────────────────────────────────────────┐
  │ 1. Ground & Delegate (Antigravity / Gemini - AGY)          │
  │    - Master Plan entry in SPRINT_PLAN_SPR_XX_X.md          │
  │    - Dispatch via delegate.py to port 4097                 │
  └─────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
  ┌────────────────────────────────────────────────────────────┐
  │ 2. Execute & Verify (Atlas + Local Ground Worker)          │
  │    - Code changes written to target files                   │
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

### 5.3 Orchestrator Non-Coding Mandate
The Strategic Guardian (**Antigravity / Gemini**) is strictly an **architect, planner, and git reviewer**. The orchestrator MUST NOT directly write code, implement features, or generate unit test files itself when an OpenAgent developer swarm is available. All code writing, test file creation, and refactoring MUST be delegated to OpenAgent.
- **Sprint 42:** Standardized BKM-034 Point 12 (mandatory shell execution on port 4096 for webview visibility), implemented ICM persistent memory hybrid offloading (BKM-037), and established daemon circuit breakers (BKM-038).
- **Sprint 47.1:** Enforced Submodule `.opencodeignore` context isolation, established the Pre-Grounded Blueprint template, documented model token quota ceilings, and added `scratch_delegate.py` helper script mapping.
- **Sprint 48 (RAG Matrix):** Discovered critical delegation gap: prose "delegate to Sisyphus-Junior" directives do NOT invoke the OmO `task()` tool — Sisyphus must emit explicit `task(agent="sisyphus-junior", ...)` tool calls for KENDER to receive work. Fixed `delegate.py` to use headless REST POST dispatch instead of blocking `subprocess.run(opencode run --attach)`. Fixed port 4096 socket wakeup via `wake_web_ui()`. Audit gate added: verify `providerID=my-windows-4090` in session message log after each story.
