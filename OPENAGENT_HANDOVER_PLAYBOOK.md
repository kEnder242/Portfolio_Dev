# 📖 OpenAgent Handover & Co-Pilot Playbook (Sprint 36)

This playbook establishes the protocol for allocating tasks, grounding local models, and validating execution when coordinating between **Antigravity** (Gemini-driven co-pilot) and **OpenAgent** (Groq/Ollama-driven autonomous coding swarm).

---

## 1. Model & Swarm Allocation Matrix

Based on our active configuration check, we allocate the following resources to minimize token costs and ensure high-fidelity coding:

| Provider/Model | Concurrency | Primary Use-Case | Invocation Command |
| :--- | :--- | :--- | :--- |
| **`my-windows-4090/omnicoder-9b`** | `1` (Local) | Heavy code generation, local refactors, file editing | `opencode run -m my-windows-4090/omnicoder-9b "task"` |
| **`groq/llama-3.3-70b-versatile`** | High | Fast search, code diagnostics, parallel review | `opencode run -m groq/llama-3.3-70b-versatile "task"` |
| **`opencode/deepseek-v4-flash-free`**| High | Low-stakes text processing, fast triage checks | `opencode run -m opencode/deepseek-v4-flash-free "task"` |
| **`google/gemini-3.5-flash`** | Dedicated | PMC strategic planning, design approvals, forensic gates | *Current CLI active session* |

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
