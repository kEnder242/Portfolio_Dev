# Sprint 100 — JIT Architecture, Parallel Orchestration & Lab Hardening
**Status:** PLANNING — Brainstorm items 4-11 captured (no stories). Stories 100.1 (intercom) and 100.2 (lock reaper ✅ DONE) staged.
**Created:** 2026-10-06
**Preceded by:** Sprint 99 (Run B merged `ff2daf4` / `85d399a`)
**FEAT tag:** FEAT-641 (stale lock reaper) committed `b384a15`

---

## Overview

This sprint captures a cluster of architectural ideas emerging from the Sprint 99 experience:
- The `dna_read()` → JIT namespace unification
- Moving JIT cache off tmp
- Token accounting for apples-to-apples cloud/local cost comparison
- IPC tools as the face of parallel agentic coordination
- Reverse/publish tools for context broadcasting
- Multi-story parallel orchestration via Atlas

> [!NOTE]
> These are brainstorm items. No stories, no implementation tasks. Scope and feasibility TBD.

---

## Item 4 — Rename `dna_read()` → `jit_read()` and Audit the `dna_*` Namespace

**Motivation:** The `clara-dna_read` tool name is opaque. The DNA acronym refers to the persistence layer, not the retrieval mechanism. `jit_read` (Just-In-Time) better captures the *behavior*: fetching live, contextual memory at inference time.

**Investigation needed:**
- Does the `jit` prefix trigger the DNA ambient hook in `ambient_recall.py`? The hook currently listens for tool names starting with `dna_`. A prefix rename breaks that trigger unless the hook is updated to match `jit_*` OR a short alias without the 'c' is added.
- Inventory all `clara-dna_*` tool names: `read`, `query_dna`, `get_protocol`, `safe_patch`, `locate_grounding`, `stage_research`, `research`, `failure_whisperer`, `handoff_checkpoint`, `locate_path`.
- Which of these are internal-facing (infra) vs agent-facing (interface)? Only agent-facing ones warrant a JIT rename.

**Proposed mapping (draft):**
| Old | New | Notes |
|-----|-----|-------|
| `dna_read` | `jit_read` | Retrieve DNA card by ID — JIT at call time |
| `query_dna` | `jit_query` | Search DNA by pattern |
| `locate_grounding` | `jit_ground` | Pull grounding header |
| `research` | `jit_research` | ← also item 7, dual use |
| `safe_patch` | `dna_patch` | Write-side; keep `dna_` as publish verb? |
| `stage_research` | `dna_stage` | Publish to staging |
| `handoff_checkpoint` | `dna_checkpoint` | Write-side |

**Open question:** Do we need to distinguish `jit_*` (reads context) vs `dna_*` (publishes context)? See Item 8.

---

## Item 5 — Move JIT Cache from `/tmp` to Persistent Cache Directory

**Motivation:** `/tmp` is ephemeral. After a delegation or subagent, the cache is gone, forcing fresh DNA reads on every delegation. This adds latency and token cost. A persistent cache dir eliminates the "clean tmp between delegations" requirement.

**Current state:**
- `context_prewarmer.py` uses `/tmp/active_warm_sessions.json`
- Cache invalidation: currently based on session token rotation (each new delegation = new session = cold start)

**Design questions:**
1. **Where?** Candidate: `HomeLabAI/run/jit_cache/` (alongside `run/*.lock`) or `AcmeLab/.jit_cache/`. Must survive service restarts but be gitignored.
2. **Invalidation:** What makes a JIT read "stale"? Candidates:
   - DNA card's own `updated_at` timestamp (per-card TTL)
   - Global cache bust on `safe_patch` writes (any write invalidates affected keys)
   - Max TTL: 1h hard cap regardless of write activity
3. **Cross-delegation sharing:** If subagents share a cache dir, concurrent writes need locking. Use atomic rename or `fcntl` like the forge lock.
4. **Cleanup:** Without `/tmp` auto-wipe, need an explicit eviction policy. Tie to accountability watchdog at 06:00.

---

## Item 6 — Token Tracking Inside Tools for Apples-to-Apples Cost Comparison

**Motivation:** Current A/B (cloud vs local) comparisons only count "outer" tokens (the LLM's input/output). But `jit_read` itself calls an embedding model or vector search — those are NOT free. Without accounting for tool-side tokens, cloud vs local comparisons are misleading.

**Scope:**
- Any MCP tool that calls an LLM (embedding, rerank, generation): `jit_read`, `jit_query`, `research`, `stage_research`, `failure_whisperer`
- Anything calling Ollama or VLLM internally counts as "local tokens"
- Anything calling OpenAI/Anthropic API from within a tool counts as "cloud tokens"

**Proposed mechanism:**
1. Each tool response includes an optional `_tokens` field in its JSON: `{"output": ..., "_tokens": {"local": 412, "cloud": 0}}`
2. Orchestrator (Atlas or delegate.py) accumulates across the delegation turn
3. End-of-turn report appends token accounting to the handoff JSON

**Comparison table goal:**
| Metric | Cloud (AGY) | Local (Ollama) |
|--------|-------------|----------------|
| Outer tokens | N | M |
| Tool tokens (local) | 0 | T |
| Tool tokens (cloud) | K | 0 |
| Total tokens | N+K | M+T |
| Wall time | Ws | Ls |

---

## Item 7 — IPC Tools as the Face of All Air & Cached Communications

**Motivation:** Parallel tool calling = parallel work. If coding tasks, research, and testing are exposed as tools, the orchestrator can fire them simultaneously. Right now, `delegate.py` serializes everything through a single call.

**Proposed tool surface:**
| Tool | Parallelizable? | Notes |
|------|----------------|-------|
| `jit_code` | ✅ Yes | Code a single file/function in isolation |
| `jit_patch` | ✅ Yes (if no dep) | Apply a targeted patch to one file |
| `jit_research` | ✅ Yes | Read-only DNA/web lookup |
| `jit_test` | ✅ Yes (read-only) | Run test suite for a module |
| `jit_debug` | ⚠️ Usually | May need serial if state-dependent |
| `jit_create_patch` | ✅ Yes | Generate diff from spec; no write |
| `dna_write` | ❌ No | DNA writes need coordination |
| `dna_patch` | ❌ No | Mutates shared state |

**Atlas as main orchestrator:**
- Atlas (L2) sees the full story backlog and decomposes into parallel `jit_*` tool calls
- L2 KV cache concern: multiple stories in parallel means very wide context. Is L2's KV cache large enough? Need empirical test.
- **Open question:** Can we do away with the `task()` write entirely if tool calls handle all side effects?

**Dependency management:**
- Atlas must track file-level write dependencies (can't parallelize two tools writing the same file)
- Story-level dependencies (Story B depends on Story A's output) block parallel scheduling
- Stories with no shared file writes can be fully parallel

---

## Item 8 — Reverse Tools: Publish vs. Consume (Two Sides of a Coin)

**Motivation:** Current tools are primarily *consumers* of context. We need *publishers* — tools that broadcast finished work back to the Air/DNA so subsequent reads are fresh.

**Taxonomy:**
```
CONSUME (read)          PUBLISH (write)
-----------             ----------------
jit_read       ←→      dna_write
jit_query      ←→      dna_index
jit_research   ←→      dna_stage
jit_ground     ←→      dna_anchor
```

**Naming convention options:**
1. **Verb-based:** `jit_*` = read/consume, `dna_*` = write/publish
2. **Tag-based:** `jitc_*` suffix for "commit" (write-back): `jitc_write`, `jitc_patch`
3. **Directional:** Arrow metaphor — `air_pull` vs `air_push`

**Open design question:** Should the agent explicitly call a publish tool after coding, or should `jit_code` auto-publish its output to a staging area? Auto-publish risks polluting DNA with draft work.

**Recommended approach (hypothesis):** Explicit two-phase:
1. `jit_code` → returns code artifact in response (no DNA write)
2. `dna_stage(artifact)` → publishes to staging for review
3. `dna_patch(staged_id)` → promotes staging to live DNA

---

## Item 9 — Double Down on Orchestrator: Multi-Story, Multi-File Parallel Coding

**Motivation:** If Atlas can manage dependencies, we can parallelize across stories within a sprint — not just across files within a story. This is the "federated parallel sprinting" concept.

**Key questions:**
1. **Can we code multiple files in parallel?** Yes, if files have no import dependency on each other. Atlas needs a dependency graph.
2. **Can we run multiple stories in parallel?** Yes, if story outputs don't feed into each other. Atlas needs story DAG.
3. **Does queuing up coding tasks leverage Air caching?** Hypothesis: yes — if all jit_code calls share a common context prefix (the sprint spec), the Air KV cache reuse is very high.
4. **Can we trust Atlas (L2) to manage dependencies?** L2 is smart enough if given a clear dependency manifest. The manifest itself is a DNA card.
5. **Is L2's KV cache too small for multi-story context?** Unknown — needs empirical test. Each story at high-detail level might be 8-16K tokens; 4 parallel stories = 32-64K context overhead.

**Orchestration model sketch:**
```
Atlas (L2, orchestrator)
├── Parallel batch 1 (no cross-deps):
│   ├── jit_code(story_A, file_1) 
│   ├── jit_code(story_A, file_2)  
│   └── jit_research(story_B, context)  
└── Serial gate (story_A output needed):
    ├── jit_test(story_A)
    └── jit_code(story_B, file_1)  ← depends on story_A result
```

**Risk:** If one parallel jit_code fails, partial writes may corrupt a story. Need transactional semantics (all-or-nothing per story).

---

## Triage Items (Live Issues — Sprint 99 Aftermath)

> [!CAUTION]
> Items below are live operational issues found at 02:41 PDT Oct 6. See forensic analysis in conversation.

### Triage 1 — RDP Not Connecting
- **Status:** `gnome-remote-desktop.service` is **active** (running since Oct 1). Service did NOT crash.
- **Root cause:** Port 3389 is NOT listening. GNOME Remote Desktop runs in user session context (via PAM/gdm), not the system service. During nightly VRAM quiesce, display session may have been disrupted.
- **Action:** RDP likely recovers when nightly forge completes and system re-stabilizes. Check again after 06:00. If persistent: `systemctl --user status gnome-remote-desktop` from a local terminal.

### Triage 2 — Accountability `FAIL`: Foyer OFFLINE + nightly_forge.lock Stale
**Root cause analysis:**

| Check | Expected | Actual | Verdict |
|-------|----------|--------|---------|
| Foyer Re-Ignition | ONLINE by 06:00 | `state=OFFLINE` (dead since 02:00:28) | 🔴 REGRESSION — Foyer did NOT re-ignite after nightly |
| Lock Cleanliness | nightly_forge.lock cleared | `DEAD PID 1870642, 240m old` | 🔴 REGRESSION — lock reaper NOT running |
| Nightly Forge | COMPLETED | `Status: RUNNING (Age: 999h)` | 🔴 REGRESSION — state ledger broken (shows 999h) |
| LoRA Training | COMPLETED | `FAILED` | 🔴 Likely consequence of forge crash/abort |
| Morning Round Table | critic > 0 | `Critic Score: 0.00` | 🔴 Consequence of Foyer OFFLINE |

**Forensic comparison vs prior work (FEAT-639):**
- FEAT-639 implemented `check_stale_locks()` in `standalone_accountability_watchdog.py` — **DETECTION works** (it correctly found the stale lock).
- FEAT-639 **did NOT implement lock reaping/cleanup**. The watchdog *reports* the stale lock but never *deletes* it. This is the gap.
- Foyer did not re-ignite: the nightly forge apparently crashed (PID 1870642 dead) without calling `record_nightly_completion()`, leaving the lock file alive and the state ledger in `RUNNING` state.
- The forge's `record_nightly_completion()` is only called on clean exit. A crash = leaked lock + corrupted state = `Age: 999h` sentinel.

**Sprint 100 candidate bug:** Add a `nightly_forge.lock` reaper to the accountability watchdog (delete stale DEAD-PID locks, not just detect them). Also add crash recovery: forge should register a systemd `ExecStopPost=` script to clean up locks on unexpected exit.

### Triage 3 — Intercom Send Lock NOT Working
**Root cause analysis:**

The send-lock code in `Portfolio_Dev/field_notes/intercom_v2.js` (lines 621-625) is **present in `field_notes`** but **STRIPPED from `www_deploy/intercom_v2.js`**.

```
diff Portfolio_Dev/field_notes/intercom_v2.js www_deploy/intercom_v2.js
621,625d571
<                 if (sendBtn) {
<                     sendBtn.disabled = true;
```

The deployed version (`www_deploy/`) is **4 features behind** `field_notes/`:
- Missing FEAT-638 (Response Feedback)
- Missing FEAT-590 (DNA Proposal Cards)
- Missing send-lock logic

Additionally: the Foyer returns `"state": "OFFLINE"` (uppercase) but the JS checks `data.state === "offline"` (lowercase). **Case mismatch** — the offline display branch never triggers.

**Sprint 100 candidate fixes:**
1. Deploy `field_notes/intercom_v2.js` → `www_deploy/`
2. Normalize Foyer state strings to lowercase OR update JS to `toLowerCase()` compare
3. Add `build_site.py` step to auto-sync intercom_v2.js to www_deploy on commit


---

## Staged Stories

### Story 100.1 — Intercom Deploy Sync & State Case Normalization

**Acceptance criteria:**
1. `www_deploy/intercom_v2.js` matches `Portfolio_Dev/field_notes/intercom_v2.js` (currently 4 FEATs behind: FEAT-638, FEAT-590, send-lock logic)
2. Foyer state string comparison uses case-insensitive match (`data.state.toLowerCase() === "offline"`) OR Foyer normalizes to lowercase before emitting — pick one
3. `build_site.py` gains an assertion that `www_deploy/intercom_v2.js` md5 matches `field_notes/intercom_v2.js` (fail-fast on drift)

**Root cause logged:** Deploy pipeline has no sync step. FEAT-638 and FEAT-590 were committed to `field_notes/` but never copied to `www_deploy/`. Send-lock lines 621-625 stripped from deployed version.

---

### Story 100.2 — Stale Lock Reaper ✅ DONE (FEAT-641, commit `b384a15`)

**What was implemented:** `check_stale_locks()` in `standalone_accountability_watchdog.py` upgraded to two-phase detect+purge:
- Phase 1: classify each lock (live/stale/unknown) via PID liveness + fcntl probe
- Phase 2: `unlink()` any confirmed-dead-PID lock older than 30 minutes
- Safety gate: never reap if kernel advisory lock is actively held
- `[REAP]` log sentinel + `reaped` list in digest JSON

**Validated live:** Reaped `nightly_forge.lock` (DEAD PID 1870642, 1088.5m old). All locks now clear.

**What's NOT fixed:** The forge itself crashed without calling `record_nightly_completion()`, leaving the state ledger at `Age: 999h`. A follow-up story should add `systemd` crash recovery (ExecStopPost or WatchdogSec) to ensure the ledger is always updated even on SIGKILL.

---

## Item 1 (Triage) — RDP Self-Healing Design

**Current state (forensic):**
- System service `gnome-remote-desktop.service` **healthy** (running since Oct 1)
- **User session** service `gnome-remote-desktop.service` (user scope): **inactive (dead)** since 11:31:35
- Last RDP disconnect reason: `ERRINFO_RPC_INITIATED_DISCONNECT` — the previous RDP client disconnected cleanly, but the user-session daemon didn't restart
- Display: only `gdm` holds `:0` (X0 socket). User display session `jallred` has no `:1` socket — no user graphical session is running.

**Root cause:** During nightly VRAM quiesce, the user graphical session was torn down (or suspended). GNOME Remote Desktop in user scope requires an active graphical session. Without one, nothing to connect to.

**What needs to be recoverable:**
| Component | Must Survive? | Current? | Self-Heal? |
|-----------|--------------|---------|-----------|
| lab-attendant (port 8765) | ✅ Yes | ✅ Yes (system service) | ✅ Already |
| Foyer API | ✅ Yes | ✅ Alive (OFFLINE state) | ✅ Ignites at end of nightly |
| RDP access | ✅ Yes | ❌ User session dead | ❌ No |
| WebSocket intercom | ✅ Yes | ✅ Yes | ✅ via reconnect loop |
| nightly_forge.lock | ✅ Clean | ✅ Reaped (FEAT-641) | ✅ Now |

**Self-healing design options for RDP:**
1. **`autologin` + `gnome-remote-desktop` as system service** (current approach): works as long as the user session stays alive. Nightly quiesce kills it.
2. **Headless VNC fallback**: `x11vnc -create` creates a virtual display even without a physical session. RDP tunneled through that. Survives session death.
3. **`systemd-logind` session keep-alive**: Add `KillUserProcesses=no` to `logind.conf` to prevent session teardown on idle. Crude but effective.
4. **Restart trigger via watchdog**: Accountability watchdog (06:00 AM) attempts `loginctl activate <session>` to re-attach user session, then checks port 3389.

**Recommended Sprint 100 story:** Add RDP session watchdog to accountability script — detect dead user-session gnome-remote-desktop, attempt `systemctl --user start gnome-remote-desktop` via `loginctl` or `machinectl`. Log result. Make this the 06:00 self-heal pass.

---

## Item 10 — Router vs Hooks vs Attendant: Generalize the Architecture

**Motivation:** `lab-attendant.service` does too many things: WebSocket server, routing, hook dispatch, state machine, process management. This creates tight coupling — a hook failure can bring down the WS server. As we add more tools (JIT tools, IPC tools from item 7), the attendant becomes a bottleneck.

**Current responsibilities of the attendant:**
- WebSocket server (inbound connections from intercom.html)
- Intent routing (which cognitive node handles this request?)
- Hook invocation (ambient hooks, pre/post hooks)
- Process lifecycle (ignition, quiesce, VRAM management)
- State machine (OFFLINE → WAKING → READY → WORKING)

**The question:** Should routing live outside the attendant?

**Proposal: Three-Layer Split**

```
Layer 1: lab-attendant (renamed: lab-conductor?)
  → Keep: WebSocket server, state machine, process lifecycle
  → Remove: routing logic, hook dispatch

Layer 2: lab-router (new, or promote existing router.py to a standalone service)
  → Intent classification, node selection, load balancing across nodes
  → Could be an HTTP microservice or pure library

Layer 3: hook-bus (new concept)
  → Receives tool call events and fires ambient hooks
  → Decoupled from both attendant and router
  → Can run hooks in parallel (non-blocking)
  → Natural home for JIT tools (item 7) and future MCP tools
```

**Naming candidates for the generalized attendant:**
- `lab-conductor` — orchestrates without doing the work itself
- `lab-runtime` — generic enough to be "plug and play"
- `lab-nexus` — junction point for all communications
- `lab-switchboard` — telephony metaphor, makes sense for IPC

**Open question:** Do we have a separate watchdog today? Answer: the accountability watchdog is a *cron job* (06:00 AM), not a live watchdog daemon. A live watchdog (restart-on-death, health-check loop) is different — and currently missing for anything except systemd's built-in `Restart=on-failure`.

**Connection to items 7+8:** If the hook-bus dispatches tools in parallel (item 7), and those tools are both JIT reads and DNA writes (item 8), the hook-bus IS the IPC layer. This unifies items 7, 8, 9, and 10.

---

## Item 11 — Ball Cleanup BKM: Tracking Actionable Items in Conversation

**Motivation:** Long conversations drop action items. Sprint planning produces decisions that never become stories. Triage produces findings that never get filed. We need a lightweight protocol to capture and track "balls in the air."

**Proposed name candidates:**
- `BKM-077: BALL_TRACK` — "Ball Tracking Protocol"
- `BKM-077: CLEAR_DESK` — "Don't leave the desk dirty"
- `BKM-077: TRAIL_CLOSE` — closing the trail of open items
- `BKM-077: ACTION_FENCE` — fencing actionable items from discussion

**Draft BKM content:**

> **BKM-077: BALL_TRACK — Conversation Action Item Closure Protocol**
>
> **Problem:** Long agentic conversations generate findings, decisions, and action items that get buried in context. Items discussed but not committed to a story, BKM, or commit are effectively dropped.
>
> **Protocol:**
> 1. **At every sprint planning session:** Before ending, list all "in-flight balls" — items discussed but not yet assigned to a story, BKM, or commit.
> 2. **Ball states:** `🎾 OPEN` (discussed, not assigned), `📌 STAGED` (added to sprint doc), `✅ DONE` (committed), `🗑️ DROPPED` (explicitly deferred/abandoned).
> 3. **Trigger:** Any item prefixed with "we should...", "plan to...", "follow-up...", "add a story to..." is automatically a ball.
> 4. **End-of-session checkpoint:** Before any handoff or context summary, agent outputs a BALL_TRACK table of all open balls from the session.
> 5. **Where balls live:** Sprint plan doc OR a dedicated `OPEN_BALLS.md` in `Portfolio_Dev/docs/`.
>
> **Naming convention for the doc:**
> `Portfolio_Dev/docs/OPEN_BALLS.md` — flat running list, one per line, with state emoji.

**Questions to resolve:**
- Do we use a separate `OPEN_BALLS.md` or embed in each sprint plan? Suggest: embed during sprint, promote to `OPEN_BALLS.md` when sprint closes without resolution.
- Should the BKM include a "ball expiry" rule? (Balls older than 2 sprints auto-drop unless re-affirmed)
- Should the ball tracker be a tool? `jit_track_ball`, `jit_close_ball`?

---

## Next Steps
- [ ] **Story 100.1:** Implement intercom deploy sync (copy from field_notes to www_deploy + case-insensitive state check + build_site.py guard)
- [ ] **Story 100.2:** ✅ Done (FEAT-641, `b384a15`) — needs follow-up: forge crash recovery via ExecStopPost
- [ ] **Item 10:** Decide on naming for generalized attendant; scope the router/hook-bus split as a future sprint
- [ ] **Item 11:** Author BKM-077 (BALL_TRACK) as a DNA card; decide OPEN_BALLS.md vs sprint-embedded
- [ ] **RDP:** Add RDP session self-heal to accountability watchdog (06:00 pass)
- [ ] **Items 4-9:** Decide split: JIT namespace (4+5) as Sprint 100, parallel orchestration (7+8+9) as Sprint 101?
- [ ] **Empirical:** Test L2 KV cache capacity for multi-story parallel context
