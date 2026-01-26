# Field Notes Dashboard - Implementation Plan

**Project:** Field Notes (Technical Interview Dashboard)
**Goal:** Create a static, secure, and professional landing page to showcase "War Stories," technical philosophy, and link to HomeLabAI tools.

## 1. Core Philosophy
- **"Class 1" Design:** Robust, self-contained, no complex frameworks or build steps. Pure HTML/CSS.
- **Tone:** Professional, direct, validation-oriented. No emojis or conversational filler.
- **Security:** Relies on Cloudflare Access (Zero Trust) for authentication, keeping the server implementation simple and stateless.

## 2. Architecture
- **Type:** Static Site (Single Page Application feel via anchor links).
- **Directory:** `~/Portfolio_Dev/field_notes/`
- **File Structure:**
    - `index.html`: Contains all content and navigation.
    - `main.css`: Clean, high-contrast stylesheet.
    - `assets/`: Directory for any necessary images or icons.

## 3. Design & Content
- **Theme:** Dark mode (slate/charcoal background, light text) for an engineering aesthetic.
- **Navigation Sidebar (Fixed Left):**
    1.  **Mission Control** (Links to HomeLabAI: VS Code, Pager, etc.)
    2.  **Systems Architecture** (e.g., VISA Tool, Metadata-Driven Design)
    3.  **Validation Methodology** (e.g., Reading Like a Robot, Negative Testing)
    4.  **Security & Yield** (e.g., RAKP Security Catch, The Texas Power-On)
    5.  **Engineering Leadership** (e.g., Count the Ok's, Content is King)
- **Main Content Area (Right):**
    - Full text of "War Stories" transcribed from source documents.
    - TBD/Future items listed as bullet points at the end of sections, styled distinctly (e.g., greyed out/italics).

## 4. Security Strategy (Cloudflare Access)
- **Mechanism:** Cloudflare Zero Trust sits in front of the application.
- **Granularity:**
    - **Field Notes Policy:** Flexible (e.g., Allow `jason@email.com` + Guest OTPs).
    - **Infrastructure Policy (Prometheus/Grafana):** Strict (e.g., Allow *only* `jason@email.com`).
- **Server-Side:** The static site requires no internal auth logic.

## 5. Deployment & Testing
- **Local Development:** Preview using Python's built-in HTTP server (`python3 -m http.server 8080`).
- **Production:** Served via Nginx/Apache or directly via Cloudflare Tunnel.

## 6. Version Control Strategy
- **Repository:** `~/Portfolio_Dev`
- **Workflow:**
    1.  Scaffold/Edit files.
    2.  `git add <files>`
    3.  `git commit -m "<message>"`
    4.  **STOP.**
- **Strict Rule:** The CLI will **NEVER** execute `git push`. Pushing to remote is reserved for the user after final review.
- **Ignored:** `.DS_Store`, `__pycache__`, OS metadata, local temp files.

## 7. Next Steps (Execution)
1.  Scaffold directory structure.
2.  Transcribe "War Stories" into semantic HTML in `index.html`.
3.  Apply CSS styling in `main.css`.
4.  Launch local preview for user verification.

## Phase 4: AI Integration & Privacy (The "Class 2" Evolution)
**Goal:** Transform the static site into a "Living Archive" managed by Pinky (Local AI).

### 4.1 Privacy & Governance ("The Censor Node")
- [ ] **Privacy Filter:** Update `scan_pinky.py` to classify extracted events as `Public`, `Private`, or `Sensitive`.
- [ ] **Audit Log:** Maintain `privacy_audit.json` to review Pinky's filtering decisions.
- [ ] **Heuristics:** Train Pinky to recognize PII (names, internal codenames) and scrub them.

### 4.2 The "Slow Burn" (Continuous Refinement)
- [ ] **Automation:** Systemd timer to run `scan_pinky.py` nightly (3 AM).
- [ ] **Iterative Indexing:** Pinky re-scans notes to find connections missed in previous passes.
- [ ] **ChromaDB Sync:** Push `pinky_index_full.json` to HomeLabAI's vector store for voice-query access ("Pinky, when did I work on Simics?").

### 4.3 Interactive Discovery ("Deep Dive")
- [ ] **Concept:** "Silent Prefetching" on the Timeline.
- [ ] **Mechanism:** As user scrolls to "2016", browser requests a "Deep Dive" summary from Pinky.
- [ ] **UX:** Subtle expansion of cards with more context, powered by real-time RAG (requires lightweight backend).

## Phase 5: The "Smoke & Mirrors" Architecture (Refined V3)
**Goal:** Create a timeline that *feels* alive and reactive without relying on a live AI backend (Class 1 Philosophy).

### 5.1 The "Date-Aware" Scanner (Data Prep)
- [x] **Logic Upgrade:** `scan_pinky.py` split into `scan_queue.py` (Manager) and `nibble.py` (Worker).
- [x] **Granularity:** Move from "Yearly Buckets" to "Dated Events" (Monthly JSONs).
- [x] **Cross-Year Handling:** Regex chunking handles internal dates properly.

### 5.2 Layered Data Structure
- [x] **Schema Change:** Granular `YYYY_MM.json` files + `YYYY.json` aggregates.
    - **Layer 1 (Surface):** `themes.json` (Skeleton).
    - **Layer 2 (Pop-in):** Monthly groupings in Timeline.

### 5.3 The Frontend Trick (Smoke & Mirrors)
- [x] **Interaction:** `IntersectionObserver` triggers data fetch on scroll.
- [x] **Implementation:** Lazy-loaded JSON with 5s simulated "Thinking" delay.

### 5.4 HomeLabAI Bridge (The Contract)
- [x] **Protocol:** Defined `FIELD_NOTES_INTEGRATION.md`.
- [x] **Direction:** Implemented `ai_engine.py` abstraction layer.
- [x] **Safety:** `nibble.py` checks Prometheus load before running.
