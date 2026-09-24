#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_connections_graph.py [v1.0]
[FEAT-596 / Sprint 85 Story 85.1]
Compiles 1st-degree explicit_links and shared-tag semantic connections across all 8 DNA domains
(PHL, WIS, FEAT, BKM, SPRINT, DISC, RDNA, ART, RESUME) into graph JSON for the 2D Synapse Visualizer.
"""

import json
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "field_notes" / "data"
MANIFEST_PATH = DATA_DIR / "dna_manifest.json"
OUTPUT_GRAPH_PATH = DATA_DIR / "dna_connections_graph.json"


def extract_all_cards(manifest: dict) -> list:
    cards = []
    seen_ids = set()

    for domain_key, items in manifest.items():
        if domain_key in ("papers", "schema_version", "last_updated"):
            continue
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict):
                    cid = item.get("id")
                    if cid and cid not in seen_ids:
                        seen_ids.add(cid)
                        # Determine canonical domain
                        domain = item.get("domain")
                        if not domain:
                            if cid.startswith("PHL-"): domain = "PHL"
                            elif cid.startswith("WIS-"): domain = "WIS"
                            elif cid.startswith("FEAT-"): domain = "FEAT"
                            elif cid.startswith("BKM-"): domain = "BKM"
                            elif cid.startswith("DISC-"): domain = "DISC"
                            elif cid.startswith("SPR-"): domain = "SPRINT"
                            elif cid.startswith("RDNA-"): domain = "RDNA"
                            elif cid.startswith("RESUME-"): domain = "RESUME"
                            elif cid.startswith("ART-"): domain = "ART"
                            else: domain = domain_key.upper()[:6]
                        item["_resolved_domain"] = domain
                        cards.append(item)
    return cards


def compile_connections_graph(manifest: dict = None) -> dict:
    if manifest is None:
        if MANIFEST_PATH.exists():
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                manifest = json.load(f)
        else:
            manifest = {}

    cards = extract_all_cards(manifest)
    card_map = {c["id"]: c for c in cards}

    nodes = []
    links = []
    link_set = set()
    degree_map = defaultdict(int)

    # 1. Collect all explicit connections
    for c in cards:
        cid = c["id"]
        meta = c.get("metadata") or {}
        synth = c.get("synthesis") or {}
        
        explicit = set()
        if "explicit_links" in c and isinstance(c["explicit_links"], list):
            explicit.update(c["explicit_links"])
        if "explicit_links" in meta and isinstance(meta["explicit_links"], list):
            explicit.update(meta["explicit_links"])
        if "lab_anchors" in synth and isinstance(synth["lab_anchors"], list):
            explicit.update(synth["lab_anchors"])

        for target in explicit:
            if target in card_map and target != cid:
                pair = tuple(sorted([cid, target]))
                if pair not in link_set:
                    link_set.add(pair)
                    links.append({
                        "source": pair[0],
                        "target": pair[1],
                        "type": "explicit",
                        "weight": 2.0
                    })
                    degree_map[pair[0]] += 1
                    degree_map[pair[1]] += 1

    # 2. Add tag co-occurrence connections (if cards share >= 2 tags)
    tag_to_cards = defaultdict(list)
    for c in cards:
        cid = c["id"]
        meta = c.get("metadata") or {}
        tags = set(c.get("tags") or [])
        tags.update(meta.get("tags") or [])
        clean_tags = {t.lower().strip("#") for t in tags if len(t) > 3}
        for t in clean_tags:
            tag_to_cards[t].append(cid)

    for tag, cids in tag_to_cards.items():
        if len(cids) > 1 and len(cids) < 30:  # Avoid ultra-dense tags connecting everything
            for i in range(len(cids)):
                for j in range(i + 1, min(len(cids), i + 4)):
                    pair = tuple(sorted([cids[i], cids[j]]))
                    if pair not in link_set:
                        link_set.add(pair)
                        links.append({
                            "source": pair[0],
                            "target": pair[1],
                            "type": "tag_cluster",
                            "tag": tag,
                            "weight": 1.0
                        })
                        degree_map[pair[0]] += 1
                        degree_map[pair[1]] += 1

    # 3. Build Nodes with resolved domain, degree, title
    census = defaultdict(int)
    for c in cards:
        cid = c["id"]
        domain = c.get("_resolved_domain", "DNA")
        census[domain] += 1
        
        synth = c.get("synthesis") or {}
        title = c.get("title") or synth.get("title") or cid
        summary = c.get("summary") or synth.get("narrative_context") or ""
        meta = c.get("metadata") or {}
        tags = list(set((c.get("tags") or []) + (meta.get("tags") or [])))

        nodes.append({
            "id": cid,
            "domain": domain,
            "title": title,
            "summary": summary[:240],
            "tags": tags[:6],
            "degree": degree_map[cid]
        })

    graph = {
        "status": "ok",
        "total_nodes": len(nodes),
        "total_links": len(links),
        "census": dict(census),
        "nodes": nodes,
        "links": links
    }
    return graph


def main():
    graph = compile_connections_graph()
    OUTPUT_GRAPH_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_GRAPH_PATH, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2)
    print(f"✅ Generated DNA connections graph with {graph['total_nodes']} nodes and {graph['total_links']} links -> {OUTPUT_GRAPH_PATH}")


if __name__ == "__main__":
    main()
