import sys
import glob
import hashlib
import json
import os
import re
from pathlib import Path

# Add HomeLabAI/src to sys.path
_HOMELAB_SRC = Path(__file__).resolve().parent.parent.parent / "HomeLabAI" / "src"
if str(_HOMELAB_SRC) not in sys.path:
    sys.path.insert(0, str(_HOMELAB_SRC))

import psutil
try:
    from infra.status_model import StatusModel
except ImportError:
    StatusModel = None

from utils import DATA_DIR, RAW_NOTES_DIR

# Config
# Absolute GLOB paths using utils single-source-of-truth
NOTES_GLOB = os.path.join(RAW_NOTES_DIR, "**/*.txt")
DOCX_GLOB = os.path.join(RAW_NOTES_DIR, "**/*.docx")
RAS_GLOB = os.path.join(RAW_NOTES_DIR, "**/ras-*.txt")

QUEUE_FILE = os.path.join(DATA_DIR, "queue.json")
STATE_FILE = os.path.join(DATA_DIR, "chunk_state.json")
MANIFEST_FILE = os.path.join(DATA_DIR, "file_manifest.json")

GAP_FILES = [
    "notes_2005_SSPD.txt",
    "notes_2005.txt",
    "notes_2006_EPSD.txt",
    "Performance review 2008-2018.txt",
]


def is_gap_file(filename: str) -> bool:
    """Check if a file is an un-dated or sparse gap file requiring context envelope injection."""
    return (
        any(os.path.basename(g) == filename for g in GAP_FILES)
        or "notes_2005" in filename
        or "notes_2006" in filename
    )


def calculate_file_priorities(raw_notes_dir=RAW_NOTES_DIR, data_dir=DATA_DIR) -> list[dict]:
    """
    [FEAT-682] Density-Weighted Archive Queue Scheduling.
    Computes priority metric: Priority = max(epsilon, Total Lines / (Indexed Gems + 1)).
    Includes manifest gating (excluding raw hardware trace dumps) and multi-year gem aggregation.
    """
    epsilon = 0.001

    state_file = os.path.join(data_dir, "chunk_state.json")
    state = {}
    if os.path.exists(state_file):
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                state = json.load(f)
        except Exception:
            pass

    manifest_file = os.path.join(data_dir, "file_manifest.json")
    manifest = {}
    if os.path.exists(manifest_file):
        try:
            with open(manifest_file, "r", encoding="utf-8") as f:
                manifest = json.load(f)
        except Exception:
            pass

    gems_by_file = {}
    gems_by_year = {}
    for jf in glob.glob(os.path.join(data_dir, "20*.json")):
        try:
            with open(jf, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                y = os.path.basename(jf).split("_")[0].replace(".json", "")
                gems_by_year[y] = gems_by_year.get(y, 0) + len(data)
                for item in data:
                    if isinstance(item, dict):
                        src = item.get("source_file") or item.get("filename")
                        if src:
                            gems_by_file[src] = gems_by_file.get(src, 0) + 1
        except Exception:
            pass

    pattern_txt = os.path.join(raw_notes_dir, "**/*.txt")
    pattern_docx = os.path.join(raw_notes_dir, "**/*.docx")
    files = sorted(set(glob.glob(pattern_txt, recursive=True) + glob.glob(pattern_docx, recursive=True)))

    results = []
    for filepath in files:
        filename = os.path.basename(filepath)
        if filename.startswith("."):
            continue

        # [Bug #2 Fix: Manifest Gating]
        # Only index core engineering notes or manifest-approved logs; skip raw test dumps
        m_entry = manifest.get(filename, {})
        m_type = m_entry.get("type")
        is_core_note = (
            (filename.startswith("notes_") and filename.endswith(".txt"))
            or (filename.startswith("ras-") and filename.endswith(".txt"))
            or m_type in ("LOG", "META")
        )
        if not is_core_note or m_entry.get("manual_review") is True:
            continue

        try:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                lines = sum(1 for _ in f)
        except Exception:
            lines = 0

        chunks_in_state = sum(1 for k in state if k.startswith(f"{filename}::"))
        direct_gems = gems_by_file.get(filename, 0)

        # [Bug #1 Fix: Multi-Year Gem Aggregation]
        year_str = str(m_entry.get("year") or "")
        if "-" in year_str and year_str.replace("-", "").isdigit():
            p = year_str.split("-")
            span_years = [str(y) for y in range(int(p[0]), int(p[1]) + 1)]
            year_gems = sum(gems_by_year.get(y, 0) for y in span_years)
        else:
            year_match = re.search(r"20\d{2}", year_str or filename)
            year_gems = gems_by_year.get(year_match.group(0), 0) if year_match else 0

        indexed_gems = max(chunks_in_state, direct_gems, year_gems)

        if lines == 0:
            priority = epsilon
        else:
            priority = max(epsilon, lines / (indexed_gems + 1))

        results.append({
            "filename": filename,
            "filepath": filepath,
            "lines": lines,
            "gems": indexed_gems,
            "priority": round(priority, 4),
        })

    results.sort(key=lambda x: x["priority"], reverse=True)
    return results


def should_yield() -> bool:
    """Check if Scan Queue should yield due to non-idle mode, memory pressure, or high load."""
    if "--force" in sys.argv:
        return False
    # Check StatusModel for logical mode
    if StatusModel is not None:
        try:
            status_model = StatusModel()
            if status_model.state.get("logical", {}).get("mode") not in ("IDLE", None):
                print("[SCAN_QUEUE] Yielding: Non-IDLE mode detected")
                return True
        except Exception:
            pass

    # Check RAM
    ram_available_gb = psutil.virtual_memory().available / (1024**3)
    if ram_available_gb < 1.5:
        print(
            f"[SCAN_QUEUE] Yielding: Memory Pressure (Available RAM: {ram_available_gb:.1f} GB)"
        )
        return True

    # Check system load
    max_load = float(os.getenv("MAX_LOAD", 4.0))
    load_avg = psutil.getloadavg()[0]
    if load_avg > max_load:
        print(f"[SCAN_QUEUE] Yielding: High System Load (Load Avg: {load_avg:.1f} > {max_load})")
        return True

    return False


def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)


def read_file(path):
    try:
        if path.endswith(".docx"):
            import docx2txt

            return docx2txt.process(path)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return ""


def get_hash(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def parse_chunks(text, filename, file_type="LOG", fallback_year=None, return_envelopes=False):
    """
    Parses text into Month or Year buckets.
    Returns dict: {'YYYY-MM': 'content...'} or {'YYYY': 'content...'}
    If return_envelopes=True, returns tuple: (chunks, envelopes)
    where envelopes are scoped strictly to gap files ([FEAT-683] / [Story 109.7]).
    """
    if file_type == "META":
        year = fallback_year or "Unknown"
        chunks = {str(year): text}
        envelopes = {str(year): None}
        return (chunks, envelopes) if return_envelopes else chunks

    date_pattern = r"^(\d{1,2})/(\d{1,2})/(\d{2,4})"
    chunks = {}
    envelopes = {}
    gap = is_gap_file(filename)

    current_bucket = fallback_year or "Unknown"
    current_lines = []
    bucket_start_idx = 0
    all_lines = text.splitlines()

    for idx, line in enumerate(all_lines):
        match = re.match(date_pattern, line.strip())
        if match:
            month, day, year = match.groups()
            if len(year) == 2:
                year = "20" + year
            month = month.zfill(2)
            new_bucket = f"{year}-{month}"

            if current_lines:
                if current_bucket not in chunks:
                    chunks[current_bucket] = []
                chunks[current_bucket].append("\n".join(current_lines))
                if gap:
                    envelopes[current_bucket] = {
                        "before": all_lines[max(0, bucket_start_idx - 5):bucket_start_idx],
                        "after": all_lines[idx:min(len(all_lines), idx + 5)],
                    }
                else:
                    envelopes[current_bucket] = None

            current_bucket = new_bucket
            current_lines = [line]
            bucket_start_idx = idx
        else:
            current_lines.append(line)

    if current_lines:
        if current_bucket not in chunks:
            chunks[current_bucket] = []
        chunks[current_bucket].append("\n".join(current_lines))
        if gap:
            envelopes[current_bucket] = {
                "before": all_lines[max(0, bucket_start_idx - 5):bucket_start_idx],
                "after": all_lines[len(all_lines):len(all_lines)],
            }
        else:
            envelopes[current_bucket] = None

    joined_chunks = {k: "\n".join(v) for k, v in chunks.items()}
    if return_envelopes:
        return joined_chunks, envelopes
    return joined_chunks


def main():
    print("--- Scan Queue Manager v2.2 (Density-Weighted & Gap-Envelope Aware) ---")
    ensure_dirs()

    # [FEAT-682] Calculate Dynamic File Priorities
    file_priorities = calculate_file_priorities()
    prio_map = {p["filename"]: p["priority"] for p in file_priorities}
    print(f"[PRIORITY] Computed density-weighted priorities for {len(file_priorities)} files.")

    # Load Manifest
    if os.path.exists(MANIFEST_FILE):
        with open(MANIFEST_FILE, "r") as f:
            manifest = json.load(f)
    else:
        print("Warning: No manifest found. Run scan_librarian.py first.")
        manifest = {}

    # Load State
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
    else:
        state = {}

    # Load Existing Queue
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, "r") as f:
            try:
                queue = json.load(f)
            except:
                queue = []
    else:
        queue = []

    files = sorted(
        glob.glob(NOTES_GLOB, recursive=True)
        + glob.glob(RAS_GLOB, recursive=True)
        + glob.glob(DOCX_GLOB, recursive=True)
    )
    tasks_added = 0

    for filepath in files:
        filename = os.path.basename(filepath)

        # Classification Logic
        info = manifest.get(filename, {})
        file_type = info.get("type", "UNKNOWN")
        year_guess = info.get("year")

        # Rule: Process if it's a LOG or a META document
        should_process = file_type in ["LOG", "META"]

        # Fallback heuristic for un-manifested notes
        if not should_process and "notes_" in filename and "GIT" not in filename:
            should_process = True
            file_type = "LOG"

        if not should_process:
            continue

        text = read_file(filepath)
        if not text:
            continue

        # Chunking with optional envelope for gap files
        gap = is_gap_file(filename)
        chunks, envelopes = parse_chunks(
            text, filename, file_type=file_type, fallback_year=year_guess, return_envelopes=True
        )

        file_prio = round(prio_map.get(filename, 10.0), 3)

        for bucket_id, content in chunks.items():
            content_hash = get_hash(content)
            chunk_id = f"{filename}::{bucket_id}"

            # [FEAT-429] Poison Chunk Quarantine Protocol
            # Logic: Is this chunk NEW or CHANGED and NOT QUARANTINED?
            if state.get(f"{chunk_id}::status") == "QUARANTINED":
                continue
            if state.get(chunk_id) != content_hash:
                # Add to queue
                task = {
                    "id": chunk_id,
                    "filename": filename,
                    "bucket": bucket_id,
                    "type": file_type,
                    "priority": file_prio,
                    "is_gap_file": gap,
                    "content": content,
                }
                if envelopes.get(bucket_id):
                    task["context_envelope"] = envelopes[bucket_id]

                # Deduplicate queue
                if not any(t["id"] == chunk_id for t in queue):
                    queue.append(task)
                    tasks_added += 1
                    print(f"Queueing {chunk_id} ({file_type}) - Priority: {file_prio}")

    # Sort queue by priority DESC
    queue.sort(key=lambda x: x.get("priority", 10.0), reverse=True)

    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=2)

    print(f"\nQueue Updated. {tasks_added} new tasks. Total Pending: {len(queue)}")


if __name__ == "__main__":
    main()
