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

---

## 5. Sprint 47.1 — Integration Test Stories (Retrospective-Driven)

> **Motivation**: Sprint 47.0 unit tests passed with `OFFLINE_STUB` fallbacks, producing false green signals without exercising the real Foyer state machine or remote node communication. These stories validate that the production `acme_lab.py` / `FoyerRouter` (port `8765`) orchestrates real multi-node Round Table turns end-to-end.
>
> **Preconditions**: The Lab Attendant (`acme_lab.py`) must be running on `localhost:8765`. Tests use `pytest.mark.skipif` when remote nodes (KENDER, M5 Air) are unreachable.
>
> **KENDER Timeout**: Use `qwen2.5-coder:14b` with a 120s timeout for all KENDER integration calls.

---

### Story 6: Foyer Liveness & Health Integration Test

- **Core Objective**: Verify the running Lab Attendant responds to REST health and status probes, confirming the Foyer is alive and reporting correct engine state before any Round Table turns are attempted.
- **Architectural Context**:
  - The Foyer (`FoyerRouter`) runs on `localhost:8765` with `GET /health` and `GET /status` endpoints.
  - This test is the **gate check** — all subsequent integration tests depend on it passing.
- **Implementation Tasks**:
  - **Task 6.1**: Create `/home/jallred/Dev_Lab/HomeLabAI/src/tests/test_integration_foyer.py`.
  - **Task 6.2**: `test_foyer_health()` — `GET http://localhost:8765/health` returns HTTP 200 with valid JSON containing engine state.
  - **Task 6.3**: `test_foyer_status()` — `GET http://localhost:8765/status` returns HTTP 200 with valid JSON containing `version`, `mode`, and node list.
  - **Task 6.4**: Both tests use `pytest.mark.skipif` with a 3s TCP probe to `localhost:8765`; skip with message `"Lab Attendant not running on port 8765"` if unreachable.
- **Acceptance Criteria**:
  - Health endpoint returns 200 with parseable JSON.
  - Status endpoint returns 200 and includes `LAB_VERSION` string.

---

### Story 7: WebSocket Round Table Inject & Transcript Capture

- **Core Objective**: Send a real user query through the Foyer WebSocket (`ws://localhost:8765/hub`) and verify that a multi-turn Round Table response is received, logged, and contains Pinky's preamble and Brain's reasoning.
- **Architectural Context**:
  - The Foyer accepts WebSocket connections at `ws://localhost:8765/hub`.
  - Messages are JSON with `{"text": "..."}` format via the `POST /inject` REST endpoint.
  - Real Round Table turns produce `CHAT` role messages from `Pinky`, `Brain`, and evaluation entries in `.round_table_evals.json`.
- **Implementation Tasks**:
  - **Task 7.1**: Create `/home/jallred/Dev_Lab/HomeLabAI/src/tests/test_integration_roundtable.py`.
  - **Task 7.2**: `test_rest_inject_produces_response()` — `POST http://localhost:8765/inject` with `{"text": "What did I work on in 2018?"}`. Assert HTTP 200 response. Assert response JSON contains a non-empty `content` or `data` field.
  - **Task 7.3**: `test_roundtable_transcript_logged()` — After the inject, verify that `HomeLabAI/logs/` contains a new evaluation batch log file with a timestamp within the last 120 seconds. The log must contain at least one `"role": "CHAT"` entry from a node other than `System`.
  - **Task 7.4**: Gate on Story 6 (`test_foyer_health`) — skip entire module if Foyer is unreachable.
- **Acceptance Criteria**:
  - A real query injected via REST produces a non-stub response from the Round Table.
  - The full dialogue transcript is logged to disk (not just evaluation metadata).

---

### Story 8: KENDER Deep Thought Remote Reasoning Integration

- **Core Objective**: Verify that the Foyer's CognitiveHub successfully dispatches a query to KENDER (`192.168.1.26:11434`) for Deep Thought reasoning and receives a real LLM-generated response (not an `OFFLINE_STUB`).
- **Architectural Context**:
  - KENDER runs Ollama with `qwen2.5-coder:14b` on `192.168.1.26:11434`.
  - The CognitiveHub routes `addressed_to: BRAIN` queries to KENDER via `POST /api/chat`.
  - A 120s timeout is used to accommodate cold-start model loading on the 4090.
- **Implementation Tasks**:
  - **Task 8.1**: Create `/home/jallred/Dev_Lab/HomeLabAI/src/tests/test_integration_kender.py`.
  - **Task 8.2**: `test_kender_ollama_reachable()` — `GET http://192.168.1.26:11434/api/tags` returns HTTP 200 with a JSON `models` list containing at least one entry. Skip if unreachable.
  - **Task 8.3**: `test_kender_chat_completion()` — `POST http://192.168.1.26:11434/api/chat` with `model: qwen2.5-coder:14b`, a system prompt identifying KENDER as Deep Thought, and a user query `"Summarize the 2018 Intel Optane AEP validation campaign in 2 sentences."`. Assert response contains `message.content` with length > 20 characters. Timeout: 120s.
  - **Task 8.4**: `test_kender_response_not_stub()` — Assert that the response content does NOT contain the strings `OFFLINE_STUB`, `VERIFIED_PASS`, or `Coherent technical alignment` (known stub phrases).
- **Acceptance Criteria**:
  - KENDER returns a real LLM-generated response (not a hardcoded fallback).
  - Response is contextually relevant to the Optane/AEP query.

---

### Story 9: M5 Air MLX Judge Live Evaluation Integration

- **Core Objective**: Verify that the M5 Air Node 3 (`192.168.1.46:8000`) receives a real turn trace via its OpenAI-compatible REST API and returns a live LLM-generated evaluation critique (not the `OFFLINE_STUB` fallback).
- **Architectural Context**:
  - M5 Air runs `mlx_lm.server` serving `mlx-community/Qwen2.5-Coder-14B-Instruct-4bit` on port `8000`.
  - The `MLXAsyncJudge` driver (`mlx_judge_node.py`) sends `POST /v1/chat/completions` payloads.
  - The key defect from Sprint 47.0: the driver's `except` block silently returned a stub with `score: 0.99` when the node was offline, causing false-green tests.
- **Implementation Tasks**:
  - **Task 9.1**: Create `/home/jallred/Dev_Lab/HomeLabAI/src/tests/test_integration_m5_air.py`.
  - **Task 9.2**: `test_m5_air_model_available()` — `GET http://192.168.1.46:8000/v1/models` returns HTTP 200 with a JSON object containing `data[0].id` matching `mlx-community/Qwen2.5-Coder-14B-Instruct-4bit`. Skip if unreachable.
  - **Task 9.3**: `test_m5_air_live_evaluation()` — Use `MLXAsyncJudge.evaluate_256k_context()` with a real turn trace. Assert that the returned `status` is `ONLINE_EVALUATED` (NOT `VERIFIED_PASS`, which is the stub status).
  - **Task 9.4**: `test_m5_air_critique_has_content()` — Assert that the evaluation result contains a `critique` key with length > 10 characters (the stub returns `style_critique`, not `critique`; the live path returns `critique`).
- **Acceptance Criteria**:
  - M5 Air returns `ONLINE_EVALUATED` status with a real `critique` string.
  - Test FAILS if the stub path is hit (distinguishes live vs. fallback).

---

### Story 10: Full Tri-Node Round Table End-to-End Integration

- **Core Objective**: Execute a complete Round Table turn that exercises all three remote nodes (Pinky on z87-Linux, KENDER Deep Thought, M5 Air Judge) through the production Foyer, and verify the full transcript is captured with contributions from each seat.
- **Architectural Context**:
  - This is the capstone integration test. It requires all nodes online and the Foyer running.
  - A query is injected via `POST /inject`. The Foyer orchestrates: Pinky preamble -> KENDER reasoning -> M5 Air async evaluation.
  - The full transcript must be captured in `HomeLabAI/logs/evaluation_batch_*.log` with entries from multiple nodes.
- **Implementation Tasks**:
  - **Task 10.1**: Create `/home/jallred/Dev_Lab/HomeLabAI/src/tests/test_integration_tri_node.py`.
  - **Task 10.2**: `test_tri_node_preconditions()` — Verify all three endpoints respond: `localhost:8765/health`, `192.168.1.26:11434/api/tags`, `192.168.1.46:8000/v1/models`. Skip entire module if any is unreachable.
  - **Task 10.3**: `test_tri_node_inject_and_capture()` — `POST http://localhost:8765/inject` with `{"text": "Tell me about my 2018 datacenter work with Intel Optane persistent memory"}`. Wait up to 120s for response. Assert response is non-empty.
  - **Task 10.4**: `test_tri_node_transcript_multi_seat()` — After injection, scan the newest `evaluation_batch_*.log` file in `HomeLabAI/logs/`. Assert it contains `CHAT` entries from at least 2 distinct `node` sources (e.g., `Pinky` and `Brain`/`Shadow`).
  - **Task 10.5**: `test_tri_node_eval_ledger_updated()` — Verify `.round_table_evals.json` has a new entry with a timestamp within the last 180 seconds.
- **Acceptance Criteria**:
  - Full end-to-end query produces transcript entries from multiple Round Table seats.
  - The evaluation ledger is updated with a fresh entry.
  - No `OFFLINE_STUB` or hardcoded fallback appears in the transcript.

---

## 6. Integration Test Verification & Validation Commands

```bash
# Integration test suite (requires Lab Attendant running on port 8765)
PYTHONPATH=.:src /home/jallred/Dev_Lab/HomeLabAI/.venv/bin/pytest \
  src/tests/test_integration_foyer.py \
  src/tests/test_integration_kender.py \
  src/tests/test_integration_m5_air.py \
  src/tests/test_integration_roundtable.py \
  src/tests/test_integration_tri_node.py \
  -v --timeout=180
```

---

## 7. Sprint 47.1 Retrospective Mandate

> All integration tests MUST distinguish between **live node responses** and **offline stub fallbacks**. A test that passes because a stub returned `VERIFIED_PASS` is a **false green** and must be treated as a test infrastructure defect. The `OFFLINE_STUB` path is for graceful production degradation, never for test validation.
