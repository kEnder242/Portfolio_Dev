# FEAT Code Review — SPR-55 Audit Report

**Date:** 2026-08-20
**Sprint:** 55 (FEAT Code Mapping)
**Method:** Document-first re-verification per FEAT_AUDIT_V5 methodology. Every verdict cites live file:line evidence (`.omo/evidence/crossref.json`, 271 entries).

---

## 🟥 LOST (in tracker, no live code)

| FEAT | Tracker | Verdict | Evidence / Recommendation |
| --- | --- | --- | --- |
| FEAT-337 | absent | **STILL-LOST** | `_check_resident_health` absent from src. Only tag: `src/debug/test_warm_wake.py:9,77`. **Rec**: re-record in tracker + restore resident liveness loop (30-60s `list_tools`). |
| FEAT-342 | absent | **STILL-LOST** | `_synchronize_and_probe` absent. Tag recycled onto `src/tests/test_rude_gauntlet.py:7,13`. **Rec**: restore wake-reprobe + BKM-009 scythe in ignition. |
| FEAT-339 | absent | **STILL-LOST** | `_run_deep_smoke` absent. Tag recycled onto task-cleanup `router.py:392,838`; also `loader.py:179,224,375` (unrelated LoRA/tier logic). **Rec**: re-record; optional deep-smoke diagnostic tool. |
| FEAT-118 | DESIGN L444 | **STILL-LOST** | `get_oracle_signal` only in backups `cognitive_hub.py.graft:19`, `.nuclear:21,28` + test strings. Never shipped (V4). **Rec**: mark ARCHIVED or implement weighted preamble picker. |

## 🟠 MISSING FROM TRACKER (code tags exist — Uncharted)

**71 tag outliers** exist in code with NO FeatureTracker entry (`.omo/evidence/outliers.json`). 65 in HomeLabAI/src, 4 in field_notes, 2 in root scripts; 24 are sub-version ids (FEAT-XXX.Y).

Representative (all 71 listed in outliers.json):
- FEAT-017 → `start_lab.sh:3`
- FEAT-074 → `nodes/archive_node.py:417,423`
- FEAT-175 → `field_notes/scan_librarian.py:160,187,204`
- FEAT-192 → `nodes/archive_node.py:1328`, `nodes/brain_node.py:64`
- FEAT-227 → `logic/cognitive_hub.py:1157`
- FEAT-251.4 → `debug/test_brain_smoke.py:12`
- FEAT-217 → `v5/foyer/router.py:764`, `debug/lifecycle_gauntlet.py:6`

**Rec**: add new tracker entries per audit (next free FEAT ids), documenting these as ACTIVE features with code homes. This is the exact gap HISTORICAL_VERIFICATION remediation #4 flagged (FEAT-451-455, LAB-094-099 never backfilled).

## 🟨 DUPLICATED / ECHO (same id, distinct content — 12 groups, 26 entries)

| Group | Entry A | Entry B |
| --- | --- | --- |
| FEAT-088 | L291 Semantic Career Recall | L725 Nightly Recruiter (Target Acquisition) |
| FEAT-095 | L347 Search Indexing Pipeline (v2.1) | L730 Public Research Ledger (Static Airlock) |
| FEAT-172 | L613 [CONSOLIDATED] Hemispheric Interjection | L752 Hemispheric Interjection |
| FEAT-186 | L617 [CONSOLIDATED] Pre-warm Lobby | L827 Pre-warm Lobby |
| FEAT-240 | L945 Native MCP Relay | L1069 Native MCP Sampling Bridge |
| FEAT-220 | L988 Diplomatic Immunity Protocol | L1274 (220.1) Physical Scavenging |
| FEAT-249 | L1100 VRAM Hibernation Matrix | L1105-1115 (249.3/249.4/249.5) |
| FEAT-428 | L1420 Exponential Backoff State Engine | L1587 PCM Audio Memory Benchmark |
| FEAT-429 | L1426 Poison Chunk Quarantine | L1603 Disconnect Memory Reclaim |
| FEAT-430 | L1432 C-Arena Heap Trimming Sentinel | L1611 Delegation Retrospective |
| FEAT-431 | L1438 GigaToken Remote Synthesis Gate | L1619 EarlyOOM Telemetry |
| FEAT-437 | L1468 3-Tier HyDE Failover Cascade | L1659 Pinky LoRA HyDE Inversion |

**Rec**: ECHO entries are distinct features sharing ids — must NOT be merged without user sign-off (FeatureTrackerDesign.md). Recommend renumbering the newer entries (e.g. FEAT-437 → FEAT-467) in a dedicated cleanup sprint.

## 🟦 INFRA (LAB — 12 entries, code = systemd/sysctl artifacts)

LAB-090/091/092/093/100/101/102/103/104/105/106/107 (L1539-1719) map to `/etc/systemd/system/` + `/etc/sysctl.d/` artifacts as "infra config" locations — no src exists. **Rec**: `**Code:**` fields point to artifact paths; verify at review batch F.

## 🟩 INCONSISTENT / DRIFT (status vs code)

| FEAT | Issue |
| --- | --- |
| FEAT-030 | ACTIVE but no code tag found anywhere (DOC-ONLY). Unity Pattern lives where? |
| FEAT-186 | DESIGN but tagged `[CONSOLIDATED]` in tracker + ECHO dup. |
| FEAT-249.x | Sub-versions 249.3/249.4/249.5 exist in tracker but base 249.3 tagged in code (loader.py). |

## ✅ PRIOR-AUDIT CLOSE-OUT (dated verdicts)

| Item | Verdict 2026-08-20 |
| --- | --- |
| FEAT-322 (Uncharted, FeatureTrackerAudit) | DEFEATURED (Sprint 31) — MAPPED (tagged) |
| FEAT-323 (Uncharted) | ACTIVE — MAPPED (tagged) |
| FEAT-318.7 / 320 / 321 (Phantoms) | **NOT IN TRACKER** — confirmed gone |
| FEAT-030 (Echo) | ACTIVE — DOC-ONLY (no tag found) |
| FEAT-080 (Echo) | ACTIVE — MAPPED |
| FEAT-302 (Drift) | ACTIVE — MAPPED |
| FEAT-186 (Drift) | DESIGN — ECHO (dup) |
| FEAT-337/342/339/118 (V5 audit) | **STILL-LOST** (T3 re-verified, all 4) |
| FEAT-028 (V5 survivor) | ACTIVE — MAPPED (restored 549aecd) |

## Recommendations (priority order)
1. Renumber ECHO duplicate groups (12 groups) — needs user sign-off.
2. Backfill 71 Uncharted outliers as new tracker entries (remediation #4 completion).
3. Restore FEAT-342 → FEAT-337 → FEAT-339 (V5 restoration order, unchanged).
4. Tag FEAT-030 at its real code home during batch A.
5. Mark FEAT-118 ARCHIVED (never shipped, backups only).
