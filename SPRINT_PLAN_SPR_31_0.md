# SPRINT 31: THE GREAT BRAIN AWAKENING [REFACTOR PLAN]
**Status:** PLANNING | NO EXECUTION PERMITTED

## 🎯 MISSION
Execute a architectural refactor to align the Lab's terminology and file structure with the Phase 15 "Neural Relay" reality. We will promote local reasoning to "The Brain," transform the 4090 into the "Deep Thought" action, and move from monolithic management to modular "Appliance-Grade" services.

---

## 🧠 1. THE CONSCIOUSNESS SHIFT (Renaming & Logic)

### 📈 Metric Shift: Fuel -> INTEREST
*   **Concept**: We are moving from "Budgeting for cost" to "Reasoning for Depth."
*   **Variable Change**: `self.current_fuel` -> `self.interest_score`.
*   **Logic**: 
    *   **The Pull Pattern**: Pinky always streams to the Brain (Full Overhearing).
    *   **The Brain's Decision**: The Brain (Local) evaluates the `interest_score`. If the score is low and the turn is semantically "Complete," the Brain can autonomously choose NOT to follow up, enforcing high-fidelity brevity.
    *   **Impact**: Simplifies streaming logic by removing the "Early Trigger" gates in favor of a constant "Neural Bridge."

### 📚 Retrieval Shift: RRF Implementation
*   **Action**: Physically implement the **RRF Hybrid Retrieval** [BKM-032] enhancement designed in Sprint 30.
*   **Goal**: Enable exact-match surfacing of technical acronyms (e.g. PECISTRESSOR) alongside semantic vector results.

### 🔬 Node Promotion: Shadow -> THE BRAIN
*   **The Name**: "Shadow" is deprecated as an architectural term. The local 2080 Ti reasoning node is now officially **THE BRAIN**.
*   **The Action**: The Sovereign 4090 Ti is now accessed via the **Deep Thought** action [HHGTTG]. 
*   **The "Lobby" Preserve**: The ability for "Deep Thought" to provide an immediate fast-track response during local engine warm-up must be preserved as a core feature.
*   **Model Awareness**: The Brain will be made aware of the currently loaded "Deep Thought" model to minimize weight-swapping thrash, preferring multi-turn build-ups over fresh ignitions.

---

## 📐 2. MODULAR ARCHITECTURE (Lab Attendant v5)
*Goal: Decompose the v4 monolith into a modular, maintainable ecosystem.*

### 🛠️ The Split Strategy
| Module | Responsibilities | Target Logic |
| :--- | :--- | :--- |
| **`attendant.ignition`** | Silicon Startup, Port Authority, VRAM Verification. | [FEAT-119], [FEAT-254] |
| **`attendant.lifecycle`** | Hibernation Matrix, AFK resource guarding, H1/H2 transitions. | [FEAT-249], [FEAT-134] |
| **`attendant.router`** | Inter-node Websocket dispatch, Triage coordination. | [FEAT-233], [FEAT-234] |
| **`attendant.forensics`**| The Physician's Ledger, Pulse logging, Trace monitoring. | [FEAT-151], [FEAT-318] |

### 🏺 Legacy Preservation (The "Gold Master")
*   **Rule**: `lab_attendant_v4.py` will NOT be modified. It remains the stable reference.
*   **Method**: V5 will define clear **API Boundaries** (e.g., `/v5/status`, `/v5/start`) allowing us to swap between the V4 monolith and V5 modules during the shakedown phase.

---

## 🗺️ 3. THE RENAMING GAUNTLET (Impact Mapping)
*A cautious review of the 'Find/Replace' vs. 'Nuance' layers.*

| Layer | Type | Impact | Strategy |
| :--- | :--- | :--- | :--- |
| **File Names** | `shadow_node.py` -> `brain_node.py` | High | Git Move + Update `infrastructure.json`. |
| **Variables** | `fuel` -> `interest` | High | Project-wide Find/Replace with manual logic audit. |
| **Prompts** | "You are Shadow" -> "You are The Brain" | High | Update `BRAIN_SYSTEM_PROMPT` and `PINKY_SYSTEM_PROMPT`. |
| **FEATs** | [FEAT-158] Grounded Shadow | Med | Rename to [FEAT-158] Grounded Brain in `FeatureTracker.md`. |
| **Nuance** | "Deep Thought" Logic | High | Refactor `CognitiveHub` to treat 4090 calls as a "Deep Action" rather than a waterfall leg. |

---

## 🧪 4. DEFERRED SEMANTIC CERTIFICATION
*Applying BKM-032 to the Refactor.*

1.  **Phase A (The Hard Switch)**: Automated batch verify that all ports bind and the "Interest" scalar still calculates correctly (0.2/0.6 logic).
2.  **Phase B (The Voice Audit)**: Gemini CLI (AI Reviewer) reads the "Deep Thought" traces. 
    *   **Check**: Does Pinky address the local node as "Brain" correctly?
    *   **Check**: Does the "Interest Decay" feel natural vs. the old "Fuel" jitter?
    *   **Check**: Does the system stay vocal during the H2 -> V5 startup?

---

### ⚖️ LEAD ENGINEER REVIEW REQUIRED
*This plan is an artifact for Sprint 31. No code changes have been made.*
