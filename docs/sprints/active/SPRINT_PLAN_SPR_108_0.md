# ⚡ SPRINT PLAN 108.0: Live Silicon Grounding & Self-Dialogue Circuit Breaker

**Sprint ID:** `SPR_108_0`  
**Theme:** Direct Real-Time Hardware Grounding (`FEAT-557`), Self-Dialogue Sanitizer Circuit Breaker (`FEAT-558`), and Triage Feedback Snapping (`FEAT-559`).  
**Status:** 📋 **PLANNED / READY FOR REVIEW**  
**Parent Frameworks:**
- [`BKM-086`]: The Paved-Path Sprint Protocol (AFK / Sovereign Execution)
- [`BKM-043`]: Master 4-Anchor Prompt Standard (Surgical Line & Grep Anchors)
- [`BKM-062`]: Fail-Fast & Explicit Failure Propagation Mandate ("Green-Lie Prevention")
- [`BKM-081`]: Pre-Flight Mistake Avoidance Ledger
- [`BKM-082`]: 5-Sprint Historical Lookback & Mistake Prevention
- [`BKM-085`]: Historical Pre-Regression Correlation Protocol
- [`FEAT-557`]: Live Host Telemetry Node & Real-Time Hardware Grounding
- [`FEAT-558`]: Self-Dialogue Sanitizer Circuit Breaker
- [`FEAT-559`]: Triage Feedback Domain Snapping & Prompt Interception
- [`INS-049`]: Dam Building: The Law of Epistemic Hydraulics and Paved Flow

**Target Silicon Nodes:**
- `z87-Linux`: Local RTX 2080 Ti (Llama-3.2-3B-AWQ base on port 8088 / `cli_voice_v1` LoRA)
- `ChromaDB`: Port 8001 (`behavioral_dna`, `feature_dna`, `wisdom_dna`)
- `lab-attendant.service`: Port 8765

---

## 🛡️ Pre-Flight Mistakes Avoided Ledger (`BKM-081` / `BKM-082`)

### 0.1 5-Sprint Historical Lookback Summary (`BKM-082 §2.1`)
- **SPR-103**: Decouple-and-Stitch Architecture (`BKM-083`) & Multi-Stage Replay Pipeline (`FEAT-645`). *Historical Lesson:* Stage isolation prevents cascading timeouts.
- **SPR-104**: Continuous Multiplier Token Pacing (`FEAT-523`) & Excision of Casual Vibe Bypass. *Historical Lesson:* Direct waterfall processing prevents node bypass.
- **SPR-105**: Decoupled Tri-Anchor Waterfall & Universal Context Fencing (`BKM-087`, `FEAT-660`). *Historical Lesson:* Concise positive fences prevent negative-priming hallucinations.
- **SPR-106**: Two-Dimensional Gem Epistemics & Polymorphic Kabal/Spine Architecture (`FEAT-662`–`FEAT-664`). *Historical Lesson:* Decoupling substance from presentation topology enables exact replay.
- **SPR-107**: Active Kabal Staging & Epistemic Bone Retirement (`FEAT-665`). *Historical Lesson:* Clean terminology and backward-compatible shims prevent session amnesia and orphaned dependencies.

### 0.2 Pre-Flight Mistakes Avoided (`BKM-082 §2.4`)
1. **The Heavy Subprocess Shelling Trap**: Avoid running expensive shell commands like `nvidia-smi` inside user turn execution loops. Use fast in-memory C-bindings (`pynvml` / `psutil` via `live_telemetry.get_host_vitals()`) to keep telemetry collection under 5ms.
2. **The Historical RAG Hardware Hallucination Trap**: When users ask "What is our current memory/VRAM usage?", standard semantic RAG searches retrieve historical specifications or past debug reports from 2024–2026. Telemetry intent must route directly to live hardware sensors, completely bypassing historical document retrieval.
3. **The Multi-Turn Self-Echo Loop**: When the LLM generates `<thought>` internal monologues or includes persona prefixes like `Brain:` or `Pinky:`, un-sanitized history injection causes the model to mimic its own prior scratchpads on subsequent turns, deteriorating into a self-dialogue loop. Sanitization must strip `<thought>...</thought>` blocks and role prefixes before history is fed into the prompt builder.
4. **The Over-Aggressive Regex Stripping Trap**: Sanitizers must operate strictly on assistant turns and preserve legitimate user-submitted code snippets or XML tags.

---

## 🏛️ Executive Summary & Master Narrative

Sprint 108.0 addresses two persistent operational issues identified in forensic session analysis (`copilot_mice_feedback_forensics_report.md`):

1. **Physical Grounding over Historical Memory (`FEAT-557`)**: The lab frequently answers inquiries about live memory, GPU temperature, or hardware headroom using outdated documentation retrieved via RAG. We wire `live_telemetry.get_host_vitals()` directly into `CognitiveHub`, snapping telemetry inquiries to live silicon metrics.
2. **Auto-Regressive Health & Circuit Breaking (`FEAT-558`)**: Multi-turn conversations degrade when model reasoning artifacts (`<thought>` tags, internal prompts) leak into conversation history buffers. We establish a strict multi-turn sanitizer circuit breaker that strips internal monologues from prior turns before context construction.
3. **Feedback Intent Snapping (`FEAT-559`)**: User corrective turns (*"stop hallucinating"*, *"feedback: you missed the point"*) snap immediately to `domain: feedback` / `vibe: CRITIQUE`, suppressing standard RAG in favor of direct corrective reflection.

---

## 🎯 Stories & 4-Anchor Specifications

### 📊 Story 108.1: Live Host Telemetry Tool & Context Injection (`FEAT-557`)
* **Objective**: Connect `live_telemetry.get_host_vitals()` into `CognitiveHub` so live hardware questions receive deterministic physical metrics (GPU VRAM, RAM, CPU load, active model).
* **Target Files**:
  - `HomeLabAI/src/logic/cognitive_hub.py`
  - `HomeLabAI/src/infra/live_telemetry.py`
* **4-Anchor Specification**:
  - **Anchor 1**: `live_telemetry.py`: Ensure `get_host_vitals()` returns structured dictionary with sub-5ms latency and graceful non-NVIDIA fallback.
  - **Anchor 2**: `cognitive_hub.py`: Introduce `inject_live_telemetry_context(domain, query)` during waterfall context construction.
  - **Anchor 3**: Suppress historical hardware spec RAG injection when live hardware intent is detected.
  - **Anchor 4**: Verification via unit tests asserting physical memory values in prompt context.

### 📊 Story 108.2: Hardware Intent Routing in Semantic Triage (`FEAT-557`)
* **Objective**: Ensure queries asking about current VRAM, RAM, GPU, or model state classify into `domain: infra` / `intent: live_telemetry` without falling through to generic tech RAG.
* **Target Files**:
  - `HomeLabAI/src/logic/triage_engine.py`
  - `HomeLabAI/src/logic/traversal_dispatcher.py`
* **4-Anchor Specification**:
  - **Anchor 1**: In `triage_engine.py`, add live telemetry trigger patterns ("how much vram", "current memory", "hardware status", "silicon vitals").
  - **Anchor 2**: Set high confidence routing to `domain: infra` with metadata flag `is_live_telemetry: True`.
  - **Anchor 3**: Verify fast-path routing bypasses heavy vector search.
  - **Anchor 4**: Unit tests in `test_fast_triage_harness.py`.

### 📊 Story 108.3: Multi-Turn Conversation History Sanitizer Circuit Breaker (`FEAT-558`)
* **Objective**: Enforce multi-turn history sanitization in `CognitiveHub` before prompt compilation, excising prior `<thought>` blocks, internal tags, and self-speaker prefixes.
* **Target Files**:
  - `HomeLabAI/src/logic/cognitive_hub.py`
  - `HomeLabAI/src/nodes/loader.py`
* **4-Anchor Specification**:
  - **Anchor 1**: In `cognitive_hub.py`, pipe all prior assistant turns in `recent_history` through `sanitize_spoken_dialogue()`.
  - **Anchor 2**: Strip multiline `<thought>.*?</thought>` and `<role>.*?</role>` artifacts.
  - **Anchor 3**: Remove redundant leading speaker prefixes (e.g. `Brain: Brain:`, `Pinky:`) from multi-turn accumulation.
  - **Anchor 4**: Unit tests asserting clean multi-turn prompt generation with zero thought leakage.

### 📊 Story 108.4: Triage Feedback Domain Snapping (`FEAT-559`)
* **Objective**: Automatically classify explicit user critique and feedback phrases into `domain: feedback` / `vibe: CRITIQUE` with priority prompt steering.
* **Target Files**:
  - `HomeLabAI/src/logic/triage_engine.py`
  - `HomeLabAI/src/logic/cognitive_hub.py`
* **4-Anchor Specification**:
  - **Anchor 1**: In `triage_engine.py`, map critique keywords (*"stop hallucinating"*, *"you missed"*, *"incorrect"*, *"feedback"*) to `vibe: CRITIQUE`.
  - **Anchor 2**: In `cognitive_hub.py`, apply corrective framing when `vibe == "CRITIQUE"`.
  - **Anchor 3**: Suppress repetitive previous verbiage and inject self-correction prompt constraints.
  - **Anchor 4**: Verification via `test_feedback_semantic_triage.py`.

### 📊 Story 108.5: Anti-Self-Echo & Live Silicon Gauntlet Validation
* **Objective**: Run full unit test gauntlets across `HomeLabAI` and `Portfolio_Dev`, perform live query validation against the attendant daemon, and certify zero regression.
* **Target Files**:
  - `HomeLabAI/src/tests/test_feedback_semantic_triage.py`
  - `HomeLabAI/src/tests/test_integrated_fast.py`
  - `Portfolio_Dev/field_notes/tests/`
* **4-Anchor Specification**:
  - **Anchor 1**: All 9 tests in `test_feedback_semantic_triage.py` passing.
  - **Anchor 2**: `pytest field_notes/tests/` passing (24/24).
  - **Anchor 3**: Live query probe: `curl` query verifying live VRAM returns actual hardware value.
  - **Anchor 4**: Commit and register `FEAT-557` and `FEAT-558` in `FeatureTracker.md`.

---

## 🏁 Verification Checklist

- [ ] Story 108.1: Live Host Telemetry Tool & Context Injection (`FEAT-557`)
- [ ] Story 108.2: Hardware Intent Routing in Semantic Triage (`FEAT-557`)
- [ ] Story 108.3: Multi-Turn Conversation History Sanitizer Circuit Breaker (`FEAT-558`)
- [ ] Story 108.4: Triage Feedback Domain Snapping (`FEAT-559`)
- [ ] Story 108.5: Anti-Self-Echo & Live Silicon Gauntlet Validation
