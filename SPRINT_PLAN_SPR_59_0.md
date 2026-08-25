# 🚀 Sprint Plan SPR-59.0: Architectural Triage & Research Evaluation Matrix

**Sprint:** 59.0  
**Date:** August 25, 2026  
**Status:** PLANNING & TRIAGE  
**Theme:** *Strategic Alignment & "Good Fit" Evaluation (Avoiding the Bolt-on Trap)*

---

## 🎯 Executive Summary & Philosophy

As the Federated Lab matures past Sprint 58, our objective is **architectural discipline**. Rather than bolting on every novel paper because "we can," Sprint 59 focuses on rigorous **Feasibility & Impact Evaluation** of our collected research against real-world hardware limits (Z87 Haswell host, 11GB RTX 2080 Ti, 16GB DDR3 RAM).

---

## 🔬 Candidate Research Synthesis Report (Google Keep Ingestion)

### **Category A: Memory & Long-Range Context Architecture**

#### 1. **HOLA: Hippocampal Linear Attention** (Wikitext / SlimPajama)
* **Core Concept**: Pairs a compressive recurrent state (delta-rule) with a bounded exact KV cache as a semi-parametric test-time memory. Recurrent state handles linearly compressible structure; exact cache stores high-entropy needle associations without learned eviction thrashing.
* **Fit Evaluation**:
  * *Strengths*: Solves the classic "needle-in-a-haystack" decay of pure SSMs / linear RNNs while keeping VRAM bounded.
  * *Risks*: Requires custom linear attention kernels or modified model architectures; may not directly drop into off-the-shelf Llama-3.2 HuggingFace weights without custom Triton training.

#### 2. **AutoMem: Automated Learning of Memory as a Cognitive Skill** (`[2607.01224]`)
* **Core Concept**: Treats memory read, write, update, and eviction as an explicit, policy-trained cognitive action rather than passive RAG stuffing.
* **Fit Evaluation**:
  * *Strengths*: Highly compatible with Pinky's `ArchiveMemory` and `peek_related_notes` tool-use paradigm.
  * *Risks*: Adds decision overhead to every prompt cycle if not compiled into prompt guardrails.

#### 3. **LightMem-Ego: AI Memory for Everyday Life** (`[2607.11487]`)
* **Core Concept**: Lightweight, edge-optimized episodic memory condensation for personal lifelong assistance.
* **Fit Evaluation**:
  * *Strengths*: Directly aligns with our 18-year career timeline and Field Manual synthesis.

---

### **Category B: Evaluators, Judges & Gating Lifecycles**

#### 1. **Ask, Don't Judge: Binary Questions for Interpretable Evaluation** (`[2606.27226]`)
* **Core Concept**: Replaces fuzzy numeric scoring (1–5 Likert scales) with deterministic batteries of atomic boolean questions (`is_code_tested?`, `does_msr_match?`, `is_error_logged?`).
* **Fit Evaluation**:
  * *Strengths*: **Extremely high fit.** Eliminates LLM judge score drift in the Cynical Curator and Validation Ledger; runs cleanly on small 3B models without ambiguity.
  * *Risks*: Requires upfront definition of atomic question checklists.

#### 2. **Netflix Production LLM Judge Lifecycle (Reasoning-Aligned Rubric Tuning)**
* **Core Concept**: Treats the judge as a 4-phase lifecycle (*Birth $\rightarrow$ Rubric Tuning $\rightarrow$ Dual-Role Deployment $\rightarrow$ Drift Monitoring*) rather than a static prompt.
* **Fit Evaluation**:
  * *Strengths*: Standardizes how the Validation Methodology ledger audits historical gems and synthetic QA pairs.
  * *Risks*: Higher governance complexity; best implemented incrementally.

---

### **Category C: Agent Execution, Efficiency & Context Management**

#### 1. **Second Thought: Reasoning in Parallel as LLM Agents Act** (`[2608.13667]`)
* **Core Concept**: Executes speculative next-step reasoning in parallel while asynchronous tools (shell commands, long I/O) execute, eliminating idle stalls.
* **Fit Evaluation**:
  * *Strengths*: Speeds up multi-step agent pipelines (Sisyphus, Nibbler).
  * *Risks*: Increases GPU compute overlap during tool execution; must respect our 165W power cap.

#### 2. **Context Compilers Over Bigger Context Windows** (Towards Data Science)
* **Core Concept**: Compiles raw file trees and codebases into structured AST / symbol graphs before prompt injection rather than blindly dumping thousands of raw lines.
* **Fit Evaluation**:
  * *Strengths*: **High fit for Z87.** Saves host DDR3 RAM and vLLM KV-cache memory budget.
  * *Risks*: Requires deterministic AST / ripgrep parser.

#### 3. **RLSVR: Self-Verifiable Rewards via Task Transformation** (`[2607.23802]`)
* **Core Concept**: Transforms open-ended code or analysis tasks into self-verifiable unit assertions before execution.
* **Fit Evaluation**:
  * *Strengths*: Directly aligns with our BKM-034 delegation verification mandates.

---

## 📊 Feasibility & Impact Matrix

| Candidate | Category | Feasibility on Z87 / 2080 Ti | System & Telemetry Impact | Alignment Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **Ask, Don't Judge (Binary Batteries)** | Evaluator | 🟢 **High** (Runs on 3B, zero extra VRAM) | 🟢 High (Eliminates score drift) | **Tier 1 (Immediate Fit)** |
| **Context Compiler (AST/Symbol Graphs)** | Agent Execution | 🟢 **High** (Host CPU / Rust / Ripgrep) | 🟢 High (Massive KV cache savings) | **Tier 1 (Immediate Fit)** |
| **AutoMem (Cognitive Skill Memory)** | Memory | 🟡 **Medium** (Prompt/Tool layer) | 🟡 Medium (Structured retrieval) | **Tier 2 (Strong Candidate)** |
| **Netflix Rubric Lifecycle** | Evaluator | 🟡 **Medium** (Process/Ledger schema) | 🟡 Medium (Curator stability) | **Tier 2 (Strong Candidate)** |
| **Second Thought (Parallel Reasoning)** | Agent Execution | 🟡 **Medium** (Requires async dual-stream) | 🔴 Risk (GPU power overlap) | **Tier 3 (Evaluate Carefully)** |
| **HOLA (Hippocampal Linear Attention)** | Memory | 🔴 **Low** (Requires custom model training) | 🟡 Medium (Architecture rewrite) | **Tabled / Research Only** |

---

## 📋 Outstanding Backlog Review & Integration Candidates

1. **`[LAB-108]` Multi-Remote Dual Push**: Wire Bitbucket private remotes alongside GitHub for dual redundancy once repos are initialized.
2. **`[FEAT-432]` Streaming Open HyDE Preprocessor**: Enhance Pinky's streaming preamble with zero-shot domain-specific acronym expansion.
3. **`[FEAT-353]` Automated Verifier Synthesis**: Generate automated test harnesses for nightly distilled QA evaluation.

---

## 📋 Sprint Execution Scope

### **Story 59.1: [FEAT-454] "Ask, Don't Judge" Deterministic Binary Evaluation Batteries**
* **Status**: 🔲 **TODO**
* **Objective**: Replace drifting 1–5 scalar scores in Cynical Curator (`scan_curator.py`) and Validation Ledger (`validation_ledger.jsonl`) with a deterministic battery of atomic boolean assertions (`is_tested`, `is_msr_clamped`, `has_reproduction_steps`, `is_syntactically_valid`).
* **Verification**: Unit tests proving 0% score variance across identical input evaluation runs.

### **Story 59.2: [FEAT-455] Context Compiler for Agent Context Compaction**
* **Status**: 🔲 **TODO**
* **Objective**: Implement an AST / symbol-graph context compiler using Python `ast` and `ripgrep` to compact raw multi-file codebases into high-density structural context before injecting into OpenAgent / Sisyphus prompts, reducing KV-cache bloat and token consumption by >50%.
* **Verification**: Benchmark comparing raw context token count vs. compiled AST context token count with 100% symbol recall.

---

## 🧭 Next Action

Review Tier 2 and Tier 3 candidate deep-dives below to prioritize future sprint allocation.
