# 📜 SPRINT PLAN: Sprint 49.0 — Unity Pattern Enforcement & Live Telemetry Architecture

**Session Focus**: Enforce the **Unity Pattern (Model Uniformity)** across all local inference and test suites, eliminate hardcoded model strings in favor of the `unified-base` single source of truth, unify benchmark suites to target the `UNITY` abstraction string, and transition benchmarking from synthetic offline scripts to continuous live NVML/Prometheus telemetry harvesting.

---

## 🏛️ Architectural Context & Deep Dive

### 1. The Unity Pattern Core Truth (`[FEAT-030]` / `LAB-003`)
* **What It Mandates**: On `z87-Linux` (RTX 2080 Ti 11GB VRAM), all local inference nodes (Pinky, Brain, Architect, Archive) **MUST share a single resident base model foundation** loaded in vLLM (`port 8088`). Multi-LoRA (`--enable-lora`) dynamically multiplexes personas (`cli_voice_v1`, `shadow_brain_v2`, `lab_history_v1`) on top of this single base within a shared **~2.5GB VRAM footprint**.
* **Model Fluidity**: The mandate does **NOT** enforce a specific brand (Llama vs. Qwen vs. Phi). The base model itself is model-fluid—whatever is designated as `unified-base` in `infrastructure.json` becomes the sole resident foundation.
* **The Failure Mode We Are Fixing**: When Node KENDER (Windows RTX 4090) goes offline, legacy failover paths in `manager.py`, `loader.py`, and integration tests attempted to spin up `qwen2.5-coder:14b` in Ollama alongside vLLM. This created a **Dual-Foundation Collision** (14B Qwen + 3B Base + ChromaDB + NeMo = 34GB total memory demand), collapsing 15GB system RAM into physical disk swap (`/dev/sda5`) and freezing mouse interrupts.

---

### 2. Single Source of Truth: `unified-base` Pointer (`infrastructure.json`)
* **The Master Pointer**: [`config/infrastructure.json`](file:///home/jallred/Dev_Lab/HomeLabAI/config/infrastructure.json#L48) defines `model_manifest.unified-base` (e.g. `"llama-3.2-3b-awq"`).
* **Global Resolution Law**:
  1. Every local module (`cognitive_hub.py`, `lab_attendant_v4.py`, `manager.py`, `loader.py`) MUST resolve local model endpoints through `infrastructure.json["model_manifest"]["unified-base"]`.
  2. Hardcoded local model strings (like `"qwen2.5-coder:14b"`, `"gemma2:2b"`, `/speedy/models/...`) in fallback logic are **STRICTLY FORBIDDEN**.
  3. If KENDER is offline, local fallback is **FORBIDDEN** from loading a non-Unity model into local Ollama/vLLM. Fallback routes strictly to `http://127.0.0.1:8088/v1` (`unified-base`).

---

### 3. System Integration Test Whitelist (`UNITY` Pointer Standard)
* **The Whitelist Pattern**: Rather than calling out exemptions for legacy experimental tools, we explicitly **whitelist System Integration Tests** that MUST enforce the `UNITY` abstraction pointer.
* **Whitelisted System Integration Tests**:
  1. `HomeLabAI/src/debug/test_uber_5x5.py`
  2. `HomeLabAI/src/debug/test_vllm_adapter_swap.py`
  3. `HomeLabAI/src/tests/test_integration_roundtable.py`
* **Whitelisting Law**: Every whitelisted integration test MUST resolve its local target model dynamically via the abstract key `UNITY` (reading `infrastructure.json["model_manifest"]["unified-base"]`). Hardcoding specific model strings or local disk paths in whitelisted tests is strictly forbidden. Experimental tools outside this whitelist (e.g. kernel/exploration scripts) remain in their own bucket.

---

### 4. Continuous Live Telemetry vs. Synthetic Offline Scripts
* **The Shift**: Replace isolated, offline synthetic benchmark scripts (which launch standalone models in memory traps) with **Continuous Live Telemetry Harvesting**.
* **The Engine**: Telemetry is harvested directly from Prometheus (`port 9400` / DCGM) and the Attendant Vitals API (`:8000/status`).
* **Operational Metrics Collected**:
  * Turn VRAM delta (MiB allocated / freed per turn)
  * Multi-LoRA adapter swap latency (sub-second target)
  * Real-time prompt throughput (tokens/sec)
  * Host disk swap activity (0 MB enforced ceiling)

---

## 🎯 Actionable Stories (Delegation Specifications — Code-Only)

> [!IMPORTANT]
> **Delegation Rule**: Stories are prepared for **CODE ONLY** execution by OpenAgent. All test validation and silicon gates will be executed on the AGY side after code changes complete.

---

### Story 1: Enforce `unified-base` Single Source of Truth in Ignition & Node Loader
* **Primary Target Files**:
  * `HomeLabAI/src/v5/ignition/manager.py`
  * `HomeLabAI/src/nodes/loader.py`
* **Context Anchors & Reference Files**:
  * `HomeLabAI/config/infrastructure.json` (`model_manifest.unified-base`)
* **Implementation Requirements**:
  1. **Infrastructure Resolver Utility**: Ensure `manager.py` and `loader.py` import and use a centralized `get_unified_base_model()` helper that reads `config/infrastructure.json`.
  2. **Purge Hardcoded Local Fallbacks**: Replace hardcoded local model strings in `manager.py` and `loader.py` with dynamic resolution to `unified-base`.
  3. **Local Fallback Route**: In `manager.py` local failover handling, if Node KENDER (`192.168.1.26:11434`) is offline/unreachable, route local fallback queries to `http://127.0.0.1:8088/v1` (`unified-base`).


---

### Story 2: Whitelisted Integration Test Abstraction (`UNITY` Pointer Standard)
* **Primary Target Files**:
  * `HomeLabAI/src/debug/test_uber_5x5.py`
  * `HomeLabAI/src/debug/test_vllm_adapter_swap.py`
  * `HomeLabAI/src/tests/test_integration_roundtable.py`
* **Context Anchors & Reference Files**:
  * `HomeLabAI/config/infrastructure.json`
* **Implementation Requirements**:
  1. **Abstract Model Resolution**: Update all whitelisted integration scripts to resolve target local model names using the abstract key `UNITY` (reading `infrastructure.json["model_manifest"]["unified-base"]`).
  2. **Purge Hardcoded Model Strings**: Remove explicit model strings (`"qwen..."`, `"llama..."`, raw `/speedy/...` paths) from test argument parsers, default parameters, and payload constructors.
  3. **Whitelisted Scope**: Focus strictly on the whitelisted integration tests; leave standalone experimental tools un-gated in their own bucket.


---

### Story 3: Continuous Live Telemetry Collector & Prometheus Harvester
* **Primary Target Files**:
  * `HomeLabAI/src/infra/live_telemetry.py` (New File)
  * `HomeLabAI/src/v5/ignition/manager.py`
* **Context Anchors & Reference Files**:
  * `HomeLabAI/docs/LAB_INFRASTRUCTURE.md` (`LAB-007`, `LAB-008`)
* **Implementation Requirements**:
  1. **Telemetry Collector (`live_telemetry.py`)**: Create a lightweight module that queries Prometheus on `http://127.0.0.1:9400` (DCGM GPU metrics) and Foyer status on `http://127.0.0.1:8765/status`.
  2. **Live Metrics Struct**: Extract live VRAM usage, GPU power draw, active LoRA adapter name, and host swap memory usage (`psutil.swap_memory()`).
  3. **Attendant Integration**: Wire `live_telemetry.py` into `manager.py`'s vitals loop so live operational benchmarks are recorded continuously to `field_notes/data/status.json` during active Round Table turns.

---

## 📜 Pre-Execution Planning & Discovery Ledger (Sprint 49.0 Refinement Log)

> **Purpose**: Document all pre-sprint discoveries, architectural refinements, and prompt payload synchronizations established prior to initiating story delegation.

### 1. Root Cause Forensics & Memory Avalanche Resolution
* **The Incident**: Un-stubbed Story 7 live integration test hit `POST http://localhost:8765/inject`. Node KENDER (Windows RTX 4090) was offline. Foyer triggered local failover, attempting to spin up `qwen2.5-coder:14b` in local Ollama alongside vLLM (`Llama-3.2-3B`), ChromaDB (`:8001`), and NeMo STT.
* **The Forensic Truth**: The 34GB memory demand collapsed local 15GB RAM / 11GB VRAM, thrashing physical disk swap (`/dev/sda5`), swapping out `gnome-shell`, and freezing mouse hardware interrupts.
* **The Architectural Rule**: Local failover on `z87-Linux` is **strictly forbidden** from loading a second foundation model into memory. When KENDER is offline, local fallback routes exclusively to the resident `unified-base` on `127.0.0.1:8088`.

### 2. Dual-Channel Agent Context Architecture ([BKM-041] / [LAB-012])
* **Channel 1 (Automagic Injection)**: ICM (`/home/jallred/.local/bin/icm`) + `BeforeAgent` hook in `settings.json` + `~/.config/icm/config.toml` (`chroma_url = "http://localhost:8001"`). Automagically injects top vector matches into system prompts before every turn.
* **Channel 2 (On-Demand Tool Bridge)**: `clara-dna` FastMCP server (`AcmeLab/src/clara_dna_mcp_server.py`) registered in `~/.gemini/config/mcp_config.json` (AGY) and `HomeLabAI/.opencode.json` (OpenAgent) for exact BKM/FEAT lookups (`get_protocol()`, `query_dna()`).
* **Port 8001 Law**: Port 8001 is ChromaDB. (Port 8000 is Prometheus RAPL Exporter). All vector embedding functions and HTTP clients connect exclusively to `:8001`.

### 3. Prompt Payload Simplification & Single Source of Truth
* **Prompt Clutter Elimination**: Removed 35+ lines of redundant negative constraint roleplay (`MUST NOT DO`, `task() roleplay`) from `OPENAGENT_HANDOVER_PLAYBOOK.md` and `delegate.py`.
* **Programmatic Code Source of Truth**: [`HomeLabAI/src/tests/delegate.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/tests/delegate.py#L165) (lines 165–174) is designated as the single programmatic code source of truth for the live delegation prompt payload sent over REST.
* **System Integration Test Whitelist Pattern**: Replaced ad-hoc script exemptions with an explicit **System Integration Test Whitelist** (`test_uber_5x5.py`, `test_vllm_adapter_swap.py`, `test_integration_roundtable.py`) that MUST enforce the `UNITY` abstraction pointer. Standalone experimental tools remain un-gated in their own bucket.

### 4. Forensic Audit of Pre-Sprint Hard Freeze (10:38 AM Incident) & Cgroup Hard Shield
* **The 10:38 AM Incident**: `delegate.py` first run failed with `[SESSION_FAILED]` because `opencode-core.service` was inactive (Scale-to-Zero). Manually starting `opencode-core.service` ignited OpenCode's engine and full plugin stack.
* **The OS Swap Thrashing Mechanics**: OpenCode booted `claude-mem` (an external marketplace plugin). `claude-mem` launched duplicate Python 3.13 `chroma-mcp` vector servers (`~/.claude-mem/chroma`) AND Bun worker processes allocating 73GB virtual address space on every tool output event. Physical RAM hit 95%, causing Linux to enter **Swap Reclaim Mode** on `/dev/sda5`. This swapped out `gnome-shell` and `xrdp` display buffers, freezing mouse interrupts and dropping RDP *before* physical RAM hit the hard OOM limit needed to trigger `OOMScoreAdjust=1000`.
* **The Cgroup Hard Memory Shield ([LAB-011] Update)**: Enforced `MemoryMax=1.8G`, `MemorySwapMax=0`, `MemoryHigh=1.5G`, and `NODE_OPTIONS=--max-old-space-size=1536` in `~/.config/systemd/user/opencode-core.service`. Forbids OpenCode from ever spilling into physical disk swap. If OpenCode exceeds 1.8GB, systemd terminates it cleanly in milliseconds, protecting `gnome-shell` and RDP stability.
* **`claude-mem` Removal & ICM Standardization**: Removed `claude-mem` from `~/.config/opencode/opencode.json` and killed all orphan Bun/Python 3.13 processes. Designated **ICM (`icm`)** as the sole compiled memory manager (<10MB RAM, connects directly to ChromaDB `:8001`). OpenCode footprint dropped from ~4GB to 74MB RAM.
* **Legacy Gemini Settings Archival**: Archived deprecated `~/.gemini/settings.json` to `~/.gemini/settings.json.deprecated`. Confirmed **AGY (`antigravity-cli`)** uses `~/.gemini/antigravity-cli/settings.json` and `~/.gemini/config/mcp_config.json`.
* **`delegate.py` Auto-Ignition**: Added auto-start check for `opencode-core.service` in `delegate.py` to eliminate `[SESSION_FAILED] Connection refused` errors on port 4097.

### 5. ICM Memory Curation Audit & Auto-Capture Root Cause (2026-08-05)
* **The Store Was Quietly Re-Bloating**: A health audit found ICM's store at 186 memories with 5 topics flagged for consolidation — `context-jallred` (57), `context-Dev_Lab` (49/50), `decisions-OpenAgent` (7), `decisions-field-notes` (9), `errors-resolved` (7). The 08-04 housekeeping had already deleted 986 garbage entries (`context-Dev_Lab`, `context-fake_printer`, decay+prune 861) + consolidated 9 topics. It re-bloated anyway.
* **Root Cause — Not Ignore Rules, But RAW Tool-Output Capture**: `icm serve --compact` (the opencode MCP server, registered in `~/.config/opencode/opencode.json`) auto-stores **every agent tool call's raw output** as a memory, namespaced by cwd-derived topic (`context-Dev_Lab` / `context-jallred`). Proven live: simply reading `opencode.json` auto-created a `context-Dev_Lab` entry at 21:31. `.venv` / `ModuleNotFoundError` / `ls: cannot access` path fragments (the classic missing-ignore garbage) flowed straight in. **`auto_extract=false` in config was a red herring** — it only disabled the synchronous LLM summary path; it did NOT stop raw tool-output capture. The actual gates are `[extraction] enabled / extract_every / store_raw` (binary source: `if (toolCallCount < EXTRACT_EVERY) return`).
* **The Memory Math (the 2GB Enigma)**: Total store on disk is only **~9.5 MB** (`memories.db`). Consolidating 186→82 memories does **not** reclaim the ~2GB of RAM/swap attributed to ICM — that footprint is `icm serve`'s runtime working set (ENGINE + EMBEDDING/BUFFERS + in-process vector index), not the memory contents. Curation wins **recall quality** (kills noise that matches every query), not **resident RAM**.
* **Consolidation Executed (semidestructive, preserves real knowledge)**: `context-jallred` 57→1 (user prefs preserved: parallel calls > sequential, atomic writes `.tmp`+`replace`, BKM density, user handles all pushes, no test frameworks in prod, submodule search boundaries, double-write workspace docs); `context-Dev_Lab` 50→1 (systemd/memory facts); `decisions-OpenAgent` 7→1; `decisions-field-notes` 9→1; `errors-resolved` 7→1; `context-quiet-falcon` cleared (dead project), 2 useful prefs folded into jallred. Net 186 → 82.
* **Config Fix Applied** (`~/.config/icm/config.toml`): replaced the ineffective `auto_extract = false` with `[extraction] enabled = false / extract_every = 1000000 / store_raw = false`. Effective-config verified via `icm config`. **Gotcha:** the running `icm serve` still holds the old config in memory — the fix only takes effect after `icm` restarts (i.e., an `opencode.app` restart). Fresh captures continued after the edit until restart.
* **The Re-Bloating Loop Is the Enemy**: Disabling capture is a one-time gate. The durable fix is to keep capture OFF and rely on explicit `icm store` / `icm_memory_store` (a separate path) for what should actually persist.

### 6. Infrastructure Hardening — Real Memory & Disk Reclaim (2026-08-05) [LAB-013 → LAB-018]
* **Context**: Sprint 49 investigation (above) established that ICM's ~2GB footprint was *resident weights*, not memory-store data. This session executed the durable fixes. All registered in `HomeLabAI/docs/LAB_INFRASTRUCTURE.md` (LAB-013 → LAB-018).
* **LAB-013 — The Real 2GB Fix (ICM Embedding Swap)**: `[embeddings] model` changed from `intfloat/multilingual-e5-base` to `Xenova/bge-small-en-v1.5` in `~/.config/icm/config.toml`. **Key distinction**: `[embeddings]` (PLURAL) = model weights; `[embedding]` (SINGULAR) = storage provider. Result: `icm serve --compact` RSS **2.07 GB → 16 MB** at cold boot; entire `opencode-core` cgroup **3.2 GB → 1.1 GB**, `swap.current → 0`. Model loads at boot only → requires `systemctl --user restart opencode-core.service`.
* **LAB-014 — ZFS Quotas (disk guardrails)**: rpool is ZFS (`rpool/USERDATA/home_xu2wtk`). Set Steam `quota=200G` (`home_xu2wtk/steam`, leaf child) + home `refquota=380G` (own-data only, Steam's bucket excluded). Combined ceel capped ~580G on 736G pool, leaving real headroom. Reversible: `zfs set quota=none`. **Gotcha**: quota sized above pool-free is a fake guardrail (never triggers before pool ENOSPC); size to taxable pool space.
* **LAB-015 — sanoid Snapshot Rotation**: Installed `sanoid` (apt 2.2.0), config `/etc/sanoid/sanoid.conf` for `[rpool/USERDATA/home_xu2wtk]` only → hourly×24 / daily×14 / weekly×8, `autosnap`+`autoprune`. `recursive = no` keeps **Steam child dataset untouched**, double-locked by `com.sun:auto-snapshot=false` on steam. Base anchor: `@base-20260805-221656`. Service 15-min tick, TZ=UTC labels. Rollback safety net for /home.
* **LAB-016 — ICM raw-capture disable final**: config `[extraction]` gates (`enabled=false`, `extract_every=1000000`, `store_raw=false`) + `PostToolUse` hook in `~/.claude/settings.json` → no-op. Original June `post-cleanup` base (10.7G) destroyed as superseded.
* **LAB-017 — Memory Shield Stack (cgroup limits)**: `opencode-core.service` (3.0G/3.5G/3.0G) + `code-server@jallred.service` (1.5G/2.0G/1.0G) drop-ins in `/etc/systemd/system/*.service.d/`; live-applied via `set-property` (no restart) + drop-in persisted. **SSH resilience**: survives swap storms via `ssh.socket` socket-activation + `systemd-oomd` knife-pointing the whale, key-only auth.
* **LAB-018 — claude-mem fully removed**: found **dual registration** — opencode plugin was cleared, but a **second Claude-Code install at `~/.claude/plugins/cache/thedotmack/claude-mem`** (registered in `~/.claude/settings.json` `enabledPlugins` + 6 hooks) kept the daemon (bun worker-service + uv `chroma~mcp` 0.2.6 + python) alive at ~230MB. AGY **never used it** (zero refs in live AGY/opencode configs; only transcript archives matched). Verified removed all dirs, stripped hooks, killed daemon. Backup: `~/.claude/settings.json.backup-claude-mem-20260805224615`. **redundancy**: claude-mem duplicated ICM + clara-dna memory stack, but with a fire-on-every-tool-event mechanism (73GB VA per event) that was the real danger.
* **VS Code interpreter wiring**: `~/.vscode-server/data/Machine/settings.json` pointed at `HomeLabAI/.venv` (venv path + default interpreter) so the Python env survives restarts.

### 7. Story 1 Execution & Verification (2026-08-05) [COMPLETED]
* **Target Files**: [`HomeLabAI/src/v5/ignition/manager.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/v5/ignition/manager.py#L31) & [`HomeLabAI/src/nodes/loader.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/nodes/loader.py#L27)
* **Execution Details**: Dispatched via `delegate.py --story 1 --agent sisyphus-junior` (Node KENDER `qwen3:14b`).
* **Implementation Summary**:
  1. Added `get_unified_base_model()` helper function in both `loader.py` and `manager.py` that dynamically reads `HomeLabAI/config/infrastructure.json` and resolves the `model_manifest.unified-base` pointer (defaulting to `"llama-3.2-3b-awq"`).
  2. Updated `_bg_prime_kender()` in `manager.py` to use `"qwen3:14b"` for KENDER VRAM warmup, with dynamic fallback logging to `http://127.0.0.1:8088/v1` (`unified-base`).
### 8. Story 2 Execution & Verification (2026-08-05) [COMPLETED]
* **Target File**: [`HomeLabAI/src/debug/test_uber_5x5.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/debug/test_uber_5x5.py#L16)
* **Execution Details**: Dispatched via `delegate.py --story 2` (Atlas / Plan Executor). Completed in 94.7s (`finish=stop`).
* **Implementation Summary**:
  1. Updated `test_uber_5x5.py` with `get_unified_base_model()` helper dynamically resolving `infrastructure.json`'s `model_manifest.unified-base` pointer (`UNITY_MODEL`).
  2. Replaced hardcoded `/speedy/...` model paths with dynamic `UNITY_MODEL` abstraction in websocket client payload constructors and logging.
### 9. Story 3 Execution & Verification (2026-08-05) [COMPLETED]
* **Target Files**: [`HomeLabAI/src/infra/live_telemetry.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/infra/live_telemetry.py#L1) & [`HomeLabAI/src/v5/ignition/manager.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/v5/ignition/manager.py#L273)
* **Execution Details**: Created `live_telemetry.py` module querying Prometheus `:9400` (DCGM GPU VRAM/power) and Foyer `:8765`, fusing live metrics with host swap (`psutil.swap_memory()`).
* **Implementation Summary**:
  1. Implemented Class-1 `merge_live_benchmarks(payload)` harvester with safe zero-degradation defaults.
  2. Wired `merge_live_benchmarks` into `manager.py`'s `update_status_file()` vitals loop to continuously log operational benchmarks into `status.json`.
  3. Verified syntax via `python3 -m py_compile` and committed to `HomeLabAI` repository (`feat(story-3)`).





