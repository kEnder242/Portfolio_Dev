# Daily BKM: Feb 5, 2026 - The Agentic Collaboration Refactor
**Status:** DRAFT (Awaiting Execution)
**Context:** Shifting from "Manual Tool Use" to "Conductor-Led Tracks" while utilizing local LLMs for context compression.

## 1. PREPARATION: The Collaborative Foundation
*   **Gemini Conductor:** `gemini extensions install https://github.com/gemini-cli-extensions/conductor --consent --auto-update`
*   **Local LLM Proxy:** Verify `ollama` is listening at `localhost:11434`. Configure LiteLLM (if needed) to allow the Gemini CLI to offload "Big Text" (logs/notes) processing to local Llama3.2/Llama3 models to save token costs.
*   **Feedback Loop:** All major tracks must start with `gemini conductor track start [track_name]`.

## 2. THE CORE LOGIC: HomeLabAI Diagnostics (The Brain)
*   **Track: intercom-audio-fix**
    *   **The Bug:** `intercom.py` fails to capture audio on first launch or drops the first character of text input.
    *   **Logic:** Audit the `PyAudio` initialization sequence and the `stdin` buffer clearing logic. 
    *   **Goal:** Zero-latency audio handshake and robust character capture.
*   **Track: rag-hallucination-audit**
    *   **The Problem:** Brain ignored RAG context in recent logs.
    *   **Logic:** Extract recent log chunks. Use local LLM to perform "Attention Analysis" (Why did the prompt fail to anchor on the RAG data?). Check `all-MiniLM-L6-v2` embedding distances for the missed queries.
*   **Track: keep-integration**
    *   **Action:** Pull Google Keep notes tagged with "AI". 
    *   **Logic:** Synthesize these notes into `HomeLabAI/docs/plans/AI_MASTER_PLAN.md`. Archive notes in Keep only *after* they are successfully committed to Git.

## 3. TRIGGER POINTS: Dev_Lab Evolution (The Face)
*   **Track: web-intercom-text**
    *   **Target:** `acme.jason-lab.dev`
    *   **Logic:** Create `intercom.html` in `Portfolio_Dev`. Implement a "Class 1" (Vanilla JS) WebSocket client connecting to `acme.jason-lab.dev`.
*   **Track: web-intercom-voice**
    *   **Target:** `acme.jason-lab.dev` (Phase 2)
    *   **Logic:** Implement `MediaStream` API in the browser to stream PCM audio to the backend. (Tabled if latency is too high).

## 4. RETROSPECTIVE: Scars & Verification
*   **Verification:** Run `gemini conductor status` after each track.
*   **BKM Summary:** Each fix must result in a new entry in `HomeLabAI/docs/Protocols.md` under Section 8.
