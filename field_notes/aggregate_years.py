import json
import os
import glob
import logging
import re

# Config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MANIFEST_FILE = os.path.join(DATA_DIR, "file_manifest.json")
logging.basicConfig(level=logging.INFO, format='[AGGREGATE] %(message)s')

def get_year_range(year_str):
    """Parses 'YYYY', 'YYYY-YYYY', or 'YYYY_MM' into a list of years."""
    if not year_str: return []
    # Normalize separators
    year_str = year_str.replace('_', '-').replace(' ', '-')
    
    # Handle YYYY-YYYY
    range_match = re.match(r'(\d{4})-(\d{4})', year_str)
    if range_match:
        start, end = map(int, range_match.groups())
        return [str(y) for y in range(start, end + 1)]
    
    # Handle YYYY-MM or YYYY
    year_match = re.match(r'^(\d{4})', year_str)
    if year_match:
        return [year_match.group(1)]
        
    return []

def aggregate_years():
    logging.info("--- Consolidating Logs into Yearly Summaries [v2.4] ---")
    
    # 1. Load Manifest
    manifest = {}
    if os.path.exists(MANIFEST_FILE):
        try:
            with open(MANIFEST_FILE, 'r') as f:
                manifest = json.load(f)
        except: pass

    # 2. Find all processed JSON files
    all_json = glob.glob(os.path.join(DATA_DIR, "*.json"))
    process_targets = []
    for f in all_json:
        fname = os.path.basename(f)
        if re.match(r'^\d{4}\.json$', fname): continue
        if any(x in fname for x in ["status", "themes", "queue", "state", "search_index", "manifest", "activity"]): continue
        process_targets.append(f)

    # 3. Map events to target years
    yearly_buckets = {}

    for fpath in process_targets:
        try:
            with open(fpath, 'r') as f:
                data = json.load(f)
                if not isinstance(data, list): continue
                
                fname_base = os.path.splitext(os.path.basename(fpath))[0]
                
                # Logic: Determine target years
                target_years = []
                
                # A. Check filename for range (e.g. 2008_2018)
                target_years = get_year_range(fname_base)
                
                # B. If not in filename, try manifest lookup
                if not target_years:
                    fname_norm = fname_base.replace(' ', '_').lower()
                    for mf, info in manifest.items():
                        mf_norm = os.path.splitext(mf)[0].replace(' ', '_').lower()
                        if mf_norm == fname_norm or mf_norm in fname_norm or fname_norm in mf_norm:
                            target_years = get_year_range(info.get('year', ''))
                            if target_years: break
                
                if not target_years:
                    target_years = ["Unknown"]

                logging.info(f"   [DISTRIBUTE] {os.path.basename(fpath)} -> {target_years}")

                for year in target_years:
                    if year == "Unknown": continue
                    if year not in yearly_buckets: yearly_buckets[year] = []
                    
                    for event in data:
                        new_event = event.copy()
                        # Sanity: Does the event actually belong in this year?
                        # If the event has a specific date, we honor it. 
                        # If it's a range date (e.g. "Oct 2007 - Dec 2007") and we are distributing to 2012, 
                        # that is a mismatch.
                        
                        raw_date = str(new_event.get('date', ''))
                        
                        # Extract year from event date if possible
                        event_year_match = re.search(r'(\d{4})', raw_date)
                        if event_year_match:
                            event_year = event_year_match.group(1)
                            # If event year is known and doesn't match target year, skip distribution
                            # EXCEPT for anchors which we pin to the start of every year in the range
                            if event_year != year and "[STRATEGIC_ANCHOR]" not in str(new_event.get('summary', '')):
                                continue

                        # Pin anchors and fuzzy dates to the target year
                        if "[STRATEGIC_ANCHOR]" in str(new_event.get('summary', '')) or not event_year_match:
                            new_event['date'] = f"{year}-01-01"
                        
                        yearly_buckets[year].append(new_event)
                    
        except Exception as e:
            logging.error(f"Error reading {fpath}: {e}")

    # 4. Final Consolidation
    for year, new_events in yearly_buckets.items():
        if year == "Unknown": continue
        
        logging.info(f"Processing Year: {year}")
        yearly_file = os.path.join(DATA_DIR, f"{year}.json")
        existing_events = []
        if os.path.exists(yearly_file):
            try:
                with open(yearly_file, 'r') as f:
                    existing_events = json.load(f)
            except: pass

        seen = set()
        final_events = []
        
        def get_fingerprint(item):
            d = str(item.get('date', 'Unknown'))
            s = item.get('summary', '')
            if isinstance(s, list): s = " ".join(s)
            s = s.strip().lower().rstrip('.')
            return f"{d}|{s}"

        for item in existing_events:
            # Cleanup: Remove leaked 2007 data from 2024 tree
            if year == "2024" and "2007" in str(item.get('date', '')) or "2007" in str(item.get('summary', '')):
                continue
            
            fp = get_fingerprint(item)
            if fp not in seen:
                final_events.append(item)
                seen.add(fp)
                
        for item in new_events:
            fp = get_fingerprint(item)
            if fp not in seen:
                final_events.append(item)
                seen.add(fp)
        
        # 5. Strategic Sort & Pinning
        def sort_key(x):
            summary = str(x.get('summary', ''))
            is_anchor = 0 if "[STRATEGIC_ANCHOR]" in summary else 1
            date = str(x.get('date', '9999-99-99'))
            return (is_anchor, date)

        final_events.sort(key=sort_key)
        
        with open(yearly_file + ".tmp", 'w') as f:
            json.dump(final_events, f, indent=2)
        os.replace(yearly_file + ".tmp", yearly_file)
        logging.info(f"   > Updated {year}.json with {len(final_events)} total events.")

    logging.info("--- Aggregation Complete ---")

if __name__ == "__main__":
    aggregate_years()
