#!/usr/bin/env python3
# wisdom_build.py [v3.0]
# [FEAT-559] Story 76.2 / Story 77.1: Multi-DNA Wisdom Studio & REST Save Pipeline
# Purpose: Generate wisdom.html from data/wisdom_data.json and data/dna_manifest.json
#          featuring public reader view, in-place interactive workbench mode (?edit=1),
#          DNA collection switcher (RW vs RO), and direct REST disk save via Foyer (:8765).
# Schema: Wisdom cards pair an immutable origin (verbatim) with live synthesis. See WIS-001.

import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "wisdom_data.json"
PHILOSOPHY_PATH = BASE_DIR / "data" / "philosophy_data.json"
MANIFEST_PATH = BASE_DIR / "data" / "dna_manifest.json"
OUTPUT_HTML = BASE_DIR / "wisdom.html"
REL_SOURCE = "Portfolio_Dev/field_notes/data/wisdom_data.json"


def escape_html(text):
    """Minimal HTML escaping for user-authored card content."""
    return (
        str(text if text is not None else "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def load_cards(data):
    """Extract cards from wisdom_data.json."""
    if isinstance(data, list):
        return data, {}
    if isinstance(data, dict):
        schema = data.get("schema", {})
        cards = data.get("cards", [])
        if not cards and "origin" in schema:
            cards = [{
                "title": schema.get("synthesis", {}).get("title", "Wisdom Card"),
                "origin": schema.get("origin", {}),
                "synthesis": schema.get("synthesis", {}),
            }]
        return cards, schema
    return [], {}


def render_takeaways(takeaways):
    if not takeaways:
        return ""
    items = "".join(f"<li>{escape_html(t)}</li>" for t in takeaways)
    return f'<div class="card-section"><span class="section-label">Takeaways</span><ul class="takeaways wb-editable" data-field="takeaways" contenteditable="false">{items}</ul></div>'


def render_anchors(anchors):
    if not anchors:
        return ""
    items = " ".join(f"<code>{escape_html(a)}</code>" for a in anchors)
    return f'<div class="card-section"><span class="section-label">Lab Anchors</span><div class="card-anchors">{items}</div></div>'


def render_tags(tags):
    if not tags:
        return '<span class="wb-editable" data-field="tags" contenteditable="false" style="color:#666;">(no tags)</span>'
    inner = "".join(f'<span class="tag">{escape_html(t)}</span>' for t in tags)
    return f'<div class="wb-editable" data-field="tags" contenteditable="false">{inner}</div>'


def render_card(card, index):
    cid = card.get("id") or f"WIS-{index:03d}"
    theme = card.get("theme") or "Wisdom"
    meta = card.get("metadata", {}) or {}
    bucket_id = meta.get("bucket_id") or card.get("bucket_id", "")
    
    origin = card.get("origin", {}) or {}
    synthesis = card.get("synthesis", {}) or {}
    verbatim = origin.get("text", "") or origin.get("verbatim", "") or card.get("verbatim", "")
    title = card.get("title") or synthesis.get("title") or f"Wisdom Card {index}"
    narrative = synthesis.get("narrative_context", "")
    review_notes = synthesis.get("review_notes", "")
    anchors = synthesis.get("lab_anchors", [])
    takeaways = synthesis.get("takeaways", [])
    tags = meta.get("tags", []) or synthesis.get("tags", [])

    origin_html = (
        f'<div class="origin-quote wb-locked" data-field="origin" contenteditable="false">{escape_html(verbatim)}</div>'
        if verbatim
        else '<div class="origin-quote wb-locked" data-field="origin" contenteditable="false">(no origin recorded)</div>'
    )

    review_notes_html = ""
    if review_notes:
        review_notes_html = f'<div class="card-section"><span class="section-label">Review Notes</span><div class="review-notes wb-editable" data-field="review_notes" contenteditable="false">{escape_html(review_notes)}</div></div>'

    bucket_badge_html = f'<span class="bucket-badge">{escape_html(bucket_id)}</span>' if bucket_id else ""

    html = f"""
        <div class="wisdom-card" data-card-id="{escape_html(cid)}" data-card-index="{index}">
            <div class="card-meta-row">
                <span><strong>{escape_html(cid)}</strong> &bull; {escape_html(theme)}</span>
                {bucket_badge_html}
            </div>
            <div class="card-title wb-editable" data-field="title" contenteditable="false">{escape_html(title)}</div>
            <div class="card-section">
                <span class="section-label">Origin <span class="immutable-flag">[IMMUTABLE]</span></span>
                {origin_html}
            </div>
            <div class="card-section">
                <span class="section-label">Narrative Context</span>
                <div class="wb-editable" data-field="narrative_context" contenteditable="false">{escape_html(narrative) if narrative else '<span style="color:#666;">(add narrative context)</span>'}</div>
            </div>
            {review_notes_html}
            {render_takeaways(takeaways)}
            {render_anchors(anchors)}
            <div class="card-section tag-row">
                <span class="section-label">Tags</span>
                <div>{render_tags(tags)}</div>
            </div>
        </div>"""
    return html


def render_cards(cards):
    return "\n".join(render_card(card, i + 1) for i, card in enumerate(cards))


def ensure_symlink():
    """Backward-compatible symlink philosophy.html -> wisdom.html."""
    philosophy = BASE_DIR / "philosophy.html"
    if philosophy.is_symlink():
        return True
    if philosophy.exists():
        philosophy.unlink()
    try:
        philosophy.symlink_to("wisdom.html")
        return True
    except OSError as e:
        print(f"⚠️  Could not create philosophy.html symlink: {e}")
        return False


def build_page():
    if not DATA_PATH.exists():
        print(f"Error: {DATA_PATH} not found.")
        return

    with open(DATA_PATH, "r") as f:
        wisdom_cards = json.load(f)

    cards, schema = load_cards(wisdom_cards)
    cards_html = render_cards(cards)

    manifest = {}
    if MANIFEST_PATH.exists():
        with open(MANIFEST_PATH, "r") as f:
            manifest = json.load(f)

    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wisdom Studio | Jason Allred</title>
    <link rel="stylesheet" href="style.css?v=826dbad3">
    <style>
        /* Wisdom Studio: Multi-DNA & Dual-View (Reader + Workbench) */
        .wisdom-header {{
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            gap: 20px;
            flex-wrap: wrap;
            margin-bottom: 8px;
        }}
        .section-title {{ margin-bottom: 4px; }}
        .view-toggle {{
            font-family: var(--font-stack);
            font-size: 0.7rem;
            color: var(--accent-color);
            background: transparent;
            border: 1px solid var(--border-color);
            padding: 4px 10px;
            border-radius: 4px;
            cursor: pointer;
            transition: background 0.2s, border-color 0.2s;
        }}
        .view-toggle:hover {{ border-color: var(--accent-color); background: var(--code-bg); }}
        .view-toggle.active {{ border-color: var(--accent-color); color: #fff; background: var(--code-bg); }}

        /* DNA Selector Bar */
        .dna-selector-bar {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin: 12px 0 16px 0;
            padding: 8px 12px;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 4px;
            font-family: var(--font-stack);
            font-size: 0.8rem;
        }}
        .dna-select {{
            background: var(--code-bg);
            border: 1px solid var(--border-color);
            color: var(--text-color);
            padding: 4px 10px;
            border-radius: 4px;
            font-family: var(--font-stack);
            font-size: 0.8rem;
            cursor: pointer;
        }}
        .dna-badge {{
            font-size: 0.65rem;
            padding: 2px 8px;
            border-radius: 3px;
            font-weight: bold;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }}
        .dna-badge.rw {{
            background: rgba(35, 134, 54, 0.2);
            border: 1px solid #238636;
            color: #3fb950;
        }}
        .dna-badge.ro {{
            background: rgba(210, 153, 34, 0.2);
            border: 1px solid #d29922;
            color: #d29922;
        }}

        .wisdom-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 16px;
            margin-top: 16px;
        }}
        .wisdom-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-left: 4px solid var(--accent-color);
            padding: 16px 18px;
            font-family: var(--font-stack);
            font-size: 0.85rem;
            line-height: 1.5;
            border-radius: 4px;
        }}
        .wisdom-card .card-meta-row {{
            display: flex;
            justify-content: space-between;
            font-size: 0.7rem;
            color: var(--sub-color);
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .wisdom-card .bucket-badge {{
            color: var(--accent-color);
            font-weight: bold;
        }}
        .wisdom-card .card-title {{
            font-weight: bold;
            color: var(--heading-color);
            font-size: 0.95rem;
            margin-bottom: 8px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 6px;
        }}
        .wisdom-card .card-section {{
            margin-bottom: 10px;
        }}
        .wisdom-card .section-label {{
            display: inline-block;
            font-weight: bold;
            color: var(--accent-color);
            text-transform: uppercase;
            font-size: 0.7rem;
            letter-spacing: 1px;
            margin-bottom: 4px;
        }}
        .wisdom-card .immutable-flag {{
            color: #d29922;
            font-size: 0.65rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-left: 6px;
        }}
        .wisdom-card .origin-quote {{
            border-left: 2px solid var(--accent-dim);
            padding-left: 10px;
            color: var(--sub-color);
            font-style: italic;
            font-size: 0.8rem;
            white-space: pre-wrap;
        }}
        .wisdom-card .review-notes {{
            font-size: 0.75rem;
            color: #8b949e;
            background: var(--code-bg);
            border-left: 2px solid var(--border-color);
            padding: 4px 8px;
            border-radius: 2px;
        }}
        .wisdom-card .card-anchors code {{
            background: var(--code-bg);
            border: 1px solid var(--border-color);
            padding: 1px 5px;
            border-radius: 3px;
            font-size: 0.7rem;
            color: var(--accent-color);
            margin-right: 4px;
        }}
        .wisdom-card ul.takeaways {{
            margin: 4px 0 0 0;
            padding-left: 18px;
        }}
        .wisdom-card ul.takeaways li {{ margin-bottom: 3px; }}
        .wisdom-card .tag-row {{ margin-top: 8px; }}
        .wisdom-card .tag {{
            display: inline-block;
            background: var(--code-bg);
            border: 1px solid var(--border-color);
            border-radius: 3px;
            padding: 1px 7px;
            font-size: 0.7rem;
            color: var(--accent-color);
            margin: 2px 4px 2px 0;
            font-family: var(--font-stack);
        }}

        /* Workbench Mode: visibility + editable fields */
        body.workbench .wisdom-card {{ border-left-color: #238636; }}
        body.workbench .wb-editable {{
            border: 1px dashed var(--border-color);
            padding: 6px 8px;
            border-radius: 3px;
            transition: border-color 0.2s;
        }}
        body.workbench .wb-editable:hover {{ border-color: var(--accent-color); }}
        body.workbench .wb-editable:focus {{ outline: none; border-style: solid; border-color: var(--accent-color); }}
        body.workbench .origin-quote.wb-locked {{
            border-color: #d29922;
            color: #8b949e;
            cursor: not-allowed;
        }}

        /* Read-only DNA collection locks */
        body.dna-ro .wb-editable {{
            border: none !important;
            padding: 0 !important;
            cursor: default !important;
        }}
        body.dna-ro #wb-add-card, body.dna-ro #wb-save-disk {{
            display: none !important;
        }}

        .wb-toolbar {{
            display: none;
            gap: 8px;
            align-items: center;
            margin-bottom: 12px;
            font-family: var(--font-stack);
            font-size: 0.75rem;
            color: var(--sub-color);
        }}
        body.workbench .wb-toolbar {{ display: flex; }}
        .wb-btn {{
            background: var(--code-bg);
            border: 1px solid var(--border-color);
            color: var(--text-color);
            font-family: var(--font-stack);
            font-size: 0.75rem;
            padding: 5px 12px;
            border-radius: 4px;
            cursor: pointer;
            transition: background 0.2s;
        }}
        .wb-btn:hover {{ background: var(--accent-dim); color: #fff; }}
        .wb-btn.add-card {{ border-color: #238636; color: #3fb950; }}
        .wb-btn.save-disk {{ border-color: #238636; color: #3fb950; font-weight: bold; }}
        .wb-btn.export {{ border-color: var(--accent-color); color: var(--accent-color); }}
        #wb-save-status {{ font-family: var(--font-stack); font-size: 0.75rem; }}
    </style>
</head>
<body>
<!-- [SOURCE_OF_TRUTH] Compiled from: {REL_SOURCE}. Do NOT edit wisdom.html directly! -->

    <button id="menu-toggle">☰ MENU</button>

    <nav id="sidebar">
        <mission-control></mission-control>
    </nav>

    <main>
        <div id="sys-console">
            <div>[INIT] Mounting Wisdom Studio...</div>
        </div>

        <section id="studio">
            <div class="wisdom-header">
                <h2 class="section-title">The Wisdom Studio: Multi-DNA Workbench</h2>
                <div>
                    <button id="toggle-workbench" class="view-toggle" title="Toggle in-place workbench mode">⚒ Workbench</button>
                    <button id="toggle-reader" class="view-toggle active" title="Public reader view">◈ Reader</button>
                </div>
            </div>

            <div class="dna-selector-bar">
                <label for="dna-select"><strong>DNA COLLECTION:</strong></label>
                <select id="dna-select" class="dna-select">
                    <option value="wisdom" selected>Wisdom DNA (RW)</option>
                    <option value="writer">Writer DNA (RW)</option>
                    <option value="feature">Feature DNA (RO)</option>
                    <option value="behavioral">Behavioral DNA [BKM] (RO)</option>
                    <option value="sprint">Sprint DNA (RO)</option>
                    <option value="philosophy">Philosophy DNA (RO)</option>
                </select>
                <span id="dna-badge" class="dna-badge rw">[READ-WRITE WORKBENCH]</span>
            </div>

            <div class="disclaimer-box" style="margin-bottom: 20px;">
                <span style="color: var(--accent-color); font-weight: bold;">[WIS-001 SCHEMA]</span>
                Wisdom cards pair an <strong>immutable origin</strong> (a verbatim, non-editable source quote) with a
                <strong>live synthesis</strong> (narrative context, takeaways, lab anchors, and tags). Reader View is the public,
                read-only presentation; Workbench Mode enables in-place curation of the synthesis layer with direct REST disk persistence on port 8765.
            </div>

            <div class="wb-toolbar" id="wb-toolbar">
                <button class="wb-btn add-card" id="wb-add-card">+ New Card</button>
                <button class="wb-btn save-disk" id="wb-save-disk">💾 Save to Disk</button>
                <button class="wb-btn export" id="wb-export">Export JSON</button>
                <span id="wb-save-status"></span>
            </div>

            <div id="wisdom-container" class="wisdom-grid">
{cards_html}
            </div>
        </section>
    </main>

    <script src="mission-control.js"></script>
    <script>
        // [FEAT-559 / FEAT-561] Story 76.2 & Story 77.1: Multi-DNA Wisdom Studio
        (function () {{
            'use strict';
            var currentMode = window.location.search.indexOf('edit=1') !== -1 ? 'workbench' : 'reader';
            var currentCollection = 'wisdom';
            var isReadOnly = false;

            function escapeHtml(str) {{
                return String(str == null ? '' : str)
                    .replace(/&/g, '&amp;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;')
                    .replace(/"/g, '&quot;');
            }}

            function setMode(mode) {{
                currentMode = mode;
                document.body.classList.toggle('workbench', mode === 'workbench');
                var readerBtn = document.getElementById('toggle-reader');
                var wbBtn = document.getElementById('toggle-workbench');
                if (readerBtn) readerBtn.classList.toggle('active', mode === 'reader');
                if (wbBtn) wbBtn.classList.toggle('active', mode === 'workbench');
                var url = new URL(window.location.href);
                if (mode === 'workbench') {{ url.searchParams.set('edit', '1'); }}
                else {{ url.searchParams.delete('edit'); }}
                window.history.replaceState({{}}, '', url.toString());
                updateEditableState();
            }}

            function updateEditableState() {{
                var container = document.getElementById('wisdom-container');
                if (!container) return;
                var editable = container.querySelectorAll('.wb-editable');
                var canEdit = (currentMode === 'workbench') && !isReadOnly;
                editable.forEach(function (el) {{
                    el.setAttribute('contenteditable', canEdit ? 'true' : 'false');
                    el.setAttribute('spellcheck', 'false');
                }});
            }}

            function setCollection(col) {{
                currentCollection = col;
                isReadOnly = (col === 'feature' || col === 'behavioral' || col === 'sprint' || col === 'philosophy');
                document.body.classList.toggle('dna-ro', isReadOnly);

                var badge = document.getElementById('dna-badge');
                if (badge) {{
                    if (isReadOnly) {{
                        badge.className = 'dna-badge ro';
                        badge.textContent = '[READ-ONLY SYSTEM DNA]';
                    }} else {{
                        badge.className = 'dna-badge rw';
                        badge.textContent = '[READ-WRITE WORKBENCH]';
                    }}
                }}

                var manifest = window.__DNA_MANIFEST__ || {{}};
                var cards = manifest[col] || [];
                if (cards.length > 0) {{
                    renderCollectionCards(cards);
                }}
                updateEditableState();
            }}

            function renderCollectionCards(cards) {{
                var container = document.getElementById('wisdom-container');
                if (!container) return;
                var html = '';
                cards.forEach(function (c, idx) {{
                    var cid = c.id || ('CARD-' + (idx + 1));
                    var theme = c.theme || c.type || currentCollection.toUpperCase();
                    var bucket_id = (c.metadata && c.metadata.bucket_id) || c.bucket_id || '';
                    var origin = c.origin || {{}};
                    var synthesis = c.synthesis || {{}};
                    var verbatim = origin.text || origin.verbatim || '';
                    var title = c.title || synthesis.title || ('Item ' + (idx + 1));
                    var narrative = synthesis.narrative_context || '';
                    var review_notes = synthesis.review_notes || '';
                    var tags = (c.metadata && c.metadata.tags) || synthesis.tags || [];
                    var anchors = synthesis.lab_anchors || [];

                    var tagsHtml = tags.map(function (t) {{ return '<span class="tag">' + escapeHtml(t) + '</span>'; }}).join('');
                    var anchorsHtml = anchors.length ? '<div class="card-section"><span class="section-label">Lab Anchors</span><div class="card-anchors">' +
                        anchors.map(function (a) {{ return '<code>' + escapeHtml(a) + '</code>'; }}).join(' ') + '</div></div>' : '';

                    html += '<div class="wisdom-card" data-card-id="' + escapeHtml(cid) + '" data-card-index="' + (idx + 1) + '">' +
                        '<div class="card-meta-row"><span><strong>' + escapeHtml(cid) + '</strong> &bull; ' + escapeHtml(theme) + '</span>' +
                        (bucket_id ? '<span class="bucket-badge">' + escapeHtml(bucket_id) + '</span>' : '') + '</div>' +
                        '<div class="card-title wb-editable" data-field="title" contenteditable="false">' + escapeHtml(title) + '</div>' +
                        '<div class="card-section"><span class="section-label">Origin <span class="immutable-flag">[IMMUTABLE]</span></span>' +
                        '<div class="origin-quote wb-locked" data-field="origin" contenteditable="false">' + escapeHtml(verbatim) + '</div></div>' +
                        '<div class="card-section"><span class="section-label">Narrative Context</span>' +
                        '<div class="wb-editable" data-field="narrative_context" contenteditable="false">' + (escapeHtml(narrative) || '<span style="color:#666;">(add narrative context)</span>') + '</div></div>' +
                        (review_notes ? '<div class="card-section"><span class="section-label">Review Notes</span><div class="review-notes wb-editable" data-field="review_notes" contenteditable="false">' + escapeHtml(review_notes) + '</div></div>' : '') +
                        anchorsHtml +
                        '<div class="card-section tag-row"><span class="section-label">Tags</span><div><div class="wb-editable" data-field="tags" contenteditable="false">' + tagsHtml + '</div></div></div>' +
                        '</div>';
                }});
                container.innerHTML = html;
            }}

            function serializeCards(container) {{
                var cards = [];
                container.querySelectorAll('.wisdom-card').forEach(function (card, idx) {{
                    var cid = card.dataset.cardId || ('WIS-' + String(idx + 1).padStart(3, '0'));
                    var getField = function (f) {{
                        var el = card.querySelector('[data-field="' + f + '"]');
                        return el ? el.textContent.trim() : '';
                    }};
                    var titleEl = card.querySelector('.card-title');
                    var originEl = card.querySelector('.origin-quote');
                    var bucketEl = card.querySelector('.bucket-badge');
                    var tagsText = getField('tags');
                    var tags = tagsText ? tagsText.split(/[\\s,]+/).filter(Boolean) : [];

                    cards.push({{
                        "id": cid,
                        "theme": "Wisdom",
                        "paper_order": idx + 1,
                        "origin": {{
                            "author": "jallred",
                            "text": originEl ? originEl.textContent.trim() : '',
                            "source": "Wisdom Studio Workbench",
                            "immutable": true
                        }},
                        "synthesis": {{
                            "title": titleEl ? titleEl.textContent.trim() : '',
                            "narrative_context": getField('narrative_context'),
                            "review_notes": getField('review_notes'),
                            "last_refined_by": "HUMAN_WORKBENCH",
                            "refinement_version": 1
                        }},
                        "metadata": {{
                            "tags": tags,
                            "bucket_id": bucketEl ? bucketEl.textContent.trim() : 'bucket_1_jitc',
                            "status": "APPROVED"
                        }}
                    }});
                }});
                return cards;
            }}

            function wireControls() {{
                var wbBtn = document.getElementById('toggle-workbench');
                var readerBtn = document.getElementById('toggle-reader');
                if (wbBtn) wbBtn.addEventListener('click', function () {{ setMode('workbench'); }});
                if (readerBtn) readerBtn.addEventListener('click', function () {{ setMode('reader'); }});

                var dnaSelect = document.getElementById('dna-select');
                if (dnaSelect) {{
                    dnaSelect.addEventListener('change', function () {{
                        setCollection(dnaSelect.value);
                    }});
                }}

                var container = document.getElementById('wisdom-container');
                var addBtn = document.getElementById('wb-add-card');
                if (addBtn && !addBtn.dataset.wired) {{
                    addBtn.dataset.wired = '1';
                    addBtn.addEventListener('click', function () {{
                        if (isReadOnly) return;
                        var card = document.createElement('div');
                        card.className = 'wisdom-card';
                        var newId = 'WIS-' + String(container.querySelectorAll('.wisdom-card').length + 1).padStart(3, '0');
                        card.dataset.cardId = newId;
                        card.innerHTML = '<div class="card-meta-row"><span><strong>' + newId + '</strong> &bull; New Wisdom</span><span class="bucket-badge">bucket_1_jitc</span></div>' +
                            '<div class="card-title wb-editable" data-field="title" contenteditable="true">New Wisdom Card</div>' +
                            '<div class="card-section"><span class="section-label">Origin <span class="immutable-flag">[IMMUTABLE]</span></span>' +
                            '<div class="origin-quote wb-locked" data-field="origin" contenteditable="false">(immutable origin quote)</div></div>' +
                            '<div class="card-section"><span class="section-label">Narrative Context</span>' +
                            '<div class="wb-editable" data-field="narrative_context" contenteditable="true">(add narrative context)</div></div>' +
                            '<div class="card-section"><span class="section-label">Review Notes</span>' +
                            '<div class="review-notes wb-editable" data-field="review_notes" contenteditable="true">(review notes)</div></div>' +
                            '<div class="card-section tag-row"><span class="section-label">Tags</span><div><div class="wb-editable" data-field="tags" contenteditable="true"><span class="tag">draft</span></div></div></div>';
                        container.appendChild(card);
                        card.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                        updateEditableState();
                    }});
                }}

                var saveDiskBtn = document.getElementById('wb-save-disk');
                if (saveDiskBtn && !saveDiskBtn.dataset.wired) {{
                    saveDiskBtn.dataset.wired = '1';
                    saveDiskBtn.addEventListener('click', function () {{
                        if (isReadOnly) return;
                        var status = document.getElementById('wb-save-status');
                        if (status) status.innerHTML = '<span style="color:var(--accent-color);">Saving to disk...</span>';
                        var cardsData = serializeCards(container);
                        var payload = {{ cards: cardsData, collection: currentCollection }};

                        fetch('http://127.0.0.1:8765/wisdom/save', {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify(payload)
                        }})
                        .then(function (res) {{ return res.json(); }})
                        .then(function (data) {{
                            if (data.status === 'success') {{
                                var now = new Date().toLocaleTimeString();
                                if (status) status.innerHTML = '<span style="color:#3fb950; font-weight:bold;">✓ Saved ' + (data.count || cardsData.length) + ' card(s) to disk at ' + now + '</span>';
                                setTimeout(function () {{ if (status) status.textContent = ''; }}, 4000);
                            }} else {{
                                if (status) status.innerHTML = '<span style="color:#f85149;">Error: ' + (data.message || 'Save failed') + '</span>';
                            }}
                        }})
                        .catch(function (err) {{
                            fetch('/wisdom/save', {{
                                method: 'POST',
                                headers: {{ 'Content-Type': 'application/json' }},
                                body: JSON.stringify(payload)
                            }})
                            .then(function (res) {{ return res.json(); }})
                            .then(function (data) {{
                                var now = new Date().toLocaleTimeString();
                                if (status) status.innerHTML = '<span style="color:#3fb950;">✓ Saved ' + cardsData.length + ' card(s) at ' + now + '</span>';
                                setTimeout(function () {{ if (status) status.textContent = ''; }}, 4000);
                            }})
                            .catch(function (fbErr) {{
                                if (status) status.innerHTML = '<span style="color:#f85149;">Save failed (Foyer daemon offline): ' + escapeHtml(err.message) + '</span>';
                            }});
                        }});
                    }});
                }}

                var exportBtn = document.getElementById('wb-export');
                if (exportBtn && !exportBtn.dataset.wired) {{
                    exportBtn.dataset.wired = '1';
                    exportBtn.addEventListener('click', function () {{
                        var cardsData = serializeCards(container);
                        var blob = new Blob([JSON.stringify(cardsData, null, 2)], {{ type: 'application/json' }});
                        var a = document.createElement('a');
                        a.href = URL.createObjectURL(blob);
                        a.download = 'wisdom_data_export.json';
                        document.body.appendChild(a);
                        a.click();
                        document.body.removeChild(a);
                        URL.revokeObjectURL(a.href);
                        var status = document.getElementById('wb-save-status');
                        if (status) {{
                            status.textContent = '✓ Exported ' + cardsData.length + ' card(s)';
                            setTimeout(function () {{ status.textContent = ''; }}, 3000);
                        }}
                    }});
                }}
            }}

            function init() {{
                wireControls();
                setMode(currentMode);
            }}

            if (document.readyState === 'loading') {{
                document.addEventListener('DOMContentLoaded', init);
            }} else {{
                init();
            }}
        }})();
    </script>
    <script>
        // [FEAT-559] Embedded DNA Manifest & Canonical Card Schema
        window.__DNA_MANIFEST__ = {json.dumps(manifest)};
        window.__WISDOM_SCHEMA__ = {json.dumps({'schema': schema})};
    </script>
</body>
</html>
"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(page_html)

    ensure_symlink()
    print(f"✅ Successfully compiled {OUTPUT_HTML} with {len(cards)} card(s) from {DATA_PATH}")


if __name__ == "__main__":
    build_page()
