#!/usr/bin/env python3
import argparse
import json
import os
import sys
import requests
from datetime import datetime, timezone

# Paths
BASE_DIR = os.path.dirname(__file__)
LOG_PATH = os.path.join(BASE_DIR, "../field_notes/data/pager_activity.json")
SECRETS_PATH = os.path.join(BASE_DIR, "secrets.json")

def get_routing_key():
    try:
        if os.path.exists(SECRETS_PATH):
            with open(SECRETS_PATH, "r") as f:
                return json.load(f).get("PAGERDUTY_ROUTING_KEY")
    except Exception as e:
        print(f"Error reading secrets: {e}", file=sys.stderr)
    return None

def notify_pd(summary, source, severity, dry_run=False):
    """
    Real PagerDuty notification via Events API v2 and local logging.
    """
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    routing_key = get_routing_key()
    
    event = {
        "timestamp": timestamp,
        "severity": severity.upper(),
        "source": source,
        "message": summary
    }
    
    print(f"[{severity.upper()}] {source}: {summary}")
    
    if dry_run or not routing_key or routing_key == "PASTE_YOUR_KEY_HERE":
        print("DRY RUN or MISSING KEY: PagerDuty notification skipped.")
    else:
        # PagerDuty Events API v2
        url = "https://events.pagerduty.com/v2/enqueue"
        payload = {
            "routing_key": routing_key,
            "event_action": "trigger",
            "payload": {
                "summary": summary,
                "source": source,
                "severity": severity if severity != "warning" else "error"  # PD uses error/critical/warning/info
            }
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 202:
                print(f"LIVE: PagerDuty alert triggered. (ID: {response.json().get('dedup_key')})")
            else:
                print(f"ERROR: PagerDuty API returned {response.status_code}: {response.text}")
        except Exception as e:
            print(f"ERROR: Failed to connect to PagerDuty: {e}")

    # Local Logging
    try:
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "r") as f:
                data = json.load(f)
        else:
            data = []
            
        data.insert(0, event)
        data = data[:100]
        
        with open(LOG_PATH, "w") as f:
            json.dump(data, f, indent=4)
            
    except Exception as e:
        print(f"Error logging pager activity: {e}", file=sys.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HomeLabAI PagerDuty Gateway")
    parser.add_argument("summary", help="Brief description of the event")
    parser.add_argument("--source", default="Manual", help="Source of the alert (e.g., Pinky, System)")
    parser.add_argument("--severity", choices=["info", "warning", "critical"], default="info", help="Severity level")
    parser.add_argument("--dry-run", action="store_true", help="Log locally but skip PagerDuty API call")
    
    args = parser.parse_args()
    
    notify_pd(args.summary, args.source, args.severity, args.dry_run)
