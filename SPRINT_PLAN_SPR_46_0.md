# Master Sprint Plan: Sprint 46 — Progressive Cooldown Engine, Poison Quarantine & Foyer Heap Trimming

> **Sprint Narrative:**
> Following system memory audits and operational feedback, Sprint 46 establishes complete memory self-governance across the Federated Lab. It implements a 3-tier **Progressive Cooldown Engine** (`FEAT-428`) to eliminate sentinel polling hammering, a **Poison Chunk Quarantine Protocol** (`FEAT-429`) to isolate failing note chunks, and an automated **Foyer C-Arena Heap Trimming Sentinel** (`FEAT-430`) to prevent PyTorch/CPython memory bloat in `acme_foyer_v5`.

---

## 🏛️ Target Files & Feature Mapping

1. **`FEAT-428` — Progressive Cooldown Engine:**
   - **Target Files:** `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/scan_queue.py`, `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/nibble_v2.py`
   - **Mechanism:** Progressive yield counter (`consecutive_yields`). 
     - 1st Yield: 15s delay.
     - 2nd Yield: 60s delay.
     - 3rd+ Consecutive Yield: Enters `COOLDOWN` state (15-minute sleep, muted polling logs).

2. **`FEAT-429` — Poison Chunk Quarantine Protocol:**
   - **Target Files:** `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/scan_queue.py`, `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/nibble_v2.py`
   - **Mechanism:** Chunk-level failure tracker (`consecutive_failures`).
     - If a note chunk fails 3 consecutive times due to context overflow, JSON parse error, or HTTP failure, tag status as `QUARANTINED` in `chunk_state.json`.
     - Queue sweeps automatically bypass `QUARANTINED` files.

3. **`FEAT-430` — Foyer C-Arena Heap Trimming Sentinel:**
   - **Target Files:** `/home/jallred/Dev_Lab/HomeLabAI/src/v5/foyer/router.py`, `/home/jallred/Dev_Lab/HomeLabAI/src/v5/ignition/manager.py`
   - **Mechanism:** Periodic `malloc_trim(0)` execution in Foyer's idle cleanup loop.
     - Trims CPython memory arena bloat in resident node sub-processes (`Pinky`, `Brain`, `Archive`, `Thought`, `Lab`), stabilizing Foyer process RSS at ~800 MB.

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

## 🤖 OpenAgent Delegation Playbook (BKM-034 Point 12 Compliance)

> **Delegation Learning:** Never pass long inline instruction blocks via the CLI. Point OpenAgent directly to this Sprint Plan file!

Launch OpenAgent attached to port 4096 using the command:

```bash
/home/jallred/.opencode/bin/opencode run --dir /home/jallred/Dev_Lab/Portfolio_Dev --attach http://127.0.0.1:4096/ "Read file:///home/jallred/Dev_Lab/Portfolio_Dev/SPRINT_PLAN_SPR_46_0.md and execute Story 1 (FEAT-428), Story 2 (FEAT-429), and Story 3 (FEAT-430). Follow all acceptance criteria and verify tests pass."
```

---

## 🧪 Acceptance Criteria & Test Verification
- [ ] `nibble_v2.py` enters 15-minute `COOLDOWN` after 3 consecutive yields.
- [ ] Sentinel log output is suppressed during `COOLDOWN`.
- [ ] Chunks failing 3 consecutive times are marked `QUARANTINED` in `chunk_state.json`.
- [ ] `scan_queue.py` bypasses `QUARANTINED` chunks without stopping queue progression.
- [ ] `malloc_trim(0)` runs periodically in `foyer/router.py`, maintaining `acme_foyer_v5` RSS < 1.0 GB.
- [ ] All workspace git repositories remain clean and aligned on `main`.
