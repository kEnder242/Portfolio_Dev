#!/usr/bin/env python3
# [FEAT-564] Story 77.4: Interactive Writer Studio & LaTeX Pipeline
# Purpose: Read ordered wisdom cards from wisdom_data.json, embed origin quotes as
#          epigraphs/blockquotes, weave synthesis explanatory text, and generate
#          arXiv-ready LaTeX files in Portfolio_Dev/docs/whitepaper/.
# Output:  main.tex (complete LaTeX document), references.bib (bibliography)
# Schema:  WIS-001 dual-channel (origin.immutable + synthesis.collaborative)

import json
import os
import re
import textwrap
from pathlib import Path

# --- Paths ---
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent  # Portfolio_Dev/
DATA_PATH = REPO_ROOT / "field_notes" / "data" / "wisdom_data.json"
OUTPUT_DIR = REPO_ROOT / "docs" / "whitepaper"
MAIN_TEX = OUTPUT_DIR / "main.tex"
REFERENCES_BIB = OUTPUT_DIR / "references.bib"
SECTION_ORDER_PATH = REPO_ROOT / "field_notes" / "writer_section_order.json"
WRITER_HTML = REPO_ROOT / "field_notes" / "writer.html"


# --- LaTeX Helpers ---

def latex_escape(text):
    """Escape special LaTeX characters in user-authored text."""
    if not text:
        return ""
    s = str(text)
    # Order matters: backslash first
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


def load_cards(data):
    """Extract cards from wisdom_data.json.

    Supports layouts:
      * Standard list: top-level JSON array of cards (WIS-001..008).
      * Dict with cards: a top-level ``cards`` list.
      * Legacy/single: schema holds origin+synthesis at top level.
    Returns (cards, schema_dict).
    """
    if isinstance(data, list):
        return data, {}

    if isinstance(data, dict):
        schema = data.get("schema", {})
        cards = data.get("cards", [])
        if not cards and "origin" in schema:
            card = {
                "title": schema.get("synthesis", {}).get("title", "Wisdom Card"),
                "origin": schema.get("origin", {}),
                "synthesis": schema.get("synthesis", {}),
            }
            cards = [card]
        return cards, schema

    return [], {}


def load_section_order():
    """Load section ordering from workbench export, if available."""
    if SECTION_ORDER_PATH.exists():
        with open(SECTION_ORDER_PATH, "r") as f:
            return json.load(f).get("sections", [])
    return []


def build_references_bib(cards):
    """Generate a references.bib file from wisdom card metadata.

    Each card becomes a @misc entry; tags become keywords. If the card's
    synthesis contains an 'arxiv' or 'doi' field, those are used.
    """
    entries = []
    for i, card in enumerate(cards):
        synthesis = card.get("synthesis", {}) or {}
        tags = synthesis.get("tags", [])
        title = card.get("title") or synthesis.get("title", f"Wisdom Card {i+1}")
        key = f"wismisc{i+1:03d}"

        # Check for explicit citation fields
        arxiv = synthesis.get("arxiv", "")
        doi = synthesis.get("doi", "")
        url = synthesis.get("url", "")

        lines = [f"@misc{{{key},"]
        lines.append(f"  title = {{{latex_escape(title)}}},")
        lines.append(f"  author = {{Jason Allred}},")

        if arxiv:
            lines.append(f"  eprint = {{{latex_escape(arxiv)}}},")
            lines.append(f"  archivePrefix = {{arXiv}},")
        elif doi:
            lines.append(f"  doi = {{{latex_escape(doi)}}},")
        elif url:
            lines.append(f"  url = {{{latex_escape(url)}}},")

        lines.append(f"  year = {{2026}},")
        if tags:
            kw = ", ".join(tags)
            lines.append(f"  keywords = {{{latex_escape(kw)}}},")
        lines.append(f"  note = {{Wisdom Card WIS-{i+1:03d}}}")
        lines.append("}")
        entries.append("\n".join(lines))

    return "\n\n".join(entries) + "\n"


def build_main_tex(cards, schema, section_order=None):
    """Generate the complete main.tex document body from wisdom cards."""
    paper_title = "The JITC Meta-Framework: Engineering Philosophy from 18 Years of Technical Logs"
    author = "Jason Allred"
    abstract = (
        "This paper presents the JITC (Just-In-Time Context) Meta-Framework, "
        "an architectural approach to encoding engineering wisdom from long-horizon "
        "technical practice into reproducible agent workflows. Drawing on 18 years "
        "of raw engineering logs, we formalize a dual-channel architecture separating "
        "immutable human origin from collaborative machine synthesis, and demonstrate "
        "automated pipeline generation from structured wisdom cards to arXiv-formatted "
        "LaTeX documents."
    )

    # Build preamble
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

% Title
\title{""" + latex_escape(paper_title) + r"""}
\author{""" + latex_escape(author) + r"""}
\date{2026}

\begin{document}
\maketitle

% Abstract
\begin{abstract}
""" + latex_escape(abstract) + r"""
\end{abstract}

\tableofcontents
\newpage
""")

    # Build sections
    sections = []

    # Introduction section (always first, not from a card)
    sections.append(textwrap.dedent(r"""\section{Introduction}

Engineering practice accumulates wisdom through repeated encounters with failure, recovery, and adaptation. The challenge is not collecting lessons learned but encoding them into formats that survive organizational turnover and toolchain evolution.

The JITC Meta-Framework addresses this by treating engineering wisdom as structured data with explicitly separated provenance layers. Each wisdom card pairs an \emph{immutable origin} (verbatim human voice) with a \emph{collaborative synthesis} (machine-generated context, analysis, and connections).

This dual-channel architecture preserves the provenance of every claim while enabling rapid iteration on technical papers through automated LaTeX generation.
"""))

    # Wisdom card sections
    for i, card in enumerate(cards):
        origin = card.get("origin", {}) or {}
        synthesis = card.get("synthesis", {}) or {}
        title = card.get("title") or synthesis.get("title", f"Wisdom Card {i+1}")
        verbatim = origin.get("verbatim", "")
        narrative = synthesis.get("narrative_context", "")
        takeaways = synthesis.get("takeaways", [])
        tags = synthesis.get("tags", [])
        card_id = card.get("id", f"WIS-{i+1:03d}")

        sec_num = i + 2  # +1 for intro, +1 for 1-based
        sec = f"\\section{{{latex_escape(title)}}}\n"

        # Origin quote as epigraph
        if verbatim:
            sec += (
                f"\\noindent\\originmark\n"
                f"\\originquote{{{latex_escape(verbatim)}}}\n"
                f"\\hfill --- \\textit{{{latex_escape(card_id)}}}\n\n"
            )

        # Synthesis narrative
        if narrative:
            sec += f"{latex_escape(narrative)}\n\n"

        # Takeaways
        if takeaways:
            sec += "\\subsection{Key Takeaways}\n"
            sec += "\\begin{itemize}\n"
            for t in takeaways:
                sec += f"  \\item {latex_escape(t)}\n"
            sec += "\\end{itemize}\n\n"

        # Tags
        if tags:
            tag_str = ", ".join(tags)
            sec += f"\\noindent\\textbf{{Keywords:}} {latex_escape(tag_str)}\n\n"

        sections.append(sec)

    # Conclusion
    sections.append(textwrap.dedent(r"""\section{Conclusion}

The dual-channel architecture --- immutable human origin alongside collaborative machine synthesis --- provides a durable foundation for encoding engineering wisdom. By automating the pipeline from structured wisdom cards to publication-ready LaTeX, the JITC Meta-Framework enables rapid iteration on technical papers while preserving the provenance of every claim.

Future work includes integrating local silicon refinement engines for synthesis enhancement, automated literature connection discovery via semantic graph traversal, and multi-paper generation from wisdom card subsets filtered by tag clusters.

\bibliographystyle{plainnat}
\bibliography{references}

\end{document}
"""))

    return preamble + "\n".join(sections)


def update_writer_html_quotes(cards):
    """Update the embedded __WRITER_QUOTES__ array in writer.html with all card origins."""
    if not WRITER_HTML.exists():
        print(f"⚠️  {WRITER_HTML} not found — skipping quote injection.")
        return

    quotes = []
    for i, card in enumerate(cards):
        origin = card.get("origin", {}) or {}
        verbatim = origin.get("text", "") or origin.get("verbatim", "")
        if verbatim:
            quotes.append({
                "text": verbatim,
                "source": card.get("id", f"WIS-{i+1:03d}")
            })

    quotes_js = json.dumps(quotes, indent=2)
    script_block = (
        "<script>\n"
        "// [FEAT-564] Workbench context: origin quotes available for slotting.\n"
        f"window.__WRITER_QUOTES__ = {quotes_js};\n"
        "</script>\n"
    )

    content = WRITER_HTML.read_text(encoding="utf-8")

    # Strip any existing quote block
    content = re.sub(
        r"<script>\s*// \[(?:FEAT-560|FEAT-564)\] Workbench context:.*?</script>\n?",
        "",
        content,
        flags=re.DOTALL,
    )

    # Insert before </body>
    content = content.replace("</body>", script_block + "</body>")

    WRITER_HTML.write_text(content, encoding="utf-8")
    print(f"✅ Updated writer.html with {len(quotes)} origin quote(s) for workbench picker.")


def main():
    if not DATA_PATH.exists():
        print(f"Error: {DATA_PATH} not found. No LaTeX files generated.")
        return

    with open(DATA_PATH, "r") as f:
        data = json.load(f)

    cards, schema = load_cards(data)
    section_order = load_section_order()

    # Apply section ordering if workbench export exists
    if section_order:
        card_order_map = {}
        for card in cards:
            cid = card.get("id", "")
            card_order_map[cid] = card
        ordered = []
        for item in section_order:
            cid = item.get("cardId")
            if cid and cid in card_order_map:
                ordered.append(card_order_map[cid])
        if ordered:
            cards = ordered
            print(f"📋 Applied section order from {SECTION_ORDER_PATH.name}: {len(cards)} cards.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate main.tex
    tex_content = build_main_tex(cards, schema, section_order)
    MAIN_TEX.write_text(tex_content, encoding="utf-8")
    print(f"✅ Generated {MAIN_TEX} ({len(cards)} wisdom card section(s)).")

    # Generate references.bib
    bib_content = build_references_bib(cards)
    REFERENCES_BIB.write_text(bib_content, encoding="utf-8")
    print(f"✅ Generated {REFERENCES_BIB} ({len(cards)} reference(s)).")

    # Update writer.html with origin quotes
    update_writer_html_quotes(cards)

    # Summary
    total_takeaways = sum(
        len((c.get("synthesis") or {}).get("takeaways", []))
        for c in cards
    )
    total_tags = set()
    for c in cards:
        total_tags.update((c.get("synthesis") or {}).get("tags", []))

    print(f"\n--- Pipeline Summary ---")
    print(f"  Cards processed: {len(cards)}")
    print(f"  Total takeaways: {total_takeaways}")
    print(f"  Unique tags:     {len(total_tags)}")
    print(f"  Output:          {MAIN_TEX}")
    print(f"                   {REFERENCES_BIB}")
    print(f"\nTo compile PDF: cd {OUTPUT_DIR} && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex")


if __name__ == "__main__":
    main()
