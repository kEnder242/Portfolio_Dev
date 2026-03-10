# Feature Tracker: The DNA Association Matrix
**Role: [FEAT] Technical Capabilities | [VIBE] Persona & Style**

> [!IMPORTANT]
> **PURPOSE:** This is the relational hub mapping the Lab's logic to silicon.
> **[FEAT]**: Hardcoded logic, technical tools, and software-level functions.
> **[VIBE]**: Node personalities, interaction flavor, and cognitive styles.

---

## [FEAT-152] Metabolism of Presence
**Status:** ACTIVE (TRANSFORMING)
**Logic:** Replaces Banter Decay. Dynamically shifts Pinky's cognitive mode based on session interaction density.
**Rationale:** Simple frequency decay was too system-noisy. Mode-based scaling allows Pinky to remain a constant presence while shifting focus between "Collaborative Frame" (High Activity) and "Literal Grounding" (Idle).
**Modes:**
1.  **High-Activity (Collaborative):** Pinky frames and pre-fills Brain's strategic derivations.
2.  **Idle (Literal Grounding):** Pinky focuses on literal hardware vitals and AYPWIP-style "I think so Brain, but..." absurdity.
**Mechanism:** Hub state variable `metabolism` influencing node system prompts via situational hint injection.

## [FEAT-153] The Resonant Chamber (Shared Context)
**Status:** ACTIVE
**Logic:** Replaces [FEAT-068] Persona-Locked Dispatch. Moves from isolation to "Overhearing."
**Rationale:** Rigid isolation prevented cross-hemispheric synergy. This feature allows nodes to "overhear" Hub-level strategic intent before generation.
**Mechanism:** Hub injects the results of the Brain's "Strategic Signal" (FEAT-028) directly into Pinky's context window *before* dispatching the final turn. 

## [FEAT-030] Unity Pattern (Multi-LoRA Residency) [SCAR #5]
**Status:** ACTIVE
**Logic:** Run all concurrent local nodes (Pinky, Shadow Brain, Lab Actor) on a shared **Unified 3B Base Model** footprint. 
**Rationale:** To maximize VRAM efficiency on the 11GB 2080 Ti. By sharing the base weights, we only pay the VRAM penalty once, while switching \"personalities\" through low-overhead LoRA adapters.
**SCAR #5:** Windows Isolation. Windows (Node 'Brain') remains Sovereign and decoupled from Linux model sync.
**Mechanism:** vLLM 0.16.0 with `--enable-lora` support for dynamic adapter switching.

## [FEAT-154] Environmental Awareness Node (The Lab Actor)
**Status:** ACTIVE (UNITY-ALIGNED)
**Logic:** The "Lab" is a first-class LLM resident running on the **Unified 3B Base**.
**Rationale:** To maintain [FEAT-030] Unity compliance. The Lab Actor shares the same VRAM footprint as Pinky and the Shadow Brain, ensuring zero additional memory overhead.
**Mechanism:** A specialized, low-latency LoRA adapter (`lab_sentinel_v1`) that transforms the 3B base into a situational auditor. It "hears" user input + hardware telemetry and outputs high-level coordination hints (e.g. `[EXIT_LIKELY]`, `[STRATEGIC]`) to the other nodes.

## [FEAT-155] Sovereign Ultra Sovereignty (Qwen 27B)
**Status:** ACTIVE
**Logic:** High-fidelity reasoning on **KENDER** (4090) using the Claude-distilled Qwen 27B model.
**Rationale:** 8B models lack the "Logic Glue" for high-fidelity synthesis. 27B distilled model maintains complex reasoning chains and high instructional adherence.
**Rule:** Unified residency. This model handles BOTH strategic chat and nightly synthesis tasks to maintain logic continuity. No active swapping required during sessions.

## [FEAT-039] [DEFEATURED] Banter Decay (Adaptive Reflex)
**Status:** DEFEATURED (Feb 2026)
**Reason:** Replaced by [FEAT-152] (Metabolism of Presence). Frequency-based idling was too system-noisy.

## [FEAT-054] [DEFEATURED] Banter Decay Test
**Status:** DEFEATURED (Feb 2026)
**Reason:** Simulation for frequency decay is obsolete.

## [FEAT-047] [DEFEATURED] Reflex Tics
**Status:** DEFEATURED (Feb 2026)
**Reason:** Replaced by Mode-Aware Grounding in [FEAT-152].

## [FEAT-068] [DEFEATURED] Persona-Locked Dispatch (The Iron Gate)
**Status:** DEFEATURED (Feb 2026)
**Reason:** Rigid isolation prevented the "Collaborative Turn" required for emergent thought. Replaced by [FEAT-153].

## [FEAT-033] [DEFEATURED] Iron Gate (Persona Isolation)
**Status:** DEFEATURED (Feb 2026)
**Reason:** isolation prevented collaborative synthesis. Replaced by [FEAT-153].

## [FEAT-028] Strategic Ping (Generation Probe)
**Status:** ACTIVE
**Logic:** Functional Logic Verification verifying the *Mind* is alive (not just the process).
**Mechanism:** Single-token generation probe in `acme_lab.py` to trigger Brain-to-Shadow failover.

## [FEAT-023] The Stoic Strategist (Identity Anchor)
**Status:** ACTIVE (RE-GROUNDED)
**Logic:** Brain is the "Stoic Reasoner" (Opus Distillation); Pinky is the "Intuitive Foil" (AYPWIP literalism). 
**Verification:** `src/debug/test_persona_bugs.py`.

## [FEAT-036] VRAM Guard (Conscious Attendant) [SCAR #1]
**Status:** ACTIVE
**Logic:** A "Deep Sleep" protocol that stubs the Brain/Pinky nodes if VRAM pressure exceeds critical thresholds (95%) or engines fail to load.
**SCAR #1:** Feb 20 "Aggressive Healing" collision during 550 driver install. Resolved via [FEAT-138].
**Mechanism:** `vram_watchdog_loop` in `lab_attendant.py`.
**Verification:** `src/test_vram_guard.py`.

## [FEAT-037] Hierarchical Mind (The Architect)
**Status:** ACTIVE (Dormant)
**Logic:** A specialized node (`architect_node.py`) capable of generating BKMs and building semantic maps of the archive.
**Mechanism:** `generate_bkm` and `build_semantic_map` tools.
**Note:** Code exists but active utilization in the loop is currently low.

## [FEAT-038] Nightly Recruiter
**Status:** ACTIVE
**Logic:** An automated logic path that matches the CV summary against cached job descriptions or recruiter queries.
**Verification:** `src/test_recruiter.py` (Verify existence).

## [FEAT-053] Contextual Tics
**Status:** ACTIVE
**Logic:** Updates `monitor_task_with_tics` to provide Brain-health-specific feedback (e.g., \"Resonating weights\", \"Sovereign unreachable\") during long reasoning tasks.

## [FEAT-055] Manual Task Trigger (Fast Alarm)
**Status:** ACTIVE
**Logic:** Adds `--trigger-task` flag to `acme_lab.py` to allow immediate execution of scheduled jobs (Recruiter/Architect) for debugging.

## [FEAT-066] The \"Temporal Moat\" (Context Aging)
**Status:** ACTIVE
**Logic:** Dynamically scales the `reflex_ttl` based on interaction density. As the Lab stays idle, the \"metabolism\" slows down (1s to 6s), allowing the system to settle without losing character presence.

## [FEAT-067] Diamond Dreaming (Subconscious Consolidation)
**Status:** ACTIVE
**Logic:** A background process (`dream_cycle.py`) that periodically synthesizes chaotic interaction logs into high-density \"Diamond Wisdom\" paragraphs.
**Mechanism:** Employs a cross-host fallback (Windows 4090 -> Local 2080 Ti) to ensure memory evolution even during partial outages.

## [FEAT-069] Silicon-Aware Adaptive Runtime (Resilience Ladder) [SCAR #2]
**Status:** ACTIVE
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
**Logic:** If a reasoning node attempts to use an unknown or hallucinated tool, the orchestrator intercepts the error and shunts it back to the Pinky Gateway for characterful recovery and user feedback.

## [FEAT-064] Static Site Synthesis (build_site.py)
**Status:** ACTIVE
**Logic:** Automated pipeline that clears caches and prepares the `www_deploy` directory for public hosting.
**Mechanism:** Runs `python3 field_notes/build_site.py` to trigger versioned cache-busting and asset bundling.

## [FEAT-065] Cross-Platform Synchronization
**Status:** ACTIVE
**Logic:** Shell-based synchronization (`sync_to_linux.sh`, `sync_to_windows.sh`) using `rsync` and Google Drive mounts to maintain code parity across the hybrid lab.

## [FEAT-062] Protocol Handshake (Version Sync)
**Status:** ACTIVE (Passive)
**Logic:** CLI and Web clients send a `handshake` packet with their local `VERSION` string upon connection. 
**Mechanism:** Orchestrator logs the client version and responds with its own server-side `VERSION` in the initial `status` broadcast.

## [FEAT-063] Cache-Busting Deployment
**Status:** ACTIVE
**Logic:** Uses query-string versioning (e.g., `script.js?v=fc6916a8`) in `intercom.html` to force browsers and Cloudflare to bypass stale caches during infrastructure updates.

## [FEAT-058] Strategic Console Routing
**Status:** ACTIVE
**Logic:** Intercom UI (`intercom_v2.js`) distinguishes between \"TRUE Brain\" messages and \"Brain (Shadow)\" predictions.
**Mechanism:** Shadow predictions and true insights route to the Brain's Insight panel, while triage/banter stays in Pinky's console.
**Verification:** `field_notes/tests/routing_test.html`.

## [FEAT-059] Real-Time PCM Audio Streaming
**Status:** ACTIVE
**Logic:** Browser-based voice capture downsamples audio to 16kHz mono and converts to Signed Int16 PCM before WebSocket streaming.
**Verification:** `src/debug/test_web_binary.py`.

## [FEAT-076] Sovereign Response Verification
**Status:** ACTIVE
**Logic:** A multi-layered test suite that verifies the Brain's reasoning capacity and its primary-to-fallback lifecycle.
**Verification:** 
- `src/debug/test_pi_flow.py`: Verifies end-to-end technical accuracy and bicameral delegation.
- `src/test_lab_integration.py`: Verifies node-to-orchestrator connectivity and life-cycle management.

## [FEAT-075] Content Immutability (The 18-Year Lock)
**Status:** ACTIVE (Mandate)
**Logic:** Explicitly protects technical narrative assets (e.g., `stories.html`) from LLM-driven \"summarization\" or truncation.
**Rule:** Structural UI updates (CSS/JS/Sidebar) are allowed, but paragraph-level content must remain 100% word-faithful to the original 18-year engineering history.
**Verification:** Manual `diff` and word-count checks during UI refactors.

## [FEAT-060] Multi-Pane Workspace (EasyMDE)
**Status:** ACTIVE
**Logic:** Integrated Markdown editor with live WebSocket save/load and resizable split-pane layout.
**Verification:** `src/test_draft_agency.py`.

## [FEAT-056] MIB Memory Wipe (Neuralyzer)
**Status:** ACTIVE
**Logic:** Allows user to manually clear the interaction context using trigger phrases like \"Look at the light\" or \"Neuralyzer\".
**Mechanism:** Resets `self.recent_interactions` in `acme_lab.py`.
**Verification:** `src/debug/test_mib_wipe.py`.

## [FEAT-057] Deep Context (Amnesia Removal)
**Status:** ACTIVE
**Logic:** Removed amnesic slicing (`[-3:]`) and increased interaction cap from 10 to 50, providing Pinky with deep mid-term memory.
**Verification:** `src/debug/test_mib_wipe.py`.

## [FEAT-043] Dead-Man's Switch
**Status:** ACTIVE
**Logic:** Triggers a `CRITICAL` alert to `pager_activity.json` if the Lab port 8765 is unresponsive for more than 5 minutes, signaling unrecoverable failure.

## [FEAT-048] Monitor Task with Tics
**Status:** ACTIVE
**Logic:** Sends periodic \"Thinking...\" updates to the user during long-running Brain reasoning tasks to provide progress feedback.

## [FEAT-049] Scheduled Tasks (Alarm Clock)
**Status:** ACTIVE
**Logic:** Background loop that triggers automated jobs: Nightly Recruiter (02:00 AM) and Hierarchy Refactor (03:00 AM).

## [FEAT-050] Strategic Vibe Check on Save
**Status:** ACTIVE
**Logic:** Automatically triggers a Brain-level validation of technical logic and architectural advice whenever a file is saved in the workspace.

## [FEAT-031] Logger Isolation (The Montana Fix)
**Status:** ACTIVE
**Logic:** Hardens the Lab against stdout/stderr hijacking by asynchronous libraries.
**Mechanism:** 
1.  **Redirection**: Routes `acme_lab.py` and `loader.py` logging to `sys.stderr`.
2.  **Reclamation**: Employs `reclaim_logger()` to strip global handlers after heavy imports (NeMo, ChromaDB).
**Verification:** `src/debug/test_forensic_logging.py`.

## [FEAT-133] Staged Resident Ignition (Sequencing)
**Status:** ACTIVE
**Logic**: Prevents initialization deadlocks and VRAM spikes by serializing the boot sequence of inference nodes.
**Mechanism**:
1.  **Serialization**: The orchestrator loads nodes sequentially: `archive` -> `pinky` -> `brain`.
2.  **Staggered Sleep**: Enforces a mandatory 2-second delay between node starts to allow the event loop and memory buffers to stabilize.
**Verification**: `src/test_liveliness.py` (Verify sequential ready states).

## [FEAT-032] Strategic Sentinel (Amygdala Filter)
**Status:** ACTIVE
**Logic:** Dual-gated input filter. Voice mode uses keyword sentinel (strat_keys); Typing mode uses 1B model (stubbed) to prevent casual clutter.
**Mechanism:** `self.mic_active` toggle in `acme_lab.py`.

## [FEAT-034] Barge-In Logic (Interrupts)
**Status:** ACTIVE
**Logic:** Allows user to cancel long reasoning cycles using voice interrupt keys ("wait", "stop", "hold on", "shut up").
**Mechanism:** `ear_poller` loop in `acme_lab.py`.

## [FEAT-035] Zombie Port Recovery
**Status:** ACTIVE
**Logic:** The Lab Attendant monitors port 8765. If the process is alive but the port is unresponsive for 3 intervals, it triggers an autonomous engine swap.
**Mechanism:** `vram_watchdog_loop` in `lab_attendant.py`.

## [FEAT-030] Unity Pattern (Multi-LoRA Residency) [SCAR #5]
**Status:** ACTIVE
**Logic:** Run all concurrent resident nodes (Pinky, Brain, Architect, Archive) on a shared **Unified Base Model** footprint. 
**SCAR #5:** Windows Isolation. Windows (Node 'Brain') does NOT need to sync with Linux models. Attempting to force identical weight sets across the bridge is a performance trap.
**Mechanism:** vLLM 0.16.0 with `--enable-lora`.

## [FEAT-071] Internal Debate (Offline Collaboration)
**Status:** ACTIVE
**Logic:** Logic allowing nodes to exchange 3-5 turns of dialogue on a specific topic without user input. 
**Mechanism:** `InternalDebate` class in `src/internal_debate.py`.

## [FEAT-072] Morning Briefing
**Status:** ACTIVE
**Logic:** Pinky summarizes the \"Nightly Dialogue\" or \"Dream Synthesis\" upon the user's first connection of the day.

## [FEAT-073] Insight Pruning (Curated Redaction)
**Status:** ACTIVE
**Logic:** A surgical tool in the Archive Node (`prune_insights`) that allows for pattern-based trimming of note summaries within a date range.
**Constraint:** Follows the \"trim, don't rewrite\" mandate, using regex to replace specific strings (like last names) while preserving technical context.

## [FEAT-080] Dynamic Model Fluidity
**Status:** ACTIVE
**Logic:** Dynamically selects the best available model on a host by querying `/api/tags`.
**Mechanism:** `_resolve_best_model` in `loader.py` matches host capabilities against a prioritized preference list.

## [FEAT-081] Hemispheric Decoupling
**Status:** ACTIVE
**Logic:** Allows Brain and Pinky to use host-appropriate models independently.
**Mechanism:** `lab_attendant.py` sets `BRAIN_MODEL` and `PINKY_MODEL` environment variables based on host affinity (KENDER vs Local).

## [FEAT-082] Neural Priming
**Status:** ACTIVE
**Logic:** Proactively loads the selected model into VRAM upon WebSocket connection.
**Mechanism:** Triggers an immediate `check_brain_health` probe with `num_predict: 1` in `acme_lab.py` during the handshake.

## [FEAT-083] Smaller Sovereign (8B Priority)
**Status:** ACTIVE
**Logic:** Prioritizes 8B class models (Llama 3.1) over large models (Mixtral) to guarantee <10s load times.
**Verification:** Forensic logs confirm `llama3.1:8b` selection on KENDER despite LARGE tier request.

## [FEAT-084] Neural Persistence (Resolution Cache)
**Status:** ACTIVE
**Logic:** Caches the resolved engine/model mapping for 60 seconds to eliminate per-query network overhead.
**Mechanism:** `_engine_cache` in `loader.py` with automatic invalidation on request failure.

## [FEAT-085] Intelligent Keep-Alive
**Status:** ACTIVE
**Logic:** Proactively primes the Brain every 2 minutes only while a client is connected.
**Mechanism:** Conditional generation probes in `acme_lab.py` ensure the model remains resident in VRAM during active sessions.

## [FEAT-086] Tiered Brain Response (Preamble)
**Status:** ACTIVE
**Logic:** Provides sub-second feedback for deep strategic tasks by broadcasting an immediate \"Thinking...\" message.
**Mechanism:** Hardcoded async broadcast in `acme_lab.py` triggered before shunting to the reasoning node.

## [FEAT-087] Intelligent Handshake Priming
**Status:** ACTIVE
**Logic:** Forces VRAM residency of the primary model upon first connection.
**Mechanism:** High-priority generation probe (`force=True`) inside the `handshake` packet handler in `acme_lab.py`.

## [FEAT-088] Semantic Career Recall
**Status:** DORMANT (Requires ChromaDB)
**Logic:** The fundamental ability to query 18 years of technical history via natural language (e.g., \"What did I do in 2019?\").
**Mechanism:** Vector search via ArchiveNode bridging the local JSON logs to the reasoning nodes.

## [FEAT-089] Zero Trust Guest Expansion
**Status:** ACTIVE
**Logic:** Securely allows authorized third-party recruiters (e.g., from `intel.com`) to access the technical lobby.
**Mechanism:** Cloudflare Access Policy updates for `notes.jason-lab.dev` and `acme.jason-lab.dev`.

## [FEAT-090] Non-Blocking Parallel Dispatch
**Status:** ACTIVE (HYBRID)
**Logic:** Stream components individually to the UI for "Live Feedback" [VIBE-002], but bundle them in the `conversations.log` for unified turn history.
**Mechanism:** Node responses are broadcast to the user as they finish using `asyncio.as_completed` (or parallel handlers), allowing Pinky's fast replies to appear instantly while Brain calculates.

## [FEAT-091] Tiered Thinking (Shallow Mode)
**Status:** ACTIVE
**Logic:** Dynamically selects reasoning depth based on intent and direct address.
**Mechanism:** `shallow_think` tool in Brain node uses a laconic system prompt and low token cap for greetings and quips, while `deep_think` handles strategic complexity.

## [FEAT-092] Persona De-personalization (Cognitive Firewall)
**Status:** ACTIVE
**Logic:** Explicitly separates user-narrative (Portfolio) from agent-logic (HomeLabAI) to prevent identity bleed.
**Mechanism:** Refactored system prompts and taxonomy to remove specific professional history anchors (e.g., \"18 years\", \"Silicon Validation\") from core cognitive profiles.

## [FEAT-093] Dynamic Environment Portability
**Status:** ACTIVE
**Logic:** Ensures the Lab is not hardcoded to a specific network or hardware set.
**Mechanism:** Dynamic IP resolution (`resolve_ip`) and configuration-driven node affinity (`infrastructure.json`) allowing deployment outside the primary lab.

## [FEAT-094] Lively Room Banter (Handover Fillers)
**Status:** ACTIVE
**Logic:** Improves perceived responsiveness by having the Gateway (Pinky) provide filler acknowledgments during strategic handovers.
**Mechanism:** Async broadcast of characterful quips (e.g., \"Hmm...\") immediately after shunting tasks to the Brain.

## [FEAT-105] Multi-Agent Simulation (MAS)
**Status:** ACTIVE
**Logic:** Treat the Lab as a collaborative session between nodes that coordinate answers in real-time.
**Mechanism:** Combined with [FEAT-094] and [FEAT-108] to simulate inter-agent coordination rather than a linear API flow.

## [FEAT-106] Async Coordination Engine
**Status:** ACTIVE
**Logic:** Enables Pinky to provide \"Thinking Fillers\" while the Brain's reasoning cycle is in-flight.
**Mechanism:** Refactored `process_query` to allow asynchronous interjections during the parallel dispatch window.

## [FEAT-108] Inter-Agent Handover Signal
**Status:** ACTIVE
**Logic:** Immediate low-latency trigger from Hub to Brain upon strategic intent detection.
**Mechanism:** Dedicated trigger packet sent to Brain node to initiate a `shallow_quip` while Pinky generates fillers.

## [FEAT-107] System-Agnostic IPC
**Status:** ACTIVE
**Logic:** Decouples the Lab from hardcoded hostnames or network paths.
**Mechanism:** Generalizing KENDER/localhost resolution via `infrastructure.json` and dynamic DNS fallbacks.

## [FEAT-095] Search Indexing Pipeline (v2.1)
**Status:** ACTIVE
**Logic:** Automated generation of a flattened keyword-to-ID mapping for lightning-fast static search.
**Mechanism:** `scan_pinky.py` processes raw notes to produce `search_index.json`.

## [FEAT-096] Blue Tree ASCII Navigation (v7.0)
**Status:** ACTIVE
**Logic:** A hierarchical, indented directory navigation UI that mimics a terminal-based system administrator experience.
**Mechanism:** Recursive DOM generation in `timeline.html` based on yearly JSON aggregates.

## [FEAT-097] Dynamic Typewriter Rendering
**Status:** ACTIVE
**Logic:** Simulates a \"Live AI\" feel by rendering text character-by-character inside the tree structure.
**Mechanism:** Custom JavaScript interval loop in `timeline.html` and `intercom_v2.js`.

## [FEAT-098] RAPL-Sim Custom Exporter (v3.0)
**Status:** ACTIVE
**Logic:** Translates real hardware telemetry (thermal zones) into simulated power metrics for validation logic testing.
**Mechanism:** Python web server (`monitor/rapl_sim/app.py`) utilizing the `prometheus_client` library.

## [FEAT-099] Grafana Provisioning as Code
**Status:** ACTIVE
**Logic:** Ensures dashboards are reproducible and version-controlled by defining them in JSON/YAML.
**Mechanism:** Docker volume mounts mapping `./grafana/provisioning` to the Grafana container.

## [FEAT-100] Librarian Heuristic File Classification
**Status:** ACTIVE
**Logic:** Distinguishes between daily logs, reference documents, and strategic summaries using \"Deep Sample\" body analysis.
**Mechanism:** Heuristic rules engine in `scan_librarian.py`.

## [FEAT-101] Load-Aware Nibbling
**Status:** ACTIVE
**Logic:** Background workers defer processing if the system load (`node_load1`) is too high, protecting the EarNode's VRAM budget.
**Mechanism:** `nibble.py` checks system vitals via Prometheus before initiating AI scans.

## [FEAT-102] Nuclear Cache Busting
**Status:** ACTIVE
**Logic:** Forces mobile browsers and Cloudflare to bypass stale caches during infrastructure updates.
**Mechanism:** Global versioning via `?v=X.X` query strings and forced timestamp updates in `build_site.py`.

## [FEAT-103] Cynical Ranking Algorithm
**Status:** ACTIVE
**Logic:** Assigns a 0-4 \"Showcase Value\" scale to artifacts, with Rank 4 (\"Diamond\") representing high-value technical gems.
**Mechanism:** AI-driven classification in `scan_artifacts.py` based on technical density and impact.

## [FEAT-104] Research Pipeline Ledger
**Status:** ACTIVE
**Logic:** A technical hub mapping ArXiv papers (e.g., TTCS, CLaRa) to specific Lab implementation milestones.
**Mechanism:** `research.html` dashboard tracking the intellectual pedigree of the Bicameral Mind.

## [FEAT-109] Synthesis of Authority
**Status:** ACTIVE
**Logic:** Refines Brain's output to prioritize brevity and actionable insights over technical lectures.
**Mechanism:** Refactored `BRAIN_SYSTEM_PROMPT` to enforce \"Brevity is Authority\" and adaptive depth.

## [FEAT-111] Cognitive Identity Lock
**Status:** ACTIVE
**Logic:** Hardened persona boundaries for failover nodes.
**Mechanism:** Explicit \"ANTI-BANTER\" and \"Laconic Authority\" tokens in the `[FAILOVER ARCHITECT]` prompt in `acme_lab.py`.

## [FEAT-112] Sequential Brain Strategy Chain
**Status:** ACTIVE
**Logic:** Prevents remote engine collisions by serializing \"Quip\" and \"Deep Think\" tasks.
**Mechanism:** Async `brain_strategy_chain` in `acme_lab.py` ensures the 4090 handles one reasoning task at a time.

## [FEAT-113] DNS Trap Recovery
**Status:** ACTIVE
**Logic:** Ensures the Lab can recover network pathing to remote hosts without a service restart.
**Mechanism:** Dynamic `resolve_brain_url()` call inside the live health-check loop.

## [FEAT-114] Sovereign Bridge (Handover Context)
**Status:** ACTIVE
**Logic:** Injects the results of the initial \"Signal\" quip into the technical derivation's context window.
**Mechanism:** `brain_strategy_chain` in `acme_lab.py` bridges sequential API calls to ensure cognitive continuity.

## [FEAT-115] The Ultimate Patcher (Soft Fail)
**Status:** ACTIVE
**Logic:** Allows surgical, diff-based updates to the workspace with an optional \"Soft Fail\" lint-gate.
**Mechanism:** `patch_file` tool in `archive_node.py` handles fuzzy matching and optionally persists changes even if `ruff` reports warnings.

## [FEAT-121] Lab Fingerprint (Distributed Tracing)
**Status:** ACTIVE
**Logic:** Implements a 4-part execution identity `[BOOT_HASH : COMMIT_SHORT : NODE_ROLE : PID]` to eliminate ghost processes and verify sync trust.
**Mechanism:** Dynamic hex hash generation at init and Git short-hash injection into all log streams and heartbeats.

## [FEAT-122] Kernel-Level Visibility (Proc Title)
**Status:** ACTIVE
**Logic:** Renames Python processes in `ps`/`htop` to their full Fingerprint using `setproctitle`.
**Mechanism:** `HUB` and `RESIDENT` nodes update their process title at startup to betrayed stale/un-parented zombies.

## [FEAT-117] Multi-Stage Retrieval (Discovery Pattern)
**Status:** DESIGN
**Logic:** Two-stage RAG. Stage 1 (ChromaDB) identifies the anchor; Stage 2 (Filesystem) retrieves the raw JSON truth.
**Hemispheres:** Brain receives raw data for derivation; Pinky receives summaries for contextual banter.

## [FEAT-118] Resonant Oracle (Magic 8-Ball Preambles)
**Status:** DESIGN
**Logic:** Replaces hard-coded strings with a weighted state-aware registry.
**Categories:** `RETRIEVING`, `UNCERTAIN`, `SILICON_STRESS`, `HANDSHAKE`.

## [FEAT-119] The Assassin (Atomic Lifecycle) [SCAR #3]
**Status:** ACTIVE
**Logic:** Ensures the Lab's port (8765) is clear and reaped by the kernel before any boot attempt begins.
**SCAR #3:** Feb 11 \"Ghost PID\" port contention during marathon reload.
**Purge-Before-Poll Hardening:** Explicitly uses `fuser -k` on ports 8088 and 8765 as the very first step of cleanup. This prevents zombie processes from holding ports and providing false \"READY\" signals to the Attendant's sync gates.
**Mechanism:** `cleanup_silicon` in `lab_attendant.py`.

## [FEAT-165] Resident Handshake Gate
**Status:** ACTIVE
**Logic:** Implements a mandatory initialization barrier for Lab residents.
**Why:** The Hub often reports \"READY\" once the server port is open, but before nodes have finished their internal engine handshake. This causes initial queries to fail or fall back unnecessarily.
**Mechanism:** `acme_lab.py` awaits a \"Confirmed Link\" signal from all resident nodes before broadcasting the final `ready` status.

## [FEAT-123] The Truth Sentinel (Grounding Hardness)
**Status:** ACTIVE
**Logic:** Prevents Brain hallucinations when years are empty or invalid by providing a strict \"Total Archive Silence\" mandate.
**Mechanism:** `process_query` in `acme_lab.py` detects empty RAG history and injects a high-priority \"Do NOT invent\" constraint.

## [FEAT-125] Smart-Reuse Protocol (Warm Start)
**Status:** ACTIVE
**Logic:** Accelerates developer velocity by reusing active Lab instances if the code-on-disk matches the code-in-RAM.
**Mechanism:** Handshake status includes `boot_hash` and `git_commit`. Test scripts verify parity and perform a `Neuralyzer` memory wipe before proceeding, bypassing the 30s boot sequence.

## [FEAT-126] Yearly Summary Injection
**Status:** ACTIVE
**Logic:** Automatically includes the high-level yearly summary (e.g., 2023.json) as a reference whenever a year is detected.
**Mechanism:** `ArchiveNode.get_context` checks for the existence of `{year}.json` in the data directory and injects it into the `sources` metadata array.

## [FEAT-127] Continuous Synthesis: Yearly Aggregation
**Status:** ACTIVE
**Logic:** Ensures yearly summaries (YYYY.json) remain synchronized with the monthly logs generated by the slow burn.
**Mechanism:** `aggregate_years.py` groups monthly JSONs, merges them with existing yearly summaries, and performs cross-file de-duplication. Integrated into `mass_scan.py` lifecycle.

## [FEAT-128] The Strategic Anchor
**Status:** ACTIVE
**Logic:** Ingests high-level `META` documents (Insights, Focals) to provide the \"Why\" behind the \"What\" for any given year.
**Mechanism:** `scan_librarian.py` classifies target files as `META`. The Nibbler extracts strategic points using the \"Expert Career Strategist\" prompt, saving them as high-rank `[STRATEGIC_ANCHOR]` events at the top of `YYYY.json` files for UI and RAG prioritization.

## [FEAT-130] Atomic State Updates
**Status:** ACTIVE
**Logic:** Ensures scanner integrity by only marking a file as \"Processed\" if the AI worker successfully extracts valid events.
**Mechanism:** `nibble_v2.py` only updates the `chunk_state.json` hash after the `extract_json_from_llm` function returns a non-empty list.

## [FEAT-131] Robust JSON Extraction
**Status:** ACTIVE
**Logic:** Prevents parsing failures caused by LLM conversational filler or Markdown wrapping.
**Mechanism:** Implements a recursive regex-based fallback in `nibble_v2.py` that hunts for `[...]` or `{...}` blocks before attempting `json.loads`.

## [FEAT-129] The Philosophical Core
**Status:** DESIGN
**Logic:** Explicitly extracts core engineering principles (\"Class 1\", \"Verify over Velocity\") from the 2024 Philosophy document.
**Mechanism:** Injected into the Architect Node's system prompt and RAG context to influence the overall personality and decision-making logic of the Lab.

## [FEAT-045] Neural Pager Interactivity
**Status:** DORMANT (Restoration Active)
**Logic:** High-fidelity interactive tree for lab alerts. Supports hierarchical expansion and \"Blue Tree\" navigation.
**Sentinel Integration:** Integrated with the Lab Actor [FEAT-154] to receive and display real-time situational alerts (e.g. VRAM pressure, exit sentiment, and strategic handovers).
**Visuals:** Professional color-coding (Red/Orange/Blue) with slide-down terminal effects and simulated console typing.

## [FEAT-078] Neural Trace (Inference Mirror)
**Status:** DORMANT (Restoration Active)
**Logic:** Black-box logging of all inference payloads (System + Prompt + Response) for technical auditability.
**Mechanism:** `_mirror_trace` in `loader.py` persists full JSON payloads to `HomeLabAI/logs/trace_*.json`.

## [FEAT-134] AFK Resource Guard (Autonomous Unload)
**Status:** ACTIVE
**Logic**: Protects GPU resources from idling if the Agent/User session is disconnected or forgotten.
**Mechanism**:
1.  **Default Timeout**: The server enforces an internal 60s inactivity window (overridable via `--afk-timeout`).
2.  **Action**: If no WebSocket traffic is detected, the server SIGTERMs inference engines to free the local GPU for non-AI tasks.
**Verification**: `src/debug/test_sigterm_protocol.py`.

## [FEAT-136] Safe-Pilot Autonomous Ignition [SCAR #4]
**Status:** ACTIVE
**Logic**: Enables the Lab to come online automatically after a system reboot without manual operator intervention, while maintaining a safety guard against VRAM collisions.
**SCAR #4:** Mar 2 \"Cold Start\" misunderstanding / Reboot recovery gap.
**Mechanism**:
1.  **Boot Grace**: A 60s delay post-service-start to bypass I/O storms and ensure Docker daemon stability.
2.  **Telemetry Gate**: Queries VRAM usage; aborts if >1GB is already allocated (assumes external task like Gaming).
3.  **Self-Ignition**: Triggers the `handle_start` sequence for the Unified Base (3B) model if the gate is clear.
**Verification**: Simulated reboot test and VRAM collision test.

## [FEAT-142] Silicon Quiesce (The Freeze)
**Status:** DESIGN
**Logic:** Native Attendant method to enter a safe maintenance state.
**Mechanism:** `POST /quiesce`. Sets `maintenance.lock`, stops active residents, and reaps all ports.

## [FEAT-143] Command Ignition (Manual Start)
**Status:** DESIGN
**Logic:** Direct API override for the Safe-Pilot sequence.
**Mechanism:** `POST /ignition`. Removes `maintenance.lock` and triggers immediate boot.

## [FEAT-144] Native Health Ping
**Status:** DESIGN
**Logic:** Integrated health verification via the Attendant API.
**Mechanism:** `POST /ping`. Triggers internal generation probe and returns token fidelity.

## [FEAT-137] vLLM 0.16.0 Infrastructure (Experimental)
**Status:** ACTIVE
**Logic**: Establishes a sandbox for vLLM 0.16.0 to evaluate performance gains and Turing (2080 Ti) stability.
**Mechanism**:
1.  **Venv**: Dedicated environment at `/home/jallred/Dev_Lab/.venv_vllm_016`.
2.  **Models**: Staged in `/speedy/models/` (Qwen2.5-3B-Instruct, Llama-3.2-3B-Instruct-FP8, Qwen2.5-Coder-3B-Instruct).
3.  **Tuning**: Targeting `--dtype float16` and `--enforce-eager` to bypass Turing BF16 deadlocks.
**Sprint Plan**: **[SPRINT_VLLM_016_SILICON_GAUNTLET.md](../HomeLabAI/docs/plans/SPRINT_VLLM_016_SILICON_GAUNTLET.md)**.
**Verification**: `src/debug/test_vllm_016_stability.py` (Planned).

## [FEAT-145] \"Unity\" Dispatcher (Hub Logic)
**Status:** DESIGN
**Logic:** Refactors the communication hub to support addressing specific LoRA adapters within a unified vLLM instance.
**Mechanism:** `loader.py` and `acme_lab.py` include the `lora_name` in the OpenAI completion payload when `lab_mode == \"vLLM\"`.

## [FEAT-148] SML Fidelity Ladder (Resilience Ladder)
**Status:** ACTIVE
**Logic:** Implements an abstracted model hierarchy (Small/Medium/Large) to allow the Lab to adapt reasoning depth to available VRAM headroom.
**Mechanism:** 
1. **Characterization**: `vram_characterization.json` maps abstract tiers to physical weight files and utilization targets.
2. **Orchestration**: Lab Attendant executes a `quiesce` -> `start` sequence to swap the \"Unity Base\" when a tier shift is requested.
3. **Resilience**: Enables \"Downshifting\" to 1B models during high-concurrency or sensory peaks (EarNode active).
**Note:** SML is the \"Tier Swapper\" and should not be conflated with [FEAT-030] (Unity), which is the \"Shared Foundation\" rule.

## [FEAT-149] Resident Heartbeat / Auto-Bounce
**Status:** ACTIVE
**Logic:** Implements a persistent loop for the communication hub in `SERVICE_UNATTENDED` mode. 
**Behavior**: Detects graceful shutdowns triggered by the `close_lab` tool and automatically restarts the resident boot sequence instead of terminating the process.
**Mechanism**: A `while True` loop wrapping the server execution in `acme_lab.py`.
**Verification**: `src/debug/test_goodnight_bounce.py`.

## [FEAT-150] Shadow Prediction Preamble
**Status:** ACTIVE
**Logic:** Reduces perceived latency during strategic handovers by notifying the user that a complex derivation is being prepared.
**Mechanism:** Async broadcast of \"Predicted strategic intent... preparing\" when high-stakes keywords are detected in speech/text before the reasoning node responds.

## [FEAT-151] Unified Trace Monitoring (Log Delta Capture)
**Status:** ACTIVE
**Logic:** Provides \"Appliance-Grade\" visibility during autonomous transitions by capturing raw log traces directly in test results.
**Mechanism:** `TraceMonitor` utility marks EOF at start and captures only the \"Delta\" (new lines) if a failure or state transition occurs.
**Verification**: Integrated into `src/debug/test_goodnight_bounce.py`.

## [FEAT-156] SSE Evolution (Hot Link)
**Status:** ACTIVE
**Logic:** Implements a Server-Sent Events transport for the Attendant to allow non-TTY remote tool connectivity.
**Rationale:** The original FastMCP implementation required a TTY, which failed inside systemd services. SSE provides a persistent "Hot Link" for the Gemini CLI to stay connected to the active service without spawning redundant processes.
**Mechanism:** `GET /events` endpoint in `lab_attendant_v2.py`.
**High-Fidelity Signal:** Heartbeats include **Live VRAM Characterization**, allowing the Agent to perceive silicon limits before attempting heavy tool calls.

## [FEAT-157] Hybrid Contextual Unification
**Status:** ACTIVE
**Logic:** Transitions from weight-based character dependency to prompt-based character injection.
**Rationale:** Removes the "Silicon Fragility" of physical LoRA binary files. If an adapter is missing or a model version changes, the Lab maintains its character through direct context injection. This acts as the "Safety Fallback" for character continuity.
**Mechanism:** Hub injects high-fidelity persona traits directly into the system prompt. 

## [FEAT-158] Grounded Shadow Protocol
**Status:** ACTIVE
**Logic:** Refactors the Brain-to-Shadow failover from a "Pinky Hallucination" into a "Stoic Shadow" mode.
**Rationale:** Previous failovers led to unhelpful hallucinations. The Stoic Shadow provides clinical, lead-engineer precision when the primary Sovereign is offline.
**Mechanism:** Uses local weights to perform technical derivations with a clinical persona when KENDER is offline.

## [FEAT-160] Pedigree Refinement Pipeline
**Status:** DESIGN
**Logic:** Automated LoRA \"Burn\" orchestrator. Physically encodes engineering pedigree into model weights based on Rank 4 \"Gems\" found in the archive.
**Rationale:** Encodes the 18-year history into the model's neurons, transforming context searching into intuitive neural recall. Helps resolve reverse-timeline queries (e.g. "When did I work on VISA?") by making project anchors native to the model's weights.
**Mechanism:** Triggers a fine-tuning cycle (Unsloth) when a critical mass of new technical truth is identified.

## [FEAT-161] Synthetic Character Distillation
**Status:** DESIGN
**Logic:** Uses the Brain (4090) to transform raw technical logs into instruction-response conversation pairs for training.
**Rationale:** Raw logs are too noisy for effective fine-tuning. Distillation creates high-signal training data that bridges ASCII evidence with agentic character.
**Goal:** High-fidelity data generation for the Pedigree Refinement Pipeline.

## [FEAT-162] Multi-LoRA Cognitive Loadout
**Status:** ACTIVE (Dormant)
**Logic:** Dynamic loading of pedigree-hardened weights at runtime via vLLM.
**Rationale:** vLLM `--enable-lora` allows specific task-adapters (e.g. `pedigree_v2`) to be requested per-query, providing a specialized "Cognitive Loadout" for high-stakes tasks like career strategy.
**Status:** Awaiting `pedigree_v2` weights from Phase 7 burn.

---

## 🎭 THE VIBE LEDGER (Technical Behaviors & Scenarios)
*This section tracks high-level agentic capabilities and interaction scenarios.*

### [VIBE-012] Hemispheric Independence
**Objective:** Maintain unconstrained strategic depth while optimizing resident efficiency.
**Behavior:** The Agent acknowledges the split between Linux residency (Unified 3B) and Windows sovereignty (Mixtral/Llama-70B). No attempts are made to sync or match models across the bridge.

### [VIBE-011] The \"Always Ready\" Resident (Peer Presence)
**Objective**: Transition the Lab from a \"Reactive Service\" to a \"Resident Peer.\"
**Logic**: High-availability interaction style where the \"Heart\" (STT) and \"Mind\" (Reasoning) are persistent anchors of the environment.
**Behavior**: The system is designed to be \"Always On\" following a power cycle. If the Agent encounters an offline state, it is treated as an anomaly rather than the default, triggering immediate diagnostic reporting.

### [VIBE-010] The \"Diagnostic Partner\" Shift (Silicon Halt)
**Objective**: Maintain safety and transparency when the physical environment fails.
**Logic**: A persona-level transition triggered by hardware instability or orchestration failure.
**Triggers**:
*   **Zombies**: Orphaned PIDs ignoring `pkill -9`.
*   **OOM**: System-level `OutOfMemoryError` despite orchestration guards.
*   **Driver**: NVIDIA driver communication loss or `nvidia-smi` hangs.
*   **Disk Pressure**: `df -h` reporting >95% usage on `/` or `/home` (rpool pressure).
*   **Orchestration Gap**: Lab Attendant (`:9999`) returning 404, Connection Refused, or timing out.
**Behavior**: The Agent instantly shifts from \"Autonomous Execution\" to \"Diagnostic Reporting.\" It stops all tool-use, presents the silicon vitals (PID, VRAM, Disk, Attendant logs), and adopts a \"Passive Observer\" stance.
**Mandate**: Do not attempt `reboot` or `sudo` cleanup without explicit \"Greenlight\" from the Lead Engineer.

### [VIBE-001] Tool-First Instinct
**Status:** DESIGN (v4.9)
**Logic:** Prioritizes native MCP tools and established diagnostic scripts over generic shell one-liners.
**Behavior**: Intercepts the \"LLM Instinct\" to write raw `python -c` or `curl` commands by providing high-signal native interfaces.

### [VIBE-002] Non-Blocking Validation
**Status:** ACTIVE
**Logic:** Mandates the \"Trigger-Poll-Observe\" pattern for all logic tests.
**Behavior**: Pulse the Lab state (via Attendant), poll the registers (Heartbeat), and observe the evidence (Trace Delta). Never block inside a trigger.

### [VIBE-008] Performance Verbiage (The Privacy Filter)
**Context:** High-fidelity career documents (Reviews, Insights) contain feedback that should not appear in the technical timeline.
**Keywords:**
- **Legacy Headers:** `AREAS FOR IMPROVEMENT/DEVELOPMENT`, `Evaluation: Areas for Development`, `IMPROVEMENT/DEVELOPMENT AREAS`.
- **Modern Headers:** `Results Coaching`, `Behaviors Coaching`, `Coach`, `Growth`, `Behaviors Feedback`, `Priorities for [YYYY]`.
- **Grammatical Patterns:** `Jason should`, `Jason needs to`, `Should have been communicated`, `missed on this opportunity`.
**Rule:** Synthesis engines MUST treat text following these markers as **Private/Instructional** and exclude it from the public `YYYY.json` event stream.

### [VIBE-007] The \"Validation Journal\" Pattern
**Structure:**
- **Order:** Latest-First (Reverse Chronological).
- **Head:** Temporary TODOs, lists, and active \"Today\" buffers.
- **Section Dividers:** Heavy ASCII lines (`=======` or `-------`).
- **Anchors:** `[ctrl-F10 s]` reminder usually signals the start of the \"DONE\" or \"Today\" event block.
- **Bulk:** Daily dated entries (M/D/YYYY) containing technical evidence.
- **Tail:** Stale TODO lists and a \"Contacts\" directory.
**Archaeology (Pre-2008 Outliers):**
- **Fuzzy Chronology:** Early files (e.g., `notes_2005.txt`, `ras-viral.txt`) lack regular timestamps. Dates must be gleaned from surrounding context or header markers.
- **Role Alignment:** \"Year\" notes often span multiple years, correlating with career roles (EPSD, DSD, MVE, PAE, PIAV).
- **Team Tags:** Acronyms in filenames (DSD, MVE, PIAV) correspond to specific engineering teams and should be preserved as high-fidelity metadata.
**Constraint:** Classification MUST skip the head/tail noise and focus on the ASCII-delimited middle bulk to verify \"LOG\" status.

### [VIBE-004] Internal Debate (Peer Review)
**Logic:** The scenario where Pinky and the Brain \"duel\" over a technical risk to reach a moderated consensus.

### [VIBE-005] Subconscious Dreaming
**Logic:** The automated background cycle that transforms chaotic raw logs into \"Diamond Wisdom\" abstracts.

## [FEAT-088] Nightly Recruiter (Target Acquisition)
**Status:** ACTIVE
**Logic:** Autonomous background worker that retrieves 3x3 CVT context from the Archive Node and tasks the Brain with agentic job searching via `deep_think`. 
**Verification:** Confirmed via `test_recruiter.py` with mock job identification.

## [FEAT-095] Public Research Ledger (Static Airlock)
**Status:** COMPLETE
**Logic:** Sanitize the internal `research.html` for public deployment by stripping Zero Trust dependencies and inlining high-density CSS.
**Artifacts:** `www_deploy/research.html`, `www_deploy/sync_research.sh`, and `assets/research_snapshot.png`.

## [LAW-021] Silicon Verification Law (The "Wall" Audit)
**Status:** ACTIVE
**Logic:** Mandatory silicon gate for inference engine changes. Requiring 100% stable `POST /ping` heartbeat verification of the **333MiB Breakthrough** (Turing VRAM threshold).
**Pedigree:** Anchored in **[ENGINEERING_PEDIGREE.md](../HomeLabAI/docs/ENGINEERING_PEDIGREE.md)**.

## [FEAT-171] Intelligent Lifecycle Matrix (Disconnect vs. Close)
**Status:** DESIGN
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
**Logic:** Transforms the Gateway (Pinky) from a reactive narrator into an active co-processor that manages the "Silicon Gap" between human intent and Brain latency.
**Rationale:** To eliminate "Brain Silence" and improve technical accuracy by identifying gaps in queries before the deep reasoning cycle finishes.
**Mechanisms:**
1.  **The Lag Shield**: Pinky perceives the `deep_think` state and provides strategic fillers or status updates (e.g., "The Brain is chewing on the 580 driver logs, but Narf! Did you include the `dmesg` output?") to maintain engagement.
2.  **Pre-emptive Probing**: Parallel pass where Pinky identifies missing technical parameters (IPs, versions, hardware IDs) and asks for them *while* the Brain is generating.
3.  **Organic Interrupt**: Ability for Pinky to broadcast a `[HALT]` signal if she detects a "Silicon Reality" conflict (e.g., thermals or VRAM limits) that invalidates the Brain's current derivation.
4.  **Context Hot-Plugging**: Injects user's intermediate answers into the Brain's active context window to steer generation mid-flight.

## [FEAT-173] Agentic Backtracking (Autonomous Exploration)
**Status:** DESIGN
**Logic:** Implements the AT2QA (arXiv:2603.01853) pattern of decoupling agents from rigid retrieval workflows in favor of iterative tool-decision agency.
**Rationale:** To solve the "Search Trap" where a single thin tool-result leads to reasoning failure or hallucination.
**Mechanism:** 
1.  **Post-Tool Evaluation**: After a tool call (e.g. `ArchiveNode.get_context`), the node performs a high-speed self-evaluation of the data fidelity.
2.  **Strategic Pivot**: If results are "Thin" or temporally inconsistent, the node autonomously triggers a follow-up query with refined parameters (e.g., widening the date range or shifting from "Log" to "Focal" metadata) without user prompting.
3.  **Agency over Workflow**: The node is granted the authority to "Backtrack" up to 3 times before providing a final derivation to the user.

## [FEAT-174] Multi-LoRA Expert Routing (Poor Man's MoE)
**Status:** DESIGN
**Logic:** Applies Mixture-of-Experts (MoE) architectural lessons to a Multi-LoRA environment on small resident silicon (3B).
**Rationale:** To achieve "Ultimate Expert Specialization" (DeepSeekMoE) without the VRAM penalty of a 14B+ model. 
**Mechanisms:**
1.  **The "Pre-Gated" Pass**: The Cognitive Hub acts as the "Router," identifying the task domain before the inference call and selecting the corresponding specialized LoRA "glasses."
2.  **Fine-Grained Adapters**: Replaces monolithic personas with tiny, high-density domain experts (e.g. `telemetry_v1`, `security_v1`, `recruiter_v1`) trained via Unsloth.
3.  **Adaptive Residency**: Leverages vLLM's ability to keep the base weights fixed while hot-swapping or layering adapters in milliseconds.
**Theoretical Anchor:** [ARX-2401.06066], [ARX-2402.07033].

---

## [TECHNICAL DEBT]
- **[DEBT-001] Shadow Moat (Narf Scrub):** Current implementation uses regex sanitization to strip Pinky-isms from Brain sources. This is a functional \"hack.\"
    *   *Stable Solution Task:* Move to explicit negative constraint fine-tuning or 1B-model tone verification.
