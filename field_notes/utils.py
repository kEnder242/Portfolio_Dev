import json
import os
import time
import glob
import subprocess
import requests
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
STATUS_FILE = os.path.join(DATA_DIR, "status.json")
INTERCOM_LAST_SEEN_FILE = os.path.join(DATA_DIR, "intercom_last_seen.tmp")
INTERCOM_DOWN_LOCK = os.path.join(DATA_DIR, "intercom_down.lock")
ROUND_TABLE_LOCK = os.path.expanduser("~/Dev_Lab/HomeLabAI/round_table.lock")
PROMETHEUS_URL = "http://localhost:9090/api/v1/query"
ATTENDANT_URL = "http://localhost:9999/mutex"

def can_burn(max_load=4.0, check_vram=True, vram_threshold=0.95):
    """Consolidated 'Politeness Check' for all background scanners."""
    # 1. Attendant API Check
    try:
        resp = requests.get(ATTENDANT_URL, timeout=0.5).json()
        if resp.get("round_table_lock_exists"):
            return False, "Attendant: Round Table Active"
    except:
        pass

    # 2. Local File Lock Check (Fallback)
    if os.path.exists(ROUND_TABLE_LOCK):
        return False, "File: Round Table Active"

    # 3. System Load Check
    load = get_system_load()
    if load > max_load:
        return False, f"Load: {load} > {max_load}"

    # 4. VRAM Check
    if check_vram:
        vram = get_vram_usage()
        if vram > vram_threshold:
            return False, f"VRAM: {vram*100:.1f}% > {vram_threshold*100:.0f}%"

    return True, "Ready"

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

def update_status(status, msg, new_items=0, filename=None, engine="Standard", progress_pct=None):
    current = {}
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, 'r') as f:
                current = json.load(f)
        except: pass

    # --- LIVE VITALS ---
    # Brain check (vLLM/Ollama port)
    brain_online = False
    try:
        # Check both potential ports
        for port in [8088, 11434]:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.1)
                if s.connect_ex(('localhost', port)) == 0:
                    brain_online = True
                    break
    except: pass

    # Intercom check
    intercom_online = False
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            if s.connect_ex(('localhost', 8765)) == 0:
                intercom_online = True
    except: pass

    # Round Table Lock check (for yielding scanner)
    scanner_yielded = os.path.exists(ROUND_TABLE_LOCK)

    # --- STATEFUL HEALTH LOGIC (IPMI SEL Style) ---
    is_down_lock = os.path.exists(INTERCOM_DOWN_LOCK)

    if intercom_online:
        with open(INTERCOM_LAST_SEEN_FILE, "w") as f:
            f.write(str(time.time()))
        
        # Recovery Transition: was DOWN, now UP
        if is_down_lock:
            trigger_pager("Intercom Uplink RECOVERED. Service is green.", severity="info", source="DeadMan")
            try: os.remove(INTERCOM_DOWN_LOCK)
            except: pass
    else:
        # Check if we should trigger the "DOWN" transition
        last_seen = 0.0
        if os.path.exists(INTERCOM_LAST_SEEN_FILE):
            with open(INTERCOM_LAST_SEEN_FILE, "r") as f:
                try: last_seen = float(f.read().strip())
                except: last_seen = time.time()
        else:
            last_seen = time.time()
            with open(INTERCOM_LAST_SEEN_FILE, "w") as f:
                f.write(str(last_seen))

        # Down Transition: threshold hit and NO lock exists
        if (time.time() - last_seen > 300) and not is_down_lock:
            trigger_pager("Intercom Uplink DOWN for >5 mins. Check server status.", severity="critical", source="DeadMan")
            with open(INTERCOM_DOWN_LOCK, "w") as f:
                f.write(str(time.time()))

    data = {
        "status": status,
        "message": msg,
        "yielded": scanner_yielded,
        "last_file": filename or current.get("last_file", "None"),
        "last_items": new_items if status == "ONLINE" else current.get("last_items", 0),
        "total_events": get_total_events(),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "engine": engine,
        "progress_pct": progress_pct if progress_pct is not None else current.get("progress_pct", 0),
        "vitals": {
            "brain": "ONLINE" if brain_online else "OFFLINE",
            "intercom": "ONLINE" if intercom_online else "OFFLINE",
            "vram": f"{get_vram_usage()*100:.1f}%"
        }
    }
    
    with open(STATUS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_vram_usage():
    """Reads real GPU memory from DCGM via Prometheus."""
    try:
        # FB_USED is in MiB in DCGM, FB_FREE is also available
        # But we want a %
        res_used = requests.get(PROMETHEUS_URL, params={"query": "DCGM_FI_DEV_FB_USED"}, timeout=1).json()
        res_free = requests.get(PROMETHEUS_URL, params={"query": "DCGM_FI_DEV_FB_FREE"}, timeout=1).json()
        
        used = float(res_used['data']['result'][0]['value'][1])
        free = float(res_free['data']['result'][0]['value'][1])
        total = used + free
        
        return used / total if total > 0 else 0.0
    except Exception as e:
        # Fallback to nvidia-smi if Prometheus/DCGM is down
        try:
            cmd = "nvidia-smi --query-gpu=memory.used,memory.total --format=csv,nounits,noheader"
            output = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
            used, total = map(int, output.split(','))
            return used / total
        except:
            return 0.0

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

import socket

def trigger_pager(summary, severity="info", source="System", dry_run=False, emergency=False):
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "monitor/notify_gatekeeper.py")
    try:
        cmd = [sys.executable, script_path, summary, "--source", source, "--severity", severity]
        if dry_run: cmd.append("--dry-run")
        if emergency: cmd.append("--emergency")
        subprocess.run(cmd, check=True)
        return True
    except Exception as e:
        print(f"Gatekeeper failed: {e}")
        return False
