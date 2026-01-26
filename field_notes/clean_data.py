import json
import glob
import os
import re

DATA_DIR = "field_notes/data"

def clean_data():
    print("--- Data Janitor v1.0 ---")
    files = glob.glob(os.path.join(DATA_DIR, "*.json"))
    
    total_fixed = 0
    total_removed = 0
    
    for filepath in files:
        filename = os.path.basename(filepath)
        if filename in ["themes.json", "queue.json", "status.json", "scan_state.json", "chunk_state.json"]:
            continue
            
        with open(filepath, 'r') as f:
            try:
                data = json.load(f)
            except:
                print(f"Skipping corrupt file: {filename}")
                continue
                
        if not isinstance(data, list): continue
        
        valid_events = []
        modified = False
        
        for event in data:
            date = event.get("date", "")
            
            # Fix: "invalid date_" prefix? User said "invalid date_ items".
            # Fix: regex format YYYY-MM-DD
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
                # Attempt repair
                # 7/22/2016 -> 2016-07-22
                match_slash = re.match(r'(\d{1,2})/(\d{1,2})/(\d{4})', date)
                if match_slash:
                    m, d, y = match_slash.groups()
                    new_date = f"{y}-{m.zfill(2)}-{d.zfill(2)}"
                    event["date"] = new_date
                    valid_events.append(event)
                    modified = True
                    total_fixed += 1
                else:
                    # Garbage date?
                    # Check if it's "2016-07" (Month only)
                    if re.match(r'^\d{4}-\d{2}$', date):
                        event["date"] = f"{date}-01" # Default to 1st
                        valid_events.append(event)
                        modified = True
                        total_fixed += 1
                    else:
                        print(f"Removing invalid date in {filename}: {date}")
                        total_removed += 1
            else:
                valid_events.append(event)
                
        if modified or len(valid_events) < len(data):
            # Sort again
            valid_events.sort(key=lambda x: x.get('date', ''))
            with open(filepath, 'w') as f:
                json.dump(valid_events, f, indent=2)
                
    print(f"Cleanup Complete. Fixed: {total_fixed}, Removed: {total_removed}")

if __name__ == "__main__":
    clean_data()
