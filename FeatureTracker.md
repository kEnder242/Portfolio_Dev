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
**Mechanism:** Shadow predictions stay in Pinky's console, while true insights and explicit `insight` channel messages route to the Brain's Insight panel.

## [FEAT-059] Real-Time PCM Audio Streaming
**Status:** ACTIVE
**Logic:** Browser-based voice capture downsamples audio to 16kHz mono and converts to Signed Int16 PCM before WebSocket streaming.
**Verification:** `src/debug/test_web_binary.py`.

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

## [FEAT-052] User Typing Awareness
**Status:** ACTIVE
**Logic:** Dynamically suppresses reflexes and character tics if the user is currently typing, preventing interaction collisions.

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

---

## [BACKLOG] Synthesis & Forensic Tasks
1.  **[COMPLETE] Forensic Mapping**: Initial DNA map populated from Feb 20 Audit.
2.  **[BACKLOG] Return to 580 Protocol**: Define the automated cleanup of isolation artifacts.
3.  **[BACKLOG] Strategic Ping Review**: Revisit timeouts and evaluate parallel heartbeat threads.
