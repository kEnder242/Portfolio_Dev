# Sprint Plan: [SPR-58.0] Relational Co-Occurrence Mesh & HyDE-Jeopardy Learning Feedback Loops

> **Context:** Evolution of the Federated Lab Learning Architecture (Post-Sprint 55/57). Standardizing on autonomous weight induction, bidirectional associative memory, and hybrid dense-sparse retrieval.

---

## 🏛️ Executive Summary & Introduction

### 1. The Lesson of Raw Notes vs. Distilled Gems
* **The Failure of Raw Notes in Fine-Tuning**: Raw daily engineering notes are terse, non-linear, fragmented, and full of ad-hoc shorthand (`"ran test on pcie, code 3, swapped harness"`). When fed directly to an LLM, the model overfits to syntax fragments rather than engineering wisdom.
* **Why Gems Succeed**: The Nibbler and Curator extract structured **Entity-Relational Tuples**:
  $$\\text{Tuple} = (\\text{Year/Era}, \\text{Platform/Role}, \\text{Tool/Technology}, \\text{Symptom/Error}, \\text{Architectural Nuance})$$
* **The Opportunity (Relational Co-Occurrence Mesh)**: We can mine the 367+ Rank 4/5 gems to construct a dynamic, bidirectional association graph. When the user asks about a concept (e.g., *"power limiting"*), the model’s internal weights activate the full co-occurrence cluster: `RAPL`, `MSR 0x610`, `PL1/PL2 limits`, `matplotlib`, `2019`, `truncated pyramid`, and `Montana protocol`.

---

## 🔄 Master Data Lifecycle & Learning Feedback Loops

Below is the true data lifecycle tracing how unstructured historical notes transform into synaptic model weights and live conversational retrieval:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 1. UNSTRUCTURED SOURCES                                 │
│             ~/raw_notes (2005–2025 TXT/MD)  +  HomeLabAI/docs/Protocols.md             │
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
│       refine_gem.py (BKM Protocol) ──▶ Upgrades to Rank 4 / Rank 5 (Diamond Wisdom)   │
│       clean_duplicates.py          ──▶ Semantic de-duplication (0.85 cosine thresh)    │
│       aggregate_years.py           ──▶ Aggregates months into consolidated year trees   │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                       5. INSTRUCTION DISTILLATION (05:00 AM)                           │
│       distill_journal_ledger()     ──▶ Converts Rank 4/5 gems into Q&A dialogue pairs  │
│       journal_ledger.jsonl         ──▶ Dataset grows autonomously (currently 360 pairs)│
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

## 🧭 Honest System Assessment: What is Live vs. What is Next

| Architecture Component | Status | Implementation Details |
| :--- | :--- | :--- |
| **Raw Note Ingestion** | **LIVE (100%)** | 0 pending chunks in `queue.json`. 18 years synthesized. |
| **Gem Refinement Loop** | **LIVE (94.5%)** | 347 out of 367 timeline events are already Rank 4/5. |
| **Autonomous Distillation** | **LIVE (100%)** | `distill_journal_ledger()` extracts Rank 4/5 gems into `journal_ledger.jsonl` (360 pairs). |
| **Nightly Unsloth LoRA** | **LIVE (100%)** | REST Quiesce $\\rightarrow$ 60-step Unsloth $\\rightarrow$ Re-ignition running automatically at 2:00 AM. |
| **HyDE Query Expansion** | **LIVE (Partial)** | Stage 2 Pinky generates HyDE queries, but currently relies on conversational LoRA rather than explicit relational training. |
| **Bidirectional Jeopardy LoRA** | **NEXT (SPR-58)** | Need to format distillation pairs into explicit bidirectional forward/reverse triplets. |
| **RAG + Regex / Grep (Hybrid RiR)**| **LIVE (MCP Only)**| `peek_related_notes` in `archive_node.py` uses keyword search, but Foyer Stage 3 ChromaDB lookup is purely dense vector. Needs hybrid lexical-dense fusing (BM25/grep + vector). |

---

## 🧠 Deep Dive: The "HyDE-Jeopardy" & Relational Mapping Strategy

### 1. Does LoRA Work on Natural Language or Raw Triplets?
* **How LoRA Learns**: LoRA (Low-Rank Adaptation) adjusts the low-rank attention projection matrices ($W_q, W_v$) within the transformer layers. It learns the **conditional probability distribution of token sequences** in natural language.
* **Why Pure Triplets (e.g. `RAPL -> 2019`) Are Insufficient**: Raw knowledge-graph triplets lack conversational syntax, leading to unnatural, stilted generation.
* **The Solution: Natural Language Wrappers for Triplets**:
  We format each relational edge into conversational natural language pairs that teach the model to bridge concepts bidirectionally:

$$\\begin{aligned}
\\text{Forward Query} &: \\text{"User: What validation framework was used for RAPL in 2019?"} \\
&\\quad\\rightarrow \\text{"Pinky: In 2019, RAPL power-limiting validation utilized RAPL-Sim with Matplotlib visualization."} \\
\\text{Reverse Query} &: \\text{"User: What telemetry and power tools were active during the 2019 validation cycle?"} \\
&\\quad\\rightarrow \\text{"Pinky: The 2019 cycle featured RAPL power sweeps, Montana protocol logger suppression, and Python ML time-series data."} \\
\\text{Relational Nuance} &: \\text{"User: How does the Montana protocol connect to RAPL telemetry?"} \\
&\\quad\\rightarrow \\text{"Pinky: The Montana protocol was designed to prevent logger hijacking during high-frequency RAPL telemetry polling."}
\\end{aligned}$$

---

## 🔎 RAG + RegExp / Grep: Hybrid Retrieval (The ArXiv "RiR" Pattern)

### 1. What We Currently Have
* In [`HomeLabAI/src/nodes/archive_node.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/nodes/archive_node.py), we have `peek_related_notes(keyword)` (RLM Research Pattern) which performs keyword searches across text files.

### 2. The ArXiv "RiR" (Retrieval-in-Retrieval) Pattern
* **Dense Vector Failure Mode**: ChromaDB embeddings sometimes suffer from "semantic blur" where a rare acronym (e.g. `PECI`, `RAKP`, `MSR 0x610`) gets drowned out by broad semantic similarity.
* **The Hybrid Solution (Dense Vector + Exact Lexical Grep)**:
  1. **Stage 2 (Pinky HyDE)** emits both a dense search query AND a list of exact regex tokens (`["RAPL", "0x610", "2019"]`).
  2. **Stage 3 (Hybrid Retriever)**:
     - Runs ChromaDB dense vector query for top-10 chunks.
     - Runs `ripgrep` / regex filter across `Portfolio_Dev/field_notes/data/` for exact token hits.
     - Intersects / re-ranks results using Reciprocal Rank Fusion (RRF).
  3. **Result**: Zero false positives on exact technical terms while retaining broad semantic understanding.

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
                - 2 Hours of polite 60s gem refinement (~100 items upgraded to Rank 4).
                - 05:00 AM Cutoff triggers: Step 6 TLC runs de-duplication, aggregation, and auto-distills new gems into journal_ledger.jsonl.

05:00 AM ──▶ 5. Subconscious Dreaming (05:00 – 05:25 AM)
                - Reads newly upgraded Rank 4 gems -> Synthesizes "Diamond Wisdom" abstracts.

05:25 AM ──▶ 6. While-You-Were-Out (WYWO) Synthesis (05:25 – 05:40 AM)
                - Generates executive morning briefing -> Pulses Neural Pager.

05:40 AM ──▶ 7. Clean Quiesce & H2 Lean Sleep (05:40 – 06:00 AM)
                - Lab rests in low-power idle, ready for your morning session.
```
