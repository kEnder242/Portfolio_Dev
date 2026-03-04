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
*   **Test Plan:**
    1.  **Tool Registration:** Verify `acme_attendant` is visible to the Gemini CLI.
    2.  **Assassin Verification:** Manually hold port 8765 open with a dummy process; trigger `quiesce` and verify parallel `SIGKILL` in `attendant.log`.
    3.  **Sync Gate:** Verify Hub ignition blocks until port 8088 (vLLM) is physically responsive.

### PHASE 2: The Resonant Chamber (Hub Refactor)
- [ ] Refactor `cognitive_hub.py` to support "Turn Bundling" (bundle Pinky + Brain).
- [ ] Implement `oracle_signal` injection into Pinky's context window.
- [ ] Update `process_query` to await parallel dispatch tasks correctly.
*   **Test Plan:**
    1.  **Bundling Check:** Verify `conversations.log` shows bundled packets for a single user turn.
    2.  **Context Injection:** Use `probe_hub.py` to confirm Pinky's prompt received the `oracle_signal` data before generating.

### PHASE 3: Sentient Sentinel & "Literal Grounding"
- [ ] Implement session sentiment monitor in `acme_lab.py`.
- [ ] Update Pinky's system prompt with AYPWIP "Hardware So-What" logic.
- [ ] Test the `[SENTIMENT: EXIT_LIKELY]` hint injection.
*   **Test Plan:**
    1.  **Sentiment Trigger:** Fire 3 casual queries in 60s; verify `[SITUATION: EXIT_LIKELY]` is injected.
    2.  **Foil Logic:** Review Pinky's response for literal hardware grounding (e.g., thermal/VRAM comments) in response to strategic tasks.

### PHASE 4: Verification (The Neural Probe)
- [x] Create `src/debug/probe_hub.py` to "sniff" the Hub's internal hints.
- [ ] Execute the full end-to-end Bicameral Gauntlet.
*   **Test Plan:**
    1.  **Neural Probe:** Verify script can intercept and display Hub-injected hints in real-time.
    2.  **The Gauntlet:** 1 Strategic Query -> Await Bundled Response -> 1 Casual Follow-up -> Verify Exit Hint and Literal Grounding.
    3.  **Core Verification:** Run `src/debug/test_lifecycle_gauntlet.py` to verify connection resilience after the Attendant V2 refactor.
    4.  **Persona Audit:** Run `src/debug/test_persona_bugs.py` to ensure Pinky's new grounding doesn't break character constraints.

### PHASE 5: Post-Evolution Hardening (Addressing Scars)
- [ ] **Probe v2.0 (Tool Improvement):** Refactor `probe_hub.py` to be bundle-aware. 
- [ ] **SSE Evolution (Tool Improvement):** Implement SSE (Server-Sent Events) in `lab_attendant_v2.py`.
- [ ] **Personality Unification (Core Hardening):** Merge persona instructions into system-prompt templates.
- [ ] **Aggregate Verification:** Update `src/debug/verify_sprint.py` to include the Bicameral bundle check.

*   **Test Plan (Phase 5):**
    1.  **Probe v2.0:** Verify `probe_hub.py` shows BOTH Pinky and Brain responses correctly for a single turn.
    2.  **SSE Check:** Verify `acme_attendant` tool can communicate without a TTY.
    3.  **Dispatch Audit:** Run `src/debug/test_dispatch_logic.py` to verify priority routing within bundles.
    4.  **Final Gauntlet:** Run `src/debug/verify_sprint.py` for final sign-off.

---
*Reference: [FEAT-030/SCAR #5] Hemispheric Independence*
