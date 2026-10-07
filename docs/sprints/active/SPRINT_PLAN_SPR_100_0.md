# Sprint 100 — JIT Architecture, Parallel Orchestration & Lab Hardening
**Status:** ACTIVE / HEADS DOWN
**Created:** 2026-10-06
**Mode:** Bicameral Hybrid — Phase 1 & 2 directly authored via `[AGY:PRIMARY]` (per BKM-049 Section 3: harness cannot self-delegate); Phase 3 certified via `[SWARM:LOCAL]`.
**Preceded by:** Sprint 99 (Run B merged `ff2daf4` / `85d399a`)
**FEAT Tags:** `[FEAT-641]` (Stale lock reaper), `[FEAT-648]` (Persistent JIT cache & file-scoped invalidation), `[FEAT-649]` (Multi-tier agent choreography DAG & JIT tool protocol).

---

## 🧭 Executive Summary & Core Invariant

Sprint 100 crystallizes the lessons of Sprint 99 into a unified Just-In-Time (JIT) execution architecture across the Federated Lab:
1. **The Tool Namespace Law:** Disentangles long-term database storage (`dna_*` targeting ChromaDB) from dynamic execution tools (`jit_*` serving L2 conductor inspection and L3 worker recall).
2. **Context Isolation Firewall:** Reaffirms that `task()` is not redundant overhead, but the essential context firewall that keeps the L2 conductor pristine (<2,000 tokens on KENDER 4090) while allowing L3 disposable surgical workers to absorb dirty test-fix loops.
3. **Persistent Local Caching:** Relocates volatile context digests from `/tmp` into `.jit_cache/` (strictly gitignored) with granular, file-scoped `mtime` invalidation.
4. **Sub-Inference Observability:** Prevents the "sub-inference trap" where heavy M5 Air neural map-reduce is hidden from telemetry by logging structured audit receipts into `.jit_cache/sub_inference_ledger.jsonl`.
5. **Zero Service Sprawl:** Retains the single monolithic systemd daemon (`lab-attendant.service`), establishing clean modular Python boundaries between ignition/hardware management (`src/v5/ignition/manager.py`) and API/WebSocket routing (`src/v5/foyer/router.py`).

---

## ⚓ BKM-077: ANCHOR_TRACK Ledger

| ID | Topic / Objective | Origin | State | Target Milestone |
| :--- | :--- | :--- | :--- | :--- |
| **ANCHOR-01** | RDP Connection Rejection Recovery & GDM Autologin | Triage 1 | `✅ DONE` | Resolved via GDM restart; port 3389 listening. Sentry design documented. |
| **ANCHOR-02** | Stale Lockfile Purge (Dead PID Reaper) | Triage 2 | `✅ DONE` | Implemented in `standalone_accountability_watchdog.py` (`b384a15`). |
| **ANCHOR-03** | Intercom Deploy Drift & State Case Normalization | Triage 3 / Item 3 | `✅ DONE` | Resolved in `intercom_v2.js`, synced to `www_deploy`, hash-guarded in `build_site.py` (`fd2906a` / `90d8fb9`). |
| **ANCHOR-04** | Tool Namespace Migration (`clara-dna_read` $\to$ `jit_*`) | Item 4 / 8 | `✅ DONE` | Story 100.2: FastMCP canonical tools & backwards-compatible aliases registered in `clara_dna_mcp_server.py`. |
| **ANCHOR-05** | Relocate Context Cache from `/tmp` to Gitignored `.jit_cache/` | Item 5 | `✅ DONE` | Story 100.3: `.jit_cache/` created, gitignored, `mtime` invalidation & `evict_cached_summary` active. |
| **ANCHOR-06** | Sub-Inference Receipt Ledger (M5 Air Token Observability) | Item 6 | `✅ DONE` | Story 100.4 & 100.5: `sub_inference_ledger.jsonl` logged by `context_prewarmer.py`, blended into `delegate.py`. |
| **ANCHOR-07** | OpenCode Permissions & Conductor Prompt Ingestion | Item 4 / 7 | `✅ DONE` | Story 100.4: `oh-my-openagent.json`, `AGENTS_L2.md`, `AGENTS_L3.md`, `test_subversive_prompt.py` verified 6/6 green. |
| **ANCHOR-08** | In-Flight Sovereign Delegation Shakedown Pass | Item 9 | `✅ DONE` | Story 100.6: Certified live on KENDER 4090 + M5 Air (`ses_eeb08d8f0ffes9iYH0Pe36rPed`). |
| **ANCHOR-09** | Modular Python Boundaries (Core vs Router vs Hooks) | Item 10 | `✅ DONE` | Verified single service `lab-attendant.service` maintains `ignition/manager.py` + `foyer/router.py` boundaries. |
| **ANCHOR-10** | Codify `BKM-077: ANCHOR_TRACK` Protocol in Protocols.md | Item 11 | `✅ DONE` | Codified in `HomeLabAI/docs/Protocols.md` (`[FEAT-649]`). |
| **ANCHOR-11** | JIT One-Shot Surgical Contract & Anti-Spiral Orchestration | Post-Sprint Alignment | `✅ DONE` | Story 100.7: Codified in `FEAT-655`, `BKM-078`, `AGENTS_L3.md`, `AGENTS_L2.md`. |

---

## 🛠️ Unified Tool Flow & Permission Matrix

The canonical mapping governing the tool migration across the 4-tier stack:

| Current Tool (MCP) | Canonical Name | Flow Role | Permission Profile (`oh-my-openagent.json`) | Purpose / Silicon Surface |
| :--- | :--- | :--- | :--- | :--- |
| `clara-dna_read` | **`jit_read`** | **Consume** (Fetch) | `atlas`: allow \| `sisyphus-junior`: deny | High-density AST structural blueprint + M5 Air semantic map (<400 tokens). |
| `clara-dna_locate_grounding` / `locate_path` | **`jit_locate`** | **Consume** (Fetch) | `atlas`: allow \| `sisyphus-junior`: allow | Context-clean path & symbol discovery without dumping code bodies. |
| `stage_research` | **`jit_stage`** | **Publish** (Save) | `atlas`: allow \| `sisyphus-junior`: deny | L2 saves pre-computed patch blueprints & diff directives for L3. |
| `research` | **`jit_research`** | **Consume** (Recall) | `atlas`: allow \| `sisyphus-junior`: allow | L3 retrieves staged blueprints, AST anchors, or AGENTS_L3 operational rules. |
| `failure_whisperer` | **`jit_diagnose`** | **Consume** (Fetch) | `atlas`: allow \| `sisyphus-junior`: allow | Isolates pytest traceback assertion failures into an atomic 2-line diagnosis. |
| `handoff_checkpoint` | **`jit_checkpoint`** | **Publish** (Save) | `atlas`: allow \| `sisyphus-junior`: allow | Commits status & modified artifacts to `delegation_ledger.jsonl`. |
| `safe_patch` *(retained)* | **`safe_patch`** | **Publish** (Execute) | `atlas`: allow \| `sisyphus-junior`: allow | Surgical, regex-tolerant disk patcher with automated syntax linting. |
| `query_dna`, `get_protocol`, `list_collections` | **`dna_*`** | **DNA DB** | Read-only across all tiers | Semantic search against ChromaDB long-term memory archive. |

---

## 🔄 The Multi-Tier Agent Choreography DAG

```text
Orchestrator (L1 / delegate.py)
   │
   ├─► Pre-Warm (M5 Air Neural Map-Reduce) ──► Populates .jit_cache/
   │
   └─► Atlas (L2 Conductor on KENDER 4090)
         │
         ├─► jit_read(file_paths) ───────► Inspects AST outlines (<400 tokens)
         ├─► jit_locate(pattern) ────────► Finds module paths
         ├─► jit_stage(blueprint) ───────► Saves AST anchors & diff directives
         │
         └─► task(category='coder') ─────► Dispatches Sisyphus-Junior (L3 on M5 Air)
               │
               ├─► jit_research(file) ───► Ingests staged blueprint without wandering
               ├─► safe_patch(diff) ─────► Applies surgical code changes to disk
               ├─► bash("pytest ...") ───► Runs isolated unit/mock verification
               │     │
               │     └─► [On failure] jit_diagnose(traceback) ──► Re-attempts patch
               │
               └─► jit_checkpoint() ────► Logs completion & modified artifacts
```

---

## 📦 Detailed Sprint Stories

### Phase 1: Lab Recovery & UI Drift (`[AGY:PRIMARY]`)

#### Story 100.1 — Intercom Deploy Sync, State Case Normalization & Ledger Clean
* **Why:** `www_deploy/intercom_v2.js` is 4 FEATs behind `field_notes/intercom_v2.js` (missing FEAT-638 feedback, FEAT-590 DNA proposals, and send-lock logic). Foyer returns uppercase `"state": "OFFLINE"` while JS tested lowercase `"offline"`, preventing the maintenance overlay from rendering. Additionally, the crashed nightly forge left a stale `Age: 999h` sentinel in `nightly_forge_state.json`.
* **How:**
  1. Sync `Portfolio_Dev/field_notes/intercom_v2.js` to `www_deploy/intercom_v2.js` and `www_deploy/assets/intercom_v2.js`.
  2. In `intercom_v2.js`, normalize state comparisons to case-insensitive: `(data.state || '').toLowerCase() === 'offline'`.
  3. In `build_site.py`, add a file hash guard asserting that `www_deploy/intercom_v2.js` matches `field_notes/intercom_v2.js`.
  4. Reset `HomeLabAI/run/nightly_forge_state.json` to clear the `Age: 999h` sentinel.
* **Proof:** Live test on http://localhost:8765 status poll; `build_site.py` passes cleanly.

---

### Phase 2: JIT Migration & Infrastructure (`[AGY:PRIMARY]`)

#### Story 100.2 — FastMCP Tool Registrations & Namespace Aliasing
* **Why:** Disentangles execution tools from database retrieval.
* **How:**
  1. In `AcmeLab/src/clara_dna_mcp_server.py`:
     - Register `jit_read` (with `read` / `clara-dna_read` aliases for backwards compatibility).
     - Register `jit_locate` (aliasing `locate_path` / `locate_grounding`).
     - Register `jit_stage` (aliasing `stage_research`).
     - Register `jit_research` (aliasing `research`).
     - Register `jit_diagnose` (aliasing `failure_whisperer`).
     - Register `jit_checkpoint` (aliasing `handoff_checkpoint`).
     - Retain `safe_patch` and `clara-dna_safe_patch`.
     - Retain `dna_*` tools for pure ChromaDB operations.
* **Proof:** Direct MCP tool invocation verification using `clara_dna_mcp_server.py` in-process probe.

#### Story 100.3 — Persistent JIT Cache Relocation & File-Scoped Invalidation
* **Why:** Ephemeral `/tmp` files force cold restarts and require constant sweeps.
* **How:**
  1. Define canonical cache root: `Dev_Lab/.jit_cache/`.
  2. Add `.jit_cache/` to `.gitignore` in `Dev_Lab/`, `HomeLabAI/`, and `AcmeLab/`.
  3. In `HomeLabAI/src/v5/cognition/context_prewarmer.py`:
     - Redirect `CONTEXT_CACHE_PATH` from `/tmp/clara_context_cache.json` to `.jit_cache/clara_context_cache.json`.
     - Implement file-scoped invalidation: store file `mtime` alongside digest.
     - On read, if disk `mtime > cached_mtime`, regenerate.
  4. In `safe_patch`: trigger cache eviction for the specific modified target file (`cache.pop(file_path, None)`).
  5. In `jit_stage` / `jit_research`: move notes path from `/tmp/clara_conductor_notes.json` to `.jit_cache/clara_conductor_notes.json`.
* **Proof:** Run unit test creating, reading, patching, and verifying cache invalidation in `.jit_cache/`.

#### Story 100.4 — OpenCode Permission Profiles & Operational Contracts
* **Why:** OpenCode enforces tool access through declarative permission blocks. If a tool is renamed without updating permissions, OpenCode blocks the agent with `deny`.
* **How:**
  1. Update `Dev_Lab/oh-my-openagent.json`:
     - Grant `atlas`: `jit_read: allow`, `jit_locate: allow`, `jit_stage: allow`, `jit_research: allow`, `jit_diagnose: allow`, `jit_checkpoint: allow`, `safe_patch: allow`.
     - Grant `sisyphus-junior`: `jit_read: deny`, `jit_locate: allow`, `jit_stage: deny`, `jit_research: allow`, `jit_diagnose: allow`, `jit_checkpoint: allow`, `safe_patch: allow`.
     - Maintain existing aliases during the transition window.
  2. Update `Dev_Lab/AGENTS_L2.md` and `Dev_Lab/AGENTS_L3.md`:
     - Update tool manifest tables and Laws 1/2 to reference `jit_*` tools.
  3. Update `HomeLabAI/src/tests/test_subversive_prompt.py`:
     - Assert `jit_read` is denied for L3 worker.
* **Proof:** Unit test suite in `test_subversive_prompt.py` passes 100%.

#### Story 100.5 — Sub-Inference Token Receipt Ledger in `delegate.py`
* **Why:** Map-reduce operations on M5 Air must be visible in telemetry to eliminate the sub-inference opacity trap.
* **How:**
  1. In `context_prewarmer.py`: when M5 Air performs map-reduce, append an audit entry to `.jit_cache/sub_inference_ledger.jsonl`:
     `{"timestamp": ..., "engine": "m5_air", "prompt_tokens": N, "completion_tokens": M}`.
  2. In `HomeLabAI/src/tests/delegate.py`: in `record_swarm_telemetry()`, read and aggregate unrecorded receipts from `.jit_cache/sub_inference_ledger.jsonl`, blending local silicon tokens into overall story telemetry.
* **Proof:** Verify that running `prewarm_files()` generates a ledger entry and `record_swarm_telemetry()` logs blended tokens.

---

### Phase 3: Live Verification & Certification (`[SWARM:LOCAL]`)

#### Story 100.6 — Sovereign Delegation Shakedown Pass
* **Why:** Live certification of the new JIT architecture under live silicon endpoints (KENDER 4090 + M5 Air).
* **How:**
  1. Execute a real story delegation via `delegate.py --story 100.6 --mode local`.
  2. Verify Atlas invokes `jit_read`, stages via `jit_stage`, dispatches `task()`, and Sisyphus-Junior consumes `jit_research`, applies `safe_patch`, and calls `jit_checkpoint`.
  3. Confirm telemetry correctly captures outer + sub-inference tokens.
* **Proof:** `✅ CERTIFIED (100% GREEN)`
  - Dispatch completed in 829.0s on KENDER 4090 + M5 Air (`ses_eeb08d8f0ffes9iYH0Pe36rPed`).
  - Full DAG verified: `jit_read` $\to$ `jit_stage` $\to$ `task(category='quick')` $\to$ `jit_research` $\to$ `safe_patch` (2 atomic edits) $\to$ `bash` pytest (1 passed in 0.08s) $\to$ `jit_checkpoint` $\to$ Atlas re-verify $\to$ `LIVE_GATE: PASSED`.
  - Recorded as `SUCCESS` in `delegation_ledger.jsonl`. Verification cmd passed cleanly.

#### Story 100.7 — JIT One-Shot Contract & Anti-Spiral Conductor Flow
* **Feature Anchor:** `[FEAT-655]` / `[BKM-078]` / `[INS-042]` / `[WIS-482]`
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Status:** `✅ DONE`
* **Why:** In multi-tier swarms, letting open-weights surgical workers ($L_3$) attempt recursive self-fixing when tests fail triggers the Waffle Trap (`[INS-042]`) and quadratic context bloat ($O(N^2)$ accumulation). Workers must operate as disposable single-shot execution probes that diagnose in context and report recommendations to $L_2$ before terminating cleanly.
* **How:**
  1. Codify `jit_one_shot` contract in `AGENTS_L3.md` (patch $\to$ test $\to$ diagnose $\to$ recommend $\to$ exit).
  2. Codify anti-spiral orchestration rules in `AGENTS_L2.md` (Atlas evaluates recommendations, detects circular spirals, and dispatches fresh pristine retries).
  3. Register `FEAT-655` in `FeatureTracker.md` and `BKM-078` in `Protocols.md`.
* **Proof:** Verified in `AGENTS_L3.md`, `AGENTS_L2.md`, `FeatureTracker.md`, `Protocols.md`.
