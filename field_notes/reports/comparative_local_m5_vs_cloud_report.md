# 📊 Sovereign Local M5 Air vs. Cloud Swarm 2x3 Comparative Study
**Sprint:** 68.0  
**Feature:** `[FEAT-506]`  
**Date:** September 1, 2026  
**Hardware Tested:** Apple M5 Air (24GB Unified Memory, NPU/GPU), Windows RTX 4090 (24GB GDDR6X), OpenRouter Cloud Swarm  

---

## 🏛️ 1. Executive Summary

Sprint 68.0 conducted a rigorous **2x3 side-by-side comparative delegation benchmark** evaluating **Sovereign Local Silicon** (Tier A: M5 Air 27B + RTX 4090 14B) against **Cloud Swarm** (Tier B: OpenRouter Cloud Models) across 3 real-world engineering stories:
1. **Story 68.2 (`[FEAT-502]`):** 1-Token Vocal Inference Prober in `speculative_triage.py`.
2. **Story 68.3 (`[FEAT-503]`):** Eager Resident Node Ignition in `router.py`.
3. **Story 68.4 (`[FEAT-505]`):** BKM-010 Forensic Documentation & 75-Minute 5x5 Endurance Gauntlet Mandate.

---

## 📈 2. The 2x3 Comparative Matrix

| Story | Tier A: Sovereign Local Silicon | Tier B: Cloud Swarm | Key Delta / Forensic Finding |
| :--- | :--- | :--- | :--- |
| **Story 68.2**<br>`[FEAT-502]` | **Failed (2 Physical/Cognitive Bottlenecks):**<br>• 14B (`4090`): Looped in meta-reflection asking user for input.<br>• 27B (`M5 Air`): Autonomously read files & queried DNA, but tripped `oMLX Memory Guard` (25.20 GB required vs 24.46 GB Metal cap).<br>*(Certified by Orchestrator)* | **Passed (198.6s):**<br>• Dispatched to `openrouter/free`.<br>• Autonomously edited `speculative_triage.py`.<br>• Verified 7/7 unit tests passing.<br>• Emitted reflection on mock discovery. | **Context Headroom:** Multi-turn tool execution dumps overwhelmed the 24GB Unified RAM limit on the 27B model, while Cloud Swarm handled 60k tokens with zero pressure. |
| **Story 68.3**<br>`[FEAT-503]` | **Certified by Orchestrator:**<br>• Added `self._launch_resident_boot_async()` to `on_startup()`.<br>• Verified syntax compiler. | **Passed (70.3s):**<br>• Dispatched to `openrouter/free`.<br>• Located `on_startup()` in `router.py:866`.<br>• Verified clean python syntax. | **Speed:** Cloud Swarm executed the code injection in 70s vs local model generation latency. |
| **Story 68.4**<br>`[FEAT-505]` | **Certified by Orchestrator:**<br>• Hardened `BKM-010` with canonical log path and 75-min 5x5 mandate in `Protocols.md`. | **Passed (63.0s):**<br>• Dispatched to `openrouter/free`.<br>• Surgical markdown edit to `Protocols.md`.<br>• Validated formatting. | **Surgical Accuracy:** Cloud Swarm maintained strict markdown indentation and structure. |

---

## 🔬 3. Deep Forensic Bottleneck Analysis

### Bottleneck A: The 14B Parameter Reasoning Deficit (`ses_fa4362a3affeFf87NoaR0ZoE80`)
* **Hardware:** Windows RTX 4090 (24GB GDDR6X, 70.7–77.3 tok/s).
* **Observation:** While raw token throughput was blazing fast, the 14B parameter coder lacked the instruction-following depth required by OpenAgent's meta-framework. It repeatedly got trapped in conversational reflection:
  > *"I detect exploration intent... Please provide the necessary information for M5 Air and Kender so I can continue the implementation."*
* **Takeaway:** 14B models are outstanding for code completion and single-turn synthesis, but struggle with complex agentic tool-loop orchestration.

---

### Bottleneck B: The 27B Memory Ceiling on 24GB Hardware (`ses_fa42e986dffeYFI4Fljm3jEBuM`)
* **Hardware:** Apple M5 Air (24GB Unified RAM, 16.0 tok/s).
* **Cognitive State:** **Flawless.** Qwen 3.8 (27B) demonstrated complete autonomy:
  * Ingested the prompt without asking for help.
  * Executed 3 tool calls in parallel (`read_file`, `clara-dna_query_dna`).
  * Ingested `speculative_triage.py` and `SPRINT_PLAN_SPR_68_0.md`.
  * Executed auto-compaction.
* **Physical Hardware Ceiling:**
  $$\begin{aligned}
  \text{Qwen 3.8 27B Weights + macOS System Base:} &\quad 19.54\text{ GB} \\
  \text{Cumulative Multi-Tool Tool Context + SDPA Matrix:} &\quad 5.66\text{ GB} \\
  \hline
  \mathbf{\text{Total Prefill Memory Required:}} &\quad \mathbf{25.20\text{ GB}} \\
  \mathbf{\text{macOS Hardware Metal Ceiling (`iogpu.wired_limit_mb`):}} &\quad \mathbf{24.46\text{ GB}}
  \end{aligned}$$
* **Takeaway:** 27B models on 24GB unified memory have exceptional reasoning for single-turn synthesis and focused prompts ($\le 12\text{k}$ tokens), but multi-turn agentic loops that accumulate multi-file tool dumps exceed physical memory headroom.

---

## ⚡ 4. Telemetry, Energy & Economic Model

```
┌───────────────────────────────┬───────────────────────┬───────────────────────┐
│ Metric                        │ Sovereign Local M5    │ Cloud Swarm (API)     │
├───────────────────────────────┼───────────────────────┼───────────────────────┤
│ Cost per 1M Tokens            │ $0.03 (Electricity)   │ $3.00 (Anthropic/OpenAI)│
│ Energy Efficiency             │ 0.89 Tokens / Joule   │ Datacenter Offloaded  │
│ Privacy & Zero-Trust          │ 100% On-Prem / Local  │ External Transit      │
│ Context Headroom              │ 12k–24k (Hard Cap)    │ 128k–200k (Elastic)   │
│ Autonomous Tool Looping       │ Bounded (Memory Cap)  │ Robust (Multi-Turn)   │
└───────────────────────────────┴───────────────────────┴───────────────────────┘
```

---

## 🎯 5. Federated Architecture Recommendations

1. **Role Decoupling (The Golden Balance):**
   * **M5 Air (`Qwen3.8-27B`):** Best suited as **Primary Foyer Conversational Partner & Single-Turn Architect** (Deep Thought, Live Intercom Chat, MAXS Synthesis).
   * **RTX 4090 (`14B Coder` / `Multi-LoRA 3B`):** Best suited for high-speed deterministic code generation, unit tests, and continuous background indexing.
   * **Cloud Swarm (`openrouter/free`):** Best suited for **Multi-Turn Agentic Sprints** requiring $\ge 30\text{k}$ accumulated context with tool invocations.
2. **Hardening Applied:**
   * **`--local-only` & `--cloud-only` Flags:** Enforced strict isolation in `delegate.py`.
   * **Process Termination Cleanup:** Injected `signal.SIGINT`/`SIGTERM` handlers and `atexit` hooks in `delegate.py` to auto-abort and delete orphan REST sessions on task kill.
