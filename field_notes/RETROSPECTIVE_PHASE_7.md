# Retrospective: Phase 7 (The System Admin Pivot)

**Date:** January 25, 2026
**Theme:** "Smoke & Mirrors" and "Functional Aesthetics"

## 🎯 The Shift
We started with a standard "Card-based" timeline but realized it felt too passive. The goal shifted to creating an interface that feels like **operating a system**, not just reading a document. We adopted a "System Admin / Hacker" aesthetic (High contrast, Monospace, ASCII Trees) to match the persona of a Validation Engineer. We pivoted from "Green Matrix" to "VS Code Blue" for a more professional finish.

## 🏗️ Architectural Wins

### 1. The "Nibbler" Pipeline (Background Intelligence)
We moved away from monolithic batch scanning to a distributed queue:
*   **`scan_librarian.py`:** The Gatekeeper. Classifies files (LOG vs REFERENCE) to keep the timeline clean. It uses heuristics (dates in file body) to catch logs disguised as backlogs.
*   **`scan_queue.py`:** The Scheduler. Instantly chunks files by date and checks for changes.
*   **`nibble.py`:** The Worker. Runs every 15 minutes via Systemd. Checks Prometheus (`node_load1`) before burning GPU cycles.
*   **`force_feed.py`:** The "Big Red Button" to aggressively process the entire queue when needed.

### 2. The "Blue Tree" Frontend (UX)
We achieved a "Live AI" feel without a backend server:
*   **Lazy Loading:** `YYYY.json` aggregates are fetched only when needed.
*   **Interaction:** Click Year (Expand) -> Click Log (Inline Terminal).
*   **Visuals:** A custom Typewriter effect renders text character-by-character inside the tree structure.
*   **Fail-Safe:** Hardcoded fallback data ensures the site never looks empty, even if the API fails.

### 3. The "Plays Nice" Integration
We prepared for the future HomeLabAI merger without creating dependency hell:
*   **`ai_engine.py`:** An abstraction layer. Currently uses `OllamaClient` (Local HTTP), but includes a stub for `AcmeLabClient` (MCP/WebSocket).

## 📉 Lessons Learned

### 1. File Classification is Hard
Regex isn't enough. Files named `notes_2005.txt` turned out to be todo lists. We implemented a "Deep Sample" heuristic in the Librarian to catch this.

### 2. Mobile Caching is Aggressive
We had to implement "Nuclear Cache Busting" (`?v=7.0`, `?t=TIMESTAMP`) to force mobile browsers to see the new UI.

### 3. UX: Cards vs. Trees
We iterated through Cards -> Grid -> Green Tree -> Blue Tree. The final design strikes the best balance between "Hacker Vibe" and "Readability."

## 🔮 Next Steps
*   **Integration:** Connect `ai_engine.py` to HomeLabAI's real `Pinky` agent.
*   **RAG:** Feed the `REFERENCE` files (identified by the Librarian) into ChromaDB.
