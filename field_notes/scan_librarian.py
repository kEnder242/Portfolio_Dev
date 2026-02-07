import json
import os
import sys
import glob
import re

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ai_engine import get_engine
from utils import update_status

# Config
NOTES_GLOB = "raw_notes/**/notes_*.txt"
RAS_GLOB = "raw_notes/**/ras-*.txt"
MANIFEST_FILE = "field_notes/data/file_manifest.json"
ENGINE = get_engine(mode="LOCAL")

def read_sample(path):
    """Read header and a chunk from the middle to catch logs behind backlogs."""
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            header = f.read(2000)
            f.seek(0, 2) # End
            size = f.tell()
            mid_point = max(0, size // 2 - 1000)
            f.seek(mid_point)
            middle = f.read(2000)
            return header + "\n\n...[SKIP]...\n\n" + middle
    except Exception:
        return ""

def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except:
            pass
    try:
        return json.loads(text.replace("```json", "").replace("```", "").strip())
    except:
        return {}

def classify_file(filename, text_sample):
    # Heuristic: Check for dates
    has_dates = bool(re.search(r'\d{1,2}/\d{1,2}/\d{2,4}', text_sample))
    date_hint = "Contains chronological date entries." if has_dates else "No obvious dates found."

    prompt = f"""
    [TASK]
    Act as a digital librarian. Analyze this file sample (Header + Middle) and classify it.
    
    [FILENAME]
    {filename}
    
    [HINT]
    {date_hint}
    
    [TEXT SAMPLE]
    {text_sample[:4000]}
    
    [CATEGORIES]
    - LOG: A chronological engineering journal. (MUST contain dates).
    - REFERENCE: A cheat sheet, config file, how-to guide, or topic dump.
    - META: Personal career docs, resumes, performance reviews.
    
    [OUTPUT]
    Return a JSON object:
    {{
      "type": "LOG" | "REFERENCE" | "META",
      "year": "YYYY" (Best guess for LOG, or null),
      "topic": "Short 2-3 word topic if REFERENCE",
      "confidence": 0.0 to 1.0
    }}
    """
    
    print(f"   > Librarian analyzing {filename}...")
    response = ENGINE.generate(prompt)
    return extract_json(response)

def main():
    print("--- Pinky Librarian v1.2 ---")
    
    # Force overrides for known tricky files
    OVERRIDES = {
        "notes_2024_PIAV.txt": "LOG",
        "Performance review 2008-2018 .txt": "META",
        "11066402 Insights 2019-2024.txt": "META",
        "ras-viral.txt": "LOG",
        "ras-einj.txt": "LOG"
    }
    
    manifest = {}
    files = sorted(glob.glob(NOTES_GLOB, recursive=True) + glob.glob(RAS_GLOB, recursive=True))
    
    for filepath in files:
        filename = os.path.basename(filepath)
        
        if filename in OVERRIDES:
            print(f"   --> {filename}: {OVERRIDES[filename]} (Manual Override)")
            manifest[filename] = {"type": OVERRIDES[filename], "note": "Manual Override"}
            continue

        text_sample = read_sample(filepath)
        
        info = classify_file(filename, text_sample)
        
        # Fallback if Pinky fails
        if not info or "type" not in info:
            # Fallback to filename heuristic
            if "notes_" in filename and any(char.isdigit() for char in filename):
                 info = {"type": "LOG", "year": filename[6:10], "note": "Fallback heuristic"}
            else:
                 info = {"type": "UNKNOWN", "manual_review": True}
            
        manifest[filename] = info
        print(f"   --> {filename}: {info.get('type')} ({info.get('year') or info.get('topic')})")
        update_status("ONLINE", f"Classifying file: {filename}", filename=filename)

    # Save Manifest
    with open(MANIFEST_FILE, 'w') as f:
        json.dump(manifest, f, indent=2)
        
    print(f"\nManifest saved to {MANIFEST_FILE}")

if __name__ == "__main__":
    main()
