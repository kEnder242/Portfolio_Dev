# [FEAT-064] Static Site Synthesis (build_site.py)
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

def deploy_to_airlock(snapshots=False):
    print("--- DEPLOYING TO PUBLIC AIRLOCK (www_deploy) ---")
    # Resolve www_deploy at repository parent level: /home/jallred/Dev_Lab/www_deploy
    repo_root = os.path.dirname(os.path.dirname(BASE_DIR))
    www_dir = os.path.join(repo_root, "www_deploy")
    if not os.path.exists(www_dir):
        # Fallback to adjacent directory if run from another structure
        www_dir = os.path.join(os.path.dirname(BASE_DIR), "www_deploy")

    if os.path.exists(www_dir):
        # Sync json data files to public airlock data directory
        src_data = os.path.join(BASE_DIR, "data")
        dst_data = os.path.join(www_dir, "data")
        if os.path.exists(src_data):
            os.makedirs(dst_data, exist_ok=True)
            import shutil
            for item in os.listdir(src_data):
                s = os.path.join(src_data, item)
                d = os.path.join(dst_data, item)
                if os.path.isfile(s):
                    # Only copy if destination is missing or source is newer
                    if not os.path.exists(d) or os.path.getmtime(s) > os.path.getmtime(d):
                        shutil.copy2(s, d)

        env = os.environ.copy()
        if snapshots:
            env["ENABLE_SNAPSHOTS"] = "1"

        # [FEAT-461] Intelligent Sync: Run sync scripts only when internal source is newer than airlock target
        sync_map = {
            "sync_protocols.sh": (os.path.join(BASE_DIR, "protocols.html"), os.path.join(www_dir, "protocols.html")),
            "sync_stories.sh": (os.path.join(BASE_DIR, "stories.html"), os.path.join(www_dir, "stories.html")),
            "sync_research.sh": (os.path.join(BASE_DIR, "research.html"), os.path.join(www_dir, "research.html")),
            "sync_public_benchmarks.sh": (os.path.join(BASE_DIR, "public_benchmarks.html"), os.path.join(www_dir, "public_benchmarks.html")),
        }

        for script, (src_file, dst_file) in sync_map.items():
            script_path = os.path.join(www_dir, script)
            if os.path.exists(script_path):
                # Run if destination is missing or source file has been modified since last deploy
                needs_sync = not os.path.exists(dst_file) or (os.path.exists(src_file) and os.path.getmtime(src_file) > os.path.getmtime(dst_file))
                if needs_sync:
                    print(f"Running {script} (changes detected)...")
                    try:
                        subprocess.run(["/bin/bash", script_path], check=True, cwd=www_dir, env=env)
                    except Exception as e:
                        print(f"❌ Failed to execute {script}: {e}")
                else:
                    print(f"Skipping {script} (up to date).")
            else:
                print(f"⚠️ Warning: Sync script not found: {script_path}")
    else:
        print(f"⚠️ Warning: Public airlock deployment directory not found: {www_dir}")

    # [FEAT-456] Clean up lingering shot-scraper/chromium render processes
    try:
        subprocess.run(["/usr/bin/pkill", "-f", "shot-scraper|chromium"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

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
        print(f"❌ Critical Error in research_build.py: {e}")
        sys.exit(1)
        
    try:
        subprocess.run([sys.executable, os.path.join(BASE_DIR, "protocols_build.py")], check=True)
    except Exception as e:
        print(f"❌ Critical Error in protocols_build.py: {e}")
        sys.exit(1)
        
    try:
        subprocess.run([sys.executable, os.path.join(BASE_DIR, "features_build.py")], check=True)
    except Exception as e:
        print(f"❌ Critical Error in features_build.py: {e}")
        sys.exit(1)
        
    # [SPR-55] Hard-gate: verify FeatureTracker.md **Code:** links resolve (skip with --no-verify)
    if not args.no_verify:
        print("--- VERIFYING FEATURE CODE LINKS ---")
        verifier = os.path.join(BASE_DIR, "verify_feature_links.py")
        result = subprocess.run([sys.executable, verifier], check=False)
        if result.returncode != 0:
            print("❌ BUILD HALTED: FeatureTracker.md Code-field link drift detected. "
                  "Fix links or rerun with --no-verify to bypass.")
            sys.exit(1)
        print("✅ Feature code link verification passed.")
    else:
        print("--- SKIPPING FEATURE CODE LINK VERIFICATION (--no-verify) ---")
        
    # [FEAT-537] Generate untracked git_anchor.json for Live Web Intercom & test handshake validation
    git_anchor_path = os.path.join(BASE_DIR, "data/git_anchor.json")
    try:
        homelab_dir = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), "HomeLabAI")
        git_target_dir = homelab_dir if os.path.exists(homelab_dir) else BASE_DIR
        hr = subprocess.run(["git", "rev-parse", "--short=7", "HEAD"], capture_output=True, text=True, cwd=git_target_dir)
        git_commit = hr.stdout.strip() if hr.returncode == 0 and hr.stdout.strip() else "unknown"
        os.makedirs(os.path.dirname(git_anchor_path), exist_ok=True)
        import time
        import json
        with open(git_anchor_path + ".tmp", "w") as f:
            json.dump({"commit": git_commit, "timestamp": int(time.time()), "generator": "build_site.py"}, f, indent=2)
        os.replace(git_anchor_path + ".tmp", git_anchor_path)
        print(f"✅ Generated git_anchor.json (commit: {git_commit})")
    except Exception as e:
        print(f"⚠️ Warning: Could not generate git_anchor.json: {e}")

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
        
        # [FEAT-222 / FEAT-426] Hardened Asset Replacement: Target HTML attributes with any query string
        for filename, h in hashes.items():
            # Matches: href="style.css" or src="intercom_v2.js?v=anything"
            pattern = r'((?:href|src)=")' + re.escape(filename) + r'(\?v=[^"]+)?(")'
            new_val = r'\1' + f"{filename}?v={h}" + r'\3'
            content = re.sub(pattern, new_val, content)
            
        if True: # Force update to refresh mtime/cache
            with open(path, 'w') as f:
                f.write(content)
            print(f"Updated: {html_file}")

    if args.trailers:
        generate_trailers()

    deploy_to_airlock(snapshots=args.snapshots)

    print("=== BUILD COMPLETE ===")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshots", action="store_true", help="Generate shot-scraper PNG screenshots during deploy (disabled by default)")
    parser.add_argument("--trailers", action="store_true", help="Generate cinematic widescreen previews")
    parser.add_argument("--benchmark", action="store_true", help="Run live model inference benchmarks (bench_models.py)")
    parser.add_argument("--no-verify", action="store_true", help="Skip FeatureTracker.md Code-link verification hard gate")
    args = parser.parse_args()
    main(args)


