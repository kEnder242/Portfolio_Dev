#!/usr/bin/env python3
"""
gem_refinement_runner.py
4-Hour Continuous Gem Extraction and Epistemic Refinement Loop.
Monitors queue, nibbles notes chunks via priority, refines existing gems,
aggregates master annual tables, and outputs live telemetry.
"""

import os
import sys
import time
import json
import subprocess
import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
QUEUE_FILE = DATA_DIR / "queue.json"
STOP_LOCK = DATA_DIR / "stop_refinement.lock"
TELEMETRY_FILE = DATA_DIR / "refinement_run_telemetry.json"
LOG_FILE = BASE_DIR / "gem_refinement_runner.log"

MAX_RUN_SECONDS = 4 * 3600  # 4 hours


def log_msg(msg: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    print(formatted, flush=True)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(formatted + "\n")
    except Exception:
        pass


def count_master_gems():
    total = 0
    by_year = {}
    for y in range(2005, 2026):
        ypath = DATA_DIR / f"{y}.json"
        if ypath.exists():
            try:
                with open(ypath) as f:
                    d = json.load(f)
                    if isinstance(d, list):
                        by_year[str(y)] = len(d)
                        total += len(d)
            except Exception:
                pass
    return total, by_year


def update_telemetry(start_time, loop_count, last_action, error_count=0):
    now = time.time()
    elapsed = now - start_time
    remaining = max(0, MAX_RUN_SECONDS - elapsed)

    queue_len = 0
    if QUEUE_FILE.exists():
        try:
            with open(QUEUE_FILE) as f:
                q = json.load(f)
                if isinstance(q, list):
                    queue_len = len(q)
        except Exception:
            pass

    total_gems, by_year = count_master_gems()

    telemetry = {
        "status": "RUNNING" if remaining > 0 else "COMPLETED",
        "start_time": datetime.datetime.fromtimestamp(start_time).isoformat(),
        "last_heartbeat": datetime.datetime.fromtimestamp(now).isoformat(),
        "elapsed_seconds": round(elapsed, 1),
        "remaining_seconds": round(remaining, 1),
        "loop_count": loop_count,
        "queue_length": queue_len,
        "total_master_gems": total_gems,
        "gems_by_year": by_year,
        "last_action": last_action,
        "error_count": error_count,
    }

    try:
        with open(TELEMETRY_FILE, "w") as f:
            json.dump(telemetry, f, indent=2)
    except Exception as e:
        log_msg(f"Failed to update telemetry: {e}")


def main():
    if STOP_LOCK.exists():
        STOP_LOCK.unlink()

    start_time = time.time()
    log_msg(f"=== Starting 4-Hour Gem Refinement Loop (PID {os.getpid()}) ===")
    log_msg(f"Target duration: {MAX_RUN_SECONDS}s ({MAX_RUN_SECONDS / 3600:.1f} hours)")

    loop_count = 0
    error_count = 0

    while time.time() - start_time < MAX_RUN_SECONDS:
        if STOP_LOCK.exists():
            log_msg("Stop lock detected. Gracefully terminating runner.")
            break

        loop_count += 1
        log_msg(f"--- Refinement Loop #{loop_count} (Elapsed: {round(time.time() - start_time, 1)}s) ---")

        # 1. Queue Health & Top-Up
        queue_len = 0
        if QUEUE_FILE.exists():
            try:
                with open(QUEUE_FILE) as f:
                    q = json.load(f)
                    queue_len = len(q) if isinstance(q, list) else 0
            except Exception:
                queue_len = 0

        if queue_len < 3:
            log_msg("Queue low (<3 tasks). Repopulating via scan_queue.py...")
            update_telemetry(start_time, loop_count, "repopulating_queue", error_count)
            try:
                subprocess.run([sys.executable, str(BASE_DIR / "scan_queue.py")], check=True, timeout=60)
            except Exception as e:
                log_msg(f"scan_queue.py error: {e}")
                error_count += 1

        # 2. Nibble Batch (Process top priority tasks)
        log_msg("Running nibble_v2 batch (limit=3)...")
        update_telemetry(start_time, loop_count, "nibbling", error_count)
        try:
            res = subprocess.run(
                [sys.executable, str(BASE_DIR / "nibble_v2.py"), "--force", "--fast", "--limit=3"],
                capture_output=True,
                text=True,
                timeout=300,
            )
            if res.returncode != 0:
                log_msg(f"nibble_v2 error (exit {res.returncode}): {res.stderr[-300:]}")
                error_count += 1
            else:
                log_msg("nibble_v2 completed batch successfully.")
        except Exception as e:
            log_msg(f"nibble_v2 execution failure: {e}")
            error_count += 1

        # 3. Epistemic Gem Refinement (dedup, elevate, link)
        log_msg("Running refine_gem pass (epochs=1, batch_size=5)...")
        update_telemetry(start_time, loop_count, "refining_gems", error_count)
        try:
            res = subprocess.run(
                [sys.executable, str(BASE_DIR / "refine_gem.py"), "--epochs=1", "--batch-size=5"],
                capture_output=True,
                text=True,
                timeout=120,
            )
            if res.returncode != 0:
                log_msg(f"refine_gem error: {res.stderr[-200:]}")
                error_count += 1
        except Exception as e:
            log_msg(f"refine_gem execution failure: {e}")
            error_count += 1

        # 4. Aggregation & Shard Consolidation
        log_msg("Aggregating monthly shards into master annual tables...")
        update_telemetry(start_time, loop_count, "aggregating_years", error_count)
        try:
            subprocess.run(
                [sys.executable, str(BASE_DIR / "aggregate_years.py")],
                capture_output=True,
                timeout=60,
            )
        except Exception as e:
            log_msg(f"aggregate_years error: {e}")
            error_count += 1

        # 5. Extract Latest Synthesis Gems
        try:
            subprocess.run(
                [sys.executable, str(BASE_DIR / "extract_latest_gems.py")],
                capture_output=True,
                timeout=30,
            )
        except Exception:
            pass

        update_telemetry(start_time, loop_count, "idle_pause", error_count)
        time.sleep(5)  # Yield pause between loops

    log_msg("=== 4-Hour Gem Refinement Loop Finished ===")
    update_telemetry(start_time, loop_count, "finished", error_count)


if __name__ == "__main__":
    main()
