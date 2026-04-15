# Sprint Plan: [SPR-21.0] WD Actions (Watchdog Sovereignty)
**Status:** DRAFT | **Goal:** Rebuild the Lab Attendant's internal watchdog to restore autonomous recovery capabilities.

---

## 🏛️ Section 1: Brainstorming & Architecture (The "Why")

**Core Problem:** A deep forensic review confirmed that the `vram_watchdog_loop` in `lab_attendant_v4.py` is an empty stub. The advanced logic from `v1` was lost.

**The Watchdog's Purpose:** The internal `vram_watchdog_loop` must be rebuilt to monitor VRAM ghosts and Hub liveness on port 8765.

---

## 🛠️ Section 2: Tasks & Tracking
- [ ] **Task 1: Rebuild Watchdog Core Logic**
- [ ] **Task 2: Implement Recovery Actions**
