#!/usr/bin/env python3
"""[FEAT-662 / BKM-085 / ADR-008] Polymorphic Kabal DNA Registry & Variable Namespace Resolver.

Manages polymorphic Kabal manuscript collections stored in Portfolio_Dev/papers/<slug>/<slug>_kabal.json.
Provides variable namespace resolution (<ROOT>.<SUB>-<NUM>), local card access,
and ChromaDB (:8001) vector sync for ambient recall hooks.
"""

import hashlib
import json
import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("kabal_registry")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

BASE_DIR = Path(__file__).resolve().parent.parent
PAPERS_DIR = BASE_DIR / "papers"
CHECKSUMS_FILE = BASE_DIR / "dna" / ".sync_checksums.json"
CHROMA_HOST = os.environ.get("CHROMA_HOST", "127.0.0.1")
CHROMA_PORT = int(os.environ.get("CHROMA_PORT", "8001"))
COLLECTION_KABAL_DNA = "kabal_dna"


def get_papers_dir() -> Path:
    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    return PAPERS_DIR


def get_kabal_path(slug: str) -> Path:
    slug_clean = slug.lower().strip().replace(" ", "_")
    return get_papers_dir() / slug_clean / f"{slug_clean}_kabal.json"


def get_spine_path(slug: str) -> Path:
    slug_clean = slug.lower().strip().replace(" ", "_")
    return get_papers_dir() / slug_clean / f"{slug_clean}_spine.json"


def format_card_id(root: str, sub: Optional[str], num: Any) -> str:
    """Formats a canonical stamp string: [ROOT.SUB-NUM] or [ROOT-NUM]."""
    root_clean = root.upper().strip()
    try:
        num_clean = f"{int(num):03d}"
    except (ValueError, TypeError):
        num_clean = str(num).strip()

    if sub:
        sub_clean = sub.upper().strip()
        return f"{root_clean}.{sub_clean}-{num_clean}"
    return f"{root_clean}-{num_clean}"


def resolve_stamp(root_or_slug: str, sub_or_num: str, num: Optional[Any] = None) -> str:
    """Resolves local numbers and sub-namespaces to canonical stamp strings.
    
    Examples:
      resolve_stamp("RESUME", "EXP", "042") -> "[RESUME.EXP-042]"
      resolve_stamp("RESUME.EXP", "042")     -> "[RESUME.EXP-042]"
      resolve_stamp("RESUME", "042")         -> "[RESUME-042]"
    """
    if num is not None:
        raw_id = format_card_id(root_or_slug, sub_or_num, num)
    else:
        # Check if root_or_slug already contains a dot (e.g. RESUME.EXP)
        if "." in root_or_slug:
            parts = root_or_slug.split(".", 1)
            raw_id = format_card_id(parts[0], parts[1], sub_or_num)
        else:
            raw_id = format_card_id(root_or_slug, None, sub_or_num)
    
    return f"[{raw_id}]"


def parse_stamp(stamp: str) -> Optional[Dict[str, str]]:
    """Parses a stamp string like '[RESUME.EXP-042]' or 'RESUME.EXP-042' into components."""
    clean = stamp.strip().strip("[]")
    m = re.match(r"^([A-Z0-9_-]+)(?:\.([A-Z0-9_-]+))?-([A-Z0-9_-]+)$", clean, re.IGNORECASE)
    if not m:
        return None
    root, sub, num = m.groups()
    return {
        "root": root.upper(),
        "sub": sub.upper() if sub else "",
        "num": num,
        "canonical_id": f"{root.upper()}{'.' + sub.upper() if sub else ''}-{num}",
        "stamp": f"[{root.upper()}{'.' + sub.upper() if sub else ''}-{num}]",
    }


def list_kabals() -> List[Dict[str, Any]]:
    """Discovers all valid Kabal bundles under Portfolio_Dev/papers/*/*_kabal.json."""
    papers_dir = get_papers_dir()
    kabals = []
    for bundle_dir in sorted(papers_dir.glob("*")):
        if bundle_dir.is_dir():
            kabal_file = bundle_dir / f"{bundle_dir.name}_kabal.json"
            spine_file = bundle_dir / f"{bundle_dir.name}_spine.json"
            if kabal_file.exists():
                try:
                    with open(kabal_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    cards = data.get("cards", [])
                    kabals.append({
                        "slug": bundle_dir.name,
                        "title": data.get("title", bundle_dir.name.replace("_", " ").title()),
                        "variable_prefix": data.get("variable_prefix", bundle_dir.name.upper()),
                        "card_count": len(cards),
                        "kabal_path": str(kabal_file),
                        "spine_path": str(spine_file) if spine_file.exists() else None,
                        "has_spine": spine_file.exists(),
                        "updated_at": data.get("updated_at"),
                    })
                except Exception as e:
                    logger.warning(f"Error reading kabal {kabal_file}: {e}")
    return kabals


def load_kabal(slug: str) -> Dict[str, Any]:
    """Loads a Kabal bundle JSON by slug or creates an empty schema if nonexistent."""
    path = get_kabal_path(slug)
    if not path.exists():
        return {
            "slug": slug.lower(),
            "variable_prefix": slug.upper(),
            "title": slug.replace("_", " ").title(),
            "version": 1,
            "cards": [],
            "created_at": None,
            "updated_at": None,
        }
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_kabal(slug: str, data: Dict[str, Any]) -> Path:
    """Saves a Kabal JSON file atomically to papers/<slug>/<slug>_kabal.json."""
    path = get_kabal_path(slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.parent / f".tmp_{path.name}"
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    temp_path.replace(path)
    logger.info(f"Saved kabal '{slug}' ({len(data.get('cards', []))} cards) to {path}")
    return path


def get_card(stamp_or_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a single card by canonical ID, stamp, or local ID across all kabals."""
    parsed = parse_stamp(stamp_or_id)
    if parsed:
        target_slug = parsed["root"].lower()
        kabal_data = load_kabal(target_slug)
        for card in kabal_data.get("cards", []):
            if card.get("id") == parsed["canonical_id"]:
                return card
    
    # Fallback: scan all kabals
    clean = stamp_or_id.strip().strip("[]")
    for k in list_kabals():
        data = load_kabal(k["slug"])
        for card in data.get("cards", []):
            if card.get("id") == clean or card.get("local_id") == clean:
                return card
    return None


def sync_to_chroma(slug_filter: Optional[str] = None) -> Dict[str, int]:
    """Syncs Kabal cards into ChromaDB :8001 under collection 'kabal_dna'."""
    try:
        import chromadb
        client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
        collection = client.get_or_create_collection(name=COLLECTION_KABAL_DNA)
    except Exception as e:
        logger.warning(f"ChromaDB connection unavailable at {CHROMA_HOST}:{CHROMA_PORT}: {e}")
        return {"synced": 0, "skipped": 0, "error": str(e)}

    synced = 0
    skipped = 0
    kabals_to_sync = [load_kabal(slug_filter)] if slug_filter else [load_kabal(k["slug"]) for k in list_kabals()]

    for k in kabals_to_sync:
        slug = k.get("slug", "unknown")
        prefix = k.get("variable_prefix", slug.upper())
        batch_ids = []
        batch_docs = []
        batch_metas = []

        for card in k.get("cards", []):
            card_id = card.get("id") or format_card_id(prefix, card.get("sub_namespace"), card.get("local_id", 0))
            origin = card.get("origin", {})
            synthesis = card.get("synthesis", {})
            doc_text = f"[{card_id}] {synthesis.get('title', '')}\n\n{synthesis.get('summary', '')}\n\nEVIDENCE:\n{origin.get('raw_text', '')}"
            meta = {
                "kabal": slug,
                "card_id": card_id,
                "local_id": str(card.get("local_id", "")),
                "sub_namespace": card.get("sub_namespace", ""),
                "title": synthesis.get("title", ""),
                "type": "KABAL",
            }
            batch_ids.append(card_id)
            batch_docs.append(doc_text)
            batch_metas.append(meta)

        if batch_ids:
            try:
                collection.upsert(
                    ids=batch_ids,
                    documents=batch_docs,
                    metadatas=batch_metas,
                )
                synced += len(batch_ids)
            except Exception as e:
                logger.error(f"Failed to batch upsert kabal '{slug}': {e}")
                skipped += len(batch_ids)

    logger.info(f"Kabal Chroma sync complete: {synced} synced, {skipped} skipped.")
    return {"synced": synced, "skipped": skipped}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Kabal DNA Registry CLI")
    parser.add_argument("--list", action="store_true", help="List all registered kabals")
    parser.add_argument("--resolve", nargs="+", help="Resolve stamp: root sub num or root num")
    parser.add_argument("--sync-chroma", action="store_true", help="Sync Kabal cards to ChromaDB")
    args = parser.parse_args()

    if args.list:
        kabals = list_kabals()
        print(f"Found {len(kabals)} registered Kabal(s):")
        for k in kabals:
            print(f" - {k['slug']} ({k['variable_prefix']}): {k['card_count']} cards [Spine: {'YES' if k['has_spine'] else 'NO'}]")
    elif args.resolve:
        if len(args.resolve) == 2:
            print(resolve_stamp(args.resolve[0], args.resolve[1]))
        elif len(args.resolve) == 3:
            print(resolve_stamp(args.resolve[0], args.resolve[1], args.resolve[2]))
        else:
            print(f"Invalid resolve args: {args.resolve}")
    elif args.sync_chroma:
        res = sync_to_chroma()
        print(f"Sync result: {res}")
    else:
        parser.print_help()
