import json
import re
import os
import glob

def clean_json():
    DATA_DIR = "field_notes/data"
    SEARCH_INDEX_FILE = "field_notes/search_index.json"
    ACRONYM_MAP_FILE = "field_notes/acronym_map.json"

    # 1. Load Current Search Index
    print(f"Loading {SEARCH_INDEX_FILE}...")
    try:
        with open(SEARCH_INDEX_FILE, "r") as f:
            search_index = json.load(f)
    except FileNotFoundError:
        search_index = {}

    # 2. Map of War Stories to Years (Heuristic)
    article_year_map = {
        "visa-tool": ["2015", "2016"],
        "xslt-parsing": ["2015", "2016"],
        "config-file": ["2015", "2016"],
        "fleet-scale": ["2018"],
        "cygwin-wall": ["2006"],
        "ti-basic": ["1998"], 
        "quakecon": ["2001"],
        "reading-robot": ["2016"], 
        "rapl-matplotlib": ["2019"],
        "rakp-security": ["2013"],
        "rmcp-optimization": ["2006"],
        "texas-power-on": ["2022"], 
        "failed-demo": ["2013"],
        "negative-testing": ["2024"] 
    }

    # 3. Merge Decentralized Data (Continuous Burn Output)
    print("Scanning data directory for new tags...")
    json_files = glob.glob(os.path.join(DATA_DIR, "*.json"))
    ignore = ["themes.json", "status.json", "queue.json", "state.json", "search_index.json", "pager_activity.json", "file_manifest.json"]
    
    for jf in json_files:
        if os.path.basename(jf) in ignore: continue
        
        # Extract year from filename (e.g., 2024.json or 2024_01.json)
        year_match = re.search(r'(\d{4})', os.path.basename(jf))
        if not year_match: continue
        year = year_match.group(1)
        
        try:
            with open(jf, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    for event in data:
                        tags = event.get('tags', [])
                        if tags:
                            map_tags_to_articles(tags, year, article_year_map, search_index)
        except: pass

    # 4. Merge Acronym Map (Hunter Scan)
    print("Merging Acronym Map...")
    try:
        with open(ACRONYM_MAP_FILE, "r") as f:
            acronym_map = json.load(f)
            
        for acr, years in acronym_map.items():
            for year in years:
                map_tags_to_articles([acr], year, article_year_map, search_index)
    except FileNotFoundError:
        print(f"No {ACRONYM_MAP_FILE} found, skipping.")

    # 5. Save Final Index
    with open(SEARCH_INDEX_FILE, "w") as f:
        # Sort keys for cleanliness
        sorted_index = {k: sorted(list(set(v))) for k, v in sorted(search_index.items())}
        json.dump(sorted_index, f, indent=2)

    print(f"Cleaned JSON and merged decentralized indices into {SEARCH_INDEX_FILE}.")

def map_tags_to_articles(tags, year, article_map, search_index):
    # Find articles for this year
    relevant_articles = []
    for art_id, years in article_map.items():
        if str(year) in years:
            relevant_articles.append(art_id)
    
    if not relevant_articles: return

    for tag in tags:
        tag_lower = tag.lower()
        if tag_lower not in search_index:
            search_index[tag_lower] = []
        
        # Add unique articles
        for art in relevant_articles:
            if art not in search_index[tag_lower]:
                search_index[tag_lower].append(art)

if __name__ == "__main__":
    clean_json()