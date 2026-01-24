# GEMINI.md: Project Manifesto & State Machine
**Host:** Z87-Linux (Native) | **User:** Jason Allred | **Tier:** Lead Engineer Portfolio

## ✅ PHASE 0: ACCOMPLISHED (Gemini.google.com & Manual)
- [x] **Infrastructure Migration:** HomeLabAI_Dev moved from WSL -> Native Linux SSH (Success).
- [x] **Connectivity:** Tailscale MagicDNS active (z87-linux); passwordless SSH verified.
- [x] **Environment:** VS Code Desktop (Remote-SSH) + Zellij + Native Terminal active.
- [x] **Access Layer:** Verified Cloudflare Tunnel hostnames (`code.jason-lab.dev`, `pager.jason-lab.dev`).
- [x] **Strategy:** Initial brainstorming on "War Story" logic and technical dashboard intent.

## 🛠️ PHASE 1: CLI ENVIRONMENT & ACCESS VERIFICATION
*Before implementation, the CLI must confirm:*
1. **Directory Integrity:** Presence of `~/Portfolio_Dev` and its subdirectories.
2. **Binary Access:** Access to `python3`, `git`
3. **Environment Isolation:** Confirm it is operating in `Portfolio_Dev` and not modifying `HomeLabAI_Dev` infrastructure unless requested.

## 🎯 THE MISSION
To integrate the collection of technical notes and stories into a cohesive "Technical Dashboard." This is a full-spectrum integration—not a "best of" list. It must reflect the rigor of a Validation Engineer.

## ⚖️ OPERATIONAL PROTOCOL (The "Cautious Design" Rule)
1. **Fact-Finding First:** The CLI must perform "discovery" on raw notes before suggesting a structure.
2. **Design Feedback Loop:** Reserve "heads-down" development for moments when specifically called out. Work with the user to gather requirments and build a detailed vision before moving forward.  Some fact finding is allowed.  Only dive into development once approved.
3. **Verification over Velocity:** Prioritize "Why" (the validation logic) over "What" (the finished text).

## Personal notes from Jaosn:

1. **War Story notes** Here is a link to my document dealing wiht my work history.  I want to fill a dashboard with all the content in this doucment - I'd like to brainstorm ways to index and display this content as an interview dashboard

Link: https://docs.google.com/document/d/12Hu34Vv9y4e5mSfj98glCJ-1CJUVOYxKtWkxWMKyYk8/edit?usp=drive_link

2. **Travel Guide notes** - This is context for the environment we are working on, some of the info is old but it details the transition from HomeLabAI development in WSL to a Remote-to-Linux dev environment (here).  I'd like to leverage the website setup described here and implemented on this host.  A landing page pointing to home lab pages might be nice.  I'd like to brainstorm security options, maybe a guest login, and preserve existing work as well as possible./

Link: https://drive.google.com/file/d/1E7RYWn-WIkMkV6UmWML8_ZLzQRmuzlJY/view?usp=drive_link

3. **Strech goals** I want to learn promethius, graphana, and influxdb.  Please leave some room for these on a landing page and in our plans.  Integration to HomeLabAI_Dev might be useful - let's brainstorm as well.

## 🤖 CLI INITIALIZATION COMMAND
> "I am acting as a Lead Engineer's thought partner. My first task is to index all existing raw notes in  and propose a dashboard layout that highlights validation logic across the entire set."