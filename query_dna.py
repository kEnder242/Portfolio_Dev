#!/usr/bin/env python3
import os
import sys
import argparse
import chromadb
from chromadb.utils import embedding_functions

DB_PATH = os.path.expanduser("~/AcmeLab/chroma_db")
COLLECTION_DNA = "behavioral_dna"
COLLECTION_FEATURE = "feature_dna"

def query_collection(client, collection_name, query_text, limit, raw):
    try:
        ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        collection = client.get_collection(name=collection_name, embedding_function=ef)
    except Exception as e:
        print(f"❌ Error loading collection '{collection_name}': {e}")
        return

    print(f"\n🔍 Querying '{collection_name}' for: '{query_text}' (limit: {limit})")
    try:
        res = collection.query(query_texts=[query_text], n_results=limit)
    except Exception as e:
        print(f"❌ Query failed: {e}")
        return

    if not res or not res["documents"] or not res["documents"][0]:
        print("   No matches found.")
        return

    for idx, (doc, meta, distance) in enumerate(zip(res["documents"][0], res["metadatas"][0], res["distances"][0])):
        print(f"   [{idx + 1}] Distance: {distance:.4f}")
        if "bkm_id" in meta:
            print(f"       ID: {meta['bkm_id']} - Name: {meta['name']}")
        elif "feature_id" in meta:
            print(f"       ID: {meta['feature_id']} - Name: {meta['name']} (Status: {meta['status']})")
        
        if raw:
            print("       --- Document ---")
            for line in doc.splitlines():
                print(f"       {line}")
        else:
            lines = doc.splitlines()
            snippet = next((line.strip() for line in lines if line.strip() and not line.startswith("ID:") and not line.startswith("Name:")), "")
            print(f"       Snippet: {snippet[:120]}...")

def main():
    parser = argparse.ArgumentParser(description="Query ClaraDB (ChromaDB) DNA Tooling for BKMs and Features.")
    parser.add_argument("query", nargs="+", help="The query terms to search for.")
    parser.add_argument("-t", "--type", choices=["bkm", "feat", "all"], default="all", help="The type of collection to search (default: all).")
    parser.add_argument("-n", "--limit", type=int, default=3, help="Maximum number of results to return per collection (default: 3).")
    parser.add_argument("--raw", action="store_true", help="Print the full content of matching documents.")
    
    args = parser.parse_args()
    query_text = " ".join(args.query)
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Error: ChromaDB database not found at {DB_PATH}")
        sys.exit(1)
        
    client = chromadb.PersistentClient(path=DB_PATH)
    
    if args.type in ("bkm", "all"):
        query_collection(client, COLLECTION_DNA, query_text, args.limit, args.raw)
    if args.type in ("feat", "all"):
        query_collection(client, COLLECTION_FEATURE, query_text, args.limit, args.raw)

if __name__ == "__main__":
    main()
