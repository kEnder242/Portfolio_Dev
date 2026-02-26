# Strategic Anchoring (Sprint SPR-11-05)

## 🎯 The Mission
The Lab currently has perfect "tactical" memory (the *What* and *When* via `notes_*.txt`) but lacks "strategic" grounding (the *Why*). This sprint will ingest the restored high-level documents (Insights, Focals, Philosophy, Resumes) and weave them into both the frontend Timeline and the backend Brain.

## 🗂️ File Inclusion Rubric
*   **Target Files (The Anchors):**
    *   `11066402 Insights 2019-2024.txt` -> High-level quarterly/yearly goals.
    *   `Performance review 2008-2018 .txt` -> Early career growth and foundational achievements.
    *   `Philosophy and Learnings 2024.docx` -> Core engineering DNA ("Class 1", "Verify over Velocity").
    *   `Jason Allred Resume - Feb 2026.txt` -> The current "Ground Truth" persona.
    *   `Jason Allred resume 2008-2014.txt` -> The "Origin Story".
*   **Excluded Files:** Individual yearly reviews (redundant to combined `.txt`), older fragmented resumes, and raw binary artifacts (handled elsewhere).

## 🧠 Semantic Re-Mapping (The Flow)

### 1. Librarian Classification (`scan_librarian.py`)
*   **Action**: Expand the `NOTES_GLOB` to explicitly include the target files listed above.
*   **Logic**: The Librarian will tag these files with `"type": "META"` instead of `LOG` or `REFERENCE`. This tells the downstream pipeline that this is *foundational context*, not a daily engineering event.

### 2. The Strategic Nibbler (`nibble_v2.py`)
*   **Action**: Create a new processing path for `META` files.
*   **Logic**: Instead of breaking the file into monthly chunks (like `LOG`s), the Nibbler will use a new `STRATEGIC_PROMPT`. It will ask the LLM to extract "Yearly Focals" and "Core Philosophies."
*   **Output**: These are saved as high-ranking events (Rank 4/5) with a specific tag (e.g., `[STRATEGIC_ANCHOR]`) and written directly into the `YYYY.json` summaries, ensuring they appear at the *top* of any given year in the Timeline UI.

### 3. The Truth Sentry Integration (`archive_node.py`)
*   **Action**: Update the `ArchiveNode` to prioritize `META` tags.
*   **Logic**: When a year is queried, the node will first fetch the `[STRATEGIC_ANCHOR]` from the `YYYY.json` file. This anchor acts as the "Grounding Mandate" for that year, ensuring the Brain understands the broader goal before it reads the granular technical logs.

## 🧪 Testing Strategy

*   **Test 1: The Anchor Verification**
    *   *Action*: Run `scan_librarian.py` and verify `file_manifest.json` correctly tags the target files as `META`.
*   **Test 2: The UI Header Check**
    *   *Action*: After running the Nibbler on `Insights 2019-2024`, check `2023.json` to ensure the strategic focal points were extracted and ranked highly.
*   **Test 3: The Grounding Fidelity Run**
    *   *Action*: Run the existing `test_grounding_fidelity.py` but modify the query to ask about "Strategic Goals in 2023." Verify the Brain cites the `Insights` document over a random `notes` log.
