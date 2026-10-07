# 🏎️ Field Note: Speculative Triage Inference Lead Calibration (`[FEAT-586]` / `[BKM-079]`)

**Document ID:** `FN-TRIAGE-CAL-2026-10`  
**Date:** 2026-10-07  
**Status:** **ACTIVE / VERIFIED**  
**Governing Features:** `[FEAT-500]`, `[FEAT-531]`, `[FEAT-586]`, `[BKM-024]`, `[BKM-079]`  

---

## 🧭 1. Executive Summary & Architectural Shift

The Federated Lab employs a **Speculative Triage Relay** (`SpeculativeTriageRelay`) to route incoming conversational prompts into structured intent and domain vectors. Two local silicon resources race to deliver this triage JSON:
1. **Apple M5 Air (oMLX on Port 8000):** Sovereign, high-parameter ternary reasoner (`TokenAI-zer--Ternary-Bonsai-2-27B-MLX-oQ2-mtp`). Delivers nuanced intent resolution and domain classification.
2. **Linux z87 2080 Ti (vLLM on Port 8088):** High-throughput, lower-parameter multi-LoRA worker (`Llama-3.2-3B-AWQ`). Operates as a zero-cost local safety net for sluggish/cold wakes and offline failover.

### The Misunderstanding: Transport Ping vs. Inference Completion
Prior iterations conflated **transport-layer socket latency / HTTP probe TTFT** (~90ms for a lightweight `GET /v1/models` check) with **end-to-end LLM structured generation** (~850ms–1,000ms for a 25-token triage JSON). This resulted in an artificially truncated head-start window of $2 \times 90\text{ms} = 180\text{ms}$. Because M5 Air cannot complete full inference in 180ms, the Foyer prematurely dispatched vLLM on every turn, allowing vLLM to undercut the warm sovereign reasoner.

### The Parallel Speculative Race Calculus
Speculative head-start windows do **not** need to wait for M5 Air's full inference to complete. In a true parallel race, vLLM is launched after lead window $W_{\text{lead}}$, running concurrently in the background.

The condition for M5 Air to win when warm is governed by the **differential equation**:
$$t_{\text{air}} < W_{\text{lead}} + t_{\text{vllm\_exec}}$$
$$\implies \mathbf{W_{\text{lead}} > t_{\text{air}} - t_{\text{vllm\_exec}}}$$

Plugging in empirical production measurements:
* Warm M5 Air ($P_{90}$): **~980 ms**
* Local vLLM execution: **~650 ms – 680 ms**
* Differential: $980\text{ms} - 650\text{ms} = \mathbf{330\text{ms}}$

Adding a ~70ms buffer for OS scheduling and network jitter yields the optimal calibrated window:
$$\mathbf{W_{\text{lead}} = 400\text{ms} \quad (t_{\text{warmed}} = 0.20\text{s})}$$

---

## 📊 2. Physical Telemetry Characterization

Based on empirical production measurements from `Portfolio_Dev/field_notes/benchmarks_cache.json` and `Portfolio_Dev/field_notes/data/foyer_stage_ledger.jsonl`:

| Metric | Apple M5 Air (`m5_air:8000`) | Linux z87 2080 Ti (`localhost:8088`) | Notes |
| :--- | :--- | :--- | :--- |
| **Model** | Ternary-Bonsai-2-27B-MLX (mtp) | Llama-3.2-3B-AWQ (Multi-LoRA) | M5 Air is primary reasoning; vLLM is backup |
| **Warm TTFT** | ~956 ms | ~180 ms | Time to first token |
| **Generation Speed** | ~4.0 tok/s | ~42.0 tok/s | Token throughput |
| **Triage Completion (Warm)** | **850 ms – 1,100 ms (avg ~930 ms)** | **600 ms – 750 ms (avg ~680 ms)** | Full structured JSON output (~25 tokens) |
| **Cold Wake Completion** | 2,500 ms – 3,800 ms | 950 ms – 1,100 ms | First-packet wake / Metal shader setup |
| **Cost / Resource Profile** | Unified memory resident (18W) | 11GB VRAM resident (85W) | Both zero-marginal-cost local silicon |

---

## 🧮 3. Regime Comparison: Old Ping vs Sequential vs Tight Race

| Regime | $W_{\text{lead}}$ | $t_{\text{warmed}}$ ($W/2$) | Warm M5 Air Outcome (~930 ms) | Cold / Sluggish M5 Air (~3.0 s) | Parallelism |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Old Ping (Sprint 71)** | **180 ms** | 0.09 s | ❌ **vLLM wins at 830 ms** (steals turn) | ✅ vLLM wins at 830 ms | High, but undercuts warm reasoning |
| **Sequential Timeout** | **1,000 ms** | 0.50 s | ✅ **Air wins at 930 ms** (vLLM never launches) | ⚠️ vLLM wins at **1,680 ms** (waits 1.0s before launch) | Zero parallelism on warm turns |
| **Tight Speculative Race** | **400 ms** | **0.20 s** | ✅ **Air wins at 930 ms** (beats vLLM by 150 ms) | ⚡ **vLLM wins at 1,080 ms** (**600 ms faster!**) | **Optimal parallel overlap** |

### Execution Breakdown at $W_{\text{lead}} = 400\text{ms}$ ($t_{\text{warmed}} = 0.20\text{s}$)
1. **Warm Steady State (~930 ms):**
   * $t=0$: M5 Air begins inference.
   * $t=400\text{ms}$: vLLM launches in parallel.
   * $t=930\text{ms}$: M5 Air finishes. vLLM is at $530\text{ms}$ (~75% through generation).
   * **Result:** M5 Air wins cleanly! vLLM is cancelled and discarded. Sovereign reasoning is preserved for >90% of turns.
2. **Cold Wake / Hibernation / Sluggishness (~3.0 s):**
   * $t=0$: M5 Air begins (Metal shader compilation / memory paging).
   * $t=400\text{ms}$: vLLM launches.
   * $t=1,080\text{ms}$: vLLM completes and delivers structured triage ($400\text{ms} + 680\text{ms}$).
   * **Result:** vLLM wins in Phase 2 and cancels sluggish Air.
   * **User Latency:** The user receives a valid triage response at **1.08 seconds** instead of waiting 1.68s or 3.0s.
3. **Offline / Unreachable Remote Seat:**
   * Fast dual-check gate detects unavailability in <50ms and falls back to LOCAL vLLM immediately with 0 ms delay.

---

## 🧠 4. Dynamic Lead Window & Per-Engine Estimator Isolation

Under `[FEAT-586]`, the lead window dynamically adapts using an EWMA latency estimator (`_EWMALatencyEstimator`):
$$W_{\text{lead}} = \max\left(2 \times t_{\text{warmed}},\, L_t + 4 \times J_t\right)$$
where $L_t$ is the smoothed latency ($\alpha = 1/8$) and $J_t$ is the mean deviation ($\beta = 1/4$).

### Per-Engine State Isolation Fix
Crucially, each engine maintains its own independent EWMA estimator:
```python
winner = racer_name if task is racer_task else lead_name
win_estimator = self._estimators.setdefault(winner, _EWMALatencyEstimator())
elapsed = time.monotonic() - (t_racer if task is racer_task else t_lead)
win_estimator.observe(elapsed)
```
- **Elapsed Timing Isolation:** Racer completions are timed relative to $t_{\text{racer}}$, not $t_{\text{lead}}$, preserving true engine latency profiles.
- **Zero Cross-Poisoning:** When vLLM wins a cold-wake sprint, it updates `vllm`'s estimator. Deep Thought's estimator remains unpolluted, ensuring subsequent warm turns grant Deep Thought its calibrated 400ms runway.

---

## 🛠️ 5. Configuration Summary

```json
// HomeLabAI/config/infrastructure.json
"seats": [
    {
        "id": "M5_AIR",
        "name": "M5_AIR",
        "host": "192.168.1.46",
        "port": 8000,
        "protocol": "OPENAI",
        "probe_path": "/v1/models",
        "default_model": "TokenAI-zer--Ternary-Bonsai-2-27B-MLX-oQ2-mtp",
        "t_warmed": 0.20,
        "t_cold": 0.85
    },
    {
        "id": "KENDER",
        "name": "KENDER",
        "host": "192.168.1.26",
        "port": 11434,
        "protocol": "OLLAMA",
        "default_model": "hf.co/unsloth/Qwen3.8-27B-GGUF:UD-Q3_K_XL",
        "t_warmed": 0.20,
        "t_cold": 0.2
    },
    {
        "id": "LOCAL",
        "name": "LOCAL",
        "host": "127.0.0.1",
        "port": 8088,
        "protocol": "VLLM",
        "t_warmed": 0.20,
        "t_cold": 0.05
    }
]
```

---

## ✅ 6. Live Verification & Certification

- **Unit Test Suite:** All 17 tests across `test_speculative_triage_seats.py`, `test_speculative_triage.py`, `test_kender_fast_gate.py`, and `test_interest_speculative_prefetch.py` certified green (`17 passed in 5.02s`).
- **Live Readiness:** Foyer resident node reload verified; active Head matches daemon commit.
