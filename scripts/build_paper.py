#!/usr/bin/env python3
"""
[FEAT-560] JITC Whitepaper Synthesis Compiler
Reads ordered Wisdom Cards from wisdom_data.json,
embeds origin quotes as verbatim blockquotes/epigraphs,
weaves synthesis sections, and compiles an arXiv-compliant LaTeX paper.
"""

import json
import os
import sys

DATA_PATH = os.path.expanduser("~/Dev_Lab/Portfolio_Dev/field_notes/data/wisdom_data.json")
OUTPUT_DIR = os.path.expanduser("~/Dev_Lab/Portfolio_Dev/docs/whitepaper")
TEX_FILE = os.path.join(OUTPUT_DIR, "main.tex")
BIB_FILE = os.path.join(OUTPUT_DIR, "references.bib")


def build_paper():
    if not os.path.exists(DATA_PATH):
        print(f"[!] Data file {DATA_PATH} not found.")
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        cards = json.load(f)

    # Sort cards by paper_order
    sorted_cards = sorted(cards, key=lambda x: x.get("paper_order", 999))
    print(f"[*] Weaving {len(sorted_cards)} Wisdom Cards into arXiv LaTeX template...")

    tex_content = r"""\documentclass[10pt,twocolumn,letterpaper]{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,amssymb}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{booktabs}
\usepackage{microtype}
\usepackage{csquotes}

\title{\textbf{The JITC-Loop Meta-Framework: Dual-Channel Memory, Token Golf, and Grounded Feedback in Sovereign Agentic Orchestration}}
\author{
    \textbf{Jason Allred} \\
    Federated Systems Architecture \\
    \texttt{jallred@devlab.local}
}
\date{\today}

\begin{document}

\maketitle

\begin{abstract}
As large language model (LLM) architectures scale toward multi-megatoken context windows, production agentic software engineering encounters the fundamental law of attention dilution: prompt reliability degrades exponentially as input token volume expands. We introduce the \textbf{Just-In-Time Context (JITC)} paradigm, a federated orchestration meta-framework that replaces monolithic prompt injection with high-speed dynamic vector grounding (sub-15ms) across local and cloud silicon topologies. By coupling \textbf{Token Golf} discipline (capping worker subagent payloads strictly below 1,500 tokens) with closed-loop \textbf{Handover Reflection backpressure}, we demonstrate deterministic task execution across sovereign hardware endpoints with zero context thrashing.
\end{abstract}

\section{Introduction \& The Attention Ceiling}
"""

    for card in sorted_cards:
        wid = card.get("id")
        title = card.get("synthesis", {}).get("title", "")
        origin_quote = card.get("origin", {}).get("text", "")
        synth_body = card.get("synthesis", {}).get("narrative_context", "")

        # Clean LaTeX special characters
        clean_quote = origin_quote.replace("&", r"\&").replace("%", r"\%").replace("$", r"\$").replace("_", r"\_")
        clean_body = synth_body.replace("&", r"\&").replace("%", r"\%").replace("$", r"\$").replace("_", r"\_")

        tex_content += f"\n\\subsection{{{title}}}\n"
        tex_content += f"\\begin{{quote}}\n\\small\\textit{{\"{clean_quote}\"}}\n\\hfill--- \\textbf{{Origin Thesis ({wid})}}\n\\end{{quote}}\n\n"
        tex_content += f"{clean_body}\n"

    tex_content += r"""
\section{Conclusion: Words Carry Thought}
By grounding machine synthesis in immutable human origin axioms and serializing agentic tasks through narrow, verifiable interfaces, the JITC-Loop meta-framework unifies stochastic generation with deterministic engineering rigor.

\bibliographystyle{plain}
\bibliography{references}

\end{document}
"""

    with open(TEX_FILE, "w", encoding="utf-8") as f:
        f.write(tex_content)
    print(f"[+] Successfully generated arXiv LaTeX document: {TEX_FILE}")

    # Scaffold BibTeX
    bib_content = r"""@article{allred2026jitc,
  title={The JITC-Loop Meta-Framework: Dual-Channel Memory and Grounded Feedback in Sovereign Agentic Orchestration},
  author={Allred, Jason},
  journal={arXiv preprint arXiv:2609.XXXXX},
  year={2026}
}
"""
    with open(BIB_FILE, "w", encoding="utf-8") as f:
        f.write(bib_content)
    print(f"[+] Successfully scaffolded BibTeX references: {BIB_FILE}")


if __name__ == "__main__":
    build_paper()
