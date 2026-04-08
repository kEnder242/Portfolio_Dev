# Forensic Review: vLLM v0.17.0 on Turing Hardware
**Date**: April 7, 2026 | **Version**: 1.0
**Target**: NVIDIA RTX 2080 Ti (Compute 7.5 / 11GB VRAM)

## 🔍 Executive Summary
Following a deep code review of the **vLLM v0.17.0** source and a comprehensive physical verification gauntlet, it is confirmed that this version enforces the **V1 Architecture**. The legacy "V0" engine core has been completely removed. Stability on Turing hardware is achievable but requires strict adherence to **Shell-Based Ignition** and specific backend parameters.

---

# 🏺 vLLM v0.17.0 Addendum: The "Python Trap" (April 7, 2026)

## 🔍 Forensic Synthesis: The Launch Method Root Cause
The stability gauntlet of Sprint 19.0 identified that the transition from **Shell-Based Ignition** to **Python-Object Management** was the primary cause of engine silence.

### 1. The "Python Trap" Hypothesis
*   **Mechanism**: Assigning a `subprocess.Popen` object to a local variable (e.g., `proc = subprocess.Popen(...)`) and then allowing that variable to go out of scope triggers Python's **Garbage Collector**. 
*   **The Fault**: On some kernel versions, when the GC reclaims the `Popen` object, it may prematurely close standard file descriptors (stdin/stdout/stderr) or send signals to the child process group, even when `start_new_session=True` is used.
*   **The Result**: The vLLM API server remains "Up" (port open), but the EngineCore background process deadlocks or is reaped, leading to "Connection Refused" during inference.

### 🏛️ vLLM Launch Evolution Table (Sprints 13-19)

| Milestone | Commit | Method | Core Parameters | Result |
| :--- | :--- | :--- | :--- | :--- |
| **Sprint 13 Baseline** | `6baec45` | **Shell Script** | `xformers`, `V0`, `util: 0.4`, `max-len: 4096` | **VOCAL** |
| **Sprint 17 Baseline** | `f2dd580` | **Shell Script** | `TRITON_ATTN`, `V0`, `util: 0.4`, `LoRAs: 4` | **VOCAL** |
| **Sleep Mode 2** | `bdff415` | **Direct Python** | `TRITON_ATTN`, `V1`, `util: 0.4` | **SILENT** |
| **Turing Lockdown** | `Verified` | **Shell Script** | `TRITON_ATTN`, `V1`, `util: 0.5`, `max-len: 8192` | **VOCAL** |

## ⚖️ The "Shell Supremacy" Standard
*   **Mandate**: The Lab Attendant must use `bash start_vllm.sh` without holding an active Python process reference.
*   **PID Tracking**: Tracking must be handled via a physical file (`run/vllm.pid`) written by the shell script itself.
*   **Headroom**: `TRITON_ATTN` + `0.5 utilization` is confirmed stable post-reboot.

---

# 🏺 vLLM v0.17.0 Addendum: The "Placebo" Flags (April 7, 2026 Update)

## 🛠️ Flag Re-Education

### 1. VLLM_SERVER_DEV_MODE=1
*   **Status**: **RECOMMENDED**.
*   **Function**: Enables FastAPI debug endpoints. While not strictly required for basic Sleep Mode, it exposes the `/reset_prefix_cache` and `/offload` routes which were part of the Sprint 16 "Eureka" success. It allows the Attendant to perform surgical state manipulation without a full engine reload.

### 2. VLLM_USE_V1=0
*   **Status**: **PLACEBO (LEGACY)**.
*   **Function**: Historically disabled the V1 engine core. In v0.17.0, the V0 core has been physically removed from the binary. 
*   **Finding**: Setting this to `0` has no physical effect on the architecture (V1 is always used), but it is maintained in the `start_vllm.sh` script for backward compatibility with older venv restores.

### 3. The Hibernation Regression
The failure of Level 2 Sleep in v0.17.0 is due to the **V1 EngineCore Deadlock**. Because V1 uses a background ZMQ pipe, any kernel-level compilation failure during the KV-cache swap causes the process to hang. The **Atomic Reap** method from Sprint 16 remains the only 100% reliable reclamation path for Turing hardware.
