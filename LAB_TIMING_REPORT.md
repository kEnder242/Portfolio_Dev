# ECOSYSTEM TIMING REPORT: The "Resonant Clock" Audit

I have synthesized the Lab's timing architecture from the forensic grep results. I am currently in **REPORT ONLY** mode.

#### 1. Comprehensive Timer Inventory

| System | Component | Interval / Timeout | Rationale |
| :--- | :--- | :--- | :--- |
| **Hub** | `pulse_loop` | **2s** | Real-time foyer updates (VRAM/Status). |
| **Hub** | `check_brain_health` | **120s** (Cooldown) | Protects Windows 4090 from redundant generation probes. |
| **Hub** | `Vibe Routing` | **5s** (Timeout) | Prevents the `archive` node from deadlocking the triage path. |
| **Hub** | `AFK Hibernate` | **600s** (10m) | **[FEAT-249]** Automatic Level 2 offload after inactivity. |
| **Nodes** | `probe_ttl_success` | **300s** (5m) | Cache engine resolution to reduce per-query network hits. |
| **Attendant** | `vram_watchdog` | **10s** | Background VRAM monitoring and orphan reaping. |
| **Attendant** | `Triton Settle` | **120s** | Mandatory wait for kernel residency on Turing silicon. |
| **Attendant** | `Ignition Gate` | **180s** | Max wait for cognitive readiness (Functional Ping). |
| **Attendant** | `PCIe Grace` | **5s** | Post-subprocess delay for OS environment alignment. |
| **Scanner** | `Dream Cycle` | **3600s** (1h?) | Periodic memory synthesis. |

---

#### 2. Brainstorming Representations

I have selected the top two ways to visualize this cyclical and hierarchical timing data.

**Method A: The "Pulse & Decay" Radial Diagram**
*   **Concept**: A clock-style concentric visualization.
*   **The Rings**:
    *   *Inner Ring (Fast)*: The 2s `pulse_loop` tick.
    *   *Middle Ring (Variable)*: The 120s `Brain Keepalive` countdown. Every user interaction or model response resets this ring to 100% (The Latch).
    *   *Outer Ring (Slow)*: The 10m `AFK Hibernate` countdown.
*   **High Level**: Allows you to see the Lab's "Metabolism" at a glance. If all rings are drifting toward 0, the Lab is approaching Deep Sleep.

**Method B: The "Silicon State Gantt" (Event-Driven)**
*   **Concept**: A horizontal timeline that doesn't just show time, but **state transitions**.
*   **Visualization**:
    *   A block for `WAKING` (showing the 65s settle vs 180s limit).
    *   A repeating tick mark for `PROBING` (the 30s TTL).
    *   A shaded area for `HIBERNATION` (showing the 90s offload curve).
*   **High Level**: Essential for debugging "Restoration Illusions." It proves *why* the Lab isn't ready yet by showing the physical dependencies (e.g., "Waiting for Triton Settle").

**Method C: The "Silicon Flame Graph" (Resource Contention)**
*   **Concept**: A standard Flame Graph where the X-axis is time and the Y-axis is **Process Hierarchy**.
*   **Visualization**:
    *   The base bar is `lab-attendant.service`.
    *   Stacked above it are the `Hub` and `vLLM` processes.
    *   When a JIT compilation or a weight-swap occurs, the "Flame" spikes in width, showing which specific operation is consuming the event loop.
*   **High Level**: Excellent for identifying **Silicon Stalls**. If the `vLLM` bar is wide but the `Hub` bars above it are missing, we have a clear ZMQ/Inference deadlock.

---

#### 3. Grafana Brainstorming (Beyond Time Series)

Grafana is traditionally a line-graph tool, but for **Cyclical Lab Data**, we can leverage advanced panels:

1.  **Status History Panel (The "Barcode" View)**:
    *   **Data**: Map `operational`, `engine_up`, and `engine_vocal` states.
    *   **Value**: Shows exactly when the Lab "lost its voice" over time. Vertical bars represent each state, making patterns of instability instantly visible.
2.  **State Timeline Panel**:
    *   **Data**: Map the "Reasons" for ignition (e.g., `MANUAL`, `RESTORE_INTERCOM`, `IDLE_TIMEOUT`).
    *   **Value**: Beyond just "Time," it shows the **Intent Frequency**.
3.  **Data Collection (The "Harvester")**:
    *   **Method 1: Promtail (Log-Based)**: Scrapes `server.log` and `vllm_server.log` for `[HEALTH]` and `[VRAM_TRACE]` tags. Low overhead, already partially in place.
    *   **Method 2: Metric Exporter (Push-Based)**: Add an `/metrics` endpoint to the Attendant that exports Prometheus-style gauges for `last_prime_delta` and `idle_seconds`. This is more "Professional" and provides cleaner data for Method A (Radial diagrams).
