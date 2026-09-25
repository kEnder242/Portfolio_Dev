#!/usr/bin/env python3
"""
[FEAT-582 / FEAT-603] DNA Forge Build System (Modular Architecture)
Compiles Sovereign 3-Tab Architecture (Drafting, Synapse Graph, Review) from templates and modular JS/CSS assets.
"""

import datetime
import html
import json
import os
import shutil
from pathlib import Path

# Paths
DNA_FORGE_DIR = Path(__file__).resolve().parent
PORTFOLIO_DEV_DIR = DNA_FORGE_DIR.parent
FIELD_NOTES_DIR = PORTFOLIO_DEV_DIR / "field_notes"
DNA_DIR = PORTFOLIO_DEV_DIR / "dna"
DATA_DIR = FIELD_NOTES_DIR / "data"

MANIFEST_PATH = DATA_DIR / "dna_manifest.json"
DECISIONS_PATH = DATA_DIR / "dna_decisions.json"
BONE_COLLECTIONS_PATH = DATA_DIR / "bone_collections.json"
CONNECTIONS_GRAPH_PATH = DATA_DIR / "dna_connections_graph.json"
NIGHTLY_STATE_PATH = PORTFOLIO_DEV_DIR.parent / "HomeLabAI/run/nightly_synthesis_state.json"
SPRINT_DATA_PATH = PORTFOLIO_DEV_DIR.parent / "Portfolio_Dev/dna/sprint_data.json"
GEMS_PATH = DATA_DIR / "latest_synthesis_gems.json"

TEMPLATE_PATH = DNA_FORGE_DIR / "templates/dna_forge.html"
OUTPUT_FORGE = FIELD_NOTES_DIR / "dna_forge.html"
OUTPUT_WISDOM = FIELD_NOTES_DIR / "wisdom.html"
OUTPUT_LOCAL_FORGE = DNA_FORGE_DIR / "dna_forge.html"


def escape_html(val):
    if val is None:
        return ""
    return html.escape(str(val))


def load_manifest():
    manifest = {
        "wisdom": [],
        "philosophy": [],
        "feature": [],
        "behavioral": [],
        "sprint": [],
        "discovery": [],
        "rdna": [],
        "resume": [],
        "papers": [],
        "gems": []
    }
    if MANIFEST_PATH.exists():
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                manifest.update(data)
        except Exception as e:
            print(f"Warning loading {MANIFEST_PATH}: {e}")

    # Fallback to direct dna files if needed
    phi_path = DNA_DIR / "philosophy_data.json"
    if not manifest["philosophy"] and phi_path.exists():
        try:
            with open(phi_path, "r", encoding="utf-8") as f:
                manifest["philosophy"] = json.load(f)
        except Exception:
            pass

    wis_path = DNA_DIR / "wisdom_data.json"
    if not manifest["wisdom"] and wis_path.exists():
        try:
            with open(wis_path, "r", encoding="utf-8") as f:
                manifest["wisdom"] = json.load(f)
        except Exception:
            pass

    # SPRINT data
    if not manifest["sprint"] and SPRINT_DATA_PATH.exists():
        try:
            with open(SPRINT_DATA_PATH, "r", encoding="utf-8") as f:
                manifest["sprint"] = json.load(f)
        except Exception:
            pass

    # GEMS data
    if GEMS_PATH.exists():
        try:
            with open(GEMS_PATH, "r", encoding="utf-8") as f:
                raw_gems = json.load(f)
                gems_list = raw_gems.get("gems", []) if isinstance(raw_gems, dict) else (raw_gems if isinstance(raw_gems, list) else [])
                formatted_gems = []
                for g in gems_list:
                    if not isinstance(g, dict):
                        continue
                    cid = g.get("id") or f"GEM-{len(formatted_gems)+1:03d}"
                    tags_raw = g.get("tags", [])
                    tag_list = tags_raw if isinstance(tags_raw, list) else [t.strip() for t in str(tags_raw).split(",") if t.strip()]
                    formatted_gems.append({
                        "id": cid,
                        "domain": "gems",
                        "title": g.get("title") or cid,
                        "origin": {
                            "text": g.get("verbatim") or g.get("synthesis", {}).get("narrative_context", ""),
                            "author": "Synthesized Gems Engine",
                            "source": "latest_synthesis_gems.json",
                            "immutable": True
                        },
                        "synthesis": {
                            "narrative_context": g.get("narrative_context") or g.get("summary") or "",
                            "lab_anchors": g.get("lab_anchors", []),
                            "tags": tag_list
                        },
                        "metadata": {
                            "tags": tag_list,
                            "date": g.get("date", "")
                        }
                    })
                manifest["gems"] = formatted_gems
        except Exception as e:
            print(f"Warning loading {GEMS_PATH}: {e}")

    return manifest


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
    domain = (card.get("domain") or card.get("_sourceCollection") or cid.split("-")[0]).upper()
    is_archived = is_archived_card(card, decisions)
    is_flagged = is_flagged_card(card, decisions)

    # Title
    title = card.get("title") or (card.get("synthesis", {}) or {}).get("title") or (card.get("theme")) or cid

    # Origin / Verbatim
    origin_obj = card.get("origin") or {}
    if isinstance(origin_obj, dict):
        origin_text = origin_obj.get("text") or origin_obj.get("verbatim") or ""
        origin_author = origin_obj.get("author") or "Human Operator"
        origin_source = origin_obj.get("source") or ""
    else:
        origin_text = card.get("verbatim") or str(origin_obj)
        origin_author = "Human Operator"
        origin_source = ""

    # Synthesis Narrative
    synth_obj = card.get("synthesis") or {}
    narrative = synth_obj.get("narrative_context") or card.get("narrative_context") or card.get("summary") or card.get("content") or ""
    lab_anchors = synth_obj.get("lab_anchors") or card.get("lab_anchors") or []

    # Metadata / Tags
    meta = card.get("metadata") or {}
    tags = meta.get("tags") or synth_obj.get("tags") or card.get("tags") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]

    card_json_attr = escape_html(json.dumps(card))

    flag_class = "flagged" if is_flagged else ""
    arch_class = "archived" if is_archived else ""

    anchors_html = ""
    if lab_anchors:
        anchors_chips = "".join(f"<code>{escape_html(a)}</code>" for a in lab_anchors[:4])
        anchors_html = f'<div class="card-anchors"><span class="section-label">Anchors:</span> {anchors_chips}</div>'

    tags_html = ""
    if tags:
        tags_chips = " ".join(f'<span class="tag">#{escape_html(str(t).lstrip("#"))}</span>' for t in tags[:6])
        tags_html = f'<div class="card-tags">{tags_chips}</div>'

    origin_block = ""
    if origin_text:
        orig_snippet = origin_text[:280] + ("..." if len(origin_text) > 280 else "")
        origin_block = f"""
        <div class="card-origin-block">
            <span class="section-label">Origin ({escape_html(origin_author)}):</span>
            <blockquote class="card-origin-text">"{escape_html(orig_snippet)}"</blockquote>
        </div>
        """

    card_markup = f"""
    <div class="dna-card {domain.lower()} {flag_class} {arch_class}" id="card-{escape_html(cid)}" data-card-id="{escape_html(cid)}" data-domain="{escape_html(domain.lower())}" data-json="{card_json_attr}">
        <div class="card-header">
            <div class="card-id-block">
                <span class="domain-pill {domain.lower()}">{escape_html(domain)}</span>
                <span class="card-id">{escape_html(cid)}</span>
            </div>
            <div class="card-actions-quick">
                <button class="btn-card-rack" data-cid="{escape_html(cid)}" title="Dock into Active Bone Rack">+ Rack</button>
                <button class="btn-card-synapse" data-cid="{escape_html(cid)}" title="View in Synapse Graph">🕸️ Synapse</button>
            </div>
        </div>
        <div class="card-body">
            <h3 class="card-title">{escape_html(title)}</h3>
            {origin_block}
            <div class="card-narrative">
                <p>{escape_html(narrative)}</p>
            </div>
            {anchors_html}
            {tags_html}
        </div>
    </div>
    """
    return card_markup


def build_page():
    manifest = load_manifest()
    bone_collections = load_bone_collections()
    decisions = load_decisions()
    connections_graph = load_connections_graph()
    mining_telemetry = load_mining_telemetry()

    buckets = ["WISDOM", "PHILOSOPHY", "FEATURE", "BEHAVIORAL", "SPRINT", "DISCOVERY", "RDNA", "RESUME", "GEMS"]

    domain_counts = {
        "FEAT": len(manifest.get("feature", [])),
        "SPRINT": len(manifest.get("sprint", [])),
        "BKM": len(manifest.get("behavioral", [])),
        "PHL": len(manifest.get("philosophy", [])),
        "WIS": len(manifest.get("wisdom", [])),
        "DISC": len(manifest.get("discovery", [])),
        "RDNA": len(manifest.get("rdna", [])),
        "GEMS": len(manifest.get("gems", []))
    }
    total_census = sum(domain_counts.values())
    sprint_delta = "+451"

    all_cards = []
    for col, items in manifest.items():
        for item in items:
            copy = dict(item)
            copy['_sourceCollection'] = col
            all_cards.append(copy)

    needs_review_count = sum(1 for c in all_cards if is_flagged_card(c, decisions))
    archived_count = sum(1 for c in all_cards if is_archived_card(c, decisions))

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

    # Sync static CSS and JS to field_notes
    os.makedirs(FIELD_NOTES_DIR / "css", exist_ok=True)
    os.makedirs(FIELD_NOTES_DIR / "js", exist_ok=True)
    shutil.copy2(DNA_FORGE_DIR / "css/dna_forge.css", FIELD_NOTES_DIR / "css/dna_forge.css")
    shutil.copy2(DNA_FORGE_DIR / "js/dna_forge.js", FIELD_NOTES_DIR / "js/dna_forge.js")
    shutil.copy2(DNA_FORGE_DIR / "js/synapse_graph.js", FIELD_NOTES_DIR / "js/synapse_graph.js")

    # Read template
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    # Replacements
    stalled_class = "stalled" if mining_telemetry['is_stalled'] else ""
    stall_status_text = "⚠️ NO-PROGRESS / STALLED HARVEST" if mining_telemetry['is_stalled'] else "🟢 MINING ACTIVE (+451 DELTA)"
    stall_reason_snippet = escape_html(mining_telemetry['stall_reason'][:75])

    page_html = template
    page_html = page_html.replace("__TOTAL_CENSUS__", str(total_census))
    page_html = page_html.replace("__SPRINT_DELTA__", sprint_delta)
    page_html = page_html.replace("__FEAT_COUNT__", str(domain_counts['FEAT']))
    page_html = page_html.replace("__SPRINT_COUNT__", str(domain_counts['SPRINT']))
    page_html = page_html.replace("__BKM_COUNT__", str(domain_counts['BKM']))
    page_html = page_html.replace("__PHL_COUNT__", str(domain_counts['PHL']))
    page_html = page_html.replace("__WIS_COUNT__", str(domain_counts['WIS']))
    page_html = page_html.replace("__DISC_COUNT__", str(domain_counts['DISC']))
    page_html = page_html.replace("__RDNA_COUNT__", str(domain_counts['RDNA']))
    page_html = page_html.replace("__GEMS_COUNT__", str(domain_counts['GEMS']))
    page_html = page_html.replace("__NEEDS_REVIEW__", str(needs_review_count))
    page_html = page_html.replace("__ARCHIVED_COUNT__", str(archived_count))
    page_html = page_html.replace("__LAST_RUN_DISPLAY__", escape_html(mining_telemetry['last_run_display']))
    page_html = page_html.replace("__DAYS_AGO__", str(mining_telemetry['days_since_run']))
    page_html = page_html.replace("__STALLED_CLASS__", stalled_class)
    page_html = page_html.replace("__STALL_REASON__", escape_html(mining_telemetry['stall_reason']))
    page_html = page_html.replace("__STALL_STATUS_TEXT__", stall_status_text)
    page_html = page_html.replace("__STALL_REASON_SNIPPET__", stall_reason_snippet)
    page_html = page_html.replace("__CARDS_HTML__", cards_html)

    page_html = page_html.replace("__MANIFEST_JSON__", json.dumps(manifest))
    page_html = page_html.replace("__BONE_COLLECTIONS_JSON__", json.dumps(bone_collections))
    page_html = page_html.replace("__MINING_TELEMETRY_JSON__", json.dumps(mining_telemetry))
    page_html = page_html.replace("__DECISIONS_JSON__", json.dumps(decisions))
    page_html = page_html.replace("__SYNAPSE_GRAPH_JSON__", json.dumps(connections_graph))

    with open(OUTPUT_FORGE, "w", encoding="utf-8") as f:
        f.write(page_html)

    with open(OUTPUT_WISDOM, "w", encoding="utf-8") as f:
        f.write(page_html)

    with open(OUTPUT_LOCAL_FORGE, "w", encoding="utf-8") as f:
        f.write(page_html)

    print(f"✅ Successfully compiled {OUTPUT_FORGE} and {OUTPUT_WISDOM} with Modular DNA Forge Architecture.")


if __name__ == "__main__":
    build_page()
