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