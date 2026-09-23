#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
[FEAT-588] / [BKM-055] / [Story 82.5]
build_writer.py: Deterministic Offline AST Document Compiler
Compiles paper and resume JSON ASTs directly into pristine LaTeX (.tex),
BibTeX (.bib), and standalone Web HTML without live database connectivity.
"""

import argparse
import json
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PORTFOLIO_DIR = BASE_DIR.parent
PAPERS_DIR = PORTFOLIO_DIR / "papers"
DATA_DIR = BASE_DIR / "data"
DNA_DIR = PORTFOLIO_DIR / "dna"
BUILD_OUTPUT_DIR = PORTFOLIO_DIR / "build" / "papers"


def load_dna_catalog():
    """Loads static DNA databases for offline BibTeX and citation resolution."""
    catalog = {}

    # 1. Philosophy DNA
    phl_path = DNA_DIR / "philosophy_data.json"
    if phl_path.exists():
        try:
            with open(phl_path, "r") as f:
                data = json.load(f)
                for item in data:
                    item_id = item.get("id")
                    title = item.get("synthesis", {}).get("title") or item.get("origin", {}).get("text", "")[:60]
                    author = item.get("origin", {}).get("author", "J. Allred")
                    year = item.get("origin", {}).get("created_at", "2026")[:4]
                    catalog[item_id] = {
                        "id": item_id,
                        "title": title,
                        "author": author,
                        "year": year,
                        "type": "Philosophy DNA",
                        "summary": item.get("synthesis", {}).get("narrative_context", "")
                    }
        except Exception as e:
            print(f"⚠️ Warning reading philosophy_data.json: {e}")

    # 2. Wisdom DNA
    wis_path = DNA_DIR / "wisdom_data.json"
    if wis_path.exists():
        try:
            with open(wis_path, "r") as f:
                data = json.load(f)
                for item in data:
                    item_id = item.get("id")
                    title = item.get("synthesis", {}).get("title") or item.get("origin", {}).get("text", "")[:60]
                    author = item.get("origin", {}).get("author", "J. Allred")
                    year = item.get("origin", {}).get("created_at", "2026")[:4]
                    catalog[item_id] = {
                        "id": item_id,
                        "title": title,
                        "author": author,
                        "year": year,
                        "type": "Wisdom DNA",
                        "summary": item.get("synthesis", {}).get("narrative_context", "")
                    }
        except Exception as e:
            print(f"⚠️ Warning reading wisdom_data.json: {e}")

    return catalog


def compile_paper_to_latex(paper: dict, catalog: dict) -> tuple[str, str]:
    """Compiles a single paper AST into LaTeX source and matching BibTeX entries."""
    title = paper.get("title", "Untitled Manuscript")
    subtitle = paper.get("subtitle", "")
    author = paper.get("author", "Jason Allred")
    created_at = paper.get("created_at", "2026")[:10]

    all_citations = set(paper.get("citations", []))
    for sec in paper.get("sections", []):
        all_citations.update(sec.get("citations", []))
        for p in sec.get("paragraphs", []):
            all_citations.update(p.get("citations", []))

    # Build BibTeX entries
    bib_entries = []
    for cid in sorted(all_citations):
        info = catalog.get(cid, {
            "id": cid,
            "title": f"Artifact Anchor {cid}",
            "author": author,
            "year": "2026",
            "type": "Lab DNA"
        })
        bib_block = f"""@misc{{{cid},
  author = {{{info.get('author')}}},
  title = {{{{{info.get('title')}}}}},
  year = {{{info.get('year')}}},
  note = {{{info.get('type')}: {cid}}}
}}"""
        bib_entries.append(bib_block)

    bib_source = "\n\n".join(bib_entries)

    # Build LaTeX Body
    tex_lines = [
        "\\documentclass[11pt,a4paper]{article}",
        "\\usepackage[utf8]{inputenc}",
        "\\usepackage[margin=1in]{geometry}",
        "\\usepackage{hyperref}",
        "\\usepackage{microtype}",
        "\\usepackage{booktabs}",
        "\\usepackage{cite}",
        "",
        f"\\title{{{title}\\\\ \\large {subtitle}}}",
        f"\\author{{{author}}}",
        f"\\date{{{created_at}}}",
        "",
        "\\begin{document}",
        "\\maketitle",
        ""
    ]

    # Sections & Paragraphs
    for sec in sorted(paper.get("sections", []), key=lambda s: s.get("order", 0)):
        heading = sec.get("heading", "Section")
        tex_lines.append(f"\\section{{{heading}}}")

        # Section bone collection notes
        sec_citations = sec.get("citations", [])
        if sec_citations:
            cites = ", ".join([f"\\cite{{{c}}}" for c in sec_citations])
            tex_lines.append(f"\\noindent \\textbf{{Section Anchors:}} {cites}\\\\")

        for p in sorted(sec.get("paragraphs", []), key=lambda x: x.get("order", 0)):
            text = p.get("curated_text") or p.get("raw_text") or ""
            p_cites = p.get("citations", [])
            cite_str = ""
            if p_cites:
                cite_str = " " + "".join([f"\\cite{{{c}}}" for c in p_cites])

            tex_lines.append(f"{text}{cite_str}")
            tex_lines.append("")

    tex_lines.extend([
        "\\bibliographystyle{plain}",
        "\\bibliography{references}",
        "\\end{document}"
    ])

    tex_source = "\n".join(tex_lines)
    return tex_source, bib_source


def compile_paper_to_html(paper: dict, catalog: dict) -> str:
    """Compiles a paper AST into a responsive, standalone HTML view."""
    title = paper.get("title", "Untitled Manuscript")
    subtitle = paper.get("subtitle", "")
    author = paper.get("author", "Jason Allred")
    created_at = paper.get("created_at", "2026")[:10]

    html_lines = [
        "<!DOCTYPE html>",
        "<html lang=\"en\">",
        "<head>",
        "  <meta charset=\"UTF-8\">",
        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">",
        f"  <title>{title} — Federated Lab</title>",
        "  <link rel=\"stylesheet\" href=\"../field_notes/style.css\">",
        "  <style>",
        "    body { max-width: 860px; margin: 40px auto; padding: 0 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1e293b; }",
        "    header { border-bottom: 2px solid #e2e8f0; padding-bottom: 20px; margin-bottom: 30px; }",
        "    h1 { margin-bottom: 4px; color: #0f172a; }",
        "    .subtitle { color: #64748b; font-size: 1.15rem; margin-bottom: 12px; }",
        "    .meta { font-size: 0.85rem; color: #94a3b8; }",
        "    .cite-chip { display: inline-block; background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; font-size: 0.75rem; padding: 2px 6px; border-radius: 4px; margin: 0 2px; text-decoration: none; font-weight: 600; }",
        "    .section-box { margin-bottom: 40px; }",
        "    .p-box { margin-bottom: 16px; }",
        "  </style>",
        "</head>",
        "<body>",
        "  <header>",
        f"    <h1>{title}</h1>",
        f"    <div class=\"subtitle\">{subtitle}</div>",
        f"    <div class=\"meta\">Author: <strong>{author}</strong> | Date: {created_at} | Status: <span class=\"cite-chip\">{paper.get('status', 'VERBATIM')}</span></div>",
        "  </header>",
        "  <main>"
    ]

    for sec in sorted(paper.get("sections", []), key=lambda s: s.get("order", 0)):
        html_lines.append("    <section class=\"section-box\">")
        html_lines.append(f"      <h2>{sec.get('heading', 'Section')}</h2>")
        for p in sorted(sec.get("paragraphs", []), key=lambda x: x.get("order", 0)):
            text = p.get("curated_text") or p.get("raw_text") or ""
            chips = "".join([f"<span class=\"cite-chip\" title=\"{catalog.get(c, {}).get('title', c)}\">{c}</span>" for c in p.get("citations", [])])
            html_lines.append(f"      <p class=\"p-box\">{text} {chips}</p>")
        html_lines.append("    </section>")

    html_lines.extend([
        "  </main>",
        "</body>",
        "</html>"
    ])

    return "\n".join(html_lines)


def build_all_papers(output_dir: Path = BUILD_OUTPUT_DIR):
    """Discovers all paper JSONs and compiles them into LaTeX, BibTeX, and HTML."""
    output_dir.mkdir(parents=True, exist_ok=True)
    catalog = load_dna_catalog()
    print(f"Loaded DNA catalog: {len(catalog)} anchors available for citation resolution.")

    paper_files = list(PAPERS_DIR.glob("paper_*.json"))
    if not paper_files:
        print(f"No papers found in {PAPERS_DIR}.")
        return

    print(f"Found {len(paper_files)} papers to compile:")
    for pf in paper_files:
        try:
            with open(pf, "r") as f:
                paper = json.load(f)
            slug = pf.stem
            paper_out_dir = output_dir / slug
            paper_out_dir.mkdir(parents=True, exist_ok=True)

            tex_code, bib_code = compile_paper_to_latex(paper, catalog)
            html_code = compile_paper_to_html(paper, catalog)

            (paper_out_dir / "paper.tex").write_text(tex_code, encoding="utf-8")
            (paper_out_dir / "references.bib").write_text(bib_code, encoding="utf-8")
            (paper_out_dir / "index.html").write_text(html_code, encoding="utf-8")

            print(f"  ✅ Compiled '{paper.get('title')}' -> {paper_out_dir.relative_to(PORTFOLIO_DIR)} (tex, bib, html)")
        except Exception as e:
            print(f"  ❌ Error compiling {pf.name}: {e}")

    print(f"\n🎉 All papers compiled successfully to {output_dir.relative_to(PORTFOLIO_DIR)}/!\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deterministic AST Document Compiler")
    parser.add_argument("--compile-all", action="store_true", help="Compile all papers in papers/")
    parser.add_argument("--output-dir", type=Path, default=BUILD_OUTPUT_DIR, help="Output directory")
    args = parser.parse_args()

    build_all_papers(output_dir=args.output_dir)
