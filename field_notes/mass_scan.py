import os
import sys
import time
import json
import subprocess
import requests
import logging
import random
import glob

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import update_status, get_vram_usage, trigger_pager

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIBRARIAN = os.path.join(BASE_DIR, "scan_librarian.py")
QUEUE_MGR = os.path.join(BASE_DIR, "scan_queue.py")
NIBBLER = os.path.join(BASE_DIR, "nibble_v2.py")
ARTIFACT_SCANNER = os.path.join(BASE_DIR, "scan_artifacts.py")
GEM_REFINER = os.path.join(BASE_DIR, "refine_gem.py")
DATA_DIR = os.path.join(BASE_DIR, "data")
QUEUE_FILE = os.path.join(DATA_DIR, "queue.json")

# Config
VRAM_THRESHOLD = 0.95 # Allow up to 95% utilization
MAX_LOAD = 4.0        # Allow higher load for "Fast Burn"
SLEEP_INTERVAL = 10   # Shorter interval for Fast Burn

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [MASS SCAN] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

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
        cwd = os.path.dirname(BASE_DIR)
        subprocess.run([sys.executable] + cmd_list, check=True, env=env, cwd=cwd)
        return True
    except Exception as e:
        logging.error(f"Task failed: {e}")
        return False

def get_low_rank_items():
    """Finds items that could benefit from re-reasoning."""
    items = []
    json_files = glob.glob(os.path.join(DATA_DIR, "*.json"))
    for jf in json_files:
        if any(x in jf for x in ["themes", "status", "queue", "state", "search_index", "pager_activity", "file_manifest"]): continue
        try:
            with open(jf, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    for event in data:
                        # Rank < 4 is a candidate for "refinement"
                        if event.get('rank', 2) < 4:
                            items.append({"file": jf, "event": event})
        except: pass
    return items

def main():
    logging.info("=== MASS SCAN: CONTINUOUS RESEARCH v2.0 ===")
    trigger_pager("Initiating High-Fidelity Synthesis Burn.", severity="info", source="MassScan")
    
    epoch_count = 0
    while True:
        epoch_count += 1
        logging.info(f"--- Starting Epoch {epoch_count} ---")
        
        # 1. Update Manifest
        logging.info("Step 1: Updating File Manifest...")
        run_task([LIBRARIAN])

        # 2. Update Queue
        logging.info("Step 2: Updating Processing Queue...")
        run_task([QUEUE_MGR])

        # 3. Artifact Map Refresh (Hybrid/Brain Mode)
        logging.info("Step 3: Refreshing Artifact Map (Hybrid Mode)...")
        years = ['DOCS', '2024', '2023', '2022', '2021', '2020', '2019']
        for year in years:
            while not vram_guard(): time.sleep(60)
            logging.info(f"Scanning Artifact Sector: {year} (Brain)")
            run_task([ARTIFACT_SCANNER, year, "--hybrid"])

        # 4. Notes Fast Burn
        logging.info("Step 4: Consuming Note Queue...")
        while True:
            if not os.path.exists(QUEUE_FILE): break
            with open(QUEUE_FILE, 'r') as f:
                try:
                    queue = json.load(f)
                except: queue = []
            if not queue: break
            
            while not vram_guard(): time.sleep(60)
            
            task = queue[0]
            logging.info(f"Processing: {task['id']} ({len(queue)} remaining)")
            use_hybrid = "2024" in task['bucket'] or "PIAV" in task['filename']
            flag = "--hybrid" if use_hybrid else "--reasoning"
            
            if run_task([NIBBLER, flag]):
                time.sleep(SLEEP_INTERVAL)
            else:
                time.sleep(60)

        # 5. Eternal Slow Burn (Refinement Loop)
        logging.info("Step 5: Entering Eternal Refinement Loop...")
        trigger_pager(f"Epoch {epoch_count} Queue Cleared. Entering Refinement.", severity="info", source="MassScan")
        
        # We stay in this loop for 50 items before re-checking the manifest/queue
        for i in range(50):
            while not vram_guard(): time.sleep(60)
            logging.info(f"Step 5.1: Refining Gem [{i+1}/50]...")
            if run_task([GEM_REFINER]):
                time.sleep(SLEEP_INTERVAL)
            else:
                time.sleep(120) 

        logging.info(f"Epoch {epoch_count} complete. Pulsing Pager.")
        trigger_pager(f"Epoch {epoch_count} Synthesis Complete. Lab is Idle.", severity="info", source="MassScan")
        time.sleep(600) # Wait 10 mins before next full manifest check

if __name__ == "__main__":
    main()
