#!/usr/bin/env python3
# Copyright 2025-2026 Jason Allred
# SPDX-License-Identifier: Apache-2.0
# timeline_build.py [v1.0]
# [FEAT-566] Story 77.6: Novel Ideas Evolutionary Timeline Compiler
# Generates Portfolio_Dev/field_notes/timeline.html from timeline_data.json,
# timeline_outliers.json, and buckets.json.

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DNA_DIR = BASE_DIR.parent / "dna"
TIMELINE_DATA_PATH = (
    DNA_DIR / "timeline_data.json"
    if (DNA_DIR / "timeline_data.json").exists()
    else DATA_DIR / "timeline_data.json"
)
OUTLIERS_DATA_PATH = DATA_DIR / "timeline_outliers.json"
BUCKETS_DATA_PATH = DATA_DIR / "buckets.json"
OUTPUT_HTML = BASE_DIR / "timeline.html"

LANES_CONFIG = [
    {
        "id": "triage",
        "title": "Triage & Classification",
        "short": "Triage",
        "color": "#388bfd",
        "bg": "rgba(56, 139, 253, 0.15)",
        "desc": "Informational inquiry gates, QQ protocol, model routing via Foyer, and semantic triage.",
    },
    {
        "id": "ambient_hooks",
        "title": "Ambient Hooks & Monitors",
        "short": "Ambient Hooks",
        "color": "#2ea043",
        "bg": "rgba(46, 160, 67, 0.15)",
        "desc": "Background watchdogs, filesystem monitors, git reset hooks, quiescence timers, and AST memory guards.",
    },
    {
        "id": "llm_kernel",
        "title": "LLM Kernel (Context · Attention · Reply)",
        "short": "LLM Kernel",
        "color": "#e3b341",
        "bg": "rgba(227, 179, 65, 0.15)",
        "desc": "In-LLM cognitive pipeline: runtime context assembly/Token Golf, attention & swarm delegation, and safe reply patching.",
    },
    {
        "id": "distillation",
        "title": "Distillation & Synthesis",
        "short": "Distillation",
        "color": "#a371f7",
        "bg": "rgba(163, 113, 247, 0.15)",
        "desc": "Post-turn synthesis, subconscious dreaming, blackboard gem refinement, and error-to-protocol crystallization.",
    },
    {
        "id": "storage",
        "title": "Memory & Substrate Storage",
        "short": "Memory & Storage",
        "color": "#f85149",
        "bg": "rgba(248, 81, 73, 0.15)",
        "desc": "ChromaDB vector vaults, persistent ICM SQLite episodic recall, git commit ledger, and zero-torch precomputed caches.",
    },
]


def load_json(path, default):
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Warning loading {path.name}: {e}")
    return default


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lab Innovations Timeline | Jason Allred</title>
    <link rel="stylesheet" href="style.css?v=826dbad3">
    <style>
        :root {
            --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
            --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            --bg-deep: #090d13;
            --bg-card: #0d1117;
            --bg-hover: #161b22;
            --border-dim: #30363d;
            --border-bright: #484f58;
            --text-main: #c9d1d9;
            --text-bright: #f0f6fc;
            --text-dim: #8b949e;
            --accent: #388bfd;
            --accent-green: #2ea043;
            --accent-purple: #a371f7;
            --accent-gold: #e3b341;
            --accent-red: #f85149;
            --accent-pink: #db61a2;
        }

        body {
            background: var(--bg-deep);
            color: var(--text-main);
            font-family: var(--font-sans);
            margin: 0;
            display: flex;
        }

        #menu-toggle {
            position: fixed;
            top: 15px;
            left: 15px;
            z-index: 1000;
            background: #1f242c;
            border: 1px solid var(--border-dim);
            color: var(--text-bright);
            padding: 8px 14px;
            border-radius: 6px;
            font-family: var(--font-mono);
            font-size: 0.85rem;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        }

        #sidebar {
            width: 280px;
            min-width: 280px;
            background: #0d1117;
            border-right: 1px solid var(--border-dim);
            height: 100vh;
            position: sticky;
            top: 0;
            overflow-y: auto;
            padding: 20px;
            box-sizing: border-box;
            transition: transform 0.25s ease-in-out;
            z-index: 999;
        }

        main {
            flex: 1;
            max-width: calc(100vw - 280px);
            padding: 30px 40px;
            box-sizing: border-box;
            overflow-x: hidden;
        }

        @media (max-width: 900px) {
            #sidebar {
                position: fixed;
                left: -280px;
            }
            #sidebar.active {
                transform: translateX(280px);
            }
            main {
                max-width: 100vw;
                padding: 60px 20px 30px 20px;
            }
        }

        .timeline-header {
            margin-bottom: 25px;
            border-bottom: 1px solid var(--border-dim);
            padding-bottom: 20px;
        }

        .timeline-title {
            font-size: 1.85rem;
            font-weight: 700;
            color: var(--text-bright);
            margin: 0 0 8px 0;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .timeline-subtitle {
            font-size: 0.95rem;
            color: var(--text-dim);
            margin: 0 0 16px 0;
            line-height: 1.5;
        }

        .metrics-bar {
            display: flex;
            flex-wrap: wrap;
            gap: 14px;
            margin-top: 15px;
        }

        .metric-pill {
            background: var(--bg-hover);
            border: 1px solid var(--border-dim);
            border-radius: 6px;
            padding: 6px 14px;
            font-family: var(--font-mono);
            font-size: 0.8rem;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .metric-val {
            font-weight: bold;
            color: var(--accent);
        }

        .controls-panel {
            background: var(--bg-card);
            border: 1px solid var(--border-dim);
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 25px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .search-row {
            display: flex;
            gap: 12px;
            align-items: center;
        }

        .search-box {
            flex: 1;
            background: var(--bg-deep);
            border: 1px solid var(--border-dim);
            border-radius: 6px;
            padding: 10px 14px;
            color: var(--text-bright);
            font-family: var(--font-mono);
            font-size: 0.85rem;
        }
        .search-box:focus {
            outline: none;
            border-color: var(--accent);
        }

        .btn-filter {
            background: var(--bg-hover);
            border: 1px solid var(--border-dim);
            color: var(--text-main);
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.8rem;
            font-family: var(--font-mono);
            transition: all 0.15s ease;
        }
        .btn-filter:hover {
            border-color: var(--text-bright);
            color: var(--text-bright);
        }
        .btn-filter.active {
            background: var(--accent);
            border-color: var(--accent);
            color: #fff;
            font-weight: bold;
        }

        .lanes-filter-row {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-items: center;
        }

        .gantt-section {
            background: var(--bg-card);
            border: 1px solid var(--border-dim);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 30px;
            overflow-x: auto;
            position: relative;
        }

        .gantt-title-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--border-dim);
        }

        .gantt-title {
            font-size: 1.05rem;
            font-weight: 600;
            color: var(--text-bright);
            font-family: var(--font-mono);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        #gantt-container {
            min-width: 900px;
            position: relative;
            user-select: none;
        }

        svg.gantt-svg {
            width: 100%;
            display: block;
        }

        .gantt-axis-line {
            stroke: var(--border-dim);
            stroke-dasharray: 4 4;
        }

        .gantt-lane-band:nth-child(even) {
            fill: rgba(255, 255, 255, 0.015);
        }

        .gantt-lane-band:nth-child(odd) {
            fill: rgba(0, 0, 0, 0.15);
        }

        .gantt-lane-label {
            font-family: var(--font-mono);
            font-size: 11px;
            font-weight: 600;
            fill: var(--text-dim);
        }

        .gantt-month-label {
            font-family: var(--font-mono);
            font-size: 11px;
            fill: var(--text-dim);
            text-anchor: middle;
        }

        .gantt-bar {
            cursor: pointer;
            rx: 4;
            transition: filter 0.15s, opacity 0.15s;
        }
        .gantt-bar:hover {
            filter: brightness(1.35) drop-shadow(0 0 6px rgba(255, 255, 255, 0.3));
        }

        .gantt-node-conception {
            cursor: pointer;
            transition: r 0.15s;
        }
        .gantt-node-conception:hover {
            r: 7;
        }

        .gantt-node-impl {
            cursor: pointer;
            transition: transform 0.15s;
        }

        .gantt-item-text {
            font-family: var(--font-mono);
            font-size: 11px;
            font-weight: bold;
            fill: #ffffff;
            pointer-events: none;
        }

        #gantt-tooltip {
            position: absolute;
            background: #1c2128;
            border: 1px solid var(--accent);
            border-radius: 6px;
            padding: 10px 14px;
            font-size: 0.8rem;
            color: var(--text-bright);
            pointer-events: none;
            display: none;
            z-index: 100;
            box-shadow: 0 8px 24px rgba(0,0,0,0.6);
            max-width: 320px;
            line-height: 1.4;
        }

        .list-section {
            margin-top: 25px;
        }

        .list-title {
            font-size: 1.15rem;
            font-weight: 600;
            color: var(--text-bright);
            margin-bottom: 16px;
            font-family: var(--font-mono);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(460px, 1fr));
            gap: 20px;
        }

        @media (max-width: 600px) {
            .cards-grid {
                grid-template-columns: 1fr;
            }
        }

        .discovery-card {
            background: var(--bg-card);
            border: 1px solid var(--border-dim);
            border-radius: 8px;
            padding: 18px;
            transition: transform 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
            position: relative;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .discovery-card:hover {
            border-color: var(--border-bright);
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.4);
        }

        .discovery-card.highlighted {
            border-color: var(--accent) !important;
            box-shadow: 0 0 16px rgba(56, 139, 253, 0.4) !important;
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 10px;
        }

        .card-id-title {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .card-id {
            font-family: var(--font-mono);
            font-size: 0.75rem;
            font-weight: bold;
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .card-title {
            font-size: 1.05rem;
            font-weight: 600;
            color: var(--text-bright);
            margin: 0;
            line-height: 1.3;
        }

        .card-badges {
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
        }

        .badge {
            font-family: var(--font-mono);
            font-size: 0.7rem;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: bold;
            text-transform: uppercase;
        }

        .badge-mature {
            background: rgba(46, 160, 67, 0.2);
            color: var(--accent-green);
            border: 1px solid var(--accent-green);
        }

        .badge-active {
            background: rgba(56, 139, 253, 0.2);
            color: var(--accent);
            border: 1px solid var(--accent);
        }

        .card-dates {
            background: var(--bg-deep);
            border: 1px solid var(--border-dim);
            border-radius: 6px;
            padding: 8px 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: var(--font-mono);
            font-size: 0.8rem;
        }

        .date-node {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }

        .date-label {
            font-size: 0.65rem;
            color: var(--text-dim);
            text-transform: uppercase;
        }

        .date-val {
            color: var(--text-bright);
            font-weight: bold;
        }

        .date-span-pill {
            background: rgba(255, 255, 255, 0.08);
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.75rem;
            color: var(--accent-gold);
        }

        .card-summary {
            font-size: 0.88rem;
            color: var(--text-main);
            line-height: 1.45;
        }

        .card-meta-rows {
            display: flex;
            flex-direction: column;
            gap: 6px;
            font-size: 0.78rem;
            border-top: 1px solid var(--border-dim);
            padding-top: 10px;
        }

        .meta-row {
            display: flex;
            align-items: baseline;
            gap: 8px;
        }

        .meta-key {
            font-family: var(--font-mono);
            color: var(--text-dim);
            min-width: 90px;
        }

        .meta-val {
            color: var(--text-bright);
            word-break: break-all;
        }

        .meta-val a {
            color: var(--accent);
            text-decoration: none;
        }
        .meta-val a:hover {
            text-decoration: underline;
        }

        .anchors-list {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-top: 2px;
        }

        .anchor-tag {
            background: rgba(56, 139, 253, 0.1);
            border: 1px solid rgba(56, 139, 253, 0.3);
            color: var(--accent);
            font-family: var(--font-mono);
            font-size: 0.7rem;
            padding: 2px 6px;
            border-radius: 4px;
        }

        .tags-row {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-top: 4px;
        }

        .tag-pill {
            background: var(--bg-hover);
            color: var(--text-dim);
            font-size: 0.7rem;
            font-family: var(--font-mono);
            padding: 2px 6px;
            border-radius: 4px;
        }

        #outliers-drawer {
            display: none;
            background: #161b22;
            border: 1px solid var(--accent-gold);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 25px;
        }

        .outlier-card {
            background: var(--bg-deep);
            border: 1px solid var(--border-dim);
            border-left: 4px solid var(--accent-gold);
            border-radius: 6px;
            padding: 14px;
            margin-top: 10px;
        }
    </style>
    <style id="option-b-viewport-fix">
        html, body { height: auto !important; min-height: 100vh !important; overflow-y: auto !important; overflow-x: hidden; }
        main { max-width: none !important; height: auto !important; min-height: 100vh; overflow-y: visible !important; flex: 1 1 auto; min-width: 0; }
        footer.apache-copyright-footer { width: 100%; box-sizing: border-box; flex-shrink: 0; }
    </style>
</head>
<body>

    <button id="menu-toggle">☰ MENU</button>

    <nav id="sidebar">
        <mission-control></mission-control>
    </nav>

    <main>
        <header class="timeline-header">
            <h1 class="timeline-title">🏛️ Lab Innovations & Evolutionary Timeline</h1>
            <p class="timeline-subtitle">
                Original innovations, architectural paradigms, and evolutionary milestones of the Federated Autonomous Lab.
                Tracking the genesis, conception-to-implementation spans, and cognitive lifecycle maturity.
            </p>

            <div class="metrics-bar">
                <div class="metric-pill">
                    <span>Milestones:</span>
                    <span class="metric-val">__METRIC_TOTAL__</span>
                </div>
                <div class="metric-pill">
                    <span>Mature Axioms:</span>
                    <span class="metric-val" style="color: var(--accent-green);">__METRIC_MATURE__</span>
                </div>
                <div class="metric-pill">
                    <span>Active Horizons:</span>
                    <span class="metric-val" style="color: var(--accent);">__METRIC_ACTIVE__</span>
                </div>
                <div class="metric-pill">
                    <span>Epoch Span:</span>
                    <span class="metric-val" style="color: var(--accent-gold);">__EPOCH_SPAN__</span>
                </div>
                <div class="metric-pill" style="cursor: pointer;" id="btn-toggle-outliers">
                    <span>Pending Outliers:</span>
                    <span class="metric-val" style="color: __OUTLIER_COLOR__;">__METRIC_OUTLIERS__ ⚠️</span>
                </div>
            </div>
        </header>

        <section id="outliers-drawer">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style="margin: 0; color: var(--accent-gold); font-family: var(--font-mono); font-size: 1rem;">
                    ⚠️ Outlier Review Pipeline (__METRIC_OUTLIERS__ item)
                </h3>
                <span style="font-size: 0.8rem; color: var(--text-dim);">Similarity confidence &lt; 0.65 threshold</span>
            </div>
            <div id="outliers-list-container"></div>
        </section>

        <section class="controls-panel">
            <div class="search-row">
                <input type="text" id="filter-input" class="search-box" placeholder="🔍 Search innovations by title, tag, code anchor, or sprint ref...">
                <button id="btn-reset-filters" class="btn-filter">Reset</button>
            </div>
            <div class="lanes-filter-row" id="lanes-filter-container">
                <button class="btn-filter active" data-lane="all">All Swimlanes (__METRIC_TOTAL__)</button>
            </div>
        </section>

        <section class="gantt-section">
            <div class="gantt-title-row">
                <div class="gantt-title">
                    <span>📊 Innovations Gantt Matrix</span>
                    <span style="font-size: 0.75rem; color: var(--text-dim); font-weight: normal;">[Conception ● ━━━ ◆ Implementation]</span>
                </div>
                <div style="font-size: 0.75rem; color: var(--text-dim); font-family: var(--font-mono);">
                    Hover for details • Click bar to inspect
                </div>
            </div>

            <div id="gantt-container">
                <svg id="gantt-svg" class="gantt-svg"></svg>
                <div id="gantt-tooltip"></div>
            </div>
        </section>

        <section class="list-section">
            <div class="list-title">
                <span id="list-counter-label">📋 All Innovations (__METRIC_TOTAL__)</span>
                <span style="font-size: 0.8rem; color: var(--text-dim); font-weight: normal;">Sorted Chronologically</span>
            </div>

            <div class="cards-grid" id="cards-container">
                <!-- Populated dynamically via JS -->
            </div>
        </section>

        <footer class="apache-copyright-footer" style="text-align: center; padding: 20px 16px; margin-top: 28px; border-top: 1px solid var(--border-dim); color: var(--text-dim); font-size: 0.78rem; font-family: var(--font-mono);">
            Copyright 2025–2026 Jason Allred
        </footer>
    </main>

    <script src="mission-control.js?v=16cf2268"></script>
    <script>
        const DISCOVERIES = __JSON_DISCOVERIES__;
        const OUTLIERS = __JSON_OUTLIERS__;
        const LANES = __JSON_LANES__;

        let currentLaneFilter = 'all';
        let searchQuery = '';
        let selectedId = null;

        document.addEventListener('DOMContentLoaded', () => {
            renderLaneFilterButtons();
            renderOutliers();
            renderGanttChart();
            renderCards();

            const filterInput = document.getElementById('filter-input');
            filterInput.addEventListener('input', (e) => {
                searchQuery = e.target.value.toLowerCase().trim();
                renderGanttChart();
                renderCards();
            });

            document.getElementById('btn-reset-filters').addEventListener('click', () => {
                filterInput.value = '';
                searchQuery = '';
                currentLaneFilter = 'all';
                selectedId = null;
                document.querySelectorAll('#lanes-filter-container .btn-filter').forEach(b => {
                    b.classList.toggle('active', b.getAttribute('data-lane') === 'all');
                });
                renderGanttChart();
                renderCards();
            });

            const outlierBtn = document.getElementById('btn-toggle-outliers');
            const outlierDrawer = document.getElementById('outliers-drawer');
            outlierBtn.addEventListener('click', () => {
                const isHidden = outlierDrawer.style.display === 'none' || outlierDrawer.style.display === '';
                outlierDrawer.style.display = isHidden ? 'block' : 'none';
                if (isHidden) {
                    outlierDrawer.scrollIntoView({ behavior: 'smooth' });
                }
            });

            window.addEventListener('resize', () => {
                renderGanttChart();
            });
        });

        function renderLaneFilterButtons() {
            const container = document.getElementById('lanes-filter-container');
            LANES.forEach(lane => {
                const count = DISCOVERIES.filter(d => d.bucket_id === lane.id).length;
                const btn = document.createElement('button');
                btn.className = 'btn-filter';
                btn.setAttribute('data-lane', lane.id);
                btn.style.borderLeft = `3px solid ${lane.color}`;
                btn.textContent = `${lane.short} (${count})`;
                btn.addEventListener('click', () => {
                    document.querySelectorAll('#lanes-filter-container .btn-filter').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    currentLaneFilter = lane.id;
                    renderGanttChart();
                    renderCards();
                });
                container.appendChild(btn);
            });

            container.querySelector('[data-lane="all"]').addEventListener('click', function() {
                document.querySelectorAll('#lanes-filter-container .btn-filter').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                currentLaneFilter = 'all';
                renderGanttChart();
                renderCards();
            });
        }

        function renderOutliers() {
            const container = document.getElementById('outliers-list-container');
            if (!OUTLIERS.length) {
                container.innerHTML = '<p style="color: var(--text-dim); font-size: 0.85rem;">No unclassified outliers pending review.</p>';
                return;
            }

            container.innerHTML = OUTLIERS.map(o => `
                <div class="outlier-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <span style="font-family: var(--font-mono); color: var(--accent-gold); font-size: 0.75rem; font-weight: bold;">[${o.id}]</span>
                            <strong style="color: var(--text-bright); margin-left: 8px; font-size: 0.95rem;">${o.title}</strong>
                        </div>
                        <span class="badge" style="background: rgba(227, 179, 65, 0.15); color: var(--accent-gold); border: 1px solid var(--accent-gold);">${o.operator_status}</span>
                    </div>
                    <p style="margin: 8px 0; font-size: 0.85rem; color: var(--text-main);">${o.summary}</p>
                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--text-dim); font-family: var(--font-mono); border-top: 1px solid var(--border-dim); padding-top: 8px; margin-top: 8px;">
                        <span>Candidate: <strong style="color: var(--accent);">${o.candidate_bucket}</strong> (sim=${o.similarity_score})</span>
                        <span>Action: <strong style="color: var(--text-bright);">${o.recommended_action}</strong></span>
                    </div>
                </div>
            `).join('');
        }

        function renderGanttChart() {
            const svg = document.getElementById('gantt-svg');
            const tooltip = document.getElementById('gantt-tooltip');
            svg.innerHTML = '';

            const filtered = getFilteredDiscoveries();

            const minTime = new Date('2025-10-15T00:00:00Z').getTime();
            const maxTime = new Date('2026-11-22T00:00:00Z').getTime();
            const totalDuration = maxTime - minTime;

            const activeLanes = LANES.filter(l => currentLaneFilter === 'all' || currentLaneFilter === l.id);
            const rowHeight = 28;
            const lanePadY = 14;
            const headerHeight = 40;
            const svgWidth = Math.max(960, document.getElementById('gantt-container').clientWidth);
            const leftMargin = 195;
            const rightMargin = 40;
            const chartWidth = svgWidth - leftMargin - rightMargin;

            function getX(dateStr) {
                const t = new Date(dateStr + 'T00:00:00Z').getTime();
                const ratio = Math.max(0, Math.min(1, (t - minTime) / totalDuration));
                return leftMargin + (ratio * chartWidth);
            }

            // Compute dynamic lane heights based on number of items so horizontal lines never overlap
            const laneLayouts = [];
            let currentY = headerHeight;
            activeLanes.forEach(lane => {
                const laneItems = filtered
                    .filter(d => d.bucket_id === lane.id)
                    .sort((a, b) => a.conception_date.localeCompare(b.conception_date));
                const laneH = Math.max(54, (laneItems.length * rowHeight) + (lanePadY * 2));
                laneLayouts.push({ lane, items: laneItems, y: currentY, height: laneH });
                currentY += laneH;
            });
            const svgHeight = currentY + 12;

            svg.setAttribute('viewBox', `0 0 ${svgWidth} ${svgHeight}`);
            svg.setAttribute('height', svgHeight);

            const months = [
                { label: "Nov '25", date: "2025-11-01" },
                { label: "Dec '25", date: "2025-12-01" },
                { label: "Jan '26", date: "2026-01-01" },
                { label: "Feb '26", date: "2026-02-01" },
                { label: "Mar '26", date: "2026-03-01" },
                { label: "Apr '26", date: "2026-04-01" },
                { label: "May '26", date: "2026-05-01" },
                { label: "Jun '26", date: "2026-06-01" },
                { label: "Jul '26", date: "2026-07-01" },
                { label: "Aug '26", date: "2026-08-01" },
                { label: "Sep '26", date: "2026-09-01" },
                { label: "Oct '26", date: "2026-10-01" },
                { label: "Nov '26", date: "2026-11-01" }
            ];

            // Draw lane backgrounds first
            laneLayouts.forEach(({ lane, y, height }) => {
                const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
                rect.setAttribute('x', 0);
                rect.setAttribute('y', y);
                rect.setAttribute('width', svgWidth);
                rect.setAttribute('height', height);
                rect.setAttribute('class', 'gantt-lane-band');
                svg.appendChild(rect);

                const marker = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
                marker.setAttribute('x', 6);
                marker.setAttribute('y', y + 10);
                marker.setAttribute('width', 4);
                marker.setAttribute('height', height - 20);
                marker.setAttribute('fill', lane.color);
                marker.setAttribute('rx', 2);
                svg.appendChild(marker);

                const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                label.setAttribute('x', 18);
                label.setAttribute('y', y + (height / 2) + 4);
                label.setAttribute('class', 'gantt-lane-label');
                label.textContent = lane.short;
                svg.appendChild(label);
            });

            // Draw monthly vertical grid lines
            months.forEach(m => {
                const x = getX(m.date);
                const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                line.setAttribute('x1', x);
                line.setAttribute('y1', headerHeight);
                line.setAttribute('x2', x);
                line.setAttribute('y2', svgHeight);
                line.setAttribute('class', 'gantt-axis-line');
                svg.appendChild(line);

                const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                text.setAttribute('x', x);
                text.setAttribute('y', 24);
                text.setAttribute('class', 'gantt-month-label');
                text.textContent = m.label;
                svg.appendChild(text);
            });
            const freezeX = getX('2026-11-22');

            // Draw horizontal evolution lines + vertical revision ticks per item
            laneLayouts.forEach(({ lane, items, y }) => {
                items.forEach((item, rowIdx) => {
                    const endDate = item.implementation_date;
                    const xStart = getX(item.conception_date);
                    const xImpl = getX(item.implementation_date);
                    const xEnd = Math.max(xStart + 10, getX(endDate));
                    const lineY = y + lanePadY + (rowIdx * rowHeight) + (rowHeight / 2);
                    const isSelected = selectedId === item.id;

                    const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                    group.style.cursor = 'pointer';

                    // Horizontal evolution line
                    const hLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                    hLine.setAttribute('x1', xStart);
                    hLine.setAttribute('y1', lineY);
                    hLine.setAttribute('x2', xEnd);
                    hLine.setAttribute('y2', lineY);
                    hLine.setAttribute('stroke', lane.color);
                    hLine.setAttribute('stroke-width', isSelected ? '4.5' : '3');
                    hLine.setAttribute('stroke-linecap', 'round');
                    hLine.setAttribute('opacity', isSelected ? '1.0' : '0.88');
                    group.appendChild(hLine);

                    // Collect vertical revision ticks (conception, implementation, and any explicit revisions)
                    const tickDates = new Set([item.conception_date, item.implementation_date]);
                    // Keep ticks crisp at conception & implementation on the graph; full git history is linked on each card

                    tickDates.forEach(dStr => {
                        const tx = getX(dStr);
                        const isOrigin = dStr === item.conception_date;
                        const tickH = isOrigin ? 8 : 6;
                        const vTick = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                        vTick.setAttribute('x1', tx);
                        vTick.setAttribute('y1', lineY - tickH);
                        vTick.setAttribute('x2', tx);
                        vTick.setAttribute('y2', lineY + tickH);
                        vTick.setAttribute('stroke', isSelected ? '#ffffff' : lane.color);
                        vTick.setAttribute('stroke-width', isOrigin ? '3' : '2');
                        vTick.setAttribute('stroke-linecap', 'round');
                        group.appendChild(vTick);
                    });

                    // Inline label placed to the right (or left if near freeze edge)
                    const labelText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                    const placeLeft = (freezeX - xEnd) < 165;
                    labelText.setAttribute('x', placeLeft ? (xStart - 8) : (xEnd + 8));
                    labelText.setAttribute('y', lineY + 3.5);
                    labelText.setAttribute('text-anchor', placeLeft ? 'end' : 'start');
                    labelText.setAttribute('fill', isSelected ? '#ffffff' : '#c9d1d9');
                    labelText.setAttribute('font-size', '11');
                    labelText.setAttribute('font-family', 'var(--font-mono)');
                    const shortTitle = item.title.length > 32 ? item.title.slice(0, 30) + '…' : item.title;
                    labelText.textContent = `${item.id}: ${shortTitle}`;
                    group.appendChild(labelText);

                    // Wide invisible hit target for easy hover/click
                    const hitLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                    hitLine.setAttribute('x1', xStart - 6);
                    hitLine.setAttribute('y1', lineY);
                    hitLine.setAttribute('x2', xEnd + 6);
                    hitLine.setAttribute('y2', lineY);
                    hitLine.setAttribute('stroke', 'transparent');
                    hitLine.setAttribute('stroke-width', '18');
                    group.appendChild(hitLine);

                    const showTip = (e) => {
                        const rectBox = document.getElementById('gantt-container').getBoundingClientRect();
                        const clientX = e.clientX || (e.touches && e.touches[0].clientX);
                        const clientY = e.clientY || (e.touches && e.touches[0].clientY);
                        const tipX = Math.min(rectBox.width - 320, Math.max(10, clientX - rectBox.left + 15));
                        tooltip.style.left = tipX + 'px';
                        tooltip.style.top = (clientY - rectBox.top + 15) + 'px';
                        const revHtml = (Array.isArray(item.revisions) && item.revisions.length)
                            ? `<div style="font-size: 0.72rem; color: var(--text-dim); margin-top: 4px;">Revisions: ${item.revisions.map(r => `${r.date} (${r.label})`).join(' • ')}</div>`
                            : '';
                        const evolvedHtml = item.last_evolved_date
                            ? `<br>Last Evolved: <strong style="color: var(--text-bright);">${item.last_evolved_date}</strong>`
                            : '';
                        tooltip.innerHTML = `
                            <div style="font-family: var(--font-mono); color: ${lane.color}; font-weight: bold; margin-bottom: 4px;">
                                [${item.id}] ${item.title}
                            </div>
                            <div style="font-size: 0.75rem; color: var(--text-dim); margin-bottom: 6px;">
                                Conception: <strong style="color: var(--text-bright);">${item.conception_date}</strong><br>
                                First Build: <strong style="color: var(--text-bright);">${item.implementation_date}</strong>${evolvedHtml}
                            </div>
                            <div style="font-size: 0.8rem; color: var(--text-main); margin-bottom: 6px;">
                                ${item.summary}
                            </div>
                            ${revHtml}
                            <div style="font-size: 0.7rem; color: var(--accent-gold); font-family: var(--font-mono); margin-top: 4px;">
                                Sprint: ${item.sprint_ref}
                            </div>
                        `;
                        tooltip.style.display = 'block';
                    };

                    const hideTip = () => {
                        tooltip.style.display = 'none';
                    };

                    const clickItem = () => {
                        selectedId = item.id;
                        renderGanttChart();
                        renderCards();
                        const targetCard = document.getElementById(`card-${item.id}`);
                        if (targetCard) {
                            targetCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        }
                    };

                    group.addEventListener('mouseenter', showTip);
                    group.addEventListener('mousemove', showTip);
                    group.addEventListener('mouseleave', hideTip);
                    group.addEventListener('click', clickItem);

                    svg.appendChild(group);
                });
            });
        }

        function getFilteredDiscoveries() {
            return DISCOVERIES.filter(item => {
                if (currentLaneFilter !== 'all' && item.bucket_id !== currentLaneFilter) {
                    return false;
                }
                if (searchQuery) {
                    const fullText = (item.id + ' ' + item.title + ' ' + item.summary + ' ' + item.sprint_ref + ' ' + item.origin_artifact + ' ' + (item.tags || []).join(' ') + ' ' + (item.code_anchors || []).join(' ')).toLowerCase();
                    if (!fullText.includes(searchQuery)) {
                        return false;
                    }
                }
                return true;
            });
        }

        function renderCards() {
            const container = document.getElementById('cards-container');
            const counterLabel = document.getElementById('list-counter-label');
            const filtered = getFilteredDiscoveries();

            counterLabel.textContent = `📋 Innovations (${filtered.length} of ${DISCOVERIES.length})`;

            if (!filtered.length) {
                container.innerHTML = `
                    <div style="grid-column: 1 / -1; padding: 40px; text-align: center; color: var(--text-dim); background: var(--bg-card); border: 1px dashed var(--border-dim); border-radius: 8px;">
                        No innovations match the current search or swimlane criteria.
                    </div>
                `;
                return;
            }

            container.innerHTML = filtered.map(item => {
                const lane = LANES.find(l => l.id === item.bucket_id) || { color: '#888', short: item.bucket_id };
                const durationDays = calculateDurationDays(item.conception_date, item.implementation_date);
                const isSelected = selectedId === item.id;

                const codeAnchorsHtml = (item.code_anchors || []).map(a => {
                    if (a.startsWith('HomeLabAI/')) {
                        const rel = a.slice('HomeLabAI/'.length);
                        const blobUrl = `https://github.com/kEnder242/HomeLabAI/blob/main/${rel}`;
                        const histUrl = `https://github.com/kEnder242/HomeLabAI/commits/main/${rel}`;
                        return `<span class="anchor-tag"><a href="${blobUrl}" target="_blank" onclick="event.stopPropagation()" style="color: inherit; text-decoration: none;"><code>${a}</code></a> <a href="${histUrl}" target="_blank" onclick="event.stopPropagation()" title="View Git commit history" style="text-decoration: none; opacity: 0.75;">⏱</a></span>`;
                    }
                    if (a.startsWith('Portfolio_Dev/')) {
                        const rel = a.slice('Portfolio_Dev/'.length);
                        const blobUrl = `https://github.com/kEnder242/Portfolio_Dev/blob/main/${rel}`;
                        const histUrl = `https://github.com/kEnder242/Portfolio_Dev/commits/main/${rel}`;
                        return `<span class="anchor-tag"><a href="${blobUrl}" target="_blank" onclick="event.stopPropagation()" style="color: inherit; text-decoration: none;"><code>${a}</code></a> <a href="${histUrl}" target="_blank" onclick="event.stopPropagation()" title="View Git commit history" style="text-decoration: none; opacity: 0.75;">⏱</a></span>`;
                    }
                    return `<span class="anchor-tag" title="Private workspace file"><code>${a}</code> <span style="opacity:0.6; font-size:0.65rem;">[private]</span></span>`;
                }).join('');

                const sprintLinksHtml = (item.sprint_links && item.sprint_links.length)
                    ? item.sprint_links.map(sl => sl.url
                        ? `<a href="${sl.url}" target="_blank" onclick="event.stopPropagation()">${sl.label} ↗</a>`
                        : `<span>${sl.label}</span>`
                    ).join(' &nbsp;/&nbsp; ')
                    : `<span>${item.sprint_ref}</span>`;

                const fmtCommit = (c, prefix) => {
                    if (!c || !c.sha) return '';
                    if (c.repo === 'HomeLabAI' || c.repo === 'Portfolio_Dev') {
                        const url = `https://github.com/kEnder242/${c.repo}/commit/${c.sha}`;
                        return `${prefix}: <a href="${url}" target="_blank" onclick="event.stopPropagation()" style="font-family: var(--font-mono);">${c.sha}</a> <span style="opacity:0.7;">(${c.date})</span>`;
                    }
                    return `${prefix}: <code>${c.sha}</code> <span style="opacity:0.7;">(${c.date})</span>`;
                };
                const gitRowParts = [fmtCommit(item.first_commit, 'First'), fmtCommit(item.last_commit, 'Latest')].filter(Boolean);
                const gitRowHtml = gitRowParts.length
                    ? `<div class="meta-row"><span class="meta-key">Git:</span><span class="meta-val" style="font-size:0.75rem;">${gitRowParts.join(' &nbsp;•&nbsp; ')}</span></div>`
                    : '';

                const tagsHtml = (item.tags || []).map(t => `
                    <span class="tag-pill">#${t}</span>
                `).join('');

                return `
                    <article class="discovery-card ${isSelected ? 'highlighted' : ''}" id="card-${item.id}" onclick="selectCard('${item.id}')">
                        <div class="card-header">
                            <div class="card-id-title">
                                <span class="card-id" style="color: ${lane.color};">Innovation [${item.id}] • ${lane.short}</span>
                                <h3 class="card-title">${item.title}</h3>
                            </div>
                            <div class="card-badges">
                                <span class="badge ${item.status === 'MATURE' ? 'badge-mature' : 'badge-active'}">${item.status}</span>
                            </div>
                        </div>

                        <div class="card-dates">
                            <div class="date-node">
                                <span class="date-label">● Conception</span>
                                <span class="date-val">${item.conception_date}</span>
                            </div>
                            <span class="date-span-pill">⏱️ ${durationDays} days span</span>
                            <div class="date-node" style="text-align: right;">
                                <span class="date-label">◆ ${item.last_evolved_date ? 'Last Evolved' : 'Implementation'}</span>
                                <span class="date-val">${item.last_evolved_date || item.implementation_date}</span>
                            </div>
                        </div>

                        <div class="card-summary">
                            ${item.summary}
                        </div>

                        <div class="card-meta-rows">
                            <div class="meta-row">
                                <span class="meta-key">Origin:</span>
                                <span class="meta-val"><code>${item.origin_artifact}</code></span>
                            </div>
                            <div class="meta-row">
                                <span class="meta-key">Sprint:</span>
                                <span class="meta-val">${sprintLinksHtml}</span>
                            </div>
                            ${gitRowHtml}
                            ${item.arxiv_inspiration ? `
                                <div class="meta-row">
                                    <span class="meta-key">ArXiv:</span>
                                    <span class="meta-val" style="color: var(--accent-purple);">${item.arxiv_inspiration}</span>
                                </div>
                            ` : ''}
                            ${codeAnchorsHtml ? `
                                <div class="meta-row" style="flex-direction: column; align-items: flex-start; gap: 4px;">
                                    <span class="meta-key">Code Anchors:</span>
                                    <div class="anchors-list">${codeAnchorsHtml}</div>
                                </div>
                            ` : ''}
                            <div class="tags-row">${tagsHtml}</div>
                        </div>
                    </article>
                `;
            }).join('');
        }

        function selectCard(id) {
            selectedId = id;
            renderGanttChart();
            document.querySelectorAll('.discovery-card').forEach(c => {
                c.classList.toggle('highlighted', c.id === `card-${id}`);
            });
        }

        function calculateDurationDays(startStr, endStr) {
            try {
                const d1 = new Date(startStr);
                const d2 = new Date(endStr);
                const diffTime = Math.abs(d2 - d1);
                return Math.max(1, Math.ceil(diffTime / (1000 * 60 * 60 * 24)));
            } catch (e) {
                return 1;
            }
        }
    </script>
</body>
</html>
"""


def resolve_sprint_links(sprint_ref: str):
    import re
    sprints_root = Path("/home/jallred/Dev_Lab/Portfolio_Dev/docs/sprints")
    parts = [p.strip() for p in (sprint_ref or "").split("/") if p.strip()]
    resolved = []
    for part in parts:
        candidates = [part]
        m = re.match(r"SPR-(\d+)(?:\.(\d+))?", part)
        if m:
            major, minor = m.group(1), m.group(2) or "0"
            candidates.append(f"SPRINT_PLAN_SPR_{major}_{minor}.md")
            candidates.append(f"SPRINT_PLAN_SPR_{major}_0.md")
        found_url = None
        found_label = part
        for cand in candidates:
            for folder in ("active", "archive"):
                if (sprints_root / folder / cand).exists():
                    found_url = f"https://github.com/kEnder242/Portfolio_Dev/blob/main/docs/sprints/{folder}/{cand}"
                    found_label = cand
                    break
            if found_url:
                break
        resolved.append({"label": found_label, "url": found_url})
    return resolved


def build_timeline_html():
    print("--- COMPILING NOVEL IDEAS TIMELINE ---")
    discoveries = load_json(TIMELINE_DATA_PATH, [])
    outliers = load_json(OUTLIERS_DATA_PATH, [])
    buckets = load_json(BUCKETS_DATA_PATH, [])

    unresolved_sprints = []
    for d in discoveries:
        links = resolve_sprint_links(d.get("sprint_ref", ""))
        d["sprint_links"] = links
        for lk in links:
            if not lk["url"]:
                unresolved_sprints.append((d["id"], lk["label"]))

    discoveries.sort(
        key=lambda x: (x.get("conception_date", ""), x.get("implementation_date", ""))
    )

    total_discoveries = len(discoveries)
    mature_count = sum(1 for d in discoveries if d.get("status") == "MATURE")
    active_count = sum(1 for d in discoveries if d.get("status") == "ACTIVE")
    outlier_count = len(outliers)

    all_dates = []
    for d in discoveries:
        for k in ("conception_date", "implementation_date", "last_evolved_date"):
            if d.get(k):
                all_dates.append(d[k])

    min_date_str = min(all_dates) if all_dates else "2025-10-01"
    max_date_str = max(all_dates) if all_dates else "2026-11-22"

    outlier_color = "var(--accent-gold)" if outlier_count > 0 else "var(--text-dim)"

    html = HTML_TEMPLATE
    html = html.replace("__METRIC_TOTAL__", str(total_discoveries))
    html = html.replace("__METRIC_MATURE__", str(mature_count))
    html = html.replace("__METRIC_ACTIVE__", str(active_count))
    html = html.replace("__METRIC_OUTLIERS__", str(outlier_count))
    html = html.replace("__OUTLIER_COLOR__", outlier_color)
    html = html.replace("__EPOCH_SPAN__", f"{min_date_str} → {max_date_str}")
    html = html.replace("__JSON_DISCOVERIES__", json.dumps(discoveries))
    html = html.replace("__JSON_OUTLIERS__", json.dumps(outliers))
    html = html.replace("__JSON_LANES__", json.dumps(LANES_CONFIG))

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(
        f"✅ Generated {OUTPUT_HTML.name} ({len(html)} bytes, {total_discoveries} discoveries, unresolved_sprints={len(unresolved_sprints)})"
    )
    if unresolved_sprints:
        print("⚠️ Unresolved sprint refs:", unresolved_sprints)


if __name__ == "__main__":
    build_timeline_html()
