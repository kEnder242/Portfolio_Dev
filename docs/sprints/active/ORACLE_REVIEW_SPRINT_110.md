# 🔮 Adversarial Oracle Audit Report: Sprint 110.0

**Sprint:** SPR-110.0 (Pre-Flight Adversarial Architecture Audit)  
**Evaluator:** Tier 1 Strategic & Adversarial Architecture Oracle (`[SWARM:ORACLE]` / AGY)  
**Timestamp:** 2026-11-04  
**Target Document:** [`Portfolio_Dev/docs/sprints/active/SPRINT_PLAN_SPR_110_0.md`](file:///home/jallred/Dev_Lab/Portfolio_Dev/docs/sprints/active/SPRINT_PLAN_SPR_110_0.md)  
**Target Codebase:** `HomeLabAI` (branch `main`), `Portfolio_Dev` (branch `main`), `www_deploy` (branch `main`)  
**Governing BKMs & Invariants:** `[BKM-005]`, `[BKM-007]`, `[BKM-015]`, `[BKM-020]`, `[BKM-024]`, `[BKM-043]`, `[BKM-049]`, `[BKM-061]`, `[BKM-077]`, `[BKM-080]`, `[BKM-081]`, `[BKM-082]`, `[BKM-084]`, `[BKM-085]`, `[BKM-086]`, `[BKM-088]`, `[BKM-089]`, `[FEAT-416]`, `[FEAT-600]`, `[INS-052]`, `[INS-047]`  

---

## 1. Executive Assessment & Macro Architectural Verdict

### 🏛️ The Verdict: **APPROVED WITH 5 MANDATORY ADVERSARIAL SAFEGUARDS**

Sprint 110.0 consolidates the multi-day transition into dual-GPU heterogeneous computing (Option A: 27GB pooled VRAM across NVIDIA RTX 2080 Ti and Intel Arc B580), executes proactive and retroactive trust-boundary scrubbing (`INS-052` / `BKM-015`), establishes empirical litmus test canaries, restores sparse background intake cadence with Foyer socket preemption, and certifies Arc B580 QSV transcoding.

The architecture is **sound, directionally aligned, and feasible**, provided the following five failure modes are actively mitigated in the implementation:

---

## 2. Adversarial Peer Review & Edge-Case Analysis

| Risk Dimension | Oracle Finding / Failure Mode | Architectural Mitigation Required | Status |
| :--- | :--- | :--- | :--- |
| **1. 3B Model Negative Prompting Blindness (`INS-052`)** | Empirical probing proves small 3B models (Pinky) ignore negative prompt constraints (*"never extract tokens/focals"*) when copying log lines into `evidence`. Having `'career_timeline'` in raw log taxonomy causes the model to classify performance reviews as career milestones. | **Mitigation**: Prune `'career_timeline'` from raw log extraction taxonomy. Reframe prompt positively: instruct pure machine-level command extraction, and provide 1-shot contrastive example demonstrating `[REDACTED]` substitution. Out-of-band regex canary (`probe_secret_and_focal_leak_test.py`) acts as the gate. | **MANDATED IN STORIES 110.1 & 110.2** |
| **2. Toolchain Collision & Driver Stack Divergence** | Compiling `llama.cpp` with both `-DGGML_CUDA=ON` and `-DGGML_SYCL=ON` on host Linux can create header/compiler conflicts between `gcc-13`/`nvcc` and Intel oneAPI `icpx`/`dpcpp`. Dynamic library linking might cause symbol collisions if `libze1` or CUDA runtime pollute each other's environments. | **Mitigation**: Leverage Vulkan 1.4 (`-DGGML_VULKAN=ON`) which natively enumerates `GPU0` (Arc B580 16GB) and `GPU1` (RTX 2080 Ti 11GB) concurrently without compiler collision or driver symbol conflicts. | **MANDATED IN STORY 110.6** |
| **3. Instant Fallback Failure & Service Lockout** | If the hybrid engine hangs or crashes during memory allocation, the lab's primary chat/orchestration service (`vLLM` on port 8088 / 8000) could remain down, blocking agent/operator communication. | **Mitigation**: Implement a dual-state launcher `serve_llm.sh --mode=[hybrid|cuda]`. The default/fallback mode remains the proven `vLLM` container/process on RTX 2080 Ti. A healthcheck probe (`curl -sf http://localhost:8088/v1/models`) must verify fallback readiness within 5 seconds of failure. | **MANDATED IN STORY 110.6** |
| **4. Foyer Intercom Preemption Flapping** | A naive check on port 8765 or a lock file could cause rapid start/stop flapping if a WebSocket connection disconnects temporarily or during heartbeats, leaving the Nibbler in a stuck state. | **Mitigation**: Implement hysteresis in `check_foyer_intercom_active()`: inspect actual established TCP socket states (`ss -t state established '( sport = :8765 )'`). If active, Nibbler logs `[PAUSED: INTERCOM ACTIVE]` and yields cleanly without spinning. | **MANDATED IN STORY 110.4** |
| **5. Secrets Scrub History Rewriting Blast Radius** | Scrubbing JFrog tokens (`AKCp8...`) using `git commit --amend` modifies the latest commit hash on `www_deploy`. If not synchronized with the `Dev_Lab` parent submodule, Git submodule divergence will block future deploys. | **Mitigation**: After amending `9bfbcfb` in `www_deploy`, immediately update and commit the submodule pointer in `Dev_Lab` via `git -C /home/jallred/Dev_Lab commit -m "chore(submodule): sync www_deploy post-scrub"`. | **MANDATED IN STORY 110.3** |

---

## 3. Directives for Heads-Down Autonomous Execution

1. **Local Swarm Waived**: Per explicit operator instruction, local delegation to Atlas (`[SWARM:LOCAL]`) is strictly avoided for this phase. All code authoring and execution is governed directly by `[AGY:PRIMARY]`.
2. **Interactive Checkboxes Mandatory**: Under `BKM-086 §1.1`, every story and task in `SPRINT_PLAN_SPR_110_0.md` must be tracked with physical digital checkboxes (`- [ ] / - [x]`) creating an immutable audit trail.
3. **Empirical Benchmarks First**: Before declaring Option A complete, execute Story 110.7 to capture true latency (TTFT) and token throughput (tok/s) under both pure CUDA (2080 Ti) and hybrid pooled (2080 Ti + B580) modes.
4. **Preserve Jellyfin QSV**: Ensure the verified Intel Arc QSV configuration (`renderD129`) in `Dev_Lab/Jellyfin-Server/docker-compose.yml` is never reverted during GPU reconfigurations.
