#!/usr/bin/env python3
import os
import re
import logging
import chromadb
from chromadb.utils import embedding_functions

# Config
DB_PATH = os.path.expanduser("~/AcmeLab/chroma_db")
COLLECTION_DNA = "behavioral_dna"
COLLECTION_FEATURE = "feature_dna"
COLLECTION_PHILOSOPHY = "philosophy_dna"
COLLECTION_WISDOM = "wisdom_dna"
COLLECTION_RDNA = "rdna"

FEATURE_TRACKER_PATH = os.path.expanduser("~/Dev_Lab/Portfolio_Dev/FeatureTracker.md")
PROTOCOLS_PATH = os.path.expanduser("~/Dev_Lab/HomeLabAI/docs/Protocols.md")
INFRASTRUCTURE_PATH = os.path.expanduser("~/Dev_Lab/HomeLabAI/docs/LAB_INFRASTRUCTURE.md")
PHILOSOPHY_DATA_PATH = os.path.expanduser("~/Dev_Lab/Portfolio_Dev/dna/philosophy_data.json")
WISDOM_DATA_PATH = os.path.expanduser("~/Dev_Lab/Portfolio_Dev/dna/wisdom_data.json")
RDNA_QUESTIONS_PATH = os.path.expanduser("~/Dev_Lab/Portfolio_Dev/dna/rdna_questions.json")

# [STORY-8614] SHA256 checksum cache for the idempotency guard (Finding 17 of
# SPRINT_86_DEEP_DIVE_DEFICIENCY_REPORT.md). Maps each source file path to the
# hex digest of its contents at the last successful sync.
CHECKSUMS_PATH = os.path.expanduser("~/Dev_Lab/Portfolio_Dev/dna/.sync_checksums.json")


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def parse_infrastructure(filepath):
    """Parses LAB_INFRASTRUCTURE.md for hardware, storage, and playbook sections."""
    if not os.path.exists(filepath):
        logging.error(f"LAB_INFRASTRUCTURE.md not found at {filepath}")
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(r"^(#{2,4})\s+(.*?)$", re.MULTILINE)
    matches = list(pattern.finditer(content))
    infra_items = []

    for i, match in enumerate(matches):
        name = match.group(2).strip()
        start_idx = match.end()
        end_idx = matches[i+1].start() if i + 1 < len(matches) else len(content)
        block_content = content[start_idx:end_idx].strip()
        if not block_content: continue

        import hashlib
        unique_id = f"INFRA_{hashlib.md5(name.encode('utf-8', errors='ignore')).hexdigest()[:8]}"

        infra_items.append({
            "id": unique_id,
            "document": f"INFRASTRUCTURE SECTION: {name}\n\n{block_content}",
            "metadata": {
                "name": name,
                "type": "INFRA",
                "source": "LAB_INFRASTRUCTURE.md"
            }
        })

    return infra_items

def get_safe_collection(client, name, ef):
    try:
        return client.get_or_create_collection(name=name, embedding_function=ef)
    except Exception:
        return client.get_or_create_collection(name=name)

# [DNA-AUDIT] Noise filter: statuses that are intentionally retired/superseded.
# Items matching these prefixes are silently skipped during sync and reported
# in the SKIP REPORT emitted at the end of each rebuild pass.
DNA_NOISE_STATUSES = {
    "DEFEATURED",
    "ARCHIVED",
    "CONSOLIDATED",
}

def _is_noise_status(status: str) -> bool:
    """Return True if the status matches a known noise/retired prefix."""
    s = status.strip().upper()
    return any(s.startswith(n) for n in DNA_NOISE_STATUSES)


# ---------------------------------------------------------------------------
# [STORY-8614] Idempotency guard: SHA256 checksum cache + dry-run planning.
# Finding 17 of SPRINT_86_DEEP_DIVE_DEFICIENCY_REPORT.md — a full
# clear-and-reupload on every run leaves ChromaDB empty if the process dies
# between the clear and the reupload. The guard below skips sources whose
# checksum is unchanged, so repeat runs are no-ops unless content changed.
# ---------------------------------------------------------------------------

# (collection, human label, source file) — one entry per clear+upload step.
# behavioral_dna appears twice because two source files feed it; each step
# wipes only its own `where={"source": ...}` scope.
SYNC_SOURCES = [
    (COLLECTION_FEATURE, "FeatureTracker.md", FEATURE_TRACKER_PATH),
    (COLLECTION_DNA, "Protocols.md", PROTOCOLS_PATH),
    (COLLECTION_DNA, "LAB_INFRASTRUCTURE.md", INFRASTRUCTURE_PATH),
    (COLLECTION_PHILOSOPHY, "philosophy_data.json", PHILOSOPHY_DATA_PATH),
    (COLLECTION_WISDOM, "wisdom_data.json", WISDOM_DATA_PATH),
    (COLLECTION_RDNA, "rdna_questions.json", RDNA_QUESTIONS_PATH),
]


def _sha256_file(filepath: str) -> str | None:
    """Return the SHA256 hex digest of a file, or None if it cannot be read."""
    import hashlib
    try:
        digest = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except OSError as e:
        logging.warning(f"Could not hash {filepath}: {e}")
        return None


def load_checksums(path: str = CHECKSUMS_PATH) -> dict:
    """Load the checksum cache; returns {} when missing or corrupt."""
    import json
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError) as e:
        logging.warning(f"Could not load checksum cache {path}: {e}. Starting fresh.")
        return {}


def save_checksums(checksums: dict, path: str = CHECKSUMS_PATH) -> None:
    """Atomically persist the checksum cache (.tmp + os.replace)."""
    import json
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp_path = path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(checksums, f, indent=2, sort_keys=True)
        os.replace(tmp_path, path)
        logging.info(f"[IDEMPOTENCY] Checksum cache updated: {path}")
    except OSError as e:
        logging.warning(f"Could not write checksum cache {path}: {e}")


def _source_changed(filepath: str, checksums: dict, force: bool) -> bool:
    """Return True if the source file needs re-syncing.

    A source is considered changed when --force is passed, its current SHA256
    differs from the cached value, or it cannot be hashed (defaulting to sync
    so the parse_* helpers can surface the file-level error).
    """
    if force:
        return True
    current = _sha256_file(filepath)
    if current is None:
        return True
    return checksums.get(filepath) != current


def parse_feature_tracker(filepath):
    """
    Parses FeatureTracker.md for [FEAT-XXX] and [VIBE-XXX] blocks.
    """
    if not os.path.exists(filepath):
        logging.error(f"FeatureTracker.md not found at {filepath}")
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex to match headers like:
# [FEAT-400] ROLE TOKEN (Multi‑LoRA Persona Switch)
    # ## [FEAT-030] Unity Pattern (Multi-LoRA Residency) [SCAR #5]
    # ### [VIBE-012] Hemispheric Independence
    pattern = re.compile(r"^(#{2,4})\s+\[((?:FEAT|VIBE)-\d+)\]\s+(.*?)$", re.MULTILINE)
    
    matches = list(pattern.finditer(content))
    features = []
    
    for i, match in enumerate(matches):
        feat_id = match.group(2)
        name = match.group(3).strip()
        start_idx = match.end()
        end_idx = matches[i+1].start() if i + 1 < len(matches) else len(content)
        
        block_content = content[start_idx:end_idx].strip()
        
        # Extract status
        status_match = re.search(r"^\*\*Status:\*\*\s*(.*?)$", block_content, re.MULTILINE | re.IGNORECASE)
        status = status_match.group(1).strip() if status_match else "UNKNOWN"
        
        # [DNA-AUDIT] Skip noise statuses — retired/superseded items don't belong
        # in the live retrieval index. Caller collects these for skip report.
        if _is_noise_status(status):
            features.append({
                "_skipped": True,
                "id": feat_id,
                "name": name,
                "status": status,
                "reason": "NOISE_STATUS",
            })
            continue

        # Extract mechanism
        mechanism_match = re.search(r"^\*\*Mechanism:\*\*\s*(.*?)$", block_content, re.MULTILINE | re.IGNORECASE)
        mechanism = mechanism_match.group(1).strip() if mechanism_match else "UNKNOWN"
        
        # Extract verification
        verification_match = re.search(r"^\*\*Verification:\*\*\s*(.*?)$", block_content, re.MULTILINE | re.IGNORECASE)
        verification = verification_match.group(1).strip() if verification_match else "UNKNOWN"
        
        # Clean clean content for doc representation
        doc_content = f"ID: {feat_id}\nName: {name}\nStatus: {status}\nMechanism: {mechanism}\nVerification: {verification}\n\n{block_content}"
        
        import hashlib
        unique_id = f"{feat_id}_{hashlib.md5(name.encode('utf-8', errors='ignore')).hexdigest()[:8]}"
        
        features.append({
            "id": unique_id,
            "document": doc_content,
            "metadata": {
                "feature_id": feat_id,
                "name": name,
                "status": status,
                "type": "FEAT" if "FEAT" in feat_id else "VIBE",
                "source": "FeatureTracker.md"
            }
        })
        
    return features

def parse_protocols(filepath):
    """
    Parses Protocols.md for BKM protocols.
    """
    if not os.path.exists(filepath):
        logging.error(f"Protocols.md not found at {filepath}")
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex to match headers like:
    # ## BKM-001: The Cold-Start Protocol (Agent Orientation)
    # ### [BKM-015.1] The Law of Semantic Indirection (The Bones)
    pattern = re.compile(r"^(#{2,4})\s+(?:\[?(BKM-\d+(?:\.\d+)?)\]?:?)\s+(.*?)$", re.MULTILINE)
    
    matches = list(pattern.finditer(content))
    protocols = []
    
    for i, match in enumerate(matches):
        bkm_id = match.group(2)
        name = match.group(3).strip()
        start_idx = match.end()
        end_idx = matches[i+1].start() if i + 1 < len(matches) else len(content)
        
        block_content = content[start_idx:end_idx].strip()
        
        doc_content = f"ID: {bkm_id}\nName: {name}\n\n{block_content}"
        
        import hashlib
        unique_id = f"{bkm_id}_{hashlib.md5(name.encode('utf-8', errors='ignore')).hexdigest()[:8]}"
        
        protocols.append({
            "id": unique_id,
            "document": doc_content,
            "metadata": {
                "bkm_id": bkm_id,
                "name": name,
                "type": "BKM",
                "source": "Protocols.md"
            }
        })
        
    return protocols

def get_chroma_client():
    """Initialize ChromaDB client with HttpClient fallback."""
    try:
        logging.info("Attempting to connect to ChromaDB HttpClient on port 8001...")
        client = chromadb.HttpClient(host="127.0.0.1", port=8001)
        # Verify connection
        heartbeat = client.heartbeat()
        logging.info(f"HttpClient heartbeat successful: {heartbeat}")
        return client
    except Exception as e:
        logging.warning(f"HttpClient connection failed: {e}. Falling back to PersistentClient.")
        return chromadb.PersistentClient(path=DB_PATH)


def parse_philosophy(filepath):
    """Parses philosophy_data.json for PHL-xxx narrative philosophy cards."""
    if not os.path.exists(filepath):
        logging.warning(f"philosophy_data.json not found at {filepath}")
        return []
    import json
    with open(filepath, "r", encoding="utf-8") as f:
        cards = json.load(f)
    
    philosophy_items = []
    for c in cards:
        pid = c.get("id", "PHL-UNK")
        theme = c.get("theme", "Philosophy")
        origin_text = c.get("origin", {}).get("text", "")
        origin_src = c.get("origin", {}).get("source", "")
        synth_title = c.get("synthesis", {}).get("title", "")
        synth_context = c.get("synthesis", {}).get("narrative_context", "")
        tags = c.get("metadata", {}).get("tags", [])
        
        doc_content = (
            f"ID: {pid}\n"
            f"Theme: {theme}\n"
            f"Title: {synth_title}\n"
            f"Origin Quote: \"{origin_text}\"\n\n"
            f"Synthesis: {synth_context}\n"
            f"Tags: {', '.join(tags)}"
        )
        
        philosophy_items.append({
            "id": pid,
            "document": doc_content,
            "metadata": {
                "philosophy_id": pid,
                "theme": theme,
                "title": synth_title,
                "tags": ",".join(tags),
                "source": "philosophy_data.json",
                "type": "PHILOSOPHY"
            }
        })
    return philosophy_items


def parse_wisdom(filepath):
    """Parses wisdom_data.json for WIS-xxx empirical validation war stories and findings."""
    if not os.path.exists(filepath):
        logging.warning(f"wisdom_data.json not found at {filepath}")
        return []
    import json
    with open(filepath, "r", encoding="utf-8") as f:
        cards = json.load(f)

    wisdom_items = []
    for c in cards:
        wid = c.get("id", "WIS-UNK")
        theme = c.get("theme", "Validation")
        origin_text = c.get("origin", {}).get("text", "")
        origin_src = c.get("origin", {}).get("source", "")
        synth_title = c.get("synthesis", {}).get("title", "")
        synth_context = c.get("synthesis", {}).get("narrative_context", "")
        tags = c.get("metadata", {}).get("tags", [])

        doc_content = (
            f"ID: {wid}\n"
            f"Theme: {theme}\n"
            f"Title: {synth_title}\n"
            f"Origin Quote: \"{origin_text}\"\n\n"
            f"Synthesis: {synth_context}\n"
            f"Tags: {', '.join(tags)}"
        )

        wisdom_items.append({
            "id": wid,
            "document": doc_content,
            "metadata": {
                "wisdom_id": wid,
                "theme": theme,
                "title": synth_title,
                "tags": ",".join(tags) if isinstance(tags, list) else str(tags),
                "source": "wisdom_data.json",
                "type": "WISDOM"
            }
        })
    return wisdom_items


def parse_rdna(filepath):

    """Parses rdna_questions.json for Reverse DNA (RDNA) questions and variants."""
    if not os.path.exists(filepath):
        logging.warning(f"rdna_questions.json not found at {filepath}")
        return []
    import json
    with open(filepath, "r", encoding="utf-8") as f:
        questions = json.load(f)
    
    rdna_items = []
    for q in questions:
        qid = q.get("id", "RDNA-UNK")
        primary_q = q.get("question", "")
        intent_cat = q.get("intent_category", "general")
        variants = q.get("question_variants", [])
        target_dna = q.get("target_dna", {})
        target_col = target_dna.get("collection", "philosophy_dna")
        target_id = target_dna.get("id", "")
        target_title = target_dna.get("title", "")
        confidence_floor = q.get("confidence_floor", 0.75)
        tags = q.get("metadata", {}).get("tags", [])
        
        # Primary question anchor
        doc_primary = (
            f"Question: {primary_q}\n"
            f"Intent: {intent_cat}\n"
            f"Target DNA: [{target_col}] {target_id} - {target_title}\n"
            f"Tags: {', '.join(tags)}"
        )
        rdna_items.append({
            "id": f"{qid}_primary",
            "document": doc_primary,
            "metadata": {
                "rdna_id": qid,
                "variant_type": "primary",
                "question_text": primary_q,
                "intent_category": intent_cat,
                "target_collection": target_col,
                "target_dna_id": target_id,
                "target_dna_title": target_title,
                "confidence_floor": float(confidence_floor),
                "tags": ",".join(tags),
                "source": "rdna_questions.json",
                "type": "RDNA"
            }
        })
        
        # Ingest each variant as an individual searchable anchor
        for idx, var in enumerate(variants):
            doc_var = (
                f"Question Variant: {var}\n"
                f"Canonical Question: {primary_q}\n"
                f"Intent: {intent_cat}\n"
                f"Target DNA: [{target_col}] {target_id} - {target_title}\n"
                f"Tags: {', '.join(tags)}"
            )
            rdna_items.append({
                "id": f"{qid}_v{idx+1}",
                "document": doc_var,
                "metadata": {
                    "rdna_id": qid,
                    "variant_type": "synonym",
                    "question_text": var,
                    "canonical_question": primary_q,
                    "intent_category": intent_cat,
                    "target_collection": target_col,
                    "target_dna_id": target_id,
                    "target_dna_title": target_title,
                    "confidence_floor": float(confidence_floor),
                    "tags": ",".join(tags),
                    "source": "rdna_questions.json",
                    "type": "RDNA"
                }
            })
            
    return rdna_items


def sync(force: bool = False, dry_run: bool = False):
    """Sync DNA source files into ChromaDB.

    Idempotency guard ([STORY-8614] / Finding 17): unless ``force`` is set,
    a source is cleared & re-uploaded only when its SHA256 checksum changed
    since the last successful sync. ``dry_run`` logs the plan and exits
    without touching ChromaDB or the checksum cache.
    """
    checksums = load_checksums()

    # Preflight idempotency plan: decide per-source whether a resync is needed.
    to_sync = {}
    for _collection, _label, src_path in SYNC_SOURCES:
        to_sync[src_path] = _source_changed(src_path, checksums, force)

    # --dry-run: report the plan and exit before touching ChromaDB or the cache.
    if dry_run:
        would_sync = 0
        for _collection, label, src_path in SYNC_SOURCES:
            if to_sync[src_path]:
                would_sync += 1
                logging.info("[DRY-RUN] WOULD-SYNC %-22s <- %s", _collection, label)
            else:
                logging.info("[DRY-RUN] SKIP       %-22s <- %s (checksum unchanged)",
                             _collection, label)
        logging.info("[DRY-RUN] %d of %d sources would be synced. "
                     "No modifications made (ChromaDB and cache untouched).",
                     would_sync, len(SYNC_SOURCES))
        return

    # Everything unchanged and not forced: exit without connecting to ChromaDB.
    if not force and not any(to_sync.values()):
        logging.info("[IDEMPOTENCY] All source checksums unchanged; nothing to sync. "
                     "Use --force for a full rebuild.")
        return

    logging.info(f"Connecting to ChromaDB at {DB_PATH}...")
    client = get_chroma_client()
    
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # 1. Sync feature_dna
    if not to_sync[FEATURE_TRACKER_PATH]:
        logging.info("[IDEMPOTENCY] Skipping feature_dna: FeatureTracker.md checksum unchanged.")
    else:
        logging.info("Parsing FeatureTracker.md...")
        features_raw = parse_feature_tracker(FEATURE_TRACKER_PATH)

        # [DNA-AUDIT] Split parsed items into live entries and skipped/noise entries
        features = [f for f in features_raw if not f.get("_skipped")]
        skipped = [f for f in features_raw if f.get("_skipped")]

        # Emit skip report on every rebuild so stale/pending items are surfaced
        if skipped:
            logging.info("[DNA-SKIP-REPORT] %d feature entries skipped (noise filter: %s):",
                         len(skipped), sorted(DNA_NOISE_STATUSES))
            for s in sorted(skipped, key=lambda x: x["id"]):
                logging.info("  SKIP [%s] %-60s | %s (reason: %s)",
                             s["id"], s["name"][:60], s["status"], s["reason"])
        else:
            logging.info("[DNA-SKIP-REPORT] No entries skipped by noise filter.")

        if features:
            collection_feat = get_safe_collection(client, COLLECTION_FEATURE, ef)
            logging.info("Clearing existing FeatureTracker.md entries from feature_dna...")
            try:
                collection_feat.delete(where={"source": "FeatureTracker.md"})
            except Exception as e:
                logging.warning(f"Could not clear feature_dna collection: {e}")

            ids = [f["id"] for f in features]
            documents = [f["document"] for f in features]
            metadatas = [f["metadata"] for f in features]

            logging.info(f"Uploading {len(ids)} feature entries to feature_dna...")
            collection_feat.add(ids=ids, documents=documents, metadatas=metadatas)
            checksums[FEATURE_TRACKER_PATH] = _sha256_file(FEATURE_TRACKER_PATH)
            logging.info("feature_dna sync complete.")
        else:
            logging.warning("No features parsed from FeatureTracker.md.")

    # 2. Sync behavioral_dna
    if not to_sync[PROTOCOLS_PATH]:
        logging.info("[IDEMPOTENCY] Skipping behavioral_dna/Protocols: Protocols.md checksum unchanged.")
    else:
        logging.info("Parsing Protocols.md...")
        protocols = parse_protocols(PROTOCOLS_PATH)
        if protocols:
            collection_dna = get_safe_collection(client, COLLECTION_DNA, ef)
            logging.info("Clearing existing Protocols.md entries from behavioral_dna...")
            try:
                collection_dna.delete(where={"source": "Protocols.md"})
            except Exception as e:
                logging.warning(f"Could not clear behavioral_dna collection: {e}")

            ids = [p["id"] for p in protocols]
            documents = [p["document"] for p in protocols]
            metadatas = [p["metadata"] for p in protocols]

            logging.info(f"Uploading {len(ids)} BKM entries to behavioral_dna...")
            collection_dna.add(ids=ids, documents=documents, metadatas=metadatas)
            checksums[PROTOCOLS_PATH] = _sha256_file(PROTOCOLS_PATH)
            logging.info("behavioral_dna sync complete.")
        else:
            logging.warning("No protocols parsed from Protocols.md.")

    # 3. Sync LAB_INFRASTRUCTURE.md into behavioral_dna
    if not to_sync[INFRASTRUCTURE_PATH]:
        logging.info("[IDEMPOTENCY] Skipping behavioral_dna/Infrastructure: LAB_INFRASTRUCTURE.md checksum unchanged.")
    else:
        logging.info("Parsing LAB_INFRASTRUCTURE.md...")
        infra_items = parse_infrastructure(INFRASTRUCTURE_PATH)
        if infra_items:
            collection_dna = get_safe_collection(client, COLLECTION_DNA, ef)
            logging.info("Clearing existing LAB_INFRASTRUCTURE.md entries from behavioral_dna...")
            try:
                collection_dna.delete(where={"source": "LAB_INFRASTRUCTURE.md"})
            except Exception as e:
                logging.warning(f"Could not clear LAB_INFRASTRUCTURE entries: {e}")

            ids = [i["id"] for i in infra_items]
            documents = [i["document"] for i in infra_items]
            metadatas = [i["metadata"] for i in infra_items]

            logging.info(f"Uploading {len(ids)} Infrastructure entries to behavioral_dna...")
            collection_dna.add(ids=ids, documents=documents, metadatas=metadatas)
            checksums[INFRASTRUCTURE_PATH] = _sha256_file(INFRASTRUCTURE_PATH)
            logging.info("LAB_INFRASTRUCTURE.md sync complete.")

    # 4. Sync philosophy_dna from philosophy_data.json
    if not to_sync[PHILOSOPHY_DATA_PATH]:
        logging.info("[IDEMPOTENCY] Skipping philosophy_dna: philosophy_data.json checksum unchanged.")
    else:
        logging.info("Parsing philosophy_data.json...")
        philosophy_items = parse_philosophy(PHILOSOPHY_DATA_PATH)
        if philosophy_items:
            collection_phl = get_safe_collection(client, COLLECTION_PHILOSOPHY, ef)
            logging.info("Clearing existing entries from philosophy_dna...")
            try:
                collection_phl.delete(where={"source": "philosophy_data.json"})
            except Exception as e:
                logging.warning(f"Could not clear philosophy_dna entries: {e}")

            ids = [p["id"] for p in philosophy_items]
            documents = [p["document"] for p in philosophy_items]
            metadatas = [p["metadata"] for p in philosophy_items]

            logging.info(f"Uploading {len(ids)} Philosophy entries to philosophy_dna...")
            collection_phl.add(ids=ids, documents=documents, metadatas=metadatas)
            checksums[PHILOSOPHY_DATA_PATH] = _sha256_file(PHILOSOPHY_DATA_PATH)
            logging.info("philosophy_dna sync complete.")

    # 4b. Sync wisdom_dna from wisdom_data.json
    if not to_sync[WISDOM_DATA_PATH]:
        logging.info("[IDEMPOTENCY] Skipping wisdom_dna: wisdom_data.json checksum unchanged.")
    else:
        logging.info("Parsing wisdom_data.json...")
        wisdom_items = parse_wisdom(WISDOM_DATA_PATH)
        if wisdom_items:
            collection_wis = get_safe_collection(client, COLLECTION_WISDOM, ef)
            logging.info("Clearing existing entries from wisdom_dna...")
            try:
                collection_wis.delete(where={"source": "wisdom_data.json"})
            except Exception as e:
                logging.warning(f"Could not clear wisdom_dna entries: {e}")

            ids = [w["id"] for w in wisdom_items]
            documents = [w["document"] for w in wisdom_items]
            metadatas = [w["metadata"] for w in wisdom_items]

            logging.info(f"Uploading {len(ids)} Wisdom entries to wisdom_dna...")
            collection_wis.add(ids=ids, documents=documents, metadatas=metadatas)
            checksums[WISDOM_DATA_PATH] = _sha256_file(WISDOM_DATA_PATH)
            logging.info("wisdom_dna sync complete.")

    # 5. Sync rdna from rdna_questions.json
    if not to_sync[RDNA_QUESTIONS_PATH]:
        logging.info("[IDEMPOTENCY] Skipping rdna: rdna_questions.json checksum unchanged.")
    else:
        logging.info("Parsing rdna_questions.json...")
        rdna_items = parse_rdna(RDNA_QUESTIONS_PATH)
        if rdna_items:
            collection_rdna = get_safe_collection(client, COLLECTION_RDNA, ef)
            logging.info("Clearing existing rdna_questions.json entries from rdna...")
            try:
                collection_rdna.delete(where={"source": "rdna_questions.json"})
            except Exception as e:
                logging.warning(f"Could not clear rdna entries: {e}")

            ids = [r["id"] for r in rdna_items]
            documents = [r["document"] for r in rdna_items]
            metadatas = [r["metadata"] for r in rdna_items]

            logging.info(f"Uploading {len(ids)} Reverse DNA (RDNA) question entries to rdna...")
            collection_rdna.add(ids=ids, documents=documents, metadatas=metadatas)
            checksums[RDNA_QUESTIONS_PATH] = _sha256_file(RDNA_QUESTIONS_PATH)
            logging.info("rdna collection sync complete.")

    save_checksums(checksums)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Sync DNA source files (FeatureTracker.md, Protocols.md, "
                    "LAB_INFRASTRUCTURE.md, philosophy/wisdom/rdna JSON) into ChromaDB."
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Clear and re-upload every collection, ignoring the checksum cache.",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Log which collections would be synced, then exit without modifying "
             "ChromaDB or the checksum cache.",
    )
    args = parser.parse_args()
    sync(force=args.force, dry_run=args.dry_run)


