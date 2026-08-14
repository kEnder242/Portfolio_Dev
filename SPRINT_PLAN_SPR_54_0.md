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

### 🚨 **The Inversion Discovery & Sprint 51/52 Forensics**
A forensic search across the sprint archives revealed that the formal **5-Stage Division of Labor Inversion** was documented in **Sprint 51 and Sprint 52** ([`SPRINT_51_EXECUTION_LEDGER.md:L115-159`](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/SPRINT_51_EXECUTION_LEDGER.md#L115-L159) and [`SPRINT_PLAN_SPR_52_0.md:L22-30`](file:///home/jallred/Dev_Lab/Portfolio_Dev/SPRINT_PLAN_SPR_52_0.md#L22-L30)):

* **Sprint 46–48 Baseline**: Deep Thought generated HyDE vectors sequentially inside `cognitive_hub.py`, missing Pinky's fine-tuned LoRA domain weights.
* **Sprint 51 Execution Ledger**: Formally reshuffled the pipeline into the **5-Stage Waterfall**:
  1. **Stage 1 (Deep Thought on Kender 4090 / $t=0$)**: Zero-Latency Preamble & Intent Triage (*"Narf! Checking validation logs..."*).
  2. **Stage 2 (Pinky vLLM + LoRA)**: Pinky generates the 3-Part HyDE hypothetical document (`[VALIDATION]`, `[STRATEGY]`, `[SRE]`) using her fine-tuned `cli_voice_v1` LoRA weights.
  3. **Stage 3 (Brain Node)**: ChromaDB vector retrieval & short technical answer.
  4. **Stage 4 (Deep Thought)**: Strategic Synthesis if `importance >= 0.7`.
  5. **Stage 5 (Pinky Out-Loud & Drainer)**: Final vibe review & Waterfall Drainer Pop delivery.

---

### 🔄 **The Inversion Mandate: Restoring the True Division of Labor**
In Sprint 54, we implement and certify this exact 5-stage architecture in code (`cognitive_hub.py` and `router.py`):

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

## 🏛️ **4. Core Architectural Patterns Incorporated from Backlog Audit**

From our audit of the previous overwrite (Task 53.7/53.8 in `SPRINT_PLAN_SPR_52_0.md`), we are explicitly incorporating the following **high-value design patterns** into Sprint 54:

1. **3-Tier Memory Topography**:
   - **Layer 1 (Bedrock Tier)**: Star artifacts + `career_compass.json` Tier 1 Anchor Map (<300 tokens) loaded directly into system prompt context.
   - **Layer 2 (Archive Tier / KB)**: ChromaDB vector collections (`artifact_vault`, `journal_kb`, `lab_journal`). Targeted by Pinky's LoRA-grounded HyDE vectors.
   - **Layer 3 (Raw Telemetry Tier)**: Real-time hardware telemetry (`nvidia-smi` / DCGM GPU metrics, RAPL power caps) + raw notes in `~/knowledge_base`.

2. **BKM-015 Compliance (Judge-Driven Casual Exit)**:
   - Zero hardcoded keyword arrays or regex pre-baked HyDE bypass lists.
   - HyDE synthesis is judge-driven: if a query does not match the 4 KB domains (e.g. casual turn `"hi"`), HyDE synthesis naturally evaluates to empty `""`, letting the ChromaDB query exit cleanly without forcing a hallucinated vector.

3. **Dynamic HyDE Prompt Loading (`data/hyde_domain_map.json`)**:
   - Extract hardcoded prompt text in `HYDE_SYNTHESIS_PROMPT` out of Python inline code into `HomeLabAI/src/data/hyde_domain_map.json`.
   - `cognitive_hub.py` loads `hyde_domain_map.json` dynamically at startup with non-fatal fallback.

4. **Real VRAM Probing & Gauntlet Repair (`[FEAT-456]`)**:
   - Integrate `pynvml` / `nvidia-smi` VRAM probing into `nightly_forge.py` and repair `run_live_lab_gauntlet.sh` verifier paths.

