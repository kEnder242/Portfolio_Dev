import json
import os
import sys
import glob
import re
import time

# Add current directory to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
from ai_engine import get_engine
from utils import update_status, can_burn, RAW_NOTES_DIR, DATA_DIR

# Config
# Expanded glob to catch Insights, Philosophy, and Reviews using Absolute Paths from utils
NOTES_GLOB = os.path.join(RAW_NOTES_DIR, "**/*.txt")
DOCX_GLOB = os.path.join(RAW_NOTES_DIR, "**/*.docx")
RAS_GLOB = os.path.join(RAW_NOTES_DIR, "**/ras-*.txt")
MANIFEST_FILE = os.path.join(DATA_DIR, "file_manifest.json")
ENGINE = get_engine(mode="LOCAL")

def read_sample(path):
    """
    [VIBE-007] Journal-Aware Sampling.
    Bypasses head TODO noise by hunting for anchors or ASCII dividers.
    """
    try:
        if path.endswith('.docx'):
            import docx2txt
            text = docx2txt.process(path)
        else:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        
        lines = text.splitlines()
        if len(lines) < 100:
            return text
        
        # Hunt for the Journal Anchor [ctrl-F10 s] or ASCII dividers
        start_idx = 0
        for i, line in enumerate(lines[:500]): # Scan first 500 lines
            if "[ctrl-F10 s]" in line or "======" in line or "------" in line:
                start_idx = i
                break
        
        # If no anchor found, skip the first 100 lines of head noise
        if start_idx == 0:
            start_idx = 100

        header = "\n".join(lines[start_idx : start_idx + 100])
        middle = "\n".join(lines[len(lines)//2 : len(lines)//2 + 50])
        return f"[STARTING AT LINE {start_idx}]\n{header}\n\n[...]\n\n{middle}"
    except Exception as e:
        print(f"Error reading {path}: {e}")
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
    """
    Calls the AI Engine to classify the file.
    """
    prompt = f"""
    [TASK]
    Act as a digital librarian. Analyze this file sample (Header + Middle) and classify it.
    
    [FILENAME]
    {filename}
    
    [CONTENT SAMPLE]
    {text_sample[:2000]}
    
    [CATEGORIES]
    - LOG: Chronological technical notes, daily logs, error traces.
    - META: Resumes, performance reviews, philosophy, high-level insights.
    - REFERENCE: Technical manuals, specs, READMEs (static info).
    - UNKNOWN: None of the above.
    
    [OUTPUT FORMAT]
    JSON only:
    {{
      "type": "LOG|META|REFERENCE|UNKNOWN",
      "year": "YYYY or null",
      "topic": "Short 2-3 word topic",
      "confidence": 0.0 to 1.0
    }}
    """
    
    print(f"   > Librarian analyzing {filename}...")
    try:
        response = ENGINE.generate(prompt)
        return extract_json(response)
    except Exception as e:
        print(f"Error classifying {filename}: {e}")
        return {"type": "UNKNOWN", "note": str(e)}

def main():
    print("--- Pinky Librarian v1.4 (Archaeology Aware) ---")
    
    if os.path.exists(MANIFEST_FILE):
        with open(MANIFEST_FILE, 'r') as f:
            manifest = json.load(f)
    else:
        manifest = {}

    files = sorted(
        glob.glob(NOTES_GLOB, recursive=True) + 
        glob.glob(RAS_GLOB, recursive=True) +
        glob.glob(DOCX_GLOB, recursive=True)
    )
    
    # [VIBE-007] Archaeology Hints & Manual Overrides
    OVERRIDES = {
        "notes_2024_PIAV.txt": {"type": "LOG", "year": "2019-2024", "tags": ["PIAV", "Manageability"]},
        "notes_2018_PAE.txt": {"type": "LOG", "year": "2016-2019", "tags": ["PAE", "AEP", "Optane"]},
        "notes_2016_MVE.txt": {"type": "LOG", "year": "2016", "tags": ["MVE", "Graphics"]},
        "notes_2015_DSD.txt": {"type": "LOG", "year": "2011-2016", "tags": ["DSD", "VISA", "Post-Silicon Debug"]},
        "notes_2006_EPSD.txt": {"type": "LOG", "year": "2005-2007", "tags": ["EPSD", "Internship"]},
        "notes_2005.txt": {"type": "LOG", "year": "2005", "tags": ["EPSD"]},
        "11066402 Insights 2019-2024.txt": {"type": "META", "year": "2019-2024"},
        "Performance_Review_2008-2018.txt": {"type": "META", "year": "2008-2018"},
        "notes_GIT.txt": {"type": "REFERENCE", "note": "Not a log"},
        "ras-viral.txt": {"type": "LOG", "year": "2018-2019", "topic": "RAS / Viral Errors"},
        "ras-einj.txt": {"type": "LOG", "year": "2018", "topic": "RAS / EINJ"}
    }
    
    # Team Anchors Heuristic
    TEAM_TAGS = {"PIAV": "2019-2024", "PAE": "2016-2019", "MVE": "2016", "DSD": "2011-2016", "EPSD": "2005-2007"}

    for filepath in files:
        filename = os.path.basename(filepath)

        # Skip already classified or excluded
        if filename in manifest and filename not in OVERRIDES:
            continue

        # --- POLITENESS CHECK ---
        while True:
            ready, reason = can_burn()
            if ready: break
            update_status("YIELD", f"Librarian Yielding: {reason}", filename=filename)
            time.sleep(10)
        
        # 1. Check Overrides (Explicit Truth)
        if filename in OVERRIDES:
            print(f"   --> {filename}: {OVERRIDES[filename]['type']} (Manual Override)")
            manifest[filename] = OVERRIDES[filename]
            continue

        # 2. Check Team Anchors (Heuristic Hint)
        found_tag = next((tag for tag in TEAM_TAGS if tag in filename), None)
        
        text_sample = read_sample(filepath)
        if not text_sample:
            continue
            
        info = classify_file(filename, text_sample)
        
        # Apply team tag context if found
        if found_tag:
            info["year"] = info.get("year") or TEAM_TAGS[found_tag]
            info["tags"] = list(set(info.get("tags", []) + [found_tag]))

        # Fallback if AI fails
        if not info or "type" not in info:
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
