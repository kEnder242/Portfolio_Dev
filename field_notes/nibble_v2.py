import datetime
import difflib
import hashlib
import json
import logging
import os
import re
import sys
import time

import psutil
import subprocess

# Add current directory and HomeLabAI/src to path
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
LAB_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))
HOMELAB_SRC = os.path.join(LAB_ROOT, "HomeLabAI/src")
for p in [BASE_DIR, HOMELAB_SRC]:
    if p not in sys.path:
        sys.path.append(p)

from ai_engine_v2 import get_engine_v2
from infra.status_model import StatusModel
from refine_gem import classify_impact_level, disentangle_chronology
from scrub_all_passwords import sanitize_text as sanitize_credentials, sanitize_with_tripwire
from utils import DATA_DIR, can_burn, update_status

# Config
QUEUE_FILE = os.path.join(DATA_DIR, "queue.json")
STATE_FILE = os.path.join(DATA_DIR, "chunk_state.json")
AUDIT_FILE = os.path.join(DATA_DIR, "privacy_audit.jsonl")
STATUS_FILE = os.path.join(DATA_DIR, "status.json")

# Setup Logging
LOG_FILE = os.path.join(DATA_DIR, "pinky_v2.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler(sys.stdout)],
)

_MANIFEST_CACHE = None


def get_file_manifest():
    global _MANIFEST_CACHE
    if _MANIFEST_CACHE is None:
        manifest_path = os.path.join(DATA_DIR, "file_manifest.json")
        if os.path.exists(manifest_path):
            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    _MANIFEST_CACHE = json.load(f)
            except Exception:
                _MANIFEST_CACHE = {}
        else:
            _MANIFEST_CACHE = {}
    return _MANIFEST_CACHE


def log(msg):
    logging.info(msg)


# AI & Metrics
REASONING_MODE = "--reasoning" in sys.argv
HYBRID_MODE = "--hybrid" in sys.argv
FAST_MODE = "--fast" in sys.argv
FORCE_MODE = "--force" in sys.argv
engine_mode = "LOCAL"
if HYBRID_MODE:
    engine_mode = "HYBRID"
elif REASONING_MODE:
    engine_mode = "REASONING"

ENGINE = get_engine_v2(mode=engine_mode)
MAX_LOAD = float(os.environ.get("MAX_LOAD", 4.0))


def check_foyer_intercom_active() -> bool:
    """[Story 110.3 / BKM-086] Check if an interactive Foyer intercom/WebSocket session is active.
    
    Inspects established TCP sockets on port 8765 or existence of /tmp/foyer_intercom.lock.
    Yields True if active, signaling Nibbler to immediately yield.
    """
    try:
        res = subprocess.run(
            ["ss", "-t", "state", "established", "( sport = :8765 or dport = :8765 )"],
            capture_output=True,
            text=True,
            timeout=2,
        )
        lines = [
            line.strip()
            for line in res.stdout.strip().split("\n")
            if line.strip() and not line.startswith("Recv-Q")
        ]
        if len(lines) > 0:
            return True
    except Exception:
        pass

    if os.path.exists("/tmp/foyer_intercom.lock"):
        return True

    return False


def should_yield() -> bool:
    """Check if Nibbler should yield due to non-idle mode, memory pressure, high load, or active intercom."""
    if FORCE_MODE:
        return False

    # Check Foyer Intercom Preemption (Sprint 110.0 / Story 110.3)
    if check_foyer_intercom_active():
        log("[NIBBLER] Yielding: Active Foyer Intercom session detected on port 8765 / lock")
        return True

    if FAST_MODE:
        ram_available_gb = psutil.virtual_memory().available / (1024**3)
        return ram_available_gb < 0.8

    # Check StatusModel for logical mode
    status_model = StatusModel()
    if status_model.state["logical"]["mode"] != "IDLE":
        log("[NIBBLER] Yielding: Non-IDLE mode detected")
        return True

    # Check RAM (Nibbler footprint is ~30MB; 1.5GB available provides 50x safety headroom)
    ram_available_gb = psutil.virtual_memory().available / (1024**3)
    if ram_available_gb < 1.5:
        log(
            f"[NIBBLER] Yielding: Memory Pressure (Available RAM: {ram_available_gb:.1f} GB < 1.5 GB)"
        )
        return True

    # Check system load against MAX_LOAD
    load_avg = psutil.getloadavg()[0]
    if load_avg > MAX_LOAD:
        log(f"[NIBBLER] Yielding: High System Load (Load Avg: {load_avg:.1f} > {MAX_LOAD})")
        return True

    return False


# FEAT-428 Progressive Cooldown State
CONSECUTIVE_YIELDS = 0


def check_system_load():
    global CONSECUTIVE_YIELDS
    if FAST_MODE:
        CONSECUTIVE_YIELDS = 0
        return True
    ready, reason = can_burn(max_load=MAX_LOAD)
    if not ready:
        CONSECUTIVE_YIELDS += 1
        if CONSECUTIVE_YIELDS == 1:
            log(f"[FEAT-428] Cooldown Tier 1 ({reason}). Sleeping 15s...")
            time.sleep(15)
        elif CONSECUTIVE_YIELDS == 2:
            log(f"[FEAT-428] Cooldown Tier 2 ({reason}). Sleeping 60s...")
            time.sleep(60)
        else:
            if CONSECUTIVE_YIELDS == 3:
                log(
                    f"[FEAT-428] Cooldown Tier 3 ({reason}). Entering COOLDOWN mode (sleeping 15m)..."
                )
            time.sleep(900)
        return False
    else:
        if CONSECUTIVE_YIELDS > 0:
            log(
                f"[FEAT-428] System load clear. Cooldown reset (was {CONSECUTIVE_YIELDS})."
            )
        CONSECUTIVE_YIELDS = 0
        return True


def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    return []


def save_json(path, data):
    tmp_path = str(path) + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp_path, path)


def extract_json_from_llm(text):
    """
    [FEAT-131] Robust JSON Extraction.
    Hunts for JSON blocks amidst conversational filler.
    """
    if not text:
        logging.info("   [DEBUG] LLM returned empty/None response.")
        return []

    # Log raw for debugging if it's not JSON
    if not text.strip().startswith(("[", "{")):
        logging.info(f"   [DEBUG] Raw LLM Response (First 100 chars): {text[:100]}...")

    # Try to find a list [ ... ]
    list_match = re.search(r"(\[.*\])", text, re.DOTALL)
    if list_match:
        try:
            data = json.loads(list_match.group(1))
            return data if isinstance(data, list) else [data]
        except:
            pass

    # Try to find a dict { ... } and wrap it in a list
    dict_match = re.search(r"(\{.*\})", text, re.DOTALL)
    if dict_match:
        try:
            data = json.loads(dict_match.group(1))
            if isinstance(data, dict) and not data:  # Ignore empty {}
                return []
            return [data] if isinstance(data, dict) else data
        except:
            pass

    # Last resort: strip markdown and attempt raw load
    clean = text.replace("```json", "").replace("```", "").strip()
    try:
        data = json.loads(clean)
        if isinstance(data, dict) and not data:
            return []
        return [data] if isinstance(data, dict) else data
    except:
        pass

    # [FEAT-131] Truncation Recovery: extract any valid JSON objects from partial streams
    recovered = []
    for m in re.finditer(r"\{[^{}]*\}", text, re.DOTALL):
        try:
            obj = json.loads(m.group(0))
            if isinstance(obj, dict) and obj:
                recovered.append(obj)
        except:
            pass
    return recovered


def validate_date(date_str):
    if not date_str:
        return None
    date_str = str(date_str).strip()
    # Check YYYY-MM-DD or YYYY-DD-MM
    m_iso = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})$", date_str)
    if m_iso:
        y, m, d = int(m_iso.group(1)), int(m_iso.group(2)), int(m_iso.group(3))
        if m > 12 and 1 <= d <= 12:
            m, d = d, m
        if 1 <= m <= 12 and 1 <= d <= 31:
            return f"{y:04d}-{m:02d}-{d:02d}"
        return None

    # Check MM/DD/YYYY or DD/MM/YYYY
    match = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", date_str)
    if match:
        p1, p2, y = int(match.group(1)), int(match.group(2)), int(match.group(3))
        if p1 > 12 and 1 <= p2 <= 12:
            m, d = p2, p1
        elif 1 <= p1 <= 12 and 1 <= p2 <= 31:
            m, d = p1, p2
        else:
            return None
        return f"{y:04d}-{m:02d}-{d:02d}"
    return None


def is_semantic_duplicate(new_event, existing_events, threshold=0.70):
    """
    [Story 109.14 / FEAT-454] Evidence-aware semantic duplicate checker.
    Rejects duplicate extractions of the same raw snippet on the same date/chunk/year.
    """
    if isinstance(new_event, str):
        new_summary = new_event
        new_evidence = ""
        new_date = None
    else:
        new_summary = new_event.get("summary", "")
        new_evidence = new_event.get("evidence", "")
        new_date = new_event.get("date") or new_event.get("event_date")

    norm_new_ev = re.sub(r"[^a-z0-9\s]", "", str(new_evidence).lower()).strip()
    norm_new_sum = str(new_summary).lower().strip()

    for ex in existing_events:
        ex_summary = str(ex.get("summary", "")).lower().strip()
        ex_evidence = ex.get("evidence", "")
        ex_date = ex.get("date") or ex.get("event_date")
        norm_ex_ev = re.sub(r"[^a-z0-9\s]", "", str(ex_evidence).lower()).strip()

        # 1. Evidence overlap check (Raw quote provenance takes highest precedence)
        if norm_new_ev and norm_ex_ev:
            if norm_new_ev == norm_ex_ev:
                return True
            if len(norm_new_ev) >= 15 and len(norm_ex_ev) >= 15:
                if norm_new_ev in norm_ex_ev or norm_ex_ev in norm_new_ev:
                    return True
            if difflib.SequenceMatcher(None, norm_new_ev, norm_ex_ev).ratio() > 0.75:
                return True
            t1, t2 = set(norm_new_ev.split()), set(norm_ex_ev.split())
            if t1 and t2 and (len(t1 & t2) / len(t1 | t2)) > 0.60:
                return True

        # 2. Summary fuzzy & token check (scoped to same date or unanchored dates)
        same_date = (new_date and ex_date and new_date == ex_date) or (not new_date or not ex_date)
        if same_date:
            if difflib.SequenceMatcher(None, norm_new_sum, ex_summary).ratio() > threshold:
                return True
            s1, s2 = set(norm_new_sum.split()), set(ex_summary.split())
            if s1 and s2 and (len(s1 & s2) / len(s1 | s2)) > 0.55:
                return True

    return False


def scrub_input_buffer(text):
    """
    [VIBE-008] Structural Guillotine.
    Drops forbidden sections based on headers.
    """
    FORBIDDEN_HEADERS = [
        r"AREAS FOR IMPROVEMENT",
        r"AREAS FOR DEVELOPMENT",
        r"Results Coaching",
        r"Behaviors Coaching",
        r"Behaviors Feedback",
        r"Coach\b",
        r"Growth Feedback",
    ]

    SAFE_HEADERS = [
        r"Next Year's Technical Strategy",
        r"Future Goals",
        r"Technical Strategy",
        r"Strategic Focal Points",
        r"Architecture Plans",
    ]

    lines = text.splitlines()
    clean_lines = []
    is_dropped = False

    for line in lines:
        # Check if we should drop
        if any(
            re.search(pattern, line, re.IGNORECASE) for pattern in FORBIDDEN_HEADERS
        ):
            logging.info(
                f"   [GUILLOTINE] Dropping section starting at: {line.strip()[:50]}..."
            )
            is_dropped = True
            continue

        # Check if we should resume
        if is_dropped and any(
            re.search(pattern, line, re.IGNORECASE) for pattern in SAFE_HEADERS
        ):
            logging.info(
                f"   [GUILLOTINE] Resuming at safe header: {line.strip()[:50]}..."
            )
            is_dropped = False

        if not is_dropped:
            clean_lines.append(line)

    return "\n".join(clean_lines)


def main():
    log(f"--- Pinky Nibbler v2.1 (Reasoning: {REASONING_MODE}) ---")

    # --- CLI FLAGS & SPARSE CADENCE (Story 110.3 / FEAT-416 / BKM-086) ---
    # Default limit is 2 chunks per execution for balanced sparse ingestion
    limit = 2
    if "--once" in sys.argv:
        limit = 1
    elif "--all" in sys.argv:
        limit = 999
    for arg in sys.argv:
        if arg.startswith("--limit="):
            limit = int(arg.split("=")[1])

    # Preemption check before queue loading
    if should_yield():
        log("[POLITENESS] Intake yielded to system conditions or active Foyer Intercom.")
        update_status("IDLE", "Nibbler yielded (load or active intercom).")
        return

    if not os.path.exists(QUEUE_FILE):
        update_status("IDLE", "Queue empty.")
        return

    with open(QUEUE_FILE, "r") as f:
        queue = json.load(f)

    if not queue:
        update_status("IDLE", "Queue empty.")
        return

    # Load State for De-duping
    state = load_json(STATE_FILE)
    if isinstance(state, list):
        state = {}  # Safety for corrupted state

    processed_this_run = 0
    while queue and processed_this_run < limit:
        task = queue.pop(0)
        processed_this_run += 1

        # --- HASH DE-DUPING ---
        content_hash = hashlib.md5(task["content"].encode("utf-8")).hexdigest()
        if state.get(task["id"]) == content_hash:
            log(f"   > Skipping {task['id']} (Hash match)")
            continue

        # --- IDLE-ONLY & RAM/LOAD SENTINEL ---
        if should_yield():
            log("[NIBBLER] Yielding due to system conditions")
            time.sleep(30)
            continue

        # --- POLITENESS CHECK ---
        while should_yield():
            update_status("YIELD", "Nibbler Yielding (Lock/Load)", filename=task["id"])
            time.sleep(10)

        log(f"Nibbling: {task['id']} ({task['bucket']})")

        # [VIBE-008] Apply structural guillotine to all content
        scrubbed_content = scrub_input_buffer(task["content"])

        fname = task.get("filename", "")
        bucket_str = str(task.get("bucket", ""))
        manifest = get_file_manifest()
        manifest_entry = manifest.get(fname, {})
        span_str = str(manifest_entry.get("year") or "")

        # [FEAT-128] Strategic Prompt selection
        file_type = task.get("type", "LOG")
        is_deep_connect = task.get("mode") == "DEEP_CONNECT"
        prompt = ""

        if is_deep_connect:
            strategic_context = task.get("strategic_context", "General Technical DNA")
            prompt = f"""
            [ROLE] You are 'Pinky', a high-fidelity technical forensic investigator.
            [STRATEGIC SEEDS] {strategic_context}
            [TASK] Perform 'Reverse RAG'. Analyze the RAW LOGS to find specific 'Technical Evidence'.
            1. Harvest high-density technical blocks (50-100 words).
            2. Focus on: Error traces, register values, post-mortem logic.
            Return a JSON list of EVIDENCE pairs:
            [
              {{
                "date": "YYYY-MM-DD", 
                "summary": "...", 
                "evidence": "...", 
                "tags": ["technical", "evidence", "lora_candidate"]
              }}
            ]
            """
        elif file_type == "META":
            prompt = f"""
            [TASK] Expert Career Strategist. Analyze this high-level document and extract the core strategic anchor.
            [EXCLUSION] EXCLUDE all behavioral feedback, coaching, or personal growth plans. Focus exclusively on technical milestones and strategic focal points.
            [YEAR] {task['bucket']}
            [CONTENT]
            {scrubbed_content[:4000]}
            
            [OUTPUT]
            Generate a JSON list containing ONE high-value entry.
            Prefix the summary with [STRATEGIC_ANCHOR].
# [FEAT-129] The Philosophical Core
            The summary should capture the primary focal point, philosophical shift, or major career milestone.
            
            [FORMAT]
            [
              {{ 
                "date": "{task['bucket']}-01-01", 
                "summary": "[STRATEGIC_ANCHOR] ...", 
                "evidence": "...", 
                "sensitivity": "Public", 
                "tags": ["strategy", "anchor"] 
              }}
            ]
            """
        else:
            # [Story 109.16 / Story 110.1 / INS-052] Calibrated Confidentiality & Machine-Log Boundary
            era_context_str = f"Document Era: {span_str}." if span_str else ""
            prompt = f"""[ROLE] You are an automated systems engineering log parser.
[TASK] Extract purely technical systems operations, CLI commands, hardware registers, and lab diagnostics.
DO NOT extract human personnel notes, manager appraisals, performance reviews, or career feedback.

[TAXONOMY DOMAINS]
Allowed domains: ['hardware_debug', 'operations', 'logistics']

[SANITIZATION LAW - BKM-015 / INS-052]
When copying commands or logs into 'evidence', strip all passwords, tokens, API keys, basic auth credentials, and device serial numbers. Replace any credential or serial value with "[REDACTED]" or "[REDACTED_PASSWORD]".
NEVER include passwords in curl commands (-u, -sku, --user, or basic auth URLs).

[EXAMPLES]
Input: "curl -f -u sys_admin:P@ssw0rd99! https://artifactory.corp/builds"
Output evidence: "curl -f -u sys_admin:[REDACTED_PASSWORD] https://artifactory.corp/builds"

Input: "curl -k -u 'debuguser:0penBmc1' https://localhost:5443/redfish"
Output evidence: "curl -k -u 'debuguser:[REDACTED_PASSWORD]' https://localhost:5443/redfish"

Input: "curl -H 'Authorization: Bearer secret_token_123' https://api.internal/deploy"
Output evidence: "curl -H 'Authorization: Bearer [REDACTED]' https://api.internal/deploy"

Input: "Board check: SN: J83920-A in slot 1 confirmed"
Output evidence: "Board check: SN: [REDACTED] in slot 1 confirmed"

[TEMPORAL CONTEXT]
Source Document: {fname}
{era_context_str}
Note: Events must be dated within or relative to this documented era. Do not convert hostnames, port numbers, or bug IDs into future dates.

Log content:
{scrubbed_content[:4000]}

[OUTPUT]
Return ONLY a valid JSON list of event objects:
[
  {{
    "date": "YYYY-MM-DD",
    "summary": "Technical summary",
    "evidence": "Command or register line with credentials redacted",
    "domain": "hardware_debug",
    "tags": ["tag1", "tag2"]
  }}
]"""

        try:
            if file_type == "META":
                # Meta documents always use the strategic anchor prompt
                response = ENGINE.generate(prompt, options={"num_predict": 1024})
            elif REASONING_MODE and hasattr(ENGINE, "generate_with_reasoning"):
                response = ENGINE.generate_with_reasoning(
                    scrubbed_content, task["bucket"]
                )
            else:
                response = ENGINE.generate(prompt, options={"num_predict": 1024})

            new_events = extract_json_from_llm(response)
        except Exception as e:
            log(f"   ! Engine Error: {e}")
            new_events = []

        if isinstance(new_events, list) and len(new_events) > 0:
            added_count = 0
            # [Story 109.16 / Pillar 1 & 2] Canonical Lakehouse Routing:
            # Target storage is strictly DATA_DIR/{event_year}.json, completely decoupled from task bucket.
            events_by_target_year: dict[str, list[dict]] = {}

            for event in new_events:
                if not isinstance(event, dict):
                    continue

                # [BKM-061 / INS-052] Deterministic Credentials Redaction
                for fld in ["summary", "evidence", "trigger_context"]:
                    if fld in event and isinstance(event[fld], str):
                        raw_val = event[fld]
                        clean_val, escaped, rules = sanitize_with_tripwire(raw_val)
                        if escaped:
                            ledger_path = os.path.join(DATA_DIR, "sanitization_escape_ledger.jsonl")
                            entry = {
                                "timestamp": datetime.now().isoformat(),
                                "file_source": task.get("file", "UNKNOWN"),
                                "field": fld,
                                "raw_snippet": raw_val,
                                "redacted_snippet": clean_val,
                                "matched_rules": rules,
                                "loop_id": "LOOP-006",
                            }
                            try:
                                with open(ledger_path, "a", encoding="utf-8") as lf:
                                    lf.write(json.dumps(entry) + "\n")
                            except Exception:
                                pass
                            log(f"[LOOP-006] Sanitization escape: field={fld} rules={rules}")
                        event[fld] = clean_val

                # Use provided date or fallback
                raw_date = event.get("date", "")
                clean_date = validate_date(raw_date)

                # Auto-assign bucket date if missing or invalid
                if not clean_date:
                    bucket_str = str(task.get("bucket", "")).split("::")[0]
                    if "-" in bucket_str:
                        parts = bucket_str.split("-")
                        if len(parts) >= 2 and len(parts[1]) == 4:
                            clean_date = f"{parts[0]}-01-01"
                        elif len(parts) >= 2 and len(parts[1]) <= 2:
                            clean_date = f"{parts[0]}-{parts[1].zfill(2)}-01"
                        elif len(parts) >= 2 and "Q" in parts[1]:
                            q_month = {"Q1": "01", "Q2": "04", "Q3": "07", "Q4": "10"}.get(parts[1], "01")
                            clean_date = f"{parts[0]}-{q_month}-01"
                        else:
                            clean_date = f"{parts[0]}-01-01"
                    elif "_" in bucket_str:
                        parts = bucket_str.split("_")
                        if len(parts) >= 2 and len(parts[1]) == 4:
                            clean_date = f"{parts[0]}-01-01"
                        elif len(parts) >= 2 and len(parts[1]) <= 2:
                            clean_date = f"{parts[0]}-{parts[1].zfill(2)}-01"
                        elif len(parts) >= 2 and "Q" in parts[1]:
                            q_month = {"Q1": "01", "Q2": "04", "Q3": "07", "Q4": "10"}.get(parts[1], "01")
                            clean_date = f"{parts[0]}-{q_month}-01"
                        else:
                            clean_date = f"{parts[0]}-01-01"
                    else:
                        clean_date = f"{bucket_str[:4]}-01-01" if bucket_str[:4].isdigit() else "2024-01-01"

                # [Story 109.10] Span-Aware Year Drift Sentinel: clamp wild year drift against known task era / span
                # Resolves user concern: multi-year files (e.g. notes_2015_DSD spanning 2011-2016)
                # must NOT force 2013 into 2015!
                fname = task.get("filename", "")
                bucket_str = str(task.get("bucket", ""))
                manifest = get_file_manifest()
                manifest_entry = manifest.get(fname, {})
                span_str = str(manifest_entry.get("year") or "")

                min_year, max_year = None, None
                for candidate in [span_str, bucket_str, fname]:
                    span_match = re.search(r"(20\d{2})[-_](20\d{2})", candidate)
                    if span_match:
                        y1, y2 = int(span_match.group(1)), int(span_match.group(2))
                        min_year, max_year = min(y1, y2), max(y1, y2)
                        break

                if min_year is None:
                    single_match = re.search(r"20\d{2}", span_str) or re.search(r"20\d{2}", bucket_str) or re.search(r"20\d{2}", fname)
                    if single_match:
                        y = int(single_match.group(0))
                        min_year, max_year = y, y

                if clean_date and min_year is not None and max_year is not None:
                    try:
                        ext_year = int(clean_date[:4])
                        # Allow 1-year margin beyond documented span boundaries
                        if ext_year < min_year - 1:
                            clean_date = f"{min_year}{clean_date[4:]}"
                        elif ext_year > max_year + 1:
                            clean_date = f"{max_year}{clean_date[4:]}"
                    except Exception:
                        pass

                event["date"] = clean_date

                # [FEAT-067 / Story 106.8] Chronological Disentanglement
                combined_text = f"{event.get('evidence', '')} {event.get('summary', '')}"
                chrono = disentangle_chronology(combined_text, clean_date)
                event.update(chrono)

                # [FEAT-454 / Story 106.6] Epistemic Two-Dimensional Model
                if "impact_level" not in event:
                    event["impact_level"] = classify_impact_level(event)
                if "refinement_level" not in event:
                    event["refinement_level"] = 0
                event["passes"] = event.get("passes", 0)
                event["consecutive_zero_deltas"] = event.get("consecutive_zero_deltas", 0)

                # Rank 5 for META anchors
                if file_type == "META":
                    event["rank"] = 5
                    event["impact_level"] = 4

                # [Story 109.16 / Pillar 1] Deterministic Target Year Resolution
                target_year = clean_date[:4] if clean_date and clean_date[:4].isdigit() else "Unknown"
                events_by_target_year.setdefault(target_year, []).append(event)

            # Atomically commit events to their canonical annual lakehouse files
            for t_year, events_to_add in events_by_target_year.items():
                canonical_year_file = os.path.join(DATA_DIR, f"{t_year}.json")
                existing_canonical_data = load_json(canonical_year_file)
                
                for event in events_to_add:
                    c_date = event.get("date")
                    candidate_events = [
                        e for e in existing_canonical_data
                        if e.get("date") == c_date or (event.get("evidence") and e.get("evidence"))
                    ]

                    if not is_semantic_duplicate(event, candidate_events):
                        if event.get("sensitivity", "Public") == "Public":
                            event["sensitivity"] = "Public"
                            existing_canonical_data.append(event)
                            added_count += 1
                        else:
                            with open(AUDIT_FILE, "a") as f:
                                f.write(json.dumps(event) + "\n")
                    else:
                        log(
                            f"   > Semantic Duplicate skipped: {event.get('summary')[:50]}..."
                        )

                existing_canonical_data.sort(key=lambda x: x.get("date", ""))
                save_json(canonical_year_file, existing_canonical_data)

            update_status(
                "ONLINE",
                f"Processed {task['bucket']}",
                added_count,
                filename=task["filename"],
                engine=engine_mode,
            )

            # [FEAT-130] Atomic State Update: ONLY mark as done if data was captured
            state[task["id"]] = content_hash
            save_json(STATE_FILE, state)
            # [Story 105.12] Refresh latest gems after committing a chunk
            try:
                from extract_latest_gems import extract_latest_gems

                extract_latest_gems()
            except Exception as e:
                log(f"   ! Gem extraction failed: {e}")
        else:
            log("   > No valid events found. State NOT updated.")

        save_json(QUEUE_FILE, queue)

        if not FAST_MODE:
            log("Waiting 15s for silicon cooling...")
            time.sleep(15)
        else:
            time.sleep(1)  # Tiny yield to prevent CPU spinning


if __name__ == "__main__":
    main()
