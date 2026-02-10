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

# NTFY Config (Placeholder - User can change)
NTFY_TOPIC = "jason_lab_alerts"
NTFY_URL = f"https://ntfy.sh/{NTFY_TOPIC}"

def get_secrets():
    try:
        if os.path.exists(SECRETS_PATH):
            with open(SECRETS_PATH, "r") as f:
                return json.load(f)
    except Exception as e:
        print(f"Error reading secrets: {e}", file=sys.stderr)
    return {}

def notify_gatekeeper(summary, source, severity, emergency=False, dry_run=False):
    """
    Triage notifications:
    - Log all to JSON.
    - CRITICAL -> NTFY.
    - --emergency flag -> PagerDuty (Backup).
    """
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    secrets = get_secrets()
    
    event = {
        "timestamp": timestamp,
        "severity": severity.upper(),
        "source": source,
        "message": summary
    }
    
    print(f"[{severity.upper()}] {source}: {summary}")

    # 1. Local Logging (Always)
    try:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "r") as f:
                data = json.load(f)
        else:
            data = []
            
        data.insert(0, event)
        data = data[:100] # Keep last 100
        
        with open(LOG_PATH, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error logging activity: {e}", file=sys.stderr)

    if dry_run:
        print("DRY RUN: External notifications skipped.")
        return

    # 2. NTFY (Live Interrupt for CRITICAL)
    if severity.lower() == "critical":
        try:
            print(f"NTFY: Sending critical alert to {NTFY_URL}...")
            requests.post(NTFY_URL, 
                          data=f"[{source}] {summary}".encode('utf-8'),
                          headers={"Title": f"LAB ALERT: {severity.upper()}", "Priority": "high"})
        except Exception as e:
            print(f"NTFY Error: {e}", file=sys.stderr)

    # 3. PagerDuty (Manual Emergency Backup)
    if emergency:
        routing_key = secrets.get("PAGERDUTY_ROUTING_KEY")
        if routing_key:
            print(f"EMERGENCY: Triggering PagerDuty backup...")
            url = "https://events.pagerduty.com/v2/enqueue"
            payload = {
                "routing_key": routing_key,
                "event_action": "trigger",
                "payload": {
                    "summary": f"EMERGENCY: {summary}",
                    "source": source,
                    "severity": "critical"
                }
            }
            try:
                response = requests.post(url, json=payload)
                if response.status_code == 202:
                    print("LIVE: PagerDuty emergency alert triggered.")
                else:
                    print(f"ERROR: PagerDuty returned {response.status_code}")
            except Exception as e:
                print(f"ERROR: PagerDuty connection failed: {e}")
        else:
            print("EMERGENCY skip: No PagerDuty routing key found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HomeLabAI Notification Gatekeeper")
    parser.add_argument("summary", help="Brief description of the event")
    parser.add_argument("--source", default="Manual", help="Source of the alert")
    parser.add_argument("--severity", choices=["info", "warning", "critical"], default="info", help="Severity level")
    parser.add_argument("--emergency", action="store_true", help="Force PagerDuty backup notification")
    parser.add_argument("--dry-run", action="store_true", help="Log locally but skip external calls")
    
    args = parser.parse_args()
    
    notify_gatekeeper(args.summary, args.source, args.severity, args.emergency, args.dry_run)
