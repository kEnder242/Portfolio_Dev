# Post-Mortem: Acme Lab Stabilization (v3.4.17) - February 11, 2026

## Objective
To achieve a stable and reliably manageable Acme Lab Intercom server (`acme_lab.py`) that can be controlled and observed by the Gemini CLI agent.

## I. Initial State & Problem Description
*   `acme_lab.py` was in a persistent crash-restart loop or failing to start in the background.
*   Debugging was hampered by:
    *   NVIDIA driver issues (system-level instability).
    *   Logger hijacking by AI/ML libraries (`nemo`, `chromadb`).
    *   Fragile WebSocket transport handling client disconnects.
    *   Aggressive `os._exit(0)` in `acme_lab.py`.
    *   Inconsistent output redirection and buffering with `nohup`.
    *   Limitations of the `run_shell_command` tool for managing long-running background processes and streaming `stdout` live.
    *   A port conflict (8765) due to lingering processes.

## II. Analysis & Learnings

### A. System-Level Resilience (NVIDIA Driver)
*   **Problem**: A kernel update broke NVIDIA drivers, rendering the GPU unusable and causing underlying AI/ML components to fail. This was the foundational instability.
*   **Resolution**: User-executed `sudo apt install nvidia-driver-570 nvidia-dkms-570 nvidia-cuda-toolkit` and `sudo update-initramfs -u`, followed by reboot. **Key learning**: Always verify `nvidia-smi` status early.

### B. Robust Logging ("Montana Protocol")
*   **Problem**: `logging` handlers were hijacked by `nemo`, `chromadb`, etc., leading to silent crashes and diagnostic blindness.
*   **Resolution**: Implemented `reclaim_logger()` in `acme_lab.py` to aggressively reset root handlers, set custom handlers (to `sys.stderr` and `server.log`), and muzzle rogue loggers. This function is called after imports and after heavy loads.
*   **Key Learning**: In complex Python environments with heavy libraries, explicit, aggressive logger management is vital.

### C. Stable Resident Initialization
*   **Problem**: Parallel `asyncio.gather` for MCP resident initialization (`archive_node`, `pinky_node`, `brain_node`) caused `mcp.shared.exceptions.McpError: Connection closed` due to race conditions or resource contention on startup.
*   **Resolution**: Reverted to **sequential initialization** with a `2-second asyncio.sleep()` between each resident in `acme_lab.py`. This "slow and steady" approach proved more stable.

### D. Non-Blocking Equipment Loading (EarNode)
*   **Problem**: `EarNode` (NeMo) loading blocked the main event loop for ~45 seconds, making the server unresponsive during boot and causing client timeouts. It also had VRAM footprint issues.
*   **Resolution**:
    *   Moved `EarNode` initialization to a background `asyncio.to_thread`.
    *   Optimized VRAM: Explicitly used FP16 (`.half()`) and `torch.cuda.empty_cache()`.
    *   Proactive CUDA Graph Disable (`_sledgehammer_disable_graphs()`) to prevent crashes.
    *   **Tactical Decision**: `DISABLE_EAR=1` is currently active to ensure core server stability while `EarNode` is refined.

### E. Client-Server Flow & Shutdown Logic
*   **Problem**: `acme_lab.py` dropped messages if `self.status != "READY"`, causing client timeouts. `DEBUG_BRAIN` mode was also auto-shutting down too quickly.
*   **Resolution**:
    *   Implemented "Lobby Access": Handshakes and file browsing are allowed immediately.
    *   Pinky provides "Still warming up..." replies if asked before `READY`.
    *   `DEBUG_BRAIN` mode's auto-shutdown logic was corrected to only trigger on client disconnect, preventing premature exits.

### F. Orchestration & Agent-Tool Limitations
*   **Problem**: The Gemini CLI agent's `run_shell_command` proved inadequate for robustly launching, managing, and streaming logs from long-running background processes. This led to persistent "stuck" states and debugging difficulties.
*   **Resolution**: Architected and implemented the `lab_attendant.py` as a dedicated **`systemd` service**.
*   **Key Learning**: For persistent background process management, delegate to an OS-native service manager (`systemd`). The agent's role shifts from process launcher to service API client.

## III. Current Stable State (v3.4.17)
*   **NVIDIA Driver**: Fully functional.
*   **`lab_attendant.service`**: Running as a `systemd` service, managing `acme_lab.py`.
*   **`acme_lab.py`**: Successfully launches in `SERVICE_UNATTENDED` mode.
*   **`EarNode`**: Currently disabled (`DISABLE_EAR=1`) to maintain core stability.
*   **Lobby Access**: Clients can connect and browse files immediately.
*   **Logging**: Robust "Montana Protocol" ensures all logs are captured reliably in `HomeLabAI/server.log` and are accessible via `lab_attendant`'s status endpoint or `sudo journalctl -u lab-attendant.service`.

## IV. Future Work & Next Steps

1.  **Re-enable and Debug `EarNode`**: With core stability, the next major task is to fully re-enable `EarNode` and resolve its `list index out of range` import error (likely related to CUDA paths or library loading order).
2.  **Granular INIT States**: Implement broadcast of more detailed `INIT` states *after* `READY` in `acme_lab.py` (e.g., `EAR_READY`, `AGENTS_ONLINE`).
3.  **Unit & Integration Tests**: Develop `pytest` unit tests for `acme_lab.py`'s lifecycle and integration tests for `lab_attendant`'s API.
4.  **Round Table Lock Contention**: Investigate and robustly handle `round_table.lock` interactions for `mass_scan.py` and other background processes.
5.  **Refine `attendant_liveliness.py`**: Further enhance the `attendant_liveliness.py` script for more advanced polling and status reporting.

This session involved a significant amount of architectural refactoring and debugging, but it has resulted in a much more robust and observable Lab environment.
