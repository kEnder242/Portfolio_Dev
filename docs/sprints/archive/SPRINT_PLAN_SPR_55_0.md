# 📜 SPRINT PLAN: Sprint 55.0 — FEAT Code Mapping

> **Status:** READY FOR EXECUTION / SPRINT 55
> **Focus:** Systematically find each and every FEAT/LAB feature in FeatureTracker and mark where it lives in code — simple, scoped, one feature at a time.

---

## 📖 **1. TL;DR (For Humans)**

**What you'll get:** Every feature (FEAT) and lab-infrastructure (LAB) item in the Feature Tracker gets an official "where in the code it lives" entry — with file paths, line numbers, and clickable GitHub links — so the feature page shows real code links instead of prose. Untagged code gets one-line feature-ID comments so AI coding agents stop accidentally deleting features during refactors. A verifier script makes the build fail if any code link goes stale. A document-first audit report lists anything lost, missing, duplicated, or inconsistent.

**How progress is tracked:** The work is split one feature at a time — every one of the ~282 items is reviewed individually (its code home confirmed, a code link added, a tag comment added if needed) and marked "reviewed" in a progress ledger. The running score is **X of 282 reviewed**, visible at a glance after every batch.

**Why this approach:** The Feature Tracker is the single source of truth and the page generator already renders any new field automatically — so adding a "Code" field per feature is the smallest, safest change. The research.html page already has working code-link machinery we copy. The audits follow the proven V5-regression methodology that caught three silently-deleted features. Per-feature review units keep each step small, independently verifiable, and continuously measurable.

**What it will NOT do:** It will not edit features.html by hand (a generator owns it). It will not touch public www_deploy. It will not delete or merge any feature entry without explicit sign-off. It will not push anything to remote git. It will not change any runtime logic — comments and docs only.

**Effort:** Large | **Risk:** Medium — 282 tracker entries to map; line links can go stale; audit may surface uncomfortable findings (by design)

---

### 🤖 TL;DR (Machine)

Large effort, medium risk. Research waves → per-feature review batches (282 = 270 FEAT + 12 LAB; 6 batches of 47; feature_progress.json reviewed/total metric) → generator git-link + LAB parsing upgrade → audit report → verify_feature_links.py hard gate → sprint registration.

---

## 🎯 **2. Scope**

### ✅ Must have
1. **`.omo/plans` → materialized sprint doc**: `Portfolio_Dev/SPRINT_PLAN_SPR_55_0.md` (THIS document — repo convention; Prometheus restriction keeps drafting in `.omo/`, execution materializes it).
2. **Inventory**: machine-readable FEAT/LAB inventory (282 headers = 270 FEAT + 12 LAB) with status + existing mechanism/verification refs (`.omo/evidence/inventory.json`).
3. **Tag scan**: tagged-features manifest of every `[FEAT-*]`/`[LAB-*]` comment/log tag in HomeLabAI/src, Portfolio_Dev/field_notes, repo-root scripts (`.omo/evidence/tagged.json`).
4. **Cross-reference + progress ledger**: per-feature verdict MAPPED / TAGGED-ONLY / DOC-ONLY / DRIFT / ECHO / INFRA (`.omo/evidence/crossref.json`) AND `.omo/evidence/feature_progress.json` — one entry per feature, `status: unreviewed|reviewed`, `pre_tagged: bool`, verdict, evidence path. Ledger drives the top-level **reviewed/total** metric.
5. **Audit report**: document-first re-verification of FEAT_AUDIT_V5 claims (FEAT-337/342/339/118) + FeatureTrackerAudit items (FEAT-322/323/318.7/320/321/030/080/302/186) + new outliers; written to `Portfolio_Dev/field_notes/features_review.md` (or FEATURE_CODE_MAP.md) with file:line evidence and recommendations.
6. **Per-feature review units**: for EVERY FEAT/LAB entry (6 sequential batches of 47, tracker order) — confirm/adjust code location from crossref evidence → add `**Code:** [<file>](<github blob link>#L<start>-L<end>) — <one-line desc>.` (or explicit `*none found (documented only)*` for DOC-ONLY Phantoms) → add one-line `# [FEAT-XXX] <desc>` tag comment at primary location if untagged ACTIVE/DESIGN (DEFEATURED not re-tagged) → mark `reviewed` in feature_progress.json. Uncharted (TAGGED-ONLY) features get NEW tracker entries per audit. Commit per batch.
7. **Generator upgrade** (`Portfolio_Dev/field_notes/features_build.py`): `format_code_link()` (mirrors research_build.py:16-23), header regex extended to `(FEAT|LAB)-\d{3}` so LAB renders, SOURCE_OF_TRUTH banner preserved.
8. **Line-drift automation**: `Portfolio_Dev/field_notes/verify_feature_links.py` parsing `**Code:**` fields, resolving path + `#Lstart-Lend`, emitting drift report, exit non-zero on drift; wired into `build_site.py` after features_build (hard gate).
9. **Sprint registration + progress closeout**: conductor/tracks.md SPR-55 row, 00_FEDERATED_STATUS.md initiative + milestone + **reviewed/total = 282/282 readout**, new tracker entry (next free FEAT ID, e.g. FEAT-463), full build + feature_dna sync check.

### 🚫 Must NOT have (guardrails, anti-slop, scope boundaries)
- **Do NOT edit `features.html` directly** — generator owns it (SOURCE_OF_TRUTH banner).
- **Do NOT use the AGY delegation tool** — OpenAgent `task()` delegation only (user directive; this environment is OpenCode/OpenAgent).
- **Do NOT delete/merge DEFEATURED or ECHO entries** without explicit human buy-in (FeatureTrackerDesign.md guardrails).
- **Do NOT push to remotes** — stage + commit only; user handles push (HomeLabAI AGENTS.md git protocol).
- **Do NOT touch public www_deploy** — features.html stays private (user-confirmed).
- **Do NOT change runtime logic** in tagging story — comment lines only, verified by diff.
- **Do NOT rewrite research.html / RESEARCH_SYNTHESIS.md**.
- **Do NOT touch unrelated dirty-worktree files** (out of scope).
- **Do NOT run review batches in parallel** — all batches write `FeatureTracker.md`; batches are strictly sequential, generator work may parallelize.

---

## 🗺️ **3. Execution Strategy**

### Parallel execution waves
- **Wave 0 (Research, fully parallel):** T1 inventory extraction ∥ T2 code-side tag scan ∥ T3 audit-claim verification. T3 independent of T1/T2.
- **Wave 1 (Synthesis + ledger scaffold):** T4 cross-reference + outlier classification + feature_progress.json scaffold (depends T1+T2). T5 audit report writing (depends T4 + T3). T6 materialize sprint doc (depends approval).
- **Wave 2 (Per-feature review — STRICTLY SEQUENTIAL batches):** T7–T12 six batches of 47 features each, tracker order. Each batch: confirm location → `**Code:**` field → tag comment → mark reviewed → run batch link check → commit. Batch N+1 starts only after batch N committed and its reviewed/total verified. Generator upgrade (T13) may start after T7 completes (Code fields exist).
- **Wave 3 (Generator + automation):** T13 features_build.py upgrade (after T7); T14 verify_feature_links.py + build_site.py hard gate (after T12 — all Code fields exist).
- **Wave 4 (Registration + closeout):** T15 sprint registration + final build + 282/282 progress readout (depends T14 passing).
- **Final wave:** F1 plan compliance, F2 code quality, F3 real QA (regenerate + inspect features.html), F4 scope fidelity — parallel after T15.

### Dependency matrix
| Todo | Depends on | Blocks | Can parallelize with |
| --- | --- | --- | --- |
| T1 inventory | — | T4 | T2, T3 |
| T2 tag scan | — | T4 | T1, T3 |
| T3 audit verify | — | T5 | T1, T2 |
| T4 crossref + progress scaffold | T1, T2 | T5, T7–T12 | — |
| T5 audit report | T3, T4 | — | T6 |
| T6 materialize sprint doc | approval | — | T5 |
| T7 review batch A (FEAT 1–47) | T4 | T8, T13 | — |
| T8 review batch B (48–94) | T7 | T9 | — |
| T9 review batch C (95–141) | T8 | T10 | — |
| T10 review batch D (142–188) | T9 | T11 | — |
| T11 review batch E (189–235) | T10 | T12 | — |
| T12 review batch F (236–282, incl. LAB) | T11 | T14 | — |
| T13 generator upgrade | T7 | T14, T15 | — |
| T14 verifier hard gate | T12, T13 | T15 | — |
| T15 registration + final build | T14 | final wave | — |

---

## 🎴 **4. Sprint 55 Stories & Delegation Specifications**

> Stories designed for OpenAgent `task()` delegation (this environment is OpenCode/OpenAgent — NOT the AGY delegation tool per user directive). Implementation + Test = ONE story. Never separate.

---

### 🎴 **STORY 55.1 — FEAT/LAB Inventory Extraction**
* **Goal**: Spawn explore agent to parse `Portfolio_Dev/FeatureTracker.md` (1-1722) into `.omo/evidence/inventory.json`: `{id, title, status, mechanism_refs, verification_refs, line_start}` for every `## [FEAT-*]` and `## [LAB-*]` header, INCLUDING DEFEATURED entries, ordered by tracker line.
* **Target Files**: `Portfolio_Dev/FeatureTracker.md` (read-only) → `.omo/evidence/inventory.json` (create)
* **Delegation Spec**: OpenAgent `task(subagent_type="explore", ...)` — parse-only; must NOT edit FeatureTracker.md.
* **Verification Gate**: `python3 -c "import json;d=json.load(open('.omo/evidence/inventory.json'));assert len(d)==282"` (270 FEAT + 12 LAB) AND every id matches `^(FEAT|LAB)-\d{3}` AND ids unique AND count of `**Status:**` fields == 274.
* **Commit**: `chore(sprint55): FEAT/LAB inventory extraction evidence`

---

### 🎴 **STORY 55.2 — Code-Side FEAT/LAB Tag Scan (THE Pre-Existing-Tag Search)**
* **Goal**: Spawn explore agent to grep all `[FEAT-\d+...]` / `[LAB-\d+]` tags in HomeLabAI/src (incl v5/, infra/, nodes/, tests/), Portfolio_Dev/field_notes (py+sh), repo-root .py/.sh → `.omo/evidence/tagged.json` `{feat_id: [{file, line, snippet<=120}]}`. Capture BOTH comment tags and log/print string tags.
* **Target Files**: HomeLabAI/src/** (dream_node.py, atomic_io.py, cognitive_audit.py, router.py, etc.), Portfolio_Dev/field_notes (build_site.py, scan_librarian.py, nibble_v2.py, generate_judge_ledger.py, jellyfin_autotune.py), apply_fixes.py, src/tests/*.py
* **Delegation Spec**: OpenAgent `task(subagent_type="explore", ...)` — ONE comprehensive scan; every review batch (T7-T12) consumes this as ground truth so reviewers never re-grep.
* **Verification Gate**: tagged.json parses; every tagged file listed in prior grep scan (22 files) present; per-file tag counts match `grep -c` on each source file; tagged.json records whether each hit is a comment or log/print string.
* **Commit**: `chore(sprint55): code-side FEAT/LAB tag manifest evidence`

---

### 🎴 **STORY 55.3 — Audit-Claim Verification (Oracle)**
* **Goal**: Spawn oracle agent to verify every claim in `HomeLabAI/docs/plans/FEAT_AUDIT_V5_REGRESSION_REPORT.md` against live code: FEAT-337 `_check_resident_health`, FEAT-342 `_synchronize_and_probe`, FEAT-339 `_run_deep_smoke`, FEAT-118 `get_oracle_signal` → verdict RESTORED / STILL-LOST / N/A with current file:line.
* **Target Files**: `HomeLabAI/src/acme_lab.py`, `HomeLabAI/src/v5/foyer/router.py`, `HomeLabAI/src/v5/ignition/manager.py:185-215`, `HomeLabAI/src/logic/cognitive_hub.py:628` (read-only)
* **Delegation Spec**: OpenAgent `task(subagent_type="oracle", ...)` — must NOT modify code; must cite live grep/read evidence.
* **Verification Gate**: verdicts file exists with one line per claim `{feat_id, verdict, evidence_file:line}`; every verdict cites a real file:line or explicit absence.
* **Commit**: `docs(sprint55): V5 audit claim re-verification`

---

### 🎴 **STORY 55.4 — Cross-Reference & Outlier Classification + Progress Ledger Scaffold**
* **Goal**: Spawn metis agent to merge inventory.json + tagged.json → crossref.json: every FEAT/LAB gets exactly one verdict MAPPED/TAGGED-ONLY/DOC-ONLY/DRIFT/ECHO/INFRA with file:line evidence. THEN scaffold `.omo/evidence/feature_progress.json`: one entry per inventory id, `{status: "unreviewed", pre_tagged: <bool from tagged.json>, verdict, evidence: null}` — the reviewed/total tracking ledger.
* **Target Files**: `.omo/evidence/crossref.json`, `.omo/evidence/feature_progress.json` (create)
* **Delegation Spec**: OpenAgent `task(subagent_type="metis", ...)` — must NOT classify without evidence; must NOT propose deletions.
* **Verification Gate**: crossref.json has exactly 282 verdicts, one per inventory id; verdict enum subset of {MAPPED,TAGGED-ONLY,DOC-ONLY,DRIFT,ECHO,INFRA}; feature_progress.json has 282 entries all `unreviewed`; outliers list non-empty.
* **Commit**: `chore(sprint55): FEAT/LAB cross-reference classification + progress ledger`

---

### 🎴 **STORY 55.5 — Cohesive Audit Report (Document-First, incl. Missed Outliers)**
* **Goal**: Write `Portfolio_Dev/field_notes/features_review.md` (or FEATURE_CODE_MAP.md companion): sections Lost / Missing / Deprecated / Inconsistent, each item with file:line evidence + recommended action; incorporate T3 verdicts + T4 outliers.
* **Target Files**: `Portfolio_Dev/field_notes/features_review.md` (create)
* **Delegation Spec**: OpenAgent `task(subagent_type="metis" OR category="writing", ...)` — recommendations only; must NOT delete or modify any FEAT entry.
* **Verification Gate**: report exists; every prior-audit item (FEAT-322/323/318.7/320/321/030/080/302/186/337/342/339/118) has a dated verdict; every new outlier from crossref.json appears.
* **Commit**: `docs(sprint55): cohesive FEAT audit report`

---

### 🎴 **STORY 55.6 — Review Batches A–F: Per-Feature Code-Location Marking (THE CORE WORK)**
* **Goal**: For each feature in tracker order, in **6 strictly-sequential batches of 47** (FEAT 1–47, 48–94, 95–141, 142–188, 189–235, 236–282 incl. LAB-090..107):
  1. **SEED from tagged.json** — `pre_tagged=true` features use their tagged.json file:line as the primary location (no fresh grep); only `pre_tagged=false` features get a fresh location search.
  2. **Confirm/adjust** primary code location from crossref.json evidence.
  3. **Add** `**Code:** [<file>](https://github.com/kEnder242/<repo>/blob/main/<path>#L<start>-L<end>) — <one-line desc>.` (or `**Code:** *none found (documented only)*` for DOC-ONLY).
  4. **Tag** — if untagged ACTIVE/DESIGN add one-line `# [FEAT-XXX] <desc>` comment at primary location (DEFEATURED never re-tagged; pre-tagged features left as-is).
  5. **Mark** `{status: "reviewed", pre_tagged, evidence}` in feature_progress.json. Uncharted features get NEW tracker entries per audit.
  6. **Batch link check** (paths exist + #L ranges valid) → **commit** per batch.
* **Target Files**: `Portfolio_Dev/FeatureTracker.md` (add `**Code:**` fields), HomeLabAI/src + field_notes (tag comments), `.omo/evidence/feature_progress.json` (mark reviewed)
* **Delegation Spec**: OpenAgent `task(category="unspecified-high", ...)` per batch — STRICTLY SEQUENTIAL; batch N+1 only after N committed + reviewed/total verified. LAB features map to /etc/systemd + sysctl artifacts as "infra config" code locations where no src exists.
* **Verification Gate** (cumulative after each batch):
  ```bash
  python3 -c "import json;d=json.load(open('.omo/evidence/feature_progress.json'));print(sum(1 for f in d.values() if f['status']=='reviewed'), '/', len(d))"
  # MUST equal 47/282 → 94/282 → 141/282 → 188/282 → 235/282 → 282/282
  ```
  Plus batch link check green per batch.
* **Commits**: `docs(sprint55): review batch A **Code:** fields + tags (47/282 reviewed)` ... `docs(sprint55): review batch F **Code:** fields + tags incl. LAB (282/282 reviewed)`

---

### 🎴 **STORY 55.7 — features_build.py Upgrade: Git Links + LAB Parsing**
* **Goal**: Add `format_code_link()` (mirror research_build.py:16-23) applied in field-render loop (features_build.py:152-166); extend header regex (features_build.py:69) to `^## \[(FEAT|LAB)-\d{3}(?:\.\d+)?\]`; keep SOURCE_OF_TRUTH banner (features_build.py:203).
* **Target Files**: `Portfolio_Dev/field_notes/features_build.py`; reference `research_build.py:16-23`, `build_site.py:116-119`
* **Delegation Spec**: OpenAgent `task(category="unspecified-high", ...)` — must NOT change output for non-Code fields; must NOT edit features.html by hand.
* **Verification Gate**: `python3 Portfolio_Dev/field_notes/features_build.py` exits 0; regenerated features.html contains `id="LAB-090"` and `https://github.com/kEnder242/` anchors; `grep -c 'SOURCE_OF_TRUTH'` == 1.
* **Commit**: `feat(sprint55): features_build.py renders Code fields + LAB headers`

---

### 🎴 **STORY 55.8 — verify_feature_links.py + build_site.py Hard Gate**
* **Goal**: Create `Portfolio_Dev/field_notes/verify_feature_links.py`: parse every `**Code:**` field in FeatureTracker.md; resolve path relative to repo root; validate file exists; validate `#Lstart-Lend` within file line count; emit drift report (`.omo/evidence/drift_report.txt`); exit non-zero on any drift. Wire into `build_site.py` after features_build.py invocation (build_site.py:116-119) as hard gate (skippable only via explicit `--no-verify` flag).
* **Target Files**: `Portfolio_Dev/field_notes/verify_feature_links.py` (create), `Portfolio_Dev/field_notes/build_site.py:106-119` (edit)
* **Delegation Spec**: OpenAgent `task(category="unspecified-high", ...)` — must NOT auto-rewrite links (report only).
* **Verification Gate**: deliberately break one link → script exits non-zero + drift_report.txt lists it; restore link → exits 0; `python3 Portfolio_Dev/field_notes/build_site.py --no-deploy` runs verifier and passes.
* **Commit**: `feat(sprint55): line-drift verification hard gate`

---

### 🎴 **STORY 55.9 — Sprint Registration & Final Build + Progress Closeout**
* **Goal**: Add SPR-55 row to conductor/tracks.md; add Active Initiative + milestone + **reviewed/total readout (282/282)** to `Portfolio_Dev/00_FEDERATED_STATUS.md`; add new tracker entry (next free FEAT ID, likely FEAT-463) documenting this sprint; run `python3 Portfolio_Dev/field_notes/build_site.py` full; check feature_dna sync hook presence (00_FEDERATED_STATUS.md:68) and run if present.
* **Target Files**: `conductor/tracks.md:3-7`, `Portfolio_Dev/00_FEDERATED_STATUS.md:15-22,64-68`, `Portfolio_Dev/FeatureTracker.md:1669-1673` (FEAT-457 submodule sync precedent), `build_site.py:95-159`
* **Delegation Spec**: OpenAgent `task(category="unspecified-high", ...)` — must NOT push; must NOT touch www_deploy.
* **Verification Gate**: `grep -c 'spr-55' conductor/tracks.md` == 1; `grep -c 'SPR-55\|Sprint 55' Portfolio_Dev/00_FEDERATED_STATUS.md` >= 1; 282/282 reviewed readout present in 00_FEDERATED_STATUS.md; build_site.py exits 0; `git status` shows only intended files.
* **Commit**: `docs(sprint55): register SPR-55 + final site build + 282/282 closeout`

---

## 📊 **5. Reviewed/Total Progress Ledger**

> Driven by `.omo/evidence/feature_progress.json` — one entry per FEAT/LAB id, `status: unreviewed|reviewed`.

| Batch | Feature Range | Reviewed/Total (cumulative) | Ledger Assert |
| :--- | :--- | :--- | :--- |
| **A** | FEAT 1–47 | **47 / 282** | `assert sum(status=='reviewed')==47` |
| **B** | FEAT 48–94 | **94 / 282** | `assert sum(status=='reviewed')==94` |
| **C** | FEAT 95–141 | **141 / 282** | `assert sum(status=='reviewed')==141` |
| **D** | FEAT 142–188 | **188 / 282** | `assert sum(status=='reviewed')==188` |
| **E** | FEAT 189–235 | **235 / 282** | `assert sum(status=='reviewed')==235` |
| **F** | FEAT 236–282 (incl. LAB-090..107) | **282 / 282** ✅ | `assert sum(status=='reviewed')==282` |

**Total = 282 items** = 270 FEAT + 12 LAB headers (exact count confirmed at inventory execution). Every batch commits with its reviewed/total milestone in the message so git history itself shows progress.

---

## ✅ **6. Verification Strategy**
> Zero human intervention — all verification is agent-executed.
- **Test decision**: tests-after (verifier script + build regression + diff hygiene) — no new runtime logic to TDD, but every generator change is verified by regenerating features.html and diffing.
- **Progress metric**: after every review batch, the ledger assert above MUST equal the expected cumulative reviewed/total.
- **Evidence**: `.omo/evidence/task-<N>-sprint-55-feat-code-mapping.<ext>` (inventory.json, tagged.json, crossref.json, feature_progress.json, drift_report.txt, regenerated features.html diff, git diff --stat).

---

## 🔒 **7. Commit Strategy**
- One atomic commit per todo (or per review batch T7-T12), conventional-commit style as listed per story.
- Evidence artifacts (`.omo/evidence/*`) committed with their producing todo.
- Never push; user handles remote push (HomeLabAI AGENTS.md git protocol).
- Sprint doc materialization (T6/STORY 55 doc) commits BEFORE source-material edits (T7) so the paper trail leads.
- Each review batch commits with its reviewed/total milestone in the message (e.g. "(47/282 reviewed)").

---

## 🏁 **8. Success Criteria**
1. `Portfolio_Dev/SPRINT_PLAN_SPR_55_0.md` exists and matches this plan (materialized paper trail). ✅ (this document)
2. **feature_progress.json reads 282/282 reviewed** — every FEAT/LAB entry carries `**Code:**` fields or explicit "none found" markers; git links resolve (verifier green).
3. features.html renders LAB rows + clickable code links; stays private.
4. Untagged ACTIVE/DESIGN features tagged at primary locations; zero logic diffs.
5. verify_feature_links.py is a hard build gate; drift report artifacts exist.
6. Audit report re-verifies all 14 prior-audit items + lists new outliers with file:line evidence.
7. Sprint 55 registered in conductor/tracks.md + 00_FEDERATED_STATUS.md with 282/282 reviewed readout; full build green; no pushes, no public changes.

---

## 📜 **9. Execution Ledger**

| Story | Title | Executor | Status | Tries / Retries | Intent Alignment |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **55.1** | FEAT/LAB Inventory Extraction | — | ⏳ PENDING | — | — |
| **55.2** | Code-Side FEAT/LAB Tag Scan | — | ⏳ PENDING | — | — |
| **55.3** | Audit-Claim Verification | — | ⏳ PENDING | — | — |
| **55.4** | Cross-Reference + Progress Ledger | — | ⏳ PENDING | — | — |
| **55.5** | Cohesive Audit Report | — | ⏳ PENDING | — | — |
| **55.6** | Review Batches A–F (282/282) | — | ⏳ PENDING | — | — |
| **55.7** | features_build.py Upgrade | — | ⏳ PENDING | — | — |
| **55.8** | verify_feature_links.py Hard Gate | — | ⏳ PENDING | — | — |
| **55.9** | Sprint Registration + Closeout | — | ⏳ PENDING | — | — |
