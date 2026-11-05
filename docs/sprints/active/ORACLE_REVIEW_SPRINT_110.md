# 🔮 Adversarial Oracle Audit Report: Sprint 110.0 Phase 2 Review

**Sprint:** SPR-110.0 (Pre-Flight Adversarial Architecture Audit)  
**Evaluator:** Tier 1 Strategic & Adversarial Architecture Oracle (`[SWARM:ORACLE]` / AGY)  
**Timestamp:** 2026-11-05  
**Target Document:** [`Portfolio_Dev/docs/sprints/active/SPRINT_PLAN_SPR_110_0.md`](file:///home/jallred/Dev_Lab/Portfolio_Dev/docs/sprints/active/SPRINT_PLAN_SPR_110_0.md)  
**Target Codebase:** `HomeLabAI` (branch `main`), `Portfolio_Dev` (branch `main`), `www_deploy` (branch `main`)  
**Governing BKMs & Invariants:** `[BKM-005]`, `[BKM-007]`, `[BKM-015]`, `[BKM-020]`, `[BKM-024]`, `[BKM-043]`, `[BKM-049]`, `[BKM-061]`, `[BKM-077]`, `[BKM-080]`, `[BKM-081]`, `[BKM-082]`, `[BKM-084]`, `[BKM-085]`, `[BKM-086]`, `[BKM-088]`, `[BKM-089]`, `[FEAT-416]`, `[FEAT-600]`, `[INS-052]`, `[INS-047]`

---

## 1. Executive Assessment & Macro Architectural Verdict

### 🏛️ The Verdict: **APPROVED WITH 8 MANDATORY ADVERSARIAL SAFEGUARDS**

Sprint 110.0 consolidates the multi-day transition into dual-GPU heterogeneous computing (Option A: 27GB pooled VRAM across NVIDIA RTX 2080 Ti and Intel Arc B580), executes proactive and retroactive trust-boundary scrubbing (`INS-052` / `BKM-015`), establishes empirical litmus test canaries, restores sparse background intake cadence with Foyer socket preemption, and certifies Arc B580 QSV transcoding.

The architecture is **sound, directionally aligned, and feasible**, provided the following eight failure modes are actively mitigated in the implementation:

---

## 2. Adversarial Peer Review & Edge-Case Analysis

| Risk Dimension | Oracle Finding / Failure Mode | Architectural Mitigation Required | Status |
| :--- | :--- | :--- | :--- |
| **1. 3B Model Negative Prompting Blindness (`INS-052`)** | Empirical probing proves small 3B models (Pinky) ignore negative prompt constraints (*"never extract tokens/focals"*) when copying log lines into `evidence`. Having `'career_timeline'` in raw log taxonomy causes the model to classify performance reviews as career milestones. | **Mitigation**: Prune `'career_timeline'` from raw log extraction taxonomy. Reframe prompt positively: instruct pure machine-level command extraction, and provide 1-shot contrastive example demonstrating `[REDACTED]` substitution. Out-of-band regex canary (`probe_secret_and_focal_leak_test.py`) acts as the gate. | **MANDATED IN STORIES 110.1 & 110.2** |
| **2. Toolchain Collision & Driver Stack Divergence** | Compiling `llama.cpp` with both `-DGGML_CUDA=ON` and `-DGGML_SYCL=ON` on host Linux can create header/compiler conflicts between `gcc-13`/`nvcc` and Intel oneAPI `icpx`/`dpcpp`. Dynamic library linking might cause symbol collisions if `libze1` or CUDA runtime pollute each other's environments. | **Mitigation**: Leverage Vulkan 1.4 (`-DGGML_VULKAN=ON`) which natively enumerates `GPU0` (Arc B580 16GB) and `GPU1` (RTX 2080 Ti 11GB) concurrently without compiler collision or driver symbol conflicts. | **MANDATED IN STORY 110.6** |
| **3. Instant Fallback Failure & Service Lockout** | If the hybrid engine hangs or crashes during memory allocation, the lab's primary chat/orchestration service (`vLLM` on port 8088 / 8000) could remain down, blocking agent/operator communication. | **Mitigation**: Implement a dual-state launcher `serve_llm.sh --mode=[hybrid|cuda]`. The default/fallback mode remains the proven `vLLM` container/process on RTX 2080 Ti. A healthcheck probe (`curl -sf http://localhost:8088/v1/models`) must verify fallback readiness within 5 seconds of failure. | **MANDATED IN STORY 110.6** |
| **4. Foyer Intercom Preemption Flapping** | A naive check on port 8765 or a lock file could cause rapid start/stop flapping if a WebSocket connection disconnects temporarily or during heartbeats, leaving the Nibbler in a stuck state. | **Mitigation**: Implement hysteresis in `check_foyer_intercom_active()`: inspect actual established TCP socket states (`ss -t state established '( sport = :8765 )'`). If active, Nibbler logs `[PAUSED: INTERCOM ACTIVE]` and yields cleanly without spinning. | **MANDATED IN STORY 110.4** |
| **5. Secrets Scrub History Rewriting Blast Radius** | Scrubbing JFrog tokens (`AKCp8...`) using `git commit --amend` modifies the latest commit hash on `www_deploy`. If not synchronized with the `Dev_Lab` parent submodule, Git submodule divergence will block future deploys. | **Mitigation**: After amending `9bfbcfb` in `www_deploy`, immediately update and commit the submodule pointer in `Dev_Lab` via `git -C /home/jallred/Dev_Lab commit -m "chore(submodule): sync www_deploy post-scrub"`. | **MANDATED IN STORY 110.3** |
| **6. Reasoning Suppression Regression (`INS-052` / `BKM-079`)** | **Phase 2 Hidden Failure Mode**: The `llama-server` CLI flags `--reasoning off` and `--reasoning-budget 0` may not be sufficient to suppress reasoning tokens when the engine runs in Vulkan multi-device mode. The reasoning suppression must be enforced at the engine/gateway boundary, not just at the CLI level. | **Mitigation**: Implement dual-layer suppression: CLI flags (`--reasoning off --reasoning-budget 0`) AND gateway-level parameter transformation in `_dispatch_vllm_triage()` to ensure `extra_body: {"reasoning": 0, "enable_thinking": False}` is always forwarded. Add validation that the response contains no `<think>` tags. | **MANDATED IN STORY 110.10** |
| **7. Career Bedrock JITC Injection Trap (`FEAT-434` / `BKM-023`)** | **Phase 2 Hidden Failure Mode**: The JITC injection logic in `cognitive_hub.py` may inadvertently leak career bedrock into operational queries when triage domain/vibe matching is too permissive. The byte-parity verification only ensures string equality but doesn't prevent timing-based information leakage. | **Mitigation**: Implement strict domain/vibe gating with explicit allow/deny lists. Add timing-based injection detection: measure response time differences between career and non-career queries to detect unintended leakage. Use cryptographic nonce in JITC prompts to detect replay attacks. | **MANDATED IN STORY 110.11** |
| **8. Dirty Lab Gate Bypass (`FEAT-524` / `BKM-024`)** | **Phase 2 Hidden Failure Mode**: The Dirty Lab Pre-Flight Gate check on port 8765 may be vulnerable to race conditions. An attacker could manipulate the socket state between the check and the actual probe execution, creating a window where dirty code is executed against clean silicon. | **Mitigation**: Implement atomic gate checking with file-based locking. Use `flock` or `lockf` to ensure the gate check and subsequent probe execution are atomic. Add cryptographic hash verification of daemon binary against Git HEAD before any probe execution. | **MANDATED IN STORY 110.12** |

---

## 3. Phase 2 Specific Adversarial Analysis

### Story 110.10: `llama-server` Native Reasoning Suppression & Triage Token Floor

**Hidden Failure Modes Identified:**

1. **Vulkan Multi-Device Reasoning Leakage**: When `llama-server` runs in Vulkan multi-device mode (`-dev "0,1"`), the reasoning suppression may only apply to the primary device (RTX 2080 Ti) while the secondary device (Arc B580) continues reasoning generation. This creates a split-brain scenario where triage results contain `<think>` tags from one GPU but not the other.

2. **Token Floor Race Condition**: The `max_tokens: 350` safety floor in `_dispatch_vllm_triage()` may race with the `llama-server` default token generation. If the server generates tokens faster than the client can consume them, the floor may be bypassed entirely, allowing reasoning tokens to escape.

3. **CLI Flag Interpretation Variance**: Different `llama.cpp` versions may interpret `--reasoning off` differently. Some versions may only suppress reasoning for specific model families (e.g., Qwen) while continuing reasoning for others (e.g., Llama).

**Adversarial Recommendations:**

- Implement device-specific reasoning suppression: Apply `--reasoning off` to both GPU devices explicitly
- Add token consumption monitoring: Implement client-side token rate limiting to ensure the floor is respected
- Version-gate the CLI flags: Check `llama-server --version` and apply version-specific flag variations

### Story 110.11: Career Compass Bedrock Decoupling & JITC with Byte-Parity Verification

**Hidden Failure Modes Identified:**

1. **JITC Timing Attack**: The conditional injection logic based on `vibe` and `domain` fields may be vulnerable to timing attacks. An attacker could measure response times to determine whether career bedrock was injected, potentially extracting sensitive information about the system's internal state.

2. **Domain/Vibe Matching Ambiguity**: The injection rules (`vibe in ("HISTORICAL", "CHRONICLE", "RETROSPECTIVE")` OR `domain in ("work_history", "career", "lab_history")`) may have edge cases where a query matches both career and operational domains, leading to unintended career bedrock leakage.

3. **Byte-Parity Verification Bypass**: The SHA256 hash comparison only ensures string equality but doesn't prevent character substitution attacks (e.g., homoglyph attacks where Unicode characters look similar but have different byte representations).

**Adversarial Recommendations:**

- Implement constant-time comparison for byte-parity verification
- Add fuzzy matching detection: Use n-gram similarity to detect paraphrased career bedrock
- Implement query classification confidence thresholds: Only inject career bedrock when the triage classifier is confident about the domain/vibe classification

### Story 110.12: Live Synthetic Probe Harness, Dirty Lab Pre-Flight Gate & Antigravity MO Out-of-Band Evaluation

**Hidden Failure Modes Identified:**

1. **Socket State Race Condition**: The `ss -t state established '( sport = :8765 )'` check may return true for a socket that's in the process of closing, creating a false positive gate pass. This could allow probes to execute against a partially initialized daemon.

2. **Antigravity MO Rubric Evasion**: The out-of-band semantic evaluation against Prompt MO rubrics (`BKM-089` / `BKM-090`) may be vulnerable to adversarial examples crafted to pass the rubric while containing hidden malicious content. The evaluation may focus on surface-level coherence rather than deep semantic analysis.

3. **Dirty Lab State Persistence**: The `dirty: false` check on port 8765 may not detect all forms of code modification. An attacker could modify the daemon binary in memory after the gate check but before the probe execution, bypassing the filesystem-based verification.

**Adversarial Recommendations:**

- Implement socket state validation with connection age checks: Reject sockets that are too new or too old
- Add adversarial robustness testing: Include known adversarial examples in the MO rubric evaluation
- Implement memory integrity verification: Use checksum or attestation mechanisms to verify daemon binary integrity in memory

---

## 4. Directives for Heads-Down Autonomous Execution

1. **Local Swarm Waived**: Per explicit operator instruction, local delegation to Atlas (`[SWARM:LOCAL]`) is strictly avoided for this phase. All code authoring and execution is governed directly by `[AGY:PRIMARY]`.

2. **Interactive Checkboxes Mandatory**: Under `BKM-086 §1.1`, every story and task in `SPRINT_PLAN_SPR_110_0.md` must be tracked with physical digital checkboxes (`- [ ] / - [x]`) creating an immutable audit trail.

3. **Empirical Benchmarks First**: Before declaring Option A complete, execute Story 110.7 to capture true latency (TTFT) and token throughput (tok/s) under both pure CUDA (2080 Ti) and hybrid pooled (2080 Ti + B580) modes.

4. **Preserve Jellyfin QSV**: Ensure the verified Intel Arc QSV configuration (`renderD129`) in `Dev_Lab/Jellyfin-Server/docker-compose.yml` is never reverted during GPU reconfigurations.

---

## 5. Escalation Triggers

**Immediate Escalation Required If:**

1. **Reasoning Suppression Fails**: Any probe returns a response containing `<think>` tags or reasoning content, indicating the suppression mechanism is bypassed.

2. **Career Bedrock Leakage Detected**: Any operational query (vibe: "OPERATIONAL" or domain: "exp_tlm") contains career bedrock content in the response.

3. **Dirty Lab Bypass**: Any probe executes successfully against a daemon with `dirty: true` status or against a daemon whose binary hash doesn't match Git HEAD.

4. **Antigravity MO Failure**: The out-of-band evaluation fails to detect semantic incoherence or adversarial content in probe responses.

---

## 6. Alternative Sketch (Escalation Path)

If any of the Phase 2 stories encounter the escalation triggers above, the following alternative path should be pursued:

1. **Immediate Isolation**: Halt all Phase 2 execution and isolate the affected component
2. **Root Cause Analysis**: Conduct a forensic analysis of the failure mode using the existing triage backpressure mechanisms
3. **Architectural Review**: Re-evaluate the reasoning suppression, JITC injection, and dirty lab gating architectures for fundamental design flaws
4. **Rollback Strategy**: Prepare a rollback to the previous stable state (Sprint 109.x) if the failure cannot be contained
5. **Documentation**: Update the Pre-Flight Mistakes Avoided Ledger with the new failure mode and mitigation strategy

---

**HANDOVER REFLECTION**: No blockers encountered during conceptual synthesis. Phase 2 stories 110.10, 110.11, 110.12 present significant adversarial challenges that require careful implementation of the eight mandatory safeguards identified above.
