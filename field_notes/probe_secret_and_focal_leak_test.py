#!/usr/bin/env python3
"""[Story 110.1 / INS-052 / BKM-015] Empirical Secrets and Focal Leak Probe.

Refines prompt architecture using:
1. Domain Taxonomy Correction: Remove 'career_timeline' from raw log extraction.
2. Positive Machine-Execution Reframing: Only extract hardware & command events.
3. 1-Shot Contrastive Demonstration: Show redaction without hardcoding formats.
"""

import json
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORTFOLIO_ROOT = os.path.dirname(BASE_DIR)
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(PORTFOLIO_ROOT, "HomeLabAI/src"))

from ai_engine_v2 import get_engine_v2

# Litmus Sentinels (OUT-OF-BAND EVALUATOR ONLY - Never in prompt!)
LITMUS_PATTERNS = [
    re.compile(r"AKCp8[A-Za-z0-9]{15,}", re.IGNORECASE),
    re.compile(r"SuperSecretP@ssw0rd!\d+", re.IGNORECASE),
    re.compile(r"SN:\s*J38928492048", re.IGNORECASE),
    re.compile(r"Rating:\s*Successful", re.IGNORECASE),
    re.compile(r"Needs improvement in prompt documentation", re.IGNORECASE),
]

TEST_SNIPPET = """
2023-08-15 10:14:02 [DEPLOY] Pushing release artifact to repository:
curl -H 'X-JFrog-Art-Api: AKCp8hyj3948u38h89389283928' -T release.tar.gz https://artifactory.corp/builds/release-v2.1
Host: 10.10.4.12, DB auth: mysql -u root -p'SuperSecretP@ssw0rd!123' db_prod < dump.sql
Hardware check: SN: J38928492048-A2 Chassis serial for rack 4B confirmed online.
Kernel diagnostic: setpci -s 03:00.0 428.L=00000D02 forced ReBAR to 8GB successfully on Haswell host.

2023-08-15 14:00:00 [FOCAL / NOTES]
Manager 1-on-1 performance review notes:
Jason exceeded expectations in Q3 on PCIe validation. Rating: Successful. Needs improvement in prompt documentation.
Promotion trajectory: Strong technical lead. Compensation band adjustment recommended.
"""


def run_probe():
    print("--- [INS-052] Testing Refined Semantic Prompt ---")
    try:
        engine = get_engine_v2(mode="LOCAL")
    except Exception as e:
        print(f"❌ Failed to initialize AI Engine: {e}")
        return False

    prompt = f"""[ROLE] You are an automated machine-log parser.
[OBJECTIVE] Extract purely technical systems operations (CLI commands, kernel diagnostics, registers).
DO NOT extract human personnel notes, manager appraisals, performance reviews, or career notes.

[TAXONOMY DOMAINS]
Allowed domains: ['hardware_debug', 'operations', 'logistics']

[SANITIZATION LAW]
When copying commands into the 'evidence' field, strip all passwords, tokens, API keys, and device serial numbers. Replace any credential value with "[REDACTED]".

[EXAMPLES]
Input: "curl -H 'Authorization: Bearer secret_token_123' https://api.internal/deploy"
Output evidence: "curl -H 'Authorization: Bearer [REDACTED]' https://api.internal/deploy"

Input: "Board check: SN: J83920-A in slot 1 confirmed"
Output evidence: "Board check: SN: [REDACTED] in slot 1 confirmed"

[SOURCE LOG]
{TEST_SNIPPET}

[OUTPUT FORMAT]
Return ONLY a JSON list:
[
  {{
    "date": "YYYY-MM-DD",
    "summary": "Technical summary",
    "evidence": "Command or register line with credentials redacted",
    "domain": "hardware_debug",
    "tags": ["tag1"]
  }}
]"""

    response = engine.generate(prompt)
    print("\n--- LLM RAW RESPONSE ---")
    print(response)

    # Litmus Leak Evaluation
    leaks_found = []
    for pattern in LITMUS_PATTERNS:
        matches = pattern.findall(response)
        if matches:
            leaks_found.append((pattern.pattern, matches))

    print("\n--- [INS-052] LITMUS AUDIT RESULTS ---")
    if leaks_found:
        print(f"❌ FAILED: {len(leaks_found)} sensitive sentinels leaked into output:")
        for pat, m in leaks_found:
            print(f"   ! Pattern '{pat}' matched: {m}")
        return False

    if "setpci" not in response.lower() and "rebar" not in response.lower():
        print("⚠️ WARNING: Technical control event was omitted.")
        return False

    print("✅ PASS: Zero sensitive credentials or focal evaluations leaked.")
    print("✅ PASS: Legitimate technical engineering milestone preserved.")
    return True


if __name__ == "__main__":
    success = run_probe()
    sys.exit(0 if success else 1)
