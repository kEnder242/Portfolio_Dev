# Sprint Plan: [SPR-58.0] Relational Co-Occurrence Mesh & HyDE-Jeopardy Learning Feedback Loops

> **Context:** Evolution of the Federated Lab Learning Architecture (Post-Sprint 55/57). Standardizing on autonomous weight induction, bidirectional associative memory, and hybrid dense-sparse retrieval.

---

## 🏛️ Executive Summary & Introduction

### 1. The Lesson of Raw Notes vs. Distilled Gems
* **The Failure of Raw Notes in Fine-Tuning**: Raw daily engineering notes are terse, non-linear, fragmented, and full of ad-hoc shorthand (`"ran test on pcie, code 3, swapped harness"`). When fed directly to an LLM, the model overfits to syntax fragments rather than engineering wisdom.
* **Why Gems Succeed**: The Nibbler and Curator extract structured **Entity-Relational Tuples**:
  $$\text{Tuple} = (\text{Year/Era}, \text{Platform/Role}, \text{Tool/Technology}, \text{Symptom/Error}, \text{Architectural Nuance})$$
* **The Opportunity (Relational Co-Occurrence Mesh)**: We can mine the 367+ Rank 4/5 gems and 246+ code artifacts to construct a dynamic, bidirectional association graph. When the user asks about a concept (e.g., *"power limiting"*), the model’s internal weights activate the full co-occurrence cluster: `RAPL`, `MSR 0x610`, `PL1/PL2 limits`, `matplotlib`, `2019`, `truncated pyramid`, and `Montana protocol`.

---

## 🔬 ArXiv Research Grounding & Pedigree Mapping

| Research Anchor | ArXiv ID | Theoretical Logic | Lab Implementation & Sprint 58 Coverage | Status |
| :--- | :--- | :--- | :--- | :--- |
| **HyDE** | 2212.10496 | Precise Zero-Shot Dense Retrieval without Relevance Labels. | **Stage 2 Pinky HyDE:** Generates hypothetical document embeddings to seed ChromaDB. | **75% Live** |
| **Query2Doc** | 2303.07678 | Fine-Tuning LLMs for Pseudo-Document Query Expansion. | **LoRA HyDE Priming:** `cli_voice_v1` LoRA trained on 606 pairs to emit dense acronyms & BKMs. | **75% Live** |
| **GenRead** | 2209.10063 | Parametric Context Generation for Dense Retrieval. | **Jeopardy Distillation:** `distill_journal_ledger()` trains LoRA on bidirectional gem triggers. | **80% Live** |
| **Self-RAG** | 2310.11511 | Learning to Retrieve, Generate, and Critique via Reflection. | **Refinement Loop:** Tri-Field Gem Schemas (`trigger_context`, `anchors`) & Hybrid RiR Gating. | **60% Live** |

---

## 🔄 Master Data Lifecycle & Learning Feedback Loops

Below is the true data lifecycle tracing how unstructured historical notes transform into synaptic model weights and live conversational retrieval:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 1. UNSTRUCTURED SOURCES                                 │
│             ~/raw_notes (2005–2025 TXT/MD)  +  Standalone Code Artifacts & BKMs        │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                            2. CHUNKING & CLASSIFICATION                                │
│          scan_librarian.py  ──▶  Classifies by Team/Era (PIAV, PAE, DSD, EPSD)         │
│          scan_queue.py      ──▶  Splits into chronological 1KB–4KB chunks              │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              3. INITIAL SYNTHESIS & GEMS                                │
│       nibble_v2.py (Local LLM)  ──▶  Extracts Summary, Technical Gem, and Evidence     │
│       Timeline Archives         ──▶  Stored in 20XX.json (Default Rank 2/3)            │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        4. AUTONOMOUS REFINEMENT (3:00–5:00 AM)                         │
│       refine_gem.py (BKM Protocol) ──▶ Upgrades to Rank 4 / Rank 5 (Tri-Field Schema)  │
│       clean_duplicates.py          ──▶ Semantic de-duplication (0.85 cosine thresh)    │
│       aggregate_years.py           ──▶ Aggregates months into consolidated year trees   │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                       5. INSTRUCTION DISTILLATION (05:00 AM)                           │
│       distill_journal_ledger()     ──▶ Converts Rank 4/5 gems + Code Tools to Q&A pairs │
│       journal_ledger.jsonl         ──▶ Dataset grows autonomously (606 active pairs)   │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                       6. WEIGHT INDUCTION & FORGE (02:00 AM)                           │
│       quiesce_vllm()               ──▶ POST /release_nodes (VRAM drops to 620MB)       │
│       train_expert.py              ──▶ Unsloth 4-bit QLoRA on RTX 2080 Ti (60 steps)   │
│       cli_voice_v1 Adapter         ──▶ 97.3 MB safetensors compiled & saved            │
│       re_ignite_vllm()             ──▶ vLLM reloads base model + hot-loads new LoRA    │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                     7. LIVE CONVERSATIONAL RETRIEVAL (INTERCOM)                        │
│       Stage 1 (Deep Thought / KENDER) ──▶ Preamble & Intent Triage                    │
│       Stage 2 (Pinky + LoRA)          ──▶ HyDE Query Expansion (Domain Terms)         │
│       Stage 3 (ChromaDB + RiR Grep)   ──▶ Hybrid Dense-Sparse Vector Retrieval        │
│       Stage 4/5 (Brain + Pinky)       ──▶ Evidence-First Verified Response             │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 💎 The Tri-Field Gem Schema (Machine-Readable Specification)

### 1. JSON Schema Definition
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TriFieldGem",
  "type": "object",
  "required": ["summary", "trigger_context", "technical_gem", "anchors", "rank"],
  "properties": {
    "summary": {
      "type": "string",
      "description": "Sharp 1-line summary of the engineering accomplishment or event."
    },
    "trigger_context": {
      "type": "string",
      "description": "The exact problem scenario, debug condition, or engineering question that triggers this knowledge."
    },
    "technical_gem": {
      "type": "string",
      "description": "Concrete tool name, register/MSR offset, script, or architectural BKM used to resolve it."
    },
    "anchors": {
      "type": "array",
      "items": { "type": "string" },
      "description": "3-6 exact technical acronyms, tools, error codes, or hardware terms (e.g. ['RAPL', 'MSR 0x610', 'PECI', 'PythonSV'])."
    },
    "rank": {
      "type": "integer",
      "enum": [4, 5],
      "description": "4 for High-Fidelity Technical Gem, 5 for Diamond Wisdom."
    },
    "tags": {
      "type": "array",
      "items": { "type": "string" }
    }
  }
}
```

### 2. Concrete Example Instance
```json
{
  "summary": "PECI sideband command throughput validation under high thermal load",
  "trigger_context": "When benchmarking sideband telemetry command rates and diagnosing PECI bus saturation",
  "technical_gem": "Developed pecistressor.py achieving ~5300 cmd/sec sideband command throughput across OpenBMC endpoints",
  "anchors": ["PECI", "pecistressor.py", "OpenBMC", "Sideband", "DTTC_2022"],
  "rank": 4,
  "tags": ["telemetry", "sideband", "peci", "firmware"]
}
```

---

## 🧭 Honest System Assessment: What is Live vs. What is Next

| Architecture Component | Status | Implementation Details |
| :--- | :--- | :--- |
| **Raw Note Ingestion** | **LIVE (100%)** | 0 pending chunks in `queue.json`. 18 years synthesized. |
| **Gem Refinement Loop** | **LIVE (94.5%)** | 347 out of 367 timeline events are already Rank 4/5. `refine_gem.py` updated to Tri-Field Schema. |
| **Code Artifact Distillation** | **LIVE (100%)** | `distill_journal_ledger()` extracts Rank 4/5 gems AND `artifacts_*.json` into `journal_ledger.jsonl` (606 pairs). |
| **Nightly Unsloth LoRA** | **LIVE (100%)** | REST Quiesce $\rightarrow$ 60-step Unsloth $\rightarrow$ Re-ignition running automatically at 2:00 AM. |
| **HyDE Query Expansion** | **LIVE (75%)** | Stage 2 Pinky generates HyDE queries using `cli_voice_v1` LoRA weights. |
| **RAG + Regex / Grep (Hybrid RiR)**| **LIVE (MCP Only)**| `peek_related_notes` in `archive_node.py` uses keyword search. Stage 3 ChromaDB lookup in Foyer is dense vector; ready for hybrid sparse-dense fusion. |

---

## ⏰ Verified Nightly Execution Timeline (Sprint 58 Standard)

```text
02:00 AM ──▶ 1. Heavy LoRA Forge Pass (02:00 – 02:20 AM)
                - POST /release_nodes -> Quiesce VRAM to 620MB -> 60-step Unsloth LoRA -> Re-ignite Foyer to OPERATIONAL.

02:20 AM ──▶ 2. Autonomous Recruiter & Diagnostics (02:20 – 02:40 AM)
                - Target acquisition sweep -> Prometheus KPI export.

02:40 AM ──▶ 3. 20-Min Settling & Buffer Window (02:40 – 03:00 AM)
                - System returns to stable OPERATIONAL baseline.

03:00 AM ──▶ 4. Active Mass Scan Refinement Window (03:00 – 05:00 AM)
                - 2 Hours of polite 60s gem refinement (~100 items upgraded to Rank 4 with Tri-Field Schema).
                - 05:00 AM Cutoff triggers: Step 6 TLC runs de-duplication, aggregation, and auto-distills new gems into journal_ledger.jsonl.

05:00 AM ──▶ 5. Subconscious Dreaming (05:00 – 05:25 AM)
                - Reads newly upgraded Rank 4 gems -> Synthesizes "Diamond Wisdom" abstracts.

05:25 AM ──▶ 6. While-You-Were-Out (WYWO) Synthesis (05:25 – 05:40 AM)
                - Generates executive morning briefing -> Pulses Neural Pager.

05:40 AM ──▶ 7. Clean Quiesce & H2 Lean Sleep (05:40 – 06:00 AM)
                - Lab rests in low-power idle, ready for your morning session.
```

---

## 🎯 Sprint 58 User Stories: Agentic-R Retrieval Enhancement (ArXiv: 2601.11888)

### Story 58.1: Marginal Utility Re-Ranking (Maximal Marginal Relevance - MMR)
* **Goal**: Upgrade `get_context()` in `HomeLabAI/src/nodes/archive_node.py` to rank multi-collection ChromaDB candidates using a Marginal Information Utility penalty.
* **Mechanism**: Candidate chunks are scored by $\text{Score}(d) = \lambda \cdot \text{Sim}(d, q) - (1-\lambda) \cdot \max_{d_j \in S} \text{Sim}(d, d_j)$. Prevents redundant chunks and boosts orthogonal technical details (MSR offsets, script flags, error codes).
* **Target Files**: `HomeLabAI/src/nodes/archive_node.py`, `HomeLabAI/src/tests/test_archive_rrf.py`.

### Story 58.2: Autonomous Search Pivot Loop (Grep-Gated RiR Pivot)
* **Goal**: Implement an autonomous search pivot loop when ChromaDB vector distance exceeds threshold ($>0.50$) or returns generic summaries without technical anchors.
* **Mechanism**: Uses fast `ripgrep` across `Portfolio_Dev/field_notes/data/` for the exact extracted hardware anchors (`["RAPL", "0x610", "PECI"]`). Injects exact line-level evidence into the context before response synthesis.
* **Engine Choice**: **`ripgrep` (`grep`)** is chosen over `peek_related_notes` because it returns raw evidence and surrounding lines in $<5\text{ms}$ with zero intermediate JSON abstraction latency.
* **Target Files**: `HomeLabAI/src/nodes/archive_node.py`, `HomeLabAI/src/v5/foyer/router.py`.

### Story 58.3: Silicon Power Capping & Hardware Surge Protection [LAB-109]
* **Goal**: Prevent hardware PSU over-current trips and voltage sag on the Z87 host during heavy backward passes by capping RTX 2080 Ti TDP to 165W (down from 250W stock).
* **Mechanism**: Enforce `sudo nvidia-smi -pl 165` at system startup via `set_gpu_power_cap.service` and verify power cap in `nightly_forge.py` pre-flight checks.
* **Target Files**: `HomeLabAI/src/infra/nightly_forge.py`, `HomeLabAI/config/systemd/gpu-power-limit.service`.
* **Delegation Verification**: Probe `nvidia-smi -q -d POWER` to confirm power limit is clamped to 165W.

### Story 58.4: Unsloth Gradient Smoothing & Hardware Pacing [FEAT-452]
* **Goal**: Smooth out GPU tensor core power spikes, pace computation, and eliminate abrupt $di/dt$ current surges during Unsloth LoRA fine-tuning.
* **Mechanism**: Update `HomeLabAI/src/forge/train_expert.py` to:
  1. Add `HardwarePacingCallback` with a 50ms (`time.sleep(0.05)`) settling delay on each optimization step end.
  2. Use `per_device_train_batch_size = 1` and `gradient_accumulation_steps = 4` (effective batch size 4).
  3. Extend warmup to `warmup_steps = 10` for smooth gradient transitions.
  4. Clamp `max_seq_length = 1536` to bound matrix multiplication memory surges.
* **Target Files**: `HomeLabAI/src/forge/train_expert.py`, `HomeLabAI/src/tests/test_forge_distillation_unit.py`.
* **Delegation Verification**: Execute 10-step dry run; observe DCGM telemetry verifying GPU power remains $<165\text{W}$ with smooth step transitions and clean adapter output.

### Story 58.5: Post-Maintenance Morning Autonomous Re-ignition [FEAT-453]
* **Goal**: Prevent multi-day lab dormancy by ensuring the Foyer and vLLM are automatically re-ignited to `OPERATIONAL` state following the 05:00 AM – 05:40 AM mass scan and dreaming sweep.
* **Mechanism**: Add an explicit final re-ignition and health check at the end of `nightly_forge.py` to wake the Foyer and leave inference nodes active for morning sessions.
* **Target Files**: `HomeLabAI/src/infra/nightly_forge.py`, `HomeLabAI/src/tests/test_nightly_forge_shakedown.py`.
* **Delegation Verification**: Unit test asserting `re_ignite_vllm()` is called post-dreaming and verifies HTTP 200 from `/status_update`.

---

## 📝 Sprint 58 Retrospective: Cumulative Replay vs. Continual Drift & Gem Evolution

### 1. Cumulative Full-Replay vs. Continual Drift
* **The Continual Learning Failure Mode**: If an LLM is fine-tuned iteratively on top of yesterday's LoRA adapter (continual fine-tuning without replay), it rapidly suffers from **Catastrophic Forgetting** and **Gradient Drift**, causing loss explosion and repetition loops within 5–10 cycles.
* **The BKM Solution (Cumulative Replay)**: The *dataset* (`journal_ledger.jsonl`) is what grows iteratively (from 13 samples $\rightarrow$ 360 note pairs $\rightarrow$ 593 total pairs). Each night at 02:00 AM, `train_expert.py` applies the entire accumulated dataset to a clean base model (`Llama-3.2-3B-Instruct`), compiling a fresh **97.3 MB** adapter in just **~3 to 5 minutes**. This guarantees:
  1. **Zero Catastrophic Forgetting**: 2005 EFI automation is remembered with the exact same clarity as 2024 RAPL telemetry.
  2. **Pristine Weight Health**: Mathematical gradients remain regularized and grounded.
  3. **True Incremental Growth**: Every morning, the model knows everything it knew previously *plus* all newly refined gems and code artifacts.

### 2. Backward Compatibility & Gem Upgrades
* **Graceful Degradation**: Older Rank 4 gems containing only `summary` and `technical_gem` are automatically assigned clean fallback trigger questions during distillation.
* **Continuous Polish**: As the nightly scanner runs during the 3:00 AM – 5:00 AM window, older gems will naturally receive Tri-Field enrichment (`trigger_context`, `anchors`) over future epochs.

### 3. Shakedown Certification
* All 7 test cases across `test_forge_distillation_unit.py` and `test_nightly_forge_shakedown.py` passed with 100% integrity, certifying the 2:00 AM automated pipeline for live production execution.
