# Retrospective: Phase 9.1 - The Appliance Refactor (March 3, 2026)
**Role: [BKM] - Architectural Hardening & Visibility**

## 🎯 OBJECTIVE
Refactor the monolithic Hub into modular managers (Sensory, Cognitive) and establish "Appliance-Grade" resilience via the persistent Auto-Bounce loop.

## 🏆 VICTORIES
- **Modularization**: Successfully decoupled `acme_lab.py` into `SensoryManager` and `CognitiveHub`. The Hub is now a clean orchestrator.
- **[FEAT-149] Auto-Bounce**: Verified 20s recovery cycle in `SERVICE_UNATTENDED` mode. The Lab is now a self-healing appliance.
- **[FEAT-151] Trace Monitoring**: Implemented "Log Delta Capture" which provides raw trace evidence during API failures. No more "blind" debugging.
- **Montana Centralization**: Centralized log reclamation into `src/infra/montana.py`. Every node now consistently reports with the 4-part fingerprint.
- **Operational Discipline**: Hardened `Protocols.md` to mandate linting for all "Heads Down" work.

## 🩹 SCARS & LESSONS
- **The NameError Trap**: Moving globals to modules (Montana) without a linter check caused `_BOOT_HASH` NameErrors that crashed the Hub. **Lesson**: Proactivity without verification is a regression. Mandate `ruff check`.
- **Race Conditions**: Discovered that the Hub must update the `CognitiveHub` residents stack *immediately* after boot to prevent stale sessions.
- **JSON Extraction**: Confirmed that models (especially 1B/3B) often wrap tool calls in conversational banter. **Fix**: Implemented robust regex extraction `(\{.*\})`.

## 📊 STATE MACHINE (Post-Sprint)
- **Sensory Layer**: 100% Modular.
- **Cognitive Layer**: 100% Modular.
- **Observability Layer**: 100% Centralized.
- **Validation**: `test_goodnight_bounce.py` PASSED with Trace Delta Capture.

## 🚀 NEXT STEPS
- Implement **Phase 3**: `LifecycleManager` to handle process state and systemd handshakes.
- Integrate **[FEAT-150] Shadow Preamble** more deeply into the Intercom UI.
