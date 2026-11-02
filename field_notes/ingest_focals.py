#!/usr/bin/env python3
"""
[FEAT-683] / [Story 109.5] Ingest Annual Performance Reviews into focal_mesh.json and ChromaDB focal_dna.

Parses annual reviews from /home/jallred/knowledge_base/Performance review 2008-2018.txt,
deduplicates against focal_ledger.json, creates Portfolio_Dev/field_notes/data/focal_mesh.json,
and inserts all focal milestones into ChromaDB collection 'focal_dna' on port 8001.
"""

import os
import sys
import json
import re
from pathlib import Path

# Paths
KNOWLEDGE_BASE = Path("/home/jallred/knowledge_base")
REVIEW_TXT = KNOWLEDGE_BASE / "Performance review 2008-2018.txt"
DATA_DIR = Path("/home/jallred/Portfolio_Dev/field_notes/data")
FOCAL_LEDGER_FILE = DATA_DIR / "focal_ledger.json"
FOCAL_MESH_FILE = DATA_DIR / "focal_mesh.json"

CHROMA_HOST = os.getenv("CHROMA_HOST", "127.0.0.1")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8001"))


def extract_keywords(text: str) -> list[str]:
    """Extract notable hardware and technology keywords."""
    tech_patterns = [
        r"\b(?:DCMI|DCTS|SOL|IPMI|ESB2|iBMC|PECI|MCTP|Redfish|SIMICS|S3E|Optane|AEP|Mellanox|Thurley|Bensley|Willowbrook|Romley|Grantley|Purley|Whitley|Fox Cove|Red Dog|FTF|Aardvark|I2C|PCIe|BIOS|MSR|BMC)\b",
        r"\b(?:Python|Linux|Firmware|Validation|Hardware|Automation)\b"
    ]
    keywords = set()
    for pat in tech_patterns:
        for match in re.finditer(pat, text, re.IGNORECASE):
            keywords.add(match.group(0).lower())
    return sorted(list(keywords))


def parse_review_sections(text: str) -> list[dict]:
    """Parse text into individual review sections."""
    raw_sections = re.split(r"\n(?=(?:Review Period|Job Title:|Oct`2007))", text)
    focals = []

    for idx, s in enumerate(raw_sections):
        s_clean = s.strip()
        if not s_clean:
            continue

        lines = [line.strip() for line in s_clean.splitlines() if line.strip()]
        header = lines[0] if lines else ""

        # Extract Year & Period
        year_match = re.search(r"\b(20\d{2})\b", header)
        if not year_match:
            year_match = re.search(r"['`](0[7-9]|1[0-8])\b", header)
            if year_match:
                year = int("20" + year_match.group(1))
            else:
                year = 2007 if "2007" in header or "`07" in header else 2008
        else:
            year = int(year_match.group(1))

        # Extract Job Title
        title_match = re.search(r"Job Title[:\s]+([^\n\r\t]+?)(?:Review Period|Grade|Job Description|$)", s_clean, re.IGNORECASE)
        job_title = title_match.group(1).strip() if title_match else "Software / Firmware Engineer"
        # Clean title
        job_title = re.sub(r"\s+", " ", job_title).strip()

        # Extract Accomplishments
        acc_match = re.search(r"Key Accomplishments[^\n]*\n(.*?)(?=\n(?:Strengths|Areas for Improvement|Evaluation|Performance Summary|$))", s_clean, re.DOTALL | re.IGNORECASE)
        accomplishments = acc_match.group(1).strip() if acc_match else s_clean[:800]

        # Extract Summary or first substantive paragraph of accomplishments
        acc_paras = [p.strip() for p in accomplishments.split("\n\n") if len(p.strip()) > 30]
        primary_para = acc_paras[0] if acc_paras else accomplishments[:300]
        # First 1-2 sentences as summary
        sentences = re.split(r"(?<=[.!?])\s+", primary_para)
        summary = " ".join(sentences[:2]) if len(sentences) >= 2 else primary_para[:200]

        tags = extract_keywords(s_clean)
        domain = "firmware_development"
        if "validation" in job_title.lower():
            domain = "system_validation"
        elif "mkt" in job_title.lower() or "marketing" in job_title.lower():
            domain = "technical_marketing"

        focal_id = f"FOCAL-{year}-001"
        event_era = f"{year}-Q4"
        document_date = f"{year}-12-31"

        focals.append({
            "id": focal_id,
            "date": document_date,
            "event_era": event_era,
            "event_year": year,
            "document_date": document_date,
            "covered_period": str(year),
            "job_title": job_title,
            "summary": f"{job_title} ({year}): {summary}",
            "evidence": primary_para,
            "full_text": s_clean,
            "domain": domain,
            "impact_level": 4,
            "refinement_level": 3,
            "status": "SATURATED",
            "tags": tags,
        })

    return focals


def load_existing_ledger() -> list[dict]:
    if FOCAL_LEDGER_FILE.exists():
        try:
            with open(FOCAL_LEDGER_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("focal_gems", [])
        except Exception as e:
            print(f"Warning: Failed to load {FOCAL_LEDGER_FILE}: {e}")
    return []


def merge_focals(existing: list[dict], parsed: list[dict]) -> list[dict]:
    """Merge parsed focals with existing ledger, deduplicating by ID or (event_year, domain)."""
    merged_by_id = {}

    # Add existing ledger items
    for item in existing:
        merged_by_id[item["id"]] = item

    # Add parsed items
    for item in parsed:
        fid = item["id"]
        if fid in merged_by_id:
            # Suffix with -002 if existing is different
            existing_summary = merged_by_id[fid].get("summary", "").lower()
            if item["summary"].lower()[:50] not in existing_summary:
                fid = f"FOCAL-{item['event_year']}-002"
                item["id"] = fid
                merged_by_id[fid] = item
        else:
            merged_by_id[fid] = item

    return sorted(list(merged_by_id.values()), key=lambda x: (x.get("event_year", 0), x.get("id", "")))


def ingest_to_chroma(focals: list[dict]):
    """Embed and insert focal items into ChromaDB focal_dna collection."""
    import chromadb
    from fastembed import TextEmbedding

    print(f"Connecting to ChromaDB at {CHROMA_HOST}:{CHROMA_PORT}...")
    client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    client.heartbeat()

    # Get or create collection with cosine similarity
    col_name = "focal_dna"
    try:
        col = client.get_or_create_collection(
            name=col_name,
            metadata={"hnsw:space": "cosine", "description": "Tier 2 Strategic Career Focals & Annual Review Milestones (FEAT-683)"}
        )
    except Exception as e:
        print(f"Error accessing collection {col_name}: {e}")
        return 0

    print(f"Loading FastEmbed model sentence-transformers/all-MiniLM-L6-v2...")
    model = TextEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

    ids = []
    documents = []
    metadatas = []

    for f in focals:
        fid = f["id"]
        doc_text = f"{f['summary']}\n\nEvidence: {f.get('evidence', '')}\n\nTags: {', '.join(f.get('tags', []))}"
        meta = {
            "id": fid,
            "year": int(f.get("event_year", 2000)),
            "era": f.get("event_era", ""),
            "job_title": f.get("job_title", ""),
            "domain": f.get("domain", "career_timeline"),
            "status": f.get("status", "SATURATED"),
            "impact_level": int(f.get("impact_level", 4)),
            "covered_period": str(f.get("covered_period", f.get("event_year", ""))),
            "document_date": f.get("document_date", ""),
        }
        ids.append(fid)
        documents.append(doc_text)
        metadatas.append(meta)

    print(f"Generating FastEmbed embeddings for {len(documents)} focals...")
    embeddings = [e.tolist() for e in model.embed(documents)]

    print(f"Upserting {len(ids)} items into '{col_name}'...")
    col.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )

    total_count = col.count()
    print(f"ChromaDB '{col_name}' collection count: {total_count}")
    return total_count


def main():
    print("=== Story 109.5: Ingest Annual Reviews into focal_mesh.json & focal_dna ===")
    if not REVIEW_TXT.exists():
        print(f"Error: Review file not found at {REVIEW_TXT}")
        sys.exit(1)

    with open(REVIEW_TXT, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    parsed = parse_review_sections(text)
    print(f"Parsed {len(parsed)} focal milestones from {REVIEW_TXT.name}:")
    for p in parsed:
        print(f"  - [{p['id']}] {p['job_title']} ({p['event_year']}): {p['summary'][:70]}...")

    existing = load_existing_ledger()
    print(f"Loaded {len(existing)} existing items from focal_ledger.json")

    merged = merge_focals(existing, parsed)
    print(f"Total merged focal milestones: {len(merged)}")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    mesh_payload = {
        "version": "2.0.0",
        "description": "Tier 2 Strategic Career Focals & Annual Review Milestones (FEAT-683)",
        "source": "Performance review 2008-2018.txt + focal_ledger.json",
        "total_focals": len(merged),
        "focal_gems": merged
    }

    with open(FOCAL_MESH_FILE, "w", encoding="utf-8") as f:
        json.dump(mesh_payload, f, indent=2)
    print(f"Wrote {len(merged)} focal items to {FOCAL_MESH_FILE}")

    # Ingest to ChromaDB focal_dna
    count = ingest_to_chroma(merged)
    if count >= 10:
        print(f"SUCCESS: focal_dna collection populated with {count} records (>= 10 requirement satisfied).")
    else:
        print(f"WARNING: focal_dna collection populated with {count} records (< 10).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
