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

### **Follow-on Enhancements & Architectural Polish**

1. **`LAB_INFRASTRUCTURE.md` Ingestion into ChromaDB DNA Flow:**
   - Updated `Portfolio_Dev/sync_chroma_dna.py` to ingest 17 infrastructure & physical floor sections (mounts, GPUs, ports, playbooks) into ChromaDB's `behavioral_dna` collection. Refined `BKM-035` in `Protocols.md` with positive venv execution guidelines. *(Commit: `acc062f`)*

2. **Deep Thought Preamble & Persona Realignment:**
   - Replaced `"Initiating mental synthesis... deep thought in progress."` with `"Listening..."` in `cognitive_hub.py` (Line 1347). *(Commit: `39ca4dc`)*
   - Refactored `PINKY_SYSTEM_PROMPT` in `pinky_node.py` to enforce verbosity matching and positive context fencing. Implemented `self.current_interest = 0.1` tapering on `CASUAL` queries in `cognitive_hub.py`. *(Commit: `a51d669`)*

3. **Status.html Expanding Folders Fix:**
   - Updated day folder rendering in `Portfolio_Dev/field_notes/status.html` to default all day folders (`📅 Jul 22, 2026 (123 logs)`) to collapsed while persisting user open state across 5s live refreshes via `window._userOpenDayFolders`. *(Commit: `087de5e`)*

4. **Unified Mission Control Sidebar & Filing Cabinet Decommissioning:**
   - Removed redundant mini-tree `<section id="filing-cabinet">` from `intercom.html` and `lab.html`.
   - Re-architected `<mission-control>` web component in `mission-control.js` into a unified component featuring `← Return to Front Page`, `Public Airlock` explicit links (`www.jason-lab.dev`), and `Mission Control` boundary separator with `🔒` internal links (`notes.jason-lab.dev`).
   - Simplified `sync_stories.sh`, `sync_protocols.sh`, and `sync_research.sh` to copy `mission-control.js` into `www_deploy` without regex surgery. *(Commit: `16a0424` & `c7076df`)*

