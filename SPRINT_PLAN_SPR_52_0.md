# SPRINT PLAN: [SPR-52.0] Kender Offload & 5-Stage Division of Labor

> **Status:** READY FOR EXECUTION / SPRINT 52
> **Focus:** Kender Node (RTX 4090 / WSL2) Unsloth LoRA Training Offload & 5-Stage Reshuffled Division of Labor Pipeline.

---

## 🎯 **Strategic Objectives & Breadcrumbs**

### 1. **Node Kender Unsloth Training Offload (`[FEAT-160]` / `[FEAT-213]`)**
* **Goal**: Offload 60-step Unsloth LoRA fine-tuning (`cli_voice_v1`) to Node Kender (RTX 4090 / WSL2).
* **Workflow**: Kender runs `train_expert.py` in $< 45\text{s}$ $\rightarrow$ rsyncs 20MB `.safetensors` adapter to `z87-Linux` (`/speedy/models/adapters/cli_voice_v1`) $\rightarrow$ vLLM on `z87-Linux` hot-reloads via REST API in $< 10\text{ms}$ with zero downtime.
* **Breadcrumbs / Code Anchors**:
  * Orchestrator Script: [`HomeLabAI/src/infra/nightly_forge.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/infra/nightly_forge.py#L2-L10)
  * SystemD Service: [`~/.config/systemd/user/field-notes-nightly.service`](file:///home/jallred/.config/systemd/user/field-notes-nightly.service#L8)
  * Training Script: [`HomeLabAI/src/forge/train_expert.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/forge/train_expert.py#L18)
  * LoRA Unit Test: [`HomeLabAI/src/tests/test_vllm_adapter_swap.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/tests/test_vllm_adapter_swap.py#L1-L152)

---

### 2. **Reshuffled 5-Stage Division of Labor Pipeline**
* **Stage 1 (Preamble & Triage)**: Node Kender (Deep Thought on 4090) at $t=0$ (Foyer local fallback).
* **Stage 2 (HyDE & Persona Alignment)**: Pinky (vLLM + LoRA) generates composite HyDE or takes Fast-Path.
* **Stage 3 (Short Technical Answer)**: Brain (Right Hemisphere) queries ChromaDB for technical scars.
* **Stage 4 (Strategic Synthesis)**: Deep Thought runs strategic synthesis if `importance >= 0.7`.
* **Stage 5 (Pinky Sanity Review & Out-Loud Speech)**: Final vibe review & Waterfall Drainer delivery (`foyer_queue.jsonl`).
* **Breadcrumbs / Code Anchors**:
  * Architecture Ledger: [`Portfolio_Dev/field_notes/SPRINT_51_EXECUTION_LEDGER.md`](file:///home/jallred/Dev_Lab/Portfolio_Dev/field_notes/SPRINT_51_EXECUTION_LEDGER.md#L45-L85)
  * Router Mechanics: [`HomeLabAI/src/v5/foyer/router.py`](file:///home/jallred/Dev_Lab/HomeLabAI/src/v5/foyer/router.py#L5-L10)

---

### 3. **Backlog Technical Items**
1. **Telemetry Context Suppression & Persona Realignment**: Audit `lab_node.py:L10` and `cognitive_hub.py` to refactor identity to **Silicon Validation & Systems Platform Engineer**.
2. **Dynamic ChromaDB `rag_registry` Collection**: Implement metadata advertisement for Acme-Lab visible collections.

---

## 🛠️ **Sprint 52 Task List**

- [ ] **Task 52.1**: Implement `train_jason_voice_lora.py` on Node Kender for nightly Unsloth passes.
- [ ] **Task 52.2**: Integrate `rsync` adapter sync step into `nightly_forge.py`.
- [ ] **Task 52.3**: Implement Stage 1 Kender Triage & Stage 2 Pinky HyDE in `router.py`.
- [ ] **Task 52.4**: Perform Telemetry Context Suppression in `lab_node.py:L10` and `cognitive_hub.py`.
- [ ] **Task 52.5**: Execute full 5-stage gauntlet verification (`test_rude_gauntlet.py`, `test_vllm_adapter_swap.py`).
