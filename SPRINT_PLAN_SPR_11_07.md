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
- [x] Complete `lab_attendant_v2.py` logic refactor.
- [x] Register `acme_attendant` tool in `~/.gemini/settings.json`.
- [x] Verify **Parallel Assassin** using the **Neural Probe**.
*   **Test Plan:**
    1.  **Tool Registration:** Verify `acme_attendant` is visible to the Gemini CLI.
    2.  **Assassin Verification:** Manually hold port 8765 open with a dummy process; trigger `quiesce` and verify parallel `SIGKILL` in `attendant.log`.
    3.  **Sync Gate:** Verify Hub ignition blocks until port 8088 (vLLM) is physically responsive.

### PHASE 2: The Resonant Chamber (Hub Refactor)
- [x] Refactor `cognitive_hub.py` to support "Turn Bundling" (bundle Pinky + Brain).
- [x] Implement `oracle_signal` injection into Pinky's context window.
- [x] Update `process_query` to await parallel dispatch tasks correctly.
*   **Test Plan:**
    1.  **Bundling Check:** Verify `conversations.log` shows bundled packets for a single user turn.
    2.  **Context Injection:** Use `probe_hub.py` to confirm Pinky's prompt received the `oracle_signal` data before generating.

### PHASE 3: Sentient Sentinel & "Literal Grounding"
- [x] Implement session sentiment monitor in `acme_lab.py`.
- [x] Update Pinky's system prompt with AYPWIP "Hardware So-What" logic.
- [x] Test the `[SENTIMENT: EXIT_LIKELY]` hint injection.
*   **Test Plan:**
    1.  **Sentiment Trigger:** Fire 3 casual queries in 60s; verify `[SITUATION: EXIT_LIKELY]` is injected.
    2.  **Foil Logic:** Review Pinky's response for literal hardware grounding (e.g., thermal/VRAM comments) in response to strategic tasks.

### PHASE 4: Verification (The Neural Probe)
- [x] Create `src/debug/probe_hub.py` to "sniff" the Hub's internal hints.
- [x] Execute the full end-to-end Bicameral Gauntlet.
*   **Test Plan:**
    1.  **Neural Probe:** Verify script can intercept and display Hub-injected hints in real-time.
    2.  **The Gauntlet:** 1 Strategic Query -> Await Bundled Response -> 1 Casual Follow-up -> Verify Exit Hint and Literal Grounding.
    3.  **Core Verification:** Run `src/debug/test_lifecycle_gauntlet.py` to verify connection resilience after the Attendant V2 refactor.
    4.  **Persona Audit:** Run `src/debug/test_persona_bugs.py` to ensure Pinky's new grounding doesn't break character constraints.

### PHASE 5: Post-Evolution Hardening (Addressing Scars)
- [x] **Probe v2.0 (Tool Improvement):** Refactor `probe_hub.py` to be bundle-aware. 
- [x] **SSE Evolution (Tool Improvement):** Implement SSE (Server-Sent Events) in `lab_attendant_v2.py`.
- [x] **Personality Unification (Core Hardening):** Merge persona instructions into system-prompt templates.
- [ ] **Aggregate Verification:** Update `src/debug/verify_sprint.py` to include the Bicameral bundle check.

*   **Test Plan (Phase 5):**
    1.  **Probe v2.0:** Verify `probe_hub.py` shows BOTH Pinky and Brain responses correctly for a single turn.
    2.  **SSE Check:** Verify `acme_attendant` tool can communicate without a TTY.
    3.  **Dispatch Audit:** Run `src/debug/test_dispatch_logic.py` to verify priority routing within bundles.
    4.  **Final Gauntlet:** Run `src/debug/verify_sprint.py` for final sign-off.

### PHASE 6: High-Fidelity Sovereignty & Shadow Refactor
- [ ] **Decouple SML Fallback from KENDER [FEAT-081]:** Ensure KENDER (Windows) connectivity failures do not force a local model downshift for Pinky.
- [ ] **Grounded Shadow Protocol:** Refactor the "Shadow Brain" failover mode from a "Pinky Hallucination" into a "Stoic Shadow" (technical derivation via local engine, characterful but clinical).
- [ ] **Adapter Integrity Sweep:** Audit physical `/speedy/models/adapters/` existence. Formally deprecate and remove `lora_name` from `infrastructure.json` to resolve "First-Class Integrity Failure" log noise.

*   **Context/Rationale:**
    - **Why:** The recent implementation showed Pinky falling back to 1B Ollama because he didn't "recognize" the 3B vLLM model ID (Fidelity Trap).
    - **Impact:** Critical fidelity loss occurs when "Theatre engines" displace "Reasoning engines" during cold-start handshake penalties (22s characterizing).
    - **Goal:** Transform Pinky from "Absurd Foil" to "Physicality Auditor" and Brain from "Genius Mouse" to "Sovereign Architect."

*   **Test Plan (Phase 6):**
    1.  **SML Decoupling:** Simulate KENDER outage; verify Pinky stays on vLLM (LARGE) instead of downshifting.
    2.  **Shadow Verification:** Trigger failover; verify response is "Stoic Shadow" persona, not "Jupiter Vacation."
    3.  **Integrity Audit:** Verify zero "Missing Adapter" warnings in `server.log`.

### PHASE 7: Silicon Refinement (The Pedigree Burn)
- [ ] **Data Distillation [FEAT-161]:** Use the Brain (4090) to transform raw technical logs and high-level documents into instruction-response pairs.
    - *Source Documents:* `stories.html`, `Philosophy and Learnings 2024.docx`, `DTTC_2022_Peci_Stress.pdf`, `Resume`, `AR - InAWorld.docx`.
- [ ] **Trainer Scaffold:** Create `HomeLabAI/src/train/refine_persona.py` using the **Unsloth** framework.
- [ ] **The Pedigree Burn [FEAT-160]:** Execute a 4-bit LoRA fine-tuning cycle on the 2080 Ti to encode the 18-year pedigree into the model's weights.
- [ ] **Multi-LoRA Integration [FEAT-162]:** Configure vLLM to dynamically load the resulting `pedigree_v2` adapter for Pinky.

*   **Context/Rationale:**
    - **Why:** To put LoRA back as a defining feature, we move from "Theatre" to "Hardened Weights." By encoding your **Engineering Pedigree** directly into the neurons, the model gains **Intuitive Anchors** for reverse-timeline recall (e.g. "When did I work on VISA?").
    - **How:** Brain acts as the **Teacher** (distilling noisy logs into high-signal training data); Pinky acts as the **Resident Student** (receiving the LoRA patch).
    - **The Hybrid Vibe:** The final state uses **LoRA for mathematical nuance** (tone/structure) and **Prompts for strategic intent** (AYPWIP/Exit Sentiment).

*   **Test Plan (Phase 7):**
    1.  **Recall Test:** Ask a reverse-timeline question (e.g., "VISA start date?"); verify the model uses intuitive recall rather than linear searching.
    2.  **Weight Verification:** Verify `vllm_server.log` shows the successful loading of the `pedigree_v2` adapter.
    3.  **Bicameral Synergy:** Verify that the "Stoic Shadow" and "AYPWIP Pinky" personas are enhanced by the new weights.

---
*Reference: [FEAT-030/SCAR #5] Hemispheric Independence*
