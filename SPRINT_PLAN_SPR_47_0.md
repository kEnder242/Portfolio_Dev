# 📋 SPRINT PLAN: Sprint 47.0 — Unified Pre-Reflection Triage & Evergreen Career Compass

> **Status:** APPROVED / READY FOR OPENAGENT EXECUTION  
> **Target Workspace:** `/home/jallred/Dev_Lab/Portfolio_Dev` & `/home/jallred/Dev_Lab/HomeLabAI`  
> **Guiding Star:** High-Density BKM Standard & Federated Round Table Architecture

---

## 🏛️ Executive Summary & Architectural Guiding Star

This sprint implements the **Unified Pre-Reflection Triage Engine**, the **Evergreen Career Compass Memory Ledger**, and the **Deep Thought HyDE Vector Pipeline**. It eliminates hardcoded pre-triage rules (e.g. year regexes) in favor of native LLM intent translation (*"I think the user is trying to say..."*) while establishing an authoritative 6-era ground truth map compiled from your actual resume ([`resume.txt`](file:///home/jallred/study/references/resume.txt)).

> **Infrastructure Note**: [`HomeLabAI/docs/LAB_INFRASTRUCTURE.md`](file:///home/jallred/Dev_Lab/HomeLabAI/docs/LAB_INFRASTRUCTURE.md) is established as the sole authoritative infrastructure manual (with entry `[LAB-010]` registered). Duplicate copies in `Portfolio_Dev` have been removed to preserve a single source of truth.

---

## 1. Architectural Guiding Star & Memory Hierarchy

### 💡 The Evergreen Career Ledger Pattern (Tiered Memory)

To keep system prompt context crisp (<300 tokens) while preserving 18 years of technical insights as new notes are discovered during nightly Continuous Burn:

```
                            ┌────────────────────────────────┐
                            │  Nightly Continuous Burn Scan  │
                            └───────────────┬────────────────┘
                                            │
                             ┌──────────────▼────────────────┐
                             │     Gem / Note Classifier      │
                             └───────┬────────────────┬───────┘
                                     │                │
                      Core Era Facts │                │ Micro-Details &
                                     ▼                │ Technical Gems
                 ┌──────────────────────┐             │
                 │ TIER 1: ANCHOR MAP   │             ▼
                 │ (Prompt Bedrock)     │   ┌─────────────────────────┐
                 │ • Fixed 3 bullets/era│   │ TIER 2: KEYWORD MESH    │
                 │ • Max 300 Tokens     │   │ • Extended JSON Index   │
                 │ • Fast & Concise     │   │ • Unlimited Scaling     │
                 └──────────────────────┘   │ • Queried via RAG Vector│
                                            └─────────────────────────┘
```

- **Tier 1 (Anchor Map Bedrock)**: Fixed 3-bullet summary per era. Token budget capped at <300 tokens in `IDENTITY_BEDROCK`.
- **Tier 2 (Dynamic Keyword Mesh - `career_compass.json`)**: Micro-details and technical gems scale infinitely on disk and ChromaDB RAG.

---

### 🚀 The Unified Pre-Reflection Pipeline

Combines Intent Translation, Triage Routing, and HyDE Vector Generation into a **single 150-token LLM pass**:

```
[USER QUERY]: "hey pinky, what did I do in 2018?"
                             │
                             ▼
              ┌──────────────────────────────┐
              │ UNIFIED PRE-REFLECTION PASS  │
              │  (Deep Thought / Larynx)     │
              └──────────────┬───────────────┘
                             │
       ┌─────────────────────┼─────────────────────┐
       ▼                     ▼                     ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
│ 1. INFERRED   │     │ 2. TRIAGE    │     │ 3. HyDE SYNTHESIS│
│    INTENT    │     │    DECISION  │     │    VECTOR        │
│ "User wants a│     │ addressed_to:│     │ "Intel Datacenter│
│ historical   │     │ BRAIN        │     │  PAE 2018, AEP   │
│ summary of   │     │ vibe:        │     │  Optane memory,  │
│ 2018 work"   │     │ DEEP_RESEARCH│     │  mailbox tools.."│
└──────────────┘     └──────────────┘     └──────────────────┘
```

---

## 2. Authoritative 6-Era Career Map

Ground truth compiled directly from [`/home/jallred/study/references/resume.txt`](file:///home/jallred/study/references/resume.txt):

| Era | Position / Focus | Key Hardware & Domain Keywords |
| :--- | :--- | :--- |
| **2005 – 2008** | Firmware Validation Engineer | Perl/TCL automation, EFI, Windows, Linux, NIC testing, IPMI recovery |
| **2008 – 2010** | BMC Firmware Engineer | IPMI, DCMI, Serial Over LAN (SOL), C socket libraries, early HECI |
| **2011 – 2015** | Post-Silicon Debug Software Developer | Intel VISA signal-trace, SoC debug, C++, TeamCity CI automation |
| **2016 (Jan–Jul)** | Pre-Silicon Graphics Modeling Engineer | GPU/SoC pre-silicon simulation, Linux modeling, log parsing |
| **2016 – 2019** | Datacenter PAE (Intel Federal) | 100-node cluster debug, BIOS/microcode, Intel Optane Persistent Memory (AEP) |
| **2019 – 2024** | Manageability Test Content Lead | IPMI, Redfish, PECI, MCTP, SIMICS (S3E/SSM), PCIe/RAS bring-up, power telemetry |
| **2024 – 2026** | Federated AI Architecture & Telemetry | Acme Lab, HomeLabAI, Portfolio Dev, vLLM, DCGM GPU telemetry, NVIDIA prep |

---

## 3. Sprint Stories & OpenAgent Implementation Context

### 🔹 Story 1: High-Fidelity Career Compass Bedrock & Memory Ledger
- **Core Objective**: Establish an authoritative, zero-hardcoding career memory ledger that grounds Pinky and Brain in your 18-year engineering history.
- **Architectural Context & Q&A Details**:
  - **Resume Ground Truth**: Incorporates verified resume facts (including PCIe validation bring-up, Redfish, PECI, MCTP, and Intel VISA signal-trace debug).
  - **Evergreen Ledger Pattern**: Tier 1 Anchor Map stays strictly under 300 tokens in `BicameralNode` `IDENTITY_BEDROCK`. Micro-details scale in Tier 2 Keyword Mesh on disk (`career_compass.json`).
  - **Token Ceiling Guardrail**: `test_career_compass_bedrock.py` enforces a hard assertion failing if Tier 1 exceeds 350 tokens.
- **Implementation Tasks**:
  - **Task 1.1**: Create `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/data/career_compass.json` containing Tier 1 Anchor Map (<300 tokens) and Tier 2 Keyword Mesh.
  - **Task 1.2**: Update `/home/jallred/Dev_Lab/HomeLabAI/src/nodes/loader.py` to inject Tier 1 Anchor Map into `BicameralNode` `IDENTITY_BEDROCK`.
  - **Task 1.3**: Create and run `/home/jallred/Dev_Lab/HomeLabAI/src/tests/test_career_compass_bedrock.py`.

### 🔹 Story 2: Unified Intent-HyDE Pre-Reflection Pipeline
- **Core Objective**: Elevate Triage from a cold, rigid JSON classifier into a single 150-token Pre-Reflection pass that translates user intent (*"I think the user is trying to say..."*).
- **Architectural Context & Q&A Details**:
  - **Tone & Nuance Resolution**: Recognizes that queries like *"hey pinky, remember 2018?"* are *both* friendly AND deep historical research lookups (`addressed_to: BRAIN, vibe: DEEP_RESEARCH`).
  - **Greeting Short-Circuit**: Implements an early-exit rule for simple 1-word greetings (`"hi"`, `"hey"`) to short-circuit in <15 tokens (~50ms) as `PINKY CASUAL 0.1`.
  - **Scalar Fuel Preservation**: Pinky continues computing scalar fuel (`casual`, `intrigue`, `importance`) to adjust persona stance and vocal energy, guided by the explicit `DEEP_RESEARCH` intent flag.
- **Implementation Tasks**:
  - **Task 2.1**: Refactor `/home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py` triage loop to execute single 150-token Pre-Reflection ("I think the user is trying to say...").
  - **Task 2.2**: Format output to extract Inferred Intent, Triage Routing (`addressed_to`, `vibe`, `importance`), and HyDE Synthesis vector in a single pass.
  - **Task 2.3**: Create and run `/home/jallred/Dev_Lab/HomeLabAI/src/tests/test_unified_prereflection.py`.

### 🔹 Story 3: Deep Thought HyDE Generator & Pinky Failover Plumbing
- **Core Objective**: Parallelize HyDE vector synthesis and local response preamble streaming while establishing a rock-solid 3-tier failover cascade.
- **Architectural Context & Q&A Details**:
  - **Parallel Warm Execution**: Deep Thought generates the HyDE vector on KENDER 4090 while Pinky simultaneously streams her opening preamble (*"Narf! Let me check your notes..."*). ChromaDB candidates are melded into context for sentence 2.
  - **3-Tier Failover Cascade**: `1. Deep Thought (Remote Fast)` -> `2. Pinky (Local 2080 Ti vLLM)` -> `3. Direct Raw Query Vector`.
  - **Vector Space Alignment**: Passes `query_texts=[hyde_document]` directly to `chroma-server.service` on port 8001 (`LAB-007`) to ensure 100% embedding space alignment with stored note chunks.
  - **Pinky's Primary Focus**: Pinky is relieved of heavy vector generation, returning 100% to sub-second streaming latency, user conversation, and multi-LoRA persona delivery (`cli_voice_v1`, `shadow_brain_v2`).
- **Implementation Tasks**:
  - **Task 3.1**: Wire Deep Thought streaming output in `cognitive_hub.py` directly into `archive_node.py` ChromaDB vector ingest.
  - **Task 3.2**: Implement local backup HyDE failover via Pinky (Llama 3.2 3B on port 8088) when Deep Thought is offline (`OLLAMA: None`).
  - **Task 3.3**: Create and run `/home/jallred/Dev_Lab/HomeLabAI/src/tests/test_hyde_plumbing.py`.

### 🔹 Story 4: Nightly Continuous Burn Map Synthesizer Integration
- **Core Objective**: Integrate the Career Compass into the background scanner pipeline so new technical gems continuously enrich Tier 2 without inflating prompt context.
- **Architectural Context & Q&A Details**:
  - **Zero Prompt Bloat**: `mass_scan.py` cross-references `raw_notes` against `resume.txt` to update the Tier 2 Keyword Mesh on disk.
  - **Preservation of Core Insights**: Tier 1 Anchor Map remains untouched (<300 tokens), preserving crisp system prompt performance.
- **Implementation Tasks**:
  - **Task 4.1**: Update `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/mass_scan.py` to index new raw notes against `resume.txt` and append micro-details to `career_compass.json` Tier 2 Mesh.
  - **Task 4.2**: Verify zero prompt context bloat (<300 token Tier 1 preservation).

### 🔹 Story 5: M5 Air MLX Offloading & Async Sanity Judge Readiness
- **Core Objective**: Integrate Node 3 (M5 MacBook Air 32GB Unified Memory / Apple MLX Framework) into the Round Table topology as an Asynchronous Sanity Judge & GigaToken Node.
- **Architectural Context & Q&A Details**:
  - **Un-truncated 256K Evaluation**: Evaluates full 256K turn traces (Jamba 1.5 Mini Mamba-SSM / Qwen 32B MLX on port 8090) asynchronously in the background without delaying initial UI response streaming on z87-Linux / KENDER 4090.
  - **Two-Lane Feedback Loop**: Factual/Archive errors route to ChromaDB vector store (`:8001`) and `refine_gem.py`; Style/Persona retorts route to offline LoRA dataset (`cli_voice_v1`).
  - **Local Tool Execution Moat**: Tool definitions and executions remain 100% local on `z87-Linux` via FastMCP/attendant. Remote nodes emit tool call JSON strings which `z87-Linux` executes locally.
  - **Infrastructure Ledger Entry**: Formally registered as **`[LAB-010] M5 Air MLX Unified Memory Node & Async Judge Protocol`**.
- **Implementation Tasks**:
  - **Task 5.1**: Define REST/WebSocket interface for Node 3 (M5 MacBook Air 32GB Unified Memory / Apple MLX framework on port 8090).
  - **Task 5.2**: Create `src/nodes/mlx_judge_node.py` stub in `HomeLabAI` capable of offloading non-blocking 256K context evaluation to Apple MLX.
  - **Task 5.3**: Register `[LAB-010] M5 Air MLX Unified Memory Node & Async Judge Protocol` entry in `Portfolio_Dev/LAB_INFRASTRUCTURE.md` (Git committed).

---

## 4. Verification & Validation Commands

```bash
# 1-liner test execution suite for OpenAgent verification
PYTHONPATH=.:src /home/jallred/Dev_Lab/HomeLabAI/.venv/bin/python3 src/tests/test_career_compass_bedrock.py && \
PYTHONPATH=.:src /home/jallred/Dev_Lab/HomeLabAI/.venv/bin/python3 src/tests/test_unified_prereflection.py && \
PYTHONPATH=.:src /home/jallred/Dev_Lab/HomeLabAI/.venv/bin/python3 src/tests/test_hyde_plumbing.py && \
PYTHONPATH=.:src /home/jallred/Dev_Lab/HomeLabAI/.venv/bin/python3 src/tests/test_feature_assertions.py
```
