# Field Notes Synthesis Report
**Date:** January 25, 2026
**Author:** Gemini CLI (Agent) & Pinky (Mistral-7B)
**Status:** Complete (v2.2)

## 🎯 Objective
To transform the static "Field Notes" portfolio into a data-driven dashboard without introducing a backend server or database ("Class 1" Philosophy). The goal was to index 18 years of raw engineering notes and correlate them with the curated "War Stories" to enhance searchability and visualize career progression.

## 🏗️ Architecture: The "Static Synthesis" Pipeline

We implemented a build-time data pipeline that leverages the local "Pinky" node (HomeLabAI) to process data, leaving the runtime site purely static.

```mermaid
graph TD
    A[Raw Notes (2005-2024)] -->|Read via Symlink| B(Pinky Scanner Script)
    C[Resume & Focal Reviews] -->|Strategic Context| B
    B -->|Mistral-7B Inference| D[pinky_index_full.json]
    D -->|Merge Script| E[search_index.json]
    E -->|Fetch| F[Dashboard (index.html)]
    D -->|Fetch| G[Timeline (timeline.html)]
```

### Components
1.  **Pinky Scanner (`field_notes/scan_pinky.py`):**
    *   A Python script that interfaces with the local Ollama instance (Port 11434).
    *   **Input:** `raw_notes/notes_*.txt` (Symlinked from `~/knowledge_base`).
    *   **Context:** Uses `Jason Allred Resume` and `Insights 2019-2024.txt` to ground the extraction.
    *   **Logic:** extract `technical_tags` and `key_events` correlated to strategic themes.

2.  **Grand Index (`field_notes/pinky_index_full.json`):**
    *   The master dataset containing the "Ground Truth" of 18 years of work.
    *   Structure: Year -> Strategic Theme -> Technical Tags -> Events.

3.  **Search Index (`field_notes/search_index.json`):**
    *   A lightweight mapping of `Tag -> [Article_IDs]`.
    *   Merged via `field_notes/merge_indices.py` to combine manual curation with AI discovery.

4.  **Frontend (Vanilla JS):**
    *   **Dashboard:** `script.js` performs a "Hybrid Search" (Visible Text + Hidden Tags).
    *   **Timeline:** `timeline.html` renders a vertical visualization of Strategy vs. Tactics.

## 📊 Results

### Search Enhancement
*   **Before:** Search limited to visible titles (approx. 30 keywords).
*   **After:** Search expanded to **100+ keywords** including deep cuts like:
    *   *Simics, NPK, IPC, Trace32* (2015 era)
    *   *Fulsim, CRC Mismatch* (2016 era)
    *   *MCTP, PECI, Kayak* (2024 era)

### Timeline Visualization
*   Created a new `timeline.html` page accessible from Mission Control.
*   Visualizes the split between "Strategic Goals" (Focal Reviews) and "Tactical Reality" (Engineering Logs).

## 📝 Files & Locations
*   **Live Site:** `https://notes.jason-lab.dev` (Port 9001)
*   **Raw Data:** `~/Portfolio_Dev/raw_notes/` (Symlink to `~/knowledge_base`)
*   **Scripts:**
    *   `field_notes/scan_pinky.py` (The AI Extractor)
    *   `field_notes/merge_indices.py` (The Index Merger)
*   **Data Artifacts:**
    *   `field_notes/pinky_index_full.json`
    *   `field_notes/search_index.json`

## 🔮 Future Recommendations
*   **Automated Re-Scan:** Add a `make scan` target to run the Python script when new notes are added.
*   **Deep Linking:** Update the Merge script to infer more precise article links based on event dates.
