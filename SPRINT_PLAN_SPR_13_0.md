# Sprint Plan: [SPR-13.0] Silicon Stability & Forensic Clarity
**Status:** ACTIVE | **Goal:** Resolve VRAM instability, implement Split Status Model, and harden Forensic Ledger.

## 🎯 THE MISSION
To stabilize the **Unified 3B Base** on the 2080 Ti (11GB) following the vLLM 0.17 transition and the recent 02:40 AM "Silicon Scrub" crash. This sprint hardens the **Forensic Ledger [FEAT-151]**, implements the **Split Status Model [FEAT-045]**, and formalizes the **Attendant V3 (Service + Proxy)** architecture to eliminate orchestration conflicts.

---

## 🏗️ ARCHITECTURAL MANDATES

### 1. Attendant V3 (Service + Proxy) [COMPLETE]
*   **Master (Service):** Sole governor of silicon and state; hosts port 9999.
*   **Proxy (MCP):** Stateless agentic interface; redirects tool calls via internal REST to avoid port/PID conflicts.
*   **Port-Strict Assassin:** [FEAT-119] Refined to target only processes physically holding Lab ports (8088, 8765), protecting control scripts and model paths.
*   **Dynamic Configuration:** Attendant now consumes utilization and backend flags from `vram_characterization.json` at runtime.

### 2. The Atomic File Swap Protocol [BKM-022] [COMPLETE]
*   **Purpose:** Ensure filesystem atomicity for all file updates.
*   **Mechanism:** Standardize on `.tmp` + `os.replace` for the **Forensic Ledger** and state snapshots.

### 3. The Split Status Model [FEAT-045/151] [COMPLETE]
*   **Volatile Status (Liveness):** Real-time system health retrieved from the Master API (:9999/heartbeat).
*   **Forensic Ledger (History):** Append-only, atomic-write-protected record (`pager_activity.json`) preserving historical alerts and log traces.

---

## 🧪 FORENSIC TRIAGE & WIN RECIPE (Mar 13 Final)

### 1. The Production "Win Recipe" (vLLM 0.17)
*   **Model:** `llama-3.2-3b-instruct-awq` (UNIFIED Tier).
*   **Backend:** `TRITON_ATTN` (Mandatory; FlashInfer JIT build fails on Compute 7.5).
*   **Utilization:** `0.5` (Verified "Safe Win" providing necessary KV cache blocks).
*   **Network:** `NCCL_P2P_DISABLE=1` and `NCCL_SOCKET_IFNAME=lo`.

### 2. Verification Gates [COMPLETE]
*   **1.5B Baseline:** Verified reasoning and VRAM (5125 MiB).
*   **3B Production:** Verified reasoning and VRAM (5125 MiB).
*   **Path Awareness:** Diagnostic suite and Attendant are working directory-independent.

---

## 🏗️ SPRINT PHASES

### PHASE 1: Forensic Hardening (The V3 Pivot) [COMPLETE]
- [x] **Implementation:** Refactor to **Attendant V3** (Master/Proxy bifurcation).
- [x] **Logic:** Fix `log_monitor_loop` file pointer bug to reliably catch readiness signals.
- [x] **Assassin:** Implement Port-Strict matching to eliminate Signal 9 "Self-Kills."

### PHASE 2: VRAM Optimization & Scale-Up [COMPLETE]
- [x] **Characterization:** Run `test_apollo_vram.py` on 1.5B and 3B baselines.
- [x] **Dynamic Config:** Update `vram_characterization.json` and Attendant to automate the "Win Recipe."
- [x] **3B Scale-Up:** physically verified 3B residency using TRITON_ATTN.

### PHASE 3: Watchdog Recovery & Resilience [ACTIVE]
- [ ] **Implementation:** Finalize \"One-Touch Auto-Restart\" in the Master watchdog loop.
- [ ] **Resilience Ladder [FEAT-069]:** Re-integrate autonomous tiered downshifting:
    - **Tier 1 (vLLM Production):** `UNIFIED` (3B-AWQ).
    - **Tier 2 (vLLM SML):** Downshift to `LARGE` (1.5B) or `SMALL` (0.5B) tiers to preserve residency during pressure.
    - **Tier 3 (Ollama Fallback):** Shift to Ollama if vLLM engine remains unstable.
- [ ] **Mode Verification:** Audit `DEBUG_BRAIN` and `DEBUG_PINKY` modes to ensure correct auto-shutdown and bypass behavior in V3.
- [ ] **Smoke Test Suite:** Standardize a rapid `/ping` smoke test for the CI/CD pipeline.


---

## 🛠️ BKM PROTOCOLS (The Implementation Law)

### [BKM-REPRO] VRAM Guard Audit
*   **One-liner:** `python3 HomeLabAI/src/debug/test_vram_guard.py`
*   **Core Logic:** Physical VRAM polling + Inference Ping to verify "Living Weights."
*   **Success Gate:** Breakthrough of the 333MiB Wall + HTTP 200 response.

---
*Reference: [BKM-018] Orchestrator-First Mandate (Attendant V3)*
