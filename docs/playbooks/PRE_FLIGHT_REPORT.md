# Pre-Flight Report: AI Engine Upgrade & Research Synthesis (v2.0)
**Date:** Feb 6, 2026
**Status:** Staging Complete (Finalized)

## 1. Grounding: AGENTS.md
The `HomeLabAI/AGENTS.md` manifesto is active. It codifies the "Class 1" design, BKM Protocol, and the **NEVER PUSH** safety rule.

## 2. Environment Audit
- **Ollama (11434):** **ONLINE**. Available: `llama-3.2-3b-awq`, `nomic-embed-text`.
- **Prometheus (9090):** **ONLINE**. `node_load1` = `0.1`.
- **Data Integrity:** `file_manifest.json` and `queue.json` verified.

## 3. Research Synthesis & Architectural Insights
This upgrade is grounded in the following technical benchmarks:

### A. TTCS (Test-Time Curriculum Synthesis - 2601.22628)
- **Insight:** Using a "Synthesize-then-Solve" loop to ground reasoning in evidence.
- **Implementation:** `CurriculumEngine` will prompt Pinky to generate 3 "Technical Anchors" from raw notes, solve them, and use the results to build the final high-density BKM entry.
- **Relevance:** Mitigates repetition loops and ensures 18 years of validation logic isn't lost to shallow summaries.

### B. FS-Researcher (File-System Memory Scaling - 2602.01566)
- **Insight:** Persistent file systems are superior to LLM context windows for long-horizon tasks.
- **Implementation:**
    - **Memory Bridge:** `ai_engine_v2.py` will read `YYYY.json` and `file_manifest.json` to "warm up" the prompt with historical context before scanning a new note.
    - **Context Builder (The Nibbler):** `nibble.py` remains the archivist.
    - **Report Writer (The Intercom):** The future Web Intercom will act as the "Report Writer," navigating the file tree to synthesize multi-year insights.
- **Hierarchical Evolution:** Move from flat JSON lists to a "BKM Tree" (e.g., `data/expertise/telemetry/pecistressor.md`) where the Librarian actively indexes "Technical Gems."

### C. Recursive Language Models (RLMs)
- **Insight:** Treat context as an external string to be "read" via code.
- **Implementation:** Implementing a `FileSystemMemory` tool that allows Pinky to "peek" at related notes during a scan.

## 4. Implementation Specification (ai_engine_v2.py)
I will implement a non-breaking extension called `CurriculumEngine`.
- **Blue/Green Pattern:** Legacy `OllamaClient` stays functional.
- **New Mode:** `mode="REASONING"` enables the TTCS loop.
- **Tooling:** Add a `HistoryBridge` to inject previous scan results into the reasoning prompt.

---
**Approval requested to proceed to implementation.**