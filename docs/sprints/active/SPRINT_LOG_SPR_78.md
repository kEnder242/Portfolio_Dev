# 📜 SPRINT LOG 78.0: Composable Writer Studio, Vocality Restoration & 5x5 Certification
**Date:** September 14, 2026  
**Sprint ID:** `SPR_78_0`  
**Parent Framework:** BKM-020 (High-Fidelity Sprint Documentation), BKM-046 (Fast-Path DNA Retrieval), BKM-024 (Live Verification)

---

## 🎯 Active Stories Execution Ledger

| Story ID | Owner | Focus & Objective | Status | Artifacts / Notes |
| :--- | :--- | :--- | :--- | :--- |
| **78.1** | `[AGY:PRIMARY]` | Discrete Paper Dataset Storage (`[FEAT-581]`) | **COMPLETED & CERTIFIED** | `Portfolio_Dev/papers/manifest.json`, `paper_jitc_intuition.json` |
| **78.2** | `[AGY:PRIMARY]` | Cross-Collection Citation Pointer Engine (`[FEAT-582]`) | **COMPLETED & CERTIFIED** | `Portfolio_Dev/scripts/build_writer.py`, LaTeX `main.tex`, `references.bib` |
| **78.3** | `[AGY:PRIMARY]` | Multi-Paper UI & Review Inspector Panel (`[FEAT-583]`) | **COMPLETED & CERTIFIED** | `writer.html` dropdown, chip click-to-inspect, `citation-inspector` |
| **78.4** | `[AGY:PRIMARY]` | Foyer REST Paper API Endpoints (`[FEAT-581]`) | **COMPLETED & CERTIFIED** | `HomeLabAI/src/v5/foyer/router.py` (`/paper/list`, `/paper/load`, `/paper/save`) |
| **78.5** | `[SWARM:CLOUD]` | Structural Tree View & SortableJS DNA Tag Drag-and-Drop (`[FEAT-583]`) | **IN PROGRESS** | `writer.html` DnD tag re-ordering |
| **78.6** | `[SWARM:CLOUD]` | Cascade Synthesis Reflow & 3-Tier Revision Carousel (`[FEAT-584]`) | **IN PROGRESS** | `writer.html` revision navigator & LLM reflow |
| **78.7** | `[SWARM:CLOUD]` | Multi-Doc PHL Scraping & Schema Guard (`[FEAT-585]`) | **IN PROGRESS** | Ingestion of 2024 docx, 2024-2026 doc, Intuition paper |
| **78.8** | `[AGY:PRIMARY]` | Round Table Vocality Restoration & Pre-Warm Handshake (`[FEAT-368]`, `[FEAT-486]`, `[FEAT-233]`) | **IN PROGRESS / INITIAL FIXES APPLIED** | Schema parsing fix + monolithic timeout removal in `router.py` |
| **78.9** | `[SWARM:CLOUD]` | Live 75-Min 5x5 Timed Gauntlet Certification (`BKM-010`, `BKM-050`, `[FEAT-501]`) | **QUEUED** | `test_perf_5x5_timed.py --intervals 0 5 10 20 40` |

---

## 🔬 Forensic Architectural Audit: Priming, Hibernation & Regression Root Cause

### 1. The Complete Priming Feature Map across Sprints
Ten distinct historical features have governed priming and model readiness:
* **`[FEAT-082]` (Neural Priming):** Initial background weight pre-loading into VRAM on startup.
* **`[FEAT-085]` (Brain Priming):** Restored background priming for remote sovereign engine (Windows 4090).
* **`[FEAT-087]` (Intelligent Handshake Priming):** Triggered `check_brain_health()` at the start of WebSocket handshakes.
* **`[FEAT-186]` (Pre-warm Lobby):** Predictive background warmup before routing queries.
* **`[FEAT-212]` (Direct REST Priming):** REST endpoint to force 4090 model residency verification.
* **`[FEAT-285]` (High-Fidelity Priming Telemetry):** Logged `t_warmed` and TTFT metrics for background warming passes.
* **`[FEAT-286.2]` (Strict Latching):** Gated priming to prevent concurrent duplicate prime tasks (`_priming_in_progress`).
* **`[FEAT-368]` (Vocal Handshake):** Differentiated process liveness (`UP`) from model engine readiness (`VOCAL`).
* **`[FEAT-426]` (Multimodal Candidate Priming):** Pre-warmed vision/multimodal models.
* **`[FEAT-486]` (Triage-as-Primer Live Vocality Check):** Fast 200ms socket probe + using the live triage prompt as the living primer.

### 2. Scale-to-Zero vs. Hibernation (Why `[FEAT-186]` was Defeatured)
* **Scale-to-Zero (`[FEAT-186]` Defeaturization):** Early iterations polled GPUs and sent dummy tokens every few minutes. Under modern systemd scale-to-zero, models were unallocated when idle to drop host power to ~8W, making pre-warm lobbies fight scale-to-zero eviction.
* **Hibernation (`[FEAT-249]` / `[FEAT-517]`):** Replaced scale-to-zero with a tiered VRAM matrix. In **Sprint 70.1 (`[FEAT-517]` - Hibernation Master Switch)**, hibernation was **permanently locked off** for daytime operations (`"daytime_node_residency": "PERMANENT_RESIDENT"`, `"idle_eviction_enabled": false`), keeping models resident 24/7.

### 3. Root Cause Analysis: Schema Mismatch & Monolithic Timeout Wrap
1. **Schema Mismatch in Health Loop (`HomeLabAI/src/v5/foyer/router.py#L552`):**
   * Code checked `models = [m.get("name") for m in data.get("models", [])]`, which was hardcoded for Ollama.
   * When querying M5 Air (MLX OpenAI schema), `data["data"]` was returned instead of `data["models"]`, evaluating `models` to `[]`.
   * Result: Every 20 seconds, `router.py` marked `self.thought_online = False` and placed Deep Thought in a 60s failure penalty box.
2. **Monolithic Outer Blocking Wrap (`HomeLabAI/src/v5/foyer/router.py#L377`):**
   * `run_division_of_labor` wrapped the entire `cognitive.process_query` in `asyncio.wait_for(...)`.
   * When an un-warmed M5 Air took 6-7s on its initial connection, the outer timeout tripped and fired `"The pipeline hit a snag mid-synthesis"` instead of allowing Pinky to return a sub-second response while Deep Thought finished asynchronously.

### 4. Verification & Prevention Standard
* Marked streaming path with `# [INVARIANT: NON-BLOCKING STREAMING - NEVER WRAP IN MONOLITHIC TIMEOUT]`.
* Patched `check_thought_health` to dynamically parse both Ollama (`data["models"]`) and OpenAI/MLX (`data["data"]`) schemas.
