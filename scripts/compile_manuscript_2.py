#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compile_manuscript_2.py [v1.0]
[FEAT-594 / Sprint 85 Story 85.4]
Compiles Manuscript #2 ("Semantic Packing, Ideographic DNA & The Voice Vector Space")
into structured Paper AST and registers it in the Paper catalog.
"""

import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FIELD_NOTES_DIR = BASE_DIR / "field_notes"
DATA_DIR = FIELD_NOTES_DIR / "data"
PAPERS_DIR = DATA_DIR / "papers"
MD_PATH = FIELD_NOTES_DIR / "dna_semantic_packing_and_voice_vector_space.md"
OUTPUT_AST_PATH = PAPERS_DIR / "PAPER-002_SEMANTIC_PACKING.json"
MANIFEST_PATH = DATA_DIR / "dna_manifest.json"


def parse_markdown_to_ast(md_text: str) -> dict:
    lines = md_text.splitlines()
    
    title = "Semantic Packing, Ideographic DNA & The Voice Vector Space"
    subtitle = "Applied Armchair Philosophy & Mathematical Decoupling"
    author = "Jason Allred & AGY"
    
    sections = []
    current_sec = None
    current_par_lines = []
    par_counter = 1
    sec_counter = 1
    
    def flush_paragraph():
        nonlocal current_par_lines, par_counter
        if not current_sec or not current_par_lines:
            current_par_lines = []
            return
        text = " ".join([l.strip() for l in current_par_lines if l.strip()])
        if not text:
            current_par_lines = []
            return
            
        # Extract citations / anchors like [PHL-035], [FEAT-586], [WIS-012], etc.
        citations = re.findall(r'\[(PHL-\d+|WIS-\d+|FEAT-\d+|BKM-\d+|DISC-\d+|RESUME-\d+|arXiv:[a-zA-Z0-9\.\/]+)\]', text)
        
        par_id = f"PAR-{sec_counter:02d}_{par_counter:02d}"
        par_node = {
            "id": par_id,
            "text": text,
            "citations": list(dict.fromkeys(citations)),
            "variants": {
                "academic": text,
                "executive": text[:180] + "..." if len(text) > 180 else text,
                "casual": text
            },
            "dirty": False,
            "review_flags": []
        }
        current_sec["paragraphs"].append(par_node)
        par_counter += 1
        current_par_lines = []

    for line in lines:
        line_str = line.strip()
        if line_str.startswith("# ") and not current_sec:
            title = line_str.lstrip("# ").strip()
            continue
        if line_str.startswith("## "):
            flush_paragraph()
            sec_heading = line_str.lstrip("# ").strip()
            sec_id = f"SEC-{sec_counter:02d}"
            current_sec = {
                "id": sec_id,
                "heading": sec_heading,
                "paragraphs": [],
                "bone_collections": []
            }
            sections.append(current_sec)
            sec_counter += 1
            par_counter = 1
            continue
            
        if not line_str:
            flush_paragraph()
            continue
            
        if line_str.startswith("---") or line_str.startswith("```") or line_str.startswith("┌") or line_str.startswith("│") or line_str.startswith("└"):
            continue
            
        if current_sec:
            current_par_lines.append(line_str)
            
    flush_paragraph()
    
    ast = {
        "id": "PAPER-002_SEMANTIC_PACKING",
        "title": title,
        "subtitle": subtitle,
        "author": author,
        "file": "PAPER-002_SEMANTIC_PACKING.json",
        "sections": sections,
        "bone_collections": [
            {
                "id": "bone_semantic_packing_core",
                "name": "Semantic Packing & Ideographic DNA Core",
                "description": "Foundational anchors bridging invariant truth with fluid stylistic projection.",
                "bones": [
                    {"id": "PHL-035", "title": "The Invariant Truth & Fluid Projection Law"},
                    {"id": "PHL-034", "title": "Polymorphic DNA Base Schema & Invariant Links"},
                    {"id": "BKM-060", "title": "Federated DNA Taxonomy & Polymorphic Schema Mandate"},
                    {"id": "FEAT-594", "title": "Synthesis Lens Crafter & Automated Paper Grading"},
                    {"id": "FEAT-595", "title": "Resume AST Decomposer & Round-Trip GDoc Formatter"},
                    {"id": "FEAT-596", "title": "DNA Forge 2D Synapse Knowledge Graph Visualizer"}
                ]
            }
        ]
    }
    return ast


def main():
    if not MD_PATH.exists():
        print(f"❌ Markdown file not found: {MD_PATH}")
        return
        
    md_content = MD_PATH.read_text(encoding="utf-8")
    ast = parse_markdown_to_ast(md_content)
    
    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_AST_PATH, "w", encoding="utf-8") as f:
        json.dump(ast, f, indent=2)
    print(f"✅ Compiled Manuscript #2 AST -> {OUTPUT_AST_PATH} ({len(ast['sections'])} sections)")
    
    # Register in dna_manifest.json
    if MANIFEST_PATH.exists():
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)
            
        if "papers" not in manifest or not isinstance(manifest["papers"], list):
            manifest["papers"] = []
            
        # Update or append
        existing_idx = next((i for i, p in enumerate(manifest["papers"]) if p.get("id") == ast["id"]), None)
        paper_entry = {
            "id": ast["id"],
            "title": ast["title"],
            "subtitle": ast["subtitle"],
            "author": ast["author"],
            "file": "PAPER-002_SEMANTIC_PACKING.json"
        }
        if existing_idx is not None:
            manifest["papers"][existing_idx] = paper_entry
        else:
            manifest["papers"].append(paper_entry)
            
        # Also ensure PAPER-RESUME is in papers array
        resume_entry = {
            "id": "PAPER-RESUME",
            "title": "Jason Allred - Technical Resume & CV",
            "subtitle": "Principal Infrastructure Architect & Pre-Silicon Validation",
            "author": "Jason Allred",
            "file": "PAPER-RESUME_v1.json"
        }
        if not any(p.get("id") == "PAPER-RESUME" for p in manifest["papers"]):
            manifest["papers"].insert(0, resume_entry)
            
        with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
        print(f"✅ Registered papers in {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
