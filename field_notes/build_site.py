import os
import hashlib
import re
import shutil

# Config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_FILES = ["style.css", "script.js", "intercom_v2.js", "mission-control.js"]
HTML_FILES = [
    "stories.html", 
    "timeline.html", 
    "files.html", 
    "status.html",
    "research.html",
    "intercom.html"
]

def get_hash(filepath):
    if not os.path.exists(filepath): return None
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]

def main():
    print("=== FIELD NOTES BUILD SYSTEM v2.0 (Modular) ===")
    
    hashes = {}
    for filename in SOURCE_FILES:
        path = os.path.join(BASE_DIR, filename)
        h = get_hash(path)
        if h:
            hashes[filename] = h
            print(f"Hash for {filename}: {h}")

    for html_file in HTML_FILES:
        path = os.path.join(BASE_DIR, html_file)
        if not os.path.exists(path):
            print(f"Skipping missing file: {html_file}")
            continue
            
        with open(path, 'r') as f:
            content = f.read()
            
        original_content = content
        
        # Replace v=X.X or hashed names
        for filename, h in hashes.items():
            pattern = re.escape(filename) + r'(\?v=[a-f0-9\.]+)?'
            new_val = f"{filename}?v={h}"
            content = re.sub(pattern, new_val, content)
            
        if content != original_content:
            with open(path, 'w') as f:
                f.write(content)
            print(f"Updated: {html_file}")

    print("=== BUILD COMPLETE ===")

if __name__ == "__main__":
    main()