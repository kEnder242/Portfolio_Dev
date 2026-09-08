# Master Sprint Plan: Sprint 45 — Configurable Sensory Policy Engine & Multimodal Model Priming

> **Sprint Narrative:**
> Following the memory sentinel recalibrations in Sprint 44, Sprint 45 shifts sensory management from a fixed pre-loaded daemon to a pluggable, highly configurable **Sensory Policy Engine** with `LAZY_TIMEOUT` (60s idle auto-deafness) as the default mode. We will also prime multimodal candidate models (`Ultravox-3B` and `Moonshine ASR`) into `loader.py` and `ai_engine_v2.py` without breaking existing Llama-3.2-3B AWQ defaults, preparing the Lab for zero-RAM-footprint audio understanding.

---

## 🎯 Master Architecture Goals & Target File Map

1. **Modular `SensoryPolicy` Engine (`LAB-090` / `FEAT-425`):**
   - **Target Files:** `HomeLabAI/src/v5/common/types.py`, `HomeLabAI/src/equipment/sensory_manager.py`, `HomeLabAI/src/v5/foyer/router.py`.
   - Enforce pluggable sensory policies: `ALWAYS_ON`, `MUTED_OFF`, `LAZY_TIMEOUT` (Default), `DEMAND_ONLY`.
   - Default: `LAZY_TIMEOUT` unloads NeMo EarNode after 60s of quiet idle and calls `malloc_trim(0)`.
   - Add `/set_sensory_policy` REST route to Foyer for live runtime policy switching.

2. **Multimodal Model Candidate Priming (`LAB-091` / `FEAT-426`):**
   - **Target Files:** `HomeLabAI/src/nodes/loader.py`, `Portfolio_Dev/field_notes/ai_engine_v2.py`.
   - Add candidate definitions for `Ultravox-3B` (`fixie-ai/ultravox-v0_4`) and `Moonshine ASR` (`usefulsensors/moonshine`) to `loader.py` engine registry and `ai_engine_v2.py`.
   - Preserve default production route (`llama-3.2-3b-awq` on port 8088).

---

## 📜 Story Backlog & Detailed Implementation Tasks

### **Story 1: `LAB-090` / `FEAT-425` — Configurable Sensory Policy Engine**
- **Target Files:** `/home/jallred/Dev_Lab/HomeLabAI/src/v5/common/types.py`, `/home/jallred/Dev_Lab/HomeLabAI/src/equipment/sensory_manager.py`, `/home/jallred/Dev_Lab/HomeLabAI/src/v5/foyer/router.py`
- **Mechanism:**
  - Define `SensoryPolicy` enum in `types.py` (`ALWAYS_ON`, `MUTED_OFF`, `LAZY_TIMEOUT`, `DEMAND_ONLY`).
  - In `sensory_manager.py`, implement 60s idle timer loop for `LAZY_TIMEOUT` policy that calls `unload_sensory_ear()` + `malloc_trim(0)` on silence.
  - In `router.py`, expose POST `/set_sensory_policy` endpoint.

---

### **Story 2: `LAB-091` / `FEAT-426` — Multimodal Candidate Priming**
- **Target Files:** `/home/jallred/Dev_Lab/HomeLabAI/src/nodes/loader.py`, `/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/ai_engine_v2.py`
- **Mechanism:**
  - Add candidate model metadata for `Ultravox-3B` and `Moonshine ASR` to `loader.py` engine registry.
  - Add model selection options in `ai_engine_v2.py` selectable via environment variables (`MULTIMODAL_AUDIO_MODEL`).

---

## 🧪 Verification & Acceptance Criteria
- [ ] `SensoryPolicy` engine supports `ALWAYS_ON`, `MUTED_OFF`, `LAZY_TIMEOUT`, and `DEMAND_ONLY` modes.
- [ ] Default `LAZY_TIMEOUT` auto-unloads NeMo EarNode after 60s silence and reclaims ~2.5 GB RAM via `malloc_trim(0)`.
- [ ] POST `/set_sensory_policy` allows live policy changes.
- [ ] `loader.py` and `ai_engine_v2.py` include `Ultravox-3B` and `Moonshine` candidate definitions without breaking existing `llama-3.2-3b-awq` production routes.
