# Retrospective: Lab Stabilization - February 11, 2026

## I. Problem Statement
The Acme Lab Intercom server (acme_lab.py) exhibited persistent startup failures, silent crashes, and inconsistent connectivity across various backgrounding attempts. This led to a high-friction debug cycle, characterized by "rapid-fire reboots" (both real and perceived) and a lack of clear diagnostic feedback. The core issues manifested as an inability to achieve a stable "Lobby" state or fully functional Web/Terminal UI communication.

## II. Root Causes & Learnings

### A. System-Level Instability (NVIDIA Driver Catastrophe)
*   **Root Cause**: An underlying NVIDIA GPU driver communication failure (due to a Linux kernel update) rendered the system fundamentally unstable for any GPU-dependent process. This was the silent killer behind many seemingly unrelated crashes.
*   **Learning**: **Always perform a `nvidia-smi` check as the absolute first step in any new session.** The agent must prioritize verifying system-level hardware readiness over application-level debugging.
*   **Remediation**: Manual user intervention required (driver purge, reinstall, `update-initramfs -u`, reboot).

### B. Logger Hijacking & Diagnostic Blindness ("Montana Protocol")
*   **Root Cause**: Heavy AI/ML libraries (specifically NeMo, ChromaDB, Sentence-Transformers) aggressively reconfigured the Python `logging` module during their import, wiping out the `acme_lab.py`'s intended handlers. This resulted in:
    *   Logs disappearing or being reformatted by external modules.
    *   `logging.basicConfig` being ineffective if called after a hijacker.
    *   Silent background process deaths due to buffered output not being flushed to disk.
*   **Learning**: Default Python logging is fragile in complex ML environments. Aggressive, explicit logger control is required.
*   **Solution Implemented**: The "Montana Protocol" (`reclaim_logger()` function) was developed to:
    *   Proactively wipe all existing root logger handlers.
    *   Forcefully re-add a `StreamHandler` (to `sys.stderr` for visibility) and a `FileHandler` (with autoflush) with the desired format.
    *   Set rogue module loggers (e.g., `nemo`, `chromadb`) to `ERROR` level and disable propagation to prevent spam.
    *   Run `reclaim_logger()` at critical points (after imports, after heavy loads).

### C. WebSocket Transport Fragility & Shutdown Logic
*   **Root Cause**: The `aiohttp` WebSocket `ClientConnectionResetError` was killing the main server if a client disconnected unexpectedly, especially during the CPU-intensive NeMo loading. Additionally, `DEBUG_BRAIN` mode was incorrectly configured to restart after client disconnects.
*   **Learning**: Network transport should be resilient. Client-side behavior should never be fatal to the server. Debug modes must provide predictable shutdown behavior.
*   **Solutions Implemented**:
    *   **Hardened `ws.send_str`**: All `ws.send_str` calls were wrapped in `try/except` blocks.
    *   **Revised Shutdown**: The server's `client_handler` `finally` block was adjusted to ensure `DEBUG_BRAIN` mode exits gracefully *only* when the client explicitly ends the session.

### D. Resident Initialization Deadlocks & Race Conditions
*   **Root Cause**: Initial attempts at parallel `asyncio.gather` initialization of MCP nodes (Archive, Pinky, Brain) led to `mcp.shared.exceptions.McpError: Connection closed`. This indicated a race condition or deadlock where one resident failed to initialize, taking down the entire `AsyncExitStack`.
*   **Learning**: While `asyncio.gather` is powerful, complex inter-process communication (like MCP's `stdio_client`) requires more delicate sequencing, especially on resource-constrained hardware.
*   **Solution Implemented**: Reverted to **Sequential Initialization** of MCP nodes (Archive -> Pinky -> Brain) with a **2-second `asyncio.sleep`** between each to allow OS buffers to settle. This "Slow & Steady" approach proved more robust.

### E. EarNode (STT) Overload & Blocking Initialization
*   **Root Cause**: The heavy NeMo model loading blocked the main event loop for ~45 seconds, making the "Lobby" unresponsive and triggering client timeouts. EarNode was also using FP32 precision, consuming 5GB VRAM.
*   **Learning**: Heavy equipment initialization must be offloaded to prevent blocking the main server loop. VRAM optimization is crucial.
*   **Solutions Implemented**:
    *   **Non-Blocking EarNode**: Moved `EarNode` initialization to a background `asyncio.to_thread`.
    *   **VRAM Optimization**: Explicitly cast NeMo model to `.half()` (FP16) and called `torch.cuda.empty_cache()`, reducing its footprint from ~5GB to ~1.5GB.
    *   **Proactive CUDA Graph Disable**: Added `_sledgehammer_disable_graphs()` in EarNode's `__init__` for stability.

### F. Client-Server Communication Flow ("Lobby Access")
*   **Root Cause**: The server's "Strict Readiness" gate (`if self.status != "READY": continue`) was dropping valid client handshakes during boot, leading to client-side timeouts and reconnection loops.
*   **Learning**: The server must provide immediate, clear feedback even during initialization.
*   **Solutions Implemented**:
    *   **Lobby Access**: Handshakes and Filing Cabinet browsing are now allowed immediately upon connection.
    *   **Granular Boot Reporting**: The server broadcasts `[LOBBY]` messages as residents initialize.
    *   **Lobby Persona**: Pinky replies with "Narf! Still in the Lobby..." for queries received before `READY`.

## III. Future Ideas & Cold Start Protocol

### A. Enhanced Cold Start Protocol
*   **NVIDIA Driver Check**: Always run `nvidia-smi` as the absolute first step in a new session. If it fails, immediate manual driver recovery is required.
*   **Tmux for Production**: For long-running `SERVICE_UNATTENDED` mode, explicitly launch `acme_lab.py` inside a `tmux` session to ensure persistence and log capture.
*   **Pre-Flight Script**: Develop a `preflight.sh` script that:
    *   Checks `nvidia-smi`.
    *   Verifies Python environment (`.venv`).
    *   Checks for orphaned `acme_lab.py` processes/port locks.
    *   Confirms `PYTHONPATH` and other critical environment variables.

### B. Further Debugging Tools
*   **`test_liveliness.py` v1.5**: Needs to be updated to reliably test the full "Lobby" sequence and report progress, not just timeout. It should also actively check for a running PID before attempting connection.
*   **Client-Side Debugging**: Implement more verbose console logging in `intercom_v2.js` for audio stream status and WebSocket message types.

### C. Feature Refinements
*   **Robust Mic Logic**: Investigate and stabilize the `intercom_v2.js` microphone `stop_audio` control flow to prevent immediate muting.
*   **"DEBUG_BRAIN" Script**: Create a `debug_brain.sh` script that launches `acme_lab.py` in `DEBUG_BRAIN` mode and automatically tails the log, ready for a direct `intercom.py` connection.
*   **Automate Test Cycles**: Implement a script that performs a clean launch, waits for ready, runs `test_liveliness.py`, and reports.

## IV. Conclusion
This session highlighted the fragility of complex AI systems under external system-level pressures (driver updates) and the importance of robust logging, error handling, and a clear understanding of asynchronous process lifecycles. The "Montana Protocol" and sequential initialization have significantly improved the Lab's stability and diagnosability, setting the stage for a more reliable future.
