# Semantic Re-Mapping (Sprint SPR-11-05)
**Status:** ACTIVE | **Goal:** Transition from Tactical Logs to Strategic Anchoring

## 🎯 THE MISSION
The Lab currently operates on "Tactical Memory"—the raw *What* and *When* extracted from `notes_*.txt`. It lacks "Strategic Grounding"—the *Why* and *How* defined in high-level career documents. This sprint implements a dual-mode processing pipeline that distinguishes between **Granular Logs** and **Structural Anchors**.

## 📍 FORENSIC ANCHORS (The Restored Core)
These files were restored on Feb 26, 2026, and are the primary targets:
*   `raw_notes/11066402 Insights 2019-2024.txt` (Multi-year focal goals)
*   `raw_notes/Performance review 2008-2018 .txt` (Combined career growth)
*   `raw_notes/Philosophy and Learnings 2024.docx` (Engineering DNA)
*   `raw_notes/Jason Allred Resume - Feb 2026.txt` (Target Persona)

## 🛠️ COMPONENT BKM (Step-by-Step Logic)

### BKM-015: Librarian Classification (`scan_librarian.py`)
*   **Preparation**: Expand `NOTES_GLOB` to `raw_notes/**/*.{txt,docx}`.
*   **Logic**:
    1.   Pinky (LLM) reads the file header.
    2.   If the filename matches `Insights`, `Review`, or `Philosophy`, force-assign `"type": "META"`.
    3.   **Reference Pointer**: Update the `OVERRIDES` dictionary in `scan_librarian.py` to ensure high-priority files bypass heuristic classification.
*   **Trigger**: Run `python3 field_notes/scan_librarian.py`.
*   **Verification**: Check `field_notes/data/file_manifest.json` for the new `META` category.

### BKM-016: The Strategic Nibbler (`nibble_v2.py`)
*   **The "Structural Split"**: Standard `LOG` files are chunked by month. `META` files must be processed as **atomic year-blocks**.
*   **Core Logic**:
    1.   Detect `type == "META"` in `queue.json`.
    2.   **The Strategic Prompt**: Switch from "Extract wins" to "Identify the core engineering theme and strategic focal point for [Year]."
    3.   **The Anchor Tag**: Prefix extracted content with `[STRATEGIC_ANCHOR]`.
*   **Output**: Injects these items into `YYYY.json` summaries with `rank: 5` (Diamond+).

### BKM-017: Truth Sentry Integration (`archive_node.py`)
*   **Logic**: Update `get_context()` to perform a "Header-First" retrieval.
    1.   Query for the `[STRATEGIC_ANCHOR]` tag matching the target year.
    2.   Prepend this anchor to the `Historical Context` block sent to the Brain.
*   **Outcome**: The 4090 Brain lead with the "Why" (Strategy) before the "What" (Logs).

## 🧪 VALIDATION GAUNTLET
1.  **Tag Check**: `grep "META" field_notes/data/file_manifest.json` must return 5+ hits.
2.  **Summary Check**: `2023.json` must have a top-level entry containing your 2023 focal goal.
3.  **Fidelity Check**: Query: *"What was the philosophical driver behind my 2024 work?"*
    *   **Pass Condition**: Response cites the `Philosophy and Learnings 2024` document and mentions "Class 1" or "Verification Rigor."

## 🧱 FEATURE TRACKER MAPPING
*   **[FEAT-128] The Strategic Anchor**: High-level context injection via the `META` pipeline.
*   **[FEAT-129] The Philosophical Core**: Explicit extraction of design principles to influence AI persona.

## ⚠️ SCARS (Lessons from Feb 12-26)
*   **Race Conditions**: Always await `cleanup_silicon` in the Attendant.
*   **Binary Bloat**: Do not scan `.docx` files without using an appropriate text-extractor (e.g., `python-docx` or `pandoc`).
*   **Sync Trust**: Calculate Git hashes dynamically to ensure "Smart-Reuse" doesn't serve stale logic.
