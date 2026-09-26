# Sprint Plan: SPR-92.0 — Ground Truth Round Table & Anti-Green-Lie Certification
**Date:** September 25, 2026  
**Goal:** Eliminate all synthetic probe mocks, default score leaks, and dirty-daemon bypasses. Enforce strict live multi-stage round table execution, genuine token latency measurement, and independent out-of-band watchdog certification.

---

## 🎯 Architectural Mandates
1. **NO GREEN LIES (BKM-062):** Probes must never use default fallback scores (e.g. `dict.get("critic_score", 0.95)`), must never treat async queue ingress (`"QUEUED"`) as execution pass, and must wait for real end-to-end multi-node deliberation completion.
2. **LIVE VALIDATION MANDATE (BKM-024):** Daemon bytecode must match Git HEAD (`dirty: false`, `engine: OPERATIONAL`) on physical silicon endpoints.
3. **TRI-LOOP OWNER DISCIPLINE (BKM-049):** All stories tagged with explicit owner tags; adversarial Cloud Oracle audit dispatched via `delegate.py --mode oracle`.
4. **DOUBLE-WRITE & PERSISTENCE:** Synchronize status and digests across `Portfolio_Dev/field_notes/data/` and `www_deploy/data/`.

---

## 📋 Story Cards

### Story 92.1: Foyer Daemon Re-Ignition & Clean Head Synchronization
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Scope:** Restart/re-ignite `acme_foyer_v5` and Lab Attendant so `boot_commit == HEAD`, `dirty == false`, and resident silicon engines (vLLM/Ollama) are hot and ready in `OPERATIONAL` state.
* **Success Criteria:** `curl http://127.0.0.1:8765/status?timeout=5` returns `state: OPERATIONAL`, `dirty: false`, `engine_up: true`.

### Story 92.2: Ground Truth Synthetic Round Table Probe Engine
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Scope:** Refactor `HomeLabAI/src/infra/probe_round_table_accountability.py` to:
  1. Wake Foyer from hibernation if needed via `POST /wake`.
  2. Inject synthetic prompt via `POST /inject` and capture `event_id`.
  3. Poll/await `Portfolio_Dev/field_notes/data/foyer_stage_ledger.jsonl` for that specific `event_id`.
  4. Verify completion of all 5 stages (`stage1_kender_triage` / `stage1_deep_thought_triage`, `stage2_pinky_hyde`, `stage3_brain_query`, `stage4_dt_synthesis`, `stage5_pinky_review`).
  5. Extract real critic score from Stage 5 payload in `logs/trace_pinky.json` rather than falling back to default values.
  6. Measure true wall-clock circuit latency (typically 3s–15s).
* **Success Criteria:** Probe reports `PASS` only when all 5 stages execute and emit genuine tokens, and reports `FAIL` if the engine is dirty, deadlocked, or truncated.

### Story 92.3: Decoupled Watchdog Live Shakedown & Audit Certification
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Scope:** Run `HomeLabAI/src/infra/standalone_accountability_watchdog.py` live against the active round table and ensure `daily_accountability_digest.json` records physical measurements across all 7 vectors.
* **Success Criteria:** Standalone watchdog runs live without mocking, grading real silicon evidence.

### Story 92.4: Cloud Oracle Adversarial Review & Certification
* **Assigned Owner:** `[SWARM:CLOUD]`
* **Scope:** Dispatch `delegate.py --mode oracle` to adversarial cloud models (`opencode/big-pickle`, `openrouter`, `cohere`) to rigorously audit the codebase against silent failure vectors.
* **Success Criteria:** Adversarial Oracle review yields CERTIFIED status.

### Story 92.5: Documentation & Feature Tracker Synchronization
* **Assigned Owner:** `[AGY:PRIMARY]`
* **Scope:** Update `FeatureTracker.md` (`FEAT-608`, `FEAT-619`, `FEAT-607`), `Protocols.md` (`BKM-062`, `BKM-066`, `BKM-067`), and `00_FEDERATED_STATUS.md`.
* **Success Criteria:** 100% clean local commits, 0 remote pushes.
