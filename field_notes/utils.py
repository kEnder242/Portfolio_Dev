import json
import os
import time
import glob
import subprocess
import requests
import sys

# --- PATH RESOLUTION (SINGLE SOURCE OF TRUTH) ---
def find_lab_root():
    """Locates the absolute Lab root by searching upward for the bootstrap anchor."""
    curr = os.path.dirname(os.path.abspath(__file__))
    for _ in range(5): # Max 5 levels up
        if os.path.exists(os.path.join(curr, "BOOTSTRAP_v4.3.md")):
            return curr
        curr = os.path.dirname(curr)
    # Fallback to current directory's parent if anchor not found
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LAB_ROOT = find_lab_root()
BASE_DIR = os.path.join(LAB_ROOT, "Portfolio_Dev/field_notes")
DATA_DIR = os.path.join(BASE_DIR, "data")
# Hardened Absolute Paths
ROUND_TABLE_LOCK = os.path.join(LAB_ROOT, "HomeLabAI/round_table.lock")
RAW_NOTES_DIR = os.path.join(LAB_ROOT, "knowledge_base") # Direct link to source
STATUS_FILE = os.path.join(DATA_DIR, "status.json")

# URLs
PROMETHEUS_URL = "http://localhost:9090/api/v1/query"
ATTENDANT_URL = "http://localhost:9999/mutex"

def update_status(status, message, last_items=0, filename=None, engine="LOCAL", progress_pct=None):
    """Updates the status.json for the front-end dashboard."""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Preserve existing data if possible
    curr_data = {}
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, 'r') as f:
                curr_data = json.load(f)
        except: pass

    data = {
        "status": status,
        "message": message,
        "last_items": last_items,
        "total_events": get_total_events(),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "engine": engine,
        "progress_pct": progress_pct if progress_pct is not None else curr_data.get("progress_pct", 0)
    }
    
    if filename:
        data["last_file"] = filename
    elif "last_file" in curr_data:
        data["last_file"] = curr_data["last_file"]

    # Atomic write
    temp_file = STATUS_FILE + ".tmp"
    with open(temp_file, 'w') as f:
        json.dump(data, f, indent=2)
    os.replace(temp_file, STATUS_FILE)

def get_total_events():
    count = 0
    # Only count yearly summaries (YYYY.json) to avoid double-counting with monthly logs
    files = glob.glob(os.path.join(DATA_DIR, "[0-9][0-9][0-9][0-9].json"))
    for f in files:
        try:
            with open(f, 'r') as fp:
                data = json.load(fp)
                if isinstance(data, list): count += len(data)
        except: pass
    return count

def get_system_load():
    try:
        response = requests.get(PROMETHEUS_URL, params={"query": "node_load1"}, timeout=2)
        response.raise_for_status()
        data = response.json()
        if data['status'] == 'success' and data['data']['result']:
            return float(data['data']['result'][0]['value'][1])
    except: 
        # Fallback to standard OS load
        try:
            load1, _, _ = os.getloadavg()
            return load1
        except:
            return 0.0
    return 999.0 

def get_vram_usage():
    """Returns VRAM usage as a fraction (0.0 to 1.0) using nvidia-smi."""
    try:
        output = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=memory.used,memory.total", "--format=csv,nounits,noheader"],
            encoding="utf-8"
        )
        used, total = map(float, output.strip().split(','))
        return used / total
    except:
        return 0.0

def can_burn(max_load=4.0, check_vram=True, vram_threshold=0.95):
    """
    Politeness check for background tasks.
    Returns (bool, reason)
    """
    # 1. Check for Active Session Lock
    if os.path.exists(ROUND_TABLE_LOCK):
        return False, "Active Intercom Session (Lock)"
    
    # 2. Check Attendant Mutex API
    try:
        resp = requests.get(ATTENDANT_URL, timeout=2)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("yielding"):
                return False, "Attendant Mutex Yielding"
    except:
        pass # If attendant is down, fallback to system metrics

    # 3. Check System Load
    load = get_system_load()
    if load > max_load:
        return False, f"System Load High ({load:.2f})"
    
    # 4. Check VRAM
    if check_vram:
        vram = get_vram_usage()
        if vram > vram_threshold:
            return False, f"VRAM High ({vram*100:.1f}%)"
            
    return True, "Nominal"

def trigger_pager(message, severity="info", source="Lab"):
    """Fires a notification to the Pager center."""
    try:
        # Pager implementation stub
        pass
    except: pass
