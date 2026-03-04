# Retrospective: [SPR-11-07] The Bicameral Evolution
**Date:** March 4, 2026 | **Scope:** Attendant V2, Bundling, and Narrative Grounding.

## 🎯 MISSION SUMMARY
The goal was to transform the relationship between **Pinky** and **The Brain** from a simple "Relay" (A then B) into an organic, emergent collaboration while debuting the **Bilingual Attendant (V2)**.

### **Key Wins:**
1.  **Attendant V2 [FEAT-142-144]:** Successfully deployed a dual-interface server supporting both REST (for systemd) and native MCP (for Gemini CLI).
2.  **The Resonant Chamber [FEAT-153]:** Implemented **Turn Bundling**, allowing the Hub to coordinate parallel node responses into a single emergent thought.
3.  **Sentient Sentinel [FEAT-154]:** Established interaction density monitoring to provide non-brittle "Exit Sentiment" hints.
4.  **Narrative Foil:** Pinky's prompt was transformed from "filler" to "Grounding Anchor," adopting the AYPWIP pattern to contrast the Brain's strategic complexity with literal hardware reality.

---

## 📖 THE "AYPWIP" STORY: EMERGENT THOUGHT
We successfully moved beyond "Banter." By injecting the Brain's **Strategic Intent** into Pinky's context, we created a "Resonant Chamber." 

**The Pattern:** 
- **Brain:** Calculates the 2019 PCIe regression root causes.
- **Pinky (The Foil):** Overhears the intent and quips: *"I think so Brain, but if the 2080 Ti gets any hotter, we'll be able to cook grilled cheese on the backplate! Narf!"*
- **Result:** The user receives a high-fidelity technical derivation grounded by a characterful, hardware-aware acknowledgement. This feels like a "Living Room" rather than an API.

---

## 🩹 THE SCARS (Forensic Analysis)

### **Scar #1: The FastMCP TTY Trap**
*   **The Issue:** Attempting to run `mcp.run_stdio_async()` inside a systemd service caused instant termination because `stdin` was redirected to `/dev/null`.
*   **The Pivot:** Implemented TTY detection in the `run_bilingual` entry point. The script now dynamically scales its protocol: **Service Mode** (REST only) vs. **Interactive Mode** (REST + MCP/Stdio).

### **Scar #2: Bundling UI Blindness**
*   **The Issue:** The `probe_hub.py` test script failed to display responses because it was hardcoded to wait for a specific `status` packet order that the new **Turn Bundling** logic had altered.
*   **The Pivot:** Verified liveness via `server.log` to confirm the nodes were processing correctly. The logic was sound; the test instrument was simply "blind" to the new parallel flow.

### **Scar #3: LoRA Path Fragility**
*   **The Issue:** Logs showed `Adapter pinky_v1 missing`. 
*   **The Reality:** The loader logic was looking for physical LoRA files that had been moved or were not yet initialized in the new vLLM environment. This caused a fallback to unified weights, which worked but lost the "Fine-Tuned" edge.

---

## 🛠️ FOLLOW-UP TASKS

### **1. Assassin Protocol: SSE Evolution (Follow-up to Scar #1)**
*   **Task:** Add an SSE (Server-Sent Events) transport to the Attendant. This will allow the Gemini CLI to connect to the running service via HTTP rather than spawning a new process, providing a "Hot Link" to the Lab without TTY issues.

### **2. Probe v2.0: Bundle-Aware Testing (Follow-up to Scar #2)**
*   **Task:** Refactor `probe_hub.py` to use an event-driven listener. Instead of waiting for specific packet order, it should "Bag" all packets associated with a unique `turn_id` and display the bundle once the Hub reports completion.

### **3. Personality Unification (Follow-up to Scar #3)**
*   **Task:** Consolidate the `pinky_v1` and `brain_v1` personality instructions directly into the Hub's system-prompt injection logic. This eliminates dependency on external LoRA adapter files, making the personality "BKM-resident" rather than "File-resident."

---
## 🏺 BASELINE COMMIT
`IMPLEMENTED: Bicameral Evolution Phases 1-4 (Attendant V2, Bundling, Sentinel)`
`SHA: c6eb613`
