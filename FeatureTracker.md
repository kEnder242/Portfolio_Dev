# Feature Tracker: The DNA Association Matrix
**Role: [FEAT] Technical Capabilities | [VIBE] Persona & Style**

# Philosophy

**Features as "The Bones"**: Prototyping is fluid, but established system capabilities must be frozen as features with unique Feature IDs in [FeatureTracker.md](https://github.com/kEnder242/Portfolio_Dev/blob/main/FeatureTracker.md). These features form the rigid, skeletal bones of the codebase.

**AI Grounding via Token Anchors**: During iterative refactoring or bug fixes, AI co-pilots are prone to context drift and accidental deletion of logic. To prevent this, we reference Feature IDs directly in prompts and code comments. This leverages the model's self-attention, anchoring the AI to our documented structural constraints and preserving the codebase's integrity.

---

## [FEAT-030] Unity Pattern (Multi-LoRA Residency) [SCAR #5]
**Status:** ACTIVE
**Code:** [src/start_vllm.sh](https://github.com/kEnder242/HomeLabAI/blob/main/src/start_vllm.sh#L3) — Unity Pattern (Multi-LoRA Residency) [SCAR #5].
**Logic:** Run all concurrent local nodes (Pinky, Shadow Brain, Lab Actor) on a shared **Unified 3B Base Model** footprint. 
**Rationale:** To maximize VRAM efficiency on the 11GB 2080 Ti. By sharing the base weights, we only pay the VRAM penalty once, while switching "personalities" through low-overhead LoRA adapters.
**SCAR #5:** Windows Isolation. Windows (Node 'Brain') remains Sovereign and decoupled from Linux model sync.
**Mechanism:** vLLM 0.16.0 with `--enable-lora` support for dynamic adapter switching.

## [FEAT-154] Environmental Awareness Node (The Lab Actor)
**Status:** ACTIVE (UNITY-ALIGNED)
**Code:** [src/debug/manual_vllm_igniter.sh](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/manual_vllm_igniter.sh#L14) — Environmental Awareness Node (The Lab Actor).
**Logic:** The "Lab" is a first-class LLM resident running on the **Unified 3B Base**.
**Rationale:** To maintain [FEAT-030] Unity compliance. The Lab Actor shares the same VRAM footprint as Pinky and the Shadow Brain, ensuring zero additional memory overhead.
**Mechanism:** A specialized, low-latency LoRA adapter (`lab_sentinel_v1`) that transforms the 3B base into a situational auditor. It "hears" user input + hardware telemetry and outputs high-level coordination hints (e.g. `[EXIT_LIKELY]`, `[STRATEGIC]`) to the other nodes.

## [FEAT-155] Sovereign Ultra Sovereignty (Qwen 27B)
**Status:** ACTIVE
**Code:** [src/v5/foyer/router.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/foyer/router.py#L565) — Sovereign Ultra Sovereignty (Qwen 27B).
**Logic:** High-fidelity reasoning on **KENDER** (4090) using the Claude-distilled Qwen 27B model.
**Rationale:** 8B models lack the "Logic Glue" for high-fidelity synthesis. 27B distilled model maintains complex reasoning chains and high instructional adherence.
**Rule:** Unified residency. This model handles BOTH strategic chat and nightly synthesis tasks to maintain logic continuity. No active swapping required during sessions.

## [FEAT-039] [DEFEATURED] Banter Decay (Adaptive Reflex)
**Status:** DEFEATURED (Feb 2026)
**Code:** *none found (documented only)*
**Reason:** Replaced by [FEAT-152] (Metabolism of Presence). Frequency-based idling was too system-noisy.

## [FEAT-054] [DEFEATURED] Banter Decay Test
**Status:** DEFEATURED (Feb 2026)
**Code:** *none found (documented only)*
**Reason:** Simulation for frequency decay is obsolete.

## [FEAT-047] [DEFEATURED] Reflex Tics
**Status:** DEFEATURED (Feb 2026)
**Code:** *none found (documented only)*
**Reason:** Replaced by Mode-Aware Grounding in [FEAT-152].

## [FEAT-068] [DEFEATURED] Persona-Locked Dispatch (The Iron Gate)
**Status:** DEFEATURED (Feb 2026)
**Code:** *none found (documented only)*
**Reason:** Rigid isolation prevented the "Collaborative Turn" required for emergent thought. Replaced by [FEAT-153].

## [FEAT-033] [DEFEATURED] Iron Gate (Persona Isolation)
**Status:** DEFEATURED (Feb 2026)
**Code:** *none found (documented only)*
**Reason:** isolation prevented collaborative synthesis. Replaced by [FEAT-153].

## [FEAT-028] Strategic Ping (Generation Probe)
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L830) — Strategic Ping (Generation Probe).
**Logic:** Functional Logic Verification verifying the *Mind* is alive (not just the process).
**Mechanism:** Single-token generation probe in `acme_lab.py` to trigger Brain-to-Shadow failover.

## [FEAT-023] The Stoic Strategist (Identity Anchor)
**Status:** ACTIVE (RE-GROUNDED)
**Code:** [field_notes/evaluate_rag.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/evaluate_rag.py#L160) — The Stoic Strategist (Identity Anchor).
**Logic:** Brain is the "Stoic Reasoner" (Opus Distillation); Pinky is the "Intuitive Foil" (AYPWIP literalism). 
**Verification:** `src/debug/test_persona_bugs.py`.

## [FEAT-036] VRAM Guard (Conscious Attendant) [SCAR #1]
**Status:** ACTIVE
**Code:** [src/v5/ignition/manager.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/ignition/manager.py#L324) — VRAM Guard (Conscious Attendant) [SCAR #1].
**Logic:** A "Deep Sleep" protocol that stubs the Brain/Pinky nodes if VRAM pressure exceeds critical thresholds (95%) or engines fail to load.
**SCAR #1:** Feb 20 "Aggressive Healing" collision during 550 driver install. Resolved via [FEAT-138].
**Mechanism:** `vram_watchdog_loop` in `lab_attendant.py`.
**Verification:** `src/test_vram_guard.py`.

## [FEAT-037] Hierarchical Mind (The Architect)
**Status:** ACTIVE (Dormant)
**Code:** [src/nodes/lab_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/lab_node.py#L62) — Hierarchical Mind (The Architect).
**Logic:** A specialized node (`architect_node.py`) capable of generating BKMs and building semantic maps of the archive.
**Mechanism:** `generate_bkm` and `build_semantic_map` tools.
**Note:** Code exists but active utilization in the loop is currently low.

## [FEAT-038] Nightly Recruiter
**Status:** ACTIVE
**Code:** [src/test_recruiter.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/test_recruiter.py#L4) — Nightly Recruiter.
**Logic:** An automated logic path that matches the CV summary against cached job descriptions or recruiter queries.
**Verification:** `src/test_recruiter.py` (Verify existence).

## [FEAT-053] Contextual Tics
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L418) — Contextual Tics.
**Logic:** Updates `monitor_task_with_tics` to provide Brain-health-specific feedback (e.g., "Resonating weights", "Sovereign unreachable") during long reasoning tasks.

## [FEAT-055] Manual Task Trigger (Fast Alarm)
**Status:** ACTIVE
**Code:** [src/debug/trigger_mute.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/trigger_mute.py#L6) — Manual Task Trigger (Fast Alarm).
**Logic:** Adds `--trigger-task` flag to `acme_lab.py` to allow immediate execution of scheduled jobs (Recruiter/Architect) for debugging.

## [FEAT-066] The "Temporal Moat" (Context Aging)
**Status:** ACTIVE (TRANSFORMING)
**Code:** [src/debug/test_banter_decay.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/test_banter_decay.py#L21) — The "Temporal Moat" (Context Aging).
**Logic:** Dynamically shifts Pinky's cognitive mode and polling interval (`reflex_ttl`) based on session interaction density.
**Rationale:** Simple frequency decay was too system-noisy. Mode-based scaling allows Pinky to remain a constant presence while shifting focus between "Collaborative Frame" (High Activity) and "Literal Grounding" (Idle).
**Modes:**
1.  **High-Activity (Collaborative):** Pinky frames and pre-fills Brain's strategic derivations.
2.  **Idle (Literal Grounding):** Pinky focuses on literal hardware vitals and AYPWIP-style "I think so Brain, but..." absurdity.
**Mechanism:** Hub state variable `metabolism` influencing node system prompts via situational hint injection, while scaling `reflex_ttl` from 1s to 6s.

## [FEAT-067] Diamond Dreaming (Subconscious Consolidation)
**Status:** ACTIVE
**Code:** [src/nodes/brain_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/brain_node.py#L6) — Diamond Dreaming (Subconscious Consolidation).
**Logic:** A background process (`dream_cycle.py`) that periodically synthesizes chaotic interaction logs into high-density "Diamond Wisdom" paragraphs.
**Mechanism:** Employs a cross-host fallback (Windows 4090 -> Local 2080 Ti) to ensure memory evolution even during partial outages.

## [FEAT-069] Hardware-Aware Adaptive Runtime (Resilience Ladder) [SCAR #2]
**Status:** ACTIVE
**Code:** [field_notes/jellyfin_autotune.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/jellyfin_autotune.py#L4) — Hardware-Aware Adaptive Runtime (Resilience Ladder) [SCAR #2].
**Logic:** Automatically "Downshifts" or suspends reasoning engines based on real-time NVML telemetry to maintain Lab availability during hardware multi-tenancy.
**SCAR #2:** Feb 13 "333MiB Wall" / Turing BF16 initialization deadlock.
**Mechanism:**
1.  **Tier 1 (Primary)**: Standard Ollama using **Unified Base (Llama-3.2-3B)**. 
2.  **Tier 2 (Downshift)**: Transition to **Llama-3.2-1B** or **TinyLlama** when moderate GPU pressure is detected (>8GB VRAM used by external apps).
3.  **Tier 3 (Hibernation)**: Full SIGTERM of AI engines during critical GPU pressure (e.g., 4K Gaming). 
4.  **Preservation**: Session context is preserved in the Hub's `recent_interactions` list, allowing for a "Warm Start" once resources are freed.
**Verification:** `src/debug/test_downshift_protocol.py`.

## [FEAT-070] Hallucination Shunting
**Status:** ACTIVE
**Code:** [src/infra/cognitive_audit.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/infra/cognitive_audit.py#L24) — Hallucination Shunting.
**Logic:** If a reasoning node attempts to use an unknown or hallucinated tool, the orchestrator intercepts the error and shunts it back to the Pinky Gateway for characterful recovery and user feedback.

## [FEAT-064] Static Site Synthesis (build_site.py)
**Status:** ACTIVE
**Code:** [field_notes/build_site.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/build_site.py#L1) — Static Site Synthesis (build_site.py).
**Logic:** Automated pipeline that clears caches and prepares the `www_deploy` directory for public hosting.
**Mechanism:** Runs `python3 field_notes/build_site.py` to trigger versioned cache-busting and asset bundling.

## [FEAT-065] Cross-Platform Synchronization
**Status:** ACTIVE
**Code:** [src/infra/delegate_retrospective.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/infra/delegate_retrospective.py#L4) — Cross-Platform Synchronization.
**Logic:** Shell-based synchronization (`sync_to_linux.sh`, `sync_to_windows.sh`) using `rsync` and Google Drive mounts to maintain code parity across the hybrid lab.

## [FEAT-062] Protocol Handshake (Version Sync)
**Status:** ACTIVE (Passive)
**Code:** [release.sh](https://github.com/kEnder242/HomeLabAI/blob/main/release.sh#L24) — Protocol Handshake (Version Sync).
**Logic:** CLI and Web clients send a `handshake` packet with their local `VERSION` string upon connection. 
**Mechanism:** Orchestrator logs the client version and responds with its own server-side `VERSION` in the initial `status` broadcast.

## [FEAT-063] Cache-Busting Deployment
**Status:** ACTIVE
**Code:** [src/tests/test_live_audio_memory_benchmark.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/test_live_audio_memory_benchmark.py#L7) — Cache-Busting Deployment.
**Logic:** Uses query-string versioning (e.g., `script.js?v=fc6916a8`) in `intercom.html` to force browsers and Cloudflare to bypass stale caches during infrastructure updates.

## [FEAT-058] Strategic Console Routing
**Status:** ACTIVE
**Code:** [field_notes/tests/routing_test.html](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/tests/routing_test.html#L1) — Strategic Console Routing.
**Logic:** Intercom UI (`intercom_v2.js`) distinguishes between "TRUE Brain" messages and "Brain (Shadow)" predictions.
**Mechanism:** Shadow predictions and true insights route to the Brain's Insight panel, while triage/banter stays in Pinky's console.
**Verification:** `field_notes/tests/routing_test.html`.

## [FEAT-059] Real-Time PCM Audio Streaming
**Status:** ACTIVE
**Code:** [src/tests/test_live_audio_memory_benchmark.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/test_live_audio_memory_benchmark.py#L3) — Real-Time PCM Audio Streaming.
**Logic:** Browser-based voice capture downsamples audio to 16kHz mono and converts to Signed Int16 PCM before WebSocket streaming.
**Verification:** `src/debug/test_web_binary.py`.

## [FEAT-076] Sovereign Response Verification
**Status:** ACTIVE
**Code:** [src/infra/cognitive_audit.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/infra/cognitive_audit.py#L13) — Sovereign Response Verification.
**Logic:** A multi-layered test suite that verifies the Brain's reasoning capacity and its primary-to-fallback lifecycle.
**Verification:** 
- `src/debug/test_pi_flow.py`: Verifies end-to-end technical accuracy and bicameral delegation.
- `src/test_lab_integration.py`: Verifies node-to-orchestrator connectivity and life-cycle management.

## [FEAT-077] Fidelity Gate (Quality Gate)
**Status:** ACTIVE
**Code:** [src/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/cognitive_hub.py#L3) — Fidelity Gate (Quality Gate).
**Logic:** Intercepts "Thin" or empty reasoning responses and triggers autonomous retries or strategic pivots.
**Rationale:** To prevent high-latency models from providing low-fidelity or hallucinated "short" answers.
**Mechanism:** `CognitiveHub` word-count check and [BKM-015.1] bypass for technical constants.

## [FEAT-075] Content Immutability (The 18-Year Lock)
**Status:** ACTIVE (Mandate)
**Code:** [src/infra/delegate_retrospective.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/infra/delegate_retrospective.py#L6) — Content Immutability (The 18-Year Lock).
**Logic:** Explicitly protects technical narrative assets (e.g., `stories.html`) from LLM-driven "summarization" or truncation.
**Rule:** Structural UI updates (CSS/JS/Sidebar) are allowed, but paragraph-level content must remain 100% word-faithful to the original 18-year engineering history.
**Verification:** Manual `diff` and word-count checks during UI refactors.

## [FEAT-060] Multi-Pane Workspace (EasyMDE)
**Status:** ACTIVE
**Code:** [src/test_draft_agency.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/test_draft_agency.py#L1) — Multi-Pane Workspace (EasyMDE).
**Logic:** Integrated Markdown editor with live WebSocket save/load and resizable split-pane layout.
**Verification:** `src/test_draft_agency.py`.

## [FEAT-056] MIB Memory Wipe (Neuralyzer)
**Status:** ACTIVE
**Code:** [src/tests/test_live_audio_memory_benchmark.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/test_live_audio_memory_benchmark.py#L3) — MIB Memory Wipe (Neuralyzer).
**Logic:** Allows user to manually clear the interaction context using trigger phrases like "Look at the light" or "Neuralyzer".
**Mechanism:** Resets `self.recent_interactions` in `acme_lab.py`.
**Verification:** `src/debug/test_mib_wipe.py`.

## [FEAT-057] Deep Context (Amnesia Removal)
**Status:** ACTIVE
**Code:** [src/debug/harness_brain.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/harness_brain.py#L13) — Deep Context (Amnesia Removal).
**Logic:** Removed amnesic slicing (`[-3:]`) and increased interaction cap from 10 to 50, providing Pinky with deep mid-term memory.
**Verification:** `src/debug/test_mib_wipe.py`.

## [FEAT-043] Dead-Man's Switch
**Status:** ACTIVE
**Code:** [field_notes/assets/marked.min.js](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/assets/marked.min.js#L65) — Dead-Man's Switch.
**Logic:** Triggers a `CRITICAL` alert to `pager_activity.json` if the Lab port 8765 is unresponsive for more than 5 minutes, signaling unrecoverable failure.

## [FEAT-048] Monitor Task with Tics
**Status:** ACTIVE
**Code:** [src/debug/monitor_wall.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/monitor_wall.py#L16) — Monitor Task with Tics.
**Logic:** Sends periodic "Thinking..." updates to the user during long-running Brain reasoning tasks to provide progress feedback.

## [FEAT-049] Scheduled Tasks (Alarm Clock)
**Status:** ACTIVE
**Code:** [src/forge/serial_harvest_v2.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/forge/serial_harvest_v2.py#L9) — Scheduled Tasks (Alarm Clock).
**Logic:** Background loop that triggers automated jobs: Nightly Recruiter (02:00 AM) and Hierarchy Refactor (03:00 AM).

## [FEAT-050] Strategic Vibe Check on Save
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L1704) — Strategic Vibe Check on Save.
**Logic:** Automatically triggers a Brain-level validation of technical logic and architectural advice whenever a file is saved in the workspace.

## [FEAT-031] Logger Isolation (The Montana Fix)
**Status:** ACTIVE
**Code:** [src/nodes/pinky_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/pinky_node.py#L4) — Logger Isolation (The Montana Fix).
**Logic:** Hardens the Lab against stdout/stderr hijacking by asynchronous libraries.
**Mechanism:** 
1.  **Redirection**: Routes `acme_lab.py` and `loader.py` logging to `sys.stderr`.
2.  **Reclamation**: Employs `reclaim_logger()` to strip global handlers after heavy imports (NeMo, ChromaDB).
**Verification:** `src/debug/test_forensic_logging.py`.

## [FEAT-133] Staged Resident Ignition (Sequencing)
**Status:** ACTIVE
**Code:** [field_notes/sanitize_achievements.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/sanitize_achievements.py#L6) — Staged Resident Ignition (Sequencing).
**Logic**: Prevents initialization deadlocks and VRAM spikes by serializing the boot sequence of inference nodes.
**Mechanism**:
1.  **Serialization**: The orchestrator loads nodes sequentially: `archive` -> `pinky` -> `brain`.
2.  **Staggered Sleep**: Enforces a mandatory 2-second delay between node starts to allow the event loop and memory buffers to stabilize.
**Verification**: `src/test_liveliness.py` (Verify sequential ready states).

## [FEAT-032] Strategic Sentinel (Amygdala Filter)
**Status:** ACTIVE
**Code:** [src/nodes/thought_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/thought_node.py#L6) — Strategic Sentinel (Amygdala Filter).
**Logic:** Dual-gated input filter. Voice mode uses keyword sentinel (strat_keys); Typing mode uses 1B model (stubbed) to prevent casual clutter.
**Mechanism:** `self.mic_active` toggle in `acme_lab.py`.

## [FEAT-034] Barge-In Logic (Interrupts)
**Status:** ACTIVE
**Code:** [src/tests/test_routing_logic.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/test_routing_logic.py#L2) — Barge-In Logic (Interrupts).
**Logic:** Allows user to cancel long reasoning cycles using voice interrupt keys ("wait", "stop", "hold on", "shut up").
**Mechanism:** `ear_poller` loop in `acme_lab.py`.

## [FEAT-035] Zombie Port Recovery
**Status:** ACTIVE
**Code:** [src/lab_attendant.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/lab_attendant.py#L1) — Zombie Port Recovery.
**Logic:** The Lab Attendant monitors port 8765. If the process is alive but the port is unresponsive for 3 intervals, it triggers an autonomous engine swap.
**Mechanism:** `vram_watchdog_loop` in `lab_attendant.py`.

## [FEAT-029] Absolute Zero Hardware Purification
**Status:** ARCHIVED (Feb 19 BKM)
**Code:** [field_notes/jellyfin_autotune.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/jellyfin_autotune.py#L4) — Absolute Zero Hardware Purification.
**Logic:** To break circular dependency deadlocks during driver installation, the system purges all GPU-polling services and physically erases module files (`.ko.zst`) to secure a 100% vacant hardware window.
**Mechanism:** `SESSION_BKM_FEB_19.md`.

## [FEAT-027] Iron Partition (Identity Separation)
**Status:** ACTIVE
**Code:** [src/infra/atomic_io.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/infra/atomic_io.py#L15) — Iron Partition (Identity Separation).
**Logic:** Server-side identity gating that ensures session artifacts and short-term context are strictly re-initialized during context switches.
**Rationale:** Prevents "Cross-Session Pollution" and ensures the Lab foyer remains a clean slate for new users.

## [FEAT-071] Internal Debate (Offline Collaboration)
**Status:** ACTIVE
**Code:** [src/internal_debate.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/internal_debate.py#L7) — Internal Debate (Offline Collaboration).
**Logic:** Logic allowing nodes to exchange 3-5 turns of dialogue on a specific topic without user input. 
**Mechanism:** `InternalDebate` class in `src/internal_debate.py`.

## [FEAT-072] Morning Briefing
**Status:** ACTIVE
**Code:** [src/tests/test_memory_architecture.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/test_memory_architecture.py#L8) — Morning Briefing.
**Logic:** Pinky summarizes the "Nightly Dialogue" or "Dream Synthesis" upon the user's first connection of the day.

## [FEAT-073] Insight Pruning (Curated Redaction)
**Status:** ACTIVE
**Code:** [src/nodes/archive_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/archive_node.py#L381) — Insight Pruning (Curated Redaction).
**Logic:** A surgical tool in the Archive Node (`prune_insights`) that allows for pattern-based trimming of note summaries within a date range.
**Constraint:** Follows the "trim, don't rewrite" mandate, using regex to replace specific strings (like last names) while preserving technical context.

## [FEAT-080] Dynamic Model Fluidity
**Status:** ACTIVE
**Code:** [src/nodes/loader.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/loader.py#L218) — Dynamic Model Fluidity.
**Logic:** Dynamically selects the best available model on a host by querying `/api/tags`.
**Mechanism:** `_resolve_best_model` in `loader.py` matches host capabilities against a prioritized preference list.

## [FEAT-081] Hemispheric Decoupling
**Status:** ACTIVE
**Code:** [src/legacy_deepagent/original_audio_server.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/legacy_deepagent/original_audio_server.py#L23) — Hemispheric Decoupling.
**Logic:** Allows Brain and Pinky to use host-appropriate models independently.
**Mechanism:** `lab_attendant.py` sets `BRAIN_MODEL` and `PINKY_MODEL` environment variables based on host affinity (KENDER vs Local).

## [FEAT-082] Neural Priming
**Status:** ACTIVE
**Code:** [src/debug/test_kender_restore.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/test_kender_restore.py#L13) — Neural Priming.
**Logic:** Proactively loads the selected model into VRAM upon WebSocket connection.
**Mechanism:** Triggers an immediate `check_brain_health` probe with `num_predict: 1` in `acme_lab.py` during the handshake.

## [FEAT-083] Smaller Sovereign (8B Priority)
**Status:** ACTIVE
**Code:** [src/test_liger.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/test_liger.py#L21) — Smaller Sovereign (8B Priority).
**Logic:** Prioritizes 8B class models (Llama 3.1) over large models (Mixtral) to guarantee <10s load times.
**Verification:** Forensic logs confirm `llama3.1:8b` selection on KENDER despite LARGE tier request.

## [FEAT-084] Neural Persistence (Resolution Cache)
**Status:** ACTIVE
**Code:** [src/nodes/loader.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/loader.py#L796) — Neural Persistence (Resolution Cache).
**Logic:** Caches the resolved engine/model mapping for 60 seconds to eliminate per-query network overhead.
**Mechanism:** `_engine_cache` in `loader.py` with automatic invalidation on request failure.

## [FEAT-085] Intelligent Keep-Alive
**Status:** ACTIVE
**Code:** [src/debug/test_frontend_5x5.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/test_frontend_5x5.py#L26) — Intelligent Keep-Alive.
**Logic:** Proactively primes the Brain every 2 minutes only while a client is connected.
**Mechanism:** Conditional generation probes in `acme_lab.py` ensure the model remains resident in VRAM during active sessions.

## [FEAT-086] Tiered Brain Response (Preamble)
**Status:** ACTIVE
**Code:** [src/infra/cognitive_audit.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/infra/cognitive_audit.py#L13) — Tiered Brain Response (Preamble).
**Logic:** Provides sub-second feedback for deep strategic tasks by broadcasting an immediate "Thinking..." message.
**Mechanism:** Hardcoded async broadcast in `acme_lab.py` triggered before shunting to the reasoning node.

## [FEAT-087] Intelligent Handshake Priming
**Status:** ACTIVE
**Code:** [release.sh](https://github.com/kEnder242/HomeLabAI/blob/main/release.sh#L34) — Intelligent Handshake Priming.
**Logic:** Forces VRAM residency of the primary model upon first connection.
**Mechanism:** High-priority generation probe (`force=True`) inside the `handshake` packet handler in `acme_lab.py`.

## [FEAT-088] Semantic Career Recall
**Status:** ACTIVE
**Code:** [src/nodes/archive_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/archive_node.py#L879) — Semantic Career Recall.
**Logic:** The "Receptionist" intent detection that triggers RAG. The fundamental ability to query 18 years of technical history via natural language based on semantic intent rather than rigid regex.
**Mechanism:** Vector search via ArchiveNode bridging the local JSON logs to the reasoning nodes. Uses the Lab Node's Intent (RECALL) as the sole authority.
**Refactor Strategy:** Expand to improve multi-year "Neighborhood" search depth, allowing the system to automatically retrieve context for preceding years to ensure narrative continuity.

## [FEAT-089] Zero Trust Guest Expansion
**Status:** ACTIVE
**Code:** [field_notes/intercom_v2.js](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/intercom_v2.js#L20) — Zero Trust Guest Expansion.
**Logic:** Securely allows authorized third-party recruiters (e.g., from `intel.com`) to access the technical lobby.
**Mechanism:** Cloudflare Access Policy updates for `notes.jason-lab.dev` and `acme.jason-lab.dev`.

## [FEAT-090] Non-Blocking Parallel Dispatch
**Status:** ACTIVE (HYBRID)
**Code:** [src/tests/test_delegate_canary.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/test_delegate_canary.py#L4) — Non-Blocking Parallel Dispatch.
**Logic:** Stream components individually to the UI for "Live Feedback" [VIBE-002], but bundle them in the `conversations.log` for unified turn history.
**Mechanism:** Node responses are broadcast to the user as they finish using `asyncio.as_completed` (or parallel handlers), allowing Pinky's fast replies to appear instantly while Brain calculates.

## [FEAT-091] Tiered Thinking (Shallow Mode)
**Status:** ACTIVE
**Code:** [src/internal_debate.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/internal_debate.py#L47) — Tiered Thinking (Shallow Mode).
**Logic:** Dynamically selects reasoning depth based on intent and direct address.
**Mechanism:** `shallow_think` tool in Brain node uses a laconic system prompt and low token cap for greetings and quips, while `deep_think` handles strategic complexity.

## [FEAT-092] Persona De-personalization (Cognitive Firewall)
**Status:** ACTIVE
**Code:** [src/train/distill_training_data.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/train/distill_training_data.py#L27) — Persona De-personalization (Cognitive Firewall).
**Logic:** Explicitly separates user-narrative (Portfolio) from agent-logic (HomeLabAI) to prevent identity bleed.
**Mechanism:** Refactored system prompts and taxonomy to remove specific professional history anchors (e.g., "18 years", "Silicon Validation") from core cognitive profiles.

## [FEAT-093] Dynamic Environment Portability
**Status:** ACTIVE
**Code:** [src/debug/test_federated_failover.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/test_federated_failover.py#L10) — Dynamic Environment Portability.
**Logic:** Ensures the Lab is not hardcoded to a specific network or hardware set.
**Mechanism:** Dynamic IP resolution (`resolve_ip`) and configuration-driven node affinity (`infrastructure.json`) allowing deployment outside the primary lab.

## [FEAT-094] Lively Room Banter (Handover Fillers)
**Status:** ACTIVE
**Code:** [src/train/distill_training_data.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/train/distill_training_data.py#L24) — Lively Room Banter (Handover Fillers).
**Logic:** Improves perceived responsiveness by having the Gateway (Pinky) provide filler acknowledgments during strategic handovers.
**Mechanism:** Async broadcast of characterful quips (e.g., "Hmm...") immediately after shunting tasks to the Brain.

## [FEAT-105] Multi-Agent Simulation (MAS)
**Status:** ACTIVE
**Code:** [src/debug/atomic_patcher.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/atomic_patcher.py#L56) — Multi-Agent Simulation (MAS).
**Logic:** Treat the Lab as a collaborative session between nodes that coordinate answers in real-time.
**Mechanism:** Combined with [FEAT-094] and [FEAT-108] to simulate inter-agent coordination rather than a linear API flow.

## [FEAT-106] Async Coordination Engine
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L673) — Async Coordination Engine.
**Logic:** Enables Pinky to provide "Thinking Fillers" while the Brain's reasoning cycle is in-flight.
**Mechanism:** Refactored `process_query` to allow asynchronous interjections during the parallel dispatch window.

## [FEAT-108] Inter-Agent Handover Signal
**Status:** ACTIVE
**Code:** [src/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/cognitive_hub.py#L9) — Inter-Agent Handover Signal.
**Logic:** Immediate low-latency trigger from Hub to Brain upon strategic intent detection.
**Mechanism:** Dedicated trigger packet sent to Brain node to initiate a `shallow_quip` while Pinky generates fillers.

## [FEAT-107] System-Agnostic IPC
**Status:** ACTIVE
**Code:** [src/infra/setup_sysrq_earlyoom.sh](https://github.com/kEnder242/HomeLabAI/blob/main/src/infra/setup_sysrq_earlyoom.sh#L65) — System-Agnostic IPC.
**Logic:** Decouples the Lab from hardcoded hostnames or network paths.
**Mechanism:** Generalizing KENDER/localhost resolution via `infrastructure.json` and dynamic DNS fallbacks.

## [FEAT-095] Search Indexing Pipeline (v2.1)
**Status:** ACTIVE
**Code:** [src/debug/simulate_moe_pipeline.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/simulate_moe_pipeline.py#L4) — Search Indexing Pipeline (v2.1).
**Logic:** Automated generation of a flattened keyword-to-ID mapping for lightning-fast static search.
**Mechanism:** `scan_pinky.py` processes raw notes to produce `search_index.json`.

## [FEAT-096] Blue Tree ASCII Navigation (v7.0)
**Status:** ACTIVE
**Code:** [field_notes/timeline.html](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/timeline.html#L1) — Blue Tree ASCII Navigation (v7.0).
**Logic:** A hierarchical, indented directory navigation UI that mimics a terminal-based system administrator experience.
**Mechanism:** Recursive DOM generation in `timeline.html` based on yearly JSON aggregates.

## [FEAT-097] Dynamic Typewriter Rendering
**Status:** ACTIVE
**Code:** [field_notes/intercom_v2.js](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/intercom_v2.js#L1) — Dynamic Typewriter Rendering.
**Logic:** Simulates a "Live AI" feel by rendering text character-by-character inside the tree structure.
**Mechanism:** Custom JavaScript interval loop in `timeline.html` and `intercom_v2.js`.

## [FEAT-098] RAPL-Sim Custom Exporter (v3.0)
**Status:** ACTIVE
**Code:** [monitor/rapl_sim/app.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/monitor/rapl_sim/app.py#L3) — RAPL-Sim Custom Exporter (v3.0).
**Logic:** Translates real hardware telemetry (thermal zones) into simulated power metrics for validation logic testing.
**Mechanism:** Python web server (`monitor/rapl_sim/app.py`) utilizing the `prometheus_client` library.

## [FEAT-099] Grafana Provisioning as Code
**Status:** ACTIVE
**Code:** [field_notes/bench_models.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/bench_models.py#L372) — Grafana Provisioning as Code.
**Logic:** Ensures dashboards are reproducible and version-controlled by defining them in JSON/YAML.
**Mechanism:** Docker volume mounts mapping `./grafana/provisioning` to the Grafana container.

## [FEAT-100] Librarian Heuristic File Classification
**Status:** ACTIVE
**Code:** [field_notes/scan_librarian.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/scan_librarian.py#L1) — Librarian Heuristic File Classification.
**Logic:** Distinguishes between daily logs, reference documents, and strategic summaries using "Deep Sample" body analysis.
**Mechanism:** Heuristic rules engine in `scan_librarian.py`.

## [FEAT-101] Dual-Pipeline Synthesis & Load-Aware Nibbling
**Status:** ACTIVE
**Code:** [field_notes/mass_scan.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/mass_scan.py#L22) — Dual-Pipeline Synthesis & Load-Aware Nibbling.
**Logic:** Delineates on-demand fast finishing scans (`scan_librarian.py`) from continuous slow-burn historical refinement (`mass_scan.py`). Deep multi-epoch synthesis is strictly bound to off-peak 2:00 AM windows (`field-notes-nightly.timer`) via a single-epoch bounded pass (`--once`), preserving full H2 Lean Sleep VRAM hibernation during daytime working hours.
**Mechanism:** `scan_librarian.py` (on-demand fast finishing), `mass_scan.py --once` (single-epoch 2AM timer), `field-notes-nightly.timer` systemd unit.


## [FEAT-102] Nuclear Cache Busting
**Status:** ACTIVE
**Code:** [src/tests/test_live_audio_memory_benchmark.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/test_live_audio_memory_benchmark.py#L7) — Nuclear Cache Busting.
**Logic:** Forces mobile browsers and Cloudflare to bypass stale caches during infrastructure updates.
**Mechanism:** Global versioning via `?v=X.X` query strings and forced timestamp updates in `build_site.py`.

## [FEAT-103] Cynical Ranking Algorithm
**Status:** ACTIVE
**Code:** [field_notes/ai_engine_v2.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/ai_engine_v2.py#L218) — Cynical Ranking Algorithm.
**Logic:** Assigns a 0-4 "Showcase Value" scale to artifacts, with Rank 4 ("Diamond") representing high-value technical gems.
**Mechanism:** AI-driven classification in `scan_artifacts.py` based on technical density and impact.

## [FEAT-104] Research Pipeline Ledger
**Status:** ACTIVE
**Code:** [field_notes/research.html](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/research.html#L1) — Research Pipeline Ledger.
**Logic:** A technical hub mapping ArXiv papers (e.g., TTCS, CLaRa) to specific Lab implementation milestones.
**Mechanism:** `research.html` dashboard tracking the intellectual pedigree of the Bicameral Mind.

## [FEAT-109] Synthesis of Authority
**Status:** ACTIVE
**Code:** [src/legacy_deepagent/original_audio_server.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/legacy_deepagent/original_audio_server.py#L40) — Synthesis of Authority.
**Logic:** Refines Brain's output to prioritize brevity and actionable insights over technical lectures.
**Mechanism:** Refactored `BRAIN_SYSTEM_PROMPT` to enforce "Brevity is Authority" and adaptive depth.

## [FEAT-111] Cognitive Identity Lock
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L17) — Cognitive Identity Lock.
**Logic:** Hardened persona boundaries for failover nodes.
**Mechanism:** Explicit "ANTI-BANTER" and "Laconic Authority" tokens in the `[FAILOVER ARCHITECT]` prompt in `acme_lab.py`.

## [FEAT-112] Sequential Brain Strategy Chain
**Status:** ACTIVE
**Code:** [src/debug/test_live_fire_triage.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/test_live_fire_triage.py#L8) — Sequential Brain Strategy Chain.
**Logic:** Prevents remote engine collisions by serializing "Quip" and "Deep Think" tasks.
**Mechanism:** Async `brain_strategy_chain` in `acme_lab.py` ensures the 4090 handles one reasoning task at a time.

## [FEAT-113] DNS Trap Recovery
**Status:** ACTIVE
**Code:** [src/tests/test_lab_sprint20.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/test_lab_sprint20.py#L71) — DNS Trap Recovery.
**Logic:** Ensures the Lab can recover network pathing to remote hosts without a service restart.
**Mechanism:** Dynamic `resolve_brain_url()` call inside the live health-check loop.

## [FEAT-114] Sovereign Bridge (Handover Context)
**Status:** ACTIVE
**Code:** [src/debug/harness_brain.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/harness_brain.py#L13) — Sovereign Bridge (Handover Context).
**Logic:** Injects the results of the initial "Signal" quip or Hub-level strategic intent into the technical derivation's context window.
**Rationale:** Moves from isolation to "Overhearing." Rigid isolation prevented cross-hemispheric synergy. This feature allows nodes to "overhear" Hub-level strategic intent before generation.
**Mechanism:** Hub injects the results of the Brain's "Strategic Signal" (FEAT-028) directly into Pinky's context window *before* dispatching the final turn. 

## [FEAT-115] The Ultimate Patcher (Soft Fail)
**Status:** ACTIVE
**Code:** [src/nodes/archive_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/archive_node.py#L30) — The Ultimate Patcher (Soft Fail).
**Logic:** Allows surgical, diff-based updates to the workspace with an optional "Soft Fail" lint-gate.
**Mechanism:** `patch_file` tool in `archive_node.py` handles fuzzy matching and optionally persists changes even if `ruff` reports warnings.

## [FEAT-121] Lab Fingerprint (Distributed Tracing)
**Status:** ACTIVE
**Code:** [src/test_lab_integration.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/test_lab_integration.py#L26) — Lab Fingerprint (Distributed Tracing).
**Logic:** Implements a 4-part execution identity `[BOOT_HASH : COMMIT_SHORT : NODE_ROLE : PID]` to eliminate ghost processes and verify sync trust.
**Mechanism:** Dynamic hex hash generation at init and Git short-hash injection into all log streams and heartbeats.

## [FEAT-122] Kernel-Level Visibility (Proc Title)
**Status:** ACTIVE
**Code:** [src/acme_lab.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/acme_lab.py#L8) — Kernel-Level Visibility (Proc Title).
**Logic:** Renames Python processes in `ps`/`htop` to their full Fingerprint using `setproctitle`.
**Mechanism:** `HUB` and `RESIDENT` nodes update their process title at startup to betrayed stale/un-parented zombies.

## [FEAT-117] Multi-Stage Retrieval (Discovery Pattern)
**Status:** DESIGN
**Code:** [src/nodes/archive_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/archive_node.py#L844) — Multi-Stage Retrieval (Discovery Pattern).
**Logic:** Two-stage RAG. Stage 1 (ChromaDB) identifies the anchor; Stage 2 (Filesystem) retrieves the raw JSON truth.
**Hemispheres:** Brain receives raw data for derivation; Pinky receives summaries for contextual banter.

## [FEAT-118] Resonant Oracle (Magic 8-Ball Preambles)
**Status:** ARCHIVED (Superseded by FEAT-414 / FEAT-436 Intent-Preamble Engine)
**Code:** [src/tests/test_sprint51_escapes.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/test_sprint51_escapes.py#L5) — Resonant Oracle (Magic 8-Ball Preambles).
**Logic:** Early V4 dynamic telemetry-weighted preamble picker prototype (`get_oracle_signal()`). Superseded by modern unified Intent-HyDE Pre-Reflection (`FEAT-436`) and MoE+ Preamble streaming (`FEAT-414`).
**Categories:** `RETRIEVING`, `UNCERTAIN`, `VRAM_STRESS`, `HANDSHAKE`.

## [FEAT-119] The Blacklist Law (Process-Strict Lifecycle) [SCAR #3]
**Status:** ACTIVE (V5 Refactor)
**Code:** [src/train/refine_persona.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/train/refine_persona.py#L3) — The Blacklist Law (Process-Strict Lifecycle) [SCAR #3].
**Logic:** Ensures the Lab's physical ports and GPU VRAM are clear before boot by explicitly targeting ONLY processes we own.
**SCAR #3:** Feb 11 "Ghost PID" port contention during marathon reload.
**Purge-Before-Poll Hardening:** Explicitly DEPRECATED `fuser -k`. We now use `pkill -9` targeted strictly at our `setproctitle` hashes (e.g., `acme_foyer_v5`) and the vLLM engine binary. This prevents suicidal client drops (e.g., Gemini CLI crashes) when external processes touch the ports.
**Mechanism:** `ExecStopPost` in `lab-attendant.service`.

## [FEAT-372] Pre-Emptive Sensory Boot
**Status:** ACTIVE
**Code:** [src/tests/test_memory_foil.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/test_memory_foil.py#L20) — Pre-Emptive Sensory Boot.
**Logic:** Loads the NeMo EarNode immediately on Foyer startup and exempts it from hibernation.
**Rationale:** Preserves the ~1.5GB VRAM footprint permanently to eliminate the 45-second latency delay upon waking, ensuring voice interactiveness is instantly available.

## [FEAT-373] Multi-Language Safe-Scalpel (Passive Mode)
**Status:** ACTIVE
**Code:** [field_notes/utils.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/utils.py#L122) — Multi-Language Safe-Scalpel (Passive Mode).
**Logic:** Upgrades `atomic_patcher.py` to support `ruff` for Python and `bash -n` for shell scripts, operating strictly in a *passive* mode.
**Rationale:** Enforces BKM-011 by providing awareness of linting issues without acting as a rigid block to developer velocity. It will always patch, but will warn if linting fails.

## [FEAT-165] Resident Handshake Gate
**Status:** ACTIVE
**Code:** [src/attendant_liveliness.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/attendant_liveliness.py#L105) — Resident Handshake Gate.
**Logic:** Implements a mandatory initialization barrier for Lab residents.
**Why:** The Hub often reports "READY" once the server port is open, but before nodes have finished their internal engine handshake. This causes initial queries to fail or fall back unnecessarily.
**Mechanism:** `acme_lab.py` awaits a "Confirmed Link" signal from all resident nodes before broadcasting the final `ready` status.

## [FEAT-123] The Truth Sentinel (Grounding Hardness)
**Status:** ACTIVE
**Code:** [src/nodes/archive_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/archive_node.py#L1169) — The Truth Sentinel (Grounding Hardness).
**Logic:** Prevents Brain hallucinations when years are empty or invalid by providing a strict "Total Archive Silence" mandate.
**Mechanism:** `process_query` in `acme_lab.py` detects empty RAG history and injects a high-priority "Do NOT invent" constraint.

## [FEAT-125] Smart-Reuse Protocol (Warm Start)
**Status:** ACTIVE
**Code:** [src/test_lab_integration.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/test_lab_integration.py#L10) — Smart-Reuse Protocol (Warm Start).
**Logic:** Accelerates developer velocity by reusing active Lab instances if the code-on-disk matches the code-in-RAM.
**Mechanism:** Handshake status includes `boot_hash` and `git_commit`. Test scripts verify parity and perform a `Neuralyzer` memory wipe before proceeding, bypassing the 30s boot sequence.

## [FEAT-126] Yearly Summary Injection
**Status:** ACTIVE
**Code:** [src/dream_cycle.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/dream_cycle.py#L123) — Yearly Summary Injection.
**Logic:** Automatically includes the high-level yearly summary (e.g., 2023.json) as a reference whenever a year is detected.
**Mechanism:** `ArchiveNode.get_context` checks for the existence of `{year}.json` in the data directory and injects it into the `sources` metadata array.

## [FEAT-127] Cumulative Synthesis (Layered Refinement)
**Status:** ACTIVE
**Code:** [src/nodes/thought_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/thought_node.py#L6) — Cumulative Synthesis (Layered Refinement).
**Logic:** Archive refinement must follow a cumulative pattern where new technical insights are layered onto existing history rather than replacing it.
**Mandate:** A strict semantic de-duplication gate (0.85 similarity) must be enforced within the same calendar day to prevent redundant narratives while ensuring no previous engineering work is lost.
**Mechanism:** `aggregate_years.py` groups monthly JSONs, merges them with existing yearly summaries, and performs cross-file de-duplication. Integrated into `mass_scan.py` lifecycle.

## [FEAT-128] The Strategic Anchor
**Status:** ACTIVE
**Code:** [field_notes/nibble_v2.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/nibble_v2.py#L274) — The Strategic Anchor.
**Logic:** Ingests high-level `META` documents (Insights, Focals) to provide the "Why" behind the "What" for any given year.
**Mechanism:** `scan_librarian.py` classifies target files as `META`. The Nibbler extracts strategic points using the "Expert Career Strategist" prompt, saving them as high-rank `[STRATEGIC_ANCHOR]` events at the top of `YYYY.json` files for UI and RAG prioritization.

## [FEAT-130] Atomic State Updates
**Status:** ACTIVE
**Code:** [field_notes/nibble_v2.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/nibble_v2.py#L384) — Atomic State Updates.
**Logic:** Ensures scanner integrity by only marking a file as "Processed" if the AI worker successfully extracts valid events.
**Mechanism:** `nibble_v2.py` only updates the `chunk_state.json` hash after the `extract_json_from_llm` function returns a non-empty list.

## [FEAT-131] Robust JSON Extraction
**Status:** ACTIVE
**Code:** [field_notes/nibble_v2.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/nibble_v2.py#L121) — Robust JSON Extraction.
**Logic:** Prevents parsing failures caused by LLM conversational filler or Markdown wrapping.
**Mechanism:** Implements a recursive regex-based fallback in `nibble_v2.py` that hunts for `[...]` or `{...}` blocks before attempting `json.loads`.

## [FEAT-129] The Philosophical Core
**Status:** DESIGN
**Code:** [field_notes/nibble_v2.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/nibble_v2.py#L308) — The Philosophical Core.
**Logic:** Explicitly extracts core engineering principles ("Class 1", "Verify over Velocity") from the 2024 Philosophy document.
**Mechanism:** Injected into the Architect Node's system prompt and RAG context to influence the overall personality and decision-making logic of the Lab.

## [FEAT-045] Neural Pager Interactivity (The Status Model)
**Status:** DORMANT (Restoration Active)
**Code:** [src/forge/serial_harvest.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/forge/serial_harvest.py#L47) — Neural Pager Interactivity (The Status Model).
**Logic:** High-fidelity interactive tree for lab alerts using the **Split Status Model**.
**Bifurcation Mandate:** 
1. **Volatile Status (Liveness):** Real-time system health and indicators (e.g. VRAM pressure) retrieved directly from the Lab Attendant API (:9999/heartbeat).
2. **Forensic Ledger (History):** Append-only record (`pager_activity.json`) of all historical alerts.
**Visuals:** Professional color-coding (Red/Orange/Blue) with slide-down terminal effects and simulated console typing.

## [FEAT-078] Neural Trace (Inference Mirror)
**Status:** DORMANT (Restoration Active)
**Code:** [src/nodes/loader.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/loader.py#L806) — Neural Trace (Inference Mirror).
**Logic:** Black-box logging of all inference payloads (System + Prompt + Response) for technical auditability.
**Mechanism:** `_mirror_trace` in `loader.py` persists full JSON payloads to `HomeLabAI/logs/trace_*.json`.

## [FEAT-134] AFK Resource Guard (Autonomous Unload)
**Status:** ACTIVE
**Code:** [src/v5/foyer/router.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/foyer/router.py#L547) — AFK Resource Guard (Autonomous Unload).
**Logic**: Protects GPU resources from idling if the Agent/User session is disconnected or forgotten.
**Mechanism**:
1.  **Default Timeout**: The server enforces an internal 60s inactivity window (overridable via `--afk-timeout`).
2.  **Action**: If no WebSocket traffic is detected, the server SIGTERMs inference engines to free the local GPU for non-AI tasks.
**Verification**: `src/debug/test_sigterm_protocol.py`.

## [FEAT-136] Safe-Pilot Autonomous Ignition [SCAR #4]
**Status:** ACTIVE
**Code:** [src/infra/nightly_forge.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/infra/nightly_forge.py#L5) — Safe-Pilot Autonomous Ignition [SCAR #4].
**Logic**: Enables the Lab to come online automatically after a system reboot without manual operator intervention, while maintaining a safety guard against VRAM collisions.
**SCAR #4:** Mar 2 "Cold Start" misunderstanding / Reboot recovery gap.
**Mechanism**:
1.  **Boot Grace**: A 60s delay post-service-start to bypass I/O storms and ensure Docker daemon stability.
2.  **Telemetry Gate**: Queries VRAM usage; aborts if >1GB is already allocated (assumes external task like Gaming).
3.  **Self-Ignition**: Triggers the `handle_start` sequence for the Unified Base (3B) model if the gate is clear.
**Verification**: Simulated reboot test and VRAM collision test.

## [FEAT-142] Service Quiesce (The Freeze)
**Status:** DESIGN
**Code:** [monitor/notify_gatekeeper.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/monitor/notify_gatekeeper.py#L13) — Service Quiesce (The Freeze).
**Logic:** Native Attendant method to enter a safe maintenance state.
**Mechanism:** `POST /quiesce`. Sets `maintenance.lock`, stops active residents, and reaps all ports.

## [FEAT-143] Command Ignition (Manual Start)
**Status:** DESIGN
**Code:** [src/v5/foyer/router.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/foyer/router.py#L632) — Command Ignition (Manual Start).
**Logic:** Direct API override for the Safe-Pilot sequence.
**Mechanism:** `POST /ignition`. Removes `maintenance.lock` and triggers immediate boot.

## [FEAT-144] Native Health Ping
**Status:** DESIGN
**Code:** [src/start_server_fast.sh](https://github.com/kEnder242/HomeLabAI/blob/main/src/start_server_fast.sh#L7) — Native Health Ping.
**Logic:** Integrated health verification via the Attendant API.
**Mechanism:** `POST /ping`. Triggers internal generation probe and returns token fidelity.

## [FEAT-137] vLLM 0.17.0 Infrastructure
**Status:** ACTIVE
**Code:** [src/start_vllm.sh](https://github.com/kEnder242/HomeLabAI/blob/main/src/start_vllm.sh#L2) — vLLM 0.17.0 Infrastructure.
**Logic**: Establishes a stable environment for vLLM 0.17.0 on Turing (2080 Ti) hardware.
**Mechanism**:
1.  **Venv**: Dedicated environment at `/home/jallred/Dev_Lab/.venv_vllm_017`.
2.  **Models**: Staged in `/speedy/models/` (Qwen2.5-3B-Instruct, Llama-3.2-3B-Instruct-AWQ).
3.  **Tuning**: Optimized via `TRITON_ATTN` and `0.5` utilization characterization.
**Verification**: `src/debug/test_vllm_017_stability.py`.

## [FEAT-145] "Unity" Dispatcher (Hub Logic)
**Status:** ACTIVE
**Code:** [src/acme_lab.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/acme_lab.py#L53) — "Unity" Dispatcher (Hub Logic).
**Logic:** Refactors the communication hub to support addressing specific LoRA adapters within a unified vLLM instance.
**Mechanism:** `loader.py` and `acme_lab.py` include the `lora_name` in the OpenAI completion payload when `lab_mode == "vLLM"`.

## [FEAT-148] SML Fidelity Ladder (Resilience Ladder)
**Status:** ACTIVE
**Code:** [field_notes/data/vram_characterization.json](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/data/vram_characterization.json#L1) — SML Fidelity Ladder (Resilience Ladder).
**Logic:** Implements an abstracted model hierarchy (Small/Medium/Large) to allow the Lab to adapt reasoning depth to available VRAM headroom.
**Mechanism:** 
1. **Characterization**: `vram_characterization.json` maps abstract tiers to physical weight files and utilization targets.
2. **Orchestration**: Lab Attendant executes a `quiesce` -> `start` sequence to swap the "Unity Base" when a tier shift is requested.
3. **Resilience**: Enables "Downshifting" to 1B models during high-concurrency or sensory peaks (EarNode active).
**Note:** SML is the "Tier Swapper" and should not be conflated with [FEAT-030] (Unity), which is the "Shared Foundation" rule.

## [FEAT-149] Resident Heartbeat / Auto-Bounce
**Status:** ACTIVE
**Code:** [src/debug/test_goodnight_bounce.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/test_goodnight_bounce.py#L95) — Resident Heartbeat / Auto-Bounce.
**Logic:** Implements a persistent loop for the communication hub in `SERVICE_UNATTENDED` mode. 
**Behavior**: Detects graceful shutdowns triggered by the `close_lab` tool and automatically restarts the resident boot sequence instead of terminating the process.
**Mechanism**: A `while True` loop wrapping the server execution in `acme_lab.py`.
**Verification**: `src/debug/test_goodnight_bounce.py`.

## [FEAT-151] Unified Trace Monitoring (Forensic Ledger)
**Status:** ACTIVE
**Code:** [src/debug/test_goodnight_bounce.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/test_goodnight_bounce.py#L19) — Unified Trace Monitoring (Forensic Ledger).
**Logic:** Provides "Appliance-Grade" visibility during autonomous transitions by capturing raw log traces directly in the **Forensic Ledger** (`pager_activity.json`).
**Mandate:** All system alerts and deltas are preserved for long-term auditability. The **Atomic File Swap Protocol [BKM-022]** must be used for ledger updates to ensure the integrity of the historical sequence without data loss.
**Mechanism:** `TraceMonitor` utility marks EOF at start and captures only the "Delta" (new lines) if a failure or state transition occurs.
**Verification**: Integrated into `src/debug/test_goodnight_bounce.py`.

## [FEAT-211] Shadow Archivist (Proactive Context Grafting)
**Status:** ACTIVE
**Code:** [src/debug/harness_brain.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/harness_brain.py#L13) — Shadow Archivist (Proactive Context Grafting).
**Logic:** The Shadow Brain acts as the "Proactive Archivist," retrieving relevant historical JSONs/links during the 4090's warm-up period.
**Rationale:** Eliminates "Wait-to-Ask" latency. High-fidelity context is "grafted" onto the Sovereign's derivation before it begins.
**Mechanism:** `cognitive_hub.py` triggers a parallel `archive.get_context` call via the Shadow Brain when strategic intent or years are detected.

## [FEAT-207] Bicameral Airtime (Tricameral Sync)
**Status:** ACTIVE
**Code:** [src/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/cognitive_hub.py#L3) — Bicameral Airtime (Tricameral Sync).
**Logic:** A three-layered response hierarchy (Pinky -> Shadow -> Sovereign) to mask latency and improve accuracy.
**Consolidation:** This feature consolidates and supersedes **[FEAT-004]** (Shadow Dispatch), **[FEAT-172]** (Hemispheric Interjection), and **[FEAT-186]** (Predictive Warm-up).
**Rationale:** To eliminate "Brain Silence" and provide immediate characterful and technical feedback while the primary model processes.
**Mechanism:** `CognitiveHub` parallel dispatch with inter-agent context injection (Neural Resonance).

## [FEAT-004] [CONSOLIDATED] Shadow Dispatch (Predictive Intent)
**Status:** CONSOLIDATED (Mar 2026)
**Code:** [src/debug/simulate_moe_pipeline.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/simulate_moe_pipeline.py#L48) — Shadow Dispatch (Predictive Intent).
**Reason:** Absorbed into [FEAT-207] Tricameral Airtime and [FEAT-211] Shadow Archivist.

## [FEAT-172] [CONSOLIDATED] Hemispheric Interjection (The Active Buffer)
**Status:** CONSOLIDATED (Mar 2026)
**Code:** [src/tests/live_fire_integration.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/live_fire_integration.py#L52) — Hemispheric Interjection (The Active Buffer).
**Reason:** Absorbed into [FEAT-207] Tricameral Airtime.

## [FEAT-186] [CONSOLIDATED] The "Pre-warm" Lobby (Predictive Warm-up)
**Status:** DEFEATURED (Superseded by Systemd Socket Activation & Scale-to-Zero)
**Code:** [src/tests/test_lab_sprint20.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/test_lab_sprint20.py#L73) — The "Pre-warm" Lobby (Predictive Warm-up).
**Reason:** Absorbed and subsequently defeatured to eliminate idle thrashing against the Hibernation Matrix. Replaced by systemd socket activation.

## [FEAT-156] SSE Evolution (Hot Link)
**Status:** ACTIVE
**Code:** [monitor/scan_cloudflare.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/monitor/scan_cloudflare.py#L41) — SSE Evolution (Hot Link).
**Logic:** Implements a Server-Sent Events transport for the Attendant to allow non-TTY remote tool connectivity.
**Rationale:** The original FastMCP implementation required a TTY, which failed inside systemd services. SSE provides a persistent "Hot Link" for the Gemini CLI to stay connected to the active service without spawning redundant processes.
**Mechanism:** `GET /events` endpoint in `lab_attendant_v2.py`.
**High-Fidelity Signal:** Heartbeats include **Live VRAM Characterization**, allowing the Agent to perceive VRAM limits before attempting heavy tool calls.

## [FEAT-157] Hybrid Contextual Unification
**Status:** ACTIVE
**Code:** [field_notes/scan_artifacts.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/scan_artifacts.py#L14) — Hybrid Contextual Unification.
**Logic:** Transitions from weight-based character dependency to prompt-based character injection.
**Rationale:** Removes the "Dependency Fragility" of physical LoRA binary files. If an adapter is missing or a model version changes, the Lab maintains its character through direct context injection. This acts as the "Safety Fallback" for character continuity.
**Mechanism:** Hub injects high-fidelity persona traits directly into the system prompt. 

## [FEAT-158] Grounded Shadow Protocol
**Status:** ACTIVE
**Code:** [src/tests/test_memory_foil.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/test_memory_foil.py#L13) — Grounded Shadow Protocol.
**Logic:** Refactors the Brain-to-Shadow failover from a "Pinky Hallucination" into a "Stoic Shadow" mode.
**Rationale:** Previous failovers led to unhelpful hallucinations. The Stoic Shadow provides clinical, lead-engineer precision when the primary Sovereign is offline.
**Mechanism:** Uses local weights to perform technical derivations with a clinical persona when KENDER is offline.

## [FEAT-160] Pedigree Refinement Pipeline
**Status:** ACTIVE
**Code:** [src/forge/train_expert.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/forge/train_expert.py#L18) — Pedigree Refinement Pipeline.
**Logic:** Automated LoRA "Burn" orchestrator. Physically encodes engineering pedigree into model weights based on Rank 4 "Gems" found in the archive.
**Rationale:** Encodes the 18-year history into the model's neurons, transforming context searching into intuitive neural recall.
**Mechanism:** `src/forge/train_expert.py`. Dynamically preloads `libnvJitLink.so.13` for CUDA 13 / SM 7.5 Unsloth LoRA fine-tuning and integrates with `nightly_forge.py` for autonomous nightly weight induction.

## [FEAT-161] Synthetic Character Distillation
**Status:** ACTIVE
**Code:** [field_notes/mass_scan.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/mass_scan.py#L266) — Synthetic Character Distillation.
**Logic:** Autonomous distillation engine in `mass_scan.py` (Step 6 TLC) that extracts Rank 4/5 gems and standalone code artifacts (`artifacts_*.json`) into bidirectional instruction-tuning pairs in `journal_ledger.jsonl` (593 active pairs). Grounded in GenRead ([arXiv:2209.10063](https://arxiv.org/abs/2209.10063)) and Query2Doc ([arXiv:2303.07678](https://arxiv.org/abs/2303.07678)).
**Rationale:** Transforms terse notes and standalone tools into natural-language training pairs with forward tool inquiries and reverse Jeopardy category searches, eliminating catastrophic forgetting via cumulative full-replay training.
**Mechanism:** `distill_journal_ledger()` in `field_notes/mass_scan.py`, `test_forge_distillation_unit.py`.

## [FEAT-162] Multi-LoRA Cognitive Loadout
**Status:** ACTIVE (Dormant)
**Code:** [src/debug/atomic_patcher.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/atomic_patcher.py#L56) — Multi-LoRA Cognitive Loadout.
**Logic:** Dynamic loading of pedigree-hardened weights at runtime via vLLM.
**Rationale:** vLLM `--enable-lora` allows specific task-adapters (e.g. `pedigree_v2`) to be requested per-query, providing a specialized "Cognitive Loadout" for high-stakes tasks like career strategy.
**Status:** Awaiting `pedigree_v2` weights from Phase 7 burn.

---

## 🎭 THE VIBE LEDGER (Technical Behaviors & Scenarios)
*This section tracks high-level agentic capabilities and interaction scenarios.*

### [VIBE-012] Hemispheric Independence
**Objective:** Maintain unconstrained strategic depth while optimizing resident efficiency.
**Behavior:** The Agent acknowledges the split between Linux residency (Unified model) and Windows sovereignty (typically larger model pre-loaded). No attempts are made to sync or match models across the bridge.

### [VIBE-011] The "Always Ready" Resident (Peer Presence)
**Objective**: Transition the Lab from a "Reactive Service" to a "Resident Peer."
**Logic**: High-availability interaction style where the "Heart" (STT) and "Mind" (Reasoning) are persistent anchors of the environment.
**Behavior**: The system is designed to be "Always On" following a power cycle. If the Agent encounters an offline state, it is treated as an anomaly rather than the default, triggering immediate diagnostic reporting.

### [VIBE-010] The "Diagnostic Partner" Shift (Engine Halt)
**Objective**: Maintain safety and transparency when the physical environment fails.
**Logic**: A persona-level transition triggered by hardware instability or orchestration failure.
**Triggers**:
*   **Zombies**: Orphaned PIDs ignoring `pkill -9`.
*   **OOM**: System-level `OutOfMemoryError` despite orchestration guards.
*   **Driver**: NVIDIA driver communication loss or `nvidia-smi` hangs.
*   **Disk Pressure**: `df -h` reporting >95% usage on `/` or `/home` (rpool pressure).
*   **Orchestration Gap**: Lab Attendant (`:9999`) returning 404, Connection Refused, or timing out.
**Behavior**: The Agent instantly shifts from "Autonomous Execution" to "Diagnostic Reporting." It stops all tool-use, presents the system vitals (PID, VRAM, Disk, Attendant logs), and adopts a "Passive Observer" stance.
**Mandate**: Do not attempt `reboot` or `sudo` cleanup without explicit "Greenlight" from the Lead Engineer.

### [VIBE-001] Tool-First Instinct
**Status:** DESIGN (v4.9)
**Logic:** Prioritizes native MCP tools and established diagnostic scripts over generic shell one-liners.
**Behavior**: Intercepts the "LLM Instinct" to write raw `python -c` or `curl` commands by providing high-signal native interfaces.

### [VIBE-002] Non-Blocking Validation
**Status:** ACTIVE
**Logic:** Mandates the "Trigger-Poll-Observe" pattern for all logic tests.
**Behavior**: Pulse the Lab state (via Attendant), poll the registers (Heartbeat), and observe the evidence (Trace Delta). Never block inside a trigger.

### [VIBE-008] Performance Verbiage (The Privacy Filter)
**Status:** ACTIVE (Modernization Planned Sprint 31)
**Logic:** Automatic redaction of 'Coaching' verbiage from archive synthesis.
**Context:** High-fidelity career documents (Reviews, Insights) contain feedback that should not appear in the technical timeline.
**Refactor Strategy:** Modernize into a high-fidelity "Sanitization Pipeline." It must accurately redact coaching verbiage (e.g., "Jason needs to...") without stripping the technical "Scars" that prove engineering impact. Move beyond basic regex to a robust semantic filter.
**Keywords:**
- **Legacy Headers:** `AREAS FOR IMPROVEMENT/DEVELOPMENT`, `Evaluation: Areas for Development`, `IMPROVEMENT/DEVELOPMENT AREAS`.
- **Modern Headers:** `Results Coaching`, `Behaviors Coaching`, `Coach`, `Growth`, `Behaviors Feedback`, `Priorities for [YYYY]`.
- **Grammatical Patterns:** `Jason should`, `Jason needs to`, `Should have been communicated`, `missed on this opportunity`.
**Rule:** Synthesis engines MUST treat text following these markers as **Private/Instructional** and exclude it from the public `YYYY.json` event stream.

### [VIBE-007] The "Validation Journal" Pattern
**Structure:**
- **Order:** Latest-First (Reverse Chronological).
- **Head:** Temporary TODOs, lists, and active "Today" buffers.
- **Section Dividers:** Heavy ASCII lines (`=======` or `-------`).
- **Anchors:** `[ctrl-F10 s]` reminder usually signals the start of the "DONE" or "Today" event block.
- **Bulk:** Daily dated entries (M/D/YYYY) containing technical evidence.
- **Tail:** Stale TODO lists and a "Contacts" directory.
**Archaeology (Pre-2008 Outliers):**
- **Fuzzy Chronology:** Early files (e.g., `notes_2005.txt`, `ras-viral.txt`) lack regular timestamps. Dates must be gleaned from surrounding context or header markers.
- **Role Alignment:** "Year" notes often span multiple years, correlating with career roles (EPSD, DSD, MVE, PAE, PIAV). (This alignment is saved and tracked in file_manifest.json)
- **Team Tags:** Acronyms in filenames (DSD, MVE, PIAV) correspond to specific engineering teams and should be preserved as high-fidelity metadata.
**Constraint:** Classification MUST skip the head/tail noise and focus on the ASCII-delimited middle bulk to verify "LOG" status.

### [VIBE-004] Internal Debate (Peer Review)
**Logic:** The scenario where Pinky and the Brain "duel" over a technical risk to reach a moderated consensus.

### [VIBE-005] Subconscious Dreaming
**Logic:** The automated background cycle that transforms chaotic raw logs into "Diamond Wisdom" abstracts.

## [FEAT-088] Nightly Recruiter (Target Acquisition)
**Status:** ACTIVE
**Code:** [src/nodes/archive_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/archive_node.py#L879) — Nightly Recruiter (Target Acquisition).
**Logic:** Autonomous background worker that retrieves 3x3 CVT context from the Archive Node and tasks the Brain with agentic job searching via `deep_think`. 
**Verification:** Confirmed via `test_recruiter.py` with mock job identification.

## [FEAT-095] Public Research Ledger (Static Airlock)
**Status:** COMPLETE
**Code:** [field_notes/research_build.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/research_build.py#L3) — Public Research Ledger (Static Airlock).
**Logic:** Sanitize the internal `research.html` for public deployment by stripping Zero Trust dependencies and inlining high-density CSS.
**Artifacts:** `www_deploy/research.html`, `www_deploy/sync_research.sh`, and `assets/research_snapshot.png`.

## [LAW-021] Hardware Verification Law (The "Wall" Audit)
**Status:** ACTIVE
**Logic:** Mandatory gate for inference engine changes. Requiring 100% stable `POST /ping` heartbeat verification of the **333MiB Breakthrough** (Turing VRAM threshold).
**Pedigree:** Anchored in **[ENGINEERING_PEDIGREE.md](../HomeLabAI/docs/ENGINEERING_PEDIGREE.md)**.

## [FEAT-171] Intelligent Lifecycle Matrix (Disconnect vs. Close)
**Status:** DESIGN
**Code:** [src/test_lab_integration.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/test_lab_integration.py#L9) — Intelligent Lifecycle Matrix (Disconnect vs. Close).
**Logic:** Context-aware lifecycle management distinguishing between passive network events and explicit tool triggers.
**Rationale:** To ensure debug sessions clean up properly on exit without interrupting persistent background operations (Dreaming/Recruiter).

| Trigger | Mode | Action |
| :--- | :--- | :--- |
| **Socket Disconnect** | Debug / Co-Pilot | **Graceful Shutdown**: Start 5-minute idle timer. If no client reconnects, execute full cleanup. |
| **Socket Disconnect** | `SERVICE_UNATTENDED` | **Ignore**: Lab remains resident in VRAM for background tasks. |
| **`close_lab`** (Tool) | Debug / Co-Pilot | **Immediate Exit**: Terminate process and return control to the Gemini CLI. |
| **`close_lab`** (Tool) | `SERVICE_UNATTENDED` | **Bounce**: Shutdown nodes and trigger autonomous re-ignition (engine refresh). |

## [FEAT-172] Hemispheric Interjection (The Active Buffer)
**Status:** DESIGN
**Code:** [src/tests/live_fire_integration.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/live_fire_integration.py#L52) — Hemispheric Interjection (The Active Buffer).
**Logic:** Transforms the Gateway (Pinky) from a reactive narrator into an active co-processor that manages the "Latency Gap" between human intent and Brain latency.
**Rationale:** To eliminate "Brain Silence" and improve technical accuracy by identifying gaps in queries before the deep reasoning cycle finishes.
**Mechanisms:**
1.  **The Lag Shield**: Pinky perceives the `deep_think` state and provides strategic fillers or status updates (e.g., "The Brain is chewing on the 580 driver logs, but Narf! Did you include the `dmesg` output?") to maintain engagement.
2.  **Pre-emptive Probing**: Parallel pass where Pinky identifies missing technical parameters (IPs, versions, hardware IDs) and asks for them *while* the Brain is generating.
3.  **Organic Interrupt**: Ability for Pinky to broadcast a `[HALT]` signal if she detects a "Hardware Reality" conflict (e.g., thermals or VRAM limits) that invalidates the Brain's current derivation.
4.  **Context Hot-Plugging**: Injects user's intermediate answers into the Brain's active context window to steer generation mid-flight.

## [FEAT-173] Agentic Backtracking (Autonomous Exploration)
**Status:** DESIGN
**Code:** [src/tests/live_fire_integration.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/live_fire_integration.py#L56) — Agentic Backtracking (Autonomous Exploration).
**Logic:** Implements the AT2QA (arXiv:2603.01853) pattern of decoupling agents from rigid retrieval workflows in favor of iterative tool-decision agency.
**Rationale:** To solve the "Search Trap" where a single thin tool-result leads to reasoning failure or hallucination.
**Mechanism:** 
1.  **Post-Tool Evaluation**: After a tool call (e.g. `ArchiveNode.get_context`), the node performs a high-speed self-evaluation of the data fidelity.
2.  **Strategic Pivot**: If results are "Thin" or temporally inconsistent, the node autonomously triggers a follow-up query with refined parameters (e.g., widening the date range or shifting from "Log" to "Focal" metadata) without user prompting.
3.  **Agency over Workflow**: The node is granted the authority to "Backtrack" up to 3 times before providing a final derivation to the user.

## [FEAT-174] Multi-LoRA Expert Routing (Poor Man's MoE)
**Status:** ACTIVE
**Code:** [src/debug/atomic_patcher.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/atomic_patcher.py#L56) — Multi-LoRA Expert Routing (Poor Man's MoE).
**Logic:** Applies Mixture-of-Experts (MoE) architectural lessons to a Multi-LoRA environment on small resident models (3B).
**Rationale:** To achieve "Ultimate Expert Specialization" (DeepSeekMoE) without the VRAM penalty of a 14B+ model. 
**Mechanisms:**
1.  **The "Pre-Gated" Pass**: The Cognitive Hub acts as the "Router," identifying the task domain before the inference call and selecting the corresponding specialized LoRA "glasses."
2.  **Fine-Grained Adapters**: Replaces monolithic personas with tiny, high-density domain experts (e.g. `telemetry_v1`, `security_v1`, `recruiter_v1`) trained via Unsloth.
3.  **Adaptive Residency**: Leverages vLLM's ability to keep the base weights fixed while hot-swapping or layering adapters in milliseconds.
**Theoretical Anchor:** [ARX-2401.06066], [ARX-2402.07033].

---

## [TECHNICAL DEBT]
- **[DEBT-001] Shadow Moat (Narf Scrub):** Current implementation uses regex sanitization to strip Pinky-isms from Brain sources. This is a functional "hack."
    *   *Stable Solution Task:* Move to explicit negative constraint fine-tuning or 1B-model tone verification.

## [FEAT-180] Tiered Resource Governance (The Resilience Ladder)
**Status:** ACTIVE (REFINED)
**Code:** [src/infra/atomic_io.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/infra/atomic_io.py#L8) — Tiered Resource Governance (The Resilience Ladder).
**Logic:** Replaces the monolithic Hard Stop with a multi-stage degradation hierarchy to maintain Lab availability during moderate hardware pressure.
**Rationale:** Fallbacks introduce "Logic Drift," but a total shutdown is the final resort. Tiered governance ensures the Lab only dies when hardware integrity is at true risk.
**Tiered Hierarchy:**
1. **Tier 1 (vLLM):** Primary high-throughput mode.
2. **Tier 2 (Ollama Fallback):** Auto-restart into Ollama with a 1B/3B model if VRAM pressure is >85% but <95%.
3. **Tier 3 (Hard Stop):** SIGTERM only when VRAM > 98% or load > 12.0.
**Mechanism:** 'lab_attendant_v2.py' monitor loop triggers state-transitions or 'SIGTERM' based on thresholds. Uses the **Atomic File Swap Protocol [BKM-022]** for all status and ledger updates.

## [FEAT-181] Behavioral DNA Registry (ChromaDB Bones)
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L194) — Behavioral DNA Registry (ChromaDB Bones).
**Logic:** Replaces static intent mapping with a vector-driven 'Vibe' retrieval system.
**Rationale:** To comply with [BKM-015.1]. Eliminates hardcoded keyword-to-expert mapping, allowing the Lab's orchestration to evolve semantically as new expertise is added to the archive.
**Mechanism:** New 'behavioral_dna' collection in ChromaDB queried by the Cognitive Hub during the pre-gating phase.

## [FEAT-182] Neural Resonance (Strategic Interjection)
**Status:** ACTIVE
**Code:** [src/debug/test_pi_flow.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/test_pi_flow.py#L11) — Neural Resonance (Strategic Interjection).
**Logic:** Implements true 'overhearing' synergy using the [FEAT-172] Active Buffer mechanism.
**Rationale:** Eliminates the 'Hollow Echo Chamber' by ensuring Pinky's initial intuition informs the Brain's deep reasoning chain in real-time.
**Mechanism:** Injects a [PINKY_HEARING] block into the Brain's context window containing the results of the triage facilitate task.

## [FEAT-183] CLaRa-Based Continuous Refinement
**Status:** ACTIVE
**Code:** [src/nodes/archive_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/archive_node.py#L1358) — CLaRa-Based Continuous Refinement.
**Logic:** Applies Continual Learning and Retrospective Analysis to behavioral anchors.
**Rationale:** Ensures the 'Tendons' (Vibes) of the system strengthen based on real-world interaction success rather than manual developer tuning.
**Mechanism:** Post-session audit task where the Lab Actor audits the 'Vibe' success and generates new anchors.

## [FEAT-184] The "Amygdala" Weight (Sentinel v2.1)
**Status:** ACTIVE
**Code:** [src/tests/test_memory_architecture.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/test_memory_architecture.py#L10) — The "Amygdala" Weight (Sentinel v2.1).
**Logic:** Refines the sentinel from a keyword list into a true "Uncertainty Gate."
**Rationale:** Keyword sentinels are too rigid. A logic-based check can decide if the Brain needs to interject based on the complexity or inconsistency of the query.
**Mechanism:** `cognitive_hub.py` Uncertainty Gate reflex plumbed into the triage layer.

## [FEAT-185] Alluring Instrumentation (Juicy Tooling)
**Status:** DESIGN
**Code:** [src/nodes/thought_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/thought_node.py#L9) — Alluring Instrumentation (Juicy Tooling).
**Logic:** Refactors tool descriptions to be highly enticing and precise for agentic reasoning.
**Rationale:** If tool descriptions sound like high-precision instruments of truth, the LLM is statistically more likely to reach for them during complex reasoning.
**Mechanism:** Applying 'The Strategic Architect's Scalpel' terminology across the toolset.

## [FEAT-186] The "Pre-warm" Lobby (Predictive Warm-up)
**Status:** DEFEATURED (Superseded by Systemd Socket Activation & Scale-to-Zero)
**Code:** [src/tests/test_lab_sprint20.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/test_lab_sprint20.py#L73) — The "Pre-warm" Lobby (Predictive Warm-up).
**Logic:** Implemented predictive Brain loading during Pinky triage. Defeatured because aggressive pre-warming constantly fought and broke the Hibernation Matrix idle windows. Replaced by clean systemd socket activation.

## [FEAT-187] CLaRa Model Re-training (Unified 3B Refinement)
**Status:** DESIGN
**Code:** [src/debug/harness_prompt_iteration.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/harness_prompt_iteration.py#L9) — CLaRa Model Re-training (Unified 3B Refinement).
**Logic:** Fine-tunes the Unified 3B Base (Llama 3.2) using "Synergy Pairs" from interaction logs.
**Rationale:** Moves beyond prompt injection to make "Neural Resonance" a native behavior of the resident nodes.
**Mechanism:** Utilizes the [FORGE-01] infrastructure to train on processed conversation turns where Pinky/Brain cooperation was successful.

## [FEAT-188] Resonant Memory (Bicameral Momentum)
**Status:** ACTIVE
**Code:** [src/tests/test_live_audio_memory_benchmark.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/test_live_audio_memory_benchmark.py#L3) — Resonant Memory (Bicameral Momentum).
**Logic:** Expands the 'Overhearing' mechanism from a single-turn injection to a multi-turn semantic buffer.
**Rationale:** To build behavioral momentum. The Brain should 'overhear' not just the immediate triage intuition, but the evolution of Pinky's sentiment over the last 3 interactions.
**Mechanism:** CognitiveHub maintains a 3-turn buffer of Pinky's triage results and injects them as a [RESONANT_HISTORY] block.

## [FEAT-189] Vibe-Driven Tool Pruning
**Status:** ACTIVE
**Code:** [src/forge/generate_sentinel_curriculum.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/forge/generate_sentinel_curriculum.py#L34) — Vibe-Driven Tool Pruning.
**Logic:** Dynamically filters the Brain's available MCP toolset based on the Hub's Vibe Check.
**Rationale:** Reduces the 'Hallucination Surface Area.' If the vibe is 'Tactical,' the Brain should only see high-precision diagnostic tools, preventing it from reaching for broad archival tools unnecessarily.
**Mechanism:** Hub generates a 'tool_allowlist' based on the retrieved vibe metadata.

## [FEAT-190] Cognitive Audit (The Judge)
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L225) — Cognitive Audit (The Judge).
**Logic:** Automated test and runtime validation using a logic-based auditor routine.
**Rationale:** To break the 'Waffle Trap' of hardcoded string matching. Replaces length-based heuristics in the Fidelity Gate with semantic judgment.
**Mechanism:** Uses the **Lab Node Sentinel** (via residents['architect'] or residents['pinky'] LoRA) to judge the technical consistency and 'Vibe' of an output.
**Verification:** Hub calls 'src/infra/cognitive_audit.py' during the Fidelity Gate check.


## [FEAT-191] Judicial Feedback Loop (The Audit)
**Status:** ACTIVE
**Code:** [src/nodes/archive_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/archive_node.py#L1214) — Judicial Feedback Loop (The Audit).
**Logic:** Integrate the 'CognitiveAudit' routine into the nightly 'dream_cycle.py' process.
**Rationale:** To perform autonomous self-correction on synthetic memories. Synthetic wisdom is peer-audited for technical accuracy before being committed to long-term memory.

## [FEAT-195] Archival Topography Injection
**Status:** ACTIVE
**Code:** [src/nodes/archive_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/archive_node.py#L1389) — Archival Topography Injection.
**Logic:** Provides the Brain with a topographical view of the 18-year archive to enable multi-hop chronological retrieval.
**Rationale:** Solves the 'Granularity Gap' where nodes only receive small portions of files. By knowing the archive's structure (The Map), the Brain can request specific 'Deep Samples' or date ranges.
**Mechanisms:**
1.  **peek_strategic_map**: Tool allowing the Brain to see which years/themes contain the most evidence.
2.  **read_chronological_excerpts**: Tool for requesting full JSON logs for specific months/years.
3.  **Map Injection**: Automated Hub-level context injection of the semantic map during Forensic vibes.

## [FEAT-196] Multi-Hop Archival Reasoning
**Status:** ACTIVE
**Code:** [src/nodes/brain_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/brain_node.py#L52) — Multi-Hop Archival Reasoning.
**Logic:** Enables the Brain node to use archival topography tools as proxies to navigate multiple years autonomously.
**Rationale:** To empower the Sovereign Brain to connect historical breadcrumbs across large temporal gaps without user re-prompting.
**Mechanism:** BrainNode proxy methods for 'peek_strategic_map' and 'read_chronological_excerpts'.

## [FEAT-197] Sequential Thinking (The Chain)
**Status:** ACTIVE
**Code:** [src/nodes/thinking_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/thinking_node.py#L18) — Sequential Thinking (The Chain).
**Logic:** Provides structured, multi-step reasoning blocks to Pinky and the Shadow Brain.
**Rationale:** Prevents logic-drift during complex derivations by forcing the LLM to commit to intermediate steps before generating a final answer.
**Mechanism:** `thinking_node.py` resident providing the `sequential_thinking` tool.

## [FEAT-199] Hub-Level CORS Support
**Status:** ACTIVE
**Code:** [src/test_liger.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/test_liger.py#L5) — Hub-Level CORS Support.
**Logic:** Implements 'aiohttp_cors' in 'acme_lab.py' to allow cross-origin WebSocket handshakes.
**Rationale:** Necessary for browser-based Intercom access when the UI is served via a different port (e.g., 9001) or hostname.
**Mechanism:** CORS configuration in Hub's 'run' loop allowing all origins by default.

## [FEAT-198] Safe-Scalpel (Surgical MCP Tool)
**Status:** ACTIVE
**Code:** [src/debug/system_scalpel.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/system_scalpel.py#L6) — Safe-Scalpel (Surgical MCP Tool).
**Logic:** A system-level MCP server providing the `safe_scalpel` tool for lint-gated code patching directly to the Gemini CLI.
**Rationale:** Promotes the surgical patching logic from a "resident" tool to a first-class system capability. Ensures exactly-once replacement and provides detailed linting feedback (Ruff/ESLint).
**Mechanism:** `system_scalpel.py` standalone MCP server registered in `settings.json`.

## [FEAT-200] UI Debug Visibility
**Status:** ACTIVE
**Code:** [src/tests/test_relay_interest_buildup.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/test_relay_interest_buildup.py#L7) — UI Debug Visibility.
**Logic:** Injects comprehensive packet logging into the Intercom UI.
**Rationale:** To provide the Lead Engineer with real-time visibility into Hub-to-UI data flow, facilitating rapid forensic diagnostics of connection or routing issues.
**Mechanism:** 'console.log("[WS RECV]", data)' in 'intercom_v2.js'.

## [FEAT-201] Neural Shock (Negative Feedback Loop)
**Status:** ACTIVE
**Code:** [src/behavior_test.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/behavior_test.py#L15) — Neural Shock (Negative Feedback Loop).
**Logic:** Replaces extreme shutdowns with a logic-based "Shock" to the LLM when it hallucinations a tool.
**Rationale:** Halts logic-drift without killing the session. Provides a negative penalty header forcing the node to re-derive its reasoning.
**Mechanism:** `[SYSTEM_SHOCK]` interjection re-injected into the query context on tool-execution error.

## [FEAT-202] Decoupled Extraction Pipeline
**Status:** ACTIVE
**Code:** [src/forge/deep_connect_epoch_v2.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/forge/deep_connect_epoch_v2.py#L6) — Decoupled Extraction Pipeline.
**Logic:** Bifurcates the "Deep-Connect" epoch into two stages: 1) Raw Asynchronous Capture and 2) Offline Surgical Refinement.
**Rationale:** Eliminates the "Thrash and Wait" cycle. High-latency LLM calls are captured into a persistent buffer (`raw_stage_1.jsonl`) regardless of parsing success, allowing for iterative regex refinement without re-running inference.
**Mechanism:** `deep_connect_epoch_v2.py` performs raw logging; `refine_bones.py` performs the nuclear parsing pass.

## [FEAT-203] Bicameral Bridge: Neural Signal Extraction
**Status:** ACTIVE
**Code:** [src/forge/refine_bones.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/forge/refine_bones.py#L39) — Bicameral Bridge: Neural Signal Extraction.
**Logic:** Hardens the Hub's parsing layer (The Corpus Callosum) using recursive regex and hybrid (Pipe/JSON) triage recognition.
**Rationale:** 3B models frequently output artifacts under pressure. This refactor ensures signal-to-noise integrity across the bridge.
**Mechanism:** `bridge_signal_clean` utility and hybrid triage loop in `cognitive_hub.py`.

## [FEAT-204] CLI Persona Induction
**Status:** ACTIVE
**Code:** [src/forge/dedupe_prompts.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/forge/dedupe_prompts.py#L6) — CLI Persona Induction.
**Logic:** Aggregates multi-year Gemini CLI prompt history into a consolidated manifest, refined by length gates, debug noise removal, and semantic de-duplication (85% threshold).
**Rationale:** Enables the creation of a "User Voice" LoRA adapter, allowing the Lab to predictively align with the engineer's technical tone and directive style.
**Mechanism:** `extract_gemini_prompts.py` -> `refine_prompts.py` -> `dedupe_prompts.py` (4,410 unique entries).

## [FEAT-208] Manifest Authority
**Status:** ACTIVE
**Code:** [src/forge/dedupe_prompts.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/forge/dedupe_prompts.py#L8) — Manifest Authority.
**Logic:** Links the extraction harvester to the Librarian's `file_manifest.json` for dynamic source file resolution.
**Rationale:** Eliminates hardcoded log mappings. Ensures that new files categorized by the Librarian are immediately accessible to the Bridge.
**Mechanism:** `serial_harvest_v2.py` performs a real-time year/type lookup against the manifest.

## [FEAT-209] Double-Tap Search Pattern
**Status:** ACTIVE
**Code:** [src/behavior_test.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/behavior_test.py#L25) — Double-Tap Search Pattern.
**Logic:** Implements redundant archival searching by querying both the raw daily log (`type:LOG`) and the distilled review/resume (`type:META`) for a given artifact year.
**Rationale:** Maximizes technical block yield. If a detail is missing from the chronological log, the high-level performance review often contains the "Physical Truth."
**Mechanism:** Sequential multi-file loop in `serial_harvest_v2.py` for every identified gem.

## [FEAT-210] Lifecycle Gauntlet (Shakedown Protocol)
**Status:** ACTIVE
**Code:** [src/nodes/loader.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/loader.py#L83) — Lifecycle Gauntlet (Shakedown Protocol).
**Logic:** A rapid-verification script that executes a 1-sample pass of the entire 01:00 AM - 04:00 AM automation sequence.
**Rationale:** To provide the Lead Engineer with high-confidence verification of the Lab's "Tendons" (Dreaming, Harvesting, Mapping, Dialogue) before concluding a session.
**Mechanism:** `lifecycle_gauntlet.py` script shunting 1-gem/1-prompt batches through the pipeline.

## [FEAT-240] Native MCP Relay (Sampling Bridge)
**Status:** DESIGN
**Code:** [src/nodes/brain_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/brain_node.py#L70) — Native MCP Relay (Sampling Bridge).
**Logic:** Moves from custom tool wrappers (`facilitate`) to the standard `mcp.sampling.createMessage` protocol.
**Mechanism:** The Hub acts as a Stateful Host, providing steering tools to nodes via the Sampling context and relaying their intents as visible events.

---

### [VIBE-006] Neural Resonance (The Overhearing)
**Logic:** Transforms the Hub into a "Corpus Callosum" that bridges Pinky's fast intuition with the Brain's deep derivation.
**Rationale:** Eliminates "Hollow Parallelism." Pinky acts as the "gut instinct" that the Brain can validate or override.
**Vibe:** Emergent Synergy.

### [VIBE-013] Sequential Blending (The Fuel Travel Model)
**Status:** ACTIVE (Modernization Planned Sprint 31)
**Logic:** Prioritize context density over raw parallel speed. 
**Sequence:**
1.  **Lab Node (Sentinel)**: Performs Triage & Domain routing.
2.  **Pinky (Reflex)**: Provides situational interjection (Visible).
3.  **Shadow Brain (Archivist)**: Provides technical intuition + Proactive RAG Context (Visible).
4.  **Sovereign Brain (Architect)**: Receives the "Blended" history of the previous three turns to produce the definitive synthesis (Visible).
**Rationale:** The "Fuel Travel" model mandates that every node that consumes fuel and produces a thought **must** be visible in the Intercom. You should see the triage framing, the technical guess, and the final grounded synthesis as a sequential "Waterfall."
**Refactor Strategy:** Address visual jitter. Refactor the Intercom's "Thought Pop" logic to ensure the sequential waterfall feels fluid rather than a series of abrupt updates.

---
**DEFEATURED REASONING (Mar 2026):**
- **[VIBE-014]**: Redundant. The user prefers a "Live Chamber" where all intuition turns are visible during the 4090 grind.
- **[FEAT-083] & [FEAT-085]**: Redundant following the consolidation of the Unified 3B resident base and Attendant-led Safe-Pilot [FEAT-136] sequences.

## [FEAT-213] Autonomous Forge (VRAM Handover)
**Status:** ACTIVE
**Code:** [src/infra/nightly_forge.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/infra/nightly_forge.py#L67) — Autonomous Forge (VRAM Handover).
**Logic:** REST-driven VRAM Handover in `nightly_forge.py` that sends `POST /release_nodes` and `POST /shutdown` to Foyer (port 8765) to evict resident models and reclaim VRAM down to 620MB, executes Unsloth LoRA training on the local GPU, and re-ignites the lab via `POST /wake` and `POST /status_update {"state": "OPERATIONAL"}`.
**Mechanism:** `src/infra/nightly_forge.py`, Foyer REST endpoints (`/release_nodes`, `/shutdown`, `/wake`, `/status_update`).

## [FEAT-214] Parameterized Nightly Forge
**Status:** ACTIVE
**Code:** [src/forge/train_expert.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/forge/train_expert.py#L130) — Parameterized Nightly Forge.
**Logic:** Updates `train_expert.py` to support `--steps`, `--dataset`, and `--output` CLI flags with dynamic base-model resolution from `infrastructure.json`, enabling autonomous and on-demand fine-tuning cycles.
**Mechanism:** `src/forge/train_expert.py` CLI argument parsing and model auto-detection.

## [FEAT-219] Service Handshake (Hardened Gate)
**Status:** ACTIVE
**Code:** [src/dream_cycle.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/dream_cycle.py#L18) — Service Handshake (Hardened Gate).
**Logic:** UI sends a key extracted from the style.css cache-busting hash; Attendant validates via middleware.
**Mechanism:** 'key_middleware' in 'lab_attendant_v3.py' supports Header (X-Lab-Key) or Query Param (?key=).

## [FEAT-220] Diplomatic Immunity Protocol
**Status:** DEFEATURED (Superseded by Systemd CGroup Memory Limits)
**Code:** [src/nodes/loader.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/loader.py#L61) — Diplomatic Immunity Protocol.
**Goal:** Prevented Attendant suicide loops during V4 PGID process reclamation. Defeatured in V5 by moving process management into single-user SystemD cgroups (`50-MemoryMax.conf`).

## [FEAT-221] Crosstalk Status Line
**Status:** ACTIVE
**Code:** [field_notes/utils.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/utils.py#L32) — Crosstalk Status Line.
**Logic:** Offloads inter-agent "thinking" banter from the primary Pinky console to a dedicated 1-line status bar.
**Mechanism:** 
1.  'intercom_v2.js' intercepts 'crosstalk' packets and updates the '#crosstalk-bar' element.
2.  Mobile UI hides the resizer bar to make room for the status line above input.
3.  'cognitive_hub.py' tick rate reduced to 10-15s intervals.

## [FEAT-222] Cognitive De-Warping (Source-First Routing)
**Status:** ACTIVE
**Code:** [field_notes/build_site.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/build_site.py#L140) — Cognitive De-Warping (Source-First Routing).
**Logic:** Prioritizes Source (Brain/Pinky) for panel routing. Removes yellow internal aesthetics.
**Mechanism:** 
1. 'intercom_v2.js' routes all BRAIN packets to Right, PINKY packets to Left.
2. All interim 'Thinking...' tics are shunted to the technical ledger.
3. Clean, high-density clinical log view.

## [FEAT-223] Global Error Sentry
**Status:** ACTIVE
**Code:** [field_notes/script.js](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/script.js#L1) — Global Error Sentry.
**Logic:** Prevents "Silent Death" of the UI by catching syntax and runtime errors before scripts load.
**Mechanism:** 
1. Inline script in <head> hooks window.onerror and unhandledrejection.
2. Surfaces critical failures as high-visibility red blocks directly in the console ledger.

## [FEAT-233] Inter-Node Waterfall (Buffered Streaming)
**Status:** ACTIVE 
**Code:** [src/nodes/loader.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/loader.py#L169) — Inter-Node Waterfall (Buffered Streaming).
**Logic:** Transition from turn-based handovers to real-time, buffered token streaming between nodes.
**Mechanism:** 
1. `CognitiveHub` extracts tokens mid-stream.
2. Tokens are buffered in 100ms chunks before hitting the websocket (The Token Batching Victory), solving UI jitter during long reasoning chains.

## [FEAT-234] Pure Scalar Fuel (Multiplicative Orchestration)
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L944) — Pure Scalar Fuel (Multiplicative Orchestration).
**Logic:** Replaces binary triage with a balanced importance function: `Fuel = ((1.0 - casual) * (intrigue + importance)) / 2`.
**Mechanism:** 
1. Lab Node outputs high-fidelity scalar scores for topic and importance.
2. Routing depth (Shadow vs. Brain) is governed solely by the calculated Fuel thresholds (0.2 / 0.6).

## [FEAT-235] Operational Shortcut (Direct Execution)
**Status:** ACTIVE
**Code:** [src/dream_cycle.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/dream_cycle.py#L41) — Operational Shortcut (Direct Execution).
**Logic:** Bypasses the parallel relay for system-level commands to save VRAM and latency.
**Mechanism:** 
1. Hub intercepts `OPERATIONAL` intent from the Lab Node stream.
2. Immediately triggers the target tool (e.g. Close/Restart) via a fast Pinky-facilitated quip.

## [FEAT-228] Agnostic Context Engine (get_context)
**Status:** PLANNED
**Code:** [field_notes/evaluate_rag.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/evaluate_rag.py#L5) — Agnostic Context Engine (get_context).
**Goal:** Decouple "Historical Pedigree" from core Lab logic.
**Mechanism:** 
1. A standalone tool that fetches evidence based on a semantic axis (Year, Topic, Device).
2. Allows the Lab to map against any database without conflating the data with the Lab's identity.

## [FEAT-236] Relay Route Awareness
**Status:** ACTIVE
**Code:** [src/tests/test_routing_logic.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/test_routing_logic.py#L18) — Relay Route Awareness.
**Logic:** Injects situational "Route Data" (Role, Fuel, Destination) into node context windows to prevent hemispheric identity bleed.
**Rationale:** Prevents small models from "Roleplaying" other nodes (e.g., Pinky calculating Pi). Nodes become aware of their specific duty in the current turn sequence.
**Mechanisms:**
1.  **Role Injection**: Hub tags Pinky as [MODE: FRAME_ONLY] if high fuel is detected.
2.  **Fuel Awareness**: Shadow receives the raw fuel scalar to determine technical verbosity.
3.  **Route Awareness**: Nodes receive a [ROUTE] block indicating which nodes have already fired or are upcoming.
**Related Features:** [FEAT-233] (Waterfall), [FEAT-234] (Scalar Fuel), [FEAT-111] (Identity Lock).

## [FEAT-238] Council of Hemispheres (Peer Vote)
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L549) — Council of Hemispheres (Peer Vote).
**Logic:** Enables mid-relay adjustment of the turn's importance level based on node-level reasoning.
**Rationale:** The Lab Node may under-estimate a query (e.g. Pi as general knowledge). This feature allows Pinky to "Pull the Alarm" by recommending a fuel boost, or "Demote" a turn if she detects it's a joke or mistake.
**Mechanism:** `CognitiveHub` parses explicit steering signals from node responses and updates the session's fuel state before the Sovereign Brain check.

## [FEAT-239] Neural Action Tags
**Status:** ACTIVE
**Code:** [field_notes/scan_librarian.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/scan_librarian.py#L142) — Neural Action Tags.
**Logic:** Uses natural language interjections like [ACTION: UPLINK] or [ACTION: THINK MORE] at the end of persona responses to provide relay hints.
**Rationale:** Replaces brittle JSON tool-calling for steering. Pinky can maintain her voice while still "Handwaving" to her smarter friend (Brain).
**Mechanism:** Hub uses regex to extract and strip tags, adding scalar "Hints" (+0.3 fuel) to the relay baseline.

## [FEAT-240] Native MCP Sampling Bridge
**Status:** ACTIVE
**Code:** [src/nodes/brain_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/brain_node.py#L70) — Native MCP Sampling Bridge.
**Logic:** Transition from turn-based handovers to standard MCP sampling requests.
**Mechanism:** `residents["pinky"].create_message(query, tools=[ask_brain])`.

## [FEAT-242.1] Handshake Tic
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L483) — Handshake Tic.
**Logic:** Mid-stream Crosstalk status updates to mask node transport latency.
**Mechanism:** 'cognitive_hub.py' broadcasts crosstalk packets signaling node activation.

## [FEAT-244] Speaker Masking
**Status:** ACTIVE
**Code:** [src/tests/test_rude_gauntlet.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/test_rude_gauntlet.py#L80) — Speaker Masking.
**Logic:** Hub-side selective muting based on the `addressed_to` scalar from Sentinel.
**Mechanism:** Prevents nodes from speaking if they are not the intended target of the semantic address.

## [FEAT-245] Identity Shielding (Semantic Isolation)
**Status:** ACTIVE (Modernization Planned Sprint 31)
**Code:** [src/test_cache_integration.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/test_cache_integration.py#L10) — Identity Shielding (Semantic Isolation).
**Logic:** Distinction between Current Lab State (The Brain) and Historical Archive (Deep Thought) to prevent memory bleed.
**Refactor Strategy:** Merge into [VIBE-012] (Hemispheric Independence). Enforce boundaries through modular prompt injection.
**Rationale:** Prevents \"Memory Bleed\" where nodes hallucinate personal experiences from the 18-year archive.

## [FEAT-246] Unified Vibe Schema
**Status:** ACTIVE
**Code:** [src/forge/generate_sentinel_curriculum.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/forge/generate_sentinel_curriculum.py#L34) — Unified Vibe Schema.
**Logic:** Consolidation of topic and vibe into a single classification loadout for BKM-015.1.
**Rationale:** Simplifies training and makes routing more semantically predictable.

## [FEAT-247] Physical Audit Gate
**Status:** PLANNED
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L1155) — Physical Audit Gate.
**Logic:** Refinement of the Cooldown phase where Pinky audits Brain's synthesis for hardware feasibility.
**Mechanism:** Refactored 'evaluate_grounding' in Cognitive Hub.

## [FEAT-249] VRAM Hibernation Matrix (Deep Sleep)
**Status:** ACTIVE
**Code:** [pulse_monitor.sh](https://gitlab.com/kEnder242/Dev_Lab/blob/main/pulse_monitor.sh#L6) — VRAM Hibernation Matrix (Deep Sleep).
**Logic:** Tiered VRAM reclamation based on client connectivity and activity timers.
**Mechanism:** Reclaims ~6GB VRAM after 10m idle time.

## [FEAT-249.3] Verified Hibernation (VRAM Polling)
**Status:** ACTIVE
**Code:** [src/tests/test_attendant_sprint20.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/test_attendant_sprint20.py#L30) — Verified Hibernation (VRAM Polling).
**Logic:** NVML-based confirmation of weight unloading.
**Mechanism:** `mcp_hibernate` polls VRAM used until it drops below 2000MB.

## [FEAT-249.4] Shadow Mute Recovery [FOR REVIEW]
**Status:** ACTIVE
**Code:** [src/tests/test_memory_foil.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/test_memory_foil.py#L13) — Shadow Mute Recovery [FOR REVIEW].
**Logic:** Lowers Shadow activation threshold to 0.0 when KENDER is offline.
**Rationale:** Ensures local technical failover is always active when sovereign compute is unreachable.

## [FEAT-249.5] Sovereign Fallback (Double-Tap Shadow)
**Status:** ACTIVE
**Code:** [field_notes/intercom_v2.js](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/intercom_v2.js#L7) — Sovereign Fallback (Double-Tap Shadow).
**Logic:** Re-invokes Shadow at high fuel (>0.6) for technical synthesis when Brain is offline.

## [FEAT-250] Surgical Ignition (Immunity-Aware)
**Status:** ACTIVE
**Code:** [start_lab.sh](https://gitlab.com/kEnder242/Dev_Lab/blob/main/start_lab.sh#L30) — Surgical Ignition (Immunity-Aware).
**Logic:** Enable engine-only reloading while sparing the active Hub process.
**Mechanism:** Assassin spares Port 8765 if `engine_only` is requested.

## [FEAT-251.2] Forensic Wait (Early Crash Detection)
**Status:** ACTIVE
**Code:** [field_notes/jellyfin_autotune.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/jellyfin_autotune.py#L5) — Forensic Wait (Early Crash Detection).
**Logic:** Monitor logs for 'Traceback' during boot to bypass blind 120s timeouts.

## [FEAT-252] Dynamic Secret Rotation
**Status:** ACTIVE
**Code:** [field_notes/features_build.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/features_build.py#L3) — Dynamic Secret Rotation.
**Logic:** Unique `uuid4` session tokens generated on every ignition to invalidate old sessions.

## [FEAT-253] Dynamic Role Discovery
**Status:** ACTIVE
**Code:** [src/nodes/loader.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/loader.py#L48) — Dynamic Role Discovery.
**Logic:** `BicameralNode` parses `--role` from `sys.argv` to resolve identity and host mapping.

## [FEAT-254] VRAM Pre-Flight Gate
**Status:** ACTIVE
**Code:** [src/debug/test_perf_5x5_timed.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/test_perf_5x5_timed.py#L34) — VRAM Pre-Flight Gate.
**Logic:** Refuse ignition if `FreeVRAM < RequiredVRAM`.

## [FEAT-257] Physical Pre-Flight Purge (Nuclear Assassin)
**Status:** ACTIVE
**Code:** [src/train/refine_persona.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/train/refine_persona.py#L4) — Physical Pre-Flight Purge (Nuclear Assassin).
**Logic:** OS-level port clearing and process reaping via systemd.
**Mechanism:** `ExecStopPost` logic in `lab-attendant.service` ensuring a clean process state when the service exits.

## [FEAT-259] Targeted Hibernation (The Butler Pattern)
**Status:** ACTIVE
**Code:** [src/behavior_test.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/behavior_test.py#L25) — Targeted Hibernation (The Butler Pattern).
**Logic:** Surgical reaping of session-specific engine processes during hibernation while sparing the management layer.
**Mechanism:** 
1.  **SPARE**: Hub (`acme_lab.py`) and Resident Nodes are spared.
2.  **REAP**: AI Engines carrying the session token are killed.

## [FEAT-260] Fast-Path STUB Engine (Model Proxy)
**Status:** ACTIVE
**Code:** [src/debug/harness_prompt_iteration.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/harness_prompt_iteration.py#L9) — Fast-Path STUB Engine (Model Proxy).
**Logic:** A high-speed simulation mode that bypasses physical GPU hardware gates.
**Mechanism:** Bypasses VRAM pre-flight and subprocess spawning for rapid state testing.

## [FEAT-261] Traceable Awakening (Mandatory Reasoning)
**Status:** ACTIVE
**Code:** [src/infra/live_telemetry.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/infra/live_telemetry.py#L124) — Traceable Awakening (Mandatory Reasoning).
**Logic:** Enforces a mandatory `reason` argument for all engine ignition events to ensure auditability.
**Mechanism:** 
1.  **Enforcement**: `/start` and `/ignition` require a `reason`.
2.  **Audit Trail**: Reasons are logged to the journal and exported to `status.json`.
3.  **Client-Aware Gate**: Hub foyer only triggers ignition if the handshake client is explicitly `intercom`.

## [FEAT-265] The Waking State Machine
**Status:** ACTIVE
**Code:** [src/acme_lab.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/acme_lab.py#L6) — The Waking State Machine.
**Logic:** Formalizes the transition from HIBERNATING to WAKING to READY.
**Mechanism:** Modifies `on_handshake` in the Hub to await engine readiness before broadcasting status, preventing UI disconnect loops. Updates crosstalk bar to reflect intermediate states (`[IGNITION IN PROGRESS]`).

## [FEAT-266] Alarm Restoration & Tiered Visibility
**Status:** ACTIVE
**Code:** [src/v5/ignition/manager.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/ignition/manager.py#L491) — Alarm Restoration & Tiered Visibility.
**Logic:** Restores the background scheduled task loop (Nightly Dialogue, Nibbler) with managed log verbosity.
**Mechanism:** Re-enables `is_window` logic. Implements `WARNING` level "Nothing to do" heartbeats for nightly tasks, and suppresses "spam" from frequent nibble tasks unless executed. Respects `MAINTENANCE_LOCK`.

## [FEAT-267] Remote Control Discovery
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L415) — Remote Control Discovery.
**Logic:** Resolves 401 Unauthorized errors during Remote Lab Control actions.
**Mechanism:** Attendant publishes its current auth key (`vitals.style_key`) in `status.json`. UI polling loop extracts this key for subsequent REST calls. Attendant middleware hardened to accept CORS `OPTIONS` preflights (HTTP 200).

## [FEAT-283] Neural Buffer & Pre-Wake Prompt Replay
**Status:** COMPLETED (Sprint 56)
**Code:** [src/v5/foyer/router.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/foyer/router.py#L1552) — Neural Buffer & Pre-Wake Prompt Replay.
**Logic:** Caches pre-wake user prompts (e.g., initial cold-boot greetings like "hi") received while logical resident nodes are igniting (`not self.residents.booted`). Holds the intent in `_dispatch_buffered_intent` while broadcasting `SYNCING` state, and automatically replays the prompt into the 5-Stage Division of Labor pipeline as soon as physical silicon and logical nodes finish booting.
**Rationale:** Guarantees that first-turn prompts asked during cold-start are answered automatically without requiring user re-querying or dropping frames.
**Mechanism:** `queue_drainer()` in `HomeLabAI/src/v5/foyer/router.py`.

## [FEAT-284] Engine-Aware Foyer Gate
**Status:** ACTIVE
**Code:** [field_notes/intercom_v2.js](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/intercom_v2.js#L6) — Engine-Aware Foyer Gate.
**Logic:** Explicitly blocks user queries during the 'WAKING' state.

## [FEAT-285] High-Fidelity Priming Telemetry
**Status:** ACTIVE
**Code:** [src/v5/foyer/router.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/foyer/router.py#L553) — High-Fidelity Priming Telemetry.
**Logic:** Verbose logging of all Windows Brain priming decisions and results.

## [FEAT-286] Escalation Probe Protocol
**Status:** ACTIVE
**Code:** [HubProbe.py](https://gitlab.com/kEnder242/Dev_Lab/blob/main/HubProbe.py#L5) — Escalation Probe Protocol.
**Logic:** Implements a 3-stage ignition sequence for remote and local engines:
1.  **Stage 1 (Ping):** Verifies physical network/port reachability.
2.  **Stage 2 (Tags):** Verifies API readiness and model manifest availability.
3.  **Stage 3 (Prime):** Performs a 1-token cognitive generation to force engine residency (The "Latch").
**Behavior:** Stages 1 & 2 are synchronous (Heartbeat); Stage 3 is asynchronous (Parallel Prime).

## [FEAT-287] Mutual Exclusion (Ignition Mutex)
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L618) — Mutual Exclusion (Ignition Mutex).
**Logic:** Enforces a strict one-in-one-out policy for state transitions using an \`asyncio.Lock\`.
**Rationale:** Prevents "Spark Collisions" where redundant ignition requests (e.g., RECOVERY + User Intent) would flood the Attendant and crash the Hub.
**Mechanism:** \`self.ignition_lock\` in \`lab_attendant_v4.py\` wrapping the entire ignition sequence.

## [FEAT-288] Hash-Based Port Authority
**Status:** ACTIVE
**Code:** [src/nodes/thought_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/thought_node.py#L8) — Hash-Based Port Authority.
**Logic:** Replaces the 'Nuclear Port Guard' (`fuser -k`) with strict PID file and process-name tracking.
**Rationale:** Solves the "Zombie Port" problem where dormant engines or `TIME_WAIT` sockets block new family members, while preventing the suicidal reaping of active client connections.
**Mechanism:** `cleanup_processes` in `manager.py` targets specific hashes.

## [FEAT-289] Atomic Induction (Alarm State Lock)
**Status:** ACTIVE
**Code:** [src/v5/ignition/manager.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/ignition/manager.py#L64) — Atomic Induction (Alarm State Lock).
**Logic:** Sets the daily lock date (last_induction_date) IMMEDIATELY upon entering the induction gate.
**Rationale:** Eliminates the "2AM Induction Storm" where the 60s loop would re-trigger the same nightly dialogue before the first one finished.
**Mechanism:** Ordering fix in \`scheduled_tasks_loop\` in \`acme_lab.py\`.

## [FEAT-302] Adaptive Cooldown Tracking (Recovery Backoff)
**Status:** ACTIVE
**Code:** [src/v5/ignition/manager.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/ignition/manager.py#L66) — Adaptive Cooldown Tracking (Recovery Backoff).
**Logic**: Prevents "Engine Thrashing" during persistent hardware or orchestration failures by implementing an exponential backoff for autonomous recovery.
**Mechanism**:
1.  **Counter**: `recovery_attempts` increments on every watchdog-triggered ignition.
2.  **Backoff**: `Cooldown = 5s + (Attempts * 120s)`.
3.  **Stability Latch**: The counter only resets if the Lab maintains `OPERATIONAL` status for at least 300s (5 minutes). This prevents resetting the backoff during short-lived "Flapping" states.
**Verification**: 5x5 Stability Gauntlet.

## [FEAT-318] Quiescence Telemetry (The Settle Window)
**Status:** ACTIVE
**Code:** [src/debug/five_by_five_gauntlet.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/five_by_five_gauntlet.py#L9) — Quiescence Telemetry (The Settle Window).
**Logic**: Exposes the remaining boot grace window to the dashboard and test harnesses for deterministic sequencing.
**Mechanism**: `/status` endpoint returns `quiescence_remaining` in seconds, derived from the internal `boot_grace_period` (decremented every 2s pulse).
**Rationale**: Eliminates "Wait-and-Guess" patterns in user interfaces and automated endurance tests.

## [FEAT-356] Foil-Aware Memory (Unified Session Ledger)
**Status:** ACTIVE (Modernization Planned Sprint 31)
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L179) — Foil-Aware Memory (Unified Session Ledger).
**Logic:** Eliminates single-turn amnesia by giving Pinky a persistent view of the Brain's strategic logic from previous turns. The short-term context buffer for debate.
**Mechanism:** Session-persistent `round_table_memory` (deque) in the `CognitiveHub` that survives turn clearances.
**Refactor Strategy:** Stabilize. Move from in-memory deque to persistent session file (`.round_table.json`).

## [FEAT-368] Vocal Handshake
**Status:** ACTIVE (Modernization Planned Sprint 31)
**Code:** [src/tests/test_deep_thought_vocal.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/test_deep_thought_vocal.py#L8) — Vocal Handshake.
**Logic:** Immediate persona feedback during engine ignition. If the engine is still warming, Pinky provides a hardcoded Semantic Handshake instead of crashing or providing reflex-only output.
**Mechanism:** Triggered within `cognitive_hub.py` and `acme_lab.py` during engine-down events or triage connection errors.
**Refactor Strategy:** Harden into a "Systemic Handshake" that triggers on all engine latency events, not just explicit connection errors.
 "Systemic Handshake" that triggers on all engine latency events, not just explicit connection errors.


## [FEAT-369] Turing JIT Path Resilience
**Status:** ACTIVE
**Code:** [src/bridge_burn_to_rag.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/bridge_burn_to_rag.py#L66) — Turing JIT Path Resilience.
**Logic**: Automates the restoration of fragmented CUDA libraries after driver upgrades.
**Mechanism**: Injects `LD_LIBRARY_PATH` dynamically into systemd and ignition scripts.

## [FEAT-370] Boot Storm Mitigation
**Status:** ACTIVE
**Code:** [src/debug/repro_vram_corruption.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/repro_vram_corruption.py#L43) — Boot Storm Mitigation.
**Logic**: Prevents redundant logical node tasks during high-frequency ignition cycles.
**Mechanism**: Uses `asyncio.Lock` and a 'booting' latch in the Resident Manager.

## [FEAT-371] Robust Token Extraction (Multi-Source)
**Status:** ACTIVE
**Code:** [src/debug/test_dispatch_logic.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/test_dispatch_logic.py#L16) — Robust Token Extraction (Multi-Source).
**Logic**: Ensures model responses are never muzzled by vLLM's internal parsing logic.
**Mechanism**: `_stream_vllm` now extracts tokens from both `content` and `tool_calls` function arguments.

## [FEAT-322] Authority Verification (Ownership Check)
**Status:** DEFEATURED (Sprint 31)
**Code:** *none found (documented only)*
**Logic**: Verification checks ensuring adopted PIDs belong strictly to user `jallred`.
**Mechanism**: Relied on in V4 to prevent multi-user process adoption collisions. Defeatured in V5 by enforcing single-user systemd sandbox constraints (`User=jallred`).

## [FEAT-323] Backoff Telemetry
**Status:** ACTIVE
**Code:** [src/v5/ignition/manager.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/ignition/manager.py#L66) — Backoff Telemetry.
**Logic**: Exposes `recovery_level` and `recovery_in_progress` status flags to the `/status` endpoint and UI during recovery actions.
**Mechanism**: Decoupled attributes mapped in `LabStatus` dataclass and populated by the `IgnitionManager` in V5.

## [FEAT-220.1] Physical Scavenging (Process Adoption)
**Status:** DEFEATURED (Sprint 31)
**Code:** [src/train/refine_persona.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/train/refine_persona.py#L3) — Physical Scavenging (Process Adoption).
**Logic**: Scans active ports/processes on boot and "adopts" existing foyer or engine processes into the ledger.
**Mechanism**: Omitted in V5 in favor of clean-slate namespaces via `ExecStartPre` namespace cleanup (`pkill -9`). Removes "ghost state" traps.

## [FEAT-374] Tiered Idle Verification Pattern
**Status:** ACTIVE
**Code:** [src/v5/ignition/manager.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/ignition/manager.py#L419) — Tiered Idle Verification Pattern.
**Logic**: Prevents premature hibernation during direct API usage of the vLLM engine by combining low-overhead TCP connection checks with precise internal engine metrics validation.
**Mechanism**:
1.  **Tier 1 (TCP Connection Check)**: Checks if there are active TCP connections on port 8088. If none, proceeds to hibernate.
2.  **Tier 2 (vLLM Metric Check)**: If connections exist, queries `http://localhost:8088/metrics` or `/health` to verify if the engine is actively executing or queueing requests (`vllm:num_requests_running > 0` or `vllm:num_requests_waiting > 0`). If idle, proceeds to hibernate. Otherwise, resets the idle timer.
3.  **Grace Window**: Prevents shutdown race conditions during the engine warmup phase by respecting a boot grace period.


## [FEAT-400] ROLE TOKEN (Multi‑LoRA Persona Switch)

**Status:** DESIGN
**Code:** [sync_chroma_dna.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/sync_chroma_dna.py#L74) — ROLE TOKEN (Multi‑LoRA Persona Switch).

**Logic:** A single special token (e.g., `<|PINKY|>`) is injected after the `PREVIOUS STAGE OUTPUT` and before the `USER PROMPT`. The hub interprets this token to switch the active LoRA adapter for the upcoming generation while preserving the KV‑cache built from the static prefix.

**Rationale:** Eliminates cache invalidation when swapping personalities, reduces latency, and enables a chat‑room‑like experience where different agents can “overhear” without resetting context.

**Mechanism:** A mapping table links each ROLE TOKEN to a LoRA adapter. The token is added to the tokenizer vocabulary if needed. During request processing the hub loads the specified LoRA before generating the final response.

**Refactor Strategy:** Update `loader.py` and `acme_lab.py` to recognize ROLE TOKENs and perform adapter switching. Add unit tests for cache integrity during token‑driven swaps.

## [FEAT-401] Semantic Annealing Pipeline

**Status:** DESIGN
**Code:** [src/debug/simulate_moe_pipeline.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/simulate_moe_pipeline.py#L4) — Semantic Annealing Pipeline.

**Logic:** Integrates background self-evaluation with online/offline human feedback. Ingested events and night dream cycles are verified by a background evaluator, while user chat corrections (online) or dashboard flags (offline) write persistent correction rules to resolve factual errors and feed the RAG correction loop.

**Rationale:** Decouples structural testing from qualitative validation, preventing fragile unit tests while providing forensic traceability. Employs semantic similarity checks (>0.85) to merge related insights, preventing database bloat once raw inputs are exhausted.

**Mechanism:** Evaluation worker `evaluate_rag.py` (triggered in `mass_scan.py`), validation output ledger `validation_ledger.jsonl`, user correction ledger `overrides.json` parsed via `cognitive_hub.py`, and rendering UI panels on `status.html`.

## [FEAT-402] Asymmetric Telemetry Probe (Failover Optimization)
**Status:** ACTIVE
**Code:** [HubProbe.py](https://gitlab.com/kEnder242/Dev_Lab/blob/main/HubProbe.py#L5) — Asymmetric Telemetry Probe (Failover Optimization).
**Logic:** Differentiates between hard offline states (Connection Refused) and soft loading states (inference lag) to optimize the remote KENDER 4090 failover.
**Rationale:** Prevents premature failover during long-running tasks or loading peaks, while ensuring rapid re-connection when the primary host boots.
**Mechanism:** Strict 5-second check timeout, asymmetric cache (300s success, 15s failure), 180-second loading grace period, and dynamic interjections for turns exceeding 10 seconds of remote latency.

## [FEAT-403] Dream Pass Synthesis (Fine-Tuning Prep)
**Status:** ACTIVE
**Code:** [src/nodes/archive_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/archive_node.py#L447) — Dream Pass Synthesis (Fine-Tuning Prep).
**Logic:** Structured dataset creation utilizing a specialized `[DREAM_PASS]` header on KENDER to synthesize raw, messy chat history into idealized instruction-response pairs for LoRA training.
**Rationale:** Standardizes weight training on high-signal logical constructs rather than noisy interactive chat.
**Mechanism:** Persona-locked generation prompts, Stage 2 regex-based output cleaning, and validation of dataset format prior to adapter training.

## [FEAT-404] Context Starvation Protocol & Abort Gate
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L559) — Context Starvation Protocol & Abort Gate.
**Logic:** Enforces a strict `[ERROR: CONTEXT_STARVED]` protocol when queries reference specific historical topics or GEM IDs while RAG context is empty and tools are unavailable. Traps the starvation token mid-stream in `_process_node_stream` to immediately cancel LLM generation, bypass downstream waterfall legs, and alert Foyer.
**Rationale:** Prevents small models (3B/7B) from hallucinating speculative facts, dates, or code structures when asked about unrecognized or unindexed historical projects. Without this abort gate, context-starved nodes generate plausible text that bleeds into subsequent waterfall reasoning legs and user output.
**Mechanism:** Dynamic injection of `CONTEXT_VALIDITY` in `loader.py` during tool-bound turns, token trapping in `cognitive_hub.py`, and mid-stream task cancellation.

## [FEAT-405] Gems-to-Notes Ground Truth Synthesis
**Status:** ACTIVE
**Code:** [src/nodes/archive_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/archive_node.py#L1085) — Gems-to-Notes Ground Truth Synthesis.
**Logic:** Resolves vector search candidates from `long_term_wisdom` by opening target physical JSON note files (e.g. `2024_01.json`) and extracting the raw chronological text entry (summary, evidence, or synopsis) directly into the returned RAG context payload.
**Rationale:** Bridges vector embedding discovery anchors to actual physical note text. Without this ground truth bridge, RAG queries return only abstract document IDs or file paths, forcing LLMs to guess underlying historical validation details.
**Mechanism:** Physical file path resolution in `archive_node.py`, neighborhood expansion of adjacent entries, and structured `[ACQUISITION]` context payload formatting.

## [FEAT-406] Coherence Judge Evaluation Ledger & Retort
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L1224) — Coherence Judge Evaluation Ledger & Retort.
**Logic:** Executes a post-generation critique loop where Pinky evaluates strategic reasoning for logic errors, slop, or contradictions using guided JSON decoding (`score`, `reasoning`, `slop_found`, `retort`). Captures `retort` in `turn_thought_trace["critique"]`, writes evaluations atomically to `.round_table_evals.json`, and dispatches the retort directly to the UI chat stream under "Pinky (Coherence Critic)".
**Rationale:** Establishes automated peer evaluation of strategic LLM output, surfacing logic gaps, logging historical quality metrics over time, and presenting immediate critique feedback to the user.
**Mechanism:** Guided decoding schema in `cognitive_hub.py` (`evaluate_grounding`), atomic file replace (`.tmp`), and `execute_dispatch` terminal summary broadcast.

## [FEAT-407] Tag-Delimited Grounding Isolation (<historical_record>)
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L514) — Tag-Delimited Grounding Isolation (<historical_record>).
**Logic:** Wraps RAG retrieval evidence within `<historical_record>` XML boundary tags during `HISTORICAL`, `FORENSIC`, and `TECHNICAL` turns, injecting a strict `GROUNDING_PROTOCOL` instruction restricting generation exclusively to tagged evidence.
**Rationale:** Protects against context leakage between historical query briefs and live operational parameters (such as current OS runtime, host CPU/GPU hardware, or active ports). Without XML boundary tags, small models mix past historical events with present-day runtime state.
**Mechanism:** Conditional string wrapping and positive grounding guidance injection in `cognitive_hub.py` (`_process_node_stream`).

## [FEAT-408] Tool-Driven Waterfall Cascade
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L469) — Tool-Driven Waterfall Cascade.
**Logic:** Dynamically queries active resident MCP tools via `_get_node_tools` during multi-leg waterfall execution (`_run_brain_leg`), passing active tool definitions to remote reasoners instead of empty tool lists.
**Rationale:** Enables downstream reasoning models (Brain/Deep Thought) to execute active tools when handling complex queries. Without dynamic tool passing, remote nodes remain context-starved and cannot query internal memory or telemetry servers.
**Mechanism:** `_get_node_tools` introspection in `cognitive_hub.py`, tool list injection into `_process_node_stream`.

## [FEAT-409] WYWO Vibe Routing & Standup Synthesis
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L964) — WYWO Vibe Routing & Standup Synthesis.
**Logic:** Classifies casual recall and status-check queries into the `WYWO` (While You Were Out) vibe, automatically querying recent nightly dialogue records (`nightly_dialogue.json`) and subconscious dream wisdom from the vector archive to synthesize a high-density standup briefing.
**Rationale:** Provides structured, automated retrieval of overnight self-reflection and subconscious debate results when the user resumes interaction. Without this vibe classification, status queries route to standard casual banter without surfacing overnight progress.
**Mechanism:** Triage prompt rule 8 in `lab_node.py`, context building in `cognitive_hub.py` (`process_query`), and `[MODE]: STANDUP` behavioral guidance.

## [FEAT-410] Adaptive Two-Tier RAG Compass
**Status:** ACTIVE
**Code:** [src/nodes/archive_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/archive_node.py#L990) — Adaptive Two-Tier RAG Compass.
**Logic:** Implements a two-tier resolution strategy for archive queries: Tier 1 matches internal entry `date` attributes where present; Tier 2 falls back to filename range bounds (`2016_2019.json`) for un-timestamped legacy notes. Dynamically expands candidate selection when target matches yield fewer than 2 entries.
**Rationale:** Eliminates context pollution from arbitrary +-1 year range hacks while preserving temporal boundaries for modern timestamped entries and safely handling early un-timestamped archives.
**Mechanism:** Year parsing and Gaussian temporal decay weighting in `archive_node.py` (`get_context`), candidate sorting via RRF score * temporal weight.

## [FEAT-411] Structured Append-Only Tool Log Archive
**Status:** ACTIVE
**Code:** [src/nodes/loader.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/loader.py#L643) — Structured Append-Only Tool Log Archive.
**Logic:** Records tool executions to an append-only workspace file (`tool_log.md`) with timestamps, node identifiers, parameters, and clickable `file:///` links, streaming execution payloads via WebSockets to client UI cards.
**Rationale:** Provides complete auditability of tool invocations without polluting the active LLM chat context window or mutating workspace whiteboard state.
**Mechanism:** `append_to_tool_log` in `loader.py`, telemetry queue worker thread, and `window.renderToolLogEntry` in `intercom_v2.js`.

## [FEAT-412] Connection-Aware Idle Hibernation Deferral
**Status:** ACTIVE
**Code:** [src/v5/foyer/router.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/foyer/router.py#L1191) — Connection-Aware Idle Hibernation Deferral.
**Logic:** Polls active Foyer client WebSocket connections before initiating VRAM hibernation, doubling the default AFK timeout (to 600s) and extending idle grace periods (+300s) while active browser sessions remain open.
**Rationale:** Prevents jarring model unloading and cold-start latency spikes while an engineer is actively interacting with or viewing the web dashboard.
**Mechanism:** Client connection counter in `foyer/router.py` (`delayed_shutdown`), status check deferral in `acme_lab.py`.

## [FEAT-413] Decoupled Queue Drainer & Node Boot Mutex
**Status:** ACTIVE
**Code:** [src/tests/test_v5_stabilization.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/test_v5_stabilization.py#L70) — Decoupled Queue Drainer & Node Boot Mutex.
**Logic:** Separates request queue processing into an asynchronous background loop with node-level initialization locks, preventing race conditions during cold node boots and damping casual routing penalties.
**Rationale:** Solves queue stalls and socket deadlocks when multiple user or background requests arrive during node cold starts.
**Mechanism:** Async queue drainer task in `foyer/router.py`, initialization mutex per resident node.

## [FEAT-414] MoE+ Latency-Hiding Telemetry Stack & Preamble Fill
**Status:** ACTIVE
**Code:** [src/debug/bench_moe_plus.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/bench_moe_plus.py#L67) — MoE+ Latency-Hiding Telemetry Stack & Preamble Fill.
**Logic:** Overlaps intent triage, RAG retrieval, and workspace gathering with model warmup latency, streaming Pinky preamble tokens to fill the air while remote compute engines (KENDER 4090 / vLLM / Brain) ignite or load KV cache. Streams multi-stage latency gauges via Prometheus on port 8010.
**Rationale:** Prevents 3–10 seconds of dead silence during remote GPU model ignition or heavy reasoning steps, providing continuous feedback and microsecond-level telemetry to Prometheus/Grafana.
**Mechanism:** `benchmark_routing` in `bench_moe_plus.py`, Prometheus gauge metrics on port 8010, concurrent preamble streaming in `cognitive_hub.py`.

## [FEAT-415] Asynchronous Non-Blocking Engine Health Gate
**Status:** ACTIVE
**Code:** [src/nodes/loader.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/loader.py#L313) — Asynchronous Non-Blocking Engine Health Gate.
**Logic:** Offloads synchronous HTTP engine health check probes during node initialization to the asyncio loop executor (`loop.run_in_executor`), preventing network latency or remote host hangs from blocking the main event loop.
**Rationale:** Prevents the main event loop from freezing when checking remote compute node health (e.g. KENDER over Tailscale/LAN). Without executor offloading, network timeouts block all local WebSocket and HTTP handling.
**Mechanism:** `loop.run_in_executor` HTTP check in `loader.py` (`ping_engine`), non-blocking health caching with 15s failure TTL.

## [FEAT-416] Single-Epoch Nightly Refinement Sweeper
**Status:** ACTIVE
**Code:** [field_notes/mass_scan.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/mass_scan.py#L375) — Single-Epoch Nightly Refinement Sweeper.
**Logic:** Executes a single bounded epoch of note nibbling, gem refinement (2:00 AM – 5:00 AM window), de-duplication, and yearly aggregation during the nightly maintenance sweep. At 05:00 AM, the refinement loop yields cleanly, ensuring a full 1-hour buffer (until 06:00 AM) for archive aggregation, de-duplication, and trailing tasks.
**Rationale:** Replaces continuous 24/7 scanning with bounded midnight execution, allowing the lab to remain in Lean Sleep during the day while refining up to ~150 gems nightly.
**Mechanism:** `--once` flag in `field_notes/mass_scan.py`, 05:00 AM cutoff check, oneshot service `field-notes-nightly.service` (4-hour `TimeoutStartSec=14400`), and `field-notes-nightly.timer` systemd unit.

## [FEAT-417] Consolidated Universal Error Trap & Live System Console Stream (`#sys-console`)
**Status:** ACTIVE
**Code:** [field_notes/script.js](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/script.js#L30) — Consolidated Universal Error Trap & Live System Console Stream (`#sys-.
**Logic:** Consolidates site-wide JavaScript error trapping into `script.js` using `window.onerror` and `window.addEventListener('unhandledrejection')`. If a `#sys-console` element is present on the page (e.g. `status.html`, `files.html`), error payloads are automatically formatted with timestamps and file location and streamed in live terminal red (`#ff3b30`) directly to the console. On pages where UI space is constrained (e.g. `intercom.html`, `stories.html`), errors are logged cleanly without taking up DOM UI space.
**Rationale:** Eliminates hidden silent JavaScript failures across static site pages, surfacing live diagnostic tracebacks directly in the user interface.
**Mechanism:** `window.onerror` and `unhandledrejection` handlers in `field_notes/script.js`.

## [FEAT-418] The Symmetrical Interest Cascade (Lead Speaker + Interjection Threshold)
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L1046) — The Symmetrical Interest Cascade (Lead Speaker + Interjection Threshol.
**Logic:** Establishes a symmetrical 2-variable formula for multi-agent interaction:
  1. `addressed_to` determines **Lead Speaker (Turn 1)**:
     - `"PINKY"` / `"NONE"` -> Pinky leads Turn 1.
     - `"BRAIN"` -> Brain leads Turn 1.
     - `"MICE"` -> Pinky & Brain both lead Turn 1.
  2. `current_interest > 0.5` determines **Partner Interjection (Turn 2)**:
     - If Pinky led Turn 1 and `current_interest > 0.5`, Brain interjects on Turn 2 with technical ground truth.
     - If Brain led Turn 1 and `current_interest > 0.5`, Pinky interjects on Turn 2 with an intuitive foil quip.
  3. Grounding Triage so casual greetings ("what's up", "hey", "hi") evaluate as `vibe: "CASUAL"`, `addressed_to: "PINKY"`, and `importance: 0.1`.
**Rationale:** Formulas decouple explicit speaker expectations (Lead Speaker) from ambient overhearing (Partner Interjection), eliminating awkward warm-up delays for casual quips while allowing emergent Round Table interjections whenever interest is high.
**Mechanism:** Lead/Partner turn loop in `cognitive_hub.py`, `triage_schema` with `addressed_to` enum (`NONE`, `PINKY`, `BRAIN`, `MICE`), and `current_interest` interjection threshold.

## [FEAT-428] Exponential Backoff & Cooldown State Engine
**Status:** ACTIVE
**Code:** [field_notes/nibble_v2.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/nibble_v2.py#L91) — Exponential Backoff & Cooldown State Engine.
**Logic:** Implements a progressive 3-tier backoff engine for background archive processing (`scan_queue.py` & `nibble_v2.py`). When yielding due to memory pressure (`available_ram < 1.5 GB`), load average (`load_avg > 2.0`), or non-IDLE logical state, the worker transitions through progressive sleep delays (15s -> 60s -> 15m `COOLDOWN` window).
**Rationale:** Eliminates tight-loop log spam and sentinel polling hammering when host memory or load stays constrained for extended periods.
**Mechanism:** `consecutive_yields` counter and `COOLDOWN` state in `scan_queue.py` and `nibble_v2.py` (`should_yield`).

## [FEAT-429] Poison Chunk Quarantine Protocol
**Status:** ACTIVE
**Code:** [field_notes/scan_queue.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/scan_queue.py#L172) — Poison Chunk Quarantine Protocol.
**Logic:** Automatically quarantines archive note chunks that encounter repeated execution failures (3 consecutive context length, JSON parsing, or API errors). Flagged chunks are tagged as `QUARANTINED` in `chunk_state.json` and isolated from immediate queue sweeps.
**Rationale:** Prevents a single corrupted or oversize note file from trapping background workers in an infinite fail-retry loop that hammers host CPU and LLM inference endpoints.
**Mechanism:** Failure counter, `QUARANTINED` status tag in `chunk_state.json`, and automatic queue bypass in `scan_queue.py`.

## [FEAT-430] Foyer C-Arena Heap Trimming Sentinel
**Status:** ACTIVE
**Code:** [src/v5/foyer/router.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/foyer/router.py#L397) — Foyer C-Arena Heap Trimming Sentinel.
**Logic:** Executes periodic glibc heap trimming (`ctypes.CDLL('libc.so.6').malloc_trim(0)`) in Foyer's idle cleanup loop and request completion hooks (`router.py`).
**Rationale:** Prevents PyTorch tensor allocation fragmentation and CPython memory arena bloat from inflating `acme_foyer_v5` process RSS footprint over long uptimes.
**Mechanism:** `malloc_trim(0)` invocation in `delayed_shutdown` and post-request cleanup handlers in `foyer/router.py`.

## [FEAT-431] GigaToken Remote Synthesis Gate (Stretch Goal)
**Status:** ACTIVE
**Code:** [src/nodes/loader.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/loader.py#L512) — GigaToken Remote Synthesis Gate (Stretch Goal).
**Logic:** Bypasses local context token clamping when routing deep historical research queries (`vibe: "DEEP_RESEARCH"`) to remote compute engines or external cloud endpoints (KENDER / Gemini / DeepSeek). Packages up to 32K–64K tokens of raw multi-year archive notes while maintaining 16K safety limits for local RTX 2080 Ti VRAM.
**Rationale:** Maximizes synthesis quality for multi-year retrospective queries on high-memory remote endpoints without triggering local VRAM OOM errors.
**Mechanism:** `is_remote_endpoint` check and context window scaler in `archive_node.py` and `cognitive_hub.py`.

## [FEAT-432] HyDE Local RAG Preprocessor (Backlog)
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L266) — HyDE Local RAG Preprocessor (Backlog).
**Logic:** Implements Hypothetical Document Embeddings ([arXiv:2212.10496](https://arxiv.org/abs/2212.10496)) using Pinky's live streaming preamble roleplay as the hypothesis generator. Pinky's spoken intuitive hypothesis ("Egad Brain, I bet Glibc C-arenas are caching PyTorch allocations!") streams to the UI as preamble text while being vectorized into ChromaDB to retrieve target BKMs with 95%+ precision.
**Rationale:** Dramatically increases vector retrieval precision for short interrogative queries against dense BKM technical notes without extra background LLM latency or cloud API keys.
**Mechanism:** Open hypothesis streaming in `cognitive_hub.py` and pre-search vectorization in `archive_node.py`.

## [FEAT-433] Asynchronous Sanity Critic Protocol
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L249) — Asynchronous Sanity Critic Protocol.
**Logic:** Fires a non-blocking background evaluator (`asyncio.create_task`) after initial turn response streaming completes. Evaluates response accuracy against historical BKMs, broadcasting a `sanity_check` WebSocket payload to render a live **"🛡️ Sanity Verified"** badge on Intercom chat cards.
**Rationale:** Provides rigorous factual verification and hallucination detection without adding latency to the user's initial streaming response.
**Mechanism:** Non-blocking async evaluator task in `cognitive_hub.py` and live badge renderer in `intercom_v2.js`.

## [FEAT-435] Evergreen Career Compass Memory Ledger
**Status:** ACTIVE
**Code:** [src/nodes/loader.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/loader.py#L41) — Evergreen Career Compass Memory Ledger.
**Logic:** Establishes an authoritative 6-era memory ledger (`data/career_compass.json`) compiled from verified resume ground truth. Tier 1 Anchor Map (<300 tokens) is injected into `BicameralNode` system prompt bedrock (`loader.py`), while Tier 2 Keyword Mesh scales micro-details infinitely on disk and ChromaDB RAG.
**Rationale:** Grounds Pinky and Brain in 18 years of technical history (PCIe validation bring-up, Redfish, PECI, MCTP, Intel VISA signal trace) without inflating system prompt token context.
**Mechanism:** `data/career_compass.json` Tier 1 Anchor Map, `BicameralNode` prompt bedrock in `loader.py`, and `test_career_compass_bedrock.py` token ceiling assertion (<350 tokens).

## [FEAT-436] Unified Intent-HyDE Pre-Reflection Engine
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L758) — Unified Intent-HyDE Pre-Reflection Engine.
**Logic:** Refactors the triage loop in `cognitive_hub.py` to execute a single 150-token Pre-Reflection pass. Outputs Inferred Intent (*"I think the user is trying to say..."*), Triage Routing (`addressed_to`, `vibe`, `importance`), and HyDE Synthesis vector in a single pass. Includes a short-circuit early-exit for simple greetings (`"hi"`, `"hey"`) in <15 tokens (~50ms) as `PINKY CASUAL 0.1`.
**Rationale:** Eliminates redundant LLM passes, resolves intent/nuance for historical retrospective queries, and reduces casual greeting latency to under 50ms.
**Mechanism:** `prereflection_triage_result` JSON schema, greeting short-circuit check, and unified execution loop in `cognitive_hub.py`.

## [FEAT-437] 3-Tier HyDE Failover Cascade & Dynamic Feedback Loop
**Status:** COMPLETED (Commit `37a1f59`)
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L76) — 3-Tier HyDE Failover Cascade & Dynamic Feedback Loop.
**Logic:** Augments the 3-tier HyDE failover cascade for ChromaDB KB vector search (`archive_node.py` & `cognitive_hub.py`):
  1. `DEEP_THOUGHT_REMOTE` (Tier 1): High-precision HyDE vector synthesized on KENDER 4090 based on the 4-Domain HyDE Map Contract.
  2. `PINKY_LOCAL_VLLM` (Tier 2): Local vLLM Llama 3.2 3B AWQ backup HyDE generator when Kender is offline.
  3. `DIRECT_RAW_QUERY` / `NON_MATCH_BYPASS` (Tier 3): Zero-dependency raw query fallback floor.
  BKM-015 Compliance & Dynamic Loop: Zero hardcoded keyword arrays or pre-baked HyDE lists. Reads the dynamic keyword mesh directly from `data/career_compass.json` (populated by `mass_scan.py` FEAT-438), closing the feedback loop between the 18-year archive scanner and HyDE vector synthesis. If the judge/triage determines a query does not match the 4 KB domains (e.g. casual turn), HyDE synthesis evaluates to empty `""`, bypassing ChromaDB retrieval without forcing a hallucinated vector.
  Taxonomy: Distinguishes between **KB** (`artifact_vault`, `journal_kb`, `lab_journal` — distilled information and 18-year archive) and **DNA** (`behavioral_dna`, `feature_dna` — system building rules and SRE playbooks).
**Rationale:** Guarantees uninterrupted high-precision KB vector retrieval across remote/local nodes while upholding BKM-015 judge-driven clean exits for casual turns and dynamic prompt learning.
**Mechanism:** `resolve_hyde_vector` 3-tier cascade, `_load_hyde_synthesis_prompt` dynamic loader from `career_compass.json`, `hyde_vector_text` parameter in `archive_node.get_context`, and `test_feat437_resolve_hyde_vector.py`.

## [FEAT-438] Nightly Continuous Burn Map Synthesizer Integration
**Status:** COMPLETED
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L108) — Nightly Continuous Burn Map Synthesizer Integration.
**Logic:** Integrates `synthesize_career_mesh()` into the background scanner pipeline (`mass_scan.py`). Step 6 TLC scans raw note gems and `resume.txt` to continuously enrich `data/career_compass.json` Tier 2 Keyword Mesh without modifying Tier 1 Bedrock. Feeds directly into FEAT-437 HyDE prompt synthesis.
**Rationale:** Allows 18-year archive processing and newly discovered technical terms to scale infinitely on disk and vector RAG while keeping system prompt context strictly under 300 tokens.
**Mechanism:** `synthesize_career_mesh()` in `field_notes/mass_scan.py`, atomic write swap, and `test_tier_1_token_ceiling` validation.

## [FEAT-439] M5 Air MLX Offloading & Async Sanity Judge Protocol
**Status:** ACTIVE
**Code:** [src/nodes/mlx_judge_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/mlx_judge_node.py#L39) — M5 Air MLX Offloading & Async Sanity Judge Protocol.
**Logic:** Integrates Node 3 (M5 MacBook Air 32GB Unified Memory / Apple MLX Framework on port 8090) into the Round Table topology as an Asynchronous Sanity Judge & GigaToken Node. Evaluates full 256K context turn traces asynchronously in the background without delaying initial response streaming.
**Rationale:** Enables un-truncated 256K context evaluation on Apple MLX unified memory with a two-lane feedback loop (Factual -> ChromaDB `:8001`; Style -> `cli_voice_v1` LoRA dataset).
**Mechanism:** `src/nodes/mlx_judge_node.py`, `MLXAsyncJudge` driver, `[LAB-010]` infrastructure registration, and `test_mlx_judge_node.py`.

---

## [FEAT-440] Taxonomy Separation: Agent DNA vs. User Work History
**Status:** ACTIVE
**Code:** [src/tests/delegate.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/delegate.py#L144) — Taxonomy Separation: Agent DNA vs. User Work History.
**Logic:** Separates system/behavioral instructions (behavioral_dna, feature_dna) from historical user pedigree (career_ledger, artifact_vault, lab_journal) across ChromaDB collections.
**Rationale:** Prevents context bleeding between internal cognitive prompts and 18-year career work history.
**Mechanism:** 5 distinct ChromaDB collections on port 8001, populated via index_artifacts_to_rag.py and index_resume_to_rag.py.

## [FEAT-441] ChromaDB Multi-Collection Cosine Reranker
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L1117) — ChromaDB Multi-Collection Cosine Reranker.
**Logic:** get_context() in archive_node.py queries all 5 ChromaDB collections in parallel via asyncio.gather and applies a unified cosine distance filter (<0.45 cutoff) and distance-based sorting.
**Rationale:** Delivers high-precision context retrieval with domain-badged metadata ([ARTIFACT], [CAREER], [BEHAVIORAL_DNA], [FEATURE_DNA], [LAB_JOURNAL]) across heterogeneous document stores.
**Mechanism:** Parallel async HTTP queries, distance sorting, domain badge formatting in archive_node.py.

---

## [FEAT-442] Query Pre-Flight Refinement (QPR) & HyDE Synergy
**Status:** PROPOSED (Sprint 44 Story 6)
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L11) — Query Pre-Flight Refinement (QPR) & HyDE Synergy.
**Logic:** Pre-retrieval query de-noising in `cognitive_hub.py` prior to ChromaDB vector search. Translates vague or noisy human queries into domain-specific indexing terms while preserving original query as fallback if top vector similarity < 0.70.
**Rationale:** Prevents semantic dilution and false-premise noise from degrading vector recall and HyDE hypothetical document generation.
**Mechanism:** `cognitive_hub.py` pre-retrieval hook, similarity threshold sentinel, and `test_qpr_hyde.py`.

---

## [FEAT-443] Premise-Aware RAG-EVAL (PAR-Eval) & Valid Refusal Scoring
**Status:** PROPOSED (Sprint 44 Story 7)
**Code:** [src/nodes/mlx_judge_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/mlx_judge_node.py#L42) — Premise-Aware RAG-EVAL (PAR-Eval) & Valid Refusal Scoring.
**Logic:** Upgrades `MLXAsyncJudge` with structured refusal payload `{ "refusal": true, "reason": "PREMISE_MISMATCH" }`. Enhances 5x5 benchmark harness (`uber_5x5.py`) to intercept validated refusals ("Jason did not perform GPU VRAM work at Intel") and score them as **5/5 PASS**.
**Rationale:** Replaces GIGO benchmark failures with true intelligence verification—validating that system pushes back on false premises instead of hallucinating.
**Mechanism:** `mlx_judge_node.py` refusal schema, `uber_5x5.py` score interceptor, and `test_par_eval_scoring.py`.

---

## [FEAT-444] Judicial Backpressure Ledger & Stream Integration
**Status:** PROPOSED (Sprint 44 Story 8)
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L1024) — Judicial Backpressure Ledger & Stream Integration.
**Logic:** Streams M5 Judge evaluation findings and design critiques to `/field_notes/data/judge_backpressure.jsonl`. Renders `Amber [JUDGE]` badges on `status.html` interleaved timeline and compiles curated design ledger `JUDGE_FIELD_LEDGER.md`.
**Rationale:** Provides an automated backpressure feedback channel for system friction, bad queries, and script constraints without blocking live UI response streaming.
**Mechanism:** `judge_backpressure.jsonl` writer in `router.py`, `status.html` badge renderer, and `generate_judge_ledger.py`.

---

## [FEAT-447] Dynamic Cosine Distance Calibration & RAG Fallback Telemetry
**Status:** ACTIVE
**Code:** [src/nodes/archive_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/archive_node.py#L636) — Dynamic Cosine Distance Calibration & RAG Fallback Telemetry.
**Logic:** Calibrates vector similarity cutoff threshold in `archive_node.get_context()` from static 0.45 to dynamic 0.55 (matched to `all-MiniLM-L6-v2` embeddings). Logs RAG collection hit rates, candidates found, HyDE fallback events, and distance thresholds to `status.json`.
**Rationale:** Prevents valid semantic matches from being dropped by overly tight 0.45 distance cutoffs while providing real-time vector engine health telemetry to the status center.
**Mechanism:** `DISTANCE_THRESHOLD = 0.55` and `_log_rag_telemetry()` in `archive_node.py`, atomic write to `status.json`.

---

## [FEAT-448] Tri-Field Gem Schema & Self-RAG Refinement
**Status:** ACTIVE
**Code:** [field_notes/refine_gem.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/refine_gem.py#L225) — Tri-Field Gem Schema & Self-RAG Refinement.
**Logic:** Upgrades the BKM gem extraction prompt and schema in `refine_gem.py` to extract `summary`, `trigger_context`, `technical_gem`, and `anchors` (3–6 exact technical acronyms). Grounded in Self-RAG ([arXiv:2310.11511](https://arxiv.org/abs/2310.11511)) and Query2Doc ([arXiv:2303.07678](https://arxiv.org/abs/2303.07678)).
**Rationale:** Structures historical knowledge into rich hypothetical problem scenarios and dense hardware tokens, enabling Pinky's Stage 2 HyDE expansion to prime vector search with >95% cosine precision.
**Mechanism:** `refine_gem.py` Tri-Field prompt, `distill_journal_ledger()` bridge in `mass_scan.py`, `test_forge_distillation_unit.py`.

---

## [FEAT-450] Maximal Marginal Relevance (MMR) Utility Re-Ranking
**Status:** ACTIVE
**Code:** [src/nodes/archive_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/archive_node.py#L637) — Maximal Marginal Relevance (MMR) Utility Re-Ranking.
**Logic:** Implements utility-based diversity re-ranking over multi-collection ChromaDB candidates using Jaccard word-overlap penalties ($\lambda=0.7$). Grounded in Agentic-R ([arXiv:2601.11888](https://arxiv.org/abs/2601.11888)).
**Rationale:** Eliminates redundant semantic near-duplicates and promotes orthogonal technical nuggets (exact MSR registers, script arguments, command outputs) into top context slots.
**Mechanism:** `compute_mmr_ranking()` in `src/nodes/archive_node.py`, `test_agentic_r_retrieval.py`.

---

## [FEAT-451] Autonomous Grep-Gated RiR Search Pivot
**Status:** ACTIVE
**Code:** [src/nodes/archive_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/archive_node.py#L679) — Autonomous Grep-Gated RiR Search Pivot.
**Logic:** Executes an autonomous search pivot using fast Ripgrep across `field_notes/data/` and raw archives when ChromaDB vector distance exceeds $0.50$ or returns zero results. Extracts hardware tokens and injects line-level evidence. Grounded in Agentic-R ([arXiv:2601.11888](https://arxiv.org/abs/2601.11888)).
**Rationale:** Prevents retrieval failure on rare hardware tokens or new register definitions where embeddings alone produce weak distance scores.
**Mechanism:** `execute_grep_search_pivot()` in `src/nodes/archive_node.py`, `test_agentic_r_retrieval.py`.

---

## [LAB-090] SSH OOM Immunity Sentinel
**Status:** COMPLETED (Sprint 50)
**Code:** *none found (documented only)*
**Logic:** Configures systemd service override for `sshd.service` with `OOMScoreAdjust=-1000`, `MemoryMin=256M`, and `CPUSchedulingPolicy=rr`.
**Rationale:** Guarantees that SSH and remote VSCode tunnel sessions are never killed or swap-frozen during extreme host RAM pressure.
**Mechanism:** `/etc/systemd/system/sshd.service.d/override.conf` or user systemd override unit.

---

## [LAB-091] Kernel SysRq Emergency Protocol
**Status:** COMPLETED (Sprint 50)
**Code:** *none found (documented only)*
**Logic:** Enables kernel-level SysRq magic key interface (`kernel.sysrq = 1`).
**Rationale:** Provides an out-of-band emergency mechanism to safely sync disks (`echo s > /proc/sysrq-trigger`) and trigger instant kernel reboot (`echo b`) during hard userland freezes.
**Mechanism:** `/etc/sysctl.d/99-sysrq.conf` sysctl configuration.

---

## [LAB-092] Proactive Memory Kicker (EarlyOOM Sentinel)
**Status:** COMPLETED (Sprint 50)
**Code:** *none found (documented only)*
**Logic:** Deploys `earlyoom` with 5% RAM and 10% Swap thresholds.
**Rationale:** Terminates runaway background Python memory consumers *before* host swap space thrashing locks the OS and I/O bus.
**Mechanism:** `earlyoom` system service configuration.

---

## [FEAT-425] Standalone WebSocket RSS Memory Profiler
**Status:** COMPLETED (Sprint 50)
**Code:** [src/forge/dream_voice_FAST.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/forge/dream_voice_FAST.py#L32) — Standalone WebSocket RSS Memory Profiler.
**Logic:** Creates `psutil` profiling harness `HomeLabAI/src/infra/profile_ws_memory.py` measuring memory footprint during live WebSocket PCM audio streaming.
**Rationale:** Isolates exact RSS memory overhead added by WebSockets vs LLM KV-cache allocations.
**Mechanism:** `profile_ws_memory.py` harness with `status.json` reporting.

---

## [FEAT-426] Intercom Loopback & Origin Security Guard
**Status:** COMPLETED (Sprint 50)
**Code:** [src/v5/foyer/router.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/foyer/router.py#L887) — Intercom Loopback & Origin Security Guard.
**Logic:** Hardens `intercom_v2.js` and `lab-attendant` with explicit `127.0.0.1` loopback binding, origin header validation, and `X-Lab-Key` token checks.
**Rationale:** Prevents unauthorized cross-origin WebSocket connections while ensuring local development uses secure loopback IPC.
**Mechanism:** `intercom_v2.js` and `attendant.py` WebSocket handler.

---

## [FEAT-427] Audio PCM Stream Buffer Sentinel
**Status:** COMPLETED (Sprint 50)
**Code:** [field_notes/jellyfin_autotune.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/jellyfin_autotune.py#L4) — Audio PCM Stream Buffer Sentinel.
**Logic:** Implements a strict ring-buffer cap on Float32 $\rightarrow$ Int16 PCM audio downsampling in `intercom_v2.js`.
**Rationale:** Prevents unmanaged memory growth in browser heap and backend WebSockets during long speech turns.
**Mechanism:** `intercom_v2.js` PCM buffer clamp.

---

## [FEAT-428] Real-Time PCM Audio Stream Memory Benchmark
**Status:** COMPLETED (Sprint 50)
**Code:** [field_notes/nibble_v2.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/nibble_v2.py#L91) — Real-Time PCM Audio Stream Memory Benchmark.
**Logic:** Creates `HomeLabAI/src/tests/test_live_audio_memory_benchmark.py` to stream simulated Float32 $\rightarrow$ Int16 PCM audio buffers to `lab-attendant` while profiling `psutil` RSS RAM and vLLM KV-cache utilization.
**Rationale:** Closes the gap between integration tests (which stub audio) and live `intercom.html` usage, verifying true memory footprint during real-time speech interaction.
**Mechanism:** `test_live_audio_memory_benchmark.py` harness and `status.json` telemetry logging.

---

## [LAB-093] Lab-Attendant Cgroup Memory Sentinel
**Status:** COMPLETED (Sprint 50)
**Code:** *none found (documented only)*
**Logic:** Configures `MemoryMax=4G` and `ManagedOOMPreference=kill` in `lab-attendant.service`.
**Rationale:** Ensures that if `lab-attendant` or audio stream buffers experience memory pressure, systemd isolates and terminates only `lab-attendant`, keeping host OS, SSH, and other services 100% online.
**Mechanism:** `lab-attendant.service` systemd unit configuration.

---

## [FEAT-429] Foyer Disconnect Memory Reclaim Sentinel
**Status:** COMPLETED (Sprint 50)
**Code:** [src/tests/test_live_audio_memory_benchmark.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/test_live_audio_memory_benchmark.py#L3) — Foyer Disconnect Memory Reclaim Sentinel.
**Logic:** Implements explicit `on_close()` cleanup handlers in `attendant.py` and `ear_node.py` triggering `gc.collect()` and audio buffer flushing upon WebSocket disconnect.
**Rationale:** Prevents memory accumulation and orphan audio buffer leaks across multiple browser reloads or tab closures.
**Mechanism:** `on_close()` handler in `attendant.py` and garbage collection sentinel.

---

## [FEAT-430] Automated Delegation Retrospective & Friction Audit Stage
**Status:** COMPLETED (Sprint 50)
**Code:** [src/v5/foyer/router.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/foyer/router.py#L397) — Automated Delegation Retrospective & Friction Audit Stage.
**Logic:** Creates `HomeLabAI/src/infra/delegate_retrospective.py` and wires `--retrospective` flag into `delegate.py`. Automatically parses `/tmp/delegate_story_*.log`, queries REST session metrics (`tokens`, `time`, `child_sessions`), compares prompt target paths vs `git diff` actuals to detect path search thrash, and synthesizes a Delegation Friction Ledger artifact for user review and sign-off.
**Rationale:** Eliminates manual friction accounting, automatically capturing prompt path mismatches and provider 503 fallbacks at the end of every heads-down execution segment.
**Mechanism:** `delegate_retrospective.py` parser, `delegate.py --retrospective` CLI integration, and `DELEGATION_RETROSPECTIVE.md` report synthesizer.

---

## [FEAT-431] EarlyOOM Telemetry & Neural Pager Hook
**Status:** COMPLETED (Sprint 50)
**Code:** [src/nodes/loader.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/loader.py#L512) — EarlyOOM Telemetry & Neural Pager Hook.
**Logic:** Configures `earlyoom` with an executive notification hook (`earlyoom_pager_notifier.sh`) that writes structured `CRITICAL` telemetry events to `field_notes/data/pager_activity.json` whenever an OOM termination occurs.
**Rationale:** Captures the exact "WHY" behind every OOM kill (killed PID, process command, RAM/swap free percentages, and OOM score) for real-time visibility on `pager.html` and `status.html` without dropping SSH connections.
**Mechanism:** `earlyoom_pager_notifier.sh` script, `earlyoom` SystemD drop-in environment hook, and `pager_activity.json` event log.

---

## [LAB-100] CPU Max Scaling Frequency Cap (3.5 GHz)
**Status:** COMPLETED (Sprint 53)
**Code:** *none found (documented only)*
**Logic:** Caps max scaling frequency across all 8 CPU cores to 3.5 GHz via `/etc/systemd/system/cap-cpu-freq.service` and `/sys/devices/system/cpu/cpu*/cpufreq/scaling_max_freq`.
**Rationale:** Prevents peak 3.9 GHz thermal throttling events and hardware THERMTRIP trips.
**Mechanism:** `cap-cpu-freq.service` systemd unit and sysfs scaling parameters.

## [LAB-101] Kernel Panic Auto-Reset & Hung Task GRUB Configuration
**Status:** COMPLETED (Sprint 53)
**Code:** *none found (documented only)*
**Logic:** Configures `kernel.hung_task_panic=1 panic=10` in `/etc/default/grub` and compiles via `update-grub`.
**Rationale:** Converts silent hardware lockups into captured kernel panic tracebacks written to disk, auto-rebooting after 10s.
**Mechanism:** `/etc/default/grub` configuration and `sysctl` kernel parameters.

## [LAB-102] ZFS ARC Max Memory Cap (1.0 GiB)
**Status:** COMPLETED (Sprint 53)
**Code:** *none found (documented only)*
**Logic:** Sets `zfs_arc_max=1073741824` in `/etc/modprobe.d/zfs.conf` and live kernel parameter `/sys/module/zfs/parameters/zfs_arc_max`.
**Rationale:** Empirically verified via `arcstat` (98-100% metadata hit rate). Immediately reclaims **2.4 GiB physical DRAM** from disk cache (Available RAM increased from 3.5 GiB $\rightarrow$ 5.9 GiB) to guarantee allocation headroom for PyTorch, vLLM, and agent loops.
**Mechanism:** `/etc/modprobe.d/zfs.conf` options file and ZFS kernel module parameter.

## [LAB-103] Service Cgroup Memory Limits (`opencode-core` & `lab-attendant`)
**Status:** COMPLETED (Sprint 53)
**Code:** *none found (documented only)*
**Logic:** Configures drop-in systemd cgroup limits for `opencode-core.service` (`MemoryHigh=3.0G`, `MemoryMax=3.5G`) and `lab-attendant.service` (`MemoryHigh=1.5G`, `MemoryMax=2.0G`).
**Rationale:** Enforces strict memory budgets per service so an agent indexing burst or audio stream buffer spike cannot starve host DRAM or trigger host-wide thrashing.
**Mechanism:** Systemd drop-in configuration files `/etc/systemd/system/*.service.d/50-memory-limit.conf`.

## [LAB-104] OpenCode Scale-to-Zero Wake-on-Touch SystemD Gateway
**Status:** COMPLETED
**Code:** *none found (documented only)*
**Logic:** Configures `opencode.socket` (`0.0.0.0:4096`) and `opencode-proxy.service` with `TriggerLimitIntervalSec=0` and `--exit-idle-time=45m`.
**Rationale:** Allows OpenCode REST engine to scale down to zero when idle (0% CPU/DRAM), automatically waking up in 200ms when `delegate.py` or a browser touches port 4096.
**Mechanism:** `~/.config/systemd/user/opencode.socket`, `opencode-proxy.service`, and `delegate.py wake_web_ui()`.

---

## [FEAT-437] Pinky LoRA HyDE Inversion & Dynamic Domain Mapping
**Status:** COMPLETED (Sprint 54)
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L76) — Pinky LoRA HyDE Inversion & Dynamic Domain Mapping.
**Logic:** Inverts `resolve_hyde_vector()` so Pinky's local vLLM pass (holding fine-tuned `cli_voice_v1` LoRA weights) acts as Tier 1 HyDE generator, with Kender `deep_think` as Tier 2 fallback. Moves synthesis prompts and 4-domain terms into `HomeLabAI/src/data/hyde_domain_map.json` loaded dynamically at startup.
**Rationale:** Restores true division of labor: Pinky holds the 18-year archive weights needed for high-precision HyDE synthesis, while Deep Thought handles $t=0$ Preamble in `router.py`.
**Mechanism:** `resolve_hyde_vector()` in `cognitive_hub.py`, `hyde_domain_map.json`, and `test_feat437_resolve_hyde_vector.py`.

## [FEAT-456] Real VRAM Probing & Gauntlet Path Repair
**Status:** COMPLETED (Sprint 54)
**Code:** [field_notes/build_site.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/build_site.py#L89) — Real VRAM Probing & Gauntlet Path Repair.
**Logic:** Replaces dummy VRAM stub in `nightly_forge.py` with real `nvidia-smi` CSV queries (`memory.total`). Fixes `run_live_lab_gauntlet.sh` test invocation path to point to `../debug/test_live_fire_triage.py`.
**Rationale:** Provides accurate VRAM reporting in MB and restores 100% test gauntlet execution.
**Mechanism:** `get_vram_usage()` in `nightly_forge.py` and `run_live_lab_gauntlet.sh`.

## [FEAT-457] FeatureTracker Alignment & Submodule Synchronization
**Status:** COMPLETED (Sprint 54)
**Code:** [src/nodes/lab_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/lab_node.py#L112) — FeatureTracker Alignment & Submodule Synchronization.
**Logic:** Synchronizes git submodule pointers between `Dev_Lab`, `Portfolio_Dev`, and `HomeLabAI`. Updates FeatureTracker DNA matrices across ChromaDB vector database (`feature_dna`).
**Rationale:** Maintains 100% git and vector database synchronization across the federated workspace.
**Mechanism:** `FeatureTracker.md`, `git submodule update`, and `sync_feature_dna.py` git hooks.

## [FEAT-458] Atlas Identity Guard & OpenAgent REST Persona Binding Contract
**Status:** COMPLETED (Sprint 54)
**Code:** [src/train/distill_training_data.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/train/distill_training_data.py#L27) — Atlas Identity Guard & OpenAgent REST Persona Binding Contract.
**Logic:** Requires `delegate.py` to pass `"agent": agent` in BOTH `POST /session` AND `POST /session/<id>/message` REST payloads using exact registered display names (`"Atlas - Plan Executor"`, `"Prometheus - Plan Builder"`). Implements `[IDENTITY ASSERTION & HARD-STOP GUARD]` to force non-Atlas models (e.g. Sisyphus) to emit `[HANDOVER REFLECTION]` and exit with 0 file edits.
**Rationale:** Prevents silent persona demotion and guarantees OpenAgent swarm orchestrator identity integrity.
**Mechanism:** `src/tests/delegate.py`, `~/.config/opencode/oh-my-openagent.json`, and `BKM-034` in `Protocols.md`.

## [FEAT-459] Deep Thought Unified Preamble & Dynamic LLM Greeting Fusion
**Status:** UPDATED (Sprint 56)
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L1402) — Deep Thought Unified Preamble & Dynamic LLM Greeting Fusion.
**Logic:** Fuses $t=0$ HyDE vector synthesis and casual greeting preambles into a single LLM-generated JSON pass from Deep Thought on KENDER (`_spawn_deep_thought_preamble`). Replaces Python regex domain keyword checks and static `casual_reflections` string arrays, fully restoring **BKM-015** compliance ("No hardcoded string lists"). If the query is casual, Deep Thought sets `"is_casual": true` and dynamically generates a 1-sentence analytical greeting; if technical, it outputs `"is_casual": false` alongside the 3-part Composite HyDE vector. Routes preambles to `channel: "insight"` for persona partitioning.
**Rationale:** Restores BKM-015 compliance, eliminates persona bleed, and provides dynamic LLM preamble responses without adding extra inference passes.
**Mechanism:** `_spawn_deep_thought_preamble` in `HomeLabAI/src/v5/foyer/router.py` & `_HYDE_SYNTHESIS_PROMPT` in `HomeLabAI/src/logic/cognitive_hub.py`.

## [FEAT-460] Build Trailer Render Process Cleanup Trap
**Status:** COMPLETED (Sprint 54)
**Code:** [src/lab_attendant.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/lab_attendant.py#L58) — Build Trailer Render Process Cleanup Trap.
**Logic:** Adds explicit subprocess cleanup (`pkill -f 'shot-scraper|chromium'`) to `deploy_to_airlock()` in `build_site.py`.
**Rationale:** Prevents Playwright/shot-scraper headless Chromium rendering instances from lingering in RAM after static site compilation.
**Mechanism:** `deploy_to_airlock()` in `Portfolio_Dev/field_notes/build_site.py`.

## [LAB-105] SystemD Cgroup Process Management & Hardened Restart Policy
**Status:** COMPLETED (Sprint 54)
**Code:** *none found (documented only)*
**Logic:** Configures `KillMode=control-group` and `TimeoutStopSec=5` in `lab-attendant.service`.
**Rationale:** Eliminates 30-second restart delays and ensures `systemctl restart lab-attendant.service` cleanly tears down 100% of child processes, vLLM servers, and background loopers in 5 seconds max without manual `kill -9` intervention.
**Mechanism:** `/etc/systemd/system/lab-attendant.service`.

## [FEAT-461] Optional Airlock Snapshot Previews
**Status:** COMPLETED (Sprint 54)
**Code:** [field_notes/build_site.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/build_site.py#L80) — Optional Airlock Snapshot Previews.
**Logic:** Adds `--snapshots` flag to `build_site.py` and wraps shot-scraper PNG rendering in `sync_protocols.sh` and `sync_research.sh` behind `ENABLE_SNAPSHOTS=1` check.
**Rationale:** Reduces default site build time from 15s to 0.8s by disabling Playwright headless browser rendering unless explicitly requested.
**Mechanism:** `build_site.py`, `www_deploy/sync_protocols.sh`, and `www_deploy/sync_research.sh`.

## [FEAT-462] Warming Anchor Hold-The-Line Retry Loop
**Status:** COMPLETED (Sprint 54)
**Code:** [src/nodes/loader.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/loader.py#L418) — Warming Anchor Hold-The-Line Retry Loop.
**Logic:** Implements a 60-second blocking await loop inside `generate_response()` in `src/nodes/loader.py` when `ping_engine()` returns `WARMING`. Yields warming header notification once, polls `ping_engine()` every 3 seconds, and seamlessly streams the generated LLM response on the active WebSocket thread as soon as the engine signals readiness.
**Rationale:** Eliminates dead-end warming notices so prompts asked during cold-start are answered automatically without requiring user re-querying.
**Mechanism:** `generate_response()` in `HomeLabAI/src/nodes/loader.py`.

## [LAB-106] Pre-Flight SystemD Page Cache Reclamation
**Status:** COMPLETED (Sprint 54)
**Code:** *none found (documented only)*
**Logic:** Adds `ExecStartPre=-/usr/bin/sudo /usr/sbin/sysctl -w vm.drop_caches=3` to `lab-attendant.service`.
**Rationale:** Automatically reclaims 7-10 GB of dirty file page caches created by build tools before PyTorch and vLLM allocate safetensors checkpoint shards in host RAM.
**Mechanism:** `/etc/systemd/system/lab-attendant.service`.

## [LAB-107] Kernel Virtual Memory Pressure & EarlyOOM Protection Daemon
**Status:** COMPLETED (Sprint 54)
**Code:** *none found (documented only)*
**Logic:** Configures `vm.vfs_cache_pressure=150` in `/etc/sysctl.d/99-lab-memory.conf` and earlyoom daemon parameters (`-m 10 -s 5 --prefer '(chrome|steam)' --avoid '(acme_foyer_v5|vllm)'`).
**Rationale:** Forces Linux kernel to release stale directory caches before swapping memory, and configures EarlyOOM to sacrifice non-critical GUI apps if RAM drops below 10%, protecting core AI nodes from kernel I/O freezes.
**Mechanism:** `/etc/sysctl.d/99-lab-memory.conf` and `/etc/default/earlyoom`.

## [LAB-108] Multi-Remote Secondary Git Mirror (Bitbucket)
**Status:** BACKLOG
**Code:** [Portfolio_Dev/SPRINT_PLAN_SPR_58_0.md](https://github.com/kEnder242/Portfolio_Dev/blob/main/SPRINT_PLAN_SPR_58_0.md#L15) — Multi-Remote Secondary Git Mirror (Bitbucket).
**Logic:** Configures dual-push secondary Git remotes (`git remote set-url --add --push`) pointing to private Bitbucket repositories alongside GitHub origin for automated redundancy across cloud hosting providers.
**Rationale:** Protects the 18-year archive and agentic codebase against single-platform outage or provider-level account restrictions without adding manual workflow friction.
**Mechanism:** Dual-push Git remote configuration across `Portfolio_Dev` and `HomeLabAI` repositories.

## [FEAT-463] Same-Origin Tunnel Remote Control Routing & Telemetry
**Status:** COMPLETED (Sprint 56)
**Code:** [src/debug/bench_moe_plus.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/bench_moe_plus.py#L1) — Same-Origin Tunnel Remote Control Routing & Telemetry.
**Logic:** Routes Remote Control actions in `status.html` through same-origin relative endpoints (`${window.location.origin}/attendant/${action}`) when accessed via Zero Trust (`notes.jason-lab.dev`), and `http://127.0.0.1:8765/${action}` when local. Maps `path: /attendant/` -> `http://localhost:8765` in `/etc/cloudflared/config.yml` and registers native `/attendant/` route handlers in `router.py`. Logs explicit `[ERROR DIAGNOSTIC]` origin/target/key telemetry on fetch exceptions.
**Rationale:** Same-origin requests ride the active Cloudflare Access session cookie and bypass cross-domain CORS preflight checks (`OPTIONS`) and browser Mixed-Content security blocks, eliminating 100% of browser `NetworkError` and HTTP 502/302 redirects.
**Mechanism:** `triggerLabAction()` in `Portfolio_Dev/field_notes/status.html`, `setup_routes()` in `HomeLabAI/src/v5/foyer/router.py`, and `/etc/cloudflared/config.yml`.

## [FEAT-464] Live Vitals Telemetry Grid Modernization
**Status:** COMPLETED (Sprint 56)
**Code:** [field_notes/status.html](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/status.html#L1) — Live Vitals Telemetry Grid Modernization.
**Logic:** Removes obsolete 0.0% VRAM and System RAM cards from `status.html`, renames `Silicon Mode` to `Bicameral State` (`OPERATIONAL`, `HIBERNATING`, `WARMING`), defaults `Active Model` to `Llama-3.2-3B-AWQ`, and sets default `Web Intercom` status to `HIBERNATING`.
**Rationale:** Aligns vitals grid with V5 architecture state machine and removes redundant telemetry cards.
**Mechanism:** `Portfolio_Dev/field_notes/status.html`.

## [FEAT-466] Crosstalk Bar Orchestrator Error Telemetry
**Status:** COMPLETED (Sprint 56)
**Code:** [src/debug/bench_moe_plus.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/bench_moe_plus.py#L1) — Crosstalk Bar Orchestrator Error Telemetry.
**Logic:** Catches unhandled Python exceptions in `_spawn_deep_thought_preamble()` and `run_division_of_labor()` in `router.py`, and immediately broadcasts a `type: crosstalk` WebSocket error frame to the UI.
**Rationale:** Eliminates silent UI stalls by rendering backend stage/orchestrator exceptions directly in the Crosstalk Bar log container in real-time.
**Mechanism:** `_spawn_deep_thought_preamble()` and `run_division_of_labor()` in `HomeLabAI/src/v5/foyer/router.py`.
**Mechanism:** `Portfolio_Dev/FeatureTracker.md`.

## [FEAT-465] FEAT/LAB Code Mapping & Link-Drift Gate
**Status:** COMPLETED (Sprint 55)
**Code:** [field_notes/features_build.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/features_build.py#L1) — FEAT/LAB Code Mapping & Link-Drift Gate.
**Logic:** Located the code home of every FEAT/LAB entry in the Feature Tracker, added **`Code:`** git-link fields, tagged untagged ACTIVE/DESIGN features at their primary code locations, published a machine-readable feature map, and installed a link-drift verification hard gate into the site build.
**Rationale:** Eliminates untracked features and broken code references by making every feature's implementation location explicit, verifiable, and build-gated.
**Mechanism:** `field_notes/features_build.py`, `field_notes/verify_feature_links.py`, `field_notes/build_site.py`, `FeatureTracker.md` **`Code:`** fields, and `field_notes/FEATURE_CODE_MAP.md`.

## [FEAT-337] Resident Liveness Health Polling Loop
**Status:** DEFEATURED (Superseded by Hibernation Matrix to Prevent Idle Wake Thrashing)
**Code:** [src/debug/test_warm_wake.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/test_warm_wake.py#L9) — Resident Liveness Health Polling Loop.
**Logic:** Periodic 30–60s active polling (`list_tools`) to probe resident nodes. Defeatured because continuous active background polling actively prevented GPU/VRAM idle sleep and broke the Hibernation Matrix.
**Mechanism:** Replaced by on-demand error boundaries and state machine transitions.

## [FEAT-342] Ignition Reprobe & Zombie Process Scythe
**Status:** DEFEATURED (Superseded by Clean Systemd Daemon Lifecycle to Prevent Suicide Loops)
**Code:** [src/tests/test_rude_gauntlet.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/test_rude_gauntlet.py#L7) — Ignition Reprobe & Zombie Process Scythe.
**Logic:** Aggressive pre-ignition port killing and socket probing (`_synchronize_and_probe`). Defeatured because aggressive socket scything was the primary root cause of V4 suicide restart storms.
**Mechanism:** Replaced by native SystemD user units and socket-activated clean process lifecycle.

## [FEAT-339] Full-Chain Deep Smoke Diagnostics
**Status:** TODO (Integration Diagnostic Test Harness)
**Code:** [src/debug/test_foyer_resilience.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/test_foyer_resilience.py#L7) — Full-Chain Deep Smoke Diagnostics.
**Logic:** End-to-end integration diagnostic probe (`_run_deep_smoke`) that validates the entire multi-node cascade and memory footprint on demand.
**Mechanism:** Diagnostic test harness utility executed during test suites or manual lab health verification, decoupled from the live query hot-path.

## [FEAT-017] Stable Lab Bootstrapper
**Status:** ACTIVE
**Code:** [start_lab.sh](https://github.com/kEnder242/Dev_Lab/blob/main/start_lab.sh#L3) — Stable Lab Bootstrapper.
**Logic:** --- Acme Lab: Unified Bootstrapper v1.0 --- [FEAT-017] Stable Lab Bootstrapper ATTENDANT_URL="http://localhost:9999 echo "--- 🚀 INITIATING ACME LAB BOOT SEQUENCE ---
**Mechanism:** `start_lab.sh` at line 3.

## [FEAT-067.2] Attendant-Aware Ignition for Dreaming.
**Status:** ACTIVE
**Code:** [src/dream_cycle.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/dream_cycle.py#L35) — Attendant-Aware Ignition for Dreaming..
**Logic:** async def ensure_engine_ready(): [FEAT-067.2] Attendant-Aware Ignition for Dreaming. try: 1. Check Status
**Mechanism:** `src/dream_cycle.py` at line 35.

## [FEAT-072.1] Component Subsystem (FEAT-072.1)
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L1734) — Component Subsystem (FEAT-072.1).
**Logic:** brain_source": "The Brain", channel": "insight", final": True })
**Mechanism:** `src/logic/cognitive_hub.py` at line 1734.

## [FEAT-074] Workbench: Instructs the UI to open a specific file in the editor.
**Status:** ACTIVE
**Code:** [src/nodes/archive_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/archive_node.py#L417) — Workbench: Instructs the UI to open a specific file in the editor..
**Logic:** @mcp.tool() async def select_file(filename: str) -> str: [FEAT-074] Workbench: Instructs the UI to open a specific file in the editor. return json.dumps({"type": "select_file", "filename": filename})
**Mechanism:** `src/nodes/archive_node.py` at line 417.

## [FEAT-127.1] Recursive Refinement: Upgrade Tier 2 artifacts to Tier 1.
**Status:** ACTIVE
**Code:** [src/dream_cycle.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/dream_cycle.py#L127) — Recursive Refinement: Upgrade Tier 2 artifacts to Tier 1..
**Logic:** logging.info("✅ Dream Cycle Finished. The Lab has evolved.") async def run_refinement_dream(self): [FEAT-127.1] Recursive Refinement: Upgrade Tier 2 artifacts to Tier 1. logging.info("💎 Initiating Deep Refinement of t...
**Mechanism:** `src/dream_cycle.py` at line 127.

## [FEAT-147] Adaptive Residency (Dynamic load/unload).
**Status:** ACTIVE
**Code:** [src/equipment/sensory_manager.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/equipment/sensory_manager.py#L14) — Adaptive Residency (Dynamic load/unload)..
**Logic:** Encapsulates binary PCM processing and NeMo residency. Ready for [FEAT-147] Adaptive Residency (Dynamic load/unload).  def __init__(self, broadcast_callback):
**Mechanism:** `src/equipment/sensory_manager.py` at line 14.

## [FEAT-153] Collaborative Handshake Test:
**Status:** ACTIVE
**Code:** [src/test_round_table.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/test_round_table.py#L10) — Collaborative Handshake Test:.
**Logic:**  [FEAT-153] Collaborative Handshake Test: 1. Sends a strategic query. 2. Verifies the Hub coordinates Pinky and Brain.
**Mechanism:** `src/test_round_table.py` at line 10.

## [FEAT-160.1] Training Scaffolding: Unsloth Expert Forge
**Status:** ACTIVE
**Code:** [src/train/train_expert.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/train/train_expert.py#L7) — Training Scaffolding: Unsloth Expert Forge.
**Logic:** [FEAT-160.1] Training Scaffolding: Unsloth Expert Forge This script is intended for use on the 2080 Ti (local) AFTER mass_scan is complete. Configuration MODEL_NAME = "unsloth/llama-3.2-3b-instruct-bnb-4bit
**Mechanism:** `src/train/train_expert.py` at line 7.

## [FEAT-167.3] Pedigree Discovery: Scan archive for hidden CV synergy.
**Status:** ACTIVE
**Code:** [src/recruiter.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/recruiter.py#L269) — Pedigree Discovery: Scan archive for hidden CV synergy..
**Logic:** async def run_synergy_scan(self): [FEAT-167.3] Pedigree Discovery: Scan archive for hidden CV synergy. if not self.brain or not self.signatures: return
**Mechanism:** `src/recruiter.py` at line 269.

## [FEAT-175] BKM Sentinel Keywords
**Status:** ACTIVE
**Code:** [field_notes/scan_librarian.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/scan_librarian.py#L160) — BKM Sentinel Keywords.
**Logic:** Team Anchors Heuristic TEAM_TAGS = {"PIAV": "2019-2024", "PAE": "2016-2019", "MVE": "2016", "DSD": "2011-2016", "EPSD": "2005-2007"} [FEAT-175] BKM Sentinel Keywords BKM_KEYWORDS = ["root cause", "silicon failure", "v...
**Mechanism:** `field_notes/scan_librarian.py` at line 160.

## [FEAT-176] Deep-Connect Mode Detection
**Status:** ACTIVE
**Code:** [field_notes/nibble.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/nibble.py#L154) — Deep-Connect Mode Detection.
**Logic:** [FEAT-176] Deep-Connect Mode Detection is_deep_connect = task.get("mode") == "DEEP_CONNECT bucket_file = os.path.join(DATA_DIR, f"{task['bucket'].replace('-', '_')}.json") existing_data = []
**Mechanism:** `field_notes/nibble.py` at line 154.

## [FEAT-177] DNA Uplink: Harvest for Expert Forge
**Status:** ACTIVE
**Code:** [field_notes/nibble.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/nibble.py#L263) — DNA Uplink: Harvest for Expert Forge.
**Logic:** [FEAT-177] DNA Uplink: Harvest for Expert Forge if is_deep_connect: try: os.makedirs(EXPERTISE_DIR, exist_ok=True)
**Mechanism:** `field_notes/nibble.py` at line 263.

## [FEAT-179] Targeted scan for the Hallway Protocol.
**Status:** ACTIVE
**Code:** [field_notes/mass_scan.py](https://github.com/kEnder242/Portfolio_Dev/blob/main/field_notes/mass_scan.py#L175) — Targeted scan for the Hallway Protocol..
**Logic:** def hallway_protocol(keyword): [FEAT-179] Targeted scan for the Hallway Protocol. logging.info(f"=== HALLWAY PROTOCOL: Targeted Search for '{keyword}' ===") 1. Grep for matching files in raw_notes
**Mechanism:** `field_notes/mass_scan.py` at line 175.

## [FEAT-192] Verifies and optionally forces engine readiness via a generation probe.
**Status:** ACTIVE
**Code:** [src/nodes/archive_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/archive_node.py#L1328) — Verifies and optionally forces engine readiness via a generation probe..
**Logic:** @mcp.tool() async def ping_engine(force: bool = False) -> str: [FEAT-192] Verifies and optionally forces engine readiness via a generation probe. success, msg = await node.ping_engine(force=force)
**Mechanism:** `src/nodes/archive_node.py` at line 1328.

## [FEAT-206] self._probe_ttl_failure = 15   # 15 Seconds [FEAT-206]
**Status:** ACTIVE
**Code:** [src/nodes/loader.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/loader.py#L128) — self._probe_ttl_failure = 15   # 15 Seconds [FEAT-206].
**Logic:** self._engine_cache = None self._last_probe = 0 self._probe_ttl_success = 300  # 5 Minutes [FEAT-206] self._probe_ttl_failure = 15   # 15 Seconds [FEAT-206]
**Mechanism:** `src/nodes/loader.py` at line 128.

## [FEAT-212] Direct REST Priming + Hub WebSocket Probing.
**Status:** ACTIVE
**Code:** [src/debug/prime_remote_brain.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/prime_remote_brain.py#L6) — Direct REST Priming + Hub WebSocket Probing..
**Logic:** Architect Prime & Probe (B+A) [FEAT-212] Direct REST Priming + Hub WebSocket Probing. This script proves model residency on the 4090 and audits the Hub's triage turns. 
**Mechanism:** `src/debug/prime_remote_brain.py` at line 6.

## [FEAT-215] Automated Verification of the 01:00 AM - 04:00 AM sequence.
**Status:** ACTIVE
**Code:** [src/debug/lifecycle_gauntlet.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/lifecycle_gauntlet.py#L6) — Automated Verification of the 01:00 AM - 04:00 AM sequence..
**Logic:** Lifecycle Gauntlet (Shakedown Protocol v3.0) [FEAT-215] Automated Verification of the 01:00 AM - 04:00 AM sequence. [FEAT-217] Sequenced Batch Forge Verification (3 souls in 1 pass). 
**Mechanism:** `src/debug/lifecycle_gauntlet.py` at line 6.

## [FEAT-217] Sequenced Batch Forge - bypass MCP catch-22
**Status:** ACTIVE
**Code:** [src/v5/foyer/router.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/foyer/router.py#L764) — Sequenced Batch Forge - bypass MCP catch-22.
**Logic:** elif task == "forge": [FEAT-217] Sequenced Batch Forge - bypass MCP catch-22 async def _run_batch_forge(): try:
**Mechanism:** `src/v5/foyer/router.py` at line 764.

## [FEAT-227] Component Subsystem (FEAT-227)
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L1157) — Component Subsystem (FEAT-227).
**Logic:** except Exception as e: logging.error(f"[HUB] Journal ledger write failed: {e}") [FEAT-247] Physical Audit Gate async def evaluate_grounding(self, source, text, interest=0.8, shutdown_event=None, request_id="default", ...
**Mechanism:** `src/logic/cognitive_hub.py` at line 1157.

## [FEAT-232] Feedback Harvester
**Status:** ACTIVE
**Code:** [src/forge/harvest_feedback.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/forge/harvest_feedback.py#L4) — Feedback Harvester.
**Logic:** [FEAT-232] Feedback Harvester Scrapes server.log for user feedback packets and formats them for curriculum induction. FORGE_DIR = os.path.dirname(os.path.abspath(__file__)) SRC_DIR = os.path.dirname(FORGE_DIR)
**Mechanism:** `src/forge/harvest_feedback.py` at line 4.

## [FEAT-233.2] Internal Token Buffer
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L165) — Internal Token Buffer.
**Logic:** self.trigger_morning_briefing_cb = trigger_morning_briefing self.last_prime_callback = last_prime_callback self.waterfall_queue = waterfall_queue # [FEAT-233.2] Internal Token Buffer self.hibernate_callback = hibernat...
**Mechanism:** `src/logic/cognitive_hub.py` at line 165.

## [FEAT-233.5] Internal Waterfall Proxy: Handshakes the node and yields tokens.
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L470) — Internal Waterfall Proxy: Handshakes the node and yields tokens..
**Logic:** return await task [FEAT-408] Tool-Driven Waterfall Cascade async def _process_node_stream(self, node_id, query, context, source_name, tools=None, behavioral_guidance="", shutdown_event=None, interest_threshold=0.0, te...
**Mechanism:** `src/logic/cognitive_hub.py` at line 470.

## [FEAT-233.7] Real-time token ingestion from decoupled nodes.
**Status:** ACTIVE
**Code:** [src/v5/foyer/router.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/foyer/router.py#L1204) — Real-time token ingestion from decoupled nodes..
**Logic:** async def handle_stream_ingest(self, request): [FEAT-233.7] Real-time token ingestion from decoupled nodes. try: data = await request.json()
**Mechanism:** `src/v5/foyer/router.py` at line 1204.

## [FEAT-240.2] The Relay Pattern: Standard-compliant 'Thinking' turn.
**Status:** ACTIVE
**Code:** [src/nodes/loader.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/loader.py#L151) — The Relay Pattern: Standard-compliant 'Thinking' turn..
**Logic:** async def think(query: str, context: str = "", tools: list = None, behavioral_guidance: str = "", internal: bool = False, temperature: float = 0.0, repetition_penalty: float = 1.1, use_lora: bool = True, response_form...
**Mechanism:** `src/nodes/loader.py` at line 151.

## [FEAT-251.4] Simple smoke test to verify Brain/Shadow response via Hub.
**Status:** ACTIVE
**Code:** [src/debug/test_brain_smoke.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/test_brain_smoke.py#L12) — Simple smoke test to verify Brain/Shadow response via Hub..
**Logic:** async def test_brain_smoke(): [FEAT-251.4] Simple smoke test to verify Brain/Shadow response via Hub. print("--- [TEST] Brain Cognitive Smoke Test ---") try:
**Mechanism:** `src/debug/test_brain_smoke.py` at line 12.

## [FEAT-254.2] Metadata Displacement: Context shifts from system to user
**Status:** ACTIVE
**Code:** [src/nodes/loader.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/loader.py#L462) — Metadata Displacement: Context shifts from system to user.
**Logic:** system_prompt = system_override or self.system_prompt [FEAT-254.2] Metadata Displacement: Context shifts from system to user This prevents 3B models from confusing system data with their core identity. user_context = 
**Mechanism:** `src/nodes/loader.py` at line 462.

## [FEAT-255.1] Dynamic Registry: Sync engine type with status.json
**Status:** ACTIVE
**Code:** [src/nodes/loader.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/loader.py#L290) — Dynamic Registry: Sync engine type with status.json.
**Logic:** return True, "Cached [FEAT-255.1] Dynamic Registry: Sync engine type with status.json resolved_ip = self._resolve_primary_host() if self.primary_host == "localhost":
**Mechanism:** `src/nodes/loader.py` at line 290.

## [FEAT-255.3] Handshake Resilience: Tolerate ZMQ/Transfer/Connection errors during boot
**Status:** ACTIVE
**Code:** [src/nodes/loader.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/loader.py#L396) — Handshake Resilience: Tolerate ZMQ/Transfer/Connection errors during boot.
**Logic:** return True, f"Online: {target} ({engine_type}) except Exception as e: [FEAT-255.3] Handshake Resilience: Tolerate ZMQ/Transfer/Connection errors during boot err_msg = str(e).lower()
**Mechanism:** `src/nodes/loader.py` at line 396.

## [FEAT-255.4] Reactive Discovery: Flush session and cache on error
**Status:** ACTIVE
**Code:** [src/nodes/loader.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/loader.py#L408) — Reactive Discovery: Flush session and cache on error.
**Logic:** self._handshake_backoff = 2 # Reset on fatal error [FEAT-255.4] Reactive Discovery: Flush session and cache on error self._engine_cache = None self._last_probe = 0
**Mechanism:** `src/nodes/loader.py` at line 408.

## [FEAT-255.6] Exponential Backoff: Give the larynx time to clear its throat
**Status:** ACTIVE
**Code:** [src/nodes/loader.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/loader.py#L399) — Exponential Backoff: Give the larynx time to clear its throat.
**Logic:** err_msg = str(e).lower() if any(k in err_msg for k in ["transfer", "reset", "disconnected", "incomplete", "refused", "eof", "connect call failed", "cannot connect", "clientconnectorerror"]): [FEAT-255.6] Exponential B...
**Mechanism:** `src/nodes/loader.py` at line 399.

## [FEAT-255.7] Dynamic Resolution with [FEAT-265] Discovery.
**Status:** ACTIVE
**Code:** [src/nodes/loader.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/loader.py#L262) — Dynamic Resolution with [FEAT-265] Discovery..
**Logic:** def _resolve_primary_host(self): [FEAT-255.7] Dynamic Resolution with [FEAT-265] Discovery. if self.primary_host in ["localhost", "127.0.0.1", "z87-Linux"]: target = "127.0.0.1
**Mechanism:** `src/nodes/loader.py` at line 262.

## [FEAT-259.1] Global Sensory Sentinel.
**Status:** ACTIVE
**Code:** [src/v5/foyer/router.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/foyer/router.py#L1464) — Global Sensory Sentinel..
**Logic:** async def ear_poller_loop(self): [FEAT-259.1] Global Sensory Sentinel. while True: try:
**Mechanism:** `src/v5/foyer/router.py` at line 1464.

## [FEAT-265.15] Unified Boot: Trigger Ear and logical nodes concurrently based on state transitions
**Status:** ACTIVE
**Code:** [src/v5/foyer/router.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/foyer/router.py#L823) — Unified Boot: Trigger Ear and logical nodes concurrently based on state transitions.
**Logic:** [FEAT-265.15] Unified Boot: Trigger Ear and logical nodes concurrently based on state transitions if self.status.state in ["HIBERNATING", "OFFLINE"]: if self.residents.booted: logger.info(f"[FOYER] Lab state is {self....
**Mechanism:** `src/v5/foyer/router.py` at line 823.

## [FEAT-265.20] Boot Patience: Wait for Hub Foyer to open
**Status:** ACTIVE
**Code:** [src/debug/test_hibernation_cycle.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/test_hibernation_cycle.py#L86) — Boot Patience: Wait for Hub Foyer to open.
**Logic:** print("[*] STEP 3: Triggering Architect Wake via Intent...") [FEAT-265.20] Boot Patience: Wait for Hub Foyer to open foyer_up = False for _ in range(12): # 60s max wait for foyer
**Mechanism:** `src/debug/test_hibernation_cycle.py` at line 86.

## [FEAT-265.28] Physical Settle: Wait for VOCAL baseline before starting cycle
**Status:** ACTIVE
**Code:** [src/debug/test_hibernation_cycle.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/test_hibernation_cycle.py#L38) — Physical Settle: Wait for VOCAL baseline before starting cycle.
**Logic:** [FEAT-265.28] Physical Settle: Wait for VOCAL baseline before starting cycle print("[*] STEP 0: Verifying Vocal Baseline...") for _ in range(24): # 120s max try:
**Mechanism:** `src/debug/test_hibernation_cycle.py` at line 38.

## [FEAT-265.8] Ignition sequence.
**Status:** ACTIVE
**Code:** [src/v5/ignition/manager.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/ignition/manager.py#L130) — Ignition sequence..
**Logic:** async def start_lab(self, reason="INTENT"): [FEAT-265.8] Ignition sequence. if self.status.state in ["WAKING", "OPERATIONAL"]: return True
**Mechanism:** `src/v5/ignition/manager.py` at line 130.

## [FEAT-266.9] Memo Layer: Retrieves pre-synthesized observations.
**Status:** ACTIVE
**Code:** [src/nodes/archive_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/archive_node.py#L473) — Memo Layer: Retrieves pre-synthesized observations..
**Logic:** @mcp.tool() async def get_observational_memo(topic: str = None, year: str = None) -> str:  [FEAT-266.9] Memo Layer: Retrieves pre-synthesized observations.
**Mechanism:** `src/nodes/archive_node.py` at line 473.

## [FEAT-270] Track consecutive failures
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L192) — Track consecutive failures.
**Logic:** self.consecutive_parse_failures = 0 self.lora_enabled = True self.triage_failures = 0 # [FEAT-270] Track consecutive failures [FEAT-181] Semantic Integration
**Mechanism:** `src/logic/cognitive_hub.py` at line 192.

## [FEAT-286.2] Strict Latching: Only one active background prime
**Status:** ACTIVE
**Code:** [src/v5/foyer/router.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/foyer/router.py#L560) — Strict Latching: Only one active background prime.
**Logic:** [FEAT-286.2] Strict Latching: Only one active background prime if getattr(self, "_priming_in_progress", False): logger.debug("[HEALTH] Heavy Prime Bypassed: Task already in progress.") return
**Mechanism:** `src/v5/foyer/router.py` at line 560.

## [FEAT-295] Tooling Parity: Mock think instead of think
**Status:** ACTIVE
**Code:** [src/tests/test_hub_intent.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/test_hub_intent.py#L10) — Tooling Parity: Mock think instead of think.
**Logic:** pinky.call_tool = AsyncMock() [FEAT-295] Tooling Parity: Mock think instead of think pinky.list_tools = AsyncMock() pinky.list_tools.return_value = MagicMock(tools=[MagicMock(name="think")])
**Mechanism:** `src/tests/test_hub_intent.py` at line 10.

## [FEAT-296] Fast-Forward: Load and potentially reverse the queue
**Status:** ACTIVE
**Code:** [src/forge/dream_voice.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/forge/dream_voice.py#L97) — Fast-Forward: Load and potentially reverse the queue.
**Logic:** [FEAT-296] Fast-Forward: Load and potentially reverse the queue with open(REFINED_PROMPTS, "r") as f_in: all_lines = f_in.readlines() if order == "reverse":
**Mechanism:** `src/forge/dream_voice.py` at line 97.

## [FEAT-304] Protocol Hardening: Ensure logs do not corrupt the MCP JSON-RPC pipe
**Status:** ACTIVE
**Code:** [src/nodes/archive_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/archive_node.py#L14) — Protocol Hardening: Ensure logs do not corrupt the MCP JSON-RPC pipe.
**Logic:** [FEAT-304] Protocol Hardening: Ensure logs do not corrupt the MCP JSON-RPC pipe reclaim_logger(role="ARCHIVE") logger = logging.getLogger(__name__) try:
**Mechanism:** `src/nodes/archive_node.py` at line 14.

## [FEAT-307] Sanitary Filter: Redirect turn-level noise to stderr
**Status:** ACTIVE
**Code:** [src/nodes/loader.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/loader.py#L173) — Sanitary Filter: Redirect turn-level noise to stderr.
**Logic:** stream_source = self.name if not internal else None [FEAT-307] Sanitary Filter: Redirect turn-level noise to stderr This is critical to prevent logs from breaking the stdio MCP transport. import sys
**Mechanism:** `src/nodes/loader.py` at line 173.

## [FEAT-308] Component Subsystem (FEAT-308)
**Status:** ACTIVE
**Code:** [src/debug/test_vllm_crash_recovery.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/test_vllm_crash_recovery.py#L12) — Component Subsystem (FEAT-308).
**Logic:** async def test_vllm_crash_recovery(): print("[#] Starting vLLM Crash Recovery Verification [FEAT-308]") 1. Capture Initial State try:
**Mechanism:** `src/debug/test_vllm_crash_recovery.py` at line 12.

## [FEAT-309.3] Serve specific log trace files or the main log.
**Status:** ACTIVE
**Code:** [src/v5/foyer/router.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/foyer/router.py#L894) — Serve specific log trace files or the main log..
**Logic:**  [FEAT-309.3] Serve specific log trace files or the main log.  try:
**Mechanism:** `src/v5/foyer/router.py` at line 894.

## [FEAT-310] Physical Truth Scavenging: Reap any high-memory orphans (>1GB)
**Status:** ACTIVE
**Code:** [apply_fixes.py](https://github.com/kEnder242/Dev_Lab/blob/main/apply_fixes.py#L15) — Physical Truth Scavenging: Reap any high-memory orphans (>1GB).
**Logic:** old = "        # 2. Stale Identity Purge \[Task 22\] new = """        # [FEAT-310] Physical Truth Scavenging: Reap any high-memory orphans (>1GB) to ensure silicon room for the engine load. Adheres to [BKM-031]. try:
**Mechanism:** `apply_fixes.py` at line 15.

## [FEAT-320] Adaptive Priority: If a model is already running on remote Ollama, use it.
**Status:** ACTIVE
**Code:** [src/nodes/loader.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/loader.py#L219) — Adaptive Priority: If a model is already running on remote Ollama, use it..
**Logic:** def _resolve_best_model(self, available_models, engine_type, running_model=None): [FEAT-080] Dynamic selection based on host capability. [FEAT-320] Adaptive Priority: If a model is already running on remote Ollama, us...
**Mechanism:** `src/nodes/loader.py` at line 219.

## [FEAT-321] Neural Queue Fidelity Test
**Status:** ACTIVE
**Code:** [src/debug/test_queue_fidelity.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/test_queue_fidelity.py#L9) — Neural Queue Fidelity Test.
**Logic:** [FEAT-321] Neural Queue Fidelity Test LAB_DIR = "/home/jallred/Dev_Lab/HomeLabAI ATTENDANT_URL = "http://127.0.0.1:8765 STATUS_URL = "http://localhost:9001/intercom.html
**Mechanism:** `src/debug/test_queue_fidelity.py` at line 9.

## [FEAT-326] Socket Persistence: 300s heartbeat for cold-wake resilience
**Status:** ACTIVE
**Code:** [src/v5/foyer/router.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/foyer/router.py#L1069) — Socket Persistence: 300s heartbeat for cold-wake resilience.
**Logic:** async def handle_websocket(self, ws_request): [FEAT-326] Socket Persistence: 300s heartbeat for cold-wake resilience [FEAT-426] Origin Security Guard: browsers cannot set custom WS headers, so the authoritative check ...
**Mechanism:** `src/v5/foyer/router.py` at line 1069.

## [FEAT-330] Auto-wake logic
**Status:** ACTIVE
**Code:** [src/debug/dynamic_prompt_lab.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/debug/dynamic_prompt_lab.py#L25) — Auto-wake logic.
**Logic:** def run_test(config): [FEAT-330] Auto-wake logic try: attendant_status = requests.get(f"http://localhost:8765/status?key={config.get('key', '92e785ba')}", timeout=2).json()
**Mechanism:** `src/debug/dynamic_prompt_lab.py` at line 25.

## [FEAT-344] Sovereignty Gate: Suppress probes during raw silicon boot / hibernation.
**Status:** ACTIVE
**Code:** [src/v5/foyer/router.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/foyer/router.py#L481) — Sovereignty Gate: Suppress probes during raw silicon boot / hibernation..
**Logic:** [FEAT-265.31/FEAT-028] State-Aware Deep Thought probe: ping->API + Heavy Prime (GPU Wake). [FEAT-344] Sovereignty Gate: Suppress probes during raw silicon boot / hibernation. state = getattr(self.status, "state", "UNK...
**Mechanism:** `src/v5/foyer/router.py` at line 481.

## [FEAT-347] Nuclear JSON Extractor: Multi-block match for 3B resilience
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L393) — Nuclear JSON Extractor: Multi-block match for 3B resilience.
**Logic:** return None [FEAT-347] Nuclear JSON Extractor: Multi-block match for 3B resilience This handles cases where models output multiple blocks or trailing garbage. json_blocks = re.findall(r'(\{.*?\})', text, re.DOTALL)
**Mechanism:** `src/logic/cognitive_hub.py` at line 393.

## [FEAT-350] Gibberish Guard: Stable Baseline
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L189) — Gibberish Guard: Stable Baseline.
**Logic:** self.request_lock = asyncio.Lock() [FEAT-350] Gibberish Guard: Stable Baseline self.consecutive_parse_failures = 0 self.lora_enabled = True
**Mechanism:** `src/logic/cognitive_hub.py` at line 189.

## [FEAT-355] VISIBLE CONSENSUS: Use <thought> tags to debate with Pinky or Deep Thought.\n
**Status:** ACTIVE
**Code:** [src/nodes/brain_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/brain_node.py#L12) — VISIBLE CONSENSUS: Use <thought> tags to debate with Pinky or Deep Thought.\n.
**Logic:** 1. INTUITIVE REFINEMENT: Focus on grounding Pinky's enthusiasm with technical truth.\n 2. FOIL TO SOVEREIGNTY: Provide the first-pass thought trace for Deep Thought to critique.\n 3. [FEAT-355] VISIBLE CONSENSUS: Use ...
**Mechanism:** `src/nodes/brain_node.py` at line 12.

## [FEAT-361] 100% Transparency: No masking of inter-node whispers.
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L352) — 100% Transparency: No masking of inter-node whispers..
**Logic:** [NEW] Push to waterfall queue for real-time UI delivery [FEAT-361] 100% Transparency: No masking of inter-node whispers. if hasattr(self, 'waterfall_queue') and self.waterfall_queue: await self.waterfall_queue.put(data)
**Mechanism:** `src/logic/cognitive_hub.py` at line 352.

## [FEAT-365] Characterful reflexes and persistence heartbeats.
**Status:** ACTIVE
**Code:** [src/v5/foyer/router.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/foyer/router.py#L1451) — Characterful reflexes and persistence heartbeats..
**Logic:** async def reflex_loop(self): [FEAT-365] Characterful reflexes and persistence heartbeats. tics = ["Narf!", "Poit!", "Zort!", "Checking circuits...", "Egad!", "Trotro!"] while True:
**Mechanism:** `src/v5/foyer/router.py` at line 1451.

## [FEAT-367] Hardened UI Truth: Waits for physical log entries before asserting DOM.
**Status:** ACTIVE
**Code:** [src/tests/test_visibility_truth.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/test_visibility_truth.py#L8) — Hardened UI Truth: Waits for physical log entries before asserting DOM..
**Logic:**  [FEAT-367] Hardened UI Truth: Waits for physical log entries before asserting DOM. Ensures 100% voice restoration and no 'easy pass' on reflexes. 
**Mechanism:** `src/tests/test_visibility_truth.py` at line 8.

## [FEAT-434] career_compass_path = os.path.expanduser("~/Dev_Lab/Portfolio_Dev/field_notes/data/career_compass.json")
**Status:** ACTIVE
**Code:** [src/nodes/loader.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/loader.py#L93) — career_compass_path = os.path.expanduser("~/Dev_Lab/Portfolio_Dev/field_notes/data/career_compass.json").
**Logic:** logging.warning(f"[{self.name}] Liger application failed: {e}") Load Career Compass Tier 1 Anchor Map Bedrock [FEAT-434] career_compass_path = os.path.expanduser("~/Dev_Lab/Portfolio_Dev/field_notes/data/career_compas...
**Mechanism:** `src/nodes/loader.py` at line 93.

## [FEAT-445] Memory Architecture & Stability Unit Test Suite.
**Status:** ACTIVE
**Code:** [src/tests/test_memory_architecture.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/tests/test_memory_architecture.py#L2) — Memory Architecture & Stability Unit Test Suite..
**Logic:**  [FEAT-445] Memory Architecture & Stability Unit Test Suite. Verifies: 1. journal_ledger spoken-only dialogue filtering & 24h retention contract.
**Mechanism:** `src/tests/test_memory_architecture.py` at line 2.

## [FEAT-451] Brain Persona Spec (Positive persona grounding, shares Brain's right-hemisphere personality)
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L68) — Brain Persona Spec (Positive persona grounding, shares Brain's right-hemisphere personality).
**Logic:** return refined [FEAT-451] Brain Persona Spec (Positive persona grounding, shares Brain's right-hemisphere personality) BRAIN_PERSONA_SPEC = ( [PERSONA]: You are Deep Thought - the Brain's pre-conscious analytical stre...
**Mechanism:** `src/logic/cognitive_hub.py` at line 68.

## [FEAT-454] Component Subsystem (FEAT-454)
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L1477) — Component Subsystem (FEAT-454).
**Logic:** self._rag_cache[cache_key] = result_text if len(self._rag_cache) > 128: self._rag_cache.pop(next(iter(self._rag_cache))) except Exception as e:
**Mechanism:** `src/logic/cognitive_hub.py` at line 1477.

## [FEAT-455] Zero-Latency Un-blocked Async Preamble: the receive
**Status:** ACTIVE
**Code:** [src/v5/foyer/router.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/foyer/router.py#L1132) — Zero-Latency Un-blocked Async Preamble: the receive.
**Logic:** req_id = data.get("request_id") [FEAT-455] Zero-Latency Un-blocked Async Preamble: the receive loop must return instantly — never await file I/O or the broadcast inline. The Deep Thought preamble + enqueue run as
**Mechanism:** `src/v5/foyer/router.py` at line 1132.

## [FEAT-470] Legacy backfill: alias Deep Thought -> "brain" only when the local
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L613) — Legacy backfill: alias Deep Thought -> "brain" only when the local.
**Logic:** }) self.turn_thought_trace[node_id] = full_text if node_id == "thought": [FEAT-470] Legacy backfill: alias Deep Thought -> "brain" only when the local
**Mechanism:** `src/logic/cognitive_hub.py` at line 613.

## [LAB-010] Lazy import — M5 Air may not be available at startup.
**Status:** ACTIVE
**Code:** [src/v5/foyer/router.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/foyer/router.py#L35) — Lazy import — M5 Air may not be available at startup..
**Logic:** [LAB-010] Lazy import — M5 Air may not be available at startup. try: from nodes.mlx_judge_node import MLXAsyncJudge as _MLXAsyncJudge _mlx_judge = _MLXAsyncJudge()
**Mechanism:** `src/v5/foyer/router.py` at line 35.

## [LAB-088] Component Subsystem (LAB-088)
**Status:** ACTIVE
**Code:** [src/equipment/sensory_manager.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/equipment/sensory_manager.py#L51) — Component Subsystem (LAB-088).
**Logic:** EarNode taking a break to free up VRAM when system is low on RAM or in Swarm/Heads-Down mode. Preserves CUDA context for quick rearming. [LAB-088]  if not self.ear:
**Mechanism:** `src/equipment/sensory_manager.py` at line 51.

## [LAB-095] TTL Sweeper: Clean orphaned pending_chunks keys inactive > 30 seconds
**Status:** ACTIVE
**Code:** [src/v5/foyer/maintenance_sweeper.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/foyer/maintenance_sweeper.py#L60) — TTL Sweeper: Clean orphaned pending_chunks keys.
**Logic:** Safely pops stale entries from `pending_chunks` and `chunk_timestamps` without KeyError.
**Mechanism:** `MaintenanceSweeper.prune_ttl_buffer()` in `src/v5/foyer/maintenance_sweeper.py` at line 60.

## [LAB-096] Heap Scavenger: Periodic garbage collection every 60s
**Status:** ACTIVE
**Code:** [src/v5/foyer/maintenance_sweeper.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/foyer/maintenance_sweeper.py#L48) — Heap Scavenger: Periodic garbage collection.
**Logic:** Executes `gc.collect()` periodically and logs collected unreachable objects.
**Mechanism:** `MaintenanceSweeper.run_heap_scavenger()` in `src/v5/foyer/maintenance_sweeper.py` at line 48.

## [LAB-099] Thermal Guard: Monitor CPU package thermal zones (thermal_zone0 / thermal_zone3)
**Status:** ACTIVE
**Code:** [src/v5/foyer/maintenance_sweeper.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/v5/foyer/maintenance_sweeper.py#L16) — Thermal Guard: Monitor CPU package thermal zones.
**Logic:** Reads sysfs thermal zones, detects when CPU exceeds 78°C threshold, and triggers 15s cooldown sleep.
**Mechanism:** `MaintenanceSweeper.check_cpu_thermal_throttle()` in `src/v5/foyer/maintenance_sweeper.py` at line 16.

## [LAB-109] Silicon Power Capping & Hardware Surge Protection
**Status:** DESIGN
**Code:** [src/infra/nightly_forge.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/infra/nightly_forge.py#L30) — Silicon Power Capping.
**Logic:** Enforce 165W power limit on RTX 2080 Ti to eliminate di/dt transient voltage drops that trip host PSU.
**Mechanism:** `nvidia-smi -pl 165` hardware limit check during pre-flight in `nightly_forge.py`.

## [FEAT-452] Unsloth Gradient Smoothing & Hardware Pacing
**Status:** DESIGN
**Code:** [src/forge/train_expert.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/forge/train_expert.py#L20) — Hardware Pacing & Smoothing.
**Logic:** HardwarePacingCallback (50ms inter-step delay), micro-batching (batch_size=1, grad_accum=4, warmup=10, max_seq_length=1536) to pace compute bursts.
**Mechanism:** Unsloth Trainer argument configuration and callback in `src/forge/train_expert.py`.

## [FEAT-453] Post-Maintenance Autonomous Morning Re-ignition
**Status:** DESIGN
**Code:** [src/infra/nightly_forge.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/infra/nightly_forge.py#L180) — Post-Maintenance Re-ignition.
**Logic:** Guarantees Foyer and vLLM are automatically re-ignited to OPERATIONAL post 05:40 AM dreaming cycle.
**Mechanism:** `re_ignite_vllm()` called unconditionally at conclusion of nightly forge orchestration.

## [FEAT-454] Universal Epistemic 5-Question Evaluation Battery
**Status:** ACTIVE
**Code:** [src/curator/scan_curator.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/curator/scan_curator.py#L25) — Universal Epistemic 5-Question Evaluation Battery.
**Logic:** Replaces subjective 1-5 integer scoring with 5 deterministic boolean checks (exact identifiers, reproduction recipe, cause-and-effect isolation, actionable BKM, zero fluff).
**Mechanism:** `evaluate_gem_quality()` calculates deterministic Rank = min(5, 1 + sum(bool)). Verified via `src/tests/test_binary_evaluator_unit.py`.

## [FEAT-455] AST Context Compiler for Agent Context Compaction
**Status:** ACTIVE
**Code:** [src/compiler/context_compiler.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/compiler/context_compiler.py#L30) — AST Context Compiler.
**Logic:** Compiles Python codebases into structured AST symbol graphs and cross-module dependency trees, stripping implementation bodies to achieve >50% token compaction.
**Mechanism:** `ContextCompiler` using stdlib `ast` in `src/compiler/context_compiler.py`. Verified via `src/tests/test_context_compiler.py`.

## [FEAT-456] Language-First Co-Pilot Feedback Loop (The Fourth Wall / BKM-035)
**Status:** ACTIVE
**Code:** [src/logic/feedback_interceptor.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/feedback_interceptor.py#L22) — Feedback Interceptor.
**Logic:** Intercepts conversational corrections semantically, auto-populates `validation_ledger.jsonl` with FAIL records and user ground-truth, and returns in-character refinement follow-ups.
**Mechanism:** `FeedbackInterceptor` wired into `CognitiveHub.process_query()`. Verified via `src/tests/test_feedback_interceptor.py`.

## [FEAT-457] Single-Layer Speculative Context Pre-fetching
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L1081) — Speculative Context Pre-fetching.
**Logic:** Pre-fetches RAG context in background during Turn 1 streaming; consumes instantly if interest >0.5 or cleanly preempts without GPU penalty.
**Mechanism:** Async background task in `_process_turn()` and consumption in `_run_brain_leg()`. Verified via `src/tests/test_interest_speculative_prefetch.py`.

## [FEAT-458] Conversational WYWO & Floating Validation Oracle
**Status:** ACTIVE
**Code:** [src/logic/floating_oracle.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/floating_oracle.py#L42) — Floating Validation Oracle.
**Logic:** Assembles ambient validation scars, mass-scan milestones, and subconscious dreams into a floating candidate pool for organic, temperature-steered conversation turns.
**Mechanism:** `FloatingOracle` wired into `CognitiveHub._process_turn()`. Verified via `src/tests/test_floating_oracle.py`.

## [LAB-110] Permanent Daytime Node Residency
**Status:** ACTIVE
**Code:** [config/infrastructure.json](https://github.com/kEnder242/HomeLabAI/blob/main/config/infrastructure.json#L2) — Permanent Daytime Node Residency.
**Logic:** Disables daytime idle timeouts (idle_eviction_enabled: false) to keep resident nodes and AWQ models permanently warm in memory, reserving VRAM flush exclusively for 2:00 AM maintenance.
**Mechanism:** Configuration in `infrastructure.json` honored by Foyer router.

## [FEAT-467] Gated On-Demand RAG & Zero Context Default
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L800) — Gated On-Demand RAG & Zero Context Default.
**Logic:** Implements the "Zero Context > Default Context" rule via gated on-demand retrieval. RAG defaults to zero context (no speculative retrieval) unless explicit anchors, named components, or historical tags are called out. Automatically scrubs literal angle brackets (`<...>`) and few-shot template placeholders before vector search.
**Rationale:** Prevents models from hallucinating 2018 Intel Federal PAE history when answering general conversational questions while preserving surgical search when explicitly requested.
**Mechanism:** `CognitiveHub._process_turn()`, `ArchiveNode.get_context()`, `triage_engine`, and `test_sprint61_integration.py`.

## [FEAT-468] Multi-Agent Speaker Demarcation & Echo-Chamber Shield
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L700) — Multi-Agent Speaker Demarcation.
**Logic:** Tags conversation history turns with structured multi-agent speaker roles (`[USER: Jason]`, `[ASSISTANT: Brain]`, `[ASSISTANT: Pinky]`). Gates Triage intent extraction to process exclusively the latest `[USER]` turn, while preserving self-awareness of what Pinky and Brain stated in previous turns.
**Rationale:** Eliminates echo-chamber feedback loops where the system mistakes Pinky's previous turn (*"vital signs"*) for the user's intent without sacrificing conversational memory.
**Mechanism:** `CognitiveHub._process_turn()`, `triage_engine`, and `test_sprint61_integration.py`.

## [FEAT-469] Epistemic Meta-Grounding: Feature DNA & Lab Infrastructure Lexicon
**Status:** ACTIVE
**Code:** [src/nodes/archive_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/archive_node.py#L783) — Epistemic Meta-Grounding.
**Logic:** Grafts Acme Lab's internal live catalog (`feature_dna` and `lab_infrastructure`) into the RAG routing priority when `vibe="META"` or `domain="lab_internal"` is detected. Explicitly excludes `behavioral_dna` (which is reserved for AGY orchestrator development) and suppresses `career_ledger` during system operations.
**Rationale:** Allows Pinky and Brain to discuss live software modules (`AudioPipeline`, `MaintenanceSweeper`, `OverrideParser`) as active lab operators without roleplaying development commit hooks.
**Mechanism:** `ArchiveNode.get_context()`, `lab_dna_router`, and `test_sprint61_integration.py`.

## [FEAT-470] Cartoon Roleplay Critic & Actionable Technical Summary
**Status:** ACTIVE
**Code:** [src/nodes/pinky_node.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/nodes/pinky_node.py#L1) — Cartoon Roleplay Critic & Summary.
**Logic:** Replaces robotic boilerplate praise (`"A well-crafted response..."`) with a dual-output critic phase: 1) a witty, satirical Pinky cartoon quip reacting to Brain's complexity, and 2) a concise 1-sentence technical summary agreement. Demarcates raw evaluation JSON to `CROSSTALK` while streaming the quip/summary to `CHAT`.
**Rationale:** Restores authentic Pinky & The Brain cartoon dynamics while delivering high-value conversational takeaways.
**Mechanism:** `PinkyNode` critic prompt, `pinky_critic_persona.py`, `CognitiveHub.evaluate_grounding()`, and `test_sprint61_integration.py`.

## [FEAT-471] Dynamic Speaker Registry & Prefix Sanitization Gate
**Status:** ACTIVE
**Code:** [src/logic/cognitive_hub.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/cognitive_hub.py#L700) — Dynamic Speaker Registry & Sanitizer.
**Logic:** Compiles a dynamic runtime regex pattern from registered active personas (`Pinky`, `Brain`, `Deep Thought`, `Archive`, `Lab`, `User`, `Jason`, `Assistant`, `System`, `Me`) to strip nested and dirty leading speaker/role prefixes from generated LLM outputs before WebSocket broadcast.
**Rationale:** Eliminates hardcoded regex maintenance debt and prevents UI name stacking thrash (`Pinky: [ASSISTANT: Pinky]...`) while scaling automatically as new agent personas are added to the lab.
**Mechanism:** `SpeakerRegistry` in `src/logic/triage_engine.py` and `test_sprint61_integration.py`.

## [FEAT-472] Dynamic Route Incubation & Solidification Pipeline
**Status:** DESIGN (Sprint 62)
**Code:** [src/logic/triage_engine.py](https://github.com/kEnder242/HomeLabAI/blob/main/src/logic/triage_engine.py#L1) — Dynamic Route Incubation & Solidification.
**Logic:** Three-tier declarative routing system featuring immutable core policy (`config/triage_policy.json`), mouse-owned supplementary playground (`config/triage_supplement.json`), and a lifecycle promotion mechanism for mouse-discovered triage routes based on live evaluation provenance.
**Rationale:** Allows resident models to dynamically map and incubate candidate routes in a sandbox without risking mutation or corruption of production routing rules.
**Mechanism:** `TriageEngine`, `triage_policy.json`, `triage_supplement.json`, and `test_route_incubation.py`.

## [LAB-111] Removable USB FOB Kernel BDI Isolation & Auto-Mount Protection
**Status:** ACTIVE
**Code:** [docs/Protocols.md](https://github.com/kEnder242/HomeLabAI/blob/main/docs/Protocols.md#BKM-033) — Removable USB FOB Kernel BDI Isolation.
**Logic:** Neutralizes kernel I/O deadlocks and D-state thread stalls caused by persistent USB flash drives (e.g., ASUS BIOS Flashback FOB). Employs a three-layer defense: 1) Udev `UDISKS_IGNORE="1"` rule preventing desktop auto-mounts with the slow `flush` penalty, 2) `/etc/fstab` on-demand user mount without `flush` (`noauto,user,noatime`), and 3) Kernel Backing Device Info (BDI) throttling on all USB storage (`max_ratio=1`, `strict_limit=1`) to prevent dirty RAM writeback backlogs from stalling global `sync()`.
**Rationale:** 100% of historical unclean shutdowns (30/30 boots in August 2026) correlated to FAT filesystem dirty-bit stalls on `/dev/sdf1` during background system sync and workspace scans.
**Mechanism:** Udev rules `90-usb-bdi-throttle.rules`, `99-bios-flashback-ignore.rules`, `/etc/fstab`, and `/etc/updatedb.conf`.


