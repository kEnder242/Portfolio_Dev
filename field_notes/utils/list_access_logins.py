#!/usr/bin/env python3
"""
[FEAT-089 / LAB-020] List Unique Logins & Cloudflare Zero Trust Access Audit
Scans local session ledgers (journal_ledger.jsonl, foyer_queue.jsonl) and
optionally queries the Cloudflare Zero Trust Access API for unique user emails
and their latest login timestamps on jason-lab.dev.
"""

import os
import re
import json
import base64
import argparse
import datetime
from typing import Dict, Any, Optional

CF_ACCOUNT_ID = "c58aa4580ff695cce2f611177d2173a5"
CF_ZONE_ID = "c560564464f6202dde62e8e67649f79c"
CERT_PATH = os.path.expanduser("~/.cloudflared/cert.pem")
DEFAULT_LEDGER = os.path.expanduser("~/Dev_Lab/Portfolio_Dev/field_notes/data/journal_ledger.jsonl")
DEFAULT_QUEUE = os.path.expanduser("~/Dev_Lab/Portfolio_Dev/field_notes/data/foyer_queue.jsonl")

EMAIL_REGEX = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
EXCLUDED_DOMAINS = ["example.com", "schema.org", "github.com", "git-amr", "gitlab"]

def extract_cert_token() -> Optional[str]:
    """Extracts the default API token embedded in ~/.cloudflared/cert.pem."""
    if not os.path.exists(CERT_PATH):
        return None
    try:
        with open(CERT_PATH, "r") as f:
            content = f.read()
        match = re.search(r"-----BEGIN ARGO TUNNEL TOKEN-----\s*([A-Za-z0-9+/=]+)\s*-----END ARGO TUNNEL TOKEN-----", content)
        if match:
            raw_b64 = match.group(1).strip()
            data = json.loads(base64.b64decode(raw_b64).decode("utf-8"))
            return data.get("apiToken")
    except Exception:
        pass
    return None

def query_cloudflare_access(api_token: str) -> list:
    """Queries Cloudflare Zero Trust Access API for access request logs."""
    try:
        import requests
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/access/logs/access_requests?limit=100"
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.json().get("result", [])
        else:
            return []
    except Exception:
        return []

def scan_local_ledgers() -> Dict[str, Dict[str, Any]]:
    """Scans local journal and foyer ledgers for unique user emails and latest timestamps."""
    results = {}

    # 1. Scan journal_ledger.jsonl
    if os.path.exists(DEFAULT_LEDGER):
        try:
            with open(DEFAULT_LEDGER, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                        ts = entry.get("ts")
                        dt = datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc) if ts else None
                        text = entry.get("dialogue", "")
                        for email in EMAIL_REGEX.findall(text):
                            if any(d in email.lower() for d in EXCLUDED_DOMAINS):
                                continue
                            if email not in results or (dt and (results[email]["latest_login"] is None or dt > results[email]["latest_login"])):
                                results[email] = {
                                    "email": email,
                                    "latest_login": dt,
                                    "source": "journal_ledger.jsonl",
                                    "occurrences": results.get(email, {}).get("occurrences", 0) + 1
                                }
                            else:
                                results[email]["occurrences"] += 1
                    except Exception:
                        pass
        except Exception:
            pass

    # 2. Scan foyer_queue.jsonl
    if os.path.exists(DEFAULT_QUEUE):
        try:
            with open(DEFAULT_QUEUE, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                        query_text = entry.get("query", "")
                        for email in EMAIL_REGEX.findall(query_text):
                            if any(d in email.lower() for d in EXCLUDED_DOMAINS):
                                continue
                            if email not in results:
                                results[email] = {
                                    "email": email,
                                    "latest_login": None,
                                    "source": "foyer_queue.jsonl",
                                    "occurrences": 1
                                }
                            else:
                                results[email]["occurrences"] += 1
                    except Exception:
                        pass
        except Exception:
            pass

    return results

def main():
    parser = argparse.ArgumentParser(description="List unique logins and access history on jason-lab.dev")
    parser.add_argument("--api-token", help="Cloudflare API Token with Access Audit read permissions")
    parser.add_argument("--json", action="store_true", help="Output raw JSON format")
    args = parser.parse_args()

    token = args.api_token or os.environ.get("CLOUDFLARE_API_TOKEN") or os.environ.get("CF_API_TOKEN") or extract_cert_token()
    cf_logs = []
    if token:
        cf_logs = query_cloudflare_access(token)

    local_logins = scan_local_ledgers()

    # Merge Cloudflare logs if available
    for log_item in cf_logs:
        user_email = log_item.get("user_email")
        created_at = log_item.get("created_at")
        if user_email and created_at:
            try:
                dt = datetime.datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            except Exception:
                dt = None
            if user_email not in local_logins or (dt and (local_logins[user_email]["latest_login"] is None or dt > local_logins[user_email]["latest_login"])):
                local_logins[user_email] = {
                    "email": user_email,
                    "latest_login": dt,
                    "source": "Cloudflare Zero Trust API",
                    "occurrences": local_logins.get(user_email, {}).get("occurrences", 0) + 1
                }

    if args.json:
        serializable = {}
        for k, v in local_logins.items():
            serializable[k] = {
                "email": v["email"],
                "latest_login": v["latest_login"].isoformat() if v["latest_login"] else None,
                "source": v["source"],
                "occurrences": v["occurrences"]
            }
        print(json.dumps(serializable, indent=2))
        return

    print("=" * 80)
    print(f"🔒 jason-lab.dev Unique User Logins & Access Audit")
    print(f"Cloudflare Account ID: {CF_ACCOUNT_ID} | Zone: {CF_ZONE_ID}")
    print("=" * 80)
    if not local_logins:
        print("No user logins detected.")
        return

    print(f"{'Email Address':<38} | {'Latest Login (UTC)':<22} | {'Hits':<5} | {'Source'}")
    print("-" * 80)
    for email, data in sorted(local_logins.items(), key=lambda x: str(x[1]["latest_login"] or ""), reverse=True):
        latest_str = data["latest_login"].strftime("%Y-%m-%d %H:%M:%S") if data["latest_login"] else "Unknown / Historical"
        print(f"{email:<38} | {latest_str:<22} | {data['occurrences']:<5} | {data['source']}")
    print("=" * 80)

if __name__ == "__main__":
    main()
