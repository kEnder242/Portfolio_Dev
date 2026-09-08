# Sprint Plan: [SPR-11-08] Target Acquisition & Recruitment Uplink
**Status:** DESIGN | **Goal:** Transition from stubbed job searching to high-fidelity team profiling and active email delivery.

## 🎯 THE MISSION
To transform the "Nightly Recruiter" from a static reporter into a proactive acquisition engine. This sprint focuses on distilling 18 years of technical history into "Team Profiles," refining search parameters for modern platforms (Hiring.Cafe), and establishing a direct communication link to the Lead Engineer via Gmail.

---

## 🏗️ STRATEGIC ANCHORS

### 1. Team-Based Profiling [FEAT-168]
*   **Logic:** Move beyond generic role titles (e.g., "Engineer"). Distill historical success into specific team archetypes:
    *   **The Telemetry Squad:** Focus on RAPL, DCGM, and MSR-level data paths (NVIDIA, Intel).
    *   **The Validation Core:** Post-silicon logic, PCIe regressions, and stress automation.
    *   **The AI Infra Team:** GPU orchestration, vLLM/Ollama scaling, and agentic workflows.
*   **Mechanism:** Architect node analyzes historical `job_brief_*.md` files to identify recurring success patterns.

### 2. Modern Search Integration (Hiring.Cafe)
*   **Target:** [Hiring.Cafe](https://hiring.cafe/)
*   **Implementation:** 
    *   Identify high-fidelity search query strings using the **Monolingual Squeeze** keywords.
    *   Explore automation: If a direct API is unavailable, generate **"Deep Link manifests"**—a set of curated, pre-filtered search URLs for daily manual review.

### 3. Notification Uplink [FEAT-167]
*   **Logic:** Bridge the "Visibility Gap." Move the Nightly Brief from a hidden JSON file to a high-priority email.
*   **Target Address:** `kender242@gmail.com` (Verified via Gmail API).
*   **Mechanism:** Implement a `GmailDispatcher` class in `recruiter.py` utilizing the `gmail.send` toolset.

---

## 🛠️ TASKS

### PHASE 1: Forensic Profile Distillation
- [ ] **Archive Analysis:** Run the Brain against `Portfolio_Dev/field_notes/data/recruiter_briefs/*.md` to extract common "Team" themes.
- [ ] **Profile Mapping:** Update `recruiter_config.json` to include a `team_profiles` array with specific keyword weights per archetype.

### PHASE 2: Search Parameter Refinement
- [ ] **Hiring.Cafe Deep Links:** Construct complex query strings for Hiring.Cafe (e.g., `role:"Telemetry" + hardware + python`).
- [ ] **LinkedIn Boolean Update:** Refine the `keywords` array in `recruiter_config.json` to use high-fidelity Boolean strings.

### PHASE 3: Gmail Dispatcher Implementation [FEAT-167]
- [ ] **Core Logic:** Add `send_email_brief()` to `HomeLabAI/src/recruiter.py`.
- [ ] **VIBE Alignment:** Ensure the email subject uses the **[BKM Protocol]** style (e.g., `[RECRUITER] Nightly Acquisition Brief - YYYY-MM-DD`).
- [ ] **Validation:** Trigger a test email to `kender242@gmail.com` using the `lab_start` tool logic.

### PHASE 4: Dashboard Integration
- [ ] **Status Mapping:** Update the **Portfolio Dashboard** to show "Last Acquisition Uplink" status.
- [ ] **Pager Alert:** Ensure CRITICAL matches trigger a Pager alert with a direct Gmail link.

---

## 🧪 VERIFICATION & BKMS

### 1. The [BKM-023] Scalpel Pass
*   **Mandate:** Every update to `recruiter.py` must use granular `replace` blocks to preserve the existing CVT and CVT-Builder logic.

### 2. Verification Gauntlet
*   **Profile Check:** Verify that the "Telemetry" profile correctly prioritizes RAPL/MSR keywords over generic "Python."
*   **Uplink Check:** Confirm receipt of 1x high-fidelity brief in the `kender242@gmail.com` inbox.

---
*Reference: [FEAT-038] Nightly Recruiter | [VIBE-011] Resident Peer Presence*
