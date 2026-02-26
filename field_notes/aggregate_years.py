import json
import os
import glob
import logging
import re

# Config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
logging.basicConfig(level=logging.INFO, format='[AGGREGATE] %(message)s')

def aggregate_years():
    logging.info("--- Consolidating Monthly Logs into Yearly Summaries ---")
    
    # 1. Find all monthly files (YYYY_MM.json)
    monthly_files = glob.glob(os.path.join(DATA_DIR, "[0-9][0-9][0-9][0-9]_[0-9][0-9].json"))
    
    # 2. Group by year
    year_map = {}
    for mf in monthly_files:
        filename = os.path.basename(mf)
        year = filename[:4]
        if year not in year_map:
            year_map[year] = []
        year_map[year].append(mf)
    
    # 3. Process each year
    for year, files in year_map.items():
        logging.info(f"Processing Year: {year} ({len(files)} months)")
        all_events = []
        
        # Load all monthly events
        for fpath in files:
            try:
                with open(fpath, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        all_events.extend(data)
            except Exception as e:
                logging.error(f"Error reading {fpath}: {e}")
        
        if not all_events:
            continue
            
        # 4. Merge with existing YYYY.json (to preserve scan_pinky artifacts or manual edits)
        yearly_file = os.path.join(DATA_DIR, f"{year}.json")
        existing_events = []
        if os.path.exists(yearly_file):
            try:
                with open(yearly_file, 'r') as f:
                    existing_events = json.load(f)
            except: pass
            
        # 5. De-duplicate based on date + summary + evidence fingerprint
        seen = set()
        final_events = []
        
        def get_fingerprint(item):
            d = item.get('date', 'Unknown')
            s = item.get('summary', '')
            if isinstance(s, list): s = " ".join(s)
            s = s.strip().lower().rstrip('.')
            
            e = item.get('evidence', '')
            if isinstance(e, list): e = " ".join(e)
            e = e.strip().lower().rstrip('.')
            return f"{d}|{s}|{e[:50]}"

        # Prioritize existing (manual/pinky) events
        for item in existing_events:
            fp = get_fingerprint(item)
            if fp not in seen:
                final_events.append(item)
                seen.add(fp)
                
        # Add new (nibbled) events
        for item in all_events:
            fp = get_fingerprint(item)
            if fp not in seen:
                final_events.append(item)
                seen.add(fp)
        
        # 6. Sort and Save
        final_events.sort(key=lambda x: x.get('date', ''))
        
        # Atomic Write
        temp_file = yearly_file + ".tmp"
        with open(temp_file, 'w') as f:
            json.dump(final_events, f, indent=2)
        os.replace(temp_file, yearly_file)
        logging.info(f"   > Updated {year}.json with {len(final_events)} total events.")

    logging.info("--- Aggregation Complete ---")

if __name__ == "__main__":
    aggregate_years()
