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
Monolithic adapters risk overfitting or pigeonholing the model to narrow personas. In Sprint 35, we will explore leveraging vLLM's native dynamic adapter hot-swapping:
1. **Vibe Grouping Scheme**: Rather than running 7 separate adapters (exceeding our VRAM slot budget), we group the taxonomy into three high-fidelity target adapters:
   - `cli_voice`: Expert in conversational flow and natural foil dialogue (mapping to the `CASUAL` vibe).
   - `architect`: Expert in systems validation, diagnostics, and telemetry analysis (consolidating the `TECHNICAL`, `OPERATIONAL`, and `ANALYTICAL` vibes).
   - `history`: Expert in historical notes, design pedigrees, and retrospective lookups (consolidating the `HISTORICAL` and `FORENSIC` vibes).
2. **Prompt-Resident Triage API**: Keep the triage node (Lab Sentinel) prompt-resident to maintain agile schema editing and avoid compile lock. Downstream experts (Brain, Pinky) will be trained via dataset distillation to natively expect, parse, and act on the triage payload (hints, vibes, and domains).

---

## 🛡️ CONCEPT 3: THE SELF-AWARENESS SHIELD (HEMISPHERIC SANDBOX)
*Objective: Prevent memory and tool bleed between lab orchestration files and physical engineering tasks.*

### 📋 Context & Research Blueprint
To prevent the model from confusing its own developmental metadata ("outside looking in" at its own state machine/systemd files) with active validation engineering tasks ("inside the lab" looking at telemetry), we will enforce strict semantic and functional isolation:
1. **Vibe Classification Guard**: The triage Sentinel node will classify queries concerning development plans, `Protocols.md`, or orchestrator details as `vibe: META`.
2. **Hemispheric Sandbox (Tool Isolation)**: To ensure safety and context purity, the `CognitiveHub` will dynamically strip and disable system-level tools (git commands, state-machine overrides, systemd controls) from the node's environment when executing standard engineering tasks (`TECHNICAL`/`HISTORY`).
3. **Prompt Routing**: Queries flagged as `vibe: META` will load system instructions containing lab metadata and expose system-level tools, while standard technical queries will be routed strictly to the engineering workspace logs and BKMs, completely shielding the model from developmental awareness during core engineering tasks.
