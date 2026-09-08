# Retrospective: The vLLM Silicon Gauntlet

### 🔬 Objective
To achieve stable vLLM residency on the RTX 2080 Ti (Turing / Compute 7.5) for multi-LoRA strategic reasoning.

### 🧪 The Silicon Gauntlet (Summary of Attempts)

| Permutation | Components | Result | Finding |
| :--- | :--- | :--- | :--- |
| **Bleeding Edge** | v0.7.2 + Driver 570 + Kernel 6.17 | **DEADLOCK** | Weight-loading hang at 333MiB. |
| **Stable Anchor** | v0.12.0 + Driver 550 + Kernel 6.8 | **DEADLOCK** | Same 333MiB stall; not a driver version issue. |
| **GGUF Last Stand** | v0.7.2 + GGUF Native weights | **DEADLOCK** | Loader-agnostic failure. |
| **Ancient Resident** | v0.4.2 + Python 3.10 + Driver 550 | **DEADLOCK** | Legacy engines also hit the initialization wall. |
| **Nuclear Resilience** | `--dtype half`, `--enforce-eager`, `XFORMERS` | **DEADLOCK** | Even with aggressive FP16 forcing, the engine stalls. |

### 🛡️ The "Physical Hardware Isolation" Breakthrough [FEAT-029]
We successfully bypassed Ubuntu's aggressive driver meta-packages and kernel auto-probes.
- **The Hammer:** Physically erased active module files (`.ko.zst`) to break the 10s reload loop.
- **The Anchor:** Secured a stable Driver 550.120 installation on Kernel 6.8.0.

### 🧬 The Root Cause (The Float Issue)
The RTX 2080 Ti (Turing) lacks native **BF16** hardware units. Modern vLLM engines (v0.5+) are heavily optimized for **Ampere+ (Compute 8.0)** instructions. The deadlock occurs when the engine attempts to map BF16 model tensors into Turing execution units, causing a silent driver-level stall.

### 🏁 Final State & Recommendations
- **Status:** vLLM resurrection is officially **TABLED** for Turing hardware. 
- **Baseline:** Standardize on **Ollama**. It natively handles the BF16->FP16 casting for Turing without the initialization deadlocks.
- **Unity Pattern:** Achievement of sub-second prompt/model swapping in Ollama provides 90% of the value we sought from vLLM.

### 💎 Lost Gems & Hard-Won BKMs

1.  **The USB-C Lurker (`i2c_nvidia_gpu`):**
    *   Turing cards feature a USB-C controller that acts as a hidden hardware probe. Even after the main driver is unloaded, this module can trigger the kernel to reload the NVIDIA driver every 10-30 seconds. 
    *   **BKM:** Force-unload `i2c_nvidia_gpu` and `i2c_ccgx_ucsi` to truly secure a vacant silicon state.

2.  **The "Bully" Kernel Conflict:**
    *   Kernels 6.14+ on Ubuntu Noble have a hard-coded "Minimum Driver" requirement for 570+. 
    *   **BKM:** To maintain Driver 550, you MUST purge all HWE kernels and lock the system to the Production Kernel (6.8.0).

3.  **Model-Implementation Independence:**
    *   Testing `--model-impl=transformers` confirmed that the deadlock persists even when bypassing vLLM's custom CUDA kernels.
    *   **Finding:** The deadlock is likely occurring during the **Python Multiprocessing/Ray fork** phase or the initial PCI-bus handshake, making it an architectural roadblock rather than a kernel mismatch.
