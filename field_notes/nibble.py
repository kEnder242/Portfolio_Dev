import json
import os
import sys
import re
import time
import glob
import requests
import hashlib

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ai_engine import get_engine

# Config
DATA_DIR = "field_notes/data"
QUEUE_FILE = os.path.join(DATA_DIR, "queue.json")
STATE_FILE = os.path.join(DATA_DIR, "chunk_state.json")
AUDIT_FILE = os.path.join(DATA_DIR, "privacy_audit.jsonl")
THEMES_FILE = os.path.join(DATA_DIR, "themes.json")
STATUS_FILE = os.path.join(DATA_DIR, "status.json")

# Inputs
RESUME_PATH = "raw_notes/Jason Allred Resume - Jan 2026.txt"
FOCAL_OLD = "raw_notes/Performance review 2008-2018 .txt"
FOCAL_NEW = "raw_notes/11066402 Insights 2019-2024.txt"

# AI & Metrics
ENGINE = get_engine(mode="LOCAL")
PROMETHEUS_URL = "http://localhost:9090/api/v1/query"
MAX_LOAD = 2.0

def update_status(status, msg, new_items=0):
    data = {
        "status": status,
        "message": msg,
        "new_items": new_items,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        with open(STATUS_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error updating status: {e}")

def get_system_load():
    try:
        response = requests.get(PROMETHEUS_URL, params={"query": "node_load1"}, timeout=2)
        response.raise_for_status()
        data = response.json()
        if data['status'] == 'success' and data['data']['result']:
            return float(data['data']['result'][0]['value'][1])
    except Exception as e:
        print(f"Warning: Could not check Prometheus ({e}). Assuming safe.")
        return 0.0
    return 999.0 

def can_burn():
    load = get_system_load()
    if load > MAX_LOAD:
        print(f"System Load High ({load} > {MAX_LOAD}). Skipping nibble.")
        update_status("IDLE", f"System busy (Load: {load})")
        return False
    return True

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        return ""

def load_json(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {}

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def extract_json_from_llm(text):
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

def main():
    print("--- Pinky Nibbler v1.3 ---")
    
    # 0. Safety Check
    if not can_burn():
        return

    # 1. Load Queue
    if not os.path.exists(QUEUE_FILE):
        print("Queue empty.")
        # Don't overwrite useful status with "Queue empty" if we just ran successfully recently?
        # Actually, let's read the status file and see if it's "ONLINE". If so, switch to "IDLE".
        current_status = {}
        if os.path.exists(STATUS_FILE):
            try:
                with open(STATUS_FILE, 'r') as f:
                    current_status = json.load(f)
            except: pass
        
        # Only update if we aren't already IDLE
        if current_status.get("status") != "IDLE":
            update_status("IDLE", "Archives sync complete. Standing by.")
        return

    with open(QUEUE_FILE, 'r') as f:
        queue = json.load(f)
        
    if not queue:
        print("Queue empty.")
        update_status("IDLE", "Archives sync complete. Standing by.")
        return

    # 2. Pop Task
    task = queue.pop(0)
    print(f"Nibbling: {task['id']} ({task['type']})")
    
    # 3. Load Context
    resume = read_file(RESUME_PATH)
    focal_1 = read_file(FOCAL_OLD)
    focal_2 = read_file(FOCAL_NEW)
    strategic_context = f"[RESUME]\n{resume[:2000]}\n[FOCALS]\n{focal_1[:3000]}\n{focal_2[:3000]}"
    
    # 4. Check for Existing Data
    bucket_file = os.path.join(DATA_DIR, f"{task['bucket'].replace('-', '_')}.json")
    existing_data = []
    if os.path.exists(bucket_file):
        existing_data = load_json(bucket_file)
        
    # 5. Prompt Pinky
    prompt = f"""
    [ROLE]
    You are 'Pinky', an expert technical archivist.

    [CONTEXT]
    {strategic_context}

    [EXISTING ARCHIVE FOR {task['bucket']}]
    {json.dumps(existing_data, indent=2)}

    [RAW NOTES CHUNK]
    {task['content']}

    [TASK]
    Analyze the RAW NOTES.
    1. Extract technical events (wins, fixes, tools).
    2. Classify sensitivity: "Public" or "Sensitive".
    3. Normalize dates to YYYY-MM-DD.
    
    Return a JSON list of NEW or UPDATED events:
    [
        {{ "date": "YYYY-MM-DD", "summary": "Technical win", "evidence": "Quote", "sensitivity": "Public", "tags": ["IPMI"] }}
    ]
    
    [OUTPUT]
    JSON list only.
    """
    
    print(f"   > Asking Pinky...")
    start_time = time.time()
    response = ENGINE.generate(prompt)
    print(f"   > Pinky answered in {time.time() - start_time:.2f}s")
    
    new_events = extract_json_from_llm(response)
    
    if isinstance(new_events, list):
        final_events = existing_data
        seen = set([(e.get('date'), e.get('summary')) for e in existing_data])
        
        added_count = 0
        for event in new_events:
            if not isinstance(event, dict): continue
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
        
        # Aggregate Year Data
        if '-' in task['bucket']:
            year = task['bucket'].split('-')[0]
            year_file = os.path.join(DATA_DIR, f"{year}.json")
            year_events = []
            monthly_files = glob.glob(os.path.join(DATA_DIR, f"{year}_*.json"))
            for mf in monthly_files:
                year_events.extend(load_json(mf))
            year_events.sort(key=lambda x: x.get('date', ''))
            save_json(year_file, year_events)

        update_status("ONLINE", f"Nibbled {task['id']}", added_count)
    else:
        print("   > Failed to parse Pinky's response.")
        update_status("WARNING", f"Failed to parse response for {task['id']}")

    # 6. Update State
    content_hash = hashlib.md5(task['content'].encode('utf-8')).hexdigest()
    state[task['id']] = content_hash
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

    # 7. Save Queue
    with open(QUEUE_FILE, 'w') as f:
        json.dump(queue, f, indent=2)

if __name__ == "__main__":
    main()
