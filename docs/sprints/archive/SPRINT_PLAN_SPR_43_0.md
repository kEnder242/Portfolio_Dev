# 📋 Sprint Plan `SPR_43_0`: High-Fidelity Energy Telemetry & Single-Pass Cold/Warm Benchmarking

> **Goal:** Implement real-time GPU power telemetry (via DCGM port 9400), marginal energy cost metrics (`$/1M Tokens`), effective vs. raw throughput accounting, and single-pass dual Cold/Warm start metric extraction into the Acme Lab benchmarking pipeline.

---

## 📐 Key Design Principles & Insights

1. **Single-Pass Dual Extraction (Cold vs. Warm):**
   - We do **NOT** need to run separate cold and warm benchmark loops.
   - In a single sequence pass, **Request #1's TTFT** captures the true **Cold-Start Latency** (including model VRAM allocation and CUDA kernel loading).
   - **Requests #2..N** capture the **Warm-Start Latency**, **Inter-Token Latency (ITL)**, and **Sustained Generation Speed**.

2. **Effective Speed vs. Raw Speed (Reasoning/Deliberation Accounting):**
   - Token cost is set by **Effective Delivery Speed (output tokens ÷ total wall-clock time)**, not raw generation speed.
   - Reasoning models (e.g. DeepSeek-R1) spend wall-clock time deliberating between tokens, holding the GPU longer and increasing energy cost per delivered token.

3. **DCGM Hardware Power Telemetry:**
   - Query `DCGM_FI_DEV_POWER_USAGE` from local DCGM Exporter on port 9400 / NVML during inference to measure average Watt draw and total Joules burned.

4. **Marginal Energy Cost per 1M Tokens (`$/1M Tokens`):**
   $$\text{Cost per 1M Output Tokens} = \frac{\text{Average Power (Watts)} \times \text{Tariff Rate } (\$/\text{kWh})}{\text{Effective Throughput (tokens/sec)} \times 3600} \times 1,000,000$$

5. **Cloud API Cost Savings Floor:**
   - Benchmark local hardware costs (~$0.04–$0.12 / 1M tokens) against cloud APIs (Gemini 2.5 Flash / GPT-4o-mini at ~$0.60 / 1M tokens), proving an 80–90% cost savings floor.

---

## 🛠️ Sprint Stories & Actionable Tasks

### Story 1: Single-Pass Dual Cold/Warm Telemetry Engine
- [ ] **Task 1.1:** Refactor `bench_models.py` to run a 2-stage request pass without discarding the first request:
  - **Request #1 (Cold Start):** Record `cold_ttft_ms` (time to first token on un-warmed model).
  - **Request #2 (Warm Start):** Record `warm_ttft_ms`, `itl_ms`, `raw_throughput` (eval tok/s), and `effective_throughput` (total output tokens ÷ total elapsed seconds).
- [ ] **Task 1.2:** Update `benchmarks_cache.json` schema to include:
  ```json
  {
    "model": "gemma4:e2b",
    "engine": "Ollama",
    "cold_ttft_ms": 1250.0,
    "warm_ttft_ms": 280.0,
    "raw_throughput": 38.5,
    "effective_throughput": 32.1,
    "avg_power_watts": 185.0,
    "cost_per_1m_tokens": 0.052
  }
  ```

### Story 2: DCGM Power Telemetry & Energy Cost Calculator
- [ ] **Task 2.1:** Add background GPU power sampler to `bench_models.py` querying `http://localhost:9400/metrics` (`DCGM_FI_DEV_POWER_USAGE`) or NVML.
- [ ] **Task 2.2:** Compute average Watts drawn and calculate **Marginal Energy Cost per 1M Tokens** based on configurable electricity rate (default: `$0.12 / kWh`).
- [ ] **Task 2.3:** Expose Prometheus gauges on port 8011:
  - `moe_model_power_watts`
  - `moe_model_cost_dollars_per_1m_tokens`
  - `moe_model_cold_ttft_seconds`
  - `moe_model_warm_ttft_seconds`

### Story 3: Cloud API Parity & Savings Floor
- [ ] **Task 3.1:** Define cloud price baseline constants in `bench_models.py` (Gemini 2.5 Flash: `$0.60`, GPT-4o-mini: `$0.60`, Gemini 3.1 Flash-Lite: `$0.40`).
- [ ] **Task 3.2:** Compute percentage savings floor for each local model vs. cloud API reference.

### Story 4: High-Density UI Redesign (`benchmarks.html`)
- [ ] **Task 4.1:** Update model cards on `benchmarks.html` to feature:
  - **Dual TTFT Badge:** `COLD: 1,250 ms` vs `WARM: 280 ms`.
  - **Dual Speed Badge:** `RAW: 38.5 tok/s` vs `EFFECTIVE: 32.1 tok/s`.
  - **Power & Cost Badges:** `POWER: 185 W` | `COST: $0.052 / 1M Tokens` (`91% vs Cloud`).
- [ ] **Task 4.2:** Add a toggle button on comparison bar charts to switch between **Cold-Start TTFT** and **Warm-Start TTFT**.
- [ ] **Task 4.3:** Re-compile site via `build_site.py` and verify rendering across local and public airlock.

### Story 5: Vector Index Domain Tagging & ChromaDB Re-Indexing
- [ ] **Task 5.1:** Update `HomeLabAI/src/bridge_burn_to_rag.py` to derive domain tags (`exp_tlm`, `exp_bkm`, `exp_for`, `sys_arch`) and append `domain` metadata to document payloads in ChromaDB `long_term_wisdom`.
- [ ] **Task 5.2:** Re-run `python3 HomeLabAI/src/bridge_burn_to_rag.py` to perform a clean re-indexing pass of ChromaDB at `~/AcmeLab/chroma_db`.

### Story 6: Validation Anchors Keyword Realignment & 100% Pass Audit
- [ ] **Task 6.1:** Update `validation_anchors.json` expected keyword sets to align with refined 18-year `YYYY.json` archive entries.
- [ ] **Task 6.2:** Execute `python3 Portfolio_Dev/field_notes/evaluate_rag.py` and verify all 5 validation anchors achieve 100% `PASS` verdicts from KENDER with keyword recall > 70%.

---

## 🧪 Acceptance Criteria
1. `bench_models.py` extracts both Cold-Start and Warm-Start metrics in a **single execution pass**.
2. GPU power draw is sampled during inference via DCGM / NVML and converted to `$/1M Tokens`.
3. `benchmarks.html` displays dual Cold/Warm TTFT, dual Raw/Effective throughput, and `$ / 1M Tokens` cost badges.
4. `bridge_burn_to_rag.py` populates `domain` metadata in ChromaDB `long_term_wisdom`.
5. `evaluate_rag.py` achieves 100% `PASS` across all 5 RAG validation anchors.
6. All changes are committed and synchronized cleanly across `Portfolio_Dev`, `www_deploy`, and `Dev_Lab`.
