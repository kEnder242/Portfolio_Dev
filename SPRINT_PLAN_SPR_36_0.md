# Sprint 36 – ROLE TOKEN Story

## Overview
This sprint captures the design discussion around the **waterfall template**, **KV‑cache strategy**, and the introduction of a **ROLE TOKEN** to enable seamless Multi‑LoRA personality switching without incurring cache invalidation penalties.

## Background
- The waterfall model prefixes a static prompt segment (e.g., *Mission Control*) before each user turn. This gives a reliable KV‑cache but forces a cache‑miss when the personality prefix changes.
- Introducing a single **ROLE TOKEN** (e.g., `<|PINKY|>`) inserted **after** the `PREVIOUS STAGE OUTPUT` and **before** the `USER PROMPT` allows the hub to switch LoRA adapters on‑the‑fly while preserving the cached static prefix.
- The token is mapped to a LoRA adapter in `loader.py`; during request processing the hub loads the corresponding adapter prior to generation.

## Design Highlights
1. **Cache‑Friendly Persona Swaps** – Only the token incurs a minimal cache miss; the heavy static prefix remains cached across turns.
2. **Chat‑Room Feel** – By injecting ROLE TOKENs for different agents, multiple personalities can “overhear” without resetting the shared context.
3. **Implementation Steps**
   - Extend the tokenizer vocabulary with the new token.
   - Add a mapping table (`role_token_map`) linking tokens to LoRA adapters.
   - Update `loader.py` and `acme_lab.py` to detect the token and perform adapter switching.
   - Add unit tests ensuring KV‑cache integrity after token‑driven swaps.

## Acceptance Criteria (Planning Phase)
- [ ] Document the token‑to‑adapter mapping in `role_tokens.yaml`.
- [ ] Prototype the token injection in the request pipeline.
- [ ] Verify that KV‑cache hit rate stays > 95% when switching personalities.
- [ ] Update sprint notes with any open questions for the next design review.

## OpenAgent Hybrid Execution (Verification Gate)
- [ ] Delegate the tokenizer extension and prototype unit tests to OpenAgent:
  * Execution: Run `opencode play feature/role-token-prototype` using the DeepSeek/Ollama parallel mapping.
  * Verification: Verify OpenAgent successfully implements and verifies the test suite without using Google Gemini tokens.

*No tasks are created yet; this file serves as the sprint narrative and reference for upcoming work.*
