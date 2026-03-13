# Architectural Design: Lab Attendant V3 (Service + MCP Proxy)
**Role:** [DESIGN] - Orchestration Decoupling
**Status:** ACTIVE (Sprint 13.0)

## 🎯 Problem Statement
Previous versions (V1/V2) treated the orchestration script as a dual-purpose entry point. This caused physical resource conflicts (Port 9999) when both the systemd service and the Gemini CLI attempted to initialize the hardware state machine simultaneously.

## 🏗️ The V3 Solution: Service + Proxy
V3 formalizes the Attendant as a permanent resident service with a stateless MCP Proxy for agentic interaction.

### 1. The Master (Resident Service)
*   **Role:** The sole governor of physical silicon, process groups (PGIDs), and VRAM.
*   **Infrastructure:** Hosts the critical REST API on port 9999.
*   **Interfaces:** Powers the `status.html` remote control and provides the backend for MCP tools.
*   **Guardians:** Executes the Watchdog, Assassin, and Quiescence loops.

### 2. The Proxy (Agentic Tooling)
*   **Role:** A stateless interface spawned by the Gemini CLI.
*   **Mechanism:** Detects `LAB_ATTENDANT_ROLE=PROXY` and bypasses all local hardware initialization.
*   **Command Flow:** Redirects MCP tool calls (`lab_start`, `lab_stop`) via internal `aiohttp` requests to the Master on `localhost:9999`.
*   **Safety:** By operating as a thin client, the Proxy avoids port conflicts and remains invisible to the Assassin's "Silicon Scrub."

## 🧱 Architectural Mandates
*   **Single State Machine:** All hardware state transitions occur within the Master service.
*   **Critical REST:** The REST API is the backbone of the Lab's observability and control, enabling both human (UI) and agentic (MCP) orchestration.
*   **Blocked Execution:** Direct execution of the Attendant script for hardware control is no longer supported; the Proxy pattern is the mandatory path for the agent.
