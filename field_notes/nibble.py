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
    # Load previous to persist "Last Action" if going IDLE
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
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # If going IDLE, maybe keep the last "Processed X" message in a separate field?
    # For now, just overwrite. The UI shows "Total Records" when IDLE.
    
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
    except Exception:
        return 0.0 # Assume safe if prometheus is down
    return 999.0 

def can_burn():
    load = get_system_load()
    if load > MAX_LOAD:
        print(f"System Load High ({load} > {MAX_LOAD}). Skipping nibble.")
        # Only update status if it was previously ONLINE? No, let's just log it.
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

def validate_date(date_str):
    if not date_str: return None
    # Strict YYYY-MM-DD
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        return date_str
    # Repair YYYY/MM/DD or MM/DD/YYYY
    match = re.match(r'(\d{1,2})/(\d{1,2})/(\d{4})', date_str)
    if match:
        m, d, y = match.groups()
        return f"{y}-{m.zfill(2)}-{d.zfill(2)}"
    return None

def get_total_events():
    count = 0
    files = glob.glob(os.path.join(DATA_DIR, "*.json"))
    for f in files:
        if "themes" in f or "status" in f or "queue" in f or "state" in f: continue
        try:
            with open(f, 'r') as fp:
                data = json.load(fp)
                if isinstance(data, list): count += len(data)
        except: pass
    return count

def main():
    print("--- Pinky Nibbler v1.4 (Strict) ---")
    
    if not can_burn():
        return

    if not os.path.exists(QUEUE_FILE):
        total = get_total_events()
        update_status("IDLE", f"Archives synced. Total records: {total}")
        return

    with open(QUEUE_FILE, 'r') as f:
        queue = json.load(f)
        
    if not queue:
        total = get_total_events()
        update_status("IDLE", f"Archives synced. Total records: {total}")
        return

    task = queue.pop(0)
    print(f"Nibbling: {task['id']}")
    
    resume = read_file(RESUME_PATH)
    focal_1 = read_file(FOCAL_OLD)
    focal_2 = read_file(FOCAL_NEW)
    strategic_context = f"[RESUME]\n{resume[:2000]}\n[FOCALS]\n{focal_1[:3000]}\n{focal_2[:3000]}"
    
    bucket_file = os.path.join(DATA_DIR, f"{task['bucket'].replace('-', '_')}.json")
    existing_data = []
    if os.path.exists(bucket_file):
        existing_data = load_json(bucket_file)
        
    prompt = f"""
    [ROLE]
    You are 'Pinky', an expert technical archivist.

    [CONTEXT]
    {strategic_context}

    [EXISTING ARCHIVE]
    {json.dumps(existing_data[:5], indent=2)}... (truncated)

    [RAW LOGS]
    {task['content'][:6000]}

    [TASK]
    Analyze the RAW NOTES.
    1. Extract technical events (Technical win, Bug fix, Tool usage).
    2. Compare with EXISTING ARCHIVE. avoid duplicates.
    3. IMPROVE descriptions if the raw notes offer more detail.
    4. **PRIVACY & REDACTION:**
       - **Public:** Technical work, bug fixes, tool usage.
         * *ACTION:* If it contains a name/email, replace it with `[REDACTED]`. Keep the technical context.
       - **Sensitive:** Personal feedback ("improvement needed"), salary, health, or purely internal non-technical gossip.
         * *ACTION:* Mark as "Sensitive".
    
    Return a JSON list of NEW or UPDATED events:
    [
        {{ "date": "YYYY-MM-DD", "summary": "Meeting with [REDACTED] about Simics debugging", "evidence": "Quote", "sensitivity": "Public", "tags": ["Simics"] }}
    ]
    """
    
    print(f"   > Asking Pinky...")
    try:
        response = ENGINE.generate(prompt)
        new_events = extract_json_from_llm(response)
    except Exception as e:
        print(f"   ! AI Error: {e}")
        new_events = []
    
    if isinstance(new_events, list) and len(new_events) > 0:
        final_events = existing_data
        seen = set([(e.get('date'), e.get('summary')) for e in existing_data])
        
        added_count = 0
        for event in new_events:
            if not isinstance(event, dict): continue
            
            clean_date = validate_date(event.get('date', ''))
            
            # Fallback to Bucket Date if Pinky missed it
            if not clean_date and '-' in task['bucket']:
                try:
                    # bucket is YYYY-MM
                    parts = task['bucket'].split('-')
                    if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                        clean_date = f"{parts[0]}-{parts[1]}-01"
                except: pass

            if not clean_date:
                continue # Skip invalid dates
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
        
        # Aggregate
        if '-' in task['bucket']:
            year = task['bucket'].split('-')[0]
            year_file = os.path.join(DATA_DIR, f"{year}.json")
            year_events = []
            monthly_files = glob.glob(os.path.join(DATA_DIR, f"{year}_*.json"))
            for mf in monthly_files:
                year_events.extend(load_json(mf))
            year_events.sort(key=lambda x: x.get('date', ''))
            save_json(year_file, year_events)

        update_status("ONLINE", f"Processed {task['bucket']}", added_count)
    else:
        print("   > No valid events found.")
        # Still update state to prevent infinite retry?
        # Yes, mark done even if empty to move on.

    # Update State & Queue
    content_hash = hashlib.md5(task['content'].encode('utf-8')).hexdigest()
    
    # Load state again (race condition safety)
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
    else:
        state = {}
        
    state[task['id']] = content_hash
    
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

    with open(QUEUE_FILE, 'w') as f:
        json.dump(queue, f, indent=2)

if __name__ == "__main__":
    main()
