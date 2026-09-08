# Sprint Plan: [SPR-11-06] The Privacy Moat & Nuclear Reset
**Status:** ACTIVE | **Goal:** Hardened Re-Ingestion of the 18-Year Archive.

## 🎯 THE MISSION
To surgically separate "Technical Pedigree" from "Personal Performance Feedback." A forensic audit confirmed that the current "Slow Burn" has contaminated the timeline with "Jason should" coaching patterns, incorrectly assigned them a **Rank 4 (Diamond)** status. This sprint executes a **Nuclear Reset** of the data and implements a **Structural Guillotine** to prevent re-contamination.

## 📍 CONTAMINATION REPORT (The "Crime Scene")
*   **Finding:** `2024.json` contains entries like: *"In Q1, Jason should: -Deliver on Kayak+Montana transition plan..."*
*   **Rank Inflation:** These entries were assigned **Rank 4**, diluting the actual technical evidence (e.g., `pecistressor.py`).
*   **Cause:** The LLM confused "Strategic Focal Goals" with "High-Value Technical Evidence" and ignored the instructional nature of the feedback.

## 🛠️ THE "NUCLEAR RESET" STRATEGY
1.  **[BACKUP]**: `cp -r field_notes/data field_notes/data_contaminated_backup` (Preserve the evidence for audit).
2.  **[WIPE]**: Delete all `20*.json` timeline logs.
3.  **[RESET]**: Reset `chunk_state.json` to `{}` to force a total re-scan.
4.  **[PERSIST]**: Preserve `file_manifest.json` (The "Librarian's Map" is healthy).

## 🛠️ COMPONENT BKM (The "Defense-in-Depth" Strategy)

### Phase 1: The "Structural Guillotine" (Pre-Processor)
*   **File:** `field_notes/nibble_v2.py`
*   **Logic:** Implement `scrub_input_buffer()` to truncate text *before* LLM ingestion.
*   **The Blade:** Drops at headers matching **[VIBE-008]** (e.g., "AREAS FOR IMPROVEMENT", "Results Coaching").
*   **The Recovery:** Logic to resume scanning at the next "Safe" technical header.

### Phase 2: The "Cognitive Firewall" (Prompt Hardening)
*   **File:** `field_notes/nibble_v2.py`
*   **Constraint:** Update the `META` processing prompt with: *"EXCLUDE all behavioral feedback, coaching, or personal growth plans. Focus exclusively on technical milestones and strategic focal points."*

### Phase 3: The "Atomic Audit" (Post-Processor)
*   **File:** `field_notes/sanitize_achievements.py` (New Tool)
*   **Logic:** A final safety scan of `YYYY.json` files for "Jason should" or "Needs to improve" patterns, purging matching JSON objects.

### Phase 4: The "Pattern-Based Vault" (Privacy Bridge)
*   **File:** `field_notes/archive_node.py`
*   **Logic:** Move "Instructional/Private" entries to `private_vault.json` instead of simple deletion.

## 🧪 VALIDATION GAUNTLET
1.  **Guillotine Check:** Verify that a mock chunk with "Results Coaching" is truncated before being sent to the LLM.
2.  **Audit Check:** Run `sanitize_achievements.py` on a test year and verify the removal of "Jason should" patterns.
3.  **Synthesis Check:** Confirm that `2024.json` contains the "Strategic Anchor" but 0% of the "Growth Feedback."

## 🧱 FEATURE TRACKER MAPPING
*   **[FEAT-073] Insight Pruning**: The implementation of surgical redaction.
*   **[FEAT-133] Success Sanitization**: The automated audit pipeline.
*   **[VIBE-008] Performance Verbiage**: The foundational privacy rule.

---
*Reference: [SPR-11-05] Semantic Re-Mapping (Infrastructure Pre-requisite)*
