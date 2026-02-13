# Acme Lab Research Ledger

## 📖 Integrated Concepts

### Observational Memory (OM)
- **Source:** [VentureBeat: Observational Memory cuts AI agent costs 10x](https://venturebeat.com/data/observational-memory-cuts-ai-agent-costs-10x-and-outscores-rag-on-long)
- **Key Takeaway:** Treating memory as a stream of observations (compressed state) rather than a bag of retrieval chunks.
- **Application:** The **Continuous Burn** (Librarian/Nibbler) should transition from indexing to **State Summarization**. Instead of "where is the note about PCIe?", Pinky should have a "State of the PCIe Validation" memory.
- **Implementation:** Background synthesis of daily "Observations" into a `compressed_history.json`.

### Bicameral Mind (Psychology/AI)
- **Concept:** The breakdown of the bicameral mind (Julian Jaynes). 
- **Application:** The Hub (`acme_lab.py`) simulates the "hallucinated voice" (Brain) that Pinky (the reactive agent) hears and interprets. 

### Unified Diffs (Patching)
- **Concept:** Robust file editing using standard Unix diffs.
- **Application:** The `patch_file` tool for agents to modify workspace documents without brittle string matching.
