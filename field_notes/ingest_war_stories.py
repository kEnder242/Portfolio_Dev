#!/usr/bin/env python3
"""
[Story 83.9 / FEAT-582] Ingest War Stories from stories.html into WIS Cards
Extracts the 29 empirical war stories from Portfolio_Dev/field_notes/stories.html
into structured WIS-001..WIS-029 cards conforming to the BKM-060 Polymorphic DNA Schema.
"""

import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

FIELD_NOTES_DIR = Path(__file__).resolve().parent
STORIES_HTML_PATH = FIELD_NOTES_DIR / "stories.html"
WISDOM_DATA_PATH = FIELD_NOTES_DIR / "data" / "wisdom_data.json"

THEME_ANCHORS = {
    "Security & Manageability": ["BKM-012", "FEAT-583"],
    "Systems Architecture & Automation": ["BKM-060", "FEAT-582", "FEAT-586"],
    "Platform Validation Methodology": ["BKM-024", "FEAT-584"],
    "Engineering Leadership": ["PHL-033", "BKM-049", "PHL-034"]
}

def clean_text(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()

def parse_stories():
    with open(STORIES_HTML_PATH, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    wis_cards = []
    card_index = 1

    sections = soup.find_all("section")
    for section in sections:
        sec_title_el = section.find(["h2", "h3"], class_="section-title") or section.find(["h2", "h3"])
        sec_title = sec_title_el.get_text(strip=True) if sec_title_el else "Platform Engineering"
        
        articles = section.find_all("article")
        for art in articles:
            art_id = art.get("id", f"story-{card_index}")
            h3_el = art.find("h3")
            title = h3_el.get_text(strip=True) if h3_el else f"War Story {card_index}"
            
            meta_div = art.find("div", class_="meta")
            meta_text = meta_div.get_text(strip=True) if meta_div else ""
            
            # Extract tags from meta
            tags = [sec_title.lower().replace(" & ", "-").replace(" ", "-")]
            if meta_text:
                parts = meta_text.split("|")
                for p in parts:
                    if ":" in p:
                        k, v = p.split(":", 1)
                        tag_val = clean_text(v).lower().replace(" ", "-")
                        if tag_val and tag_val not in tags:
                            tags.append(tag_val)

            # Extract body paragraphs
            paragraphs = [p.get_text(strip=True) for p in art.find_all("p")]
            full_text = " ".join(paragraphs)
            
            # Narrative lesson distillation
            strong_el = art.find("strong")
            key_lesson = strong_el.get_text(strip=True) if strong_el else (paragraphs[-1] if paragraphs else title)
            
            wis_id = f"WIS-{card_index:03d}"
            anchors = THEME_ANCHORS.get(sec_title, ["BKM-060"])

            card = {
                "id": wis_id,
                "theme": sec_title,
                "paper_order": card_index,
                "origin": {
                    "author": "jallred",
                    "text": full_text,
                    "source": f"Portfolio Stories (stories.html#{art_id})",
                    "immutable": True,
                    "created_at": "2026-09-17T17:00:00Z"
                },
                "synthesis": {
                    "title": title,
                    "narrative_context": key_lesson,
                    "lab_anchors": anchors,
                    "review_notes": f"Ingested from empirical field note #{art_id}.",
                    "last_refined_by": "AGY",
                    "refinement_version": 1
                },
                "metadata": {
                    "tags": tags,
                    "explicit_links": anchors + ["PHL-034"],
                    "aliases": [art_id],
                    "status": "APPROVED",
                    "bucket_id": f"bucket_{sec_title.lower().replace(' & ', '_').replace(' ', '_')}"
                }
            }
            wis_cards.append(card)
            card_index += 1

    print(f"[*] Successfully parsed {len(wis_cards)} War Stories from stories.html.")
    WISDOM_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(WISDOM_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(wis_cards, f, indent=2)
    print(f"[+] Written to {WISDOM_DATA_PATH}")

if __name__ == "__main__":
    parse_stories()
