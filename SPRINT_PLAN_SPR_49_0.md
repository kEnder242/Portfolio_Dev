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

### 3. System Integration Test Whitelist (`UNITY` Pointer Standard)
* **The Whitelist Pattern**: Rather than calling out exemptions for legacy experimental tools, we explicitly **whitelist System Integration Tests** that MUST enforce the `UNITY` abstraction pointer.
* **Whitelisted System Integration Tests**:
  1. `HomeLabAI/src/debug/test_uber_5x5.py`
  2. `HomeLabAI/src/debug/test_vllm_adapter_swap.py`
  3. `HomeLabAI/src/tests/test_integration_roundtable.py`
* **Whitelisting Law**: Every whitelisted integration test MUST resolve its local target model dynamically via the abstract key `UNITY` (reading `infrastructure.json["model_manifest"]["unified-base"]`). Hardcoding specific model strings or local disk paths in whitelisted tests is strictly forbidden. Experimental tools outside this whitelist (e.g. kernel/exploration scripts) remain in their own bucket.

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
  2. **Purge Hardcoded Local Fallbacks**: Replace hardcoded local model strings in `manager.py` and `loader.py` with dynamic resolution to `unified-base`.
  3. **Local Fallback Route**: In `manager.py` local failover handling, if Node KENDER (`192.168.1.26:11434`) is offline/unreachable, route local fallback queries to `http://127.0.0.1:8088/v1` (`unified-base`).


---

### Story 2: Whitelisted Integration Test Abstraction (`UNITY` Pointer Standard)
* **Primary Target Files**:
  * `HomeLabAI/src/debug/test_uber_5x5.py`
  * `HomeLabAI/src/debug/test_vllm_adapter_swap.py`
  * `HomeLabAI/src/tests/test_integration_roundtable.py`
* **Context Anchors & Reference Files**:
  * `HomeLabAI/config/infrastructure.json`
* **Implementation Requirements**:
  1. **Abstract Model Resolution**: Update all whitelisted integration scripts to resolve target local model names using the abstract key `UNITY` (reading `infrastructure.json["model_manifest"]["unified-base"]`).
  2. **Purge Hardcoded Model Strings**: Remove explicit model strings (`"qwen..."`, `"llama..."`, raw `/speedy/...` paths) from test argument parsers, default parameters, and payload constructors.
  3. **Whitelisted Scope**: Focus strictly on the whitelisted integration tests; leave standalone experimental tools un-gated in their own bucket.


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

---

## 📜 Pre-Execution Planning & Discovery Ledger (Sprint 49.0 Refinement Log)

> **Purpose**: Document all pre-sprint discoveries, architectural refinements, and prompt payload synchronizations established prior to initiating story delegation.

### 1. Root Cause Forensics & Memory Avalanche Resolution
* **The Incident**: Un-stubbed Story 7 live integration test hit `POST http://localhost:8765/inject`. Node KENDER (Windows RTX 4090) was offline. Foyer triggered local failover, attempting to spin up `qwen2.5-coder:14b` in local Ollama alongside vLLM (`Llama-3.2-3B`), ChromaDB (`:8001`), and NeMo STT.
* **The Forensic Truth**: The 34GB memory demand collapsed local 15GB RAM / 11GB VRAM, thrashing physical disk swap (`/dev/sda5`), swapping out `gnome-shell`, and freezing mouse hardware interrupts.
* **The Architectural Rule**: Local failover on `z87-Linux` is **strictly forbidden** from loading a second foundation model into memory. When KENDER is offline, local fallback routes exclusively to the resident `unified-base` on `127.0.0.1:8088`.

### 2. Dual-Channel Agent Context Architecture ([BKM-041] / [LAB-012])
* **Channel 1 (Automagic Injection)**: ICM (`/home/jallred/.local/bin/icm`) + `BeforeAgent` hook in `settings.json` + `~/.config/icm/config.toml` (`chroma_url = "http://localhost:8001"`). Automagically injects top vector matches into system prompts before every turn.
* **Channel 2 (On-Demand Tool Bridge)**: `clara-dna` FastMCP server (`AcmeLab/src/clara_dna_mcp_server.py`) registered in `~/.gemini/config/mcp_config.json` (AGY) and `HomeLabAI/.opencode.json` (OpenAgent) for exact BKM/FEAT lookups (`get_protocol()`, `query_dna()`).
* **Port 8001 Law**: Port 8001 is ChromaDB. (Port 8000 is Prometheus RAPL Exporter). All vector embedding functions and HTTP clients connect exclusively to `:8001`.

### 3. Prompt Payload Simplification & Single Source of Truth
* **Prompt Clutter Elimination**: Removed 35+ lines of redundant negative constraint roleplay (`MUST NOT DO`, `task() roleplay`) from `OPENAGENT_HANDOVER_PLAYBOOK.md` and `delegate.py`.
* **Programmatic Code Source of Truth**: [`HomeLabAI/src/tests/delegate.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/tests/delegate.py#L165) (lines 165–174) is designated as the single programmatic code source of truth for the live delegation prompt payload sent over REST.
* **System Integration Test Whitelist Pattern**: Replaced ad-hoc script exemptions with an explicit **System Integration Test Whitelist** (`test_uber_5x5.py`, `test_vllm_adapter_swap.py`, `test_integration_roundtable.py`) that MUST enforce the `UNITY` abstraction pointer. Standalone experimental tools remain un-gated in their own bucket.

