# 🏗️ SPRINT 34: SEMANTIC RETRIEVAL & SILICON TELEMETRY (NVIDIA PIVOT)
*Status: ACTIVE | EXECUTING*

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

### 📋 NVIDIA DC GPU Principal Modeling Architect Demo Alignment
*   **Pedigree & Intent**: *"We need to show live validation-level KPIs for model execution. By aligning tokens as they stream (TTFT, tokens/sec) with physical GPU telemetry (watts consumed via DCGM on port 9400, VRAM, and thermals), we can calculate a live synthetic cost-per-token and real-time efficiency metrics."* — Lead Engineer.
*   **Tasks**:
    *   [ ] **Task 20.1 (Token Metric Instrumentation)**: Instrument `BicameralNode` and `CognitiveHub` to track TTFT (Time-to-First-Token), throughput (tokens/sec), and total generation duration per turn, exporting them in the stream payload to the Foyer.
    *   [ ] **Task 20.2 (NVIDIA DCGM / Prometheus Integration)**: Build a lightweight Python collector or query helper that hits the local Prometheus/DCGM exporter on port 9400 to fetch real-time power (watts) and thermal metrics during active generation turns.
    *   [ ] **Task 20.3 (Token-Aligned KPI Fusion)**: Correlate power draw with generation time to calculate energy per token (Joules/token) and compute a synthetic "price/TCO" based on Turing vs Kender (4090) hardware running costs.
    *   [ ] **Task 20.4 (UI Uplink - status.html)**: Add a `KPIs` tab in `status.html`'s Neural Uplink Telemetry section. Render real-time graphs showing latency, speed, power efficiency, and synthetic TCO.

---

## ⚡ SPRINT 34 PHASE 3: SILICON BENCHMARKING LEDGER (Task 21)
*Objective: Create a benchmark dashboard and evaluation framework to compare local vs. remote models.*

### 📋 Performance Comparison & Online Judge (BKM-032 / LLM-as-a-Judge)
*   **Pedigree & Intent**: *"Evaluating models on generic test sets is useless for the lab. We need to measure how well local and remote models (Qwen 3B vs Sovereign 27B) understand the 18-year lab history, using consistency queries and automated judges to tag model runs."* — Lead Engineer.
*   **Tasks**:
    *   [ ] **Task 21.1 (Performance Benchmark Ledger)**: Design a SQLite database or JSONL ledger `data/benchmarks.jsonl` that tracks offline and online execution runs, tagging model type, quant level, context length, TTFT, speed, and energy.
    *   [ ] **Task 21.2 (Benchmark Frontend)**: Create a new page `benchmarks.html` or a dedicated tab in `status.html` that reads the benchmark ledger and renders comparative bar charts (latency, speed, energy efficiency).
    *   [ ] **Task 21.3 (LLM-as-a-Judge Evaluation)**: Implement an online judge workflow using the Sovereign node (or a specialized evaluator) to rate answers to historical queries on a 1-5 scale, recording validation scores in the ledger.
    *   [ ] **Task 21.4 (BKM-032 Consistency Gate)**: Establish an automated test suite that queries historical anchors and triggers warning alerts on the Pager if semantic drift or factual contradictions are detected.
