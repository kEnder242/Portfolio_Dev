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
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
from ai_engine_v2 import get_engine_v2
from utils import update_status, get_system_load, ROUND_TABLE_LOCK, can_burn, DATA_DIR

# Config
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
MAX_LOAD = float(os.environ.get("MAX_LOAD", 4.0))

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
            try:
                return json.load(f)
            except: return []
    return []

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def extract_json_from_llm(text):
    """
    [FEAT-131] Robust JSON Extraction.
    Hunts for JSON blocks amidst conversational filler.
    """
    if not text: 
        logging.info("   [DEBUG] LLM returned empty/None response.")
        return []
    
    # Log raw for debugging if it's not JSON
    if not text.strip().startswith(("[", "{")):
        logging.info(f"   [DEBUG] Raw LLM Response (First 100 chars): {text[:100]}...")

    # Try to find a list [ ... ]
    list_match = re.search(r'(\[.*\])', text, re.DOTALL)
    if list_match:
        try:
            data = json.loads(list_match.group(1))
            return data if isinstance(data, list) else [data]
        except: pass
        
    # Try to find a dict { ... } and wrap it in a list
    dict_match = re.search(r'(\{.*\})', text, re.DOTALL)
    if dict_match:
        try:
            data = json.loads(dict_match.group(1))
            if isinstance(data, dict) and not data: # Ignore empty {}
                return []
            return [data] if isinstance(data, dict) else data
        except: pass

    # Last resort: strip markdown and attempt raw load
    clean = text.replace("```json", "").replace("```", "").strip()
    try:
        data = json.loads(clean)
        if isinstance(data, dict) and not data: return []
        return [data] if isinstance(data, dict) else data
    except:
        return []

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
    log(f"--- Pinky Nibbler v2.1 (Reasoning: {REASONING_MODE}) ---")
    
    # --- LIMIT FLAG ---
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
        
        # --- HASH DE-DUPING ---
        content_hash = hashlib.md5(task['content'].encode('utf-8')).hexdigest()
        if state.get(task['id']) == content_hash:
            log(f"   > Skipping {task['id']} (Hash match)")
            continue

        # --- POLITENESS CHECK ---
        while not check_politeness():
            update_status("YIELD", f"Nibbler Yielding (Lock/Load)", filename=task['id'])
            time.sleep(10)

        log(f"Nibbling: {task['id']} ({task['bucket']})")
        
        # [FEAT-128] Strategic Prompt selection
        file_type = task.get('type', 'LOG')
        prompt = ""
        
        if file_type == "META":
            prompt = f"""
            [TASK] Expert Career Strategist. Analyze this high-level document and extract the core strategic anchor.
            [YEAR] {task['bucket']}
            [CONTENT]
            {task['content'][:8000]}
            
            [OUTPUT]
            Generate a JSON list containing ONE high-value entry.
            Prefix the summary with [STRATEGIC_ANCHOR].
            The summary should capture the primary focal point, philosophical shift, or major career milestone.
            
            [FORMAT]
            [
              {{ 
                "date": "{task['bucket']}-01-01", 
                "summary": "[STRATEGIC_ANCHOR] ...", 
                "evidence": "...", 
                "sensitivity": "Public", 
                "tags": ["strategy", "anchor"] 
              }}
            ]
            """
        else:
            prompt = f"Extract technical events from this log: {task['content'][:4000]}"

        bucket_file = os.path.join(DATA_DIR, f"{task['bucket'].replace('-', '_')}.json")
        existing_data = load_json(bucket_file)
            
        try:
            if file_type == "META":
                # Meta documents always use the strategic anchor prompt
                response = ENGINE.generate(prompt)
            elif REASONING_MODE and hasattr(ENGINE, 'generate_with_reasoning'):
                response = ENGINE.generate_with_reasoning(task['content'], task['bucket'])
            else:
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
                
                # Use provided date or fallback
                raw_date = event.get('date', '')
                clean_date = validate_date(raw_date)
                
                # Auto-assign bucket date if missing or invalid
                if not clean_date:
                    if '-' in task['bucket']:
                        parts = task['bucket'].split('-')
                        clean_date = f"{parts[0]}-{parts[1]}-01"
                    else:
                        # Year bucket (META)
                        clean_date = f"{task['bucket']}-01-01"

                event['date'] = clean_date
                
                # Rank 5 for META anchors
                if file_type == "META":
                    event['rank'] = 5
                
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
            
            # [FEAT-130] Atomic State Update: ONLY mark as done if data was captured
            state[task['id']] = content_hash
            save_json(STATE_FILE, state)
        else:
            log("   > No valid events found. State NOT updated.")

        save_json(QUEUE_FILE, queue)

        if not FAST_MODE:
            log("Waiting 15s for silicon cooling...")
            time.sleep(15)
        else:
            time.sleep(1) # Tiny yield to prevent CPU spinning

if __name__ == "__main__":
    main()
