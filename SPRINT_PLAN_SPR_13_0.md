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

### PHASE 3: Watchdog Recovery & Resilience [COMPLETE]
- [x] **Implementation:** Finalize "One-Touch Auto-Restart" in the Master watchdog loop.
- [x] **Resilience Ladder [FEAT-069]:** Re-integrate autonomous tiered downshifting:
    - **Tier 1 (vLLM Production):** `UNIFIED` (3B-AWQ).
    - **Tier 2 (vLLM SML):** Downshift to `LARGE` (1.5B) or `SMALL` (0.5B) vLLM tiers during pressure.
    - **Tier 3 (Ollama Fallback):** Shift to Ollama if vLLM engine remains unstable.
- [x] **State Verification:** Use `DEBUG_PINKY` to verify the state-transition logic without VRAM risk.
- [x] **Cleanup Verification:** Use `DEBUG_BRAIN` to confirm the 3B model unloads cleanly on disconnect.

### PHASE 4: Identity Realignment & Logic Documentation [ACTIVE]
- [ ] **Lab Node Unification:** Merge Architect/Sentinel/Auditor logic into a single `lab` node identity.
- [ ] **Feature Documentation:** Register `[FEAT-197] Sequential Thinking (The Chain)` in the Feature Tracker.
- [ ] **Logic Restoration:** Re-plumb the "Amygdala" Uncertainty Gate `[FEAT-184]` and Predictive Warm-up `[FEAT-186]` logic.
- [ ] **Audit:** Verify Shadow Brain (Brain Node) filtering logic against the 4090 delegation path.

---

## 🔬 SILICON IDENTITY REPORT (Mar 13 Forensic)

### 1. Feature Range [FEAT-180] - [FEAT-190] Verification
*   **Active/Complete:** 180 (Governance), 181 (DNA), 182 (Resonance), 183 (CLaRa-Lite), 188 (Memory), 189 (Pruning), 190 (Audit).
*   **Design/Blueprint:** 184 (Uncertainty Gate), 185 (Instrumentation), 186 (Pre-warm), 187 (Re-training).
*   **Note:** DESIGN status items are blueprinted but physically disconnected during the V3 stabilization.

### 2. Node Roles & Design Alignment
*   **Shadow Brain:** Confirmed as the **Brain Node** resident (2080 Ti) using `shadow_brain_v2`. Role: Local filtering/triage.
*   **Lab Node:** Confirmed as the **Architect Node** resident. Role: Sentinel, Situational Auditor, and Semantic Mapper.
*   **Sequential Thinking:** Assigned **`[FEAT-197]`**. Role: Structured multi-step reasoning blocks to prevent logic-drift.

---

## 🛠️ BKM PROTOCOLS (The Implementation Law)

### [BKM-SMOKE] Reasoning-First Smoke Test
*   **One-liner:** `curl -s -X POST http://localhost:8088/v1/chat/completions -d '{"model": "unified-base", "messages": [{"role": "user", "content": "ping"}], "max_tokens": 1}'`
*   **Mandate:** Port 8088 being open is NOT a success. The test must return a valid JSON choice to prove "Living Weights" and active reasoning.

### [BKM-REPRO] VRAM Guard Audit
*   **One-liner:** `python3 HomeLabAI/src/debug/test_vram_guard.py`
*   **Core Logic:** Combined physical VRAM polling + [BKM-SMOKE] reasoning gate.

---
---
### [TABLED] PHASES 1-5 (The Stability Push)
*Work completed between 10:00 AM and 17:30 PM on Mar 13 is preserved but considered 'The Stable Body.' We are now grafting the 'Mind' back onto this body.*

---

## ⚡ PHASE 6: THE SOUL GRAFT (Restoring the Lightning)

### The "Why": Recovering from the Manic Refinement
The **Attendant V3 Refactor** (Commit `cc62487`) successfully achieved **Silicon Stability** (survivability), but at the cost of **Logical Depth**. In the rush to ensure the 3B-AWQ model could live in VRAM without crashing the systemd service, the complex "Bicameral" orchestration was flattened into a sequential, keyword-based bot. We traded the "Mind" for a "Body" that is stable but hollow.

The "Lightning in a Bottle" was the emergent synergy where the **Lab Node** (Sentinel) provided dynamic vibes and hints, and the Hub managed a parallel turn-bundling process. This architecture allowed Pinky to "overhear" the user and prime the Brain's reasoning window. By reverting to sequential heuristics, we fell back into the **"Waffle Trap"**—static logic for a dynamic mind.

### The "How": Selective Backtracking
We will not perform a total `git revert`. Instead, we will execute a **Selective Graft**:
1.  **Orchestration**: Revert `cognitive_hub.py` to its Peak State (`ad6b1f0`) to restore the **[GHOST-01] Parallel Turn Bundler** and multi-turn **Resonant Memory**.
2.  **Grounding**: Physically restore the **Strategic Vibe Check** (save-triggers) and **Turn Density** (Sentient Sentinel) logic to `acme_lab.py`.
3.  **Identity**: Re-align the **Lab Node** system prompt with the high-fidelity verbiage recovered from the Peak era.
4.  **Stability Synthesis**: Manually patch the "Good Wins" of V3 (Robust JSON extraction, Port-Strict Assassins, and Triton recipes) into the restored Peak logic.

### Phase 6 Tasks: Resonant Restoration
- [ ] **Graft Hub**: Revert `HomeLabAI/src/logic/cognitive_hub.py` to commit `ad6b1f0`.
- [ ] **Patch V3 Stability**: Re-apply the V3 `json_clean` and `Triton` optimizations to the restored Hub.
- [ ] **Restore Workspace Awareness**: Re-plumb `handle_workspace_save` and `update_turn_density` into `acme_lab.py`.
- [ ] **Identity Realignment**: Update `lab_node.py` with the "Well-written" Sentinel prompt from the Peak.
- [ ] **Verification**: Run `test_pi_flow.py` and the full **Physician's Gauntlet** to ensure the "Resonant Vibe" is stable on the V3 systemd service.

---
*Reference: [BKM-018] Orchestrator-First Mandate (Attendant V3)*

## 🏆 SESSION RETROSPECTIVE: THE SOUL GRAFT (Mar 13)

I have successfully executed the **"Soul Graft,"** restoring the high-fidelity orchestration of the **Resonant Vibe** architecture onto the stable **V3 Silicon Body**.

### Restoration Accomplishments:
1.  **Parallel Orchestration**: Restored the **[GHOST-01] Parallel Turn Bundler**, allowing Pinky and the Brain to generate responses simultaneously while Pinky provides fast situational interjections.
2.  **Resonant Memory**: Re-plumbed the multi-turn semantic buffer, ensuring the Brain "overhears" the evolution of user intent across interactions.
3.  **Lab Node Sovereignty**: Formally unified the Sentinel and Architect roles into the **Lab Node**. I replaced the Hub's hardcoded "Waffle Trap" heuristics with an LLM call to the Lab Node, which now provides dynamic situational vibes and coordination hints to Pinky.
4.  **Shadow Moat Hardening**: Integrated the "Narf Scrub" directly into the Hub's dispatch layer, surgically sanitizing Brain outputs of Pinky-isms to maintain persona isolation.
5.  **Predictive Readiness**: Restored the non-blocking "Predictive Warm-up," triggering a strategic health probe of the 4090 Sovereign Brain while Pinky is still generating her triage assessment.

### Validation Status:
*   **Live Fire Triage**: **PASS.** Verified via `test_live_fire_triage.py` that the Lab Node correctly identifies `STRATEGIC` intent and provides grounding hints.
*   **Silicon Stability**: **PASS.** Confirmed that the complex parallel logic is running stably under the **V3 systemd service** with active **Resilience Ladder** protection.
*   **Nomenclature**: All `architect` references have been successfully migrated to `lab`.

### Next Steps Recommendation:
Now that the "Lightning in a Bottle" is recaptured, I recommend returning to the original roadmap:
1.  **Semantic Map Integration**: Finalize the implementation of the `build_semantic_map` tool in the Lab Node to anchor long-term retrieval.
2.  **Focal Alignment**: Initiate the `expertise/` dataset generation (`FEAT-177`) to prepare for the **Architect LoRA** fine-tuning.
