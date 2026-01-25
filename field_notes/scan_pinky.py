import requests
import json
import os
import glob
import re

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral:7b"

# Inputs
RESUME_PATH = "raw_notes/Jason Allred Resume - Jan 2026.txt"
FOCAL_OLD = "raw_notes/Performance review 2008-2018 .txt"
FOCAL_NEW = "raw_notes/11066402 Insights 2019-2024.txt"
NOTES_GLOB = "raw_notes/notes_*.txt"

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return ""

def ask_pinky(prompt, label=""):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_ctx": 8192  # Increased context window for heavier loads
        }
    }
    try:
        print(f"   > Pinky is thinking ({label})...")
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json()['response']
    except Exception as e:
        print(f"   ! Error calling Ollama: {e}")
        return "{}"

def extract_json(text):
    """Attempt to find and parse JSON in LLM response."""
    # Look for ```json ... ``` or just { ... }
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except:
            pass
    # Fallback: try to clean markdown
    text = text.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(text)
    except:
        return {"error": "Failed to parse JSON", "raw": text}

def main():
    print("--- Pinky Grand Scanner v2.0 ---")
    
    # 1. Load Strategic Context
    print(f"1. Loading Strategic Context...")
    resume = read_file(RESUME_PATH)
    focal_1 = read_file(FOCAL_OLD)
    focal_2 = read_file(FOCAL_NEW)
    
    strategic_context = f"""
    [RESUME SUMMARY]
    {resume[:3000]}

    [PERFORMANCE REVIEWS (STRATEGIC HISTORY)]
    {focal_1[:5000]}
    ...\n    {focal_2[:5000]}
    """
    
    # 2. Identify Target Files
    note_files = sorted(glob.glob(NOTES_GLOB))
    print(f"2. Found {len(note_files)} note files to process: {[os.path.basename(f) for f in note_files]}")

    master_index = {}

    # 3. Iterate and Process
    for note_file in note_files:
        filename = os.path.basename(note_file)
        # Extract year if possible (e.g. notes_2016_MVE.txt -> 2016)
        year_match = re.search(r'20\d{2}', filename)
        year = year_match.group(0) if year_match else "Unknown"
        
        print(f"\nProcessing {filename} ({year})...")
        notes_text = read_file(note_file)
        
        # We assume notes might be large, so we truncate to fit context if needed.
        # Mistral 7B has ~8k context usually, so let's be safe with ~12k chars of notes 
        # plus the strategic context.
        
        prompt = f"""
        [ROLE]
        You are 'Pinky', an expert technical archivist.

        [STRATEGIC CONTEXT]
        Use this Resume and Performance Review history to understand the user's career progression and high-level goals:
        {strategic_context[:4000]}\n
        [TASK]
        Analyze the following RAW NOTES from the year {year}.
        Correlate the raw technical work with the strategic context.
        
        Return a JSON object with this structure:
        {{
            "year": "{year}",
            "strategic_theme": "One sentence linking these notes to the performance review goals.",
            "technical_tags": ["Tag1", "Tag2"],
            "key_events": [
                {{ "date": "YYYY-MM-DD", "summary": "Event description", "evidence": "Quote from notes" }}
            ]
        }}

        [RAW NOTES {year}]
        {notes_text[:12000]}
        
        [OUTPUT]
        JSON only.
        """
        
        result_text = ask_pinky(prompt, label=year)
        data = extract_json(result_text)
        
        master_index[year] = data
        
        # Incremental Save
        with open("field_notes/pinky_index_full.json", "w") as f:
            json.dump(master_index, f, indent=2)

    print("\n--- SCAN COMPLETE ---")
    print(json.dumps(master_index, indent=2))

if __name__ == "__main__":
    main()