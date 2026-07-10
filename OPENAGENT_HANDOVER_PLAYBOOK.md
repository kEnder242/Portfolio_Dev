# 📖 OpenAgent Handover & Co-Pilot Playbook (Sprint 36)

This playbook establishes the protocol for allocating tasks, grounding local models, and validating execution when coordinating between **Antigravity** (Gemini-driven co-pilot) and **OpenAgent** (Groq/Ollama-driven autonomous coding swarm).

---

## 1. Model & Swarm Allocation Matrix

Based on our active configuration check, we allocate the following resources to minimize token costs and ensure high-fidelity coding:

| Provider/Model | Concurrency | Primary Role / Use-Case | Invocation Command |
| :--- | :--- | :--- | :--- |
| **`google/gemini-2.5-flash`** | Dedicated | **Sisyphus (Delegator)**: Cloud-driven orchestration, tool calling, subagent planning | `opencode run "task"` |
| **`my-windows-4090/qwen2.5-coder:14b`** | `5` (Ollama) | **Sisyphus-Junior (Ground Worker)**: specialized coding model, MCP tool use, syntax edits | `opencode run -m my-windows-4090/qwen2.5-coder:14b "task"` |
| **`groq/llama-3.3-70b-versatile`** | High | **Prometheus (Planner)**: fast parallel search, code diagnostics, reviews | `opencode run -m groq/llama-3.3-70b-versatile "task"` |
| **`opencode/deepseek-v4-flash-free`**| High | Low-stakes text processing, fast triage checks | `opencode run -m opencode/deepseek-v4-flash-free "task"` |

---

## 2. Incremental Grounding Protocol (The Handoff)

Before executing any delegated task, **OpenAgent must be grounded** to prevent context drift.

### Step 1: Pre-Flight Check (LSP Grounding)
Add the path of the Feature Tracker and Playbook directly to the target instructions so OpenAgent loads them at startup:
```bash
opencode run --prompt "Review the system rules in file:///home/jallred/Dev_Lab/Portfolio_Dev/FeatureTracker.md and BKM-015 in file:///home/jallred/Dev_Lab/Portfolio_Dev/AGY_TO_OPENAGENT_PLAYBOOK.md before starting."
```

### Step 2: Incremental Task Scoping
Do **not** hand over the entire sprint plan at once. Allocate tasks incrementally, starting with Phase 1 prototypes.

*   **Task 1 (Goal 1 Prototype):** Token Vocabulary mapping and configuration setup.
    ```bash
    opencode run "Implement Goal 1, Task 1.1: Define and write the token-to-adapter registry file 'HomeLabAI/config/role_tokens.json' matching the nodes configured in infrastructure.json."
    ```

---

## 3. Communication & Execution Loop

```
  ┌────────────────────────────────────────────────────────────┐
  │ 1. Ground & Delegate (Gemini CLI)                          │
  │    - Set task card in SPRINT_PLAN_SPR_36_0.md              │
  │    - Run target opencode command                           │
  └─────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
  ┌────────────────────────────────────────────────────────────┐
  │ 2. Execute & Log (OpenAgent Swarm)                         │
  │    - Code changes written directly to workspace            │
  │    - Local test run outputs written to command terminal   │
  └─────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
  ┌────────────────────────────────────────────────────────────┐
  │ 3. Forensic Review & Gate (Gemini CLI)                     │
  │    - Read git diffs of written code                       │
  │    - Run verification script or systemd checks             │
  │    - Certify task status in Master Plan                    │
  └────────────────────────────────────────────────────────────┘
```

---

## 4. Diagnostics & Troubleshooting Ledger

If OpenAgent crashes or fails to respond:

1.  **Check Service Status:**
    ```bash
    systemctl --user status opencode-core.service opencode-proxy.service
    ```
2.  **Inspect Logs for Context Blowup:**
    If logs show `Session too large to compact`, verify that `.opencodeignore` is active in `~/Dev_Lab/.opencodeignore` and excludes the target folders.
3.  **Kill Stuck Sessions:**
    If the coordinator hangs on a background agent:
    ```bash
    systemctl --user restart opencode-core.service
    ```
    Always start a **fresh session** (TUI or CLI) after a service restart to avoid context carryover.

4.  **Directory Context (Ignoring `.venv`):**
    Always launch OpenAgent from the root `/home/jallred/Dev_Lab` folder (not within subdirectories). The root contains the authoritative `.opencodeignore` which excludes heavy `.venv/` libraries. Launching from subdirectories bypasses ignores, causing context blowouts.

5.  **Model Selection for Logic Diffs:**
    Use `opencode/deepseek-v4-flash-free` for coding logic and complex refactoring. Smaller models (like `omnicoder-9b`) are prone to path hallucinations and syntax failures.

6.  **Complex Tasks (Silent Exits):**
    For multi-phase changes (e.g., parsing + scoring + ranking), do not delegate the entire logic block in a single prompt. Slice the instruction card into atomic steps:
    *   *Step A:* Implement parser and utilities.
    *   *Step B:* Implement core algorithm.
    *   *Step C:* Implement verification test suite.
    This prevents the model from reading files and exiting silently due to context/reasoning bounds.

---

## 5. Live Verification Guide (Restoring Workspace Tools)

### The Crash Cause
The Gemini CLI language server failed to start because the database migration `MIGRATION_ID_POPULATE_PROJECT_UPDATED_AT` panicked on a nil pointer dereference inside the summaries store initialization. This caused the CLI to fall back to a restricted safe mode (preventing workspace tools from loading).

### The Fix Applied
1.  We manually added the panicked migration ID to the list of completed migrations in `/home/jallred/.gemini/config/.migrated`:
    ```text
    MIGRATION_ID_POPULATE_PROJECT_UPDATED_AT
    MIGRATION_ID_SIDECAR_USER_CONFIG_BYPASS
    ```
2.  This instructs the language server to bypass the broken migration step.

### Restoring Your Active Terminal Session
To reload the language server and restore your `Dev_Lab` workspace tools:
1.  Exit your current `agy` CLI shell or VS Code/editor session.
2.  Launch a fresh shell or restart the editor.
3.  The language server will boot cleanly, skip the migrations, load `Dev_Lab`, and re-expose all MCP tools and indexers.

---

## 6. Playbook Protocol Refinement (Swarm Pain Points)

Based on recent integration tests, follow these strict execution guardrails:
1.  **Deadlock Prevention (Ollama Concurrency)**: Ensure `"maxConcurrency": 5` is defined in `opencode.json` for the local 4090. If set to `1`, parallel subagent requests to Ollama will freeze the model.
2.  **Lint-Gated Commits**: Subagents are strictly prohibited from committing code if the verification check (`ast.parse` or `pytest`) fails. Breaking syntax in the codebase violates DNA integrity.
3.  **DNA Grounding**: Subagents must actively check the `feature_dna` and `behavioral_dna` collections via ChromaDB before proposing code changes to avoid clobbering active architectural rules.
4.  **No-Hallucination Prompts**: Avoid leaving prompts open-ended. Always embed explicit `MUST DO` / `MUST NOT DO` constraints so local models do not lose context or hallucinate user instructions.
5.  **Session Naming Rules**: The first prompt of any new session must explicitly start with `SESSION: Sprint XX Story YY — Phase Z` to ensure the session is properly indexed with a clear title instead of generic "New session" or "Greeting".
6.  **VRAM Inversion Strategy**: Evaluate if the local 4090 VRAM should be inverted: instead of running heavy orchestrators locally (which suffer high latency and context limits), utilize cloud endpoints for orchestration and reservation, and load local models (like `qwen2.5-coder`) primarily for *heavy code generation/refactoring*. Evaluate if coding models still require tool usage or if they can rely on unified diff patches.
