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

## 🛠️ Plan of Action: [FEAT-121] Distributed Tracing "Lab Fingerprint"
**Objective**: Eliminate "Ghost Processes" and "Sync Trust" gaps through verifiable execution context.

### 1. The Fingerprint Schema
Every Lab process will generate a 4-part identity at initialization:
`[BOOT_HASH : COMMIT_SHORT : NODE_ROLE : PID]`
*   **BOOT_HASH**: A dynamic 4-character hex (e.g., `A7B2`) generated at entry-point.
*   **COMMIT_SHORT**: Output of `git rev-parse --short HEAD` to verify disk-to-RAM synchronization.
*   **NODE_ROLE**: Identity of the process (HUB, ARCHIVE, PINKY, etc.).
*   **FILE_MTIME**: (Log-only) The modified timestamp of the executing `__file__` to verify sync completion.

### 2. [FEAT-122] Kernel-Level Visibility (Proc Title)
*   **Action**: Use `setproctitle` to rename processes in `ps`/`htop` to their full Fingerprint.
*   **Benefit**: Instant identification of "Ghost" processes from previous boot cycles without checking logs.

### 3. Montana Protocol Extension (Traceable Logs)
*   **Init Registration**: Every node logs its full Fingerprint and executing file path once at startup.
*   **Heartbeat (Optional/Configurable)**: A periodic `[STATUS_PULSE][Fingerprint]` log entry, disabled by default to prevent clutter but togglable for deep debugging of silent/hijacked logs.

### 4. Strategic Culprit: The Attendant's Blind Spot
*   **Diagnosis**: Current `cleanup_silicon` logic uses string-matching `SIGKILL`, which orphans resident subprocesses and skips `finally` cleanup blocks.
*   **Strategy**:
    *   **Process Groups**: Modify the Attendant to use `os.killpg()` to ensure entire process trees are terminated.
    *   **Fingerprint Audit**: Implement a "Ghost Hunter" tool that scans active PIDs for mismatched `BOOT_HASH` or `COMMIT_SHORT` tags and terminates them.

---
*Reference: [HomeLabAI/docs/plans/SPRINT_STATUS_VISIBILITY_v4.6.md](../HomeLabAI/docs/plans/SPRINT_STATUS_VISIBILITY_v4.6.md)*
