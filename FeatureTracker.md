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
