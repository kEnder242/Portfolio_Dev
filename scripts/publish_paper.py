#!/usr/bin/env python3
# [FEAT-616 / VIBE-008] Multi-View Offline Paper Publisher & Drift Heuristic Engine
# Purpose: Compiles paper ASTs into standalone offline HTML with 3 baked-in projected views
#          (Formal Academic, Executive Brief, Story Narrative), paper switching, and cross-view drift evaluation.
# Output:  www_deploy/papers.html (and Portfolio_Dev/field_notes/papers.html) with 0 live API dependencies.

import argparse
import html
import json
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
        for col in ["wisdom", "philosophy", "inspiration", "behavioral", "feature", "discovery", "vibe"]:
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


def build_single_paper_html(paper_id, paper, dna_index):
    """Builds the HTML section for a single paper."""
    title = html.escape(paper.get("title", "Research Manuscript"))
    subtitle = html.escape(paper.get("subtitle", "Sovereign AI Systems Architecture"))
    author = html.escape(paper.get("author", "Jason Allred"))
    date_str = html.escape(paper.get("created_at", "2026-09-25")[:10])

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

    paper_card = f'''
    <section id="paper-card-{paper_id}" class="paper-card-container" data-paper-id="{paper_id}">
        <header class="paper-header">
            <h1 class="paper-main-title">{title}</h1>
            <div class="subtitle">{subtitle}</div>
            <div class="meta-bar">
                <span>✍️ {author}</span>
                <span>📅 {date_str}</span>
                <span class="drift-badge">🛡️ Cross-View Drift: {drift["views"]["formal"]["drift_score"]}%</span>
            </div>
        </header>

        <!-- View Navigation Tabs -->
        <nav class="view-switcher" data-paper-target="{paper_id}">
            <button class="view-tab-btn active" data-view="formal">🔬 Formal Academic View</button>
            <button class="view-tab-btn" data-view="executive">💼 Executive Summary</button>
            <button class="view-tab-btn" data-view="story">📖 Narrative &amp; Origins</button>
        </nav>

        <!-- View 1: Formal Academic -->
        <div id="view-formal-{paper_id}" class="view-content active">
            <article class="formal-view">
                {"".join(formal_sections)}
            </article>
        </div>

        <!-- View 2: Executive Brief -->
        <div id="view-executive-{paper_id}" class="view-content">
            <div class="exec-view">
                {"".join(exec_sections)}
            </div>
        </div>

        <!-- View 3: Story Narrative -->
        <div id="view-story-{paper_id}" class="view-content">
            <div class="story-view">
                {"".join(story_sections)}
            </div>
        </div>
    </section>
    '''

    return paper_card, drift


def generate_multi_paper_html(papers_dict, dna_index):
    """Generates the full standalone multi-paper viewer with paper-selector."""
    paper_options = []
    paper_cards = []
    overall_drift = {}

    first_id = list(papers_dict.keys())[0] if papers_dict else "paper_jitc"

    for pid, pdata in papers_dict.items():
        title = html.escape(pdata.get("title", pid))
        is_selected = "selected" if pid == first_id else ""
        paper_options.append(f'<option value="{pid}" {is_selected}>{title}</option>')
        card_html, drift = build_single_paper_html(pid, pdata, dna_index)
        paper_cards.append(card_html)
        overall_drift[pid] = drift

    html_page = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Published Papers &amp; Projections — Federated Lab</title>
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
            padding: 24px 16px;
        }}
        .container {{
            max-width: 960px;
            margin: 0 auto;
        }}
        .top-nav-bar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 10px 16px;
            margin-bottom: 24px;
            gap: 12px;
            flex-wrap: wrap;
        }}
        .nav-brand {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.85rem;
            font-weight: 700;
            color: var(--accent-color);
            letter-spacing: 0.5px;
        }}
        .nav-brand a {{
            color: var(--text-bright);
            text-decoration: none;
        }}
        .paper-selector-group {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.85rem;
        }}
        .paper-selector-label {{
            color: var(--sub-color);
            font-weight: 600;
        }}
        .paper-select {{
            background: #0d1117;
            border: 1px solid var(--border-color);
            color: var(--text-bright);
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            outline: none;
        }}
        .paper-select:focus {{
            border-color: var(--accent-color);
        }}
        .paper-card-container {{
            display: none;
        }}
        .paper-card-container.active {{
            display: block;
        }}
        .paper-header {{
            text-align: center;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 24px;
        }}
        .paper-main-title {{
            font-size: 2.1rem;
            color: var(--text-bright);
            font-family: var(--font-serif);
            margin-bottom: 8px;
            line-height: 1.25;
        }}
        .subtitle {{
            font-size: 1.05rem;
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
            flex-wrap: wrap;
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
            margin-bottom: 28px;
            background: var(--card-bg);
            padding: 6px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            flex-wrap: wrap;
        }}
        .view-tab-btn {{
            background: transparent;
            border: none;
            color: var(--sub-color);
            font-size: 0.88rem;
            font-weight: 600;
            padding: 8px 16px;
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
            padding: 36px 40px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }}
        .section-title {{
            font-size: 1.35rem;
            color: var(--text-bright);
            margin: 24px 0 12px 0;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 6px;
        }}
        .formal-p {{
            margin-bottom: 16px;
            text-align: justify;
            line-height: 1.8;
        }}
        .cite-pill {{
            font-family: var(--font-mono);
            font-size: 0.72rem;
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
            gap: 20px;
        }}
        .story-chapter {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 24px;
        }}
        .story-title {{
            font-size: 1.25rem;
            color: var(--amber-glow);
            margin-bottom: 14px;
        }}
        .story-par-block {{
            margin-bottom: 16px;
        }}
        .story-p {{
            font-size: 0.98rem;
            line-height: 1.7;
        }}
        .narrative-epigraph {{
            background: rgba(210, 153, 34, 0.08);
            border-left: 3px solid var(--amber-glow);
            padding: 8px 12px;
            border-radius: 4px;
            margin-bottom: 10px;
            font-size: 0.85rem;
            color: var(--sub-color);
        }}
        .epigraph-anchor {{
            font-family: var(--font-mono);
            font-weight: 600;
            color: var(--amber-glow);
        }}
        .epigraph-author {{
            display: block;
            margin-top: 4px;
            font-size: 0.78rem;
            color: var(--sub-color);
        }}
        footer {{
            margin-top: 48px;
            padding-top: 24px;
            border-top: 1px solid var(--border-color);
            text-align: center;
            font-size: 0.8rem;
            color: var(--sub-color);
        }}
    </style>
    <script src="mission-control.js?v=papers" defer></script>
</head>
<body>
    <mission-control></mission-control>
    <div class="container">
        <!-- Top Navigation Bar with Paper Selector -->
        <nav class="top-nav-bar">
            <div class="nav-brand">
                <span>📚 Sovereign Papers Showcase</span>
            </div>
            <div class="paper-selector-group">
                <label for="paper-selector" class="paper-selector-label">Active Document:</label>
                <select id="paper-selector" class="paper-select">
                    {"".join(paper_options)}
                </select>
            </div>
        </nav>

        <!-- Paper Cards Container -->
        <div id="papers-deck">
            {"".join(paper_cards)}
        </div>

        <footer>
            <p>Federated Lab Sovereign Publishing Engine (FEAT-616 • FEAT-589 • BKM-065 • VIBE-008)</p>
            <p>100% Offline Static Bundle • Zero Live Runtime Dependencies</p>
        </footer>
    </div>

    <script>
        (function() {{
            const paperSelect = document.getElementById('paper-selector');
            const paperCards = document.querySelectorAll('.paper-card-container');

            function showPaper(pid) {{
                paperCards.forEach(c => {{
                    if (c.getAttribute('data-paper-id') === pid) {{
                        c.classList.add('active');
                    }} else {{
                        c.classList.remove('active');
                    }}
                }});
            }}

            if (paperSelect) {{
                paperSelect.addEventListener('change', function() {{
                    showPaper(this.value);
                }});
                showPaper(paperSelect.value);
            }}

            // View Tabs Switcher per paper card
            document.querySelectorAll('.view-switcher').forEach(switcher => {{
                const targetPaperId = switcher.getAttribute('data-paper-target');
                const buttons = switcher.querySelectorAll('.view-tab-btn');
                const card = document.getElementById('paper-card-' + targetPaperId);
                if (!card) return;
                const views = card.querySelectorAll('.view-content');

                buttons.forEach(btn => {{
                    btn.addEventListener('click', () => {{
                        const targetView = btn.getAttribute('data-view');
                        buttons.forEach(b => b.classList.remove('active'));
                        views.forEach(v => v.classList.remove('active'));

                        btn.classList.add('active');
                        const targetEl = document.getElementById('view-' + targetView + '-' + targetPaperId);
                        if (targetEl) targetEl.classList.add('active');
                    }});
                }});
            }});
        }})();
    </script>
</body>
</html>
'''
    return html_page, overall_drift


def find_published_papers():
    """Locates all available published paper ASTs."""
    candidates = [
        (REPO_ROOT / "papers" / "paper_jitc_intuition.json", "paper_jitc"),
        (REPO_ROOT / "field_notes" / "data" / "papers" / "PAPER-002_SEMANTIC_PACKING.json", "paper_semantic_packing"),
        (REPO_ROOT / "field_notes" / "data" / "papers" / "PAPER-RESUME_v1.json", "paper_resume_v1"),
        (REPO_ROOT / "field_notes" / "data" / "papers" / "PAPER-RESUME_v2_farah_sharghi_recruiter_v1.json", "paper_resume_v2")
    ]
    papers_dict = {}
    for ppath, pid in candidates:
        if ppath.exists():
            try:
                data = json.loads(ppath.read_text(encoding="utf-8"))
                papers_dict[pid] = data
            except Exception as e:
                print(f"⚠️ Warning loading paper {ppath}: {e}")
    return papers_dict


def main():
    parser = argparse.ArgumentParser(description="Multi-View Offline Paper Publisher (FEAT-616 / FEAT-589)")
    parser.add_argument("--paper", help="Path to single manuscript JSON AST (optional)")
    parser.add_argument("--out", default=str(WWW_DEPLOY), help="Path to output HTML")
    args = parser.parse_args()

    out_path = Path(args.out)
    dna_index = load_dna_index()

    if args.paper:
        paper_path = Path(args.paper)
        if not paper_path.exists():
            print(f"❌ Error: Paper file {paper_path} does not exist.")
            sys.exit(1)
        paper = json.loads(paper_path.read_text(encoding="utf-8"))
        papers_dict = {paper_path.stem: paper}
    else:
        papers_dict = find_published_papers()

    if not papers_dict:
        print("❌ Error: No paper datasets found.")
        sys.exit(1)

    html_content, drift = generate_multi_paper_html(papers_dict, dna_index)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html_content, encoding="utf-8")
    print(f"✅ Published standalone multi-paper viewer: {out_path}")

    # Mirror to field_notes/papers.html
    FIELD_NOTES_PAPERS.parent.mkdir(parents=True, exist_ok=True)
    FIELD_NOTES_PAPERS.write_text(html_content, encoding="utf-8")
    print(f"✅ Mirrored to field notes: {FIELD_NOTES_PAPERS}")

    print("\n--- Cross-View Drift Summary ---")
    for pid, pdrift in drift.items():
        print(f"📄 Paper [{pid}]:")
        for vname, vdata in pdrift.get("views", {}).items():
            print(f"  • View [{vname.capitalize()}]: Coverage {vdata['coverage_pct']}% | Drift {vdata['drift_score']}%")


if __name__ == "__main__":
    main()