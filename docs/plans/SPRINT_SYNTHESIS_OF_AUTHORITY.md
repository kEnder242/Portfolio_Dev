# Sprint Plan: SPR-11-03 "Synthesis of Authority"
**Date:** Feb 23, 2026 | **State:** ACTIVE | **Sprint ID:** SPR-11-03

## 🎯 Primary Objective
Refine the Lab's output quality by shifting the Brain from "Verbose Derivation" to "Synthesis of Authority" and hardening the persona boundaries (The Shadow Moat).

## 🧬 Feature Set
### [FEAT-109] Synthesis of Authority
- **Logic:** Refactor the Brain's system prompt to prioritize concise, actionable insights over long technical lectures.
- **Mechanism:** Replace "Verbose Rigor" with "Adaptive Synthesis." Encourage the use of a hidden `<thought>` process if necessary, but keep the user-facing output laconic.

### [FEAT-110] The Shadow Moat (Banter Sanitizer)
- **Logic:** Prevent Pinky's personality traits (Narf, Poit) from leaking into the Shadow Brain responses.
- **Mechanism:** Implement a post-generation regex filter in `acme_lab.py` that strips interjections from any source containing "Brain".

### [FEAT-111] Cognitive Identity Lock
- **Logic:** Harder negative constraints in the Shadow Brain system prompt.
- **Mechanism:** Explicit "ANTI-BANTER" tokens and role enforcement for local failover nodes.

## 🧪 Testing Methodology
### Proposed Tests:
1.  **`test_persona_leakage.py`**
    *   **Goal:** Verify that responses from "Brain" or "Brain (Shadow)" do not contain "Narf" or "Poit".
    *   **Status:** TODO.
2.  **`test_synthesis_brevity.py`**
    *   **Goal:** Measure word count for complex queries.
    *   **Target:** Reductions of > 50% in output volume without loss of technical accuracy.
    *   **Status:** TODO.

## 🗺️ Architectural Invariants
1.  **Brevity is Authority:** Genius mouse persona shouldn't feel the need to over-explain.
2.  **Source Integrity:** The Hub is the final arbiter of source-appropriate tone.
3.  **Zero-Latency Sanitization:** Regex filters must be sub-millisecond.

---
*Sprint Active. Targeting Eloquence.*
