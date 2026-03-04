# Sprint Plan: [SPR-11-07] The Bicameral Evolution
**Status:** ACTIVE | **Goal:** Transition to Attendant V2, integrate Qwen 27B, and refine Bicameral Synergy.

## 🎯 THE MISSION
To evolve the relationship between **Pinky** and **The Brain** from a simple "UI/Engine" split into an organic, emergent collaboration. This sprint serves as the production debut for the **Bilingual Attendant (V2)** and the **Sovereign Ultra (Qwen 27B)** tier.

---

## 🏗️ SUPPORTING ARCHITECTURE & MODELS

### 1. Bilingual Attendant (V2) & MCP Toolkit
*   **Source:** `HomeLabAI/src/lab_attendant_v2.py`
*   **Roadmap:** [SPRINT_ATTENDANT_BILINGUAL_v4.9.md](../HomeLabAI/docs/plans/SPRINT_ATTENDANT_BILINGUAL_v4.9.md)
*   **Interface:** Dual-protocol (REST + MCP).
    *   **REST (:9999):** Maintains compatibility with the existing `lab-attendant.service` (systemd).
    *   **MCP (Native Gemini CLI):** Registers as a local tool via `~/.gemini/settings.json`.
*   **Hardening [FEAT-119]:** Formally implements the **Parallel Assassin** logic (Parallel `SIGKILL` + 2s kernel settle) to prevent port 8765 contention.
*   **Engine Readiness Gate:** Hub ignition is gated by a physical `TCP_CONNECT` poll to port 8088/11434 to ensure weights are resident.

### 2. Sovereign Ultra Model (Qwen 27B)
*   **Identity:** `Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled-GGUF`
*   **Host:** **KENDER** (Windows 11 / RTX 4090 / 24GB VRAM)
*   **Quantization:** Q4_K_M (~16.5 GB footprint).
*   **Logical Glue:** Distilled from Claude 3.5 Opus to maintain high instructional adherence and recursive reasoning during complex archive synthesis tasks.
*   **Unified Residency [FEAT-155]:** No active swapping required. This model handles both strategic chat and the nightly "Dream Cycle."

---

## 🧠 THE BICAMERAL TWEAK: EMERGENT THOUGHT

### 1. Pinky as the "Narrative Foil" [FEAT-152]
*   **Role Transition:** Move Pinky from "Technical Interface" to "Grounding Anchor."
*   **The AYPWIP Pattern:** Inspired by "Pinky and the Brain" scripts, Pinky provides literal/hardware-level observations that compliment the Brain's strategic focus.
*   **Mechanism:** Update Pinky's system prompt to identify Brain's focus and provide a practical "Hardware So-What" (e.g., "Brain is calculating the 2019 PCIe regressions, Narf! If we get any more errors, the 2080 Ti might just start typing the resume for us!").

### 2. The "Lab" as a Strategic Actor [FEAT-154]
*   **The Sentinel Actor:** The Hub (`acme_lab.py`) monitors session density and sentiment.
*   **Non-Brittle Hinting:** Instead of word-matching, the Hub identifies "Exit Sentiment" (e.g., three casual turns following a deep synthesis) and injects a `[SITUATION: EXIT_LIKELY]` hint to Pinky to suggest closure naturally.

---

## 🧪 DEBUG & AGENTIC STRATEGY

### 1. Owning the Future (No Retreat)
*   **Primary Instruments:** Use the **Atomic Patcher** and **Attendant V2** for all modifications and lifecycle tasks.
*   **Mandate:** If a modern tool fails, **fix the tool**. Do not revert to legacy shell scripts or manual `curl` commands unless the Lab is physically unbootable.
*   **Verification:** Always check the `[BOOT_HASH : COMMIT_SHORT : PID]` in the logs to verify the active code version.
*   **Log Delta [FEAT-151]:** Use the `TraceMonitor` utility to capture only the changes during a test cycle, preventing "tail fatigue."

### 2. Agentic Conduct (Cognitive Load Reduction)
*   **Orchestration:** Linear Dispatch (one task at a time) for code implementation. I (the Main Agent) conduct the specialists.
*   **Design Protection:** Sub-agents produce code and evidence; they are **NOT** permitted to modify `Portfolio_Dev/*.md` files. Only the Main Agent conducts design/DNA updates.
*   **Non-Blocking Resilience:** Every node call (`pinky`, `brain`, `archive`) must be wrapped in an `asyncio.timeout(120)`. If the Windows host hangs, Pinky must provide characterful failover text.

---

## 🛠️ TASKS

### PHASE 1: Attendant V2 & MCP Integration
- [ ] Complete `lab_attendant_v2.py` logic refactor.
- [ ] Register `acme_attendant` tool in `~/.gemini/settings.json`.
- [ ] Verify **Parallel Assassin** using the **Neural Probe**.

### PHASE 2: The Resonant Chamber (Hub Refactor)
- [ ] Refactor `cognitive_hub.py` to support "Turn Bundling" (bundle Pinky + Brain).
- [ ] Implement `oracle_signal` injection into Pinky's context window.
- [ ] Update `process_query` to await parallel dispatch tasks correctly.

### PHASE 3: Sentient Sentinel & "Literal Grounding"
- [ ] Implement session sentiment monitor in `acme_lab.py`.
- [ ] Update Pinky's system prompt with AYPWIP "Hardware So-What" logic.
- [ ] Test the `[SENTIMENT: EXIT_LIKELY]` hint injection.

### PHASE 4: Verification (The Neural Probe)
- [ ] Create `src/debug/probe_hub.py` to "sniff" the Hub's internal hints.
- [ ] Execute the full end-to-end Bicameral Gauntlet.

---
*Reference: [FEAT-030/SCAR #5] Hemispheric Independence*
