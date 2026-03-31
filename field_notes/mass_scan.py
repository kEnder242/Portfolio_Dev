import os
import sys
import time
import json
import subprocess
import requests
import logging
import random
import glob
import argparse

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
RAW_NOTES_DIR = os.path.join(os.path.dirname(BASE_DIR), "raw_notes")

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

def hallway_protocol(keyword):
    """[FEAT-179] Targeted scan for the Hallway Protocol."""
    logging.info(f"=== HALLWAY PROTOCOL: Targeted Search for '{keyword}' ===")
    
    # 1. Grep for matching files in raw_notes
    try:
        # Use ripgrep or grep to find files containing the keyword
        cmd = ["grep", "-rl", keyword, RAW_NOTES_DIR]
        res = subprocess.run(cmd, capture_output=True, text=True)
        files = res.stdout.strip().split("\n") if res.stdout else []
        
        if not files or (len(files) == 1 and files[0] == ''):
            logging.info(f"No raw notes found matching '{keyword}'.")
            return
        
        # Limit to top 5 for fast response
        target_files = files[:5]
        logging.info(f"Found {len(files)} matches. Scanning top {len(target_files)}...")
        
        # 2. Force these files into the nibbler
        for f in target_files:
            rel_path = os.path.relpath(f, RAW_NOTES_DIR)
            logging.info(f"Deep Harvesting: {rel_path}")
            # We use --reasoning mode for high-fidelity extraction
            run_task([NIBBLER, "--reasoning", "--file", f])
            
    except Exception as e:
        logging.error(f"Hallway Protocol failed: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword", help="Run a targeted Hallway Protocol scan.")
    args = parser.parse_args()

    if args.keyword:
        hallway_protocol(args.keyword)
        return

    logging.info("=== MASS SCAN: CONTINUOUS RESEARCH v2.0 ===")
    trigger_pager("Initiating High-Fidelity Synthesis Burn.", severity="info", source="MassScan")
    
    lock_path = ROUND_TABLE_LOCK
    maint_lock = os.path.join(DATA_DIR, "maintenance.lock")

    epoch_count = 0
    while True:
        # --- [FEAT-259.1] TOP LEVEL LOCK CHECKS ---
        if os.path.exists(maint_lock):
            logging.info("[LOCK] Maintenance Lock Active. Silencing all background tasks.")
            update_status("IDLE", "Maintenance Active. Scanner yielded.")
            time.sleep(300)
            continue

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
        
        # 2. Update Queue
        run_task([QUEUE_MGR])

        # 3. Artifact Map Refresh (Hybrid/Brain Mode)
        # Only run if there is work or if specifically requested
        if os.path.exists(QUEUE_FILE):
            with open(QUEUE_FILE, 'r') as f:
                queue = json.load(f)
            
            if queue:
                logging.info("Step 3: Refreshing Artifact Map (Hybrid Mode)...")
                years = ['DOCS', '2024', '2023', '2022', '2021', '2020', '2019']
                for idx, year in enumerate(years):
                    if check_lock(lock_path) or os.path.exists(maint_lock): break
                    while not vram_guard(): 
                        update_status("WAITING", "VRAM Cooling...")
                        time.sleep(60)
                    
                    progress = int((idx / len(years)) * 100)
                    logging.info(f"Scanning Artifact Sector: {year} (Brain) [{progress}%]")
                    update_status("ONLINE", f"Scanning Artifacts: {year}", progress_pct=progress)
                    run_task([ARTIFACT_SCANNER, year, "--hybrid"])
        
        if check_lock(lock_path) or os.path.exists(maint_lock): continue

        # 4. Notes Fast Burn
        logging.info("Step 4: Consuming Note Queue...")
        initial_queue_size = 0
        if os.path.exists(QUEUE_FILE):
            try:
                with open(QUEUE_FILE, 'r') as f:
                    queue = json.load(f)
                    initial_queue_size = len(queue)
            except: queue = []

            while queue:
                if check_lock(lock_path) or os.path.exists(maint_lock): break
                
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
                
                # Reload queue
                with open(QUEUE_FILE, 'r') as f:
                    queue = json.load(f)

        if check_lock(lock_path) or os.path.exists(maint_lock): continue

        # 5. Eternal Slow Burn (Refinement Loop)
        # [POLITENESS] Only refine if the queue was just cleared or specifically idle
        items_to_refine = get_low_rank_items()
        if items_to_refine:
            logging.info(f"Step 5: Refining {len(items_to_refine)} items...")
            for i in range(min(len(items_to_refine), 50)):
                if check_lock(lock_path) or os.path.exists(maint_lock): break
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
