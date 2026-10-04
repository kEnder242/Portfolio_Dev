# 🔍 ORACLE ADVERSARIAL REVIEW: Sprint 99.0 (Round Table Refinements & Anti-Green-Lie Hardening)

**Reviewer:** `[SWARM:ORACLE]`  
**Date:** 2026-10-04  
**Target Specifications:** [`SPRINT_PLAN_SPR_99_0.md`](file:///home/jallred/Dev_Lab/Portfolio_Dev/docs/sprints/active/SPRINT_PLAN_SPR_99_0.md)  
**Governing Laws:** `[BKM-062]` (Zero-Mock Anti-Green-Lie Mandate), `[BKM-015]` (Semantic Anchor Protocol), `[BKM-024]` (Live Validation Mandate), `[BKM-049]` (Delegation Execution Rulebook), `[INS-044]` / `[DISC-012]` (Subversive Tool IPC)

---

## 1. Executive Summary & Findings Matrix

| Focus Area | Current Failure Mode / Risk | Severity | Required Mitigation |
| :--- | :--- | :---: | :--- |
| **Round Table Probe Tests** | `test_round_table_probe_unit.py` mocks `/inject` returning synthetic `{"status": "QUEUED", "critic_score": 0.98}`. Real `/inject` returns async queue receipt without score. | **CRITICAL (`[BKM-062]`)** | Refactor probe to poll `foyer_stage_ledger.jsonl` and `judge_backpressure.jsonl` for genuine stage completion. Purge all fake default scores. |
| **Brain Gatekeeper** | Naive substring matching for DNA / domain relevance violates `[BKM-015]` and causes false drops on vocabulary shifts. | **HIGH (`[BKM-015]`)** | Use semantic cosine distances ($\le 0.55$) against ChromaDB `:8001` / `/ambient_recall`. |
| **Heads-Down Delegation** | Autonomous batch execution via `delegate.py` does not display ambient memory grounding headers because operator is not typing interactive prompts. | **MEDIUM (`[FEAT-650]`)** | Integrate `_trigger_ambient_hook_telemetry()` into `delegate.py` to invoke `ambient_hook.sh` and stream grounding metadata. |
| **Subversive Tool Shakedown** | Ensure $L_2$ stages plans via `stage_research` and $L_3$ queries `research` on Turn 1 without unprompted grep wander. | **HIGH (`[BKM-072]`)** | Run live shakedown battery across local silicon stack (Kender 4090 + M5 Air). |

---

## 2. Invariant & Architecture Audit

### A. The "Green Lie" Trap in Probe Unit Tests (`[BKM-062]`)
- **Flaw:** `test_round_table_probe_unit.py` line 34-53 mocked a synchronous response containing `critic_score: 0.98`. This allowed the unit test suite to report 100% green even if the multi-node deliberation daemon was completely stalled or deadlocked.
- **Remedy:** Probes must explicitly track asynchronous stage progression via the structured ledgers (`foyer_stage_ledger.jsonl` and `judge_backpressure.jsonl`) with realistic timeout bounds and zero fake defaults (`dict.get("critic_score", 0.95)`).

### B. BKM-015 Semantic Anchor Enforcement
- **Flaw:** Hardcoded keyword triggers (e.g. searching for exact string literals in turn prompts) fail during legitimate model paraphrase.
- **Remedy:** Enforce vector cosine distance thresholds ($\le 0.55$) in `vector_pre_triage.py` and `brain_node.py`.

### C. Ambient Hook Integration in `delegate.py` (`[FEAT-650]`)
- **Recommendation:** At the conclusion of `delegate()`, invoke `/home/jallred/.gemini/config/scripts/ambient_hook.sh` passing `{"invocationNum": N, "userMessage": f"Story {story_num}: {title} completed"}` and print the resulting `Grounding Header` and inject steps.

---

## 3. Certification & Gate Clearance
Sprint 99.0 plan is **APPROVED for execution** across Stories 99.1, 99.2, 99.3, and 99.4 on branch `exp/sprint-99-roundtable-shakedown`.
