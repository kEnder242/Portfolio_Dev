# 🚀 Sprint Plan SPR-62.0: Declarative Triage Policy, Dynamic Route Incubation Sandbox & Bidirectional Traversal

**Sprint:** 62.0  
**Date:** August 25, 2026  
**Status:** ✅ DELIVERED & VERIFIED  
**Theme:** *Declarative Triage Policy Engine, Dynamic Route Incubation Sandbox (`[FEAT-472]`), and Bidirectional Traversal Dispatcher (`TOPIC_FIRST` vs. `TIME_FIRST`)*

---

## 🧭 Executive Summary & Architectural Contract

Sprint 62.0 builds upon the modularized Triage Engine of Sprint 61 to deliver a completely declarative, sandboxed, and self-tuning routing system:

1. **Declarative Triage Policy Engine (`config/triage_policy.json`)**: Extracts hardcoded vibe-to-domain rules, retrieval permissions, and distance thresholds from Python code into a validated JSON policy loaded and hot-reloaded by `src/logic/triage_policy_loader.py`.
2. **Dynamic Route Incubation Sandbox (`[FEAT-472]`)**: Establishes a three-tier lifecycle:
   - **Tier 1 (Immutable Core)**: Production-hardened `config/triage_policy.json`.
   - **Tier 2 (Mouse Sandbox)**: `config/triage_supplement.json` where resident models (Brain / Deep Thought) have full sovereignty to register, test, and incubate candidate routes (`src/logic/route_incubator.py`).
   - **Tier 3 (Solidification)**: Proven sandbox routes promoted to core policy based on evaluation metrics.
3. **Bidirectional Traversal Dispatcher (`src/logic/traversal_dispatcher.py`)**:
   - `TOPIC_FIRST`: Keyword / Silicon Spec $\rightarrow$ Epochs / Gems / BKMs (Composite HyDE).
   - `TIME_FIRST`: Time / Era / Year Anchor $\rightarrow$ Keywords / Narratives (Fuzzy Temporal Compass).
4. **Gated On-Demand RAG & Decoupled Actor Selection**: RAG parameters are optional and omitted for conversational vibes. Actor selection is decoupled from vibes, relying on natural intent loops and explicit user naming.
5. **Mandatory Live Physical Verification**: SystemD service reboot (`acme-lab.service`), 60s Quiescence window (`[FEAT-136]`), and live WebSocket gauntlet over `ws://127.0.0.1:8765/`.

---

## 📋 Granular Story Breakdown & Delegation Matrix

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│ SPRINT 62 DELEGATION TOPOLOGY (ALL DELIVERED & VERIFIED)                                 │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ Story 62.1: triage_policy_loader.py ──(OpenAgent Subagent)──> 48 Unit Tests (PASS)       │
│ Story 62.2: route_incubator.py      ──(OpenAgent Subagent)──> 54 Unit Tests (PASS)       │
│ Story 62.3: traversal_dispatcher.py ──(OpenAgent Subagent)──> 58 Unit Tests (PASS)       │
│ Story 62.4: Core Wiring & Hub       ──(AGY Orchestrator)───> 9 Integration Tests (PASS) │
│ Story 62.5: Physical Reboot & Live  ──(AGY Orchestrator)───> ws://127.0.0.1:8765 (PASS)   │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### **Story 62.1: [FEAT-467] Declarative Triage Policy Engine (`triage_policy_loader.py`)**
* **Status**: ✅ **DELIVERED & VERIFIED (48/48 Tests Green)**
* **Target Files**:
  * `HomeLabAI/config/triage_policy.json`
  * `HomeLabAI/src/logic/triage_policy_loader.py`
  * `HomeLabAI/src/tests/test_triage_policy_loader.py`
* **Satellite Responsibilities**:
  1. Provided production `config/triage_policy.json` defining standard vibes (`CASUAL`, `SUPERVISORY`, `WYWO`, `META`, `OPERATIONAL`, `FORENSIC`, `TECHNICAL`, `HISTORICAL`).
  2. Implemented `TriagePolicyLoader` with `load_policy()`, `get_vibe_rule(vibe: str)`, `get_active_vibes()`, `validate_policy_schema(policy_dict)`.
  3. Implemented non-blocking file-watch / mtime check for sub-millisecond hot-reloading.
  4. Ensured RAG parameters are optional: if omitted, `get_rag_config()` returns `None`.

---

### **Story 62.2: [FEAT-472] Dynamic Route Incubation Sandbox (`route_incubator.py`)**
* **Status**: ✅ **DELIVERED & VERIFIED (54/54 Tests Green)**
* **Target Files**:
  * `HomeLabAI/config/triage_supplement.json`
  * `HomeLabAI/src/logic/route_incubator.py`
  * `HomeLabAI/src/tests/test_route_incubator.py`
* **Satellite Responsibilities**:
  1. Maintained `config/triage_supplement.json` for mouse-defined candidate routes (`MOUSE_DEF: <name>`).
  2. Implemented `RouteIncubator` with `register_candidate_route(vibe_name, intent, target_domain, traversal_mode=None, creator="Brain")`.
  3. Implemented `record_route_hit(vibe_name, success: bool, feedback: str = "")`.
  4. Implemented `get_candidate_routes()`, `export_for_solidification(vibe_name)`, and `retire_candidate_route(vibe_name)`.

---

### **Story 62.3: [FEAT-117/467] Bidirectional Traversal Dispatcher (`traversal_dispatcher.py`)**
* **Status**: ✅ **DELIVERED & VERIFIED (58/58 Tests Green)**
* **Target Files**:
  * `HomeLabAI/src/logic/traversal_dispatcher.py`
  * `HomeLabAI/src/tests/test_traversal_dispatcher.py`
* **Satellite Responsibilities**:
  1. Implemented `TraversalDispatcher` resolving `TOPIC_FIRST` vs `TIME_FIRST` vs `STREAM_REPLAY`.
  2. For `TOPIC_FIRST`: synthesizes/formats topic-first queries with silicon and protocol keywords, prioritizing `artifact_vault` and `behavioral_dna`.
  3. For `TIME_FIRST`: extracts temporal year anchors (e.g. `2018`, `2024`, `Sprint 35`) and applies temporal filtering bounds on `career_ledger` and `artifact_vault`.
  4. For `STREAM_REPLAY` / `DREAM_CACHE`: targets short-term dream stream without touching 18-year archive.

---

### **Story 62.4: [CORE/ORCH] Core Hub Wiring & Integration Test Suite**
* **Status**: ✅ **DELIVERED & VERIFIED (9/9 Integration Tests Green)**
* **Target Files**:
  * `HomeLabAI/src/logic/cognitive_hub.py`
  * `HomeLabAI/src/nodes/archive_node.py`
  * `HomeLabAI/src/logic/triage_engine.py`
  * `HomeLabAI/src/tests/test_sprint62_integration.py`
* **Accomplishments**:
  1. Wired `TriagePolicyLoader` and `RouteIncubator` into `triage_engine.classify_vibe_and_domain()`.
  2. Wired `TraversalDispatcher` into `ArchiveNode.get_context()`.
  3. Built and executed `test_sprint62_integration.py` verifying full end-to-end integration across all 4 components.
  4. Verified full suite: **328/328 tests passing in < 9s**.

---

### **Story 62.5: [OPS-01] Mandatory Stack Restart & Live-Fire Verification Gauntlet**
* **Status**: ✅ **DELIVERED & VERIFIED (5/5 Live WebSocket Turns Passed)**
* **Target Files**:
  * `HomeLabAI/src/tests/test_live_sprint62_e2e.py`
* **Accomplishments**:
  1. Physical restart of `acme-lab.service` via `systemctl --user restart acme-lab`.
  2. Observed 60s Quiescence stability window (`[FEAT-136]`).
  3. Executed live WebSocket gauntlet over `ws://127.0.0.1:8765/`:
     - Turn 1 (Supervisory Feedback): `PASS`
     - Turn 2 (WYWO / Dream Stream): `PASS`
     - Turn 3 (Technical Topic-First): `PASS`
     - Turn 4 (Historical Time-First): `PASS`
     - Turn 5 (Mouse Route Sandbox `[FEAT-472]`): `PASS`
