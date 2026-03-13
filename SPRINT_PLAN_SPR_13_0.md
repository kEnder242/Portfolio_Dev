# Sprint Plan: [SPR-13.0] Silicon Stability & Forensic Clarity
**Status:** ACTIVE | **Goal:** Resolve VRAM instability, implement Split Status Model, and harden Forensic Ledger.

## 🎯 THE MISSION
To stabilize the **Unified 3B Base** on the 2080 Ti (11GB) following the vLLM 0.17 transition and the recent 02:40 AM "Silicon Scrub" crash. This sprint hardens the **Forensic Ledger [FEAT-151]**, implements the **Split Status Model [FEAT-045]**, and formalizes the **Attendant V3 (Service + Proxy)** architecture to eliminate orchestration conflicts.

---

## 🏗️ ARCHITECTURAL MANDATES

### 1. Attendant V3 (Service + Proxy) [NEW]
*   **Master (Service):** Sole governor of silicon and state; hosts port 9999.
*   **Proxy (MCP):** Stateless agentic interface; redirects tool calls via internal REST to avoid port/PID conflicts.
*   **Port-Strict Assassin:** [FEAT-119] Refined to target only processes physically holding Lab ports (8088, 8765), protecting control scripts.

### 2. The Atomic File Swap Protocol [BKM-022]
*   **Purpose:** Ensure filesystem atomicity for all file updates.
*   **Mechanism:** Standardize on `.tmp` + `os.replace` for the **Forensic Ledger** and state snapshots.

### 3. The Split Status Model [FEAT-045/151]
*   **Volatile Status (Liveness):** Real-time system health retrieved from the Master API (:9999/heartbeat).
*   **Forensic Ledger (History):** Append-only, atomic-write-protected record (`pager_activity.json`) preserving historical alerts and log traces.

---

## 🧪 FORENSIC TRIAGE & WIN RECIPE (Mar 13 Update)

### 1. The "Win Recipe" (from 0.16 Archeology)
*   **Engine:** vLLM 0.17 (V1 Architecture).
*   **Backend:** `TRITON_ATTN` (Required for 3B models on Compute 7.5; FlashInfer JIT fails).
*   **Utilization:** `0.5` (Verified "Safe Win" for 3B models; `0.4` is the redline).
*   **Network:** `NCCL_P2P_DISABLE=1` and `NCCL_SOCKET_IFNAME=lo`.

### 2. Baseline Verification [COMPLETE]
*   **Success:** Established confirmed baseline with **1.5B model** (`qwen-2.5-1.5b-awq`).
*   **VRAM Peak:** 5178 MiB (46%) under `TRITON_ATTN`.
*   **Reasoning:** Physically verified via inference ping.

---

## 🏗️ SPRINT PHASES

### PHASE 1: Forensic Hardening (The V3 Pivot) [COMPLETE]
- [x] **Implementation:** Refactor to **Attendant V3** (Master/Proxy bifurcation).
- [x] **Logic:** Fix `log_monitor_loop` to correctly maintain file pointers for readiness signals.
- [x] **Assassin:** Implement Port-Strict matching to prevent Signal 9 "Self-Kills."

### PHASE 2: VRAM Optimization & Config Exploration [ACTIVE]
- [ ] **Characterization:** Run `test_apollo_vram.py` (V3-Aware) on the 1.5B baseline with `0.5 utilization` and `TRITON_ATTN`.
- [ ] **Decoupling [FEAT-145]:** Update `mass_scan.py` to skip EarNode loading during heavy synthesis.
- [ ] **Scale-Up:** Attempt 3B-AWQ ignition using the verified "Win Recipe."

### PHASE 3: Watchdog Recovery & Resilience
- [ ] **Recovery Logic:** Implement "One-Touch Auto-Restart" in the Master watchdog.
- [ ] **Resilience Ladder [FEAT-069]:** Re-integrate autonomous downshifting (vLLM -> Ollama) during VRAM pressure (>85%).

---

## 🛠️ BKM PROTOCOLS (The Implementation Law)

### [BKM-REPRO] VRAM Guard Audit
*   **One-liner:** `python3 HomeLabAI/src/debug/test_vram_guard.py`
*   **Core Logic:** Physical VRAM polling + Inference Ping to verify "Living Weights."
*   **Success Gate:** Breakthrough of the 333MiB Wall + HTTP 200 response.

---
*Reference: [BKM-018] Orchestrator-First Mandate (Attendant V3)*
