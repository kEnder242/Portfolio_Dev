# Semantic Re-Mapping (Sprint SPR-11-05)

## 🎯 The Mission
The Lab currently has perfect "tactical" memory (the *What* and *When* via `notes_*.txt`) but lacks "strategic" grounding (the *Why*). This sprint will ingest high-level documents (Insights, Focals, Philosophy, Resumes) and weave them into both the frontend Timeline and the backend Brain via a new `META` processing pipeline.

## 🗂️ File Inclusion Rubric
*   **Target Files (The Anchors):**
    *   `raw_notes/11066402 Insights 2019-2024.txt` -> High-level quarterly/yearly goals.
    *   `raw_notes/Performance review 2008-2018 .txt` -> Early career growth.
    *   `raw_notes/Philosophy and Learnings 2024.docx` -> Core engineering DNA.
    *   `raw_notes/Jason Allred Resume - Feb 2026.txt` -> Current "Ground Truth".
    *   `raw_notes/Jason Allred resume 2008-2014.txt` -> The "Origin Story".
*   **Excluded Files:** Redundant individual yearly reviews and older resume drafts.

## 🧠 Semantic Re-Mapping (The Flow)

### 1. Librarian Classification (`scan_librarian.py`)
*   **Pointers**: Config `NOTES_GLOB` and `OVERRIDES` map.
*   **Action**: Expand globs to include `*.txt` and `*.docx`. Tag target files as `"type": "META"`.
*   **Vibe**: The Librarian transitions from a "Text-File Counter" to a "Context Gatekeeper."

### 2. The Strategic Nibbler (`nibble_v2.py`)
*   **Pointers**: Main loop task fetching and `process_chunk` logic.
*   **Action**: Detect `META` type in the queue. Use a dedicated `STRATEGIC_PROMPT` to extract "Yearly Focals" and "Core Philosophies" instead of monthly events.
*   **Behavior**: Injects results as Rank 4/5 `[STRATEGIC_ANCHOR]` items into `YYYY.json`.

### 3. The Truth Sentry Integration (`archive_node.py`)
*   **Pointers**: `get_context` and the new `Yearly Summary Injection` (FEAT-126).
*   **Action**: Prioritize these `[STRATEGIC_ANCHOR]` tags in RAG retrieval.
*   **Outcome**: The Brain lead with the "Why" (Strategy) before the "What" (Logs).

## 🧪 Testing & Validation
*   **Anchor Verification**: Run `scan_librarian.py` -> Verify `file_manifest.json` tags.
*   **UI Header Check**: Verify `2023.json` contains high-rank extracted focal points.
*   **Grounding Fidelity**: Modify `test_grounding_fidelity.py` to query "Strategic Goals in 2023" and verify citation of the `Insights` document.

## 📝 Feature Tracker Mapping
*   **[FEAT-128] The Strategic Anchor**: High-level context injection.
*   **[FEAT-129] The Philosophical Core**: Design principle extraction.
