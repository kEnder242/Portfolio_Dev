import json
import os
import re
import glob

# Audit on the backup
TARGET_DIR = "Portfolio_Dev/field_notes/data_contaminated_backup"
REPORT_FILE = "Portfolio_Dev/field_notes/data/privacy_audit.json"

FORBIDDEN_PATTERNS = [
    r"Jason should",
    r"needs to improve",
    r"missed on this opportunity",
    r"areas for development",
    r"feedback",
    r"coaching",
    r"Results Coaching",
    r"Behaviors Coaching"
]

def audit():
    print(f"--- Privacy Audit: Analyzing {TARGET_DIR} ---")
    if not os.path.exists(TARGET_DIR):
        print(f"Error: Target directory {TARGET_DIR} not found.")
        return
        
    files = glob.glob(os.path.join(TARGET_DIR, "20*.json"))
    report = []
    
    for fpath in sorted(files):
        with open(fpath, 'r') as f:
            try:
                data = json.load(f)
                if not isinstance(data, list): continue
            except: continue
            
        for entry in data:
            evidence = entry.get('evidence', '')
            summary = entry.get('summary', '')
            text_to_check = f"{summary} {evidence}"
            
            for pattern in FORBIDDEN_PATTERNS:
                if re.search(pattern, text_to_check, re.IGNORECASE):
                    report.append({
                        "file": os.path.basename(fpath),
                        "pattern": pattern,
                        "entry": entry
                    })
                    break
                    
    with open(REPORT_FILE, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"Audit complete. Found {len(report)} contaminated entries. Saved to {REPORT_FILE}")

if __name__ == "__main__":
    audit()
