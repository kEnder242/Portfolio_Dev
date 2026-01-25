import requests
import json
import os
import glob
import re

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral:7b"
NOTES_GLOB = "raw_notes/notes_*.txt"

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        return ""

def ask_pinky(chunk):
    prompt = f"""
    [TASK]
    Scan the following engineering notes and extract a list of TECHNICAL ACRONYMS (2-6 uppercase letters).
    
    [CRITERIA]
    - MUST be technical (e.g., RTL, OCLA, TCL, BMC, IPMI, JTAG, PCIE, DDR).
    - IGNORE common words (e.g., THE, AND, FOR, TODO, NOTE, FYI).
    - IGNORE specific names if they aren't tools (e.g., JASON, MIKE).
    
    [INPUT TEXT]
    {chunk[:4000]}
    
    [OUTPUT]
    Return ONLY a JSON list of strings. Example: ["RTL", "OCLA", "TCL"]
    """
    
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1}
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        text = response.json()['response']
        # Extract JSON list from text
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        return []
    except Exception as e:
        return []

def main():
    print("--- Acronym Hunter v1.1 ---")
    files = sorted(glob.glob(NOTES_GLOB))
    
    file_acronyms = {}
    
    for filepath in files:
        filename = os.path.basename(filepath)
        print(f"Scanning {filename}...", end="", flush=True)
        text = read_file(filepath)
        
        acronyms = ask_pinky(text)
        file_acronyms[filename] = acronyms
        
        print(f" Found {len(acronyms)}")

    # Filter against a basic stoplist just in case Pinky slipped

    # Filter against a basic stoplist just in case Pinky slipped
    stoplist = {"THE", "AND", "FOR", "BUT", "NOT", "YES", "CAN", "SEE", "USE", "GET", "NEW", "OLD", "NOW", "ONE", "TWO", "BUG", "FIX", "RAN", "RUN"}
    
    # Invert the map: Acronym -> List of Years
    acronym_map = {}
    
    for filename, acr_list in file_acronyms.items():
        # Extract year
        year_match = re.search(r'20\d{2}', filename)
        year = year_match.group(0) if year_match else "Unknown"
        
        for acr in acr_list:
            clean_acr = acr.upper().strip()
            if re.match(r'^[A-Z0-9]{2,8}$', clean_acr) and clean_acr not in stoplist:
                if clean_acr not in acronym_map:
                    acronym_map[clean_acr] = set()
                acronym_map[clean_acr].add(year)

    # Convert sets to lists for JSON
    final_map = {k: sorted(list(v)) for k, v in acronym_map.items()}
    
    print("\n--- CANDIDATE ACRONYM MAP ---")
    print(json.dumps(final_map, indent=2))
    
    # Save for merge
    with open("field_notes/acronym_map.json", "w") as f:
        json.dump(final_map, f, indent=2)

if __name__ == "__main__":
    main()
