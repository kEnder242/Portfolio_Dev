import json
import os
import re
import glob

# [FEAT-133] Success Sanitizer: Post-Burn Privacy Guard
DATA_DIR = "Portfolio_Dev/field_notes/data"
FORBIDDEN_PATTERNS = [
    r"Jason should",
    r"needs to improve",
    r"missed on this opportunity",
    r"areas for development",
    r"feedback",
    r"coaching",
    r"Results Coaching",
    r"Behaviors Coaching",
    r"Growth Feedback"
]

def sanitize_file(fpath):
    if not os.path.exists(fpath): return
    with open(fpath, 'r') as f:
        try:
            data = json.load(f)
            if not isinstance(data, list): return
        except: return
        
    clean_data = []
    dropped = []
    for entry in data:
        text = f"{entry.get('summary', '')} {entry.get('evidence', '')}"
        if any(re.search(p, text, re.IGNORECASE) for p in FORBIDDEN_PATTERNS):
            dropped.append(entry)
        else:
            clean_data.append(entry)
            
    if dropped:
        print(f"   [SANTIZE] {os.path.basename(fpath)}: Dropped {len(dropped)} entries.")
        with open(fpath, 'w') as f:
            json.dump(clean_data, f, indent=2)
        
        # Append to a persistent audit log for review
        with open(os.path.join(DATA_DIR, "privacy_audit.jsonl"), "a") as f:
            for d in dropped:
                d['source_file'] = os.path.basename(fpath)
                f.write(json.dumps(d) + "
")

if __name__ == "__main__":
    print("--- Success Sanitizer v1.0 (Post-Burn Guard) ---")
    # Scan both yearly and monthly files
    files = sorted(glob.glob(os.path.join(DATA_DIR, "20*.json")))
    for f in files:
        sanitize_file(f)
