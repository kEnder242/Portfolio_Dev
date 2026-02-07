import os
import hashlib
import re
import shutil

# Config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets") # Not really used, files are in root
SOURCE_FILES = ["style.css", "script.js", "intercom_v2.js"]
HTML_FILES = [
    "stories.html", 
    "timeline.html", 
    "files.html", 
    "pager.html", 
    "intercom/index.html"
]

def get_hash(filepath):
    if not os.path.exists(filepath): return None
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]

def main():
    print("=== FIELD NOTES BUILD SYSTEM v1.0 ===")
    
    hashes = {}
    for filename in SOURCE_FILES:
        # Some files might be in root, some in subdirs? 
        # Current project has them in field_notes/
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
            # Pattern 1: style.css?v=10.3
            # Pattern 2: style.css (no version)
            # Pattern 3: style.[hash].css (if we already did it)
            
            # We will use the Query String approach but AUTOMATED via hash.
            # This ensures no broken links if build fails halfway.
            # It's also cleaner for a static server.
            
            pattern = re.escape(filename) + r'(\?v=[a-f0-9]+)?'
            new_val = f"{filename}?v={h}"
            content = re.sub(pattern, new_val, content)
            
        if content != original_content:
            with open(path, 'w') as f:
                f.write(content)
            print(f"Updated: {html_file}")

    print("=== BUILD COMPLETE ===")

if __name__ == "__main__":
    main()
