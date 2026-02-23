# Sprint Plan: SPR-11-02 "Agentic Reflection"
**Date:** Feb 23, 2026 | **State:** DRAFT | **Sprint ID:** SPR-11-02

## 🎯 Primary Objective
Transform the Lab from a linear tool-calling system into a "Lively Room" using **Agentic Reflection**. Agents will coordinate in front of the user using fillers, stutters, and immediate "perk-up" quips to eliminate perceived latency and simulate a multi-agent simulation (MAS).

## 🧬 Feature Set
### [FEAT-105] Multi-Agent Simulation (MAS)
- **Logic:** The Lab is a collaborative session where Pinky and Brain coordinate answers in real-time.
- **Goal:** Move beyond "Agent as API" to "Agent as Participant."

### [FEAT-106] Async Coordination Engine
- **Logic:** Enable Pinky to provide "Thinking Fillers" while the Brain's reasoning cycle is in-flight.
- **Refinement:** Pinky will use organic stutters (e.g., "Hmm...", "Wait...") immediately after shunting tasks.

### [FEAT-108] Inter-Agent Handover Signal
- **Logic:** The Hub (`acme_lab.py`) sends a low-latency "perk-up" trigger to the Brain as soon as intent is classified as strategic.
- **Result:** Brain provides an immediate `shallow_quip` while Pinky is still finishing his filler.

## 🧪 Testing Methodology
We will use a "Sequence Validation" approach to ensure the agents don't just talk, but talk *in order*.

### Proposed Tests:
1.  **`test_reflection_sequence.py`**
    *   **Goal:** Verify the 1-2-3 punch: User -> Pinky Filler -> Brain Quip -> Brain Deep.
    *   **Pass Condition:** All three messages arrive in < 5s, with the first two in < 1.5s.
2.  **`test_intent_shunt_latency.py`**
    *   **Goal:** Measure the time from User Input to the Brain's first "Perk-up" token.
    *   **Target:** < 800ms.
3.  **`test_persona_consistency.py`**
    *   **Goal:** Ensure Pinky's "Hmm..." doesn't accidentally trigger a recursive loop where Brain thinks Pinky is talking to him.
4.  **`test_room_liveliness.py`**
    *   **Goal:** Simulated stress test with overlapping queries to see if the "Room" remains coherent.

## 🗺️ Architectural Invariants
1.  **Non-Blocking:** No agent may wait for another before providing initial feedback.
2.  **Character over Speed:** A slightly slower organic stutter is better than a fast, robotic "Processing..." message.
3.  **No Echo:** Agents must ignore [SYSTEM] handovers in their own long-term context to prevent "Persona Bleed."

---
*Awaiting review and buy-in for SPR-11-02.*
