# 📋 Sprint Plan: [SPR-83.0] The DNA Forge, Reverse DNA & Cognitive Resonance Sprint

> **Sprint Type:** Live Collaborative Sprint & Architectural Alignment  
> **Status:** IN PROGRESS (Phase 3: The DNA Forge & Cognitive Tooling)  
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
| **3C** | **Cloud Delegation Order** | ✅ ALIGNED | Story 83.6, 83.7, 83.8 dispatched via `delegate.py --cloud`; Story 83.9–83.15 executed in structured sequence. |
| **3D** | **Configurable Triage Preference** | ✅ ACTIVE | Dynamic `preferred_triage_engine` with 2x head-start lead window registered in [`FEAT-586`](file:///home/jallred/Dev_Lab/Portfolio_Dev/FeatureTracker.md#L3140). |
| **3E** | **Persona Quip Exclusivity** | ✅ CERTIFIED | Persona quips generated strictly by `DEEP_THOUGHT` (M5 Air) to buy airtime for local vLLM. Updated in [`FEAT-584`](file:///home/jallred/Dev_Lab/Portfolio_Dev/FeatureTracker.md#L3124). |
| **4** | **War Stories Ingestion** | ✅ CERTIFIED | Ingested 29 `<article>` war stories from [`stories.html`](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/stories.html) into standalone `WIS-001`..`WIS-029` cards. |
| **5** | **Live Validation Mandate** | ✅ MANDATORY | Live integration test against `http://127.0.0.1:8765/v5/triage` and `/chat` ([`BKM-024`](file:///home/jallred/Dev_Lab/HomeLabAI/docs/Protocols.md)). |
| **6** | **Sprint Flow & Housekeeping** | ✅ ALIGNED | Plan $\rightarrow$ Approve $\rightarrow$ Delegate flow. Clean in-session housekeeping without blind find/replace. |
| **7** | **JITC & Ambient Hook Protocol** | ✅ CERTIFIED | Ground context dynamically at runtime (`icm_hook.py`, FastEmbed probes, `BKM-060` taxonomy lookup). Added to [`AGENTS.md`](file:///home/jallred/Dev_Lab/AGENTS.md#L17). |

---

## 🎯 Sprint Objective
Consolidate knowledge curation into the **DNA Forge (`dna_forge.html`)**, formalize the **Federated DNA Taxonomy (`BKM-060`)**, restore **Discrete Multi-LoRA Adapter Training**, build the **Dynamic Triage Engine Preference Gate (`FEAT-586`)**, ingest **War Stories into `WIS` Cards**, build the **Bone Collection Builder & Unified Card Component**, wire the **Round-Table `propose_dna_update` Tool**, and validate the **Unified Pre-Reflection Pipeline** end-to-end against the live Foyer daemon (`http://127.0.0.1:8765`).

---

## 🗺️ Story Breakdown & Delegation Matrix

| Story | Title | Owner | Dispatch Mode | Key Deliverables & Target Files |
| :--- | :--- | :--- | :--- | :--- |
| **83.1** | Hardware-Grouped Silicon Alignment & Lab Config Audit | `[AGY:PRIMARY]` | Local In-Session | `infrastructure.json` audit, harmonized M5_AIR port 8000 and KENDER default model. (✅ CERTIFIED) |
| **83.2** | Philosophy DNA Ingestion (`PHL-032`, `PHL-033`) | `[AGY:PRIMARY]` | Local In-Session | Ingested `PHL-032` (Creative Process) & `PHL-033` (Human Co-Pilot) into `philosophy_dna`. (✅ CERTIFIED) |
| **83.3** | Reverse DNA (RDNA) Question Bank Engine (`FEAT-583`) | `[AGY:PRIMARY]` | Local In-Session | `rdna_questions.json`, ChromaDB `rdna` collection (26 question variants mapped to `PHL-xxx`). (✅ CERTIFIED) |
| **83.4** | Unified Vector Pre-Triage Integration (`FEAT-584`) | `[AGY:PRIMARY]` | Local In-Session | `vector_pre_triage.py` updated with `rdna` and `philosophy_dna`, 3/3 pytests passing. (✅ CERTIFIED) |
| **83.5** | Silicon Benchmark Suite Refresh | `[AGY:PRIMARY]` | Local In-Session | `bench_models.py` profile updated for M5 Air Qwen3.5-9B, live sweep & static build certified. (✅ CERTIFIED) |
| **83.6** | Dual Oracle Swarm Review: Architecture & Blast Radius Audit | `[SWARM:CLOUD]` | `delegate.py --cloud` | Dispatches architectural & blast-radius review package to Cloud Swarm on port 4097. (✅ CERTIFIED) |
| **83.7** | Discrete Multi-LoRA Nightly Training Pipeline | `[SWARM:CLOUD]` | `delegate.py --cloud` | Refactor [`nightly_lora_training.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/infra/nightly_lora_training.py) to train 4 discrete adapters (`cli_voice_v1`, `lab_history_v1`, `triage_v1`, `reviewer_v1`) into `/speedy/models/adapters/`. (✅ CERTIFIED) |
| **83.8** | Dynamic Triage Engine Preference & RDNA HyDE Bypass (`FEAT-586`, `FEAT-583`) | `[SWARM:CLOUD]` | `delegate.py --cloud` | Add `preferred_triage_engine` in [`infrastructure.json`](file:///home/jallred/Dev_Lab/HomeLabAI/config/infrastructure.json), asymmetric 2x head-start gate in [`speculative_triage.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/speculative_triage.py), and RDNA HyDE bypass ($< 0.45$). (✅ CERTIFIED) |
| **83.9** | War Stories (`stories.html`) Ingestion into `WIS` Cards | `[AGY:PRIMARY]` | Local In-Session | Parser in `dna_forge_build.py` extracting 29 `<article>` sections from [`stories.html`](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/stories.html) into structured `WIS-001`..`WIS-029` cards in `wisdom_data.json`. (✅ CERTIFIED) |
| **83.10**| DNA Forge UI & Sidebar Consolidation (`FEAT-582`) | `[AGY:PRIMARY]` | Local In-Session | Unified [`dna_forge.html`](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/dna_forge.html) (PHL/WIS/RDNA tabs), retire duplicate `wisdom.html`, update all sidebars & links. (✅ CERTIFIED) |
| **83.11**| Live Foyer Daemon End-to-End Pre-Reflection Test Suite | `[AGY:PRIMARY]` | Local In-Session | Live test in [`test_live_pre_reflection_triage.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/tests/test_live_pre_reflection_triage.py) against `http://127.0.0.1:8765/v5/triage` and `/chat`. (✅ CERTIFIED) |
| **83.12**| Unified DNA Card Component & Tron-Red Flagged Styling (`FEAT-588`) | `[AGY:PRIMARY]` | Local In-Session | Shared [`dna_card.js`](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/components/dna_card.js) component across Forge & Writer with Tron neon-red highlight for `[FLAGGED]`/`[AR]` cards. (✅ CERTIFIED) |
| **83.13**| Interactive Bone Collection Builder & Infill Suggester (`FEAT-589`) | `[AGY:PRIMARY]` | Local In-Session | Centered search, persistent "Bone Rack" staging shelf, and "Suggest Complementary Bones" infill in [`dna_forge.html`](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/dna_forge.html). (✅ CERTIFIED) |
| **83.14**| Round-Table `propose_dna_update` Tool & WYWO Approval Flow (`FEAT-590`) | `[AGY:PRIMARY]` | Local In-Session | Round-3 synthesis tool in [`cognitive_hub.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/nodes/cognitive_hub.py) rendering interactive proposal cards in [`intercom_v2.js`](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/intercom_v2.js). (✅ CERTIFIED) |
| **83.15**| Comprehensive Unit & Live Integration Test Suite (`BKM-024`) | `[AGY:PRIMARY]` | Local In-Session | Full pytest test suite for Bone Collections, polymorphic DNA schemas, and live Foyer/CLaRa endpoints. (✅ CERTIFIED) |
| **83.16**| Invariant Ingestion Guard: Preserve `mass_scan.py` Historical Archive | `[AGY:PRIMARY]` | Local In-Session | Affirm `mass_scan.py` and `journal_ledger.jsonl` (595 pairs) as invariant chronological note digestion pipeline. (✅ CERTIFIED) |
| **83.17**| Historical Journal to DNA Manifest Bridge (`FEAT-592`) | `[AGY:PRIMARY]` | Local In-Session | Create [`journal_to_dna_bridge.py`](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/journal_to_dna_bridge.py) to parse Rank 4/5 gems and tools into staged `[WIS]` / `[DISC]` cards in `wisdom_data.json` & `dna_manifest.json`. (✅ CERTIFIED) |
| **83.18**| Daily Chat Mining & Feedback Harvester (`serial_harvest_v2.py`) | `[AGY:PRIMARY]` | Local In-Session | Connect transcript harvester to output staged `DnaProposal` objects into `data/dna_candidates.json` for Forge review. (✅ CERTIFIED) |
| **83.19**| Nightly Pipeline Orchestration & CLaRa Vector Sync Integration | `[AGY:PRIMARY]` | Local In-Session | Update [`nightly_forge.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/forge/nightly_forge.py) Step 2 to sequence `mass_scan.py` $\rightarrow$ `journal_to_dna_bridge.py` $\rightarrow$ `dna_forge_build.py` $\rightarrow$ CLaRa ChromaDB sync. (✅ CERTIFIED) |
| **83.20**| Streamlined UI, Integrated Census HUD Search & 1-Click Approval/Archive Engine (`FEAT-593`) | `[AGY:PRIMARY]` | Local In-Session | Streamline `dna_forge_build.py`, integrate header search, add `[✅ Approve]` and `[📦 Archive]` (internal `REJECTED`) buttons, track decisions in `data/dna_decisions.json`. (✅ CERTIFIED) |



---

## 🔬 Architectural Report: Historical Ingestion Bridge & Dependency Miss Fixups

### 1. Forensic Analysis of `journal_ledger.jsonl` & `mass_scan.py`
* **Ledger Status:** Confirmed active on disk at [`Portfolio_Dev/field_notes/data/journal_ledger.jsonl`](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/data/journal_ledger.jsonl) (595 entries, 242 KB).
* **Mass Scan Architecture:** Operates over 18 years of raw historical notes (`raw_notes/`) using `nibble_v2.py`, `scan_librarian.py`, `refine_gem.py`, `clean_duplicates.py`, and `aggregate_years.py`. Step 6 (`distill_journal_ledger()`) extracts Rank 4/5 entries into bidirectional instruction-tuning pairs.
* **Invariant Law:** `mass_scan.py` is kept untouched / invariant as the raw-note digestion baseline.

### 2. The Dependency Miss & DNA Stalling Root Cause
* During the sprint's polymorphic DNA refactor (`BKM-060`), the DNA Forge (`FEAT-582`) and CLaRa-DNA vector stores were decoupled from `journal_ledger.jsonl` and raw chat logs.
* No bridge existed to convert distilled gems or chat breakthroughs into `dna_manifest.json` (`wisdom_data.json`, `rdna_questions.json`). Consequently, the DNA Census HUD watchdog flagged stalling because new findings were never manifested.

### 3. Execution Blueprint (`FEAT-592`)
```
[Historical Notes]  ──> mass_scan.py ──> journal_ledger.jsonl
                                                │
                                    [FEAT-592: journal_to_dna_bridge.py]
                                                ▼
[Chat Transcripts]  ──> serial_harvest_v2.py ──> dna_manifest.json ──> dna_forge.html & CLaRaDB (:8001)
```
1. **Bridge Execution:** `journal_to_dna_bridge.py` maps Rank 4/5 gems and code artifacts to polymorphic schema (`id`, `domain: "WIS"|"DISC"`, `title`, `summary`, `content`, `tags`, `explicit_links`, `metadata`).
2. **Nightly Integration:** Wired into `nightly_forge.py` so overnight cron sweeps automatically refresh `dna_manifest.json` and sync ChromaDB.

