# Master Sprint Plan: Sprint 44 — Lab Resilience, Memory Guardrails & Telemetry Visibility

> **Sprint Narrative:**
> As our Federated Lab expands with active AI subagent swarms and high-density RAG synthesis, memory stability on our 16 GB host (`z87-Linux`) is paramount. Sprint 44 focuses on transforming the Lab from reactive memory recovery to proactive memory governance. We will enforce strict RAM sentinels for background scanners, implement the "Emergency Deafness" policy to protect system headroom, eliminate duplicate PyTorch/SentenceTransformer RAM allocations, restore the true Vocal Probe BKM, and surface real-time vLLM engine health and errors directly into `status.html`.

---

## 🎯 Master Architecture Goals

1. **Memory Pressure Protections (`LAB-088` & `LAB-089`):**
   - EarNode pre-loads on startup for VRAM allocation hygiene, but automatically unloads under RAM pressure (`available_ram < 3.0 GB`) or during Swarm / Heads-Down mode. Re-enabled for manual integration testing.
   - Nibbler (`nibble_v2.py`) is strictly **IDLE ONLY** (Priority 0: Evict First), requiring pre-flight RAM checks (`available_ram >= 3.0 GB`) before every chunk pass.

2. **Shared Vector Embedding Service:**
   - Consolidate PyTorch and `SentenceTransformer` imports across `archive_node.py` and `bridge_burn_to_rag.py` into a single shared HTTP/socket embedding daemon, saving ~1.5 GB RAM.

3. **Vocal Probe Enforcement & Interleaved Log Error Visibility:**
   - Restore the full Vocal Probe (`/v1/chat/completions` token check with `unified-base`) in `loader.py` instead of trusting `/v1/models` (`200 OK`).
   - Wire vLLM engine errors directly to `trigger_pager()` for display on `status.html`.

4. **Git & Scanner Hardening (`BKM-035`):**
   - Delete duplicate `Portfolio_Dev/venv/` and enforce git curation.
   - Harden `scan_artifacts.py` so LLM fallback failures never overwrite rich AI synopses with generic `"Heuristic"` placeholders.

---

## 📜 Story Backlog & Detailed Implementation Tasks

### **Story 1: `LAB-088` / `FEAT-420` — Emergency Deafness & EarNode Lifecycle Management**
- **Rationale:** Prevent NeMo EarNode (~2.5 GB RAM / ~1.0 GB VRAM) from causing memory lockups during subagent swarms or RAG synthesis.
- **Mechanism:**
  - Keep startup pre-loading for contiguous CUDA VRAM organization on RTX 2080 Ti.
  - Add `unload_sensory_ear()` trigger in Foyer Router whenever `available_ram < 3.0 GB` or Swarm / Heads-Down mode is declared.
  - Re-arm EarNode upon manual integration test request.
- **Proof:** Run memory stress probe while initiating subagent swarm; verify EarNode drops cleanly and available RAM remains > 3.0 GB.

---

### **Story 2: `LAB-089` / `FEAT-421` — Idle-Only Nibbler & RAM Sentinel**
- **Rationale:** Nibbler is continuous background refinement and must yield to all interactive/agentic tasks.
- **Mechanism:**
  - In `nibble_v2.py` / `scan_queue.py`, add pre-flight check:
    `if available_ram < 3.0 GB or active_locks: sleep(30); yield`
  - Re-design Nibbler to check system load average (< 2.0) before every chunk summary.
- **Proof:** Trigger heavy load or subagent task; verify Nibbler logs `[NIBBLER] Yielding: Memory/Load Pressure` and consumes zero CPU/RAM.

---

### **Story 3: Shared Embedding Daemon (PyTorch RAM Deduplication)**
- **Rationale:** Eliminate duplicate PyTorch + SentenceTransformer loads across `archive_node.py` and `bridge_burn_to_rag.py`.
- **Mechanism:**
  - Route all RAG vector embeddings through the persistent ChromaDB HTTP daemon on port 8001 (or a single FastEmbed service).
  - Remove direct `SentenceTransformer` imports from `archive_node.py`.
- **Proof:** Check `ps aux --sort=-%mem`; verify total memory saved is ~1.5 GB.

---

### **Story 4: Interleaved Log Error Visibility & Vocal Probe Enforcement**
- **Rationale:** Never trust `200 OK` on `/v1/models`. Surface real engine errors to the user UI.
- **Mechanism:**
  - Restore full Vocal Probe (`/v1/chat/completions` with payload `{"model": "unified-base", "messages": [{"role": "user", "content": "Respond with SUCCESS."}]}`) in `src/nodes/loader.py`.
  - Pass vLLM stream errors (`r.status != 200`) to `trigger_pager()`, writing directly to `pager_activity.json`.
- **Proof:** Simulate engine failure; verify red alert appears on `status.html` log tree.

---

### **Story 5: Scanner Hardening & Git Hygiene Cleanup (`BKM-035`)**
- **Rationale:** Prevent loss of rich AI synopses in `artifacts_*.json` and eliminate virtualenv indexing bloat.
- **Mechanism:**
  - Delete `Portfolio_Dev/venv/`.
  - Update `scan_artifacts.py`: if `ENGINE.generate()` fails or returns None, preserve `existing_map[filename]` AI entry instead of overwriting with `method: "Heuristic"`.
- **Proof:** Run `scan_artifacts.py` with offline engine; verify `artifacts_DOCS.json` preserves all 360 high-fidelity AI synopses.

---

## 🧪 Verification & Acceptance Criteria
- [ ] Available system RAM remains > 3.0 GB during active development and subagent runs.
- [ ] EarNode pre-loads on boot but unloads cleanly under pressure or during Swarm mode.
- [ ] Nibbler runs strictly during idle periods and yields immediately under load.
- [ ] vLLM engine errors appear on `status.html` interleaved timeline.
- [ ] High-fidelity AI synopses in `artifacts_*.json` are protected against fallback erasures.
