# 🚀 Sprint Plan SPR-62.0: Declarative Triage Policy, Dynamic Route Incubation Sandbox & Bidirectional Traversal

**Sprint:** 62.0  
**Date:** August 25, 2026  
**Status:** IN PROGRESS (Heads Down Autonomous Execution)  
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
│ SPRINT 62 DELEGATION TOPOLOGY                                                            │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ Story 62.1: triage_policy_loader.py ──(OpenAgent Subagent)──> 25+ Unit Tests (Green)     │
│ Story 62.2: route_incubator.py      ──(OpenAgent Subagent)──> 25+ Unit Tests (Green)     │
│ Story 62.3: traversal_dispatcher.py ──(OpenAgent Subagent)──> 25+ Unit Tests (Green)     │
│                                                                                          │
│ Story 62.4: Core Wiring & Hub       ──(AGY Orchestrator)───> 15+ Integration Tests (Green)│
│ Story 62.5: Physical Reboot & Live  ──(AGY Orchestrator)───> ws://127.0.0.1:8765 Gauntlet │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### **Story 62.1: [FEAT-467] Declarative Triage Policy Engine (`triage_policy_loader.py`)**
* **Status**: 🔲 **READY FOR DELEGATION**
* **Target Files**:
  * `HomeLabAI/config/triage_policy.json`
  * `HomeLabAI/src/logic/triage_policy_loader.py`
  * `HomeLabAI/src/tests/test_triage_policy_loader.py`
* **Satellite Responsibilities**:
  1. Provide production `config/triage_policy.json` defining standard vibes (`CASUAL`, `SUPERVISORY`, `WYWO`, `META`, `OPERATIONAL`, `FORENSIC`, `TECHNICAL`, `HISTORICAL`).
  2. Implement `TriagePolicyLoader` with `load_policy()`, `get_vibe_rule(vibe: str)`, `get_active_vibes()`, `validate_policy_schema(policy_dict)`.
  3. Implement non-blocking file-watch / mtime check for sub-millisecond hot-reloading.
  4. Ensure RAG parameters are optional: if omitted, `get_rag_config()` returns `None`.

---

### **Story 62.2: [FEAT-472] Dynamic Route Incubation Sandbox (`route_incubator.py`)**
* **Status**: 🔲 **READY FOR DELEGATION**
* **Target Files**:
  * `HomeLabAI/config/triage_supplement.json`
  * `HomeLabAI/src/logic/route_incubator.py`
  * `HomeLabAI/src/tests/test_route_incubator.py`
* **Satellite Responsibilities**:
  1. Maintain `config/triage_supplement.json` for mouse-defined candidate routes (`MOUSE_DEF: <name>`).
  2. Implement `RouteIncubator` with `register_candidate_route(vibe_name, intent, target_domain, traversal_mode=None, creator="Brain")`.
  3. Implement `record_route_hit(vibe_name, success: bool, feedback: str = "")`.
  4. Implement `get_candidate_routes()`, `export_for_solidification(vibe_name)`, and `retire_candidate_route(vibe_name)`.

---

### **Story 62.3: [FEAT-117/467] Bidirectional Traversal Dispatcher (`traversal_dispatcher.py`)**
* **Status**: 🔲 **READY FOR DELEGATION**
* **Target Files**:
  * `HomeLabAI/src/logic/traversal_dispatcher.py`
  * `HomeLabAI/src/tests/test_traversal_dispatcher.py`
* **Satellite Responsibilities**:
  1. Implement `TraversalDispatcher` resolving `TOPIC_FIRST` vs `TIME_FIRST` vs `STREAM_REPLAY`.
  2. For `TOPIC_FIRST`: synthesizes/formats topic-first queries with silicon and protocol keywords, prioritizing `artifact_vault` and `behavioral_dna`.
  3. For `TIME_FIRST`: extracts temporal year anchors (e.g. `2018`, `2024`, `Sprint 35`) and applies temporal filtering bounds on `career_ledger` and `artifact_vault`.
  4. For `STREAM_REPLAY` / `DREAM_CACHE`: targets short-term dream stream without touching 18-year archive.

---

### **Story 62.4: [CORE/ORCH] Core Hub Wiring & Integration Test Suite**
* **Status**: 🔲 **PLANNED (AGY Orchestrator)**
* **Target Files**:
  * `HomeLabAI/src/logic/cognitive_hub.py`
  * `HomeLabAI/src/nodes/archive_node.py`
  * `HomeLabAI/src/logic/triage_engine.py`
  * `HomeLabAI/src/tests/test_sprint62_integration.py`
* **Scope**:
  1. Wire `TriagePolicyLoader` into `triage_engine.py` and `CognitiveHub`.
  2. Wire `RouteIncubator` into `CognitiveHub` and register tool for Deep Thought / Brain.
  3. Wire `TraversalDispatcher` into `ArchiveNode.get_context()`.
  4. Build and execute `test_sprint62_integration.py` verifying full end-to-end integration.

---

### **Story 62.5: [OPS-01] Mandatory Stack Restart & Live-Fire Verification Gauntlet**
* **Status**: 🔲 **PLANNED (AGY Orchestrator)**
* **Target Files**:
  * `HomeLabAI/src/tests/test_live_sprint62_e2e.py`
* **Scope**:
  1. Physical restart of `acme-lab.service` via `systemctl --user restart acme-lab`.
  2. Observe 60s Quiescence stability window (`[FEAT-136]`).
  3. Execute live WebSocket gauntlet verifying:
     - Supervisory feedback handling without RAG context.
     - WYWO dream stream lookup without 18-year career hallucination.
     - Topic-first technical query execution.
     - Time-first historical query execution.
     - Dynamic candidate route registration in sandbox.
