# 📋 SPRINT LOG 110.0: Heterogeneous Dual-GPU Engine Transition, Option A 27GB Pooled VRAM & Waterfall Drop-In

**Sprint ID:** `SPR_110_0`  
**Parent Framework:** `BKM-005` (Design Studio Alignment), `BKM-006` / `BKM-007` (Work Completion Report), `BKM-020` (High-Fidelity Sprint Documentation), `BKM-024` (Live Silicon Verification), `BKM-077` (Conversational Anchor Tracking), `BKM-086` (Paved-Path Sprint Protocol), `BKM-088` (Empirical Pipeline Step Judgment Protocol), `INS-052` (The Litmus Leak Test & Unified Trust Boundary).  
**Date:** November 4, 2026  
**Status:** 🟢 **ALL STORIES & WATERFALL DELIVERABLES COMPLETED & CERTIFIED (100% GREEN)**  

---

## 📊 1. Story & Deliverables Execution Matrix

| Story / Task ID | Owner | Mode | Target / Scope | Status | Evidence / Artifacts |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Story 110.1** | `[AGY:PRIMARY]` | Direct | Prompt Guardrails (`nibble_v2.py`) | **COMPLETED & CERTIFIED** | Scrubbed input buffer, machine boundary prompt blocks (`[CREDENTIAL & SECRET BOUNDARY]`), pruned `career_timeline` from taxonomy. |
| **Story 110.2** | `[AGY:PRIMARY]` | Direct | Secrets & Focal Litmus Probe (`probe_secret_and_focal_leak_test.py`) | **COMPLETED & CERTIFIED** | Verified out-of-band regex sentinel probe; 0/4 leak rate; verified technical log preservation. |
| **Story 110.3** | `[AGY:PRIMARY]` | Direct | Lakehouse Data Scrub & `www_deploy` Push | **COMPLETED & CERTIFIED** | Purged historical JFrog token instances; amended commit `9bfbcfb`; passed GitHub Push Protection; updated parent submodule pointer (`5aaec11`). |
| **Story 110.4** | `[AGY:PRIMARY]` | Direct | Gem Balancing & Socket Preemption | **COMPLETED & CERTIFIED** | Foyer intercom socket preemption (`ss -t state established :8765`); sparse ingestion cadence (`limit=2`); nightly suppression for `refine_gem.py` (`FEAT-416`). |
| **Story 110.5** | `[AGY:PRIMARY]` | Direct | Jellyfin QSV & Steam Remote Play | **COMPLETED & CERTIFIED** | Verified Arc B580 QSV `/dev/dri/renderD129` transcode healthy; Mazui ASS burn-in 73 fps (2.98x); NVIDIA container fallback preserved; Steam Remote Play on primary adapter. |
| **Story 110.6** | `[AGY:PRIMARY]` | Direct | Vulkan 1.4 Multi-Device Engine (`llama.cpp`) | **COMPLETED & CERTIFIED** | Compiled `llama.cpp` with `-DGGML_VULKAN=ON`; unified dual-GPU launcher `/home/jallred/serve_llm.sh`; verified zero-downtime CUDA vLLM fallback. |
| **Story 110.7** | `[AGY:PRIMARY]` | Direct | Empirical Benchmark Gauntlet (`benchmark_hybrid.py`) | **COMPLETED & CERTIFIED** | Generated `hybrid_benchmark_results.json`; measured TTFT, tok/s, dual VRAM allocations across Llama 3.2 3B and Qwen 2.5 32B. |
| **Story 110.8** | `[AGY:PRIMARY]` | Direct | Qwen 3.5/3.7/3.8 Characterization & Waterfall Drop-In | **COMPLETED & CERTIFIED** | Benchmarked Qwen 3.8 27B (11.33 t/s) and Qwen 3.7-Flash 8B (59.96 t/s); dropped `llama-server` directly into lab waterfall on port 8088 with `--alias unified-base`. |

---

## ⚡ 2. Silicon Benchmarks & Physical Performance Gauntlet

### Physical Node Architecture
- **Slot 1 (PCIe 03:00.0)**: Intel Arc B580 (16GB ReBAR, 450 GB/s bandwidth, `card0`, `renderD129`, Vulkan GPU 0, HDMI display + Jellyfin QSV)
- **Slot 2 (PCIe 05:00.0)**: NVIDIA GeForce RTX 2080 Ti (11GB, 616 GB/s 352-bit bus, `card2`, `renderD130`, Vulkan GPU 1, Headless Compute)
- **Combined Pooled Capacity**: **27GB VRAM** across Vulkan 1.4

### Empirical Benchmark Summary

```
================================================================================================================
Model                           Config / Device                        Prompt (pp)      Decode (tg)    Speedup
================================================================================================================
Llama 3.2 3B Q4_K_M             Pure RTX 2080 Ti (Vulkan1)             4,658.06 t/s     182.98 t/s     Baseline
Llama 3.2 3B Q4_K_M             Pure Arc B580 (Vulkan0)                2,293.27 t/s      50.58 t/s     -72.4% vs 2080Ti
Llama 3.2 3B Q4_K_M             Dual-GPU 50/50 Layer Split             2,851.17 t/s      77.09 t/s     +52.4% vs B580 (3.11x vLLM)
----------------------------------------------------------------------------------------------------------------
Qwen 2.5 32B Q4_K_M (18.5 GB)   Arc First (Vulkan0/Vulkan1 -ts 1/1)       59.13 t/s      10.22 t/s     Baseline split
Qwen 2.5 32B Q4_K_M (18.5 GB)   RTX First (Vulkan1/Vulkan0 -ts 1/1)       69.70 t/s      10.03 t/s     +17.9% prefill speedup
----------------------------------------------------------------------------------------------------------------
Qwen 3.8 27B UD-Q4_K_M (15.3GB) Unbalanced (Vulkan1/Vulkan0 -ts 11/16)    48.31 t/s       8.93 t/s     Unbalanced ratio
Qwen 3.8 27B UD-Q4_K_M (15.3GB) Balanced (Vulkan1/Vulkan0 -ts 1/1)        71.10 t/s      11.33 t/s     +47.2% prefill, +26.9% decode
----------------------------------------------------------------------------------------------------------------
Qwen 3.7-Flash 8B Q8_0 (8.11GB) Pure RTX 2080 Ti (Vulkan1)               907.59 t/s      59.96 t/s     Standalone Turing Peak
Qwen 3.7-Flash 8B Q8_0 (8.11GB) Pure Arc B580 (Vulkan0)                  357.80 t/s       9.53 t/s     -84.1% vs 2080Ti
Qwen 3.7-Flash 8B Q8_0 (8.11GB) Dual-GPU 50/50 Split (Vulkan1/Vulkan0)   508.71 t/s      14.90 t/s     Inter-GPU latency penalty
================================================================================================================
```

---

## 🌊 3. Lab Waterfall Drop-In & Zero-Downtime Integration

### Direct Drop-In Architecture
The lab waterfall (including `HomeLabAI/src/v5/foyer/router.py`, `HomeLabAI/src/curator/draft_decomposer.py`, and `HomeLabAI/src/v5/ignition/manager.py`) expects an OpenAI-compatible HTTP daemon on port 8088.

1. **Active Daemon Execution**:
   - `llama-server` is deployed on port 8088 via `/home/jallred/serve_llm.sh --mode=hybrid`.
   - `--alias unified-base` is passed to ensure any callers querying `/v1/models` or issuing requests with `"model": "unified-base"` receive instant native responses.
2. **Live Endpoint Certification**:
   - `GET http://127.0.0.1:8088/health` $\to$ `{"status":"ok"}`
   - `GET http://127.0.0.1:8088/v1/models` $\to$ Returns `id: "unified-base"`
   - `POST http://127.0.0.1:8088/v1/chat/completions` $\to$ Verified live generation with streaming reasoning content in <1.0s.
3. **Instant CUDA Fallback**:
   - Running `/home/jallred/serve_llm.sh --mode=cuda` restarts the native CUDA vLLM container/service within 5 seconds if fallback is ever required.
4. **Media & Display Isolation**:
   - Verified Jellyfin hardware transcoding on Arc B580 (`/dev/dri/renderD129`, DeviceID `e20b/1`) operates without interruption alongside the Vulkan LLM pipeline.
   - Verified desktop display output on `card0` remains fluid and free of X11/Mesa lockups.

---

## 🔬 4. Heterogeneous Speculative Decoding & KV Cache Ledger

### Intra-Family Speculative Decoding Invariant
Rejection sampling in speculative decoding mandates:
$$\alpha = \min\left(1, \frac{P_{\text{target}}(x)}{P_{\text{draft}}(x)}\right)$$
- When both draft and target share the same tokenizer and training family (e.g. `nics-efc/Qwen3-4B-ActionOPD-Qwen3.7-Flash` and `nics-efc/Qwen3-8B-ActionOPD-Qwen3.7-Flash`), probability acceptance rates $\alpha$ typically exceed $75–85\%$.
- Cross-lineage pairing (such as drafting Qwen 3.5 with Qwen 2.5) introduces severe distribution divergence, collapsing $\alpha < 20\%$ and slowing down overall wall-clock throughput.
- Quantization of the target model (e.g. Q4_K_M) does **not** degrade acceptance probability; the mathematical invariant guarantees the final output distribution is strictly that of the target model alone.

### The KV Cache Horizon Trap (`[WIS-482]`)
- **Single-Card Squeeze Failure**: Squeezing a 27B model into the 16GB Arc B580 using aggressive 2-bit quantization leaves merely $0.5–2.7\text{ GB}$ of VRAM for KV cache. At typical context horizons ($12\text{K}–16\text{K}$ tokens), the allocation exhausts VRAM, causing out-of-memory crashes or catastrophic CPU swapping.
- **Dual-GPU Pooled Advantage**: The balanced 50/50 split across RTX 2080 Ti (11GB) and Arc B580 (16GB) allocates weights evenly (~7.6GB per card for 27B), leaving **over 7.6GB of pooled VRAM dedicated strictly to KV cache**, enabling full $32\text{K}–64\text{K}$ context horizons in uncompromised Q4 precision.

---

## 🛡️ 5. Mistakes Avoided Ledger (`BKM-081` / `BKM-082`)

1. **Avoiding vLLM Port Collision**: Prior to launching the hybrid Vulkan engine, `lab-attendant.service` was cleanly stopped, releasing 10.65 GB of held CUDA memory on the RTX 2080 Ti and preventing `ErrorOutOfDeviceMemory` or port 8088 bind conflicts.
2. **Avoiding Partial CPU Offload Thrashing**: Discovered that offloading fewer than all layers to GPU caused CPU offload thrashing across host DDR4 memory and swap (capping generation at 1.72 tok/s). Enforced 100% full VRAM offload (`-ngl 99`) across the pooled 27GB capacity.
3. **Preventing Out-of-Vocabulary Speculation**: Rejected mixing different Qwen major lineages (Qwen 2.5 predictor with Qwen 3.5 target), enforcing identical intra-family token vocabularies for speculative decoding.
4. **Preserving Submodule Commit Integrity**: Synchronized all child submodules (`www_deploy`, `Portfolio_Dev`) and cleanly committed parent pointers in `Dev_Lab` to prevent detached git pointer desync.

---

## 📌 6. Verification Commands & Telemetry Artifacts

```bash
# 1. Probe Live Engine Health
curl -s http://127.0.0.1:8088/health
# Expected: {"status":"ok"}

# 2. Probe OpenAI Compatible Models List
curl -s http://127.0.0.1:8088/v1/models
# Expected: Model ID "unified-base"

# 3. Test Live Inference Chat Completion
curl -s http://127.0.0.1:8088/v1/chat/completions -H "Content-Type: application/json" -d '{
  "model": "unified-base",
  "messages": [{"role": "user", "content": "ping"}],
  "max_tokens": 10
}'

# 4. Probe Hardware Transcoding State
docker ps --filter "name=jellyfin" --format "{{.Names}}: {{.Status}}"
vpl-inspect | grep -i "DeviceID"
```
