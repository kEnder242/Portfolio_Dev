import json
import os
import sys
import re

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ai_engine import get_engine
from nibble import extract_json_from_llm

ENGINE = get_engine(mode="LOCAL")
FILE_PATH = "raw_notes/notes_2024_PIAV.txt"

def debug_chunk():
    print(f"--- DEBUGGING 2024 ---")
    
    # 1. Read File
    try:
        with open(FILE_PATH, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read(8000) # Read first 8k chars (Header + Q1) 
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # 2. Construct Prompt (Matching nibble.py v1.5)
    prompt = f"""
    [ROLE]
    You are 'Pinky', an expert technical archivist.

    [DEBUG TASK]
    Analyze this raw text from 2024. 
    1. Extract technical events.
    2. **PRIVACY & REDACTION:**
       - **Public:** Technical work. REPLACE names/emails with `[REDACTED]`.
       - **Sensitive:** Personal feedback/Salary.
    
    [RAW TEXT]
    {text}
    
    [OUTPUT]
    JSON list: [ {{ "date": "YYYY-MM-DD", "summary": "...", "sensitivity": "Public" }} ]
    """
    
    print("\n[PROMPT SENT TO OLLAMA]")
    print(prompt[:500] + "... (truncated)")
    
    print("\n[WAITING FOR OLLAMA...]")
    try:
        response = ENGINE.generate(prompt)
    except Exception as e:
        print(f"Ollama Error: {e}")
        return

    print("\n[RAW RESPONSE]")
    print(response)
    
    print("\n[PARSED JSON]")
    data = extract_json_from_llm(response)
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    debug_chunk()
