#!/usr/bin/env python3
# Copyright 2025-2026 Jason Allred
# SPDX-License-Identifier: Apache-2.0
"""[LOOP-006 / BKM-015 / INS-052] Nibbler Escape & Backup Tripwire Test.

Demonstrates and verifies the end-to-end backup tripwire:
  1. Synthetic LLM output escapes (CLI option secrets, curl -u, URL auth, API keys)
     are caught by `sanitize_with_tripwire()`, logged to an isolated temp ledger,
     and flagged by `check_sanitization_escape_tripwire()`.
  2. Idempotency: re-running on redacted output produces escaped=False.
  3. Optional `--live`: sends a CLI-password canary through the local LLM using
     Nibbler's prompt to observe whether the LLM strips it or escapes to backup.
"""

import argparse
import datetime
import json
import os
import sys
import tempfile
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.abspath(os.path.join(BASE_DIR, "../../HomeLabAI/src")))

from scrub_all_passwords import sanitize_with_tripwire  # noqa: E402
from nibble_v2 import audit_focal_coaching_tripwire  # noqa: E402
from infra import standalone_accountability_watchdog as watchdog  # noqa: E402


ESCAPE_CANARIES = [
    ("cli_svn_password", "svn --username jallred --password CanarySecret99 export https://example.invalid/repo"),
    ("cli_docker_eq", "docker login --password=CanarySecretEq88 https://reg.example.invalid"),
    ("cli_gh_token", 'gh auth --token "ghp_CanaryTokenValue123456"'),
    ("cli_mysql_quoted", "mysql -u root -p'CanaryMysqlSecret!1' db_prod < dump.sql"),
    ("curl_userpass", "curl -k -u 'admin:CanaryCurlPass12' https://127.0.0.1/redfish"),
    ("url_basic_auth", "https://deploy_user:CanaryUrlPass34@artifactory.example.invalid/pkg"),
    ("jfrog_key", "X-JFrog-Art-Api: AKCp8CanaryJfrogKey1234567890"),
]


def run_tripwire_watch() -> bool:
    print("=== [1] WATCHING SIMULATED ESCAPES -> BACKUP TRIPWIRE ===")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        ledger_path = tmp_path / "sanitization_escape_ledger.jsonl"

        for label, raw in ESCAPE_CANARIES:
            clean, escaped, rules = sanitize_with_tripwire(raw)
            print(f"  [{label}] escaped={escaped} rules={rules}")
            print(f"    raw:      {raw}")
            print(f"    redacted: {clean}")
            assert escaped, f"Expected backup to catch {label}"
            assert clean != raw, f"Expected redaction for {label}"

            # Verify idempotency on already-redacted output
            clean2, escaped2, _rules2 = sanitize_with_tripwire(clean)
            assert not escaped2 and clean2 == clean, f"Not idempotent for {label}"

            entry = {
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "file_source": f"canary:{label}",
                "field": "evidence",
                "raw_snippet": raw,
                "redacted_snippet": clean,
                "matched_rules": rules,
                "loop_id": "LOOP-006",
            }
            with open(ledger_path, "a", encoding="utf-8") as lf:
                lf.write(json.dumps(entry) + "\n")

        # Verify non-secret port flag is NOT false-positived
        port_cmd = "llama-server -p 8088 --host 127.0.0.1"
        p_clean, p_esc, p_rules = sanitize_with_tripwire(port_cmd)
        assert not p_esc and p_rules == [] and p_clean == port_cmd, f"False positive on port flag: {p_rules}"
        print(f"  [non_secret_port_flag] escaped={p_esc} rules={p_rules} (clean)")

        # Verify watchdog tripwire flags the temp ledger as passed=False
        orig_output_dir = watchdog.OUTPUT_DIR
        try:
            watchdog.OUTPUT_DIR = tmp_path
            res = watchdog.check_sanitization_tripwire()
        finally:
            watchdog.OUTPUT_DIR = orig_output_dir

        print("=== [2] WATCHDOG TRIPWIRE RESULT ===")
        print(f"  passed={res['passed']} | detail={res['detail']}")
        assert res["passed"] is False, "Expected watchdog tripwire to fail when escapes exist"
    return True


def run_focal_coaching_tripwire_test() -> bool:
    print("=== [3] TESTING FOCAL / COACHING ESCAPE TRIPWIRE [VIBE-008] ===")
    
    # 1. Pure coaching / appraisal -> DROP
    pure_coaching_event = {
        "summary": "Annual review performance rating notes",
        "evidence": "AREAS FOR IMPROVEMENT: CanaryUser performance appraisal feedback notes. Rated Successful.",
        "domain": "operations"
    }
    clean_ev, escaped, rules, disp = audit_focal_coaching_tripwire(pure_coaching_event)
    print(f"  [pure_coaching] escaped={escaped} disp={disp} rules={rules}")
    assert escaped, "Expected pure coaching event to be caught"
    assert disp == "DROP", f"Expected DROP disposition, got {disp}"
    assert "areas_for_improvement" in rules or "rated_successful" in rules

    # 2. Hybrid event with technical registers/commands -> SURGICAL_SUTURE
    hybrid_event = {
        "summary": "PCIe ReBAR Configuration on Haswell Host",
        "evidence": "setpci -s 03:00.0 428.L=00000D02 forced ReBAR to 8GB. Results Coaching: In Q1 CanaryUser should complete migration milestone.",
        "domain": "hardware_debug"
    }
    clean_ev2, escaped2, rules2, disp2 = audit_focal_coaching_tripwire(hybrid_event)
    print(f"  [hybrid_tech] escaped={escaped2} disp={disp2} rules={rules2}")
    print(f"    cleaned evidence: {clean_ev2['evidence']}")
    assert escaped2, "Expected hybrid event to be caught"
    assert disp2 == "SURGICAL_SUTURE", f"Expected SURGICAL_SUTURE, got {disp2}"
    assert "setpci -s 03:00.0 428.L=00000D02 forced ReBAR to 8GB." in clean_ev2["evidence"]
    assert "Results Coaching" not in clean_ev2["evidence"]

    # 3. Clean technical message with word-boundary safety -> CLEAN
    clean_msg_event = {
        "summary": "PlatformConfig.xml generated successfully",
        "evidence": "/nfs/site/disks/svtools/gfxplatform generate --device cnl.3x8.a0 --ofile PlatformConfig_amber.xml",
        "domain": "hardware_debug"
    }
    clean_ev3, escaped3, rules3, disp3 = audit_focal_coaching_tripwire(clean_msg_event)
    print(f"  [clean_tech_word_boundary] escaped={escaped3} disp={disp3} rules={rules3}")
    assert not escaped3, f"False positive on generated successfully: {rules3}"
    assert disp3 == "CLEAN"

    print("  ✅ All Focal Coaching Tripwire checks certified.")
    return True


def run_live_llm_canary():
    from ai_engine_v2 import get_engine_v2

    print("=== [3] LIVE LLM CANARY (WATCHING PROMPT VS BACKUP) ===")
    engine = get_engine_v2(mode="LOCAL")
    canary_pw = "CanaryLiveCliPass77!"
    prompt = (
        "[SANITIZATION LAW - BKM-015]\n"
        "When copying commands into 'evidence', strip all passwords, tokens, and API keys. "
        'Replace any credential value with "[REDACTED_PASSWORD]".\n\n'
        "[SOURCE LOG]\n"
        f"2024-05-01 09:00:00 [DEPLOY] svn --username devuser --password {canary_pw} export https://svn.example.invalid/trunk\n\n"
        'Return ONLY JSON: [{"date": "2024-05-01", "summary": "...", "evidence": "..."}]'
    )
    raw_resp = engine.generate(prompt)
    clean_resp, escaped, rules = sanitize_with_tripwire(raw_resp)
    print(f"  LLM raw response:\n{raw_resp.strip()}")
    print(f"  Backup tripwire triggered? escaped={escaped}, rules={rules}")
    if escaped:
        print("  ⚠️  CRITICAL ESCAPE: LLM leaked credential; backup caught and redacted it!")
        print(f"  Redacted output:\n{clean_resp.strip()}")
    else:
        print("  ✅ LLM redacted cleanly without needing backup.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Watch Nibbler credential escapes & backup tripwire.")
    parser.add_argument("--live", action="store_true", help="Also run live local LLM canary test")
    args = parser.parse_args()

    run_tripwire_watch()
    run_focal_coaching_tripwire_test()
    if args.live:
        run_live_llm_canary()
    print("✅ ALL NIBBLER ESCAPE TRIPWIRE CHECKS PASSED")
