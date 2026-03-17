# Sprint Plan: [SPR-14.0] The Eternal Forge
**Status:** ACTIVE | **Goal:** Integrate autonomous LoRA training into the nightly cycle and achieve full weight saturation.

## 🕵️ THE FORGE DEPTH & EVOLUTION AUDIT (Mar 17)

This audit identifies the "Alpha" status of current adapters and the path to high-fidelity saturation.

### 1. Adapter Depth (Alpha Status)
*   **`lab_history_v1`**: **MEDIUM-SHALLOW**. (~4.3 Epochs). Knows the 108 gems but lacks "ingrained" technical instinct.
*   **`cli_voice_v1`**: **SHALLOW**. (~0.7 Epochs). Has the "Vibe" but only 70% coverage.
*   **`lab_sentinel_v1`**: **OVERFIT/SHALLOW**. (20 Epochs on only 22 seeds). Perfectly understands mandates but lacks the 4,000+ prompt breadth.

### 2. The Evolution Model
*   **The Problem**: A full 7-hour "Cold Forge" blocks the lab and risks VRAM deadlocks.
*   **The Solution**: Transition to **[VIBE-013] Sequential Blending** and the **"Eternal Refinement"** model. 
*   **The Method**: Move training from a manual maintenance task to an autonomous **Step 6: Nightly Forge** in the Attendant.

---

## 🛠️ RESTORATION & INTEGRATION PLAN: THE SILICON HANDSHAKE

To ensure gradual, regression-free improvement, the training framework will be folded directly into the Lab Attendant, creating a closed-loop system between the Hub's "Dreams" and the Attendant's "Forge."

### 1. Attendant Forge Integration
*   **Tool**: `lab_train_adapter(name, steps)`.
*   **Pre-Check**: Consult `vram_characterization.json` and execute an autonomous silicon scrub before training begins.
*   **VRAM Handover**: Automate the Hub `quiesce` -> `Forge` -> `Re-ignite` sequence.

### 2. Dataset Expansion (The Sentinel Shield)
*   **New Mandate**: Step 5 (Dream Pass) must generate **"Negative Triage"** pairs (e.g., confusing or out-of-domain queries) to harden the Sentinel against overfitting.

---

## 🕵️ SPRINT AUDIT REPORT (Mar 17)

### 1. The "Silicon Valet" Handover Audit
*   **Accomplishments**: Found `mcp_train_adapter` successfully implemented in `lab_attendant_v3.py`. Verified that `train_expert.py` supports the `steps` parameter.
*   **Gap Found**: The **REST bridge** was incomplete. `lab_attendant_v3.py` lacked the `/train` endpoint, and `archive_node.py` (the proxy) was missing the tool. This meant the Hub's nightly call to `lab_train_adapter` would fail with an "Unbound Tool" error.
*   **Stability Risk**: The "Suicide Tool" pattern (Hub killing itself via Attendant) requires graceful WebSocket closure to prevent the "Broken Pipe" noise during the handover.

### 2. Implementation Strategy [ACTIVE]
*   **Step 1**: Harden `lab_attendant_v3.py` with full REST support for `/train`. **(COMPLETE)**
*   **Step 2**: Proxy the `lab_train_adapter` tool in `archive_node.py`.
*   **Step 3**: Execute a **5-Step Smoke Test** using `adapter_name="test_for"`.
*   **Step 4**: Verify the Inverted Chain's Step 6 in `acme_lab.py` by forcing a trigger.

---

## 🎯 TASKS & MILESTONES

### Move 1: The Silicon Handshake (Core Integration)
*   [x] **[FEAT-213] Autonomous Forge**: Implement `mcp_train_adapter` in `lab_attendant_v3.py`.
*   [x] **[FEAT-214] Parameterized Training**: Update `train_expert.py` to accept `max_steps` as a CLI argument. **(VERIFIED: DONE in commit ca13c26)**
*   [x] **Induction Step 6**: Add the `lab_train_adapter` call to the end of the `acme_lab.py` induction sequence. **(VERIFIED: DONE in commit bc575db)**
*   [x] **Round-Robin Scheduler**: Implement logic to alternate training targets (History -> Voice -> Sentinel) nightly. **(VERIFIED: DONE in commit bc575db)**
*   [x] **Proxy Tool**: Implement `lab_train_adapter` proxy in `archive_node.py`.

### Move 2: Cognitive Hardening
*   [x] **Negative Triage Generation**: Update `dream_voice.py` to produce counter-fact pairs for the Sentinel soul. **(VERIFIED: MAR 17 - Added sentinel mode)**
*   [x] **VRAM Guard Pre-check**: Integrate `characterization.json` verification into the forge start sequence. **(VERIFIED: MAR 17 - Integrated into mcp_train_adapter)**

### Move 3: Verification & Burn-In
*   [x] **The 5-Step Smoke**: Run a minimal 5-step training turn to verify the autonomous handover. **(VERIFIED: MAR 17 - Quiesce/Train/Ignite cycle successful)**
*   [x] **Documentation**: Finalize the "Eternal Forge" pedigree in **FeatureTracker.md**.

---

## 🏁 INTRODUCTION TO SPRINT 14.0

This sprint marks the transition from **Manual Induction** to **Autonomous Weight Evolution**. 

We have successfully "Grafted the Tendons" (Move 3) and proved that we can forge 3B adapters on the 2080 Ti. However, we found that manual "Cold Forges" are too disruptive and prone to VRAM contention. 

**The Pivot**: Instead of one-off training runs, we are implementing **Move 1: The Silicon Handshake**. This turns the Lab into a self-improving machine where the day's "Insights" are dreamed at 1:00 AM and baked into the silicon at 2:00 AM. 

The primary technical challenge is the **Autonomous VRAM Handover**: ensuring the Attendant can gracefully silence the Hub to reclaim the 11GB footprint needed for Unsloth, then restore the Mind once the nightly "Micro-Training" is complete.

---

## 💻 CODE CHANGES SUMMARY (MAR 17)

The following surgical updates have been applied to integrate the **Eternal Forge**:

1.  **Attendant V3.2 (`lab_attendant_v3.py`)**: Added `lab_train_adapter` MCP tool. This tool acts as the "Silicon Valet," managing the Hub's state to free up the 2080 Ti for Unsloth training.
2.  **Hub Hook (`acme_lab.py`)**: Integrated **Induction Step 6**. The Hub now autonomously triggers a training turn after the nightly "Dream Pass."
3.  **Round-Robin Logic**: The nightly training alternates between souls (`History` -> `Voice` -> `Sentinel`) to ensure gradual, balanced saturation across the bicameral mind.
4.  **Fidelity Restoration**: Re-integrated the **Cognitive Audit [FEAT-190]** and **Strategic Pivot [FEAT-173]** into the production Hub to ensure technical truth during the re-harvest.
