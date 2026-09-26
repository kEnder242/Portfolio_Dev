#!/usr/bin/env python3
# [FEAT-616 / VIBE-008] Multi-View Offline Paper Publisher & Drift Heuristic Engine
# Purpose: Compiles paper AST into standalone offline HTML with 3 baked-in projected views
#          (Formal Academic, Executive Brief, Story Narrative) and verifies cross-view semantic drift.
# Output:  www_deploy/papers.html (and Portfolio_Dev/field_notes/papers.html) with 0 live API dependencies.

import argparse
import html
import json
import os
import re
import sys
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent  # Portfolio_Dev/
LAB_ROOT = REPO_ROOT.parent    # Dev_Lab/
WWW_DEPLOY = LAB_ROOT / "www_deploy" / "papers.html"
FIELD_NOTES_PAPERS = REPO_ROOT / "field_notes" / "papers.html"
DNA_MANIFEST = REPO_ROOT / "field_notes" / "data" / "dna_manifest.json"


def load_dna_index():
    """Build citation anchor lookup dictionary."""
    if not DNA_MANIFEST.exists():
        return {}
    try:
        manifest = json.loads(DNA_MANIFEST.read_text(encoding="utf-8"))
        lookup = {}
        for col in ["wisdom", "philosophy", "inspiration", "behavioral", "feature", "discovery"]:
            for item in manifest.get(col, []):
                cid = item.get("id")
                if cid:
                    origin = item.get("origin", {}) or {}
                    synth = item.get("synthesis", {}) or {}
                    lookup[cid] = {
                        "id": cid,
                        "title": item.get("title", cid),
                        "text": origin.get("text") or origin.get("verbatim") or synth.get("narrative_context", ""),
                        "author": origin.get("author", "Federated Lab")
                    }
        return lookup
    except Exception as e:
        print(f"⚠️ Warning loading DNA index: {e}")
        return {}


def calculate_drift(paper, views_content):
    """
    [FEAT-616] Heuristic drift evaluator comparing coverage of core citation anchors
    and AST paragraphs across views.
    """
    all_cites = set(paper.get("citations", []))
    total_pars = 0
    for sec in paper.get("sections", []):
        all_cites.update(sec.get("citations", []))
        for p in sec.get("paragraphs", []):
            all_cites.update(p.get("citations", []))
            total_pars += 1

    drift_report = {
        "total_anchors": len(all_cites),
        "total_paragraphs": total_pars,
        "views": {}
    }

    for vname, vtext in views_content.items():
        found_cites = sum(1 for c in all_cites if c in vtext or c.replace("-", "") in vtext)
        coverage_pct = (found_cites / len(all_cites) * 100.0) if all_cites else 100.0
        drift_report["views"][vname] = {
            "anchors_covered": found_cites,
            "coverage_pct": round(coverage_pct, 1),
            "drift_score": round(100.0 - coverage_pct, 1)
        }

    return drift_report


def generate_html(paper, dna_index):
    """Generate self-contained, standalone offline HTML."""
    title = html.escape(paper.get("title", "Research Manuscript"))
    subtitle = html.escape(paper.get("subtitle", "Sovereign AI Systems Architecture"))
    author = html.escape(paper.get("author", "Jason Allred"))
    date_str = html.escape(paper.get("created_at", "2026-09-25")[:10])

    # 1. Build Views HTML
    # View A: Formal Academic
    formal_sections = []
    for sec in paper.get("sections", []):
        s_heading = html.escape(sec.get("heading", sec.get("id", "Section")))
        pars_html = []
        for p in sec.get("paragraphs", []):
            p_text = html.escape(p.get("text") or p.get("cached_words") or "")
            cites = p.get("citations", [])
            cite_badges = "".join([f'<span class="cite-pill" title="{html.escape(dna_index.get(c, {}).get("text", ""))}">{html.escape(c)}</span>' for c in cites])
            pars_html.append(f'<p class="formal-p">{p_text} {cite_badges}</p>')
        
        formal_sections.append(f'''
        <div class="paper-section">
            <h2 class="section-title">{s_heading}</h2>
            {"".join(pars_html)}
        </div>
        ''')

    # View B: Executive Brief
    exec_sections = []
    for sec in paper.get("sections", []):
        s_heading = html.escape(sec.get("heading", sec.get("id", "Section")))
        bullets = []
        for p in sec.get("paragraphs", []):
            p_text = (p.get("text") or p.get("cached_words") or "").strip()
            if not p_text:
                continue
            first_sent = p_text.split(". ")[0] + ("." if not p_text.split(". ")[0].endswith(".") else "")
            cites = p.get("citations", [])
            cite_badges = "".join([f'<span class="cite-pill">{html.escape(c)}</span>' for c in cites])
            bullets.append(f'<li><strong>{html.escape(first_sent)}</strong> <span class="exec-dim">{html.escape(p_text[len(first_sent):].strip())}</span> {cite_badges}</li>')
        
        exec_sections.append(f'''
        <div class="exec-card">
            <h3 class="exec-heading">⚡ {s_heading}</h3>
            <ul class="exec-list">
                {"".join(bullets)}
            </ul>
        </div>
        ''')

    # View C: Story & Discovery Narrative
    story_sections = []
    for sec in paper.get("sections", []):
        s_heading = html.escape(sec.get("heading", sec.get("id", "Section")))
        story_blocks = []
        for p in sec.get("paragraphs", []):
            p_text = html.escape(p.get("text") or p.get("cached_words") or "")
            cites = p.get("citations", [])
            epigraphs = []
            for c in cites:
                cinfo = dna_index.get(c)
                if cinfo and cinfo.get("text"):
                    epigraphs.append(f'''
                    <div class="narrative-epigraph">
                        <span class="epigraph-anchor">📜 {html.escape(c)}</span>:
                        <em>"{html.escape(cinfo['text'])}"</em>
                        <span class="epigraph-author">--- {html.escape(cinfo.get('author', 'Origin'))}</span>
                    </div>
                    ''')
            
            story_blocks.append(f'''
            <div class="story-par-block">
                {"".join(epigraphs)}
                <p class="story-p">{p_text}</p>
            </div>
            ''')

        story_sections.append(f'''
        <div class="story-chapter">
            <h2 class="story-title">📖 {s_heading}</h2>
            {"".join(story_blocks)}
        </div>
        ''')

    raw_views = {
        "formal": "".join(formal_sections),
        "executive": "".join(exec_sections),
        "story": "".join(story_sections)
    }

    drift = calculate_drift(paper, raw_views)

    html_page = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Multi-View Sovereign Publication</title>
    <style>
        :root {{
            --bg-color: #0d1117;
            --card-bg: #161b22;
            --border-color: #30363d;
            --text-color: #c9d1d9;
            --text-bright: #f0f6fc;
            --sub-color: #8b949e;
            --accent-color: #58a6ff;
            --green-glow: #3fb950;
            --amber-glow: #d29922;
            --font-serif: "Merriweather", "Georgia", "Cambria", serif;
            --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            --font-mono: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background-color: var(--bg-color);
            color: var(--text-color);
            font-family: var(--font-sans);
            line-height: 1.6;
            padding: 32px 16px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        header {{
            text-align: center;
            padding-bottom: 24px;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 24px;
        }}
        h1 {{
            font-size: 2.2rem;
            color: var(--text-bright);
            font-family: var(--font-serif);
            margin-bottom: 8px;
            line-height: 1.25;
        }}
        .subtitle {{
            font-size: 1.1rem;
            color: var(--sub-color);
            margin-bottom: 12px;
            font-style: italic;
        }}
        .meta-bar {{
            display: flex;
            justify-content: center;
            gap: 16px;
            font-size: 0.85rem;
            color: var(--sub-color);
        }}
        .drift-badge {{
            display: inline-flex;
            align-items: center;
            background: rgba(63, 185, 80, 0.15);
            border: 1px solid var(--green-glow);
            color: var(--green-glow);
            padding: 2px 10px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 0.75rem;
        }}
        /* View Switcher Tabs */
        .view-switcher {{
            display: flex;
            justify-content: center;
            gap: 8px;
            margin-bottom: 32px;
            background: var(--card-bg);
            padding: 6px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }}
        .view-tab-btn {{
            background: transparent;
            border: none;
            color: var(--sub-color);
            font-size: 0.9rem;
            font-weight: 600;
            padding: 8px 18px;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        .view-tab-btn.active {{
            background: #21262d;
            color: var(--text-bright);
            box-shadow: 0 1px 3px rgba(0,0,0,0.4);
            border: 1px solid var(--accent-color);
        }}
        /* View Containers */
        .view-content {{
            display: none;
        }}
        .view-content.active {{
            display: block;
        }}
        /* Formal View Styling */
        .formal-view {{
            font-family: var(--font-serif);
            font-size: 1.05rem;
            background: #12161c;
            padding: 40px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }}
        .section-title {{
            font-size: 1.4rem;
            color: var(--text-bright);
            margin: 28px 0 14px 0;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 6px;
        }}
        .formal-p {{
            margin-bottom: 18px;
            text-align: justify;
            line-height: 1.8;
        }}
        .cite-pill {{
            font-family: var(--font-mono);
            font-size: 0.75rem;
            background: rgba(88, 166, 255, 0.12);
            color: var(--accent-color);
            border: 1px solid rgba(88, 166, 255, 0.3);
            padding: 1px 5px;
            border-radius: 4px;
            margin-left: 4px;
            cursor: help;
        }}
        /* Executive View Styling */
        .exec-view {{
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}
        .exec-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
            border-left: 4px solid var(--accent-color);
        }}
        .exec-heading {{
            font-size: 1.15rem;
            color: var(--text-bright);
            margin-bottom: 12px;
        }}
        .exec-list {{
            list-style-type: none;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        .exec-list li {{
            font-size: 0.95rem;
            line-height: 1.5;
        }}
        .exec-dim {{
            color: var(--sub-color);
            font-size: 0.88rem;
        }}
        /* Story Narrative View Styling */
        .story-view {{
            display: flex;
            flex-direction: column;
            gap: 24px;
        }}
        .story-chapter {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 28px;
        }}
        .story-title {{
            font-size: 1.3rem;
            color: var(--amber-glow);
            margin-bottom: 16px;
        }}
        .story-par-block {{
            margin-bottom: 20px;
        }}
        .story-p {{
            font-size: 1rem;
            line-height: 1.7;
        }}
        .narrative-epigraph {{
            background: rgba(210, 153, 34, 0.08);
            border-left: 3px solid var(--amber-glow);
            padding: 8px 12px;
            border-radius: 4px;
            margin-bottom: 10px;
            font-size: 0.85rem;
        }}
        .epigraph-anchor {{
            color: var(--amber-glow);
            font-weight: 700;
            font-family: var(--font-mono);
        }}
        .epigraph-author {{
            display: block;
            text-align: right;
            color: var(--sub-color);
            font-size: 0.75rem;
            margin-top: 4px;
        }}
        footer {{
            margin-top: 48px;
            text-align: center;
            font-size: 0.8rem;
            color: var(--sub-color);
            border-top: 1px solid var(--border-color);
            padding-top: 16px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{title}</h1>
            <div class="subtitle">{subtitle}</div>
            <div class="meta-bar">
                <span>✍️ {author}</span>
                <span>📅 {date_str}</span>
                <span class="drift-badge">🛡️ Cross-View Drift: {drift["views"]["formal"]["drift_score"]}%</span>
            </div>
        </header>

        <!-- View Navigation Tabs -->
        <nav class="view-switcher">
            <button class="view-tab-btn active" data-view="formal">🔬 Formal Academic View</button>
            <button class="view-tab-btn" data-view="executive">💼 Executive Summary</button>
            <button class="view-tab-btn" data-view="story">📖 Narrative &amp; Origins</button>
        </nav>

        <!-- View 1: Formal Academic -->
        <main id="view-formal" class="view-content active">
            <article class="formal-view">
                {"".join(formal_sections)}
            </article>
        </main>

        <!-- View 2: Executive Brief -->
        <main id="view-executive" class="view-content">
            <div class="exec-view">
                {"".join(exec_sections)}
            </div>
        </main>

        <!-- View 3: Story Narrative -->
        <main id="view-story" class="view-content">
            <div class="story-view">
                {"".join(story_sections)}
            </div>
        </main>

        <footer>
            <p>Federated Lab Sovereign Publishing Engine (FEAT-616 • BKM-065 • VIBE-008)</p>
            <p>100% Offline Static Bundle • Zero Live Runtime Dependencies</p>
        </footer>
    </div>

    <script>
        (function() {{
            const buttons = document.querySelectorAll('.view-tab-btn');
            const views = document.querySelectorAll('.view-content');

            buttons.forEach(btn => {{
                btn.addEventListener('click', () => {{
                    const targetView = btn.getAttribute('data-view');
                    
                    buttons.forEach(b => b.classList.remove('active'));
                    views.forEach(v => v.classList.remove('active'));

                    btn.classList.add('active');
                    const targetEl = document.getElementById('view-' + targetView);
                    if (targetEl) targetEl.classList.add('active');
                }});
            }});
        }})();
    </script>
</body>
</html>
'''
    return html_page, drift


def main():
    parser = argparse.ArgumentParser(description="Multi-View Offline Paper Publisher (FEAT-616)")
    parser.add_argument("--paper", default=str(REPO_ROOT / "papers" / "paper_jitc_intuition.json"), help="Path to manuscript JSON AST")
    parser.add_argument("--out", default=str(WWW_DEPLOY), help="Path to output HTML")
    args = parser.parse_args()

    paper_path = Path(args.paper)
    out_path = Path(args.out)

    if not paper_path.exists():
        print(f"❌ Error: Paper file {paper_path} does not exist.")
        sys.exit(1)

    paper = json.loads(paper_path.read_text(encoding="utf-8"))
    dna_index = load_dna_index()

    html_content, drift = generate_html(paper, dna_index)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html_content, encoding="utf-8")
    print(f"✅ Published standalone multi-view paper: {out_path}")

    # Also mirror to field_notes/papers.html
    FIELD_NOTES_PAPERS.parent.mkdir(parents=True, exist_ok=True)
    FIELD_NOTES_PAPERS.write_text(html_content, encoding="utf-8")
    print(f"✅ Mirrored to field notes: {FIELD_NOTES_PAPERS}")

    print("\n--- Cross-View Drift Summary ---")
    for vname, vdata in drift.get("views", {}).items():
        print(f"  • View [{vname.capitalize()}]: Coverage {vdata['coverage_pct']}% | Drift {vdata['drift_score']}%")


if __name__ == "__main__":
    main()
