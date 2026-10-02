# 🚀 SPRINT PLAN 97.0: Single-Home Runtime Data, Intercom Feedback Loop & Cognitive Triage Vibe Expansion

**Sprint ID:** `SPR_97_0`  
**Theme:** Single Canonical File Homes (Anti-Duplication), Active Feedback Loop Closure (`👍/👎`), Process Lifecycle & Dead-Lock Reaping, Expanded Cognitive Vibe Palette (`SOCRATIC`, `CHRONICLE`, `RETROSPECTIVE`, etc.), and Passive Telemetry Gating (`FEAT-632`–`FEAT-636`)  
**Status:** ACTIVE  
**Parent Framework:** `[BKM-049]` (The Delegation Execution Rulebook), `[BKM-071]` (Delegation Playbook Index), `[BKM-060]` (Federated DNA Domains), `[BKM-015]` (Semantic Anchor Protocol), `[BKM-020]` (High-Fidelity Sprint Documentation), `[INS-038]` (The Rug Bump Law), `[INS-042]` (The Waffle Trap & Circular Fixing Traps)  
**Target Silicon Nodes:** z87-Linux (RTX 2080 Ti Local vLLM 3B Base), Node KENDER (RTX 4090 Ollama Conductor), Node Brain (macOS M5 Air MLX :8002), ChromaDB Port 8001 (CLaRa-DNA)

## 📝 Operator Directives & Governance Rules
- **BKM-049 Story Owner Tag Law**: Every sprint story MUST declare an Assigned Owner (`[SWARM:LOCAL]`, `[SWARM:CLOUD]`, `[SWARM:ORACLE]`, or `[AGY:PRIMARY]`).
- **Strict Anti-Bypass Guard**: Direct primary-agent code edits on `[SWARM:*]` stories are strictly forbidden without prior failed execution attempts via `delegate.py`.
- **Tri-Loop Diagnostic Protocol**: Follow the 3-attempt local diagnostic retry loop for `[SWARM:LOCAL]`, direct cloud dispatch for `[SWARM:CLOUD]`, and mandatory `OPENAGENT_HANDOVER_PLAYBOOK.md` audit before any AGY takeover.
- **Single Canonical Homes (Rule 4)**: Multi-homing and copying runtime files between submodules is prohibited. Write dynamic logs and ledgers directly to `Portfolio_Dev/field_notes/data/`.

---

## 🧭 Executive Summary & Architectural Roadmap

Sprint 97.0 executes critical operational hardening and cognitive expansion across the Federated Lab:
1. **Story 97.0 (Oracle Pre-Pass):** Pre-certifies sprint contracts and test matrices against bedrock DNA invariants.
2. **Story 97.1 (Single-Home Runtime Data):** Abolishes multi-homed file writing; routes accountability ledgers directly to canonical data directories and integrates them into the `status.html` Interleaved System Log timeline.
3. **Story 97.2 (Intercom Feedback UI):** Implements clickable `👍/👎` feedback icons in `intercom.html` / `intercom_v2.js` connecting directly to the `POST /feedback` REST bridge (`[FEAT-632]`).
4. **Story 97.3 (Dead-Lock Reaping & Queue Hardening):** Deploys automated 05:45 AM stale lock reaping in the Attendant with `CRITICAL` alerting, eliminates bogus "Lab Hibernating" messages in `types.py`, and enforces "Disabled to Send" button gating.
5. **Story 97.4 (Triage Vibe Expansion):** Deprecates `CASUAL` vibe; implements an expressive cognitive palette (`SOCRATIC`, `FORENSIC`, `CHRONICLE`, `RETROSPECTIVE`, `ARCHITECTURAL`, `TACTICAL`, `STRATEGIC`, `PROVOCATIVE`, `METABOLIC`) with BKM-015 vector hints and M5 Air speculative lead calibration.
6. **Story 97.5 (Live Lab Vitals & Passive Guarantee):** Adds "6:00 AM Daily Sanity Check" visual badges to `status.html` vital cards and quarantines audio vocal synthesis testing strictly to the 06:00 AM daily health audit.

```mermaid
flowchart TD
    subgraph STAGE0 ["🔍 Architectural Pre-Flight"]
        S97_0["Story 97.0: Oracle Pre-Pass on Sprint 97 & DNA Grounding [SWARM:ORACLE]"]
    end
    subgraph STAGE1 ["📡 Telemetry, Single-Home & Intercom Feedback"]
        S97_1["Story 97.1: Single-Home Runtime Data & Interleaved Logs [FEAT-633] [SWARM:CLOUD]"]
        S97_2["Story 97.2: Intercom Feedback UI (Thumbs Up/Down) [FEAT-632] [SWARM:LOCAL]"]
    end
    subgraph STAGE2 ["🛡️ Silicon Lifecycle, Queue Hardening & Reaping"]
        S97_3["Story 97.3: Dead-Lock Reaping, VRAM Status & Queue Gate [FEAT-634] [SWARM:CLOUD]"]
    end
    subgraph STAGE3 ["🧠 Cognitive Vibe Palette & Speculative Calibration"]
        S97_4["Story 97.4: Triage Vibe Expansion & Speculative Lead Calibration [FEAT-635] [SWARM:CLOUD]"]
    end
    subgraph STAGE4 ["🏥 Vitals Sanity Badges & Passive Polling"]
        S97_5["Story 97.5: Live Lab Vitals 6:00 AM Sanity Badges & Passive Polling [FEAT-636] [SWARM:LOCAL]"]
    end

    S97_0 --> S97_1 --> S97_2 --> S97_3 --> S97_4 --> S97_5
```

---

## 📋 Sprint 97 Stories & 4-Anchor Specifications

### 🔍 Story 97.0: Oracle Pre-Pass on Sprint 97 Plan & Architectural Invariant Grounding
* **Assigned Owner:** `[SWARM:ORACLE]`
* **Status:** **PENDING EXECUTION**
* **Why & Root Cause:** Prevent circular fixing traps (`INS-042`) and enforce complexity conservation (`INS-038`) before code dispatch.
* **Mechanism:** The Oracle persona audits Sprint 97 story specifications against bedrock protocols (`BKM-006`, `BKM-024`, `BKM-049`, `BKM-060`, `BKM-071`, `BKM-073`). Validates that all target files exist, test batteries are declared verbatim, and owner tags comply with swarm governance.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `Portfolio_Dev/docs/sprints/active/SPRINT_PLAN_SPR_97_0.md`, `Portfolio_Dev/docs/sprints/active/ORACLE_REVIEW_SPRINT_97.md`.
  * **Anchor 2 (Verification Command):** `delegate.py --persona oracle --task "Audit Sprint 97 story contracts"`
  * **Anchor 3 (Live Silicon Invariant):** 100% of sprint stories verified for single canonical file paths, explicit test commands, and non-overlapping vibe scopes.
  * **Anchor 4 (DNA Links):** `[BKM-049]`, `[BKM-071]`, `[INS-038]`, `[INS-042]`.

---

#### 📡 Story 97.1: Single-Home Runtime Data & Accountability in Interleaved Logs
* **Assigned Owner:** `[SWARM:CLOUD]`
* **Feature Anchor:** `[FEAT-637]`
* **Status:** **PENDING EXECUTION**
* **Why & Root Cause:** Multi-homed writes between `Portfolio_Dev/field_notes/data/` and `www_deploy/data/` caused split-brain status discrepancies. Morning accountability audits were writing to isolated run paths, leaving `pollPager()` blind in `status.html`.
* **Task Breakdown:**
  1. Update all daemon write paths (`manager.py`, `router.py`, `daily_accountability_audit.py`) to output directly and exclusively to `Portfolio_Dev/field_notes/data/accountability_ledger.jsonl` and `status.json`.
  2. Update `pollPager()` in `Portfolio_Dev/field_notes/status.html` to fetch `data/accountability_ledger.jsonl` and render green accountability badge events interleaved with `pager_activity.json` and `validation_ledger.jsonl`.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `Portfolio_Dev/field_notes/status.html`, `HomeLabAI/src/infra/daily_accountability_audit.py`, `HomeLabAI/src/v5/ignition/manager.py`.
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_accountability_ledger.py -v`
  * **Anchor 3 (Live Silicon Invariant):** Zero duplicate runtime data writes to `www_deploy/data/`; `accountability_ledger.jsonl` rendered in `status.html` timeline.
  * **Anchor 4 (DNA Links):** `[FEAT-637]`, `[BKM-022]`, `[BKM-024]`.

---

### 👍 Story 97.2: Intercom Feedback UI (Thumbs Up/Down) & Co-Pilot Bridge
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Feature Anchor:** `[FEAT-638]`
* **Status:** **PENDING EXECUTION**
* **Why & Root Cause:** Story 96.5 implemented the backend `POST /feedback` endpoint in `router.py`, but the user-facing clickable icons were deferred, leaving the Fourth Wall feedback flywheel open.
* **Task Breakdown:**
  1. Add discrete `👍` (thumbs up) and `👎` (thumbs down) icon buttons to assistant message bubbles in `Portfolio_Dev/field_notes/intercom.html` and `intercom_v2.js`.
  2. Wire click handlers to send `POST /feedback` payloads (`{ "message_id": id, "verdict": "UP"|"DOWN", "query": q, "response": r }`) to Foyer port `8765`.
  3. Provide instant visual feedback (green/red active glow) and toast notification upon successful recording.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `Portfolio_Dev/field_notes/intercom.html`, `Portfolio_Dev/field_notes/intercom_v2.js`.
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_foyer_feedback.py -v`
  * **Anchor 3 (Live Silicon Invariant):** User feedback clicks immediately append JSONL records to `foyer_feedback_ledger.jsonl` on port 8765.
  * **Anchor 4 (DNA Links):** `[FEAT-638]`, `[BKM-035]`, `[INS-033]`.

---

### 🛡️ Story 97.3: Dead-Lock Reaping, VRAM Status Clean-up & Queue Hardening
* **Assigned Owner:** `[SWARM:CLOUD]`
* **Feature Anchor:** `[FEAT-639]`
* **Status:** **PENDING EXECUTION**
* **Why & Root Cause:** 
  1. An unhandled `SIGKILL` during nightly LoRA training left an orphaned `maintenance.lock`, blocking `/wake` and stranding VRAM at 208MB.
  2. `types.py` line 114 contained a hardcoded binary ternary emitting `"Lab Hibernating"` for any non-operational state even when hibernation was disabled.
  3. When Foyer was locked or offline, the intercom UI allowed clicking "Send", dropping user messages.
* **Task Breakdown:**
  1. Deploy an automated **Dead-Lock Reaping Sweep at 05:45 AM** in `HomeLabAI/src/v5/foyer/router.py` / `engine_watchdog.py` checking PID liveness; if `maintenance.lock` exists without an active training process, forcibly delete the lock, log a `CRITICAL` alert to `pager_activity.json`, and trigger `/wake`.
  2. Add a **60-minute hard watchdog** to nightly fine-tuning subprocesses to abort hung jobs before the 06:00 AM audit.
  3. Fix `HomeLabAI/src/v5/common/types.py` line 114 to output genuine state strings (`"Lab Offline"`, `"Standby (Scale-to-Zero)"`, `"Maintenance"`).
  4. Enforce **"Disabled to Send"** button state in `intercom_v2.js` when Foyer is locked/offline, preserving unsent text in the client input area.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `HomeLabAI/src/v5/foyer/router.py`, `HomeLabAI/src/v5/common/types.py`, `HomeLabAI/src/v5/ignition/manager.py`, `Portfolio_Dev/field_notes/intercom_v2.js`.
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_lock_reaper.py -v`
  * **Anchor 3 (Live Silicon Invariant):** Zero orphaned lock files survive beyond 05:45 AM; `status.json` reflects true hardware states with zero false "Hibernating" text.
  * **Anchor 4 (DNA Links):** `[FEAT-639]`, `[FEAT-136]`, `[BKM-044]`, `[BKM-024]`.

---

### 🧠 Story 97.4: Triage Vibe Palette Expansion & Speculative Head-Start Calibration
* **Assigned Owner:** `[SWARM:CLOUD]`
* **Feature Anchor:** `[FEAT-640]`
* **Status:** **PENDING EXECUTION**
* **Why & Root Cause:** `CASUAL` vibe acted as an over-aggressive catch-all that dampened reasoning depth. Work Past vs Recent Past was conflated under "HISTORICAL".
* **Task Breakdown:**
  1. Deprecate `CASUAL` vibe and expand cognitive triage taxonomy in `cognitive_hub.py` and `speculative_triage.py`:
     - `SOCRATIC`: Conceptual inquiries, design trade-offs, philosophical exploration.
     - `FORENSIC`: Tracebacks, crash logs, stack inspection, dead PIDs.
     - `CHRONICLE`: Intel work notes, distilled gems, past engineering milestones, distant past lookups.
     - `RETROSPECTIVE`: Recent lab sprints, yesterday's debugging logs, active session progress.
     - `ARCHITECTURAL`: System boundaries, component interfaces, complexity conservation (`INS-038`).
     - `TACTICAL`: Concrete code edits, surgical fixes, unit testing, task execution.
     - `STRATEGIC`: Portfolio vision, executive synthesis, leadership war stories.
     - `PROVOCATIVE`: Red-teaming, stress-testing design assertions, disagreement trapping.
     - `METABOLIC`: Document spine curation, memory pruning, refining DNA cards.
  2. Update `vector_pre_triage.py` to inject gentle `semantic_hint` vector priors without brittle hardcoded keyword lists (`BKM-015`).
  3. Calibrate `SpeculativeTriageRelay` in `speculative_triage.py` so REST-probed M5 Air is given the full dynamic EWMA lead window ($W_{\text{lead}} = 2 \cdot t_{\text{warmed}} + L_t + 4 \cdot J_t$) before local vLLM is dispatched as a fallback racer.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `HomeLabAI/src/logic/cognitive_hub.py`, `HomeLabAI/src/logic/speculative_triage.py`, `HomeLabAI/src/logic/vector_pre_triage.py`, `HomeLabAI/src/tests/test_live_pre_reflection_triage.py`.
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_live_pre_reflection_triage.py HomeLabAI/src/tests/test_vector_pre_triage.py -v`
  * **Anchor 3 (Live Silicon Invariant):** 100% of test battery queries resolve to correct expanded vibes; M5 Air lead window operates without latency races on warm silicon.
  * **Anchor 4 (DNA Links):** `[FEAT-640]`, `[FEAT-586]`, `[FEAT-583]`, `[BKM-015]`, `[BKM-060]`.

---

### 🏥 Story 97.5: Live Lab Vitals 6:00 AM Daily Sanity Check Badges & Passive Polling Guarantee
* **Assigned Owner:** `[SWARM:LOCAL]`
* **Feature Anchor:** `[FEAT-641]`
* **Status:** **PENDING EXECUTION**
* **Why & Root Cause:** UI vital cards lacked visual anchoring to the 06:00 AM health audit, and live telemetry required verification to ensure 100% passive, zero-wake behavior.
* **Task Breakdown:**
  1. Verify and enforce that all telemetry endpoints (`/status`, `/sys_metrics`, `/telemetry_kpi`, DCGM port 9400) in `HomeLabAI/src/infra/live_telemetry.py` are 100% passive read-only operations with zero `/wake` or GPU ignition side effects.
  2. Quarantine audio vocal synthesis and TTS testing strictly to the 06:00 AM Daily Health Audit (`daily_accountability_audit.py`), barring regular status polling from firing audio pipelines.
  3. Add a visual **"6:00 AM Daily Sanity Check" badge** (`[HEALTH: NOMINAL]` / `[HEALTH: AUDIT_STALE]`) to each vital card in `Portfolio_Dev/field_notes/status.html`.
* **4-Anchor Specification:**
  * **Anchor 1 (Target Files):** `Portfolio_Dev/field_notes/status.html`, `HomeLabAI/src/infra/live_telemetry.py`, `HomeLabAI/src/infra/daily_accountability_audit.py`.
  * **Anchor 2 (Verification Command):** `/home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest HomeLabAI/src/tests/test_telemetry_collector.py -v`
  * **Anchor 3 (Live Silicon Invariant):** Continuous 5s status polling produces zero VRAM delta or engine state transitions; vital cards display 06:00 AM health status.
  * **Anchor 4 (DNA Links):** `[FEAT-641]`, `[FEAT-607]`, `[BKM-024]`.
