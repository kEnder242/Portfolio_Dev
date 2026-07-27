# Master Sprint Plan: Sprint 46 — Progressive Cooldown Engine & Poison Chunk Quarantine

> **Sprint Narrative:**
> Following the memory sentinel recalibrations in Sprint 44/45 and the system triage in Sprint 45, Sprint 46 establishes robust operational self-governance for the background note refinement pipeline (`scan_queue.py` & `nibble_v2.py`). It implements a 3-tier **Progressive Cooldown Engine** (`FEAT-428`) to eliminate tight-loop log spam and sentinel hammering, alongside a **Poison Chunk Quarantine Protocol** (`FEAT-429`) to isolate broken or context-overflowing note files from infinite retry sweeps.

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

---

## 📜 Story Backlog & Detailed Implementation Tasks

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

## 🤖 OpenAgent Delegation Playbook (BKM-034 Point 12 Compliance)

When delegating Story 1 & Story 2 to OpenAgent via the OpenCode CLI, execute the exact command below attached to port 4096:

```bash
/home/jallred/.opencode/bin/opencode run --dir /home/jallred/Dev_Lab/Portfolio_Dev --attach http://127.0.0.1:4096/ "SESSION: Sprint 46 Story 1 & 2 — Progressive Cooldown Engine (FEAT-428) & Poison Chunk Quarantine (FEAT-429). Implement 3-tier progressive backoff in nibble_v2.py/scan_queue.py (15s -> 60s -> 15m COOLDOWN) and quarantine chunks failing 3 consecutive times as QUARANTINED in chunk_state.json."
```

---

## 🧪 Acceptance Criteria & Test Verification
- [ ] `nibble_v2.py` enters 15-minute `COOLDOWN` after 3 consecutive yields under low RAM or non-IDLE mode.
- [ ] Sentinel log output is suppressed during `COOLDOWN`.
- [ ] Chunks failing 3 consecutive times are marked `QUARANTINED` in `chunk_state.json`.
- [ ] `scan_queue.py` bypasses `QUARANTINED` chunks without stopping queue progression.
- [ ] All workspace git repositories remain clean and aligned on `main`.
