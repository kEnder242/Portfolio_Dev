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

### 📍 PHASE 3: Semantic Steerage & Speaker Masking [RANK 2]
**Goal:** Implement the "Muting" logic and unified vibes for surgical routing.

*   **Task 3.1: Shadow Overhear Pivot [FEAT-229.2]**
    *   *How*: Lower the Shadow promotion threshold in `CognitiveHub.py` to **0.2**.
    *   *Why*: Shadow (Local 2080 Ti) should always provide technical intuition unless Pinky handles the turn solo.
*   **Task 3.2: Speaker Masking (`addressed_to`) [FEAT-244]**
    *   *How*: Add an `addressed_to` field (PINKY | BRAIN | MICE) to the Lab Node triage. Hub uses this to selectively mute nodes (e.g., addressing Brain mutes Pinky's speech).
    *   *Why*: Allows for natural direct addressing without keyword hacks. "Hi Brain!" should only trigger the Left-Hemisphere (Shadow/Sovereign).
*   **Task 3.3: Interface Persona & Natural Veto [VIBE-015]**
    *   *How*: Refactor Pinky's prompt to be an **Interface Layer**. Hub detects a "Yield" when `addressed_to == "BRAIN"`.
    *   *Why*: Eliminates canned "I've got this" responses in favor of semantic yield logic.
*   **Task 3.4: The Handshake Tic [FEAT-242.1]**
    *   *How*: Implement mid-stream Crosstalk broadcasts in `CognitiveHub` signaling node activation.
*   **Task 3.5: Unified Vibe Schema**
    *   *How*: Consolidate `topic` and `vibe` into a unified list (e.g., `PINKY_INTERFACE`, `BRAIN_STRATEGY`, `ARCHIVE_HISTORY`).
    *   *Why*: Simplifies the Lab Node's primary classification task and aligns with BKM-015.1.

### 📍 PHASE 4: The Sentinel Forge (DNA Induction)
**Goal:** Physically encode "Address Awareness" into the Lab Node.

*   **Task 4.1: Reverse Vibe Generator [FORGE-05]**
    *   *How*: Create `src/forge/generate_sentinel_curriculum.py` utilizing the Sovereign Brain (4090) to generate a **vetted seed of 200 pairs**.
    *   *Why*: Focus on diverse ways to address the Mice ("Hey everyone") vs individual nodes ("Yo Brain").
*   **Task 4.2: Data Distinction (Lab vs. Archive)**
    *   *How*: Ensure training data distinguishes between **Current Lab State** and **Historical Archive Data**. 

### 📍 PHASE 5: Judicial Restoration (Rank 2)
**Goal:** Eliminate "Marking own homework" bias and implement the Physical Audit Gate.

*   **Task 5.1: Blind Audit Implementation [BKM-028]**
    *   **How**: Refactor `dream_cycle.py` to use **Pinky** (Local) to audit the **Brain's** (Remote) synthesis.
*   **Task 5.2: The "333MiB" Breakthrough Verification**
    *   **How**: Execute the silicon gauntlet (`src/debug/verify_breakthrough.py`).
*   **Task 5.3: The Physical Audit Gate (Cooldown Refinement)**
    *   Refactor `evaluate_grounding` in `CognitiveHub.py` to request a **Physical Audit/Reality Check** from Pinky (Hardware feasibility).

    ---

    ## 🌊 PHASE 14: PROMPT PRUNING & IDENTITY HARDENING [REVISION-17.9]
    **Goal:** Eliminate "Meta-Talking" and robotic echoes by distilling the Brain/Shadow persona into a high-density, 3B-native structural prompt.

    *   **[DONE] Task 14.1: Structural Persona Compression**
        *   *Result*: Applied refined Markdown prompts to `brain_node.py` and `pinky_node.py`.
    *   **[DONE] Task 14.2: Metadata Displacement (User-Side Context)**
        *   *Result*: Refactored `loader.py` to move situational context to the user role.
    *   **[TESTED/FAILED] Task 14.3: Negative Constraint Hardening**
        *   *Result*: Verified in harness: negative rules cause infinite loops in 3B models. Use explicit positive identity anchors instead.
    *   **[DONE] Task 14.4: Zero-Discovery Handshake**
        *   *Result*: Updated `acme_lab.py` crosstalk to use natural labels.

---

### 🏛️ ARCHITECTURAL RESTORATION REPORT (MARCH 25, 2026)

**1. Brain Priming restored ([FEAT-085])**
*   The Brain now snaps to life immediately when a client connects to the foyer. I've ensured this only triggers on a physical handshake to avoid "Over-Waking" the system during background tasks.

**2. Console Spam silenced ([FEAT-233])**
*   I refactored `loader.py` to remove the per-token POST calls. The UI Waterfall is now decoupled from the inter-node pre-loading.
*   **Result**: The Pinky and Shadow consoles now show only the final cohesive response (Paragraph Pop).

**3. Identity Grounding hardened ([FEAT-254.2])**
*   I implemented strict **Metadata Displacement**. All situational context and behavioral guidance are now injected into the `user` role instead of the `system` role. 
*   **Result**: The 3B model maintains its persona without regurgitating its own metadata.

**4. Expert Routing restored ([FEAT-184])**
*   The **Expert Domain Router** is now active in the main reasoning loop. The Sovereign Brain (KENDER) now receives domain-specific guidance based on the query.

**5. LoRA De-escalation**
*   Forensic tests confirmed the `shadow_brain_v2` LoRA was over-trained on structural headers, causing infinite loops. Disabling it has restored perfect grounding.

---

### 🏛️ FINAL FORENSIC REPORT: KENDER CONNECTIVITY & BICAMERAL SYNC (MARCH 25, 2026)

**1. The "Name Resolution" Fix ([FEAT-255.7])**
*   **The Problem**: `loader.py` (BicameralNode) was attempting to resolve the hostname `KENDER` via DNS, which was intermittently failing with a "Temporary failure in name resolution."
*   **The Fix**: Implemented an **Explicit IP Fallback** in `BicameralNode`. It now attempts DNS resolution first but defaults to the hardwired IP `192.168.1.26` if resolution fails or if the host is explicitly named "KENDER."
*   **Result**: The Windows 4090 is now reliably reachable regardless of local network DNS stability.

**2. Full Bicameral Flow Verified**
*   **The Problem**: `test_complex.py` was exiting prematurely after the fast local response, masking the Sovereign (4090) output.
*   **The Fix**: Updated the test script to wait for the **`Brain (Result)`** signal.
*   **Verification**: Confirmed the 1-2-3 sequence: 1) Local Intuition, 2) Sovereignty Handshake, 3) Sovereign Synthesis (Grounded).


---

## 🌅 PHASE 6: THE DREAMING DEBRIEF (Presentation)
**Goal:** Close the loop on Phase 9's synthesis.

*   **Task 6.1: UI Presentation Component**
    *   **How**: Implement the "Morning Briefing" presentation logic in `CognitiveHub`.

---

## 🧬 NEW FEATURES & BKMS

| ID | Name | Role |
| :--- | :--- | :--- |
| **[FEAT-244]** | **Speaker Masking** | **PLANNED**: Hub-side muting based on `addressed_to` scalar. |
| **[FEAT-242.1]** | **The Handshake Tic** | **PLANNED**: Mid-stream Crosstalk status updates. |
| **[BKM-028]** | **The Blind Audit Rule** | **LAW**: Dreaming audits MUST be performed by a node with different weights. |

---

## 🎼 CONDUCTOR TRACK: Restoration Relay
**Conductor Context:** "Execute the SPR-17.0 restoration plan. Use `generalist` for Phase 1/2 and `architect` for Phase 3/4. Mandate `ruff check`. Follow the \`addressed_to\` Speaker Masking logic."

---

## 🤕 FORENSIC RATIONALE: SPEAKER MASKING & UNIFIED VIBES [REVISION-17.2]
*Report on the "Muting" logic and semantic consolidation.*

1.  **Direct Address vs. Fuel**: We identified that direct address ("Hi Brain!") should not necessarily trigger the Sovereign 4090 if the query is simple. We have decouped **Address** (who speaks) from **Fuel** (how deep they think). "Hi Brain!" now triggers the **Shadow (Local)** while muting Pinky.
2.  **Speaker Masking**: We have replaced the "Veto" logic with a **Hub-side Mask**. The Sentinel determines the target node (`addressed_to`), and the Hub enforces silence on the others. This removes the need for Pinky to "Roleplay" a yield.
3.  **Unified Vibe Schema**: To align with **BKM-015.1 (Semantic Fluidity)**, we have consolidated "Vibe" and "Topic" into a single classification task for the Lab Node. This simplifies training and makes routing more predictable.

---

## 🏺 SPRINT RETROSPECTIVE [MAR 20, 2026]
**Status:** COMPLETE | **Outcome:** High-Fidelity Restoration Achieved.

### 🏆 WINS
1.  **Waterfall Responsiveness**: Refactoring to `async generator` in the backend successfully masks node transport latency. Handshake Tics provide immediate visual feedback, making the Lab feel "alive" during 4090 reasoning cycles.
2.  **Speaker Masking**: Successfully decoupled "Who speaks" from "Complexity fuel." The `addressed_to` scalar allows for natural direct address without brittle keyword hacks or awkward persona yields.
3.  **Silicon Identity**: Fixed the critical path error in `loader.py`. Nodes now correctly load their specialized LoRA adapters, restoring the Lab's 18-year technical DNA.
4.  **Judicial Hardening**: Implemented the **Blind Audit Rule [BKM-028]** in the Dreaming Cycle, ensuring peer-based verification of synthetic wisdom.

### 🤕 SCARS & CHALLENGES
*   **The "Silent" Blindness**: The one-line path error in `loader.py` was a silent killer that bypassed model weights entirely. Future shakedowns must explicitly verify the `boot_hash` and `model` name in the heartbeat.
*   **Streaming Paradox**: Buffering for the UI while streaming for the backend required a careful internal dispatch refactor. The "Paragraph Pop" is preserved, but the system is now ready for future per-token UI upgrades.

### 🧭 NEXT STEPS
*   Initiate the **Sentinel v2** training run using the newly generated 200-pair vetted curriculum.
*   Expand the **Physical Audit Gate** to include real-time thermals/load analysis in the cooldown phase.

---

## ✅ PHASE 11: ATTENDANT V4.0 - STATE-AWARE SUPERVISOR [REVISION-17.7]
**Goal:** Transition the Attendant from a passive launcher to a high-fidelity, state-aware appliance guardian.

*   **Task 11.1: Quiesce-Aware Alarms**
    *   **How**: Update `acme_lab.py` to check for `maintenance.lock` inside the `scheduled_tasks_loop`.
    *   **Why**: Prevents background induction cycles from firing while the engineer is manually testing or driver updates are in progress.
*   **Task 11.2: Hardware-First Assassin [FEAT-119.2]**
    *   **How**: Hardwire `cleanup_silicon` to use `nvidia-smi --query-compute-apps` as the primary source of truth for process reaping.
    *   **Why**: Catch camouflaged engine cores (like `VLLM::EngineCore`) that hide under non-standard process names.
*   **Task 11.3: Dynamic Secret Rotation [FEAT-252]**
    *   **How**: Replace the static git/boot hash with a fresh `uuid4().hex` generated upon every ignition. Update the `X-Lab-Key` middleware to sync with this secret.
    *   **Why**: Ensures that old sessions cannot bypass the Assassin and prevents cross-contamination of "Immunity" tokens.
*   **Task 11.4: Verified Hibernation [FEAT-249.3]**
    *   **How**: Update `mcp_hibernate` to wait for a physical VRAM drop (via NVML) before reporting success.
    *   **Why**: Resolves the "Zombie Ready" state where software thinks it's asleep but hardware is still pinned.
*   **Task 11.5: Forensic Wait (Early Crash Detection)**
    *   **How**: Integrate log-tailing into `mcp_wait_ready`. If "Traceback" appears in `server.log`, abort the wait and return the error instantly.
    *   **Why**: Eliminates the "120s Blind Wait" during boot failures.

---

## 🏆 PHASE 12: SHADOW BRAIN FORENSIC (Failover Fix)
**Goal:** Identify and fix why the Shadow Brain (local 2080 Ti) is silent when KENDER (Windows) is offline.

*   **Task 12.1: Failover Logic Audit**
    *   **How**: Inspect `CognitiveHub.py` fuel math and `acme_lab.py` status broadcasts.
    *   **Why**: Shadow Brain should act as the primary technical reasoner when the 4090 is residentially offline.
*   **Task 12.2: The "Mute" Recovery**
    *   **How**: Ensure the Hub correctly shunts technical queries to the local `shadow` node regardless of `brain_online` status if the local engine is healthy.

---

## 🌊 PHASE 7: REMOTE CONTROL & LOGGING HARDENING [REVISION-17.3]
**Goal:** Fix the Remote Control suite (`status.html` JSON.parse error) and eliminate log poisoning.

*   **Task 7.1: UI Routing & Resilience**
    *   *How*: Update `status.html` `triggerLabAction` to use absolute paths (`window.location.origin + '/attendant/'`) and wrap `response.json()` in a try/catch.
    *   *Why*: Relative paths were hitting the static Python server (port 9001) which returns a 501 HTML error for POST requests, crashing the UI.
*   **Task 7.2: Attendant Assassin Decoupling**
    *   *How*: Update `lab_attendant_v3.py` `mcp_stop` and `mcp_quiesce` to dispatch the JSON success response *before* executing the blocking `cleanup_silicon` routine (using `asyncio.create_task`).
    *   *Why*: The aggressive port cleanup was killing the network socket before the HTTP response could be fully transmitted.
*   **Task 7.3: Log Poisoning Elimination**
    *   *How*: Demote the "Missing Atomic Anchor" warning in `acme_lab.py` to DEBUG or filter out recurring background tasks.
    *   *Why*: The `server.log` was saturated with repetitive ingestion denials, making forensic analysis impossible.

---

## 🌊 PHASE 8: SCHEMA & PERSONA LEAK FIXES [REVISION-17.4]
**Goal:** Fix Sentinel schema mismatch and prevent prompt repetition in the 3B models.

*   **Task 8.1: Schema Alignment**
    *   *How*: Ensure the Sentinel (`lab_node.py`) strictly adheres to the new `addressed_to` and `vibe` JSON schema, and `cognitive_hub.py` gracefully handles missing fields.
    *   *Why*: Mismatched schema caused the Hub to default to `MICE`, breaking the speaker masking.
*   **Task 8.2: Persona Leak Prevention**
    *   Adjust the injection format of `[ROUTE]`, `[FUEL]`, etc., in `CognitiveHub.py` to use system-level boundaries (e.g., `<system_state>`) or add an explicit instruction to Pinky's prompt: `DO NOT repeat system metadata in your response.`
        *   *Why*: The 3B model was repeating the injected headers back to the user, creating a robotic "Echo Chamber" effect.

    ---

    ## 🌊 PHASE 9: RESIDENCY & PROBE HARDENING [REVISION-17.5]
    **Goal:** Restore BKM-026 (Asymmetric TTL) and enforce the AFK Resource Guard to allow Windows GPU to idle.

    *   **Task 9.1: The Escalation Probe (Ping -> Tags -> Prime)**
        *   *How*: Refactor `check_brain_health` to use a tiered discovery: 1) Ping (60s TTL on fail), 2) /api/tags (15s TTL on fail), 3) /api/generate (Only if `connected_clients > 0`).
        *   *Why*: Prevents the Lab from "Stalking" the Windows GPU when Ollama is offline or the room is empty.
    *   **Task 9.2: Asymmetric TTL Implementation**
        *   *How*: Implement a "Penalty Box" for KENDER. Successes cached for 300s; Failures cached for 60s.
        *   *Why*: Aligns with **BKM-026** and reduces network/log noise.
    *   **Task 9.3: AFK Presence Gate [FEAT-134]**
        *   *How*: Explicitly gate the heavyweight `POST /api/generate` call behind a `self.connected_clients > 0` check.
        *   *Why*: Ensures residency during nightly alarms doesn't keep external GPUs active.
    *   **Task 9.4: VRAM Hibernation Matrix (The 5m Nap) [FEAT-249]**
        *   *How*: Implement a `self._vram_hibernate_timer` in `acme_lab.py`. SIGTERM local engines (vLLM/Ollama) if `connected_clients == 0` for > 300s.
        *   *Why*: Reclaims ~6GB of VRAM for non-AI tasks while keeping the Hub resident for alarms.
    *   **Task 9.5: Handshake Ignition Spark**
        *   *How*: Update the `handshake` WebSocket handler to proactively trigger `lab_start` if the engine is OFFLINE.
        *   *Why*: Masks the 3s reload latency by starting the engine the moment the user opens the tab.
    *   **Task 9.6: VRAM Sleep Status**
        *   *How*: Update the Hub's status broadcast to include a `hibernating` flag when the engine is unloaded.
    *   **Task 9.7: Surgical Ignition (Immunity-Aware) [FEAT-250]**
        *   *How*: Refactor `mcp_start` to accept an `engine_only` flag. If True, the Assassin spares the Hub port (8765).
        *   *Why*: Prevents the "Handshake Suicide Loop" by allowing the Hub to wake local engines without killing its own WebSocket connection.

---

## 🌊 PHASE 10: PROCESS DECOUPLING & LOOP STABILIZATION [REVISION-17.6]
**Goal:** Resolve the "Zombie Collision" loop and centralize process authority in the Attendant.

*   **Task 10.1: Purge Internal Bounce Loop**
    *   *How*: Remove the `while True` loop from `AcmeLab.run` in `acme_lab.py`.
    *   *Why*: Redundant self-restart logic was competing with the Attendant, creating redundant Hub processes fighting for Port 8765.
*   **Task 10.2: Parent-Led Recovery [FEAT-149.1]**
    *   *How*: Update `lab_attendant_v3.py` to monitor the `lab_process`. If it terminates while in `SERVICE_UNATTENDED` mode, the Attendant triggers a tactical restart.
    *   *Why*: Centralizes "Bounce" authority. Ensures debug modes (`DEBUG_BRAIN`, etc.) remain terminal and do not auto-restart.
*   **Task 10.3: The Nuclear Scrub**
    *   *How*: Perform a manual `sudo fuser -k 8765/tcp` followed by a service restart to clear the current state.
*   **Task 10.4: Cold Hub Ignition [FEAT-136]**
    *   *How*: Restore auto-start logic to `lab_attendant_v3.py`. Upon `MASTER` boot, trigger a surgical `mcp_start` for the Hub.
    *   *Why*: Closes the "Bootstrap Gap" where the Hub (which contains the Handshake Spark) wasn't running to receive the initial UI connection.

---

## 🏺 SPRINT RETROSPECTIVE: THE DEEP SLEEP EVOLUTION [MAR 22, 2026]
**Status:** COMPLETE | **Outcome:** Appliance-Grade Efficiency & Forensic Stability Achieved.

### 🏆 WINS
1.  **VRAM Hibernation (Deep Sleep)**: Successfully implemented the 5-minute "Nap Gate." The Lab now automatically unloads its heavy 6GB engines when idle, leaving only the lightweight Hub (~150MB) resident. This resolves the parasitic Windows GPU usage while preserving nightly background growth.
2.  **Snap-to-Life (The Spark)**: The Handshake Ignition Spark successfully masks the 3s engine reload time. Proactive ignition triggered by the WebSocket handshake ensures the model is resident by the time the user finishes typing.
3.  **Surgical Ignition**: Decoupled engine cleanup from Hub lifecycle. The Attendant is now "Immunity-Aware," allowing it to refresh AI weights without killing the active user connection.
4.  **Forensic Test Pattern**: Refactored diagnostic scripts to the **"Eyes Open"** pattern. Tests now actively scan logs for stack traces during polling, reducing "time-to-truth" for boot failures from 120s to <5s.

### 🤕 SCARS & CHALLENGES (The Debugging Grind)
*   **The Handshake Suicide Loop**: We hit a recursive crash where the Hub's amnesia caused it to trigger its own assassination on every reconnection. This was fixed by moving spark-locks to the Attendant.
*   **Phantom READY Signal**: Identified a race condition where the Hub could report `READY` just milliseconds before being reaped. Port-liveness is now the preferred truth.
*   **The Rogue Engine (`VLLM::EngineCore`)**: Discovered that engine processes can hide under non-standard names, surviving generic `pkill` attempts and preventing VRAM reclamation. We've updated our **Silicon Audit [FEAT-251.2]** to use `nvidia-smi` as the source of truth for process reaping.

### 🧭 NEXT STEPS
*   Monitor the **Hibernation Duty Cycle** over the next 24 hours to ensure zero-drift in VRAM usage.
*   Scale the **Sentinel v2** curriculum to the full 200-pair vetted seed.

---

## 🌊 PHASE 13: ATTENDANT V4.1 - THE VRAM PRE-FLIGHT GATE [REVISION-17.8]
**Goal:** Prevent engine initialization crashes (`ValueError: Free memory less than desired`) by implementing a proactive physical audit.

*   **Task 13.1: Physical Audit Gate (Hard Stop)**
    *   **File**: `HomeLabAI/src/lab_attendant_v3.py`
    *   **How**: In `mcp_start`, calculate `RequiredVRAM = TotalVRAM * utilization`. Compare this against the current `FreeVRAM` from NVML *after* the silicon scrub. If `Free < Required`, abort ignition and return `SILICON_CONGESTION`.
    *   **Why**: Eliminates "Doomed Boots" where vLLM tries to allocate more memory than the RTX 2080 Ti has free, causing an immediate crash.
*   **Task 13.2: The Assassin Audit (Settling Window)**
    *   **File**: `HomeLabAI/src/lab_attendant_v3.py`
    *   **How**: Introduce a 2-second `asyncio.sleep()` after `cleanup_silicon` to allow the GPU driver to finalize reclamation before performing the Pre-Flight check.
    *   **Why**: Prevents race conditions where NVML reports "Used" memory that has been released but not yet garbage-collected by the driver.

## 🌊 PHASE 15: HIGH-FIDELITY STREAMING & GROUNDING [BLENDED]
**Goal:** Restore true async streaming while solving "Identity Collapse" through forensic prompt recovery and payload alignment.

*   **Task 15.1: [DONE] [HARNESS] Streaming Baseline** (Verified Waterfall on 2080 Ti)
*   **Task 15.2: [DONE] [HARNESS] Forensic Prompt Recovery** (Identified "Structure Paradox": 3B models fail on Markdown headers)
*   **Task 15.3: [DONE] [CONDUCTOR] Minimalist Identity Anchor** (Applied to brain_node.py)
*   **Task 15.4: [DONE] [CONDUCTOR] LoRA De-escalation** (Disabled shadow_brain_v2 in infrastructure.json)
*   **Task 15.5: [DONE] [VERIFICATION] Resonant Shakedown** (Verified via test_complex.py: 167 tokens streamed, zero hallucinations)


