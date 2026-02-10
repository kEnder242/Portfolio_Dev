import os
import json
import logging

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
EXPERTISE_DIR = os.path.join(DATA_DIR, "expertise")
OUTPUT_FILE = os.path.join(DATA_DIR, "artifacts_EXPERTISE.json")

logging.basicConfig(level=logging.INFO, format='[EXPERTISE SCAN] %(message)s')

def scan_expertise():
    logging.info("Indexing Expertise Hierarchy...")
    artifacts = []
    
    if not os.path.exists(EXPERTISE_DIR):
        logging.warning("Expertise directory missing.")
        return

    # Categories: telemetry, manageability, validation
    categories = os.listdir(EXPERTISE_DIR)
    for cat in categories:
        cat_path = os.path.join(EXPERTISE_DIR, cat)
        if os.path.isdir(cat_path):
            files = os.listdir(cat_path)
            for f in files:
                if f.endswith(".md"):
                    file_path = os.path.join(cat_path, f)
                    
                    # Quick metadata extraction
                    with open(file_path, 'r') as file:
                        lines = file.readlines()
                        synopsis = "Master Blueprint"
                        for line in lines:
                            if line.startswith("#"):
                                synopsis = line.replace("#", "").strip()
                                break
                    
                    artifacts.append({
                        "filename": f,
                        "synopsis": synopsis,
                        "type": "Blueprint",
                        "rank": 5, # Expertise docs are always top rank
                        "category": cat,
                        "method": "Expert",
                        "keywords": [cat, "BKM", "Blueprint"]
                    })

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(artifacts, f, indent=2)
    
    logging.info(f"✅ Success: Indexed {len(artifacts)} blueprints.")

if __name__ == "__main__":
    scan_expertise()
