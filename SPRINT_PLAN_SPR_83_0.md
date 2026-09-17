# 📋 Sprint Plan: [SPR-83.0] The DNA Forge, Reverse DNA & Cognitive Resonance Sprint

> **Sprint Type:** Live Collaborative Sprint & Architectural Alignment  
> **Status:** IN PROGRESS (Phase 2)  
> **Date:** 2026-09-17  
> **Assigned Lead:** AGY + Sovereign Sovereign (Pair Programming)  

---

## 🧭 Consensus Trace & Verification Checklist (1–7)

| Point | Topic | Status | Key Resolution & Artifact / Code Reference |
| :--- | :--- | :--- | :--- |
| **1A** | **First-Class DNA Citizens** | ✅ CERTIFIED | All lab knowledge types (`FEAT`, `BKM`, `PHL`, `GEM`, `WIS`, `VIBE`, `DISC`, `SPRINT`, `RDNA`, `ART`) share a polymorphic schema. Registered in [`PHL-034`](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/data/philosophy_data.json) and synced to ChromaDB `philosophy_dna`. |
| **1B** | **Domain vs. Tag Law** | ✅ CERTIFIED | DNA Domain = Container/Bucket; Tag = Subject Topic. Codified in [`BKM-060`](file:///home/jallred/Dev_Lab/HomeLabAI/docs/Protocols.md#L965). |
| **1C** | **Sideways Re-Bucketing Flow** | ✅ CERTIFIED | Promotion is lateral migration (`DISC`/`WIS` $\rightarrow$ `BKM` $\rightarrow$ `PHL`) with bidirectional `explicit_links` preserved. Updated in [`FEAT-585`](file:///home/jallred/Dev_Lab/Portfolio_Dev/FeatureTracker.md#L3132). |
| **2** | **Active DNA Forge Studio** | ✅ IN PROGRESS | Consolidates knowledge viewing into active synthesis and human-in-the-loop polish queues ([`FEAT-582`](file:///home/jallred/Dev_Lab/Portfolio_Dev/FeatureTracker.md#L3110)). |
| **3A** | **Triage, Filler & HyDE Topology** | ✅ IN PROGRESS | Hardware timing model: CPU vector probe (sub-15ms) $\rightarrow$ M5 Air opening persona quip (15–200ms) $\rightarrow$ Local vLLM JSON routing & fallback HyDE (200–500ms). |
| **3B** | **Oracle Deliberation Prompts** | ✅ READY | Packaged 3 design inquiries + Triage Waffle + Side Effects review for Swarm Cloud Oracle consensus. |
| **3C** | **Cloud Delegation Order** | ✅ ALIGNED | Story 83.6, 83.7, 83.8 dispatched via `delegate.py --cloud`; Story 83.9–83.11 executed locally in-session. |
| **3D** | **Configurable Triage Preference** | ✅ ACTIVE | Dynamic `preferred_triage_engine` with 2x head-start lead window registered in [`FEAT-586`](file:///home/jallred/Dev_Lab/Portfolio_Dev/FeatureTracker.md#L3140). |
| **3E** | **Persona Quip Exclusivity** | ✅ CERTIFIED | Persona quips generated strictly by `DEEP_THOUGHT` (M5 Air) to buy airtime for local vLLM. Updated in [`FEAT-584`](file:///home/jallred/Dev_Lab/Portfolio_Dev/FeatureTracker.md#L3124). |
| **4** | **War Stories Ingestion** | ✅ READY | Ingesting 29 `<article>` war stories from [`stories.html`](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/stories.html) into standalone `WIS-001`..`WIS-029` cards. |
| **5** | **Live Validation Mandate** | ✅ MANDATORY | Live integration test against `http://127.0.0.1:8765/v5/triage` and `/chat` ([`BKM-024`](file:///home/jallred/Dev_Lab/HomeLabAI/docs/Protocols.md)). |
| **6** | **Sprint Flow & Housekeeping** | ✅ ALIGNED | Plan $\rightarrow$ Approve $\rightarrow$ Delegate flow. Clean in-session housekeeping without blind find/replace. |
| **7** | **JITC & Ambient Hook Protocol** | ✅ CERTIFIED | Ground context dynamically at runtime (`icm_hook.py`, FastEmbed probes, `BKM-060` taxonomy lookup). Added to [`AGENTS.md`](file:///home/jallred/Dev_Lab/AGENTS.md#L17). |

---

## 🎯 Sprint Objective
Consolidate knowledge curation into the **DNA Forge (`dna_forge.html`)**, formalize the **Federated DNA Taxonomy (`BKM-060`)**, restore **Discrete Multi-LoRA Adapter Training**, build the **Dynamic Triage Engine Preference Gate (`FEAT-586`)**, ingest **War Stories into `WIS` Cards**, and validate the **Unified Pre-Reflection Pipeline** end-to-end against the live Foyer daemon (`http://127.0.0.1:8765`).

---

## 🗺️ Story Breakdown & Delegation Matrix

| Story | Title | Owner | Dispatch Mode | Key Deliverables & Target Files |
| :--- | :--- | :--- | :--- | :--- |
| **83.1** | Hardware-Grouped Silicon Alignment & Lab Config Audit | `[AGY:PRIMARY]` | Local In-Session | `infrastructure.json` audit, harmonized M5_AIR port 8000 and KENDER default model. (✅ CERTIFIED) |
| **83.2** | Philosophy DNA Ingestion (`PHL-032`, `PHL-033`) | `[AGY:PRIMARY]` | Local In-Session | Ingested `PHL-032` (Creative Process) & `PHL-033` (Human Co-Pilot) into `philosophy_dna`. (✅ CERTIFIED) |
| **83.3** | Reverse DNA (RDNA) Question Bank Engine (`FEAT-583`) | `[AGY:PRIMARY]` | Local In-Session | `rdna_questions.json`, ChromaDB `rdna` collection (26 question variants mapped to `PHL-xxx`). (✅ CERTIFIED) |
| **83.4** | Unified Vector Pre-Triage Integration (`FEAT-584`) | `[AGY:PRIMARY]` | Local In-Session | `vector_pre_triage.py` updated with `rdna` and `philosophy_dna`, 3/3 pytests passing. (✅ CERTIFIED) |
| **83.5** | Silicon Benchmark Suite Refresh | `[AGY:PRIMARY]` | Local In-Session | `bench_models.py` profile updated for M5 Air Qwen3.5-9B, live sweep & static build certified. (✅ CERTIFIED) |
| **83.6** | Dual Oracle Review: Architecture & Blast Radius Audit | `[SWARM:CLOUD]` | `delegate.py --cloud` | Dispatches architectural & blast-radius review package to Cloud Swarm on port 4097. |
| **83.7** | Discrete Multi-LoRA Nightly Training Pipeline | `[SWARM:CLOUD]` | `delegate.py --cloud` | Refactor [`nightly_lora_training.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/infra/nightly_lora_training.py) to train 4 discrete adapters (`cli_voice_v1`, `lab_history_v1`, `triage_v1`, `reviewer_v1`) into `/speedy/models/adapters/`. |
| **83.8** | Dynamic Triage Engine Preference & RDNA HyDE Bypass (`FEAT-586`, `FEAT-583`) | `[SWARM:CLOUD]` | `delegate.py --cloud` | Add `preferred_triage_engine` in [`infrastructure.json`](file:///home/jallred/Dev_Lab/HomeLabAI/config/infrastructure.json), asymmetric 2x head-start gate in [`speculative_triage.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/speculative_triage.py), and RDNA HyDE bypass ($< 0.45$). |
| **83.9** | War Stories (`stories.html`) Ingestion into `WIS` Cards | `[AGY:PRIMARY]` | Local In-Session | Parser in `dna_forge_build.py` extracting 29 `<article>` sections from [`stories.html`](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/stories.html) into structured `WIS-001`..`WIS-029` cards in `wisdom_data.json`. |
| **83.10**| DNA Forge UI & Sidebar Consolidation (`FEAT-582`) | `[AGY:PRIMARY]` | Local In-Session | Unified [`dna_forge.html`](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/dna_forge.html) (PHL/WIS/RDNA tabs), retire duplicate `wisdom.html`, update all sidebars & links. |
| **83.11**| Live Foyer Daemon End-to-End Pre-Reflection Test Suite | `[AGY:PRIMARY]` | Local In-Session | Live test in [`test_live_pre_reflection_triage.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/tests/test_live_pre_reflection_triage.py) against `http://127.0.0.1:8765/v5/triage` and `/chat`. |

---

## 🚀 Swarm Delegation Execution Commands (`BKM-034`)

### Story 83.6: Dual Oracle Swarm Review
```bash
HomeLabAI/.venv/bin/python3 HomeLabAI/src/tests/delegate.py \
  --sprint 83 \
  --story 83.6 \
  --title "Dual Oracle Review: Architecture & Blast Radius Audit" \
  --reference Portfolio_Dev/SPRINT_PLAN_SPR_83_0.md \
  --target "HomeLabAI/src/logic/speculative_triage.py,HomeLabAI/src/infra/nightly_lora_training.py" \
  --cloud \
  --prompt "Conduct in-depth dual oracle review: 1) Architecture & Triage Waffle buffering vs streaming, EWMA lead window formula, and RDNA vector boundaries; 2) Side effects & blast radius audit for VRAM collision, UI SSE sync, and wisdom.html deprecation."
```

### Story 83.7: Discrete Multi-LoRA Nightly Training Pipeline
```bash
HomeLabAI/.venv/bin/python3 HomeLabAI/src/tests/delegate.py \
  --sprint 83 \
  --story 83.7 \
  --title "Discrete Multi-LoRA Nightly Training Pipeline" \
  --reference Portfolio_Dev/SPRINT_PLAN_SPR_83_0.md \
  --target "HomeLabAI/src/infra/nightly_lora_training.py" \
  --cloud \
  --prompt "Refactor nightly_lora_training.py to sequentially train 4 discrete LoRA adapters: cli_voice_v1, lab_history_v1, triage_v1, reviewer_v1 into /speedy/models/adapters/ with clean CUDA memory deallocation between runs."
```

### Story 83.8: Dynamic Configurable Triage Engine Preference & RDNA HyDE Bypass
```bash
HomeLabAI/.venv/bin/python3 HomeLabAI/src/tests/delegate.py \
  --sprint 83 \
  --story 83.8 \
  --title "Dynamic Triage Engine Preference & RDNA HyDE Bypass" \
  --reference Portfolio_Dev/SPRINT_PLAN_SPR_83_0.md \
  --target "HomeLabAI/config/infrastructure.json,HomeLabAI/src/logic/speculative_triage.py" \
  --cloud \
  --prompt "Implement preferred_triage_engine (M5_AIR vs LOCAL_VLLM) in infrastructure.json and speculative_triage.py with dynamic lead window and sub-15ms RDNA vector probe HyDE bypass (distance < 0.45)."
```
