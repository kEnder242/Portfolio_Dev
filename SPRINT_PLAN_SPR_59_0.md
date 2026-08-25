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

## 📋 Detailed Feedback & Architectural Consensus Ledger

This section records the exact user insights, engineering rationales, and design boundaries established during Sprint 59 planning to preserve complete pedigree:

1. **Silicon Hard Freeze & Linux Dirty Page Cache Phenomenon**:
   * *User Forensic Truth*: Host never lost power; it entered an unrecoverable kernel hard freeze (NumLock dead, interrupts frozen).
   * *Forensic Reality*: In Linux, userspace logs are buffered in RAM page cache (`dirty_writeback_centisecs`). When the kernel enters unevictable D-state deadlock (DDR3 bus lockup during unquantized tensor deserialization), unflushed step logs in RAM evaporate before hitting the SSD journal.
   * *Settling Pacing*: A 5.0-second inter-step delay (`HardwarePacingCallback`) allows switching VRM inductors to discharge and heatsink thermal mass to return to idle baseline (~30°C/15W), eliminating compounding junction heat.
2. **Local Training Law (Zero Remote Offload)**:
   * *Mandate*: Unsloth LoRA fine-tuning MUST remain 100% local on Pinky / Z87 (Turing RTX 2080 Ti). Remote offload to Kender (4090) or M5 Air for forge is strictly forbidden.
3. **Anti-Embellishment Corollary (Conversational WYWO)**:
   * *Principle*: Avoid hardcoded `vibe=casual` triggers (BKM-015 compliance). Instead, when prompt information density is shallow ("hi", "what's up"), Pinky dynamically floats genuine unresolved validation scars (`validation_ledger.jsonl`) or Diamond Gems rather than inventing assistant filler. User feedback to floated topics is treated as original ground-truth.
4. **Tools-Over-UI / The Fourth Wall Feedback Loop (BKM-035)**:
   * *Principle*: Deprecate cluttered UI vote buttons. When the user speaks to the "fourth wall" or expresses disagreement ("Wait, that's wrong...", "Pinky, note that..."), the Hub semantically classifies the critique and auto-populates `validation_ledger.jsonl` failure tests and Cynical Curator rubric constraints.
5. **Single-Layer Cascade Preemption**:
   * *Rule*: Speculative context pre-fetching runs strictly Turn 1 $\rightarrow$ Turn 2 (Pinky $\rightarrow$ Brain only). Deep Thought is never speculatively pre-fetched ahead of Brain, eliminating double-preemption thrashing and remote network storms.
6. **Daytime Residency vs. 2:00 AM Nightly Offline Quiesce**:
   * *Daytime Nominal (`FAST_WAKE`)*: All resident nodes (`pinky`, `brain`, `archive`, `lab`) and `Llama-3.2-3B-AWQ` remain permanently resident in System RAM and GPU VRAM with zero daytime idle timeout eviction.
   * *Nightly Maintenance (`02:00 AM`)*: The physical `POST /release_nodes` endpoint remains active exclusively for `nightly_forge.py` to flush VRAM during the scheduled 2:00 AM window before auto-reigniting via `re_ignite_vllm()`.

---

## 📋 Sprint Execution Scope & Granular Task Specifications

### **Story 59.1: [FEAT-454] "Ask, Don't Judge" Deterministic Binary Evaluation Batteries**
* **Status**: 🔲 **TODO**
* **Target Files**:
  * [`HomeLabAI/src/curator/scan_curator.py`](file:///home/jallred/Dev_Lab/HomeLabAI) (Lines ~120–180: `evaluate_gem_quality()`)
  * [`Portfolio_Dev/field_notes/data/validation_ledger.jsonl`](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/data/validation_ledger.jsonl)
* **Finalized Design**:
  * **Universal Epistemic 5-Question Battery**: Avoids brittle domain-classification drift by evaluating the core epistemic rigor of any engineering artifact:
    1. `has_exact_identifiers`: Cites specific physical registers, ports, IPs, or error codes (e.g. MSR 0x610, port 8088, PCIe AER 0x10) rather than vague prose.
    2. `has_reproduction_recipe`: Contains copy-pasteable CLI commands or script reproduction steps.
    3. `isolates_cause_and_effect`: Clearly explains the physical failure mechanism and how the fix operates.
    4. `is_actionable_bkm`: Provides immediately executable SRE / validation procedures.
    5. `has_zero_conversational_fluff`: Contains pure, high-density technical truth without filler.
  * **Deterministic Scoring**: $\text{Rank} = 1 + \sum(\text{True assertions}) \quad (1 \text{ to } 5)$.
* **Verification**: `test_binary_evaluator_unit.py` proving 0% score variance across 20 repeated runs on identical synthetic gems.

### **Story 59.2: [FEAT-455] Context Compiler for Agent Context Compaction**
* **Status**: 🔲 **TODO**
* **Target Files**:
  * [`HomeLabAI/src/compiler/context_compiler.py`](file:///home/jallred/Dev_Lab/HomeLabAI) (New Module)
  * [`HomeLabAI/src/tests/delegate.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/tests/delegate.py#L250)
* **Finalized Design**:
  * **Call-Graph & Cross-Module Hierarchy**: AST extracts symbol signatures, argument types, and docstrings, combined with ripgrep-extracted caller/dependency graphs across files, stripping internal function bodies to achieve $>60\%$ token compaction with 100% symbol interface fidelity.
* **Verification**: Benchmark comparing raw context tokens vs. compiled AST context tokens demonstrating $>50\%$ token savings with 100% symbol recall.

### **Story 59.3: [FEAT-456] Language-First Co-Pilot Feedback Loop (The Fourth Wall / BKM-035)**
* **Status**: 🔲 **TODO (Delegation Ready)**
* **Target Files**:
  * [`HomeLabAI/src/logic/feedback_interceptor.py`](file:///home/jallred/Dev_Lab/HomeLabAI) (New Modular Satellite Service)
  * [`HomeLabAI/src/tests/test_feedback_interceptor.py`](file:///home/jallred/Dev_Lab/HomeLabAI) (New Test Suite)
  * [`HomeLabAI/docs/Protocols.md`](file:///home/jallred/Dev_Lab/HomeLabAI/docs/Protocols.md) (`BKM-035` Registered)
* **Finalized Design**:
  * **Modular Satellite Service**: Extract critique parsing and failure ledger logging into `feedback_interceptor.py` to allow isolated OpenAgent delegation.
  * **Semantic Intent Interception**: Classifies `GROUNDING_CORRECTION` intent without hardcoded regex (BKM-015 compliant).
  * **Interactive Refinement Prompt**: Pinky acknowledges the correction in-character, appends a `FAIL` record to `validation_ledger.jsonl`, and immediately asks one targeted follow-up question to clarify boundary conditions or register masks.
* **Verification**: `test_feedback_interceptor.py` verifying conversational corrections auto-populate `validation_ledger.jsonl` and return structured refinement prompts.

### **Story 59.4: [FEAT-457] Single-Layer Speculative Context Pre-fetching & Interest Preemption**
* **Status**: ✅ **COMPLETED & CERTIFIED**
* **Target Files**:
  * [`HomeLabAI/src/logic/cognitive_hub.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py#L1081) (Lines 1081–1107, 1515–1555)
  * [`HomeLabAI/src/tests/test_interest_speculative_prefetch.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/tests/test_interest_speculative_prefetch.py)
* **Finalized Design**:
  * Turn 1 (Pinky) immediately sparks asynchronous background `_fetch_rag_context()`.
  * If interest $>0.5$, Turn 2 (Brain) starts instantly with pre-fetched context in memory.
  * If interest $\le 0.5$, prefetch task is cleanly cancelled/preempted. Enforced single-layer cascade (Brain does not prefetch Deep Thought).
* **Verification**: `test_interest_speculative_prefetch.py` passed 2/2 unit tests (0.31s).

### **Story 59.5: [FEAT-458] Conversational WYWO & Floating Validation Oracle (Anti-Embellishment Corollary)**
* **Status**: 🔲 **TODO (Delegation Ready)**
* **Target Files**:
  * [`HomeLabAI/src/logic/floating_oracle.py`](file:///home/jallred/Dev_Lab/HomeLabAI) (New Modular Satellite Service)
  * [`HomeLabAI/src/tests/test_floating_oracle.py`](file:///home/jallred/Dev_Lab/HomeLabAI) (New Test Suite)
* **Finalized Design**:
  * **Modular Satellite Service**: Extract candidate harvesting into `floating_oracle.py` returning `[FLOATING_CANDIDATE_POOL]` from `validation_ledger.jsonl`, `scan_state.json`, and `nightly_dialogue.json`.
  * **Zero Hardcoding**: Evaluates semantic `GREETING` or `SHALLOW_INQUIRY` intent (no hardcoded string matches, BKM-015 compliant). Pinky's natural temperature ($T=0.7$) and prompt context steer topic selection organically.
* **Verification**: `test_floating_oracle.py` asserting accurate candidate harvesting and prompt formatting.

### **Story 59.6: [LAB-110] Permanent Daytime Node Residency & Hibernation Plumbing Preservation**
* **Status**: 🔲 **TODO**
* **Target Files**:
  * [`HomeLabAI/config/infrastructure.json`](file:///home/jallred/Dev_Lab/HomeLabAI/config/infrastructure.json#L2)
  * [`HomeLabAI/src/v5/foyer/router.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/v5/foyer/router.py#L675)
* **Exact Mechanism**:
  1. Configure `"idle_eviction_enabled": false` and `"daytime_node_residency": "PERMANENT_RESIDENT"` in `infrastructure.json`.
  2. Foyer maintains all nodes warm in host system RAM permanently during daytime, while keeping `POST /release_nodes` active strictly for the 2:00 AM Nightly Forge window.
* **Verification**: Integration test verifying all resident nodes remain `READY` across extended idle intervals.

---

## 💾 Memory Management & Idle Flow Policy (Sprint 59.0 Revision)

1. **VRAM Residency (FAST_WAKE Nominal State)**: `Llama-3.2-3B-AWQ` remains permanently pinned in GPU VRAM (2.5GB) during all standard operations, enabling sub-100ms conversational turn response times. VRAM is flushed exclusively during the 2:00 AM Nightly Forge window (`quiesce_vllm()`).
2. **Host System RAM Residency**: With `low_cpu_mem_usage=True` preventing PyTorch DDR3 memory staging leaks, the Z87 host maintains >4.5 GiB of available RAM. All resident nodes (`archive_node.py`, `pinky_node.py`, `brain_node.py`, and ChromaDB) remain resident in system memory without aggressive swap or eviction.

---

## 🧭 Next Action

Execute Stories 59.1, 59.2, 59.3, 59.5, and 59.6 per Sprint 59 roadmap.
