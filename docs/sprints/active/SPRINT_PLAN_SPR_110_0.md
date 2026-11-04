# 📑 SPRINT PLAN 110.0: Dual-GPU Heterogeneous 27GB VRAM Engine & Unified Trust Boundary

**Sprint ID:** `SPR_110_0`  
**Theme:** Heterogeneous Multi-GPU Layer Splitting (Option A: 27GB Pooled VRAM via `llama.cpp` CUDA + SYCL/Vulkan/RPC), Zero-Downtime CUDA Fallback Architecture, Retroactive Trust-Boundary Scrubbing (`INS-052` / `BKM-015`), Balanced Sparse Intake Cadence with Foyer Intercom Preemption (`FEAT-416`), and Operational Hardware QSV Certification.  
**Status:** 🟡 **HEADS DOWN (IN PROGRESS)**  
**Parent Frameworks:**
- [`BKM-086`]: The Paved-Path Sprint Protocol (AFK / Sovereign Execution)
- [`BKM-088`]: The Empirical Pipeline Step Judgment Protocol (Micro-Harness & Benchmark Gauntlet)
- [`BKM-077`]: Conversational Anchor Tracking Protocol (1:1 Swim Lanes)
- [`BKM-081`]: Pre-Flight Mistakes Avoided Ledger
- [`BKM-082`]: 5-Sprint Historical Lookback & Mistake Prevention
- [`BKM-015`]: Semantic Anchor Protocol (Anti-Hardcoding & Regex Governance)
- [`BKM-024`]: Live Silicon Probe Protocol
- [`FEAT-416`]: Strict Nightly Refinement Isolation (02:00–05:00 AM)
- [`FEAT-600`]: Grounding Protocol & Dropped Threads Ledger
- [`INS-052`]: The Litmus Leak Test & Unified Trust Boundary
- [`INS-047`]: Live is King, History is Queen (Anti-Amnesia Sovereign Dyad)

**Target Silicon Nodes:**
- `Slot 1 (PCIe 03:00.0)`: Intel Arc B580 (16GB ReBAR, `card0`, `renderD129`, HDMI display)
- `Slot 2 (PCIe 05:00.0)`: NVIDIA GeForce RTX 2080 Ti (11GB, `card2`, `renderD130`, headless CUDA)
- `vLLM Daemon`: Port 8088 / 8000 (Pure CUDA fallback)
- `Foyer Daemon`: Port 8765 (WebSocket Intercom Preemption Signal)
- `Jellyfin Service`: Port 8096 (Arc B580 QSV HW Accel)

---

## 🛑 Pre-Flight Checklist Gate (`BKM-082 §GATE` / `BKM-086 §1.1`)
- [x] **1. 5-Sprint Lookback**: Reviewed SPR-105 through SPR-109 for traps, sentinels, and regression vectors (`BKM-082 §2.1`).
- [x] **2. Mistakes-Avoided Ledger**: Enumerated 5 concrete historical mistakes avoided (`BKM-082 §2.4` in §0.2).
- [x] **3. Oracle Review**: Adversarial architecture review completed via `ask_oracle` and documented with 4 mandatory safeguards in [`ORACLE_REVIEW_SPRINT_110.md`](file:///home/jallred/Dev_Lab/Portfolio_Dev/docs/sprints/active/ORACLE_REVIEW_SPRINT_110.md).
- [x] **4. Delegation Justification**: Evaluated per user directive: **Local delegation to Atlas (`[SWARM:LOCAL]`) is explicitly waived/forbidden due to risk in multi-card driver boundaries.** All tasks assigned to `[AGY:PRIMARY]`.
- [x] **5. Risk Assessment**: Identified toolchain conflicts (CUDA `nvcc` vs oneAPI `dpcpp`), service lockout risks, socket preemption flapping, and Git submodule sync. Concrete mitigations embedded in stories.

---

## 🛡️ Pre-Flight Mistakes Avoided Ledger (`BKM-081` / `BKM-082`)

| Historical Trap | Prior Incident | Sprint 110 Mitigation |
| :--- | :--- | :--- |
| **1. The Flapping Preemption Trap** | Sprint 64: Periodic healthchecks causing race conditions on locks | Use socket state queries (`ss -t state established '( sport = :8765 )'`) with 60-second backoff rather than volatile un-debounced lock files. |
| **2. The Driver Stack Collision Trap** | Sprint 108: Conflicting torch versions between venvs (`torch 2.11` vs `2.8`) | Keep `intel_ai_venv` completely quarantined from `Portfolio_Dev/.venv`. Build hybrid binaries in a distinct directory (`/home/jallred/hybrid_engine`). |
| **3. The Blind Push Block Trap** | Sprint 109: GitHub Push Protection rejecting tokens in historical JSONs | Implement an automated regex sanitize loop replacing JFrog tokens with `[REDACTED_JFROG_API_KEY]` before pushing. |
| **4. The Lockout Fallback Trap** | Sprint 77: Crashing experimental inference engine orphaned all LLM callers | Implement `serve_llm.sh --mode=[hybrid|cuda]` with automated healthcheck fallback to `vLLM` within 5 seconds. |
| **5. The Submodule Desync Trap** | Sprint 93: Amending commits in child submodule leaves parent git pointer dirty | Ensure `Dev_Lab` immediately commits the updated `www_deploy` submodule hash after push. |

---

## 📋 Sprint Stories & 4-Anchor Execution

### Story 110.1: Retroactive Secrets Scrub & Trust Boundary (`INS-052` / `BKM-015`)
* **Objective**: Remove leaked JFrog API tokens from `www_deploy` and `Portfolio_Dev/field_notes/data/*.json`, establishing the regex litmus escape filter.
* **Owner**: `[AGY:PRIMARY]`
* **Anchor 1 (Target Files & Line Numbers)**:
  - `www_deploy/data/queue.json`
  - `www_deploy/data/2023.json`
  - `www_deploy/data/public_benchmarks.json`
  - `Portfolio_Dev/field_notes/data/queue.json`
  - `Portfolio_Dev/field_notes/data/2023.json`
* **Anchor 2 (Verification Command)**:
  ```bash
  grep -rnE "AKCp8[A-Za-z0-9]{20,}" /home/jallred/Dev_Lab/www_deploy/data/ /home/jallred/Dev_Lab/Portfolio_Dev/field_notes/data/
  ```
  *(Expected: Zero matches)*
* **Anchor 3 (Verbatim Code Specs)**:
  - Regex target: `AKCp8[A-Za-z0-9]{20,}`
  - Replacement: `[REDACTED_JFROG_API_KEY]`
* **Anchor 4 (DNA Links)**: `[INS-052]`, `[BKM-015]`, `[WIS-484]`

---

### Story 110.2: `www_deploy` Amend, Remote Push & Submodule Sync
* **Objective**: Amend commit `ffbdc4c` in `www_deploy` post-scrub, verify GitHub Push Protection passes, and sync parent `Dev_Lab` submodule pointer.
* **Owner**: `[AGY:PRIMARY]`
* **Anchor 1 (Target Files & Line Numbers)**:
  - `Dev_Lab/www_deploy` (Git commit pointer)
* **Anchor 2 (Verification Command)**:
  ```bash
  git -C /home/jallred/Dev_Lab/www_deploy status -uno && git -C /home/jallred/Dev_Lab status -uno
  ```
  *(Expected: Clean working tree, remote up to date)*
* **Anchor 3 (Verbatim Code Specs)**:
  - `git -C /home/jallred/Dev_Lab/www_deploy commit --amend --no-edit`
  - `git -C /home/jallred/Dev_Lab/www_deploy push origin main`
  - `git -C /home/jallred/Dev_Lab add www_deploy && git -C /home/jallred/Dev_Lab commit -m "chore(submodule): sync www_deploy post-scrub"`
* **Anchor 4 (DNA Links)**: `[BKM-009]`, `[BKM-020]`

---

### Story 110.3: Gem Balancing & Sparse Ingestion Cadence with Preemption
* **Objective**: Re-tune `nibble_v2.py` to run every 15 minutes processing 1–2 chunks, enforce nightly-only quarantine for `refine_gem.py` ([FEAT-416]), and implement Foyer intercom socket preemption.
* **Owner**: `[AGY:PRIMARY]`
* **Anchor 1 (Target Files & Line Numbers)**:
  - `Portfolio_Dev/field_notes/nibble_v2.py`
  - `Portfolio_Dev/field_notes/refine_gem.py`
* **Anchor 2 (Verification Command)**:
  ```bash
  python3 -c "from field_notes.nibble_v2 import check_foyer_intercom_active; print('Intercom check:', check_foyer_intercom_active())"
  ```
  *(Expected: Boolean returned cleanly without exceptions)*
* **Anchor 3 (Verbatim Code Specs)**:
  ```python
  def check_foyer_intercom_active() -> bool:
      # Inspect established TCP sockets on Foyer WebSocket port 8765
      # or presence of active chat lock
  ```
  - Interval configured to 900 seconds (15 minutes).
  - Max chunks per cycle: 2.
* **Anchor 4 (DNA Links)**: `[FEAT-416]`, `[FEAT-101]`, `[BKM-086]`

---

### Story 110.4: Jellyfin Arc B580 QSV & Steam Remote Play Certification
* **Objective**: Validate that Jellyfin hardware transcoding on Arc B580 QSV remains operational with fallback stanzas preserved, and confirm display server routing for Steam Remote Play.
* **Owner**: `[AGY:PRIMARY]`
* **Anchor 1 (Target Files & Line Numbers)**:
  - `Dev_Lab/Jellyfin-Server/docker-compose.yml`
  - `/var/lib/jellyfin-data/config/config/encoding.xml`
* **Anchor 2 (Verification Command)**:
  ```bash
  docker ps --filter "name=jellyfin" --format "{{.Status}}" && vpl-inspect | grep -i "DeviceID"
  ```
  *(Expected: Container Up healthy, B580 e20b visible in oneVPL)*
* **Anchor 3 (Verbatim Code Specs)**:
  - Ensure `/dev/dri:/dev/dri` mapped.
  - Verify `renderD129` active in `encoding.xml`.
* **Anchor 4 (DNA Links)**: `[BKM-024]`, `[INS-047]`

---

### Story 110.5: Multi-Backend Hybrid Inference Engine (Option A: 27GB Pooled VRAM)
* **Objective**: Build and deploy `llama.cpp` supporting heterogeneous layer splitting across NVIDIA RTX 2080 Ti (11GB CUDA) and Intel Arc B580 (16GB SYCL/Vulkan/RPC) with instantaneous toggle fallback to pure CUDA `vLLM`.
* **Owner**: `[AGY:PRIMARY]`
* **Anchor 1 (Target Files & Line Numbers)**:
  - `/home/jallred/hybrid_engine/` (Build & wrapper scripts)
  - `/home/jallred/serve_llm.sh` (Unified fallback launcher)
* **Anchor 2 (Verification Command)**:
  ```bash
  /home/jallred/serve_llm.sh --test
  ```
  *(Expected: Model loads, distributes layers across both GPUs, passes healthcheck)*
* **Anchor 3 (Verbatim Code Specs)**:
  - Heterogeneous device split: `-dev cuda0,sycl0` (or Vulkan device IDs `0,1`)
  - `--split-mode layer` (`-sm layer`)
  - Tensor split ratio: `-ts 11,16`
* **Anchor 4 (DNA Links)**: `[BKM-088]`, `[INS-047]`

---

### Story 110.6: Empirical Throughput & Latency Benchmark Gauntlet (`BKM-088`)
* **Objective**: Execute an empirical benchmark gauntlet comparing pure CUDA (RTX 2080 Ti) vs hybrid pooled VRAM (RTX 2080 Ti + Arc B580), recording TTFT, tok/s, and physical memory footprint.
* **Owner**: `[AGY:PRIMARY]`
* **Anchor 1 (Target Files & Line Numbers)**:
  - `Portfolio_Dev/field_notes/benchmark_hybrid.py`
  - `Portfolio_Dev/field_notes/data/hybrid_benchmark_results.json`
* **Anchor 2 (Verification Command)**:
  ```bash
  python3 /home/jallred/Dev_Lab/Portfolio_Dev/field_notes/benchmark_hybrid.py
  ```
  *(Expected: Benchmark JSON persisted with latency and throughput metrics)*
* **Anchor 3 (Verbatim Code Specs)**:
  - Benchmark payloads: Short prompt (32 tokens), Long prompt (1024 tokens)
  - Record: `ttft_ms`, `tokens_per_second`, `vram_cuda_mb`, `vram_arc_mb`
* **Anchor 4 (DNA Links)**: `[BKM-088]`, `[BKM-024]`
