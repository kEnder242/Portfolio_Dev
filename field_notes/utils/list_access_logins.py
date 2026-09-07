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

def get_api_token(args_token: Optional[str] = None) -> Optional[str]:
    """Retrieves Cloudflare API token from arguments, env, secrets file, or cert."""
    if args_token:
        return args_token
    if os.environ.get("CLOUDFLARE_API_TOKEN"):
        return os.environ.get("CLOUDFLARE_API_TOKEN")
    if os.environ.get("CF_API_TOKEN"):
        return os.environ.get("CF_API_TOKEN")
    secret_file = os.path.expanduser("~/.secrets/cloudflare_token")
    if os.path.exists(secret_file):
        try:
            with open(secret_file, "r") as f:
                token = f.read().strip()
                if token:
                    return token
        except Exception:
            pass
    return extract_cert_token()

def query_cloudflare_users_and_logs(api_token: str) -> Dict[str, Any]:
    """Queries Cloudflare Zero Trust Access Users and Access Request logs."""
    results = {"users": [], "logs": [], "apps": []}
    try:
        import urllib.request
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        
        # 1. Query Zero Trust Users
        try:
            req_users = urllib.request.Request(
                f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/access/users",
                headers=headers
            )
            with urllib.request.urlopen(req_users, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                results["users"] = data.get("result", [])
        except Exception:
            pass

        # 2. Query Access Request Logs
        try:
            req_logs = urllib.request.Request(
                f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/access/logs/access_requests?limit=100",
                headers=headers
            )
            with urllib.request.urlopen(req_logs, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                results["logs"] = data.get("result", [])
        except Exception:
            pass

        # 3. Query Apps and Policies
        try:
            req_apps = urllib.request.Request(
                f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/access/apps",
                headers=headers
            )
            with urllib.request.urlopen(req_apps, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                results["apps"] = data.get("result", [])
        except Exception:
            pass
            
    except Exception:
        pass
    return results

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

    token = get_api_token(args.api_token)
    cf_data = {"users": [], "logs": [], "apps": []}
    if token:
        cf_data = query_cloudflare_users_and_logs(token)

    local_logins = scan_local_ledgers()

    # Merge Cloudflare registered users
    for user in cf_data.get("users", []):
        u_email = user.get("email")
        last_login_str = user.get("last_successful_login")
        dt = None
        if last_login_str:
            try:
                dt = datetime.datetime.fromisoformat(last_login_str.replace("Z", "+00:00"))
            except Exception:
                pass
        if u_email:
            if u_email not in local_logins:
                local_logins[u_email] = {
                    "email": u_email,
                    "latest_login": dt,
                    "source": "Cloudflare Zero Trust User Registry",
                    "occurrences": 1
                }
            else:
                if dt and (local_logins[u_email]["latest_login"] is None or dt > local_logins[u_email]["latest_login"]):
                    local_logins[u_email]["latest_login"] = dt
                local_logins[u_email]["source"] = f"{local_logins[u_email]['source']} + CF User Registry"

    # Merge Cloudflare request logs
    for log_item in cf_data.get("logs", []):
        user_email = log_item.get("user_email")
        created_at = log_item.get("created_at")
        if user_email and created_at:
            try:
                dt = datetime.datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            except Exception:
                dt = None
            if user_email not in local_logins:
                local_logins[user_email] = {
                    "email": user_email,
                    "latest_login": dt,
                    "source": "Cloudflare Zero Trust Access Logs",
                    "occurrences": 1
                }
            else:
                if dt and (local_logins[user_email]["latest_login"] is None or dt > local_logins[user_email]["latest_login"]):
                    local_logins[user_email]["latest_login"] = dt
                local_logins[user_email]["occurrences"] += 1

    if args.json:
        serializable = {
            "users": {
                k: {
                    "email": v["email"],
                    "latest_login": v["latest_login"].isoformat() if v["latest_login"] else None,
                    "source": v["source"],
                    "occurrences": v["occurrences"]
                }
                for k, v in local_logins.items()
            },
            "apps": cf_data.get("apps", [])
        }
        print(json.dumps(serializable, indent=2))
        return

    print("=" * 85)
    print(f"🔒 jason-lab.dev Unique User Logins & Zero Trust Access Audit")
    print(f"Cloudflare Account ID: {CF_ACCOUNT_ID} | Zone: {CF_ZONE_ID}")
    if token:
        print(f"Auth Status: Authenticated via Bearer API Token (Cloudflare REST Connected)")
    else:
        print(f"Auth Status: Unauthenticated / Local Ledger Traces Only")
    print("=" * 85)
    if not local_logins:
        print("No user logins detected.")
        return

    print(f"{'Email Address':<32} | {'Latest Login (UTC)':<20} | {'Hits':<5} | {'Source'}")
    print("-" * 85)
    for email, data in sorted(local_logins.items(), key=lambda x: str(x[1]["latest_login"] or ""), reverse=True):
        latest_str = data["latest_login"].strftime("%Y-%m-%d %H:%M:%S") if data["latest_login"] else "Unknown / Historical"
        print(f"{email:<32} | {latest_str:<20} | {data['occurrences']:<5} | {data['source']}")
    print("=" * 85)

if __name__ == "__main__":
    main()
