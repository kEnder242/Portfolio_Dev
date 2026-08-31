# 🚀 SPRINT PLAN: SPR-66.0
## Federated Silicon Benchmarking Engine & Dynamic Swarm Aliases

---

### 🏛️ 1. Executive Summary & Architectural Vision
Sprint 66.0 transforms [`benchmarks.html`](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/benchmarks.html) from a stale single-node RTX 2080 Ti snapshot into a **Federated Silicon & ROI Telemetry Workbench**. It also introduces a centralized **Swarm Model Alias Registry** (`[FEAT-493]`) in `infrastructure.json` that decouples agent roles from transient upstream checkpoint names, enabling seamless model swaps and unified fallback flows across all 4 hardware seats.

---

### 📐 2. The 4 Federated Hardware Seats

| Seat | Hardware Topography | Primary Resident Model | Memory Architecture | Target Role |
|:---|:---|:---|:---|:---|
| **Apple M5 Air** (`:8000`) | Apple Silicon M5 (24GB Unified) | `mlx-community--Qwen3.8-27B-4bit` | 16.8GB Unified RAM | **Deep Architectural Reasoning & Planner** |
| **Windows Kender** (`:11434`) | NVIDIA RTX 4090 (24GB VRAM) | `qwen2.5-coder:14b` | 1,008 GB/s GDDR6X | **High-Throughput Interactive Coding** |
| **Linux z87** (`:8088`) | NVIDIA RTX 2080 Ti (11GB VRAM) | `Llama-3.2-3B-AWQ` | 616 GB/s GDDR6 | **Sensory Foyer & Multi-LoRA Engine** |
| **Cloud Swarm** (`:4097`) | Distributed Cloud Cluster | Dynamic Free Tier (`openrouter/free`) | Cloud High-Context | **Swarm Fallbacks & Cross-Review** |

---

### 🎯 3. Sprint Epics & User Stories

```
SPRINT 66.0
├── [STORY 66.1] Centralized Swarm Model Alias Registry (FEAT-493)
├── [STORY 66.2] benchmarks.html 3-Tab Overhaul & Live Shakedown Engine (FEAT-494)
└── [STORY 66.3] Multi-Strategy Swarm Delegation Shakedown (Prompt Experimentation)
```

#### 📦 Story 66.1: Centralized Swarm Model Alias Registry (`[FEAT-493]`)
* **Goal:** Define logical aliases (`champion_reasoner`, `champion_coder`, `fast_worker`, `fallback_tier`) in `HomeLabAI/config/infrastructure.json`.
* **Mechanism:** Wire `delegate.py` and OpenCode config to resolve aliases dynamically, so swapping a model on M5 Air or Kender requires updating only a single line in `infrastructure.json`.

#### 📦 Story 66.2: `benchmarks.html` 3-Tab Overhaul & Live Shakedown Runner (`[FEAT-494]`)
* **Goal:** Replace stale Grafana iframes and static bars with a modern 3-tab workbench:
  * **Tab 1: 🏛️ Silicon Arena:** Side-by-side card grid comparing M5 Unified vs RTX 4090 vs RTX 2080 Ti vs Cloud Swarm with live status badges.
  * **Tab 2: ⚡ Energy & Financial ROI:** Joules per 1k tokens ($\text{J}/\text{kTok}$), power draw envelopes, and cumulative local dollar savings counter vs Claude 3.5 API rates ($3.00/MTok).
  * **Tab 3: 🧠 Intelligence Quotient & CoT:** Reasoning Token Ratio ($\text{CoT} / \text{Output}$), Parameter density, and coding Elo ratings.
  * **Live Shakedown Engine:** A vanilla JS "⚡ Run Live Shakedown" button that dispatches a test payload to all reachable seats and renders live stage waterfalls.

#### 📦 Story 66.3: Multi-Strategy Swarm Delegation Shakedown
* **Goal:** Concurrently offload isolated tasks to `delegate.py` while testing distinct prompt engineering styles:
  * *Style A:* Strict BKM Specification (Hard tool mandates, line numbers).
  * *Style B:* Goal-Oriented Relaxed Specification (High-level criteria, agent autonomy).
* **Evaluation:** Capture and evaluate Handover Reflections to determine optimal prompt density.

---

### 📚 4. Academic Anchors & Research Pedigree
* **Roofline Model for LLM Inference (*ArXiv:2208.07339*):** Memory bandwidth bounds on Unified Memory vs GDDR6X.
* **Test-Time Compute Scaling / TTCS (*ArXiv:2408.03314*):** Explains why 27B CoT reasoning tokens yield higher code correctness than smaller fast models.
* **Energy-Aware LLM Inference (*ArXiv:2310.03013*):** Energy calculation: $E_{\text{tok}} = \frac{P_{\text{avg}} \times T_{\text{gen}}}{N_{\text{tokens}}}$.
