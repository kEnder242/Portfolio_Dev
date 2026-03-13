# Sprint Plan: [SPR-13.0] Silicon Stability & Forensic Clarity
**Status:** ACTIVE | **Goal:** Resolve VRAM instability, implement Split Status Model, and harden Forensic Ledger.

## 🎯 THE MISSION
To stabilize the **Unified 3B Base** on the 2080 Ti (11GB) following the vLLM 0.17 transition and the recent 02:40 AM "Silicon Scrub" crash. This sprint hardens the **Forensic Ledger [FEAT-151]**, implements the **Split Status Model [FEAT-045]**, and formalizes the **Attendant V3 (Service + Proxy)** architecture to eliminate orchestration conflicts.

---

## 🏗️ ARCHITECTURAL MANDATES

### 1. Attendant V3 (Service + Proxy) [COMPLETE]
*   **Master (Service):** Sole governor of silicon and state; hosts port 9999.
*   **Proxy (MCP):** Stateless agentic interface; redirects tool calls via internal REST to avoid port/PID conflicts.
*   **Port-Strict Assassin:** [FEAT-119] Refined to target only processes physically holding Lab ports (8088, 8765), protecting control scripts.
*   **Dynamic Configuration:** Attendant now consumes utilization and backend flags from `vram_characterization.json` at runtime.

### 2. Operational Modes [NEW]
*   **SERVICE_UNATTENDED:** Default production mode. Persistent residency for background tasks (Nibbler).
*   **DEBUG_BRAIN:** Interactive mode. Loads full stack but executes auto-shutdown on client disconnect.
*   **DEBUG_PINKY:** Orchestration test mode. Loads only the Experience Node (Pinky), bypassing GPU inference.

### 4. Infrastructure-First Mandate [NEW]
*   **Avoid the Shell Trap:** Manual orchestration via `curl`, `requests` one-liners, or complex shell scripts is an anti-pattern. These "baby steps" lead to process fragmentation and "Assassin" collisions.
*   **Tool Stewardship:** The agent must exclusively use the **Lab Attendant MCP tools** (`lab_start`, `lab_stop`, `lab_quiesce`) for Lab orchestration. These tools handle the "Physical Truth" (PGIDs, ports, and scrubs) atomically.

---

## 🧪 FORENSIC TRIAGE & WIN RECIPE (Mar 13 Final)

### 1. The Production "Win Recipe" (vLLM 0.17)
*   **Model:** `llama-3.2-3b-instruct-awq` (UNIFIED Tier).
*   **Backend:** `TRITON_ATTN` (Mandatory for 3B models on Compute 7.5).
*   **Utilization:** `0.5` (Verified "Safe Win" for KV cache block allocation).
*   **Network:** `NCCL_P2P_DISABLE=1` and `NCCL_SOCKET_IFNAME=lo`.

---

## 🏗️ SPRINT PHASES

### PHASE 1: Forensic Hardening (The V3 Pivot) [COMPLETE]
- [x] **Implementation:** Refactor to **Attendant V3** (Master/Proxy bifurcation).
- [x] **Logic:** Fix `log_monitor_loop` file pointer bug to reliably catch readiness signals.
- [x] **Assassin:** Narrow focus to Port-Strict matching to prevent "Self-Kills."

### PHASE 2: VRAM Optimization & Scale-Up [COMPLETE]
- [x] **Characterization:** Run `test_apollo_vram.py` on 1.5B and 3B models.
- [x] **Dynamic Config:** Automate the "Win Recipe" via `vram_characterization.json`.
- [x] **Scale-Up:** Physically verified 3B residency using `TRITON_ATTN` at `0.5 util`.

### PHASE 3: Watchdog Recovery & Resilience [ACTIVE]
- [ ] **Implementation:** Finalize "One-Touch Auto-Restart" in the Master watchdog loop.
- [ ] **Resilience Ladder [FEAT-069]:** Re-integrate autonomous tiered downshifting:
    - **Tier 1 (vLLM Production):** `UNIFIED` (3B-AWQ).
    - **Tier 2 (vLLM SML):** Downshift to `LARGE` (1.5B) or `SMALL` (0.5B) vLLM tiers during pressure.
    - **Tier 3 (Ollama Fallback):** Shift to Ollama if vLLM engine remains unstable.
- [ ] **State Verification:** Use `DEBUG_PINKY` to verify the state-transition logic without VRAM risk.
- [ ] **Cleanup Verification:** Use `DEBUG_BRAIN` to confirm the 3B model unloads cleanly on disconnect.

---

## 🛠️ BKM PROTOCOLS (The Implementation Law)

### [BKM-SMOKE] Reasoning-First Smoke Test
*   **One-liner:** `curl -s -X POST http://localhost:8088/v1/chat/completions -d '{"model": "unified-base", "messages": [{"role": "user", "content": "ping"}], "max_tokens": 1}'`
*   **Mandate:** Port 8088 being open is NOT a success. The test must return a valid JSON choice to prove "Living Weights" and active reasoning.

### [BKM-REPRO] VRAM Guard Audit
*   **One-liner:** `python3 HomeLabAI/src/debug/test_vram_guard.py`
*   **Core Logic:** Combined physical VRAM polling + [BKM-SMOKE] reasoning gate.

---
*Reference: [BKM-018] Orchestrator-First Mandate (Attendant V3)*
