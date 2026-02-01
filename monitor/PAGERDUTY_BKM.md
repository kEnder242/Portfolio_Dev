# BKM Protocol: Neural Pager Deployment

**Status:** ACTIVE / LIVE
**Date:** February 1, 2026

## 1. Preparation (The "Soil")
```bash
# Environment
pip install requests

# Secrets & Safety
echo '{"PAGERDUTY_ROUTING_KEY": "YOUR_32_CHAR_KEY"}' > monitor/secrets.json
echo "monitor/secrets.json" >> .gitignore
```

## 2. The Critical Logic (The "Core")
**The API Uplink (`notify_pd.py`):**
```python
# Atomic UTC Timestamping (Fixes Python 3.12+ Deprecation)
timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

# The Payload Structure (Maps 'warning' to PD 'error' for API compliance)
payload = {
    "routing_key": key,
    "event_action": "trigger",
    "payload": { "summary": msg, "source": src, "severity": sev if sev != "warning" else "error" }
}
requests.post("https://events.pagerduty.com/v2/enqueue", json=payload)
```

**The Node Bridge (`pinky_node.py`):**
```python
# Decoupled Intelligence/Platform execution
cmd = ["python3", os.path.expanduser("~/Dev_Lab/Portfolio_Dev/monitor/notify_pd.py"), summary, "--source", source, "--severity", severity]
subprocess.run(cmd, capture_output=True)
```

## 3. Trigger Points (The "Action")
```bash
# Manual Validation
python3 monitor/notify_pd.py "Neural Pager: LIVE Deployment Successful" --source "System" --severity "critical"
```

## 4. Retrospective (The "Scars")
*   **Mis-step:** Using `utcnow()` created noisy terminal warnings. **Fix:** Use `now(timezone.utc)`.
*   **Mis-step:** Hardcoded "Back" buttons in `timeline.html` caused navigation drift. **Fix:** Centralized all "Home" logic into the **Mission Control** sidebar.
*   **Mis-step:** PD API rejected `warning` severity. **Fix:** Ternary mapping in the payload generator.