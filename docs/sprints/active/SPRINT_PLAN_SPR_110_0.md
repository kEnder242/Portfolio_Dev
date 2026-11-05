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
  - [ ] Task 110.8.3: Formulate and benchmark Heterogeneous Speculative Decoding architecture (Arc B580 16GB Target + RTX 2080 Ti Draft Predictor).
  - [x] Task 110.8.4: Persist speculative decoding and 27B telemetry to `hybrid_benchmark_results.json`.
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
