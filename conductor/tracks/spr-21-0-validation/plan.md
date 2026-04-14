# Implementation Plan: [SPR-21.0] UI Refinement & Systematic Validation

## Phase 1: Code Down (UI & Crosstalk Alignment)
**Protocol:** Use BKM-022 (Atomic IO) and [FEAT-198] Safe-Scalpel for targeted file modifications. Code first, then test.

- [ ] **Step 1:** Modify `Portfolio_Dev/field_notes/intercom.html`. Remove the hardcoded "⚡ Systems nominal." from `#crosstalk-bar` and replace it with a neutral "Awaiting neural uplink...".
- [ ] **Step 2:** Modify `HomeLabAI/src/logic/cognitive_hub.py`. Convert `logging.info` for UPLINK, THINK MORE, and Morning Briefing to `self.broadcast({"type": "crosstalk"...})`. Convert SILICON LOBOTOMY logging to a similar broadcast.
- [ ] **Step 3:** Lint and perform static analysis on modified files (`python3 -m py_compile`).

## Phase 2: Systematic Stability Testing (The Ledger)
- [ ] **Step 4 (Tier 1):** Run Foundational Telemetry tests (`test_vllm_alpha.py`, `test_liger.py`, `test_apollo_vram.py`). Verify VRAM curves and cold-start timeouts.
- [ ] **Step 5 (Tier 2):** Run Orchestration tests (`test_lifecycle_gauntlet.py`, `test_shutdown.py`, `test_intercom_flow.py`). Validate graceful sleep and zombie PID cleanup.
- [ ] **Step 6 (Tier 3):** Run Persona & Triage tests (`test_live_fire_triage.py`, `test_contextual_echo.py`, `test_agentic_backtrack.py`). Verify string vs dictionary type alignment.
- [ ] **Step 7 (Tier 4):** Run Holistic Validation (`acme_lab.py --mode DEEP_SMOKE` and `test_strategic_live_fire.py`). Verify Neural Buffer queuing during deep reasoning.