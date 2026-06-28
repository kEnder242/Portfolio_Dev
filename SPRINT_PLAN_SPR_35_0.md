# 🏗️ SPRINT 35: CLOSED-LOOP TRAINING & ADAPTIVE LORAS
*Status: PLANNED*

### 🎯 MISSION
Transition the Acme Lab from a semi-automated batch training workflow into a fully closed-loop, self-refreshing intelligence lifecycle. Building upon the VRAM and audio pre-emption optimizations stabilized in Sprint 34, this sprint introduces the blueprint for automated daily dataset harvesting/dreaming and dynamic, multi-LoRA domain-specific layering at runtime.

---

## 🔄 CONCEPT 1: CLOSED-LOOP NIGHTLY DATASET REFRESH
*Objective: Automate the harvest-refine-dream cycle prior to nightly training.*

### 📋 Context & Research Blueprint
Currently, dataset extraction (`extract_gemini_prompts.py`), refinement (`refine_prompts.py`), and target voice synthesis (`dream_voice.py`) are manual or semi-automated batch processes. In Sprint 35, the system will integrate these steps directly into the **Daily Induction Window** loop managed by the `IgnitionManager`:
1. **Incremental Chat Harvesting**: Run the extractor to scan local session logs under `~/.gemini/tmp/` for the day's chats, followed by refinement to filter terminal noise.
2. **Incremental Dreaming**: Before shutting down the vLLM server to free VRAM, query the active engine to synthesize "Ideal Peer Responses" only for the newly harvested prompts (using the resume seen-prompt check).
3. **Collation & Forge**: Re-compile `cli_voice_training.jsonl`, spin down the vLLM engine, acquire the VRAM mutex, and execute `train_expert.py` to compile the new weights.

---

## 🧠 CONCEPT 2: DYNAMIC TASK-SPECIFIC ADAPTER LAYERING
*Objective: Layer specialized low-rank adapters at runtime instead of relying on a monolithic voice/history file.*

### 📋 Context & Research Blueprint
Monolithic adapters (like the historical `cli_voice`) risk overfitting or pigeonholing the model to narrow personas. In Sprint 35, we will explore leveraging vLLM's native dynamic adapter hot-swapping:
1. **Specialized Experts**: Train tiny, high-density, single-purpose adapters:
   - `telemetry_audit_lora`: Expert in GPU/PCIe/MSR registers.
   - `architecture_lora`: Expert in systems design and BKM documentation.
   - `conversational_casual_lora`: A pure dialogue/banter foil.
2. **Dynamic Layering**: The Foyer Router will read triage vibes from the Sentinel node and dynamically load/combine these adapters in the inference request headers on-the-fly, providing tailored cognitive loadouts for each user query.
