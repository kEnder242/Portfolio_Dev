import requests
import json
import os
import glob
import re
import hashlib
import sys
import random

# Add current directory to path to allow sibling import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_engine import get_engine

# Configuration
ENGINE = get_engine(mode="LOCAL")

# Inputs
RESUME_PATH = "raw_notes/Jason Allred Resume - Jan 2026.txt"
FOCAL_OLD = "raw_notes/Performance review 2008-2018 .txt"
FOCAL_NEW = "raw_notes/11066402 Insights 2019-2024.txt"
NOTES_GLOB = "raw_notes/**/notes_*.txt"
RAS_GLOB = "raw_notes/**/ras-*.txt"
GAP_FILES = [
    "raw_notes/Performance review 2008-2018 .txt",
    "raw_notes/notes_2006_EPSD.txt",
    "raw_notes/notes_2005.txt"
]

DATA_DIR = "field_notes/data"
STATE_FILE = os.path.join(DATA_DIR, "scan_state.json")
THEMES_FILE = os.path.join(DATA_DIR, "themes.json")
AUDIT_FILE = os.path.join(DATA_DIR, "privacy_audit.jsonl")

# Limits
SLOW_BURN_BATCH_LIMIT = 2  # Total batches to process in a background run
FAST_BURN_BATCH_LIMIT = 1  # Batches to process when targeting a file
RE_SCAN_CHANCE = 0.1       # 10% chance to re-scan an old file for new insights

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

def parse_gap_notes(text):
    """Loose chunking for files without strict timestamp structure."""
    chunks = []
    current_chunk = []
    current_len = 0
    
    # Split by double newlines (paragraphs) to preserve some structure
    paragraphs = text.split('\n\n')
    
    for p in paragraphs:
        p = p.strip()
        if not p: continue
        
        # 3000 chars is a good chunk size for LLM context
        if current_len + len(p) > 3000: 
            chunks.append({"date": "Gap/Context", "content": "\n\n".join(current_chunk)})
            current_chunk = []
            current_len = 0
            
        current_chunk.append(p)
        current_len += len(p)
        
    if current_chunk:
        chunks.append({"date": "Gap/Context", "content": "\n\n".join(current_chunk)})
    return chunks

def parse_notes_into_chunks(text, filename=""):
    # Check if this is a "Gap" file requiring special handling
    is_gap = False
    for gap_file in GAP_FILES:
        if os.path.basename(gap_file) == filename:
            is_gap = True
            break
    
    # Also catch notes_2005/2006 if passed via glob but not in GAP_FILES list explicitly matched by basename
    if "notes_2005" in filename or "notes_2006" in filename:
        is_gap = True

    if is_gap:
        return parse_gap_notes(text)

    # Standard Strict Logic (Start of line date)
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
    print("--- Pinky Lazy-Data Scanner v4.2 (Smart Slow Burn) ---")
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
    
    # Gather all files
    all_files = set(glob.glob(NOTES_GLOB, recursive=True))
    all_files.update(glob.glob(RAS_GLOB, recursive=True))
    for gf in GAP_FILES:
        if os.path.exists(gf):
            all_files.add(gf)
            
    # CLI Filter
    target_filter = sys.argv[1] if len(sys.argv) > 1 else None
    
    note_files = sorted(list(all_files))
    batches_processed_total = 0
    
    # In Slow Burn mode, shuffle files to find work randomly
    if not target_filter:
        import random
        random.shuffle(note_files)

    for note_file in note_files:
        # Check global limit for Slow Burn
        if not target_filter and batches_processed_total >= SLOW_BURN_BATCH_LIMIT:
            print(f"\n[Slow Burn] Global batch limit ({SLOW_BURN_BATCH_LIMIT}) reached. Exiting.")
            break

        filename = os.path.basename(note_file)
        
        # Filter logic
        if target_filter and target_filter not in filename:
            continue
            
        file_hash = get_file_hash(note_file)
        
        # Determine if we should scan
        should_scan = False
        is_gap_file = any(os.path.basename(g) == filename for g in GAP_FILES) or "notes_2005" in filename or "notes_2006" in filename
        
        # 1. New or Changed File
        if state.get(filename) != file_hash:
            should_scan = True
            print(f"Scanning {filename} (New/Modified)...")
            
        # 2. Targeted File (Fast Burn)
        elif target_filter:
            should_scan = True
            print(f"Scanning {filename} (Targeted)...")
            
        # 3. Gap File (Always prioritize slightly higher in logic, but subject to chance if unchanged)
        elif is_gap_file and random.random() < (RE_SCAN_CHANCE * 2): # Double chance for gap files
             should_scan = True
             print(f"Scanning {filename} (Gap Re-Scan)...")

        # 4. Random Re-Scan (Refining Insights)
        elif random.random() < RE_SCAN_CHANCE:
            should_scan = True
            print(f"Scanning {filename} (Random Re-Scan)...")
        
        if not should_scan:
            continue

        text = read_file(note_file)
        chunks = parse_notes_into_chunks(text, filename)
        
        # If Re-Scanning, pick a RANDOM chunk instead of the first one
        start_index = 0
        if state.get(filename) == file_hash and not target_filter:
             if len(chunks) > 5:
                start_index = random.randint(0, len(chunks) - 5)
                print(f"   > Randomly starting at chunk {start_index}...")

        # Process chunks
        batch_size = 5
        
        # Determine Limit for THIS file
        if target_filter:
            file_limit = FAST_BURN_BATCH_LIMIT
        else:
            # In slow burn, we only do 1 batch per file to spread the love
            file_limit = 1
        
        chunks_subset = chunks[start_index:]
        
        for i in range(0, len(chunks_subset), batch_size):
            if i // batch_size >= file_limit:
                print(f"   > File limit ({file_limit} batch) reached.")
                break
                
            # Check global limit again inside loop
            if not target_filter and batches_processed_total >= SLOW_BURN_BATCH_LIMIT:
                break

            batch = chunks_subset[i:i+batch_size]
            
            # Contextual prompt for Gap files
            date_instruction = "Normalize dates to YYYY-MM-DD."
            if is_gap_file:
                date_instruction += " **CRITICAL:** These notes lack strict timestamps. You MUST infer the date from context. Date format is usually Month/Day/Year (MM/DD/YY). Use 'YYYY-01-01' if only year is known."

            batch_text = "\n\n---\n\n".join([f"DATE: {c['date']}\n{c['content']}" for c in batch])
            
            prompt = f"""
            [ROLE]
            You are 'Pinky', an expert technical archivist.

            [CONTEXT]
            {strategic_context}

            [TASK]
            Analyze these engineering notes. Extract key events.
            Classify sensitivity: \"Public\" (Resume safe) or \"Sensitive\" (PII, internal, personal).
            {date_instruction}
            
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
            
            try:
                result_text = ask_pinky(prompt, label=f"{filename} batch")
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
                        
                batches_processed_total += 1
                
            except Exception as e:
                print(f"Error processing batch: {e}")

        # Update state only if we started from 0 (full scan) 
        # OR if we want to mark it "touched" - but for re-scans we might not want to update hash 
        # to ensure it stays in the rotation? 
        # Actually, let's always update hash if we scanned *at all* to prove file is accessible,
        # but since we are doing random re-scans, the state check will just fail next time and rely on RNG.
        # So updating state is fine.
        state[filename] = file_hash
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)

    print(f"\n--- SCAN COMPLETE (Processed {batches_processed_total} batches) ---")

if __name__ == "__main__":
    main()