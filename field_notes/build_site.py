import os
import hashlib
import re
import shutil
import argparse
import subprocess
import sys

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
TRAILERS_DIR = os.path.join(BASE_DIR, "assets/trailers")

def get_hash(filepath):
    if not os.path.exists(filepath): return None
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]

def generate_trailers():
    print("--- GENERATING STATIC TRAILERS ---")
    os.makedirs(TRAILERS_DIR, exist_ok=True)
    
    # Cinematic JS: Hide sidebar, expand content
    overlay_js = "document.getElementById('sidebar').style.display='none'; document.querySelector('main').style.padding='40px'; document.querySelector('main').style.maxWidth='100%';"
    
    # Use the absolute path to the local shot-scraper binary in the venv
    shot_scraper_bin = os.path.join(os.path.dirname(BASE_DIR), ".venv/bin/shot-scraper")

    for html_file in HTML_FILES:
        output_name = html_file.replace(".html", "_trailer.jpg")
        output_path = os.path.join(TRAILERS_DIR, output_name)
        input_url = f"http://localhost:9001/{html_file}"
        
        print(f"Capturing {html_file}...")
        try:
            cmd = [
                shot_scraper_bin, "shot", input_url,
                "--width", "1920", "--height", "800",
                "--javascript", overlay_js,
                "--output", output_path,
                "--quality", "80"
            ]
            subprocess.run(cmd, check=True)
            print(f"✅ Trailer saved: {output_name}")
        except Exception as e:
            print(f"❌ Failed to capture {html_file}: {e}")

def main(args):
    print("=== FIELD NOTES BUILD SYSTEM v2.1 (Trailers Enabled) ===")
    
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

    if args.trailers:
        generate_trailers()

    print("=== BUILD COMPLETE ===")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--trailers", action="store_true", help="Generate cinematic widescreen previews")
    args = parser.parse_args()
    main(args)
