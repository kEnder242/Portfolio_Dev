import json
import os
import requests
import sys
from datetime import datetime, timezone

# Paths
BASE_DIR = os.path.dirname(__file__)
SECRETS_PATH = os.path.join(BASE_DIR, "secrets.json")
PAGER_LOG = os.path.join(BASE_DIR, "../field_notes/data/pager_activity.json")

def load_secrets():
    if not os.path.exists(SECRETS_PATH):
        print(f"Error: {SECRETS_PATH} not found.")
        return None
    with open(SECRETS_PATH, "r") as f:
        return json.load(f)

def fetch_cf_logs(secrets):
    token = secrets.get("CF_API_TOKEN")
    account_id = secrets.get("CF_ACCOUNT_ID")
    
    if not token or not account_id:
        print("Error: Missing CF_API_TOKEN or CF_ACCOUNT_ID in secrets.json")
        return []

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 1. Try Audit Logs (Comprehensive trail)
    url_audit = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/audit_logs"
    try:
        response = requests.get(url_audit, headers=headers)
        if response.status_code == 200:
            audit_result = response.json().get("result", [])
            pseudo_logs = []
            for entry in audit_result:
                action = entry.get("action", {})
                # Look for Access login/token creation events
                if "login" in action.get("type", "").lower() or "access" in action.get("type", "").lower():
                    pseudo_logs.append({
                        "created_at": entry.get("when"),
                        "user_email": entry.get("actor", {}).get("email", "System"),
                        "app_name": "Zero Trust (Audit Log)",
                        "action": action.get("type", "login")
                    })
            if pseudo_logs: return pseudo_logs
        else:
            print(f"Info: CF Audit Logs returned {response.status_code}. Falling back to Access Users.")
    except Exception as e:
        print(f"Error connecting to CF Audit: {e}")

    # 2. Try Access Users (Summary of last logins)
    url_users = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/access/users"
    try:
        response = requests.get(url_users, headers=headers)
        if response.status_code == 200:
            users = response.json().get("result", [])
            # Map user 'last_successful_login' to log format
            pseudo_logs = []
            for u in users:
                if u.get("last_successful_login"):
                    pseudo_logs.append({
                        "created_at": u["last_successful_login"],
                        "user_email": u["email"],
                        "app_name": "Zero Trust (Active Session)",
                        "action": "login"
                    })
            return pseudo_logs
        else:
            print(f"Error: CF Users API returned {response.status_code}: {response.text}")
            return []
    except Exception as e:
        print(f"Error connecting to CF Users: {e}")
        return []

def main():
    print("--- Cloudflare Access Retro-Scanner ---")
    secrets = load_secrets()
    if not secrets: return

    logs = fetch_cf_logs(secrets)
    if not logs:
        print("No new logs found or error occurred.")
        return

    print(f"Found {len(logs)} access requests.")

    # Load existing pager logs
    if os.path.exists(PAGER_LOG):
        with open(PAGER_LOG, "r") as f:
            try:
                pager_data = json.load(f)
            except: pager_data = []
    else:
        pager_data = []

    # Map CF logs to Pager events
    added_count = 0
    seen_timestamps = {e.get("timestamp") for e in pager_data}

    for log in logs:
        # CF uses created_at
        ts = log.get("created_at")
        if ts and ts not in seen_timestamps:
            email = log.get("user_email", "Unknown")
            app = log.get("app_name", "Zero Trust")
            action = log.get("action", "request")
            
            event = {
                "timestamp": ts,
                "severity": "INFO",
                "source": "Cloudflare",
                "message": f"Access {action} by {email} for {app}."
            }
            pager_data.append(event)
            seen_timestamps.add(ts)
            added_count += 1

    if added_count > 0:
        # Sort by timestamp DESC
        pager_data.sort(key=lambda x: x.get("timestamp"), reverse=True)
        # Trim to 100
        pager_data = pager_data[:100]
        
        with open(PAGER_LOG, "w") as f:
            json.dump(pager_data, f, indent=4)
        print(f"Success: Added {added_count} events to pager.")
    else:
        print("No new unique events to add.")

if __name__ == "__main__":
    main()
