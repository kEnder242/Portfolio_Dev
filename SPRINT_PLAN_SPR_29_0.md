# SPRINT 29: THE PERFORMANCE FRONTIER [MAY 19 12:00]
**Status:** DRAFT | Systems Engineering Audit & vLLM Optimization

## 🎯 MISSION
To verify and maximize the performance of the Acme Lab's multi-LoRA routing architecture. We aim for 100% KV-cache prefix hits between Triage and Persona phases to minimize Time-to-First-Token (TTFT).

---

## 🚨 PRELIMINARY FORENSIC AUDIT (Pre-Heads Down)

### 📍 CACHE INVALIDATORS FOUND (TTFT Killers)
1. **[SYSTEM_PROMPT_DRIFT]**: Triage (`lab_node.py`) and Personas (`pinky_node.py`) use entirely different system prompts. Since the system message is the hash-root, vLLM treats them as 100% distinct prefixes.
2. **[CONTEXT_MUTATION]**: `loader.py` prepends dynamic metrics (`[SYSTEM_DESIGN_STANCE]`) to the user prompt. Because these metrics (Fuel, Route) are updated *after* triage, the hash for the user prompt always misses.
3. **[RECIPE_GAP]**: The vLLM launch command in `lab_attendant_v4.py` is missing the `--enable-prefix-caching` flag.

### 📍 FORENSIC DISCOVERY: RAG BYPASS [HIGH SEVERITY]
- **Root Cause**: Investigation of `CognitiveHub.py` reveals that the `intent` variable is being initialized to `"STRATEGIC"` in the `except` blocks of the Triage loop. If a triage model fails even a single attempt, the `RECALL` intent is lost. Furthermore, the `archive` resident is not being reliably re-initialized after an H2 wake.

---

## 🛠️ SPRINT GOALS

### 🎯 GOAL 19: SHELL-SIDE RECIPE HARDENING [PERF-001]
*Objective: Stabilize vLLM flags and prevent Python GC interference.*

- [ ] **Task 20.1 (Move Flags to start_vllm.sh)**: Port all vLLM optimization flags (`--enable-prefix-caching`, `--max-loras`, `--gpu-memory-utilization`) directly into the shell script to avoid Python GC deaths and flag parsing issues.
- [ ] **Task 20.2 (Attendant Simplification)**: Update `lab_attendant_v4.py` to rely on the script for the "Bulletproof Recipe," passing only the `model_path` and `venv` as arguments.

### 🎯 GOAL 20: THE PHYSICAL BEDROCK (AGENTIC PREAMBLE) [FEAT-351]
*Objective: Achieve 100% stable prefix-cache hits for repeated or related queries via BKM-015.*

- [ ] **Task 20.3 (Identity Bedrock Implementation - BKM-015)**: Create a shared constant string describing the Lab's 3-tier memory topography (Diamond/Archive/Raw), RAG capabilities, and resident roles (Pinky/Shadow/Brain). 
    - **Constraint**: Describe the *locations* and *capabilities* only. No hard-coded telemetry values or fuel metrics (BKM-015 compliance).
- [ ] **Task 20.4 (Prompt-Engineering Routing)**: Shift triage from Python logic to "Agentic Routing" within the shared identity preamble.
- [ ] **Task 20.5 (Context Displacement)**: Move all dynamic "Fuel/Route" data to the *tail* of the prompt or a trailing user message role to preserve the Bedrock prefix hash.
- [ ] **Task 20.6 (Throughput Benchmarking)**: Develop `src/debug/bench_vllm_cache.py` to physically measure the latency difference between a cold prefill and a prefix-cached hit.

### 🎯 GOAL 21: THE QWEN PIVOT [FEAT-352]
*Objective: Standardize on Qwen2.5-3B for superior tool-calling and performance.*

- [ ] **Task 20.7 (Qwen Transition)**: Update `infrastructure.json` to set `qwen2.5-3b-awq` as the `unified-base`.
- [ ] **Task 20.8 (Adapter Legacy Preservation)**: Move existing Llama LoRAs to `/speedy/models/adapters/llama_legacy`.
- [ ] **Task 20.9 (Nightly Task Adaptation)**: Update the Nightly Dream Pass and Training scripts to generate Qwen-compatible adapters.

---

## 🛠️ EXECUTION SEQUENCE (BKM-029)
1. **Priority 1**: RAG Bypass Cleanup (Stability).
2. **Priority 2**: Shell-Side Hardening (GC Shielding).
3. **Priority 3**: Physical Bedrock Implementation (Cache Optimization).
4. **Priority 4**: The Qwen Pivot (Intelligence Upgrade).

---

## 🧪 PROPOSED VERIFICATION TESTS

### 1. The "Throughput Ghost" Test
**Method**: Send the same 1000-token technical prompt twice.
**Assertion**: The second request must have a TTFT < 50ms (Cache Hit).

### 2. The "Triage-to-Persona" Handover
**Method**: Send a query that triggers Triage -> Shadow -> Brain.
**Assertion**: shadow_node must report a prefix-cache hit on the shared user input tokens.

---

## ⚖️ DISCUSSION POINTS FOR LEAD ENGINEER
1. **Universal System Prompt**: Should we force all nodes to share the first 2-3 blocks of identity to enable cross-node caching?
2. **Qwen vs Llama (VRAM vs Perf)**: Confirming buy-in for Qwen2.5-3B (Superior tool-calling + native performance) or sticking with Llama-3.2-3B for VRAM budget?
