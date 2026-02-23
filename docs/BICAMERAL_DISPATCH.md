# Bicameral Dispatch: System Design & Persona Architecture (v3.5)

> [!NOTE]
> **vLLM STATUS:** The features described herein (Amygdala, Sentinel, Corpus Callosum) were originally designed for a native vLLM implementation. While currently **TABLED** for the Turing (2080 Ti) due to BF16 deadlocks, the logic remains the architectural blueprint for future Ampere+ deployments. The Lab currently uses an **Ollama-Standard** implementation of these metaphors.

## 🏛️ The Acme Lab Taxonomy (The Glossary of Mind)
These metaphors serve as architectural hints for system design:

- **Corpus Callosum**: The Hub (`acme_lab.py`). The asynchronous bridge that manages hemispheric communication.
- **The Amygdala**: The **Logic Structure**. The specific triage gate inside the Hub that decides, "This signal matches a known 'Scar' or 'Uncertainty'—wake the Brain now."
- **The Sentinel**: The **Sensory State**. The active, low-power background listening loop (the "Eyes and Ears") that feeds the Amygdala.
- **The Architect**: The **Hierarchy Refactoring**. A background node that decides how memories should be organized (e.g., "This belongs in the strategic Resume layer, not just tactical Notes").
- **Dreaming**: The **Memory Consolidation**. Turning the day's tactical chatter into summarized "Wisdom."
- **Sleeping Mind**: A resident model (Shared Weights) that is "Resident but Respendable" (Pre-cached).
- **The Phone Ring**: An unscheduled user connection (WebSocket) that triggers an immediate "Wake."
- **The Alarm Clock**: Scheduled background tasks (Job Search, Dreaming, Burn).
- **Banter TTL**: Weighted decay that prevents infinite hemispheric arguments.

## 1. The Communication Hub (Corpus Callosum)

### A. The Amygdala (Sentinel v2.0)
- **Logic:** Moves beyond brittle keywords. Brain interjects if it detects Pinky being too simplistic or if a "Validation Scar" from the archives is logically relevant.
- **Trigger:** "Strategic Uncertainty"—detected logical gaps or requests for scaling.

### B. The Sleeping State (Pre-Cache)
- **Philosophy:** Weights remain resident in VRAM for instant response but are invalidated via **SIGTERM** by the Lab Attendant if a non-AI task (Game/Transcode) requests resources.
- **Ollama Parity:** Implement prompt-swapping to allow Ollama to mimic vLLM persona concurrency (albeit slower).

## 2. Collaborative Workspace

### A. The Strategic Patch Tool
- **Tool:** `patch_file`. Described to agents as "The Strategic Architect's Scalpel."
- **Validation Vibe Check:** Upon a `💾 SAVE` event, the Brain performs active logic/code validation (e.g., race condition checks) rather than just acknowledging the save.

### B. The Hierarchical Semantic Map
- **Structure:** 
    1. **Top Layer:** Resume/CVT (Strategic Summary).
    2. **Middle Layer:** Insights/Focals (Technical themes).
    3. **Bottom Layer:** Raw Notes (Detailed scars).
- **Consumer:** Pinky uses the Semantic Map as his "Working Memory" to ground his reactive responses.
