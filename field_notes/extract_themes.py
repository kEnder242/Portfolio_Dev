import json
import os
import glob

DATA_DIR = "field_notes/data"
OUTPUT_FILE = os.path.join(DATA_DIR, "themes.json")
MONOLITH_FILE = "field_notes/pinky_index_full.json"

def extract_themes():
    # 1. Get strategic themes from monolith if available
    themes = {}
    if os.path.exists(MONOLITH_FILE):
        with open(MONOLITH_FILE, 'r') as f:
            monolith = json.load(f)
            for year, content in monolith.items():
                if year == "Unknown": continue
                themes[year] = {
                    "strategic_theme": content.get("strategic_theme", "No strategic theme defined."),
                    "technical_tags": content.get("technical_tags", [])
                }

    # 2. Check for granular data files to ensure all years are represented
    data_files = glob.glob(os.path.join(DATA_DIR, "*.json"))
    for df in data_files:
        filename = os.path.basename(df)
        if filename == "themes.json" or filename == "scan_state.json": continue
        
        year = filename.replace(".json", "")
        if year not in themes:
            themes[year] = {
                "strategic_theme": "Historical archive data (Strategy scan pending).",
                "technical_tags": []
            }

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(themes, f, indent=2)
    
    print(f"Themes skeleton updated in {OUTPUT_FILE}")

if __name__ == "__main__":
    extract_themes()