# 🚀 SPRINT PLAN: SPR-66.0
## Federated Silicon Benchmarking Engine, Dynamic Swarm Aliases & Live Telemetry Stream

---

### 🏛️ 1. Executive Summary & Architectural Vision
Sprint 66.0 transforms [`benchmarks.html`](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/benchmarks.html) from a stale single-node RTX 2080 Ti snapshot into a **Federated Silicon & ROI Telemetry Workbench**. It also introduces a centralized **Swarm Model Alias Registry** (`[FEAT-493]`) in `infrastructure.json` that decouples agent roles from transient upstream checkpoint names, enabling seamless model swaps and unified fallback flows across all 4 hardware seats. Furthermore, it creates a **Dynamic Auto-Discovery Benchmark Engine** (`[FEAT-495]`) hooked into the nightly forge, and a **Passive Real-Time Swarm Telemetry Stream** (`[FEAT-496]`) providing continuous "free benchmarking" of live workloads.

---

### 📐 2. The 4 Federated Hardware Seats

| Seat | Hardware Topography | Primary Resident Model | Memory Architecture | Target Role | Live Verified Throughput |
|:---|:---|:---|:---|:---|:---|
| **Apple M5 Air** (`:8000`) | Apple Silicon M5 (24GB Unified) | `mlx-community--Qwen3.8-27B-4bit` | 16.8GB Unified RAM | **Deep Architectural Reasoning & Planner** | **16.07 tok/s (910ms TTFT)** |
| **Windows Kender** (`:11434`) | NVIDIA RTX 4090 (24GB VRAM) | `qwen2.5-coder:14b` | 1,008 GB/s GDDR6X | **High-Throughput Interactive Coding** | **48.5 tok/s (280ms TTFT)** |
| **Linux z87** (`:8088`) | NVIDIA RTX 2080 Ti (11GB VRAM) | `Llama-3.2-3B-AWQ` | 616 GB/s GDDR6 | **Sensory Foyer & Multi-LoRA Engine** | **42.0 tok/s (180ms TTFT)** |
| **Cloud Swarm** (`:4097`) | Distributed Cloud Cluster | Dynamic Free Tier (`openrouter/free`) | Cloud High-Context | **Swarm Fallbacks & Cross-Review** | **35.0 tok/s (450ms TTFT)** |

---

### 🎯 3. Sprint Epics & User Stories

```
SPRINT 66.0
├── [STORY 66.1] Centralized Swarm Model Alias Registry (FEAT-493) [COMPLETE]
├── [STORY 66.2] benchmarks.html 3-Tab Overhaul & Live Shakedown Engine (FEAT-494) [COMPLETE]
├── [STORY 66.3] Multi-Strategy Swarm Delegation Shakedown & Reachability Sentinel [COMPLETE]
├── [STORY 66.4] Dynamic Auto-Discovery Benchmark Engine & Nightly Sweep Integration (FEAT-495)
├── [STORY 66.5] Passive Real-Time Swarm Telemetry Stream & Live Activity Widget (FEAT-496)
└── [STORY 66.6] Federated End-to-End Live Shakedown & Silicon Certification (FEAT-497)
```

#### 📦 Story 66.1: Centralized Swarm Model Alias Registry (`[FEAT-493]`) — [COMPLETED]
* **Goal:** Define logical aliases (`champion_reasoner`, `champion_coder`, `fast_worker`, `default_ladder`) in `HomeLabAI/config/infrastructure.json`.
* **Delivery:** `delegate.py` resolves aliases dynamically; swapping a model on M5 Air or Kender requires updating only a single line in `infrastructure.json`.

#### 📦 Story 66.2: `benchmarks.html` 3-Tab Overhaul & Live Shakedown Runner (`[FEAT-494]`) — [COMPLETED]
* **Goal:** Replace stale Grafana iframes and static bars with a modern 3-tab workbench:
  * **Tab 1: 🏛️ Silicon Arena:** Side-by-side card grid comparing M5 Unified vs RTX 4090 vs RTX 2080 Ti vs Cloud Swarm with live status badges.
  * **Tab 2: ⚡ Energy & Financial ROI:** Joules per 1k tokens ($	ext{J}/	ext{kTok}$), power draw envelopes, and cumulative local dollar savings counter vs Claude 3.5 API rates ($3.00/MTok).
  * **Tab 3: 🧠 Intelligence Quotient & CoT:** Reasoning Token Ratio ($	ext{CoT} / 	ext{Output}$), Parameter density, and academic pedigree references.
  * **Live Shakedown Engine:** A vanilla JS "⚡ Run Live Shakedown" button that dispatches test probes across all reachable seats and renders live stage waterfalls.

#### 📦 Story 66.3: Multi-Strategy Swarm Delegation Shakedown & Reachability Sentinel — [COMPLETED]
* **Goal:** Implement proactive 500ms socket reachability filtering in `delegate.py` to eliminate 60s TCP connection hangs when physical hardware is sleeping.
* **Delivery:** Verified live on Story 905 (40.9s execution) and Story 663 (0.5s offline bypass).

#### 📦 Story 66.4: Dynamic Auto-Discovery Benchmark Engine & Nightly Sweep Integration (`[FEAT-495]`)
* **Goal:** Overhaul `Portfolio_Dev/field_notes/bench_models.py` to dynamically query endpoints (`:8000/v1/models`, `:11434/api/tags`, `:8088/v1/models`), discover whichever model is resident on each seat, run standardized throughput/TTFT sweeps, and atomically overwrite `benchmarks_cache.json`.
* **Integration:** Hook `bench_models.py --no-serve` into Step 6 of `HomeLabAI/src/infra/nightly_forge.py` so every morning's benchmarks reflect the latest hardware deployments.

#### 📦 Story 66.5: Passive Real-Time Swarm Telemetry Stream & Live Activity Widget (`[FEAT-496]`)
* **Goal:** Instrument `delegate.py` and `router.py` to automatically append real-world execution metrics (seat, model, tokens, duration, throughput, task type) to `Portfolio_Dev/field_notes/data/live_usage_stream.jsonl`.
* **Dashboard:** Add a live activity widget and rolling 24-hour throughput stream to `benchmarks.html`.

#### 📦 Story 66.6: Federated End-to-End Live Shakedown & Silicon Certification (`[FEAT-497]`)
* **Goal:** Execute live multi-node integration test across all active hardware seats (M5 Air at 16.07 tok/s, Local z87, Cloud Swarm) capturing real workload telemetry, certifying end-to-end pipeline health.

---

### 📚 4. Academic Anchors & Research Pedigree
* **Roofline Model for LLM Inference (*ArXiv:2208.07339*):** Memory bandwidth bounds on Unified Memory vs GDDR6X.
* **Test-Time Compute Scaling / TTCS (*ArXiv:2408.03314*):** Explains why 27B CoT reasoning tokens yield higher code correctness than smaller fast models.
* **Energy-Aware LLM Inference (*ArXiv:2310.03013*):** Energy calculation: $E_{	ext{tok}} = rac{P_{	ext{avg}} 	imes T_{	ext{gen}}}{N_{	ext{tokens}}}$.
