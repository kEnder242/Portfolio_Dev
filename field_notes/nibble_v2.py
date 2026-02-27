import json
import os
import sys
import re
import time
import glob
import requests
import hashlib
import logging
import difflib

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ai_engine_v2 import get_engine_v2
from utils import update_status, get_system_load, ROUND_TABLE_LOCK, can_burn

# Config
DATA_DIR = "/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/data"
QUEUE_FILE = os.path.join(DATA_DIR, "queue.json")
STATE_FILE = os.path.join(DATA_DIR, "chunk_state.json")
AUDIT_FILE = os.path.join(DATA_DIR, "privacy_audit.jsonl")
STATUS_FILE = os.path.join(DATA_DIR, "status.json")

# Setup Logging
LOG_FILE = os.path.join(DATA_DIR, "pinky_v2.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

def log(msg):
    logging.info(msg)

# AI & Metrics
REASONING_MODE = "--reasoning" in sys.argv
HYBRID_MODE = "--hybrid" in sys.argv
FAST_MODE = "--fast" in sys.argv
engine_mode = "LOCAL"
if HYBRID_MODE: engine_mode = "HYBRID"
elif REASONING_MODE: engine_mode = "REASONING"

ENGINE = get_engine_v2(mode=engine_mode)
MAX_LOAD = float(os.environ.get("MAX_LOAD", 2.0))

def check_politeness():
    if FAST_MODE: return True
    ready, reason = can_burn(max_load=MAX_LOAD)
    if not ready:
        log(f"Yielding: {reason}")
        return False
    return True

def load_json(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return []

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def extract_json_from_llm(text):
    match = re.search(r'\[.*\]', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except: pass
    text = text.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(text)
    except: return []

def validate_date(date_str):
    if not date_str: return None
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        return date_str
    match = re.match(r'(\d{1,2})/(\d{1,2})/(\d{4})', date_str)
    if match:
        m, d, y = match.groups()
        return f"{y}-{m.zfill(2)}-{d.zfill(2)}"
    return None

def is_semantic_duplicate(new_summary, existing_events, threshold=0.85):
    """Checks if a summary is semantically similar to any existing event on the same date."""
    for event in existing_events:
        existing_summary = event.get('summary', '')
        # Simple fuzzy ratio
        ratio = difflib.SequenceMatcher(None, new_summary.lower(), existing_summary.lower()).ratio()
        if ratio > threshold:
            return True
    return False

def main():
    log(f"--- Pinky Nibbler v2.0 (Reasoning: {REASONING_MODE}) ---")
    
    # --- NEW: LIMIT FLAG ---
    limit = 999
    for arg in sys.argv:
        if arg.startswith("--limit="):
            limit = int(arg.split("=")[1])

    if not os.path.exists(QUEUE_FILE):
        update_status("IDLE", "Queue empty.")
        return

    with open(QUEUE_FILE, 'r') as f:
        queue = json.load(f)
        
    if not queue:
        update_status("IDLE", "Queue empty.")
        return

    # Load State for De-duping
    state = load_json(STATE_FILE)
    if isinstance(state, list): state = {} # Safety for corrupted state

    processed_this_run = 0
    while queue and processed_this_run < limit:
        task = queue.pop(0)
        processed_this_run += 1
        
        # --- NEW: HASH DE-DUPING ---
        content_hash = hashlib.md5(task['content'].encode('utf-8')).hexdigest()
        if state.get(task['id']) == content_hash:
            log(f"   > Skipping {task['id']} (Hash match: {content_hash})")
            continue

        # --- POLITENESS CHECK ---
        while not check_politeness():
            update_status("YIELD", f"Nibbler Yielding (Lock/Load)", filename=task['id'])
            time.sleep(10)

        log(f"Nibbling: {task['id']} ({task['bucket']})")
        
        bucket_file = os.path.join(DATA_DIR, f"{task['bucket'].replace('-', '_')}.json")
        existing_data = load_json(bucket_file)
            
        try:
            if REASONING_MODE and hasattr(ENGINE, 'generate_with_reasoning'):
                response = ENGINE.generate_with_reasoning(task['content'], task['bucket'])
            else:
                # Fallback to standard prompt if not in reasoning mode
                prompt = f"Extract technical events from this log: {task['content'][:4000]}"
                response = ENGINE.generate(prompt)
                
            new_events = extract_json_from_llm(response)
        except Exception as e:
            log(f"   ! Engine Error: {e}")
            new_events = []
        
        if isinstance(new_events, list) and len(new_events) > 0:
            final_events = existing_data
            
            added_count = 0
            for event in new_events:
                if not isinstance(event, dict): continue
                clean_date = validate_date(event.get('date', ''))
                
                # Auto-assign bucket date if missing
                if not clean_date and '-' in task['bucket']:
                    try:
                        parts = task['bucket'].split('-')
                        clean_date = f"{parts[0]}-{parts[1]}-01"
                    except: pass

                if not clean_date: continue
                event['date'] = clean_date
                
                # Filter events for the same date to check for semantic duplicates
                same_date_events = [e for e in final_events if e.get('date') == clean_date]
                
                if not is_semantic_duplicate(event.get('summary', ''), same_date_events):
                    if event.get("sensitivity") == "Public":
                        final_events.append(event)
                        added_count += 1
                    else:
                        with open(AUDIT_FILE, "a") as f:
                            f.write(json.dumps(event) + "\n")
                else:
                    log(f"   > Semantic Duplicate skipped: {event.get('summary')[:50]}...")
            
            final_events.sort(key=lambda x: x.get('date', ''))
            save_json(bucket_file, final_events)
            update_status("ONLINE", f"Processed {task['bucket']}", added_count, filename=task['filename'], engine=engine_mode)
        else:
            log("   > No valid events found.")

        # Update State
        state[task['id']] = content_hash
        save_json(STATE_FILE, state)
        save_json(QUEUE_FILE, queue)

        if not FAST_MODE:
            log("Waiting 15s for silicon cooling...")
            time.sleep(15)
        else:
            time.sleep(1) # Tiny yield to prevent CPU spinning

if __name__ == "__main__":
    main()
