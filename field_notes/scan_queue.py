import os
import glob
import re
import json
import hashlib
import sys

# Config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Absolute GLOB paths
NOTES_GLOB = os.path.join(os.path.dirname(BASE_DIR), "raw_notes/**/*.txt")
DOCX_GLOB = os.path.join(os.path.dirname(BASE_DIR), "raw_notes/**/*.docx")
RAS_GLOB = os.path.join(os.path.dirname(BASE_DIR), "raw_notes/**/ras-*.txt")

DATA_DIR = os.path.join(BASE_DIR, "data")
QUEUE_FILE = os.path.join(DATA_DIR, "queue.json")
STATE_FILE = os.path.join(DATA_DIR, "chunk_state.json")
MANIFEST_FILE = os.path.join(DATA_DIR, "file_manifest.json")

def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)

def read_file(path):
    try:
        if path.endswith('.docx'):
            import docx2txt
            return docx2txt.process(path)
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return ""

def get_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def parse_chunks(text, filename, file_type="LOG", fallback_year=None):
    """
    Parses text into Month or Year buckets. 
    Returns dict: {'YYYY-MM': 'content...'} or {'YYYY': 'content...'}
    """
    if file_type == "META":
        # Meta documents are processed as a single chunk for the year
        year = fallback_year or "Unknown"
        return {str(year): text}

    date_pattern = r'^(\d{1,2})/(\d{1,2})/(\d{2,4})'
    chunks = {}
    
    # [VIBE-007] Use manifest year as absolute fallback for archeology
    current_bucket = fallback_year or "Unknown"
    current_lines = []

    for line in text.splitlines():
        match = re.match(date_pattern, line.strip())
        if match:
            # New date found, determine bucket
            month, day, year = match.groups()
            if len(year) == 2: year = "20" + year # Assume 20xx
            
            # Pad month
            month = month.zfill(2)
            new_bucket = f"{year}-{month}"
            
            # Flush previous bucket if content exists
            if current_lines:
                if current_bucket not in chunks: chunks[current_bucket] = []
                chunks[current_bucket].append("\n".join(current_lines))
            
            current_bucket = new_bucket
            current_lines = [line]
        else:
            current_lines.append(line)
            
    # Flush final
    if current_lines:
        if current_bucket not in chunks: chunks[current_bucket] = []
        chunks[current_bucket].append("\n".join(current_lines))
        
    # Join lists into single strings
    return {k: "\n".join(v) for k, v in chunks.items()}

def main():
    print("--- Scan Queue Manager v2.1 (Hardened & Meta-Aware) ---")
    ensure_dirs()
    
    # Load Manifest
    if os.path.exists(MANIFEST_FILE):
        with open(MANIFEST_FILE, 'r') as f:
            manifest = json.load(f)
    else:
        print("Warning: No manifest found. Run scan_librarian.py first.")
        manifest = {}

    # Load State
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
    else:
        state = {}
        
    # Load Existing Queue
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, 'r') as f:
            try:
                queue = json.load(f)
            except: queue = []
    else:
        queue = []

    files = sorted(
        glob.glob(NOTES_GLOB, recursive=True) + 
        glob.glob(RAS_GLOB, recursive=True) +
        glob.glob(DOCX_GLOB, recursive=True)
    )
    tasks_added = 0
    
    for filepath in files:
        filename = os.path.basename(filepath)
        
        # Classification Logic
        info = manifest.get(filename, {})
        file_type = info.get("type", "UNKNOWN")
        year_guess = info.get("year")
        
        # Rule: Process if it's a LOG or a META document
        should_process = (file_type in ["LOG", "META"])
        
        # Fallback heuristic for un-manifested notes
        if not should_process and "notes_" in filename and "GIT" not in filename:
            should_process = True
            file_type = "LOG"
        
        if not should_process:
            continue

        text = read_file(filepath)
        if not text: continue
        
        # Chunking
        chunks = parse_chunks(text, filename, file_type=file_type, fallback_year=year_guess)
        
        for bucket_id, content in chunks.items():
            content_hash = get_hash(content)
            chunk_id = f"{filename}::{bucket_id}"
            
            # Logic: Is this chunk NEW or CHANGED?
            if state.get(chunk_id) != content_hash:
                # Add to queue
                task = {
                    "id": chunk_id,
                    "filename": filename,
                    "bucket": bucket_id,
                    "type": file_type, 
                    "priority": 10 if file_type == "LOG" else 20, # Prioritize strategy
                    "content": content
                }
                
                # Deduplicate queue
                if not any(t['id'] == chunk_id for t in queue):
                    queue.append(task)
                    tasks_added += 1
                    print(f"Queueing {chunk_id} ({file_type})")
            
    # Sort queue by priority DESC
    queue.sort(key=lambda x: x.get('priority', 10), reverse=True)
    
    with open(QUEUE_FILE, 'w') as f:
        json.dump(queue, f, indent=2)
        
    print(f"\nQueue Updated. {tasks_added} new tasks. Total Pending: {len(queue)}")

if __name__ == "__main__":
    main()
