# Sprint Plan: [SPR-15.0] The Neural Relay
**Status:** ACTIVE | **Goal:** Implement the "Ping Pong" Flow (Fuel, Travel, and Cooldown) with speculative inter-node yielding.

---

## 🏛️ ARCHITECTURE DESIGN: THE NEURAL RELAY

### 1. The Speculative Handshake (Parallel Fan-out)
Moving from a linear "Wait-for-Turn" model to a synchronized, token-aware relay.
*   **The Logic**: 
    *   **Stage 0**: Lab Node (Sentinel) triages intent.
    *   **Stage 1 & 2 (Parallel Spark)**: Pinky and Shadow both start processing immediately. 
    *   **Intra-Node Yielding**: Shadow (2080 Ti) calculates technical intuition in the background but *yields* its output until Pinky (Persona) provides the "Fuel" score.
*   **The Why**: To eliminate perceived latency while maintaining deep hemispheric synergy. The Sovereign Brain (Remote 4090) receives a pre-filtered context package (Triage + Technical Hypothesis) rather than just a raw query.

### 2. Scalar Fuel Math (Emergent Routing)
Replacing booleans with a scalar `Importance` function.
*   **Fuel = f(Casual, Intrigue)**: 
    *   Calculated by the Sentinel but **mutable** by Pinky/Shadow. 
    *   If Pinky identifies a "High Stakes" keyword during her triage, she can "Add Fuel," forcing the relay to continue to the Sovereign tier even if the initial read was casual.
*   **The Why**: To allow the system to "change its mind" mid-turn if the complexity deepens during the triage phase.

### 3. The Ascension Rule (UI Partitioning)
*   **Ephemeral Layer (The Bar)**: Background tics and speculative pre-work (`final: false`) are shunted to the 1-line status bar. These are transient and never saved to history.
*   **Persistent Layer (The Console)**: Only when a turn is "Promoted" (`final: true`) does the text move from the status bar into the permanent technical ledger.
*   **The Why**: Maintains a clean, high-fidelity technical history without the clutter of "Thinking..." artifacts or rejected speculative paths.

---

## 🛠️ TASKS

### 📍 Phase 1: Protocol Hardening & Cooldown [FEAT-227]
**Goal:** Establish the safety rules and grounding logic.
*   **Task 1.1: Loopback Protection**: 
    *   *How*: Update `acme_lab.py` to strictly gate WebSocket ingestion on the `[ME]` anchor.
    *   *Why*: Prevents the "Are you pondering..." challenge from re-triggering the relay loop.
*   **Task 1.2: The Grounding Gate**: 
    *   *How*: Implement `evaluate_grounding()` in the Hub. Trigger Pinky summary for any node result (Shadow or Brain) that exceeds the Importance/Length threshold.
    *   *Why*: To ensure technical dumps are always anchored by a persona-driven TL;DR.
*   **Task 1.3: Terminal Cooldown**: 
    *   *How*: Tag Pinky's grounding turn as `is_terminal: true`.
    *   *Why*: To ensure the relay stops at the human-facing summary.

### 📍 Phase 2: The Speculative Handshake (Yielding) [FEAT-229]
**Goal:** Parallelize the local workload.
*   **Task 2.1: Local Fan-out**:
    *   *How*: Use `asyncio.gather` to spark Stage 1 (Pinky) and Stage 2 (Shadow) simultaneously.
    *   *Why*: Shadow is faster; its pre-work should be ready the moment Pinky finishes.
*   **Task 2.2: Speculative Buffer**:
    *   *How*: Implement a token buffer in `CognitiveHub`. Shadow output is held in `final: false` until "Fuel" confirms relevance.
    *   *Why*: To avoid UI flickering for rejected speculative paths.

### 📍 Phase 3: Scalar Routing (The Fuel Function) [FEAT-230]
**Goal:** Graduate from boolean intent to situational importance.
*   **Task 3.1: JSON Triage Expansion**:
    *   *How*: Update `lab_node.py` to return scalar `casual` and `intrigue` scores.
    *   *Why*: Allows for fine-grained control over model verbosity.
*   **Task 3.2: Shadow Scoring**: 
    *   *How*: Log calculated Fuel to `server.log` for calibration.
    *   *Why*: Verifies the math is grounded before it controls the physical silicon.

---

## ⚠️ COMPLEXITY & RISK MITIGATION REPORT

### 1. The "ME" Sentinel
*   **Risk**: High. Recursive dialogue loops.
*   **Mitigation**: **Atomic Anchor**. Hub ignores any input missing the `[ME]` signature.

### 2. Intra-Node Yielding
*   **Risk**: Speculative OOM.
*   **Mitigation**: **Unity Pattern Enforcement**. Both tasks run on the same 3B base to share memory.

### 3. Indicator of Speculation
*   **Status**: **[TBD]**.
*   **Concept**: Status bar shows `⚡ Shadow: 42% speculative...` during the yield phase.
