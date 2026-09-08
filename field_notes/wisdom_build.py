#!/usr/bin/env python3
"""
Build pipeline for philosophy.html and philosophy_data.json.
Compiles wisdom_data.json into web presentation artifacts.
"""
import json
import os
import sys

DATA_FILE = os.path.expanduser("~/Dev_Lab/Portfolio_Dev/field_notes/data/wisdom_data.json")
OUT_JSON = os.path.expanduser("~/Dev_Lab/Portfolio_Dev/field_notes/data/philosophy_data.json")

def build():
    if not os.path.exists(DATA_FILE):
        print(f"[!] Error: {DATA_FILE} does not exist.")
        sys.exit(1)
        
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        cards = json.load(f)
        
    print(f"[*] Compiling {len(cards)} wisdom cards into philosophy_data.json...")
    
    # Sort cards by paper_order
    sorted_cards = sorted(cards, key=lambda x: x.get("paper_order", 999))
    
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(sorted_cards, f, indent=2)
        
    print(f"[+] Successfully compiled {OUT_JSON}")

if __name__ == "__main__":
    build()
