# Retrospective: Phase 7 (The System Admin Pivot)

**Date:** January 25, 2026
**Theme:** "Smoke & Mirrors" and "Functional Aesthetics"

## 🎯 The Shift
We started with a standard "Card-based" timeline but realized it felt too passive. The goal shifted to creating an interface that feels like **operating a system**, not just reading a document. We adopted a "System Admin / Hacker" aesthetic (High contrast, Monospace, ASCII Trees) to match the persona of a Validation Engineer.

## 🏗️ Architectural Wins

### 1. The "Nibbler" Pipeline (Background Intelligence)
We moved away from monolithic batch scanning to a distributed queue:
*   **`scan_librarian.py`:** The Gatekeeper. Classifies files (LOG vs REFERENCE) to keep the timeline clean.
*   **`scan_queue.py`:** The Scheduler. Instantly chunks files by date and checks for changes.
*   **`nibble.py`:** The Worker. Runs every 15 minutes via Systemd. Checks Prometheus (`node_load1`) before burning GPU cycles.

### 2. The "Smoke & Mirrors" Frontend (UX)
We achieved a "Live AI" feel without a backend server:
*   **Lazy Loading:** `YYYY.json` aggregates are fetched only when needed.
*   **Interaction:** Clicking a Year "Powers it on." Clicking a Month "Queries the logs."
*   **Visuals:** A custom Typewriter effect renders text character-by-character, simulating a high-speed terminal buffer.

### 3. The "Plays Nice" Integration
We prepared for the future HomeLabAI merger without creating dependency hell:
*   **`ai_engine.py`:** An abstraction layer. Currently uses `OllamaClient` (Local HTTP), but includes a stub for `AcmeLabClient` (MCP/WebSocket).

## 📉 Lessons Learned

### 1. File Classification is Hard
Regex isn't enough. Files named `notes_2005.txt` turned out to be todo lists. We had to implement a heuristic that checks the *middle* of the file for dates to correctly classify logs disguised as backlogs.

### 2. DOM vs. JSON
The "Lazy JSON" approach is superior for this volume of data. It keeps the initial load instant and allows the "Smoke & Mirrors" effect to hide the network latency (by pretending to "Think").

### 3. Syntax Matters
We hit several snags with Python f-strings and JSON formatting when writing scripts via the CLI. The lesson: Use `write_file` for complex code, not `cat`, and be meticulous about escaping.

## 🔮 Next Steps
*   **Integration:** Connect `ai_engine.py` to HomeLabAI's real `Pinky` agent.
*   **RAG:** Feed the `REFERENCE` files (identified by the Librarian) into ChromaDB.
