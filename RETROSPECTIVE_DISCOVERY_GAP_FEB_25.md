# Retrospective: The "Ghost in the Machine" & The Discovery Gap [Feb 25, 2026]

## 1. The Context
I have been in a protracted debug loop attempting to finalize **[FEAT-117] Multi-Stage Discovery** and **[FEAT-120] Context Transparency**. The goal is to provide clickable source links (e.g., `[Ref: 2019.json]`) in the Intercom UI to prove truth-grounding and eliminate hallucinations.

## 2. The Forensic Scars (What happened)
*   **The Scoping Trap**: Python's `nonlocal` requirement for nested async functions inside `process_query` caused variables like `historical_context` to remain empty inside the reasoning chain despite successful retrieval. (Resolved).
*   **The Metadata Mismatch**: ChromaDB was using the key `date` or `source` in its metadata, while the code was strictly looking for `timestamp`. (Resolved).
*   **The Semantic Drift**: Vector similarity was prioritizing "Theme" (Validation) over "Year" (2019), leading to 2021/2023 results for a 2019 query.

## 3. The "Ghost in the Machine" (The Current Block)
Despite applying the **"Hard Year Filter"** logic to `archive_node.py` (forcing a metadata `where` filter on the year), the Lab server appears to be executing an older version of the code in memory.
*   **Symptom**: `server.log` refuses to show the new `[ARCHIVE]` or `[HISTORY]` logging tags added to the source on disk.
*   **Diagnosis**: Lingering zombie processes or stale `__pycache__` bytecode are likely persisting the old logic in RAM, even after `hard_reset` attempts.

## 4. Proposed Mitigation Strategies
*   **[BURN] The Cache Purge**: Recursively delete all `__pycache__` directories to force source re-reading.
*   **[ISOLATE] Node Verification**: Test the `ArchiveNode` as a standalone process to prove the RAG logic in a clean room before Hub integration.
*   **[SHIFT] The Atomic Port**: Temporarily move the Lab to port **8766** to bypass any zombies holding 8765.
*   **[PROOF] Metadata Audit**: A script to verify every collection key in the 2019 dataset to ensure the `where` filter matches the database schema.

## 5. Summary of Learnings
*   **Verification Velocity**: Waiting for full Lab boots (~30s) is the primary bottleneck for logic verification.
*   **Process Management**: `hard_reset` is insufficient for deep logic changes; aggressive process termination and cache purges are required for total synchronization.

---
*Reference: [HomeLabAI/docs/plans/SPRINT_STATUS_VISIBILITY_v4.6.md](../HomeLabAI/docs/plans/SPRINT_STATUS_VISIBILITY_v4.6.md)*
