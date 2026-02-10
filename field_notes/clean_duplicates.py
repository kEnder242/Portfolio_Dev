import json
import os
import glob
import logging

# Config
DATA_DIR = "Portfolio_Dev/field_notes/data"
logging.basicConfig(level=logging.INFO, format='[CLEAN] %(message)s')

def clean_duplicates():
    logging.info("--- Starting Archive De-Duplication ---")
    
    json_files = glob.glob(os.path.join(DATA_DIR, "*.json"))
    ignore = ["themes.json", "status.json", "queue.json", "state.json", "search_index.json", "pager_activity.json", "file_manifest.json"]
    
    total_removed = 0
    
    for jf in json_files:
        if os.path.basename(jf) in ignore: continue
        
        try:
            with open(jf, 'r') as f:
                data = json.load(f)
            
            if not isinstance(data, list): continue
            
            original_count = len(data)
            unique_data = []
            seen = set()
            
            for item in data:
                # Create a fingerprint: Date + Normalized Summary
                # We strip trailing punctuation and whitespace for better matching
                summary_norm = item.get('summary', '').strip().lower().rstrip('.')
                evidence_norm = item.get('evidence', '').strip().lower().rstrip('.')
                fingerprint = f"{item.get('date')}|{summary_norm}|{evidence_norm[:100]}"
                
                if fingerprint not in seen:
                    unique_data.append(item)
                    seen.add(fingerprint)
            
            new_count = len(unique_data)
            removed = original_count - new_count
            
            if removed > 0:
                logging.info(f"File: {os.path.basename(jf)} | Removed {removed} duplicates.")
                total_removed += removed
                with open(jf, 'w') as f:
                    json.dump(unique_data, f, indent=2)
                    
        except Exception as e:
            logging.error(f"Failed to clean {os.path.basename(jf)}: {e}")

    logging.info(f"--- De-Duplication Complete. Total removed: {total_removed} ---")

if __name__ == "__main__":
    clean_duplicates()
