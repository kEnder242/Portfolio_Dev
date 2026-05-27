# Bicameral Dispatch: System Design & Persona Architecture (v4.0)

> [!NOTE]
> **vLLM STATUS:** The metaphors described herein are fully realized via a native vLLM implementation on Turing (2080 Ti) silicon, utilizing Multi-LoRA residency [FEAT-030] to maintain sub-second TTFT across all nodes.

## 🏛️ The Acme Lab Taxonomy (The Glossary of Mind)
These metaphors serve as architectural anchors for the physical code:

- **Corpus Callosum**: The Hub (`acme_lab.py` / `cognitive_hub.py`). The asynchronous bridge that manages real-time token streaming [FEAT-233].
- **The Amygdala**: The **Triage Gate**. Uses the Lab Sentinel (vLLM adapter) to calculate the **Scalar Fuel** [FEAT-234], deciding which nodes to wake.
- **The Sentinel**: The **Domain Router**. The low-power first pass that identifies intent (RECALL, STRATEGIC, CASUAL) and domain (TELEMETRY, BKM, FORGE).
- **The Architect**: The Sovereign Brain (4090). The definitive synthesis layer for high-stakes technical derivations.
- **Dreaming**: Background memory consolidation [FEAT-067].
- **Sleeping Mind**: [FEAT-249] VRAM Hibernation. Engines are alive but passive until the **Vocal Handshake** triggers.

## 1. The Communication Hub (Waterfall Relay)

### A. Scalar Fuel [FEAT-234]
- **Formula**: `Fuel = ((1.0 - casual) * (intrigue + importance)) / 2`.
- **Thresholds**: 
    - **0.2**: Wakes the Shadow Brain (Archivist).
    - **0.6**: Wakes the Sovereign Brain (Architect).
- **Consensus**: Nodes can autonomously recommend fuel boosts using [Council of Hemispheres] signals.

### B. Inter-Node Waterfall [FEAT-233]
- **Streaming**: Pinky's intuitions are piped directly into Shadow's context window *while* generation is active.
- **Visibility**: Every node that consumes fuel produces a visible thought in the UI, ensuring no "Black Box" reasoning occurs.

### C. The Vocal Handshake [FEAT-368]
- **Logic**: Prevents "Silicon Silence" during engine ignition.
- **Behavior**: If the heavy model is still loading, Pinky provides a hardcoded Semantic Handshake ("establishing connections...") to acknowledge the user immediately.

## 2. Collaborative Workspace

### A. The Safe-Scalpel [FEAT-198]
- **Tool**: `safe_scalpel`. Lint-gated surgical patching protocol.
- **Validation**: Every automated edit is verified via `ruff` or `eslint` before being committed to the DNA.

### B. Double-Tap Search [FEAT-209]
- **Pattern**: RAG queries hit the Chronological Log AND the Strategic Meta files (Resume/CVT) simultaneously to maximize factual yield.

## 3. The Law of Semantic Indirection [BKM-015.1]

### A. Anti-Hardcoding Mandate
To prevent functional drift and "Logic Traps," the Lab prohibits hardcoded technical keywords in routing blocks.
- **Current Pattern**: Instead of `if "MSR" in query: load_msr_tool()`, the system utilizes the **Lab Sentinel** to classify the "Vibe" and "Intent" of the user.
- **Physical Implementation**: The Hub foyer performs a semantic pass to identify `RECALL` or `SILICON_TELEMETRY` before any tool-decision is made.

### B. Intent Authority
The **Lab Node (Sentinel)** is the sole authority for intent.
- **RECALL**: Triggers the ArchiveNode's `get_context` tool.
- **STRATEGIC**: Promotes the turn to the **Sovereign Brain** (4090).
- **CASUAL**: Handled by **Pinky** with minimal fuel usage.

### C. The Retrieval Exception
Per **BKM-015 #4**, hardcoded optimizations (like year-based regex) are permitted strictly for physical file retrieval *after* a semantic intent has been established. This ensures high-fidelity access to chronological logs without sacrificing semantic flexibility.
