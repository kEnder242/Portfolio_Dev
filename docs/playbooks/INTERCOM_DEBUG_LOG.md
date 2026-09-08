# Intercom Debug Log
**Date:** Feb 8, 2026
**Status:** Active Debugging

## 1. The Echo Bug
**Symptom:** Text input is displayed twice in the Web Intercom (once as "[YOU]" locally, once as "[YOU]" from server).
**Cause:**
- `intercom_v2.js` optimistically appends the user's message to the chat window immediately upon sending.
- `acme_lab.py` receives `text_input` and explicitly echoes it back with `type: "final"`.
- `intercom_v2.js` receives `type: "final"` and appends it again.
**Fix:** Remove the server-side echo in `acme_lab.py` for `text_input` events. Voice input (STT) still needs the `final` event as there is no local text prediction.

## 2. RAG Plumbing & Brain Alignment
**Goal:** Ensure the Brain prioritizes retrieved context (Keep notes, logs) over creative storytelling.
**Analysis:**
- `acme_lab.py`: Correctly fetches `memory` from `archive_node` and injects it into `augmented_context`.
- `brain_node.py`: Receives `context` but the System Prompt lacks a strong directive to *adhere* to it.
**Fix:** Update `brain_node.py` System Prompt to include a strict "GROUNDING" rule.

## 3. API Stability (Agent)
**Note:** User reports "Cannot read properties of undefined (reading 'candidates')" from the Gemini CLI.
**Strategy:** frequent saves, concise tool calls.