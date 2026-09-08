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
---

## 🛠️ SESSION RESTORE: Feb 27, 2026
**Current State**: 
* **Scanner**: OFFLINE (Crashed Feb 26, 23:03:35 during SPR-11-05 initial burn).
* **Blocker**: Ollama Read Timeout (30s) on large chunks of `notes_2024_PIAV.txt`.
* **Vitals**: Hardware is stable, `round_table.lock` path is unified to `~/Dev_Lab/HomeLabAI/round_table.lock`.
* **Branch Status**: `feature/sprint-11-05-hardening` contains high-fidelity Gems but also dangerous regressions.

### 📅 Consolidated Task List

#### **Phase A: Infrastructure & Parity (High Priority)**
- [x] **[FEAT-125] API-First Mutex**: Implementation confirmed in `lab_attendant.py` and `utils.py`.
- [x] **[UI] Blue Tree Status**: Non-destructive refresh confirmed in `status.html`.
- [x] **[HARDEN] AI Engine Timeout**: Increased timeout in `ai_engine.py` to **120s**.
- [x] **[HARDEN] Absolute GLOB Transition**: Refactored `scan_librarian.py` and `scan_queue.py` using `BASE_DIR`.
- [x] **[FIX] Event Over-count**: Updated `utils.py` to ignore `YYYY_MM.json` patterns.
- [ ] **[PARITY] Slow Burn Re-Ignition**: Restart `mass_scan.py` in background mode.

#### **Phase B: Strategic Anchoring [FEAT-128]**
- [x] **[LIBRARIAN] Anchor Extraction**: Ported `[STRATEGIC_ANCHOR]` identification logic.
- [x] **[LIBRARIAN] DOCX Support**: Integrated `docx2txt` for "War Stories" and "Philosophy".
- [x] **[NIBBLER] Robust JSON Extraction**: Ported [FEAT-131] regex-based fallback `(\[.*\])`.
- [x] **[NIBBLER] Atomic State Updates**: Ported [FEAT-130] success-gate logic.
- [ ] **[AGGREGATOR] Year Injection**: Update `aggregate_years.py` to inject anchors at the absolute top of `YYYY.json` files.

#### **Phase C: Documentation & Audit**
- [ ] **[DOCS] Diagnostic Map v4.1**: Update `DIAGNOSTIC_SCRIPT_MAP.md` with "Ghost Hunter" and "Assassin" verification.
- [x] **[AUDIT] Script Map Validation**: Verified Librarian archaeology and pathing stability.

#### **Phase D: The Last Mile (Strategic Awareness)**
- [x] **[AGGREGATOR] Anchor Pinning**: Updated `aggregate_years.py` to pin `[STRATEGIC_ANCHOR]` to top.
- [x] **[RECOVERY] Nudge Meta**: Created `nudge_meta.py` for surgical cache invalidation.
- [x] **[FEAT-128] Multi-Year Explosion**: Distributed anchors across year ranges.
- [x] **[BURN] Anchor Burn**: Completed high-fidelity burn of primary META docs.
- [ ] **[FEAT-133] Success Sanitization**: Implement [VIBE-008] "Performance Verbiage" filtering in the nibbler prompt.
- [ ] **[CLEANUP] Success Audit**: Create `sanitize_achievements.py` to scrub existing feedback from `YYYY.json` files.

---

## 🧪 LAST MILE VERIFICATION GATES

### **Gate 1: Aggregator Integrity**
* **Test**: Run `aggregate_years.py` on a mock dataset with a `[STRATEGIC_ANCHOR]`.
* **Success Criteria**: Anchor event is at index 0 of the yearly JSON; no duplicate events created.

### **Gate 2: Cache Invalidation (Nudge)**
* **Test**: Execute `nudge_meta.py`.
* **Success Criteria**: `chunk_state.json` hashes for `META` files are removed; `LOG` hashes remain intact.

### **Gate 3: Multi-Year Distribution**
* **Test**: Process a document with a range (e.g., 2011-2016) and run the aggregator.
* **Success Criteria**: The anchor appears in every yearly file within that span (`2011.json` through `2016.json`).

### **Gate 4: High-Fidelity Extraction**
* **Test**: Run `nibble_v2.py` on the nudged `META` files.
* **Success Criteria**: Ollama stays within the 120s timeout; `[STRATEGIC_ANCHOR]` events are correctly formatted with `rank: 5`.

---

---

## 🗄️ BRANCH AUDIT: feature/sprint-11-05-hardening
*Forensic summary for surgical porting.*

### **💎 Gems to Port (High Confidence)**
1. **[FEAT-128] Strategic Prompts:** The "Expert Career Strategist" prompt in `nibble_v2.py` for `META` files.
2. **[FEAT-131] Robust JSON:** The recursive regex extractor in `nibble_v2.py`.
3. **[FEAT-130] Atomic Hash:** Only marking a file as "Done" if events > 0.
4. **[DOCX] Support:** Integration of `docx2txt` in `scan_librarian.py`.
5. **[HARDEN] Absolute Paths:** Transitioning all relative GLOBs to `BASE_DIR` anchors.

### **🚫 Bad Ideas to Discard (Do NOT Port)**
1. **Attendant/AcmeLab Regressions:** The branch rolls back `The Assassin` [FEAT-119] and `Lab Fingerprint` [FEAT-121]. **Discard these changes entirely.**
2. **Lock Path Drift:** The branch attempts to move `round_table.lock`. **Discard.**
3. **Direct OLLAMA Bypass:** The branch forces a bypass of the `AcmeLabWebSocketClient`. **Discard** (main's factory is superior for resilience).
4. **Manual OVERRIDES Bloat:** The branch hardcodes specific filenames into the librarian. **Discard** (maintain heuristic authority).

---

## 🧰 THE HIDDEN DEBUG TOOLKIT (Scanner Recovery)
*Use these scripts for surgical interventions when the Slow Burn stalls.*

| Script | Purpose | When to use |
| :--- | :--- | :--- |
| `nudge_2024.py` | Surgical Re-nibble | Clears the hash for 2024 files in `chunk_state.json` to force a re-scan of ONLY that year. |
| `force_feed.py` | Emergency Ingestion | Bypasses all "Politeness" and "Mutex" checks to jam a specific file into the engine immediately. |
| `test_chunking.py` | Librarian Debug | Verifies the logic for splitting large files into buckets before they reach the queue. |
| `debug_2024.py` | Path Probe | Lower-level tool for checking absolute path resolution for the 2024 notes. |
| `clean_data.py` | **NUCLEAR OPTION** | Wipes the `data/` directory. Only use if the archive is fundamentally corrupted. |

---

## ⚡ HEADS-DOWN EXECUTION STRATEGY

### **Core Objectives:**
1. **Hardening (The Infrastructure):**
    * **Timeout Boost:** Increase the `requests` timeout in `ai_engine_v2.py` (and `ai_engine.py`) to **120s** to prevent Ollama crashes during deep reasoning.
    * **Absolute Pathing:** Refactor `scan_librarian.py` and `scan_queue.py` to use `BASE_DIR` for all GLOB operations, eliminating CWD-dependency bugs.
    * **Telemetry Fix:** Update `utils.py` to prevent the `YYYY_MM.json` monthly logs from double-counting in the "Total Events" vital.

2. **Synthesis Port (The Gems):**
    * **DOCX Integration:** Add `docx2txt` support to `scan_librarian.py` to ingest the high-fidelity "War Stories" and "Philosophy" documents.
    * **Strategic Anchoring [FEAT-128]:** Port the "Expert Career Strategist" logic into `nibble_v2.py` to extract `[STRATEGIC_ANCHOR]` events from `META` files.
    * **Robust JSON [FEAT-131]:** Port the regex-based JSON extractor to `nibble_v2.py` to handle "chatty" LLM responses.
    * **Atomic Updates [FEAT-130]:** Port the success-gate logic to ensure `chunk_state.json` is only updated when valid data is captured.

3. **Verification & Re-Ignition:**
    * Run `test_chunking.py` and `debug_2024.py` to verify the new absolute pathing.
    * Restart `mass_scan.py` in the background to re-ignite the **Slow Burn** epoch.

### **Iterative Verification Gates:**
1. **Infrastructure Hardening (Timeout & Paths):**
    * **Check:** After refactoring `scan_librarian.py` and `scan_queue.py` to use `BASE_DIR`, run them from the root `~/Dev_Lab` (not their home folder) to prove absolute pathing works.
    * **Lint:** `ruff check` on all modified Python files.
2. **Telemetry Fix (Event Counting):**
    * **Check:** Run `python3 -c "from utils import get_total_events; print(get_total_events())"` before and after the fix. The "After" count should be lower.
3. **DOCX & Librarian Port:**
    * **Check:** Execute `python3 scan_librarian.py` and verify that `Philosophy and Learnings 2024.docx` is correctly classified as `META` in the `file_manifest.json`.
4. **Strategic Anchoring & Robust JSON [FEAT-128/131]:**
    * **Check:** Use `force_feed.py` on a single `META` file. Inspect the resulting `.json` for the `[STRATEGIC_ANCHOR]` prefix and `rank: 5`.
5. **Atomic State [FEAT-130]:**
    * **Check:** Simulate a "Null Response" from the engine and verify that the file's hash in `chunk_state.json` **remains unchanged**.

### **Excluded Items (Out of Scope):**
* **Yearly Injection Logic:** `aggregate_years.py` updates deferred until anchors are generated.
* **Lab Hub Refactoring:** `acme_lab.py` and `lab_attendant.py` preserved as stable `main` versions.
* **UI Layout Changes:** No modifications to `status.html` or `timeline.html` CSS.

---
*Reference: [RETROSPECTIVE_STABILIZATION_FEB_26.md](./RETROSPECTIVE_STABILIZATION_FEB_26.md)*
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
