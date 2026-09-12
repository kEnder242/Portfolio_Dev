#!/usr/bin/env python3
# wisdom_build.py [v4.0]
# [FEAT-559 / FEAT-568 / FEAT-569] Story 77.0: Multi-DNA In-Place Wisdom Studio & Single-Card REST Save
# Purpose: Generate wisdom.html from data/wisdom_data.json and data/dna_manifest.json
#          featuring in-place per-card unlock/save/discard curation, reactive bucket selector,
#          DNA collection switcher (RW vs RO), stubbed Markdown origin backflow,
#          and atomic single-card REST disk save via Foyer (:8765/wisdom/save_card).
# Schema: Wisdom cards pair an immutable origin (verbatim) with live synthesis. See WIS-001.

import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "wisdom_data.json"
PHILOSOPHY_PATH = BASE_DIR / "data" / "philosophy_data.json"
BUCKETS_PATH = BASE_DIR / "data" / "buckets.json"
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


def load_buckets():
    """Load taxonomy buckets from buckets.json."""
    if BUCKETS_PATH.exists():
        try:
            with open(BUCKETS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Could not load buckets.json: {e}")
    return [
        {"id": "bucket_1_jitc", "name": "Memory & Just-In-Time Context (JITC)"},
        {"id": "bucket_2_backpressure", "name": "Stability, Feedback & Backpressure"},
        {"id": "bucket_3_foil", "name": "Human-AI Interface & The Perfect Foil"},
        {"id": "bucket_4_rigor", "name": "Engineering Rigor & Verification Vectors"},
        {"id": "bucket_5_infra", "name": "Sovereign Architecture & Federated Silicon"}
    ]


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


def render_bucket_controls(bucket_id, buckets, is_rw):
    """Render bucket badge + hidden bucket select dropdown for in-place switching."""
    options = []
    found = False
    for b in buckets:
        bid = b.get("id", "")
        bname = b.get("name", bid)
        sel = ' selected' if bid == bucket_id else ''
        if sel:
            found = True
        options.append(f'<option value="{escape_html(bid)}"{sel}>{escape_html(bname)}</option>')
    if not found and bucket_id:
        options.insert(0, f'<option value="{escape_html(bucket_id)}" selected>{escape_html(bucket_id)}</option>')
    
    options_html = "".join(options)
    badge_html = f'<span class="bucket-badge" data-bucket-id="{escape_html(bucket_id)}">{escape_html(bucket_id if bucket_id else "No Bucket")}</span>'
    select_html = f'<select class="bucket-select" style="display:none;" data-field="bucket_id">{options_html}</select>'
    return badge_html + (select_html if is_rw else "")


def render_card(card, index, buckets, is_rw=True):
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

    bucket_ctrl_html = render_bucket_controls(bucket_id, buckets, is_rw=is_rw)

    if is_rw:
        action_btn_html = """<div class="card-actions">
            <button class="card-btn-edit" title="Unlock and edit this card in-place">🔓 Edit</button>
            <button class="card-btn-save" style="display:none;" title="Save changes atomically to disk and ChromaDB">💾 Save</button>
            <button class="card-btn-discard" style="display:none;" title="Discard unsaved changes">✖ Discard</button>
            <span class="card-save-status"></span>
        </div>"""
    else:
        action_btn_html = """<div class="card-actions">
            <span class="ro-stub-badge" title="Markdown origin files (Protocols.md / FeatureTracker.md) are git-anchored and read-only in this studio">[ 🔒 Markdown Origin (Git Anchored) - Stubbed ]</span>
        </div>"""

    html = f"""
        <div class="wisdom-card" data-card-id="{escape_html(cid)}" data-card-index="{index}">
            <div class="card-top-bar">
                <div class="card-meta-row">
                    <span><strong>{escape_html(cid)}</strong> &bull; {escape_html(theme)}</span>
                    <div class="bucket-container">
                        {bucket_ctrl_html}
                    </div>
                </div>
                {action_btn_html}
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


def render_cards(cards, buckets, is_rw=True):
    return "\n".join(render_card(card, i + 1, buckets, is_rw=is_rw) for i, card in enumerate(cards))


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

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        wisdom_cards = json.load(f)

    buckets = load_buckets()
    cards, schema = load_cards(wisdom_cards)
    cards_html = render_cards(cards, buckets, is_rw=True)

    manifest = {}
    if MANIFEST_PATH.exists():
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)

    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wisdom Studio | Jason Allred</title>
    <link rel="stylesheet" href="style.css?v=826dbad3">
    <style>
        /* Wisdom Studio: In-Place Multi-DNA Studio [v4.0] */
        .wisdom-header {{
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            gap: 20px;
            flex-wrap: wrap;
            margin-bottom: 8px;
        }}
        .section-title {{ margin-bottom: 4px; }}

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
            transition: border-left-color 0.2s, box-shadow 0.2s;
            position: relative;
        }}
        .wisdom-card.card-editing {{
            border-left-color: #238636 !important;
            box-shadow: 0 0 10px rgba(35, 134, 54, 0.25);
        }}
        .wisdom-card .card-top-bar {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 10px;
            margin-bottom: 8px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            padding-bottom: 6px;
        }}
        .wisdom-card .card-meta-row {{
            display: flex;
            flex-direction: column;
            gap: 4px;
            font-size: 0.7rem;
            color: var(--sub-color);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .wisdom-card .bucket-badge {{
            color: var(--accent-color);
            font-weight: bold;
            display: inline-block;
        }}
        .wisdom-card .bucket-select {{
            background: var(--code-bg);
            border: 1px solid var(--accent-color);
            color: var(--text-color);
            padding: 2px 6px;
            border-radius: 3px;
            font-family: var(--font-stack);
            font-size: 0.7rem;
            max-width: 190px;
        }}

        /* Per-Card In-Place Actions */
        .wisdom-card .card-actions {{
            display: flex;
            align-items: center;
            gap: 6px;
            flex-shrink: 0;
        }}
        .wisdom-card .card-btn-edit,
        .wisdom-card .card-btn-save,
        .wisdom-card .card-btn-discard {{
            font-family: var(--font-stack);
            font-size: 0.7rem;
            padding: 3px 8px;
            border-radius: 3px;
            cursor: pointer;
            transition: background 0.15s, border-color 0.15s;
            background: var(--code-bg);
            border: 1px solid var(--border-color);
            color: var(--text-color);
        }}
        .wisdom-card .card-btn-edit:hover {{
            border-color: var(--accent-color);
            color: var(--accent-color);
        }}
        .wisdom-card .card-btn-save {{
            border-color: #238636;
            color: #3fb950;
            font-weight: bold;
        }}
        .wisdom-card .card-btn-save:hover {{
            background: rgba(35, 134, 54, 0.2);
        }}
        .wisdom-card .card-btn-discard {{
            border-color: #f85149;
            color: #f85149;
        }}
        .wisdom-card .card-btn-discard:hover {{
            background: rgba(248, 81, 73, 0.2);
        }}
        .wisdom-card .card-save-status {{
            font-size: 0.68rem;
            font-family: var(--font-stack);
            margin-left: 4px;
        }}
        .ro-stub-badge {{
            font-size: 0.65rem;
            padding: 2px 6px;
            border-radius: 3px;
            background: rgba(210, 153, 34, 0.15);
            border: 1px solid #d29922;
            color: #d29922;
            font-family: var(--font-stack);
            letter-spacing: 0.3px;
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
        .wisdom-card .origin-quote.wb-locked {{
            border-color: #d29922;
            color: #8b949e;
            cursor: not-allowed;
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

        /* In-Place Editing Styles */
        .wisdom-card.card-editing .wb-editable {{
            border: 1px dashed var(--accent-color) !important;
            padding: 4px 6px !important;
            border-radius: 3px;
            background: rgba(255, 255, 255, 0.02);
            outline: none;
        }}
        .wisdom-card.card-editing .wb-editable:focus {{
            border-style: solid !important;
            background: rgba(255, 255, 255, 0.04);
        }}

        /* Global Toolbar */
        .studio-toolbar {{
            display: flex;
            gap: 8px;
            align-items: center;
            margin-bottom: 12px;
            font-family: var(--font-stack);
            font-size: 0.75rem;
            color: var(--sub-color);
        }}
        .studio-btn {{
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
        .studio-btn:hover {{ background: var(--accent-dim); color: #fff; }}
        .studio-btn.add-card {{ border-color: #238636; color: #3fb950; }}
        .studio-btn.export {{ border-color: var(--accent-color); color: var(--accent-color); }}
        #studio-toolbar-status {{ font-family: var(--font-stack); font-size: 0.75rem; }}
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
                <span id="dna-badge" class="dna-badge rw">[READ-WRITE STUDIO]</span>
            </div>

            <div class="disclaimer-box" style="margin-bottom: 20px;">
                <span style="color: var(--accent-color); font-weight: bold;">[WIS-001 SCHEMA & IN-PLACE STUDIO]</span>
                Wisdom cards pair an <strong>immutable origin</strong> (a verbatim, non-editable source quote) with a
                <strong>live synthesis</strong> (narrative context, takeaways, lab anchors, and tags). Each card can be
                unlocked, edited, bucket-categorized, and saved individually with atomic REST persistence on port 8765.
            </div>

            <div class="studio-toolbar" id="studio-toolbar">
                <button class="studio-btn add-card" id="studio-add-card">+ New Card</button>
                <button class="studio-btn export" id="studio-export">Export JSON</button>
                <span id="studio-toolbar-status"></span>
            </div>

            <div id="wisdom-container" class="wisdom-grid">
{cards_html}
            </div>
        </section>
    </main>

    <script src="mission-control.js"></script>
    <script>
        // [FEAT-559 / FEAT-568 / FEAT-569] In-Place Wisdom Studio & Single-Card Save Engine
        (function () {{
            'use strict';
            var currentCollection = 'wisdom';
            var isReadOnly = false;
            var BUCKETS = {json.dumps(buckets)};

            function escapeHtml(str) {{
                return String(str == null ? '' : str)
                    .replace(/&/g, '&amp;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;')
                    .replace(/"/g, '&quot;');
            }}

            function setCollection(col) {{
                currentCollection = col;
                isReadOnly = (col === 'feature' || col === 'behavioral' || col === 'sprint' || col === 'philosophy');
                document.body.classList.toggle('dna-ro', isReadOnly);

                var badge = document.getElementById('dna-badge');
                var addBtn = document.getElementById('studio-add-card');
                if (badge) {{
                    if (isReadOnly) {{
                        badge.className = 'dna-badge ro';
                        badge.textContent = '[READ-ONLY SYSTEM DNA]';
                    }} else {{
                        badge.className = 'dna-badge rw';
                        badge.textContent = '[READ-WRITE STUDIO]';
                    }}
                }}
                if (addBtn) {{
                    addBtn.style.display = isReadOnly ? 'none' : 'inline-block';
                }}

                var manifest = window.__DNA_MANIFEST__ || {{}};
                var cards = manifest[col] || [];
                if (cards.length > 0) {{
                    renderCollectionCards(cards);
                }}
            }}

            function renderBucketControlsJs(bucket_id, is_rw) {{
                var options = [];
                var found = false;
                BUCKETS.forEach(function (b) {{
                    var bid = b.id || '';
                    var bname = b.name || bid;
                    var sel = (bid === bucket_id) ? ' selected' : '';
                    if (sel) found = true;
                    options.push('<option value="' + escapeHtml(bid) + '"' + sel + '>' + escapeHtml(bname) + '</option>');
                }});
                if (!found && bucket_id) {{
                    options.unshift('<option value="' + escapeHtml(bucket_id) + '" selected>' + escapeHtml(bucket_id) + '</option>');
                }}
                var badgeHtml = '<span class="bucket-badge" data-bucket-id="' + escapeHtml(bucket_id) + '">' + escapeHtml(bucket_id ? bucket_id : 'No Bucket') + '</span>';
                var selectHtml = '<select class="bucket-select" style="display:none;" data-field="bucket_id">' + options.join('') + '</select>';
                return badgeHtml + (is_rw ? selectHtml : '');
            }}

            function renderCollectionCards(cards) {{
                var container = document.getElementById('wisdom-container');
                if (!container) return;
                var html = '';
                var is_rw = !isReadOnly;
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

                    var actionsHtml = is_rw ?
                        '<div class="card-actions">' +
                            '<button class="card-btn-edit" title="Unlock and edit this card in-place">🔓 Edit</button>' +
                            '<button class="card-btn-save" style="display:none;" title="Save changes atomically to disk and ChromaDB">💾 Save</button>' +
                            '<button class="card-btn-discard" style="display:none;" title="Discard unsaved changes">✖ Discard</button>' +
                            '<span class="card-save-status"></span>' +
                        '</div>' :
                        '<div class="card-actions">' +
                            '<span class="ro-stub-badge" title="Markdown origin files are git-anchored and read-only in this studio">[ 🔒 Markdown Origin (Git Anchored) - Stubbed ]</span>' +
                        '</div>';

                    html += '<div class="wisdom-card" data-card-id="' + escapeHtml(cid) + '" data-card-index="' + (idx + 1) + '">' +
                        '<div class="card-top-bar">' +
                            '<div class="card-meta-row">' +
                                '<span><strong>' + escapeHtml(cid) + '</strong> &bull; ' + escapeHtml(theme) + '</span>' +
                                '<div class="bucket-container">' + renderBucketControlsJs(bucket_id, is_rw) + '</div>' +
                            '</div>' +
                            actionsHtml +
                        '</div>' +
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
                wireCardActions(container);
            }}

            function serializeSingleCard(card) {{
                var cid = card.dataset.cardId || 'WIS-000';
                var getField = function (f) {{
                    var el = card.querySelector('[data-field="' + f + '"]');
                    return el ? el.textContent.trim() : '';
                }};
                var titleEl = card.querySelector('.card-title');
                var originEl = card.querySelector('.origin-quote');
                var bucketSelect = card.querySelector('.bucket-select');
                var bucketBadge = card.querySelector('.bucket-badge');
                var bucketId = (bucketSelect && bucketSelect.value) || (bucketBadge && bucketBadge.dataset.bucketId) || 'bucket_1_jitc';

                var tagsText = getField('tags');
                var tags = tagsText ? tagsText.split(/[\\s,]+/).filter(Boolean) : [];

                return {{
                    "id": cid,
                    "theme": "Wisdom",
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
                        "refinement_version": 2
                    }},
                    "metadata": {{
                        "tags": tags,
                        "bucket_id": bucketId,
                        "status": "APPROVED"
                    }}
                }};
            }}

            function unlockCard(card) {{
                // Snapshot original state
                var titleEl = card.querySelector('.card-title');
                var narrEl = card.querySelector('[data-field="narrative_context"]');
                var notesEl = card.querySelector('[data-field="review_notes"]');
                var tagsEl = card.querySelector('[data-field="tags"]');
                var bucketBadge = card.querySelector('.bucket-badge');
                var bucketSelect = card.querySelector('.bucket-select');

                card.__snapshot__ = {{
                    title: titleEl ? titleEl.innerHTML : '',
                    narrative: narrEl ? narrEl.innerHTML : '',
                    notes: notesEl ? notesEl.innerHTML : '',
                    tags: tagsEl ? tagsEl.innerHTML : '',
                    bucketId: (bucketSelect && bucketSelect.value) || (bucketBadge && bucketBadge.dataset.bucketId) || ''
                }};

                card.classList.add('card-editing');
                var editable = card.querySelectorAll('.wb-editable');
                editable.forEach(function (el) {{
                    el.setAttribute('contenteditable', 'true');
                    el.setAttribute('spellcheck', 'false');
                }});

                if (bucketBadge) bucketBadge.style.display = 'none';
                if (bucketSelect) {{
                    bucketSelect.style.display = 'inline-block';
                    if (card.__snapshot__.bucketId) bucketSelect.value = card.__snapshot__.bucketId;
                }}

                var btnEdit = card.querySelector('.card-btn-edit');
                var btnSave = card.querySelector('.card-btn-save');
                var btnDiscard = card.querySelector('.card-btn-discard');
                if (btnEdit) btnEdit.style.display = 'none';
                if (btnSave) btnSave.style.display = 'inline-block';
                if (btnDiscard) btnDiscard.style.display = 'inline-block';
            }}

            function discardCard(card) {{
                if (card.__snapshot__) {{
                    var s = card.__snapshot__;
                    var titleEl = card.querySelector('.card-title');
                    var narrEl = card.querySelector('[data-field="narrative_context"]');
                    var notesEl = card.querySelector('[data-field="review_notes"]');
                    var tagsEl = card.querySelector('[data-field="tags"]');
                    var bucketBadge = card.querySelector('.bucket-badge');
                    var bucketSelect = card.querySelector('.bucket-select');

                    if (titleEl) titleEl.innerHTML = s.title;
                    if (narrEl) narrEl.innerHTML = s.narrative;
                    if (notesEl) notesEl.innerHTML = s.notes;
                    if (tagsEl) tagsEl.innerHTML = s.tags;
                    if (bucketSelect) bucketSelect.value = s.bucketId;
                    if (bucketBadge) {{
                        bucketBadge.textContent = s.bucketId || 'No Bucket';
                        bucketBadge.dataset.bucketId = s.bucketId;
                    }}
                }}
                lockCard(card);
            }}

            function lockCard(card) {{
                card.classList.remove('card-editing');
                var editable = card.querySelectorAll('.wb-editable');
                editable.forEach(function (el) {{
                    el.setAttribute('contenteditable', 'false');
                }});

                var bucketBadge = card.querySelector('.bucket-badge');
                var bucketSelect = card.querySelector('.bucket-select');
                if (bucketSelect) {{
                    var val = bucketSelect.value;
                    if (bucketBadge) {{
                        bucketBadge.textContent = val || 'No Bucket';
                        bucketBadge.dataset.bucketId = val;
                    }}
                    bucketSelect.style.display = 'none';
                }}
                if (bucketBadge) bucketBadge.style.display = 'inline-block';

                var btnEdit = card.querySelector('.card-btn-edit');
                var btnSave = card.querySelector('.card-btn-save');
                var btnDiscard = card.querySelector('.card-btn-discard');
                if (btnEdit) btnEdit.style.display = 'inline-block';
                if (btnSave) btnSave.style.display = 'none';
                if (btnDiscard) btnDiscard.style.display = 'none';
            }}

            function saveCard(card) {{
                var statusEl = card.querySelector('.card-save-status');
                if (statusEl) statusEl.innerHTML = '<span style="color:var(--accent-color);">Saving...</span>';

                var cardData = serializeSingleCard(card);
                var payload = {{
                    card: cardData,
                    collection: currentCollection
                }};

                var saveUrl = 'http://127.0.0.1:8765/wisdom/save_card';
                var fallbackUrl = '/wisdom/save_card';

                function doFetch(url) {{
                    return fetch(url, {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(payload)
                    }}).then(function (res) {{ return res.json(); }});
                }}

                doFetch(saveUrl)
                    .then(function (data) {{
                        handleSaveSuccess(card, data, statusEl);
                    }})
                    .catch(function (err) {{
                        doFetch(fallbackUrl)
                            .then(function (data) {{
                                handleSaveSuccess(card, data, statusEl);
                            }})
                            .catch(function (fbErr) {{
                                if (statusEl) statusEl.innerHTML = '<span style="color:#f85149;">Save failed (Foyer offline)</span>';
                            }});
                    }});
            }}

            function handleSaveSuccess(card, data, statusEl) {{
                if (data.status === 'success') {{
                    var now = new Date().toLocaleTimeString();
                    if (statusEl) {{
                        statusEl.innerHTML = '<span style="color:#3fb950; font-weight:bold;">✓ Saved at ' + now + '</span>';
                        setTimeout(function () {{ statusEl.textContent = ''; }}, 3500);
                    }}
                    lockCard(card);
                }} else {{
                    if (statusEl) statusEl.innerHTML = '<span style="color:#f85149;">Error: ' + escapeHtml(data.message || 'Save failed') + '</span>';
                }}
            }}

            function wireCardActions(targetContainer) {{
                var container = targetContainer || document.getElementById('wisdom-container');
                if (!container) return;

                container.querySelectorAll('.wisdom-card').forEach(function (card) {{
                    if (card.dataset.wiredActions) return;
                    card.dataset.wiredActions = '1';

                    var btnEdit = card.querySelector('.card-btn-edit');
                    var btnSave = card.querySelector('.card-btn-save');
                    var btnDiscard = card.querySelector('.card-btn-discard');

                    if (btnEdit) {{
                        btnEdit.addEventListener('click', function () {{
                            unlockCard(card);
                        }});
                    }}
                    if (btnDiscard) {{
                        btnDiscard.addEventListener('click', function () {{
                            discardCard(card);
                        }});
                    }}
                    if (btnSave) {{
                        btnSave.addEventListener('click', function () {{
                            saveCard(card);
                        }});
                    }}
                }});
            }}

            function wireControls() {{
                var dnaSelect = document.getElementById('dna-select');
                if (dnaSelect) {{
                    dnaSelect.addEventListener('change', function () {{
                        setCollection(dnaSelect.value);
                    }});
                }}

                var container = document.getElementById('wisdom-container');
                wireCardActions(container);

                var addBtn = document.getElementById('studio-add-card');
                if (addBtn && !addBtn.dataset.wired) {{
                    addBtn.dataset.wired = '1';
                    addBtn.addEventListener('click', function () {{
                        if (isReadOnly) return;
                        var newIdx = container.querySelectorAll('.wisdom-card').length + 1;
                        var newId = 'WIS-' + String(newIdx).padStart(3, '0');
                        var card = document.createElement('div');
                        card.className = 'wisdom-card';
                        card.dataset.cardId = newId;
                        card.dataset.cardIndex = newIdx;

                        card.innerHTML = '<div class="card-top-bar">' +
                            '<div class="card-meta-row">' +
                                '<span><strong>' + newId + '</strong> &bull; Wisdom</span>' +
                                '<div class="bucket-container">' + renderBucketControlsJs('bucket_1_jitc', true) + '</div>' +
                            '</div>' +
                            '<div class="card-actions">' +
                                '<button class="card-btn-edit" title="Unlock and edit this card in-place">🔓 Edit</button>' +
                                '<button class="card-btn-save" style="display:none;" title="Save changes atomically to disk and ChromaDB">💾 Save</button>' +
                                '<button class="card-btn-discard" style="display:none;" title="Discard unsaved changes">✖ Discard</button>' +
                                '<span class="card-save-status"></span>' +
                            '</div>' +
                        '</div>' +
                        '<div class="card-title wb-editable" data-field="title" contenteditable="false">New Wisdom Card</div>' +
                        '<div class="card-section"><span class="section-label">Origin <span class="immutable-flag">[IMMUTABLE]</span></span>' +
                        '<div class="origin-quote wb-locked" data-field="origin" contenteditable="false">(immutable origin quote)</div></div>' +
                        '<div class="card-section"><span class="section-label">Narrative Context</span>' +
                        '<div class="wb-editable" data-field="narrative_context" contenteditable="false">(add narrative context)</div></div>' +
                        '<div class="card-section"><span class="section-label">Review Notes</span>' +
                        '<div class="review-notes wb-editable" data-field="review_notes" contenteditable="false">(review notes)</div></div>' +
                        '<div class="card-section tag-row"><span class="section-label">Tags</span><div><div class="wb-editable" data-field="tags" contenteditable="false"><span class="tag">draft</span></div></div></div>';

                        container.prepend(card);
                        wireCardActions(container);
                        unlockCard(card);
                        card.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                    }});
                }}

                var exportBtn = document.getElementById('studio-export');
                if (exportBtn && !exportBtn.dataset.wired) {{
                    exportBtn.dataset.wired = '1';
                    exportBtn.addEventListener('click', function () {{
                        var cardsData = [];
                        container.querySelectorAll('.wisdom-card').forEach(function (card) {{
                            cardsData.push(serializeSingleCard(card));
                        }});
                        var blob = new Blob([JSON.stringify(cardsData, null, 2)], {{ type: 'application/json' }});
                        var a = document.createElement('a');
                        a.href = URL.createObjectURL(blob);
                        a.download = 'wisdom_studio_export.json';
                        document.body.appendChild(a);
                        a.click();
                        document.body.removeChild(a);
                        URL.revokeObjectURL(a.href);
                        var status = document.getElementById('studio-toolbar-status');
                        if (status) {{
                            status.textContent = '✓ Exported ' + cardsData.length + ' card(s)';
                            setTimeout(function () {{ status.textContent = ''; }}, 3000);
                        }}
                    }});
                }}
            }}

            function init() {{
                wireControls();
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
