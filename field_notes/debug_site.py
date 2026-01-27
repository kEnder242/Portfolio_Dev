import os
import json
import re

DATA_DIR = "field_notes/data"
HTML_FILE = "field_notes/timeline.html"

def check_file(path):
    if os.path.exists(path):
        print(f"[OK] Found {path}")
        return True
    else:
        print(f"[FAIL] Missing {path}")
        return False

def check_json(path):
    if not check_file(path): return False
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        count = len(data) if isinstance(data, (dict, list)) else 0
        print(f"   -> Valid JSON. Items: {count}")
        return True
    except json.JSONDecodeError as e:
        print(f"   -> [FAIL] Invalid JSON: {e}")
        return False

def main():
    print("--- SITE DIAGNOSTIC HARNESS ---")
    
    # 1. Check HTML
    if check_file(HTML_FILE):
        with open(HTML_FILE, 'r') as f:
            html = f.read()
        
        # Check Cache Busters
        css_match = re.search(r'style.css\?v=([0-9.]+)', html)
        if css_match:
            print(f"   -> CSS Version: {css_match.group(1)}")
        else:
            print("   -> [WARN] No CSS cache buster found.")
            
        js_match = re.search(r'themes.json\?t=', html)
        if js_match:
            print(f"   -> JS Cache Buster: Present")
        else:
            print("   -> [WARN] No JS cache buster found.")

    # 2. Check Skeleton
    print("\nChecking Themes:")
    if check_json(os.path.join(DATA_DIR, "themes.json")):
        with open(os.path.join(DATA_DIR, "themes.json"), 'r') as f:
            themes = json.load(f)
            years = list(themes.keys())
            print(f"   -> Years in Theme: {years}")
            
            # 3. Check Granular Data
            for year in years:
                json_path = os.path.join(DATA_DIR, f"{year}.json")
                if not check_json(json_path):
                    print(f"      [WARN] Data missing for {year}")

    print("\n--- DIAGNOSTIC COMPLETE ---")

if __name__ == "__main__":
    main()
