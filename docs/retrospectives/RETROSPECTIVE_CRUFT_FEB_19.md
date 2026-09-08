# Retrospective: Technical Debt & Cruft (Feb 19)

### 🏚️ Architectural Warp
The following logic was introduced as experimental "Band-Aids" and remains in the core `acme_lab.py`:

1.  **Nested Dispatcher:** `execute_dispatch` is currently an inner function of `process_query`. This was done to capture local scope during parallel task execution, but it should be refactored into a class method.
2.  **Architect's Raw Shunt:** Line 357 in `acme_lab.py` contains a hard-coded `if source == "Brain"` check to bypass JSON parsing. This is a "Non-Starter" idea that worked for this session but breaks the "Everything is a Tool" contract.
3.  **Amygdala Placeholder:** `is_strategic = True` is hard-coded for non-mic interactions. This was an experimental way to force the Brain to speak, bypassing the intent-detection that was failing earlier.

### 🧟 Zombie Configurations
- **`USE_BRAIN_VLLM`**: Still being injected into nodes despite vLLM being tabled.
- **`BRAIN_MODEL`**: Hard-coded to `LARGE` in the environment to force Llama 3.1, bypassing the Attendant's more flexible mapping logic.

### 📂 File System Residue
The `HomeLabAI/src/debug/` folder now contains:
- `vllm_zombie_check.py`: Our #1 diagnostic, but no longer needed for production.
- `long_burn_check.py`: The 10-minute patience monitor.
- `vacuum_sentinel.sh`: The aggressive "Amputation" script used for driver swaps.
- `*.patch`: Multiple manual fixes that were never integrated into a clean versioning system.

### 📍 Recovery Breadcrumbs
- `HomeLabAI/src/acme_lab.py`: Lines 330-450 contain the bulk of the session's "warped" logic.
- `Portfolio_Dev/field_notes/intercom_v2.js`: Lines 120-150 contain the new "Clear Flag" and source-routing logic which may need future hardening.
