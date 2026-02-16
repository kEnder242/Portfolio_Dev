# 🏺 BKM-014: Forensic Silicon Reconstruction (Feb 15)
**Goal:** Step-by-step restoration of the Gemma 2 2B Stable Baseline.

## BKM-014.1: The Identity Shift (Gemma Baseline)
**Trigger**: VRAM exhaustion on 11GB RTX 2080 Ti with larger models (e.g., Mistral).
**One-Liner**: `ollama pull gemma2:2b`
**Core Logic**: 
- Shift identity to Gemma 2 2B for superior JSON tool-calling at 1/4 the VRAM cost.
- Standardize all 2080 Ti residents (Pinky, Brain, Archive, Architect) on this base.

## BKM-014.2: The GGUF Harvest (vLLM Attempt)
**Trigger**: Attempting high-throughput serving in Phase 3.
**One-Liner**: 
`ollama show gemma2:2b --modelfile` (to find blob path)
`python3 -m vllm.entrypoints.openai.api_server --model /usr/share/ollama/... --load-format gguf`
**Scars**: 
- vLLM 0.15.1 fails to map `lm_head.weight` from this GGUF blob.
- **Hardware Conflict**: Gemma 2 requires `bfloat16` for numerical stability, but RTX 2080 Ti (Compute 7.5) does not support `bfloat16`. 
- **The Double Bind**: vLLM refuses to boot `float16` for Gemma 2, and the 2080 Ti refuses to boot `bfloat16`.
- **Mitigation**: Fallback to OLLAMA for the stable release. Ollama's Q4_K_M quantization path bypasses this hardware requirement.

## BKM-014.3: The Substrate Drift (Audit)
**Trigger**: Checkout of old branches into a new environment.
**Status**: 
- `vllm` 0.15.1 (Current) vs 0.6.1 (Log)
- `torch` 2.9.1 (Current) vs 2.4.0 (Log)
**Scars**:
- New vLLM builds have stricter GGUF mapping requirements than previous versions.
- Older code expecting `transformers` backend may clash with vLLM's internal optimized model classes.
