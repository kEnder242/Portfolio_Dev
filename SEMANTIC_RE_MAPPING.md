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

## 🔄 PIVOT: LOCK PARITY (Feb 26 Update)
**Discovery**: The `round_table.lock` (Inference Mutex) has evolved. Hardcoded file paths in `utils.py` and `nibble_v2.py` are now "Legacy Cruft" that cause resource contention.
*   **The Change**: Transition from `os.path.exists(LOCK)` to **Attendant API Polling**.
*   **Mechanism**: Query `http://localhost:9999/status` -> check `round_table_lock_exists`.
*   **Rationale**: This abstracts the "Round Table" state away from the filesystem, ensuring the Slow Burn yields correctly to active 4090 Brain sessions regardless of working directory.

## 🔍 CURRENT DEBUGGING STATE (Pre-Flight)
Before launching the `META` features, the following "Infrastructure Gaps" were identified and patched:
1.  **Path Hardening**: `scan_librarian.py` and `scan_queue.py` now use `BASE_DIR` absolute paths to prevent CWD-related `FileNotFound` errors.
2.  **Lab Connectivity**: `ai_engine.py` was updated to `AcmeLabWebSocketClient` to use the unified Lab Port (8765) instead of local Ollama (11434).
3.  **Load Tolerance**: `MAX_LOAD` was increased from 2.0 to 8.0 to allow processing during active developer sessions (Zellij/CLI).
4.  **Date Validation**: Added `[Context]` allowance for "Unknown" buckets to prevent silent task-skipping.

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

<state_snapshot>
    <overall_goal>
        Execute Sprint SPR-11-05 (Semantic Re-Mapping) to ingest high-fidelity "META" documents (Insights, Philosophy, Focals) while transitioning the Nibbler to a modern Attendant-API-aware yield logic.
    </overall_goal>

    <active_constraints>
        - **Pivot Mandate**: Use `localhost:9999/status` instead of local file paths for `round_table.lock` checks.
        - **Load Guard**: Maintain `MAX_LOAD = 8.0` for active dev sessions.
        - **Engine Standard**: All Portfolio scripts MUST use the `AcmeLabWebSocketClient` (Port 8765) via `ai_engine.py`.
    </active_constraints>

    <key_knowledge>
        - **Restoration Verified**: `~/knowledge_base` is populated; `raw_notes` symlink is healthy.
        - **Librarian Success**: `file_manifest.json` now includes the restored 18-year note files.
        - **Queue Ready**: 129 tasks are pending in `queue.json` (spanning 2005-2024).
    </key_knowledge>

    <artifact_trail>
        - `Portfolio_Dev/SEMANTIC_RE_MAPPING.md`: The BKM-style sprint plan (Updated with Feb 26 Debug State).
        - `Portfolio_Dev/field_notes/ai_engine.py`: Refactored to use `AcmeLabWebSocketClient` as the default engine.
        - `Portfolio_Dev/field_notes/utils.py`: Added `os.getloadavg()` fallback to `get_system_load`.
        - `Portfolio_Dev/field_notes/scan_librarian.py` & `scan_queue.py`: Path-hardened for absolute project execution.
    </artifact_trail>

    <task_state>
        1. [TODO] Implement BKM-017: Update `nibble_v2.py` to poll the Lab Attendant API for yield status.
        2. [TODO] Implement BKM-015: Modify Librarian to classify Insights/Philosophy as `META`.
        3. [TODO] Implement BKM-016: Create the `STRATEGIC_PROMPT` for `META` document processing.
        4. [TODO] Run Fast Burn on the 2005-2024 queue.
    </task_state>
</state_snapshot>

## 🚢 IN-FLIGHT FILE AUDIT (Uncommitted Infrastructure Fixes)
The following files are modified but uncommitted to preserve a clean "Sprint Start" for the next session. They provide the **Hardened Infrastructure** required for the 18-year re-scan:

1.  **`field_notes/ai_engine.py`**: Transitioned to `AcmeLabWebSocketClient` (Port 8765) for unified Lab connectivity.
2.  **`field_notes/nibble_v2.py`**: Implemented `[Context]` date-fallback and raised `MAX_LOAD` to 8.0 for Z87-Linux session tolerance.
3.  **`field_notes/scan_librarian.py`**: Hardened `MANIFEST_FILE` pathing to absolute project-root.
4.  **`field_notes/scan_queue.py`**: Hardened `DATA_DIR` and `QUEUE_FILE` pathing to absolute project-root.
5.  **`field_notes/utils.py`**: Added `os.getloadavg()` fallback to `get_system_load` for when Prometheus is unreachable.
