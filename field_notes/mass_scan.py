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
from utils import update_status, get_vram_usage, trigger_pager, ROUND_TABLE_LOCK, DATA_DIR

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIBRARIAN = os.path.join(BASE_DIR, "scan_librarian.py")
QUEUE_MGR = os.path.join(BASE_DIR, "scan_queue.py")
NIBBLER = os.path.join(BASE_DIR, "nibble_v2.py")
ARTIFACT_SCANNER = os.path.join(BASE_DIR, "scan_artifacts.py")
GEM_REFINER = os.path.join(BASE_DIR, "refine_gem.py")
CLEANER = os.path.join(BASE_DIR, "clean_duplicates.py")
AGGREGATOR = os.path.join(BASE_DIR, "aggregate_years.py")
QUEUE_FILE = os.path.join(DATA_DIR, "queue.json")

# Config
VRAM_THRESHOLD = 0.95 # Allow up to 95% utilization
MAX_LOAD = 4.0        # True Slow Burn threshold
SLEEP_INTERVAL = 60   # Longer interval for polite background operation

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
        cwd = BASE_DIR
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

def check_lock(lock_path):
    """Returns True if background tasks should yield to Intercom."""
    if os.path.exists(lock_path):
        # Check for stale lock (older than 30 mins for faster recovery)
        if time.time() - os.path.getmtime(lock_path) > 1800:
            logging.warning("[LOCK] Stale Round Table Lock detected (>30m). Ignoring.")
            return False
        return True
    return False

def main():
    logging.info("=== MASS SCAN: CONTINUOUS RESEARCH v2.0 ===")
    trigger_pager("Initiating High-Fidelity Synthesis Burn.", severity="info", source="MassScan")
    
    lock_path = ROUND_TABLE_LOCK

    epoch_count = 0
    while True:
        # --- TOP LEVEL LOCK CHECK ---
        if check_lock(lock_path):
            logging.info("[LOCK] Round Table Active. Entering Low-Power Wait...")
            update_status("WAITING", "Round Table Active. Scanner yielded.")
            time.sleep(300) # Wait 5 minutes
            continue

        epoch_count += 1
        logging.info(f"--- Starting Epoch {epoch_count} ---")
        update_status("ONLINE", f"Starting Epoch {epoch_count}...")
        
        # 1. Update Manifest
        run_task([LIBRARIAN])
        if check_lock(lock_path): continue

        # 2. Update Queue
        run_task([QUEUE_MGR])
        if check_lock(lock_path): continue

        # 3. Artifact Map Refresh (Hybrid/Brain Mode)
        logging.info("Step 3: Refreshing Artifact Map (Hybrid Mode)...")
        years = ['DOCS', '2024', '2023', '2022', '2021', '2020', '2019']
        for idx, year in enumerate(years):
            if check_lock(lock_path): break
            while not vram_guard(): 
                update_status("WAITING", "VRAM Cooling...")
                time.sleep(60)
            
            progress = int((idx / len(years)) * 100)
            logging.info(f"Scanning Artifact Sector: {year} (Brain) [{progress}%]")
            update_status("ONLINE", f"Scanning Artifacts: {year}", progress_pct=progress)
            run_task([ARTIFACT_SCANNER, year, "--hybrid"])
        
        if check_lock(lock_path): continue

        # 4. Notes Fast Burn
        logging.info("Step 4: Consuming Note Queue...")
        initial_queue_size = 0
        if os.path.exists(QUEUE_FILE):
            try:
                with open(QUEUE_FILE, 'r') as f:
                    initial_queue_size = len(json.load(f))
            except: pass

        while True:
            if check_lock(lock_path): break
            if not os.path.exists(QUEUE_FILE): break
            with open(QUEUE_FILE, 'r') as f:
                try:
                    queue = json.load(f)
                except: queue = []
            if not queue: break
            
            while not vram_guard(): 
                update_status("WAITING", "VRAM Cooling...")
                time.sleep(60)
            
            task = queue[0]
            remaining = len(queue)
            progress = 100
            if initial_queue_size > 0:
                progress = int(((initial_queue_size - remaining) / initial_queue_size) * 100)
            
            logging.info(f"Processing: {task['id']} ({remaining} remaining) [{progress}%]")
            update_status("BUSY", f"Nibbling: {task['id']}", filename=task['filename'], progress_pct=progress)
            
            use_hybrid = "2024" in task['bucket'] or "PIAV" in task['filename']
            flag = "--hybrid" if use_hybrid else "--reasoning"
            
            if run_task([NIBBLER, flag]):
                time.sleep(SLEEP_INTERVAL)
            else:
                time.sleep(60)

        if check_lock(lock_path): continue

        # 5. Eternal Slow Burn (Refinement Loop)
        logging.info("Step 5: Entering Eternal Refinement Loop...")
        trigger_pager(f"Epoch {epoch_count} Queue Cleared. Entering Refinement.", severity="info", source="MassScan")
        
        # We stay in this loop for 50 items before re-checking the manifest/queue
        for i in range(50):
            if check_lock(lock_path): break
            while not vram_guard(): 
                update_status("WAITING", "VRAM Cooling...")
                time.sleep(60)
            logging.info(f"Step 5.1: Refining Gem [{i+1}/50]...")
            update_status("ONLINE", f"Refining Gem {i+1}/50")
            if run_task([GEM_REFINER]):
                time.sleep(SLEEP_INTERVAL)
            else:
                time.sleep(120) 

        if check_lock(lock_path): continue

        # 6. Final TLC: De-duplicate, Aggregate and Tidy
        logging.info("Step 6: Performing Archive TLC (De-duplication & Aggregation)...")
        update_status("ONLINE", "Tidying Archive...")
        run_task([CLEANER])
        run_task([AGGREGATOR])

        logging.info(f"Epoch {epoch_count} complete. Pulsing Pager.")
        update_status("IDLE", f"Epoch {epoch_count} complete.")
        trigger_pager(f"Epoch {epoch_count} Synthesis Complete. Lab is Idle.", severity="info", source="MassScan")
        time.sleep(600) # Wait 10 mins before next full manifest check

if __name__ == "__main__":
    main()
