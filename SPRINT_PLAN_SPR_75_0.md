# 🚀 SPRINT PLAN 75.0: Silicon Engine Resilience, Tense-Aware Triage Grounding & Zero Trust Security Hardening

**Sprint ID:** `SPR_75_0`  
**Theme:** Unsloth Nightly VRAM Quiesce & Handover, Tense-Aware Semantic Triage Flowchart, Live Host Telemetry Tool Node (`FEAT-557`), Self-Dialogue Circuit Breaker (`FEAT-558`), and Cloudflare Zero Trust Access Hardening  
**Status:** PROPOSED & READY FOR EXECUTION  
**Parent Framework:** `BKM-020` (Sprint Documentation Standard), `BKM-004` (Invariant Ground Truth), `LAB-020` (Cloudflare Infrastructure), `FEAT-213` (Autonomous Forge VRAM Handover)  
**Target Submodules:** `HomeLabAI`, `Portfolio_Dev`

---

## 🎯 Sprint Objective

Resolve the core operational friction points identified in recent session forensics:
1. **Unblock Nightly LoRA Training**: Ensure Foyer `/release_nodes` and `quiesce_vllm()` cleanly terminate vLLM to reclaim the full 11GB VRAM, and fix the dataset path bug in `nightly_forge.py`.
2. **Eliminate RAG Historical Bleed**: Deploy the Tense & Temporal Horizon Flowchart in `triage_engine.py` and activate Pinky as the Speculative Domain Foil to distinguish live lab vitals from 18-year archive queries.
3. **Hardware Telemetry Grounding (`FEAT-557`)**: Provide a real-time NVML/`psutil` host vitals tool hook so queries about current system resources return live hardware numbers rather than historical hallucinations.
4. **Self-Dialogue Circuit Breaker (`FEAT-558`)**: Sanitize multi-turn history in `CognitiveHub` to prevent Brain `<thought>` tags from triggering recursive archive search loops.
5. **Zero Trust Access Policy Review**: Audit Cloudflare Zero Trust Access policies, document domain whitelist enforcement (`@intel.com`, `@nvidia.com`, `@supermicro.com`), and verify origin header authentication in Foyer.

---

## 📜 Story Specifications

### 🔴 Story 75.1: Unsloth Nightly VRAM Quiesce & Dataset Path Fix (P1)
* **Objective:** Enable unattended 150-step Unsloth LoRA training at 2:00 AM without VRAM collisions or path errors.
* **Files:**
  * [`HomeLabAI/src/infra/nightly_forge.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/infra/nightly_forge.py)
  * [`HomeLabAI/src/v5/foyer/router.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/v5/foyer/router.py)
* **Tasks:**
  1. Fix `DATASET_PATH` in `nightly_forge.py` to use `os.path.expanduser("~/Dev_Lab/Portfolio_Dev/field_notes/data/journal_ledger.jsonl")` (eliminating `/root` path failures).
  2. Update `quiesce_vllm()` in `nightly_forge.py` to execute targeted `pkill -f vllm.entrypoints.openai.api_server` during sleep phase so physical VRAM drops from $6.8\text{GB} \rightarrow < 1.5\text{GB}$.
  3. Verify that the 30s settling loop detects VRAM $< 1500\text{MB}$ and launches `train_expert.py` cleanly.

---

### 🟡 Story 75.2: Tense-Aware Triage Flowchart & Pinky Speculative Domain Foil (P2)
* **Objective:** Implement temporal horizon discrimination in Triage and enable Pinky as a conversational clarifier for ambiguous queries.
* **Files:**
  * [`HomeLabAI/src/logic/triage_engine.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/triage_engine.py)
  * [`HomeLabAI/src/logic/cognitive_hub.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py)
  * [`HomeLabAI/src/tests/test_feedback_semantic_triage.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/tests/test_feedback_semantic_triage.py)
* **Tasks:**
  1. Update `_build_triage_mode_context()` with the Grammatical Tense & Temporal Horizon Rules:
     - *Present Tense / Imperative* (*"what's the memory?"*) $\rightarrow$ `domain: "lab_internal"` (Zero Archive RAG).
     - *Immediate Horizon / Peer Reference* (*"what did Pinky mean?"*) $\rightarrow$ `domain: "lab_internal"` (Sliding window ledger).
     - *Distant Past + Epoch Marker* (*"what did we do in 2018 for RAPL?"*) $\rightarrow$ `domain: "exp_tlm"` (ChromaDB RAG).
  2. Expand schema to support `domain: "unclear"` with `hyde_vector_text: ""` to cleanly suppress cold RAG.
  3. Wire `[MODE]: SPECULATIVE_FOIL` behavioral guidance into Pinky when `domain == "unclear"`.

---

### 🟡 Story 75.3: Live Host Telemetry Tool Node (`FEAT-557`) (P2)
* **Objective:** Allow Brain and Pinky to query physical GPU VRAM, host RAM, CPU load, and temperature dynamically.
* **Files:**
  * [`HomeLabAI/src/nodes/brain_node.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/nodes/brain_node.py)
  * [`HomeLabAI/src/equipment/live_telemetry.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/equipment/live_telemetry.py)
* **Tasks:**
  1. Expose `get_host_vitals()` as an MCP tool on `Brain` and `Lab` nodes.
  2. Return structured JSON with live GPU VRAM used/total, host RAM used/total, CPU load average, and active model residency.
  3. Ensure queries like *"what does memory look like?"* execute `get_host_vitals()` instead of searching 2014 archive notes.

---

### 🟢 Story 75.4: Self-Dialogue Sanitizer Circuit Breaker (`FEAT-558`) (P3)
* **Objective:** Prevent Brain's internal reflection `<thought>` tags from leaking into multi-turn history and triggering self-archive loops.
* **Files:**
  * [`HomeLabAI/src/logic/cognitive_hub.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/logic/cognitive_hub.py)
* **Tasks:**
  1. Update `_persist_journal_ledger()` and `turn_ledger` construction to strip `<thought>...</thought>` blocks and nested `<PINKY>/<BRAIN>` prefix tags before logging to `self.round_table_memory`.
  2. Add regex sanitizer ensuring only user utterances and final spoken character responses enter the sliding history window.

---

### 🟢 Story 75.5: Cloudflare Zero Trust Dual-Tier Access Control & Doorbell Knock Policy (P3) [COMPLETED ✅]
* **Objective:** Implement the dual-tier access gate on `jason-lab.dev` allowing VIP auto-grant for whitelisted companies (`intel.com`, `nvidia.com`, `supermicro.com`, `jabil.com`, `amd.com`, `panasonic.aero`) and a "Knock" Access Request doorbell for all other visitors requiring manual admin approval.
* **Files:**
  * [`HomeLabAI/docs/LAB_INFRASTRUCTURE.md`](file:///home/jallred/Dev_Lab/HomeLabAI/docs/LAB_INFRASTRUCTURE.md)
  * [`Portfolio_Dev/field_notes/utils/list_access_logins.py`](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/utils/list_access_logins.py)
  * [`Portfolio_Dev/docs/FIELD_NOTES_ARCHITECTURE.md`](file:///home/jallred/Dev_Lab/Portfolio_Dev/docs/FIELD_NOTES_ARCHITECTURE.md)
* **Live Deployed & Verified Policy (`notes.jason-lab.dev` / App ID `8a77121a-5cd3-4f3e-aaf0-4df2cd07cfe1`):**
  1. **Precedence 1 — `Lobby Access` (VIP Fast-Pass):**
     - **Action:** `allow`
     - **Include:** `kender242@gmail.com`, `@nvidia.com`, `@intel.com`, `@jabil.com`, `@amd.com`, `@panasonic.aero`
     - **Approval Required:** `None` (Instant OTP delivery directly to user)
  2. **Precedence 2 — `Access Request Knock` (Doorbell Approval Gate):**
     - **Action:** `allow`
     - **Include:** `everyone`
     - **Approval Required:** `true`
     - **Approval Group:** `kender242@gmail.com` (`approvals_needed: 1`)
     - **Purpose Justification Required:** `true` (`"Please state your name and purpose for visiting Jason Lab."`)
     - **Session Duration:** `24h`
* **Verification Status:** Verified against Cloudflare REST API at `2026-09-07T02:57:55Z` using active `Gemini z87` token.
