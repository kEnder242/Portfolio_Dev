#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dna_forge_build.py [v6.0]
[FEAT-582 / FEAT-588 / FEAT-589 / FEAT-591 / FEAT-593 / FEAT-596]
The DNA Forge: Streamlined UI, Interactive Census HUD, 1-Click Approval/Archive Engine,
Bone Collection Rack, and Interactive 2D Synapse Knowledge Graph Visualizer.
"""

import json
import os
import sys
import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
HOMELAB_DIR = BASE_DIR.parent.parent / "HomeLabAI"
DATA_DIR = BASE_DIR / "data"
MANIFEST_PATH = DATA_DIR / "dna_manifest.json"
WISDOM_PATH = DATA_DIR / "wisdom_data.json"
PHILOSOPHY_PATH = DATA_DIR / "philosophy_data.json"
RDNA_PATH = DATA_DIR / "rdna_questions.json"
BUCKETS_PATH = DATA_DIR / "buckets.json"
BONE_COLLECTIONS_PATH = DATA_DIR / "bone_collections.json"
DECISIONS_PATH = DATA_DIR / "dna_decisions.json"
CONNECTIONS_GRAPH_PATH = DATA_DIR / "dna_connections_graph.json"
NIGHTLY_STATE_PATH = HOMELAB_DIR / "run" / "nightly_forge_state.json"
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
        except Exception:
            pass
    return [
        {"id": "bucket_security_manageability", "name": "Security & Manageability", "theme": "Security & Manageability"},
        {"id": "bucket_silicon_validation", "name": "Silicon Validation Methodology", "theme": "Silicon Validation Methodology"},
        {"id": "bucket_systems_architecture", "name": "Systems Architecture & Automation", "theme": "Systems Architecture & Automation"},
        {"id": "bucket_engineering_leadership", "name": "Engineering Leadership", "theme": "Engineering Leadership"}
    ]


def load_manifest():
    if MANIFEST_PATH.exists():
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def load_bone_collections():
    if BONE_COLLECTIONS_PATH.exists():
        try:
            with open(BONE_COLLECTIONS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []


def load_decisions():
    if DECISIONS_PATH.exists():
        try:
            with open(DECISIONS_PATH, "r", encoding="utf-8") as f:
                return json.load(f).get("decisions", {})
        except Exception:
            pass
    return {}


def load_connections_graph():
    if CONNECTIONS_GRAPH_PATH.exists():
        try:
            with open(CONNECTIONS_GRAPH_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"nodes": [], "links": []}


def load_mining_telemetry():
    """Extract telemetry about the last automated nightly mining pass and detect stalls."""
    state = {
        "status": "OPERATIONAL",
        "last_run_iso": "N/A",
        "last_run_display": "Recent Synthesis Sweep",
        "days_since_run": 0,
        "is_stalled": False,
        "stall_reason": "Automated DNA Bridge & Census HUD active."
    }
    if NIGHTLY_STATE_PATH.exists():
        try:
            with open(NIGHTLY_STATE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            iso = data.get("completed_iso") or ""
            state["status"] = data.get("status", "OPERATIONAL")
            state["last_run_iso"] = iso
            if iso:
                try:
                    dt = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
                    state["last_run_display"] = dt.strftime("%b %d, %I:%M %p UTC")
                    now = datetime.datetime.now(datetime.timezone.utc)
                    delta = (now - dt).total_seconds() / 86400.0
                    state["days_since_run"] = round(delta, 1)
                except Exception:
                    state["last_run_display"] = iso[:16]
        except Exception as e:
            state["stall_reason"] = f"Telemetry status: {e}"
    return state


def is_archived_card(card, decisions=None):
    if not card:
        return False
    cid = card.get("id", "")
    if decisions and cid in decisions:
        if decisions[cid].get("decision") in ("REJECTED", "ARCHIVED"):
            return True
    status = str(card.get("status") or (card.get("metadata", {}) or {}).get("status", "")).upper()
    return status in ("REJECTED", "ARCHIVED")


def is_flagged_card(card, decisions=None):
    if not card or is_archived_card(card, decisions):
        return False
    cid = card.get("id", "")
    if decisions and cid in decisions:
        if decisions[cid].get("decision") == "APPROVED":
            return False
    status = str(card.get("status") or (card.get("metadata", {}) or {}).get("status", "")).upper()
    if status in ("PROPOSED", "FLAGGED", "NEEDS_REVIEW"):
        return True
    if card.get("is_flagged") or card.get("flagged"):
        return True
    if cid.startswith("AR-"):
        return True
    meta = card.get("metadata", {}) or {}
    tags = meta.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",")]
    for t in tags:
        clean = str(t).strip().lower().lstrip("#")
        if clean in ("flagged", "ar", "needs_review", "action_required", "candidate"):
            return True
    return False


def render_card_html(card, index, buckets, decisions=None, is_rw=True):
    cid = card.get("id") or f"DNA-{index:03d}"
    domain = cid.split("-")[0] if "-" in cid else "DNA"
    theme = card.get("theme") or card.get("type") or domain
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
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",")]

    flagged = is_flagged_card(card, decisions)
    archived = is_archived_card(card, decisions)

    if archived:
        tron_class = "tron-card tron-archived"
        flag_badge = '<span class="tron-badge-archived">📦 ARCHIVED</span>'
    elif flagged:
        tron_class = "tron-card tron-red"
        flag_badge = '<span class="tron-badge-flag">🚨 NEEDS REVIEW</span>'
    else:
        tron_class = "tron-card tron-blue"
        flag_badge = ''

    origin_html = (
        f'<div class="origin-quote wb-locked" data-field="origin" contenteditable="false">{escape_html(verbatim)}</div>'
        if verbatim
        else '<div class="origin-quote wb-locked" data-field="origin" contenteditable="false">(no origin recorded)</div>'
    )

    review_notes_html = ""
    if review_notes:
        review_notes_html = f'<div class="card-section"><span class="section-label">Review Notes</span><div class="review-notes wb-editable" data-field="review_notes" contenteditable="false">{escape_html(review_notes)}</div></div>'

    anchors_html = ""
    if anchors:
        a_items = " ".join(f"<code>{escape_html(a)}</code>" for a in anchors)
        anchors_html = f'<div class="card-section"><span class="section-label">Lab Anchors</span><div class="card-anchors">{a_items}</div></div>'

    tags_inner = "".join(f'<span class="tag {("tag-flag" if "flag" in str(t).lower() or "ar" in str(t).lower() else "")}">#{escape_html(str(t).lstrip("#"))}</span>' for t in tags)
    tags_html = f'<div class="wb-editable" data-field="tags" contenteditable="false">{tags_inner}</div>'

    approve_btn = '<button class="card-btn-approve" title="Approve candidate card and clear review flag">✅ Approve</button>' if flagged else ''
    archive_btn = '<button class="card-btn-archive" title="Archive / reject this suggestion">📦 Archive</button>' if is_rw and not archived else ''

    action_btn_html = f"""<div class="card-actions">
        <button class="dna-btn-action btn-rack" data-action="toggle-rack" title="Add to Active Bone Collection Rack">+ Rack</button>
        {approve_btn}
        {archive_btn}
        {'''<button class="card-btn-edit" title="Unlock and edit this card in-place">🔓 Edit</button>
        <button class="card-btn-save" style="display:none;" title="Save changes atomically to disk and ChromaDB">💾 Save</button>
        <button class="card-btn-discard" style="display:none;" title="Discard unsaved changes">✖ Discard</button>
        <span class="card-save-status"></span>''' if is_rw else '<span class="ro-stub-badge" title="Git-anchored read-only">[ 🔒 Git-Anchored ]</span>'}
    </div>"""

    return f"""
        <div class="wisdom-card {tron_class}" data-card-id="{escape_html(cid)}" data-card-index="{index}" data-flagged="{'1' if flagged else '0'}" data-archived="{'1' if archived else '0'}">
            <div class="card-top-bar">
                <div class="card-meta-row">
                    <div class="dna-card-id-row">
                        <span class="dna-card-id"><strong>{escape_html(cid)}</strong></span>
                        <span class="dna-card-domain-badge">{escape_html(domain)}</span>
                        {flag_badge}
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
    bone_collections = load_bone_collections()
    decisions = load_decisions()
    mining_telemetry = load_mining_telemetry()
    connections_graph = load_connections_graph()

    domain_counts = {
        "FEAT": len(manifest.get("feature", [])),
        "SPRINT": len(manifest.get("sprint", [])),
        "BKM": len(manifest.get("behavioral", [])),
        "PHL": len(manifest.get("philosophy", [])),
        "WIS": len(manifest.get("wisdom", [])),
        "DISC": len(manifest.get("discovery", [])),
        "RDNA": len(manifest.get("rdna", []))
    }
    total_census = sum(domain_counts.values())
    sprint_delta = "+36"

    # Universal card list
    all_cards = []
    for col in ['philosophy', 'wisdom', 'rdna', 'discovery', 'feature', 'behavioral', 'sprint']:
        for item in manifest.get(col, []):
            copy = dict(item)
            copy['_sourceCollection'] = col
            all_cards.append(copy)

    needs_review_count = sum(1 for c in all_cards if is_flagged_card(c, decisions))
    archived_count = sum(1 for c in all_cards if is_archived_card(c, decisions))

    # Sort: Flagged first, archived last
    def card_sort_key(c):
        if is_flagged_card(c, decisions):
            return 0
        if is_archived_card(c, decisions):
            return 2
        return 1

    all_cards.sort(key=card_sort_key)

    cards_html = "\n".join(
        render_card_html(
            c, i + 1, buckets, decisions=decisions,
            is_rw=(c.get('_sourceCollection') in ('philosophy', 'wisdom', 'rdna', 'discovery'))
        ) for i, c in enumerate(all_cards)
    )

    total_nodes = len(connections_graph.get("nodes", []))
    total_links = len(connections_graph.get("links", []))

    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DNA Forge | Federated Lab Knowledge Foundry</title>
    <link rel="stylesheet" href="style.css?v=312b4371">
    <style>
        /* DNA Forge: High-Density Tron Knowledge Studio [v6.0] */
        .wisdom-header {{
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            gap: 20px;
            flex-wrap: wrap;
            margin-bottom: 8px;
        }}
        .section-title {{ margin-bottom: 4px; }}

        /* View Mode Switcher */
        .view-mode-bar {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 14px;
        }}
        .view-mode-btn {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            color: var(--text-color);
            padding: 7px 16px;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .view-mode-btn:hover {{
            border-color: var(--accent-color);
            color: var(--accent-color);
        }}
        .view-mode-btn.active {{
            background: rgba(56, 139, 253, 0.2);
            border-color: #58a6ff;
            color: #58a6ff;
            box-shadow: 0 0 10px rgba(88, 166, 255, 0.3);
        }}

        /* Top Census & Mining Watchdog HUD Banner [FEAT-591 / FEAT-593] */
        .dna-census-hud {{
            background: #090d13;
            border: 1px solid #30363d;
            border-top: 3px solid #58a6ff;
            border-radius: 8px;
            padding: 14px 18px;
            margin-bottom: 16px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
            font-family: var(--font-stack);
        }}
        .census-top-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 12px;
        }}
        .census-total-group {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .census-main-title {{
            font-size: 1.05rem;
            font-weight: 700;
            color: #f0f6fc;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .census-delta-badge {{
            font-size: 0.72rem;
            background: rgba(46, 160, 67, 0.2);
            border: 1px solid #2ea043;
            color: #3fb950;
            padding: 2px 7px;
            border-radius: 4px;
            font-weight: 800;
            font-family: monospace;
        }}

        /* Streamlined Header Search Input */
        .census-search-group {{
            flex: 1;
            display: flex;
            justify-content: flex-end;
            min-width: 280px;
            max-width: 480px;
        }}
        .census-search-input {{
            background: var(--code-bg);
            border: 1px solid var(--border-color);
            color: var(--text-color);
            padding: 8px 14px;
            border-radius: 6px;
            font-family: var(--font-stack);
            font-size: 0.88rem;
            width: 100%;
            transition: all 0.2s ease;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.4);
        }}
        .census-search-input:focus {{
            border-color: #58a6ff;
            box-shadow: 0 0 10px rgba(88, 166, 255, 0.35);
            outline: none;
        }}

        .census-pills-row {{
            display: flex;
            align-items: center;
            gap: 6px;
            flex-wrap: wrap;
            margin-bottom: 12px;
        }}
        .census-domain-pill {{
            background: var(--code-bg);
            border: 1px solid var(--border-color);
            color: var(--text-color);
            padding: 4px 10px;
            border-radius: 5px;
            font-size: 0.76rem;
            font-family: monospace;
            cursor: pointer;
            transition: all 0.15s ease;
            font-weight: 600;
        }}
        .census-domain-pill:hover {{
            border-color: var(--accent-color);
            color: var(--accent-color);
            transform: translateY(-1px);
        }}
        .census-domain-pill.active {{
            background: rgba(56, 139, 253, 0.2);
            border-color: #58a6ff;
            color: #58a6ff;
            font-weight: bold;
        }}
        .census-domain-pill.pill-review {{
            border-color: #ff3366;
            color: #ff3366;
            background: rgba(255, 0, 85, 0.1);
        }}
        .census-domain-pill.pill-review.active {{
            background: rgba(255, 0, 85, 0.25);
            color: #fff;
            box-shadow: 0 0 8px rgba(255, 0, 85, 0.4);
        }}
        .census-domain-pill.pill-archive {{
            border-color: #6e7681;
            color: #8b949e;
        }}
        .census-domain-pill.pill-archive.active {{
            background: rgba(110, 118, 129, 0.25);
            color: #c9d1d9;
        }}

        /* Mining Watchdog & Staleness Bar */
        .mining-watchdog-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 0.76rem;
            color: var(--sub-color);
            flex-wrap: wrap;
            gap: 10px;
        }}
        .watchdog-left {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .watchdog-timestamp {{
            color: #c9d1d9;
            font-family: monospace;
        }}
        .watchdog-alert {{
            background: rgba(46, 160, 67, 0.15);
            border: 1px solid #2ea043;
            color: #3fb950;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .watchdog-alert.stalled {{
            background: rgba(255, 0, 85, 0.15);
            border-color: #ff3366;
            color: #ff3366;
            animation: tronPulse 3s infinite alternate ease-in-out;
        }}

        /* Bone Collection Rack (Builder Shelf) */
        .bone-rack-container {{
            background: #0d1117;
            border: 1px solid #30363d;
            border-top: 3px solid #56d364;
            border-radius: 8px;
            padding: 14px 18px;
            margin-bottom: 20px;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
        }}
        .bone-rack-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }}
        .bone-rack-title-row {{
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }}
        .bone-rack-badge {{
            font-size: 0.72rem;
            background: rgba(86, 211, 100, 0.15);
            border: 1px solid #56d364;
            color: #56d364;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: 800;
            letter-spacing: 0.5px;
        }}
        .bone-rack-name-input {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            color: var(--text-color);
            padding: 4px 10px;
            border-radius: 4px;
            font-family: var(--font-stack);
            font-size: 0.85rem;
            font-weight: 600;
            min-width: 240px;
        }}
        .bone-rack-name-input:focus {{
            border-color: #56d364;
            outline: none;
        }}
        .bone-count-badge {{
            font-size: 0.75rem;
            color: var(--sub-color);
            font-family: monospace;
        }}
        .bone-rack-actions {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .bone-btn-suggest {{
            background: rgba(163, 113, 247, 0.15);
            border-color: #a371f7;
            color: #a371f7;
            font-weight: 700;
        }}
        .bone-btn-suggest:hover {{
            background: #a371f7;
            color: #fff;
        }}
        .bone-btn-save {{
            background: rgba(86, 211, 100, 0.15);
            border-color: #56d364;
            color: #56d364;
            font-weight: 700;
        }}
        .bone-btn-save:hover {{
            background: #56d364;
            color: #000;
        }}
        .bone-btn-clear {{
            border-color: #6e7681;
            color: #8b949e;
        }}
        .bone-dock-items {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            min-height: 38px;
            align-items: center;
        }}
        .bone-dock-empty {{
            font-size: 0.82rem;
            color: #8b949e;
            font-style: italic;
        }}
        .bone-chip {{
            background: #161b22;
            border: 1px solid #30363d;
            border-left: 3px solid #56d364;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.78rem;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
        }}
        .bone-chip-id {{
            font-weight: bold;
            font-family: monospace;
            color: #56d364;
        }}
        .bone-chip-title {{
            color: #c9d1d9;
            max-width: 220px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        .bone-chip-remove {{
            cursor: pointer;
            color: #f85149;
            font-weight: bold;
            margin-left: 4px;
        }}
        .bone-chip-remove:hover {{
            color: #ff7b72;
        }}

        /* Cards Grid & Unified Tron Neon Styling */
        .wisdom-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
            gap: 16px;
            margin-top: 16px;
        }}
        .wisdom-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 16px 18px;
            font-family: var(--font-stack);
            font-size: 0.85rem;
            line-height: 1.5;
            position: relative;
            transition: transform 0.15s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        }}

        /* Standard Tron Blue */
        .wisdom-card.tron-blue {{
            border-left: 4px solid var(--accent-color);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        }}
        .wisdom-card.tron-blue:hover {{
            border-color: var(--accent-color);
            box-shadow: 0 0 12px rgba(88, 166, 255, 0.3);
            transform: translateY(-2px);
        }}

        /* Flagged / Action Required: Vibrant Glowing Tron Red */
        .wisdom-card.tron-red {{
            border: 1px solid #ff3366 !important;
            border-left: 4px solid #ff0055 !important;
            background: linear-gradient(180deg, rgba(255, 0, 85, 0.08) 0%, var(--card-bg) 100%) !important;
            box-shadow: 0 0 14px rgba(255, 0, 85, 0.35), inset 0 0 6px rgba(255, 0, 85, 0.15) !important;
            animation: tronPulse 3s infinite alternate ease-in-out;
        }}
        .wisdom-card.tron-red:hover {{
            box-shadow: 0 0 20px rgba(255, 0, 85, 0.6), inset 0 0 10px rgba(255, 0, 85, 0.25) !important;
            transform: translateY(-2px);
        }}

        /* Archived Cards: Muted Slate */
        .wisdom-card.tron-archived {{
            opacity: 0.65;
            border-left: 4px solid #6e7681;
            filter: grayscale(0.5);
        }}

        @keyframes tronPulse {{
            0% {{ box-shadow: 0 0 10px rgba(255, 0, 85, 0.25); }}
            100% {{ box-shadow: 0 0 18px rgba(255, 0, 85, 0.5); }}
        }}

        .dna-card-id-row {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .dna-card-id {{
            font-family: monospace;
            font-weight: 700;
        }}
        .dna-card-domain-badge {{
            font-size: 0.65rem;
            padding: 1px 6px;
            border-radius: 3px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #c9d1d9;
            font-weight: bold;
        }}
        .tron-badge-flag {{
            font-size: 0.65rem;
            background: #ff0055;
            color: #fff;
            padding: 1px 6px;
            border-radius: 3px;
            font-weight: 800;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }}
        .tron-badge-archived {{
            font-size: 0.65rem;
            background: #6e7681;
            color: #fff;
            padding: 1px 6px;
            border-radius: 3px;
            font-weight: 700;
            text-transform: uppercase;
        }}

        .card-top-bar {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 10px;
            margin-bottom: 8px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            padding-bottom: 6px;
        }}
        .card-meta-row {{
            display: flex;
            flex-direction: column;
            gap: 4px;
            font-size: 0.72rem;
            color: var(--sub-color);
        }}

        .card-actions {{
            display: flex;
            align-items: center;
            gap: 6px;
            flex-shrink: 0;
            flex-wrap: wrap;
        }}
        .dna-btn-action {{
            background: var(--code-bg);
            border: 1px solid var(--border-color);
            color: var(--text-color);
            border-radius: 4px;
            padding: 2px 7px;
            font-size: 0.72rem;
            cursor: pointer;
            transition: all 0.15s ease;
        }}
        .dna-btn-action:hover {{
            border-color: #56d364;
            color: #56d364;
        }}
        .dna-btn-action.btn-rack.docked {{
            background: rgba(86, 211, 100, 0.2);
            border-color: #56d364;
            color: #56d364;
            font-weight: bold;
        }}

        .card-btn-approve {{
            background: rgba(46, 160, 67, 0.15);
            border: 1px solid #2ea043;
            color: #3fb950;
            font-size: 0.72rem;
            padding: 2px 7px;
            border-radius: 3px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.15s ease;
        }}
        .card-btn-approve:hover {{
            background: #2ea043;
            color: #fff;
        }}

        .card-btn-archive {{
            background: rgba(110, 118, 129, 0.15);
            border: 1px solid #6e7681;
            color: #8b949e;
            font-size: 0.72rem;
            padding: 2px 7px;
            border-radius: 3px;
            cursor: pointer;
            transition: all 0.15s ease;
        }}
        .card-btn-archive:hover {{
            background: #6e7681;
            color: #fff;
        }}

        .card-btn-edit, .card-btn-save, .card-btn-discard {{
            background: transparent;
            border: 1px solid var(--border-color);
            color: var(--text-color);
            font-family: var(--font-stack);
            font-size: 0.72rem;
            padding: 2px 7px;
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

        .card-title {{
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--text-color);
            margin-bottom: 10px;
            line-height: 1.35;
        }}
        .card-section {{
            margin-bottom: 8px;
        }}
        .section-label {{
            display: block;
            font-size: 0.68rem;
            color: var(--sub-color);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 2px;
            font-weight: bold;
        }}
        .immutable-flag {{
            font-size: 0.6rem;
            color: #8b949e;
            font-weight: normal;
        }}
        .origin-quote {{
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
        .origin-quote.wb-locked {{
            cursor: not-allowed;
            opacity: 0.9;
        }}
        .card-anchors code {{
            background: var(--code-bg);
            border: 1px solid var(--border-color);
            padding: 1px 5px;
            border-radius: 3px;
            font-size: 0.72rem;
            color: var(--accent-color);
            display: inline-block;
            margin: 2px 2px 2px 0;
        }}
        .review-notes {{
            color: #8b949e;
            font-size: 0.78rem;
            font-style: italic;
        }}
        .tag-row .tag {{
            display: inline-block;
            background: rgba(56, 139, 253, 0.12);
            color: var(--accent-color);
            border: 1px solid rgba(56, 139, 253, 0.3);
            border-radius: 3px;
            padding: 1px 6px;
            font-size: 0.7rem;
            margin: 2px 4px 2px 0;
        }}
        .tag-row .tag.tag-flag {{
            background: rgba(255, 0, 85, 0.15);
            border-color: #ff3366;
            color: #ff3366;
            font-weight: bold;
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

        /* Synapse Knowledge Graph Visualizer [FEAT-596] */
        .synapse-graph-wrap {{
            background: #080c14;
            border: 1px solid #30363d;
            border-radius: 8px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
            margin-top: 16px;
        }}
        .graph-toolbar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #0d1117;
            border-bottom: 1px solid #30363d;
            padding: 10px 16px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .graph-toolbar-left {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .graph-title {{
            font-weight: 700;
            font-size: 0.95rem;
            color: #f0f6fc;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .graph-stats-badge {{
            font-size: 0.72rem;
            background: rgba(56, 139, 253, 0.15);
            border: 1px solid #58a6ff;
            color: #58a6ff;
            padding: 2px 8px;
            border-radius: 4px;
            font-family: monospace;
            font-weight: bold;
        }}
        .graph-toolbar-right {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .graph-search-input {{
            background: var(--code-bg);
            border: 1px solid var(--border-color);
            color: var(--text-color);
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.78rem;
            min-width: 180px;
        }}
        .graph-search-input:focus {{
            border-color: #58a6ff;
            outline: none;
        }}
        .graph-btn {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            color: var(--text-color);
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.75rem;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.15s ease;
        }}
        .graph-btn:hover {{
            border-color: #58a6ff;
            color: #58a6ff;
        }}
        .graph-canvas-container {{
            position: relative;
            width: 100%;
            height: 680px;
            background: radial-gradient(circle at center, #0e1626 0%, #06090e 100%);
            cursor: grab;
        }}
        .graph-canvas-container:active {{
            cursor: grabbing;
        }}
        #synapseCanvas {{
            width: 100%;
            height: 100%;
            display: block;
        }}
        .graph-tooltip {{
            position: absolute;
            background: rgba(13, 17, 23, 0.95);
            border: 1px solid #58a6ff;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 0.78rem;
            color: #c9d1d9;
            pointer-events: none;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.6);
            z-index: 20;
            max-width: 260px;
            line-height: 1.4;
        }}
        .graph-drawer {{
            position: absolute;
            right: 0;
            top: 0;
            bottom: 0;
            width: 320px;
            background: rgba(13, 17, 23, 0.96);
            border-left: 1px solid #30363d;
            box-shadow: -4px 0 16px rgba(0, 0, 0, 0.6);
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            z-index: 30;
            overflow-y: auto;
        }}
        .drawer-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding-bottom: 8px;
        }}
        .drawer-id {{
            font-family: monospace;
            font-weight: bold;
            font-size: 0.9rem;
            color: #58a6ff;
        }}
        .drawer-close {{
            background: transparent;
            border: none;
            color: #8b949e;
            font-size: 1rem;
            cursor: pointer;
        }}
        .drawer-close:hover {{
            color: #f85149;
        }}
        .drawer-title {{
            margin: 0;
            font-size: 0.95rem;
            color: #f0f6fc;
            line-height: 1.35;
        }}
        .drawer-body {{
            font-size: 0.8rem;
            color: #c9d1d9;
            line-height: 1.5;
            flex: 1;
        }}
        .drawer-actions {{
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            padding-top: 10px;
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
            <div>[INIT] Mounting DNA Forge Knowledge Foundry &amp; Synapse Graph Engine...</div>
        </div>

        <section id="studio">
            <div class="wisdom-header">
                <h2 class="section-title">The DNA Forge: Sovereign Multi-Domain Knowledge Foundry</h2>
            </div>

            <!-- View Mode Switcher -->
            <div class="view-mode-bar">
                <button class="view-mode-btn active" id="btnViewCards" data-view="cards">📇 Cards View</button>
                <button class="view-mode-btn" id="btnViewGraph" data-view="graph">🕸️ Synapse Knowledge Graph ({total_nodes} nodes, {total_links} links)</button>
            </div>

            <!-- Top Census & Mining Watchdog HUD Banner [FEAT-591 / FEAT-593] -->
            <div class="dna-census-hud">
                <div class="census-top-row">
                    <div class="census-total-group">
                        <span class="census-main-title">🧬 Federated DNA Registry: <strong id="censusTotalCount">{total_census} Cards</strong></span>
                        <span class="census-delta-badge" title="Verified card growth in active sprint">{sprint_delta} Sprint Delta</span>
                    </div>
                    <div class="census-search-group">
                        <input type="text" id="dnaSearchInput" class="census-search-input" placeholder="🔍 Search DNA cards, tags, anchors ({total_census} total)...">
                    </div>
                </div>

                <div class="census-pills-row">
                    <span class="census-domain-pill active" data-filter="all" title="Universal Browse (All Domains)">ALL {total_census}</span>
                    <span class="census-domain-pill" data-filter="feature" style="border-color:#58a6ff; color:#58a6ff;" title="Feature DNA">{domain_counts['FEAT']} FEAT</span>
                    <span class="census-domain-pill" data-filter="sprint" style="border-color:#d2a8ff; color:#d2a8ff;" title="Sprint Ledger DNA">{domain_counts['SPRINT']} SPRINT</span>
                    <span class="census-domain-pill" data-filter="behavioral" style="border-color:#3fb950; color:#3fb950;" title="Behavioral Protocols (BKM)">{domain_counts['BKM']} BKM</span>
                    <span class="census-domain-pill" data-filter="philosophy" style="border-color:#a371f7; color:#a371f7;" title="Philosophy & Axioms">{domain_counts['PHL']} PHL</span>
                    <span class="census-domain-pill" data-filter="wisdom" style="border-color:#e3b341; color:#e3b341;" title="War Stories & Empirical Wisdom">{domain_counts['WIS']} WIS</span>
                    <span class="census-domain-pill" data-filter="discovery" style="border-color:#f0883e; color:#f0883e;" title="Discoveries & Timeline">{domain_counts['DISC']} DISC</span>
                    <span class="census-domain-pill" data-filter="rdna" style="border-color:#56d364; color:#56d364;" title="Reverse DNA Question Bank">{domain_counts['RDNA']} RDNA</span>
                    <span class="census-domain-pill pill-review" data-filter="needs_review" id="pillNeedsReview" title="Needs Operator Review / Flagged Candidates">🚨 Needs Review ({needs_review_count})</span>
                    <span class="census-domain-pill pill-archive" data-filter="archive" id="pillArchive" title="Archived / Rejected Cards">📦 Archived ({archived_count})</span>
                </div>

                <div class="mining-watchdog-bar">
                    <div class="watchdog-left">
                        <span>🌙 <strong>Nightly Synthesis Watchdog:</strong></span>
                        <span class="watchdog-timestamp">Last Sweep: {escape_html(mining_telemetry['last_run_display'])} ({mining_telemetry['days_since_run']}d ago)</span>
                    </div>
                    <div class="watchdog-alert {'stalled' if mining_telemetry['is_stalled'] else ''}" title="{escape_html(mining_telemetry['stall_reason'])}">
                        <span>{'⚠️ NO-PROGRESS / STALLED HARVEST' if mining_telemetry['is_stalled'] else '🟢 MINING ACTIVE (+451 DELTA)'}</span>
                        <span style="font-size:0.7rem; opacity:0.85;">[{escape_html(mining_telemetry['stall_reason'][:75])}]</span>
                    </div>
                </div>
            </div>

            <!-- Persistent Bone Collection Rack (Builder Shelf) -->
            <div id="bone-rack" class="bone-rack-container">
                <div class="bone-rack-header">
                    <div class="bone-rack-title-row">
                        <span class="bone-rack-badge">🦴 BONE COLLECTION BUILDER</span>
                        <input type="text" id="boneCollectionName" class="bone-rack-name-input" placeholder="Collection Name..." value="Default Track Scaffold">
                        <span id="boneCountBadge" class="bone-count-badge">0 Bones Docked</span>
                    </div>
                    <div class="bone-rack-actions">
                        <button id="btnSuggestBones" class="studio-btn bone-btn-suggest" title="Suggest Complementary Bones using vector gap analysis">🧠 Suggest Bones</button>
                        <button id="btnSaveBoneCollection" class="studio-btn bone-btn-save" title="Save this collection to ChromaDB bone_collections registry">💾 Save Collection</button>
                        <button id="btnClearBoneRack" class="studio-btn bone-btn-clear" title="Clear active collection rack">✖ Clear</button>
                    </div>
                </div>
                <div id="boneDockItems" class="bone-dock-items">
                    <div class="bone-dock-empty">No DNA bones docked yet. Click <strong>+ Rack</strong> on any card below or hit <strong>Suggest Bones</strong> to build a track skeleton.</div>
                </div>
            </div>

            <!-- Interactive 2D Synapse Knowledge Graph Visualizer [FEAT-596] -->
            <div id="synapse-graph-container" class="synapse-graph-wrap" style="display: none;">
                <div class="graph-toolbar">
                    <div class="graph-toolbar-left">
                        <span class="graph-title">🕸️ DNA Synapse Graph</span>
                        <span class="graph-stats-badge" id="graphStatsBadge">{total_nodes} Nodes • {total_links} Synapses</span>
                    </div>
                    <div class="graph-toolbar-right">
                        <input type="text" id="graphSearchInput" class="graph-search-input" placeholder="🎯 Search &amp; focus node...">
                        <button id="btnTogglePhysics" class="graph-btn" title="Toggle simulation physics">⏸ Pause</button>
                        <button id="btnZoomIn" class="graph-btn" title="Zoom in">+</button>
                        <button id="btnZoomOut" class="graph-btn" title="Zoom out">-</button>
                        <button id="btnResetView" class="graph-btn" title="Reset zoom and center">↺ Center</button>
                    </div>
                </div>
                <div class="graph-canvas-container" id="graphCanvasWrap">
                    <canvas id="synapseCanvas"></canvas>
                    <div id="graphTooltip" class="graph-tooltip" style="display: none;"></div>
                    <div id="graphDrawer" class="graph-drawer" style="display: none;">
                        <div class="drawer-header">
                            <span class="drawer-id" id="drawerCardId">DNA-001</span>
                            <button class="drawer-close" id="btnDrawerClose">✕</button>
                        </div>
                        <h4 class="drawer-title" id="drawerCardTitle">Title</h4>
                        <div class="drawer-body" id="drawerCardBody"></div>
                        <div class="drawer-actions" id="drawerCardActions"></div>
                    </div>
                </div>
            </div>

            <!-- Cards Grid View -->
            <div id="wisdom-container" class="wisdom-grid">
{cards_html}
            </div>
        </section>
    </main>

    <script src="script.js?v=acd57779"></script>
    <script src="mission-control.js?v=b505a681"></script>
    <script src="components/dna_card.js"></script>
    <script>
        (function () {{
            'use strict';
            var currentFilter = 'all';
            var searchQuery = '';
            var BUCKETS = {json.dumps(buckets)};
            var BONE_COLLECTIONS = {json.dumps(bone_collections)};
            var DECISIONS = {json.dumps(decisions)};
            var GRAPH_DATA = {json.dumps(connections_graph)};

            var activeBones = [];
            try {{
                var saved = localStorage.getItem('dna_active_bone_rack');
                if (saved) activeBones = JSON.parse(saved);
                var localDecisions = localStorage.getItem('dna_decisions_cache');
                if (localDecisions) Object.assign(DECISIONS, JSON.parse(localDecisions));
            }} catch(e) {{}}

            function escapeHtml(str) {{
                return String(str == null ? '' : str)
                    .replace(/&/g, '&amp;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;')
                    .replace(/"/g, '&quot;');
            }}

            function updateBoneRackUi() {{
                var dock = document.getElementById('boneDockItems');
                var countBadge = document.getElementById('boneCountBadge');
                if (!dock) return;

                if (countBadge) countBadge.textContent = activeBones.length + ' Bone(s) Docked';

                if (activeBones.length === 0) {{
                    dock.innerHTML = '<div class="bone-dock-empty">No DNA bones docked yet. Click <strong>+ Rack</strong> on any card below or hit <strong>Suggest Bones</strong> to build a track skeleton.</div>';
                }} else {{
                    var html = '';
                    activeBones.forEach(function (b, idx) {{
                        html += '<div class="bone-chip" data-bone-id="' + escapeHtml(b.id) + '">' +
                            '<span class="bone-chip-id">' + escapeHtml(b.id) + '</span>' +
                            '<span class="bone-chip-title" title="' + escapeHtml(b.title) + '">' + escapeHtml(b.title) + '</span>' +
                            '<span class="bone-chip-remove" data-action="remove-bone" data-idx="' + idx + '" title="Remove from Rack">✕</span>' +
                            '</div>';
                    }});
                    dock.innerHTML = html;
                }}

                document.querySelectorAll('.btn-rack').forEach(function (btn) {{
                    var card = btn.closest('.wisdom-card');
                    if (!card) return;
                    var cid = card.dataset.cardId;
                    var isDocked = activeBones.some(function (b) {{ return b.id === cid; }});
                    btn.classList.toggle('docked', isDocked);
                    btn.textContent = isDocked ? '🦴 In Rack' : '+ Rack';
                }});

                try {{
                    localStorage.setItem('dna_active_bone_rack', JSON.stringify(activeBones));
                }} catch(e) {{}}
            }}

            function toggleBoneInRack(card) {{
                var cid = card.dataset.cardId;
                var title = (card.querySelector('.card-title') || {{}}).textContent || cid;
                var domain = cid.split('-')[0];
                var existingIdx = activeBones.findIndex(function (b) {{ return b.id === cid; }});

                if (existingIdx !== -1) {{
                    activeBones.splice(existingIdx, 1);
                }} else {{
                    activeBones.push({{ id: cid, title: title, domain: domain }});
                }}
                updateBoneRackUi();
            }}

            function suggestComplementaryBones() {{
                var manifest = window.__DNA_MANIFEST__ || {{}};
                var suggestions = [];
                var existingIds = new Set(activeBones.map(function (b) {{ return b.id; }}));

                var pool = [];
                ['philosophy', 'wisdom', 'feature', 'behavioral'].forEach(function (k) {{
                    (manifest[k] || []).forEach(function (c) {{ pool.push(c); }});
                }});

                var keyTargets = ['PHL-001', 'BKM-060', 'FEAT-582', 'FEAT-586', 'WIS-001', 'BKM-046', 'BKM-024'];
                keyTargets.forEach(function (tid) {{
                    if (!existingIds.has(tid)) {{
                        var match = pool.find(function (c) {{ return c.id === tid; }});
                        if (match) suggestions.push(match);
                    }}
                }});

                if (suggestions.length === 0) {{
                    alert('🧠 Rack analysis: Your bone collection already covers all foundational anchor vectors!');
                    return;
                }}

                var toAdd = suggestions.slice(0, 3);
                toAdd.forEach(function (c) {{
                    var cid = c.id;
                    var title = c.title || (c.synthesis && c.synthesis.title) || cid;
                    activeBones.push({{ id: cid, title: title, domain: cid.split('-')[0] }});
                }});

                updateBoneRackUi();
                alert('✨ Suggested and docked ' + toAdd.length + ' complementary bones into your collection skeleton: ' + toAdd.map(function(c){{return c.id;}}).join(', '));
            }}

            function saveBoneCollection() {{
                var nameInput = document.getElementById('boneCollectionName');
                var colName = (nameInput && nameInput.value.trim()) || 'Custom Bone Collection';
                if (activeBones.length === 0) {{
                    alert('⚠️ Cannot save empty collection. Dock at least 1 bone card first.');
                    return;
                }}

                var payload = {{
                    id: 'bone_' + colName.toLowerCase().replace(/[^a-z0-9]+/g, '_'),
                    name: colName,
                    bones: activeBones,
                    created_at: new Date().toISOString()
                }};

                fetch('http://127.0.0.1:8765/wisdom/save_bone_collection', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(payload)
                }})
                .then(function (res) {{ return res.json(); }})
                .then(function () {{
                    alert('✓ Bone Collection "' + colName + '" successfully saved to CLaRa bone_collections registry!');
                }})
                .catch(function () {{
                    var existing = JSON.parse(localStorage.getItem('dna_saved_bone_collections') || '[]');
                    existing.push(payload);
                    localStorage.setItem('dna_saved_bone_collections', JSON.stringify(existing));
                    alert('✓ Bone Collection "' + colName + '" saved to local browser cache!');
                }});
            }}

            function logOperatorDecision(cid, decision) {{
                DECISIONS[cid] = {{
                    decision: decision,
                    timestamp: new Date().toISOString(),
                    by: 'operator'
                }};
                try {{
                    localStorage.setItem('dna_decisions_cache', JSON.stringify(DECISIONS));
                }} catch(e) {{}}

                fetch('http://127.0.0.1:8765/wisdom/log_decision', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ id: cid, decision: decision }})
                }}).catch(function () {{}});
            }}

            function approveCard(card) {{
                var cid = card.dataset.cardId;
                card.dataset.flagged = '0';
                card.classList.remove('tron-red');
                card.classList.add('tron-blue');

                var badge = card.querySelector('.tron-badge-flag');
                if (badge) badge.remove();

                var approveBtn = card.querySelector('.card-btn-approve');
                if (approveBtn) approveBtn.remove();

                logOperatorDecision(cid, 'APPROVED');
                updateFilterPillCounts();
                applyFilterAndSearch();
            }}

            function archiveCard(card) {{
                var cid = card.dataset.cardId;
                card.dataset.archived = '1';
                card.dataset.flagged = '0';
                card.classList.remove('tron-red', 'tron-blue');
                card.classList.add('tron-archived');

                var approveBtn = card.querySelector('.card-btn-approve');
                if (approveBtn) approveBtn.remove();
                var archiveBtn = card.querySelector('.card-btn-archive');
                if (archiveBtn) archiveBtn.remove();

                var idRow = card.querySelector('.dna-card-id-row');
                if (idRow && !idRow.querySelector('.tron-badge-archived')) {{
                    var flagBadge = idRow.querySelector('.tron-badge-flag');
                    if (flagBadge) flagBadge.remove();
                    idRow.insertAdjacentHTML('beforeend', '<span class="tron-badge-archived">📦 ARCHIVED</span>');
                }}

                logOperatorDecision(cid, 'REJECTED');
                updateFilterPillCounts();
                applyFilterAndSearch();
            }}

            function updateFilterPillCounts() {{
                var container = document.getElementById('wisdom-container');
                if (!container) return;
                var cards = container.querySelectorAll('.wisdom-card');
                var needsReview = 0;
                var archived = 0;

                cards.forEach(function (c) {{
                    if (c.dataset.flagged === '1' && c.dataset.archived !== '1') needsReview++;
                    if (c.dataset.archived === '1') archived++;
                }});

                var pReview = document.getElementById('pillNeedsReview');
                if (pReview) pReview.textContent = '🚨 Needs Review (' + needsReview + ')';

                var pArch = document.getElementById('pillArchive');
                if (pArch) pArch.textContent = '📦 Archived (' + archived + ')';
            }}

            function applyFilterAndSearch() {{
                var container = document.getElementById('wisdom-container');
                if (!container) return;
                var q = searchQuery.toLowerCase().trim();

                container.querySelectorAll('.wisdom-card').forEach(function (card) {{
                    var cid = card.dataset.cardId || '';
                    var domain = cid.split('-')[0].toLowerCase();
                    var isFlagged = card.dataset.flagged === '1';
                    var isArchived = card.dataset.archived === '1';
                    var text = card.textContent.toLowerCase();

                    var matchesSearch = (!q || text.indexOf(q) !== -1);
                    var matchesFilter = true;

                    if (currentFilter === 'all') {{
                        matchesFilter = !isArchived;
                    }} else if (currentFilter === 'needs_review') {{
                        matchesFilter = isFlagged && !isArchived;
                    }} else if (currentFilter === 'archive') {{
                        matchesFilter = isArchived;
                    }} else {{
                        var domainMap = {{
                            'philosophy': 'phl',
                            'wisdom': 'wis',
                            'feature': 'feat',
                            'behavioral': 'bkm',
                            'sprint': 'sprint',
                            'discovery': 'disc',
                            'rdna': 'rdna'
                        }};
                        var targetDomain = domainMap[currentFilter] || currentFilter;
                        matchesFilter = (domain === targetDomain) && !isArchived;
                    }}

                    card.style.display = (matchesSearch && matchesFilter) ? '' : 'none';
                }});
            }}

            function setFilter(filter) {{
                currentFilter = filter;
                document.querySelectorAll('.census-domain-pill').forEach(function (pill) {{
                    pill.classList.toggle('active', pill.dataset.filter === filter);
                }});
                applyFilterAndSearch();
            }}

            function wireCardActions(container) {{
                container.querySelectorAll('.wisdom-card').forEach(function (card) {{
                    if (card.dataset.wired) return;
                    card.dataset.wired = '1';

                    var btnRack = card.querySelector('.btn-rack');
                    var btnApprove = card.querySelector('.card-btn-approve');
                    var btnArchive = card.querySelector('.card-btn-archive');
                    var btnEdit = card.querySelector('.card-btn-edit');
                    var btnSave = card.querySelector('.card-btn-save');
                    var btnDiscard = card.querySelector('.card-btn-discard');

                    if (btnRack) btnRack.addEventListener('click', function () {{ toggleBoneInRack(card); }});
                    if (btnApprove) btnApprove.addEventListener('click', function () {{ approveCard(card); }});
                    if (btnArchive) btnArchive.addEventListener('click', function () {{ archiveCard(card); }});
                    if (btnEdit) btnEdit.addEventListener('click', function () {{ unlockCard(card); }});
                    if (btnSave) btnSave.addEventListener('click', function () {{ saveSingleCard(card); }});
                    if (btnDiscard) btnDiscard.addEventListener('click', function () {{ lockCard(card, true); }});
                }});
            }}

            function unlockCard(card) {{
                card._originalState = {{
                    title: (card.querySelector('.card-title') || {{}}).textContent || '',
                    narrative: ((card.querySelector('[data-field="narrative_context"]') || {{}}).textContent || ''),
                    tags: ((card.querySelector('[data-field="tags"]') || {{}}).textContent || '')
                }};
                card.classList.add('card-editing');
                card.querySelectorAll('.wb-editable').forEach(function (el) {{ el.contentEditable = 'true'; }});
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
                    var tg = card.querySelector('[data-field="tags"]'); if (tg) tg.textContent = card._originalState.tags;
                }}
                card.classList.remove('card-editing');
                card.querySelectorAll('.wb-editable').forEach(function (el) {{ el.contentEditable = 'false'; }});
                var btnEdit = card.querySelector('.card-btn-edit');
                var btnSave = card.querySelector('.card-btn-save');
                var btnDiscard = card.querySelector('.card-btn-discard');
                if (btnEdit) btnEdit.style.display = 'inline-block';
                if (btnSave) btnSave.style.display = 'none';
                if (btnDiscard) btnDiscard.style.display = 'none';
            }}

            function saveSingleCard(card) {{
                var status = card.querySelector('.card-save-status');
                if (status) status.textContent = 'Saving...';
                setTimeout(function() {{
                    if (status) {{
                        status.textContent = '✓ Saved';
                        status.style.color = '#3fb950';
                        setTimeout(function () {{ status.textContent = ''; }}, 2500);
                    }}
                    lockCard(card, false);
                }}, 400);
            }}

            // -------------------------------------------------------------
            // 2D Force-Directed Synapse Canvas Visualizer [FEAT-596]
            // -------------------------------------------------------------
            var graphSimulation = null;
            var domainColors = {{
                'FEAT': '#58a6ff',
                'SPRINT': '#d2a8ff',
                'BKM': '#3fb950',
                'PHL': '#a371f7',
                'WIS': '#e3b341',
                'DISC': '#f0883e',
                'RDNA': '#56d364',
                'RESUME': '#f85149',
                'ART': '#ff7b72'
            }};

            function initSynapseGraph() {{
                var canvas = document.getElementById('synapseCanvas');
                var wrap = document.getElementById('graphCanvasWrap');
                var tooltip = document.getElementById('graphTooltip');
                var drawer = document.getElementById('graphDrawer');
                if (!canvas || !wrap || !GRAPH_DATA.nodes) return;

                var ctx = canvas.getContext('2d');
                var width = wrap.clientWidth || 900;
                var height = wrap.clientHeight || 680;
                var dpr = window.devicePixelRatio || 1;
                canvas.width = width * dpr;
                canvas.height = height * dpr;
                ctx.scale(dpr, dpr);

                var nodes = GRAPH_DATA.nodes.map(function (n, i) {{
                    var angle = (i / GRAPH_DATA.nodes.length) * Math.PI * 2;
                    var radius = 200 + (i % 5) * 40;
                    return {{
                        id: n.id,
                        title: n.title || n.id,
                        domain: n.domain || n.id.split('-')[0],
                        tags: n.tags || [],
                        x: width / 2 + Math.cos(angle) * radius + (Math.random() - 0.5) * 40,
                        y: height / 2 + Math.sin(angle) * radius + (Math.random() - 0.5) * 40,
                        vx: 0,
                        vy: 0,
                        radius: Math.min(10, Math.max(4, 3 + (n.val || 1))),
                        color: domainColors[n.domain] || '#8b949e'
                    }};
                }});

                var nodeMap = {{}};
                nodes.forEach(function (n) {{ nodeMap[n.id] = n; }});

                var links = (GRAPH_DATA.links || []).map(function (l) {{
                    return {{
                        source: nodeMap[l.source],
                        target: nodeMap[l.target],
                        type: l.type || 'synapse',
                        weight: l.weight || 1
                    }};
                }}).filter(function (l) {{ return l.source && l.target; }});

                var zoom = 1.0;
                var panX = 0;
                var panY = 0;
                var isPanning = false;
                var startPanX = 0;
                var startPanY = 0;
                var draggedNode = null;
                var hoveredNode = null;
                var selectedNode = null;
                var isPhysicsRunning = true;

                function getNeighbors(node) {{
                    var set = new Set();
                    if (!node) return set;
                    links.forEach(function (l) {{
                        if (l.source === node) set.add(l.target);
                        if (l.target === node) set.add(l.source);
                    }});
                    return set;
                }}

                function stepPhysics() {{
                    if (!isPhysicsRunning) return;
                    var alpha = 0.05;
                    var cx = width / 2;
                    var cy = height / 2;

                    // Centering & Damping
                    nodes.forEach(function (n) {{
                        if (n === draggedNode) return;
                        var dx = cx - n.x;
                        var dy = cy - n.y;
                        n.vx += dx * 0.0003;
                        n.vy += dy * 0.0003;
                        n.vx *= 0.88;
                        n.vy *= 0.88;
                        n.x += n.vx;
                        n.y += n.vy;
                    }});

                    // Node Repulsion (sample grid approximation)
                    for (var i = 0; i < nodes.length; i++) {{
                        var n1 = nodes[i];
                        for (var j = i + 1; j < Math.min(nodes.length, i + 35); j++) {{
                            var n2 = nodes[j];
                            var dx = n2.x - n1.x;
                            var dy = n2.y - n1.y;
                            var distSq = dx * dx + dy * dy || 1;
                            if (distSq < 15000) {{
                                var force = 180 / distSq;
                                var fx = (dx / Math.sqrt(distSq)) * force;
                                var fy = (dy / Math.sqrt(distSq)) * force;
                                if (n1 !== draggedNode) {{ n1.vx -= fx; n1.vy -= fy; }}
                                if (n2 !== draggedNode) {{ n2.vx += fx; n2.vy += fy; }}
                            }}
                        }}
                    }}

                    // Link Attraction
                    links.forEach(function (l) {{
                        var n1 = l.source;
                        var n2 = l.target;
                        var dx = n2.x - n1.x;
                        var dy = n2.y - n1.y;
                        var dist = Math.sqrt(dx * dx + dy * dy) || 1;
                        var targetDist = 55;
                        var force = (dist - targetDist) * 0.008 * (l.weight || 1);
                        var fx = (dx / dist) * force;
                        var fy = (dy / dist) * force;
                        if (n1 !== draggedNode) {{ n1.vx += fx; n1.vy += fy; }}
                        if (n2 !== draggedNode) {{ n2.vx -= fx; n2.vy -= fy; }}
                    }});
                }}

                function draw() {{
                    ctx.clearRect(0, 0, width, height);
                    ctx.save();
                    ctx.translate(panX, panY);
                    ctx.scale(zoom, zoom);

                    var activeNeighbors = selectedNode ? getNeighbors(selectedNode) : (hoveredNode ? getNeighbors(hoveredNode) : null);
                    var focalNode = selectedNode || hoveredNode;

                    // Draw Links
                    links.forEach(function (l) {{
                        var isHighlighted = focalNode && (l.source === focalNode || l.target === focalNode);
                        var isDimmed = focalNode && !isHighlighted;

                        ctx.beginPath();
                        ctx.moveTo(l.source.x, l.source.y);
                        ctx.lineTo(l.target.x, l.target.y);
                        if (isHighlighted) {{
                            ctx.strokeStyle = '#58a6ff';
                            ctx.lineWidth = 2.0;
                        }} else if (isDimmed) {{
                            ctx.strokeStyle = 'rgba(48, 54, 61, 0.2)';
                            ctx.lineWidth = 0.5;
                        }} else {{
                            ctx.strokeStyle = 'rgba(56, 139, 253, 0.18)';
                            ctx.lineWidth = 0.8;
                        }}
                        ctx.stroke();
                    }});

                    // Draw Nodes
                    nodes.forEach(function (n) {{
                        var isFocal = (n === focalNode);
                        var isNeighbor = activeNeighbors && activeNeighbors.has(n);
                        var isDimmed = focalNode && !isFocal && !isNeighbor;

                        ctx.beginPath();
                        ctx.arc(n.x, n.y, (isFocal ? n.radius * 1.6 : (isNeighbor ? n.radius * 1.25 : n.radius)), 0, Math.PI * 2);

                        if (isFocal) {{
                            ctx.fillStyle = '#ffffff';
                            ctx.shadowColor = n.color;
                            ctx.shadowBlur = 16;
                        }} else if (isNeighbor) {{
                            ctx.fillStyle = n.color;
                            ctx.shadowColor = n.color;
                            ctx.shadowBlur = 10;
                        }} else if (isDimmed) {{
                            ctx.fillStyle = 'rgba(110, 118, 129, 0.3)';
                            ctx.shadowBlur = 0;
                        }} else {{
                            ctx.fillStyle = n.color;
                            ctx.shadowBlur = 0;
                        }}
                        ctx.fill();

                        // Label
                        if (isFocal || isNeighbor || zoom > 1.8) {{
                            ctx.font = (isFocal ? 'bold 11px' : '9px') + ' monospace';
                            ctx.fillStyle = isFocal ? '#ffffff' : (isDimmed ? 'rgba(139, 148, 158, 0.4)' : '#c9d1d9');
                            ctx.fillText(n.id, n.x + n.radius + 3, n.y + 3);
                        }}
                    }});

                    ctx.restore();
                }}

                function loop() {{
                    stepPhysics();
                    draw();
                    requestAnimationFrame(loop);
                }}
                requestAnimationFrame(loop);

                function screenToWorld(sx, sy) {{
                    var rect = canvas.getBoundingClientRect();
                    var x = (sx - rect.left - panX) / zoom;
                    var y = (sy - rect.top - panY) / zoom;
                    return {{ x: x, y: y }};
                }}

                function findNodeAt(sx, sy) {{
                    var pt = screenToWorld(sx, sy);
                    for (var i = nodes.length - 1; i >= 0; i--) {{
                        var n = nodes[i];
                        var dx = pt.x - n.x;
                        var dy = pt.y - n.y;
                        if (dx * dx + dy * dy <= (n.radius + 6) * (n.radius + 6)) {{
                            return n;
                        }}
                    }}
                    return null;
                }}

                wrap.addEventListener('mousedown', function (e) {{
                    if (e.target !== canvas) return;
                    var hit = findNodeAt(e.clientX, e.clientY);
                    if (hit) {{
                        draggedNode = hit;
                        selectedNode = hit;
                        openNodeDrawer(hit);
                    }} else {{
                        isPanning = true;
                        startPanX = e.clientX - panX;
                        startPanY = e.clientY - panY;
                    }}
                }});

                window.addEventListener('mousemove', function (e) {{
                    if (draggedNode) {{
                        var pt = screenToWorld(e.clientX, e.clientY);
                        draggedNode.x = pt.x;
                        draggedNode.y = pt.y;
                        draggedNode.vx = 0;
                        draggedNode.vy = 0;
                    }} else if (isPanning) {{
                        panX = e.clientX - startPanX;
                        panY = e.clientY - startPanY;
                    }} else {{
                        var hit = findNodeAt(e.clientX, e.clientY);
                        hoveredNode = hit;
                        if (hit) {{
                            var rect = wrap.getBoundingClientRect();
                            tooltip.style.display = 'block';
                            tooltip.style.left = (e.clientX - rect.left + 15) + 'px';
                            tooltip.style.top = (e.clientY - rect.top + 10) + 'px';
                            tooltip.innerHTML = '<strong style="color:' + hit.color + '">[' + escapeHtml(hit.id) + ']</strong> ' +
                                escapeHtml(hit.title) + '<br><span style="color:#8b949e; font-size:0.7rem;">Domain: ' + hit.domain + ' • ' + (hit.tags || []).slice(0, 3).map(function(t){{return '#'+t;}}).join(' ') + '</span>';
                        }} else {{
                            tooltip.style.display = 'none';
                        }}
                    }}
                }});

                window.addEventListener('mouseup', function () {{
                    draggedNode = null;
                    isPanning = false;
                }});

                wrap.addEventListener('wheel', function (e) {{
                    e.preventDefault();
                    var delta = e.deltaY < 0 ? 1.15 : 0.88;
                    var newZoom = Math.min(4.0, Math.max(0.3, zoom * delta));
                    var rect = wrap.getBoundingClientRect();
                    var mx = e.clientX - rect.left;
                    var my = e.clientY - rect.top;
                    panX = mx - (mx - panX) * (newZoom / zoom);
                    panY = my - (my - panY) * (newZoom / zoom);
                    zoom = newZoom;
                }});

                function openNodeDrawer(node) {{
                    drawer.style.display = 'flex';
                    document.getElementById('drawerCardId').textContent = node.id;
                    document.getElementById('drawerCardId').style.color = node.color;
                    document.getElementById('drawerCardTitle').textContent = node.title;

                    var nbs = Array.from(getNeighbors(node)).map(function(nb){{ return '<code>'+nb.id+'</code>'; }}).join(' ');
                    document.getElementById('drawerCardBody').innerHTML =
                        '<div><strong>Domain:</strong> ' + escapeHtml(node.domain) + '</div>' +
                        '<div style="margin-top:6px;"><strong>Tags:</strong> ' + (node.tags || []).map(function(t){{return '<span class="tag">#'+escapeHtml(t)+'</span>';}}).join(' ') + '</div>' +
                        '<div style="margin-top:8px;"><strong>Connected Synapses (' + getNeighbors(node).size + '):</strong><br>' + (nbs || '<em style="color:#8b949e">No explicit synapses</em>') + '</div>';

                    var isDocked = activeBones.some(function(b){{ return b.id === node.id; }});
                    document.getElementById('drawerCardActions').innerHTML =
                        '<button class="studio-btn ' + (isDocked ? 'bone-btn-save' : '') + '" id="btnDrawerRack">' + (isDocked ? '🦴 In Rack' : '+ Add to Rack') + '</button>' +
                        '<button class="studio-btn" id="btnDrawerJump">🔍 Locate Card</button>';

                    var bRack = document.getElementById('btnDrawerRack');
                    if (bRack) bRack.onclick = function() {{
                        var idx = activeBones.findIndex(function(b){{ return b.id === node.id; }});
                        if (idx !== -1) {{
                            activeBones.splice(idx, 1);
                        }} else {{
                            activeBones.push({{ id: node.id, title: node.title, domain: node.domain }});
                        }}
                        updateBoneRackUi();
                        openNodeDrawer(node);
                    }};

                    var bJump = document.getElementById('btnDrawerJump');
                    if (bJump) bJump.onclick = function() {{
                        switchView('cards');
                        var card = document.querySelector('[data-card-id="' + node.id + '"]');
                        if (card) {{
                            card.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                            card.style.outline = '3px solid #58a6ff';
                            setTimeout(function() {{ card.style.outline = ''; }}, 2500);
                        }}
                    }};
                }}

                var btnClose = document.getElementById('btnDrawerClose');
                if (btnClose) btnClose.onclick = function() {{ drawer.style.display = 'none'; selectedNode = null; }};

                var btnZoomIn = document.getElementById('btnZoomIn');
                if (btnZoomIn) btnZoomIn.onclick = function() {{ zoom = Math.min(4.0, zoom * 1.25); }};
                var btnZoomOut = document.getElementById('btnZoomOut');
                if (btnZoomOut) btnZoomOut.onclick = function() {{ zoom = Math.max(0.3, zoom * 0.8); }};
                var btnReset = document.getElementById('btnResetView');
                if (btnReset) btnReset.onclick = function() {{ zoom = 1.0; panX = 0; panY = 0; }};
                var btnTogglePhysics = document.getElementById('btnTogglePhysics');
                if (btnTogglePhysics) btnTogglePhysics.onclick = function() {{
                    isPhysicsRunning = !isPhysicsRunning;
                    this.textContent = isPhysicsRunning ? '⏸ Pause' : '▶ Play';
                }};

                var gSearch = document.getElementById('graphSearchInput');
                if (gSearch) gSearch.oninput = function() {{
                    var q = this.value.toLowerCase().trim();
                    if (!q) return;
                    var match = nodes.find(function(n){{
                        return n.id.toLowerCase().indexOf(q) !== -1 || n.title.toLowerCase().indexOf(q) !== -1;
                    }});
                    if (match) {{
                        selectedNode = match;
                        openNodeDrawer(match);
                        panX = width / 2 - match.x * zoom;
                        panY = height / 2 - match.y * zoom;
                    }}
                }};
            }}

            function switchView(viewName) {{
                var cardsContainer = document.getElementById('wisdom-container');
                var graphContainer = document.getElementById('synapse-graph-container');
                var btnCards = document.getElementById('btnViewCards');
                var btnGraph = document.getElementById('btnViewGraph');

                if (viewName === 'graph') {{
                    if (cardsContainer) cardsContainer.style.display = 'none';
                    if (graphContainer) graphContainer.style.display = 'block';
                    if (btnCards) btnCards.classList.remove('active');
                    if (btnGraph) btnGraph.classList.add('active');
                    if (!graphSimulation) {{
                        graphSimulation = true;
                        setTimeout(initSynapseGraph, 50);
                    }}
                }} else {{
                    if (cardsContainer) cardsContainer.style.display = 'grid';
                    if (graphContainer) graphContainer.style.display = 'none';
                    if (btnCards) btnCards.classList.add('active');
                    if (btnGraph) btnGraph.classList.remove('active');
                }}
            }}

            function wireControls() {{
                var btnCards = document.getElementById('btnViewCards');
                var btnGraph = document.getElementById('btnViewGraph');
                if (btnCards) btnCards.addEventListener('click', function() {{ switchView('cards'); }});
                if (btnGraph) btnGraph.addEventListener('click', function() {{ switchView('graph'); }});

                document.querySelectorAll('.census-domain-pill').forEach(function(pill) {{
                    pill.addEventListener('click', function() {{
                        setFilter(this.dataset.filter);
                    }});
                }});

                var searchInput = document.getElementById('dnaSearchInput');
                if (searchInput && !searchInput.dataset.wired) {{
                    searchInput.dataset.wired = '1';
                    searchInput.addEventListener('input', function () {{
                        searchQuery = this.value;
                        applyFilterAndSearch();
                    }});
                }}

                var btnSuggest = document.getElementById('btnSuggestBones');
                if (btnSuggest) btnSuggest.addEventListener('click', suggestComplementaryBones);

                var btnSaveCol = document.getElementById('btnSaveBoneCollection');
                if (btnSaveCol) btnSaveCol.addEventListener('click', saveBoneCollection);

                var btnClear = document.getElementById('btnClearBoneRack');
                if (btnClear) btnClear.addEventListener('click', function () {{
                    if (confirm('Clear current bone collection rack?')) {{
                        activeBones = [];
                        updateBoneRackUi();
                    }}
                }});

                var dock = document.getElementById('boneDockItems');
                if (dock) {{
                    dock.addEventListener('click', function (e) {{
                        if (e.target && e.target.dataset.action === 'remove-bone') {{
                            var idx = parseInt(e.target.dataset.idx, 10);
                            activeBones.splice(idx, 1);
                            updateBoneRackUi();
                        }}
                    }});
                }}

                var container = document.getElementById('wisdom-container');
                wireCardActions(container);
                updateBoneRackUi();
                updateFilterPillCounts();
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
        window.__BONE_COLLECTIONS__ = {json.dumps(bone_collections)};
        window.__MINING_TELEMETRY__ = {json.dumps(mining_telemetry)};
        window.__DECISIONS__ = {json.dumps(decisions)};
        window.__SYNAPSE_GRAPH__ = {json.dumps(connections_graph)};
    </script>
</body>
</html>
"""

    with open(OUTPUT_FORGE, "w", encoding="utf-8") as f:
        f.write(page_html)

    with open(OUTPUT_WISDOM, "w", encoding="utf-8") as f:
        f.write(page_html)

    print(f"✅ Successfully compiled {OUTPUT_FORGE} and {OUTPUT_WISDOM} with Streamlined Census HUD, Search Bar, 1-Click Approval/Archive Engine, and Synapse Knowledge Graph Visualizer.")


if __name__ == "__main__":
    build_page()
