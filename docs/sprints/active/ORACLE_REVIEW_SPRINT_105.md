# 🔮 Adversarial Oracle Audit Report: Sprint 105 Phase 2

**Sprint:** SPR-105.0 (Phase 2)  
**Evaluator:** Cloud Oracle (`openrouter/nvidia/nemotron-3-super-120b-a12b:free` via `delegate.py --oracle`)  
**Timestamp:** 2026-10-17T00:52:14Z  
**Session ID:** `ses_eb728ab75ffelOOY6bOZ73VhIS`  
**Governing BKMs & Invariants:** `[BKM-007]`, `[BKM-020]`, `[BKM-024]`, `[BKM-049]`, `[BKM-080]`, `[BKM-081]`, `[BKM-082]`, `[BKM-086]`, `[FEAT-451]`, `[FEAT-330]`, `[FEAT-619]`, `[FEAT-523]`, `[FEAT-416]`, `[INS-047]` ("Live is King, History is Queen")  

---

## Story-by-Story Adversarial Findings

### Story 105.6: RAG-First Ripgrep Expansion Pipeline
* **Race Conditions / Concurrency:** High risk in `cognitive_hub.py` where `execute_grep_search_pivot` output is appended to prompt context. Concurrent turns could cause interleaved prompt context if shared variables are mutated.
* **Mitigation Directives:**
  - Keep grep context scoped strictly to local function variables within the active turn thought trace.
  - Bound `/usr/bin/rg` execution with a strict `timeout=1.5s` and `--max-count 5` to prevent sub-process hang under parallel queries.

### Story 105.7: Nibbler McpClient Authentication & Groundhog Loop Unblock
* **Race Conditions / Contention:** HTTP token retrieval from `http://127.0.0.1:8765/status` followed by WebSocket connection creates a TOCTOU window where token expiration or port contention blocks authentication.
* **Mitigation Directives:**
  - Read `X-Lab-Key` directly from the local environment variable `LAB_ATTENDANT_KEY` or `HomeLabAI/config/foyer_key.json` rather than introducing a circular network dependency on an HTTP status endpoint.
  - Fall back to static lab key config if port 8765 HTTP probe is unavailable.

### Story 105.8: Accountability Watchdog Green Lie Excision & Freshness Verification
* **Race Conditions / Thresholds:** File `mtime` check followed by action creates classic TOCTOU window. Additionally, a static 86400s threshold may trip false alarms if nightly runs complete slightly past 06:00 AM.
* **Mitigation Directives:**
  - Check file `stat().st_mtime` once and capture both timestamp and file size in a single atomic inspection.
  - Set freshness tolerance to 30 hours (108,000s) to comfortably span the 24-hour nightly window without false positive alarms on day-boundary shifts.

### Story 105.9: Dedicated Nightly Batch Window for Nibbler & 24/7 Polling Suppression
* **Temporal Drift / Systemd:** `systemd` user timers must account for local time and system sleep states.
* **Mitigation Directives:**
  - Use `Persistent=true` in `field-notes-nightly.timer` so missed runs (e.g. machine asleep) execute upon wake.
  - In `nibble_v2.py`: Enforce daytime quiet hours (07:00 AM – 02:00 AM) unless `--force` or `--once` is explicitly commanded.

### Story 105.10: Post-Waterfall Learning Target Queueing
* **Race Conditions / Concurrency (CRITICAL):** Multiple `cognitive_hub` turns appending to `Portfolio_Dev/field_notes/data/queue.json` without file locking will corrupt the JSON file or drop learning targets.
* **Mitigation Directives:**
  - Implement atomic file operations using `tempfile.NamedTemporaryFile` + atomic rename (`os.replace`) or `fcntl.flock` to guarantee transactional queue appends.
  - Maintain a set of existing queue anchors in memory to deduplicate identical targets within a 24-hour window.

### Story 105.11: Continuous Ceiling-Only Headroom & Prompt De-Fluffing
* **Degradation / Under-Synthesis:** Eliminating token floors carries a risk that complex technical prompts under-synthesize if prompts over-index on brevity.
* **Mitigation Directives:**
  - On high-interest technical modes ($interest \ge 0.8$), phrase the budget prompt affirmatively: *"Headroom ceiling is {ceiling} tokens. Deliver a complete, high-authority engineering synthesis within this ceiling; do not add conversational fluff or padding."*
  - Ensure `max_tokens` passed to the physical LLM runner (`vLLM`/`Ollama`) matches the calculated ceiling to provide physical silicon protection.

---

## Pre-Flight Verdict & Action Items
* **Verdict:** PROCEED TO EXECUTION WITH MITIGATIONS.
* **Required Plan Adjustments:**
  1. Add atomic file locking (`fcntl` / `os.replace`) to Story 105.10 specs.
  2. Direct Story 105.7 to source `X-Lab-Key` from config/environment rather than an ephemeral HTTP status route.
  3. Ensure Story 105.11 preserves high-interest technical substance while eliminating fluff.
