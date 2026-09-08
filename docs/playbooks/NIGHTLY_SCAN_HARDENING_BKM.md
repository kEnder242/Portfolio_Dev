# BKM: Hardening the Nightly Archive Scan
**Target**: Reliability, Path Integrity, and Mutex Precision.

## 1. 🏗️ Infrastructure: Absolute Pathing
All maintenance scripts (`scan_librarian.py`, `scan_queue.py`, `nibble_v2.py`) should be hardened against working-directory drift.
*   **Action**: Use `BASE_DIR = os.path.dirname(os.path.abspath(__file__))` to anchor all data and log paths.

## 2. 🚦 The API-Based Mutex
Filesystem locks are brittle. The Lab Attendant should serve as the authority for GPU availability.
*   **Insight**: Adding a `/status` endpoint to the Lab Attendant allows the Nibbler to poll for safety before starting a "burn."
*   **Logic**:
    ```python
    # In lab_attendant.py
    async def handle_status(self, request):
        return web.json_response({
            "round_table_lock_exists": os.path.exists(ROUND_TABLE_LOCK),
            "full_lab_ready": self.ready_event.is_set()
        })
    ```

## 3. 🛡️ Lab Server Hardening (`acme_lab.py`)
*   **Sentinel Safety**: Remove the single word "shutdown" from the heuristic shutdown trigger. It appears too often in technical logs.
*   **JSON Robustness**: Models often wrap JSON in Markdown blocks. Use `re.search(r"(\{.*\})", text, re.DOTALL)` to extract the raw object before calling `json.loads`.
*   **Programmatic Preservation**: When a query contains the word "json," the Hub's `execute_dispatch` should return the `raw_text` instead of attempting to summarize or flatten the output into a string.

## 4. 🧠 AI Engine Upgrades (`ai_engine.py`)
*   **Source Prioritization**: The `AcmeLabWebSocketClient` should be modified to wait specifically for "Brain" sources. This prevents the client from accidentally capturing Pinky's "facilitation" messages instead of the structured data.
*   **Direct Mode**: Implement a mode that allows `requests.post` directly to Ollama (11434). This is essential for high-volume maintenance tasks where the full Lab persona overhead is not required.

## 5. 📉 Nibbler Stability (`nibble_v2.py`)
*   **Atomic State Updates**: Only update `chunk_state.json` when `added_count > 0` or a valid list is returned. This ensures that if the Lab is laggy or the model hallucinates, the task remains in the queue for a subsequent attempt.
*   **Strategic Prompts**: For high-value documents, use a specialized prompt that requests a `[STRATEGIC_ANCHOR]` and sets `rank: 5` to ensure these appear at the top of the timeline.
