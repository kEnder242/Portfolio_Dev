import os
import sys
import time
import json
import re
import subprocess
import requests
import logging
import random
import glob
import argparse
import signal
import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import update_status, get_vram_usage, trigger_pager, ROUND_TABLE_LOCK, DATA_DIR

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LAB_RUN_DIR = os.path.expanduser("~/Dev_Lab/HomeLabAI/run")
MASS_SCAN_PID_FILE = os.path.join(LAB_RUN_DIR, "mass_scan.pid")
# [FEAT-101] Dual-Pipeline Synthesis & Load-Aware Nibbling
LIBRARIAN = os.path.join(BASE_DIR, "scan_librarian.py")
QUEUE_MGR = os.path.join(BASE_DIR, "scan_queue.py")
NIBBLER = os.path.join(BASE_DIR, "nibble_v2.py")
ARTIFACT_SCANNER = os.path.join(BASE_DIR, "scan_artifacts.py")
GEM_REFINER = os.path.join(BASE_DIR, "refine_gem.py")
CLEANER = os.path.join(BASE_DIR, "clean_duplicates.py")
AGGREGATOR = os.path.join(BASE_DIR, "aggregate_years.py")
QUEUE_FILE = os.path.join(DATA_DIR, "queue.json")
RAW_NOTES_DIR = os.path.join(os.path.dirname(BASE_DIR), "raw_notes")

# Config
VRAM_THRESHOLD = 0.95 # Allow up to 95% utilization
MAX_LOAD = 4.0        # True Slow Burn threshold
SLEEP_INTERVAL = 60   # Longer interval for polite background operation

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [MASS SCAN] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# [FEAT-330] Signal Throttling
IS_PAUSED = False

def handle_pause(signum, frame):
    global IS_PAUSED
    logging.warning("[GOVERNOR] Received PAUSE signal (SIGUSR1). Throttling execution...")
    IS_PAUSED = True

def handle_resume(signum, frame):
    global IS_PAUSED
    logging.info("[GOVERNOR] Received RESUME signal (SIGUSR2). Resuming execution...")
    IS_PAUSED = False

signal.signal(signal.SIGUSR1, handle_pause)
signal.signal(signal.SIGUSR2, handle_resume)

def atomic_write_text(path, content):
    """Atomically writes text content to path via a temp file + os.replace."""
    tmp_path = path + ".tmp"
    with open(tmp_path, "w") as f:
        f.write(content)
    os.replace(tmp_path, path)

def register_pid():
    """Writes the current PID to the Lab's run directory for Attendant tracking."""
    try:
        os.makedirs(LAB_RUN_DIR, exist_ok=True)
        atomic_write_text(MASS_SCAN_PID_FILE, str(os.getpid()))
        logging.info(f"Registered PID {os.getpid()} at {MASS_SCAN_PID_FILE}")
    except Exception as e:
        logging.error(f"Failed to register PID: {e}")

def wait_if_paused():
    """Polls the pause state and yields CPU if throttled."""
    while IS_PAUSED:
        time.sleep(5)

def vram_guard():
    usage = get_vram_usage()
    if usage > VRAM_THRESHOLD:
        logging.warning(f"VRAM usage high ({usage:.2f}). Waiting for cooling...")
        return False
    return True

def run_task(cmd_list):
    try:
        env = os.environ.copy()
        env["MAX_LOAD"] = "5.0"
        lab_root = os.path.dirname(os.path.dirname(BASE_DIR))
        homelab_src = os.path.join(lab_root, "HomeLabAI/src")
        curr_pp = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = f"{BASE_DIR}:{homelab_src}:{curr_pp}" if curr_pp else f"{BASE_DIR}:{homelab_src}"
        cwd = BASE_DIR
        subprocess.run([sys.executable] + cmd_list, check=True, env=env, cwd=cwd, timeout=1800)
        return True
    except Exception as e:
        logging.error(f"Task failed: {e}")
        return False

def get_low_rank_items():
    """Finds items that could benefit from re-reasoning."""
    items = []
    json_files = glob.glob(os.path.join(DATA_DIR, "*.json"))
    for jf in json_files:
        if any(x in jf for x in ["themes", "status", "queue", "state", "search_index", "pager_activity", "file_manifest"]): continue
        try:
            with open(jf, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    for event in data:
                        # Rank < 4 is a candidate for "refinement"
                        if event.get('rank', 2) < 4:
                            items.append({"file": jf, "event": event})
        except: pass
    return items

LOCK_ACQUIRE_TIMEOUT = 10.0

def wait_for_roundtable_lock(lock_path, timeout=LOCK_ACQUIRE_TIMEOUT):
    """Polls every 0.5s for the Round Table lock to clear, up to timeout seconds.
    Returns True if the lock cleared, False if it is still held."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if not check_lock(lock_path):
            return True
        time.sleep(0.5)
    return False

def lock_pid_alive(pid):
    """Returns True if the given PID is still alive, False otherwise.
    Non-int/empty values are treated as alive (True)."""
    try:
        pid = int(pid)
    except (TypeError, ValueError):
        return True
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False

def check_lock(lock_path):
    """Returns True if background tasks should yield to Intercom."""
    if os.path.exists(lock_path):
        # Check for stale lock (older than 30 mins for faster recovery)
        if time.time() - os.path.getmtime(lock_path) > 1800:
            logging.warning("[LOCK] Stale Round Table Lock detected (>30m). Ignoring.")
            return False
        # If the lock file holds a valid PID that is no longer alive, treat as stale
        try:
            with open(lock_path, 'r') as f:
                content = f.read().strip()
            if content:
                pid = int(content)
                if not lock_pid_alive(pid):
                    logging.warning(f"[LOCK] Round Table Lock PID {pid} is dead. Removing stale lock.")
                    try:
                        os.remove(lock_path)
                    except OSError as e:
                        logging.error(f"[LOCK] Failed to remove stale lock {lock_path}: {e}")
                    return False
        except (ValueError, OSError):
            # Empty or unreadable content: fall back to mtime check only
            pass
        return True
    return False

def hallway_protocol(keyword):
    """[FEAT-179] Targeted scan for the Hallway Protocol."""
    logging.info(f"=== HALLWAY PROTOCOL: Targeted Search for '{keyword}' ===")
    
    # 1. Grep for matching files in raw_notes
    try:
        # Use ripgrep or grep to find files containing the keyword
        cmd = ["grep", "-rl", keyword, RAW_NOTES_DIR]
        res = subprocess.run(cmd, capture_output=True, text=True)
        files = res.stdout.strip().split("\n") if res.stdout else []
        
        if not files or (len(files) == 1 and files[0] == ''):
            logging.info(f"No raw notes found matching '{keyword}'.")
            return
        
        # Limit to top 5 for fast response
        target_files = files[:5]
        logging.info(f"Found {len(files)} matches. Scanning top {len(target_files)}...")
        
        # 2. Force these files into the nibbler
        for f in target_files:
            rel_path = os.path.relpath(f, RAW_NOTES_DIR)
            logging.info(f"Deep Harvesting: {rel_path}")
            # We use --reasoning mode for high-fidelity extraction
            run_task([NIBBLER, "--reasoning", "--file", f])
            
    except Exception as e:
        logging.error(f"Hallway Protocol failed: {e}")

def synthesize_career_mesh():
    """[FEAT-438] Indexes raw notes and gems against resume.txt to update Tier 2 Keyword Mesh without inflating Tier 1 Bedrock."""
    compass_file = os.path.join(DATA_DIR, "career_compass.json")
    resume_file = os.path.expanduser("~/study/references/resume.txt")
    if not os.path.exists(compass_file):
        logging.warning("[COMPASS] career_compass.json not found. Skipping synthesis.")
        return

    try:
        with open(compass_file, 'r') as f:
            compass = json.load(f)
        
        # Load resume terms if available
        resume_text = ""
        if os.path.exists(resume_file):
            with open(resume_file, 'r') as f:
                resume_text = f.read()

        keywords = set(compass.get("tier_2_keyword_mesh", {}).get("keywords", []))
        
        # Extract potential technical terms from resume
        if resume_text:
            found_terms = re.findall(r'\b[A-Z0-9]{2,10}\b', resume_text)
            for t in found_terms:
                if len(t) >= 2 and not t.isdigit() and t not in ["AND", "THE", "FOR", "WITH", "FROM", "OUT"]:
                    keywords.add(t)

        # Scan processed JSONs for matching high-rank terms
        json_files = glob.glob(os.path.join(DATA_DIR, "*.json"))
        for jf in json_files:
            fname = os.path.basename(jf)
            if any(x in fname for x in ["status", "themes", "queue", "state", "search_index", "pager_activity", "file_manifest", "career_compass"]):
                continue
            try:
                with open(jf, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        for ev in data:
                            summary = str(ev.get("summary", ""))
                            techs = re.findall(r'\b[A-Z0-9]{3,10}\b', summary)
                            for tech in techs:
                                if tech in resume_text or tech in keywords:
                                    keywords.add(tech)
            except Exception:
                pass

        # Update Tier 2 Mesh
        tier_2 = compass.get("tier_2_keyword_mesh", {})
        tier_2["keywords"] = sorted(list(keywords))
        tier_2["last_scanned"] = time.strftime("%Y-%m-%d %H:%M:%S")
        compass["tier_2_keyword_mesh"] = tier_2

        # Atomic write
        tmp_file = compass_file + ".tmp"
        with open(tmp_file, 'w') as f:
            json.dump(compass, f, indent=2)
        os.replace(tmp_file, compass_file)
        logging.info(f"[COMPASS] Successfully synthesized Tier 2 Keyword Mesh ({len(keywords)} terms). Tier 1 Anchor Map preserved.")
    except Exception as e:
        logging.error(f"[COMPASS] Failed to synthesize career mesh: {e}")

def distill_journal_ledger():
    """[FEAT-161] Distills all Rank 4 and Rank 5 technical gems into instruction-tuning conversation pairs for train_expert.py."""
    ledger_file = os.path.join(DATA_DIR, "journal_ledger.jsonl")
    json_files = glob.glob(os.path.join(DATA_DIR, "20*.json"))
    
    existing_dialogues = set()
    preserved_entries = []
    if os.path.exists(ledger_file):
        try:
            with open(ledger_file, "r") as f:
                for line in f:
                    if line.strip():
                        item = json.loads(line)
                        d = str(item.get("dialogue", "")).strip()
                        # Only preserve complete conversational pairs with responses
                        if d and ("Pinky:" in d or "Assistant:" in d) and d not in existing_dialogues:
                            existing_dialogues.add(d)
                            preserved_entries.append(item)
        except Exception as e:
            logging.warning(f"[DISTILL] Failed reading existing ledger: {e}")

    extracted_count = 0
    new_entries = []
    for jf in sorted(json_files):
        if "_" in os.path.basename(jf):
            continue  # Skip raw month fragments; use consolidated yearly archives
        try:
            with open(jf, "r") as f:
                events = json.load(f)
            if not isinstance(events, list):
                continue
            
            for ev in events:
                rank = ev.get("rank", 0)
                if rank >= 4:
                    summary = str(ev.get("summary") or "").strip()
                    evidence = str(ev.get("evidence") or "").strip()
                    tech_gem = str(ev.get("technical_gem") or "").strip()
                    date_str = str(ev.get("date") or "").strip()
                    
                    if not summary and not tech_gem:
                        continue
                    
                    finding = tech_gem if tech_gem else summary
                    ev_text = evidence if evidence else "Historical telemetry evidence."
                    raw_trigger = str(ev.get("trigger_context") or "").strip()
                    trigger = raw_trigger if raw_trigger else f"What was the technical milestone and validation finding for {summary}?"
                    anchors = ev.get("anchors", [])
                    anchor_text = f"\nAnchors: {', '.join(anchors)}" if isinstance(anchors, list) and anchors else ""
                    dialogue_text = f"User: {trigger} ({date_str})\nPinky: In {date_str}, the milestone was: {finding}\n\nEvidence: {ev_text}{anchor_text}"
                    
                    if dialogue_text not in existing_dialogues:
                        existing_dialogues.add(dialogue_text)
                        new_entries.append({
                            "ts": int(time.time()),
                            "dialogue": dialogue_text,
                            "rank": rank,
                            "date": date_str
                        })
                        extracted_count += 1
        except Exception as e:
            logging.warning(f"[DISTILL] Error parsing {jf}: {e}")

    # 2. Harvest standalone code artifacts and scripts from artifacts_*.json
    artifact_files = glob.glob(os.path.join(DATA_DIR, "artifacts_*.json"))
    for af in sorted(artifact_files):
        try:
            with open(af, "r") as f:
                art_items = json.load(f)
            if not isinstance(art_items, list):
                continue
            
            for item in art_items:
                fname = str(item.get("filename") or "").strip()
                synopsis = str(item.get("synopsis") or "").strip()
                category = str(item.get("category") or "Engineering Tool").strip()
                rank = item.get("rank", 3)
                
                if not fname or not synopsis:
                    continue
                
                # Pair 1: Forward Tool Identification
                d1 = f"User: What is the {fname} tool and how is it used?\nPinky: {fname} is a {category} in Jason's technical portfolio. Purpose: {synopsis}"
                if d1 not in existing_dialogues:
                    existing_dialogues.add(d1)
                    new_entries.append({"ts": int(time.time()), "dialogue": d1, "rank": rank, "type": "artifact_tool"})
                    extracted_count += 1
                
                # Pair 2: Reverse Category Search (Jeopardy Style)
                d2 = f"User: What tools did Jason develop for {category}?\nPinky: For {category}, Jason developed {fname}. Synopsis: {synopsis}"
                if d2 not in existing_dialogues:
                    existing_dialogues.add(d2)
                    new_entries.append({"ts": int(time.time()), "dialogue": d2, "rank": rank, "type": "artifact_category"})
                    extracted_count += 1
        except Exception as e:
            logging.warning(f"[DISTILL] Error parsing artifact file {af}: {e}")

    total_entries = preserved_entries + new_entries
    if total_entries:
        lines = [json.dumps(entry) + "\n" for entry in total_entries]
        atomic_write_text(ledger_file, "".join(lines))
        logging.info(f"✨ [DISTILL] Updated journal_ledger.jsonl: {len(total_entries)} total pairs ({extracted_count} newly harvested from gems & code artifacts).")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword", help="Run a targeted Hallway Protocol scan.")
    parser.add_argument("--once", action="store_true", help="Run a single epoch pass and exit cleanly.")
    args = parser.parse_args()

    if args.keyword:
        hallway_protocol(args.keyword)
        return

    # [FEAT-330] Register for physical governance
    register_pid()

    logging.info("=== MASS SCAN: CONTINUOUS RESEARCH v2.0 ===")
    trigger_pager("Initiating High-Fidelity Synthesis Burn.", severity="info", source="MassScan")
    
    lock_path = ROUND_TABLE_LOCK
    maint_lock = os.path.join(DATA_DIR, "maintenance.lock")

    epoch_count = 0
    while True:
        # [FEAT-330] Yield to physical governor
        wait_if_paused()

        # --- [FEAT-259.1] TOP LEVEL LOCK CHECKS ---
        if os.path.exists(maint_lock):
            logging.info("[LOCK] Maintenance Lock Active. Silencing all background tasks.")
            update_status("IDLE", "Maintenance Active. Scanner yielded.")
            time.sleep(300)
            continue

        if check_lock(lock_path):
            logging.info("[LOCK] Round Table Active. Entering Low-Power Wait...")
            update_status("WAITING", "Round Table Active. Scanner yielded.")
            if not wait_for_roundtable_lock(lock_path):
                time.sleep(300) # Wait 5 minutes
            continue

        epoch_count += 1
        logging.info(f"--- Starting Epoch {epoch_count} ---")
        update_status("ONLINE", f"Starting Epoch {epoch_count}...")
        
        # 1. Update Manifest
        run_task([LIBRARIAN])
        
        # 2. Update Queue
        run_task([QUEUE_MGR])

        # 3. Artifact Map Refresh (Hybrid/Brain Mode)
        # Only run if there is work or if specifically requested
        # 3. Artifact Map Refresh
        logging.info("Step 3: Refreshing Artifact Map (Hybrid Mode)...")
        years = ['DOCS', '2024', '2023', '2022', '2021', '2020', '2019']
        for idx, year in enumerate(years):
            if check_lock(lock_path) or os.path.exists(maint_lock): break
            while not vram_guard(): 
                update_status("WAITING", "VRAM Cooling...")
                time.sleep(60)
            
            progress = int((idx / len(years)) * 100)
            logging.info(f"Scanning Artifact Sector: {year} (Brain) [{progress}%]")
            update_status("ONLINE", f"Scanning Artifacts: {year}", progress_pct=progress)
            run_task([ARTIFACT_SCANNER, year, "--hybrid"])
        
        if check_lock(lock_path) or os.path.exists(maint_lock): continue

        # 4. Notes Fast Burn
        logging.info("Step 4: Consuming Note Queue...")
        initial_queue_size = 0
        if os.path.exists(QUEUE_FILE):
            try:
                with open(QUEUE_FILE, 'r') as f:
                    queue = json.load(f)
                    initial_queue_size = len(queue)
            except: queue = []

            while queue:
                if check_lock(lock_path) or os.path.exists(maint_lock): break
                
                while not vram_guard(): 
                    update_status("WAITING", "VRAM Cooling...")
                    time.sleep(60)
                
                task = queue[0]
                remaining = len(queue)
                progress = 100
                if initial_queue_size > 0:
                    progress = int(((initial_queue_size - remaining) / initial_queue_size) * 100)
                
                logging.info(f"Processing: {task['id']} ({remaining} remaining) [{progress}%]")
                update_status("BUSY", f"Nibbling: {task['id']}", filename=task['filename'], progress_pct=progress)
                
                use_hybrid = "2024" in task['bucket'] or "PIAV" in task['filename']
                flag = "--hybrid" if use_hybrid else "--reasoning"
                
                if run_task([NIBBLER, flag]):
                    time.sleep(SLEEP_INTERVAL)
                else:
                    time.sleep(60)
                
                # Reload queue
                with open(QUEUE_FILE, 'r') as f:
                    queue = json.load(f)

        if check_lock(lock_path) or os.path.exists(maint_lock): continue

        # 5. Eternal Slow Burn (Refinement Loop)
        # [POLITENESS] Window-bounded: refine low-rank items during 3:00 AM – 5:00 AM window
        items_to_refine = get_low_rank_items()
        if items_to_refine:
            logging.info(f"Step 5: Refining {len(items_to_refine)} items (Active Window: 3:00 AM – 5:00 AM)...")
            for i, item in enumerate(items_to_refine):
                if check_lock(lock_path) or os.path.exists(maint_lock): break
                
                # [FEAT-416] 05:00 AM Maintenance Cutoff: leave 1-hour buffer for trailing tasks and aggregation
                now = datetime.datetime.now()
                if 5 <= now.hour < 22:
                    logging.info(f"Step 5.1: 05:00 AM maintenance cutoff reached ({now.strftime('%H:%M:%S')}). Gracefully yielding refinement loop.")
                    break
                
                while not vram_guard(): 
                    update_status("WAITING", "VRAM Cooling...")
                    time.sleep(60)
                logging.info(f"Step 5.1: Refining Gem [{i+1}/{len(items_to_refine)}]...")
                update_status("ONLINE", f"Refining Gem {i+1}/{len(items_to_refine)}")
                if run_task([GEM_REFINER]):
                    time.sleep(SLEEP_INTERVAL)
                else:
                    time.sleep(120) 

        if check_lock(lock_path): continue

        # 6. Final TLC: De-duplicate, Aggregate and Tidy
        logging.info("Step 6: Performing Archive TLC (De-duplication & Aggregation)...")
        update_status("ONLINE", "Tidying Archive...")
        run_task([CLEANER])
        run_task([AGGREGATOR])
        synthesize_career_mesh()
        distill_journal_ledger()

        logging.info(f"Epoch {epoch_count} complete. Pulsing Pager.")
        update_status("IDLE", f"Epoch {epoch_count} complete.")
        trigger_pager(f"Epoch {epoch_count} Synthesis Complete. Lab is Idle.", severity="info", source="MassScan")
        if args.once:
            trigger_pager("Nightly Dialogue Summary: Refinement & Dream Synthesis Complete.", severity="info", source="nightly-dialogue")
            logging.info("Single epoch requested (--once). Exiting cleanly.")
            break
        time.sleep(600) # Wait 10 mins before next full manifest check

if __name__ == "__main__":
    main()

