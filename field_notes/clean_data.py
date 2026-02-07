import json
import os
import sys
import re
from ai_engine import get_engine

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

ENGINE = get_engine(mode="LOCAL")
DATA_DIR = "field_notes/data"

def clean_file(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r') as f:
        data = json.load(f)

    if not isinstance(data, list) or len(data) == 0:
        return

    print(f"--- Cleaning {filename} ({len(data)} items) ---")
    
    # Group by rough date or keyword similarity
    # For Unknown.json, let's just group everything and ask the model to consolidate
    
    # Process in batches of 10 to avoid token limits
    batch_size = 10
    cleaned_data = []
    
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        
        prompt = f"""
        [TASK]
        Act as a data hygiene expert. Below is a list of technical events extracted from logs.
        Identify and MERGE duplicate or near-duplicate events. 
        A duplicate is an event that describes the same technical win, tool release, or bug fix, even if the phrasing is slightly different.
        
        [EVENTS]
        {json.dumps(batch, indent=2)}
        
        [RULES]
        1. Keep the most detailed description and evidence.
        2. Combine tags.
        3. If dates are different (e.g., 2019-01-01 vs 2019-01-07) but it's the same tool release, pick the more specific date.
        4. Return ONLY a JSON list of cleaned events.
        
        [OUTPUT FORMAT]
        [
          {{ "date": "...", "summary": "...", "evidence": "...", "sensitivity": "Public", "tags": [] }}
        ]
        """
        
        print(f"   > Processing batch {i//batch_size + 1}...")
        response = ENGINE.generate(prompt)
        
        # Extract JSON list
        match = re.search(r'\[.*\]', response, re.DOTALL)
        if match:
            try:
                cleaned_batch = json.loads(match.group(0))
                cleaned_data.extend(cleaned_batch)
            except:
                print("   ! Error parsing JSON response.")
                cleaned_data.extend(batch) # Keep original if failed
        else:
            cleaned_data.extend(batch)

    # Final de-dupe check (exact summary match)
    final_list = []
    seen = set()
    for item in cleaned_data:
        key = (item.get('date'), item.get('summary'))
        if key not in seen:
            final_list.append(item)
            seen.add(key)

    # Atomic write
    temp_file = filepath + ".tmp"
    with open(temp_file, 'w') as f:
        json.dump(final_list, f, indent=2)
    os.replace(temp_file, filepath)
    print(f"--- Done. Reduced to {len(final_list)} items. ---")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
        clean_file(target)
    else:
        # Default to Unknown.json
        clean_file("Unknown.json")