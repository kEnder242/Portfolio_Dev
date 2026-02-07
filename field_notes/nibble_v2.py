import json
import os
import sys
import re
import time
import glob
import requests
import hashlib
import logging

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ai_engine_v2 import get_engine_v2

# Config
DATA_DIR = "field_notes/data"
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
ENGINE = get_engine_v2(mode="REASONING" if REASONING_MODE else "LOCAL")
PROMETHEUS_URL = "http://localhost:9090/api/v1/query"
MAX_LOAD = float(os.environ.get("MAX_LOAD", 2.0))

def update_status(status, msg, new_items=0):
    current = {}
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, 'r') as f:
                current = json.load(f)
        except: pass

    data = {
        "status": status,
        "message": msg,
        "new_items": new_items if status == "ONLINE" else current.get("new_items", 0),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "engine": "Curriculum/TTCS" if REASONING_MODE else "Standard"
    }
    
    with open(STATUS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_system_load():
    try:
        response = requests.get(PROMETHEUS_URL, params={"query": "node_load1"}, timeout=2)
        response.raise_for_status()
        data = response.json()
        if data['status'] == 'success' and data['data']['result']:
            return float(data['data']['result'][0]['value'][1])
    except: return 0.0
    return 999.0 

def can_burn():
    load = get_system_load()
    if load > MAX_LOAD:
        log(f"System Load High ({load} > {MAX_LOAD}). Skipping nibble.")
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

def main():
    log(f"--- Pinky Nibbler v2.0 (Reasoning: {REASONING_MODE}) ---")
    
    if not can_burn(): return

    if not os.path.exists(QUEUE_FILE):
        update_status("IDLE", "Queue empty.")
        return

    with open(QUEUE_FILE, 'r') as f:
        queue = json.load(f)
        
    if not queue:
        update_status("IDLE", "Queue empty.")
        return

    task = queue.pop(0)
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
        seen = set([(e.get('date'), e.get('summary')) for e in existing_data])
        
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

            key = (event.get('date'), event.get('summary'))
            if key not in seen:
                if event.get("sensitivity") == "Public":
                    final_events.append(event)
                    seen.add(key)
                    added_count += 1
                else:
                    with open(AUDIT_FILE, "a") as f:
                        f.write(json.dumps(event) + "\n")
        
        final_events.sort(key=lambda x: x.get('date', ''))
        save_json(bucket_file, final_events)
        update_status("ONLINE", f"Processed {task['bucket']}", added_count)
    else:
        log("   > No valid events found.")

    # Update State & Queue
    content_hash = hashlib.md5(task['content'].encode('utf-8')).hexdigest()
    state = load_json(STATE_FILE)
    state[task['id']] = content_hash
    save_json(STATE_FILE, state)
    save_json(QUEUE_FILE, queue)

if __name__ == "__main__":
    main()
