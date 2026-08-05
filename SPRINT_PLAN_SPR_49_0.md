# 📜 SPRINT PLAN: Sprint 49.0 — Unity Pattern Enforcement & Live Telemetry Architecture

**Session Focus**: Enforce the **Unity Pattern (Model Uniformity)** across all local inference and test suites, eliminate hardcoded model strings in favor of the `unified-base` single source of truth, unify benchmark suites to target the `UNITY` abstraction string, and transition benchmarking from synthetic offline scripts to continuous live NVML/Prometheus telemetry harvesting.

---

## 🏛️ Architectural Context & Deep Dive

### 1. The Unity Pattern Core Truth (`[FEAT-030]` / `LAB-003`)
* **What It Mandates**: On `z87-Linux` (RTX 2080 Ti 11GB VRAM), all local inference nodes (Pinky, Brain, Architect, Archive) **MUST share a single resident base model foundation** loaded in vLLM (`port 8088`). Multi-LoRA (`--enable-lora`) dynamically multiplexes personas (`cli_voice_v1`, `shadow_brain_v2`, `lab_history_v1`) on top of this single base within a shared **~2.5GB VRAM footprint**.
* **Model Fluidity**: The mandate does **NOT** enforce a specific brand (Llama vs. Qwen vs. Phi). The base model itself is model-fluid—whatever is designated as `unified-base` in `infrastructure.json` becomes the sole resident foundation.
* **The Failure Mode We Are Fixing**: When Node KENDER (Windows RTX 4090) goes offline, legacy failover paths in `manager.py`, `loader.py`, and integration tests attempted to spin up `qwen2.5-coder:14b` in Ollama alongside vLLM. This created a **Dual-Foundation Collision** (14B Qwen + 3B Base + ChromaDB + NeMo = 34GB total memory demand), collapsing 15GB system RAM into physical disk swap (`/dev/sda5`) and freezing mouse interrupts.

---

### 2. Single Source of Truth: `unified-base` Pointer (`infrastructure.json`)
* **The Master Pointer**: [`config/infrastructure.json`](file:///home/jallred/Dev_Lab/HomeLabAI/config/infrastructure.json#L48) defines `model_manifest.unified-base` (e.g. `"llama-3.2-3b-awq"`).
* **Global Resolution Law**:
  1. Every local module (`cognitive_hub.py`, `lab_attendant_v4.py`, `manager.py`, `loader.py`) MUST resolve local model endpoints through `infrastructure.json["model_manifest"]["unified-base"]`.
  2. Hardcoded local model strings (like `"qwen2.5-coder:14b"`, `"gemma2:2b"`, `/speedy/models/...`) in fallback logic are **STRICTLY FORBIDDEN**.
  3. If KENDER is offline, local fallback is **FORBIDDEN** from loading a non-Unity model into local Ollama/vLLM. Fallback routes strictly to `http://127.0.0.1:8088/v1` (`unified-base`).

---

### 3. Benchmark Abstraction (`UNITY` Pointer)
* **The Problem**: Benchmark suites (`test_uber_5x5.py`, `test_vllm_adapter_swap.py`, `test_apollo_vram.py`) currently mix hardcoded model names, raw file paths, and Ollama model strings, causing benchmark comparisons to fail or drift when foundation models change.
* **The Solution**:
  * Benchmarks MUST NOT hardcode model names or local paths.
  * Benchmarks MUST query the abstract pointer string: **`UNITY`**.
  * `UNITY` resolves dynamically via `infrastructure.json` to the current `unified-base`.
  * **Exemption Note**: `test_liger_memory.py` is specifically designed to test Liger kernel transformers against specific model architectures (e.g. `apply_liger_kernel_to_qwen2`) and is **EXEMPT** from the `UNITY` abstraction mandate.

---

### 4. Continuous Live Telemetry vs. Synthetic Offline Scripts
* **The Shift**: Replace isolated, offline synthetic benchmark scripts (which launch standalone models in memory traps) with **Continuous Live Telemetry Harvesting**.
* **The Engine**: Telemetry is harvested directly from Prometheus (`port 9400` / DCGM) and the Attendant Vitals API (`:8000/status`).
* **Operational Metrics Collected**:
  * Turn VRAM delta (MiB allocated / freed per turn)
  * Multi-LoRA adapter swap latency (sub-second target)
  * Real-time prompt throughput (tokens/sec)
  * Host disk swap activity (0 MB enforced ceiling)

---

## 🎯 Actionable Stories (Delegation Specifications — Code-Only)

> [!IMPORTANT]
> **Delegation Rule**: Stories are prepared for **CODE ONLY** execution by OpenAgent. All test validation and silicon gates will be executed on the AGY side after code changes complete.

---

### Story 1: Enforce `unified-base` Single Source of Truth in Ignition & Node Loader
* **Primary Target Files**:
  * `HomeLabAI/src/v5/ignition/manager.py`
  * `HomeLabAI/src/nodes/loader.py`
* **Context Anchors & Reference Files**:
  * `HomeLabAI/config/infrastructure.json` (`model_manifest.unified-base`)
* **Implementation Requirements**:
  1. **Infrastructure Resolver Utility**: Ensure `manager.py` and `loader.py` import and use a centralized `get_unified_base_model()` helper that reads `config/infrastructure.json`.
  2. **Purge Hardcoded Local Fallbacks**: Replace all hardcoded local model fallbacks (`qwen2.5-coder:14b`, `qwen-2.5-1.5b-awq`, `gemma2:2b`) in `manager.py` and `loader.py` with dynamic resolution to `unified-base`.
  3. **Strict KENDER Failover Isolation**: In `manager.py` local failover handling, if Node KENDER (`192.168.1.26:11434`) is offline/unreachable, enforce that local fallback defaults strictly to `http://127.0.0.1:8088/v1` (`unified-base`). **Prohibit any local invocation of 14B models on z87-Linux.**

---

### Story 2: Benchmark Harness Abstraction (`UNITY` Pointer Standard)
* **Primary Target Files**:
  * `HomeLabAI/src/debug/test_uber_5x5.py`
  * `HomeLabAI/src/debug/test_vllm_adapter_swap.py`
  * `HomeLabAI/src/debug/test_apollo_vram.py`
* **Context Anchors & Reference Files**:
  * `HomeLabAI/config/infrastructure.json`
* **Implementation Requirements**:
  1. **Abstract Model Resolution**: Update benchmark scripts to resolve target local model names using the abstract key `UNITY` (reading `infrastructure.json["model_manifest"]["unified-base"]`).
  2. **Purge Hardcoded Model Strings**: Remove explicit model strings (`"qwen..."`, `"llama..."`, raw `/speedy/...` paths) from test argument parsers and default parameters.
  3. **Preserve Liger Exemption**: Maintain explicit architecture tests in `test_liger_memory.py` without modifying its kernel-specific model imports.

---

### Story 3: Continuous Live Telemetry Collector & Prometheus Harvester
* **Primary Target Files**:
  * `HomeLabAI/src/infra/live_telemetry.py` (New File)
  * `HomeLabAI/src/v5/ignition/manager.py`
* **Context Anchors & Reference Files**:
  * `HomeLabAI/docs/LAB_INFRASTRUCTURE.md` (`LAB-007`, `LAB-008`)
* **Implementation Requirements**:
  1. **Telemetry Collector (`live_telemetry.py`)**: Create a lightweight module that queries Prometheus on `http://127.0.0.1:9400` (DCGM GPU metrics) and Foyer status on `http://127.0.0.1:8765/status`.
  2. **Live Metrics Struct**: Extract live VRAM usage, GPU power draw, active LoRA adapter name, and host swap memory usage (`psutil.swap_memory()`).
  3. **Attendant Integration**: Wire `live_telemetry.py` into `manager.py`'s vitals loop so live operational benchmarks are recorded continuously to `field_notes/data/status.json` during active Round Table turns.
