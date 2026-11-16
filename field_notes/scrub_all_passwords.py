#!/usr/bin/env python3
"""
[BKM-061 / Story 110.30] Global Deterministic Secrets and Credentials Scrubber.
Scans and scrubs sensitive credentials (curl -u, passwords, Artifactory tokens, basic auth)
across all JSON datasets in Portfolio_Dev and www_deploy.
"""

import base64
import glob
import json
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORTFOLIO_DATA = os.path.join(BASE_DIR, "data")
DEPLOY_DATA = os.path.abspath(os.path.join(BASE_DIR, "../../www_deploy/data"))

KNOWN_PASSWORDS_FILE = os.environ.get(
    "HOMELAB_KNOWN_PASSWORDS_FILE",
    os.path.expanduser("~/.config/homelab/known_passwords.json"),
)


def _load_known_passwords() -> list[str]:
    if not os.path.exists(KNOWN_PASSWORDS_FILE):
        return []
    try:
        with open(KNOWN_PASSWORDS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        items = data.get("known_passwords", []) if isinstance(data, dict) else data
        return sorted({str(x) for x in items if isinstance(x, str) and x}, key=len, reverse=True)
    except Exception:
        return []


KNOWN_PASSWORDS = _load_known_passwords()


def sanitize_with_tripwire(text: str) -> tuple[str, bool, list[str]]:
    """Sanitize text and return (sanitized_text, escaped, matched_rules).
    
    escaped = True if any secret was redacted.
    matched_rules = list of rule names that triggered redaction.
    """
    if not isinstance(text, str):
        return text, False, []

    original = text
    matched_rules = []

    # 1. Strip curl -u / -sku / -ku / -fu / --user flags with user:password
    def _scrub_curl_userpass(m):
        if m.group(3).startswith("[REDACTED"):
            return m.group(0)
        matched_rules.append("curl_userpass")
        return m.group(1) + m.group(2) + ":[REDACTED_PASSWORD]" + m.group(4)

    text = re.sub(
        r'(-[a-zA-Z]*u\s+[\"\']?)([^:\s\"\']+):([^\s\"\']+)([\"\']?)',
        _scrub_curl_userpass,
        text
    )
    text = re.sub(
        r'(--user\s+[\"\']?)([^:\s\"\']+):([^\s\"\']+)([\"\']?)',
        _scrub_curl_userpass,
        text
    )

    # 2. URLs with basic auth: https://user:pass@host
    def _scrub_url_auth(m):
        if m.group(3).startswith("[REDACTED"):
            return m.group(0)
        matched_rules.append("url_basic_auth")
        return m.group(1) + m.group(2) + ":[REDACTED_PASSWORD]@"

    text = re.sub(
        r'(https?://)([^:\s/@]+):([^@\s/]+)@',
        _scrub_url_auth,
        text
    )

    # 3. Known historical leaked lab passwords / tokens (loaded from external secret file)
    if KNOWN_PASSWORDS:
        for sec in KNOWN_PASSWORDS:
            if re.search(re.escape(sec), text, flags=re.IGNORECASE):
                matched_rules.append("known_password")
                break
        text = re.sub(
            "|".join(map(re.escape, KNOWN_PASSWORDS)),
            "[REDACTED_PASSWORD]",
            text,
            flags=re.IGNORECASE,
        )

    # 4. setx / export password assignments
    text = re.sub(
        r'(setx\s+(?:sys_pwd|password|passwd|token)\s+)([^\s,]+)',
        lambda m: (matched_rules.append("setx_export") or m.group(1) + "[REDACTED_PASSWORD]"),
        text,
        flags=re.IGNORECASE
    )
    text = re.sub(
        r'(export\s+(?:sys_pwd|password|passwd|token)=)([^\s,]+)',
        lambda m: (matched_rules.append("setx_export") or m.group(1) + "[REDACTED_PASSWORD]"),
        text,
        flags=re.IGNORECASE
    )

    # 5. JFrog Artifactory API keys (AKCp8...)
    text = re.sub(
        r'AKCp8[a-zA-Z0-9]{15,}',
        lambda m: (matched_rules.append("jfrog_api_key") or "[REDACTED_JFROG_API_KEY]"),
        text
    )

    # 6. [BKM-015:APPROVED_REGEX] Generic CLI Option Secrets (--password val, --password=val, --token val, etc.)
    def _scrub_cli_option(m):
        val = m.group(2)
        if val.startswith("[REDACTED"):
            return m.group(0)
        matched_rules.append("cli_option_secret")
        return m.group(1) + "[REDACTED_PASSWORD]" + m.group(3)

    text = re.sub(
        r'((?:^|\s)--?(?:password|passwd|pwd|pass|token|api[-_]?key|secret|access[-_]?token|auth[-_]?token)(?:=|\s+)[\"\']?)([^\s\"\']+)([\"\']?)',
        _scrub_cli_option,
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r'((?:^|\s)-p[\"\'])([^\"\']+)([\"\'])',
        _scrub_cli_option,
        text,
    )

    escaped = text != original
    # Deduplicate matched_rules while preserving order
    seen = set()
    deduped_rules = [r for r in matched_rules if not (r in seen or seen.add(r))]
    return text, escaped, deduped_rules


def sanitize_text(text: str) -> str:
    """Backward compatible wrapper - returns only sanitized text."""
    return sanitize_with_tripwire(text)[0]


def sanitize_obj(obj):
    if isinstance(obj, str):
        return sanitize_text(obj)
    elif isinstance(obj, list):
        return [sanitize_obj(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: sanitize_obj(v) for k, v in obj.items()}
    return obj


def process_file(filepath: str) -> int:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Skipping unreadable file {filepath}: {e}")
        return 0

    sanitized = sanitize_text(content)
    if sanitized != content:
        # Atomic write
        tmp_path = filepath + ".scrub.tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(sanitized)
        os.replace(tmp_path, filepath)
        print(f"   [SCRUBBED] {filepath}")
        return 1
    return 0


def main():
    print("--- [BKM-061] Global Secrets & Credentials Scrubber ---")
    total_modified = 0

    target_dirs = [PORTFOLIO_DATA, DEPLOY_DATA]
    for d in target_dirs:
        if not os.path.exists(d):
            print(f"Directory not found: {d}")
            continue
        print(f"\nScanning: {d}")
        json_files = sorted(glob.glob(os.path.join(d, "**/*.json"), recursive=True))
        for jf in json_files:
            total_modified += process_file(jf)

    print(f"\nDone. Total files scrubbed and updated: {total_modified}")


if __name__ == "__main__":
    main()
