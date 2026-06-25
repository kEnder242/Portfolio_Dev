# 🏗️ SPRINT 34: SEMANTIC RETRIEVAL & HIERARCHICAL COGNITION
*Status: DRAFT | PLANNING*

### 🎯 MISSION
Deepen the grounding and efficiency of the Bicameral Mind. We will transition the flat semantic index into a hierarchical database, implement MCompassRAG (metadata-guided paragraph retrieval) to bypass costly real-time LLM re-ranking on Turing silicon, stabilize the multi-host dreaming pipeline by resolving V4-to-V5 rest mismatches, and deploy intelligent socket disconnect rules.

### 📋 SPRINT 34 TASKS (Task 19)
*   [ ] **Task 19.1 (Hierarchical Semantic Map)**: Refactor `build_semantic_map` in [lab_node.py](file:///home/jallred/Dev_Lab/HomeLabAI/src/nodes/lab_node.py) to cluster files, achievements, and timelines into hierarchical pillars (Strategic, Analytical, Tactical) rather than flat lists.
*   [ ] **Task 19.2 (Metadata-Guided RAG)**: Integrate `MCompassRAG` logic in [archive_node.py](file:///home/jallred/Dev_Lab/HomeLabAI/src/nodes/archive_node.py) and [cognitive_hub.py](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py). Filter paragraph-level search spaces dynamically using triage metadata (e.g. `exp_tlm`, `exp_bkm`) to minimize context noise and latency.
*   [ ] **Task 19.3 (Dreaming Pipeline Stabilization)**: Patch [dream_cycle.py](file:///home/jallred/Dev_Lab/HomeLabAI/src/dream_cycle.py) to use V5 `/wake` remote REST API endpoint instead of the deprecated V4 `/start` endpoint. Harden lock files against cross-platform collisions.
*   [ ] **Task 19.4 (Intelligent Socket Logic - FEAT-171)**: Update [router.py](file:///home/jallred/Dev_Lab/HomeLabAI/src/v5/foyer/router.py) to enforce mode-aware idle shutdown. If the server is in `DEBUG_BRAIN` mode, shut down after a 5-minute client disconnect timeout. If in `SERVICE_UNATTENDED` mode, remain online.
