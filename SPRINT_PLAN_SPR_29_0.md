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

### 📍 STREAMING & ASYNC BOTTLENECKS
1. **[SERIALIZED_TRIAGE]**: We currently wait for the *complete* Triage JSON block before sparking the next Waterfall leg.
2. **[FAST_TRACK_WIN]**: The `Cached Lobby Relay` is our most performant path (0.8s TTFT), but it only fires if the Brain is warm.

---

## 🛠️ SPRINT GOALS

### 🎯 GOAL 19: KV-CACHE SINCERITY [PERF-001]
*Objective: Achieve 100% stable prefix-cache hits for repeated or related queries.*

- [ ] **Task 20.1 (Unified System Anchor)**: Implement a shared "Physical Bedrock" string (64+ tokens) that prepends all system prompts across all nodes.
- [ ] **Task 20.2 (Context Displacement)**: Move dynamic metadata (Fuel, Route, Triage Hints) to the *tail* of the prompt or a trailing user message to prevent prefix invalidation.
- [ ] **Task 20.3 (Recipe Hardening)**: Add `--enable-prefix-caching=True` and tune `--max-loras=7` in `lab_attendant_v4.py`.

### 🎯 GOAL 20: ASYNC WATERFALL OPTIMIZATION [PERF-002]
*Objective: Fast-track the Persona leg as soon as intent is identified.*

- [ ] **Task 20.4 (Speculative Spark)**: If Triage tokens contain "STRATEGIC" or "TECHNICAL", spark the next leg in the Waterfall *before* the JSON block finishes.
- [ ] **Task 20.5 (Throughput Benchmarking)**: Develop `src/debug/bench_vllm_cache.py` to physically measure the latency difference between a cold prefill and a prefix-cached hit.

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
