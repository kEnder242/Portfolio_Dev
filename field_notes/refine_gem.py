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
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
logging.basicConfig(level=logging.INFO, format='[REFINE] %(message)s')

def cosine_similarity(a, b):
    import numpy as np
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def deduplicate_gems():
    import glob
    import numpy as np
    from sentence_transformers import SentenceTransformer
    
    logging.info("Running Semantic De-duplication check [Goal 6]...")
    
    try:
        model = SentenceTransformer("all-MiniLM-L6-v2")
    except Exception as e:
        logging.error(f"Failed to load SentenceTransformer: {e}")
        return
        
    json_files = glob.glob(os.path.join(DATA_DIR, "*.json"))
    ignore = ["themes.json", "status.json", "queue.json", "state.json", "search_index.json", "pager_activity.json", "file_manifest.json", "overrides.json"]
    
    events_by_date = {}
    for jf in json_files:
        if os.path.basename(jf) in ignore: continue
        try:
            with open(jf, 'r') as f:
                data = json.load(f)
                if not isinstance(data, list): continue
                for i, event in enumerate(data):
                    date = event.get('date')
                    if not date: continue
                    if date not in events_by_date:
                        events_by_date[date] = []
                    events_by_date[date].append({
                        "file_path": jf,
                        "index": i,
                        "event": event
                    })
        except: pass

    modified_files = set()
    file_contents = {}
    
    def get_content(path):
        if path not in file_contents:
            with open(path, 'r') as f:
                file_contents[path] = json.load(f)
        return file_contents[path]

    for date, items in events_by_date.items():
        if len(items) < 2: continue
        
        summaries = [it["event"].get("summary", "") for it in items]
        embeddings = model.encode(summaries)
        
        merged_indices = set()
        for i in range(len(items)):
            if i in merged_indices: continue
            for j in range(i + 1, len(items)):
                if j in merged_indices: continue
                
                sim = cosine_similarity(embeddings[i], embeddings[j])
                if sim > 0.85:
                    logging.info(f"   [MERGE] Found duplicates on {date} (similarity: {sim:.2f})")
                    logging.info(f"     1: {summaries[i][:50]}...")
                    logging.info(f"     2: {summaries[j][:50]}...")
                    
                    event_i = items[i]["event"]
                    event_j = items[j]["event"]
                    
                    if len(event_j.get("summary", "")) > len(event_i.get("summary", "")):
                        event_i["summary"] = event_j["summary"]
                        
                    ev_i = event_i.get("evidence", "")
                    ev_j = event_j.get("evidence", "")
                    if ev_j and ev_j not in ev_i:
                        event_i["evidence"] = f"{ev_i}\n\nEvidence 2: {ev_j}".strip()
                        
                    tags_i = set(event_i.get("tags", []))
                    tags_j = set(event_j.get("tags", []))
                    event_i["tags"] = list(tags_i.union(tags_j))
                    event_i["rank"] = 4
                    
                    merged_indices.add(j)
                    
                    content_i = get_content(items[i]["file_path"])
                    content_j = get_content(items[j]["file_path"])
                    
                    content_i[items[i]["index"]] = event_i
                    modified_files.add(items[i]["file_path"])
                    content_j[items[j]["index"]] = None
                    modified_files.add(items[j]["file_path"])

    for path in modified_files:
        content = file_contents[path]
        cleaned_content = [item for item in content if item is not None]
        try:
            with open(path, 'w') as f:
                json.dump(cleaned_content, f, indent=2)
            logging.info(f"💾 Saved merged changes to {os.path.basename(path)}")
        except Exception as e:
            logging.error(f"Failed to save {path}: {e}")

def main():
    logging.info("--- Technical Gem Refinement Loop ---")
    
    # 1. Run Semantic Deduplication (Goal 6)
    try:
        deduplicate_gems()
    except Exception as e:
        logging.error(f"Deduplication check failed: {e}")
        
    # 2. Target the Brain (Hybrid Mode)
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
