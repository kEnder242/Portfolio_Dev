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
| **Primary Local Ground Worker (KENDER)** | Node KENDER / Windows 4090 (Port 11434 Ollama: `Qwen3-14B-GGUF`) for fast 75 tok/s code editing with 14.8 GB VRAM cache | Subagent `task()` primary target (`sisyphus-junior`) |
| **Primary Local Reasoning Node (M5 Air)** | Mac M5 Air (Port 8000 MLX: `Qwen3.8-27B-4bit`) for deep architectural thought & speculative triage | Subagent target for deep reasoning |
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

### 3.4 Local Silicon Token Overhead & Metal Memory Ceilings
- **The Physical Memory Constraint (24GB Apple Silicon):** When running a 27B quantized model (e.g. `Qwen3.8-27B` at 21.2 GB resident weights), the attention SDPA prefill buffer for contexts larger than ~4k tokens exceeds the 24.46 GB macOS Metal allocation cap (`iogpu.wired_limit_mb`), triggering `AI_APICallError: oMLX prefill memory guard rejected this prompt`.
- **Worker Realignment to Kender 4090:** To avoid Metal memory exhaustion, coding worker execution (`sisyphus-junior` and `unspecified-low`) is resident on Kender (RTX 4090 + Ollama). `Qwen3-14B-GGUF` takes only 9.2 GB VRAM, leaving **14.8 GB of VRAM for KV caching** at 75 tok/s.

### 3.5 Subagent Tool Scoping & The ICM Ballast Tax ([BKM-051])
- **The 24.5k Token Ghost:** OpenCode automatically injects all registered MCP tool schemas into every subagent prompt. When ICM was enabled with 31 tools + CLaRa + LSP, worker base prompts ballooned to **24,488 input tokens** before reading any code.
- **The Mandatory Tool Denial Law:** Execution workers (`sisyphus-junior`, `hephaestus`) MUST explicitly deny non-essential tools in `oh-my-openagent.json`:
  ```json
  "permission": {
    "edit": "allow",
    "icm_*": "deny",
    "websearch_*": "deny",
    "codegraph_*": "deny",
    "question": "deny"
  }
  ```
  This collapses worker prompt overhead from 24.5k down to **$< 1,500$ tokens**, reducing prefill time on local silicon from 90 seconds to 2 seconds.

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
- **Story 901 Reflection:** ` from the response text (line 375-379) and stores to ICM. But the **active model identifier** is NOT explicitly echoed anywhere in delegate.py's output. The message payload requests a model but there's no assertion that the response actually ran on that model.  This is the architecture plan. Let me write it now (read-only — no edits).  # Story 901 — Atlas Shakedown: Architecture Plan  ## 1. ROOT CAUSE & ARCHITECTURAL IMPACT  **Root cause (the shakedown target):** There is a **declared-vs-actual model identity gap** between the swarm's *configured* model routing and what the delegation engine *actually requests*. Story 901 exists to surface and verify this by echoing the **active model identifier** and **agent identity** through a live `Atlas` delegation.  Three distinct identity sources diverge:  | Source | Declared Atlas model | Loc | |---|---|---| | `oh-my-openagent.json` → `agents.atlas.model` | `opencode/hy3-free` | `~/.config/opencode/oh-my-openagent.json:26` | | `opencode.json` → `agent["Atlas - Plan Executor"].model` | `opencode/hy3-free` | `~/.config/opencode/opencode.json:33` | | `delegate.py` → `msg_dict.model` **(hardcoded)** | **`opencode/big-pickle`** | `HomeLabAI/src/tests/delegate.py:311-313` |  **The shakedown finding:** `delegate.py` **hardcodes** the REST dispatch request to `{"providerID": "opencode", "modelID": "big-pickle"}` at lines 311–313, **ignoring** both the `--agent atlas` persona and the configured `hy3-free` primary. Every delegated Atlas/Sisyphus task therefore *requests* `big-pickle`, not the audited primary `hy3-free`. The live "active model identifier" Atlas reports will reflect whatever the engine resolves — which may be `big-pickle` (via runtime fallback) even though the config declares `hy3-free`.  **Architectural impact:** - **Verification integrity (LIVE-IS-GOD, BKM-034):** The audit doc (Section 4) and smoke test (Story 999) assert Atlas/Sisyphus route to `hy3-free`, but the dispatch layer undermines this. Story 901 is the live probe that reveals the truth. - **Config drift:** Three serialization points (JSON configs × 2 + `delegate.py` payload) can diverge; `delegate.py` is the single source that *ignores* config entirely. - **No model-echo assertion:** `delegate.py` prints the execution report + handover reflection but never asserts the response actually ran on the requested/declared model. The "active model identifier" is not currently echoed programmatically.  ---  ## 2. TARGET FILES & EXACT SYMBOL ANCHORS  **Primary shakedown invocation (read-only, live):** - `HomeLabAI/src/tests/delegate.py` — `delegate()` function, `msg_dict` (lines 310–313), `AGENT_MAP` (lines 174–179), handover reflection extraction (lines 375–379).  **Config truth anchors (verification references, not edits for this plan):** - `~/.config/opencode/oh-my-openagent.json` — `agents.atlas` block (lines 25–36). - `~/.config/opencode/opencode.json` — `agent["Atlas - Plan Executor"]` (lines 32–34). - `/home/jallred/Dev_Lab/Portfolio_Dev/OPENAGENT_MODEL_AUDIT_AUG2026.md` — Section 4 swarm matrix, Section 9 smoke test. *(Note: story references `OPENAGENT_MODEL_AUG2026.md` — **file does not exist**; actual audit doc is `OPENAGENT_MODEL_AUDIT_AUG2026.md`.)*  **Edit target note:** Story 901 is a **shakedown/echo**, not a doc-edit. The "edit target = reference" is a placeholder; the true artifact produced is a **live verification report** capturing the echoed model ID + agent identity.  ---  ## 3. PROPOSED FIX OPTIONS  ### Option A — Live Echo Probe (verbatim dispatch, diagnose only) Dispatch through the existing path and *observe* the echo without touching code: ``` python3 HomeLabAI/src/tests/delegate.py \   --story 901 --title "Atlas Shakedown" \   --reference /home/jallred/Dev_Lab/Portfolio_Dev/OPENAGENT_MODEL_AUDIT_AUG2026.md \   --agent atlas --mode plan \   --details "Echo the active model identifier and agent identity" \   --dir /home/jallred/Dev_Lab ``` Assistant instructs Atlas to return `providerID/modelID` + its persona in the handover reflection.  - ✅ **Zero risk**, pure diagnosis; surfaces the real resolved model. - ❌ **Passive** — does not fix the `big-pickle` hardcode; echo proves whatever the current (possibly wrong) path yields. - **Trade-off:** Best as a **baseline shakedown** to measure current truth before any change.  ### Option B — Fix dispatch to honor config + add model-echo assertion In `delegate.py`, replace the hardcoded `msg_dict["model"]` (lines 311–313) with the persona-resolved value, and assert the echoed model in the completion handler (lines 355–399). - `modelID`: derive from the resolved `agent`/category primary (default `hy3-free`), not hardcoded `big-pickle`. - Add a regex assertion on the execution report for `providerID/modelID` (mirroring the handover-reflection extraction at 375–379) so the shakedown **fails loudly** if the echoed model ≠ declared model.  - ✅ **Root-cause fix** (LIVE-IS-GOD compliance); restores config-as-truth; makes future shakedowns self-asserting. - ❌ **Behavior change** to the dispatch engine — must be regression-tested against cloud quota + fallback chain (interacts with `runtime_fallback`, `model_fallback: true`). - **Trade-off:** More involved; changes the RPC contract. **Recommended for a follow-on exec story**, not the shakedown itself.  ### Recommendation **Phase 1 = Option A** (live echo probe = genuine "Atlas Shakedown"), **Phase 2 = Option B** routed to a separate execution story after findings are certified.  ---  ## 4. VERIFICATION STRATEGY & RISK RATING  | Check | Method | Pass criteria | |---|---|---| | Engine reachable | `delegate.py` pre-flight `check_cloud_quota()` (port 4097) | Session created; exit 0 | | Agent identity echoes | Handover reflection text contains `[Atlas]` / "Plan Executor" persona | Present in `/tmp/delegate_story_901.log` | | Active model identifier echoes | Report line contains `opencode/<modelID>` | Matches resolved model | | Declared-vs-actual delta | Cross-check echoed ID vs `oh-my-openagent.json:26` vs `delegate.py:312` | Delta documented (expect `big-pickle` hardcode, `hy3-free` declared) | | ICM trail | Reflection auto-ingested (`delegate.py:374-393`) | `icm recall "story-901"` returns entry |  **Risk rating: LOW–MEDIUM.** - LOW: Option A is read-only, no file edits, no state transitions (per BKM-034 delegation gate, plan mode). - MEDIUM: Discovered `big-pickle` hardcode is a latent correctness issue; if any fix is applied carelessly it could break the fallback chain (400/429/500 retry, `runtime_fallback`). Do NOT fix in Story 901 — isolate to a dedicated exec story with full regression.  **God-view gate:** Before certifying, cross-reference `00_FEDERATED_STATUS.md` and store findings to ICM under `context-portfolio_dev` / `errors-resolved` per AGENTS.md memory mandate.  ---  ## HANDOVER REFLECTION  The prompt gave a sprint-plan path (`.../OPENAGENT_MODEL_AUG2026.md`) that does not exist on disk — the real audit doc is `OPENAGENT_MODEL_AUDIT_AUG2026.md`. That forced a detour to locate and read the correct file, plus the JSON configs and `delegate.py`, to reconstruct what "shakedown + echo" actually means. What was missing from the handoff: (1) the fact that this is a **live echo/verification** story rather than a doc-edit, and (2) any pointer to the **hardcoded `big-pickle` model in `delegate.py`**, which is the single most load-bearing detail for a model-identity shakedown. A one-line addition — *"asserting/echoing the model the dispatch actually requests; note `delegate.py` hardcodes `opencode/big-pickle` at lines 311–313"* — would have collapsed the investigation to a single read.
- **Story 1 Reflection:** The prompt was clean and surgically scoped — the sprint plan had already done the hard work of specifying exact queries, collection targets, and field schemas, so the execution was mostly a transcription task with grounding work on `ground_truth_summary` and `expected_keywords` fields. What tripped me up slightly was the absence of explicit `ground_truth_summary` content in the sprint plan — the queries were specified verbatim, but the summary answers had to be inferred from the codebase context (ABMD, LabDNARouter, DCGM, RAPL MSR register maps, etc.), meaning I was authoring domain knowledge, not just filling in a template. The single prompt improvement: **include a one-liner `ground_truth_summary` per anchor in the sprint plan spec itself** — this would eliminate the inference step and make the story a pure mechanical write rather than a knowledge-authoring task.
- **Story 2 Reflection:** The biggest friction point was the **import names in the spec being incorrect** — `LabDNARouter` doesn't exist as a class export from `lab_dna_router.py`, and `TraversalDispatcher` isn't needed in evaluate_rag.py at all. This required a codegraph exploration to discover the actual exports (`get_collection_priorities`, `filter_candidate_context`). The single change that would have saved time: provide the actual function names from the target modules rather than assumed class names, since `evaluate_rag.py` delegates to `get_context()` which already handles collection routing internally.
- **Story 4 Reflection:** The grep anchors in the spec (line ranges like "Lines 40-50, 80-90") were off by several lines from the actual code — the file had shifted from prior edits, so I had to re-scan the actual file contents rather than trust the line numbers. The spec also referenced a `safe_load_json()` function that doesn't exist in utils.py, making the verification command unrunnable as-written — I substituted a working import check. The single change that would've made this faster: **providing the actual bare-except grep output with exact line matches** instead of approximate ranges, since the codebase is clearly mid-migration and line numbers are unstable.
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
