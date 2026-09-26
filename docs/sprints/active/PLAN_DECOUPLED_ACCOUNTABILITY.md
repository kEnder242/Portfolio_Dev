# Sprint / Architecture Plan: Decoupled Morning Accountability Watchdog (FEAT-619 & BKM-066)

**Goal:** Decouple the Daily Accountability Audit from the internal control flow of `nightly_forge.py`. Establish an independent, out-of-band Morning Accountability Watchdog that executes at the conclusion of the nightly maintenance window (06:00 AM) to independently audit telemetry, detect silent crashes / deadlocks / OOM kills, and guarantee authoritative `daily_accountability_digest.json` generation.

---

## 🏛️ Architectural Principles (BKM-066)
1. **Separation of Execution and Auditing:** "Never let the executing process be solely responsible for grading its own completion." If `nightly_forge.py` segfaults, OOM-dies, or terminates unexpectedly, an external auditor MUST catch the absence of completion and sound the alarm.
2. **Out-of-Band Audit Inputs:** The watchdog inspects:
   - `HomeLabAI/run/nightly_forge_state.json` & `nightly_forge.lock`
   - `HomeLabAI/run/nightly_lora_training_state.json`
   - Raw step logs (`/tmp/nightly_forge_step.log`, `HomeLabAI/run/nightly_forge.log`)
   - Running daemons via REST (`Foyer :8765`, `Chroma :8001`, `vLLM :8088`)
   - Physical GPU state (`nvidia-smi` power clamp & memory status)
   - Live Synthetic Morning Round Table Probe (`probe_round_table_accountability.py`)
3. **Dead-Man Switch / Liveness Invariant:** If `nightly_forge` did not record `status: COMPLETED` with a timestamp inside the last 24 hours, the watchdog classifies the night as `CRITICAL_FAIL (SILENT_ABORT_OR_CRASH)`, generates the failure digest, and fires Neural Pager alerts.

---

## 🔬 Component Breakdown

### 1. `HomeLabAI/src/infra/standalone_accountability_watchdog.py` (FEAT-619)
- Independent CLI entrypoint executable via cron/systemd at 06:00 AM or on-demand:
  `HomeLabAI/.venv/bin/python3 -m infra.standalone_accountability_watchdog [--force] [--json]`
- Implements 7 decoupled audit checks:
  1. `GPU Power Limit Clamp`: Live nvidia-smi check (<= 170W).
  2. `VRAM & Engine State`: Verifies Foyer/vLLM operational.
  3. `Nightly Forge State Liveness`: Audits `nightly_forge_state.json` timestamp & completion status.
  4. `LoRA Multi-Adapter Pass`: Audits `nightly_lora_training_state.json` and adapter artifact directories in `/speedy/models/adapters/`.
  5. `Subconscious Dreaming & Deduplication`: Audits gems & wisdom card refinement counts.
  6. `Synthetic Morning Round Table Probe`: Runs live end-to-end conversation probe.
  7. `Stale Lock & Crash Sentry`: Detects lingering `.lock` files without active PIDs.
- Emits atomic `Portfolio_Dev/field_notes/data/daily_accountability_digest.json` and mirrors to `www_deploy/data/`.
- Broadcasts Neural Pager / Intercom alert if `status != PASS`.

### 2. Protocol & Feature Indexing
- `BKM-066`: Decoupled Watchdog & Independent Audit Invariant.
- `FEAT-619`: Standalone Morning Accountability Watchdog.
