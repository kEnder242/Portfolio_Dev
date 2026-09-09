#!/usr/bin/env python3
# wisdom_build.py [v2.0]
# [FEAT-559] Story 76.2: Dual-View Wisdom Studio
# Purpose: Generate wisdom.html from data/wisdom_data.json featuring a solidified public
#          reader view and an in-place interactive workbench mode (?edit=1 or toggle).
#          Also ensures backward-compatible symlink philosophy.html -> wisdom.html.
# Schema: Wisdom cards pair an immutable origin (verbatim) with a live synthesis
#         (narrative_context, takeaways, tags). See WIS-001.

import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "wisdom_data.json"
TEMPLATE_HTML = BASE_DIR / "wisdom.html"
OUTPUT_HTML = BASE_DIR / "wisdom.html"
REL_SOURCE = "Portfolio_Dev/field_notes/data/wisdom_data.json"

# [FEAT-559] Self-healing fallback: if wisdom.html is ever truncated/missing the
# wisdom-container marker, regenerate the shell from this embedded default so a
# corrupted generated file can never brick the build. Kept minimal and aligned
# with the sibling pages (style.css + mission-control.js + inline workbench JS).
DEFAULT_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wisdom Studio | Jason Allred</title>
    <link rel="stylesheet" href="style.css?v=700f9482">
    <style>
        .wisdom-header { display: flex; align-items: baseline; justify-content: space-between; gap: 20px; flex-wrap: wrap; margin-bottom: 8px; }
        .section-title { margin-bottom: 4px; }
        .view-toggle { font-family: var(--font-stack); font-size: 0.7rem; color: var(--accent-color); background: transparent; border: 1px solid var(--border-color); padding: 4px 10px; border-radius: 4px; cursor: pointer; transition: background 0.2s, border-color 0.2s; }
        .view-toggle:hover { border-color: var(--accent-color); background: var(--code-bg); }
        .view-toggle.active { border-color: var(--accent-color); color: #fff; }
        .wisdom-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 16px; margin-top: 20px; }
        .wisdom-card { background: var(--card-bg); border: 1px solid var(--border-color); border-left: 4px solid var(--accent-color); padding: 16px 18px; font-family: var(--font-stack); font-size: 0.85rem; line-height: 1.5; border-radius: 4px; }
        .wisdom-card .card-title { font-weight: bold; color: var(--heading-color); font-size: 0.95rem; margin-bottom: 8px; border-bottom: 1px solid var(--border-color); padding-bottom: 6px; }
        .wisdom-card .card-section { margin-bottom: 10px; }
        .wisdom-card .section-label { display: inline-block; font-weight: bold; color: var(--accent-color); text-transform: uppercase; font-size: 0.7rem; letter-spacing: 1px; margin-bottom: 4px; }
        .wisdom-card .immutable-flag { color: #d29922; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1px; margin-left: 6px; }
        .wisdom-card .origin-quote { border-left: 2px solid var(--accent-dim); padding-left: 10px; color: var(--sub-color); font-style: italic; font-size: 0.8rem; white-space: pre-wrap; }
        .wisdom-card ul.takeaways { margin: 4px 0 0 0; padding-left: 18px; }
        .wisdom-card ul.takeaways li { margin-bottom: 3px; }
        .wisdom-card .tag-row { margin-top: 8px; }
        .wisdom-card .tag { display: inline-block; background: var(--code-bg); border: 1px solid var(--border-color); border-radius: 3px; padding: 1px 7px; font-size: 0.7rem; color: var(--accent-color); margin: 2px 4px 2px 0; font-family: var(--font-stack); }
        body.workbench .wisdom-card { border-left-color: #238636; }
        body.workbench .wb-editable { border: 1px dashed var(--border-color); padding: 6px 8px; border-radius: 3px; transition: border-color 0.2s; }
        body.workbench .wb-editable:hover { border-color: var(--accent-color); }
        body.workbench .wb-editable:focus { outline: none; border-style: solid; border-color: var(--accent-color); }
        body.workbench .origin-quote.wb-locked { border-color: #d29922; color: #8b949e; cursor: not-allowed; }
        .wb-toolbar { display: none; gap: 8px; align-items: center; margin-bottom: 12px; font-family: var(--font-stack); font-size: 0.75rem; color: var(--sub-color); }
        body.workbench .wb-toolbar { display: flex; }
        .wb-btn { background: var(--code-bg); border: 1px solid var(--border-color); color: var(--text-color); font-family: var(--font-stack); font-size: 0.75rem; padding: 5px 12px; border-radius: 4px; cursor: pointer; transition: background 0.2s; }
        .wb-btn:hover { background: var(--accent-dim); color: #fff; }
        .wb-btn.add-card { border-color: #238636; color: #3fb950; }
        .wb-btn.export { border-color: var(--accent-color); color: var(--accent-color); }
        .empty-state { text-align: center; color: var(--sub-color); font-family: var(--font-stack); padding: 40px 20px; border: 1px dashed var(--border-color); border-radius: 4px; margin-top: 20px; }
    </style>
</head>
<body>
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
                <h2 class="section-title">The Wisdom Studio: Dual-View Card Curator</h2>
                <div>
                    <button id="toggle-workbench" class="view-toggle" title="Toggle in-place workbench mode">⚒ Workbench</button>
                    <button id="toggle-reader" class="view-toggle active" title="Public reader view">◈ Reader</button>
                </div>
            </div>
            <div class="disclaimer-box" style="margin-bottom: 20px;">
                <span style="color: var(--accent-color); font-weight: bold;">[WIS-001 SCHEMA]</span>
                Wisdom cards pair an <strong>immutable origin</strong> (a verbatim, non-editable source quote) with a
                <strong>live synthesis</strong> (narrative context, takeaways, and tags). Reader View is the public,
                read-only presentation; Workbench Mode enables in-place curation of the synthesis layer.
            </div>
            <div class="wb-toolbar" id="wb-toolbar">
                <button class="wb-btn add-card" id="wb-add-card">+ New Card</button>
                <button class="wb-btn export" id="wb-export">Export JSON</button>
                <span id="wb-save-status"></span>
            </div>
            <div id="wisdom-container">
                <!-- Cards rendered by wisdom_build.py from wisdom_data.json -->
            </div>
        </section>
    </main>
    <script src="mission-control.js"></script>
    <script>
        // [FEAT-559] Story 76.2: Dual-View Wisdom Studio
        // Reader View (public, read-only) + Workbench Mode (in-place curation).
        (function () {
            'use strict';
            var currentMode = window.location.search.indexOf('edit=1') !== -1 ? 'workbench' : 'reader';
            function setMode(mode) {
                currentMode = mode;
                document.body.classList.toggle('workbench', mode === 'workbench');
                var readerBtn = document.getElementById('toggle-reader');
                var wbBtn = document.getElementById('toggle-workbench');
                if (readerBtn) readerBtn.classList.toggle('active', mode === 'reader');
                if (wbBtn) wbBtn.classList.toggle('active', mode === 'workbench');
                var url = new URL(window.location.href);
                if (mode === 'workbench') { url.searchParams.set('edit', '1'); }
                else { url.searchParams.delete('edit'); }
                window.history.replaceState({}, '', url.toString());
            }
            function initToggle() {
                var wbBtn = document.getElementById('toggle-workbench');
                var readerBtn = document.getElementById('toggle-reader');
                if (wbBtn) wbBtn.addEventListener('click', function () { setMode('workbench'); });
                if (readerBtn) readerBtn.addEventListener('click', function () { setMode('reader'); });
                setMode(currentMode);
            }
            function wireWorkbench() {
                var container = document.getElementById('wisdom-container');
                if (!container) return;
                var editable = container.querySelectorAll('.wb-editable');
                editable.forEach(function (el) {
                    if (el.getAttribute('contenteditable')) return;
                    el.setAttribute('contenteditable', 'true');
                    el.setAttribute('spellcheck', 'false');
                });
                var addBtn = document.getElementById('wb-add-card');
                if (addBtn && !addBtn.dataset.wired) {
                    addBtn.dataset.wired = '1';
                    addBtn.addEventListener('click', function () {
                        var card = document.createElement('div');
                        card.className = 'wisdom-card';
                        card.innerHTML = '<div class="card-title wb-editable" data-field="title" contenteditable="true">New Wisdom Card</div>' +
                            '<div class="card-section"><span class="section-label">Origin <span class="immutable-flag">[IMMUTABLE]</span></span>' +
                            '<div class="origin-quote wb-locked">(no origin yet)</div></div>' +
                            '<div class="card-section"><span class="section-label">Narrative Context</span>' +
                            '<div class="wb-editable" data-field="narrative_context" contenteditable="true">(add narrative context)</div></div>' +
                            '<div class="card-section"><span class="section-label">Takeaways</span>' +
                            '<ul class="takeaways"><li class="wb-editable" data-field="takeaways" contenteditable="true">(add a takeaway)</li></ul></div>' +
                            '<div class="tag-row"><span class="section-label">Tags</span> <span class="wb-editable" data-field="tags" contenteditable="true"></span></div>';
                        container.appendChild(card);
                        card.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    });
                }
                var exportBtn = document.getElementById('wb-export');
                if (exportBtn && !exportBtn.dataset.wired) {
                    exportBtn.dataset.wired = '1';
                    exportBtn.addEventListener('click', function () { exportCards(container); });
                }
                container.querySelectorAll('.wisdom-card').forEach(function (card) {
                    card.querySelectorAll('.wb-editable').forEach(function (el) {
                        if (!el.getAttribute('contenteditable')) {
                            el.setAttribute('contenteditable', 'true');
                            el.setAttribute('spellcheck', 'false');
                        }
                    });
                });
            }
            function exportCards(container) {
                var schema;
                try { schema = window.__WISDOM_SCHEMA__ || { "schema": {} }; } catch (e) { schema = { "schema": {} }; }
                var cards = container.querySelectorAll('.wisdom-card');
                var output = { "schema": schema.schema || {}, "cards": [] };
                cards.forEach(function (card) {
                    var getField = function (f) {
                        var el = card.querySelector('[data-field="' + f + '"]');
                        return el ? el.textContent.trim() : '';
                    };
                    var titleEl = card.querySelector('.card-title');
                    var originEl = card.querySelector('.origin-quote');
                    output.cards.push({
                        "id": "WIS-" + String(output.cards.length + 1).padStart(3, '0'),
                        "title": (titleEl ? titleEl.textContent.trim() : ''),
                        "origin": { "immutable": true, "verbatim": originEl ? originEl.textContent.trim() : '' },
                        "synthesis": {
                            "narrative_context": getField('narrative_context'),
                            "takeaways": (getField('takeaways') || '').split(/\\n/).filter(Boolean),
                            "tags": (getField('tags') || '').split(/[\\s,]+/).filter(Boolean)
                        }
                    });
                });
                var blob = new Blob([JSON.stringify(output, null, 2)], { type: 'application/json' });
                var a = document.createElement('a');
                a.href = URL.createObjectURL(blob);
                a.download = 'wisdom_data_export.json';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(a.href);
                var status = document.getElementById('wb-save-status');
                if (status) { status.textContent = '✓ Exported ' + cards.length + ' card(s)'; setTimeout(function () { status.textContent = ''; }, 3000); }
            }
            function init() { initToggle(); wireWorkbench(); }
            if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', init); } else { init(); }
        })();
    </script>
</body>
</html>
"""


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
    """Extract cards from wisdom_data.json.

    Supports two layouts:
      * Future/normalized: a top-level ``cards`` list, each item carrying
        ``origin`` + ``synthesis`` (+ optional ``title`` / ``id``).
      * Legacy/single (WIS-001): the existing file nests one card inside
        ``schema`` (origin + synthesis at the top level of ``schema``).
    Returns (cards, schema_dict).
    """
    schema = data.get("schema", {})
    cards = data.get("cards", [])

    if not cards:
        # Backward-compatible single-card layout: schema holds origin+synthesis.
        card = {
            "title": schema.get("synthesis", {}).get("title", "Wisdom Card"),
            "origin": schema.get("origin", {}),
            "synthesis": schema.get("synthesis", {}),
        }
        cards = [card]

    return cards, schema


def render_takeaways(takeaways):
    if not takeaways:
        return '<div class="wb-editable" data-field="takeaways" contenteditable="false" style="color:#666;">(none recorded)</div>'
    items = "".join(
        f'<li>{escape_html(t)}</li>'
        for t in takeaways
    )
    # Single data-field anchor per card so workbench export captures ALL takeaways.
    return (
        f'<ul class="takeaways wb-editable" data-field="takeaways" contenteditable="false">{items}</ul>'
    )


def render_tags(tags):
    if not tags:
        return '<span class="wb-editable" data-field="tags" contenteditable="false" style="color:#666;">(no tags)</span>'
    inner = "".join(f'<span class="tag">{escape_html(t)}</span>' for t in tags)
    # Single data-field anchor per card so workbench export captures ALL tags.
    return (
        f'<div class="wb-editable" data-field="tags" contenteditable="false">{inner}</div>'
    )


def render_card(card, index):
    origin = card.get("origin", {}) or {}
    synthesis = card.get("synthesis", {}) or {}
    verbatim = origin.get("verbatim", "") or escape_html(card.get("verbatim", ""))
    title = card.get("title") or synthesis.get("title") or f"Wisdom Card {index}"

    origin_html = (
        f'<div class="origin-quote wb-locked" data-field="origin" '
        f'contenteditable="false">{escape_html(verbatim)}</div>'
        if verbatim
        else '<div class="origin-quote wb-locked" data-field="origin" contenteditable="false">(no origin recorded)</div>'
    )

    narrative = escape_html(synthesis.get("narrative_context", "")) or (
        '<span style="color:#666;">(add narrative context)</span>'
    )

    html = f"""
        <div class="wisdom-card" data-card-index="{index}">
            <div class="card-title wb-editable" data-field="title" contenteditable="false">{escape_html(title)}</div>
            <div class="card-section">
                <span class="section-label">Origin <span class="immutable-flag">[IMMUTABLE]</span></span>
                {origin_html}
            </div>
            <div class="card-section">
                <span class="section-label">Narrative Context</span>
                <div class="wb-editable" data-field="narrative_context" contenteditable="false">{narrative}</div>
            </div>
            <div class="card-section">
                <span class="section-label">Takeaways</span>
                {render_takeaways(synthesis.get("takeaways", []))}
            </div>
            <div class="card-section tag-row">
                <span class="section-label">Tags</span>
                <div>{render_tags(synthesis.get("tags", []))}</div>
            </div>
        </div>"""
    return html


def render_cards(cards):
    return "\n".join(render_card(card, i + 1) for i, card in enumerate(cards))


def inject(content, tag, payload):
    start = content.find(tag)
    if start == -1:
        return content, False
    return content[: start + len(tag)] + "\n" + payload + content[start + len(tag):], True


def inject_before(content, tag, payload):
    """Insert ``payload`` immediately BEFORE the first occurrence of ``tag``."""
    start = content.find(tag)
    if start == -1:
        return content, False
    return content[:start] + payload + content[start:], True


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


def load_template():
    """Read wisdom.html; if missing/truncated (no container marker or body tag),
    fall back to the embedded DEFAULT_TEMPLATE so the build always self-heals."""
    if TEMPLATE_HTML.exists():
        raw = TEMPLATE_HTML.read_text(encoding="utf-8")
        if "<div id=\"wisdom-container\">" in raw and "<body>" in raw:
            return raw
        print(f"⚠️  {TEMPLATE_HTML} missing/truncated — regenerating from embedded default template.")
    return DEFAULT_TEMPLATE


def main():
    if not DATA_PATH.exists():
        print(f"Error: {DATA_PATH} not found. No cards generated.")
        # Still ensure symlink + write a minimal template copy so the page isn't broken.
        ensure_symlink()
        return

    with open(DATA_PATH, "r") as f:
        data = json.load(f)

    cards, schema = load_cards(data)
    cards_html = render_cards(cards)

    content = load_template()

    # Source-of-truth marker (idempotent).
    source_comment = f"<!-- [SOURCE_OF_TRUTH] Compiled from: {REL_SOURCE}. Do NOT edit wisdom.html directly! -->\n"
    if "<!-- [SOURCE_OF_TRUTH]" not in content:
        body_idx = content.find("<body>")
        if body_idx != -1:
            content = content[: body_idx + 6] + "\n" + source_comment + content[body_idx + 6:]
    else:
        import re
        content = re.sub(r"<!-- \[SOURCE_OF_TRUTH\].*?-->\n", source_comment, content)

    # Render cards into the container — idempotent: replace whatever currently sits
    # between the container's opening and closing tags (so re-runs never duplicate).
    import re
    container_re = re.compile(
        r'(<div id="wisdom-container">)(.*?)(</div>\s*</section>)',
        re.DOTALL,
    )
    match = container_re.search(content)
    if not match:
        print("Error: wisdom-container not found in template.")
        return
    updated = content[: match.start()] + match.group(1) + "\n" + cards_html + match.group(3) + content[match.end():]

    # Embed schema for the workbench exporter (window.__WISDOM_SCHEMA__) — idempotent.
    # Drop any previously embedded block first so we never duplicate it on re-runs.
    import re
    updated = re.sub(
        r"<script>\s*// \[FEAT-559\] Workbench export context.*?</script>\n?",
        "",
        updated,
        flags=re.DOTALL,
    )
    schema_js = (
        "<script>\n"
        "// [FEAT-559] Workbench export context: canonical card schema.\n"
        f"window.__WISDOM_SCHEMA__ = {json.dumps({'schema': schema})};\n"
        "</script>\n"
    )
    # Insert just before </body> (after the strip, exactly one copy remains).
    updated, ok_schema = inject_before(updated, "</body>", schema_js)

    with open(OUTPUT_HTML, "w") as f:
        f.write(updated)

    ensure_symlink()

    print(f"✅ Successfully compiled {OUTPUT_HTML} with {len(cards)} card(s) from {DATA_PATH}")
    if philosophy := (BASE_DIR / "philosophy.html"):
        target = os.readlink(philosophy) if philosophy.is_symlink() else "(not a symlink)"
        print(f"   philosophy.html -> {target}")


if __name__ == "__main__":
    main()
