# 🚀 SPRINT PLAN: SPR-68.0
## Sovereign Local M5 Air vs. Cloud Swarm Head-to-Head Comparative Study & Telemetry Disambiguation

---

### 🏛️ 1. Executive Summary & Experimental Methodology
Sprint 68.0 conducts a fair, isolated, head-to-head empirical comparison between **Sovereign Local Silicon (Apple M5 Air Qwen 3.8 27B + Windows RTX 4090)** and the **Cloud Swarm (OpenRouter / OpenCode)** across three functional production stories.

To ensure scientific fairness and avoid test cross-contamination:
1. **Identical Prompts & Acceptance Criteria:** Both branches receive byte-for-byte identical story prompts and file targets via `delegate.py`.
2. **Branch Isolation:**
   * Branch `bench/local-m5-air-delegation`: Executed with `--local-only` (M5 Air Planning + 4090 Coding).
   * Branch `bench/cloud-swarm-delegation`: Executed against Cloud Swarm (`openrouter/free` / `hy3-free`).
3. **Serial Execution:** Runs are dispatched sequentially (never in parallel) to prevent socket timeouts and file locks.
4. **2x3 Guardrail Rule:** If delegation encounters failure on either tier, up to 3 fix+retry attempts are permitted. If 3 attempts fail, the orchestrator implements directly.
5. **Telemetry Disambiguation (`[FEAT-504]`):** Real-time telemetry is enhanced to explicitly segment `sovereign_local` vs `cloud_swarm` tokens, latency, velocity, and power.

---

### 🎯 2. The 3 Comparative Stories

```
SPRINT 68.0 COMPARATIVE GAUNTLET
├── [STORY 68.1] Real-Time Telemetry Cloud vs. Local Tier Disambiguation (FEAT-504)
├── [STORY 68.2] 1-Token Vocal Inference Prober (FEAT-502) [Comparative Run]
├── [STORY 68.3] Eager Resident Ignition on Foyer Boot (FEAT-503) [Comparative Run]
├── [STORY 68.4] BKM-010 Forensic Documentation & 5x5 Mandate Hardening (FEAT-505) [Comparative Run]
└── [STORY 68.5] Comparative Synthesis Report & Master Feature Merge (FEAT-506)
```

---

### 📦 3. Detailed Story Specifications

#### 📦 Story 68.1: Real-Time Telemetry Cloud vs. Local Disambiguation (`[FEAT-504]`)
* **Target:** `HomeLabAI/src/infra/cumulative_telemetry.py`, `Portfolio_Dev/field_notes/benchmarks.html`, `data/cumulative_tokens.json`.
* **Objective:** Add explicit `tier` tag (`"sovereign_local"` vs `"cloud_swarm"`) and separate token/run counters so the live usage stream and dashboard visually distinguish local execution from cloud fallback.
* **Verification:** Run a local live event and cloud event; verify both write distinct tier tags to `live_usage_stream.jsonl`.

#### 📦 Story 68.2: 1-Token Vocal Inference Prober (`[FEAT-502]`)
* **Target:** `HomeLabAI/src/logic/speculative_triage.py`.
* **Objective:** Replace the raw TCP socket probe in `resolve_active_deep_thought_target()` with an async 1-token live completion probe (`POST /v1/chat/completions`, `max_tokens=1`, 300ms timeout) that detects memory errors and avoids false-positive lock-ins.
* **Verification:** Unit tests in `test_speculative_triage.py` pass; probe correctly identifies live M5 Air without double-ping latency.

#### 📦 Story 68.3: Eager Resident Ignition on Foyer Boot (`[FEAT-503]`)
* **Target:** `HomeLabAI/src/v5/foyer/router.py`.
* **Objective:** Eagerly boot and synchronize resident worker subprocesses (`PINKY`, `ARCHIVE`, `THOUGHT`, `BRAIN`, `LAB`) upon daemon startup, eliminating the 56s first-connect delay.
* **Verification:** Daemon initialization completes background node synchronization before accepting client traffic.

#### 📦 Story 68.4: BKM-010 Forensic Documentation & 5x5 Mandate Hardening (`[FEAT-505]`)
* **Target:** `HomeLabAI/docs/Protocols.md`.
* **Objective:** Update `BKM-010` (*Debug Co-Pilot*) to permanently anchor the canonical path `file:///home/jallred/Dev_Lab/HomeLabAI/src/server.log` and the 75-minute 5x5 mandate (0m, 5m, 10m, 20m, 40m).
* **Verification:** Markdown lint passes; CLaRa DNA sync embeds updated BKM.

#### 📦 Story 68.5: Comparative Synthesis Report & Master Feature Merge (`[FEAT-506]`)
* **Target:** `Portfolio_Dev/field_notes/reports/comparative_local_m5_vs_cloud_report.md`.
* **Objective:** Synthesize metrics (first-pass accuracy, token velocity, context bloat, handover reflections) into a formal benchmark artifact, then merge certified implementations into the master feature branch.

---
