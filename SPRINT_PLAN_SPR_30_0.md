# SPRINT 30: REFACTOR READINESS [MAY 22 - MAY 29]
**Status:** PLANNING | NO EXECUTION PERMITTED

## 🎯 MISSION
Prepare the Lab for a "Nuclear" architectural refactor (Sprint 31) by codifying the existing DNA. We will map all critical features to their physical code locations, modernize foundational documentation, and establish a "Hand-Crank" batch-testing protocol to ensure no functional regressions occur during the upcoming transformation.

---

## 🗺️ 1. FEATURE MAP (The DNA Matrix)
*Goal: Categorize every feature from the DNA Matrix by its role in the Lab Flow to ensure full-spectrum preservation during the Sprint 31 refactor.*

### 📍 The Inflection Core (Defining Features)
*These features represent the "Soul" of the Lab. A refactor that loses these is a failed refactor.*
| Feature | Role in the Lab Flow | Refactor Strategy |
| :--- | :--- | :--- |
| **[FEAT-071] Internal Debate (TTCS)** | The primary reasoning loop where Pinky/Shadow foil the Brain. | **Sacred**. Preserved in Orchestrator. |
| **[FEAT-207] Bicameral Airtime** | Manages the "Silicon Gap" with fillers and overhearing. | **Sacred**. Prevents "Brain Silence." |
| **[FEAT-088] Semantic Recall** | The "Receptionist" intent detection that triggers RAG. | **Critical**. Grounding must remain intent-driven. |
| **[FEAT-117] Multi-Stage RAG** | Discovery (ChromaDB) -> Acquisition (Filesystem) pattern. | **Critical**. Accuracy bedrock. |
| **[FEAT-151] Forensic Ledger** | Unified Trace Monitoring for autonomous transitions. | **Critical**. Reliability bedrock. |
| **[FEAT-368] Vocal Handshake** | Immediate persona feedback during engine ignition. | **Harden**. 100% visibility during warming. |
| **[FEAT-036] VRAM Guard** | The autonomous survival instinct against OOM crashes. | **Harden**. Port to new architecture. |
| **[FEAT-249] VRAM Hibernation Matrix**| Tiered reclamation based on activity/connectivity. | **Harden**. Essential for multi-tenancy. |
| **[FEAT-069] Resilience Ladder** | The graceful degradation (Downshift to 1B/Stub). | **Keep**. Resource efficiency. |
| **[FEAT-119] The Assassin** | Atomic port-reaping ensuring clean silicon boots. | **Keep**. Physical stability. |
| **[FEAT-067] Diamond Dreaming** | Background consolidation of raw logs into wisdom. | **Modernize**. Align with new logging. |
| **[FEAT-160] Pedigree Refinement**| Physically encoding history into model weights (LoRA). | **Keep**. Long-term neural recall. |

### ⚙️ Active Infrastructure (The Supporting Cast)
*Categorized by Lab Flow stage. These implementations are critical, but the specific code can change.*

| Flow Stage | Features | Strategy |
| :--- | :--- | :--- |
| **Lifecycle** | [FEAT-133], [FEAT-136], [FEAT-149], [FEAT-250], [FEAT-251.2], [FEAT-265], [FEAT-287], [FEAT-288] | **Consolidate**: Move all ignition/mutex logic into a single 'IgnitionAuthority'. |
| **Triage & Gate** | [FEAT-032], [FEAT-181], [FEAT-184], [FEAT-189], [FEAT-234], [FEAT-235], [FEAT-238], [FEAT-244], [FEAT-284] | **Decouple**: Separate scalar fuel math from the dispatch loop. |
| **The Debate** | [FEAT-030], [FEAT-114], [FEAT-145], [FEAT-182], [FEAT-188], [FEAT-197], [FEAT-203], [FEAT-233], [FEAT-236], [FEAT-239] | **Streamline**: Optimize the 'Overhearing' buffer for lower latency. |
| **RAG & Synthesis** | [FEAT-073], [FEAT-123], [FEAT-126], [FEAT-127], [FEAT-128], [FEAT-130], [FEAT-131], [FEAT-195], [FEAT-196], [FEAT-208], [FEAT-209] | **Expand**: Shift from year-sticky RAG to full semantic neighborhoods. |
| **The Forge** | [FEAT-213], [FEAT-214], [FEAT-161], [FEAT-162], [FEAT-204] | **Stable**: Maintain as background asynchronous tasks. |
| **Frontend/UI** | [FEAT-058], [FEAT-059], [FEAT-060], [FEAT-062], [FEAT-063], [FEAT-096], [FEAT-097], [FEAT-199], [FEAT-221], [FEAT-222], [FEAT-223] | **Keep**: Maintain high-density clinical log view. |

---

## 🎭 2. THE VIBE LEDGER (Persona & Style)
*Goal: Preserve the agentic "Flavor" that differentiates Acme Lab from a generic LLM wrapper.*

| Vibe ID | Title | Lab Behavior / Manifestation | Refactor Priority |
| :--- | :--- | :--- | :--- |
| **[VIBE-012]** | **Hemispheric Independence** | KENDER (4090) vs Local (2080) model split. No forced weight sync. | **High** |
| **[VIBE-013]** | **Sequential Blending** | **The Fuel Travel Model**: Every node thought MUST be visible. | **Sacred** |
| **[VIBE-006]** | **Neural Resonance** | The Hub as a 'Corpus Callosum'; Brain overhears Pinky's gut instinct. | **High** |
| **[VIBE-004]** | **Internal Debate** | Pinky and Brain 'duel' over technical risk for moderated consensus. | **High** |
| **[VIBE-010]** | **Diagnostic Partner** | Instant shift to 'Passive Observer' during silicon blackout/failure. | **High** |
| **[VIBE-011]** | **Always Ready** | High-availability peer presence. Offline is an anomaly, not a default. | **Med** |
| **[VIBE-008]** | **Privacy Filter** | Automatic redaction of 'Coaching' verbiage from archive synthesis. | **Critical** |
| **[VIBE-001]** | **Tool-First Instinct** | Prioritize native MCP tools over generic bash one-liners. | **Med** |
| **[VIBE-007]** | **Validation Journal** | Reverse-chronological focus with section-divider anchors. | **Med** |

---

## 🏺 3. DORMANT & DEFEATURED (Historical Record)
*Preserved to prevent re-implementing superseded logic.*
| Feature | Status | Reason for Retirement |
| :--- | :--- | :--- |
| **[FEAT-039] Banter Decay** | [DEFEATURED] | Replaced by [FEAT-152] Metabolism of Presence. |
| **[FEAT-068] Persona-Locked Dispatch**| [DEFEATURED] | Violated the "Visible" mandate. |
| **[FEAT-045] Neural Pager Interactivity**| [DORMANT] | Simplified to clinical ledger to save VRAM. |
| **[FEAT-078] Neural Trace** | [DORMANT] | Replaced by [FEAT-151] Forensic Ledger. |
| **[VIBE-014]** | [DEFEATURED] | User prefers 100% "Live Chamber" visibility over silence. |

---

## 📚 4. DOC MODERNIZATION PLAN
...

### 🔮 Proposed & Undocumented [POTENTIAL]
- **[FEAT-369] Sovereign Verifier Synthesis**: Autonomous test generation during Sprints (derived from AutoHarness).
- **[FEAT-370] Stochastic KV Optimization**: Deep cross-layer attention sharing for long-horizon sessions.

---

## 📚 2. DOC MODERNIZATION PLAN
*Goal: Align blueprints with Phase 15 "Neural Relay" reality.*

1.  **[00_MASTER_INDEX.md] Update**: 
    - [ ] Add `LAB_TIMING_REPORT.md` (The Resonant Clock).
    - [ ] Add `SPRINT_PLAN_SPR_30_0.md` to the active roadmap.
2.  **Architecture & Logic Modernization**:
    - [ ] **FIELD_NOTES_ARCHITECTURE.md**: Reflect the shift from "Sequential Handovers" to "Bicameral Debate."
    - [ ] **BICAMERAL_DISPATCH.md**: Update the Amygdala/Sentinel metaphors to include "Foil Awareness" and "Vocal handshakes."
3.  **Timing & Vitals**:
    - [ ] **LAB_TIMING_REPORT.md**: Incorporate H1/H2 wake latency benchmarks established in Sprint 29.

---

## 🧪 3. TEST MAP (The Gauntlet)
*Goal: Correlate features to physical verification scripts.*

### 🛠️ The Inflection Test Set
| Feature Group | Script(s) | Type | Gap/Strategy |
| :--- | :--- | :--- | :--- |
| **Ignition & State** | `test_attendant_sanity.py`, `test_liveliness.py` | Unit | Needs H2 -> Operational loop verification. |
| **Persona & Voice** | `test_visibility_truth.py`, `semantic_probe.py` | Integration | **Deferred Evaluation required** for semantic quality. |
| **Archival RAG** | `test_intent_recall.py`, `test_rag_logic.py` | Mock | Needs broad "No-Year" semantic trigger test. |
| **VRAM Resilience** | `test_apollo_vram.py`, `uber_5x5_hand_crank.py`| Stress | **Ultimate Pass**: 5-cycle increasing wait. |

---

## ⚙️ 4. DEFERRED SEMANTIC EVALUATION [BKM-032]
*Vibe: Human-in-the-Loop Batch Evaluation. Replaces the "Hand-Crank" nomenclature to decouple the testing pattern from the specific 5x5 stress test.*

### 🔄 Logic Flow
1.  **Batch Execution**: Run a suite of tests (like the Uber 5x5) in a non-blocking, automated sequence.
2.  **Hard Validation (System)**: The runner notifies immediately on "Hard" errors (Crashes, Connection Failures, Silence, Gibberish).
3.  **Wordy Output Capture**: The system captures the full LLM reasoning trace, the visible `<thought>` blocks, and persona nuances into a log.
4.  **AI Evaluation (The Deferred Review)**:
    - **Step**: Gemini CLI (acting as the Lead Engineer's proxy) reads the wordy output *after* the batch completes.
    - **Criteria**: Evaluates for: *Coherence, Historical Grounding, and Persona Fidelity*.
    - **Verdict**: The AI decides if the behavior "Feels Right" in the context of the Lab's 18-year history, moving beyond brittle string-matching to true semantic verification.

---

### ⚖️ LEAD ENGINEER REVIEW REQUIRED
*This plan is an artifact for Sprint 30. No code changes have been made.*
