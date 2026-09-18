#!/usr/bin/env python3
# dna_forge_build.py [v2.0]
# [FEAT-582 / FEAT-559 / FEAT-568 / FEAT-569] The DNA Forge: Multi-DNA Workbench & Single-Card Save Engine
# Purpose: Generate dna_forge.html and wisdom.html from data/dna_manifest.json featuring:
#          - Universal DNA collection dropdown selector (PHL, WIS, RDNA, DISC, FEAT, BKM, SPRINT)
#          - In-place per-card unlock/save/discard curation for all RW collections
#          - Reactive taxonomy bucket selector and lateral re-bucketing
#          - Real-time search filter and status badges
#          - Atomic REST disk save via Foyer (:8765/wisdom/save_card) and ChromaDB synchronization

import json
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = BASE_DIR / "data" / "dna_manifest.json"
WISDOM_PATH = BASE_DIR / "data" / "wisdom_data.json"
PHILOSOPHY_PATH = BASE_DIR / "data" / "philosophy_data.json"
RDNA_PATH = BASE_DIR / "data" / "rdna_questions.json"
BUCKETS_PATH = BASE_DIR / "data" / "buckets.json"
OUTPUT_FORGE = BASE_DIR / "dna_forge.html"
OUTPUT_WISDOM = BASE_DIR / "wisdom.html"


def escape_html(text):
    return (
        str(text if text is not None else "")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def load_buckets():
    if BUCKETS_PATH.exists():
        try:
            with open(BUCKETS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Could not load buckets.json: {e}")
    return [
        {"id": "bucket_1_jitc", "name": "Memory & Just-In-Time Context (JITC)", "theme": "Memory & JITC"},
        {"id": "bucket_2_backpressure", "name": "Stability, Feedback & Backpressure", "theme": "Stability & Feedback"},
        {"id": "bucket_3_foil", "name": "Human-AI Interface & The Perfect Foil", "theme": "Human-AI Interface"},
        {"id": "bucket_4_rigor", "name": "Engineering Rigor & Verification Vectors", "theme": "Engineering Rigor"},
        {"id": "bucket_5_infra", "name": "Sovereign Architecture & Federated Silicon", "theme": "Architecture & Infrastructure"}
    ]


def load_manifest():
    if MANIFEST_PATH.exists():
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Could not load dna_manifest.json: {e}")
    return {}


def render_bucket_controls(bucket_id, buckets, is_rw=True):
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


def render_card_html(card, index, buckets, is_rw=True):
    cid = card.get("id") or f"DNA-{index:03d}"
    theme = card.get("theme") or card.get("type") or "DNA"
    meta = card.get("metadata", {}) or {}
    bucket_id = meta.get("bucket_id") or card.get("bucket_id", "")
    
    origin = card.get("origin", {}) or {}
    synthesis = card.get("synthesis", {}) or {}
    verbatim = origin.get("text", "") or origin.get("verbatim", "") or card.get("verbatim", "")
    title = card.get("title") or synthesis.get("title") or f"DNA Item {index}"
    narrative = synthesis.get("narrative_context", "")
    review_notes = synthesis.get("review_notes", "")
    anchors = synthesis.get("lab_anchors", [])
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
            <span class="ro-stub-badge" title="Origin files are git-anchored and read-only in this studio">[ 🔒 Git-Anchored Read-Only ]</span>
        </div>"""

    anchors_html = ""
    if anchors:
        a_items = " ".join(f"<code>{escape_html(a)}</code>" for a in anchors)
        anchors_html = f'<div class="card-section"><span class="section-label">Lab Anchors</span><div class="card-anchors">{a_items}</div></div>'

    tags_inner = "".join(f'<span class="tag">{escape_html(t)}</span>' for t in tags)
    tags_html = f'<div class="wb-editable" data-field="tags" contenteditable="false">{tags_inner}</div>'

    return f"""
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
                <div class="wb-editable" data-field="narrative_context" contenteditable="false">{escape_html(narrative)}</div>
            </div>
            {review_notes_html}
            {anchors_html}
            <div class="card-section tag-row">
                <span class="section-label">Tags</span>
                <div>{tags_html}</div>
            </div>
        </div>"""


def build_page():
    manifest = load_manifest()
    buckets = load_buckets()
    
    # Default to philosophy cards on initial render
    default_cards = manifest.get("philosophy", [])
    if not default_cards and manifest.get("wisdom"):
        default_cards = manifest.get("wisdom", [])

    cards_html = "\n".join(render_card_html(c, i + 1, buckets, is_rw=True) for i, c in enumerate(default_cards))

    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DNA Forge | Federated Lab Knowledge Foundry</title>
    <link rel="stylesheet" href="style.css?v=312b4371">
    <style>
        /* DNA Forge: In-Place Multi-DNA Studio [v5.0] */
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
            padding: 10px 14px;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            font-family: var(--font-stack);
            font-size: 0.85rem;
            flex-wrap: wrap;
        }}
        .dna-select {{
            background: var(--code-bg);
            border: 1px solid var(--border-color);
            color: var(--text-color);
            padding: 6px 12px;
            border-radius: 4px;
            font-family: var(--font-stack);
            font-size: 0.85rem;
            cursor: pointer;
            font-weight: 500;
        }}
        .dna-select:focus {{
            border-color: var(--accent-color);
            outline: none;
        }}
        .dna-badge {{
            font-size: 0.7rem;
            padding: 3px 10px;
            border-radius: 4px;
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

        .search-filter-input {{
            background: var(--code-bg);
            border: 1px solid var(--border-color);
            color: var(--text-color);
            padding: 6px 12px;
            border-radius: 4px;
            font-family: var(--font-stack);
            font-size: 0.85rem;
            min-width: 220px;
            margin-left: auto;
        }}
        .search-filter-input:focus {{
            border-color: var(--accent-color);
            outline: none;
        }}

        .wisdom-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
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
            box-shadow: 0 0 12px rgba(35, 134, 54, 0.3);
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
            font-size: 0.72rem;
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
            font-size: 0.72rem;
            max-width: 220px;
        }}

        /* Per-Card In-Place Actions */
        .wisdom-card .card-actions {{
            display: flex;
            align-items: center;
            gap: 6px;
            flex-shrink: 0;
        }}
        .card-btn-edit, .card-btn-save, .card-btn-discard {{
            background: transparent;
            border: 1px solid var(--border-color);
            color: var(--text-color);
            font-family: var(--font-stack);
            font-size: 0.72rem;
            padding: 3px 8px;
            border-radius: 3px;
            cursor: pointer;
            transition: all 0.15s ease;
        }}
        .card-btn-edit:hover {{
            border-color: var(--accent-color);
            color: var(--accent-color);
        }}
        .card-btn-save {{
            background: #238636;
            border-color: #2ea043;
            color: #fff;
            font-weight: bold;
        }}
        .card-btn-save:hover {{
            background: #2ea043;
        }}
        .card-btn-discard {{
            border-color: #da3633;
            color: #f85149;
        }}
        .card-btn-discard:hover {{
            background: rgba(218, 54, 51, 0.15);
        }}
        .card-save-status {{
            font-size: 0.7rem;
            margin-left: 4px;
        }}
        .ro-stub-badge {{
            font-size: 0.65rem;
            color: var(--sub-color);
            font-style: italic;
        }}

        .wisdom-card .card-title {{
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--text-color);
            margin-bottom: 10px;
            line-height: 1.35;
        }}
        .wisdom-card .card-section {{
            margin-bottom: 8px;
        }}
        .wisdom-card .section-label {{
            display: block;
            font-size: 0.68rem;
            color: var(--sub-color);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 2px;
            font-weight: bold;
        }}
        .wisdom-card .immutable-flag {{
            font-size: 0.6rem;
            color: #8b949e;
            font-weight: normal;
        }}
        .wisdom-card .origin-quote {{
            background: var(--code-bg);
            border-left: 2px solid var(--sub-color);
            padding: 6px 10px;
            font-style: italic;
            color: #c9d1d9;
            margin: 4px 0;
            border-radius: 0 3px 3px 0;
            font-size: 0.82rem;
            max-height: 160px;
            overflow-y: auto;
        }}
        .wisdom-card .origin-quote.wb-locked {{
            cursor: not-allowed;
            opacity: 0.9;
        }}
        .wisdom-card .card-anchors code {{
            background: var(--code-bg);
            border: 1px solid var(--border-color);
            padding: 1px 5px;
            border-radius: 3px;
            font-size: 0.72rem;
            color: var(--accent-color);
            display: inline-block;
            margin: 2px 2px 2px 0;
        }}
        .wisdom-card .review-notes {{
            color: #8b949e;
            font-size: 0.78rem;
            font-style: italic;
        }}
        .wisdom-card .tag-row .tag {{
            display: inline-block;
            background: rgba(56, 139, 253, 0.12);
            color: var(--accent-color);
            border: 1px solid rgba(56, 139, 253, 0.3);
            border-radius: 3px;
            padding: 1px 6px;
            font-size: 0.7rem;
            margin: 2px 4px 2px 0;
        }}

        /* Contenteditable styling when active */
        .wisdom-card.card-editing .wb-editable[contenteditable="true"] {{
            background: rgba(255, 255, 255, 0.04);
            border: 1px dashed var(--accent-color);
            padding: 4px 6px;
            border-radius: 3px;
            outline: none;
            min-height: 20px;
        }}

        /* Studio Toolbar */
        .studio-toolbar {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 10px 0;
        }}
        .studio-btn {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            color: var(--text-color);
            padding: 5px 12px;
            border-radius: 4px;
            font-size: 0.78rem;
            cursor: pointer;
        }}
        .studio-btn:hover {{
            border-color: var(--accent-color);
        }}
        .studio-btn.add-card {{
            background: rgba(56, 139, 253, 0.15);
            border-color: var(--accent-color);
            color: var(--accent-color);
            font-weight: bold;
        }}

        body.dna-ro .studio-btn.add-card {{
            display: none !important;
        }}
    </style>
</head>
<body>
    <button id="menu-toggle">☰ MENU</button>

    <nav id="sidebar">
        <mission-control></mission-control>
    </nav>

    <main>
        <div id="sys-console">
            <div>[INIT] Mounting DNA Forge Knowledge Foundry...</div>
        </div>

        <section id="studio">
            <div class="wisdom-header">
                <h2 class="section-title">The DNA Forge: Sovereign Multi-Domain Knowledge Foundry</h2>
            </div>

            <div class="dna-selector-bar">
                <label for="dna-select"><strong>DNA COLLECTION:</strong></label>
                <select id="dna-select" class="dna-select">
                    <option value="all" selected>ALL Collections (Universal Browse &amp; Search)</option>
                    <option value="philosophy">Philosophy DNA [PHL] (RW)</option>
                    <option value="wisdom">War Stories &amp; Wisdom [WIS] (RW)</option>
                    <option value="rdna">Reverse DNA Questions [RDNA] (RW)</option>
                    <option value="discovery">Innovations Timeline [DISC] (RW)</option>
                    <option value="feature">Feature DNA [FEAT] (RO)</option>
                    <option value="behavioral">Behavioral DNA [BKM] (RO)</option>
                    <option value="sprint">Sprint DNA [SPRINT] (RO)</option>
                </select>
                <span id="dna-badge" class="dna-badge rw">[ALL COLLECTIONS]</span>
                <input type="text" id="dnaSearchInput" class="search-filter-input" placeholder="🔍 Search across ALL DNA (620+ cards)...">
            </div>

            <div class="disclaimer-box" style="margin-bottom: 20px;">
                <span style="color: var(--accent-color); font-weight: bold;">[FIRST-CLASS DNA CITIZEN ARCHITECTURE]</span>
                All federated knowledge domains (<code>PHL</code>, <code>WIS</code>, <code>RDNA</code>, <code>DISC</code>, <code>FEAT</code>, <code>BKM</code>, <code>SPRINT</code>) share a polymorphic schema.
                Unlock, edit, laterally re-bucket, and persist cards with atomic REST synchronization on port 8765.
            </div>

            <div class="studio-toolbar" id="studio-toolbar">
                <button class="studio-btn add-card" id="studio-add-card" style="display:none;">+ New Card</button>
                <button class="studio-btn export" id="studio-export">Export JSON</button>
                <span id="studio-toolbar-status"></span>
            </div>

            <div id="wisdom-container" class="wisdom-grid">
{cards_html}
            </div>
        </section>
    </main>

    <script src="script.js?v=acd57779"></script>
    <script src="mission-control.js?v=b505a681"></script>
    <script>
        (function () {{
            'use strict';
            var currentCollection = 'all';
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
                isReadOnly = (col === 'feature' || col === 'behavioral' || col === 'sprint');
                document.body.classList.toggle('dna-ro', isReadOnly);

                var badge = document.getElementById('dna-badge');
                var addBtn = document.getElementById('studio-add-card');
                if (badge) {{
                    if (col === 'all') {{
                        badge.className = 'dna-badge rw';
                        badge.textContent = '[ALL COLLECTIONS]';
                    }} else if (isReadOnly) {{
                        badge.className = 'dna-badge ro';
                        badge.textContent = '[READ-ONLY SYSTEM DNA]';
                    }} else {{
                        badge.className = 'dna-badge rw';
                        badge.textContent = '[READ-WRITE STUDIO]';
                    }}
                }}
                if (addBtn) {{
                    addBtn.style.display = (isReadOnly || col === 'all') ? 'none' : 'inline-block';
                }}

                var manifest = window.__DNA_MANIFEST__ || {{}};
                var cards = [];
                if (col === 'all') {{
                    ['philosophy', 'wisdom', 'rdna', 'discovery', 'feature', 'behavioral', 'sprint'].forEach(function (k) {{
                        var list = manifest[k] || [];
                        list.forEach(function (item) {{
                            var copy = Object.assign({{}}, item);
                            copy._sourceCollection = k;
                            cards.push(copy);
                        }});
                    }});
                }} else {{
                    cards = manifest[col] || [];
                }}
                renderCollectionCards(cards);
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
                cards.forEach(function (c, idx) {{
                    var sourceCol = c._sourceCollection || currentCollection;
                    var cardIsRw = (sourceCol === 'philosophy' || sourceCol === 'wisdom' || sourceCol === 'rdna' || sourceCol === 'discovery');
                    var cid = c.id || ('CARD-' + (idx + 1));
                    var theme = c.theme || c.type || sourceCol.toUpperCase();
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

                    var actionsHtml = cardIsRw ?
                        '<div class="card-actions">' +
                            '<button class="card-btn-edit" title="Unlock and edit this card in-place">🔓 Edit</button>' +
                            '<button class="card-btn-save" style="display:none;" title="Save changes atomically to disk and ChromaDB">💾 Save</button>' +
                            '<button class="card-btn-discard" style="display:none;" title="Discard unsaved changes">✖ Discard</button>' +
                            '<span class="card-save-status"></span>' +
                        '</div>' :
                        '<div class="card-actions">' +
                            '<span class="ro-stub-badge" title="Origin files are git-anchored and read-only in this studio">[ 🔒 Git-Anchored Read-Only ]</span>' +
                        '</div>';

                    html += '<div class="wisdom-card" data-card-id="' + escapeHtml(cid) + '" data-card-index="' + (idx + 1) + '">' +
                        '<div class="card-top-bar">' +
                            '<div class="card-meta-row">' +
                                '<span><strong>' + escapeHtml(cid) + '</strong> &bull; ' + escapeHtml(theme) + '</span>' +
                                '<div class="bucket-container">' + renderBucketControlsJs(bucket_id, cardIsRw) + '</div>' +
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
                container.innerHTML = html || '<div style="padding: 20px; color: var(--sub-color);">No cards found in this collection.</div>';
                wireCardActions(container);
            }}

            function serializeSingleCard(card) {{
                var cid = card.dataset.cardId || 'DNA-000';
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
                var tags = tagsText ? tagsText.split(/[\s,]+/).filter(Boolean) : [];

                return {{
                    "id": cid,
                    "theme": currentCollection.toUpperCase(),
                    "origin": {{
                        "author": "jallred",
                        "text": originEl ? originEl.textContent.trim() : '',
                        "source": "DNA Forge Studio",
                        "immutable": (currentCollection !== 'rdna')
                    }},
                    "synthesis": {{
                        "title": titleEl ? titleEl.textContent.trim() : '',
                        "narrative_context": getField('narrative_context'),
                        "review_notes": getField('review_notes'),
                        "last_refined_by": "HUMAN_FORGE",
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
                card._originalState = {{
                    title: (card.querySelector('.card-title') || {{}}).textContent || '',
                    narrative: ((card.querySelector('[data-field="narrative_context"]') || {{}}).textContent || ''),
                    review: ((card.querySelector('[data-field="review_notes"]') || {{}}).textContent || ''),
                    tags: ((card.querySelector('[data-field="tags"]') || {{}}).textContent || ''),
                    bucket: (card.querySelector('.bucket-select') || {{}}).value || ''
                }};

                card.classList.add('card-editing');
                card.querySelectorAll('.wb-editable').forEach(function (el) {{
                    el.contentEditable = 'true';
                }});

                var badge = card.querySelector('.bucket-badge');
                var select = card.querySelector('.bucket-select');
                if (badge && select) {{
                    badge.style.display = 'none';
                    select.style.display = 'inline-block';
                }}

                var btnEdit = card.querySelector('.card-btn-edit');
                var btnSave = card.querySelector('.card-btn-save');
                var btnDiscard = card.querySelector('.card-btn-discard');
                if (btnEdit) btnEdit.style.display = 'none';
                if (btnSave) btnSave.style.display = 'inline-block';
                if (btnDiscard) btnDiscard.style.display = 'inline-block';
            }}

            function lockCard(card, revert) {{
                if (revert && card._originalState) {{
                    var t = card.querySelector('.card-title'); if (t) t.textContent = card._originalState.title;
                    var n = card.querySelector('[data-field="narrative_context"]'); if (n) n.textContent = card._originalState.narrative;
                    var r = card.querySelector('[data-field="review_notes"]'); if (r) r.textContent = card._originalState.review;
                    var tg = card.querySelector('[data-field="tags"]'); if (tg) tg.textContent = card._originalState.tags;
                    var s = card.querySelector('.bucket-select'); if (s) s.value = card._originalState.bucket;
                }}

                card.classList.remove('card-editing');
                card.querySelectorAll('.wb-editable').forEach(function (el) {{
                    el.contentEditable = 'false';
                }});

                var badge = card.querySelector('.bucket-badge');
                var select = card.querySelector('.bucket-select');
                if (badge && select) {{
                    badge.textContent = select.value || 'No Bucket';
                    badge.dataset.bucketId = select.value;
                    badge.style.display = 'inline-block';
                    select.style.display = 'none';
                }}

                var btnEdit = card.querySelector('.card-btn-edit');
                var btnSave = card.querySelector('.card-btn-save');
                var btnDiscard = card.querySelector('.card-btn-discard');
                if (btnEdit) btnEdit.style.display = 'inline-block';
                if (btnSave) btnSave.style.display = 'none';
                if (btnDiscard) btnDiscard.style.display = 'none';
            }}

            function saveSingleCard(card) {{
                var status = card.querySelector('.card-save-status');
                var btnSave = card.querySelector('.card-btn-save');
                if (status) status.textContent = 'Saving...';
                if (btnSave) btnSave.disabled = true;

                var cardPayload = serializeSingleCard(card);
                cardPayload.collection = currentCollection;

                fetch('http://127.0.0.1:8765/wisdom/save_card', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(cardPayload)
                }})
                .then(function (res) {{
                    if (!res.ok) throw new Error('HTTP ' + res.status);
                    return res.json();
                }})
                .then(function (data) {{
                    if (status) {{
                        status.textContent = '✓ Saved';
                        status.style.color = '#3fb950';
                        setTimeout(function () {{ status.textContent = ''; }}, 2500);
                    }}
                    lockCard(card, false);
                }})
                .catch(function (err) {{
                    // Fallback to in-browser storage
                    try {{
                        var localSaved = JSON.parse(localStorage.getItem('dna_forge_offline_cards') || '[]');
                        localSaved.push(cardPayload);
                        localStorage.setItem('dna_forge_offline_cards', JSON.stringify(localSaved));
                        if (status) {{
                            status.textContent = '✓ Saved (Local Cache)';
                            status.style.color = '#e3b341';
                            setTimeout(function () {{ status.textContent = ''; }}, 3000);
                        }}
                        lockCard(card, false);
                    }} catch (e) {{
                        if (status) {{
                            status.textContent = '✗ Error: ' + err.message;
                            status.style.color = '#f85149';
                        }}
                    }}
                }})
                .finally(function () {{
                    if (btnSave) btnSave.disabled = false;
                }});
            }}

            function wireCardActions(container) {{
                container.querySelectorAll('.wisdom-card').forEach(function (card) {{
                    if (card.dataset.wired) return;
                    card.dataset.wired = '1';

                    var btnEdit = card.querySelector('.card-btn-edit');
                    var btnSave = card.querySelector('.card-btn-save');
                    var btnDiscard = card.querySelector('.card-btn-discard');

                    if (btnEdit) btnEdit.addEventListener('click', function () {{ unlockCard(card); }});
                    if (btnSave) btnSave.addEventListener('click', function () {{ saveSingleCard(card); }});
                    if (btnDiscard) btnDiscard.addEventListener('click', function () {{ lockCard(card, true); }});
                }});
            }}

            function wireControls() {{
                var sel = document.getElementById('dna-select');
                if (sel && !sel.dataset.wired) {{
                    sel.dataset.wired = '1';
                    sel.addEventListener('change', function () {{
                        setCollection(this.value);
                    }});
                }}

                var searchInput = document.getElementById('dnaSearchInput');
                if (searchInput && !searchInput.dataset.wired) {{
                    searchInput.dataset.wired = '1';
                    searchInput.addEventListener('input', function () {{
                        var q = this.value.toLowerCase().trim();
                        var container = document.getElementById('wisdom-container');
                        if (!container) return;
                        container.querySelectorAll('.wisdom-card').forEach(function (card) {{
                            var text = card.textContent.toLowerCase();
                            card.style.display = (!q || text.indexOf(q) !== -1) ? '' : 'none';
                        }});
                    }});
                }}

                var addBtn = document.getElementById('studio-add-card');
                var container = document.getElementById('wisdom-container');
                if (addBtn && container && !addBtn.dataset.wired) {{
                    addBtn.dataset.wired = '1';
                    addBtn.addEventListener('click', function () {{
                        if (isReadOnly) return;
                        var prefix = currentCollection === 'rdna' ? 'RDNA-' : (currentCollection === 'wisdom' ? 'WIS-' : (currentCollection === 'discovery' ? 'DISC-' : 'PHL-'));
                        var newIdx = container.querySelectorAll('.wisdom-card').length + 1;
                        var newId = prefix + String(newIdx).padStart(3, '0');
                        var card = document.createElement('div');
                        card.className = 'wisdom-card';
                        card.dataset.cardId = newId;
                        card.dataset.cardIndex = newIdx;

                        card.innerHTML = '<div class="card-top-bar">' +
                            '<div class="card-meta-row">' +
                                '<span><strong>' + newId + '</strong> &bull; ' + currentCollection.toUpperCase() + '</span>' +
                                '<div class="bucket-container">' + renderBucketControlsJs('bucket_1_jitc', true) + '</div>' +
                            '</div>' +
                            '<div class="card-actions">' +
                                '<button class="card-btn-edit" title="Unlock and edit this card in-place">🔓 Edit</button>' +
                                '<button class="card-btn-save" style="display:none;" title="Save changes atomically to disk and ChromaDB">💾 Save</button>' +
                                '<button class="card-btn-discard" style="display:none;" title="Discard unsaved changes">✖ Discard</button>' +
                                '<span class="card-save-status"></span>' +
                            '</div>' +
                        '</div>' +
                        '<div class="card-title wb-editable" data-field="title" contenteditable="false">New DNA Card Title</div>' +
                        '<div class="card-section"><span class="section-label">Origin <span class="immutable-flag">[IMMUTABLE]</span></span>' +
                        '<div class="origin-quote wb-locked" data-field="origin" contenteditable="false">(origin record text)</div></div>' +
                        '<div class="card-section"><span class="section-label">Narrative Context</span>' +
                        '<div class="wb-editable" data-field="narrative_context" contenteditable="false">(add narrative context / distilled axiom)</div></div>' +
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
                        a.download = 'dna_forge_export_' + currentCollection + '.json';
                        document.body.appendChild(a);
                        a.click();
                        document.body.removeChild(a);
                        URL.revokeObjectURL(a.href);
                    }});
                }}

                wireCardActions(container);
            }}

            if (document.readyState === 'loading') {{
                document.addEventListener('DOMContentLoaded', wireControls);
            }} else {{
                wireControls();
            }}
        }})();
    </script>
    <script>
        window.__DNA_MANIFEST__ = {json.dumps(manifest)};
    </script>
</body>
</html>
"""

    with open(OUTPUT_FORGE, "w", encoding="utf-8") as f:
        f.write(page_html)

    with open(OUTPUT_WISDOM, "w", encoding="utf-8") as f:
        f.write(page_html)

    print(f"✅ Successfully compiled {OUTPUT_FORGE} and {OUTPUT_WISDOM} with {len(default_cards)} default card(s) and full manifest.")


if __name__ == "__main__":
    build_page()
