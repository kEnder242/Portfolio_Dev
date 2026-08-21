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
