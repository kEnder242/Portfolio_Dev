# 📑 SPRINT PLAN 110.0: Dual-GPU Heterogeneous 27GB VRAM Engine & Unified Trust Boundary

**Sprint ID:** `SPR_110_0`  
**Theme:** Full Conversational Roll-Up: Heterogeneous Multi-GPU Layer Splitting (Option A: 27GB Pooled VRAM via `llama.cpp` Vulkan Multi-Device), Zero-Downtime CUDA Fallback Architecture, Format-Agnostic LLM Intake Guardrails, Empirical Litmus Leak Probe (`INS-052`), Retroactive Secrets Scrub & Airlock Push, Balanced Sparse Intake Cadence with Foyer Intercom Preemption (`FEAT-416`), and Operational Hardware QSV Certification.  
**Status:** 🟢 **COMPLETE (VERIFIED)**  
**Parent Frameworks:**
- [`BKM-086`]: The Paved-Path Sprint Protocol (AFK / Sovereign Execution)
- [`BKM-088`]: The Empirical Pipeline Step Judgment Protocol (Micro-Harness & Benchmark Gauntlet)
- [`BKM-077`]: Conversational Anchor Tracking Protocol (Strict 1:1 Numbered Swim Lanes)
- [`BKM-081`]: Pre-Flight Mistakes Avoided Ledger
- [`BKM-082`]: 5-Sprint Historical Lookback & Mistake Prevention
- [`BKM-015`]: Semantic Anchor Protocol (Anti-Hardcoding & Regex Governance)
- [`BKM-024`]: Live Silicon Probe Protocol
- [`FEAT-416`]: Strict Nightly Refinement Isolation (02:00–05:00 AM)
- [`FEAT-600`]: Grounding Protocol & Dropped Threads Ledger
- [`INS-052`]: The Litmus Leak Test & Unified Trust Boundary (Prompt Verification via Controlled Occlusion)
- [`INS-047`]: Live is King, History is Queen (Anti-Amnesia Sovereign Dyad)

**Target Silicon Nodes:**
- `Slot 1 (PCIe 03:00.0)`: Intel Arc B580 (16GB ReBAR, `card0`, `renderD129`, Vulkan GPU0, HDMI display)
- `Slot 2 (PCIe 05:00.0)`: NVIDIA GeForce RTX 2080 Ti (11GB, `card2`, `renderD130`, Vulkan GPU1, headless CUDA)
- `vLLM Daemon`: Port 8088 / 8000 (Pure CUDA fallback)
- `Foyer Daemon`: Port 8765 (WebSocket Intercom Preemption Signal)
- `Jellyfin Service`: Port 8096 (Arc B580 QSV HW Accel)

---

## 🛑 Pre-Flight Checklist Gate (`BKM-082 §GATE` / `BKM-086 §1.1`)
- [x] **1. 5-Sprint Lookback**: Reviewed SPR-105 through SPR-109 for traps, sentinels, and regression vectors (`BKM-082 §2.1` in §0.1).
- [x] **2. Mistakes-Avoided Ledger**: Enumerated 6 concrete historical mistakes avoided (`BKM-082 §2.4` in §0.2).
- [x] **3. Oracle Review**: Adversarial architecture review completed via `ask_oracle` and documented with 4 mandatory safeguards in [`ORACLE_REVIEW_SPRINT_110.md`](file:///home/jallred/Dev_Lab/Portfolio_Dev/docs/sprints/active/ORACLE_REVIEW_SPRINT_110.md).
- [x] **4. Delegation Justification**: Evaluated per operator mandate: **Local delegation to Atlas (`[SWARM:LOCAL]`) is explicitly waived and forbidden due to multi-card driver boundary risks.** All tasks assigned to `[AGY:PRIMARY]`.
- [x] **5. Risk Assessment**: Evaluated negative prompting failure on 3B models, driver stack collisions, socket preemption flapping, service lockouts, and submodule desync. Concrete mitigations embedded in stories.

---

## 🛡️ Pre-Flight Mistakes Avoided Ledger (`BKM-081` / `BKM-082`)

| Historical Trap | Prior Incident | Sprint 110 Mitigation |
| :--- | :--- | :--- |
| **1. The Negative Prompting Blindness Trap** | Sprint 64: 3B models ignoring negative instructions ("never output X") | Reframe prompt positively: prune `career_timeline` from raw log taxonomy, instruct machine-only extraction, and provide 1-shot contrastive redaction demonstration. |
| **2. The Hardcoded Evaluation Leak Trap** | Sprint 106: Prompt authoring hardcoded specific regex matches into model instructions | Under `BKM-015` and `INS-052`, prompt remains 100% format-agnostic; hardcoded sentinels exist strictly in the out-of-band litmus evaluator. |
| **3. The Flapping Preemption Trap** | Sprint 64: Periodic healthchecks causing race conditions on locks | Use established socket state queries (`ss -t state established '( sport = :8765 )'`) with 60-second backoff rather than volatile un-debounced lock files. |
| **4. The Driver Stack Collision Trap** | Sprint 108: Conflicting torch versions between venvs (`torch 2.11` vs `2.8`) | Isolate build to `/home/jallred/hybrid_engine/llama.cpp` using Vulkan 1.4, which exposes both Arc B580 and RTX 2080 Ti natively with zero driver conflicts. |
| **5. The Lockout Fallback Trap** | Sprint 77: Crashing experimental inference engine orphaned all LLM callers | Implement `serve_llm.sh --mode=[hybrid|cuda]` with automated healthcheck fallback to `vLLM` within 5 seconds. |
| **6. The Submodule Desync Trap** | Sprint 93: Amending commits in child submodule leaves parent git pointer dirty | Ensure `Dev_Lab` immediately commits the updated `www_deploy` submodule hash after push. |

---

## ⚖️ Gem Balancing Architecture (User Request 1.2)

| Gem Flow | Cadence | Chunk Volume | Target Execution Window | Preemption & Resource Policy |
| :--- | :--- | :--- | :--- | :--- |
| **1. Nibbler** (`nibble_v2.py`) | Every 15 min | 1–2 chunks max | Continuous background (sparse) | **Instant yield** if Foyer WS `:8765` active or CPU load > 4.0 |
| **2. Refinement** (`refine_gem.py`) | Nightly only | Batch accumulated | **02:00 – 05:00 AM** (`FEAT-416`) | Quiescent during daytime Lean Sleep (`--force` override) |
| **3. Dreaming** (`dream_cycles.py`) | Nightly only | Consolidated passes | **04:00 – 05:30 AM** (`FEAT-101`) | Quiescent during daytime Lean Sleep |

---

## 📋 Sprint Stories & 4-Anchor Execution (1:1 Roll-Up)

### Story 110.1: LLM Extraction Prompt Guardrails (`BKM-015` / `BKM-089` / `INS-052`)
* **Objective**: Formulate format-agnostic prompt exclusion rules in `nibble_v2.py` preventing extraction of API keys, credentials, passwords, serial numbers, and managerial focal feedback.
* **Owner**: `[AGY:PRIMARY]`
* **Tasks**:
  - [x] Task 110.1.1: Prune `career_timeline` from raw log taxonomy to eliminate focal review capture vectors.
  - [x] Task 110.1.2: Add positive machine-execution boundary (`[CREDENTIAL & SECRET BOUNDARY - BKM-015 / INS-052]`) to `nibble_v2.py`.
  - [x] Task 110.1.3: Add performance/focal review exclusion clause (`[PERFORMANCE & FOCAL EXCLUSION - INS-052]`).
* **Anchor 1 (Target Files & Line Numbers)**:
  - `Portfolio_Dev/field_notes/nibble_v2.py:495-535`
* **Anchor 2 (Verification Command)**:
  ```bash
  python3 -c "from field_notes.nibble_v2 import scrub_input_buffer; print('Scrubber loaded cleanly')"
  ```
* **Anchor 3 (Verbatim Code Specs)**:
  - Sanitization clause: *"Never extract or preserve private authentication tokens, API keys, bearer tokens, passwords, secrets, or hardware serial numbers..."*
  - Focal clause: *"Exclude all personal performance ratings, manager appraisals, focal feedback, self-assessment scoring..."*
* **Anchor 4 (DNA Links)**: `[BKM-015]`, `[BKM-089]`, `[INS-052]`

---

### Story 110.2: Empirical Secrets & Focal Litmus Probe (`INS-052` / `BKM-088`)
* **Objective**: Build and execute a dedicated empirical probe (`probe_secret_and_focal_leak_test.py`) that uses hardcoded sentinels as an out-of-band canary while keeping the prompt format-agnostic.
* **Owner**: `[AGY:PRIMARY]`
* **Tasks**:
  - [x] Task 110.2.1: Author `Portfolio_Dev/field_notes/probe_secret_and_focal_leak_test.py` with test payload containing JFrog curl key, root password, chassis serial, and focal rating.
  - [x] Task 110.2.2: Implement out-of-band regex canary evaluators (`LITMUS_PATTERNS`).
  - [x] Task 110.2.3: Execute probe live against local engine and record failure modes / calibration deltas.
* **Anchor 1 (Target Files & Line Numbers)**:
  - `Portfolio_Dev/field_notes/probe_secret_and_focal_leak_test.py`
* **Anchor 2 (Verification Command)**:
  ```bash
  python3 /home/jallred/Dev_Lab/Portfolio_Dev/field_notes/probe_secret_and_focal_leak_test.py
  ```
* **Anchor 3 (Verbatim Code Specs)**:
  - Sentinels: `AKCp8[A-Za-z0-9]{15,}`, `SuperSecretP@ssw0rd!`, `SN: J38928492048`, `Rating: Successful`
  - Control assertion: Valid technical log (`setpci -s 03:00.0 ... ReBAR`) must be preserved.
* **Anchor 4 (DNA Links)**: `[INS-052]`, `[BKM-088]`, `[BKM-015]`

---

### Story 110.3: Retroactive Lakehouse Data Scrub & `www_deploy` Remote Push
* **Objective**: Remove leaked JFrog tokens from historical lakehouse JSONs, amend commit `9bfbcfb`, pass GitHub Push Protection, and sync parent submodule pointer.
* **Owner**: `[AGY:PRIMARY]`
* **Tasks**:
  - [x] Task 110.3.1: Execute regex scrub replacing `AKCp8...` with `[REDACTED_JFROG_API_KEY]` across all `data/*.json`.
  - [x] Task 110.3.2: Verify zero token occurrences remain via ripgrep/grep.
  - [x] Task 110.3.3: Amend commit `9bfbcfb` in `www_deploy` and push cleanly to `origin/main`.
  - [x] Task 110.3.4: Commit updated submodule pointer in `Dev_Lab` (`5aaec11`).
* **Anchor 1 (Target Files & Line Numbers)**:
  - `www_deploy/data/queue.json`
  - `www_deploy/data/2023.json`
  - `www_deploy/data/public_benchmarks.json`
  - `Portfolio_Dev/field_notes/data/*.json`
  - `Dev_Lab/www_deploy` (Submodule)
* **Anchor 2 (Verification Command)**:
  ```bash
  grep -rnE "AKCp8[A-Za-z0-9]{20,}" /home/jallred/Dev_Lab/www_deploy/data/ /home/jallred/Dev_Lab/Portfolio_Dev/field_notes/data/
  ```
  *(Expected: Zero matches)*
* **Anchor 3 (Verbatim Code Specs)**:
  - `git -C /home/jallred/Dev_Lab/www_deploy commit --amend --no-edit`
  - `git -C /home/jallred/Dev_Lab/www_deploy push origin main`
* **Anchor 4 (DNA Links)**: `[INS-052]`, `[BKM-009]`, `[BKM-020]`

---

### Story 110.4: Gem Balancing & Sparse Ingestion Cadence with Preemption
* **Objective**: Re-tune `nibble_v2.py` to regular 15-minute sparse cadence (default `limit=2` chunks), enforce nightly-only quarantine for `refine_gem.py` ([FEAT-416]), and implement Foyer intercom socket preemption.
* **Owner**: `[AGY:PRIMARY]`
* **Tasks**:
  - [x] Task 110.4.1: Implement `check_foyer_intercom_active()` checking established TCP sockets on `:8765`.
  - [x] Task 110.4.2: Integrate socket preemption into `should_yield()` in `nibble_v2.py`.
  - [x] Task 110.4.3: Set default `limit=2` and remove blanket daytime block in `nibble_v2.py`.
  - [x] Task 110.4.4: Add `--force` and `FEAT-416` daytime suppression to `refine_gem.py`.
* **Anchor 1 (Target Files & Line Numbers)**:
  - `Portfolio_Dev/field_notes/nibble_v2.py:78-115, 380-410`
  - `Portfolio_Dev/field_notes/refine_gem.py:965-995`
* **Anchor 2 (Verification Command)**:
  ```bash
  cd /home/jallred/Dev_Lab/Portfolio_Dev && python3 -c "from field_notes.nibble_v2 import check_foyer_intercom_active; print('Intercom check:', check_foyer_intercom_active())" && python3 field_notes/refine_gem.py
  ```
  *(Expected: False returned for intercom; refine_gem prints daytime suppressed)*
* **Anchor 3 (Verbatim Code Specs)**:
  - Socket probe: `ss -t state established '( sport = :8765 or dport = :8765 )'`
  - Window: 02:00–05:00 AM nightly.
* **Anchor 4 (DNA Links)**: `[FEAT-416]`, `[FEAT-101]`, `[BKM-086]`

---

### Story 110.5: Jellyfin Arc B580 QSV & Steam Remote Play Certification
* **Objective**: Validate that Jellyfin hardware transcoding on Arc B580 QSV remains operational with fallback stanzas preserved, and confirm display server routing for Steam Remote Play.
* **Owner**: `[AGY:PRIMARY]`
* **Tasks**:
  - [x] Task 110.5.1: Verify Jellyfin container running on `/dev/dri/renderD129` with `DeviceID: e20b/1`.
  - [x] Task 110.5.2: Verify Mazui ASS subtitle burn-in runs at 73 fps (2.98x real-time).
  - [x] Task 110.5.3: Ensure commented NVIDIA container reservations remain intact in `docker-compose.yml`.
  - [x] Task 110.5.4: Confirm Steam Remote Play routes via primary Arc HDMI adapter (`card0`).
* **Anchor 1 (Target Files & Line Numbers)**:
  - `Dev_Lab/Jellyfin-Server/docker-compose.yml`
  - `/var/lib/jellyfin-data/config/config/encoding.xml`
* **Anchor 2 (Verification Command)**:
  ```bash
  docker ps --filter "name=jellyfin" --format "{{.Status}}" && vpl-inspect | grep -i "DeviceID"
  ```
  *(Expected: Container Up healthy, B580 visible in oneVPL)*
* **Anchor 3 (Verbatim Code Specs)**:
  - Device path: `/dev/dri/renderD129`
  - `EnableVppTonemapping=true`, `AllowAv1Encoding=true`
* **Anchor 4 (DNA Links)**: `[BKM-024]`, `[INS-047]`

---

### Story 110.6: Multi-Backend Hybrid Inference Engine (Option A: 27GB Pooled VRAM)
* **Objective**: Build and deploy `llama.cpp` supporting heterogeneous layer splitting across NVIDIA RTX 2080 Ti (11GB) and Intel Arc B580 (16GB) via Vulkan 1.4 multi-device backend, with instantaneous toggle fallback to pure CUDA `vLLM`.
* **Owner**: `[AGY:PRIMARY]`
* **Tasks**:
  - [x] Task 110.6.1: Document historical Intel+NVIDIA compatibility layer (Codeplay DPC++, oneCCL, ZLUDA).
  - [x] Task 110.6.2: Install Vulkan development headers (`libvulkan-dev`, `glslc`, `spirv-headers`, `glslang-tools`).
  - [x] Task 110.6.3: Clone and compile `llama.cpp` with `-DGGML_VULKAN=ON` (`llama-cli`, `llama-server`, `llama-bench`).
  - [x] Task 110.6.4: Author unified launcher `/home/jallred/serve_llm.sh` with automated healthcheck fallback to CUDA.
* **Anchor 1 (Target Files & Line Numbers)**:
  - `/home/jallred/hybrid_engine/llama.cpp/build_vulkan/bin/llama-server`
  - `/home/jallred/serve_llm.sh`
* **Anchor 2 (Verification Command)**:
  ```bash
  /home/jallred/serve_llm.sh --test
  ```
  *(Expected: All silicon endpoints GPU0 Arc B580 and GPU1 RTX 2080 Ti verified healthy)*
* **Anchor 3 (Verbatim Code Specs)**:
  - Vulkan device split: `-dev "0,1" -sm layer -ts 16,11 -ngl 99`
  - Fallback: `systemctl restart vllm.service`
* **Anchor 4 (DNA Links)**: `[BKM-088]`, `[INS-047]`

---

### Story 110.7: Empirical Throughput & Latency Benchmark Gauntlet (`BKM-088`)
* **Objective**: Execute an empirical benchmark gauntlet comparing pure CUDA (RTX 2080 Ti) vs hybrid pooled VRAM (RTX 2080 Ti + Arc B580), recording TTFT, tok/s, and physical memory footprint.
* **Owner**: `[AGY:PRIMARY]`
* **Tasks**:
  - [x] Task 110.7.1: Author `Portfolio_Dev/field_notes/benchmark_hybrid.py` measuring TTFT, tokens/sec, and dual VRAM.
  - [x] Task 110.7.2: Execute benchmark across short (32 tokens) and standard (256 tokens) workloads.
  - [x] Task 110.7.3: Persist telemetry into `Portfolio_Dev/field_notes/data/hybrid_benchmark_results.json`.
* **Anchor 1 (Target Files & Line Numbers)**:
  - `Portfolio_Dev/field_notes/benchmark_hybrid.py`
  - `Portfolio_Dev/field_notes/data/hybrid_benchmark_results.json`
* **Anchor 2 (Verification Command)**:
  ```bash
  python3 /home/jallred/Dev_Lab/Portfolio_Dev/field_notes/benchmark_hybrid.py
  ```
  *(Expected: Benchmark JSON persisted with latency and throughput metrics)*
* **Anchor 3 (Verbatim Code Specs)**:
  - Metrics: `ttft_ms`, `tokens_per_second`, `cuda_vram_mb`, `arc_vram_mb`
* **Anchor 4 (DNA Links)**: `[BKM-088]`, `[BKM-024]`

---

### Story 110.8: Cross-Card Speculative Decoding & Qwen 3.5 / 3.8 Characterization
* **Objective**: Benchmark Qwen 3.8 27B across dual-GPU Vulkan layer-split, incorporate Qwen 3.5 Instruct lineage from M5 Air / Kender historical baselines, and evaluate Heterogeneous Speculative Decoding (Arc B580 Target + RTX 2080 Ti Fast Predictor).
* **Owner**: `[AGY:PRIMARY]`
* **Tasks**:
  - [x] Task 110.8.1: Download and benchmark `Qwen3.8-27B-UD-Q4_K_M.gguf` under `Vulkan1/Vulkan0` (RTX 2080 Ti first).
  - [x] Task 110.8.2: Compare 27B throughput directly against 32B (10.0 tok/s) and M5 Air / RTX 4090 historical baselines.
  - [x] Task 110.8.3: Formulate and benchmark Heterogeneous Speculative Decoding architecture (Arc B580 16GB Target + RTX 2080 Ti Draft Predictor).
  - [x] Task 110.8.4: Persist speculative decoding and 27B telemetry to `hybrid_benchmark_results.json`.
  - [x] Task 110.8.5: Zero-Downtime Waterfall Drop-In: Deploy `llama-server` on port 8088 with `--alias unified-base`, verify live chat completions, and preserve instant CUDA fallback.
* **Anchor 1 (Target Files & Line Numbers)**:
  - `/speedy/models/gguf/Qwen3.8-27B-UD-Q4_K_M.gguf`
  - `Portfolio_Dev/field_notes/data/hybrid_benchmark_results.json`
* **Anchor 2 (Verification Command)**:
  ```bash
  /home/jallred/hybrid_engine/llama.cpp/build_vulkan/bin/llama-bench -m /speedy/models/gguf/Qwen3.8-27B-UD-Q4_K_M.gguf -dev Vulkan1/Vulkan0 -sm layer -ts 11/16 -ngl 99 -p 64 -n 32
  ```
  *(Expected: 100% VRAM offload, zero CPU layers, tok/s > 11.5)*
* **Anchor 3 (Verbatim Code Specs)**:
  - Model: `Qwen3.8-27B-UD-Q4_K_M.gguf` ($15.33\text{ GiB}$)
  - Speculative Topology: Target on `Vulkan0` (Arc B580), Draft on `Vulkan1` (RTX 2080 Ti)
* **Anchor 4 (DNA Links)**: `[BKM-088]`, `[FEAT-501]`, `[LAB-115]`, `[LAB-117]`

---

### Story 110.9: Pure 3.7-Flash Speculative Sweet Spot, Memory Safety & LAB Field Note (`[BKM-079]`)
* **Objective**: Codify the pure intra-family `Qwen 3.7-Flash` pairing (Target: 8B on Arc B580 Vulkan1 vs Draft Predictor: 4B on RTX 2080 Ti Vulkan0) with restored `Q4_0` KV cache, enforce host RAM protection via `--no-mmap` to defeat `systemd-oomd`, resolve feasibility of draft model deconstruction, and author production LAB entry `FN-SPEC-DECODE-HETEROGENEOUS-2026-11`.
* **Owner**: `[AGY:PRIMARY]`
* **Tasks**:
  - [x] Task 110.9.1: Empirical benchmark of Qwen 3.7-Flash 4B draft model standalone on RTX 2080 Ti ($1,435.21\text{ t/s}$ prefill, $76.34\text{ t/s}$ generation).
  - [x] Task 110.9.2: Complete root-cause forensic analysis of host RAM saturation under 16GB RAM during dual-model loading; resolve via `--no-mmap` in `/home/jallred/serve_llm.sh`.
  - [x] Task 110.9.3: Assess feasibility of standalone predictor access during speculative serving; establish architectural decision to treat `llama-server` as a single, fast, opaque drop-in on port 8088.
  - [x] Task 110.9.4: Author LAB entry `Portfolio_Dev/field_notes/HETEROGENEOUS_SPECULATIVE_DECODING_SWEET_SPOT.md` (`FN-SPEC-DECODE-HETEROGENEOUS-2026-11`).
  - [x] Task 110.9.5: Codify Backlog item for PyTorch CUDA LoRA training offload to Kender (RTX 4090) vs local GGUF quantization.
* **Anchor 1 (Target Files & Line Numbers)**:
  - `/home/jallred/serve_llm.sh#L52-L89`
  - `Portfolio_Dev/field_notes/HETEROGENEOUS_SPECULATIVE_DECODING_SWEET_SPOT.md`
  - `HomeLabAI/config/infrastructure.json#L4-L28`
* **Anchor 2 (Verification Command)**:
  ```bash
  /home/jallred/hybrid_engine/llama.cpp/build_vulkan/bin/llama-bench -m /speedy/models/gguf/Qwen3.7-Flash-4B-Q8_0.gguf -dev Vulkan0 -ngl 99 -p 64 -n 32
  ```
  *(Expected: tg32 > 70 tok/s on RTX 2080 Ti, zero cross-card layer splitting)*
* **Anchor 3 (Verbatim Code Specs)**:
  - Speculative Topology: Target 8B on Arc B580 (`Vulkan1`), Draft 4B on RTX 2080 Ti (`Vulkan0`), `--no-mmap`, `--spec-draft-n-max 4`, `-ctk q4_0 -ctv q4_0`
  - Drop-in Port: 8088 (`--alias unified-base`)
* **Anchor 4 (DNA Links)**: `[BKM-079]`, `[BKM-086]`, `[FEAT-586]`, `[INS-047]`

---

## 🧭 Phase 2: Engine Thinking Suppression & Just-In-Time Bedrock Decoupling

### 📖 Live Tracked Conversational Narrative Preamble (`[BKM-077]` / `[BKM-097]` / `[INS-047]`)

> **Executive Context & Forensic Discovery (2026-11-05 Morning Accountability Gauntlet):**
> During the synthetic 06:00 AM round table probe (`bff308bb`: *"Audit active silicon residency and memory topology"*), the M5 Air Bonsai-27B Judge slammed Pinky with a terminal **`0.0 / 1.0`** evaluation. Forensic investigation revealed a critical multi-layer failure chain that tracked back to two core architectural root causes:
>
> 1. **The "Turn Off Thinking" Engine Regression:**
>    - *Incident:* Port 8088 (`llama-server` on RTX 2080 Ti running `Qwen3.7-Flash-8B-Q8_0.gguf`) returned an empty string (`""`, TTFT: 0.0ms) on local triage.
>    - *Root Cause:* `_dispatch_vllm_triage()` bounded the call to `max_tokens: 128`. Because `llama-server` defaulted to auto-reasoning (`reasoning_format: deepseek`), Qwen3.7 spent all 128 tokens inside its `<think>` scratchpad (665 characters of thought) and reached `finish_reason: length` before emitting a single token of JSON `content`.
>    - *Historical Lookback:* Across **SPR-100**, **SPR-103**, and **SPR-108 (`[FEAT-680]` / `[BKM-079]`)**, the lab repeatedly fought the "Prompt-Persuasion Fallacy" on reasoning models (discovering Ollama required root `"think": false`, OpenAI/oMLX required `extra_body: {"reasoning": 0, "enable_thinking": False}`, and LiteLLM required gateway-level parameter transformation). When `llama-server` was introduced in Sprint 110 as a "drop-in" vLLM replacement, we omitted `--reasoning off` / `--reasoning-budget 0` from `serve_llm.sh`. The DNA correctly flagged reasoning suppression in past sprints, but the new Vulkan engine CLI surface was not calibrated to match.
>
> 2. **Verification of Triage Backpressure:**
>    - *Result:* `_is_valid_triage()` in `speculative_triage.py` properly rejected the empty local triage result, kept waiting, and safely fell back to Deep Thought on the M5 Air, which correctly classified the query as `vibe: OPERATIONAL`, `domain: exp_tlm`. Triage backpressure and fallback worked as designed.
>
> 3. **Career Bedrock Static Leak vs Just-In-Time Context (JITC):**
>    - *Incident:* Even though the backup triage judged the query as `OPERATIONAL` and the Hub successfully blocked ChromaDB RAG (`[FEAT-657] Zero RAG: empty search terms`), the models hallucinated that our consumer Z87 Haswell motherboard was running Intel enterprise server BMC firmware, DCMI interfaces, and Purley RAS validation scripts.
>    - *Root Cause:* In `src/nodes/loader.py`, `[CAREER_COMPASS_BEDROCK]` (Jason's 2005–2024 validation career timeline) is permanently baked into `self.IDENTITY_BEDROCK` on *every single node* during initialization. When `resolve_hyde_vector` invoked Pinky's Stage 2 reflex take, Pinky latched onto the BMC/DCMI text in the static system prompt. The Hub stamped this into `[PINKY_STANCE]` and passed it downstream to Brain and Deep Thought, completely circumventing the `OPERATIONAL` RAG barrier.
>    - *Resolution:* Decouple `[CAREER_COMPASS_BEDROCK]` from the static node system prompt. Leverage the existing triage policy rules (`triage_policy.json` / `FEAT-673`) to inject career bedrock strictly as Just-In-Time Context (JITC) when `vibe == "HISTORICAL"` or `domain in ("work_history", "career", "lab_history")`. When `OPERATIONAL` or `CASUAL`, career history is completely omitted.

#### 💬 Tracked Dialogue Reconciliation by Numbered Swim Lane (`[BKM-077] §4`)

##### 1) Swim Lane 1: `llama-server` Native Reasoning Suppression & Live Micro-Harness
* **User Directive**: Use historical sprint knowledge to architect an effective way to disable thinking natively on the engine, test it live rapidly, and avoid inventing unvetted solutions.
* **Technical Agreement**: Pass native CLI flags `--reasoning off` and `--reasoning-budget 0` directly into `/home/jallred/serve_llm.sh`. Verify live on port 8088 using a curl/urllib micro-harness confirming non-empty triage JSON in $< 500\text{ms}$.

##### 1.1) Swim Lane 1.1: Token Clamping vs Continuous Fuel Pacing (`[FEAT-523]`)
* **User Directive**: Review how and why hard limits were removed for soft limits. Did we regress?
* **Technical Agreement**: Yes, `max_tokens: 128` in `_dispatch_vllm_triage()` was an ad-hoc hardcoded guillotine clamp that regressed the principles of `[FEAT-523]` (Continuous Fuel Pacing). We will raise the safety token floor to 350 while maintaining prompt-driven soft pacing, allowing non-reasoning structured triage to complete cleanly without truncation.

##### 1.2) Swim Lane 1.2: Strategic Oracle Review & Engine Architecture Fallback (`[BKM-079]` / `[INS-052]`)
* **User Directive**: Consult the Strategic Delegation Oracle, connect its recommendations to documentation, and maintain the instant fallback to pure CUDA vLLM.
* **Technical Agreement**: Consult Tier 1 Oracle (`ask_oracle`). Retain the dual-backend architecture in `serve_llm.sh` (`--fallback-cuda` / `systemctl restart vllm.service`). Anchor the suppression at the engine/gateway boundary, upholding `[BKM-079]`.

##### 3) Swim Lane 3: Career Bedrock Decoupling into JITC with Byte-Parity Verification (`[FEAT-434]` / `[FEAT-075]` / `[BKM-023]`)
* **User Directive**: Move `CAREER_COMPASS_BEDROCK` to conditional JITC. Include an explicit task confirming moved text is NOT paraphrased (anti-paraphrasing check via exact variable reuse or pre/post diff).
* **Technical Agreement**: Remove `[CAREER_COMPASS_BEDROCK]` from static `self.IDENTITY_BEDROCK` in `src/nodes/loader.py`. Export it as an immutable constant and inject it strictly via `cognitive_hub.py` when triage domain/vibe matches historical career queries. Enforce a cryptographic/string byte-parity check (`assert new_bedrock == original_bedrock`) satisfying `[FEAT-075]` and `[BKM-023]`.

##### 4 & 5) Swim Lane 4 & 5: Live Test Harness, Dirty Lab Gate (`[FEAT-524]`) & Antigravity MO Out-of-Band Judge (`[BKM-089]` / `[BKM-090]`)
* **User Directive**: Mock has its place, but live tests are essential. Ground on dirty lab pre-flight failure gates (never test stale RAM). Antigravity must act as the out-of-band evaluator judging probe coherence against 'MO' (Modus Operandi) criteria for unknown regressions.
* **Technical Agreement**: Author Story 110.12. Assert `dirty: false` on `http://127.0.0.1:8765/status` prior to live verification. If code changes, enforce `systemctl restart lab-attendant.service` before running live probes (`[FEAT-524]`). Antigravity evaluates probe outputs out-of-band against Prompt MO rubrics (`BKM-089` / `BKM-090`) to verify end-to-end semantic coherence.

---

### 🗺️ Authoritative `ANCHOR_TRACK` Reconciliation Table (`[BKM-097]` / `[BKM-077]`)

| Anchor # | User Origin Prompt & Topic | Technical Architecture Agreed | Sprint Story / Target | Status |
| :---: | :--- | :--- | :--- | :---: |
| **1** | Turn off thinking natively on `llama-server` & rapid test | Pass `--reasoning off` / `--reasoning-budget 0` in `serve_llm.sh`; micro-harness verification | Story 110.10 | `DONE` |
| **1.1** | Soft limits vs hard token clamps (`max_tokens: 128` regression) | Raise triage token floor to 350, align with `FEAT-523` continuous fuel pacing | Story 110.10 | `DONE` |
| **1.2** | Consult Strategic Oracle, connect to docs, preserve vLLM fallback | Tier 1 Oracle review, engine-level suppression (`BKM-079`), instant CUDA fallback | Story 110.10 | `DONE` |
| **3** | Decouple Career Bedrock into JITC with anti-paraphrasing check | Remove from static node init in `loader.py`; conditional JITC in `cognitive_hub.py`; 100% byte-parity test | Story 110.11 | `DONE` |
| **4** | Live testing vs mocks; Dirty Lab Pre-Flight Gate (`FEAT-524`) | Pre-flight daemon check (`GET /status`), daemon restart on code edits, live silicon probe gate | Story 110.12 | `DONE` |
| **5** | Antigravity judge role under 'MO' criteria for unknown regressions | Out-of-band semantic probe evaluation against Prompt MO rubrics (`BKM-089` / `BKM-090`) | Story 110.12 | `DONE` |

---

### 🛡️ Pre-Flight Mistakes Avoided Ledger (`[BKM-081]` / `[BKM-082]`)

1. **Mistake Avoided: Prompt-Persuasion Fallacy (`[BKM-079]`)**: We will NOT attempt to disable thinking by adding `"Do not think"` to the triage system prompt. Reasoning suppression is enforced natively at the `llama-server` CLI boundary.
2. **Mistake Avoided: The Green Lie Trap (`[BKM-070]` / `[BKM-088]`)**: We will NOT accept unit tests mocking the LLM as proof of reasoning suppression. Certification requires hitting the running `llama-server` on port 8088.
3. **Mistake Avoided: The Dirty Lab Bytecode Trap (`[FEAT-524]`)**: We will NOT execute live probes against stale Python bytecode in daemon RAM. Any edits to `loader.py` or `cognitive_hub.py` mandate a clean `systemctl restart lab-attendant.service` before live probing.
4. **Mistake Avoided: The Paraphrasing Drift (`[FEAT-075]` / `[BKM-023]`)**: We will NOT re-type, re-word, or summarize the `[CAREER_COMPASS_BEDROCK]` text during relocation. Exact string byte-equality will be enforced.
5. **Mistake Avoided: The Prompt MO Asymmetry Trap (`[BKM-089]`)**: We will NOT bloat the runtime JITC prompt with meta-explanations of *why* the career bedrock was conditionally injected. The prompt explains HOW; the out-of-band MO harness evaluates WHY.

---

### 🛑 Pre-Flight Checklist Gate (`[BKM-086]` / AFK Sprint)

- [x] **Pillar 1: Explicit Grounding & Pre-Regression Archaeology (`[BKM-082]`, `[BKM-085]`)**
  - [x] Conducted 5-sprint historical lookback (SPR-100 Ollama `think: false`, SPR-103 oMLX `extra_body`, SPR-108 `[FEAT-680]` LiteLLM translation, SPR-109, SPR-110).
  - [x] Documented Pre-Flight Mistakes Avoided Ledger (`BKM-081`).
- [x] **Pillar 2: Deterministic 4-Anchor Planning & Parity Verification (`[BKM-030]`, `[BKM-043]`)**
  - [x] Anchor 1: Target Files & Line Numbers specified for all stories.
  - [x] Anchor 2: Concrete Verification Commands authored for all stories.
  - [x] Anchor 3: Verbatim Code Specifications declared.
  - [x] Anchor 4: Concrete DNA Links mapped.
  - [x] Anti-Paraphrasing Byte-Parity Mandate verified (`FEAT-075` / `BKM-023` baseline hash `10bbbf8e107428a11d510be0bb637b9a0a65c58141f8ac773c7bf57adf27428b` captured).
- [x] **Pillar 3: Structured Delegation & Anti-Bypass Guard (`[BKM-049]`, `[BKM-006]`)**
  - [x] Evaluated Swarm Delegation: Systemd launcher scripts, daemon lifecycles, and core hub stage prompts assigned to `[AGY:PRIMARY]` with explicit architectural justification.
- [x] **Pillar 4: Adversarial Audit & Silicon Certification (`[BKM-007]`, `[BKM-024]`, `[INS-047]`, `[INS-010]`)**
  - [x] Run Pre-Flight Cloud Oracle adversarial audit via `delegate.py --oracle` (Completed in `ORACLE_REVIEW_SPRINT_110.md`).
  - [x] Verify Dirty Lab Pre-Flight Gate (`FEAT-524`): Verified clean (`dirty: false`, `state: OPERATIONAL`, `boot_commit: ada017a`).
  - [x] Live is King Physical Daemon Certification (`BKM-024`, `INS-047`): Synthetic accountability probe passed on physical silicon (Bonsai score 0.95 / 1.0).
  - [x] Antigravity MO Out-of-Band Evaluation (`BKM-089`, `BKM-090`): Verified semantic coherence, zero BMC/DCMI hallucinations, pure NVML residency telemetry.

---

### Story 110.10: `llama-server` Native Reasoning Suppression & Triage Token Floor (`[BKM-079]` / `[FEAT-680]`)
* **Objective**: Ensure the local `llama-server` engine on port 8088 suppresses reasoning tokens by default during fast structured utility calls, eliminating empty triage completions, aligning with `[FEAT-523]` continuous soft limits, and enforcing dual-layer suppression per Cloud Oracle review.
* **Owner**: `[AGY:PRIMARY]`
* **Tasks**:
  - [x] Task 110.10.1: Update `/home/jallred/serve_llm.sh` launcher to pass `--reasoning off` and `--reasoning-budget 0` across devices by default, preventing unexpected `<think>` generation during API serving.
  - [x] Task 110.10.2: Update `_dispatch_vllm_triage()` in `cognitive_hub.py` to raise `max_tokens` from 128 to 350 as a safety floor, and ensure `extra_body: {"reasoning": 0, "enable_thinking": False}` is forwarded (dual-layer defense).
  - [x] Task 110.10.3: Execute direct micro-harness test verifying port 8088 returns non-empty structured JSON under `prereflection_triage_result` in $< 500\text{ms}$ with 0 `<think>` tags.
* **Anchor 1 (Target Files & Line Numbers)**:
  - `/home/jallred/serve_llm.sh#L52-L95`
  - `HomeLabAI/src/logic/cognitive_hub.py#L1012-L1031`
* **Anchor 2 (Verification Command)**:
  ```bash
  python3 -c "import urllib.request, json; req = urllib.request.Request('http://127.0.0.1:8088/v1/chat/completions', data=json.dumps({'model': 'unified-base', 'messages': [{'role': 'user', 'content': 'Audit silicon'}], 'max_tokens': 128}).encode(), headers={'Content-Type': 'application/json'}); res = json.loads(urllib.request.urlopen(req).read()); c = res['choices'][0]['message']['content']; assert len(c) > 0 and '<think>' not in c; print('PASS: non-empty triage without think tags')"
  ```
* **Anchor 3 (Verbatim Code Specs)**:
  - CLI Flags: `--reasoning off --reasoning-budget 0`
  - Safety Floor: `max_tokens: 350`
  - Dual-Layer Payload: `extra_body: {"reasoning": 0, "enable_thinking": False}`
  - Target Latency: $< 500\text{ ms}$
* **Anchor 4 (DNA Links)**: `[BKM-079]`, `[FEAT-680]`, `[FEAT-523]`, `[SPR-108]`

---

### Story 110.11: Career Compass Bedrock Decoupling & JITC with Verbatim Byte-Parity Verification (`[FEAT-434]` / `[FEAT-075]` / `[BKM-023]`)
* **Objective**: Decouple `[CAREER_COMPASS_BEDROCK]` from `BicameralNode.IDENTITY_BEDROCK` in `src/nodes/loader.py`, converting it into dynamically injected Just-In-Time Context (JITC) governed strictly by explicit triage vibe/domain allow/deny lists, with strict byte-parity verification against paraphrasing drift.
* **Owner**: `[AGY:PRIMARY]`
* **Tasks**:
  - [x] Task 110.11.1: Refactor `src/nodes/loader.py` to remove `tier_1_bedrock` from static `self.IDENTITY_BEDROCK`, exposing standalone helper `get_career_compass_bedrock()`.
  - [x] Task 110.11.2: Enforce Anti-Paraphrasing Byte-Parity: Execute a programmatic verification confirming that `get_career_compass_bedrock()` matches `SHA256: 10bbbf8e107428a11d510be0bb637b9a0a65c58141f8ac773c7bf57adf27428b`.
  - [x] Task 110.11.3: Update `build_two_mice_stage_prompt` and `resolve_hyde_vector` in `cognitive_hub.py` to inject `[CAREER_COMPASS_BEDROCK]` conditionally:
    * **STRICT ALLOW LIST**: `vibe in ("HISTORICAL", "CHRONICLE", "RETROSPECTIVE")` OR `domain in ("work_history", "career", "lab_history")` OR `"career_ledger" in target_domains`.
    * **STRICT DENY LIST**: `vibe in ("OPERATIONAL", "CASUAL", "WYWO")` OR `domain in ("exp_tlm", "telemetry", "social")`.
  - [x] Task 110.11.4: Run offline unit tests `test_career_compass_bedrock.py` confirming injection on historical vibes and omission on operational vibes.
* **Anchor 1 (Target Files & Line Numbers)**:
  - `HomeLabAI/src/nodes/loader.py#L117-L150`
  - `HomeLabAI/src/logic/cognitive_hub.py#L647-L720`, `#L2770-L2830`
* **Anchor 2 (Verification Command)**:
  ```bash
  pytest -v HomeLabAI/src/tests/test_career_compass_bedrock.py HomeLabAI/src/tests/test_round_table_probe_unit.py
  ```
* **Anchor 3 (Verbatim Code Specs)**:
  - Anti-Paraphrasing Assertion: `assert hashlib.sha256(new_bedrock.encode()).hexdigest() == '10bbbf8e107428a11d510be0bb637b9a0a65c58141f8ac773c7bf57adf27428b'`
  - JITC Gate: `should_inject_career_bedrock(vibe: str, domain: str, target_domains: list) -> bool`
* **Anchor 4 (DNA Links)**: `[FEAT-434]`, `[FEAT-075]`, `[FEAT-673]`, `[BKM-023]`, `[BKM-085]`, `[INS-052]`

---

### Story 110.12: Live Synthetic Probe Harness, Dirty Lab Pre-Flight Gate & Antigravity MO Out-of-Band Evaluation (`[BKM-024]` / `[FEAT-524]` / `[BKM-089]` / `[BKM-090]`)
* **Objective**: Establish the live probe verification harness with a strict Dirty Lab Pre-Flight Gate, certifying execution against physical running daemons, and conduct out-of-band semantic judgment under Prompt MO rubrics.
* **Owner**: `[AGY:PRIMARY]`
* **Tasks**:
  - [x] Task 110.12.1: Implement Dirty Lab Pre-Flight Gate check: Query `http://127.0.0.1:8765/status` to confirm `dirty: false` and `state: OPERATIONAL`. If backend code was edited, restart `lab-attendant.service` and verify boot commit matches Git HEAD (`[FEAT-524]`).
  - [x] Task 110.12.2: Execute live synthetic round table probe replay (`bff308bb`: *"Audit active silicon residency and memory topology"*) against running daemon on port 8765.
  - [x] Task 110.12.3: Verify operational query emits pure NVML hardware telemetry with zero BMC/DCMI/Purley hallucination and passes M5 Air Bonsai Judge with score $\ge 0.85$.
  - [x] Task 110.12.4: Antigravity Out-of-Band Judgment: Evaluate probe response artifacts against Prompt MO rubrics (`BKM-089` / `BKM-090`) to certify epistemic coherence and catch any unknown regressions.
* **Anchor 1 (Target Files & Line Numbers)**:
  - `HomeLabAI/src/server.log`
  - `HomeLabAI/src/tests/test_round_table_probe_unit.py`
  - `HomeLabAI/src/tools/standalone_accountability_watchdog.py`
* **Anchor 2 (Verification Command)**:
  ```bash
  python3 /home/jallred/Dev_Lab/HomeLabAI/src/tools/standalone_accountability_watchdog.py --single-probe "Audit active silicon residency and memory topology"
  ```
* **Anchor 3 (Verbatim Code Specs)**:
  - Dirty Lab Gate: `assert status["dirty"] is False, "Dirty lab detected: restart daemon"`
  - Bonsai Judge Metric: `score >= 0.85`
  - Zero Leak Fencing: `0 occurrences of ("BMC", "DCMI", "Purley", "validation career")` in operational stance
* **Anchor 4 (DNA Links)**: `[BKM-024]`, `[FEAT-524]`, `[BKM-089]`, `[BKM-090]`, `[INS-010]`, `[INS-047]`


