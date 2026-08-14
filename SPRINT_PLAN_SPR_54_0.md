# 📜 SPRINT PLAN: Sprint 54.0 — Preamble & HyDE Division of Labor Inversion

> **Status:** PLANNING / NARRATIVE IN PROGRESS
> **Focus:** Formal Inversion of the Federated Division of Labor: Deep Thought Triage/Preamble vs. Pinky (LoRA) HyDE Synthesis.

---

## 📖 **1. Contextual Narrative & Architectural Background**

### 🏛️ **The Original Blueprint (Sprint 46 Archive)**
When the **"Open HyDE"** concept was first anchored in `00_FEDERATED_STATUS.md` and `SPRINT_PLAN_SPR_46_0.md`, Pinky's roleplay preamble (*"Egad Brain! I bet Glibc C-arenas are caching PyTorch allocations!"*) was captured live to eliminate extra LLM latency:
* **The Intention**: Pinky held our custom fine-tuned **`cli_voice_v1` LoRA** adapters on `z87-Linux`. Because her LoRA was trained directly on 18 years of lab notes, resume artifacts, and validation BKMs, **Pinky possessed the exact domain weights needed to produce high-precision HyDE hypothetical documents** (`[VALIDATION]`, `[STRATEGY]`, `[SRE]`).
* **The Gap**: Deep Thought on Node Kender (RTX 4090) was idle during initial turn ignition while heavy models warmed up.

---

### 🚨 **The Drift & Historical Discovery**
In Sprint 47 (`FEAT-436`/`FEAT-437`), the 3-Tier HyDE Failover Cascade was implemented in `cognitive_hub.py`. During implementation, the order was inverted:
* **What Happened**: `resolve_hyde_vector()` assigned **Tier 1 (HyDE Synthesis)** to Deep Thought on Kender (RTX 4090) and made Pinky a Tier 2 backup failover.
* **The Failure Mode**:
  1. Deep Thought lacks Pinky's fine-tuned LoRA weights, producing generic open-source HyDE strings instead of lab-grounded BKM terms.
  2. If Kender was offline or slow (>8s), the pipeline stalled before falling back to Pinky.
  3. Deep Thought's zero-latency preamble streaming capability at $t=0$ was bypassed during intent triage.

---

### 🔄 **The Inversion Mandate: Restoring the True Division of Labor**
In Sprint 54, we formally invert the pipeline roles to align with model strengths and hardware topology:

```
[User Query]
    │
    ▼ Stage 1: Deep Thought (Kender 4090 / WSL2) at t=0
    ├── 1. Instant Intent Triage & Domain Gate (CASUAL vs DEEP_TECHNICAL)
    └── 2. Zero-Latency UI Preamble Streaming ("Narf! Checking validation logs...")
    │
    ▼ Stage 2: Pinky (z87-Linux / vLLM + LoRA)
    └── 1. Fine-Tuned HyDE Vector Synthesis ([VALIDATION], [STRATEGY], [SRE])
    │
    ▼ Stage 3: ChromaDB Vector Engine (port 8001)
    └── 1. Query ChromaDB using Pinky's LoRA-grounded HyDE vector
    │
    ▼ Stage 4: Round Table Synthesis (Brain / Kender)
    └── 1. Deep Technical Answer & Waterfall Drainer Delivery
```

---

## 🗝️ **2. Key Management & Environment Architecture**

To support OpenRouter model routing without exposing secret keys in git repositories:

* **Location**: Secret keys are stored in `~/.config/environment.d/70-openrouter-key.conf` and exported in `~/.bashrc`.
* **OpenCode Configuration**: Referenced dynamically via `{env:OPENROUTER_API_KEY}` inside `~/.config/opencode/opencode.json`.
* **Git Hygiene**: `*.conf`, `.env`, and secret config files remain strictly outside git boundaries and ignored via `.gitignore`.

---

## 🛠️ **3. Sprint 54 Implementation Stories (Draft / Contextual Stage)**

*(Implementation story details and test specs will be added after final narrative alignment)*
