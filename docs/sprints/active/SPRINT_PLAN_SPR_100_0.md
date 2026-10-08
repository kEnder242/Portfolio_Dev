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
| **ANCHOR-12** | Speculative Triage Inference Lead Calibration (`FEAT-586` / `BKM-079`) | Live Characterization | `✅ DONE` | Story 100.8: Calibrated $t_{\text{warmed}}=0.20\text{s} \to W_{\text{lead}}=0.40\text{s}$ via parallel differential model ($W_{\text{lead}} > t_{\text{air}} - t_{\text{vllm}}$); isolated EWMA estimators in `speculative_triage.py`. |
| **ANCHOR-13** | HyDE Turn Isolation & Multi-Turn Context Leak Fix (`FEAT-640` / `FEAT-437`) | Live Intercom Feedback | `STAGED` | Story 100.9: Enforce `ContextScope.TURN` on HyDE synthesis, purge prior turn context, and pass explicit `request_id`. |
| **ANCHOR-14** | Defeature `CASUAL` Vibe via Prompt Comment (Preserve Plumbing) (`FEAT-640`) | User Turn 2.2 | `STAGED` | Story 100.10: Comment out `CASUAL` line in `cognitive_hub.py#L1486` prompt string while retaining Python fast-path plumbing. |
| **ANCHOR-15** | Mandatory Brain Information Gatekeeper & Complete Deletion of Sprint 32 Brief (`FEAT-635`) | User Turn 4 | `STAGED` | Story 100.11: Make Stage 1 Brain Gatekeeper mandatory for technical queries; completely delete 68-sprint-old `_distill_strategic_brief()` (commit `15b4705`) and retire `_run_brain_leg()`. |
| **ANCHOR-16** | Pinky Critic Scorecard (Single-Pass WHY Reasoning + Spoken Retort) (`FEAT-406` / `FEAT-470`) | User Turn 2.3 / 2.4 | `STAGED` | Story 100.12: Align `build_critic_prompt` and `eval_schema`, eliciting technical `reasoning` and in-character spoken `retort`, keeping debug scalar visible. |
| **ANCHOR-17** | Cloud Delegation Baseline & Model Invocation Probe (`FEAT-649` / `BKM-071`) | Swarm Audit | `STAGED` | Story 100.13: Verify cloud delegate dispatch executes with designated cloud models, babysit logs at regular intervals, and enforce Playbook Calibration protocol. |
| **ANCHOR-18** | Triage Voting & In-Line / Hover Timestamp Feedback UI (`FEAT-638`) | User Turn 2.1 | `STAGED` | Story 100.14: Whitelist triage in `intercom_v2.js`, inject `voteable_sources` from `infrastructure.json` via `build_site.py`, and relocate buttons to `.msg-header` hover (0 extra lines). |
| **ANCHOR-19** | Re-Purge Vestigial `internal=True` Masking in Adherence to `FEAT-361` (`FEAT-361`) | User Turn 3 | `STAGED` | Story 100.15: Abolish silent token suppression (`stream_source = None`) in `nodes/loader.py`; route intermediate tokens to dedicated channels without gagging. |
| **ANCHOR-20** | Oracle Adversarial Pre-Pass on Phase 4 & Legacy Regression Audit (`BKM-061`) | Operator Directive | `✅ DONE` | Story 100.8B: Genuine Cloud Oracle pass executed via `delegate.py --oracle` (Session `ses_ee7ce694effequXShiSXcZD0cN`, OpenRouter Nemotron-120B / Free Tier, 54,632 tokens). Adversarial findings blended into `ORACLE_REVIEW_SPRINT_100.md`. |

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

#### Story 100.8 — Speculative Triage Inference Lead Calibration
* **Feature Anchor:** `[FEAT-586]` / `[BKM-079]`
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Status:** `✅ DONE`
* **Why:** The previous static 1.0s lead wait caused unnecessary 1s sluggishness on every turn, misinterpreting the lead requirement as waiting for full completion rather than providing an asynchronous head start. Furthermore, EWMA estimators shared across speculative engines caused metric cross-talk.
* **How:**
  1. Calibrate warm lead time to $W_{\text{lead}} = 0.40\text{s}$ using the parallel differential model ($W_{\text{lead}} > t_{\text{air}} - t_{\text{vllm}}$ with $t_{\text{air}}=1.70\text{s}$, $t_{\text{vllm}}=1.50\text{s}$), ensuring oMLX wins $\ge 90\%$ of races when warm while vLLM works in parallel.
  2. Isolate EWMA latency trackers per candidate engine in `speculative_triage.py`.
  3. Author `Portfolio_Dev/field_notes/triage_inference_calibration.md` and update `FEAT-586` spec in `features.html`.
* **Proof:** Verified in `HomeLabAI/src/logic/speculative_triage.py` (commit `d5334ea`), tests passing, and documentation updated (`96d8e8b`).


---

### Phase 4: Multi-Turn Conversation Hardening, Triage Feedback & Critic Retort Architecture (`[SWARM:LOCAL]` / `[SWARM:CLOUD]`)

#### 📋 Comprehensive Forensics & Context Analysis Report (Verbatim Operational Record)

```markdown
### ⚓ BKM-077: Tracked Conversational Ledger

| Anchor ID | Topic / Item | Origin | State | Target File(s) / Surface | Assigned Owner |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ANCHOR-13** | HyDE Turn Isolation & Multi-Turn Context Leak Fix | Turn Trace 3 | `STAGED` | `HomeLabAI/src/logic/cognitive_hub.py` | `[SWARM:LOCAL]` |
| **ANCHOR-14** | Defeature `CASUAL` Vibe via Prompt Comment (Preserve Plumbing) | User Turn 2.2 | `STAGED` | `HomeLabAI/src/logic/cognitive_hub.py#L1486` | `[SWARM:LOCAL]` |
| **ANCHOR-15** | Mandatory Brain Information Gatekeeper & Complete Deletion of Sprint 32 Brief | User Turn 4 | `STAGED` | `HomeLabAI/src/logic/cognitive_hub.py` | `[SWARM:LOCAL]` |
| **ANCHOR-16** | Extend Critic Single-Pass Scorecard (Semantic WHY Reasoning + Spoken Retort) | User Turn 2.3 / 2.4 | `STAGED` | `HomeLabAI/src/nodes/pinky_critic_persona.py` | `[SWARM:LOCAL]` |
| **ANCHOR-17** | Cloud Delegation Baseline & Model Invocation Probe | Swarm Audit | `STAGED` | `HomeLabAI/src/tests/delegate.py`, `oh-my-openagent.json` | `[SWARM:CLOUD]` |
| **ANCHOR-18** | Triage Voting & In-Line / Hover Timestamp Feedback UI | User Turn 2.1 | `STAGED` | `Portfolio_Dev/field_notes/intercom_v2.js`, `build_site.py` | `[SWARM:CLOUD]` |
| **ANCHOR-19** | Re-Purge Vestigial `internal=True` Masking in Adherence to `FEAT-361` | User Turn 3 | `STAGED` | `HomeLabAI/src/nodes/loader.py`, `cognitive_hub.py` | `[SWARM:LOCAL]` |

---

### 2.1: Triage Voting & In-Line Hover UI ([ANCHOR-14])

#### 2.1.1: Regex & Baked Config for Voteable Sources
* **Case-Insensitive Regex:** Matching `/triage/i` (or `/lab|triage/i`) in `intercom_v2.js` will immediately capture all triage variants (`Lab (Triage)`, `Deep Thought (Triage)`, `System (Triage)`) across different engines.
* **Baked Config via `build_site.py`:** Rather than hardcoding the whitelist in client-side JavaScript, we define `voteable_sources: ["pinky", "brain", "thought", "triage", "lab"]` in `HomeLabAI/config/infrastructure.json`. During `build_site.py`, this list is injected into `intercom_v2.js` as `const VOTEABLE_SOURCES = [...]`. This ensures full single-source-of-truth parity.

#### 2.1.2: Zero-Line Hover / In-Line Placement
Moving `.resp-fb` into `.msg-header` directly adjacent to `.msg-time` completely eliminates the extra vertical line. The voting buttons (`👍 👎`) will render with subtle opacity or reveal on message hover:
```css
.msg-header { display: flex; align-items: center; justify-content: space-between; }
.msg-header .resp-fb { opacity: 0.35; transition: opacity 0.15s ease-in-out; margin-left: 8px; }
.intercom-msg:hover .msg-header .resp-fb { opacity: 1.0; }
```

---

### 2.2: Defeaturing `CASUAL` via Prompt Comment ([ANCHOR-15])

We preserve 100% of the underlying Python plumbing for `CASUAL` (handling `vibe == "CASUAL"`, fast-path brevity, clamps, and telemetry) completely intact in the code, but **comment out the line in the prompt string** so the LLM classifier never sees it as an option:

In `HomeLabAI/src/logic/cognitive_hub.py#L1486`:
```python
             "• 6 CORE ARCHETYPES (vibe & domain):\n"
             # [DEFEATURED - Sprint 100]: Preserve plumbing, but exclude from active classifier prompt:
             # '  1. CASUAL: Conversational pleasantries, small talk ("hi", "hello") -> vibe="CASUAL", domain="unknown".\n'
             '  2. WYWO: Standup briefs or overnight activity inquiries...\n'
```
Because the LLM never sees `CASUAL` in its prompt choices, it will never classify incoming greetings into that mode, but no plumbing is destroyed if we decide to re-tune and re-enable it later.

---

### 2.3 & 2.4: Pinky Critic — Scorecard WHY & Retort ([ANCHOR-16])

#### Recommendation: Extend What We Have (Single-Pass Structured Judge Evaluation)
Pinky should NOT make a split decision and then scramble to invent a post-hoc rationalization. Filling out the scorecard must capture the **WHY** in that very same single turn.

The reason it collapsed into `"No\n\nNo"` was not because the scorecard concept is flawed, but because:
1. `build_critic_prompt()` asked for `cartoon_retort` and `critique_suggestions`.
2. `eval_schema` forced `score`, `reasoning`, `slop_found`, and `retort`.
3. Neither contained schema descriptions or prompt instructions, so the 3B model treated `reasoning` and `retort` as boolean string flags (`"No"`).

#### The Extension Plan:
We keep the single-pass structured evaluation, but provide explicit semantic definitions in both prompt and schema:
* **`score` (integer 1-5):** Telemetry scalar for backpressure tracking (kept visible in debug telemetry per user request).
* **`reasoning` (string):** The **WHY** — an analytical technical assessment directly addressing whether Brain accurately answered the user's specific query without off-topic hallucinations.
* **`retort` (string):** Pinky's **Judge Reply** spoken directly into the conversation (e.g., *"Narf! Brain, you're quoting 2015 PECI tap registers when Jason specifically asked for regular expressions!"*).
* **`slop_found` (bool):** Boilerplate detection.

The Critic's conversational output into the room will be Pinky's `retort` accompanied by the `reasoning`, functioning as a true conversational judge.

---

### 3: The `internal=True` History & Censorship Waffle Forensics

#### 1. The Sprint Where We Purged Internal
In **Sprint 29 (May 21, 2026)**, we codified **`[FEAT-361]` NUKE INTERNAL MASKING (100% Transparency)**:
> *"Remove the ability for any node to be silenced or hidden... Remove `is_internal` and `internal` parameters. We wanted every inter-node whisper visible."*

#### 2. The Sprint Where It Got Folded Back In
In **Sprint 32 (`Portfolio_Dev/docs/sprints/archive/SPRINT_PLAN_SPR_32_0.md:211-215`)**, this exact issue was documented as **"Goal 1: The Censorship Waffle ([FEAT-361] vs V5)"**:
> *"The Drift: During the V5 FastMCP rewrite, we 'waffled.' To solve a UI stuttering issue, `internal=True` was lazily re-added to the Hub's `think` tool calls. The Consequence: This gagged the MCP nodes, preventing them from transmitting telemetry to the Foyer's `/stream_ingest` endpoint. The Hub became the 'censor' and the sole broadcaster. When the Hub routing logic had a flaw, Brain and Pinky disappeared entirely from the UI."*

Task 14.1 was assigned to remove it, but it was only partially stripped. `internal: bool = False` remained embedded in `nodes/loader.py#L181` and `cognitive_hub.py#L817`.

#### 3. Operational Direction
1. **Never use `internal=True` to silence nodes:** Gagging token streams creates the hidden text trap.
2. **Triage Belongs in the Conversation:** Triage is a core conversational milestone. It will stream openly to the chat pane (`channel: "chat"`) with visible reasoning, parameters, and up/down vote buttons.
3. **Use Channels for Separation:** Scratchpads or low-level handshakes route to `crosstalk` (status bar) or `insight` (Right Console), but never silenced into a black hole.
```

---

## 📝 Operator Directives & Mid-Flight Guidance (BKM-006 §7)

1. **Mid-Flight Sprint Pause & Regression Halt:** Immediately halt in-flight Story 100.9 execution to insert an adversarial Oracle pre-pass across each story.
2. **Oracle Adversarial Story Audit Mandate:** Review each Phase 4 story (100.9 through 100.15) to uncover legacy regressions, obsolete architectural assumptions (e.g. Sprint 32 leftovers), and alignment with latest certified designs (Sprint 90+ Critic, Sprint 95 Triage, Sprint 96 Two-Mice Handover).
3. **Employer Persona Quarantine:** Guarantee zero employer/job persona terms (e.g. PECI, MSR, platform scars) leak into general lab prompts or code logic. Career validation history belongs exclusively in quarantined `WIS-xxx` personal reference Gems.
4. **Heads Down Execution Authorization:** Upon completion and certification of the Oracle audit pass, proceed into autonomous Heads Down execution (BKM-006) across the approved story backlog.

---

### Phase 4 Stories: Hardening & Refinement

#### Story 100.8B — Oracle Adversarial Pre-Pass on Phase 4 & Legacy Regression Audit
* **Feature Anchor:** `[BKM-061]` / `[BKM-007]` / `[FEAT-640]`
* **Assigned Owner:** `[SWARM:ORACLE]`
* **Status:** `✅ DONE`
* **Why:** The operator requested an adversarial Oracle pass to review each Phase 4 story (100.9 through 100.15) before execution, explicitly to catch legacy regressions and obsolete code patterns (such as Sprint 32 leftovers like `_distill_strategic_brief()`, `PECI/MSR` text, `internal=True` Censorship Waffle, and vestigial gags in `loader.py`) and verify 100% alignment with latest designs (Sprint 96 Two-Mice Handover, Sprint 90+ Coherence Critic, Sprint 95 Triage Taxonomy, BKM-015 Semantic Anchors, BKM-062 Anti-Green-Lie).
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files & Line Anchors):**
    - `Portfolio_Dev/docs/sprints/active/SPRINT_PLAN_SPR_100_0.md`
    - `Portfolio_Dev/docs/sprints/active/ORACLE_REVIEW_SPRINT_100.md`
  * **Anchor 2 (Verification Command & Literal Test Battery):**
    - Command: `HomeLabAI/.venv/bin/python3 HomeLabAI/src/tests/delegate.py --sprint 100 --story 100.8B --title "Phase 4 Oracle Adversarial Audit & Legacy Regression Sweep" --reference Portfolio_Dev/docs/sprints/active/SPRINT_PLAN_SPR_100_0.md --target "Portfolio_Dev/docs/sprints/active/ORACLE_REVIEW_SPRINT_100.md" --details "Adversarially audit Stories 100.9 through 100.15 for legacy regressions, outdated architectural assumptions, and target file alignment" --oracle`
    - Assertions: Comprehensive audit matrix compiled in `ORACLE_REVIEW_SPRINT_100.md`; all CRITICAL and HIGH severity findings resolved or remediated in story specs prior to execution.
  * **Anchor 3 (Verbatim Code Anchors & Injection Specs):**
    Audit checklist across each story:
    - Story 100.9: Validate HyDE turn scope isolation (`ContextScope.TURN`) vs `_process_node_stream` parameters.
    - Story 100.10: Validate `CASUAL` defeature preserves Python enum / fast-path plumbing while purging from prompt choices.
    - Story 100.11: Validate total excision of `_distill_strategic_brief()`, elimination of `_run_brain_leg()`, zero `PECI/MSR` strings, and mandatory Stage 1 Brain Gatekeeper on 100% of technical queries.
    - Story 100.12: Validate Pinky Critic single-pass scorecard schema (`score`, `reasoning`, `retort`, `slop_found`) matches `build_critic_prompt` and `evaluate_grounding`.
    - Story 100.13: Validate Cloud pre-flight probe verifies genuine cloud model invocation (OpenRouter/Cohere) and log babysitting protocol.
    - Story 100.14: Validate triage vote whitelist in `infrastructure.json`, `build_site.py`, and hover UI in `intercom_v2.js`.
    - Story 100.15: Validate complete removal of `stream_source = None` gags in `loader.py` per FEAT-361.
  * **Anchor 4 (Silicon Invariants & DNA Links):**
    - Invariant: Zero silent fallback to dead code; zero employer persona leakage outside `WIS-xxx` Gems; 100% alignment with active system state.
    - DNA Links: `[BKM-061]`, `[BKM-007]`, `[BKM-015]`, `[BKM-062]`, `[FEAT-640]`.
* **Verification Log:** Dispatched to Cloud Oracle via `delegate.py --oracle` (Session `ses_ee7ce694effequXShiSXcZD0cN`, OpenRouter Nemotron-120B / Free Tier, 54,632 total tokens, 5,386 reasoning tokens). External Cloud Oracle independently audited Stories 100.9–100.15, catching declarative drift in `config/triage_policy.json` and mandating global searches for `stream_source = None` and `_distill_strategic_brief`. Blended findings committed to `ORACLE_REVIEW_SPRINT_100.md`.

---

#### Story 100.9 — Multi-Turn Turn Isolation & HyDE Context Poisoning Remediation
* **Feature Anchor:** `[FEAT-640]` / `[FEAT-437]` / `[BKM-015]`
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Status:** `COMPLETED`
* **Verification Log:** Dispatched to SWARM:LOCAL via `delegate.py --mode local` on Node KENDER Windows RTX 4090 (`my-windows-4090`). Atlas conducted surgical worker Sisyphus-Junior to patch `cognitive_hub.py` (threading `request_id` and passing `scope=ContextScope.TURN` on HyDE `_process_node_stream`) and author companion TDD unit tests in `test_feat437_resolve_hyde_vector.py`. Certified via pytest (13 passed in 0.55s) with live daemon synchronization verified. Committed in HomeLabAI `bc38f7b`.
* **Why:** In multi-turn sessions, HyDE synthesis in `resolve_hyde_vector` defaulted to `ContextScope.LONG` because its `source_name` (`"Pinky (HyDE)"`) lacked the substring `"triage"`. Consequently, previous debate context (`[PREVIOUS_DEBATE]: User: hi`) was injected into Pinky's HyDE synthesis prompt. Pinky latched onto the previous turn's greeting, hallucinated `{"is_casual": true, "hyde_vector": ""}`, and suppressed RAG retrieval on technical queries.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files & Line Anchors):**
    - `HomeLabAI/src/logic/cognitive_hub.py#L2465-L2485` (`resolve_hyde_vector`)
    - `HomeLabAI/src/logic/cognitive_hub.py#L1001-L1028` (`_process_node_stream`)
  * **Anchor 2 (Verification Command & Literal Test Battery):**
    - Command: `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_feat437_resolve_hyde_vector.py HomeLabAI/src/tests/test_triage_context_squeeze.py -v`
    - Assertions: `test_resolve_hyde_vector_turn_scope_isolation`, `test_hyde_synthesis_does_not_ingest_previous_debate`.
  * **Anchor 3 (Verbatim Code Anchors & Injection Specs):**
    ```python
    # In HomeLabAI/src/logic/cognitive_hub.py::resolve_hyde_vector
    async for token in self._process_node_stream(
        "pinky",
        HYDE_SYNTHESIS_PROMPT,
        triage_context,
        "Pinky (HyDE)",
        tools=[],
        temperature=0.2,
        max_tokens=150,
        scope=ContextScope.TURN,      # [FEAT-640] Mandatory single-turn isolation
        request_id=request_id,         # [FEAT-640] Forward explicit turn request ID
    ):
    ```
  * **Anchor 4 (Silicon Invariants & DNA Links):**
    - Invariant: Zero `[PREVIOUS_DEBATE]` tokens present in Stage 2 HyDE prompt; vector synthesis operates strictly on active query + intent.
    - DNA Links: `[FEAT-640]`, `[FEAT-437]`, `[BKM-015]`.

---

#### Story 100.10 — Defeature `CASUAL` Vibe via Prompt Comment & Align 9-Vibe Taxonomy
* **Feature Anchor:** `[FEAT-640]` / `[BKM-015]`
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Status:** `COMPLETED & CERTIFIED`
* **Verification Log:** Dispatched to SWARM:LOCAL via `delegate.py --mode local` on Node KENDER Windows RTX 4090 (`my-windows-4090`). Atlas staged blueprints via `jit_stage()` and dispatched surgical worker Sisyphus-Junior on M5 Air. Junior commented out `CASUAL` from active prompt choices in `cognitive_hub.py#L1487`, updated fallback assertions in `test_triage_engine.py` (L578, L632) to `SOCRATIC`, and AGY sanitized line 1490 to eliminate employer persona leakage per Oracle review. Certified via `test_triage_engine.py` (79/79 passed in 0.24s). Live gate passed (`[LIVE_GATE: PASSED]`); committed in HomeLabAI `3b1972d`.
* **Why:** The triage prompt still listed `1. CASUAL: Conversational pleasantries...`, causing greetings to be classified as `vibe: "CASUAL"`, which bypassed RAG and downstream analysis. Defeaturing `CASUAL` in the prompt prevents the LLM from choosing it while preserving all underlying Python fast-path handling.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files & Line Anchors):**
    - `HomeLabAI/src/logic/cognitive_hub.py#L1485-L1492` (`triage_mode_context`)
    - `HomeLabAI/config/triage_policy.json`
  * **Anchor 2 (Verification Command & Literal Test Battery):**
    - Command: `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_triage_engine.py HomeLabAI/src/tests/test_triage_policy_loader.py -v`
    - Assertions: Assert `CASUAL` is not present in triage prompt options; greetings classify into `SOCRATIC` or general domain.
  * **Anchor 3 (Verbatim Code Anchors & Injection Specs):**
    ```python
    # In HomeLabAI/src/logic/cognitive_hub.py::triage_mode_context
    "• 6 CORE ARCHETYPES (vibe & domain):\n"
    # [DEFEATURED - Sprint 100 / FEAT-640]: Preserve Python plumbing, comment out from active prompt:
    # '  1. CASUAL: Conversational pleasantries, small talk ("hi", "hello") -> vibe="CASUAL", domain="unknown".\n'
    '  2. WYWO: Standup briefs or overnight activity inquiries...\n'
    ```
  * **Anchor 4 (Silicon Invariants & DNA Links):**
    - Invariant: Triage engine output `vibe` never equals `CASUAL` on live silicon turns; falls back to 9-vibe taxonomy.
    - DNA Links: `[FEAT-640]`, `[BKM-015]`.

---

#### Story 100.11 — Mandatory Stage 1 Brain Information Gatekeeper & Complete Deletion of Sprint 32 Brief
* **Feature Anchor:** `[FEAT-635]` / `[FEAT-489]` / `[BKM-015]`
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Status:** `IN-PROGRESS (Attempt 1b)`
* **Verification Log:**
  - **Attempt 1 (Fast-Halt Blocker):** Atlas inspected `cognitive_hub.py` via `jit_read` on Kender RTX 4090, identified 4 callsites and 2 sibling test dependencies for `_run_brain_leg` that were under-specified in the story plan. Obeying Law 6 (`Under-Specified Contract Blocker Mandate`), Atlas fast-halted without code mutations and emitted structured feedback in its `[HANDOVER REFLECTION]`.
  - **Attempt 1b (BKM-049 Tri-Loop Remediation):** AGY audited reflection and formulated the decoupled stub pattern: completely delete `_distill_strategic_brief()`, enforce Stage 1 Brain Gatekeeper on 100% of technical queries when `lead_node == 'brain'`, and retain `_run_brain_leg` as a clean pass-through stub so sibling tests and `both`-branch calls stay green. Staged and dispatched via `delegate.py --mode local`.
* **Why:** Originating in Sprint 32 (May 2026, commit `15b4705`), `_distill_strategic_brief()` is a 68-sprint-old dinosaur that hardcoded `"Extract specific platform anchors, validation targets, and known PECI/MSR scars."` In Turn 2, when interest was $< 0.70$, execution fell into the legacy `_run_brain_leg()` fallback, invoking this ancient relic and polluting Brain's output with off-topic PECI/MSR text. Rather than maintaining or patching this dead code, we completely delete `_distill_strategic_brief()`, retire `_run_brain_leg()`, and route 100% of technical queries through the modern Sprint 96 Brain Information Gatekeeper (`build_two_mice_stage_prompt(stage=1)`), making Stage 1 mandatory regardless of interest.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files & Line Anchors):**
    - `HomeLabAI/src/logic/cognitive_hub.py#L1831-L1885` (turn dispatch)
    - `HomeLabAI/src/logic/cognitive_hub.py#L2298-L2339` (complete deletion of `_distill_strategic_brief`)
    - `HomeLabAI/src/logic/cognitive_hub.py#L2622-L2790` (retirement of legacy `_run_brain_leg`)
  * **Anchor 2 (Verification Command & Literal Test Battery):**
    - Command: `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_brain_gatekeeper.py HomeLabAI/src/tests/test_two_mice_handover.py -v`
    - Assertions: `test_stage1_prompt_contains_gatekeeper_and_curator_instructions`, `test_mandatory_gatekeeper_low_interest_technical_query`, assert zero references to `_distill_strategic_brief` exist in codebase.
  * **Anchor 3 (Verbatim Code Anchors & Injection Specs):**
    ```python
    # In HomeLabAI/src/logic/cognitive_hub.py::process_message
    # [FEAT-635 / Sprint 100]: Mandatory Stage 1 Brain Information Gatekeeper
    if lead_node == "brain":
        # Stage 1 Brain Gatekeeper executes for ALL technical inquiries:
        stage1_success = await self._run_two_mice_handover(
            turn, focus_context=handover_context, shutdown_event=shutdown_event, request_id=request_id
        )
    ```
    Complete deletion:
    ```python
    # DELETED: def _distill_strategic_brief(self, raw_context, request_id="default"):
    # DELETED: def _run_brain_leg(...)
    ```
  * **Anchor 4 (Silicon Invariants & DNA Links):**
    - Invariant: Zero occurrences of `_distill_strategic_brief` or ungrounded `PECI/MSR` text in codebase or runtime logs.
    - DNA Links: `[FEAT-635]`, `[FEAT-489]`, `[BKM-015]`.

---

#### Story 100.12 — Pinky Coherence Critic Retort & Reasoning Scorecard Architecture
* **Feature Anchor:** `[FEAT-406]` / `[FEAT-470]`
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Status:** `STAGED`
* **Why:** In Turn 2, Pinky Critic emitted `"No\n\nNo"` because `build_critic_prompt()` and `eval_schema` had conflicting keys (`cartoon_retort` vs `retort`), and no field-level guidance existed. Pinky must generate a coherent single-pass scorecard containing both the analytical technical WHY (`reasoning`) and the spoken in-character judge reply (`retort`), with the `{ "score": ... }` scalar remaining visible as debug telemetry.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files & Line Anchors):**
    - `HomeLabAI/src/nodes/pinky_critic_persona.py#L91-L140` (`build_critic_prompt`)
    - `HomeLabAI/src/nodes/pinky_critic_persona.py#L292-L335` (`format_chat_delivery`)
    - `HomeLabAI/src/logic/cognitive_hub.py#L2175-L2295` (`evaluate_grounding`)
  * **Anchor 2 (Verification Command & Literal Test Battery):**
    - Command: `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_pinky_critic_persona.py -v`
    - Assertions: `test_critic_generates_grounded_reasoning_and_retort`, `test_format_chat_delivery_blends_retort_and_reasoning`.
  * **Anchor 3 (Verbatim Code Anchors & Injection Specs):**
    ```python
    # In HomeLabAI/src/nodes/pinky_critic_persona.py
    eval_schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "coherence_evaluation",
            "schema": {
                "type": "object",
                "properties": {
                    "score": {"type": "integer", "minimum": 1, "maximum": 5, "description": "1-5 grounding score"},
                    "reasoning": {"type": "string", "description": "1-sentence analytical critique explaining WHY the technical response succeeds or fails"},
                    "slop_found": {"type": "boolean", "description": "True if canned pleasantries or robotic boilerplate detected"},
                    "retort": {"type": "string", "description": "Witty in-character cartoon voice quip addressed directly to Brain as the conversational judge"},
                },
                "required": ["score", "reasoning", "slop_found", "retort"],
            },
        },
    }
    ```
  * **Anchor 4 (Silicon Invariants & DNA Links):**
    - Invariant: Critic delivers authentic spoken retort + reasoning to chat console; telemetry packet retains scalar score without throwing `"No\n\nNo"`.
    - DNA Links: `[FEAT-406]`, `[FEAT-470]`.

---

#### Story 100.13 — Cloud Delegation Baseline & Model Invocation Smoke Test
* **Feature Anchor:** `[FEAT-649]` / `[BKM-071]` / `[BKM-051]`
* **Assigned Owner:** `[SWARM:CLOUD]`
* **Status:** `STAGED`
* **Why:** Before dispatching frontend and UI modifications to the cloud tier, we must verify that recent local submodule updates, permission schema adjustments (`oh-my-openagent.json`), and JIT tool migrations have not perturbed the cloud execution path. Furthermore, we must confirm that cloud worker dispatches actually invoke designated cloud models (e.g. OpenRouter free-tier / Cohere Oracle) rather than silently falling back to local loops.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files & Line Anchors):**
    - `HomeLabAI/src/tests/delegate.py#L380-L450` (`dispatch_session`)
    - `Dev_Lab/oh-my-openagent.json` (agent definitions)
    - `Portfolio_Dev/docs/playbooks/OPENAGENT_HANDOVER_PLAYBOOK.md` (§7 Calibration Ledger & §8 Version Control Ground Truth)
  * **Anchor 2 (Verification Command & Literal Test Battery):**
    - Command: `python3 HomeLabAI/src/tests/delegate.py --sprint 100 --story 100.13 --title "Cloud Probe" --mode plan --target "Portfolio_Dev/field_notes/data/status.json"`
    - Assertions: Session initializes on port 4097; `delegation_ledger.jsonl` logs model identifier from cloud provider; 0 local VRAM thrashing on M5 Air.
  * **Anchor 3 (Verbatim Code Anchors & Injection Specs):**
    - Active Monitoring Protocol: During cloud execution, the orchestrator MUST inspect `delegation_ledger.jsonl` and OpenCode daemon logs at regular 30s intervals:
      ```bash
      tail -n 20 HomeLabAI/logs/delegation_ledger.jsonl
      journalctl --user -u codex -n 30 --no-pager
      ```
    - Grounding & Fix Mandate: If cloud execution fails or model routing drifts, the agent MUST ground itself in `OPENAGENT_HANDOVER_PLAYBOOK.md` (§0–§8) before touching code, and record every diagnostic fix and parameter adjustment in §7 (Calibration Ledger) at the end of the file.
  * **Anchor 4 (Silicon Invariants & DNA Links):**
    - Invariant: Cloud worker sessions resolve to external cloud endpoints; zero Google API token consumption (`[BKM-071]`); verified entry in §7 Calibration Ledger if fixes are applied.
    - DNA Links: `[FEAT-649]`, `[BKM-071]`, `[BKM-051]`, `[INS-043]`.

---

#### Story 100.14 — Lab Triage Intercom Feedback & In-Line Hover Timestamp Voting UI
* **Feature Anchor:** `[FEAT-638]` / `[BKM-077]`
* **Assigned Owner:** `[SWARM:CLOUD]`
* **Status:** `STAGED`
* **Why:** In Turn 1, the user downvoted crosstalk because Lab Triage lacked vote buttons. The whitelist in `intercom_v2.js` excluded `triage` and `lab`, and feedback buttons took up an extra line of vertical space.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files & Line Anchors):**
    - `Portfolio_Dev/field_notes/intercom_v2.js#L346-L358`, `L420-L428`
    - `HomeLabAI/config/infrastructure.json` (`voteable_sources`)
    - `Portfolio_Dev/field_notes/build_site.py#L140-L160`
  * **Anchor 2 (Verification Command & Literal Test Battery):**
    - Command: `python3 Portfolio_Dev/field_notes/build_site.py`
    - Assertion: Verify `intercom_v2.js` in `www_deploy/` receives `const VOTEABLE_SOURCES` including `triage`, and hash parity test passes.
  * **Anchor 3 (Verbatim Code Anchors & Injection Specs):**
    ```javascript
    // In Portfolio_Dev/field_notes/intercom_v2.js
    const isVoteableSource = VOTEABLE_SOURCES.some(src => new RegExp(src, 'i').test(source));
    if (channel === 'chat' && !isRestoringHistory && isVoteableSource && text) {
        respFbHtml = '<div class="resp-fb"><button type="button" class="fb-btn" data-fb="UP" onclick="submitResponseFeedback(this)">👍</button><button type="button" class="fb-btn" data-fb="DOWN" onclick="submitResponseFeedback(this)">👎</button></div>';
    }
    // Place into .msg-header adjacent to timestamp:
    msg.innerHTML = `
        <div class="msg-header">
            <span class="msg-time">${time}</span>
            <span class="msg-source ${sl}">[${displaySource}]</span>
            ${respFbHtml}
        </div>
        <div class="msg-body">${formattedText}</div>
        ${metaHtml}
    `;
    ```
  * **Anchor 4 (Silicon Invariants & DNA Links):**
    - Invariant: Triage messages in Intercom UI render in-line `👍 👎` buttons; 0 extra vertical lines consumed.
    - DNA Links: `[FEAT-638]`, `[BKM-077]`.

---

#### Story 100.15 — Re-Purge Vestigial `internal=True` Masking in Adherence to `FEAT-361` Transparency Mandate
* **Feature Anchor:** `[FEAT-361]`
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Status:** `STAGED`
* **Why:** In Sprint 29, `[FEAT-361]` mandated 100% transparency. During the V5 FastMCP rewrite, `internal=True` was re-introduced to solve UI stutter, but created the "hidden text trap" where nodes are silenced at the physical MCP layer (`stream_source = None`). Internal reasoning must be routed to dedicated consoles (`channel: "insight"` or `crosstalk`), never gagged.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files & Line Anchors):**
    - `HomeLabAI/src/nodes/loader.py#L208-L245` (`stream_source` logic)
    - `HomeLabAI/src/logic/cognitive_hub.py#L815-L820` (`waterfall_queue.put`)
  * **Anchor 2 (Verification Command & Literal Test Battery):**
    - Command: `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_triage_engine.py HomeLabAI/src/tests/test_two_mice_handover.py -v`
    - Assertion: Verify no node streams are silenced at the MCP bridge; packets carry valid channel tags (`chat`, `insight`, `crosstalk`).
  * **Anchor 3 (Verbatim Code Anchors & Injection Specs):**
    ```python
    # In HomeLabAI/src/nodes/loader.py::think
    # [FEAT-361 / Sprint 100]: Never gag node telemetry; preserve channel-based routing
    stream_source = self.name
    async for token in self.generate_response(...):
        self._broadcast_token(token, stream_source, request_id=request_id)
    ```
  * **Anchor 4 (Silicon Invariants & DNA Links):**
    - Invariant: Zero silent drops in `loader.py`; 100% of node generation tokens stream to Foyer with appropriate channel tags.
    - DNA Links: `[FEAT-361]`.

---

## 📜 Real-Time Execution Ledger (Sprint Log)
*Governed by `[BKM-081]` (The Sprint Append Ledger Protocol). Timely chronological trace of execution milestones, forensic lessons, and verification certificates.*

### [2026-10-07 20:45 PDT] — Story 100.8B: Oracle Adversarial Pre-Pass on Phase 4
- **Assigned Tier & Silicon:** `[SWARM:ORACLE]` (OpenRouter `nvidia/nemotron-3-super-120b-a12b:free`, 54,632 tokens).
- **Status:** `✅ COMPLETED & CERTIFIED`
- **Forensic Delta / Code Modified:** Audited Stories 100.9–100.15 against active codebase. Compiled risk matrix in `ORACLE_REVIEW_SPRINT_100.md`.
- **Forensic Insights & Lessons Learned:** Flagged legacy Sprint 32 PECI/MSR scars in `_distill_strategic_brief()`, HyDE turn scope leakage (`ContextScope.LONG`), and declarative policy drift in `triage_policy.json`. Generated actionable remediation checklists for Phase 4.
- **Live Gate Status:** `[LIVE_GATE: PASSED]`

### [2026-10-07 22:30 PDT] — Story 100.9: Multi-Turn Turn Isolation & HyDE Context Poisoning Remediation
- **Assigned Tier & Silicon:** `[SWARM:LOCAL]` (Node KENDER Windows RTX 4090 $\to$ M5 Air).
- **Status:** `✅ COMPLETED & CERTIFIED`
- **Forensic Delta / Code Modified:** `HomeLabAI/src/logic/cognitive_hub.py` (enforced `scope=ContextScope.TURN` and threaded `request_id` in `resolve_hyde_vector` and `_process_node_stream`); authored companion TDD tests in `HomeLabAI/src/tests/test_feat437_resolve_hyde_vector.py`.
- **Verification Evidence:** `pytest test_feat437_resolve_hyde_vector.py` $\to$ **13 passed in 0.55s**.
- **Forensic Insights & Lessons Learned:** Multi-turn HyDE defaulted to `ContextScope.LONG` because `source_name="Pinky (HyDE)"` lacked `"triage"`, injecting previous turn banter into vector generation and suppressing RAG. Threading explicit single-turn scope completely cured context poisoning.
- **Live Gate Status:** `[LIVE_GATE: PASSED]` (Committed in HomeLabAI `bc38f7b`).

### [2026-10-08 01:05 PDT] — Story 100.10: Defeature CASUAL Vibe & 9-Vibe Taxonomy Alignment
- **Assigned Tier & Silicon:** `[SWARM:LOCAL]` (Node KENDER Windows RTX 4090 $\to$ M5 Air).
- **Status:** `✅ COMPLETED & CERTIFIED`
- **Forensic Delta / Code Modified:** `cognitive_hub.py#L1487` (commented out CASUAL prompt choice with `[DEFEATURED]` tag); `test_triage_engine.py` (L578, L632 updated fallback assertions to `SOCRATIC`); sanitized line 1490 to eliminate employer persona leakage.
- **Verification Evidence:** `pytest test_triage_engine.py` $\to$ **79 passed in 0.24s** (full battery 126 passed, 10 skipped).
- **Forensic Insights & Lessons Learned:** The Oracle review suggested setting `enabled: false` in `triage_policy.json`. Auditing the reflection per `BKM-049` revealed that disabling it in policy broke `test_triage_policy_loader.py::test_production_has_all_nine_vibes`. Defeaturing CASUAL belongs in the LLM prompt choices, keeping the underlying 9-vibe policy contract intact.
- **Live Gate Status:** `[LIVE_GATE: PASSED]` (Committed in HomeLabAI `3b1972d`).

### [2026-10-08 01:16 PDT] — Story 100.11: Mandatory Stage 1 Brain Gatekeeper & Complete Deletion of Sprint 32 Brief
- **Assigned Tier & Silicon:** `[SWARM:LOCAL]` (Node KENDER Windows RTX 4090 $\to$ M5 Air).
- **Status:** `🔄 IN-PROGRESS (Attempt 1b)`
- **Forensic Delta / Code Modified:** In Attempt 1, Atlas inspected `cognitive_hub.py` via `jit_read`, detected 4 callsites and 2 sibling test dependencies for `_run_brain_leg`, and strictly halted per Law 6 (`Under-Specified Contract Blocker Mandate`) to escalate to AGY without mutating code.
- **Remediation Formulated (Attempt 1b):** AGY formulated the decoupled stub pattern: completely excise `_distill_strategic_brief()`, enforce Stage 1 Brain Gatekeeper (`_run_two_mice_handover`) on 100% of technical queries when `lead_node == 'brain'`, and retain `_run_brain_leg` as a clean decoupled pass-through stub so sibling tests and `both`-branch calls stay green.
- **Live Gate Status:** `[LIVE_GATE_PENDING: daemon=8765 endpoint=/status probe=pytest test_brain_gatekeeper.py test_two_mice_handover.py -v]`



