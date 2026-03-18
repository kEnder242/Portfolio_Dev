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

## 🛠️ TASKS
*   [ ] **Immunity Injection**: Plumb `_BOOT_HASH` into `mcp_start` environment.
*   [ ] **Safe-Assassin**: Upgrade `cleanup_silicon` to use token-aware PGID purging.
*   [ ] **VRAM Watchdog**: Implement [FEAT-180] logic to downshift tiers under pressure.
*   [ ] **Gauntlet v3.0**: Run `lifecycle_gauntlet.py` to verify the full sequenced forge (3 souls in 1 pass).
