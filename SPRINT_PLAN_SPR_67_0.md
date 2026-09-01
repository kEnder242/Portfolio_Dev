# 🚀 SPRINT PLAN: SPR-67.0
## Deep Thought Migration to Apple M5 Air & Role-Hardware Decoupling

---

### 🏛️ 1. Executive Summary & Architectural Assessment
Sprint 67.0 migrates the **Deep Thought** strategic synthesis & speculative triage persona from Windows KENDER (RTX 4090) to the **Apple M5 Air** (`192.168.1.46:8000`). 

This migration takes full advantage of the M5 Air's **24GB Unified Memory (32k context)** and **18W power envelope (0.901 Tokens/Joule)** for deep Test-Time Compute Scaling (`Qwen3.8-27B-4bit` CoT reasoning), while leaving the Windows RTX 4090 free to focus 100% on high-throughput coding tasks (100+ tok/s).

---

### 🔍 2. Edge Cases & Hard-Coding Audit

| Subsystem | Previous State (Hardcoded / Fragile) | Remediated State (Role-Hardware Decoupled) |
|:---|:---|:---|
| **Configuration** | `infrastructure.json` hardcoded `nodes.thought.primary = "KENDER"` | Decoupled: `nodes.thought.primary = "M5_AIR"`, `fallback = "KENDER"`, `local_fallback = "localhost"`. |
| **Variable Naming** | Role names mixed with hardware names (`KENDER_HOST`, `stage1_kender_triage`) | Standardized on **`DEEP_THOUGHT_HOST`** / **`DEEP_THOUGHT_ENDPOINT`** as requested. |
| **API Protocol** | `_probe_ollama()` assumed all remote seats ran Ollama `/api/tags` | Dual Protocol Prober: Supports **OpenAI `/v1/models` (oMLX)** on M5 Air and **Ollama `/api/tags`** on KENDER. |
| **Liveliness & Sticking** | Speculative relay only checked Kender | **Ping-First & Stick:** Probes M5 Air (`:8000`) first. If alive, sticks to M5 Air. If sleeping, falls back to Kender (`:11434`), then local vLLM (`:8088`). |
| **System Prompts** | `thought_node.py` hardcoded "(Resident on RTX 4090 / Node Kender)" | Prompt updated to "Strategic Synthesis Node (Resident on Sovereign Lab Silicon)". |

---

### 📐 3. The 4 Federated Hardware Tiers & Roles

| Role Variable | Primary Target | Fallback Target | Engine / Protocol | Memory & Context | Target Persona |
|:---|:---|:---|:---|:---|:---|
| **`DEEP_THOUGHT`** | **Apple M5 Air (`:8000`)** | Windows 4090 (`:11434`) | `oMLX` / OpenAI REST | 24GB Unified / 32k context | Strategic Synthesis, HyDE, Triage |
| **`CHAMPION_CODER`**| **Windows 4090 (`:11434`)**| Apple M5 Air (`:8000`) | Ollama / REST | 24GB GDDR6X / 32k context | High-throughput Code Execution |
| **`SENSORY_FOYER`** | **Linux z87 (`:8088`)** | localhost (`:11434`) | vLLM Multi-LoRA | 11GB GDDR6 / 8k context | Pinky Voice, LoRA Adapters, Ear |
| **`SWARM_FALLBACK`**| **Cloud Swarm (`:4097`)** | openrouter/free | OpenCode REST | Cloud 128k context | Cross-Review & Fallbacks |

---

### 🎯 4. Sprint Epics & User Stories

```
SPRINT 67.0
├── [STORY 67.1] Role-Hardware Abstraction & Config Decoupling (FEAT-499)
├── [STORY 67.2] Unified Deep Thought Multi-Seat Prober & Dual-Check Gate (FEAT-500)
├── [STORY 67.3] Foyer Division of Labor & UI Stage Ledger Realignment
└── [STORY 67.4] Live 5x5 Gauntlet Shakedown & Silicon Validation (FEAT-501)
```

#### 📦 Story 67.1: Role-Hardware Abstraction & Config Decoupling (`[FEAT-499]`)
* **Goal:** Update `HomeLabAI/config/infrastructure.json` to assign `nodes.thought.primary = "M5_AIR"` and update `thought_node.py` system prompts to remove hardcoded machine names.

#### 📦 Story 67.2: Unified Deep Thought Multi-Seat Prober & Dual-Check Gate (`[FEAT-500]`)
* **Goal:** Refactor `speculative_triage.py` and `cognitive_hub.py` to use `DEEP_THOUGHT_HOST`, supporting both OpenAI REST (`/v1/models`) and Ollama (`/api/tags`), with a ping-first M5 Air policy that sticks to reachable endpoints.

#### 📦 Story 67.3: Foyer Division of Labor & UI Stage Ledger Realignment
* **Goal:** Refactor `router.py` to rename `stage1_kender_triage` $ightarrow$ `stage1_deep_thought_triage` and map Deep Thought persona execution to M5 Air.

#### 📦 Story 67.4: Live 5x5 Gauntlet Shakedown & Silicon Validation (`[FEAT-501]`)
* **Goal:** Execute live 5x5 multi-turn integration test across the running Foyer, certifying speculative triage, HyDE resolution, and strategic synthesis on M5 Air.

---
