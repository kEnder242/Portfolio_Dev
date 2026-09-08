# Sprint 37 Session Log

> This log records the chronological narrative of decisions, discoveries, and changes made during Sprint 37 sessions.
> It is intended for future context injection, retrospective review, and agent cold-start orientation.

---

## Session: 2026-07-04 to 2026-07-08

### Context & Starting State

Sprint 37 began with objectives of benchmarking the heterogeneous model stack, hardening the RAG pipeline (decoupled diagnostics, Gems-to-Notes ground truth), and polishing the resident AI personas. It ran across multiple AGY sessions due to token exhaustion and interruptions.

---

## Stories 1-5: Completed Prior Sessions

These were completed and committed before the July 8 session. See SPRINT_PLAN_SPR_37_0.md for full task ledgers.

- **Story 1** (443f426): Multi-model benchmarking script bench_models.py, NVML VRAM capture, benchmarks.html console-dense dashboard.
- **Story 2** (9ccc155): Strict year filtering in archive_node.py to prevent temporal drift in RAG recall.
- **Story 3** (9ccc155): Pinky Coherence Critic -- evaluator JSON (score, reasoning, slop_found, retort), round_table_evals.json ledger.
- **Story 4** (8a82eb8): Interleaved RAG evaluation rows in status.html timeline with [+]/[-] expand indicators.
- **Story 5**: Decoupled RAG diagnostic logging (data/rag_runs/), lazy-load expandable UI panel, Gems-to-Notes context bridge in archive_node.py.

---

## Story 6: Resident Persona Polish & Triage Fidelity

**Problem:** Resident models (Pinky, Brain) were over-narrating the lab's own architecture in responses. Triage was hallucinating project codes (BANANA-5095). JSON blobs were rendering raw in the chat UI.

**Decisions:**
- IDENTITY_BEDROCK in loader.py refactored to lead with user's silicon telemetry domain, demoting lab topology to a footnote. Positive domain anchor crowds out meta-narration without a prohibitive instruction.
- Triage situation field in lab_node.py (LAB_SYSTEM_PROMPT Rule 6) constrained to paraphrase-only. BANANA-5095 and similar hallucinations were caused by the model pattern-matching on retrieval artifacts and generating plausible-sounding codes.
- Frontend (intercom_v2.js): JS guards added to parse and pretty-print triage and critic JSON on the WebSocket handler. Raw blobs hidden from the console.
- @media print CSS added to style.css to suppress sidebar, menu-toggle, vitals bar, and sys-console from print output of protocols.html.

---

## Session: 2026-07-08 (This Session)

### OpenAgent Delegation Improvements

**Root Cause of model failures (from log analysis):**
1. ses_0c61ebab0ffeRC23pP7kxbiQjU ran for ~7 hours across multiple days. Context accumulation in a single long-running session degrades small model KV cache. Models appeared to "loop" or "not follow" because accumulated history was overwhelming their effective budget.
2. google/gemini-2.5-flash (free tier) was hitting RESOURCE_EXHAUSTED (HTTP 429) -- 20 req/day limit -- mid-task. Models with google as primary silently failed when quota was hit.
3. URL encoding bug in Sisyphus web UI: %7Bid%7D (literal {id}) passed as a session ID -- cosmetic frontend bug, not a model failure.

**Decisions:**
- BKM-034 updated with Step 6: Session Lifecycle Management. Key rule: one session per Story, not per sprint. Fork with --fork before risky operations. Name sessions via their first message.
- AGY_TO_OPENAGENT_PLAYBOOK.md Section 7 added: full decision matrix (run vs --session vs -c vs --fork), context window health warnings, remediation guidance.
- oh-my-openagent.json: All google/* models removed from primary positions. Demoted to fallback-only. Free-tier google is a liability as a primary. momus, metis, multimodal-looker -> Groq primary; visual-engineering -> DeepSeek primary.

### Sisyphus Model Upgrade (devstral:24b)

**Research:**

| Model           | Active Params | VRAM Q4 | SWE-bench | Architecture | Decision |
|:----------------|:--------------|:--------|:----------|:-------------|:---------|
| omnicoder-9b    | 9B            | ~6 GB   | N/A       | Dense        | Too weak for agentic chains |
| qwen3.5:27b     | 27B           | ~16 GB  | ~48%      | Dense        | Capable, already installed |
| gemma4:26b      | 26B           | ~17 GB  | Unknown   | Dense        | Confirmed poor tool-following |
| qwen3-coder:30b-a3b | 3.3B     | ~10 GB  | ~48%      | MoE          | Fast, more headroom |
| devstral:24b    | 24B           | ~19 GB  | ~68%      | Dense        | SELECTED -- best agentic SWE score |

**Decision:** devstral:24b selected as primary for sisyphus and atlas. Highest SWE-bench Verified score (~68%) among consumer-GPU-fitting models. Purpose-built for agentic multi-file workflows (OpenHands/Aider pedigree). Fits 4090 with ~5GB VRAM headroom. omnicoder-9b demoted to fallback.

Pull triggered to Windows 4090 at 192.168.1.26:11434 (background, ~18.9GB). opencode-core.service restarted to pick up new config.

### Story 7: ChromaDB DNA Integration

**Problem:** BKM-034 handover prompts injected full FeatureTracker.md and Protocols.md as raw file content. For small local models this consumed a significant fraction of KV cache before the first task token was generated.

**Discovery:** sync_chroma_dna.py and the pre-commit hook were already implemented from a prior sprint. The hook fires automatically on every git commit touching either source file. Verified: fired 4 times during this session, syncing 214 FEAT entries and 29 BKM entries each time.

**ChromaDB Architecture:**
- Script: Portfolio_Dev/sync_chroma_dna.py
- Store: ~/AcmeLab/chroma_db (ChromaDB PersistentClient)
- Embeddings: sentence-transformers/all-MiniLM-L6-v2 (CPU-only on z87-Linux, ~7-9s per sync)
- No GPU usage, no Google API calls -- fully local CPU inference.
- Collections: behavioral_dna (Protocols/BKMs), feature_dna (FeatureTracker/FEATs/VIBEs)
- Trigger: git pre-commit hook (not a background daemon)

**Task 7.3** (324bfac): BKM-034 Step 5 handover template updated. Raw file:///...FeatureTracker.md and file:///...Protocols.md links replaced with ChromaDB semantic query examples. Sprint plan pointer retained as direct link -- it is ephemeral state, not DNA-managed.

**Story 7 complete** on commit 29d59f4.

---

### Cloudflare Investigation & Resolution

**Problem:** list_cf_apps.py returning 401 Authentication error despite a valid token.

**Investigation timeline:**
1. Token verify endpoint (/user/tokens/verify) -> active. Token exists and is valid.
2. DNS zones endpoint (/zones) -> 9109: Cannot use the access token from location: 50.39.128.157 -- IP restriction on token.
3. After user removed IP restriction in dashboard: DNS zones OK, but access/apps still 401.
4. Root cause: access/apps was being called at the account level (/accounts/{id}/access/apps). The token has Access: Apps and Policies scoped to the zone level only.
5. Zone-level endpoint (/zones/{zone_id}/access/apps) -> returned both apps successfully.

**Fixes applied:**
- App renamed: Jason Lab - Sovereign -> Jason Lab - Strategic via PUT /zones/.../access/apps/{id}.
- panasonic.aero whitelisted: Added email_domain panasonic.aero to the Lobby Access policy.

**Critical finding for future sessions:**
The correct Cloudflare API path for this token is ZONE-level:
  /zones/c560564464f6202dde62e8e67649f79c/access/apps
NOT account-level:
  /accounts/c58aa4585f3e0c942a07a4e06ef3b5dc/access/apps
Update list_cf_apps.py and add_domain_cf.py scratch scripts accordingly.

**Lobby Access policy final state:**
- kender242@gmail.com
- nvidia.com
- intel.com
- jabil.com
- amd.com
- panasonic.aero (added this session)

---

## Commits This Session

| Hash    | Repo         | Description |
|:--------|:-------------|:------------|
| 86d83aa | Portfolio_Dev | BKM-034.6 session lifecycle docs, Story 7 ChromaDB DNA added |
| 1979abf | HomeLabAI    | BKM-034 step 6 -- session lifecycle management |
| 787e4ab | Portfolio_Dev | Story 7 tasks 7.1/7.2 marked complete |
| 324bfac | HomeLabAI    | Task 7.3 -- BKM-034 handover template updated to ChromaDB queries |
| 29d59f4 | Portfolio_Dev | Story 7 complete -- ChromaDB DNA fully operational |

---

## Open Items Carrying Into Sprint 38

- devstral:24b pull in progress on 4090. Check: curl -s http://192.168.1.26:11434/api/tags
- Update list_cf_apps.py and add_domain_cf.py scratch scripts to use zone-level API path.
- Sprint 38 planning not yet started.
