# WWW & Hybrid Cloud Strategy
**Goal:** Create a public-facing entry point (`www`) while securing the internal lab (`acme`).

## 1. The Topology
We are adopting a **Hybrid Cloud** model to separate "Public Identity" from "Private Infrastructure."

| Domain | Hosted By | Access | Role |
| :--- | :--- | :--- | :--- |
| **www.jason-lab.dev** | **GitHub Pages** | 🌍 Public | The "Airlock." Static welcome page. 100% Uptime. |
| **notes.jason-lab.dev** | **Home Lab** (z87) | 🔐 Auth (Knock) | The Portfolio. Deep technical logs. |
| **acme.jason-lab.dev** | **Home Lab** (z87) | 🔐 Auth (Vault) | The API. WebSocket Intercom for the Brain. |
| **kEnder242.github.io** | **GitHub** | n/a | The raw host for `www`. |

## 2. Infrastructure Plan

### A. The Public Face (www)
*   **Tech:** Single HTML file. "Class 1" Design.
*   **Deployment:** Git push to `kEnder242/kEnder242.github.io`.
*   **DNS:** Cloudflare CNAME `www` -> `kender242.github.io`.

### B. The Intercom (acme)
*   **Client:** `intercom.html` hosted on the *existing* Notes server (`notes.jason-lab.dev/intercom`).
*   **Server:** Existing `acme_lab.py` (Port 8765).
*   **Tunnel:** `cloudflared` maps `acme.jason-lab.dev` -> `localhost:8765`.
*   **Protocol:** `wss://` (Secure WebSocket).

## 3. GitHub Pages Setup Guide
1.  **Create Repo:** Name it exactly `kEnder242.github.io`.
2.  **Add File:** Push an `index.html` (The chosen design).
3.  **Cloudflare:**
    *   Add CNAME record: `www` points to `kEnder242.github.io`.
    *   Ensure "Proxy Status" is **Proxied (Orange Cloud)**.
4.  **GitHub Settings:**
    *   Settings > Pages > Custom Domain > `www.jason-lab.dev`.
    *   GitHub will create a `CNAME` file in your repo.

## 4. Voice/Audio Strategy
*   **Phase 1:** Text Only. (Typing "Narf!" works).
*   **Phase 2:** Voice tabled until WebRTC/PCM streaming is designed.
