import os
import json
import logging
import datetime
import glob

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OM_FILE = os.path.join(DATA_DIR, "compressed_history.json")

logging.basicConfig(level=logging.INFO, format='%(asctime)s [OM] %(message)s')

def synthesize_observations():
    """
    Scans recent artifact updates and chat interactions to build a 
    compressed 'State of the Lab' memory.
    """
    logging.info("Starting Observational Synthesis...")
    
    # 1. Load existing state
    state = {}
    if os.path.exists(OM_FILE):
        try:
            with open(OM_FILE, 'r') as f:
                state = json.load(f)
        except: pass

    # 2. Identify 'Active Focals' (What did we work on today?)
    # For now, we'll scan the .json files in data/ modified in the last 24h
    today = datetime.datetime.now().date().isoformat()
    active_topics = set()
    
    json_files = glob.glob(os.path.join(DATA_DIR, "*.json"))
    for jf in json_files:
        if any(x in jf for x in ["themes", "status", "queue", "state", "search_index", "pager_activity", "file_manifest", "compressed_history"]): continue
        
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(jf)).date().isoformat()
        if mtime == today:
            active_topics.add(os.path.basename(jf).replace(".json", ""))

    # 3. Update State
    state["last_synthesis"] = datetime.datetime.now().isoformat()
    state["active_sectors"] = list(active_topics)
    
    # Placeholder for AI-driven summarization (will integrate with Brain later)
    state["observations"] = state.get("observations", [])
    if active_topics:
        obs = f"Observed high activity in sectors: {', '.join(active_topics)} on {today}."
        if not any(o["content"] == obs for o in state["observations"]):
            state["observations"].append({
                "date": today,
                "type": "activity_burst",
                "content": obs
            })

    # 4. Trim history (Keep last 10 observations for short-term OM)
    state["observations"] = state["observations"][-10:]

    # 5. Atomic Write
    temp_file = OM_FILE + ".tmp"
    with open(temp_file, 'w') as f:
        json.dump(state, f, indent=2)
    os.replace(temp_file, OM_FILE)
    logging.info(f"Observational Memory updated with {len(active_topics)} active sectors.")

if __name__ == "__main__":
    synthesize_observations()
