# 📋 SPRINT PLAN 114.0: Disjoint Heterogeneous MoE Sharding, Strata Exploration, & Public Telemetry

**Parent Frameworks:** `BKM-015` (Prompt Engineering & Formatting), `BKM-018` (Orchestrator-First Mandate), `BKM-024` (Live Silicon Verification), `BKM-062` (Ground Truth Verification), `BKM-079` (Hybrid Silicon Topology), `BKM-081` (In-Tree Append Ledger), `BKM-082` (Historical Grounding & 5-Sprint Lookback), `BKM-086` (Paved-Path Sprint Protocol / AFK), `BKM-088` (Sparse MoE Dual-GPU Optimization), `[FEAT-525]` (Hardware Telemetry Workbench), `[FEAT-687]` (Sparse MoE Silicon Sharding), `[FEAT-689]` (Heterogeneous Dual-GPU Engine Integration), `[REF-SPEC-DYNAMIC-01]` (Heterogeneous Speculative Decision Matrix).  
**Sprint Horizon:** November 21, 2026 – November 25, 2026  
**Status:** 🏗️ PROPOSED / READY FOR REVIEW  
**Sprint Lead:** `[AGY:PRIMARY]` (Antigravity Autonomous Pair)  
**Tracking Mode:** In-Tree Append-Only Ledger (`BKM-081`)

---

## 🛑 Pre-Flight Checklist Gate (`BKM-082 §GATE` / `BKM-086 §1.1`)
- [x] **1. 5-Sprint Lookback**: Reviewed SPR-109 through SPR-113.0 for traps, sentinels, and regression vectors (`BKM-082 §2.1`).
  - *SPR-110 (Story 110.18 & 110.19)*: Proved that 100% VRAM sharding across the 23GB pool yields 25.8–29.8 tok/s under Dual-Vulkan and 35.87 tok/s under CUDA+RPC.
  - *SPR-110 (Story 110.13 Oracle Audit)*: Audited `FlashML-org/FreeToken`. Proved falling back to host RAM on DDR3-1600 (~8-10 GB/s) incurs an 8.3x performance cliff. Reaffirmed: **Zero DDR3 model caching / light host RAM touch is mandatory.**
  - *SPR-111 (Story 111.10)*: Consolidated engine control into `HomeLabAI/src/engine_ctl.sh` across all 5 operational modes.
  - *SPR-112.1 (Story 112.190)*: Certified waterfall pre-streaming daemon via `probe_round_table_accountability.py`. Local `Qwen3.6-35B-A3B` acts as the verified sovereign bedrock engine.
  - *SPR-113.0 (Streaming & Benchmarks)*: Certified canvas/grafana dual-view telemetry workbench and live workload stream pipelines.
- [x] **2. Mistakes-Avoided Ledger (`BKM-082 §2.4`)**:
  - *Mistake 1 (The DDR3 Host Cache Cliff)*: Avoid letting MoE runtimes default to "system RAM caching." With DDR3-1600, cold expert paging causes severe stalls. Guardrail: Enforce strict VRAM budget limits (`--resident-budget-gib` / `--expert-cache vram` / `system_ram_cache_gib: 0.0`) so 100% of weights remain inside the 23GB physical GPU pool.
  - *Mistake 2 (The Multi-Driver Compiler Collision)*: Attempting to build mixed CUDA + Intel oneAPI/SYCL runtimes on host Ubuntu results in GCC/NVCC/ICPX symbol collisions. Guardrail: **Prioritize Vulkan 1.4 (`STRATA_ENGINE_BACKEND=vulkan`) in Phase 1**, which natively enumerates both NVIDIA and Intel GPUs cleanly.
  - *Mistake 3 (The Premature RPC Pivot)*: Jumping to RPC before proving the basic Vulkan multi-device baseline. Guardrail: Prove the Vulkan disjoint sharding baseline first (Phase 1); once certified, move to the CUDA+RPC method (Phase 2).
  - *Mistake 4 (The Lab Port Contention / Dirty State Trap)*: Running experimental inference engines while `lab-attendant.service` or `llama-server` is bound to ports 8088/8000 causes OOM crashes and port collision. Guardrail: Plan full lab quiescence (`engine_ctl.sh stop`, `systemctl stop lab-attendant.service`) prior to any experiment.
  - *Mistake 5 (The Telemetry Amnesia Trap)*: Running benchmarks in scratch logs without flowing receipts into `benchmarks_cache.json` and `benchmarks.html`. Guardrail: Enforce Phase 3 public benchmark synchronization as a core sprint story.
  - *Mistake 6 (The Re-Quantization Tax)*: Re-downloading or re-quantizing models when proven GGUFs already exist on local high-speed NVMe. Guardrail: Ingest `/speedy/models/gguf/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` (20.61 GB) directly into Strata.
- [x] **3. Oracle / Architectural Audit**: Pre-flight review completed via `delegate.py --mode oracle` (`ses_e00696892ffePX7bJWeOnC5wpJ`). Verdict: Plan coherent and guarded. Verified disjoint attention/expert layout, zero DDR3 host cache enforcement (`system_ram_cache_gib: 0.0`), Vulkan-first progression, and isolated `strata_exp/` blast radius.
- [x] **4. Delegation Gate (`BKM-049` / `BKM-086 §Pillar 3`)**: Per human operator directive, leaf and plumbing stories formerly targeted to `[SWARM:LOCAL]` are promoted directly to `[SWARM:CLOUD]` (Stories 114.2, 114.3, 114.5, 114.7, 114.8). `[AGY:PRIMARY]` is strictly reserved for physical silicon lifecycle (Story 114.1 quiescence, Story 114.4 config authoring, Story 114.6 CUDA bridge, Story 114.9 restoration). Under `BKM-049` / `delegate.py`, each Cloud story receives a single dispatch attempt; if Cloud fails for that specific story, that story alone may be escalated to `[AGY:PRIMARY]` while subsequent stories continue to target `[SWARM:CLOUD]`. Zero blanket self-promotion.
- [x] **5. Risk Assessment**: Modifying inference backends is isolated to experimental directories (`/home/jallred/strata_exp/`). Zero impact to production git state or databases.

---

## 🗺️ Sprint Track Architecture

```
PHASE 1: DUAL-VULKAN DISJOINT MOE EXPLORATION
   Track 1: Lab Quiescence & VRAM Clean-Room Prep (Story 114.1)
      │
      ▼
   Track 2: Strata Engine Toolchain & Vulkan Provisioning (Story 114.2)
      │
      ▼
   Track 3: GGUF Model Ingestion & Verification (Story 114.3)
      │
      ▼
   Track 4: Strata Multi-GPU Configuration Authoring (Story 114.4)
      │
      ▼
   Track 5: Vulkan Empirical Benchmarking & Profiling (Story 114.5)
      │
      ▼
PHASE 2: POST-VULKAN RPC METHOD EXPLORATION
   Track 6: Native CUDA FlashAttention + RPC Bridge Setup (Story 114.6)
      │
      ▼
   Track 7: RPC Empirical Benchmarking & Comparative Profile (Story 114.7)
      │
      ▼
PHASE 3: PUBLIC BENCHMARKS INTEGRATION & PRODUCTION RESTORATION
   Track 8: Public Benchmarks & Telemetry Generator Sync (Story 114.8)
      │
      ▼
   Track 9: Restoration, Quiescence Exit, & Accountability Quorum (Story 114.9)
```

---

## Phase 1: Dual-Vulkan Disjoint MoE Exploration

### 🛡️ Story 114.1: Lab Quiescence & Dual-GPU VRAM Reclamation Protocol
* **Status:** ✅ COMPLETE
* **Owner:** `[AGY:PRIMARY]`
* **Goal:** Gracefully quiesce the active lab services (`lab-attendant.service`, `vllm`/`llama-server` on port 8088/8000, Foyer WebSocket) to free 100% of GPU VRAM on both the RTX 2080 Ti (11GB) and Intel Arc B580 (12GB heap).
* **Anchor 1 (Target Files & Line Numbers):**
  - `/home/jallred/Dev_Lab/HomeLabAI/src/engine_ctl.sh:1-120`
  - `/etc/systemd/system/lab-attendant.service`
* **Anchor 2 (Verification Command):**
  - `/home/jallred/Dev_Lab/HomeLabAI/src/engine_ctl.sh stop`
  - `sudo systemctl stop lab-attendant.service`
  - `nvidia-smi --query-gpu=memory.used,memory.free --format=csv` (verifies $\le 300\text{ MB}$ used on 2080 Ti)
  - `vulkaninfo | grep -E "Vulkan0|Vulkan1"` (verifies Arc B580 clean)
* **Anchor 3 (Verbatim Specs & Implementation Ledger):**
  - Verify zero lingering processes on port 8088, 8000, or 8765 via `ss -tulpn`.
  - Capture pre-experiment snapshot of lab vitals to ensure 100% clean recovery at sprint conclusion.
* **Anchor 4 (DNA Links):** `[BKM-024]`, `[BKM-079]`.

---

### ⚙️ Story 114.2: Strata Engine Toolchain Setup & Vulkan Backend Compilation
* **Status:** ✅ COMPLETE
* **Owner:** `[SWARM:CLOUD]`
* **Goal:** Clone `Niko1221/Strata` into an isolated workspace (`/home/jallred/strata_exp/Strata`), audit dependencies, and compile/build the Vulkan inference backend (`STRATA_ENGINE_BACKEND=vulkan`) to enable cross-vendor device enumeration across NVIDIA and Intel.
* **Anchor 1 (Target Files & Line Numbers):**
  - `/home/jallred/strata_exp/Strata/`
  - `/home/jallred/strata_exp/Strata/CMakeLists.txt` or `Cargo.toml`
  - `/home/jallred/strata_exp/build_vulkan.sh`
* **Anchor 2 (Verification Command):**
  - `git clone https://github.com/Niko1221/Strata /home/jallred/strata_exp/Strata`
  - `cmake -B build -DSTRATA_BACKEND=VULKAN ... && cmake --build build -j 4`
  - `/home/jallred/strata_exp/Strata/bin/strata --version`
  - `/home/jallred/strata_exp/Strata/bin/strata --list-devices` (verifies enumeration of both RTX 2080 Ti and Arc B580)
* **Anchor 3 (Verbatim Specs & Implementation Ledger):**
  - Document compiler flags, library dependencies (Vulkan SDK, Mesa headers, SPIRV-Tools), and driver linkage.
  - Verify that both devices report correct memory pools without symbol collision.
* **Anchor 4 (DNA Links):** `[BKM-079]`, `[FEAT-689]`.

---

### 📦 Story 114.3: Model Ingestion & GGUF Compatibility Verification
* **Status:** ✅ COMPLETE
* **Owner:** `[SWARM:CLOUD]`
* **Goal:** Validate that our production model `/speedy/models/gguf/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` (20.61 GB) loads directly into Strata's tensor layout without re-quantization or architectural mismatches.
* **Anchor 1 (Target Files & Line Numbers):**
  - `/speedy/models/gguf/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf`
  - `/home/jallred/strata_exp/inspect_model.sh`
* **Anchor 2 (Verification Command):**
  - `ls -lh /speedy/models/gguf/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` (20.61 GB)
  - `/home/jallred/strata_exp/Strata/bin/strata inspect --model /speedy/models/gguf/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf`
* **Anchor 3 (Verbatim Specs & Implementation Ledger):**
  - Inspect model tensor metadata: verify 40 transformer layers, 8 experts per layer, 2 active experts (`top_k=2`), hidden size 4096, and quantized tensor types (`q4_K`, `q6_K`).
  - Confirm Strata tensor parser identifies MoE expert blocks vs dense self-attention blocks correctly.
* **Anchor 4 (DNA Links):** `[BKM-024]`, `[BKM-088]`.

---

### 🧩 Story 114.4: Strata Heterogeneous Multi-GPU Configuration Authoring
* **Status:** ✅ COMPLETE
* **Owner:** `[AGY:PRIMARY]`
* **Goal:** Translate our disjoint split architecture into a validated Strata configuration file (`strata-hetero.json`), strictly enforcing **Light System RAM Touch** (zero DDR3 model caching) and asymmetric device roles.
* **Anchor 1 (Target Files & Line Numbers):**
  - `/home/jallred/strata_exp/strata-hetero.json`
  - `/home/jallred/strata_exp/launch_strata.sh`
* **Anchor 2 (Verification Command):**
  - Validate JSON schema: `jq . /home/jallred/strata_exp/strata-hetero.json`
  - Launch dry-run: `/home/jallred/strata_exp/Strata/bin/strata launch --config /home/jallred/strata_exp/strata-hetero.json --dry-run`
* **Anchor 3 (Verbatim Specs & Implementation Ledger):**
  - Author `/home/jallred/strata_exp/strata-hetero.json`:
    ```json
    {
      "backend": "vulkan",
      "model_path": "/speedy/models/gguf/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf",
      "devices": [
        {
          "device_id": 1,
          "name": "NVIDIA GeForce RTX 2080 Ti",
          "role": "main",
          "vram_budget_gib": 10.5,
          "host_attention": true,
          "host_router": true,
          "expert_slice": [0, 1, 2]
        },
        {
          "device_id": 0,
          "name": "Intel Arc B580",
          "role": "helper",
          "vram_budget_gib": 11.2,
          "host_attention": false,
          "host_router": false,
          "expert_slice": [3, 4, 5, 6, 7]
        }
      ],
      "memory_policy": {
        "system_ram_cache_gib": 0.0,
        "pure_vram_pinning": true,
        "allow_host_spill": false
      },
      "context": {
        "max_context_tokens": 16384,
        "kv_quant": "q4_0"
      },
      "server": {
        "port": 8099,
        "api": "openai"
      }
    }
    ```
  - Enforce zero DDR3 host cache: assert system memory allocation remains strictly below $1.0\text{ GB}$ (process overhead only).
* **Anchor 4 (DNA Links):** `[BKM-079]`, `[BKM-088]`, `[REF-SPEC-DYNAMIC-01]`.

---

### 📊 Story 114.5: Vulkan Empirical Benchmarking, Profiling & Analysis
* **Status:** ⏳ PENDING
* **Owner:** `[SWARM:CLOUD]`
* **Goal:** Execute rigorous empirical benchmarks (TTFT, tokens/sec generation over 128/256/512 tokens, inter-GPU sync overhead) under the Vulkan backend and record baseline metrics.
* **Anchor 1 (Target Files & Line Numbers):**
  - `/home/jallred/strata_exp/bench_strata.py`
  - `/home/jallred/strata_exp/results/strata_vulkan_results.json`
* **Anchor 2 (Verification Command):**
  - `python3 /home/jallred/strata_exp/bench_strata.py --port 8099 --prompt-len 512 --gen-len 128 --runs 3`
  - Record: Warm TTFT (ms), Sustained decode throughput (tok/s), Peak VRAM usage on both GPUs (`nvidia-smi`, `xpu-smi`).
* **Anchor 3 (Verbatim Specs & Implementation Ledger):**
  - Measure:
    1. Warm Time-to-First-Token (TTFT) across 512-token prompts.
    2. Generation speed (tok/s) across 128, 256, and 512 generated tokens.
    3. Host system RAM delta during inference (assert zero DDR3 thrashing).
    4. Inter-GPU synchronization latency over Vulkan.
* **Anchor 4 (DNA Links):** `[BKM-024]`, `[BKM-088]`.

---

## Phase 2: Post-Vulkan RPC Heterogeneous Method Exploration

### ⚡ Story 114.6: Native CUDA FlashAttention + RPC Bridge Setup
* **Status:** ⏳ PENDING
* **Owner:** `[AGY:PRIMARY]`
* **Goal:** Once Phase 1 is proven, move beyond Vulkan to explore the **RPC Method**: compile native CUDA with FlashAttention for the RTX 2080 Ti (hosting Attention + Router + Expert slice 0–2), and bridge to an RPC daemon on the Intel Arc B580 (hosting Expert slice 3–7).
* **Anchor 1 (Target Files & Line Numbers):**
  - `/home/jallred/strata_exp/build_cuda_rpc.sh`
  - `/home/jallred/strata_exp/strata-rpc.json`
* **Anchor 2 (Verification Command):**
  - Build command: native CUDA Turing CC75 flags with RPC client/server support.
  - Launch Arc B580 RPC server daemon: `strata-rpc-server --dev Vulkan0 --port 50053`
  - Test loopback uplink: `curl -sf http://127.0.0.1:50053/health`
* **Anchor 3 (Verbatim Specs & Implementation Ledger):**
  - Author `/home/jallred/strata_exp/strata-rpc.json` with `backend: "cuda"` for local device (RTX 2080 Ti) and `remote_endpoint: "127.0.0.1:50053"` for remote expert slice.
  - Unlock Turing Tensor Core FlashAttention-2 prefill on the 2080 Ti while keeping the Arc B580 unencumbered as an external expert worker.
* **Anchor 4 (DNA Links):** `[BKM-079]`, `[FEAT-689]`.

---

### 📈 Story 114.7: RPC Empirical Benchmarking & Comparative Head-to-Head
* **Status:** ⏳ PENDING
* **Owner:** `[SWARM:CLOUD]`
* **Goal:** Benchmark the CUDA+RPC disjoint MoE configuration against Phase 1's Dual-Vulkan results and the canonical `moe-cuda-rpc` pipeline baseline (35.87 tok/s).
* **Anchor 1 (Target Files & Line Numbers):**
  - `/home/jallred/strata_exp/bench_strata.py`
  - `/home/jallred/strata_exp/results/strata_rpc_results.json`
  - `/home/jallred/strata_exp/results/moe_architecture_comparison.json`
* **Anchor 2 (Verification Command):**
  - `python3 /home/jallred/strata_exp/bench_strata.py --port 8099 --prompt-len 512 --gen-len 128 --runs 3`
  - Output side-by-side scorecard: Dual-Vulkan vs. CUDA+RPC vs. Canonical Pipeline.
* **Anchor 3 (Verbatim Specs & Implementation Ledger):**
  - Compare TTFT prefill boost (evaluating whether CUDA FlashAttention yields the same +49% prefill speedup seen in Sprint 110).
  - Profile loopback TCP/socket latency vs. Vulkan semaphore latency for inter-GPU expert vector dispatch.
* **Anchor 4 (DNA Links):** `[BKM-024]`, `[BKM-088]`.

---

## Phase 3: Public Benchmarks Integration & Production Restoration

### 🌐 Story 114.8: Public Benchmarks Telemetry & Cache Integration
* **Status:** ⏳ PENDING
* **Owner:** `[SWARM:CLOUD]`
* **Goal:** Ingest the certified empirical receipts from Phase 1 and Phase 2 into `benchmarks_cache.json`, `live_usage_stream.jsonl`, and the public benchmark generator docs, updating the Hardware Dashboard cards and Prometheus exporter.
* **Anchor 1 (Target Files & Line Numbers):**
  - `Portfolio_Dev/field_notes/benchmarks_cache.json:54-76`
  - `Portfolio_Dev/field_notes/data/live_usage_stream.jsonl`
  - `Portfolio_Dev/field_notes/benchmarks.html`
  - `Portfolio_Dev/field_notes/bench_models.py`
* **Anchor 2 (Verification Command):**
  - `python3 Portfolio_Dev/field_notes/bench_models.py --update-cache`
  - `curl -s http://z87-linux:9001/benchmarks_cache.json | jq '.results[] | select(.display_name | contains("Strata"))'`
* **Anchor 3 (Verbatim Specs & Implementation Ledger):**
  - Add new hardware configuration receipts:
    - `Hybrid MoE (Strata Dual-Vulkan Disjoint)`
    - `Hybrid MoE (Strata CUDA+RPC Disjoint)`
  - Populate: Throughput (tok/s), Warm TTFT (ms), Tokens/Joule efficiency, and VRAM memory footprint.
  - Deploy updated cache to `www_deploy/`.
* **Anchor 4 (DNA Links):** `[BKM-024]`, `[FEAT-525]`.

---

### 🔄 Story 114.9: Lab State Restoration, Quiescence Exit, & Accountability Quorum
* **Status:** ⏳ PENDING
* **Owner:** `[AGY:PRIMARY]`
* **Goal:** Safely terminate experimental Strata processes, restore canonical production runtime (`engine_ctl.sh start moe-cuda-rpc`), restart `lab-attendant.service`, and certify live cognitive health via accountability probe.
* **Anchor 1 (Target Files & Line Numbers):**
  - `/home/jallred/Dev_Lab/HomeLabAI/src/engine_ctl.sh`
  - `/home/jallred/Dev_Lab/HomeLabAI/src/tests/probe_round_table_accountability.py`
* **Anchor 2 (Verification Command):**
  - `/home/jallred/Dev_Lab/HomeLabAI/src/engine_ctl.sh start moe-cuda-rpc`
  - `sudo systemctl start lab-attendant.service`
  - `python3 /home/jallred/Dev_Lab/HomeLabAI/src/tests/probe_round_table_accountability.py` (verifies `critic_score: 1.0`, zero errors, live quorum certified)
* **Anchor 3 (Verbatim Specs & Implementation Ledger):**
  - Confirm production engine responds on `http://127.0.0.1:8088/v1/chat/completions`.
  - Confirm web intercom and status telemetry dashboards reflect `OPERATIONAL`.
* **Anchor 4 (DNA Links):** `[BKM-024]`, `[BKM-079]`.

---

## 📋 Pre-Flight Mistakes Avoided & Risk Mitigation Ledger

| Risk Factor | Historical Trap | Mitigation Invariant in SPRINT 114 |
| :--- | :--- | :--- |
| **DDR3 Host Spilling** | MoE runtimes default to host memory paging when VRAM feels constrained, causing an 8.3x performance collapse on DDR3-1600. | Set `system_ram_cache_gib: 0.0` and pin 100% of weights across the 23 GB VRAM pool. |
| **Compiler / Driver Clashes** | Mixing CUDA and oneAPI compilers corrupts Linux system libraries. | Use **Vulkan 1.4** as the primary Phase 1 backend, enumerating both GPUs in unified user space. |
| **Premature RPC Complexity** | Debugging RPC sockets before validating basic tensor sharding creates multi-variable diagnostic fog. | Complete and certify Phase 1 (Dual-Vulkan) before attempting Phase 2 (CUDA+RPC). |
| **Model Ingestion Waste** | Downloading duplicates of 20GB+ models exhausts speedy drive storage. | Point Strata directly to existing `/speedy/models/gguf/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf`. |
| **Service Interference** | Testing inference on active lab ports (8088/8000) causes port conflicts and crashes. | Quiesce the lab before experimenting; run Strata on isolated port `8099`. |
| **Telemetry Siloing** | Benchmark results remain buried in local scratch logs without public visibility. | Ingest certified receipts into `benchmarks_cache.json` and `benchmarks.html` via Story 114.8. |
| **Recovery Amnesia** | Experimental scripts leave dangling GPU memory or unstarted production daemons. | Enforce mandatory Story 114.9 restoration with `probe_round_table_accountability.py` certification. |
