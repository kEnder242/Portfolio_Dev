# 🏗️ SPRINT 35: CLOSED-LOOP TRAINING & ADAPTIVE LORAS
*Status: PLANNED*

### 🎯 MISSION
Transition the Acme Lab from a semi-automated batch training workflow into a fully closed-loop, self-refreshing intelligence lifecycle. Building upon the VRAM and audio pre-emption optimizations stabilized in Sprint 34, this sprint introduces the blueprint for automated daily dataset harvesting/dreaming, dynamic multi-LoRA domain-specific layering at runtime, and strict context shielding to prevent self-awareness bleed.

---

## 🔄 CONCEPT 1: CLOSED-LOOP NIGHTLY DATASET REFRESH
*Objective: Automate the harvest-refine-dream cycle prior to nightly training.*

### 📋 Context & Research Blueprint
Currently, dataset extraction (`extract_gemini_prompts.py`), refinement (`refine_prompts.py`), and target voice synthesis (`dream_voice.py`) are manual or semi-automated batch processes. In Sprint 35, the system will integrate these steps directly into the **Daily Induction Window** loop managed by the `IgnitionManager`:
1. **Transitional Log Merger**: Update the prompt extractor to dynamically scan and merge user session logs from both the legacy path (`~/.gemini/tmp/`) and the new AGY App Data layout (`~/.gemini/antigravity-cli/brain/`) during the transitional migration period.
2. **The Documentation Distiller**: Move away from training on raw notes or telemetry data. Implement a synthetic Q&A generation pipeline where the copilot reads local engineering markdown documents and BKMs (such as `FeatureTracker.md` or `Protocols.md`) and synthesizes high-density, conversational Q&A pairs (simulating technical peer-to-peer dialogues).
3. **Incremental Dreaming**: Before shutting down the vLLM server to free VRAM, query the active engine to synthesize "Ideal Peer Responses" only for the newly harvested prompts (using the resume seen-prompt check).
4. **Collation & Forge**: Re-compile the datasets, spin down the vLLM engine, acquire the VRAM mutex, and execute `train_expert.py` to compile the new weights.

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

---

## 🛡️ CONCEPT 3: THE SELF-AWARENESS SHIELD (CONTEXT ISOLATION)
*Objective: Prevent memory bleed between lab orchestration files and physical engineering tasks.*

### 📋 Context & Research Blueprint
To prevent the model from confusing its own developmental metadata ("outside looking in" at its own state machine/systemd files) with active validation engineering tasks ("inside the lab" looking at telemetry), we will enforce strict semantic isolation:
1. **Vibe Classification Guard**: The triage Sentinel node will classify queries concerning development plans, `Protocols.md`, or orchestrator details as `vibe: META`.
2. **Prompt Routing**: Queries flagged as `vibe: META` will load system instructions containing lab metadata, while standard technical queries will be routed strictly to the engineering workspace logs and BKMs, completely shielding the model from developmental awareness during core engineering tasks.
