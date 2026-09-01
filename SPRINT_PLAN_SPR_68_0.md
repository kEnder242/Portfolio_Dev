# 🚀 SPRINT PLAN: SPR-68.0
## Sovereign Local M5 Air vs. Cloud Swarm Head-to-Head Comparative Study (2x3 Matrix)

---

### 🏛️ 1. Executive Summary & Experimental Methodology
Sprint 68.0 conducts a fair, isolated, head-to-head empirical comparison between **Sovereign Local Silicon (Apple M5 Air Qwen 3.8 27B + Windows RTX 4090)** and the **Cloud Swarm (OpenRouter / OpenCode)** across three functional production stories.

**The 2x3 Matrix (6 Total Dispatches):**
* **Tier A (Local Sovereign Silicon):** 3 Stories dispatched with `--local-only` (M5 Air Planning / Architect + 4090 Coding).
* **Tier B (Cloud Swarm):** 3 Stories dispatched with standard cloud ladder (`openrouter/free` / `hy3-free`).

---

### 🎯 2. The 3 Production Stories
1. **Story 68.2 (`[FEAT-502]`):** 1-Token Vocal Inference Prober in `HomeLabAI/src/logic/speculative_triage.py`.
2. **Story 68.3 (`[FEAT-503]`):** Eager Resident Node Ignition on Foyer Boot in `HomeLabAI/src/v5/foyer/router.py`.
3. **Story 68.4 (`[FEAT-505]`):** BKM-010 Forensic Documentation & 5x5 Mandate Hardening in `HomeLabAI/docs/Protocols.md`.

---

### 🛡️ 3. Execution Rules & Guardrails
1. **Branch Isolation:**
   * Local runs commit to branch `bench/local-m5-air-delegation`.
   * Cloud runs commit to branch `bench/cloud-swarm-delegation`.
2. **Identical Prompts & Criteria:** Both branches receive identical `--reference`, `--target`, and `--details` arguments.
3. **Serial Execution:** Runs execute sequentially to prevent port/socket collisions.
4. **2x3 Guardrail Limit:** Up to 3 retry/fix attempts per story. If 3 fail, orchestrator implements directly.
5. **Synthesis & Feature Merge (`[FEAT-506]`):** Merges certified code into `feat/m5-deep-thought-migration` and generates a comparative report.
