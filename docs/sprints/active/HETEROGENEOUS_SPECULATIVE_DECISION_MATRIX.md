# 🧭 HETEROGENEOUS DUAL-GPU SPECULATIVE DECISION MATRIX & DYNAMIC RE-EVALUATION PROTOCOL

**Document ID:** `REF-SPEC-DYNAMIC-01`  
**Parent Frameworks:** `BKM-024` (Live Silicon Grounding), `BKM-086` (Paved-Path Sprint Protocol), `BKM-088` (Empirical Pipeline Step Judgment), `FEAT-155` (Logic Glue & Sovereign Scaling), `INS-042` (Anti-Waffle & Complexity Conservation).  
**Context:** Multi-GPU Heterogeneous Inference across **Intel Arc B580 (Slot 1)** and **NVIDIA GeForce RTX 2080 Ti (Slot 2)** under Linux 6.x (`xe` / Vulkan 1.4 & NVIDIA Proprietary Driver).  
**Revision Date:** November 4, 2026  
**Status:** **AUTHORITATIVE LIVING GUIDE & DECISION MATRIX**

---

## 📌 1. Forensic Executive Summary & Mistakes Avoided

### What Went Wrong in Prior Evaluations (The Anti-Amnesia Record)
1. **The Phantom 16GB Trap**:
   - We assumed the Arc B580 offered $15.3\text{ GiB}$ of usable VRAM because the physical PCB has 16GB.
   - *Empirical Truth*: Under Linux kernel 6.x (`xe` driver) and Mesa 25.2.8 (`anv` Vulkan), the kernel driver exposes a **maximum device-local heap of only $\mathbf{11.93\text{ GiB}}$** (`12,809,404,416` bytes).
   - When the HDMI monitor was plugged into Card 0, `Xorg`, `gnome-shell`, `mutter`, and `Steam` ate another $1.22\text{ GiB}$, leaving **only $10.73\text{ GiB}$ free for Vulkan compute**.
2. **The Inflation of KV Cache Footprint (The FP16 Fallacy)**:
   - We anchored on FP16 KV caching ($147.5\text{ KB/token}$ on 8B, $196.6\text{ KB/token}$ on 14B), which falsely made $32\text{K}–64\text{K}$ context look impossible without gigabytes of bloat.
   - *Empirical Truth*: Modern quantized KV caching (`-ctk q4_0 -ctv q4_0`) reduces memory by **$75\%$** with $<0.05$ perplexity delta, bringing $64\text{K}$ context on a 14B model down to just **$3.15\text{ GB}$**.
3. **The Layer-Split Blunder**:
   - Despite an explicit directive to test target/predictor (`-m` and `-md`) and avoid layer splits, we defaulted back to `-sm layer -ts 1,1`, dragging 8B generation from $60\text{ tok/s}$ down to $14.9\text{ tok/s}$ due to inter-GPU PCIe layer round-trips.
4. **The Overlooked 14B Sweet Spot**:
   - We assumed 14B wouldn't fit on an 11GB card, ignoring that **`14B Q4_0` is only $\mathbf{7.6–7.9\text{ GB}}$**, fitting cleanly on the 2080 Ti with $3.2\text{ GB}$ left for a $32\text{K}–64\text{K}$ context window.

---

## 🔌 2. The Physical Silicon Topology (Swapped HDMI Reality)

When the display cable is swapped to the NVIDIA RTX 2080 Ti:

| Metric | Intel Arc B580 (Slot 1, `card0`, `renderD129`) | NVIDIA GeForce RTX 2080 Ti (Slot 2, `card2`, `renderD130`) |
| :--- | :--- | :--- |
| **Physical VRAM** | 16.0 GB GDDR6 (192-bit bus, 450 GB/s) | 11.0 GB GDDR6 (352-bit bus, 616 GB/s) |
| **Kernel / Driver** | Linux `xe` driver + Mesa `anv` Vulkan 1.4 | NVIDIA Proprietary (Driver 580.x) |
| **Exposed Vulkan Heap** | **11.93 GiB** (Driver hard cap) | **11.00 GiB** (11,264 MiB full allocation) |
| **Display / OS Load** | **0.00 GiB (100% Headless Compute)** | **$\sim 1.30\text{ GiB}$ (Xorg, GNOME, Steam, Mutter)** |
| **Net Usable Compute VRAM** | **$\mathbf{11.93\text{ GiB}}$** ⭐ **(The Large Capacity Node)** | **$\mathbf{9.30–9.50\text{ GiB}}$** ⚡ **(The Fast Predictor Node)** |
| **Optimal Architectural Role** | **TARGET MODEL ($M$) + Target KV Cache** | **DRAFT PREDICTOR ($M_d$) + Draft KV Cache** |

---

## 🏛️ 3. Core Architectural Invariants (Non-Negotiable Laws)

1. **Law 1: Strict Intra-Family Lineage Only**:
   - The Target and Draft models **MUST** belong to the exact same training lineage, sharing identical tokenizers, vocabularies, and representation distributions.
   - *Approved Lineages*:
     - **Qwen 3.7-Flash / ActionOPD**: Target 8B + Draft 4B.
     - **Qwen 3.5 Dense**: Target 14B + Draft 3B.
     - **DeepSeek-R1-Distill-Qwen**: Target 14B + Draft 1.5B/7B.
   - *Forbidden*: Cross-family pairing (e.g. Qwen 3.5 draft with Qwen 3.8 target, or Llama draft with Qwen target). Divergence collapses acceptance rate $\alpha < 20\%$.
2. **Law 2: Zero Layer-Splitting Across PCIe (`-sm none`)**:
   - No individual model weights may span both cards. Layer-by-layer sequential round trips over PCIe incur an unacceptable latency tax.
3. **Law 3: RTX 2080 Ti is the Dedicated Sprinter**:
   - With $616\text{ GB/s}$ bandwidth and Turing Tensor Cores, the 2080 Ti must always host the Draft model ($M_d$) drafting at $\ge 80–140\text{ tok/s}$.
4. **Law 4: Arc B580 is the Dedicated Verifier**:
   - With $11.93\text{ GiB}$ headless capacity, the Arc B580 hosts the Target model ($M$), verifying $K$-token candidate batches in a single parallel prefill forward pass.
5. **Law 5: Weight & KV Compression as First-Order Requirements**:
   - `Q4_0` / `UD-Q3` weights and `q4_0` KV caching are standard baseline configurations, not afterthoughts.
6. **Law 6: Non-Anemic Context Runway ($\ge 32\text{K}–64\text{K}$)**:
   - Any proposed deployment must maintain at least $32\text{K}$ (and ideally $64\text{K}$) context with $\ge 1.5\text{ GB}$ physical headroom buffer.

---

## ⚡ 4. The FlashAttention vs. KV Quantization Tension (M5 Air Lessons)

### The Technical Conflict
In `llama.cpp` (and MLX on Apple Silicon):
- **FlashAttention (`-fa on`)**: Restructures attention computation into tiled blocks to prevent materializing the full $N \times N$ attention matrix, slashing memory bandwidth usage during long-context processing.
- **The Kernel Limitation**: Most FlashAttention implementations require continuous, unquantized **FP16 or BF16** KV cache tensors.
- When quantized KV caching (`-ctk q4_0 -ctv q4_0`) is combined with `-fa on`:
  - On some backends (Metal / older CUDA / Vulkan), `llama.cpp` prints a warning and **silently falls back to standard dequantized attention**, OR fails kernel launch assertions.
  - On newer Vulkan backends, dynamic dequantization inside tiled shaders is supported but incurs an arithmetic overhead.

### The Decision Rule:
$$\text{Context Length} \le 16\text{K} \implies \text{FlashAttention ON } (\text{FP16 KV Cache acceptable})$$
$$\text{Context Length} \ge 32\text{K}–64\text{K} \implies \mathbf{Q4\_0\text{ KV Cache Takes Precedence}} \text{ (Capacity Overrules Tile Optimization)}$$

At $64\text{K}$ context, avoiding an out-of-memory crash is infinitely more valuable than a $10\%$ compute tiling speedup. Always verify backend support with `--flash-attn on -ctk q4_0` via live test.

---

## 📊 5. The Dynamic ROI & Feasibility Matrix

*Assuming Swapped HDMI: Arc B580 = $11.93\text{ GiB}$ Headless; RTX 2080 Ti = $9.40\text{ GiB}$ Display-Bound.*

| Architecture Tier | Target ($M$) on Arc B580 | Draft ($M_d$) on 2080 Ti | Target VRAM ($64\text{K}$ Q4 KV) | Draft VRAM ($64\text{K}$ Q4 KV) | Speculative Acceptance $\alpha$ | Est. Net Tok/s | ROI & Feasibility Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Tier 1: 14B Dense** ⭐ *(Golden Speculative)* | `Qwen 3.5 14B Q4_0` ($7.7\text{ GB}$) | `Qwen 3.5 3B Q4_0` ($2.2\text{ GB}$) | $7.7 + 3.15 = \mathbf{10.85\text{ GB}} \le 11.93$ | $2.2 + 1.83 = \mathbf{4.03\text{ GB}} \le 9.40$ | $\approx 72–78\%$ | **$38–48\text{ t/s}$** | 🟢 **OPTIMAL ROI**: True 14B logic depth, full 64K context, massive margin on 2080 Ti. |
| **Tier 2: 14B Distill** ⭐ *(Frontier Reasoning)* | `DeepSeek-R1-Distill-Qwen-14B Q4_0` ($7.7\text{ GB}$) | `DeepSeek-R1-Distill-Qwen-1.5B/7B Q4_0` ($1.2–4.5\text{ GB}$) | $7.7 + 3.15 = \mathbf{10.85\text{ GB}} \le 11.93$ | $4.5 + 1.83 = \mathbf{6.33\text{ GB}} \le 9.40$ | $\approx 80–85\%$ | **$35–45\text{ t/s}$** | 🟢 **MAX INTELLIGENCE ROI**: R1 chain-of-thought traces with tight draft coupling. |
| **Tier 3: 8B Flash** *(High Speed)* | `Qwen 3.7-Flash 8B Q4_0` ($4.8\text{ GB}$) | `Qwen 3.7-Flash 4B Q4_0` ($2.6\text{ GB}$) | $4.8 + 2.36 = \mathbf{7.16\text{ GB}} \le 11.93$ | $2.6 + 1.83 = \mathbf{4.43\text{ GB}} \le 9.40$ | $\approx 85–90\%$ | **$45–55\text{ t/s}$** | 🟡 **GOOD, BUT REDUNDANT**: Very fast, but 8B standalone on 2080 Ti already hits 50+ tok/s. |
| **Tier 4: 27B Unsloth** *(Physical Wall)* | `Qwen 3.8 27B UD-Q3` ($11.2\text{ GB}$) | `Qwen 3.5 3B Q4_0` ($2.2\text{ GB}$) | $11.2 + 3.15 = \mathbf{14.35\text{ GB}} > 11.93$ | $2.2 + 1.83 = \mathbf{4.03\text{ GB}}$ | N/A | **0 t/s (OOM)** | 🔴 **FATAL (DO NOT ATTEMPT)**: Exceeds Arc B580 11.93 GiB driver limit. |
| **Tier 5: 14B Standalone** *(No Speculation)* | `Qwen 3.5 14B Q4_0` on 2080 Ti | None (Standalone) | N/A (Arc Idle) | $7.7 + 1.57\text{ (32K)} = \mathbf{9.27\text{ GB}} \le 9.40$ | N/A | **$38–42\text{ t/s}$** | 🟡 **TIGHT MARGIN**: Fits at 32K context; at 64K, display load will cause OOM. |

---

## 📋 6. The Re-Evaluation Checklist Protocol

Before downloading, converting, or configuring any model pairing, run through this 8-step verification gate:

```markdown
- [ ] 1. Lineage Gate: Do Target ($M$) and Draft ($M_d$) belong to the exact same training family and vocabulary?
         (e.g., Qwen 3.5 + Qwen 3.5, or R1-Distill-Qwen + R1-Distill-Qwen). If NO, STOP.
- [ ] 2. Arc B580 Weight Gate: Are Target model weights $\le 8.5\text{ GiB}$?
         ($11.93\text{ GiB exposed heap} - 8.5\text{ GiB weights} = 3.43\text{ GiB reserved for 64K KV cache}$).
- [ ] 3. 2080 Ti Draft Weight Gate: Are Draft model weights $\le 5.0\text{ GiB}$?
         ($9.40\text{ GiB net budget} - 5.0\text{ GiB weights} = 4.40\text{ GiB reserved for Draft KV + display}$).
- [ ] 4. KV Quantization Flag: Is quantized KV caching enabled?
         (`-ctk q4_0 -ctv q4_0` for Target and `-ctkd q4_0 -ctvd q4_0` for Draft).
- [ ] 5. Context Horizon Assertion: Does the planned context ($32\text{K}$ or $64\text{K}$) fit within the remaining headroom?
         (14B @ 64K Q4 KV = $3.15\text{ GB}$; 8B @ 64K Q4 KV = $2.36\text{ GB}$; 3B @ 64K Q4 KV = $1.83\text{ GB}$).
- [ ] 6. Zero Layer-Split Check: Are device assignments completely segregated?
         (`-dev Vulkan0 -ngl 99` for Target on Arc B580; `-devd Vulkan1 -ngld 99` for Draft on 2080 Ti; NO `-sm layer`).
- [ ] 7. FlashAttention Compatibility Check: Test run 1 turn with `-fa on`.
         If driver warns of dequantization or throws kernel error, leave `-fa auto` or rely on Q4 KV cache.
- [ ] 8. Silicon Sanity Benchmark: Run 64 prompt / 32 gen tokens:
         `llama-cli -m <target> -dev Vulkan0 -md <draft> -devd Vulkan1 --spec-draft-n-max 4 -n 32`
         Verify draft acceptance rate $\alpha \ge 70\%$ and net throughput $\ge 35\text{ tok/s}$.
```

---

## 🎯 7. Definitive Recommendation for Next Boot

Once you swap the HDMI cable to the RTX 2080 Ti and reboot:

1. **Deploy Tier 1 or Tier 2 Speculative Pairing**:
   - **Target on Arc B580 (Headless 11.93 GiB)**: `Qwen 3.5 14B Q4_0` (or `DeepSeek-R1-Distill-Qwen-14B Q4_0`).
   - **Draft on RTX 2080 Ti (Display-Bound 9.40 GiB)**: `Qwen 3.5 3B Q4_0` (or `DeepSeek-R1-Distill-Qwen-1.5B/7B Q4_0`).
   - **Flags**: `-ctk q4_0 -ctv q4_0 -c 65536 --spec-draft-n-max 4`.
2. **Expected System Performance**:
   - **$38–45\text{ tok/s}$** generation speed on a true 14-billion parameter reasoning brain.
   - Full **$64\text{K}$ context window** with zero paging.
   - Zero layer splitting; $100\%$ hardware offload across both GPUs.
