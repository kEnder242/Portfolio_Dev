import json
import os
import sys
import subprocess

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
QUEUE_FILE = os.path.join(DATA_DIR, "queue.json")
# Use the known symlink path relative to the repo root
RAW_NOTES_DIR = os.path.join(os.path.dirname(BASE_DIR), "raw_notes")
NOTES_FILE = "notes_2024_PIAV.txt"

def nudge():
    print(f"=== NUDGE: {NOTES_FILE} ===")
    
    # 1. Clear State (Force re-scan)
    state_file = os.path.join(DATA_DIR, "chunk_state.json")
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            state = json.load(f)
        
        # Remove hashes for 2024 chunks
        keys_to_remove = [k for k in state.keys() if "2024" in k]
        for k in keys_to_remove:
            del state[k]
            
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
        print(f"Cleared state for {len(keys_to_remove)} chunks.")

    # 2. Run Queue Manager (to re-chunk)
    print("Running Queue Manager...")
    subprocess.run(["python3", os.path.join(BASE_DIR, "scan_queue.py")])
    
    # 3. Run Nibbler v2 in FAST MODE
    print("Nibbling (Fast Mode)...")
    # Just run it once, it will loop through the queue
    subprocess.run(["python3", os.path.join(BASE_DIR, "nibble_v2.py"), "--fast"])

    print("\n=== NUDGE COMPLETE ===")

if __name__ == "__main__":
    nudge()
