import json
import os
import sys
import logging
import random

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ai_engine_v2 import get_engine_v2
from utils import update_status

# Config
DATA_DIR = "field_notes/data"
logging.basicConfig(level=logging.INFO, format='[REFINE] %(message)s')

def main():
    logging.info("--- Technical Gem Refinement Loop ---")
    
    # 1. Target the Brain (Hybrid Mode)
    engine = get_engine_v2(mode="HYBRID") # Pinky Orchestrator + Brain Backend
    
    # 2. Find a low-rank artifact
    import glob
    json_files = glob.glob(os.path.join(DATA_DIR, "*.json"))
    ignore = ["themes.json", "status.json", "queue.json", "state.json", "search_index.json", "pager_activity.json", "file_manifest.json"]
    
    candidates = []
    for jf in json_files:
        if os.path.basename(jf) in ignore: continue
        try:
            with open(jf, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    for i, event in enumerate(data):
                        if event.get('rank', 2) < 4:
                            candidates.append((jf, i, event))
        except: pass

    if not candidates:
        logging.info("All gems are currently Rank 4 (Diamond). No refinement needed.")
        return

    # 3. Pick one and refine
    file_path, index, event = random.choice(candidates)
    logging.info(f"Refining: {event.get('summary')} in {os.path.basename(file_path)}")

    refine_prompt = f"""
    [ROLE] Senior Silicon Validation Architect.
    [BKM PROTOCOL] 1. One-liner, 2. Core Logic, 3. Trigger, 4. Scars.
    
    [CURRENT ENTRY]
    Date: {event.get('date')}
    Summary: {event.get('summary')}
    Technical Gem: {event.get('technical_gem', 'None')}
    Evidence: {event.get('evidence')}
    
    [TASK]
    Review the entry above. If the 'Technical Gem' is generic (e.g., 'fixed a bug', 'ran a test'), 
    re-analyze the [Evidence] to find a specific tool name, error code, or architectural nuance.
    
    [OUTPUT FORMAT]
    Output ONLY a JSON object with the improved fields and set "rank": 4.
    {{ "summary": "...", "technical_gem": "...", "rank": 4, "tags": [...] }}
    """
    
    try:
        response = engine.generate(refine_prompt)
        # Extract JSON
        import re
        match = re.search(r'\{.*\}', response, re.DOTALL)
        if match:
            new_data = json.loads(match.group(0))
            
            # 4. Save back
            with open(file_path, 'r') as f:
                full_data = json.load(f)
            
            # Update fields
            full_data[index].update(new_data)
            
            with open(file_path, 'w') as f:
                json.dump(full_data, f, indent=2)
            
            logging.info(f"✨ Refinement Success! Gem upgraded to Rank 4.")
            update_status("REFINE", f"Upgraded gem: {event.get('summary')[:30]}", 1)
        else:
            logging.warning("Brain provided invalid JSON for refinement.")
    except Exception as e:
        logging.error(f"Refinement failed: {e}")

if __name__ == "__main__":
    main()
