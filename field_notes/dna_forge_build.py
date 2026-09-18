#!/usr/bin/env python3
"""
dna_forge_build.py [v1.0]
[FEAT-582 / Story 83.10] The DNA Forge: Unified Multi-Domain Knowledge Foundry
Generates dna_forge.html consolidating Philosophy (PHL), Wisdom (WIS), and Reverse DNA (RDNA)
with interactive domain switching, card cohesiveness metrics, and human-in-the-loop polish queues.
"""

import json
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PHILOSOPHY_PATH = BASE_DIR / "data" / "philosophy_data.json"
WISDOM_PATH = BASE_DIR / "data" / "wisdom_data.json"
RDNA_PATH = BASE_DIR / "data" / "rdna_questions.json"
OUTPUT_HTML = BASE_DIR / "dna_forge.html"


def escape_html(text):
    return (
        str(text if text is not None else "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def load_json(path):
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Could not load {path.name}: {e}")
    return []


def render_card(card, domain_type):
    card_id = escape_html(card.get("id", "DNA-000"))
    synthesis = card.get("synthesis", {})
    title = escape_html(synthesis.get("title", card.get("title", "Untitled Axiom")))
    narrative = escape_html(synthesis.get("narrative_context", card.get("summary", "")))
    origin = card.get("origin", {})
    origin_text = escape_html(origin.get("text", ""))
    origin_source = escape_html(origin.get("source", "Federated Lab Knowledge"))
    
    metadata = card.get("metadata", {})
    tags = metadata.get("tags", [])
    anchors = synthesis.get("lab_anchors", metadata.get("explicit_links", []))
    status = metadata.get("status", "APPROVED")
    
    tag_html = "".join(f'<span class="dna-tag">{escape_html(t)}</span>' for t in tags)
    anchor_html = " ".join(f'<code>{escape_html(a)}</code>' for a in anchors)
    
    needs_polish = len(narrative) < 50 or "placeholder" in narrative.lower() or status == "NEEDS_REVIEW"
    badge_html = '<span class="badge polish">Needs Polish</span>' if needs_polish else '<span class="badge approved">Verified</span>'

    return f"""
    <div class="dna-card" data-domain="{domain_type}" data-id="{card_id}">
        <div class="card-header">
            <div class="card-id-row">
                <span class="dna-id-chip {domain_type.lower()}">{card_id}</span>
                {badge_html}
            </div>
            <h3 class="card-title">{title}</h3>
        </div>
        <div class="card-body">
            <div class="origin-quote">
                <span class="section-label">Origin Record</span>
                <p>"{origin_text}"</p>
                <div class="origin-source">— {origin_source}</div>
            </div>
            <div class="synthesis-block">
                <span class="section-label">Distilled Axiom / Lesson</span>
                <p>{narrative}</p>
            </div>
            {f'<div class="anchors-block"><span class="section-label">Lab Anchors</span><div class="anchors">{anchor_html}</div></div>' if anchor_html else ''}
        </div>
        <div class="card-footer">
            <div class="tags-row">{tag_html}</div>
        </div>
    </div>
    """


def render_rdna_item(item):
    q_id = escape_html(item.get("id", "RDNA-000"))
    question = escape_html(item.get("question", ""))
    target_id = escape_html(item.get("target_dna_id", ""))
    target_title = escape_html(item.get("target_dna_title", ""))
    domain = escape_html(item.get("target_collection", "philosophy_dna"))
    tags = item.get("tags", [])
    
    tag_html = "".join(f'<span class="dna-tag">{escape_html(t)}</span>' for t in tags)

    return f"""
    <div class="dna-card rdna-card" data-domain="RDNA" data-id="{q_id}">
        <div class="card-header">
            <div class="card-id-row">
                <span class="dna-id-chip rdna">{q_id}</span>
                <span class="badge hyde-bypass">HyDE Bypass Candidate</span>
            </div>
            <h3 class="card-title">"{question}"</h3>
        </div>
        <div class="card-body">
            <div class="rdna-target-box">
                <span class="section-label">Target DNA Anchor</span>
                <div class="target-link">
                    <span class="target-id">{target_id}</span>: <strong class="target-title">{target_title}</strong>
                </div>
                <div class="target-collection">Collection: <code>{domain}</code></div>
            </div>
        </div>
        <div class="card-footer">
            <div class="tags-row">{tag_html}</div>
        </div>
    </div>
    """


def build_dna_forge_html():
    phl_cards = load_json(PHILOSOPHY_PATH)
    wis_cards = load_json(WISDOM_PATH)
    rdna_items = load_json(RDNA_PATH)
    
    phl_html = "".join(render_card(c, "PHL") for c in phl_cards)
    wis_html = "".join(render_card(c, "WIS") for c in wis_cards)
    rdna_html = "".join(render_rdna_item(i) for i in rdna_items)
    
    total_entries = len(phl_cards) + len(wis_cards) + len(rdna_items)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DNA Forge | Federated Lab Knowledge Foundry</title>
    <link rel="stylesheet" href="style.css?v=312b4371">
    <style>
        .forge-hero {{
            padding: 2rem 1.5rem 1rem;
            background: linear-gradient(180deg, rgba(20, 20, 28, 0.8) 0%, rgba(10, 10, 15, 0.4) 100%);
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 1.5rem;
        }}
        .forge-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }}
        .forge-title {{
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--text-color);
            margin: 0;
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }}
        .forge-subtitle {{
            color: var(--text-muted);
            font-size: 0.95rem;
            margin-top: 0.4rem;
        }}
        .forge-stats {{
            display: flex;
            gap: 1rem;
        }}
        .stat-chip {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            font-size: 0.85rem;
            display: flex;
            gap: 0.4rem;
            align-items: center;
        }}
        .stat-num {{
            font-weight: 700;
            color: var(--accent-color);
        }}
        .forge-tabs {{
            display: flex;
            gap: 0.5rem;
            margin-top: 1.5rem;
            border-bottom: 2px solid var(--border-color);
        }}
        .tab-btn {{
            background: none;
            border: none;
            padding: 0.7rem 1.2rem;
            color: var(--text-muted);
            font-weight: 600;
            font-size: 0.95rem;
            cursor: pointer;
            border-bottom: 2px solid transparent;
            margin-bottom: -2px;
            transition: all 0.2s ease;
        }}
        .tab-btn:hover {{
            color: var(--text-color);
        }}
        .tab-btn.active {{
            color: var(--accent-color);
            border-bottom-color: var(--accent-color);
        }}
        .forge-controls {{
            display: flex;
            gap: 1rem;
            margin-bottom: 1.5rem;
            align-items: center;
            flex-wrap: wrap;
        }}
        .forge-search {{
            flex: 1;
            min-width: 260px;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            padding: 0.6rem 1rem;
            border-radius: 6px;
            color: var(--text-color);
            font-size: 0.9rem;
        }}
        .card-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 1.2rem;
        }}
        .dna-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.2rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
            transition: transform 0.15s ease, border-color 0.15s ease;
        }}
        .dna-card:hover {{
            border-color: var(--accent-color);
            transform: translateY(-2px);
        }}
        .card-id-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.4rem;
        }}
        .dna-id-chip {{
            font-family: monospace;
            font-size: 0.75rem;
            font-weight: 700;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.12);
        }}
        .dna-id-chip.phl {{ color: #7aa2f7; border-color: #7aa2f744; }}
        .dna-id-chip.wis {{ color: #e0af68; border-color: #e0af6844; }}
        .dna-id-chip.rdna {{ color: #bb9af7; border-color: #bb9af744; }}
        .badge {{
            font-size: 0.7rem;
            font-weight: 600;
            padding: 0.15rem 0.4rem;
            border-radius: 4px;
        }}
        .badge.approved {{ background: rgba(74, 222, 128, 0.15); color: #4ade80; }}
        .badge.polish {{ background: rgba(248, 113, 113, 0.15); color: #f87171; }}
        .badge.hyde-bypass {{ background: rgba(187, 154, 247, 0.15); color: #bb9af7; }}
        .card-title {{
            font-size: 1.05rem;
            font-weight: 600;
            margin: 0;
            line-height: 1.4;
        }}
        .origin-quote {{
            background: rgba(0, 0, 0, 0.25);
            border-left: 3px solid rgba(255, 255, 255, 0.2);
            padding: 0.6rem 0.8rem;
            border-radius: 0 4px 4px 0;
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-bottom: 0.8rem;
        }}
        .origin-quote p {{ margin: 0 0 0.4rem; font-style: italic; }}
        .origin-source {{ font-size: 0.75rem; text-align: right; color: rgba(255, 255, 255, 0.4); }}
        .synthesis-block p {{
            margin: 0.3rem 0 0;
            font-size: 0.9rem;
            line-height: 1.5;
            color: var(--text-color);
        }}
        .section-label {{
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            font-weight: 700;
            display: block;
        }}
        .anchors {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.3rem;
            margin-top: 0.3rem;
        }}
        .anchors code {{
            font-size: 0.75rem;
            background: rgba(255, 255, 255, 0.06);
            padding: 0.15rem 0.4rem;
            border-radius: 3px;
        }}
        .tags-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.3rem;
        }}
        .dna-tag {{
            font-size: 0.72rem;
            color: var(--text-muted);
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 0.15rem 0.45rem;
            border-radius: 12px;
        }}
        .rdna-target-box {{
            background: rgba(187, 154, 247, 0.06);
            border: 1px solid rgba(187, 154, 247, 0.2);
            padding: 0.8rem;
            border-radius: 6px;
        }}
        .target-id {{
            font-family: monospace;
            font-weight: 700;
            color: #bb9af7;
        }}
        .target-collection {{
            margin-top: 0.4rem;
            font-size: 0.75rem;
            color: var(--text-muted);
        }}
        .tab-panel {{ display: none; }}
        .tab-panel.active {{ display: grid; }}
    </style>
</head>
<body>
    <button id="menu-toggle">☰ MENU</button>

    <nav id="sidebar">
        <mission-control></mission-control>
    </nav>

    <main>
        <div class="forge-hero">
            <div class="forge-header">
                <div>
                    <h1 class="forge-title">⚡ DNA Forge Studio</h1>
                    <div class="forge-subtitle">The Living Knowledge Foundry — Philosophy, Empirical Wisdom & Reverse DNA</div>
                </div>
                <div class="forge-stats">
                    <div class="stat-chip">Philosophy (PHL): <span class="stat-num">{len(phl_cards)}</span></div>
                    <div class="stat-chip">Wisdom (WIS): <span class="stat-num">{len(wis_cards)}</span></div>
                    <div class="stat-chip">Reverse DNA: <span class="stat-num">{len(rdna_items)}</span></div>
                </div>
            </div>

            <div class="forge-tabs">
                <button class="tab-btn active" data-tab="phl-panel">🏛️ Philosophy ({len(phl_cards)})</button>
                <button class="tab-btn" data-tab="wis-panel">📜 Wisdom & War Stories ({len(wis_cards)})</button>
                <button class="tab-btn" data-tab="rdna-panel">❓ Reverse DNA Bank ({len(rdna_items)})</button>
            </div>
        </div>

        <div class="content-container">
            <div class="forge-controls">
                <input type="text" id="dna-search" class="forge-search" placeholder="Search across DNA cards, tags, anchors, and concepts...">
            </div>

            <div id="phl-panel" class="tab-panel card-grid active">
                {phl_html}
            </div>

            <div id="wis-panel" class="tab-panel card-grid">
                {wis_html}
            </div>

            <div id="rdna-panel" class="tab-panel card-grid">
                {rdna_html}
            </div>
        </div>
    </main>

    <script src="script.js?v=acd57779"></script>
    <script src="mission-control.js?v=888b46e6"></script>
    <script>
        // Tab switching logic
        document.querySelectorAll('.tab-btn').forEach(btn => {{
            btn.addEventListener('click', () => {{
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
                btn.classList.add('active');
                const target = document.getElementById(btn.dataset.tab);
                if (target) target.classList.add('active');
            }});
        }});

        // Live search filter
        const searchInput = document.getElementById('dna-search');
        if (searchInput) {{
            searchInput.addEventListener('input', (e) => {{
                const q = e.target.value.toLowerCase();
                document.querySelectorAll('.dna-card').forEach(card => {{
                    const text = card.textContent.toLowerCase();
                    card.style.display = text.includes(q) ? '' : 'none';
                }});
            }});
        }}
    </script>
</body>
</html>
"""
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ Successfully compiled {OUTPUT_HTML} with {total_entries} total DNA entries.")


if __name__ == "__main__":
    build_dna_forge_html()
