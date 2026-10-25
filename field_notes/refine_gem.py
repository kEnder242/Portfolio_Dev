import json
import logging
import os
import random
import sys
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ai_engine_v2 import get_engine_v2
from utils import update_status

# Config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
logging.basicConfig(level=logging.INFO, format="[REFINE] %(message)s")


def cosine_similarity(a, b):
    import numpy as np

    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


import re


def _has_technical_evidence(text: str) -> bool:
    """Detect hard technical evidence in a gem's evidence string.

    Returns True if the text contains any of:
      - Memory/register hex addresses  (0x..., hex with 0x prefix, 4+ digits)
      - CLI flags                     (--foo, -v, --force)
      - Script/code file extensions   (.py, .sh, .js, .ts, .c, .cpp, .rb, .pl, .go, .rs, .java, .ipynb)
      - Hardware / firmware acronyms  (RAPL, PECI, MSR, PCIe, I2C, IPMI, BMC,
                                       OpenBMC, BIOS, PythonSV, ITP, JTAG)
    """
    if not isinstance(text, str) or not text:
        return False

    # 1. Hex register / address patterns (0x + 2+ hex digits)
    if re.search(r"0x[0-9a-fA-F]{2,}", text):
        return True

    # 2. CLI flags (--long-flag or -single-char, not at line-start)
    if re.search(r"(?<!\S)--[a-zA-Z][\w-]+", text):
        return True
    if re.search(r"(?<!\S)-[a-zA-Z](?=\s|$|[,:;])", text):
        return True

    # 3. Script / code file extensions
    tech_exts = (
        r"\.(py|sh|bash|js|ts|c|cpp|h|hpp|rb|pl|pm|go|rs|java|ipynb|json|yaml|yml|toml|ini|cfg|conf|xml|csv)\b"
    )
    if re.search(tech_exts, text):
        return True

    # 4. Hardware / firmware acronyms (word-boundary match, case-sensitive for most)
    hw_acronyms = (
        r"\bRAPL\b",
        r"\bPECI\b",
        r"\bMSR\b",
        r"\bPCIe\b",
        r"\bI2C\b",
        r"\bIPMI\b",
        r"\bBMC\b",
        r"\bOpenBMC\b",
        r"\bBIOS\b",
        r"\bPythonSV\b",
        r"\bITP\b",
        r"\bJTAG\b",
    )
    for pattern in hw_acronyms:
        if re.search(pattern, text):
            return True

    return False


# [FEAT-067 / Story 106.8] Platform Release & Active Debug Windows
PLATFORM_ERA_MAP = {
    r"\bGrantley\b": (2014, "2014-Q2"),
    r"\bHaswell\b": (2013, "2013-Q3"),
    r"\bBroadwell\b": (2015, "2015-Q1"),
    r"\bPurley\b|\bSkylake[- ]SP\b": (2017, "2017-Q3"),
    r"\bCascade Lake\b": (2019, "2019-Q2"),
    r"\bWhitley\b|\bIce Lake[- ]SP\b|\bICX\b": (2020, "2020-Q4"),
    r"\bEagle Stream\b|\bSapphire Rapids\b|\bSPR\b": (2023, "2023-Q1"),
    r"\bBirch Stream\b|\bGranite Rapids\b|\bGNR\b": (2024, "2024-Q3"),
    r"\bSierra Forest\b|\bSRF\b": (2024, "2024-Q2"),
    r"\bKayak\b|\bMontana\b": (2023, "2023-Q4"),
    r"\bOakstream\b": (2020, "2020-Q3"),
}


def disentangle_chronology(raw_text: str, document_date_str: str) -> dict:
    """[FEAT-067 / Story 106.8] Deterministic extraction of event_era independent of document_date."""
    if not isinstance(raw_text, str):
        raw_text = ""
    doc_year = 2024
    if document_date_str and isinstance(document_date_str, str):
        try:
            doc_year = int(document_date_str.split("-")[0])
        except (ValueError, IndexError):
            doc_year = 2024

    # Stage 1: Explicit Date Pattern within the text (e.g. "8/29/2019", "2019-07-01", "07-15-2019")
    m_full = re.search(r"\b(\d{1,2})[/.-](\d{1,2})[/.-](20\d{2})\b", raw_text)
    if m_full:
        month, day, year = int(m_full.group(1)), int(m_full.group(2)), int(m_full.group(3))
        if 2005 <= year <= 2026 and 1 <= month <= 12 and 1 <= day <= 31:
            q = f"{year}-Q{(month - 1) // 3 + 1}"
            return {
                "document_date": document_date_str,
                "event_era": f"{year:04d}-{month:02d}-{day:02d}",
                "event_year": year,
                "event_quarter": q,
                "temporal_confidence": 0.95,
                "temporal_provenance": "explicit_incident_date",
            }
    m_iso = re.search(r"\b(20\d{2})[-/](\d{1,2})[-/](\d{1,2})\b", raw_text)
    if m_iso:
        year, month, day = int(m_iso.group(1)), int(m_iso.group(2)), int(m_iso.group(3))
        if 2005 <= year <= 2026 and 1 <= month <= 12 and 1 <= day <= 31:
            q = f"{year}-Q{(month - 1) // 3 + 1}"
            return {
                "document_date": document_date_str,
                "event_era": f"{year:04d}-{month:02d}-{day:02d}",
                "event_year": year,
                "event_quarter": q,
                "temporal_confidence": 0.95,
                "temporal_provenance": "explicit_incident_date",
            }

    # Stage 2: Explicit Year Mention (e.g. "in 2014", "back in 2019", "late 2019")
    m_year = re.search(
        r"\b(?:in|during|back in|around|circa|late|early|mid|h1|h2)\s+(20\d{2})\b",
        raw_text,
        re.IGNORECASE,
    )
    if m_year:
        year = int(m_year.group(1))
        if 2005 <= year <= 2026:
            return {
                "document_date": document_date_str,
                "event_era": f"{year:04d}-01-01",
                "event_year": year,
                "event_quarter": f"{year}-Q1",
                "temporal_confidence": 0.85,
                "temporal_provenance": "explicit_incident_year",
            }

    # Stage 3: Platform Generation Anchor Map
    for pattern, (era_year, era_q) in PLATFORM_ERA_MAP.items():
        if re.search(pattern, raw_text, re.IGNORECASE):
            return {
                "document_date": document_date_str,
                "event_era": f"{era_year:04d}-06-01",
                "event_year": era_year,
                "event_quarter": era_q,
                "temporal_confidence": 0.70,
                "temporal_provenance": f"platform_heuristic_{pattern.strip(r'\\b')}",
            }

    # Stage 4: Retrospective Shift Detection (e.g. "10 years ago")
    m_rel = re.search(r"\b(\d{1,2})\s+years?\s+ago\b", raw_text, re.IGNORECASE)
    if m_rel:
        offset = int(m_rel.group(1))
        calc_year = doc_year - offset
        if 2005 <= calc_year <= 2026:
            return {
                "document_date": document_date_str,
                "event_era": f"{calc_year:04d}-01-01",
                "event_year": calc_year,
                "event_quarter": f"{calc_year}-Q1",
                "temporal_confidence": 0.75,
                "temporal_provenance": "relative_offset",
            }

    # Stage 5: Default Fallback to Document Date
    fallback_year = doc_year
    q_str = f"{fallback_year}-Q1"
    if document_date_str and len(document_date_str) >= 7:
        try:
            m = int(document_date_str[5:7])
            q_str = f"{fallback_year}-Q{(m - 1) // 3 + 1}"
        except Exception:
            pass

    return {
        "document_date": document_date_str,
        "event_era": document_date_str if document_date_str else f"{fallback_year}-01-01",
        "event_year": fallback_year,
        "event_quarter": q_str,
        "temporal_confidence": 0.50,
        "temporal_provenance": "document_date_fallback",
    }


_COMPASS_CACHE = None


def _get_compass_keywords() -> set:
    global _COMPASS_CACHE
    if _COMPASS_CACHE is not None:
        return _COMPASS_CACHE
    keywords = set()
    compass_file = os.path.join(DATA_DIR, "career_compass.json")
    if os.path.exists(compass_file):
        try:
            with open(compass_file, "r") as f:
                cdata = json.load(f)
                mesh = cdata.get("tier_2_keyword_mesh", {}).get("keywords", [])
                keywords.update([k.lower() for k in mesh if isinstance(k, str)])
                anchors = cdata.get("tier_1_anchor_map", {})
                for era, lines in anchors.items():
                    for line in lines:
                        for word in re.findall(r"\b[A-Za-z0-9_-]{3,}\b", line):
                            if word.isupper() or any(c.isdigit() for c in word):
                                keywords.add(word.lower())
        except Exception as e:
            logging.warning(f"Failed to load career_compass.json for keywords: {e}")
    _COMPASS_CACHE = keywords
    return keywords


def classify_impact_level(gem: dict, graph_data: list = None) -> int:
    """[FEAT-454 / Story 106.6] Classify gem into discrete impact levels (1 to 4):

    1: Leaf (atomic operational exhaust, raw logs, shipping, routine)
    2: Subsystem Branch (localized component debug, workarounds)
    3: Cross-Platform Branch (cross-subsystem architecture, multi-team enablement)
    4: Strategic Trunk (direct tie to career_compass or resume_data)
    """
    if not isinstance(gem, dict):
        return 1

    summary = (gem.get("summary") or "").lower()
    evidence = gem.get("evidence") or ""
    tags = [str(t).lower() for t in gem.get("tags", [])]

    # 1. Platform Trunk Check (Impact 4)
    if gem.get("rank") == 5 or "[strategic_anchor]" in summary:
        return 4

    compass_kw = _get_compass_keywords()
    strong_hits = 0
    for kw in compass_kw:
        if kw in tags or re.search(r"\b" + re.escape(kw) + r"\b", summary):
            strong_hits += 1

    if strong_hits >= 2:
        return 4

    # 2. Graph Relations Centrality / Spanning check
    if graph_data:
        gem_id = gem.get("id") or gem.get("summary", "")[:50]
        edges = [
            r
            for r in graph_data
            if r.get("source") == gem_id or r.get("target") == gem_id
        ]
        if len(edges) >= 4:
            return 3
        elif len(edges) >= 2:
            return 2

    # 3. Technical Evidence Check (Impact 2 or 3)
    has_tech = _has_technical_evidence(evidence) or _has_technical_evidence(summary)
    if has_tech:
        if strong_hits >= 1 or len(gem.get("anchors", [])) >= 3 or gem.get("rank") == 4:
            return 3
        return 2

    # 4. Fallback: Leaf (Impact 1)
    return 1


def get_embedding_function():
    """Get an embedding function with ChromaDB HttpClient fallback.

    Attempts to connect to a ChromaDB server at 127.0.0.1:8000 and use its
    SentenceTransformer embedding function.  Falls back to local
    SentenceTransformer initialization if the server is unreachable.

    Returns:
        An object with an ``encode(texts)`` method that returns a NumPy array
        of embeddings, or ``None`` if both paths fail.
    """
    # Attempt 1: ChromaDB HttpClient -> SentenceTransformerEmbeddingFunction
    try:
        import chromadb
        from chromadb.utils import embedding_functions

        logging.info(
            "Attempting HttpClient connection for embeddings at " "127.0.0.1:8001..."
        )
        client = chromadb.HttpClient(host="127.0.0.1", port=8001)
        heartbeat = client.heartbeat()

        logging.info(
            f"HttpClient heartbeat successful (tick: {heartbeat}). "
            "Offloading embeddings to ChromaDB server."
        )

        ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        logging.info(
            "Final embedding method: ChromaDB "
            "SentenceTransformerEmbeddingFunction (server-side)."
        )

        # SentenceTransformerEmbeddingFunction is callable but does not expose
        # an ``.encode()`` method; wrap it so the downstream code can call
        # ``.encode(texts)`` unchanged.
        class _ChromaDBEmbedder:
            def encode(self, texts):
                import numpy as np

                return np.array(ef(texts))

        return _ChromaDBEmbedder()

    except ImportError:
        logging.warning(
            "chromadb package not installed. "
            "Falling back to local SentenceTransformer."
        )
    except Exception as e:
        logging.warning(
            f"HttpClient connection failed: {e}. "
            "Falling back to local SentenceTransformer."
        )

    # Attempt 2: Local SentenceTransformer
    try:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("all-MiniLM-L6-v2")
        logging.info(
            "Final embedding method: local SentenceTransformer " "(all-MiniLM-L6-v2)."
        )
        return model
    except Exception as e:
        logging.error(f"Failed to load SentenceTransformer: {e}")
        return None


def deduplicate_gems():
    import glob

    logging.info("Running Semantic De-duplication check [Goal 6]...")

    model = get_embedding_function()
    if model is None:
        return

    json_files = glob.glob(os.path.join(DATA_DIR, "*.json"))
    ignore = [
        "themes.json",
        "status.json",
        "queue.json",
        "state.json",
        "search_index.json",
        "pager_activity.json",
        "file_manifest.json",
        "overrides.json",
    ]

    events_by_date = {}
    for jf in json_files:
        if os.path.basename(jf) in ignore:
            continue
        try:
            with open(jf, "r") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    continue
                for i, event in enumerate(data):
                    date = event.get("date")
                    if not date:
                        continue
                    if date not in events_by_date:
                        events_by_date[date] = []
                    events_by_date[date].append(
                        {"file_path": jf, "index": i, "event": event}
                    )
        except:
            pass

    modified_files = set()
    file_contents = {}

    def get_content(path):
        if path not in file_contents:
            with open(path, "r") as f:
                file_contents[path] = json.load(f)
        return file_contents[path]

    for date, items in events_by_date.items():
        if len(items) < 2:
            continue

        summaries = [it["event"].get("summary", "") for it in items]
        embeddings = model.encode(summaries)

        merged_indices = set()
        for i in range(len(items)):
            if i in merged_indices:
                continue
            for j in range(i + 1, len(items)):
                if j in merged_indices:
                    continue

                sim = cosine_similarity(embeddings[i], embeddings[j])
                if sim > 0.85:
                    logging.info(
                        f"   [MERGE] Found duplicates on {date} (similarity: {sim:.2f})"
                    )
                    logging.info(f"     1: {summaries[i][:50]}...")
                    logging.info(f"     2: {summaries[j][:50]}...")

                    event_i = items[i]["event"]
                    event_j = items[j]["event"]

                    if len(event_j.get("summary", "")) > len(
                        event_i.get("summary", "")
                    ):
                        event_i["summary"] = event_j["summary"]

                    ev_i = event_i.get("evidence", "")
                    ev_j = event_j.get("evidence", "")
                    if ev_j and ev_j not in ev_i:
                        event_i["evidence"] = f"{ev_i}\n\nEvidence 2: {ev_j}".strip()

                    tags_i = set(event_i.get("tags", []))
                    tags_j = set(event_j.get("tags", []))
                    event_i["tags"] = list(tags_i.union(tags_j))

                    # STORY 105.13: Conditional rank promotion based on technical evidence
                    rank_i = event_i.get("rank", 2)
                    rank_j = event_j.get("rank", 2)
                    base_rank = max(rank_i, rank_j)
                    if _has_technical_evidence(event_i.get("evidence", "")):
                        event_i["rank"] = max(4, base_rank)
                    else:
                        event_i["rank"] = base_rank

                    merged_indices.add(j)

                    content_i = get_content(items[i]["file_path"])
                    content_j = get_content(items[j]["file_path"])

                    content_i[items[i]["index"]] = event_i
                    modified_files.add(items[i]["file_path"])
                    content_j[items[j]["index"]] = None
                    modified_files.add(items[j]["file_path"])

    for path in modified_files:
        content = file_contents[path]
        cleaned_content = [item for item in content if item is not None]
        try:
            with open(path, "w") as f:
                json.dump(cleaned_content, f, indent=2)
            logging.info(f"💾 Saved merged changes to {os.path.basename(path)}")
        except Exception as e:
            logging.error(f"Failed to save {path}: {e}")


QUEUE_FILE = os.path.join(DATA_DIR, "refinement_rotation_queue.json")
GRAPH_FILE = os.path.join(DATA_DIR, "graph_relations.json")
LOOP_LEDGER_FILE = os.path.join(DATA_DIR, "loop_ledger.jsonl")


class RotationalRefinementEngine:
    """[FEAT-067 / Story 106.5 / LOOP-004] Multi-Pass Epistemic Refinement Engine & Active Rotation Queue."""

    def __init__(self, epoch: int = 106):
        self.queue_data = self._load_queue()
        self.epoch = self.queue_data.get("epoch", epoch)
        self.graph_data = self._load_graph()

    def _load_queue(self) -> dict:
        if os.path.exists(QUEUE_FILE):
            try:
                with open(QUEUE_FILE, "r") as f:
                    return json.load(f)
            except Exception as e:
                logging.warning(f"Could not load {QUEUE_FILE}: {e}")
        return {
            "version": "1.0.0",
            "last_updated": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "epoch": self.epoch,
            "queue": [],
        }

    def _save_queue(self):
        self.queue_data["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
        self.queue_data["epoch"] = self.epoch
        # Retain only un-saturated gems (refinement_level < 3) in the active queue
        self.queue_data["queue"] = [
            it
            for it in self.queue_data.get("queue", [])
            if it.get("refinement_level", 0) < 3
        ]
        with open(QUEUE_FILE, "w") as f:
            json.dump(self.queue_data, f, indent=2)

    def _load_graph(self) -> list:
        if os.path.exists(GRAPH_FILE):
            try:
                with open(GRAPH_FILE, "r") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
            except Exception as e:
                logging.warning(f"Could not load {GRAPH_FILE}: {e}")
        return []

    def _save_graph(self):
        with open(GRAPH_FILE, "w") as f:
            json.dump(self.graph_data, f, indent=2)

    def populate_queue_from_archive(self, max_items: int = 50, persist_updates: bool = True):
        """Scan monthly JSON tables, stamp unassigned levels on disk, and enqueue candidate gems."""
        existing_ids = {it["gem_id"] for it in self.queue_data.get("queue", [])}
        import glob

        json_files = sorted(glob.glob(os.path.join(DATA_DIR, "20*.json")), reverse=True)
        ignore = [
            "status.json",
            "queue.json",
            "state.json",
            "search_index.json",
            "pager_activity.json",
            "refinement_rotation_queue.json",
            "file_manifest.json",
        ]

        candidate_entries = []
        total_stamped = 0

        for jf in json_files:
            fname = os.path.basename(jf)
            if fname in ignore:
                continue
            try:
                with open(jf, "r") as f:
                    items = json.load(f)
                if not isinstance(items, list):
                    continue

                file_modified = False
                for idx, gem in enumerate(items):
                    if not isinstance(gem, dict):
                        continue
                    # Ensure chronology & levels stamped
                    if "event_era" not in gem or not gem.get("event_era"):
                        chrono = disentangle_chronology(
                            gem.get("evidence", "") + " " + gem.get("summary", ""),
                            gem.get("date", ""),
                        )
                        gem.update(chrono)
                        file_modified = True
                    if "impact_level" not in gem or gem.get("impact_level") in ("unassigned", None):
                        gem["impact_level"] = classify_impact_level(
                            gem, self.graph_data
                        )
                        file_modified = True
                        total_stamped += 1
                    if "refinement_level" not in gem or gem.get("refinement_level") is None:
                        gem["refinement_level"] = (
                            3
                            if gem.get("rank", 0) >= 4 and gem.get("trigger_context")
                            else (1 if gem.get("rank", 0) >= 3 else 0)
                        )
                        file_modified = True

                    gem_id = gem.get("id") or f"{fname}::{idx}"
                    if gem["refinement_level"] < 3 and gem_id not in existing_ids:
                        anchors = gem.get("anchors") or gem.get("tags", [])
                        entry = {
                            "gem_id": gem_id,
                            "file_path": fname,
                            "index": idx,
                            "refinement_level": gem["refinement_level"],
                            "impact_level": gem["impact_level"],
                            "passes": gem.get("passes", 0),
                            "consecutive_zero_deltas": gem.get(
                                "consecutive_zero_deltas", 0
                            ),
                            "last_touch_epoch": self.epoch - 1,
                            "priority": 1.0,
                            "anchors": (
                                anchors[:4]
                                if isinstance(anchors, list)
                                else [str(anchors)]
                            ),
                        }
                        entry["priority"] = self.compute_priority(entry)
                        candidate_entries.append(entry)

                if file_modified and persist_updates:
                    try:
                        with open(jf, "w") as f:
                            json.dump(items, f, indent=2)
                        logging.info(f"Persisted epistemic stamps to {fname}")
                    except Exception as fe:
                        logging.warning(f"Could not write epistemic stamps to {fname}: {fe}")

            except Exception as e:
                logging.debug(f"Error scanning {fname}: {e}")

        # Prioritize candidates by calculated priority (higher impact, higher refinement deficit)
        candidate_entries.sort(key=lambda x: x["priority"], reverse=True)
        to_enqueue = candidate_entries[:max_items]

        for entry in to_enqueue:
            self.queue_data["queue"].append(entry)
            existing_ids.add(entry["gem_id"])

        enqueued = len(to_enqueue)
        if enqueued > 0 or total_stamped > 0:
            logging.info(
                f"Enqueued {enqueued} unrefined candidate gems into active rotation (stamped {total_stamped} gems on disk)."
            )
            self._save_queue()

    def compute_priority(self, item: dict) -> float:
        """W_i = Impact * (3 - RefinementLevel) * log2(2 + Age) * Damping."""
        import math

        impact = item.get("impact_level", 1)
        ref_deficit = max(0, 3 - item.get("refinement_level", 0))
        age = self.epoch - item.get("last_touch_epoch", self.epoch - 1)
        damping = 0.5 if age <= 0 else 1.0
        return round(
            impact * ref_deficit * math.log2(2 + max(0, age)) * damping, 3
        )

    def pick_batch(self, batch_size: int = 5) -> list:
        for item in self.queue_data.get("queue", []):
            item["priority"] = self.compute_priority(item)
        self.queue_data["queue"].sort(key=lambda x: x["priority"], reverse=True)
        return self.queue_data["queue"][:batch_size]

    def advance_gem_pass(self, item: dict, engine=None) -> dict:
        target_path = os.path.join(DATA_DIR, item["file_path"])
        if not os.path.exists(target_path):
            return {"gem_id": item["gem_id"], "delta": 0, "is_saturated": False}

        with open(target_path, "r") as f:
            file_data = json.load(f)

        idx = item["index"]
        if idx >= len(file_data) or not isinstance(file_data[idx], dict):
            return {"gem_id": item["gem_id"], "delta": 0, "is_saturated": False}

        gem = file_data[idx]
        anchors = gem.get("anchors") or item.get("anchors") or []
        if isinstance(anchors, str):
            anchors = [anchors]

        new_edges = 0
        gem_node_label = (
            f"{gem.get('date', 'UNKNOWN')}: {gem.get('summary', '')[:60]}"
        )

        # Link discovered anchors in graph relations
        for anchor in anchors:
            if not anchor or len(str(anchor)) < 3:
                continue
            anchor_str = str(anchor).lower()
            already_linked = any(
                (
                    anchor_str in r.get("source", "").lower()
                    and gem_node_label.lower() in r.get("target", "").lower()
                )
                or (
                    gem_node_label.lower() in r.get("source", "").lower()
                    and anchor_str in r.get("target", "").lower()
                )
                for r in self.graph_data
            )
            if not already_linked:
                self.graph_data.append(
                    {
                        "source": gem_node_label,
                        "target": str(anchor),
                        "type": "anchored_to",
                        "epoch": self.epoch,
                    }
                )
                new_edges += 1

        # Check field completeness & generate minimal trigger context if missing
        updated_fields = 0
        if not gem.get("trigger_context"):
            if engine:
                try:
                    prompt = f"Given event summary: '{gem.get('summary')}' and evidence: '{gem.get('evidence', '')[:200]}', provide a concise 1-sentence engineering trigger context: what debug condition or inquiry activates this knowledge? Output plain text only."
                    resp = engine.generate(prompt)
                    if resp and len(resp.strip()) > 10:
                        gem["trigger_context"] = resp.strip()
                        updated_fields += 1
                except Exception:
                    pass
            if not gem.get("trigger_context"):
                gem["trigger_context"] = (
                    f"Triggered during platform validation of {', '.join(anchors[:3]) if anchors else 'subsystem'}."
                )
                updated_fields += 1

        # Stamp chronological disentanglement if missing
        if "event_era" not in gem or not gem.get("event_era"):
            chrono = disentangle_chronology(
                gem.get("evidence", "") + " " + gem.get("summary", ""),
                gem.get("date", ""),
            )
            gem.update(chrono)
            updated_fields += 1

        # Stamp impact_level if missing or unassigned
        if "impact_level" not in gem or gem.get("impact_level") in ("unassigned", None):
            gem["impact_level"] = item.get("impact_level") or classify_impact_level(gem, self.graph_data)
            updated_fields += 1

        delta = new_edges + updated_fields
        item["passes"] = item.get("passes", 0) + 1
        item["last_touch_epoch"] = self.epoch
        gem["passes"] = item["passes"]

        if delta > 0:
            item["consecutive_zero_deltas"] = 0
            item["refinement_level"] = min(2, item.get("refinement_level", 0) + 1)
        else:
            item["consecutive_zero_deltas"] = (
                item.get("consecutive_zero_deltas", 0) + 1
            )

        gem["consecutive_zero_deltas"] = item["consecutive_zero_deltas"]
        gem["refinement_level"] = item["refinement_level"]

        min_passes_map = {1: 1, 2: 2, 3: 3, 4: 3}
        required_passes = min_passes_map.get(item.get("impact_level", 1), 2)

        is_saturated = (
            item["refinement_level"] >= 2
            and item["consecutive_zero_deltas"] >= 2
            and item["passes"] >= required_passes
        )

        if is_saturated:
            item["refinement_level"] = 3
            item["status"] = "SATURATED"
            gem["refinement_level"] = 3
            gem["status"] = "SATURATED"

        file_data[idx] = gem
        try:
            with open(target_path, "w") as f:
                json.dump(file_data, f, indent=2)
        except Exception as e:
            logging.warning(f"Failed to write updated gem back to {target_path}: {e}")

        return {
            "gem_id": item["gem_id"],
            "delta": delta,
            "is_saturated": is_saturated,
        }

    def run_rotation_epoch(self, batch_size: int = 5, engine=None) -> dict:
        if not self.queue_data.get("queue"):
            self.populate_queue_from_archive()

        batch = self.pick_batch(batch_size=batch_size)
        if not batch:
            logging.info("Rotation queue is currently empty or quiescently saturated.")
            return {
                "epoch": self.epoch,
                "processed": 0,
                "new_edges": 0,
                "graduations": 0,
                "status": "QUIESCENT",
            }

        total_delta = 0
        graduations = 0
        results = []
        for item in batch:
            res = self.advance_gem_pass(item, engine=engine)
            results.append(res)
            total_delta += res["delta"]
            if res["is_saturated"]:
                graduations += 1

        self._save_graph()
        self._save_queue()

        # Telemetry into loop_ledger.jsonl
        telemetry = {
            "loop_id": "LOOP-004",
            "epoch": self.epoch,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "batch_size": len(batch),
            "processed_gems": len(results),
            "total_delta": total_delta,
            "graduations": graduations,
            "active_queue_remaining": len(self.queue_data.get("queue", [])),
            "status": "CONVERGING" if total_delta > 0 else "STABLE",
        }
        try:
            with open(LOOP_LEDGER_FILE, "a") as lf:
                lf.write(json.dumps(telemetry) + "\n")
        except Exception as e:
            logging.warning(f"Could not append to loop_ledger.jsonl: {e}")

        logging.info(
            f"Completed Epoch {self.epoch}: processed {len(results)} gems, delta={total_delta}, graduations={graduations}"
        )
        return telemetry


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="[LOOP-004] Epistemic Gem Refinement Rotation Loop"
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=5,
        help="Number of refinement rotation epochs to run (default: 5)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=5,
        help="Batch size per epoch (default: 5)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Polite delay between epochs in seconds (default: 1.0)",
    )
    parser.add_argument(
        "--stamp-all",
        action="store_true",
        help="Pre-emptively scan and stamp all archive tables on disk",
    )
    args = parser.parse_args()

    logging.info(
        f"--- [LOOP-004] Epistemic Gem Refinement Rotation Loop (epochs={args.epochs}, batch_size={args.batch_size}) ---"
    )

    # 1. Run Semantic Deduplication (Goal 6)
    try:
        deduplicate_gems()
    except Exception as e:
        logging.error(f"Deduplication check failed: {e}")

    # 2. Rotational Multi-Pass Connection Loop
    engine_client = None
    try:
        engine_client = get_engine_v2(mode="HYBRID")
    except Exception as e:
        logging.warning(
            f"Optional AI Engine not available ({e}); using topological link engine."
        )

    rot_engine = RotationalRefinementEngine(epoch=106)
    if args.stamp_all:
        rot_engine.populate_queue_from_archive(max_items=1000, persist_updates=True)

    total_processed = 0
    total_graduations = 0
    total_delta = 0
    epochs_run = 0

    for ep in range(args.epochs):
        telemetry = rot_engine.run_rotation_epoch(
            batch_size=args.batch_size, engine=engine_client
        )
        epochs_run += 1
        total_processed += telemetry.get("processed_gems", 0)
        total_graduations += telemetry.get("graduations", 0)
        total_delta += telemetry.get("total_delta", 0)

        # Increment epoch for monotonic progression
        rot_engine.epoch += 1

        if ep < args.epochs - 1 and args.delay > 0:
            time.sleep(args.delay)

    summary = {
        "status": "PASS" if total_processed > 0 or not rot_engine.queue_data.get("queue") else "QUIESCENT",
        "epochs_run": epochs_run,
        "processed_gems": total_processed,
        "total_delta": total_delta,
        "graduations": total_graduations,
        "active_queue_remaining": len(rot_engine.queue_data.get("queue", [])),
    }

    update_status(
        "REFINE",
        f"{epochs_run} Epochs: {total_processed} gems, {total_graduations} saturated",
        total_processed,
    )

    # Structured telemetry JSON printed on stdout for pipeline consumption
    print(json.dumps(summary))
    return summary


if __name__ == "__main__":
    main()

