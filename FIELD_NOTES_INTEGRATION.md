# Field Notes <-> HomeLabAI Integration Strategy

**Version:** 1.0 (Draft)
**Status:** Planning / Partial Implementation
**Goal:** Define the interface between the static "Field Notes" portfolio and the active "HomeLabAI" agentic system.

---

## 1. Cognitive Architecture (The "Brain" Interface)

The Portfolio currently uses a "Direct Model Access" (DMA) pattern to generate tags and timelines. It bypasses the agentic personality of "Pinky" for raw speed and stability.

### Current Implementation: `OllamaClient`
- **Path:** `field_notes/ai_engine.py`
- **Protocol:** HTTP POST to `localhost:11434/api/generate`.
- **Logic:** Direct prompt engineering ("You are an archivist...").
- **Pros:** Fast, independent, works even if `Acme Lab` is offline.
- **Cons:** No "Memory" of previous chats; no "Personality."

### Future Implementation: `AcmeLabClient` (The Goal)
- **Path:** `field_notes/ai_engine.py` (Swappable Class)
- **Protocol:** MCP (Model Context Protocol) or WebSocket (`localhost:8765`).
- **Logic:** `client.call_tool("archive_notes", { "text": ... })`
- **Pros:** 
    - Pinky (The Agent) decides *if* it should run.
    - Pinky can "Remember" this context for later chats ("I remember reading your 2016 notes...").
    - Centralized governance (Privacy rules managed in one place).

### Migration Guide
To switch from Ollama to Acme Lab:
1. Ensure `HomeLabAI` exposes an "Archivist" capability (likely via `PinkyNode`).
2. Update `field_notes/ai_engine.py` to import `mcp.client`.
3. Replace `ask_pinky()` with an MCP tool call.

---

## 2. Telemetry Bridge (Prometheus & Grafana)

The "Slow Burn" (Background Indexing) and HomeLabAI itself need to be aware of system load.

### The Shared Truth: Prometheus (Port 9090)
Both systems should query the *same* metrics to avoid fighting for GPU resources.

**Metric:** `node_load1` (CPU) and `nvidia_gpu_duty_cycle` (if available).

**Portfolio Responsibility:**
- `nibble.py` checks `load < 0.5` before running a scan chunk.
- If load is high, it yields (Sleeps).

**HomeLabAI Responsibility (Planned):**
- **New Node:** `TelemetryNode` (or part of `BrainNode`).
- **Logic:** Before starting a "Dream" cycle or a heavy RAG ingestion:
    1. Query Prometheus.
    2. If `load > 2.0`, queue the task for later.
    3. *Bonus:* Pinky can "See" the heat. "I'm feeling a bit feverish (High Temp), let's wait."

### Dashboard Integration
- **Grafana:** The "Mission Control" on the Portfolio.
- **HomeLabAI:** Should act as a *writer* to Grafana (via Annotations).
    - *Example:* When Pinky finishes a "Dream," it posts an Annotation to the Grafana timeline: "Dream Cycle 45 Complete."

---

## 3. Data Exchange (The Knowledge Graph)

The Portfolio generates valuable structured data that the Lab should consume.

**Artifact:** `field_notes/pinky_index_full.json`
**Schema:**
```json
{
  "2016": {
    "strategic_theme": "...",
    "technical_tags": ["Simics", "Fulsim"],
    "key_events": [ ... ]
  }
}
```

**Ingestion Strategy:**
1.  **Symlink:** The Lab already has access to `~/Portfolio_Dev`.
2.  **RAG Sync:** Create a Lab tool `sync_career_memory()`.
    -   Reads `pinky_index_full.json`.
    -   Chunk strategy: "In 2016, Jason worked on Simics..."
    -   Upserts to **ChromaDB** (The Lab's Long Term Memory).
3.  **Benefit:** You can ask Pinky on your phone: *"When did I first use JTAG?"* and it retrieves the exact date from the Portfolio's research.

## 4. Future Capability: The Self-Refining Knowledge Graph
**Concept:** A "Gardening" loop where HomeLabAI actively curates the Portfolio.

### The Vision
Instead of a linear scan, the Lab implements a CMS-like loop:
1.  **Drafting:** Pinky scans raw logs and creates draft "Story Nodes" (JSON).
2.  **Critique:** The Brain Node reviews drafts against the "Strategic Themes" (Focals). "Is this log relevant to the Q3 Goal?"
3.  **Pruning:** Low-value logs are merged or deleted. High-value logs are promoted to "War Stories."
4.  **Display:** The Portfolio simply renders the curated `knowledge_graph.json`, removing the need for complex client-side logic.

### Technical Requirement
- **Shared Storage:** The `field_notes/data` directory must be writable by the `acme_lab` user/service.
- **State Management:** A SQLite DB or ChromaDB is required to track "Refinement Depth" (How many times has this node been reviewed?).

## 5. Boundary Risk Assessment (Portfolio <-> Lab)

### Risk 1: Concurrency & Locks
- **Scenario:** `nibble.py` (Portfolio) and `ArchiveNode` (Lab) try to write to `status.json` or `queue.json` simultaneously.
- **Impact:** Corrupt JSON. Data loss.
- **Mitigation:**
    - Use `sqlite` (WAL mode) instead of JSON for shared state.
    - Or enforce a "Single Writer" policy (Lab owns the write, Portfolio only reads).

### Risk 2: Permissions
- **Scenario:** `field-notes.service` runs as `jallred` (User). `acme-lab.service` might run as `acme` or root?
- **Impact:** Permission Denied errors when cleaning up files.
- **Mitigation:** Ensure both services run as the same user (`jallred`) or use a shared group (`lab_staff`) with `rw` permissions.

### Risk 3: Symlink fragility
- **Scenario:** `raw_notes` symlink breaks if the underlying drive (`~/knowledge_base`) moves or unmounts.
- **Mitigation:** Add a `pre-flight` check in `nibble.py` to verify the symlink resolves before queueing work.