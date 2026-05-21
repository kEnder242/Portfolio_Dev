# SPRINT 29: THE PERFORMANCE FRONTIER [MAY 19 12:00]
**Status:** ACTIVE | 90% COMPLETE (Pending Qwen Adapter Forge)

## 🎯 MISSION
To verify and maximize the performance of the Acme Lab's multi-LoRA routing architecture. We aim for 100% KV-cache prefix hits between Triage and Persona phases to minimize Time-to-First-Token (TTFT).

---

## 🚨 FORENSIC DISCOVERY: RAG BYPASS [HIGH SEVERITY]
- **Root Cause**: Investigation of `CognitiveHub.py` reveals that the `intent` variable was being initialized to `"STRATEGIC"` in triage exception blocks, overwriting `RECALL`.
- **Status**: [x] **FIXED**. Initialized as `None` and preserved through retry loops.

---

## 🛠️ SPRINT GOALS

### 🎯 GOAL 18: WAKE-ON-INTENT HARDENING [STABL-001]
*Objective: Eliminate the "Chaotic Wake-up" race conditions.*

- [x] **Task 20.0.1 (Wait-for-Ready Lock)**: Port-8088 ping loop moved to `_synchronize_and_probe` to prevent triage before binding.
- [x] **Task 20.0.2 (Cached Lobby Relay)**: Bypassed local boot wait if Brain is online for instant responses (0.8s TTFT).

### 🎯 GOAL 19: SHELL-SIDE RECIPE HARDENING [PERF-001]
*Objective: Stabilize vLLM flags and prevent Python GC interference.*

- [x] **Task 20.1 (Move Flags to start_vllm.sh)**: Port all vLLM optimization flags (`--enable-prefix-caching`, `--max-loras`, `--gpu-memory-utilization`) directly into the shell script to avoid Python GC deaths and flag parsing issues.
- [x] **Task 20.2 (Attendant Simplification)**: Update `lab_attendant_v4.py` to rely on the script for the "Bulletproof Recipe," passing only the `model_path` and `venv` as arguments.

### 🎯 GOAL 20: THE PHYSICAL BEDROCK (AGENTIC PREAMBLE) [FEAT-351]
*Objective: Achieve 100% stable prefix-cache hits for repeated or related queries via BKM-015.*

- [x] **Task 20.3 (Identity Bedrock Implementation - BKM-015)**: Create a shared constant string describing the Lab's 3-tier memory topography (Diamond/Archive/Raw), RAG capabilities, and resident roles (Pinky/Shadow/Brain). 
    - **Constraint**: Describe the *locations* and *capabilities* only. No hard-coded telemetry values or fuel metrics (BKM-015 compliance).
- [x] **Task 20.4 (Prompt-Engineering Routing)**: Shift triage from Python logic to "Agentic Routing" within the shared identity preamble.
- [x] **Task 20.5 (Context Displacement)**: Move all dynamic "Fuel/Route" data to the *tail* of the prompt or a trailing user message role to preserve the Bedrock prefix hash.
- [x] **Task 20.6 (Throughput Benchmarking)**: Develop `src/debug/bench_vllm_cache.py` to physically measure the latency difference between a cold prefill and a prefix-cached hit.

### 🎯 GOAL 21: THE QWEN PIVOT [FEAT-352]
*Objective: Standardize on Qwen2.5-3B for superior tool-calling and performance.*

- [x] **Task 20.7 (Qwen Transition)**: Update `infrastructure.json` to set `qwen2.5-3b-awq` as the `unified-base`.
- [x] **Task 20.8 (Adapter Legacy Preservation)**: Move existing Llama LoRAs to `/speedy/models/adapters/llama_legacy`.
- [x] **Task 20.9 (Nightly Task Adaptation)**: Update the Nightly Dream Pass and Training scripts to generate Qwen-compatible adapters.

---

## 🛠️ EXECUTION SEQUENCE (BKM-029)
1. **Priority 1**: RAG Bypass Cleanup (Stability). [COMPLETE]
2. **Priority 2**: Shell-Side Hardening (GC Shielding). [COMPLETE]
3. **Priority 3**: Physical Bedrock Implementation (Cache Optimization). [COMPLETE]
4. **Priority 4**: The Qwen Pivot (Intelligence Upgrade). [IN PROGRESS]

---

## 🧪 PROPOSED VERIFICATION TESTS

### 1. The "Throughput Ghost" Test
**Method**: Send the same 1000-token technical prompt twice.
**Assertion**: The second request must have a TTFT < 50ms (Cache Hit).
**Status**: [x] **PASSED**. 75-min gauntlet (5x5) verified **0.01s TTFT** consistently.

### 2. The "Triage-to-Persona" Handover
**Method**: Send a query that triggers Triage -> Shadow -> Brain.
**Assertion**: shadow_node must report a prefix-cache hit on the shared user input tokens.
**Status**: [x] **PASSED**. 0.01s TTFT confirmed during multi-node transitions.

### 3. RAG Sincerity Check
**Method**: Ask "What did I do with RAPL in the past?"
**Assertion**: Verify Hub logs show intent: RECALL and the archive node is physically invoked.
**Status**: [x] **PASSED**. Forensic logs confirm **RECALL** intent firing without year regex.

---


---

## 🔬 RESEARCH RECOVERY & MODERNIZATION REPORT [BKM-023]
**Date:** May 20, 2026 | **Status:** PROPOSED

### 🎯 Restoration Summary
Following a forensic audit of `research.html` and `RESEARCH_SYNTHESIS.md`, we have restored the high-fidelity ArXiv-centric architecture. Internal `FEAT` markers have been subordinated to their theoretical anchors to maintain a professional "Research Ledger" appearance.

### 🧬 ArXiv Mapping & Pedigree Correlation
| Research Anchor | ArXiv ID | Implementation Milestone | Status |
| :--- | :--- | :--- | :--- |
| **FS-Researcher** | 2602.01566 | [FEAT-095] Static Synthesis | Live |
| **Agentic-R** | 2601.11888 | [FEAT-080] Learning to Retrieve | Active |
| **TTCS / Curriculum**| 2601.22628 | [FEAT-114] Sovereign Bridge | Live |
| **Apple CLaRa** | 2511.18659 | [FEAT-073] Semantic Condenser | Live |
| **Liger Kernel** | 2410.10989 | [FEAT-137] Triton Optimization | Live |
| **Byzantine ToM** | 2603.00142 | [FEAT-071] Internal Debate | Live |
| **AT2QA** | 2603.01853 | [FEAT-173] Autonomous Pivot | Design |
| **Memex (RL)** | 2603.04257 | [FEAT-067] Diamond Dreaming | Live |
| **TTT-Discover** | 2601.16175 | N/A | Planned |
| **MAXS** | 2601.12538 | N/A | Planned |

### 🛠️ Actions Taken [BKM-023 Compliance]
1.  **Surgical Update**: `RESEARCH_SYNTHESIS.md` updated with explicit ArXiv IDs.
2.  **Noise Filtering**: Cleaned up "Tabled & Future" items in the source markdown.
3.  **Demo Creation**: `field_notes/research_demo.html` generated (not committed) for UI comparison. 
4.  **BKM-023 Adherence**: All edits performed via `replace` to preserve surrounding engineering context.

### 🔮 Next Steps
- [ ] Review `research.html`.
- [ ] Perform the Google Keep brain dump for Epoch 2 research.
- [ ] Sync the refined ledger to the public airlock (`sync_research.sh`).
