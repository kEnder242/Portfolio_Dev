# Documentation Refactor Plan: [SPR-11-07] Bicameral Evolution
**Status:** DESIGN | **Goal:** Align all public and internal documentation with high-fidelity technical personas and the Bilingual Attendant architecture.

---

## 📍 1. Public & High-Level Refactors

### A. HomeLabAI/README.md
- **Identity Update:** Introduce the **Sovereign Architect** (4090) and **Physicality Auditor** (2080 Ti). Move away from general "Right/Left Hemisphere" descriptions toward specific technical roles.
<<<<<<< SEARCH
*   **The Heart (EarNode):** The invariant sensory core.
*   **The Right Hemisphere (Pinky):** Intuitive, Aware, and Presence-focused.
*   **The Left Hemisphere (The Brain):** Logical, Abstract, and Strategic.
=======
*   **The Heart (EarNode):** The invariant sensory core.
*   **Lab:** The **Environmental Sentinel**. Monitors the "4th Wall" (Hardware vitals, Silicon limits) and coordinates the hemispheres.
*   **Pinky:** The **Physicality Auditor (Foil)**. Grounds strategic derivations in hardware reality (VRAM, Thermals) using AYPWIP-style literalism.
*   **Brain:** The **Sovereign Architect (4090)**. High-fidelity reasoning and archive synthesis using the Qwen 27B Ultra tier.
*   **Architect:** The **Structural Registrar**. Resident BKM Librarian responsible for high-density formatting of derivations into the BKM Protocol [v3.0] format.
>>>>>>> REPLACE

- **Architecture Update:** Document the **Bilingual Attendant (v2)**. Replace `curl` examples with native `acme_attendant` MCP tool examples.
    - *Naming Note:* "Bilingual" signifies the dual-protocol support (REST for systemd + MCP for Agentic tools).
    - *Implementation:* Refactor the "Getting Started" section to use `acme_attendant lab_start` instead of manual `curl`.

- **Model Standard:** Update from "Gemma 2 2B" to the **Unified 3B Base (Llama 3.2 / Qwen 2.5)** and the **Sovereign Ultra (Qwen 27B)** tier.
<<<<<<< SEARCH
*   **v4.0 (ACTIVE):** Transitioned to **Unified Base (Gemma 2 2B)** for all 2080 Ti nodes.
=======
*   **v4.1 (ACTIVE):** Transitioned to **Unified 3B Base (Llama 3.2 / Qwen 2.5)**. 
    - *Hardware Scar:* Gemma 2 2B officially **Tabled** due to the 2080 Ti's lack of native `bfloat16` support (Compute 7.5), causing the "333MiB Wall" deadlock. 
    - *Efficiency BKM:* Standardized on **Monolingual (English) Squeeze** [FEAT-166] to maximize 11GB VRAM headroom for the EarNode sensory core.
>>>>>>> REPLACE

- **Operational Laws (New Section):** Document the **Montana Protocol** (Logger Isolation) and **BKM Protocol** (Execution/Validation/Scars) as core standards.

### B. Portfolio_Dev/README.md
- **VIBE Update:** Highlight the **"Living Room" VIBE** and the **Resonant Chamber** as key portfolio demonstrations of agentic coordination.
- **Logic Update:** Clarify that "Static Synthesis" is now guided by the **Lab Actor (Sentinel)** which provides situational awareness to the pipeline.
<<<<<<< SEARCH
The backend is a sophisticated AI pipeline that indexes 18 years of raw engineering logs. It utilizes a local LLM ("Pinky") to process heavy data.
=======
The backend is a **Bicameral Synthesis Pipeline**. It uses a **"Dual-Protocol" Attendant (V2)** to coordinate a high-fidelity derivation on the 4090 Brain, grounded by a hardware-aware "Foil" (Pinky) on the local 2080 Ti.
- **Always Ready Resident:** Transitioned from a "Static Dashboard" to **[VIBE-011] Resident Peer Presence**, representing an always-on engineering environment.
- **Neural Pedigree Recall:** Driven by LoRA-hardened weights encoding 18 years of technical history directly into the model's neurons.
>>>>>>> REPLACE

### C. field_notes/research.html (Enrichment)
- **Milestone:** Add "Bicameral Evolution (March 2026)".
<<<<<<< SEARCH
                    <tr>
                        <td>Internal Debate [FEAT-071]</td>
                        <td>Moderated Consensus: Dueling independent reasoning paths to reduce hallucinations.</td>
                        <td>Multi-agent collaboration for high-stakes architectural decision making.</td>
                        <td><span class="impact-badge impact-live">Live</span></td>
                    </tr>
=======
                    <tr>
                        <td>Internal Debate [FEAT-071]</td>
                        <td>Moderated Consensus: Dueling independent reasoning paths to reduce hallucinations.</td>
                        <td>Multi-agent collaboration for high-stakes architectural decision making.</td>
                        <td><span class="impact-badge impact-live">Live</span></td>
                    </tr>
                    <tr>
                        <td>Resonant Chamber [FEAT-153]</td>
                        <td>Multi-Agent Coordination: Overhearing strategic intent to improve grounding.</td>
                        <td>Hub-level context injection between Pinky and Brain during derivation.</td>
                        <td><span class="impact-badge impact-live">Live</span></td>
                    </tr>
>>>>>>> REPLACE

---

## 📍 2. Internal & Connectivity Refactors

### A. 00_FEDERATED_STATUS.md
- **Phase Transition:** Officially close Phase 10 (Artifact Synthesis) and mark **Phase 11 (Signature Synthesis & Scaling)** as ACTIVE.
- **Bridge Update:** Document the **Resident Handshake Gate** as the primary reliability bridge between the Hub and vLLM.

### B. FeatureTracker.md (Audit)
- **Status Sync:** Ensure all FEAT-152 through FEAT-165 are marked as **ACTIVE** or **DESIGN** as per the recent implemention sweep. (Completed, but verify cross-links).

---

## 📍 3. Protocols & BKMs (The Agentic Contract)

### A. Protocols.md Update
- **BKM-014: Agentic Delegation (Context Preservation):**
    - **Rule:** Use sub-agents (`generalist`, `conductor`) for surgical implementation tasks to prevent "Manic Phases" (cognitive overload leading to lossy compression of design docs).
    - **Constraint:** Sub-agents are restricted from editing `Portfolio_Dev/*.md` files. Only the Main Agent conducts design updates.
- **BKM-015: The Bilingual Attendant (MCP Toolset):**
    - **Usage:** Standardize on native tool calls (`lab_heartbeat`, `lab_start`) instead of manual `curl` or shell hacks.
    - **Verification:** Always verify the `[BOOT_HASH]` returned by the tool to ensure sync trust.

## 📍 4. Repo Archaeology & Git Integrity

### A. Intra-Repo Migrations (Preserve Blame)
- **Forensics Archive:** Use `git mv` to relocate "Silicon Scars" (Reports from Feb 13/20, BKM Feb 15) to `HomeLabAI/docs/forensics/`.
- **Persona History:** Relocate legacy `docs/archive/PinkyAndTheBrain_Persona_Plan.md` -> `docs/forensics/persona_v1_legacy.md`.

### B. Inter-Repo Connectivity
- **Cross-Repo Indexing:** Maintain files in their birth repositories to preserve git blame history. Enrich `Portfolio_Dev/00_MASTER_INDEX.md` with absolute links to `HomeLabAI/docs/` for discoverability.

### C. Connective Enrichment
- **LAB_INFRASTRUCTURE.md:** Patch to include the **Bilingual Transport Layer** (REST port 9999, MCP stdio, Hub port 8765) to align with the Attendant V2 and Resident Handshake Gate architecture.

---

## 🛠️ IMPLEMENTATION STRATEGY
1.  **Linear Dispatch:** One file at a time to ensure fidelity.
2.  **Verification:** Use the **Neural Probe** to confirm that the changes described in the READMEs match the actual system behavior.
3.  **Traceability:** Every refactor must link back to a specific `FEAT` ID from the tracker.

**HALT. Awaiting buy-in for this documentation roadmap.**
