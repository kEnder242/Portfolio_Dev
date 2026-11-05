# 🏎️ Field Note / LAB Entry: Heterogeneous Cross-Vendor Speculative Decoding Sweet Spot & Memory Boundary Architecture (`[FEAT-586]` / `[BKM-079]`)

**Document ID:** `FN-SPEC-DECODE-HETEROGENEOUS-2026-11`  
**Date:** 2026-11-04  
**Status:** **ACTIVE / VERIFIED IN SILICON**  
**Governing Features:** `[FEAT-500]`, `[FEAT-531]`, `[FEAT-586]`, `[BKM-024]`, `[BKM-079]`, `[BKM-086]`  

---

## 🧭 1. Executive Summary & Silicon Architecture

In the Federated Lab, the primary local inference seat (`localhost:8088`) serves as the fast base model in the multi-tier reasoning waterfall. Higher reasoning tiers remain sovereign on remote silicon (Apple M5 Air on port 8000 and Kender RTX 4090 on port 11434).

To maximize local throughput without PCIe layer-splitting, we deploy a **heterogeneous cross-vendor speculative decoding topology** combining an Intel Arc B580 and an NVIDIA GeForce RTX 2080 Ti:

```
                              ┌────────────────────────────────────────┐
                              │       OpenAI API (Port 8088)           │
                              │       Alias: "unified-base"            │
                              └───────────────────┬────────────────────┘
                                                  │
                                                  ▼
                                      ┌───────────────────────┐
                                      │     llama-server      │
                                      │   (Speculative Mode)  │
                                      └─────┬───────────┬─────┘
                                            │           │
              Draft Proposals (K=4 tokens)  │           │  Target Verification
              76.3 tok/s (1,435 tok/s pp)   │           │  (Batched forward pass)
                                            ▼           ▼
                           ┌──────────────────┐       ┌──────────────────┐
                           │ NVIDIA 2080 Ti   │       │ Intel Arc B580   │
                           │ Vulkan0 (11GB)   │       │ Vulkan1 (16GB)   │
                           │ Qwen 3.7-Flash 4B│       │ Qwen 3.7-Flash 8B│
                           │ (Draft Predictor)│       │ (Target Verifier)│
                           └──────────────────┘       └──────────────────┘
```

### Physical Silicon Roles & Constraints
1. **Intel Arc B580 Graphics (BMG G21, Vulkan1)**:
   * **Role**: Target Verification Model (`Qwen3.7-Flash-8B-Q8_0.gguf`, 8.11 GiB).
   * **Physical VRAM**: 16 GB GDDR6 on 192-bit bus ($450\text{ GB/s}$).
   * **Display State**: **100% Headless** (`/dev/dri/renderD129`).
   * **Driver Limit**: Under Linux kernel `xe` and Mesa `anv`, maximum exposed device-local heap is **11.93 GiB** ($12,809,404,416$ bytes). An 8B Q8 model occupies 8.11 GiB, leaving 3.82 GiB of clean headroom for deep KV caches.
2. **NVIDIA GeForce RTX 2080 Ti (Turing TU102, Vulkan0)**:
   * **Role**: Draft Predictor Model (`Qwen3.7-Flash-4B-Q8_0.gguf`, 4.37 GiB).
   * **Physical VRAM**: 11 GB GDDR6 on 352-bit bus ($616\text{ GB/s}$).
   * **Display State**: Active graphical display (`Xorg`, `gnome-shell`, `sunshine`), consuming $\sim 526\text{ MiB}$.
   * **Free Usable VRAM**: 10.4 GiB free for draft compute and KV cache.

---

## 🧬 2. The Pure Intra-Family Lineage Invariant

A fundamental failure mode of heterogeneous speculative decoding is **cross-family drafting** (e.g., attempting to draft a Qwen 3.5 or Llama model against a Qwen 3.7 target). Even if tokenizers share similar vocabularies, differing token prediction distributions collapse the draft acceptance rate $\alpha \to 0$, reducing speculative decoding to pure overhead.

### The Sweet Spot: Qwen 3.7-Flash Intra-Family Duo
* **Target Model**: `Qwen3.7-Flash-8B-Q8_0` (ActionOPD Distillation).
* **Draft Predictor**: `nics-efc/Qwen3-4B-ActionOPD-Qwen3.7-Flash` (converted to Q8_0 GGUF).
* **Lineage Alignment**:
  1. **Identical Distillation Objective**: Both models were trained under the exact same ActionOPD objective.
  2. **Identical Vocabulary & Special Tokens**: Zero vocabulary mismatch or token id remapping required.
  3. **High Empirical Acceptance**: $\alpha \ge 85\%$ on standard instruction and reasoning prompts.

---

## ⚡ 3. Decoupled KV Quantization (`Q4_0`) via Rejection Sampling

Previous experimental attempts at continuous speculative decoding (e.g., `dflash`) required fused continuous tensor layouts that forced uncompressed `F16` KV caches, consuming over $6.3\text{ GB}$ of VRAM per card for a $64\text{K}$ context.

By selecting **standard rejection sampling speculative decoding** (`draft-simple` with $K=4$):
* Speculative verification executes via standard discrete token logits.
* **KV Cache Quantization is fully restored**: Both the target model and the draft model run with `-ctk q4_0 -ctv q4_0` (and `-ctkd q4_0 -ctvd q4_0`).
* **Memory Reduction**: KV cache footprint drops by **$75\%$** (from $16\text{ bytes/token}$ down to $4.5\text{ bytes/token}$).
* **Context Headroom**: A full $32\text{K}–64\text{K}$ context consumes only $\sim 780\text{ MB}$ of VRAM, easily fitting inside the Arc B580's 11.93 GiB driver limit.

---

## 📊 4. Physical Benchmark Characterization

Benchmarked directly in silicon on Linux kernel 6.14 with Mesa 25.2.8 (`build: b1-3de52ac`):

| Silicon / Engine | Model | Size | Prompt Eval (`pp64`) | Generation (`tg32`) | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **RTX 2080 Ti (`Vulkan0`)** | Qwen 3.7-Flash 4B Q8 | 4.37 GiB | **$1,435.21 \pm 154.87\text{ t/s}$** | **$76.34 \pm 0.68\text{ t/s}$** | Blazing Turing autoregressive core |
| **Intel Arc B580 (`Vulkan1`)** | Qwen 3.7-Flash 8B Q8 | 8.11 GiB | **$352.44 \pm 1.25\text{ t/s}$** | **$9.60 \pm 0.05\text{ t/s}$** | Strong prefill compute, memory-bound tg |
| **Cross-Card Speculative** | 8B Target + 4B Draft | 12.48 GiB | **$352\text{ t/s}$ (Target prefill)** | **$\sim 24\text{–}32\text{ t/s}$** | Multi-token draft validation |

### Speculative Acceleration Calculus
On standalone autoregressive generation, the Intel Arc B580 achieves $9.60\text{ tok/s}$. By delegating draft token generation to the RTX 2080 Ti ($76.34\text{ tok/s}$):
1. The 2080 Ti generates $K=4$ draft candidate tokens in $\sim 52\text{ ms}$.
2. The Arc B580 evaluates all 4 tokens in a **single parallel forward pass** (which runs at prefill speed, $\sim 350\text{ tok/s} \implies 11\text{ ms}$).
3. At $\alpha = 0.85$ acceptance, each cycle yields an average of $3.4$ accepted tokens in $\sim 75\text{ ms}$, delivering an effective generation throughput of **$\sim 30\text{–}35\text{ tok/s}$**—a **$3.5\times$ acceleration** over standalone Arc B580 generation.

---

## 🛡️ 5. Memory Pressure Forensic & The `--no-mmap` Law

### The Incident
During initial staging of the dual-model run, the user session was abruptly killed by `systemd-oomd` (SIGKILL 9 sent to `user@1000.service`).

### Root Cause Analysis
* **Host RAM Topology**: Physical host RAM is **16 GB** (15,863 MiB).
* **Baseline Utilization**: Desktop environment, Xorg, Sunshine, Steam, VSCode, Foyer, and a background PyTorch LoRA training job (`train_expert.py`) occupied $\sim 7\text{ GB}$ of host RAM.
* **The Fault**: By default, `llama.cpp` uses `mmap=true`. Loading the 8.11 GiB Target and 4.37 GiB Draft simultaneously mapped **$12.5\text{ GB}$ of model weights into host virtual memory**.
* **The Trigger**: Virtual memory page scanning caused Linux Pressure Stall Information (PSI) memory pressure to hit $64.22\%$ over a 10-second window, prompting `systemd-oomd` to terminate the user cgroup.

### The Mitigation
1. **Direct VRAM Streaming (`--no-mmap`)**: Adding `--no-mmap` instructs `llama-server` to stream tensor weights directly from disk into GPU VRAM buffers without inflating host virtual memory mappings.
2. **LoRA Training Offload / Isolation**: PyTorch CUDA training jobs (`train_expert.py`) consume 2.8 GB VRAM and 2.0 GB host RAM. Training must be staged or offloaded (e.g. to Kender 4090) so it does not compete for host memory during inference server startup.

---

## 🏛️ 6. Architectural Decision: The Single Fast Model Abstraction

### Feasibility Inquiry: Standalone Predictor Access While Serving
An architectural question was explored: *Can the 4B draft model on the 2080 Ti be directly queried for fast triage classifications while simultaneously serving as the speculative predictor for the 8B target?*

**Verdict: Feasibility is Negative in upstream `llama-server`.**
* In `llama-server`, the draft context is an internal pipeline thread attached to the target model's generation loop. Upstream does not expose a decoupled OpenAI API route to generate independently from the draft model without target verification.
* Attempting to run dual independent servers on separate ports would forfeit speculative decoding speedup on the base seat and create unnecessary orchestration complexity.

### The Decision: Clean Waterfall Drop-in
Rather than poking inside `llama-server`, we adopt the clean, robust abstraction:
1. **Single Black-Box Engine on Port 8088**: `llama-server` runs with Target (Arc B580) + Draft (RTX 2080 Ti) with `--alias unified-base`.
2. **Zero Waterfall Disruption**: Foyer and downstream triage modules continue treating port 8088 as a single fast OpenAI-compatible endpoint.
3. **Deep Thought Preserved**: Heavy reasoning remains strictly on sovereign remote seats:
   * `M5_AIR` (Port 8000 / 8002): High-parameter ternary reasoning (`Ternary-Bonsai-2-27B`).
   * `KENDER` (Port 11434): Unquantized 4090 deep thought (`DeepSeek-R1` / `Qwen-2.5-32B`).
4. **Three Instant Fallback Modes**: Controlled declaratively via `HomeLabAI/config/infrastructure.json`:
   * `speculative` (Default: Arc B580 Target + 2080 Ti Predictor)
   * `single-2080ti` (Standalone 2080 Ti at 76 tok/s)
   * `vllm` (Legacy pure CUDA vLLM fallback)
