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
PROMETHEUS_URL = "http://localhost:9090/api/v1/query"

def get_total_events():
    count = 0
    files = glob.glob(os.path.join(DATA_DIR, "*.json"))
    for f in files:
        if any(x in f for x in ["themes", "status", "queue", "state", "search_index", "pager_activity", "file_manifest"]): continue
        try:
            with open(f, 'r') as fp:
                data = json.load(fp)
                if isinstance(data, list): count += len(data)
        except: pass
    return count

def update_status(status, msg, new_items=0, filename=None, engine="Standard"):
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

    data = {
        "status": status,
        "message": msg,
        "last_file": filename or current.get("last_file", "None"),
        "last_items": new_items if status == "ONLINE" else current.get("last_items", 0),
        "total_events": get_total_events(),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "engine": engine,
        "vitals": {
            "brain": "ONLINE" if brain_online else "OFFLINE",
            "intercom": "ONLINE" if intercom_online else "OFFLINE",
            "vram": f"{get_vram_usage()*100:.1f}%"
        }
    }
    
    with open(STATUS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_vram_usage():
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
    except: return 0.0
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
