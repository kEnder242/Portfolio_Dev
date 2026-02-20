# 🧭 Portfolio_Dev Master Index
**"The Map Room"**

This document serves as the primary navigational hub for the `Portfolio_Dev` repository. Use this to orient yourself, locate specific architectural details, or understand the project's history.

## 📍 Primary Entry Points
*   **[README.md](./README.md)**: **The Public Face.** High-level project overview, philosophy ("Class 1"), and usage commands.
*   **[GEMINI.md](./GEMINI.md)**: **The Agent Manifesto.** The active state machine, current phase checklist, and core mandates. **Start here for context.**
*   **[FeatureTracker.md](./FeatureTracker.md)**: **The God View.** Current Tier 1 milestones and architectural roadmap.

## 📐 Architecture & Logic
*   **[FIELD_NOTES_ARCHITECTURE.md](./FIELD_NOTES_ARCHITECTURE.md)**: **The Blueprints.**
    *   System Topology (Librarian/Nibbler/Pinky).
    *   **Access Control Layer:** (New) BKM for Cloudflare Access Requests.
    *   Fragility Report (Mobile caching, JSON hallucination).
*   **[FIELD_NOTES_INTEGRATION.md](./FIELD_NOTES_INTEGRATION.md)**: **The Bridge.** Defines how this static portfolio connects to the broader `HomeLabAI` system (Shared Venv, Symlinks, Data flow).
*   **[../HomeLabAI/docs/TOOL_RUNDOWN.md](../HomeLabAI/docs/TOOL_RUNDOWN.md)**: **The Toolbox.** Technical inventory of all agentic tools and node duties.
*   **[../HomeLabAI/docs/plans/VLLM_INTEGRATION_PLAN.md](../HomeLabAI/docs/plans/VLLM_INTEGRATION_PLAN.md)**: **The Silicon Core.** Roadmap for high-throughput, multi-node inference on the 2080 Ti using the Unified Gemma 2 2B base.

## 🛠️ Protocols & Procedures
*   **[../HomeLabAI/docs/Protocols.md](../HomeLabAI/docs/Protocols.md)**: **The Law.**
    *   Defines "The Builder Protocol," "Design Studio," and "BKM Style."
    *   **Must Read** for interaction standards.
*   **[monitor/PAGERDUTY_BKM.md](./monitor/PAGERDUTY_BKM.md)**: **Example BKM.** Specific deployment guide for the Neural Pager.
*   **[Travel_Guide_2026.md](./Travel_Guide_2026.md)**: **Confidential.** (Local Only). Contains infrastructure credentials, paths, and "Pinky" logic. **Do not commit.**

## 📜 Archives & Journals
*   **[PHASE_3_JOURNAL.md](./PHASE_3_JOURNAL.md)**: **The Log.** Detailed build log for the Observability Lab (Prometheus/Grafana).
*   **[FIELD_NOTES_PLAN.md](./FIELD_NOTES_PLAN.md)**: **The Roadmap.** (Partially Deprecated). Original master plan. Check `GEMINI.md` for current status.
*   **[INTERVIEW_CHEAT_SHEET.md](./INTERVIEW_CHEAT_SHEET.md)**: **Study Material.** Active document for interview prep.

## 🏺 Engineering Pedigree (Scars & Lessons)
*   **[Silicon Gauntlet Retro (Feb 19)](./RETROSPECTIVE_VLLM_RESURRECTION.md)**: Final verdict on vLLM/Turing compatibility.
*   **[Lessons Learned (Feb 19)](./RETROSPECTIVE_LESSONS_LEARNED_FEB_19.md)**: Strategic collaborative wins & isolation BKMs.
*   **[Recovery & Cruft Retro (Feb 19)](./RETROSPECTIVE_FEB_19_RECOVERY.md)**: Identity, telemetry, and technical debt mapping.
*   **[Feb 11 Post-Mortem](./POST_MORTEM_FEB_11_2026.md)**: Driver & Logger conflicts.
*   **[Resurrection Retrospective (Feb 15)](./RETROSPECTIVE_FEB_15_2026.md)**: The 7B-to-3B pivot.

## 🧹 Housekeeping & Drift Report (Feb 2026)
*Status: Pending Review*

1.  **`PHASE_3_LEARNING_PRIMER.md`**: Phase 3 is complete. Consider archiving to `docs/archive/` or merging key lessons into `PHASE_3_JOURNAL.md`.
2.  **`FIELD_NOTES_PLAN.md`**: Verify if Phase 2/3 sections are marked complete. The document might need a "Deprecated" header to avoid confusion with `GEMINI.md`.
3.  **`CLOUDFLARE_ACCESS_REQUESTS_MANUAL.md`**: (Deleted). Content successfully migrated to `FIELD_NOTES_ARCHITECTURE.md`.
