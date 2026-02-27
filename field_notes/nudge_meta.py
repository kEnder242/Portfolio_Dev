import json
import os

# Config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MANIFEST_FILE = os.path.join(DATA_DIR, "file_manifest.json")
STATE_FILE = os.path.join(DATA_DIR, "chunk_state.json")

def nudge_meta():
    print("--- Nudging META documents for Re-Extraction ---")
    
    if not os.path.exists(MANIFEST_FILE) or not os.path.exists(STATE_FILE):
        print("Error: Manifest or State file missing.")
        return

    with open(MANIFEST_FILE, 'r') as f:
        manifest = json.load(f)
    
    with open(STATE_FILE, 'r') as f:
        state = json.load(f)

    # 1. Identify META files
    meta_files = [fname for fname, info in manifest.items() if info.get('type') == 'META']
    print(f"Found {len(meta_files)} META documents in manifest.")

    # 2. Surgical invalidation
    removed_count = 0
    new_state = {}
    for chunk_id, content_hash in state.items():
        # Check if chunk_id starts with a meta filename followed by ::
        is_meta = False
        for mf in meta_files:
            if chunk_id.startswith(f"{mf}::"):
                is_meta = True
                break
        
        if is_meta:
            removed_count += 1
        else:
            new_state[chunk_id] = content_hash

    # 3. Save updated state
    with open(STATE_FILE, 'w') as f:
        json.dump(new_state, f, indent=2)

    print(f"Removed {removed_count} chunk hashes. META files will be re-queued.")

if __name__ == "__main__":
    nudge_meta()
