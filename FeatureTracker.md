# Feature Tracker: Acme Lab Bicameral Mind
**The DNA Association Matrix**

> [!IMPORTANT]
> **PURPOSE:** This is a Relational Hub for mapping **Features** to **Code**, **Research**, and **Tests**.
> **NOT A MISSION DOC:** Refer to **[HomeLabAI/docs/ENGINEERING_PEDIGREE.md](../HomeLabAI/docs/ENGINEERING_PEDIGREE.md)** for the Strategic Mission and Architecture Laws.

---

## [ARTIFACT] Hardware Isolation Protocol
**Context:** Reversion artifact used during the "Driver 550 Resurgence."
**Mechanism:** Purge kernels, stop polling, and physically erase modules (e.g., `i2c_nvidia_gpu`).
**BKM:** Refer to `SESSION_BKM_FEB_19.md` for the "Undo" sequence if moving back to 580/Ampere.

## [FEAT-028] Strategic Ping (Generation Probe)
**Status:** ACTIVE
**Logic:** Functional Logic Verification verifying the *Mind* is alive (not just the process).
**Mechanism:** Single-token generation probe in `acme_lab.py` to trigger Brain-to-Shadow failover.

## [FEAT-023] The Stoic Strategist (Identity Anchor)
**Status:** ACTIVE
**Logic:** Enforces "Bicameral Identity" where the Brain provides pure strategic insight without conversational filler, while Pinky handles the banter.
**Verification:** `src/debug/test_persona_bugs.py`.

## [FEAT-036] VRAM Guard (Conscious Attendant)
**Status:** ACTIVE
**Logic:** A "Deep Sleep" protocol that stubs the Brain/Pinky nodes if VRAM pressure exceeds critical thresholds (95%) or engines fail to load.
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

## [FEAT-054] Banter Decay Test
**Status:** ACTIVE
**Logic:** A simulation test (`test_banter_decay.py`) that verifies the `reflex_ttl` interval increases correctly when the user is idle.

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

## [FEAT-068] Persona-Locked Dispatch (The Iron Gate)
**Status:** ACTIVE
**Logic:** Strictly prevents \"Persona Bleed\" by intercepting casual conversation and gating it to Pinky, while stripping header artifacts (e.g., system prompt echoes) from the Brain's output.

## [FEAT-069] Silicon-Aware Adaptive Runtime
**Status:** ACTIVE
**Logic:** The Lab Attendant characterises the 11GB VRAM budget and automatically \"Downshifts\" the reasoning engine (vLLM -> Ollama -> Suspend) based on real-time NVML telemetry.

## [FEAT-070] Hallucination Shunting
**Status:** ACTIVE
**Logic:** If a reasoning node attempts to use an unknown or hallucinated tool, the orchestrator intercepts the error and shunts it back to the Pinky Gateway for characterful recovery and user feedback.

## [FEAT-064] Static Site Synthesis (build_site.py)
**Status:** ACTIVE
**Logic:** Automated pipeline that clears caches and prepares the `www_deploy` directory for public hosting.
**Mechanism:** Runs `python3 field_notes/build_site.py` to trigger versioned cache-busting and asset bundling.

## [FEAT-065] Cross-Platform Synchronization
**Status:** ACTIVE
**Logic:** Shell-based synchronization (`sync_to_linux.sh`, `sync_to_windows.sh`) using `rsync` and Google Drive mounts to maintain code parity across the hybrid lab (Z87-Linux and Windows 4090).

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

## [FEAT-039] Banter Decay (Adaptive Reflex)
**Status:** ACTIVE
**Logic:** Automatically increases the polling interval (`reflex_ttl`) when the user is idle (>60s), reducing system noise and resource usage.

## [FEAT-043] Dead-Man's Switch
**Status:** ACTIVE
**Logic:** Triggers a `CRITICAL` alert to `pager_activity.json` if the Lab port 8765 is unresponsive for more than 5 minutes, signaling unrecoverable failure.

## [FEAT-047] Reflex Tics
**Status:** ACTIVE
**Logic:** Occasionally bubbles up characterful banter ("Narf!", "Poit!") when the Lab is idle and ready, maintaining persona presence.

## [FEAT-048] Monitor Task with Tics
**Status:** ACTIVE
**Logic:** Sends periodic "Thinking..." updates to the user during long-running Brain reasoning tasks to provide progress feedback.

## [FEAT-049] Scheduled Tasks (Alarm Clock)
**Status:** ACTIVE
**Logic:** Background loop that triggers automated jobs: Nightly Recruiter (02:00 AM) and Hierarchy Refactor (03:00 AM).

## [FEAT-050] Strategic Vibe Check on Save
**Status:** ACTIVE
**Logic:** Automatically triggers a Brain-level validation of technical logic and architectural advice whenever a file is saved in the workspace.

## [FEAT-031] Montana Protocol (Logger Isolation)
**Status:** ACTIVE
**Context:** Montana name was derived from original experience with a legacy project; implemented to manage logger hijacking by NeMo/ChromaDB.
**Logic:** Strictly isolates asynchronous library logs from the Lab Attendant's telemetry stream.

## [FEAT-032] Strategic Sentinel (Amygdala Filter)
**Status:** ACTIVE
**Logic:** Dual-gated input filter. Voice mode uses keyword sentinel (strat_keys); Typing mode uses 1B model (stubbed) to prevent casual clutter.
**Mechanism:** `self.mic_active` toggle in `acme_lab.py`.

## [FEAT-033] Iron Gate (Persona Isolation)
**Status:** ACTIVE
**Logic:** Strictly isolates casual greetings to Pinky and clears the Architect's Insight panel during greetings to prevent persona bleed.
**Mechanism:** `is_casual` check in `acme_lab.py`.

## [FEAT-034] Barge-In Logic (Interrupts)
**Status:** ACTIVE
**Logic:** Allows user to cancel long reasoning cycles using voice interrupt keys ("wait", "stop", "hold on", "shut up").
**Mechanism:** `ear_poller` loop in `acme_lab.py`.

## [FEAT-035] Zombie Port Recovery
**Status:** ACTIVE
**Logic:** The Lab Attendant monitors port 8765. If the process is alive but the port is unresponsive for 3 intervals, it triggers an autonomous engine swap.
**Mechanism:** `vram_watchdog_loop` in `lab_attendant.py`.

## [FEAT-030] vLLM Multi-LoRA Engine
**Status:** TABLED (Hardware Blocked)
**Note:** Physically untenable on Turing (2080 Ti). **RETAIN** code and configs for future Ampere+ upgrades.

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
**Logic:** Provides sub-second feedback for deep strategic tasks by broadcasting an immediate "Thinking..." message.
**Mechanism:** Hardcoded async broadcast in `acme_lab.py` triggered before shunting to the reasoning node.

## [FEAT-087] Intelligent Handshake Priming
**Status:** ACTIVE
**Logic:** Forces VRAM residency of the primary model upon first connection.
**Mechanism:** High-priority generation probe (`force=True`) inside the `handshake` packet handler in `acme_lab.py`.

## [FEAT-088] Semantic Career Recall
**Status:** DORMANT (Requires ChromaDB)
**Logic:** The fundamental ability to query 18 years of technical history via natural language (e.g., "What did I do in 2019?").
**Mechanism:** Vector search via ArchiveNode bridging the local JSON logs to the reasoning nodes.

## [FEAT-089] Zero Trust Guest Expansion
**Status:** ACTIVE
**Logic:** Securely allows authorized third-party recruiters (e.g., from `intel.com`) to access the technical lobby.
**Mechanism:** Cloudflare Access Policy updates for `notes.jason-lab.dev` and `acme.jason-lab.dev`.

## [FEAT-090] Non-Blocking Parallel Dispatch
**Status:** ACTIVE
**Logic:** Eliminates synchronization barriers in the hemispheric dispatch loop.
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
**Mechanism:** Refactored `BRAIN_SYSTEM_PROMPT` to enforce "Brevity is Authority" and adaptive depth.

## [FEAT-111] Cognitive Identity Lock
**Status:** ACTIVE
**Logic:** Hardened persona boundaries for failover nodes.
**Mechanism:** Explicit "ANTI-BANTER" and "Laconic Authority" tokens in the `[FAILOVER ARCHITECT]` prompt in `acme_lab.py`.

## [FEAT-112] Sequential Brain Strategy Chain
**Status:** ACTIVE
**Logic:** Prevents remote engine collisions by serializing "Quip" and "Deep Think" tasks.
**Mechanism:** Async `brain_strategy_chain` in `acme_lab.py` ensures the 4090 handles one reasoning task at a time.

## [FEAT-113] DNS Trap Recovery
**Status:** ACTIVE
**Logic:** Ensures the Lab can recover network pathing to remote hosts without a service restart.
**Mechanism:** Dynamic `resolve_brain_url()` call inside the live health-check loop.

## [FEAT-114] Sovereign Bridge (Handover Context)
**Status:** ACTIVE
**Logic:** Injects the results of the initial "Signal" quip into the technical derivation's context window.
**Mechanism:** `brain_strategy_chain` in `acme_lab.py` bridges sequential API calls to ensure cognitive continuity.

## [FEAT-115] The Ultimate Patcher (Soft Fail)
**Status:** ACTIVE
**Logic:** Allows surgical, diff-based updates to the workspace with an optional "Soft Fail" lint-gate.
**Mechanism:** `patch_file` tool in `archive_node.py` handles fuzzy matching and optionally persists changes even if `ruff` reports warnings.

## [FEAT-121] Lab Fingerprint (Distributed Tracing)
**Status:** DESIGN
**Logic:** Implements a 4-part execution identity `[BOOT_HASH : COMMIT_SHORT : NODE_ROLE : PID]` to eliminate ghost processes and verify sync trust.
**Mechanism:** Dynamic hex hash generation at init and Git short-hash injection into all log streams and heartbeats.

## [FEAT-122] Kernel-Level Visibility (Proc Title)
**Status:** DESIGN
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

## [FEAT-119] The Assassin (Atomic Lifecycle)
**Status:** ACTIVE
**Logic:** Ensures the Lab's port (8765) is clear and reaped by the kernel before any boot attempt begins.
**Mechanism:** `cleanup_silicon` in `lab_attendant.py` identifies PIDs holding the TCP port. The `boot_sequence` coroutine implements an **Atomic Lifecycle Barrier** by awaiting total cleanup before spawning the new process, eliminating race-condition collisions.

## [FEAT-123] The Truth Sentinel (Grounding Hardness)
**Status:** ACTIVE
**Logic:** Prevents Brain hallucinations when years are empty or invalid by providing a strict "Total Archive Silence" mandate.
**Mechanism:** `process_query` in `acme_lab.py` detects empty RAG history and injects a high-priority "Do NOT invent" constraint.

## [FEAT-125] Smart-Reuse Protocol (Warm Start)
**Status:** ACTIVE
**Logic:** Accelerates developer velocity by reusing active Lab instances if the code-on-disk matches the code-in-RAM.
**Mechanism:** Handshake status includes `boot_hash` and `git_commit`. Test scripts verify parity and perform a `Neuralyzer` memory wipe before proceeding, bypassing the 30s boot sequence.

## [FEAT-126] Yearly Summary Injection
**Status:** ACTIVE
**Logic:** Automatically includes the high-level yearly summary (e.g., 2023.json) as a reference whenever a year is detected.
**Mechanism:** `ArchiveNode.get_context` checks for the existence of `{year}.json` in the data directory and injects it into the `sources` metadata array.

## [FEAT-045] Neural Pager Interactivity
**Status:** DORMANT (Restoration Active)
**Logic:** High-fidelity interactive tree for lab alerts. Supports hierarchical expansion and "Blue Tree" navigation.
**Visuals:** Professional color-coding (Red/Orange/Blue) with slide-down terminal effects and simulated console typing.

## [FEAT-078] Neural Trace (Inference Mirror)
**Status:** DORMANT (Restoration Active)
**Logic:** Black-box logging of all inference payloads (System + Prompt + Response) for technical auditability.
**Mechanism:** `_mirror_trace` in `loader.py` persists full JSON payloads to `HomeLabAI/logs/trace_*.json`.

---

## 🎭 THE VIBE LEDGER (Technical Behaviors & Scenarios)
*This section tracks high-level agentic capabilities and interaction scenarios.*

### [VIBE-001] Semantic Career Recall
**Logic:** Asking about specific years or themes (e.g., "What did I do in 2019?") triggers a multi-turn retrieval and synthesis loop.

### [VIBE-002] 3x3 CVT Synthesis
**Logic:** Automated correlation of 18 years of technical history with yearly strategic goals for high-density positioning.

### [VIBE-003] Insight Pruning (Hard Scrub)
**Logic:** Following a direct order to surgically scrub patterns (e.g., last names) from historical summaries using regex-based automation.

### [VIBE-004] Internal Debate (Peer Review)
**Logic:** The scenario where Pinky and the Brain "duel" over a technical risk to reach a moderated consensus.

### [VIBE-005] Subconscious Dreaming
**Logic:** The automated background cycle that transforms chaotic raw logs into "Diamond Wisdom" abstracts.

### [VIBE-006] The "Wave Paper" Event
**Logic:** Collaborative UI behavior where a mouse notifies the user or auto-refreshes the editor when they write to the whiteboard.

## [TECHNICAL DEBT]
- **[DEBT-001] Shadow Moat (Narf Scrub):** Current implementation uses regex sanitization to strip Pinky-isms from Brain sources. This is a functional "hack."
    *   *Stable Solution Task:* Move to explicit negative constraint fine-tuning or 1B-model tone verification.

## [BACKLOG] Synthesis & Forensic Tasks
1.  **[VIBE] Semantic Gatekeeper**: Replace brittle `casual_keys` and `strat_keys` with a 1B/3B intent classifier.
2.  **[UI] Authority of Formatting**: Instruction for Brain to use **Bold conclusions**, bullets, and `<details>` tags for better readability.
3.  **[VIBE] Dynamic Temperature**: Research if Pinky can adjust the Brain's `temperature` on the fly based on task urgency.
4.  **[VIBE] Tone Checker**: Implement a local 1B model as a "moat" to verify Brain output is free of interjections before broadcast.
5.  **[VIBE] Semantic Barge-In**: Catch halts like \"Hold on\" or \"Not yet\" using semantic similarity rather than keyword matching.
6.  **[BACKLOG] Return to 580 Protocol**: Define the automated cleanup of isolation artifacts.
