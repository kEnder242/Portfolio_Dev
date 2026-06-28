# 🏗️ SPRINT 35: CLOSED-LOOP TRAINING & ADAPTIVE LORAS
*Status: ACTIVE*

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

---

## ⚡ SPRINT 35 PHASE 1: DATASET CLOSED-LOOP AUTOMATION & HEMISPHERIC SHIELDING
*Objective: Implement the data transition scripts, documentation distiller, automated pre-forge refresh, and tool isolation.*
*Status: ACTIVE*

### 📋 Forensic Rationale
To fulfill the strategic goals of closed-loop training and context safety, we require robust scripting to transition legacy CLI logs, extract conceptual QA records from project files, automate the nightly pipeline steps before model hibernation, and isolate toolsets at the router level during standard non-META queries. Each task is executed under the strict BKM-029 loop.

### 🛠️ Tasks
*   [x] **Task 1.0 (Transitional Log Merger)**:
    *   **Why**: Prevent losing historical conversation inputs during the migration to AGY CLI app data formats.
    *   **How (Mechanism)**: Modify `src/forge/extract_gemini_prompts.py` to search for chat transcripts in both legacy `~/.gemini/tmp/**/chats/*.json` and new AGY `/home/jallred/.gemini/antigravity-cli/brain/` directories, deduplicating and merging their outputs into `gemini_prompts_manifest.jsonl`.
    *   **Proof (Validation)**: Run `extract_gemini_prompts.py` and verify the log output reports parsing files from both roots and saving a valid manifest.
*   [x] **Task 1.1 (The Documentation Distiller)**:
    *   **Why**: Teach local models BKM structures and system logic from actual markdown files without raw text overfitting.
    *   **How (Mechanism)**: Create a new pipeline script `src/forge/distill_documentation.py` that reads specified markdown files, uses the active 4090 Brain to generate structured QA pairs (Question/Response format), and appends them to `bkm_master_manifest.jsonl`.
    *   **Proof (Validation)**: Run the distiller on `Protocols.md` and verify that the generated JSONL contains valid instruction/output formatting.
*   [x] **Task 1.2 (Ignition Pre-Forge Dataset Refresh)**:
    *   **Why**: Automate dialogue learning so that daily user interactions are trained into the weights during the next nightly loop.
    *   **How (Mechanism)**: Update `src/v5/ignition/manager.py` within the daily alarm sequence to trigger the dataset generation sequence (`extract_gemini_prompts.py`, `refine_prompts.py`, `dream_voice.py`, and `build_lora_datasets.py`) prior to calling `stop_lab` and invoking `train_expert.py`.
    *   **Proof (Validation)**: Perform a dry-run of the alarm flow and verify from the attendant logs that the dataset compilation scripts are invoked in sequence before training commands.
*   [x] **Task 1.3 (Hemispheric Sandbox Tool Isolation)**:
    *   **Why**: Prevent model tool hallucinations and protect system repositories from accidental execution of git or systemd tools during normal validation runs.
    *   **How (Mechanism)**: Update `src/logic/cognitive_hub.py` to inspect the triage vibe. If the vibe is NOT `META`, filter the available MCP tools, stripping out git, systemd, and state-machine controllers from the node's environment.
*   [ ] **Task 1.4 (Re-enable Nightly Induction Window)**:
    *   **Why**: Ensure the daily automated training sequence runs correctly at 2am after active development is complete.
    *   **How (Mechanism)**: Remove the `disable_induction.lock` file and perform a system check to verify that `is_window` status checks remain stable and responsive.
    *   **Proof (Validation)**: Remove `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/data/disable_induction.lock`, run a status query, and verify from log check that `disable_induction.lock` file is absent.

