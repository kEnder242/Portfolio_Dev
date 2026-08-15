# 📜 SPRINT PLAN: Sprint 54.0 — Preamble & HyDE Division of Labor Inversion

> **Status:** READY FOR EXECUTION / SPRINT 54
> **Focus:** Formal Inversion of the Federated Division of Labor: Deep Thought Triage/Preamble vs. Pinky (LoRA) HyDE Synthesis.

---

## 📖 **1. Contextual Narrative & Architectural Background**

### 🏛️ **The Original Blueprint (Sprint 46 Archive)**
When the **"Open HyDE"** concept was first anchored in `00_FEDERATED_STATUS.md` and `SPRINT_PLAN_SPR_46_0.md`, Pinky's roleplay preamble (*"Egad Brain! I bet Glibc C-arenas are caching PyTorch allocations!"*) was captured live to eliminate extra LLM latency:
* **The Intention**: Pinky held our custom fine-tuned **`cli_voice_v1` LoRA** adapters on `z87-Linux`. Because her LoRA was trained directly on 18 years of lab notes, resume artifacts, and validation BKMs, **Pinky possessed the exact domain weights needed to produce high-precision HyDE hypothetical documents** (`[VALIDATION]`, `[STRATEGY]`, `[SRE]`).
* **The Gap**: Deep Thought on Node Kender (RTX 4090) was idle during initial turn ignition while heavy models warmed up.

---

### 🚨 **The Inversion Discovery & Sprint 51/52 Forensics**
A forensic search across the sprint archives revealed that the formal **5-Stage Division of Labor Inversion** was documented in **Sprint 51 and Sprint 52** ([`SPRINT_51_EXECUTION_LEDGER.md:L115-159`](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/SPRINT_51_EXECUTION_LEDGER.md#L115-L159) and [`SPRINT_PLAN_SPR_52_0.md:L22-30`](file:///home/jallred/Dev_Lab/Portfolio_Dev/SPRINT_PLAN_SPR_52_0.md#L22-L30)):

* **Sprint 46–48 Baseline**: Deep Thought generated HyDE vectors sequentially inside `cognitive_hub.py`, missing Pinky's fine-tuned LoRA domain weights.
* **Sprint 51 Execution Ledger**: Formally reshuffled the pipeline into the **5-Stage Waterfall**:
  1. **Stage 1 (Deep Thought on Kender 4090 / $t=0$)**: Zero-Latency Preamble & Intent Triage (*"Narf! Checking validation logs..."*).
  2. **Stage 2 (Pinky vLLM + LoRA)**: Pinky generates the 3-Part HyDE hypothetical document (`[VALIDATION]`, `[STRATEGY]`, `[SRE]`) using her fine-tuned `cli_voice_v1` LoRA weights.
  3. **Stage 3 (Brain Node)**: ChromaDB vector retrieval & short technical answer.
  4. **Stage 4 (Deep Thought)**: Strategic Synthesis if `importance >= 0.7`.
  5. **Stage 5 (Pinky Out-Loud & Drainer)**: Final vibe review & Waterfall Drainer Pop delivery.

---

### 🔄 **The Inversion Mandate: Restoring the True Division of Labor**
In Sprint 54, we implement and certify this exact 5-stage architecture in code (`cognitive_hub.py` and `router.py`):

```
[User Query]
    │
    ▼ Stage 1: Deep Thought (Kender 4090 / WSL2) at t=0
    ├── 1. Instant Intent Triage & Domain Gate (CASUAL vs DEEP_TECHNICAL)
    └── 2. Zero-Latency UI Preamble Streaming ("Narf! Checking validation logs...")
    │
    ▼ Stage 2: Pinky (z87-Linux / vLLM + LoRA)
    └── 1. Fine-Tuned HyDE Vector Synthesis ([VALIDATION], [STRATEGY], [SRE])
    │
    ▼ Stage 3: ChromaDB Vector Engine (port 8001)
    └── 1. Query ChromaDB using Pinky's LoRA-grounded HyDE vector
    │
    ▼ Stage 4: Round Table Synthesis (Brain / Kender)
    └── 1. Deep Technical Answer & Waterfall Drainer Delivery
```

---

## 🗝️ **2. Key Management & Environment Architecture**

To support OpenRouter model routing without exposing secret keys in git repositories:

* **Location**: Secret keys are stored in `~/.config/environment.d/70-openrouter-key.conf` and exported in `~/.bashrc`.
* **OpenCode Configuration**: Referenced dynamically via `{env:OPENROUTER_API_KEY}` inside `~/.config/opencode/opencode.json`.
* **Git Hygiene**: `*.conf`, `.env`, and secret config files remain strictly outside git boundaries and ignored via `.gitignore`.

---

## 🏛️ **3. Core Architectural Patterns Incorporated from Backlog Audit**

From our audit of the previous overwrite (Task 53.7/53.8 in `SPRINT_PLAN_SPR_52_0.md`), we are explicitly incorporating the following **high-value design patterns** into Sprint 54:

1. **3-Tier Memory Topography**:
   - **Layer 1 (Bedrock Tier)**: Star artifacts + `career_compass.json` Tier 1 Anchor Map (<300 tokens) loaded directly into system prompt context.
   - **Layer 2 (Archive Tier / KB)**: ChromaDB vector collections (`artifact_vault`, `journal_kb`, `lab_journal`). Targeted by Pinky's LoRA-grounded HyDE vectors.
   - **Layer 3 (Raw Telemetry Tier)**: Real-time hardware telemetry (`nvidia-smi` / DCGM GPU metrics, RAPL power caps) + raw notes in `~/knowledge_base`.

2. **BKM-015 Compliance (Judge-Driven Casual Exit)**:
   - Zero hardcoded keyword arrays or regex pre-baked HyDE bypass lists.
   - HyDE synthesis is judge-driven: if a query does not match the 4 KB domains (e.g. casual turn `"hi"`), HyDE synthesis naturally evaluates to empty `""`, letting the ChromaDB query exit cleanly without forcing a hallucinated vector.

3. **Dynamic HyDE Prompt Loading (`data/hyde_domain_map.json`)**:
   - Extract hardcoded prompt text in `HYDE_SYNTHESIS_PROMPT` out of Python inline code into `HomeLabAI/src/data/hyde_domain_map.json`.
   - `cognitive_hub.py` loads `hyde_domain_map.json` dynamically at startup with non-fatal fallback.

4. **Real VRAM Probing & Gauntlet Repair (`[FEAT-456]`)**:
   - Integrate `pynvml` / `nvidia-smi` VRAM probing into `nightly_forge.py` and repair `run_live_lab_gauntlet.sh` verifier paths.

---

## 🔬 **4. Code Architecture Audit & Potential Kinks (Deep Dive Grounding)**

Before delegating implementation tasks, we audited `cognitive_hub.py` and `router.py` to identify potential friction points ("kinks"):

### ⚠️ **Identified Kink 1: Hardcoded Keyword Domain Gate in `router.py` vs BKM-015**
- **Current Code**: In `router.py:L1024-1029`, Stage 1 checks `is_domain_match = any(kw in query_lower for kw in domain_keywords)` using a static array of ~25 string keywords (`"pcie"`, `"rapl"`, `"bkm"`, etc.).
- **Kink**: This violates BKM-015 (no hardcoded keyword arrays). If a user asks a technical question using terms outside those 25 words, Stage 1 emits `casual_bypass` and skips HyDE!
- **Resolution**: Refactor Stage 1 in `router.py` to load `domain_keywords` dynamically from `HomeLabAI/src/data/hyde_domain_map.json` (or use a dynamic pre-reflection triage pass).

### ⚠️ **Identified Kink 2: Ordering of Tier 1 vs Tier 2 in `resolve_hyde_vector()`**
- **Current Code**: In `cognitive_hub.py:L1374-1397`, Tier 1 calls `self.residents["thought"].call_tool("deep_think", ...)` (Deep Thought on Kender), while Tier 2 reads `triage_result.get("hyde_vector_text")` (Pinky local vLLM).
- **Kink**: This is the exact inverted code we identified! It forces a call to Deep Thought first, bypassing Pinky's fine-tuned LoRA.
- **Resolution**: Invert the logic inside `resolve_hyde_vector()`:
  - **Tier 1 (Pinky + LoRA)**: Read `triage_result.get("hyde_vector_text")` generated by Pinky's local vLLM pass with her active `cli_voice_v1` LoRA weights.
  - **Tier 2 (Deep Thought Remote)**: Fallback to Kender `deep_think` only if Pinky's local vLLM pass is empty or unavailable.
  - **Tier 3 (Casual Bypass / Direct Floor)**: Empty string `""` exit.

### ⚠️ **Identified Kink 3: Preamble Crosstalk vs. Output Duplication**
- **Current Code**: `_spawn_deep_thought_preamble()` emits a crosstalk frame at $t=0$, but `cognitive_hub.py` also formats output buffers.
- **Kink**: Ensure `_spawn_deep_thought_preamble()` handles zero-latency preamble streaming to the UI without duplicating response text in Stage 5.

---

## 🛠️ **5. Sprint 54 Implementation Stories & Delegation Specifications**

These stories are designed for seamless execution via `delegate.py` or direct AGY execution:

---

### 🎴 **STORY 54.1 — `FEAT-437`: Invert `resolve_hyde_vector()` to Prioritize Pinky LoRA**
* **Goal**: Refactor `resolve_hyde_vector()` in `cognitive_hub.py` so Pinky's local vLLM pass (holding `cli_voice_v1` LoRA weights) acts as Tier 1 HyDE generator, with Kender `deep_think` as Tier 2 fallback.
* **Target File**: [`HomeLabAI/src/logic/cognitive_hub.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py#L1372-L1406)
* **Delegation Command**:
  ```bash
  python3 HomeLabAI/src/tests/delegate.py --story 54.1 --title "FEAT-437 Invert resolve_hyde_vector for Pinky LoRA Tier 1" --file "HomeLabAI/src/logic/cognitive_hub.py" --details "Invert Tier 1 and Tier 2 in resolve_hyde_vector so Pinky vLLM hyde_vector_text is Tier 1 and Kender deep_think is Tier 2 fallback." --verification "pytest HomeLabAI/src/tests/test_feat437_resolve_hyde_vector.py" --dir "/home/jallred/Dev_Lab/HomeLabAI"
  ```
* **Verification Gate**: `test_feat437_resolve_hyde_vector.py` 9/9 PASS; server logs show `[FEAT-437][TIER1]` calling Pinky LoRA HyDE.

---

### 🎴 **STORY 54.2 — `FEAT-437`: Dynamic HyDE Domain Map (`hyde_domain_map.json`)**
* **Goal**: Remove inline prompt string literals and hardcoded keyword arrays from `router.py` and `cognitive_hub.py`. Move 4-domain terms into `HomeLabAI/src/data/hyde_domain_map.json` and load dynamically at startup.
* **Target Files**:
  * [`HomeLabAI/src/data/hyde_domain_map.json`](file:///home/jallred/Dev_Lab/HomeLabAI/src/data/hyde_domain_map.json)
  * [`HomeLabAI/src/v5/foyer/router.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/v5/foyer/router.py#L1024)
  * [`HomeLabAI/src/logic/cognitive_hub.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py#L1374)
* **Delegation Command**:
  ```bash
  python3 HomeLabAI/src/tests/delegate.py --story 54.2 --title "FEAT-437 Dynamic HyDE Domain Map Loading" --file "HomeLabAI/src/data/hyde_domain_map.json" --details "Extract hardcoded domain keywords and synthesis prompts into hyde_domain_map.json and load dynamically in router.py and cognitive_hub.py." --verification "pytest HomeLabAI/src/tests/test_qpr_hyde.py" --dir "/home/jallred/Dev_Lab/HomeLabAI"
  ```
* **Verification Gate**: `test_qpr_hyde.py` 5/5 PASS; no hardcoded domain arrays in `router.py`.

---

### 🎴 **STORY 54.3 — `FEAT-456`: Real VRAM Probing & Gauntlet Repair**
* **Goal**: Replace `get_vram_usage()` stub in `nightly_forge.py` with real `pynvml` / `nvidia-smi` GPU VRAM probes. Repair test path in `run_live_lab_gauntlet.sh` (`src/debug/test_live_fire_triage.py`).
* **Target Files**:
  * [`HomeLabAI/src/infra/nightly_forge.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/infra/nightly_forge.py#L193)
  * [`HomeLabAI/src/tests/run_live_lab_gauntlet.sh`](file:///home/jallred/Dev_Lab/HomeLabAI/src/tests/run_live_lab_gauntlet.sh)
* **Delegation Command**:
  ```bash
  python3 HomeLabAI/src/tests/delegate.py --story 54.3 --title "FEAT-456 Real VRAM Probing and Gauntlet Repair" --file "HomeLabAI/src/infra/nightly_forge.py" --details "Implement pynvml/nvidia-smi probing in get_vram_usage() and fix test_live_fire_triage.py path in run_live_lab_gauntlet.sh." --verification "bash HomeLabAI/src/tests/run_live_lab_gauntlet.sh" --dir "/home/jallred/Dev_Lab/HomeLabAI"
  ```
* **Verification Gate**: `run_live_lab_gauntlet.sh` 4/4 suites PASS; `nightly_forge.py` logs real VRAM in MB.

---

### 🎴 **STORY 54.4 — `FEAT-457`: FeatureTracker Alignment & Submodule Synchronization**
* **Goal**: Update `FeatureTracker.md` statuses for Sprints 50–53 from `PROPOSED` to `COMPLETED` with commit hashes. Sync git submodule pointers in parent `Dev_Lab` repository.
* **Target Files**:
  * [`Portfolio_Dev/FeatureTracker.md`](file:///home/jallred/Dev_Lab/Portfolio_Dev/FeatureTracker.md)
  * [`Dev_Lab`](file:///home/jallred/Dev_Lab)
* **Execution**: AGY Direct.

---

## 🔍 **6. Discrepancy & Alignment Audit (Details vs. Intent)**

We audited the entire Sprint 54 plan against your overarching intent:

| Area | Stated Intent | Current Code / Doc Detail | Discrepancy Assessment | Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| **HyDE Generator** | Pinky (LoRA) produces HyDE vectors because she holds 18-year archive weights. | Code in `cognitive_hub.py` called Kender 4090 `deep_think` first as Tier 1. | **HIGH DISCREPANCY**: Code missed Pinky's LoRA advantage and added 8s timeout risk. | **FIX IN STORY 54.1**: Invert `resolve_hyde_vector()` so Pinky LoRA is Tier 1. |
| **Stage 1 Triage** | Deep Thought handles zero-latency preamble & intent triage at $t=0$. | `router.py:L1024` uses static array of 25 hardcoded keywords (`is_domain_match`). | **MEDIUM DISCREPANCY**: Hardcoded keywords violate BKM-015 (zero hardcoded arrays). | **FIX IN STORY 54.2**: Load domain map dynamically from `hyde_domain_map.json`. |
| **OpenRouter Keys** | Store keys securely outside git repositories. | OpenCode config used `{env:OPENROUTER_API_KEY}`. | **ALIGNED**: Saved key to `~/.config/environment.d/70-openrouter-key.conf`. | **NO CHANGE NEEDED**. |
| **Delegation Spec** | Concise, self-contained story cards pointing to specific files and verification commands. | Sprint plans previously mixed narrative prose with inline code diffs. | **IMPROVED**: Formatted Stories 54.1–54.4 as clean `delegate.py` command cards. | **READY FOR EXECUTION**. |

---

## 📜 **7. Sprint 54 Execution & Intent Violation Ledger**

### 📊 **Story Execution Summary**

| Story | Title | Executor | Status | Tries / Retries | Intent Alignment |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **54.1** | `FEAT-437` Pinky LoRA HyDE Inversion | AGY Direct | **COMPLETED** | 1 (Direct) | **100% Intent Aligned**: Restored Pinky local vLLM as Tier 1 HyDE generator. |
| **54.2** | `FEAT-437` Dynamic HyDE Domain Map Loading | OpenAgent (OpenRouter) | **COMPLETED** | 3 (M5-Air hung $\rightarrow$ OpenRouter) | **Intent Aligned with Schema Adaptations**: Extracted keywords & prompts to JSON. |
| **54.3** | `FEAT-456` Real VRAM Probing & Gauntlet Repair | OpenAgent (OpenRouter) | **COMPLETED** | 1 (OpenRouter) | **100% Intent Aligned**: Swapped dummy VRAM stub with `nvidia-smi` CSV queries; fixed test path. |
| **54.4** | `FEAT-457` FeatureTracker Alignment & Submodule Sync | AGY Direct | **COMPLETED** | 1 (Direct) | **100% Intent Aligned**: Updated FeatureTracker, built site, synced ChromaDB, committed submodules. |

---

### 🚨 **Intent vs. 'To The Letter' Violation Ledger**

1. **Story 54.2 (HyDE Domain Map Extractor)**:
   - **Letter of Request**: Extract hardcoded domain keywords and synthesis prompts into `HomeLabAI/src/data/hyde_domain_map.json`.
   - **Intent Violation / Divergence**: OpenAgent attempted to read `AGENTS.md` and synthesized a full project architecture document alongside `hyde_domain_map.json` because the initial prompt lacked exact JSON key schemas.
   - **Mitigation / Remediation**: Validated `hyde_domain_map.json` structure, verified with `test_qpr_hyde.py` (5/5 PASSED), and committed only clean schema-compliant code.

2. **OpenAgent Delegation Topology Stalls**:
   - **Initial Condition**: M5-Air (`my-m5-air`) was configured with a **262K context window**, causing prompt KV memory thrashing and API hangs during heavy delegation dispatches.
   - **Remediation**:
     1. Capped M5-Air context limit to **32K (32,768)** in `opencode.json`.
     2. Re-assigned heavy orchestrator roles (`prometheus`, `sisyphus`, `atlas`) to **OpenRouter (`nvidia/nemotron-3.5-lightning:free`)**.
     3. Assigned light sub-agent execution roles (`sisyphus-junior`, `hephaestus`) to M5-Air for fast local execution.

---

### 📌 **Stalled / Hung Dispatch Log**

*   **Attempt 1 (Story 54.1 on M5-Air)**: Hung on LM Studio context allocation (`262K`). Process killed after 340s timeout; completed AGY Direct.
*   **Attempt 2 (Story 54.2 on M5-Air)**: Returned `APIError: Prompt context exceeded`. Switched provider to OpenRouter; completed in 28s.
*   **Attempt 3 (Story 54.3 on OpenRouter)**: Dispatched cleanly via OpenRouter Nemotron-3.5; completed in 150.8s with full `nvidia-smi` implementation.

---

## 📜 **8. Post-Execution Log — FEAT-028 Deep Thought Regression Fix (2026-08-14)**

> **Recorded by:** Sisyphus (orchestrator) — appended post-deployment per user request.
> **Commit:** `549aecd` — `fix(foyer): restore Deep Thought ping->API health check and gate HyDE routing on lab state`

### 🚨 **The Regression Found — A FEAT Ignored During the V4→V5 Refactor**

During Sprint 54 execution, a production incident surfaced: the lab was **hammering the remote Deep Thought node (KENDER, 192.168.1.26:11434) with a request every ~7–8 seconds while HIBERNATING**.

**Root Cause Chain:**
1. `get_vram_status()` returns `self.status.vocal` — which is `false` during HIBERNATING.
2. `cognitive_hub.py` used `if not self.get_vram_status():` as the *only* gate for routing every query to remote Deep Thought for HyDE synthesis (the "Brain Early-Reply" path).
3. Result: while hibernating, **every turn triggered a remote generation call** — exactly the traffic the lab should produce **zero** of during hibernation.

**The Deeper Cause (refactor scar):** The original ping→API health check — `resolve_thought_url()` + `check_thought_health()` — **was deleted in commit `ca31a51` during the V4→V5 promotion** (Sprint 31). A later commit (`cd48b9b`) then *re-wired the routing trigger to `not get_vram_status()`*, coupling "should I call Deep Thought" to a **VRAM/vocal state flag instead of a reachability probe**. The deletion of the health check + the re-wiring of the trigger together recreated the exact hammering behavior FEAT-028 was built to prevent — a classic "FEAT ignored in refactor" regression: the feature survived in documentation and routing logic, but its protective probe layer was silently dropped.

### 🛠️ **The Fix (3 Files, +297/−30)**

**`src/v5/foyer/router.py`** (+233) — restored and V5-adapted the deleted health machinery:
- `resolve_thought_url()` — config-driven target resolution from `config/infrastructure.json` (`nodes.thought.primary` → `http://192.168.1.26:11434/api/tags`); **no hardcoded machine name** (per user directive: "we can call it deep thought" — do not hardcode KENDER).
- `is_deep_thought_reachable()` — Tier 1 probe: TCP socket ping → GET `/api/tags` (2s timeout) → 200 + non-empty model list; BKM-026 60s failure penalty box (`_last_thought_fail`).
- `check_thought_health()` — [FEAT-028/FEAT-265.31] state-aware probe: **Sovereignty Gate** (aborts during `BOOTING`/`INIT`/`HIBERNATING`) → Tier 1 API check → Tier 2 Heavy Prime (1-token `/api/generate` generation probe = the FEAT-028 "Mind alive" check), gated by FEAT-134 AFK presence, FEAT-285 120s cooldown, FEAT-286.2 single-in-flight latch.
- `thought_health_loop()` — 20s periodic probe, registered in `on_startup`.

**`src/logic/cognitive_hub.py`** (+71/−26) — the routing gate correction:
- Brain Early-Reply now gated on `lab_state != "HIBERNATING"` **AND** an awaited `is_deep_thought_reachable()` probe; unreachable → fall back to local triage.
- HIBERNATING → explicit "zero remote traffic" skip (no wait loop).
- `_prime_first_try()` also hibernation-gated (no remote quip traffic while dormant).

**`src/v5/ignition/manager.py`** (+11/−12) — **Interleaved System Logs fix** (separate user directive):
- Removed the filter that suppressed `python3` / `acme_foyer` / `acme_ignition` lines from `journal_monitor`.
- **Why**: "Interleaved system logs are supposed to show what the lab is doing, not filter them out." The lab's own activity was being hidden from the UI log stream.

### ✅ **Verification & Deployment**
- `py_compile` clean on all 3 files; import smoke test: `resolve_thought_url()` → `http://192.168.1.26:11434/api/tags`; live probe against KENDER: socket ping OK, `/api/tags` 200, `llama3.1:8b` present (preferred Heavy Prime probe model).
- Committed as `549aecd`; deployed via `sudo systemctl restart lab-attendant.service`.
- Post-deploy: `127.0.0.1:8765/health` → `{"status": "ONLINE", "version": "5.0.0-foyer"}`; boot commit `549aecd`; log shows `[HEALTH] Deep Thought health loop active.`
- **Live gate confirmation**: lab was HIBERNATING at deploy time → sovereignty gate suppressed all probes (debug-level abort) → **zero remote traffic**, the exact intended behavior.

### 🧭 **The Scars (What to Avoid)**
1. **Never re-trigger remote routing off a VRAM/vocal flag.** Reachability is a *socket/API question*, not a memory-pressure question. When deleting a health-check function, grep for all trigger sites before removing it.
2. **A feature documented ≠ a feature present.** FEAT-028 survived in the sprint narrative while its probe layer was deleted in a refactor. Cross-reference FeatureTracker against live code when promoting major versions (V4→V5).
3. **Hibernation must mean zero egress.** "When we're hibernating we shouldn't be generating traffic" — any remote-generation path needs an explicit state gate, not an implicit vocal-state coincidence.
4. **Do not hardcode remote node names** — resolve from `infrastructure.json` (nodes → hosts) so node identity stays configuration data.
