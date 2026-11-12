# 📋 SPRINT PLAN 112.1: Decoupled ClaraDB Grounding, The MO Standard & Conversational Untangling

**Parent Frameworks:** `BKM-015` (Prompt Engineering & Formatting), `BKM-018` (Orchestrator-First Mandate), `BKM-024` (Live Verification), `BKM-049` (Multi-Tier Swarm Governance), `BKM-062` (Ground Truth Verification), `BKM-077` (Conversational Anchor Tracking), `BKM-082` (Historical Grounding & 5-Sprint Lookback), `BKM-086` (Paved-Path Sprint Protocol / AFK), `BKM-088` (Cognitive Prompt Governance), `BKM-090` (Layer 1 Orchestrator Governance), `BKM-097` (Roll-Up Audit Protocol), `BKM-100` (4-Tier Epistemic Memory Architecture), `BKM-101` (Live Shakedown Protocol), `[FEAT-659]` (Semantic Scope Resolution), `[FEAT-685]` (Centralized Timeout Management).  
**Sprint Horizon:** November 12, 2026 – November 16, 2026  
**Status:** 🚀 PLANNING / NARRATIVE ROLL-UP  
**Sprint Lead:** `[AGY:PRIMARY]` (Antigravity Autonomous Pair)  
**Tracking Mode:** In-Tree Append-Only Ledger (`BKM-081`)

---

## 🛑 Pre-Flight Checklist Gate (`BKM-082 §GATE` / `BKM-086 §1.1`)
- [ ] **1. 5-Sprint Lookback**: Reviewed SPR-108 through SPR-112.0 for traps, sentinels, and regression vectors (`BKM-082 §2.1`).
- [ ] **2. Mistakes-Avoided Ledger**:
  - *Mistake 1 (L2 As Accidental Censor)*: Avoided allowing high-level career abstracts (`career_ledger`) to restrict ClaraDB RAG queries, ensuring low-level work history stores (`artifact_vault`, `lab_journal`) remain fully accessible.
  - *Mistake 2 (The 100% AGY:PRIMARY Bypass)*: Codified Item 4.1 in `Protocols.md` to prevent sole-owner authoring without an explicit in-prompt operator waiver (`BKM-049 §3.4` / `BKM-086 §Pillar 3`).
  - *Mistake 3 (Shallow End-to-End Scoring)*: Avoided relying solely on opaque `critic_score >= 0.70`, replacing it with an out-of-band Modus Operandi (MO) Expectation Vector.
  - *Mistake 4 (Wisdom Pigeonholing)*: Avoided mischaracterizing low-level datacenter platform engineering collateral (PECI, Simics, transition plans) as philosophical "wisdom gems".
  - *Mistake 5 (Hardcoded Re-Ignition Timeouts)*: Centralized `engine_reignition_probe_timeout_sec` (240s) in `lab_accountability_thresholds.json` under `[FEAT-685]`.
- [ ] **3. Oracle Review**: Adversarial audit completed and appended via Cloud Synthesizer (`BKM-007` / `BKM-061` / `delegate.py --mode oracle`).
- [ ] **4. Delegation Gate (`BKM-049` / `BKM-086 §Pillar 3`)**: Dispatched to `[SWARM:LOCAL]` or `[SWARM:CLOUD]` via `delegate.py`.
- [ ] **4.1 Sole-Owner & Zero-Delegation Tripwire (`BKM-049 §3.4` / `BKM-086 §Pillar 3`)**: Verified AGY is NOT the sole owner across 100% of sprint stories and zero delegation was assigned.
- [ ] **5. Risk Assessment**: Evaluated blast radius of modifying `traversal_dispatcher.py` collection expansion, Brain continuity tagging, and watchdog MO evaluation.
- [ ] **6. BKM Invariant & Anti-Bypass Audit**: Verified plan against `BKM-101` (Live Shakedown), `BKM-024` (Live Silicon Gate), `BKM-044` (Attendant Authority), and `BKM-084` (Dropped Threads Governance).

---

## 📜 1. The Narrative: Decoupled ClaraDB Grounding, The MO Standard & Conversational Continuity

### 1) Layer 2 as Connective Tissue (Abolishing the Censor)
* **The Diagnostic**: In Sprint 112.0, triage correctly identified the prompt *"Examine the Kayak and Montana platform transition and native PECI execution"* as `domain="work_history"`, mapping to `"career_ledger"`. However, [`traversal_dispatcher.py:413-426`](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/traversal_dispatcher.py#L413-L426) treated `target_domains` as an absolute solitary constraint. It locked RAG search exclusively to `career_ledger`, which contains only 12 high-level resume summaries. The empirical, low-level technical records (PECI validation, Simics collateral, 18-year notes) living in `artifact_vault` and `lab_journal` were completely masked.
* **The Invariant Law**: Layer 2 (Career Compass / Resume Ledgers) is **optional connective tissue** to bridge eras and organize context—it must **never act as an information censor**.
* **The Decoupled Resolution**: When triage resolves a technical or historical inquiry to `career_ledger`, ClaraDB uses Layer 2 as an index to establish era anchors, while fanning search into the underlying ground-truth collections (`artifact_vault`, `lab_journal`, `discovery`). If Layer 2 yields nothing meaningful, Brain simply drops the L2 chunk; the lower-level evidence still flows through unhindered.

---

### 2) The Modus Operandi (MO) Standard & Out-of-Band Judicial Audit
* **2.1 Excision of the Wisdom Red Herring**: Technical validation artifacts (PECI, Simics automation, hardware handoffs) are concrete **work history**, not philosophical wisdom gems. Pigeonholing low-level engineering collateral into `wisdom_dna` distracted from resolving the RAG retrieval flow.
* **2.2 The Equivalence of Terms**: `MO` $\equiv$ `tags per stage` $\equiv$ `expectations`.
  - **The Blindness Invariant**: Runtime models (Pinky, Deep Thought, Brain, and the MLX Judge) are completely **BLIND** to the MO during turn generation. The MO is never injected into resident prompts.
  - **The Out-of-Band Auditor**: The MO exists exclusively out-of-band to evaluate the critic and the pipeline during nightly audits (`standalone_accountability_watchdog.py`).
  - **The Conditional Pass Standard**: An MO expectation can declare `permissible_outcome: "REFUSAL_MANDATORY"` when a topic genuinely has zero records in the lab. If Pinky correctly refuses, it earns a **Conditional Pass**. Conversely, claiming absence on a record that exists in ClaraDB is flagged as an unambiguous **LAZY_REFUSAL_DEFECT (False Negative Green Lie)**.
* **2.3 The 4 Expectation Sources (ABCD Framework)**:
  - **Source A (`Test Probe`)**: Fixed synthetic benchmark archetypes with frozen stage expectations.
  - **Source B (`Nightly AGY`)**: Curated stage expectations authored during sprint planning or retro reviews.
  - **Source C (`Nightly Oracle`)**: Fully autonomous 02:00–06:00 AM Cloud Oracle pass that mines fresh journal entries, synthesizes test primers, and compiles their expected stage tags.
  - **Source D (`Human`)**: Direct operator-specified primer and ground-truth expectation assertions.
  - **Anti-Consensus Bubble Invariant**: Expectation authoring is strictly quarantined from execution results. Post-generation review is evaluated against pre-established MO vectors to prevent expectation bleed.
  - **Canonical MO Ledger Schema**: Stored in [`Portfolio_Dev/field_notes/data/mo_expectations_ledger.jsonl`](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/data/mo_expectations_ledger.jsonl) with flexible per-stage expectation columns and execution history tracking.

---

### 3) Conversational Continuity: Untangling Bleed Without Goldfish Memory
* **3.1 Cohesion vs. Contamination**: In human dialogue, retaining entities across turns (e.g. remembering a workgroup discussed two turns ago) is desirable **working memory and conversational cohesion**. Suppressing history causes amnesia. However, un-annotated history causes models to conflate prior organizational topics with new low-level hardware inquiries.
* **3.2 Brain CONTINUITY_VECTOR Tagging**:
  - In Stage 1/2, Brain evaluates the relationship between the incoming primer and trailing session history, tagging:
    - `[CONTINUITY_VECTOR: THREAD_CONTINUATION]`: Deepening an ongoing topic.
    - `[CONTINUITY_VECTOR: TOPIC_PIVOT]`: Shifting to a new subject.
* **3.3 Deep Thought Untangling Directive**:
  - When `TOPIC_PIVOT` is tagged, Deep Thought's Stage 3 prompt is hydrated with an explicit untangling directive:
    > *"Jason has pivoted from the prior discussion to a distinct technical subject. Do not conflate the two or penalize missing entities from the prior turn. Guide Pinky to address the new subject directly."*
  - This allows Pinky to naturally transition (*"Shifting gears from the workgroup to the platform handoff..."*) without hallucinating missing entities or dropping working memory.

---

### 4) Infrastructure Timeout Governance (`FEAT-685`)
* Centralized `engine_reignition_probe_timeout_sec: 240.0` in [`lab_accountability_thresholds.json`](file:///home/jallred/Dev_Lab/HomeLabAI/config/lab_accountability_thresholds.json) and dynamically wired into [`nightly_forge.py:_v1_models_blocking_probe()`](file:///home/jallred/Dev_Lab/HomeLabAI/src/infra/nightly_forge.py), eliminating the 180s false-alarm re-ignition warning during cold dual-GPU model loads.
