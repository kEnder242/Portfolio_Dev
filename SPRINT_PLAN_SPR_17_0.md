# Sprint Plan: [SPR-17.0] The Resonant Restoration
**Status:** ACTIVE | **Goal:** Restore the "Neural Relay" while enforcing **Semantic Fluidity [BKM-015.1]** and protocol-standard streaming.

---

## 🏛️ ARCHITECTURAL INTRODUCTION: THE ALIGNED RELAY

This sprint marks a critical turning point in the Lab's evolution. We are moving away from "Inception-style" nested tool calls (`facilitate`) toward a **Native MCP Sampling** architecture. This transition, while strategically sound, caused a temporary "Logic Gap" where the Lab lost its physical identity and real-time responsiveness.

The goal of **SPR-17.0** is to "Meld" the best of both worlds:
1.  **Protocol Hygiene**: Maintaining the Standard MCP Sampling bridge for its industry-standard compatibility and logic isolation.
2.  **Bicameral Vibe**: Restoring the "Thinking" waterfall where Pinky (Persona), Shadow (Intuition), and Brain (Synthesis) collaborate with sub-second perceived latency.
3.  **Semantic Fluidity**: Replacing the last vestiges of hard-coded keyword routing with a scalar "Vibe" engine that natively understands complexity, history, and collective address (the "Mice").

We are not just fixing bugs; we are hardening the **Tendons** of the Lab.

---

## 🛠️ PHASES OF IMPLEMENTATION

### 📍 PHASE 1: Silicon Restoration (The Foundation) [RANK 1]
**Goal:** Restore the Lab's physical identity and KENDER (4090) connectivity.

*   **Task 1.1: Fix `loader.py` Path Hardening [FEAT-240.1]**
    *   *How*: Update the `LAB_DIR` calculation in `src/nodes/loader.py` to correctly resolve the `infrastructure.json` path (3-level `dirname`).
    *   *Why*: Currently, nodes are defaulting to `localhost` and skipping their LoRA adapters, effectively "blinding" the Lab to its 18-year DNA.
*   **Task 1.2: Implement Hub-Side Morning Briefing [FEAT-072.1]**
    *   *How*: Add the missing `trigger_morning_briefing` logic to `CognitiveHub.execute_dispatch`. 
    *   *Why*: Nodes can request a debrief, but the Hub currently ignores the signal, orphaning the "Dreaming" history.

### 📍 PHASE 2: The Waterfall Restoration (Streaming) [RANK 1]
**Goal:** Restore sub-second responsiveness without violating the "Paragraph Pop" UI mandate.

*   **Task 2.1: Async Generator Bridge [FEAT-233.3]**
    *   *How*: Refactor `BicameralNode.native_sample` in `loader.py` to be an `async for` generator.
    *   *Why*: The current tool buffers the entire response, turning the "Waterfall" back into a "Blocking Block."
*   **Task 2.2: Hub-Side Token Buffer [FEAT-233.4]**
    *   *How*: Update `CognitiveHub` to consume the new generator stream, identifying `[ACTION]` tags and `final=true` signals *mid-stream* to spark subsequent nodes.
    *   *Why*: Allows the Brain to start pre-warming the moment Pinky's intent is clear, while still holding the UI display for a "Clinical Pop."

### 📍 PHASE 3: Semantic Steerage & Persona Pivot [RANK 2]
**Goal:** Transition to "Overhearing" and rebalance the Mice for high-fidelity interface.

*   **Task 3.1: Shadow Overhear Pivot [FEAT-229.2]**
    *   *How*: Lower the Shadow promotion threshold in `CognitiveHub.py` to **0.2**.
    *   *Why*: Shadow (Local 2080 Ti) should always provide technical intuition unless Pinky explicitly handles the query (Casual).
*   **Task 3.2: Collective Triage [FEAT-241]**
    *   *How*: Update `lab_node.py` system prompt to recognize "Collective" vibes (Mice/Echo Chamber) and assign high intrigue.
    *   *Why*: Restores the ability to address the Lab as a group without the system defaulting to casual silence.
*   **Task 3.3: Interface Persona & Natural Veto [VIBE-015]**
    *   *How*: Refactor Pinky's prompt to be an **Interface Layer** (Enthusiastic Assistant) rather than a "Talking Dashboard." Demote hardware metrics to **Passive Awareness**.
    *   *Why*: Prevents "VRAM Hyper-focus" and makes her interjections feel natural. Hub detects a Veto when `fuel < 0.2` and `intent == "CASUAL"`.

### 📍 PHASE 4: The Sentinel Forge (DNA Induction)
**Goal:** Physically encode "Vibe Awareness" and data distinction into the Lab Node.

*   **Task 4.1: Reverse Vibe Generator [FORGE-05]**
    *   *How*: Create `src/forge/generate_sentinel_curriculum.py` utilizing the Sovereign Brain (4090) to generate synthetic query-to-scalar pairs.
    *   *Why*: To provide a high-density training dataset that aligns the Sentinel's intuition with the new scalar schema.
*   **Task 4.2: Data Distinction (Lab vs. Archive)**
    *   *How*: Ensure training data distinguishes between **Current Lab State** (Pinky/Shadow) and **Historical Archive Data** (Brain). 
    *   *Why*: Prevents "Memory Bleed" where the Mice act as if they have personally experienced 18 years of history.

### 📍 PHASE 5: Judicial Restoration (Rank 2)
**Goal:** Eliminate "Marking own homework" bias and implement the Physical Audit Gate.

*   **Task 5.1: Blind Audit Implementation [BKM-028]**
    *   **How**: Refactor `dream_cycle.py` to use **Pinky** (Local) to audit the **Brain's** (Remote) synthesis.
    *   **Why*: Prevents high-fidelity hallucinations from being permanently anchored in the archive.
*   **Task 5.2: The "333MiB" Breakthrough Verification**
    *   **How**: Execute the silicon gauntlet (`src/debug/verify_breakthrough.py`) to confirm VRAM headroom.
    *   **Why**: Mandatory silicon gate per `ENGINEERING_PEDIGREE.md`.
*   **Task 5.3: The Physical Audit Gate (Cooldown Refinement)**
    *   **How**: Refactor `evaluate_grounding` in `CognitiveHub.py` to request a **Physical Audit/Reality Check** from Pinky (Hardware feasibility) rather than a generic "TLDR."
    *   **Why**: Makes Pinky the "Grounding Wire" for the Brain's abstract technical logic.

---

## 🌅 PHASE 6: THE DREAMING DEBRIEF (Presentation)
**Goal:** Close the loop on Phase 9's synthesis by presenting "Diamond Wisdom" to the user.

*   **Task 6.1: UI Presentation Component**
    *   **How**: Implement the "Morning Briefing" presentation logic in `CognitiveHub` that pulls the latest `dream` entry from the Archive.
    *   **Why**: Diamond Wisdom is currently synthesized but remains "unseen."

---

## 🧬 NEW FEATURES & BKMS

| ID | Name | Role |
| :--- | :--- | :--- |
| **[FEAT-241]** | **Collective Triage** | **PLANNED**: Explicit scalar weights for group-based address ("Mice/Everyone"). |
| **[FEAT-242]** | **Async Tool Streaming** | **PLANNED**: Ability to trigger relay promotions mid-sentence via stream-parsing. |
| **[BKM-028]** | **The Blind Audit Rule** | **LAW**: Dreaming audits MUST be performed by a node with different weights/personality to prevent echo-chamber bias. |

---

## 🧪 VALIDATION PLAN
*   **Phase 1**: Run `src/debug/test_attendant_sanity.py` to verify path restoration.
*   **Phase 2**: Use `src/debug/test_waterfall_spark.py` to verify sub-second node sparking.
*   **Phase 3**: Execute the "Hi Mice" gauntlet to verify collective triage and scalar fuel routing.
*   **Phase 4**: Audit `server.log` for `[SENTINEL_SCALAR]` entries.

---

## 🎼 CONDUCTOR TRACK: Restoration Relay
**Conductor Context:** "Execute the SPR-17.0 restoration plan. Use `generalist` for Phase 1/2 refactors and `architect` for Phase 3/4 curriculum design. Mandate `ruff check` on every edit. Refer to the Post-Mortem and BKM-015.1 for grounding."

---

## 🤕 FORENSIC RATIONALE: PERSONA REBALANCING [REVISION-17.1]
*Report on the "Mice" persona pivot and grounding refinements.*

1.  **From Dashboard to Assistant**: We identified that Pinky was becoming a "Talking VRAM Dashboard," leading to hyper-focused and repetitive interjections. We have pivoted her role to be the **Interface Layer** of the Lab. She maintains **Passive Awareness** of hardware but only speaks to it when the physical state impacts the logical flow.
2.  **The Physical Auditor**: The "TLDR" phase (Grounding Gate) was identified as a low-fidelity summary trap. We have refactored this into a **Reality Check**. Pinky now audits the Brain's abstract synthesis against the physical constraints of the Lab (VRAM/Thermals/Complexity).
3.  **The Identity Shield**: To prevent the Mice from "hallucinating" 18 years of personal experience, we have enforced a **Data Distinction**. The Brain remains the sole "Historical Sovereign," while Pinky and Shadow treat the archive as external "Sacred Logs" to be queried, not personal memories.
4.  **Shadow Handshake**: We have formalized the "Tapping into intuition" flow, where Pinky leads the turn and acknowledges the multi-node consensus building, turning latency into a technical feature.
