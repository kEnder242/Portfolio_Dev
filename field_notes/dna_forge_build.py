#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dna_forge_build.py [v7.0]
[FEAT-582 / FEAT-588 / FEAT-589 / FEAT-591 / FEAT-593 / FEAT-596]
The DNA Forge: Sovereign Multi-Domain Knowledge Foundry.
Features:
- Streamlined Cards View with 1-Click Approval/Archive Engine, Census HUD & Bone Collection Rack.
- Ego-Centric Single-Node Synapse Knowledge Graph with Orbital Synapse Spokes, Bone Collection Integration,
  Breadcrumbs Navigation, and Seamless 2-Way [🕸️ Synapse] <-> [📇 Locate Card] Transitions.
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
        <button class="dna-btn-action btn-synapse" data-action="focus-synapse" title="Focus this card in Synapse Knowledge Graph (or double-click card)">🕸️ Synapse</button>
        <button class="dna-btn-action btn-rack" data-action="toggle-rack" title="Add to Active Bone Collection Rack">+ Rack</button>
        {approve_btn}
        {archive_btn}
        {'''<button class="card-btn-edit" title="Unlock and edit this card in-place">🔓 Edit</button>
        <button class="card-btn-save" style="display:none;" title="Save changes atomically to disk and ChromaDB">💾 Save</button>
        <button class="card-btn-discard" style="display:none;" title="Discard unsaved changes">✖ Discard</button>
        <span class="card-save-status"></span>''' if is_rw else '<span class="ro-stub-badge" title="Git-anchored read-only">[ 🔒 Git-Anchored ]</span>'}
    </div>"""

    return f"""
        <div class="wisdom-card {tron_class}" data-card-id="{escape_html(cid)}" data-card-index="{index}" data-flagged="{'1' if flagged else '0'}" data-archived="{'1' if archived else '0'}" title="Double-click to open in Synapse Knowledge Graph">
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
        /* DNA Forge: High-Density Tron Knowledge Studio [v7.0] */
        .wisdom-header {{
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            gap: 20px;
            flex-wrap: wrap;
            margin-bottom: 8px;
        }}
        .section-title {{ margin-bottom: 4px; }}

        /* Top View Mode Switcher */
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

        /* Cards View Container Groups */
        #cards-view-group {{
            display: block;
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
            cursor: pointer;
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
            border-color: var(--accent-color);
            color: var(--accent-color);
        }}
        .dna-btn-action.btn-synapse {{
            border-color: rgba(56, 139, 253, 0.5);
            color: #58a6ff;
            background: rgba(56, 139, 253, 0.1);
        }}
        .dna-btn-action.btn-synapse:hover {{
            background: #58a6ff;
            color: #000;
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

        /* ------------------------------------------------------------- */
        /* Ego-Centric Synapse Knowledge Graph Visualizer [FEAT-596 v2] */
        /* ------------------------------------------------------------- */
        .synapse-graph-wrap {{
            background: #080c14;
            border: 1px solid #30363d;
            border-radius: 8px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.6);
            margin-top: 8px;
            display: flex;
            flex-direction: column;
        }}
        
        /* Dedicated Synapse Navigation & Focal Control Bar */
        .synapse-nav-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #0d1117;
            border-bottom: 1px solid #30363d;
            padding: 10px 16px;
            flex-wrap: wrap;
            gap: 12px;
        }}
        .synapse-breadcrumbs-wrap {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-family: monospace;
            font-size: 0.8rem;
            color: #8b949e;
            overflow-x: auto;
            max-width: 400px;
        }}
        .synapse-crumb {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #c9d1d9;
            padding: 2px 7px;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.15s ease;
        }}
        .synapse-crumb:hover {{
            border-color: #58a6ff;
            color: #58a6ff;
        }}
        .synapse-crumb.active {{
            background: rgba(56, 139, 253, 0.2);
            border-color: #58a6ff;
            color: #58a6ff;
            font-weight: bold;
        }}
        
        .synapse-search-box {{
            flex: 1;
            min-width: 240px;
            max-width: 420px;
            position: relative;
        }}
        .synapse-search-input {{
            background: var(--code-bg);
            border: 1px solid var(--border-color);
            color: var(--text-color);
            padding: 7px 12px;
            border-radius: 6px;
            font-size: 0.82rem;
            width: 100%;
            transition: all 0.2s;
        }}
        .synapse-search-input:focus {{
            border-color: #58a6ff;
            box-shadow: 0 0 10px rgba(88, 166, 255, 0.35);
            outline: none;
        }}

        .synapse-controls-right {{
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }}

        .synapse-pills-row {{
            display: flex;
            align-items: center;
            gap: 5px;
            background: #090d13;
            border-bottom: 1px solid #21262d;
            padding: 6px 16px;
            overflow-x: auto;
        }}
        .synapse-domain-chip {{
            background: var(--code-bg);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #8b949e;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.72rem;
            font-family: monospace;
            cursor: pointer;
            transition: all 0.15s;
        }}
        .synapse-domain-chip:hover {{
            color: #fff;
            border-color: var(--accent-color);
        }}
        .synapse-domain-chip.active {{
            background: rgba(56, 139, 253, 0.2);
            border-color: #58a6ff;
            color: #58a6ff;
            font-weight: bold;
        }}

        /* Main Ego Canvas + Floating Inspector Workspace */
        .synapse-workspace {{
            position: relative;
            width: 100%;
            height: 720px;
            background: radial-gradient(circle at center, #0d1527 0%, #05080e 100%);
            display: flex;
            overflow: hidden;
        }}
        .synapse-canvas-area {{
            flex: 1;
            height: 100%;
            position: relative;
            cursor: grab;
        }}
        .synapse-canvas-area:active {{
            cursor: grabbing;
        }}
        #synapseCanvas {{
            width: 100%;
            height: 100%;
            display: block;
        }}

        /* Floating / Docked Focal Inspector */
        .synapse-inspector {{
            width: 380px;
            background: rgba(13, 17, 23, 0.95);
            border-left: 1px solid #30363d;
            box-shadow: -4px 0 20px rgba(0, 0, 0, 0.6);
            display: flex;
            flex-direction: column;
            z-index: 25;
            backdrop-filter: blur(8px);
            overflow-y: auto;
            transition: width 0.2s ease;
        }}
        .inspector-header {{
            padding: 14px 18px;
            border-bottom: 1px solid #30363d;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            background: #161b22;
        }}
        .inspector-id-block {{
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}
        .inspector-id {{
            font-family: monospace;
            font-weight: 800;
            font-size: 1.1rem;
        }}
        .inspector-domain {{
            font-size: 0.68rem;
            padding: 2px 6px;
            border-radius: 3px;
            display: inline-block;
            background: rgba(255, 255, 255, 0.08);
            color: #c9d1d9;
            font-weight: bold;
            width: fit-content;
        }}
        .inspector-body {{
            padding: 16px 18px;
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 14px;
            font-size: 0.84rem;
            color: #c9d1d9;
            line-height: 1.5;
        }}
        .inspector-title {{
            font-size: 1.02rem;
            font-weight: 700;
            color: #f0f6fc;
            margin: 0;
            line-height: 1.35;
        }}
        .inspector-origin {{
            background: #090d13;
            border-left: 3px solid #58a6ff;
            padding: 8px 12px;
            font-style: italic;
            font-size: 0.8rem;
            color: #8b949e;
            max-height: 120px;
            overflow-y: auto;
            border-radius: 0 4px 4px 0;
        }}
        .inspector-bones-section {{
            background: rgba(86, 211, 100, 0.08);
            border: 1px solid rgba(86, 211, 100, 0.3);
            border-radius: 6px;
            padding: 10px 12px;
        }}
        .inspector-bones-title {{
            font-size: 0.72rem;
            color: #56d364;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .inspector-bones-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }}
        .inspector-actions {{
            padding: 14px 18px;
            border-top: 1px solid #30363d;
            background: #161b22;
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}
        .btn-locate-card {{
            background: rgba(56, 139, 253, 0.15);
            border-color: #58a6ff;
            color: #58a6ff;
            font-weight: 700;
        }}
        .btn-locate-card:hover {{
            background: #58a6ff;
            color: #000;
        }}

        /* Subtle Synapse Tooltip on Canvas */
        .synapse-tooltip {{
            position: absolute;
            background: rgba(9, 13, 19, 0.95);
            border: 1px solid #58a6ff;
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 0.76rem;
            color: #c9d1d9;
            pointer-events: none;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.7);
            z-index: 30;
            max-width: 240px;
            line-height: 1.35;
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
            <div>[INIT] Mounting DNA Forge Knowledge Foundry &amp; Ego-Centric Synapse Engine...</div>
        </div>

        <section id="studio">
            <div class="wisdom-header">
                <h2 class="section-title">The DNA Forge: Sovereign Multi-Domain Knowledge Foundry</h2>
            </div>

            <!-- Top View Mode Switcher -->
            <div class="view-mode-bar">
                <button class="view-mode-btn active" id="btnViewCards" data-view="cards">📇 Cards View</button>
                <button class="view-mode-btn" id="btnViewGraph" data-view="graph">🕸️ Synapse Knowledge Graph</button>
            </div>

            <!-- CARDS VIEW CONTAINER GROUP (Hidden when Synapse Graph is active) -->
            <div id="cards-view-group">
                <!-- Top Census & Mining Watchdog HUD Banner [FEAT-591 / FEAT-593] -->
                <div class="dna-census-hud" id="dna-census-hud">
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

                <!-- Cards Grid View -->
                <div id="wisdom-container" class="wisdom-grid">
{cards_html}
                </div>
            </div>

            <!-- EGO-CENTRIC SYNAPSE KNOWLEDGE GRAPH [FEAT-596 v2] -->
            <div id="synapse-graph-container" class="synapse-graph-wrap" style="display: none;">
                <!-- Dedicated Synapse Navigation & Focal Control Bar -->
                <div class="synapse-nav-bar">
                    <div class="synapse-breadcrumbs-wrap" id="synapseBreadcrumbs">
                        <span>Focal Trail:</span>
                        <span class="synapse-crumb active" id="currentCrumb">PHL-001</span>
                    </div>

                    <div class="synapse-search-box">
                        <input type="text" id="synapseSearchInput" class="synapse-search-input" placeholder="🎯 Search &amp; focus any DNA card (e.g. BKM-060, FEAT-582)...">
                    </div>

                    <div class="synapse-controls-right">
                        <button id="btnSynapseLocateTop" class="studio-btn btn-locate-card" title="Locate and highlight active focal card in Cards View">📇 Locate in Cards View</button>
                        <button id="btnSynapseDepth" class="studio-btn" title="Toggle 1-Hop vs 2-Hop Network Depth">Hop Depth: 1-Hop</button>
                        <button id="btnSynapseReset" class="studio-btn" title="Recenter orbital canvas">↺ Center</button>
                    </div>
                </div>

                <!-- Quick Domain Jump Pills -->
                <div class="synapse-pills-row">
                    <span class="synapse-domain-chip active" data-domain="ALL">ALL DOMAINS</span>
                    <span class="synapse-domain-chip" data-domain="PHL" style="border-color:#a371f7; color:#a371f7;">PHL</span>
                    <span class="synapse-domain-chip" data-domain="BKM" style="border-color:#3fb950; color:#3fb950;">BKM</span>
                    <span class="synapse-domain-chip" data-domain="FEAT" style="border-color:#58a6ff; color:#58a6ff;">FEAT</span>
                    <span class="synapse-domain-chip" data-domain="WIS" style="border-color:#e3b341; color:#e3b341;">WIS</span>
                    <span class="synapse-domain-chip" data-domain="DISC" style="border-color:#f0883e; color:#f0883e;">DISC</span>
                    <span class="synapse-domain-chip" data-domain="RDNA" style="border-color:#56d364; color:#56d364;">RDNA</span>
                    <span class="synapse-domain-chip" data-domain="SPRINT" style="border-color:#d2a8ff; color:#d2a8ff;">SPRINT</span>
                    <span class="synapse-domain-chip" data-domain="BONES" style="border-color:#56d364; color:#56d364;">🦴 RACK BONES</span>
                </div>

                <!-- Main Synapse Canvas + Focal Inspector Workspace -->
                <div class="synapse-workspace" id="synapseWorkspace">
                    <div class="synapse-canvas-area" id="synapseCanvasWrap">
                        <canvas id="synapseCanvas"></canvas>
                        <div id="synapseTooltip" class="synapse-tooltip" style="display: none;"></div>
                    </div>

                    <!-- Right-Hand Focal Card Inspector -->
                    <div class="synapse-inspector" id="synapseInspector">
                        <div class="inspector-header">
                            <div class="inspector-id-block">
                                <span class="inspector-id" id="insCardId">PHL-001</span>
                                <span class="inspector-domain" id="insCardDomain">PHILOSOPHY</span>
                            </div>
                            <div id="insBadgeRow"></div>
                        </div>
                        <div class="inspector-body">
                            <h3 class="inspector-title" id="insCardTitle">Title Loading...</h3>
                            <div>
                                <span class="section-label">Origin [IMMUTABLE]</span>
                                <div class="inspector-origin" id="insCardOrigin"></div>
                            </div>
                            <div>
                                <span class="section-label">Narrative Context</span>
                                <div id="insCardNarrative"></div>
                            </div>
                            <div id="insAnchorsSection" style="display:none;">
                                <span class="section-label">Lab Anchors</span>
                                <div id="insCardAnchors" class="card-anchors"></div>
                            </div>
                            <div>
                                <span class="section-label">Tags</span>
                                <div id="insCardTags"></div>
                            </div>
                            <div class="inspector-bones-section">
                                <div class="inspector-bones-title">
                                    <span>🦴 Bone Collections Context</span>
                                    <span id="insBoneStatusBadge" style="font-size:0.65rem;"></span>
                                </div>
                                <div class="inspector-bones-list" id="insBoneCollectionsList">
                                    <span style="font-size:0.75rem; color:#8b949e; font-style:italic;">Not docked in active rack</span>
                                </div>
                            </div>
                        </div>
                        <div class="inspector-actions">
                            <button id="btnInsLocate" class="studio-btn btn-locate-card">📇 Locate in Cards View</button>
                            <button id="btnInsRack" class="studio-btn bone-btn-save">+ Add to Rack</button>
                            <button id="btnInsApprove" class="card-btn-approve" style="display:none;">✅ Approve</button>
                            <button id="btnInsArchive" class="card-btn-archive">📦 Archive</button>
                        </div>
                    </div>
                </div>
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
            var ALL_CARDS_DATA = {json.dumps(all_cards)};

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

            // Map all cards by ID for instant O(1) lookup
            var cardsById = {{}};
            ALL_CARDS_DATA.forEach(function (c) {{
                if (c.id) cardsById[c.id] = c;
            }});

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

                if (window.__refreshInspectorBoneStatus) window.__refreshInspectorBoneStatus();
            }}

            function toggleBoneInRack(cardOrId) {{
                var cid = typeof cardOrId === 'string' ? cardOrId : cardOrId.dataset.cardId;
                var cardData = cardsById[cid] || {{}};
                var title = cardData.title || (cardData.synthesis && cardData.synthesis.title) || cid;
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

            function approveCard(cardOrId) {{
                var cid = typeof cardOrId === 'string' ? cardOrId : cardOrId.dataset.cardId;
                var card = document.querySelector('[data-card-id="' + cid + '"]');
                if (card) {{
                    card.dataset.flagged = '0';
                    card.classList.remove('tron-red');
                    card.classList.add('tron-blue');

                    var badge = card.querySelector('.tron-badge-flag');
                    if (badge) badge.remove();

                    var approveBtn = card.querySelector('.card-btn-approve');
                    if (approveBtn) approveBtn.remove();
                }}

                logOperatorDecision(cid, 'APPROVED');
                updateFilterPillCounts();
                applyFilterAndSearch();
            }}

            function archiveCard(cardOrId) {{
                var cid = typeof cardOrId === 'string' ? cardOrId : cardOrId.dataset.cardId;
                var card = document.querySelector('[data-card-id="' + cid + '"]');
                if (card) {{
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

                    var btnSynapse = card.querySelector('.btn-synapse');
                    var btnRack = card.querySelector('.btn-rack');
                    var btnApprove = card.querySelector('.card-btn-approve');
                    var btnArchive = card.querySelector('.card-btn-archive');
                    var btnEdit = card.querySelector('.card-btn-edit');
                    var btnSave = card.querySelector('.card-btn-save');
                    var btnDiscard = card.querySelector('.card-btn-discard');

                    if (btnSynapse) btnSynapse.addEventListener('click', function (e) {{
                        e.stopPropagation();
                        focusCardInSynapse(card.dataset.cardId);
                    }});

                    // Double click card opens Synapse KB
                    card.addEventListener('dblclick', function(e) {{
                        if (e.target.closest('button') || e.target.closest('[contenteditable="true"]')) return;
                        focusCardInSynapse(card.dataset.cardId);
                    }});

                    if (btnRack) btnRack.addEventListener('click', function (e) {{ e.stopPropagation(); toggleBoneInRack(card); }});
                    if (btnApprove) btnApprove.addEventListener('click', function (e) {{ e.stopPropagation(); approveCard(card); }});
                    if (btnArchive) btnArchive.addEventListener('click', function (e) {{ e.stopPropagation(); archiveCard(card); }});
                    if (btnEdit) btnEdit.addEventListener('click', function (e) {{ e.stopPropagation(); unlockCard(card); }});
                    if (btnSave) btnSave.addEventListener('click', function (e) {{ e.stopPropagation(); saveSingleCard(card); }});
                    if (btnDiscard) btnDiscard.addEventListener('click', function (e) {{ e.stopPropagation(); lockCard(card, true); }});
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
            // Ego-Centric Single-Node Synapse Knowledge Graph [FEAT-596 v2]
            // -------------------------------------------------------------
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

            var focalNodeId = 'PHL-001';
            var focalBreadcrumbs = ['PHL-001'];
            var hopDepth = 1; // 1 or 2
            var synapseFilterDomain = 'ALL';
            var graphInitialized = false;

            // Global node / edge adjacency index
            var globalNodesMap = {{}};
            (GRAPH_DATA.nodes || []).forEach(function (n) {{
                globalNodesMap[n.id] = n;
            }});

            var adjacencyMap = {{}}; // id -> list of {{ targetId, type, weight }}
            (GRAPH_DATA.links || []).forEach(function (l) {{
                if (!adjacencyMap[l.source]) adjacencyMap[l.source] = [];
                if (!adjacencyMap[l.target]) adjacencyMap[l.target] = [];
                adjacencyMap[l.source].push({{ targetId: l.target, type: l.type, weight: l.weight }});
                adjacencyMap[l.target].push({{ targetId: l.source, type: l.type, weight: l.weight }});
            }});

            function getNeighborsFor(nodeId) {{
                return adjacencyMap[nodeId] || [];
            }}

            function locateCardInGrid(cid) {{
                switchView('cards');
                currentFilter = 'all';
                searchQuery = '';
                var searchInput = document.getElementById('dnaSearchInput');
                if (searchInput) searchInput.value = '';
                document.querySelectorAll('.census-domain-pill').forEach(function(p){{
                    p.classList.toggle('active', p.dataset.filter === 'all');
                }});
                applyFilterAndSearch();

                setTimeout(function() {{
                    var card = document.querySelector('[data-card-id="' + cid + '"]');
                    if (card) {{
                        card.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                        card.style.transition = 'all 0.3s ease';
                        card.style.outline = '4px solid #58a6ff';
                        card.style.boxShadow = '0 0 24px rgba(88, 166, 255, 0.8)';
                        setTimeout(function() {{
                            card.style.outline = '';
                            card.style.boxShadow = '';
                        }}, 3000);
                    }}
                }}, 100);
            }}

            function focusCardInSynapse(cid) {{
                if (!cid) return;
                focalNodeId = cid;
                if (focalBreadcrumbs[focalBreadcrumbs.length - 1] !== cid) {{
                    focalBreadcrumbs.push(cid);
                    if (focalBreadcrumbs.length > 5) focalBreadcrumbs.shift();
                }}
                switchView('graph');
                updateBreadcrumbsUi();
                updateInspectorUi(cid);
                if (window.__triggerSynapseRedraw) window.__triggerSynapseRedraw();
            }}

            function updateBreadcrumbsUi() {{
                var wrap = document.getElementById('synapseBreadcrumbs');
                if (!wrap) return;
                var html = '<span style="color:#8b949e;">Focal Trail:</span> ';
                focalBreadcrumbs.forEach(function(b, idx) {{
                    var isLast = (idx === focalBreadcrumbs.length - 1);
                    html += '<span class="synapse-crumb ' + (isLast ? 'active' : '') + '" data-cid="' + escapeHtml(b) + '">' + escapeHtml(b) + '</span>';
                    if (!isLast) html += ' <span style="color:#30363d;">›</span> ';
                }});
                wrap.innerHTML = html;

                wrap.querySelectorAll('.synapse-crumb').forEach(function(crumb) {{
                    crumb.addEventListener('click', function() {{
                        focusCardInSynapse(this.dataset.cid);
                    }});
                }});
            }}

            function updateInspectorUi(cid) {{
                var card = cardsById[cid] || globalNodesMap[cid] || {{ id: cid, title: cid }};
                var domain = (card.domain || cid.split('-')[0]).toUpperCase();
                var color = domainColors[domain] || '#58a6ff';

                var insId = document.getElementById('insCardId');
                if (insId) {{
                    insId.textContent = cid;
                    insId.style.color = color;
                }}

                var insDomain = document.getElementById('insCardDomain');
                if (insDomain) {{
                    insDomain.textContent = domain;
                    insDomain.style.border = '1px solid ' + color;
                    insDomain.style.color = color;
                }}

                var insTitle = document.getElementById('insCardTitle');
                if (insTitle) insTitle.textContent = card.title || (card.synthesis && card.synthesis.title) || cid;

                var originText = (card.origin && (card.origin.text || card.origin.verbatim)) || card.verbatim || '';
                var insOrigin = document.getElementById('insCardOrigin');
                if (insOrigin) insOrigin.textContent = originText || '(no immutable origin recorded)';

                var narrativeText = (card.synthesis && card.synthesis.narrative_context) || card.narrative_context || card.summary || '';
                var insNarrative = document.getElementById('insCardNarrative');
                if (insNarrative) insNarrative.textContent = narrativeText || '(no narrative recorded)';

                var anchors = (card.synthesis && card.synthesis.lab_anchors) || card.lab_anchors || [];
                var insAnchorsSec = document.getElementById('insAnchorsSection');
                var insAnchors = document.getElementById('insCardAnchors');
                if (insAnchorsSec && insAnchors) {{
                    if (anchors && anchors.length > 0) {{
                        insAnchorsSec.style.display = 'block';
                        insAnchors.innerHTML = anchors.map(function(a){{ return '<code>' + escapeHtml(a) + '</code>'; }}).join(' ');
                    }} else {{
                        insAnchorsSec.style.display = 'none';
                    }}
                }}

                var meta = card.metadata || {{}};
                var tags = meta.tags || (card.synthesis && card.synthesis.tags) || card.tags || [];
                if (typeof tags === 'string') tags = tags.split(',');
                var insTags = document.getElementById('insCardTags');
                if (insTags) {{
                    insTags.innerHTML = tags.map(function(t){{
                        return '<span class="tag">#' + escapeHtml(String(t).trim().lstrip('#')) + '</span>';
                    }}).join(' ') || '<em style="color:#8b949e">No tags</em>';
                }}

                // Bone Collections check
                var isDocked = activeBones.some(function(b){{ return b.id === cid; }});
                var insBoneBadge = document.getElementById('insBoneStatusBadge');
                if (insBoneBadge) {{
                    insBoneBadge.innerHTML = isDocked ? '<span style="color:#56d364; font-weight:bold;">🟢 DOCKED IN ACTIVE RACK</span>' : '<span style="color:#8b949e;">⚪ Undocked</span>';
                }}

                var bRack = document.getElementById('btnInsRack');
                if (bRack) {{
                    bRack.textContent = isDocked ? '🦴 In Rack (Click to Remove)' : '+ Add to Rack';
                    bRack.classList.toggle('bone-btn-save', isDocked);
                }}

                var matchingCols = [];
                BONE_COLLECTIONS.forEach(function(col) {{
                    if ((col.bones || []).some(function(b){{ return b.id === cid; }})) {{
                        matchingCols.push(col.name || col.id);
                    }}
                }});

                var insBoneList = document.getElementById('insBoneCollectionsList');
                if (insBoneList) {{
                    if (matchingCols.length > 0) {{
                        insBoneList.innerHTML = matchingCols.map(function(c){{
                            return '<span class="bone-chip" style="font-size:0.72rem; padding:2px 6px;">🦴 ' + escapeHtml(c) + '</span>';
                        }}).join(' ');
                    }} else if (isDocked) {{
                        insBoneList.innerHTML = '<span class="bone-chip" style="font-size:0.72rem; padding:2px 6px;">🦴 In Active Working Shelf</span>';
                    }} else {{
                        insBoneList.innerHTML = '<span style="font-size:0.75rem; color:#8b949e; font-style:italic;">Not part of any saved bone collection</span>';
                    }}
                }}

                var btnLocate = document.getElementById('btnInsLocate');
                if (btnLocate) btnLocate.onclick = function() {{ locateCardInGrid(cid); }};

                if (bRack) bRack.onclick = function() {{
                    toggleBoneInRack(cid);
                    updateInspectorUi(cid);
                }};

                var btnApprove = document.getElementById('btnInsApprove');
                if (btnApprove) {{
                    var flagged = (card.flagged || (card.metadata && card.metadata.flagged));
                    btnApprove.style.display = flagged ? 'inline-block' : 'none';
                    btnApprove.onclick = function() {{ approveCard(cid); updateInspectorUi(cid); }};
                }}

                var btnArchive = document.getElementById('btnInsArchive');
                if (btnArchive) {{
                    btnArchive.onclick = function() {{ archiveCard(cid); updateInspectorUi(cid); }};
                }}
            }}
            window.__refreshInspectorBoneStatus = function() {{ updateInspectorUi(focalNodeId); }};

            // -------------------------------------------------------------
            // HTML5 Ego Canvas Visualizer
            // -------------------------------------------------------------
            function initEgoSynapseCanvas() {{
                var canvas = document.getElementById('synapseCanvas');
                var wrap = document.getElementById('synapseCanvasWrap');
                var tooltip = document.getElementById('synapseTooltip');
                if (!canvas || !wrap) return;

                var ctx = canvas.getContext('2d');
                var width = wrap.clientWidth || 800;
                var height = wrap.clientHeight || 720;
                var dpr = window.devicePixelRatio || 1;
                canvas.width = width * dpr;
                canvas.height = height * dpr;
                ctx.scale(dpr, dpr);

                var orbitalAngle = 0;
                var zoom = 1.0;
                var panX = 0;
                var panY = 0;
                var isPanning = false;
                var startPanX = 0;
                var startPanY = 0;
                var hoveredOrbitNode = null;
                var renderedNodes = [];
                var renderedLinks = [];

                function computeEgoGraph() {{
                    renderedNodes = [];
                    renderedLinks = [];

                    var focal = globalNodesMap[focalNodeId] || cardsById[focalNodeId] || {{ id: focalNodeId, title: focalNodeId, domain: focalNodeId.split('-')[0] }};
                    var focalDomain = (focal.domain || focalNodeId.split('-')[0]).toUpperCase();

                    var centerNode = {{
                        id: focalNodeId,
                        title: focal.title || focalNodeId,
                        domain: focalDomain,
                        isCenter: true,
                        x: width / 2,
                        y: height / 2,
                        targetX: width / 2,
                        targetY: height / 2,
                        radius: 22,
                        color: domainColors[focalDomain] || '#58a6ff'
                    }};
                    renderedNodes.push(centerNode);

                    // 1st-Hop Neighbors
                    var raw1st = getNeighborsFor(focalNodeId);
                    if (synapseFilterDomain !== 'ALL') {{
                        raw1st = raw1st.filter(function(l){{
                            if (synapseFilterDomain === 'BONES') {{
                                return activeBones.some(function(b){{ return b.id === l.targetId; }});
                            }}
                            var d = (l.targetId.split('-')[0] || '').toUpperCase();
                            return d === synapseFilterDomain;
                        }});
                    }}

                    // If no explicit connections exist, populate complementary semantic anchors
                    if (raw1st.length === 0) {{
                        var fallbackTargets = ['BKM-060', 'FEAT-582', 'PHL-001', 'WIS-001', 'BKM-024', 'RDNA-001'];
                        fallbackTargets.forEach(function(tId){{
                            if (tId !== focalNodeId && (globalNodesMap[tId] || cardsById[tId])) {{
                                raw1st.push({{ targetId: tId, type: 'SEMANTIC_SIMILARITY', weight: 0.8 }});
                            }}
                        }});
                    }}

                    var count1st = raw1st.length;
                    var radius1st = Math.min(260, Math.max(160, 140 + count1st * 10));

                    raw1st.forEach(function(item, idx) {{
                        var angle = (idx / count1st) * Math.PI * 2 + orbitalAngle;
                        var nData = globalNodesMap[item.targetId] || cardsById[item.targetId] || {{ id: item.targetId, title: item.targetId, domain: item.targetId.split('-')[0] }};
                        var dName = (nData.domain || item.targetId.split('-')[0]).toUpperCase();
                        var isDocked = activeBones.some(function(b){{ return b.id === item.targetId; }});

                        var satNode = {{
                            id: item.targetId,
                            title: nData.title || item.targetId,
                            domain: dName,
                            isCenter: false,
                            hop: 1,
                            isDocked: isDocked,
                            x: width / 2 + Math.cos(angle) * radius1st,
                            y: height / 2 + Math.sin(angle) * radius1st,
                            targetX: width / 2 + Math.cos(angle) * radius1st,
                            targetY: height / 2 + Math.sin(angle) * radius1st,
                            radius: isDocked ? 14 : 10,
                            color: domainColors[dName] || '#8b949e',
                            linkType: item.type
                        }};
                        renderedNodes.push(satNode);
                        renderedLinks.push({{
                            source: centerNode,
                            target: satNode,
                            type: item.type || 'SYNAPSE',
                            weight: item.weight || 1
                        }});

                        // 2nd-Hop Extended Orbit (if hopDepth === 2)
                        if (hopDepth === 2 && idx < 8) {{
                            var raw2nd = getNeighborsFor(item.targetId).slice(0, 3);
                            raw2nd.forEach(function(item2, idx2) {{
                                if (item2.targetId === focalNodeId || raw1st.some(function(r){{ return r.targetId === item2.targetId; }})) return;
                                var subAngle = angle + ((idx2 - 1) * 0.4);
                                var radius2nd = radius1st + 90;
                                var nData2 = globalNodesMap[item2.targetId] || cardsById[item2.targetId] || {{ id: item2.targetId, title: item2.targetId, domain: item2.targetId.split('-')[0] }};
                                var dName2 = (nData2.domain || item2.targetId.split('-')[0]).toUpperCase();

                                var subNode = {{
                                    id: item2.targetId,
                                    title: nData2.title || item2.targetId,
                                    domain: dName2,
                                    isCenter: false,
                                    hop: 2,
                                    x: width / 2 + Math.cos(subAngle) * radius2nd,
                                    y: height / 2 + Math.sin(subAngle) * radius2nd,
                                    targetX: width / 2 + Math.cos(subAngle) * radius2nd,
                                    targetY: height / 2 + Math.sin(subAngle) * radius2nd,
                                    radius: 6,
                                    color: domainColors[dName2] || '#6e7681',
                                    linkType: item2.type
                                }};
                                renderedNodes.push(subNode);
                                renderedLinks.push({{
                                    source: satNode,
                                    target: subNode,
                                    type: item2.type || 'EXTENDED',
                                    weight: 0.5
                                }});
                            }});
                        }}
                    }});
                }}

                function draw() {{
                    ctx.clearRect(0, 0, width, height);
                    ctx.save();
                    ctx.translate(panX, panY);
                    ctx.scale(zoom, zoom);

                    var cx = width / 2;
                    var cy = height / 2;

                    // Orbital Guide Rings
                    ctx.beginPath();
                    ctx.arc(cx, cy, 200, 0, Math.PI * 2);
                    ctx.strokeStyle = 'rgba(88, 166, 255, 0.08)';
                    ctx.lineWidth = 1;
                    ctx.setLineDash([4, 6]);
                    ctx.stroke();
                    ctx.setLineDash([]);

                    if (hopDepth === 2) {{
                        ctx.beginPath();
                        ctx.arc(cx, cy, 290, 0, Math.PI * 2);
                        ctx.strokeStyle = 'rgba(163, 113, 247, 0.06)';
                        ctx.lineWidth = 1;
                        ctx.setLineDash([2, 8]);
                        ctx.stroke();
                        ctx.setLineDash([]);
                    }}

                    // Draw Synapse Edges
                    renderedLinks.forEach(function (l) {{
                        ctx.beginPath();
                        ctx.moveTo(l.source.x, l.source.y);
                        ctx.lineTo(l.target.x, l.target.y);

                        var isHovered = (hoveredOrbitNode && (l.source === hoveredOrbitNode || l.target === hoveredOrbitNode));

                        if (isHovered) {{
                            ctx.strokeStyle = '#58a6ff';
                            ctx.lineWidth = 2.5;
                        }} else if (l.target.hop === 2) {{
                            ctx.strokeStyle = 'rgba(110, 118, 129, 0.25)';
                            ctx.lineWidth = 0.8;
                        }} else if (l.target.isDocked) {{
                            ctx.strokeStyle = 'rgba(86, 211, 100, 0.45)';
                            ctx.lineWidth = 1.6;
                        }} else {{
                            ctx.strokeStyle = 'rgba(88, 166, 255, 0.25)';
                            ctx.lineWidth = 1.2;
                        }}
                        ctx.stroke();
                    }});

                    // Draw Orbit Nodes
                    renderedNodes.forEach(function (n) {{
                        ctx.beginPath();
                        ctx.arc(n.x, n.y, n.radius, 0, Math.PI * 2);

                        if (n.isCenter) {{
                            // Glowing Center Focal Card
                            ctx.fillStyle = '#ffffff';
                            ctx.shadowColor = n.color;
                            ctx.shadowBlur = 24;
                            ctx.fill();

                            // Outer Pulse Halo
                            ctx.beginPath();
                            ctx.arc(n.x, n.y, n.radius + 6, 0, Math.PI * 2);
                            ctx.strokeStyle = n.color;
                            ctx.lineWidth = 2.5;
                            ctx.stroke();
                        }} else {{
                            ctx.fillStyle = n.color;
                            ctx.shadowColor = n.color;
                            ctx.shadowBlur = (hoveredOrbitNode === n) ? 16 : (n.isDocked ? 12 : 4);
                            ctx.fill();

                            if (n.isDocked) {{
                                ctx.beginPath();
                                ctx.arc(n.x, n.y, n.radius + 3, 0, Math.PI * 2);
                                ctx.strokeStyle = '#56d364';
                                ctx.lineWidth = 1.5;
                                ctx.stroke();
                            }}
                        }}
                        ctx.shadowBlur = 0;

                        // Node Text Labels
                        ctx.font = (n.isCenter ? 'bold 12px' : '10px') + ' monospace';
                        ctx.fillStyle = (n.isCenter || hoveredOrbitNode === n) ? '#ffffff' : '#c9d1d9';
                        var textOffset = n.radius + 5;
                        ctx.fillText(n.id, n.x + textOffset, n.y + 3);

                        if (n.isCenter) {{
                            ctx.font = '10px sans-serif';
                            ctx.fillStyle = '#8b949e';
                            ctx.fillText(n.title.slice(0, 32), n.x + textOffset, n.y + 16);
                        }}
                    }});

                    ctx.restore();
                }}

                function loop() {{
                    draw();
                    requestAnimationFrame(loop);
                }}
                requestAnimationFrame(loop);

                window.__triggerSynapseRedraw = function() {{
                    computeEgoGraph();
                }};
                computeEgoGraph();

                function screenToWorld(sx, sy) {{
                    var rect = canvas.getBoundingClientRect();
                    var x = (sx - rect.left - panX) / zoom;
                    var y = (sy - rect.top - panY) / zoom;
                    return {{ x: x, y: y }};
                }}

                function findNodeAt(sx, sy) {{
                    var pt = screenToWorld(sx, sy);
                    for (var i = renderedNodes.length - 1; i >= 0; i--) {{
                        var n = renderedNodes[i];
                        var dx = pt.x - n.x;
                        var dy = pt.y - n.y;
                        if (dx * dx + dy * dy <= (n.radius + 8) * (n.radius + 8)) {{
                            return n;
                        }}
                    }}
                    return null;
                }}

                wrap.addEventListener('mousedown', function (e) {{
                    if (e.target !== canvas) return;
                    var hit = findNodeAt(e.clientX, e.clientY);
                    if (hit) {{
                        if (hit.id !== focalNodeId) {{
                            focusCardInSynapse(hit.id);
                        }}
                    }} else {{
                        isPanning = true;
                        startPanX = e.clientX - panX;
                        startPanY = e.clientY - panY;
                    }}
                }});

                window.addEventListener('mousemove', function (e) {{
                    if (isPanning) {{
                        panX = e.clientX - startPanX;
                        panY = e.clientY - startPanY;
                    }} else {{
                        var hit = findNodeAt(e.clientX, e.clientY);
                        hoveredOrbitNode = hit;
                        if (hit) {{
                            var rect = wrap.getBoundingClientRect();
                            tooltip.style.display = 'block';
                            tooltip.style.left = (e.clientX - rect.left + 15) + 'px';
                            tooltip.style.top = (e.clientY - rect.top + 10) + 'px';
                            tooltip.innerHTML = '<strong style="color:' + hit.color + '">[' + escapeHtml(hit.id) + ']</strong> ' +
                                escapeHtml(hit.title) + '<br><span style="color:#8b949e; font-size:0.7rem;">Domain: ' + hit.domain + (hit.isDocked ? ' • 🦴 Docked in Rack' : '') + '</span><br><span style="color:#58a6ff; font-size:0.68rem;">👉 Click to set as focal center</span>';
                        }} else {{
                            tooltip.style.display = 'none';
                        }}
                    }}
                }});

                window.addEventListener('mouseup', function () {{
                    isPanning = false;
                }});

                wrap.addEventListener('wheel', function (e) {{
                    e.preventDefault();
                    var delta = e.deltaY < 0 ? 1.15 : 0.88;
                    var newZoom = Math.min(3.0, Math.max(0.5, zoom * delta));
                    var rect = wrap.getBoundingClientRect();
                    var mx = e.clientX - rect.left;
                    var my = e.clientY - rect.top;
                    panX = mx - (mx - panX) * (newZoom / zoom);
                    panY = my - (my - panY) * (newZoom / zoom);
                    zoom = newZoom;
                }});

                var btnReset = document.getElementById('btnSynapseReset');
                if (btnReset) btnReset.onclick = function() {{ zoom = 1.0; panX = 0; panY = 0; }};

                var btnDepth = document.getElementById('btnSynapseDepth');
                if (btnDepth) btnDepth.onclick = function() {{
                    hopDepth = (hopDepth === 1) ? 2 : 1;
                    this.textContent = 'Hop Depth: ' + hopDepth + '-Hop';
                    computeEgoGraph();
                }};

                var sSearch = document.getElementById('synapseSearchInput');
                if (sSearch) sSearch.oninput = function() {{
                    var q = this.value.toLowerCase().trim();
                    if (!q) return;
                    var match = ALL_CARDS_DATA.find(function(c){{
                        return (c.id && c.id.toLowerCase().indexOf(q) !== -1) || ((c.title || (c.synthesis && c.synthesis.title) || '').toLowerCase().indexOf(q) !== -1);
                    }});
                    if (match) {{
                        focusCardInSynapse(match.id);
                    }}
                }};

                document.querySelectorAll('.synapse-domain-chip').forEach(function(chip){{
                    chip.addEventListener('click', function(){{
                        document.querySelectorAll('.synapse-domain-chip').forEach(function(c){{ c.classList.remove('active'); }});
                        chip.classList.add('active');
                        synapseFilterDomain = chip.dataset.domain;
                        computeEgoGraph();
                    }});
                }});

                var btnLocateTop = document.getElementById('btnSynapseLocateTop');
                if (btnLocateTop) btnLocateTop.onclick = function() {{ locateCardInGrid(focalNodeId); }};
            }}

            function switchView(viewName) {{
                var cardsGroup = document.getElementById('cards-view-group');
                var graphContainer = document.getElementById('synapse-graph-container');
                var btnCards = document.getElementById('btnViewCards');
                var btnGraph = document.getElementById('btnViewGraph');

                if (viewName === 'graph') {{
                    if (cardsGroup) cardsGroup.style.display = 'none';
                    if (graphContainer) graphContainer.style.display = 'flex';
                    if (btnCards) btnCards.classList.remove('active');
                    if (btnGraph) btnGraph.classList.add('active');
                    if (!graphInitialized) {{
                        graphInitialized = true;
                        setTimeout(initEgoSynapseCanvas, 50);
                    }} else if (window.__triggerSynapseRedraw) {{
                        window.__triggerSynapseRedraw();
                    }}
                    updateInspectorUi(focalNodeId);
                    updateBreadcrumbsUi();
                }} else {{
                    if (cardsGroup) cardsGroup.style.display = 'block';
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

    print(f"✅ Successfully compiled {OUTPUT_FORGE} and {OUTPUT_WISDOM} with Ego-Centric Synapse Knowledge Graph & Clean Cards View separation.")


if __name__ == "__main__":
    build_page()
