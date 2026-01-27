import os
import sys
import time
import subprocess

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIBRARIAN = os.path.join(BASE_DIR, "scan_librarian.py")
QUEUE_MGR = os.path.join(BASE_DIR, "scan_queue.py")
NIBBLER = os.path.join(BASE_DIR, "nibble.py")
DATA_DIR = os.path.join(BASE_DIR, "data")
QUEUE_FILE = os.path.join(DATA_DIR, "queue.json")

def run_script(script_path):
    print(f"\n>> Running {os.path.basename(script_path)}...")
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}: {e}")
        return False
    return True

def main():
    print("=== FIELD NOTES FORCE FEED v1.0 ===")
    print("This will aggressively consume the entire backlog using local AI.")
    
    # 1. Update Manifest
    if not run_script(LIBRARIAN): return

    # 2. Update Queue
    if not run_script(QUEUE_MGR): return

    # 3. Nibble Loop
    print("\n>> Starting Nibble Loop...")
    import json
    
    while True:
        # Check Queue
        if not os.path.exists(QUEUE_FILE):
            print("Queue file missing.")
            break
            
        with open(QUEUE_FILE, 'r') as f:
            queue = json.load(f)
            
        if not queue:
            print("Queue empty. Feed complete.")
            break
            
        count = len(queue)
        print(f"\n[PENDING: {count}] Consuming next chunk...")
        
        if not run_script(NIBBLER):
            print("Nibbler crashed. Stopping.")
            break
            
        # Optional: Cool down for GPU?
        # time.sleep(1) 

    # Final Status Update
    from nibble import update_status, get_total_events
    total = get_total_events()
    update_status("IDLE", f"Archives synced. Total records: {total}")

    print("\n=== FEED COMPLETE ===")

if __name__ == "__main__":
    main()
