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
    "index.html",
    "stories.html", 
    "timeline.html", 
    "files.html", 
    "status.html",
    "research.html",
    "protocols.html",
    "features.html",
    "intercom.html",
    "benchmarks.html"
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

def deploy_to_airlock():
    print("--- DEPLOYING TO PUBLIC AIRLOCK (www_deploy) ---")
    www_dir = os.path.expanduser("~/Dev_Lab/www_deploy")
    if os.path.exists(www_dir):
        for script in ["sync_protocols.sh", "sync_stories.sh", "sync_research.sh"]:
            script_path = os.path.join(www_dir, script)
            if os.path.exists(script_path):
                print(f"Running {script}...")
                try:
                    subprocess.run(["/bin/bash", script_path], check=True, cwd=www_dir)
                except Exception as e:
                    print(f"❌ Failed to execute {script}: {e}")

def main(args):
    print("=== FIELD NOTES BUILD SYSTEM v2.3 (Trailers Enabled) ===")
    
    # Rebuild dynamically compiled pages
    print("--- COMPILING DYNAMIC CONTENT ---")
    if args.benchmark:
        try:
            subprocess.run([sys.executable, os.path.join(BASE_DIR, "bench_models.py"), "--no-serve"], check=True)
        except Exception as e:
            print(f"❌ Failed to run bench_models.py: {e}")
        
    try:
        subprocess.run([sys.executable, os.path.join(BASE_DIR, "research_build.py")], check=True)
    except Exception as e:
        print(f"❌ Failed to run research_build.py: {e}")
        
    try:
        subprocess.run([sys.executable, os.path.join(BASE_DIR, "protocols_build.py")], check=True)
    except Exception as e:
        print(f"❌ Failed to run protocols_build.py: {e}")
        
    try:
        subprocess.run([sys.executable, os.path.join(BASE_DIR, "features_build.py")], check=True)
    except Exception as e:
        print(f"❌ Failed to run features_build.py: {e}")
        
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
        
        # [FEAT-222] Hardened Asset Replacement: Only target HTML attributes
        for filename, h in hashes.items():
            # Matches: href="style.css" or src="script.js?v=1.0"
            # Captures the attribute prefix (href=" or src=") to ensure we aren't in a JS string
            pattern = r'((?:href|src)=")' + re.escape(filename) + r'(\?v=[a-f0-9\.]+)?(")'
            new_val = r'\1' + f"{filename}?v={h}" + r'\3'
            content = re.sub(pattern, new_val, content)
            
        if True: # Force update to refresh mtime/cache
            with open(path, 'w') as f:
                f.write(content)
            print(f"Updated: {html_file}")

    if args.trailers:
        generate_trailers()

    if not args.no_deploy:
        deploy_to_airlock()

    print("=== BUILD COMPLETE ===")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--trailers", action="store_true", help="Generate cinematic widescreen previews")
    parser.add_argument("--benchmark", action="store_true", help="Run live model inference benchmarks (bench_models.py)")
    parser.add_argument("--no-deploy", action="store_true", help="Skip automatic airlock deployment")
    args = parser.parse_args()
    main(args)


