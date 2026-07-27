# Master Sprint Plan: Sprint 46 — Progressive Cooldown, Heap Trimming, Open HyDE & Async Sanity Critic

> **Sprint Narrative:**
> Following system memory audits and operational feedback, Sprint 46 establishes complete memory self-governance and advanced RAG retrieval across the Federated Lab. It implements a 3-tier **Progressive Cooldown Engine** (`FEAT-428`), a **Poison Chunk Quarantine Protocol** (`FEAT-429`), an automated **Foyer C-Arena Heap Trimming Sentinel** (`FEAT-430`), an **Open HyDE Preamble Preprocessor** (`FEAT-432`) using Pinky's spoken hypothesis for ChromaDB vector search, and an **Asynchronous Sanity Critic Protocol** (`FEAT-433`) for non-blocking factual verification.

---

## 🏛️ Target Files & Feature Mapping

1. **`FEAT-428` — Progressive Cooldown Engine:**
   - **Target Files:** `Portfolio_Dev/field_notes/scan_queue.py`, `Portfolio_Dev/field_notes/nibble_v2.py`
   - **Mechanism:** Progressive yield counter (`consecutive_yields`). 1st Yield: 15s delay. 2nd Yield: 60s delay. 3rd+ Yield: `COOLDOWN` state (15m sleep, muted logs).

2. **`FEAT-429` — Poison Chunk Quarantine Protocol:**
   - **Target Files:** `Portfolio_Dev/field_notes/scan_queue.py`, `Portfolio_Dev/field_notes/nibble_v2.py`
   - **Mechanism:** Chunk-level failure tracker (`consecutive_failures`). Tag chunks failing 3x as `QUARANTINED` in `chunk_state.json`.

3. **`FEAT-430` — Foyer C-Arena Heap Trimming Sentinel:**
   - **Target Files:** `HomeLabAI/src/v5/foyer/router.py`, `HomeLabAI/src/v5/ignition/manager.py`
   - **Mechanism:** Periodic `malloc_trim(0)` execution in Foyer's idle cleanup loop to stabilize process RSS < 1.0 GB.

4. **`FEAT-432` — Open HyDE Preamble Preprocessor:**
   - **Target Files:** `HomeLabAI/src/nodes/archive_node.py`, `HomeLabAI/src/logic/cognitive_hub.py`
   - **Mechanism:** Pinky's open streaming preamble roleplay serves as the HyDE hypothetical document generator. Her spoken hypothesis text is vectorized into ChromaDB to retrieve target BKMs with 95%+ precision without extra hidden LLM latency.

5. **`FEAT-433` — Asynchronous Sanity Critic Protocol:**
   - **Target Files:** `HomeLabAI/src/logic/cognitive_hub.py`, `HomeLabAI/src/v5/foyer/router.py`, `Portfolio_Dev/field_notes/intercom_v2.js`
   - **Mechanism:** Fires a non-blocking background task (`asyncio.create_task`) after the initial turn response streams. Evaluates response against historical BKMs and streams a `sanity_check` WebSocket payload to render a live **"🛡️ Sanity Verified"** badge on the Intercom card.

---

## 📜 Story Backlog & Implementation Tasks

### **Story 1: `FEAT-428` — Progressive Cooldown Engine**
- **Target Files:** `Portfolio_Dev/field_notes/scan_queue.py`, `Portfolio_Dev/field_notes/nibble_v2.py`
- **Tasks:**
  1. Add `consecutive_yields` state tracking to `should_yield()` in `nibble_v2.py`.
  2. Implement progressive sleep scaling: 15s on 1st yield, 60s on 2nd yield, 900s (15 min) on 3rd+ yield.
  3. Suppress redundant log output during the 15-minute `COOLDOWN` window.
  4. Reset `consecutive_yields` to 0 upon a clean, uninhibited chunk execution.

---

### **Story 2: `FEAT-429` — Poison Chunk Quarantine Protocol**
- **Target Files:** `Portfolio_Dev/field_notes/scan_queue.py`, `Portfolio_Dev/field_notes/nibble_v2.py`
- **Tasks:**
  1. Add `failure_count` per chunk in `data/chunk_state.json`.
  2. Increment `failure_count` upon exception or invalid JSON response.
  3. When `failure_count >= 3`, mark chunk `status = "QUARANTINED"`.
  4. Update `scan_queue.py` filtering to skip `QUARANTINED` chunks.

---

### **Story 3: `FEAT-430` — Foyer C-Arena Heap Trimming Sentinel**
- **Target Files:** `HomeLabAI/src/v5/foyer/router.py`, `HomeLabAI/src/v5/ignition/manager.py`
- **Tasks:**
  1. Add `ctypes.CDLL('libc.so.6').malloc_trim(0)` to `delayed_shutdown` and idle maintenance loops in `router.py`.
  2. Call `malloc_trim(0)` after request completion to return freed PyTorch C-arenas back to OS `MemAvailable`.

---

### **Story 4: `FEAT-432` — Open HyDE Preamble Preprocessor**
- **Target Files:** `HomeLabAI/src/nodes/archive_node.py`, `HomeLabAI/src/logic/cognitive_hub.py`
- **Tasks:**
  1. Capture Pinky's streaming preamble output in `cognitive_hub.py`.
  2. Pass preamble hypothesis string to `archive_node.py` prior to RAG candidate retrieval.
  3. Vectorize hypothesis string into ChromaDB to fetch target BKMs.

---

### **Story 5: `FEAT-433` — Asynchronous Sanity Critic Protocol**
- **Target Files:** `HomeLabAI/src/logic/cognitive_hub.py`, `Portfolio_Dev/field_notes/intercom_v2.js`
- **Tasks:**
  1. Create non-blocking background evaluator (`evaluate_response_async`) in `cognitive_hub.py`.
  2. Broadcast `sanity_check` payload with confidence score over WebSocket.
  3. Update `intercom_v2.js` to render live **"🛡️ Sanity Verified"** badge on message cards.

---

## 🤖 OpenAgent Delegation Playbook (BKM-034 Point 12 Compliance)

Launch OpenAgent attached to port 4096 using the command:

```bash
/home/jallred/.opencode/bin/opencode run --dir /home/jallred/Dev_Lab/Portfolio_Dev --attach http://127.0.0.1:4096/ "Read file:///home/jallred/Dev_Lab/Portfolio_Dev/SPRINT_PLAN_SPR_46_0.md and execute Stories 1 through 5 (FEAT-428, FEAT-429, FEAT-430, FEAT-432, FEAT-433). Follow all acceptance criteria and verify tests pass."
```

---

## 🧪 Acceptance Criteria & Test Verification
- [ ] `nibble_v2.py` enters 15-minute `COOLDOWN` after 3 consecutive yields.
- [ ] Chunks failing 3 consecutive times are marked `QUARANTINED` in `chunk_state.json`.
- [ ] `malloc_trim(0)` runs periodically in `foyer/router.py`, maintaining `acme_foyer_v5` RSS < 1.0 GB.
- [ ] Pinky preamble text vectorizes via ChromaDB as the Open HyDE preprocessor (`FEAT-432`).
- [ ] Non-blocking Async Sanity Critic (`FEAT-433`) streams verification badge to Intercom UI without delaying initial response.
- [ ] All workspace git repositories remain clean and aligned on `main`.
