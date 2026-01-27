import json
import glob
import os
import re

DATA_DIR = "field_notes/data"

def clean_data():
    print("--- Data Janitor v2.0 (Polite) ---")
    files = glob.glob(os.path.join(DATA_DIR, "*.json"))
    
    total_fixed = 0
    
    for filepath in files:
        filename = os.path.basename(filepath)
        if filename in ["themes.json", "queue.json", "status.json", "scan_state.json", "chunk_state.json"]:
            continue
            
        # Infer year from filename (e.g. 2024.json or 2024_01.json)
        file_year = "Unknown"
        match_year = re.match(r'(\d{4})', filename)
        if match_year:
            file_year = match_year.group(1)

        with open(filepath, 'r') as f:
            try:
                data = json.load(f)
            except:
                continue
                
        if not isinstance(data, list): continue
        
        valid_events = []
        modified = False
        
        for event in data:
            date = event.get("date", "")
            summary = event.get("summary", "")
            
            # Check for "invalid date" strings or None
            if not date or "invalid" in str(date).lower() or "unknown" in str(date).lower():
                # It's an Insight or General Log
                # Try to rescue it?
                # If summary looks like "Q3 Goals", set date to YYYY-07-01?
                # For now, just set it to a clean "Season" marker
                
                if file_year != "Unknown":
                    # Put it at the beginning of the year/file
                    event["date"] = f"{file_year}-01-01" 
                    # Add a tag to display differently? 
                    # We can prepend to summary: "[Strategic Context] ..."
                    if not summary.startswith("["):
                        event["summary"] = f"[Strategic Context] {summary}"
                else:
                    event["date"] = "1970-01-01" # Bottom of the pile
                    
                modified = True
                total_fixed += 1
            
            # Check for "Month Names" (e.g. "October")
            elif re.match(r'^[A-Z][a-z]+$', date):
                # "October"
                try:
                    m_idx = time.strptime(date[:3], '%b').tm_mon
                    event["date"] = f"{file_year}-{m_idx:02d}-01"
                    modified = True
                    total_fixed += 1
                except:
                    pass

            valid_events.append(event)
                
        if modified:
            # Sort again
            valid_events.sort(key=lambda x: x.get('date', ''))
            with open(filepath, 'w') as f:
                json.dump(valid_events, f, indent=2)
                
    print(f"Cleanup Complete. Polished: {total_fixed}")

import time
if __name__ == "__main__":
    clean_data()
