# Master Sprint Plan: Sprint 44 — Lab Resilience, Memory Guardrails & Telemetry Visibility

> **Sprint Narrative:**
> As our Federated Lab expands with active AI subagent swarms and high-density RAG synthesis, memory stability on our 16 GB host (`z87-Linux`) is paramount. Sprint 44 focuses on transforming the Lab from reactive memory recovery to proactive memory governance. We will enforce strict RAM sentinels for background scanners, implement the "Emergency Deafness" policy to protect system headroom, eliminate duplicate PyTorch/SentenceTransformer RAM allocations, restore the true Vocal Probe BKM, and surface real-time vLLM engine health and errors directly into `status.html`.

---

## 🎯 Master Architecture Goals & Target File Map

1. **Memory Pressure Protections (`LAB-088` & `LAB-089`):**
   - **Target Files:** `HomeLabAI/src/v5/foyer/router.py`, `HomeLabAI/src/v5/common/types.py`, `Portfolio_Dev/field_notes/nibble_v2.py`, `Portfolio_Dev/field_notes/scan_queue.py`.
   - EarNode pre-loads on startup for VRAM allocation hygiene, but automatically unloads under RAM pressure (`available_ram < 3.0 GB`) or during Swarm / Heads-Down mode. Re-enabled for manual integration testing.
   - Nibbler (`nibble_v2.py`) is strictly **IDLE ONLY** (Priority 0: Evict First), requiring pre-flight RAM checks (`available_ram >= 3.0 GB`) before every chunk pass.

2. **Shared Vector Embedding Service:**
   - **Target Files:** `HomeLabAI/src/nodes/archive_node.py`, `HomeLabAI/src/bridge_burn_to_rag.py`.
   - Consolidate PyTorch and `SentenceTransformer` imports across `archive_node.py` and `bridge_burn_to_rag.py` into a single shared HTTP/socket embedding daemon, saving ~1.5 GB RAM.

3. **Vocal Probe Enforcement & Interleaved Log Error Visibility:**
   - **Target Files:** `HomeLabAI/src/nodes/loader.py`, `Portfolio_Dev/field_notes/data/pager_activity.json`, `Portfolio_Dev/field_notes/status.html`.
   - Restore the full Vocal Probe (`/v1/chat/completions` token check with `unified-base`) in `loader.py` instead of trusting `/v1/models` (`200 OK`).
   - Wire vLLM engine errors directly to `trigger_pager()` for display on `status.html`.

4. **Git & Scanner Hardening (`BKM-035`):**
   - **Target Files:** `Portfolio_Dev/.gitignore`, `Portfolio_Dev/field_notes/scan_artifacts.py`.
   - Delete duplicate `Portfolio_Dev/venv/` and enforce git curation.
   - Harden `scan_artifacts.py` so LLM fallback failures never overwrite rich AI synopses with generic `"Heuristic"` placeholders.

---

## 📜 Story Backlog & Detailed Implementation Tasks

### **Story 1: `LAB-088` / `FEAT-420` — Emergency Deafness & EarNode Lifecycle Management**
- **Target Files:** `/home/jallred/Dev_Lab/HomeLabAI/src/v5/foyer/router.py`, `/home/jallred/Dev_Lab/HomeLabAI/src/v5/common/types.py`
- **Rationale:** Prevent NeMo EarNode (~2.5 GB RAM / ~1.0 GB VRAM) from causing memory lockups during subagent swarms or RAG synthesis.
- **Mechanism:**
  - In `router.py`, keep startup pre-loading for contiguous CUDA VRAM organization on RTX 2080 Ti.
  - Add `unload_sensory_ear()` trigger in `FoyerRouter` whenever `available_ram < 3.0 GB` or Swarm / Heads-Down mode is declared.
  - Add `rearm_sensory_ear()` upon manual integration test request.
- **Proof:** Run memory stress probe while initiating subagent swarm; verify EarNode drops cleanly and available RAM remains > 3.0 GB.

---

### **Story 2: `LAB-089` / `FEAT-421` — Idle-Only Nibbler & RAM Sentinel**
- **Target Files:** `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/nibble_v2.py`, `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/scan_queue.py`
- **Rationale:** Nibbler is continuous background refinement and must yield to all interactive/agentic tasks.
- **Mechanism:**
  - In `nibble_v2.py` / `scan_queue.py`, add pre-flight check:
    `if available_ram < 3.0 GB or active_locks: sleep(30); yield`
  - Re-design Nibbler to check system load average (< 2.0) before every chunk summary.
- **Proof:** Trigger heavy load or subagent task; verify Nibbler logs `[NIBBLER] Yielding: Memory/Load Pressure` and consumes zero CPU/RAM.

---

### **Story 3: Shared Embedding Daemon (PyTorch RAM Deduplication)**
- **Target Files:** `/home/jallred/Dev_Lab/HomeLabAI/src/nodes/archive_node.py`, `/home/jallred/Dev_Lab/HomeLabAI/src/bridge_burn_to_rag.py`
- **Rationale:** Eliminate duplicate PyTorch + SentenceTransformer loads across `archive_node.py` and `bridge_burn_to_rag.py`.
- **Mechanism:**
  - Route all RAG vector embeddings through the persistent ChromaDB HTTP daemon on port 8001 (or a single FastEmbed service).
  - Remove direct `SentenceTransformer` imports from `archive_node.py`.
- **Proof:** Check `ps aux --sort=-%mem`; verify total memory saved is ~1.5 GB.

---

### **Story 4: Interleaved Log Error Visibility & Vocal Probe Enforcement**
- **Target Files:** `/home/jallred/Dev_Lab/HomeLabAI/src/nodes/loader.py`, `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/data/pager_activity.json`, `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/status.html`
- **Rationale:** Never trust `200 OK` on `/v1/models`. Surface real engine errors to the user UI.
- **Mechanism:**
  - Restore full Vocal Probe (`/v1/chat/completions` with payload `{"model": "unified-base", "messages": [{"role": "user", "content": "Respond with SUCCESS."}]}`) in `src/nodes/loader.py`.
  - Pass vLLM stream errors (`r.status != 200`) to `trigger_pager()`, writing directly to `pager_activity.json`.
- **Proof:** Simulate engine failure; verify red alert appears on `status.html` log tree.

---

### **Story 5: Scanner Hardening & Git Hygiene Cleanup (`BKM-035`)**
- **Target Files:** `/home/jallred/Dev_Lab/Portfolio_Dev/.gitignore`, `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/scan_artifacts.py`
- **Rationale:** Prevent loss of rich AI synopses in `artifacts_*.json` and eliminate virtualenv indexing bloat.
- **Mechanism:**
  - Verify `Portfolio_Dev/venv/` removal and `.gitignore` rule.
  - Update `scan_artifacts.py`: if `ENGINE.generate()` fails or returns None, preserve `existing_map[filename]` AI entry instead of overwriting with `method: "Heuristic"`.
- **Proof:** Run `scan_artifacts.py` with offline engine; verify `artifacts_DOCS.json` preserves all 360 high-fidelity AI synopses.

---

## 🧪 Verification & Acceptance Criteria
- [x] Available system RAM remains > 3.0 GB during active development and subagent runs.
- [x] EarNode pre-loads on boot but unloads cleanly under pressure or during Swarm mode.
- [x] Nibbler runs strictly during idle periods and yields immediately under load.
- [x] vLLM engine errors appear on `status.html` interleaved timeline.
- [x] High-fidelity AI synopses in `artifacts_*.json` are protected against fallback erasures.

---

## 📊 Final Execution Report & Architectural Polish

### **Primary Sprint Deliverables (Stories 1–5)**
- **Story 1 (`LAB-088` / `FEAT-420` EarNode Deafness):** Implemented `unload_sensory_ear()` / `rearm_sensory_ear()` in `HomeLabAI/src/equipment/sensory_manager.py` and `/rearm_ear` REST route in `src/v5/foyer/router.py`. NeMo Speech Streaming model buffers automatically unmapped when `available_ram < 3.0 GB` or Swarm/Heads-Down mode triggers. *(Commit: `c89ab25`)*
- **Story 2 (`LAB-089` / `FEAT-421` Idle-Only Nibbler):** Implemented `should_yield()` pre-flight sentinels in `Portfolio_Dev/field_notes/nibble_v2.py` and `scan_queue.py` checking `available_ram >= 3.0 GB` and `load_avg <= 2.0`. Yields instantly without allocating memory under pressure. *(Commit: `fd2fa7a`)*
- **Story 3 (PyTorch Deduplication):** Routed vector embedding generation directly to ChromaDB HTTP server on port 8001 in `HomeLabAI/src/nodes/archive_node.py` and `src/bridge_burn_to_rag.py`. Saved **~1.5 GB RAM**. *(Commit: `9bc35d3`)*
- **Story 4 (Vocal Probe BKM & Error Pager):** Enforced POST `/v1/chat/completions` token generation probe in `HomeLabAI/src/nodes/loader.py` and linked vLLM stream/ping errors directly to `trigger_pager()` for display on `status.html`. *(Commit: `9efbf0d`)*
- **Story 5 (Scanner Hardening & Git Hygiene `BKM-035`):** Hardened `Portfolio_Dev/.gitignore` (`venv/`, `env/`, `*.egg-info/`) and updated `scan_artifacts.py` to preserve rich AI synopses during fallback scenarios. *(Commit: `feb3483`)*

---

---

## 🚀 Active Backlog — Atomic Story Cards (Stories 6–8)

### 🎴 STORY CARD 6: `FEAT-442` — Query Pre-Flight Refinement (QPR) & HyDE Synergy
- **Feature ID**: `FEAT-442` (Proposed / Active)
- **Target Repository & Files**: `HomeLabAI` $\rightarrow$ `src/logic/cognitive_hub.py`, `src/tests/test_qpr_hyde.py`
- **Objective & Technical Spec**: Implement pre-retrieval query de-noising in `get_context()` before ChromaDB vector search. Translates noisy human queries into domain-specific indexing terms. Keeps original query as fallback if top vector similarity distance > 0.45 (score < 0.70). Prevents semantic noise from degrading HyDE hypothetical doc generation.
- **Live-Lab Validation Gate**:
  1. `sudo systemctl restart lab-attendant.service`
  2. `pytest src/tests/test_qpr_hyde.py`
  3. Inject live test query via `intercom.html` and verify `attendant.log` confirms refined query lookup.
- **Spoon-Fed OpenAgent Delegation Command**:
  ```bash
  /home/jallred/.opencode/bin/opencode run --dir /home/jallred/Dev_Lab/HomeLabAI --attach http://127.0.0.1:4096/ "SESSION: Sprint 44 Story 6 — FEAT-442 QPR & HyDE Integration

  CONTEXT:
  - Target file: /home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py
  - Task: Implement pre-retrieval query de-noising in get_context() before ChromaDB search.
  - Rule: Refine noisy user queries into domain-specific indexing terms. Keep original query as fallback if top vector similarity distance is > 0.45 (< 0.70 score).
  - Test File: Create src/tests/test_qpr_hyde.py testing QPR refinement and fallback logic.
  - Validation Gate: Restart lab-attendant.service via systemctl, run pytest, and verify clean execution."
  ```

---

### 🎴 STORY CARD 7: `FEAT-443` — Premise-Aware RAG-EVAL (PAR-Eval) & Valid Refusal Scoring
- **Feature ID**: `FEAT-443` (Proposed / Active)
- **Target Repository & Files**: `HomeLabAI` $\rightarrow$ `src/nodes/mlx_judge_node.py`, `src/debug/uber_5x5_v5.py`, `src/tests/test_par_eval_scoring.py`
- **Objective & Technical Spec**: Enhance `MLXAsyncJudge` with structured refusal schema `{ "refusal": true, "reason": "PREMISE_MISMATCH" }`. Update 5x5 benchmark harness (`uber_5x5.py`) `evaluate_fidelity()` to intercept validated refusal payloads ("Jason did not perform GPU VRAM work at Intel") and score them as **5/5 PASS**.
- **Live-Lab Validation Gate**:
  1. `sudo systemctl restart lab-attendant.service`
  2. `pytest src/tests/test_par_eval_scoring.py`
  3. Run `python3 src/debug/uber_5x5_v5.py --fast` with false-premise probe and verify 5/5 PASS certification.
- **Spoon-Fed OpenAgent Delegation Command**:
  ```bash
  /home/jallred/.opencode/bin/opencode run --dir /home/jallred/Dev_Lab/HomeLabAI --attach http://127.0.0.1:4096/ "SESSION: Sprint 44 Story 7 — FEAT-443 PAR-Eval & Refusal Interceptor

  CONTEXT:
  - Target files: /home/jallred/Dev_Lab/HomeLabAI/src/nodes/mlx_judge_node.py & src/debug/uber_5x5_v5.py
  - Task: 
    1. Add refusal JSON schema {'refusal': True, 'reason': 'PREMISE_MISMATCH'} to MLXAsyncJudge evaluate_256k_context().
    2. Update evaluate_fidelity() in uber_5x5_v5.py to intercept validated refusal payloads and score them as 5/5 PASS.
  - Test File: Create src/tests/test_par_eval_scoring.py.
  - Validation Gate: Restart lab-attendant.service, run uber_5x5_v5.py --fast, and confirm valid refusal queries pass 5/5."
  ```

---

### 🎴 STORY CARD 8: `FEAT-444` — Judicial Backpressure Ledger (`JUDGE_FIELD_LEDGER.md`)
- **Feature ID**: `FEAT-444` (Proposed / Active)
- **Target Repository & Files**: `HomeLabAI` & `Portfolio_Dev` $\rightarrow$ `src/v5/foyer/router.py`, `field_notes/status.html`, `field_notes/generate_judge_ledger.py`
- **Objective & Technical Spec**: Stream M5 Judge evaluation findings and design critiques to `/field_notes/data/judge_backpressure.jsonl`. Interleave `Amber [JUDGE]` badges on `status.html` live timeline and compile curated design ledger `JUDGE_FIELD_LEDGER.md` for human/architect review.
- **Live-Lab Validation Gate**:
  1. `sudo systemctl restart lab-attendant.service`
  2. Trigger turn trace via live UI, confirm `judge_backpressure.jsonl` appends event.
  3. Verify `status.html` renders `Amber [JUDGE]` badge and `generate_judge_ledger.py` compiles clean Markdown.
- **Spoon-Fed OpenAgent Delegation Command**:
  ```bash
  /home/jallred/.opencode/bin/opencode run --dir /home/jallred/Dev_Lab/Portfolio_Dev --attach http://127.0.0.1:4096/ "SESSION: Sprint 44 Story 8 — FEAT-444 Judicial Backpressure Ledger

  CONTEXT:
  - Target files: 
    1. /home/jallred/Dev_Lab/HomeLabAI/src/v5/foyer/router.py (write judge results to field_notes/data/judge_backpressure.jsonl)
    2. /home/jallred/Dev_Lab/Portfolio_Dev/field_notes/status.html (render Amber [JUDGE] timeline badge)
    3. Create /home/jallred/Dev_Lab/Portfolio_Dev/field_notes/generate_judge_ledger.py to compile JUDGE_FIELD_LEDGER.md.
  - Validation Gate: Restart lab-attendant.service, trigger turn trace, confirm judge_backpressure.jsonl appends, status.html shows Amber badge, and generate_judge_ledger.py outputs markdown."
  ```



