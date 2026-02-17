# Design Document: Feature Tracker (FeatureTracker.md)
**Status:** Draft | **Owner:** Human Architect / Lead Engineer

## 1. Purpose & Scope
The **Feature Tracker** is the central "Map Room" for the project's functional DNA. While documentation remains the Source of Truth, the Feature Tracker is the **Searchable Index and Relational Map**. 

**The Searchable Index Pointer Strategy:**
The whole point of `FeatureTracker.md` is to **track the "Why"**. It acts as a relational hub that points to code, research, and tests, ensuring that the architectural intent behind every implementation is preserved across cold-starts and refactors. It identifies *how we want the system to be* based on explicit buy-in.

## 2. Contents of FeatureTracker.md

### A. Goal Section
**Use Case:** Use this file as a guiding tool when refactoring code and minimize feature drift and loss during future debug, planning, and implementation phases.

### B. Guardrail Section (The Invariants)
*   **Architectural Buy-in:** Only remove features with explicit buy-in by the human architect.
*   **Change Control:** Changes must have human buy-in for changes in feature identity (e.g., code location, implementation changes).
*   **Semantic Anchors:** Every feature must have a unique ID (e.g., `[FEAT-001]`) cross-referenced in code comments for instant `grep` traceability.

### C. Feature Association Matrix (Machine-Readable)
This file should provide a common location to connect: **Feature, Code, Research, & Tests.** Common features are grouped in the same location for easy navigation.
*   **Status States:** `ACTIVE`, `DEGRADED`, `STUBBED`, or `ZOMBIE`.
*   **Association Chain:** `[Feature ID] | [How->Why] | [Where (Code)] | [Research/BKM] | [Verification (Test)]`

### D. Lost Gems (The Resurrection Ledger)
A section for functionality previously implemented but sidelined.
*   **Kill Reason:** Why it was removed (e.g., VRAM limits, library conflict).
*   **Restoration Trigger:** Environmental triggers for its return (e.g., "GPU Upgrade").

### E. Future Requirements
A ledger of long-term technical needs (not tasks).

## 3. Ecosystem Integration & Anti-Redundancy
To ensure `FeatureTracker.md` melds and enhances rather than complicates, we enforce the following distinctions:

*   **vs. `HomeLabAI/docs/TOOL_RUNDOWN.md`**: 
    *   **The Plan:** This file will be **deprecated** during the buildup phase. Its content (the "What") will be absorbed into the Tracker's relational matrix (the "Why" and "Where").
*   **vs. `HomeLabAI/ProjectStatus.md`**:
    *   **The Distinction:** `ProjectStatus.md` is **Dynamic and Ephemeral** (tracks "how it is now" / current health). `FeatureTracker.md` is **Static and Foundational** (tracks "how we want it to be" / buy-in identity).
*   **The Pointer Principle:** If a feature is explained in depth in architecture docs (e.g., `FIELD_NOTES_ARCHITECTURE.md`), the Tracker *points* to that explanation rather than duplicating it.

## 4. Buildup Guide: Populating the Tracker
This is a forensic and analytical process to map truth to the filesystem:

1.  **Review Documentation:** Documentation should be the source of truth, `FeatureTracker.md` the map. Audit all existing Markdown files.
2.  **Scour the Silicon:** Scour code, tests, and utilities for undocumented features and the "how" of their implementation. 
3.  **Parse logs:** Parse old Gemini logs for lost gems and the historical "why" behind decisions.
4.  **Ecosystem Harmony:** Keep in mind the document ecosystem itself; `FeatureTracker.md` needs to meld and enhance, not complicate. Every "Where" link must be verified by a `grep` or `ls` check.
