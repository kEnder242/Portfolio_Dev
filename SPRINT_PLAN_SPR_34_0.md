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
*Status: ACTIVE*

### 📋 Forensic Rationale
During physical telemetry integration (Phase 2), querying `/telemetry_kpi` and `/sys_metrics` from the static web server (`notes.jason-lab.dev` or port `9001`) to the Foyer Attendant (`pager.jason-lab.dev` or port `8765`) triggered browser CORS `NetworkError` blocks. This occurred because wildcard CORS configurations (`Access-Control-Allow-Origin: *`) are fundamentally incompatible with credentials forwarding (`Access-Control-Allow-Credentials: true`), which is required to pass Cloudflare Access authentication tokens. To resolve this, a custom middleware allowlist is implemented in the Foyer router to dynamically echo the request origin, and fetch calls on the frontend are updated to request credentials forwarding.

### 🛠️ Tasks
*   [ ] **Task 22.1 (CORS Middleware Integration)**: Integrate custom `_cors_mw` middleware in `src/v5/foyer/router.py` to echo valid origins and allow credentials.
*   [ ] **Task 22.2 (Frontend Credentials Forwarding)**: Update `status.html` fetch calls to include `{ credentials: 'include' }`.
*   [ ] **Task 22.3 (Service Ignition & Verification)**: Restart `lab-attendant.service` and verify dashboard vitals rendering.
*   [ ] **Task 22.4 (Baseline Eval Execution)**: Execute `run_evals.py` to record baseline metrics in `benchmarks.jsonl`.

