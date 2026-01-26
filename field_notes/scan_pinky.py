import requests
import json
import os
import glob
import re
import hashlib
import sys

# Add current directory to path to allow sibling import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_engine import get_engine

# Configuration
ENGINE = get_engine(mode="LOCAL")

# Inputs
RESUME_PATH = "raw_notes/Jason Allred Resume - Jan 2026.txt"
FOCAL_OLD = "raw_notes/Performance review 2008-2018 .txt"
FOCAL_NEW = "raw_notes/11066402 Insights 2019-2024.txt"
NOTES_GLOB = "raw_notes/notes_*.txt"
DATA_DIR = "field_notes/data"
STATE_FILE = os.path.join(DATA_DIR, "scan_state.json")
THEMES_FILE = os.path.join(DATA_DIR, "themes.json")
AUDIT_FILE = os.path.join(DATA_DIR, "privacy_audit.jsonl")

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return ""

def get_file_hash(path):
    content = read_file(path)
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def parse_notes_into_chunks(text):
    date_pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4})'
    chunks = []
    current_date = "Header/Unknown"
    current_content = []
    
    lines = text.splitlines()
    for line in lines:
        match = re.match(date_pattern, line.strip())
        if match:
            if current_content:
                chunks.append({"date": current_date, "content": "\n".join(current_content)})
            current_date = match.group(1)
            current_content = [line]
        else:
            current_content.append(line)
    if current_content:
        chunks.append({"date": current_date, "content": "\n".join(current_content)})
    return chunks

def ask_pinky(prompt, label=""):
    print(f"   > Pinky is thinking ({label})...")
    return ENGINE.generate(prompt)

def extract_json(text):
    match = re.search(r'\[.*\]', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except:
            pass
    # Fallback for list-like structure
    text = text.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(text)
    except:
        return []

def save_year_data(year, events):
    filepath = os.path.join(DATA_DIR, f"{year}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            existing = json.load(f)
    else:
        existing = []
    
    # Merge unique events (dedup by date+summary)
    seen = set([(e.get('date'), e.get('summary')) for e in existing])
    for event in events:
        if (event.get('date'), event.get('summary')) not in seen:
            existing.append(event)
            seen.add((event.get('date'), event.get('summary')))
    
    with open(filepath, 'w') as f:
        json.dump(existing, f, indent=2)

def main():
    print("--- Pinky Lazy-Data Scanner v4.0 ---")
    os.makedirs(DATA_DIR, exist_ok=True)
    
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
    else:
        state = {}

    resume = read_file(RESUME_PATH)
    focal_1 = read_file(FOCAL_OLD)
    focal_2 = read_file(FOCAL_NEW)
    strategic_context = f"[RESUME]\n{resume[:2000]}\n[FOCALS]\n{focal_1[:3000]}\n{focal_2[:3000]}"
    
    note_files = sorted(glob.glob(NOTES_GLOB))
    
    for note_file in note_files:
        filename = os.path.basename(note_file)
        file_hash = get_file_hash(note_file)
        
        if state.get(filename) == file_hash:
            print(f"Skipping {filename} (Already fully scanned).")
            continue

        print(f"\nScanning {filename}...")
        text = read_file(note_file)
        chunks = parse_notes_into_chunks(text)
        
        # Batch process chunks (grouping by 5 days for efficiency)
        batch_size = 5
        batch_limit = 2 # ONLY PROCESS 2 BATCHES FOR TESTING
        batches_processed = 0
        for i in range(0, len(chunks), batch_size):
            if batches_processed >= batch_limit: break
            batch = chunks[i:i+batch_size]
            batch_text = "\n\n---\n\n".join([f"DATE: {c['date']}\n{c['content']}" for c in batch])
            
            prompt = f"""
            [ROLE]
            You are 'Pinky', an expert technical archivist.

            [CONTEXT]
            {strategic_context}

            [TASK]
            Analyze these engineering notes. Extract key events.
            Classify sensitivity: "Public" (Resume safe) or "Sensitive" (PII, internal, personal).
            Normalize dates to YYYY-MM-DD.
            
            Return a JSON list:
            [
                {{ "date": "YYYY-MM-DD", "summary": "Technical win", "evidence": "Quote", "sensitivity": "Public", "tags": ["IPMI"] }},
                {{ "date": "YYYY-MM-DD", "summary": "Internal meeting", "evidence": "Quote", "sensitivity": "Sensitive", "tags": [] }}
            ]

            [NOTES]
            {batch_text}
            
            [OUTPUT]
            JSON list only.
            """
            
            result_text = ask_pinky(prompt, label=f"{filename} batch {i//batch_size + 1}")
            batches_processed += 1
            events = extract_json(result_text)
            
            if isinstance(events, list):
                year_buckets = {}
                for event in events:
                    if event.get("sensitivity") == "Public":
                        date_str = event.get("date", "Unknown")
                        year = date_str[:4] if re.match(r'\d{4}', date_str) else "Unknown"
                        if year not in year_buckets: year_buckets[year] = []
                        year_buckets[year].append(event)
                    else:
                        with open(AUDIT_FILE, "a") as f:
                            f.write(json.dumps(event) + "\n")
                
                for year, year_events in year_buckets.items():
                    save_year_data(year, year_events)

        state[filename] = file_hash
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)

    print("\n--- SCAN COMPLETE ---")

if __name__ == "__main__":
    main()