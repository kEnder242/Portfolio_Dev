# Sprint Plan: [SPR-14.0] The Eternal Forge
**Status:** ACTIVE | **Goal:** Integrate autonomous LoRA training into the nightly cycle and achieve full weight saturation.

## 🕵️ THE FORGE DEPTH & EVOLUTION AUDIT (Mar 17)

This audit is active to ensure the high-fidelity 18-year archive is correctly inducing weights into the Unified 3B Base.

### ✅ Hardening Phase 1 (Complete)
*   **Silicon Handshake [FEAT-219]**: Key-based (MD5 hash of style.css) validation for all Attendant REST endpoints.
*   **Relative Proxy (Option B)**: Unified ingress via `notes.jason-lab.dev/attendant/`.
*   **Heartbeat Bridge**: Added native `/heartbeat` to Hub for truthful liveness reporting.

### 🚧 Hardening Phase 2: Silicon Stability (Active)
*   **Diplomatic Immunity [FEAT-220]**: Cryptographic link between Attendant and children to prevent suicide loops.
*   **PGID Family Purge**: Restoring aggressive process-group reclamation using the immunity gate.
*   **Synchronous Reliability**: Reverted `mcp_start` to deterministic sync execution.

## 🏺 FORENSIC REPORT: THE PGID HISTORY (Mar 17)
*   **Context**: Archive search confirmed PGID was originally chosen to handle deep process trees (vLLM workers).
*   **The Scar**: Recent "friendly fire" crashes were caused by the Master Attendant finding itself in its own name/port search and committing suicide.
*   **The Fix**: Use `_BOOT_HASH` as a `LAB_IMMUNITY_TOKEN`. Mismatch or Absence = Terminate PGID. Match = Immunity.

## 🧪 [DRAFT/EXPERIMENTAL] Unified Origin Architecture
*   **Concept**: Consolidate WebSockets (`/hub`) and API (`/attendant/`) onto the single `notes.jason-lab.dev` domain to solve Zero Trust session splitting.
*   **Logic**: Browser sends the same session cookie for all paths, ensuring 100% auth sync.
*   **Status**: ON HOLD (Reverted to Situation A for stability).

## 🛠️ TASKS
*   [x] **Immunity Injection**: Plumb `_BOOT_HASH` into `mcp_start` environment. ✅
*   [x] **Safe-Assassin**: Upgrade `cleanup_silicon` to use token-aware PGID purging. ✅
*   [ ] **VRAM Watchdog**: Implement [FEAT-180] logic to downshift tiers under pressure.
*   [x] **Crosstalk Migration [FEAT-221]**: Move inter-agent banter to a 1-line status bar and slow down the tick rate. ✅
*   [x] **Cognitive De-Warping [FEAT-222]**: Fix panel routing (Brain=Right, Pinky=Left) and remove yellow crosstalk aesthetics. ✅
*   [ ] **Gauntlet v3.0**: Run `lifecycle_gauntlet.py` to verify the full sequenced forge (3 souls in 1 pass).

## 🏺 FORENSIC RETROSPECTIVE: THE MAR 18 UPLINK BREACH
*   **The Incident**: After Hardening Phase 2, the desktop Intercom became unresponsive ("Stale Uplink").
*   **The False Lead**: I hypothesized a "Zero Trust Session Split" and pivoted to a **Unified Origin** (`/hub` path). This was an overreach that added more complexity without fixing the root cause.
*   **The Smoking Gun**: A `SyntaxError` (Redeclaration of `sl_low`) in `intercom_v2.js` was preventing the script from even attempting a connection.
*   **The Resolution**: Reverted to the stable **Subdomain Model** (Situation A) and surgically fixed the JS syntax error.

## 🩹 SCARS & THRASH (Technical Debt to Fix Later)
1.  **Orphaned Ingress**: The `notes.jason-lab.dev/hub` rule was removed from `config.yml`, but `acme_lab.py` still has the dual-registration code for it. This is harmless but technically "Dead Code."
2.  **JS Selector Fragility**: The `querySelector` for `style.css?v=` is still manual. If `build_site.py` misses a file, the security key will break again.
3.  **VRAM Residency**: Multiple ignition attempts left Ollama with multiple model instances. A host reboot is recommended to clear the ~8GB peak back to the ~2GB baseline.

## 🏺 FORENSIC REPORT: THE UI WARPING (Mar 17)
*   **The Issue**: Messages from 'Brain (Signal)' were bleeding into Pinky's console because the `is_internal` flag was overriding source-based routing. 
*   **The Aesthetic**: The `.internal` CSS class was applying a heavy yellow border and label that cluttered the clinical log view.
*   **The Logic**: Some 'Thinking...' tics were bypassing the crosstalk bar because of inconsistent packet typing.
*   **The Fix**: Prioritize Source (Brain/Pinky) for routing, delete the yellow CSS, and unify all tics under `type: crosstalk`.
