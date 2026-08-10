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

- [x] **Task 52.1**: Implement `train_jason_voice_lora.py` on Node Kender for nightly Unsloth passes. *(impl spec locked — dispatched for Kender deployment; Silicon validation pending post-dispatch)*

### Task 52.1 — Kender Unsloth Training Offload (`train_jason_voice_lora.py`)

**CLI:** `python3 train_jason_voice_lora.py <dataset_jsonl> <output_lora_dir> [steps] [base_model]` — defaults `steps=60`, `base_model="unsloth/Llama-3.2-3B-Instruct-bnb-4bit"`; canonical path `~/kender_forge/train_jason_voice_lora.py` (Node Kender / WSL2, RTX 4090).

**Perf Gate:** 60-step pass `< 45s` on the 4090, timed by the script itself; outputs `adapter_model.safetensors` (~20MB) + `adapter_config.json`.

```python
#!/usr/bin/env python3
"""
[FEAT-160] [SPR-52.0] Kender Unsloth Training Offload (RTX 4090 / WSL2, BF16).
Canonical path: ~/kender_forge/train_jason_voice_lora.py
"""
import os
import sys
import time

os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

try:
    from unsloth import FastLanguageModel
    import torch
    from trl import SFTTrainer
    from transformers import TrainingArguments
    from datasets import load_dataset
except ImportError:
    print("Unsloth not installed on Kender. Aborting — no mock fallback in production path.")
    sys.exit(1)

def train_jason_voice_lora(dataset_path: str, output_dir: str, steps: int = 60,
                           model_name: str = "unsloth/Llama-3.2-3B-Instruct-bnb-4bit"):
    """[SPR-52.0] Train Rank-16 LoRA adapter on RTX 4090 (BF16)."""
    print(f"Starting Kender training on {dataset_path} -> {output_dir} ({steps} steps)")
    t0 = time.time()

    max_seq_length = 2048
    dtype = None
    load_in_4bit = True

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = model_name,
        max_seq_length = max_seq_length,
        dtype = dtype,
        load_in_4bit = load_in_4bit,
    )

    model = FastLanguageModel.get_peft_model(
        model,
        r = 16,
        target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_alpha = 16,
        lora_dropout = 0,
        bias = "none",
        use_gradient_checkpointing = "unsloth",
        random_state = 3407,
        use_rslora = False,
        loftq_config = None,
    )

    dataset = load_dataset("json", data_files=dataset_path, split="train")

    def formatting_prompts_func(examples):
        # [FIX] Robust key detection to handle diverse datasets (Sentinel vs Voice vs History)
        available_keys = list(examples.keys())

        # Determine which fields to use
        instr_key = "instruction" if "instruction" in available_keys else ("prompt" if "prompt" in available_keys else None)
        out_key = "output" if "output" in available_keys else ("response" if "response" in available_keys else ("text" if "text" in available_keys else None))

        if not instr_key or not out_key:
            print(f"❌ DATASET SCHEMA ERROR: Found keys {available_keys}")
            raise KeyError("Missing required keys. Needs 'instruction' or 'prompt' and 'output' or 'response'.")

        instructions = examples[instr_key]
        outputs      = examples[out_key]
        texts = []
        for instruction, output in zip(instructions, outputs):
            text = f"User: {instruction}\n\nAssistant: {output}" + tokenizer.eos_token
            texts.append(text)
        return { "text" : texts, }

    dataset = dataset.map(formatting_prompts_func, batched = True,)

    trainer = SFTTrainer(
        model = model,
        tokenizer = tokenizer,
        train_dataset = dataset,
        dataset_text_field = "text",
        max_seq_length = max_seq_length,
        dataset_num_proc = 2,
        packing = False,
        args = TrainingArguments(
            per_device_train_batch_size = 1,
            gradient_accumulation_steps = 8,
            warmup_steps = 5,
            max_steps = steps,
            learning_rate = 2e-4,
            # [SPR-52.0] RTX 4090 is BF16-capable (unlike Turing 2080 Ti) — bf16 forced.
            # Flash-attention / triton kernels available on 4090 (SM 8.9).
            fp16 = False,
            bf16 = True,
            logging_steps = 1,
            optim = "adamw_8bit",
            weight_decay = 0.01,
            lr_scheduler_type = "linear",
            seed = 3407,
            output_dir = "outputs",
            report_to = "none",
        ),
    )

    trainer.train()

    model.save_pretrained(output_dir)
    elapsed = time.time() - t0
    print(f"Saved adapter to {output_dir}")
    print(f"[PERF] 60-step pass completed in {elapsed:.1f}s (budget < 45s)")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 train_jason_voice_lora.py <dataset_jsonl> <output_lora_dir> [steps] [base_model]")
        sys.exit(1)

    dataset_in = sys.argv[1]
    output_out = sys.argv[2]
    steps_in = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    model_in = sys.argv[4] if len(sys.argv) > 4 else "unsloth/Llama-3.2-3B-Instruct-bnb-4bit"

    train_jason_voice_lora(dataset_in, output_out, steps=steps_in, model_name=model_in)
```

### Task 52.1 — Implementation Disposition

- **Deployment Target:** `~/kender_forge/train_jason_voice_lora.py` (Node Kender / WSL2, RTX 4090).
- **Output Artifacts:** `adapter_model.safetensors` (~20MB) + `adapter_config.json` via `save_pretrained()`, consumed by Task 52.2 rsync sync (KENDER_ADAPTER_STAGE = `~/kender_forge/adapters/cli_voice_v1/`).
- **Perf Gate:** 60-step pass < 45s on 4090 (BF16, flash-attention / triton on SM 8.9); self-timed at script exit.
- **Status:** Spec verified against [FEAT-160]/[SPR-52.0] — Rank-16 LoRA, 4-bit load, `unsloth/Llama-3.2-3B-Instruct-bnb-4bit` default, `adamw_8bit`, `bf16=True`. Physical deployment + dry-run validation performed by Silicon post-dispatch.

- [x] **Task 52.2**: Integrate `rsync` adapter sync step into `nightly_forge.py`. *(spec authored — impl pending Silicon)*

### Task 52.2 — Rsync Adapter Sync & vLLM Hot-Reload (`nightly_forge.py`)

**Functional Requirement [SPR-52.0 / Story 3]:** rsync the ~20MB `cli_voice_v1` LoRA adapter from Node Kender (`~/kender_forge/adapters/cli_voice_v1/`) to `/speedy/models/adapters/` on z87-Linux, then trigger vLLM hot-reload via REST API (zero-downtime).

**Integration Spec** — ordered edit list for `HomeLabAI/src/infra/nightly_forge.py`. Legacy `run_unsloth_forge()` is retained as the `--local` fallback (repo legacy-preservation rule).

> **⚠️ Pre-existing landmine (Silicon must fix at impl time):** the legacy function is declared `def re-ignite_vllm():` at `nightly_forge.py:43` — a hyphenated identifier, **invalid Python syntax**, so the module does not currently parse. Rename it to `re_ignite_vllm()` (definition + all callers, incl. the `finally:` block in `main()`) as a minimal bugfix while integrating. All spec code below uses the corrected name.

**1. New module constants** (insert after `OUTPUT_LORA_DIR`, line 26; add `import shutil` to the import block):

```python
KENDER_SSH_TARGET = "jallred@192.168.1.26"  # explicit user@host; ~/.ssh alias may be added later
KENDER_TRAIN_SCRIPT = "~/kender_forge/train_jason_voice_lora.py"
KENDER_DATA_STAGE = "~/kender_forge/data/journal_ledger.jsonl"
KENDER_ADAPTER_STAGE = "~/kender_forge/adapters/cli_voice_v1/"
SYNC_STAGING_DIR = "/speedy/models/adapters/.sync-staging/cli_voice_v1/"
VLLM_URL = "http://localhost:8088"
```
**2. New function `run_kender_forge()`** (insert after `run_unsloth_forge()`):

```python
def run_kender_forge():
    """[SPR-52.0] Offload Unsloth pass to Kender (4090), rsync adapter back, hot-reload vLLM."""
    if not os.path.exists(DATASET_PATH):
        logger.warning(f"[SPR-52.0] Dataset {DATASET_PATH} not found. Skipping Kender training pass.")
        return

    # (a) Push dataset to Kender staging
    try:
        res = subprocess.run(["rsync", "-avz", "--timeout=60", DATASET_PATH,
                              f"{KENDER_SSH_TARGET}:{KENDER_DATA_STAGE}"],
                             capture_output=True, text=True)
        if res.returncode != 0:
            logger.warning(f"[SPR-52.0] Dataset rsync failed: {res.stderr[-300:]}")
            return
    except Exception as e:
        logger.warning(f"[SPR-52.0] Dataset rsync error: {e}")
        return

    # (b) Trigger remote training (60 steps)
    cmd = ["ssh", KENDER_SSH_TARGET,
           f"python3 {KENDER_TRAIN_SCRIPT} {KENDER_DATA_STAGE} {KENDER_ADAPTER_STAGE} 60"]
    logger.info(f"[SPR-52.0] Executing: {' '.join(cmd)}")
    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            logger.error(f"[SPR-52.0] Kender training failed (code {res.returncode}): {res.stderr[-300:]}")
            return
        logger.info(f"[SPR-52.0] Kender training OK. Tail: {res.stdout[-300:]}")
    except Exception as e:
        logger.error(f"[SPR-52.0] Error executing remote training: {e}")
        return

    # (c) Pull adapter back to staging dir
    try:
        os.makedirs(SYNC_STAGING_DIR, exist_ok=True)
        res = subprocess.run(["rsync", "-avz", "--partial",
                              f"{KENDER_SSH_TARGET}:{KENDER_ADAPTER_STAGE}", SYNC_STAGING_DIR],
                             capture_output=True, text=True)
        if res.returncode != 0:
            logger.warning(f"[SPR-52.0] Adapter rsync failed: {res.stderr[-300:]}")
            return
    except Exception as e:
        logger.warning(f"[SPR-52.0] Adapter rsync error: {e}")
        return

    # (d) Atomic swap: staging -> live (vLLM never reads a half-written safetensors)
    try:
        os.makedirs(os.path.dirname(OUTPUT_LORA_DIR), exist_ok=True)
        if os.path.exists(OUTPUT_LORA_DIR):
            os.rename(OUTPUT_LORA_DIR, OUTPUT_LORA_DIR + ".old")
        os.rename(SYNC_STAGING_DIR, OUTPUT_LORA_DIR)
        if os.path.exists(OUTPUT_LORA_DIR + ".old"):
            shutil.rmtree(OUTPUT_LORA_DIR + ".old")
        logger.info(f"[SPR-52.0] Adapter atomically swapped into {OUTPUT_LORA_DIR}")
    except Exception as e:
        logger.error(f"[SPR-52.0] Atomic swap failed: {e}")
        return

    # (e) vLLM hot-reload (zero-downtime); fall back to re_ignite_vllm() on failure
    try:
        resp = requests.post(f"{VLLM_URL}/v1/load_lora_adapter",
                             json={"lora_name": "cli_voice_v1", "lora_path": OUTPUT_LORA_DIR},
                             timeout=10)
        if resp.status_code == 200:
            logger.info("[SPR-52.0] vLLM hot-reloaded cli_voice_v1 (zero-downtime <10ms claim kept).")
        else:
            logger.warning(f"[SPR-52.0] load_lora_adapter returned HTTP {resp.status_code}; falling back to re_ignite_vllm()")
            re_ignite_vllm()
    except Exception as e:
        logger.warning(f"[SPR-52.0] vLLM hot-reload error: {e}; falling back to re_ignite_vllm()")
        re_ignite_vllm()
```
**3. `main()` wiring** — keep steps 1-2 and 4; replace step 3 with `run_kender_forge()` unless `--local`:

```python
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Nightly Forge orchestrator")
    parser.add_argument("--local", action="store_true",
                        help="Run legacy run_unsloth_forge() on z87 instead of Kender offload")
    args = parser.parse_args()

    logger.info("=== [FEAT-160/FEAT-213/SPR-52.0] NIGHTLY FORGE ORCHESTRATION INITIATED ===")

    # 1. Ingest Raw Notes
    run_mass_scan()

    # 2. Quiesce VRAM
    quiesced = quiesce_vllm()

    try:
        # 3. Train LoRA Adapter (Kender offload; --local keeps legacy z87 path)
        if args.local:
            run_unsloth_forge()
        else:
            run_kender_forge()
    finally:
        # 4. Re-ignite Foyer
        re_ignite_vllm()

    logger.info("=== NIGHTLY FORGE ORCHESTRATION COMPLETE ===")
```

**4. Verification (Silicon post-dispatch):**

- [ ] Kender dry-run: `python3 ~/kender_forge/train_jason_voice_lora.py <dataset> <out> 60` completes in `< 45s`.
- [ ] Adapter dir contains `adapter_model.safetensors` (~20MB) + `adapter_config.json`.
- [ ] rsync pull lands under `/speedy/models/adapters/cli_voice_v1`.
- [ ] Probe vLLM: `curl http://localhost:8088/v1/chat/completions` with `"model": "cli_voice_v1"` returns 200.
- [ ] `python3 -m pytest HomeLabAI/src/tests/test_vllm_adapter_swap.py` passes.
- [ ] `nightly_forge.py --local` still trains locally on z87.

### Task 52.2 — Implementation Disposition

- **Deployment Target:** `HomeLabAI/src/infra/nightly_forge.py` (module currently does NOT parse — `def re-ignite_vllm():` at line 43 is invalid Python; rename to `re_ignite_vllm()` as minimal bugfix while integrating).
- **Rsync Source:** `KENDER_ADAPTER_STAGE = ~/kender_forge/adapters/cli_voice_v1/` (Node Kender / WSL2, RTX 4090 — ~20MB `adapter_model.safetensors` + `adapter_config.json`).
- **Destination:** `OUTPUT_LORA_DIR = /speedy/models/adapters/cli_voice_v1` via atomic swap from `SYNC_STAGING_DIR = /speedy/models/adapters/.sync-staging/cli_voice_v1/`.
- **Hot-Reload:** `POST http://localhost:8088/v1/load_lora_adapter` `{"lora_name": "cli_voice_v1", "lora_path": OUTPUT_LORA_DIR}`; fallback `re_ignite_vllm()` on non-200/exception.
- **Status:** Spec authored — impl pending Silicon (validated post-dispatch). Anchors verified against source: `OUTPUT_LORA_DIR` @ `nightly_forge.py:26`; `def re-ignite_vllm():` @ `nightly_forge.py:43` (hyphenated identifier — module does not parse); `import shutil` absent from import block (`nightly_forge.py:13-18`); `re-ignite_vllm()` call site @ `nightly_forge.py:99` in `finally:` block of `main()`.

### Task 52.3 — 5-Stage Division of Labor Orchestration (`router.py`)

**Functional Requirement [SPR-52.0 / Story 5]:** Update `HomeLabAI/src/v5/foyer/router.py` to orchestrate the reshuffled 5-Stage Division of Labor pipeline: (1) Kender triage, (2) Pinky HyDE, (3) Brain ChromaDB query, (4) Deep Thought strategic synthesis, (5) Pinky sanity review & out-loud delivery. Add per-stage hooks and graceful, non-fatal error handling. The Cognitive Hub remains the reasoning engine (`cognitive.process_query`); the router adds the stage-hook observability + containment layer around it (legacy-preservation rule — no hub rewrite).

**Integration Spec** — ordered edit list for `HomeLabAI/src/v5/foyer/router.py`.

**1. New module constants** (insert after `JUDGE_BACKPRESSURE_PATH`, line 49):

```python
# [SPR-52.0 / Task 52.3] 5-Stage Division of Labor Orchestration
DIVISION_OF_LABOR_STAGES = (
    ("stage1_kender_triage",  "Deep Thought / Lab Node (Kender · t=0)", "Preamble & Triage"),
    ("stage2_pinky_hyde",     "Pinky (vLLM + LoRA)",                    "HyDE & Persona Alignment"),
    ("stage3_brain_query",    "Brain (Right Hemisphere)",               "Short Technical Answer / ChromaDB"),
    ("stage4_dt_synthesis",   "Deep Thought (Kender)",                  "Strategic Synthesis (importance >= 0.7)"),
    ("stage5_pinky_review",   "Pinky (Sanity / Vibe Check)",            "Out-Loud Delivery -> Waterfall Drainer"),
)
STAGE_SOURCE_MAP = {
    "Deep Thought": "stage1_kender_triage",
    "Lab (Triage)": "stage1_kender_triage",
    "Pinky":        "stage2_pinky_hyde",
    "Brain":        "stage3_brain_query",
}
STAGE_TIMEOUTS = {
    "stage1_kender_triage": 45,
    "stage2_pinky_hyde":    30,
    "stage3_brain_query":   30,
    "stage4_dt_synthesis":  60,
    "stage5_pinky_review":  20,
}
STAGE_LEDGER_PATH = os.path.join(DATA_DIR, "foyer_stage_ledger.jsonl")
```

**2. `__init__` additions** (insert after the `processed_ids` hygiene block, after line 99):

```python
        # [SPR-52.0 / Task 52.3] Stage-hook registry for the 5-Stage Division of Labor
        self.stage_hooks = {sid: [] for sid, _, _ in DIVISION_OF_LABOR_STAGES}
        self.stage_memory = {}  # request_id -> {stage_id: status}
```

**3. New methods** (insert after `record_pager()`, after line 202): `register_stage_hook()`, `_emit_stage_progress()`, `_stream_pinky_fallback()`, and the guarded orchestrator `run_division_of_labor()`:

```python
    def register_stage_hook(self, stage_id, hook):
        """[SPR-52.0 / Task 52.3] Register a callable fired on stage transitions."""
        if stage_id not in self.stage_hooks:
            raise KeyError(f"Unknown stage: {stage_id}")
        self.stage_hooks[stage_id].append(hook)

    async def _emit_stage_progress(self, stage_id, request_id, status, detail=""):
        """[SPR-52.0 / Task 52.3] Non-fatal stage transition: broadcast + ledger + hooks.

        NEVER raises into the caller. Stage hooks are observer callbacks
        (fire-and-forget); a bad hook only logs a warning.
        """
        try:
            stage_node, stage_purpose = next(
                ((s[1], s[2]) for s in DIVISION_OF_LABOR_STAGES if s[0] == stage_id),
                (stage_id, ""),
            )
            self.stage_memory.setdefault(request_id, {})[stage_id] = status
            try:
                os.makedirs(os.path.dirname(STAGE_LEDGER_PATH), exist_ok=True)
                with open(STAGE_LEDGER_PATH, "a") as f:
                    f.write(json.dumps({
                        "ts": time.time(),
                        "request_id": request_id,
                        "stage": stage_id,
                        "node": stage_node,
                        "purpose": stage_purpose,
                        "status": status,
                        "detail": detail,
                    }, default=str) + "\n")
            except Exception as e:
                logger.warning(f"[SPR-52.0] Stage ledger append failed: {e}")
            stage_index = next((i for i, s in enumerate(DIVISION_OF_LABOR_STAGES) if s[0] == stage_id), 0) + 1
            await self.broadcast({
                "type": "crosstalk",
                "channel": "stage",
                "stage": stage_id,
                "stage_index": stage_index,
                "stage_total": len(DIVISION_OF_LABOR_STAGES),
                "node": stage_node,
                "purpose": stage_purpose,
                "stage_status": status,
                "detail": detail,
                "brain": f"[STAGE {stage_index}/5] {stage_purpose} — {status}",
                "brain_source": "Foyer",
                "request_id": request_id,
                "version": LAB_VERSION,
            })
            for hook in self.stage_hooks.get(stage_id, []):
                try:
                    hook(request_id, status, detail)
                except Exception as e:
                    logger.warning(f"[SPR-52.0] Stage hook error ({stage_id}): {e}")
        except Exception as e:
            logger.warning(f"[SPR-52.0] Stage progress emission failed (non-fatal): {e}")

    async def _stream_pinky_fallback(self, request_id):
        """[SPR-52.0 / Task 52.3] Graceful degradation: guarantee UI delivery on failure."""
        try:
            await self.broadcast({
                "type": "chat",
                "brain": "The pipeline hit a snag mid-synthesis. Retrying via Pinky's direct line...",
                "brain_source": "Pinky",
                "final": True,
                "channel": "chat",
                "request_id": request_id,
            })
        except Exception as e:
            logger.warning(f"[SPR-52.0] Pinky fallback emit failed: {e}")

    async def run_division_of_labor(self, query, source="REST", request_id=None):
        """[SPR-52.0 / Task 52.3] 5-Stage Division of Labor orchestrator.

        Wraps the Cognitive Hub waterfall with per-stage hooks and graceful
        error containment. Stage 1 (Kender triage) is idempotent: the WS path
        emits STARTED at t=0 via _spawn_deep_thought_preamble; REST paths emit
        it here. Stages 2-4 progress is deduced from incoming node streams via
        STAGE_SOURCE_MAP in handle_stream_ingest. Stage 5 completes when the
        waterfall drainer flushes the final Pop for this request_id.
        """
        if request_id is None:
            import uuid
            request_id = uuid.uuid4().hex[:8]

        # Stage 1: Preamble & Triage (Kender · t=0, local fallback)
        if self.stage_memory.get(request_id, {}).get("stage1_kender_triage") is None:
            await self._emit_stage_progress("stage1_kender_triage", request_id, "STARTED")

        kender_online = False
        try:
            thought = self.residents.get_node("thought")
            if thought is not None:
                res = await asyncio.wait_for(thought.call_tool("ping_engine", {"force": False}), timeout=5.0)
                if getattr(res, "content", None):
                    kender_online = '"success": true' in res.content[0].text
        except Exception as e:
            logger.warning(f"[SPR-52.0][STAGE1] Kender ping failed — local fallback engaged: {e}")
        await self._emit_stage_progress(
            "stage1_kender_triage", request_id, "COMPLETED",
            detail="kender_online" if kender_online else "local_fallback",
        )

        # Stages 2-4 run inside the hub; guarded by a total-budget timeout.
        shutdown_ev = asyncio.Event()
        try:
            await asyncio.wait_for(
                self.cognitive.process_query(query, shutdown_event=shutdown_ev, request_id=request_id),
                timeout=STAGE_TIMEOUTS["stage4_dt_synthesis"] * 4,
            )
        except asyncio.TimeoutError:
            logger.error(f"[SPR-52.0] Division of Labor exceeded total budget for {request_id}")
            await self._emit_stage_progress("stage4_dt_synthesis", request_id, "FAILED", detail="total_timeout")
            await self._stream_pinky_fallback(request_id)
        except Exception as e:
            logger.error(f"[SPR-52.0] Division of Labor failed for {request_id}: {e}")
            await self._emit_stage_progress("stage5_pinky_review", request_id, "FAILED", detail=str(e)[:200])
            await self._stream_pinky_fallback(request_id)
```

**4. Wiring** — three call sites:

**(a)** `_spawn_deep_thought_preamble()` (line ~870): after the `is_domain_match` computation, add the Stage 1 entry hook before the existing broadcast:

```python
            # [SPR-52.0 / Task 52.3] Stage 1: t=0 triage entry hook (WS path)
            if not self.stage_memory.get(request_id, {}).get("stage1_kender_triage"):
                await self._emit_stage_progress(
                    "stage1_kender_triage", request_id, "STARTED",
                    detail="domain_match" if is_domain_match else "casual_bypass",
                )
```

**(b)** `handle_stream_ingest()` (line ~812): after the `cognitive.handle_stream_token` relay, deduce Stage 2-4 progress from the node stream source (final tokens only):

```python
            # [SPR-52.0 / Task 52.3] Stage 2-4 hooks: deduce progress from node streams
            stage_id = STAGE_SOURCE_MAP.get(data.get("source", ""))
            if stage_id and data.get("final"):
                await self._emit_stage_progress(stage_id, data.get("request_id", "default"), "COMPLETED")
```

**(c)** `waterfall_drainer()` (final flush block, ~line 946): after the final `await self.broadcast(...)` Pop for a request_id, mark Stage 5 complete (idempotent):

```python
                        # [SPR-52.0 / Task 52.3] Stage 5: contract completion (idempotent)
                        if self.stage_memory.get(request_id, {}).get("stage5_pinky_review") is None:
                            await self._emit_stage_progress("stage5_pinky_review", request_id, "COMPLETED")
```

**(d)** `queue_drainer()` dispatch (line 1142): route intents through the guarded orchestrator instead of calling `cognitive.process_query` directly:

```python
                                        # [SPR-52.0 / Task 52.3] Dispatch via 5-Stage orchestrator
                                        asyncio.create_task(self.run_division_of_labor(event.query, source=event.source, request_id=event.id))
```

**5. Verification (Silicon post-dispatch):**

- [ ] `python3 -m py_compile HomeLabAI/src/v5/foyer/router.py` passes (module parses).
- [ ] `python3 -m pytest HomeLabAI/src/tests/test_rude_gauntlet.py` passes.
- [ ] `python3 -m pytest HomeLabAI/src/tests/test_vllm_adapter_swap.py` passes (no regression on adapter swap).
- [ ] REST inject (`curl -X POST http://127.0.0.1:8765/inject -d '{"query":"RAPL PCIe error triage"}'`) produces 5 crosstalk `channel=stage` transitions (STARTED/COMPLETED) in UI.
- [ ] `field_notes/data/foyer_stage_ledger.jsonl` gains one row per stage transition with terminal status (COMPLETED/SKIPPED/FAILED) per request_id.
- [ ] Kender offline (thought node ping fails): Stage 1 reports `local_fallback` and the pipeline completes without raising; Pinky fallback fires only on real pipeline failure.
- [ ] Casual turn (`"hello"`): Stage 1 emits `casual_bypass` and Stages 2-5 still terminate (Pinky fast-path exit).

### Task 52.3 — Implementation Disposition

- **Deployment Target:** `HomeLabAI/src/v5/foyer/router.py` (router-level layer only; `cognitive_hub.py` engine untouched — legacy-preservation rule).
- **Stage Semantics:** Stage 1 = Kender Deep Thought / local `lab` triage (already embedded in `cognitive.process_query`, `cognitive_hub.py:770-798`; Kender ping via `thought` node `ping_engine` tool, `thought_node.py:76-79`). Stage 2 = Pinky HyDE from `hyde_vector_text` triage field. Stage 3 = Brain ChromaDB short answer. Stage 4 = Deep Thought strategic synthesis gated by `importance >= 0.7` (ledger contract; hub uses 0.5 grounding gate internally). Stage 5 = `waterfall_drainer` final Pop flush + Pinky out-loud.
- **Anchors Verified Against Source:** `JUDGE_BACKPRESSURE_PATH` @ `router.py:49`; `processed_ids` block @ `router.py:97-99`; `record_pager` @ `router.py:200-202`; `_spawn_deep_thought_preamble` @ `router.py:870-902`; `handle_stream_ingest` @ `router.py:812-826`; `waterfall_drainer` final flush @ `router.py:929-946`; single `cognitive.process_query` dispatch site @ `router.py:1142` (queue drainer); resident names `pinky/archive/thought/brain/lab` @ `residents.py:55-61`; `Thought` node exports `deep_think`/`ping_engine` @ `thought_node.py:22-79`.
- **Fallback Contract:** `STAGE_SOURCE_MAP` is best-effort observability — an unmapped/unknown stream source never raises; `_emit_stage_progress` is fully guarded and non-fatal. Stage 5 completion is authoritative via the drainer flush (the UI contract), with stage-failure containment guaranteeing a UI-deliverable Pinky fallback message.
- **Status:** Spec authored — impl pending Silicon (validated post-dispatch).

- [x] **Task 52.3**: Implement Stage 1 Kender Triage & Stage 2 Pinky HyDE in `router.py`. *(impl spec authored — impl pending Silicon, validated post-dispatch)*
- [x] **Task 52.4**: Perform Telemetry Context Suppression in `lab_node.py:L10` and `cognitive_hub.py`.
- [ ] **Task 52.5**: Execute full 5-stage gauntlet verification (`pytest HomeLabAI/src/tests/test_vllm_adapter_swap.py`).

---

## 📜 Task 52.5 — Verification & Adapter Swap Gauntlet

> **Status:** PENDING EXECUTION (Integration Gate)  
> **Command:** `pytest HomeLabAI/src/tests/test_vllm_adapter_swap.py`

### 1. Purpose & Target Contract
- Verifies the zero-downtime hot-reload contract for `cli_voice_v1` LoRA adapter on vLLM (`http://localhost:8088/v1/chat/completions`).
- Tests end-to-end adapter loading, swap verification, and API response validity post-training.

### 2. Key Transition Requirements & Prerequisites
1. **Local Nightly Forge Run (`--local`):** Executes `run_mass_scan()` -> `quiesce_vllm()` -> `run_unsloth_forge()` on z87.
2. **Adapter Staging:** LoRA weights saved to `/speedy/models/adapters/cli_voice_v1`.
3. **vLLM Hot-Reload / Re-ignition:** `POST /v1/load_lora_adapter` or `re_ignite_vllm()` restores Foyer state to `OPERATIONAL`.
4. **Execution Gate:** Run `pytest HomeLabAI/src/tests/test_vllm_adapter_swap.py` after the 02:00 AM nightly forge run or manual trigger.

