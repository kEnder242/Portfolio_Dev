# 🏗️ SPRINT 34: SEMANTIC RETRIEVAL & SILICON TELEMETRY (NVIDIA PIVOT)
*Status: ACTIVE | PHASES 1-3 COMPLETE | PHASE 4 COMPLETE*

### 🎯 MISSION
Deepen the grounding and efficiency of the Bicameral Mind. Having successfully stabilized hierarchical semantic retrieval and socket isolation in Goal 1, we pivot to build high-fidelity GPU and token telemetry dashboards. We will leverage NVIDIA DCGM metrics alongside token-level metrics (TTFT, speed) to showcase real-time latency, power, and synthetic TCO/Turing-class cost metrics, culminating in a model benchmarking page to evaluate performance across the local and remote lab silicon.

---

## 🏗️ GOAL 1: SEMANTIC RETRIEVAL & HIERARCHICAL COGNITION (Task 19)
*Objective: Build an engineering layer for precise retrieval and VRAM/socket lifecycle hygiene.*

### 📋 Context & Execution Status
*   **Status**: COMPLETE (Verified June 25, 2026).
*   **Validation Results**:
    *   **Task 19.1**: Hierarchical Semantic Map successfully generated with 93 strategic anchors and verified via `test_architect_flow.py`.
    *   **Task 19.2**: MCompassRAG domain pre-filtering and active domain fallback via `status.json` verified using extended `test_rag_logic.py` test suite.
    *   **Task 19.3**: Dreaming cycle V5 remote REST endpoint (`/wake`) stabilized and verified.
    *   **Task 19.4**: 5-minute socket idle shutdown under `DEBUG_BRAIN` mode implemented in `router.py` and verified using `test_auto_shutdown.py`.

### 🛠️ Tasks
*   [x] **Task 19.1 (Hierarchical Semantic Map)**: Refactor `build_semantic_map` in `lab_node.py` to cluster files, achievements, and timelines into Strategic, Analytical, and Tactical layers.
*   [x] **Task 19.2 (Metadata-Guided RAG)**: Integrate `MCompassRAG` pre-filtering in `archive_node.py` and `cognitive_hub.py` to filter search spaces using triage metadata.
*   [x] **Task 19.3 (Dreaming Pipeline Stabilization)**: Patch `dream_cycle.py` to target V5 remote REST endpoint (`/wake`) and resolve cross-platform lock file collisions.
*   [x] **Task 19.4 (Intelligent Socket Logic - FEAT-171)**: Enforce mode-aware client disconnect idle timer in `router.py` and `acme_lab.py`.

---

## ⚡ SPRINT 34 PHASE 2: LIVE GPU & TOKEN TELEMETRY DASHBOARD (Task 20)
*Objective: Showcase token-aligned KPIs (latency, speed, power, synthetic cost) based on active lab runs.*
*Status: COMPLETE (June 25, 2026)*

### 📋 NVIDIA DC GPU Principal Modeling Architect Demo Alignment
*   **Pedigree & Intent**: *"We need to show live validation-level KPIs for model execution. By aligning tokens as they stream (TTFT, tokens/sec) with physical GPU telemetry (watts consumed via DCGM on port 9400, VRAM, and thermals), we can calculate a live synthetic cost-per-token and real-time efficiency metrics."* — Lead Engineer.
*   **Commit**: `[FEAT-T20] Silicon KPI Telemetry Pipeline` + `[FEAT-T20.4] KPI Tab`
*   **Tasks**:
    *   [x] **Task 20.1 (Token Metric Instrumentation)**: Instrument `BicameralNode` and `CognitiveHub` to track TTFT, throughput (tokens/sec), and total generation duration per turn. Files: `loader.py`, `cognitive_hub.py`.
    *   [x] **Task 20.2 (NVIDIA DCGM / Prometheus Integration)**: `telemetry_collector.py` — lightweight DCGM scraper with 5s TTL cache, `TelemetrySample` dataclass, append-only ledger writer.
    *   [x] **Task 20.3 (Token-Aligned KPI Fusion)**: Joules/token + synthetic TCO ($0.10/kWh) computed in `TelemetrySample.enrich_economics()`. `/telemetry_kpi` REST endpoint in `router.py`.
    *   [x] **Task 20.4 (UI Uplink - status.html)**: KPI tab in Neural Uplink Telemetry. 5 sparkline stat cards (TTFT, throughput, GPU power, J/token, synthetic TCO µ$). Recent-query table.
    *   [x] **Task 20.5 (SYSTEM Graph Tab)**: Replaced LOAD+TEMP Grafana iframe tabs with single live canvas graph. Polls `/sys_metrics` every 5s. 5 series: CPU%, RAM%, VRAM%, GPU Temp°C, GPU Power W. 60-point ring buffer (~5 min). DPR-aware rendering. Files: `status.html`, `router.py`.

---

## ⚡ SPRINT 34 PHASE 3: SILICON BENCHMARKING LEDGER (Task 21)
*Objective: Create a benchmark dashboard and evaluation framework to compare local vs. remote models.*
*Status: COMPLETE (June 25, 2026)*

### 📋 Performance Comparison & Online Judge (BKM-032 / LLM-as-a-Judge)
*   **Pedigree & Intent**: *"Evaluating models on generic test sets is useless for the lab. We need to measure how well local and remote models (Qwen 3B vs Sovereign 27B) understand the 18-year lab history, using consistency queries and automated judges to tag model runs."* — Lead Engineer.
*   **Commit**: `[FEAT-T21] Silicon Benchmarking Engine` + `[FEAT-T21.2] Silicon Benchmarks dashboard`
*   **Tasks**:
    *   [x] **Task 21.1 (Performance Benchmark Ledger)**: `benchmarks.jsonl` append-only ledger via `run_evals.py`. Schema: model, engine, quant, tags, prompt, response, TTFT, tok/s, GPU power, J/token, TCO, judge_score (1-5), judge_reasoning.
    *   [x] **Task 21.2 (Benchmark Frontend)**: `benchmarks.html` — model comparison cards with score bar + sparkline, run history table with score badges (color-coded 1-5), prompt inspector modal, tag filter buttons. `/benchmarks_kpi` REST endpoint with per-model aggregates. Navigation link in `mission-control.js` (v1.4).
    *   [x] **Task 21.3 (LLM-as-a-Judge Evaluation)**: `run_evals.py` — 10 domain-tagged prompts (telemetry, history, inference, tco), async vLLM/Ollama runner, Cynical Curator rubric, JSON extraction with regex fallback.
    *   [x] **Task 21.4 (BKM-032 Consistency Gate)**: Watchdog in `run_evals.py` checks sliding avg over last N runs. Fires `pager_relay.trigger_pager(WARNING)` if score drops below `BENCH_SCORE_THRESHOLD` (default 3.0, env-configurable). Eval dispatch via `/trigger_task?task=eval` POST.

---

## 📊 Sprint 34 — Delivery Summary

| Component | Files Changed | Status |
|---|---|---|
| Token telemetry pipeline | `loader.py`, `cognitive_hub.py`, `telemetry_collector.py` | ✅ |
| REST endpoints | `router.py` (+4 endpoints) | ✅ |
| KPI + SYSTEM tabs | `status.html` | ✅ |
| Benchmark harness | `run_evals.py` | ✅ |
| Benchmark dashboard | `benchmarks.html`, `mission-control.js` | ✅ |

**Run first eval batch:**
```bash
cd ~/Dev_Lab/HomeLabAI/src
PYTHONPATH=$(pwd) python run_evals.py --tag baseline --engine vllm
```

---

## ⚡ SPRINT 34 PHASE 4: CORS REMEDIATION & BASELINE EVALUATION (Task 22)
*Objective: Stabilize dashboard telemetry across origins via CORS credentials allowance, and perform baseline model benchmarking.*
*Status: COMPLETE (June 25, 2026)*

### 📋 Forensic Rationale
During physical telemetry integration (Phase 2), querying `/telemetry_kpi` and `/sys_metrics` from the static web server (`notes.jason-lab.dev` or port `9001`) to the Foyer Attendant (`pager.jason-lab.dev` or port `8765`) triggered browser CORS `NetworkError` blocks. This occurred because wildcard CORS configurations (`Access-Control-Allow-Origin: *`) are fundamentally incompatible with credentials forwarding (`Access-Control-Allow-Credentials: true`), which is required to pass Cloudflare Access authentication tokens. To resolve this, a custom middleware allowlist is implemented in the Foyer router to dynamically echo the request origin, and fetch calls on the frontend are updated to request credentials forwarding.

### 🛠️ Tasks
*   [x] **Task 22.0 (Tiered Idle Verification - FEAT-374)**: Implement fast TCP port connection checks and vLLM metric checks inside `IgnitionManager` before triggering natural hibernation.
*   [x] **Task 22.1 (CORS Middleware Integration)**: Integrate custom `_cors_mw` middleware in `src/v5/foyer/router.py` to echo valid origins and allow credentials.
*   [x] **Task 22.2 (Frontend Credentials Forwarding)**: Update `status.html` fetch calls to include `{ credentials: 'include' }`.
*   [x] **Task 22.3 (Service Ignition & Verification)**: Restart `lab-attendant.service` and verify dashboard vitals rendering.
*   [x] **Task 22.4 (Baseline Eval Execution)**: Execute `run_evals.py` to record baseline metrics in `benchmarks.jsonl`.

### 📋 Phase 4 Execution Challenges & Keep-Awake Strategy
During baseline evaluation execution, two major blockers were identified and must be managed:
1. **Hugging Face Hub Lock Contention**:
   Stale lock files in `~/.cache/huggingface/hub/.locks/` (specifically under `models--sentence-transformers--all-MiniLM-L6-v2/` and `models--nvidia--nemotron-speech-streaming-en-0.6b/`) modified months ago cause the node synchronization (SentenceTransformers and Nemotron STT) to block the Foyer Attendant's single-threaded event loop on startup. This causes a 3-4 minute startup hang.
   *Remediation*: Delete these stale lock files before restarting the service.

2. **AFK / Idle Timeout Conflict**:
   The `IgnitionManager` terminates the vLLM engine if no active WebSocket clients connect to the router for more than 120 seconds. Because `run_evals.py` communicates directly with vLLM via HTTP on port 8088 rather than connecting via WebSocket, the router reports 0 active clients, causing the manager to hibernate vLLM mid-evaluation.
   *Keep-Awake Strategy*: During evaluations, run a background loop calling `/wake` every 50 seconds to refresh the active timer:
   ```bash
    while true; do curl -s -X POST http://localhost:8765/wake > /dev/null; sleep 50; done &
    ```

---

## ⚡ SPRINT 34 PHASE 5: COGNITIVE TAXONOMY & CACHE ALIGNMENT (COMPLETE)
*Objective: Collapse intent/vibe taxonomy to eliminate routing conflicts, enforce prefix-caching, and restore peer-to-peer prompt alignment.*

### 📋 Context & Research History
During casual dialogue testing, the dual taxonomy of `intent` and `vibe` created a structural conflict (e.g., triage classifying `"Hello mice!"` as `intent: CASUAL` but `vibe: TECHNICAL`, bypassing conversational overrides and forcing report-style lecturing). Historically:
*   **Validation Era (v3.1.9)**: Hard-coded silicon anchors restricted dialogue to strict diagnostics.
*   **Moat Era (ad1fa25)**: Banter Sanitizers and negative constraints ("NO BANTER") were added to block cross-node bleed, creating a cold, arrogant persona.
*   **Graft Era (857d891)**: `IDENTITY_BEDROCK` hardcoded subservient roleplay ("The Lead Engineer who built you"), which was baked into the `cli_voice` adapter.

### 🛠️ Proposed Realignment Strategy
1.  **Collapse Taxonomy**: Remove `intent` from triage schema in `lab_node.py` and rely entirely on `vibe` (e.g. `CASUAL` selects local conversational Pinky, `TECHNICAL` selects strategic Deep Thought).
2.  **Restore Prefix Caching**: Place a static, objective `IDENTITY_BEDROCK` at the absolute beginning of all node prompts to maximize vLLM prefix cache hits, and append all dynamic context to the end of user queries.
3.  **Positive Prompting**: Shift from negative constraints to positive style descriptions (collaborative technical peer vs. subservient reporting).

### 📋 Tasks to Review
*   [x] **Task 23.1 (Taxonomy Simplification)**: Refactor `lab_node.py` and `cognitive_hub.py` to route and style based on `vibe` alone, removing `intent` redundancies.
*   [x] **Task 23.2 (Prefix Cache Optimization)**: Restructure system prompt assembly to prepend the static bedrock topography, moving all dynamic variables (RAG hints, telemetry, user context) to the query end.
*   [x] **Task 23.3 (Dream Voice Peer Adaptation)**: Update `dream_voice.py` fine-tuning template to target "engineering peer" rather than "Lead Engineer" and run a refinement burn.
*   [x] **Task 23.4 (Log Viewer Restoration)**: Resolve the systemd regression by restoring native Foyer trace file reading inside `status.html` to reclaim local execution visibility.
