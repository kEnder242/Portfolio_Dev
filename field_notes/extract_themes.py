import json
import os
import glob

DATA_DIR = "field_notes/data"
OUTPUT_FILE = os.path.join(DATA_DIR, "themes.json")
MONOLITH_FILE = "field_notes/pinky_index_full.json"

def extract_themes():
    themes = {}
    
    # 1. Load Strategic Descriptions from Monolith (Source of Truth for Text)
    monolith_themes = {}
    if os.path.exists(MONOLITH_FILE):
        with open(MONOLITH_FILE, 'r') as f:
            monolith = json.load(f)
            for year, content in monolith.items():
                monolith_themes[year] = content.get("strategic_theme", "Historical data.")

    # 2. Scan Granular Data to find ALL active years (Source of Truth for Time)
    # We look for YYYY.json files (Aggregates)
    data_files = glob.glob(os.path.join(DATA_DIR, "????.json"))
    
    for df in data_files:
        filename = os.path.basename(df)
        year = filename.replace(".json", "")
        
        # Get description from monolith (matching filename year usually)
        # But wait, if we have 2015.json built from notes_2016.txt, the monolith might have "2015" key?
        # Yes, pinky_index_full had keys by file-year.
        # So we try to find the best match.
        
        desc = monolith_themes.get(year, "Tactical archive active.")
        
        themes[year] = {
            "strategic_theme": desc,
            "technical_tags": [] # Tags are dynamically loaded now
        }

    # 3. Sort and Save
    # Convert to sorted dict? No, JSON keys are unordered technically, but we save for humans.
    # The frontend sorts anyway.
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(themes, f, indent=2)
    
    print(f"Themes skeleton updated in {OUTPUT_FILE} (Found {len(themes)} years)")

if __name__ == "__main__":
    extract_themes()