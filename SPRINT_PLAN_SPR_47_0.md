# 📋 SPRINT PLAN: Sprint 47.0 — Unified Pre-Reflection Triage & Evergreen Career Compass

> **Status:** APPROVED / READY FOR EXECUTION  
> **Target Workspace:** `/home/jallred/Dev_Lab/Portfolio_Dev` & `/home/jallred/Dev_Lab/HomeLabAI`  
> **BKM Compliance:** High-Density BKM Standard (1-liner setup, core logic, explicit trigger points, scars retrospective)

---

## 🏛️ Executive Summary & Design Pedigree

This sprint implements the **Unified Pre-Reflection Triage Engine** and the **Evergreen Career Compass Memory Ledger**. It eliminates hardcoded pre-triage rules (e.g. year regexes) in favor of native LLM intent translation (*"I think the user is trying to say..."*) while establishing an authoritative 6-era ground truth map compiled from your actual resume ([`resume.txt`](file:///home/jallred/study/references/resume.txt)).

---

## 1. Architectural Design & Memory Hierarchy

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

## 3. Sprint Stories & Implementation Tasks

### 🔹 Story 1: High-Fidelity Career Compass Bedrock & Memory Ledger
- **Task 1.1**: Create `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/data/career_compass.json` containing Tier 1 Anchor Map (<300 tokens) and Tier 2 Keyword Mesh.
- **Task 1.2**: Update `/home/jallred/Dev_Lab/HomeLabAI/src/nodes/loader.py` to inject Tier 1 Anchor Map into `BicameralNode` `IDENTITY_BEDROCK`.
- **Task 1.3**: Create and run `/home/jallred/Dev_Lab/HomeLabAI/src/tests/test_career_compass_bedrock.py`.

### 🔹 Story 2: Unified Intent-HyDE Pre-Reflection Pipeline
- **Task 2.1**: Refactor `/home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py` triage loop to execute single 150-token Pre-Reflection ("I think the user is trying to say...").
- **Task 2.2**: Format output to extract Inferred Intent, Triage Routing (`addressed_to`, `vibe`, `importance`), and HyDE Synthesis vector in a single pass.
- **Task 2.3**: Create and run `/home/jallred/Dev_Lab/HomeLabAI/src/tests/test_unified_prereflection.py`.

### 🔹 Story 3: Deep Thought HyDE Generator & Pinky Failover Plumbing
- **Task 3.1**: Wire Deep Thought streaming output in `cognitive_hub.py` directly into `archive_node.py` ChromaDB vector ingest.
- **Task 3.2**: Implement local backup HyDE failover via Pinky (Llama 3.2 3B on port 8088) when Deep Thought is offline (`OLLAMA: None`).
- **Task 3.3**: Create and run `/home/jallred/Dev_Lab/HomeLabAI/src/tests/test_hyde_plumbing.py`.

### 🔹 Story 4: Nightly Continuous Burn Map Synthesizer Integration
- **Task 4.1**: Update `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/mass_scan.py` to index new raw notes against `resume.txt` and append micro-details to `career_compass.json` Tier 2 Mesh.
- **Task 4.2**: Verify zero prompt context bloat (<300 token Tier 1 preservation).

---

## 4. Verification & Validation Commands

```bash
# 1-liner test execution suite
PYTHONPATH=.:src /home/jallred/Dev_Lab/HomeLabAI/.venv/bin/python3 src/tests/test_career_compass_bedrock.py && \
PYTHONPATH=.:src /home/jallred/Dev_Lab/HomeLabAI/.venv/bin/python3 src/tests/test_unified_prereflection.py && \
PYTHONPATH=.:src /home/jallred/Dev_Lab/HomeLabAI/.venv/bin/python3 src/tests/test_hyde_plumbing.py && \
PYTHONPATH=.:src /home/jallred/Dev_Lab/HomeLabAI/.venv/bin/python3 src/tests/test_feature_assertions.py
```
