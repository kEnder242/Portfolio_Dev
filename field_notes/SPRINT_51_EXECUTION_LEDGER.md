# 📜 SPRINT 51 EXECUTION & ARCHITECTURAL DISCUSSION LEDGER

> **Sprint**: `SPR-51-0` (Conversational Polish, Deep Thought Refinement, Mobile Crosstalk UI & Thermal Guardrails)  
> **Date**: August 08, 2026  
> **Status**: Execution Active  

---

## 🏛️ Architectural Discussions & Key Insights Log

### 1. Thermal Throttling & Host Reboot Retrospective
* **Incident Summary**: Host `z87-Linux` suffered an unexpected kernel/hardware reboot at 11:15 AM PDT during background delegation (`task-2613`).
* **Empirical Root Cause (`journalctl -b -1`)**:
  ```text
  Aug 08 11:12:17 z87-Linux pcp-pmie[5588]: Severe demand for real memory 69pgsout/s@z87-Linux
  Aug 08 11:12:17 z87-Linux pcp-pmie[5588]: CPU is experiencing thermal throttling 10853%time[cpu0]@z87-Linux ... 10859%time[cpu6]@z87-Linux
  ```
  Unthrottled C-extension thread spawns across all 8 CPU cores drove severe page swapping (`69 pgsout/s`) and 100% CPU thermal throttling, triggering a host reset.
* **Remediation & Permanent Hardening (`LAB-099`)**:
  * **SystemD Process Priority**: Added `Nice=19` and `IOSchedulingClass=3` to `~/.config/systemd/user/opencode-core.service.d/override.conf`.
  * **Worker Thread Caps**: Exported `OMP_NUM_THREADS=2`, `OPENBLAS_NUM_THREADS=2`, `MKL_NUM_THREADS=2`, `TORCH_NUM_THREADS=2` in `delegate.py`.
  * **Foyer Thermal Watchdog**: Integrated CPU package thermal zone probe (`/sys/class/thermal/thermal_zone3/temp`) into `scheduled_tasks_loop()`. If CPU temp $\ge 78^\circ\text{C}$, background loops automatically pause for 15s.

---

### 2. SystemD Swap Preservation (`MemorySwapMax=3.0G`)
* **Discussion Note**: When setting `MemoryHigh=3.0G` and `MemoryMax=3.5G` via `systemctl --user set-property`, SystemD's cgroup v2 manager automatically defaulted `MemorySwapMax` to `0B`.
* **Resolution**: Updated `override.conf` to explicitly set `MemorySwapMax=3.0G` and stored permanent rule in ICM (`01KZHA6A7DTKQXQM489C00STEK`): *"User explicitly wants Swap enabled (`MemorySwapMax=3.0G`) for opencode-core.service. Never disable or zero out swap."*

---

### 3. Persona Boundary Hardening (Zero Regex Censorship, `FEAT-451`)
* **Discussion Note**: Deep Thought pre-reflections occasionally leaked Pinky's catchphrases (`"Narf!"`, `"Poit!"`).
* **BKM Compliance**: Ad-hoc regex string-matching (`re.sub("narf", ...)`) was rejected as a symptom patch.
* **Resolution**: Grounded Deep Thought in `BRAIN_PERSONA_SPEC` in `cognitive_hub.py`. System prompt explicitly enforces that Deep Thought represents the Brain's pre-conscious analytical stream (calm, non-interactive), strictly forbidding Pinky catchphrases.

---

### 4. Fast Offline HyDE Map Gating & Async Decoupling (`FEAT-452` / `FEAT-455`)
* **Crucial Architectural Realization**: Preamble is zero-latency async and fires at $t=0$ upon WebSocket frame receipt—BEFORE triage runs or LLM JSON parsing completes. Preamble cannot wait for triage, or it loses its zero-latency async nature.
* **The HyDE Domain Map Contract**: Fast offline intent gating in `_spawn_deep_thought_preamble()` evaluates raw query text against the 4 Lab Domains:
  1. `exp_tlm`: Silicon Telemetry & PCIe RAS
  2. `exp_bkm`: SRE Playbooks & Diagnostics
  3. `exp_for`: Forensic Logs & Panic Tracebacks
  4. `lab_history`: 18-Year Archive & Career History
* **Behavior**:
  * **Domain Match**: Emits `Deep Thought: Domain match detected. Synthesizing Composite HyDE...`
  * **Casual / Greeting**: Emits `Deep Thought: Casual greeting/query detected. Bypassing HyDE...`, sets `hyde_vector_text = ""`, and skips ChromaDB RAG entirely without hardcoded keyword arrays (BKM-015 compliant).

---

## 📊 Completed Stories Execution Summary

| Story | Feature ID | Status | Verification | Commit Hash / Output |
| :--- | :--- | :--- | :--- | :--- |
| **Story 1** | `FEAT-451` | **COMPLETED** | `test_sprint51_escapes.py` (6/6 PASS) | `fix(persona): replace negative prompt words with positive Brain persona grounding...` |
| **Story 2** | `FEAT-452` | **COMPLETED** | `test_qpr_hyde.py` (5/5 PASS) | `feat(stories-1-2): implement 4-Domain HyDE map contract...` |
| **Story 3** | `FEAT-455` | **COMPLETED** | `test_integration_foyer.py` (3/3 PASS) | `feat(story-3): add fast offline HyDE map gating to async preamble` |
| **Story 4** | `FEAT-453` | **COMPLETED** | Mobile UI Check & Scan Librarian | `feat(story-4): route diagnostic floods into scrollable crosstalk bar` |
| **Story 5** | `LAB-099` | **COMPLETED** | Thermal Probe & SystemD Overrides | `feat(story-5): implement thermal zone monitoring and worker thread caps` |
| **Story 6** | `FEAT-454` | **COMPLETED** | **Full Gauntlet: 14/14 PASSED (48.13s)** | `test(story-6): add test_sprint51_escapes.py covering persona bleed, dual-flow HyDE, and cold-start hibernation` |

---

## 📜 SPRINT 51 PHASE 2: LORA HISTORY RETROSPECTIVE & 5-STAGE WATERFALL REPORT

### 1. 🕵️‍♂️ Historical Deep Dive: When Did We Lose LoRA Training?

From a search across `FeatureTracker.md` and historical sprint plans (`SPR-14`, `SPR-18`, `SPR-22`, `SPR-34`, `SPR-35`):

* **Sprint 14–18 (The Origin of Nightly Training)**:
  * We built the **Nightly Forge (`train_expert.py` with Unsloth)** to train `cli_voice_v1`, `shadow_brain_v2`, and `lab_sentinel_v1`.
  * It ran at 2:00 AM. Unsloth required stopping vLLM to free all VRAM on the 11GB RTX 2080 Ti for PyTorch backpropagation, taking the lab **completely offline for 1 hour**.
* **Sprint 22 & Sprint 34 (When It Blocked & Deadlocked)**:
  * *Sprint 22*: The 1-hour training lockdown created the *"Lying Status Anomaly"*—if a user connected over WebSocket, the server hung or threw errors because vLLM was offline.
  * *Sprint 34 (V5 Modular Refactor)*: The `/train` endpoint was omitted from `FoyerRouter`. When `IgnitionManager` triggered the forge, stopping vLLM caused logical nodes to become `None`, producing a **silent deadlock**.
* **Sprint 35 (Resilient Character Fallback & Deprecation)**:
  * `FEAT-158` (Resilient Character Fallback) merged persona instructions directly into System Context (`BRAIN_SYSTEM_PROMPT`, `PINKY_SYSTEM_PROMPT`). Because prompt injection worked reliably and didn't lock up the GPU for 1 hour, **the Unsloth training loop was left disabled**.

---

### 🛡️ 2. The 4 Stability Requirements for LoRA Restoration

To safely restore physical LoRA adapters without crashing or taking the lab offline:

1. **Model Compatibility**: Target standard attention projections (`q_proj`, `v_proj`, `k_proj`, `o_proj`) on `Llama-3.2-3B` weights.
2. **Runtime Stability**: Ensure `loader.py` dynamically requests adapters via vLLM `--enable-lora` with graceful fallback to base weights if an adapter is missing.
3. **Adapter Availability**: Maintain physical ~20MB adapter directories in host storage.
4. **Non-Disruptive Nightly Training (Kender Offloading)**:
   * **Never stop z87-Linux vLLM during user hours.**
   * **Offload Training to Kender**: Run Unsloth / PEFT training on Node Kender (RTX 4090 / WSL2) in the background during nightly passes. 
   * Once training completes, rsync the lightweight 20MB adapter file to z87-Linux and hot-reload via vLLM REST API in $< 10\text{ms}$!

---

### 🔄 3. The Reshuffled 5-Stage Division of Labor Waterfall

```mermaid
flowchart TD
    WS["User Query via WebSocket (ws://localhost:8765)"] --> STAGE1

    subgraph STAGE 1: Preamble & Triage (Kender Host / t=0)
        STAGE1["Deep Thought / Lab Node on Kender (Ollama / 4090)"]
        STAGE1 -- "Parallel Pass 1" --> CS["Pre-Reflection Crosstalk Stream (#crosstalk-bar)"]
        STAGE1 -- "Parallel Pass 2" --> TR_DATA["Triage Output: casual, vibe, importance, domain map"]
        OFFLINE["Local Offline Foyer Fallback (z87-Linux)"] -. "If Kender Offline" .-> TR_DATA
    end

    TR_DATA --> STAGE2

    subgraph STAGE 2: HyDE & Persona Alignment (Pinky Node)
        STAGE2["Pinky Node (vLLM + LoRA)"]
        STAGE2 -- "Casual Turn" --> RAG_EXIT["RAG Fast-Path Exit (0ms) -> Pinky Out-Loud Dialogue"]
        STAGE2 -- "Domain Match" --> HYDE["Pinky predicts 'What Jason would say / Archive Document' -> 3-Part HyDE"]
    end

    HYDE --> STAGE3

    subgraph STAGE 3: Short Technical Answer (Brain Node)
        STAGE3["Brain Node (Right Hemisphere)"]
        STAGE3 --> RAG["Query ChromaDB (artifact_vault / career_ledger)"]
        RAG --> SHORT_ANS["Short, High-Density Technical Answer (Blue Bubble)"]
    end

    SHORT_ANS --> STAGE4

    subgraph STAGE 4: Strategic Synthesis (Deep Thought / Kender)
        STAGE4{"importance >= 0.7 or vibe == STRATEGIC?"}
        STAGE4 -- Yes --> DT_SYNTH["Deep Thought Strategic Synthesis & Critique"]
        STAGE4 -- No --> STAGE5
        DT_SYNTH --> STAGE5
    end

    STAGE5 --> WD

    subgraph STAGE 5: Pinky Sanity Review & Out-Loud Delivery
        STAGE5["Pinky Final Sanity / Vibe Check & Out-Loud Speech"]
        WD["Waterfall Drainer (foyer_queue.jsonl) -> Pop Mode UI"]
    end
```

### 1. 🔀 Division of Labor: Parallel Preamble & Dynamic Inference Architecture

```mermaid
flowchart TD
    A["Raw User Query (WebSocket)"] --> B["Deep Thought Preamble (Kender Host / $t=0$)"]
    
    subgraph Parallel Execution at t=0
        B -- "Instant Pre-Thought" --> C["Crosstalk UI Bar (#crosstalk-bar)"]
        B -- "Zero-Latency RAG Gate" --> D{"ChromaDB rag_registry (< 5ms)"}
    end

    subgraph Dual-Flow Branching
        D -- "Casual Turn ('hello')" --> E["Bypass HyDE & ChromaDB RAG"]
        E --> F["Pinky (Left Hemisphere - Out-Loud Warm Response)"]

        D -- "Domain Match ('RAPL / PCIe')" --> G["vLLM Base Engine (RTX 2080 Ti)"]
        G -- "LoRA Adapter: jason-voice" --> H["Brain / Deep Thought (Right Hemisphere - Technical Analysis)"]
    end
```

* **Zero-Latency RAG Gate**: ChromaDB is an in-memory SQLite/Parquet vector index that opens in $< 5\text{ms}$. It evaluates semantic distance against domain anchors before vLLM finishes waking up ($15\text{--}20\text{s}$).
* **Preamble Flow**: Deep Thought emits natural pre-thoughts directly into `recent_crosstalk`, which feeds into Pinky/Brain without hardcoded scripted text.

---

### 2. 🕵️‍♂️ Audit of Nightly Passes & LoRA Adapter Status

#### **What Currently Runs During Nightly Passes**
1. **`dream_node.py`**: Consolidates 24-hour `journal_ledger.jsonl` into ChromaDB collection `lab_journal` and generates the "WYWO Morning Briefing" in `nightly_dialogue.json`.
2. **`mass_scan.py` / `refine_gem.py` / `nibble_v2.py`**: Continuous burn pipeline indexing raw notes into ChromaDB `artifact_vault` and upgrading Rank 2/3 notes to Rank 4/5 "Gems".

#### **Audit Result: Missing LoRA Adapter Training**
* **Status**: **MISSING (Future Backlog)**.
* **Finding**: The system currently performs vector indexing, gem refinement, and dream brief synthesis—**not LoRA weight training**.
* **Phase 2 Backlog Proposal**: Implement `train_jason_voice_lora.py` during nightly passes using Unsloth/TRL or MLX. It will compile refined Gems and dialogue ledgers into a lightweight ~20MB LoRA adapter (`jason-voice-adapter`) served natively by vLLM (`--enable-lora`).

---

### 📋 3. Backlog Realignment

1. **Telemetry Context Suppression & Persona Realignment**: Suppress over-amplified "telemetry engineer" phrasing in `lab_node.py:L10`, `cognitive_hub.py`, and system prompt templates. Refactor primary identity to **Silicon Validation & Systems Platform Engineer**.
2. **Dynamic ChromaDB RAG Registry (`rag_registry`)**: Store collection manifests and resume domain anchors in a $<5\text{ms}$ ChromaDB collection for dynamic HyDE domain resolution.
3. **Nightly LoRA Adapter Generation (`train_jason_voice_lora.py`)**: Train a ~20MB persona/voice adapter during nightly burn passes for vLLM Multi-LoRA serving.
