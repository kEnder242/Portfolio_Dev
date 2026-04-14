# Sprint Plan: [SPR-20.0] Mind Healing & Stability
**Status:** PLANNED | **Goal:** Resolve triage deadlocks and restore cognitive continuity.

---

## 🏛️ Section 1: FORENSIC CRASH REPORT (Verbatim)

#### 1. The Core Crash (The "Why")
The conversation crashed because of two interlocking logical failures in `cognitive_hub.py` that surfaced during your live trial:

*   **[ERR-05] AttributeError: `brain_online`**: In Turn 131, I refactored the Hub to use a callback for Brain health, but I missed the `run_shadow` method. When the model attempted a shadow interjection, it called `self.brain_online()` (the old way) instead of using the new callback, causing the entire query task to die instantly.
*   **[ERR-06] Triage JSON Type Mismatch**: The `lab` node, when called over stdio, is returning a Python **Dictionary** for its triage hint. The Hub's triage loop is currently hardcoded to expect a **String** and tries to `json.loads` it. This triggers a `TypeError`, exhausting all 3 triage attempts and leading to the **☢️ SILICON LOBOTOMY** warning.

#### 2. Comprehensive Error Ledger (Outstanding)

| Error ID | Symbol / Message | Physical Cause | Impact |
| :--- | :--- | :--- | :--- |
| **ERR-05** | `AttributeError` | Call site mismatch in `run_shadow` method. | **FATAL.** Kills the query task immediately. |
| **ERR-06** | `TypeError: JSON object must be str` | Hub double-parsing a raw dict from the node. | **STALL.** Causes triage to fail and query to be dropped. |
| **ERR-07** | `Cognitive processing failed` | Hub-side broadcast after task group crash. | **USER NOISE.** Tells the user something is wrong but doesn't fix it. |
| **ERR-08** | `Wait-Ready request failed` | Attendant API timing out during heavy JIT loads. | **SYNC LOSS.** Foyer thinks Lab is dead when it's just slow. |

---

## 🏗️ Section 2: Technical Fix Architecture & Connectivity

### 1. The "Callback Alignment" (Resolving ERR-05)
*   **Path:** `HomeLabAI/src/logic/cognitive_hub.py`
*   **Description:** The Hub has transitioned from an internal attribute-based state (`self.brain_online`) to a callback-driven state (`self.get_vram_status()`) to maintain 127.0.0.1 alignment with the Attendant.
*   **Fix:** We must surgically audit all call sites in `process_query` and its sub-methods (`run_shadow`, `run_pinky`, and the Brain streaming block). 
*   **Surgical Analysis:** Nearby code including the `asyncio.gather` and `_process_node_stream` calls is physically stable and should NOT be modified. We are only changing the **Boolean source** for the shadow failover check.

### 2. The "Triage Type Guard" (Resolving ERR-06)
*   **Path:** `HomeLabAI/src/logic/cognitive_hub.py`
*   **Description:** When the `lab_node` returns its triage hint via MCP tool-call, the stdio transport sometimes returns a raw Python dictionary instead of a JSON-string. 
*   **Fix:** The Hub's triage loop (approx. line 355) must implement a type check: `if isinstance(raw_t_text, dict): return raw_t_text`. 
*   **Connectivity:** This fix is the "Pre-requisite" for the entire conversation. If triage fails, the Hub defaults to "CASUAL" or "ERROR," silencing the strategic adapters.

### 3. The "Neural Buffer" [FEAT-283]
*   **Path:** `HomeLabAI/src/acme_lab.py`
*   **Description:** Currently, any query sent while the engine is in the 60s Triton settle window is rejected and lost.
*   **Fix:** Implement an `asyncio.Queue` in the `client_handler`. If `self.status != "OPERATIONAL"`, the message is pushed to the queue. Once the `engine_ready` event is set, a background "Drainer" task pops and dispatches.
*   **Blocker Risk:** Race conditions between the WebSocket receiver and the Queue drainer. We must ensure the queue only starts draining *after* the `Mind is READY` broadcast.

### 📉 Code Morphism & TLC Analysis
Over the last several turns, the code has shifted from **Sequential Blockers** to **Parallel Background Tasks**. This has improved responsiveness but introduced **State Ambiguity**. 
*   **TLC Needed:** `check_brain_health` in `acme_lab.py` now has complex nested background tasks (`_bg_prime`). We need to ensure these don't orphan if the Hub is restarted. 
*   **The Lesson:** "Truth Gating" (the functional ping) has revealed the true latency of the hardware (~120s). The Hub logic must now be hardened to survive this "Dark Window" without crashing its internal tasks.

---

## 📝 Section 3: Tasks & Tracking

### 🛠️ New Sprint Tasks (Mind Healing)
- [ ] **Task 1: Resolve Hub Callback Mismatch (ERR-05)**
    - Target: `cognitive_hub.py`. Replace all `brain_online()` with `get_vram_status()`.
- [ ] **Task 2: Resolve Triage Type Mismatch (ERR-06)**
    - Target: `cognitive_hub.py`. Implement `isinstance(dict)` check in triage loop.
- [ ] **Task 3: Implement [FEAT-283] Neural Buffer**
    - Target: `acme_lab.py`. Create `self._neural_queue` and implement the "Wait-for-Wake" drainer.
- [ ] **Task 4: Attendant API Resilience (ERR-08)**
    - Target: `lab_attendant_v4.py`. Increase `handle_wait_ready_rest` timeout to 30s.

### 🖇️ Stragglers from SPR-19.0
- [ ] **Verify L2 Weight Mapping Latency**: Confirm if the 180s post-restoration timeout in `test_hibernation_cycle.py` is sufficient for a 100% pass.
- [ ] **Verify [FEAT-287] Activity Latch**: Confirm in a multi-turn session that typing "Resets" the 120s prime cooldown.
- [ ] **Audit `active_pids.json`**: Ensure the PID Ledger correctly reclaims ports after a hard service crash without leaving "Ghost Contexts."

---
**Governing Standard:** [BKM-020] High-Fidelity Sprint Documentation & [BKM-023] Surgical Preservation Protocol.
