# Bicameral Dispatch: System Design & Persona Architecture (v3.5)

## Overview
Transitioning from **Linear Triage** to **Asynchronous Dispatch**. The system moves from a "Request/Response" model to a "Multi-Stream Interjective" model.

## 1. The Communication Hub (`acme_lab.py`)

### A. Reflex Loop & Contextual Handover
- **Pinky's Reflexes:** Non-blocking task for character tics and environment alerts.
- **Handover Logic:** When dispatching to the Brain, the Hub prepends Pinky's last 3 interactions. 
- **Banter TTL:** To prevent infinite loops, interjections are limited to a "Banter TTL" of 2 turns before mandatory user yield.

### B. Sentinel Mode & Sentinel Insights
- **Proactive Interjection:** Brain monitors audio/logs. If confidence > 0.85, it interjects to the **Insight Panel (Pink)**.
- **Muted Console:** Brain remains silent in the main **Pinky Console (Blue)** unless explicitly asked.

### C. Brain State Management (Offline Robustness)
- **States:** `UNREACHABLE`, `PENDING_WAKE (WOL)`, `PRIMING`, `READY`.
- **Bicameral Fallback:** If Brain is `UNREACHABLE`, Hub uses a "Stub" response (characterful "Brain is Napping"). Single-weight model swapping is backlogged for vLLM stabilization.
- **Remote Model Pull:** Hub can trigger model downloads on the Windows host and report progress to the Insight panel.

## 2. Collaborative Workspace (The "Mice" Toolset)

### A. The Patch Tool (Unified Diff)
- **Goal:** Move away from "Chopstick Coding" (brittle string replacement).
- **Logic:** Both Pinky and Brain can generate and apply Unified Diffs to files in the `AcmeLab/workspace`.
- **UI Interaction:** A "Save" event in the UI broadcasts to both nodes. Agents "notice" the save and can interject with a vibe check or validation.

### B. Workspace Collision Handling
- **Auto-Save:** User edits are auto-saved locally before an agent-initiated file switch occurs.
- **Dirty State:** If the user is typing, agents are "polite" and append suggestions to the **Whiteboard** instead of clobbering the active file.

## 3. Observational Memory (Continuous Burn v2.0)
- **From RAG to State:** Transition from simple chunk retrieval to an "Observational World Model."
- **The Librarian's Duty:** The background burn now builds a "Compressed History" JSON that serves as the Lab's short-term "Working Memory."
- **Research Anchor:** [Observational Memory cuts AI agent costs 10x](https://venturebeat.com/data/observational-memory-cuts-ai-agent-costs-10x-and-outscores-rag-on-long)

## 4. UI/UX Mapping
- **Pinky (Right side, Blue):** Main chat console. Gateway/Reflexes.
- **Brain (Left side, Pink):** Insight panel. Logic/Sentinel/Deep Thinking.
