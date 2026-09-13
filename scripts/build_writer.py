#!/usr/bin/env python3
# [FEAT-582] Story 78.2: Cross-Collection DNA Citation Engine & Multi-Paper Compiler
# Purpose: Read discrete paper dataset from Portfolio_Dev/papers/, resolve cross-collection
#          DNA citation pointers (PHL, WIS, DISC, FEAT, ArXiv), weave cached word collections
#          with origin quotes as epigraphs, and generate arXiv-ready LaTeX + update writer.html.
# Output:  Portfolio_Dev/docs/whitepaper/main.tex, references.bib, and writer.html hydration.

import json
import os
import re
import sys
import textwrap
from pathlib import Path

# --- Paths ---
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent  # Portfolio_Dev/
LAB_ROOT = REPO_ROOT.parent    # Dev_Lab/
PAPERS_DIR = REPO_ROOT / "papers"
PAPERS_MANIFEST = PAPERS_DIR / "manifest.json"
DNA_MANIFEST = REPO_ROOT / "field_notes" / "data" / "dna_manifest.json"
RESEARCH_MD = LAB_ROOT / "HomeLabAI" / "docs" / "plans" / "RESEARCH_SYNTHESIS.md"
FEATURE_TRACKER_MD = REPO_ROOT / "FeatureTracker.md"
OUTPUT_DIR = REPO_ROOT / "docs" / "whitepaper"
MAIN_TEX = OUTPUT_DIR / "main.tex"
REFERENCES_BIB = OUTPUT_DIR / "references.bib"
WRITER_HTML = REPO_ROOT / "field_notes" / "writer.html"


# --- LaTeX Helpers ---

def latex_escape(text):
    """Escape special LaTeX characters in user-authored text."""
    if not text:
        return ""
    s = str(text)
    replacements = [
        ("\\", "\\textbackslash{}"),
        ("&", "\\&"),
        ("%", "\\%"),
        ("$", "\\$"),
        ("#", "\\#"),
        ("_", "\\_"),
        ("{", "\\{"),
        ("}", "\\}"),
        ("~", "\\textasciitilde{}"),
        ("^", "\\textasciicircum{}"),
    ]
    for old, new in replacements:
        s = s.replace(old, new)
    return s


# --- Loaders & Citation Resolvers ---

def load_papers_manifest():
    """Load papers manifest indexing all active manuscripts."""
    if not PAPERS_MANIFEST.exists():
        return {"papers": []}
    with open(PAPERS_MANIFEST, "r", encoding="utf-8") as f:
        return json.load(f)


def load_active_paper(paper_file_name=None):
    """Load active paper dataset from Portfolio_Dev/papers/."""
    manifest = load_papers_manifest()
    papers = manifest.get("papers", [])
    if not papers:
        raise FileNotFoundError(f"No papers indexed in {PAPERS_MANIFEST}")

    target_file = paper_file_name
    if not target_file:
        target_file = papers[0].get("file")

    paper_path = PAPERS_DIR / target_file
    if not paper_path.exists():
        raise FileNotFoundError(f"Paper file {paper_path} not found")

    with open(paper_path, "r", encoding="utf-8") as f:
        return json.load(f), manifest


def load_dna_manifest():
    """Load master DNA manifest covering all collections."""
    if not DNA_MANIFEST.exists():
        return {}
    with open(DNA_MANIFEST, "r", encoding="utf-8") as f:
        return json.load(f)


def load_arxiv_registry():
    """Parse RESEARCH_SYNTHESIS.md into an ArXiv mapping."""
    arxiv_map = {}
    if not RESEARCH_MD.exists():
        return arxiv_map

    content = RESEARCH_MD.read_text(encoding="utf-8")
    for line in content.splitlines():
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) >= 4 and parts[1].replace(".", "").isdigit():
            anchor_name = parts[0].replace("**", "")
            arxiv_id = parts[1]
            logic = parts[2]
            arxiv_map[arxiv_id] = {
                "name": anchor_name,
                "arxiv": arxiv_id,
                "logic": logic,
                "source": "RESEARCH_SYNTHESIS.md"
            }
            arxiv_map[f"ARXIV:{arxiv_id}"] = arxiv_map[arxiv_id]
            arxiv_map[anchor_name] = arxiv_map[arxiv_id]
    return arxiv_map


def build_citation_index(dna_manifest, arxiv_registry):
    """Build a unified dictionary of all resolvable citations across collections."""
    index = {}

    # 1. Philosophy & Wisdom DNA
    for col in ["philosophy", "wisdom"]:
        for card in dna_manifest.get(col, []):
            cid = card.get("id", "")
            origin = card.get("origin", {}) or {}
            synthesis = card.get("synthesis", {}) or {}
            entry = {
                "id": cid,
                "collection": col,
                "title": synthesis.get("title") or card.get("title", cid),
                "origin_text": origin.get("text") or origin.get("verbatim", ""),
                "origin_source": origin.get("source", "Lab Journal"),
                "narrative": synthesis.get("narrative_context", ""),
                "tags": card.get("metadata", {}).get("tags", []) or synthesis.get("tags", []),
                "author": origin.get("author", "Jason Allred")
            }
            index[cid] = entry
            # Map WIS-xxx to PHL-xxx and vice-versa for backwards compatibility
            if cid.startswith("WIS-"):
                alt = cid.replace("WIS-", "PHL-")
                index[alt] = entry
            elif cid.startswith("PHL-"):
                alt = cid.replace("PHL-", "WIS-")
                index[alt] = entry

    # 2. Discovery / Innovations Timeline
    for disc in dna_manifest.get("discovery", []):
        did = disc.get("id", "")
        origin = disc.get("origin", {}) or {}
        synthesis = disc.get("synthesis", {}) or {}
        index[did] = {
            "id": did,
            "collection": "discovery",
            "title": disc.get("title", did),
            "origin_text": origin.get("text") or synthesis.get("narrative_context", ""),
            "origin_source": origin.get("source", "Innovations Timeline"),
            "narrative": synthesis.get("narrative_context", ""),
            "tags": disc.get("metadata", {}).get("tags", []) or synthesis.get("tags", []),
            "author": "Jason Allred"
        }

    # 3. ArXiv Research Anchors
    for key, item in arxiv_registry.items():
        index[key] = {
            "id": key,
            "collection": "research",
            "title": item["name"],
            "origin_text": item["logic"],
            "origin_source": f"arXiv:{item['arxiv']}",
            "narrative": item["logic"],
            "tags": ["prior-art", "academic"],
            "author": "Academic Literature",
            "arxiv": item["arxiv"]
        }

    return index


# --- LaTeX Generation ---

def build_references_bib(paper, citation_index):
    """Generate a references.bib file dynamically for all citations in the paper."""
    used_keys = set()
    for sec in paper.get("sections", []):
        for par in sec.get("paragraphs", []):
            for cite in par.get("citations", []):
                used_keys.add(cite)

    entries = []
    for key in sorted(used_keys):
        resolved = citation_index.get(key)
        safe_key = re.sub(r'[^a-zA-Z0-9]', '', key)
        if not safe_key:
            continue

        if resolved:
            title = resolved.get("title", key)
            author = resolved.get("author", "Jason Allred")
            arxiv = resolved.get("arxiv", "")
            tags = resolved.get("tags", [])

            lines = [f"@misc{{{safe_key},"]
            lines.append(f"  title = {{{latex_escape(title)}}},")
            lines.append(f"  author = {{{latex_escape(author)}}},")
            if arxiv:
                lines.append(f"  eprint = {{{latex_escape(arxiv)}}},")
                lines.append(f"  archivePrefix = {{arXiv}},")
            lines.append(f"  year = {{2026}},")
            if tags:
                lines.append(f"  keywords = {{{latex_escape(', '.join(tags))}}},")
            lines.append(f"  note = {{Anchor {latex_escape(key)}}}")
            lines.append("}")
            entries.append("\n".join(lines))
        else:
            entries.append(
                f"@misc{{{safe_key},\n"
                f"  title = {{{latex_escape(key)}}},\n"
                f"  author = {{Federated Lab}},\n"
                f"  year = {{2026}}\n"
                f"}}"
            )

    return "\n\n".join(entries) + "\n"


def build_main_tex(paper, citation_index):
    """Generate the complete main.tex document from the active paper dataset."""
    title = paper.get("title", "The JITC Meta-Framework")
    author = paper.get("author", "Jason Allred")
    date = paper.get("date", "2026")

    # Find abstract paragraph if present
    abstract_text = ""
    for sec in paper.get("sections", []):
        if sec.get("type") == "abstract":
            paragraphs = sec.get("paragraphs", [])
            if paragraphs:
                abstract_text = paragraphs[0].get("cached_words", "")
                break

    preamble = textwrap.dedent(r"""\documentclass[11pt]{article}

% arXiv-compatible packages
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage[colorlinks=true,linkcolor=blue,urlcolor=blue,citecolor=blue]{hyperref}
\usepackage{natbib}
\usepackage{geometry}
\geometry{margin=1in}
\usepackage{parskip}

% Custom commands for wisdom card elements
\newcommand{\originquote}[1]{%
  \begin{quote}
  \textit{#1}
  \end{quote}
}
\newcommand{\originmark}{%
  \textsc{Origin}\enspace
}

\title{""" + latex_escape(title) + r"""}
\author{""" + latex_escape(author) + r"""}
\date{""" + latex_escape(date) + r"""}

\begin{document}
\maketitle
""")

    if abstract_text:
        preamble += textwrap.dedent(r"""
\begin{abstract}
""" + latex_escape(abstract_text) + r"""
\end{abstract}

\tableofcontents
\newpage
""")

    sections_tex = []
    for sec in paper.get("sections", []):
        if sec.get("type") == "abstract":
            continue

        heading = sec.get("heading", "Section")
        sec_block = [f"\\section{{{latex_escape(heading)}}}\n"]

        for par in sec.get("paragraphs", []):
            citations = par.get("citations", [])
            cached_words = par.get("cached_words", "").strip()

            # Epigraph for paragraph citations
            for cite in citations:
                resolved = citation_index.get(cite)
                if resolved and resolved.get("origin_text"):
                    quote = resolved["origin_text"]
                    sec_block.append(
                        f"\\noindent\\originmark\n"
                        f"\\originquote{{{latex_escape(quote)}}}\n"
                        f"\\hfill --- \\textit{{{latex_escape(cite)}}}\n\n"
                    )

            # Paragraph prose
            if cached_words:
                cite_commands = []
                for cite in citations:
                    safe_key = re.sub(r'[^a-zA-Z0-9]', '', cite)
                    if safe_key:
                        cite_commands.append(f"\\cite{{{safe_key}}}")
                
                prose = latex_escape(cached_words)
                if cite_commands:
                    prose += f" {' '.join(cite_commands)}"
                sec_block.append(f"{prose}\n\n")

        sections_tex.append("".join(sec_block))

    conclusion = textwrap.dedent(r"""
\bibliographystyle{plainnat}
\bibliography{references}

\end{document}
""")

    return preamble + "\n".join(sections_tex) + conclusion


# --- HTML Hydration ---

def hydrate_writer_html(paper, manifest, citation_index):
    """Hydrate writer.html with active paper dataset, manifest, and quote picker."""
    if not WRITER_HTML.exists():
        print(f"⚠️  {WRITER_HTML} not found — skipping hydration.")
        return

    content = WRITER_HTML.read_text(encoding="utf-8")

    # Build quotes array for picker
    quotes = []
    for key, item in citation_index.items():
        if item.get("origin_text"):
            quotes.append({
                "text": item["origin_text"],
                "source": key,
                "title": item.get("title", key)
            })

    # Strip existing injected context script blocks (preserve main interactive UI script)
    content = re.sub(
        r"<script>\s*// \[(?:FEAT-564|FEAT-581|FEAT-582)\] Workbench context:.*?</script>\n?",
        "",
        content,
        flags=re.DOTALL,
    )

    script_block = (
        "<script>\n"
        "// [FEAT-581/FEAT-582] Workbench context: active paper, manifest, citation index\n"
        f"window.__PAPERS_MANIFEST__ = {json.dumps(manifest, indent=2)};\n"
        f"window.__ACTIVE_PAPER__ = {json.dumps(paper, indent=2)};\n"
        f"window.__CITATION_INDEX__ = {json.dumps(citation_index, indent=2)};\n"
        f"window.__WRITER_QUOTES__ = {json.dumps(quotes, indent=2)};\n"
        "</script>\n"
    )

    content = content.replace("</body>", script_block + "</body>")
    WRITER_HTML.write_text(content, encoding="utf-8")
    print(f"✅ Hydrated {WRITER_HTML} with active paper and {len(quotes)} citation anchor(s).")


# --- Main Orchestration ---

def main():
    paper, manifest = load_active_paper()
    dna = load_dna_manifest()
    arxiv = load_arxiv_registry()
    citation_index = build_citation_index(dna, arxiv)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate LaTeX
    tex_content = build_main_tex(paper, citation_index)
    MAIN_TEX.write_text(tex_content, encoding="utf-8")
    print(f"✅ Generated {MAIN_TEX} ({len(paper.get('sections', []))} sections).")

    # Generate References
    bib_content = build_references_bib(paper, citation_index)
    REFERENCES_BIB.write_text(bib_content, encoding="utf-8")
    print(f"✅ Generated {REFERENCES_BIB}.")

    # Hydrate HTML
    hydrate_writer_html(paper, manifest, citation_index)

    print(f"\n--- Cross-Collection Compiler Summary ---")
    print(f"  Paper:       {paper.get('title')}")
    print(f"  Sections:    {len(paper.get('sections', []))}")
    print(f"  Citations:   {len(citation_index)} indexed")
    print(f"  LaTeX:       {MAIN_TEX}")
    print(f"  Bib:         {REFERENCES_BIB}")


if __name__ == "__main__":
    main()
