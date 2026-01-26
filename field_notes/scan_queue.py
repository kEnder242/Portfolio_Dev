import os
import glob
import re
import json
import hashlib

# Config
NOTES_GLOB = "raw_notes/notes_*.txt"
DATA_DIR = "field_notes/data"
QUEUE_FILE = os.path.join(DATA_DIR, "queue.json")
STATE_FILE = os.path.join(DATA_DIR, "chunk_state.json")

def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        return ""

def get_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def parse_chunks(text, filename):
    """
    Parses text into Month buckets. 
    Returns dict: {'YYYY-MM': 'content...'}
    """
    date_pattern = r'^(\d{1,2})/(\d{1,2})/(\d{2,4})'
    chunks = {}
    current_bucket = "Unknown"
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
    print("--- Scan Queue Manager v1.0 ---")
    ensure_dirs()
    
    # Load State
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
    else:
        state = {}
        
    # Load Existing Queue
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, 'r') as f:
            queue = json.load(f)
    else:
        queue = []

    files = sorted(glob.glob(NOTES_GLOB))
    tasks_added = 0
    
    for filepath in files:
        filename = os.path.basename(filepath)
        
        # Exclude Reference Files
        if "GIT" in filename or "resume" in filename.lower():
            print(f"Skipping Reference File: {filename}")
            continue

        text = read_file(filepath)
        
        # Regex chunking
        month_chunks = parse_chunks(text, filename)
        
        for bucket_id, content in month_chunks.items():
            content_hash = get_hash(content)
            chunk_id = f"{filename}::{bucket_id}"
            
            # Logic: Is this chunk NEW or CHANGED?
            if state.get(chunk_id) != content_hash:
                # Add to queue
                task = {
                    "id": chunk_id,
                    "filename": filename,
                    "bucket": bucket_id,
                    "type": "NEW", # Or REFRESH
                    "priority": 10,
                    "content": content, # Store content in queue? Or ref? 
                    # Ref is safer for memory, but content ensures consistency. 
                    # Let's store content for now (Notes are text, not huge).
                }
                
                # Deduplicate queue
                if not any(t['id'] == chunk_id for t in queue):
                    queue.append(task)
                    tasks_added += 1
                    print(f"Queueing {chunk_id} (New/Changed)")
                
                # Update state optimistically? No, update state only after Nibble success.
                # Actually, queue manager shouldn't update state, Nibbler should.
                # BUT, to avoid re-queueing every time scan runs, we need a "Queued" state.
                # Let's simple queue dedup handle it.
            
            else:
                # Content hasn't changed.
                # Check for "Refinement" opportunity (Low priority)
                # (Future logic: if last_scan > 30 days, re-queue with type=REFINE)
                pass

    # Sort queue by priority
    queue.sort(key=lambda x: x['priority'], reverse=True)
    
    with open(QUEUE_FILE, 'w') as f:
        json.dump(queue, f, indent=2)
        
    print(f"\nQueue Updated. {tasks_added} new tasks. Total Pending: {len(queue)}")

if __name__ == "__main__":
    main()
