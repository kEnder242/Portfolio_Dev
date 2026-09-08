#!/usr/bin/env python3
import os
import re
import sys
import logging
import chromadb
from chromadb.utils import embedding_functions

# Config
DB_PATH = os.path.expanduser("~/AcmeLab/chroma_db")
COLLECTION_DNA = "behavioral_dna"
COLLECTION_FEATURE = "feature_dna"
COLLECTION_PHILOSOPHY = "philosophy_dna"

FEATURE_TRACKER_PATH = os.path.expanduser("~/Dev_Lab/Portfolio_Dev/FeatureTracker.md")
PROTOCOLS_PATH = os.path.expanduser("~/Dev_Lab/HomeLabAI/docs/Protocols.md")
INFRASTRUCTURE_PATH = os.path.expanduser("~/Dev_Lab/HomeLabAI/docs/LAB_INFRASTRUCTURE.md")
WISDOM_DATA_PATH = os.path.expanduser("~/Dev_Lab/Portfolio_Dev/field_notes/data/wisdom_data.json")

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


def parse_wisdom(filepath):
    """Parses wisdom_data.json for WIS-xxx wisdom and philosophy cards."""
    if not os.path.exists(filepath):
        logging.warning(f"wisdom_data.json not found at {filepath}")
        return []
    import json
    with open(filepath, "r", encoding="utf-8") as f:
        cards = json.load(f)
    
    wisdom_items = []
    for c in cards:
        wid = c.get("id", "WIS-UNK")
        theme = c.get("theme", "Philosophy")
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
                "tags": ",".join(tags),
                "source": "wisdom_data.json",
                "type": "WISDOM"
            }
        })
    return wisdom_items


def sync():
    logging.info(f"Connecting to ChromaDB at {DB_PATH}...")
    client = get_chroma_client()
    
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # 1. Sync feature_dna
    logging.info("Parsing FeatureTracker.md...")
    features = parse_feature_tracker(FEATURE_TRACKER_PATH)
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
        logging.info("feature_dna sync complete.")
    else:
        logging.warning("No features parsed from FeatureTracker.md.")

    # 2. Sync behavioral_dna
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
        logging.info("behavioral_dna sync complete.")
    else:
        logging.warning("No protocols parsed from Protocols.md.")

    # 3. Sync LAB_INFRASTRUCTURE.md into behavioral_dna
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
        logging.info("LAB_INFRASTRUCTURE.md sync complete.")

    # 4. Sync philosophy_dna from wisdom_data.json
    logging.info("Parsing wisdom_data.json...")
    wisdom_items = parse_wisdom(WISDOM_DATA_PATH)
    if wisdom_items:
        collection_phl = get_safe_collection(client, COLLECTION_PHILOSOPHY, ef)
        logging.info("Clearing existing wisdom_data.json entries from philosophy_dna...")
        try:
            collection_phl.delete(where={"source": "wisdom_data.json"})
        except Exception as e:
            logging.warning(f"Could not clear philosophy_dna entries: {e}")

        ids = [w["id"] for w in wisdom_items]
        documents = [w["document"] for w in wisdom_items]
        metadatas = [w["metadata"] for w in wisdom_items]

        logging.info(f"Uploading {len(ids)} Wisdom & Philosophy entries to philosophy_dna...")
        collection_phl.add(ids=ids, documents=documents, metadatas=metadatas)
        logging.info("philosophy_dna sync complete.")
