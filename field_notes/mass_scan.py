import os
import sys
import time
import json
import subprocess
import requests
import logging

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIBRARIAN = os.path.join(BASE_DIR, "scan_librarian.py")
QUEUE_MGR = os.path.join(BASE_DIR, "scan_queue.py")
NIBBLER = os.path.join(BASE_DIR, "nibble_v2.py")
ARTIFACT_SCANNER = os.path.join(BASE_DIR, "scan_artifacts.py")
DATA_DIR = os.path.join(BASE_DIR, "data")
QUEUE_FILE = os.path.join(DATA_DIR, "queue.json")

# Config
VRAM_THRESHOLD = 0.85 # 80% utilization limit
MAX_LOAD = 4.0        # Allow higher load for "Fast Burn"
SLEEP_INTERVAL = 30   # 30 seconds between tasks in Fast Burn

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [MASS SCAN] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

def get_vram_usage():
    try:
        # Use nvidia-smi to get utilization
        cmd = "nvidia-smi --query-gpu=memory.used,memory.total --format=csv,nounits,noheader"
        output = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
        used, total = map(int, output.split(','))
        return used / total
    except:
        return 0.0

def vram_guard():
    usage = get_vram_usage()
    if usage > VRAM_THRESHOLD:
        logging.warning(f"VRAM usage high ({usage:.2f}). Waiting for cooling...")
        return False
    return True

def run_task(cmd_list):
    try:
        env = os.environ.copy()
        env["MAX_LOAD"] = "5.0"
        subprocess.run([sys.executable] + cmd_list, check=True, env=env)
        return True
    except Exception as e:
        logging.error(f"Task failed: {e}")
        return False

def main():
    logging.info("=== MASS SCAN: FAST BURN v1.0 ===")
    
    # 1. Update Manifest
    logging.info("Step 1: Updating File Manifest...")
    run_task([LIBRARIAN])

    # 2. Update Queue
    logging.info("Step 2: Updating Processing Queue...")
    run_task([QUEUE_MGR])

    # 3. Artifact Map Refresh (Reasoning Mode)
    logging.info("Step 3: Refreshing Artifact Map (Reasoning Mode)...")
    years = ['DOCS', '2024', '2023', '2022', '2021', '2020', '2019']
    for year in years:
        while not vram_guard(): time.sleep(60)
        logging.info(f"Scanning Artifact Sector: {year}")
        run_task([ARTIFACT_SCANNER, year, "--reasoning"])

    # 4. Notes Fast Burn
    logging.info("Step 4: Starting Notes Fast Burn...")
    while True:
        if not os.path.exists(QUEUE_FILE): break
        
        with open(QUEUE_FILE, 'r') as f:
            queue = json.load(f)
            
        if not queue:
            logging.info("Queue empty. Fast Burn complete.")
            break
            
        while not vram_guard(): time.sleep(60)
        
        logging.info(f"Processing next note chunk ({len(queue)} remaining)...")
        # Run nibble_v2 with reasoning and force (via environment or flag if we added it)
        # We'll just run it normally, it pops 1 task.
        if run_task([NIBBLER, "--reasoning"]):
            time.sleep(SLEEP_INTERVAL)
        else:
            logging.error("Nibbler crashed. Retrying in 60s...")
            time.sleep(60)

    logging.info("=== MASS SCAN COMPLETE ===")

if __name__ == "__main__":
    main()
