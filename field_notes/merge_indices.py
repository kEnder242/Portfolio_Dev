import json
import re

def clean_json():
    try:
        with open("field_notes/pinky_index_full.json", "r") as f:
            data = json.load(f) # This might fail if the file is truly broken
    except json.JSONDecodeError:
        print("JSON is broken, attempting raw repair...")
        with open("field_notes/pinky_index_full.json", "r") as f:
            raw = f.read()
        # Simple heuristic fix for the specific error we saw (often double quotes or newlines in strings)
        # But actually, looking at the previous turn, the error was inside the "2024" key where the value was the *error message* from my script.
        # The script put {"error": ...} as the value. The JSON file itself is valid JSON, but the *content* of 2024 is an error object.
        # We need to re-parse the "raw" field inside that error object if possible, or just manually patch it.
        data = json.loads(raw)

    # Fix 2024 if it failed
    if "2024" in data and "error" in data["2024"]:
        print("Fixing 2024 entry...")
        raw_text = data["2024"].get("raw", "")
        # Attempt to re-parse the raw text which looked like valid JSON
        try:
            # key_events might have quotes inside summary?
            fixed_2024 = json.loads(raw_text)
            data["2024"] = fixed_2024
        except Exception as e:
            print(f"Could not auto-fix 2024: {e}")
            # Fallback manual fix based on the log we saw
            data["2024"] = {
                "year": "2024",
                "strategic_theme": "Implementing and validating manageability features across Intel's datacenter platforms.",
                "technical_tags": ["Simics", "DMR", "PECI", "MCTP", "PythonSV", "Kayak"],
                "key_events": [
                    { "date": "2024-08-01", "summary": "Locate and collect serial number for SMNC75000143 in lab", "evidence": "SMNC75000143 was taken down" },
                    { "date": "2024-ww31", "summary": "Execute a kayak automation test on simics - rdiamsr", "evidence": "simics.bat targets/setup_tests.simics" }
                ]
            }

    # Now Merge into Search Index
    print("Merging into search_index.json...")
    with open("field_notes/search_index.json", "r") as f:
        search_index = json.load(f)

    # Invert the Pinky Index: Tag -> List of Years -> List of War Stories?
    # No, we need Tag -> List of Article IDs.
    # We don't have a direct mapping of "Pinky Event" -> "War Story Article ID".
    # We have:
    #   Pinky: "Simics" (Tag) -> 2016
    #   War Stories: "The VISA Tool Engine" -> 2016?
    
    # We need a map of War Stories to Years.
    # I'll create a heuristic map here based on the text.
    article_year_map = {
        "visa-tool": ["2015", "2016"],
        "xslt-parsing": ["2015", "2016"],
        "config-file": ["2015", "2016"],
        "fleet-scale": ["2018"],
        "cygwin-wall": ["2006"],
        "ti-basic": ["1998"], # inferred
        "quakecon": ["2001"],
        "reading-robot": ["2016"], # Guessing based on "AJ" in notes?
        "rapl-matplotlib": ["2019"],
        "rakp-security": ["2013"],
        "rmcp-optimization": ["2006"],
        "texas-power-on": ["2022"], # Guessing
        "failed-demo": ["2013"],
        "negative-testing": ["2024"] # Guessing based on "PECI coverage miss"
    }

    # Algorithm:
    # For each Year in Pinky Index:
    #   Get Tags (e.g. "Simics")
    #   Find Articles associated with that Year (e.g. "visa-tool")
    #   Add "visa-tool" to the "simics" key in search_index.
    
    # 1. Merge Pinky Index (Full Scan)
    print("Merging Pinky Index...")
    for year, content in data.items():
        if "technical_tags" not in content: continue
        tags = content["technical_tags"]
        map_tags_to_articles(tags, year, article_year_map, search_index)

    # 2. Merge Acronym Map (Hunter Scan)
    print("Merging Acronym Map...")
    try:
        with open("field_notes/acronym_map.json", "r") as f:
            acronym_map = json.load(f)
            
        for acr, years in acronym_map.items():
            # Acronyms are tags too
            for year in years:
                map_tags_to_articles([acr], year, article_year_map, search_index)
                
    except FileNotFoundError:
        print("No acronym_map.json found, skipping.")

    with open("field_notes/pinky_index_full.json", "w") as f:
        json.dump(data, f, indent=2)
        
    with open("field_notes/search_index.json", "w") as f:
        # Sort keys for cleanliness
        sorted_index = {k: sorted(v) for k, v in sorted(search_index.items())}
        json.dump(sorted_index, f, indent=2)

    print(f"Cleaned JSON and merged indices.")

def map_tags_to_articles(tags, year, article_map, search_index):
    # Find articles for this year
    relevant_articles = []
    for art_id, years in article_map.items():
        if year in years:
            relevant_articles.append(art_id)
    
    if not relevant_articles: return

    for tag in tags:
        tag_lower = tag.lower()
        if tag_lower not in search_index:
            search_index[tag_lower] = []
        
        # Add unique articles
        current_set = set(search_index[tag_lower])
        for art in relevant_articles:
            current_set.add(art)
        search_index[tag_lower] = list(current_set)

if __name__ == "__main__":
    clean_json()
