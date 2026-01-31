import json
import os
import sys

DATA_DIR = "field_notes/data"
QUEUE_FILE = os.path.join(DATA_DIR, "queue.json")
NOTES_FILE = "notes_2024_PIAV.txt"

def nudge():
    print(f"Nudging {NOTES_FILE} into the queue...")
    
    # 1. Load Queue
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, 'r') as f:
            queue = json.load(f)
    else:
        queue = []

    # 2. Read File Content
    try:
        with open(f"raw_notes/{NOTES_FILE}", 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # 3. Create Task (Bucket Unknown/Whole file for now to force scan)
    # Actually, we should chunk it properly. But let's just push the whole file as a single high-priority task 
    # if it's not massive, or rely on scan_queue to re-chunk it.
    # Better: Reset the state for this file and run scan_queue.
    
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

    # 4. Run Queue Manager
    print("Running Queue Manager...")
    os.system("python3 field_notes/scan_queue.py")
    
    # 5. Run Nibbler (Loop a few times)
    print("Nibbling...")
    for _ in range(5):
        os.system("python3 field_notes/nibble.py")

if __name__ == "__main__":
    nudge()
