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

## ⚖️ DISCUSSION POINTS FOR LEAD ENGINEER
1. **Universal System Prompt**: [x] **RESOLVED**. Shared `IDENTITY_BEDROCK` is active and forcing cache hits.
2. **Qwen vs Llama (VRAM vs Perf)**: [x] **RESOLVED**. Moving to Qwen2.5-3B as the standard.
