# Field Notes Architecture & Security

## 🚀 Overview
The "Field Notes" project is a professional technical dashboard designed to showcase engineering "War Stories," validation philosophy, and system architecture. It is built as a **"Class 1"** application: a robust, framework-less static site served via native Linux services.

## 🏗️ Technical Stack
- **Source:** Pure HTML5 / CSS3 (Dark Mode Engineering Aesthetic).
- **Service:** Systemd unit `field-notes.service` running `python3 -m http.server`.
- **Network:** Cloudflare Tunnel (`acme-lab`) mapping port `9001` to `notes.jason-lab.dev`.
- **Security:** Cloudflare Zero Trust (Access) with a "Split-Policy" model.

## 🛡️ Security Model (Split-Policy)
We maintain a strict boundary between public-facing "Lobby" content and internal "Vault" tools.

### 1. The Lobby (`notes.jason-lab.dev`)
- **Purpose:** Interviewer/Recruiter access.
- **Policy:** **Lobby Access**
  - **Administrator:** Full access (OTP).
  - **NVIDIA Guests:** Allow all users with `@nvidia.com` domains (OTP).
  - **Method:** One-Time PIN via email.

### 2. The Vault (`code.jason-lab.dev`, `pager.jason-lab.dev`)
- **Purpose:** Development and Observability.
- **Policy:** **Admin Only**
  - **Administrator:** `kender242@gmail.com` ONLY.
  - **Auth:** Dual-layer (Cloudflare OTP + App-level Password).

## 📂 Project Structure
- `index.html`: Semantic content for all war stories.
- `style.css`: Custom "Class 1" dark theme.
- `Travel_Guide_2026.md`: **(LOCAL ONLY)** Historical context, Pinky logic, and credentials. (Git-ignored).
- `FIELD_NOTES_PLAN.md`: Roadmap and Phase status.

## 🔗 External Documentation
Detailed setup instructions, API token permissions, and deployment commands are maintained in the secure Google Workspace:
- [Cloudflare Zero Trust Setup Guide](https://docs.google.com/document/d/1ffro9ZtR4VO_9dqoUR46-QlQnxBZ97RhcrhEZloCKk8)

---
*Note: This file is a high-level grounding document. For sensitive IDs or CLI management, refer to the private Google Doc or the `.secrets/` directory on the host.*
