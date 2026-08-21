#!/usr/bin/env python3
# features_build.py [v2.0]
# [FEAT-465] FEAT/LAB Code Mapping & Dynamic Table Generator
# Purpose: Generate features.html from FeatureTracker.md with 5-column ledger layout matching research.html:
# [Feature ID & Name | Logic | Acme Implementation / Mechanism | Git Link | Status]

import os
import re
import markdown

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_MD = os.path.abspath(os.path.join(BASE_DIR, "../FeatureTracker.md"))
OUTPUT_HTML = os.path.join(BASE_DIR, "features.html")
REL_SOURCE_MD = "Portfolio_Dev/FeatureTracker.md"


def convert_internal_links(md_content):
    if not md_content:
        return ""
    return re.sub(r'\[((?:FEAT|LAB)-\d{3}(?:\.\d+)?)\]', r'[\1](#\1)', md_content)


def format_code_link(code_md):
    if not code_md or "none found" in code_md or "documented only" in code_md:
        return '<span style="color:#666; font-style:italic;">None (Doc Only)</span>'
    
    match = re.search(r'\[(.*?)\]\((.*?)\)', code_md)
    if match:
        text = match.group(1)
        url = match.group(2)
        return f'<a href="{url}" target="_blank" style="color:var(--accent-color); text-decoration:none; font-family:var(--font-stack); font-size:0.8rem;">{text}</a>'
    
    url_match = re.search(r'(https://[^\s)]+)', code_md)
    if url_match:
        url = url_match.group(1)
        display = url.split('/')[-1] if '/' in url else url
        return f'<a href="{url}" target="_blank" style="color:var(--accent-color); text-decoration:none; font-family:var(--font-stack); font-size:0.8rem;">{display}</a>'
        
    return code_md


def parse_philosophy(content):
    philosophy_start = content.find("# Philosophy")
    if philosophy_start == -1:
        return ""
    
    first_feat = re.search(r'^## \[((?:FEAT|LAB)-\d{3})\]', content[philosophy_start:], re.MULTILINE)
    if not first_feat:
        return content[philosophy_start:].strip()
        
    philosophy_end = philosophy_start + first_feat.start()
    philosophy_block = content[philosophy_start:philosophy_end].strip()
    lines = philosophy_block.split('\n')
    if lines and lines[0].startswith('# Philosophy'):
        lines = lines[1:]
        
    return '\n'.join(lines).strip()


def parse_feature_block(block):
    field_pattern = re.compile(r'(?:^|\n)\*\*([^*:]+)(?::\*\*|\*\*:)')
    matches = list(field_pattern.finditer(block))
    
    fields = {}
    if not matches:
        return block.strip(), fields
        
    intro = block[:matches[0].start()].strip()
    for idx, m in enumerate(matches):
        field_name = m.group(1).strip()
        start_pos = m.end()
        end_pos = matches[idx+1].start() if idx + 1 < len(matches) else len(block)
        field_value = block[start_pos:end_pos].strip()
        
        if field_value.startswith(':'):
            field_value = field_value[1:].strip()
            
        fields[field_name] = field_value
        
    return intro, fields


def parse_feature_tracker(content):
    header_pattern = re.compile(r'^## \[((?:FEAT|LAB)-\d{3}(?:\.\d+)?)\]\s*(.*?)$', re.MULTILINE)
    matches = list(header_pattern.finditer(content))
    
    features = []
    for i, match in enumerate(matches):
        feat_id = match.group(1)
        feat_title = match.group(2).strip()
        
        start_idx = match.end()
        end_idx = matches[i+1].start() if i + 1 < len(matches) else len(content)
        
        body = content[start_idx:end_idx].strip()
        intro, fields = parse_feature_block(body)
        
        features.append({
            "id": feat_id,
            "title": feat_title,
            "intro": intro,
            "fields": fields
        })
        
    return features


def generate_rows(features):
    html_rows = ""
    for item in features:
        feat_id = item['id']
        title = item['title']
        fields = item['fields']
        
        status_val = fields.get('Status', 'ACTIVE').strip()
        clean_status = "ACTIVE"
        for word in ["ACTIVE", "DESIGN", "DEFEATURED", "ARCHIVED", "CONSOLIDATED", "DORMANT", "TODO", "COMPLETED"]:
            if word in status_val.upper():
                clean_status = word
                break
                
        status_upper = clean_status.upper()
        if status_upper in ["ACTIVE", "COMPLETED"]:
            status_class = "impact-live"
        elif status_upper in ["DESIGN", "TODO"]:
            status_class = "impact-design"
        elif status_upper in ["DEFEATURED", "ARCHIVED", "CONSOLIDATED"]:
            status_class = "impact-archived"
        else:
            status_class = "impact-stable"
            
        logic_raw = fields.get('Logic') or item['intro'] or fields.get('Goal') or ""
        logic_html = markdown.markdown(convert_internal_links(logic_raw)).strip()
        
        mech_raw = fields.get('Mechanism') or fields.get('Rationale') or fields.get('Refactor Strategy') or ""
        mech_html = markdown.markdown(convert_internal_links(mech_raw)).strip()
        
        code_raw = fields.get('Code', '')
        code_html = format_code_link(code_raw)
        
        row = f"""                    <tr id="{feat_id}">
                        <td style="vertical-align: top; padding: 10px 12px; border-bottom: 1px solid #222;">
                            <span style="font-weight: bold; color: var(--accent-color); font-family: var(--font-stack); font-size: 0.85rem;">[{feat_id}]</span><br>
                            <span style="color: #fff; font-weight: 500; font-size: 0.85rem;">{title}</span>
                        </td>
                        <td style="vertical-align: top; padding: 10px 12px; border-bottom: 1px solid #222; font-size: 0.8rem; line-height: 1.4; color: var(--text-color);">
                            {logic_html}
                        </td>
                        <td style="vertical-align: top; padding: 10px 12px; border-bottom: 1px solid #222; font-size: 0.8rem; line-height: 1.4; color: #aaa;">
                            {mech_html}
                        </td>
                        <td style="vertical-align: top; padding: 10px 12px; border-bottom: 1px solid #222; font-size: 0.8rem;">
                            {code_html}
                        </td>
                        <td style="vertical-align: top; padding: 10px 12px; border-bottom: 1px solid #222; text-align: center;">
                            <span class="impact-badge {status_class}">{clean_status}</span>
                        </td>
                    </tr>"""
        html_rows += row + "\n"
        
    return html_rows


def build_full_page(features, phil_md):
    rows_html = generate_rows(features)
    
    phil_html = ""
    if phil_md:
        phil_html = f"""
            <div class="disclaimer-box" id="philosophy-box" style="margin-bottom: 15px; padding: 10px; font-size: 0.8rem; border-left-width: 3px;">
                <span style="color: var(--accent-color); font-weight: bold;">[PHILOSOPHY: THE BONES]</span><br>
                {markdown.markdown(phil_md)}
            </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Feature DNA Matrix | Jason Allred</title>
    <link rel="stylesheet" href="style.css">
    <style>
        /* High-Density Ledger Table Styling */
        .ledger-table {{
            width: 100%;
            border-collapse: collapse;
            font-family: var(--font-stack);
            font-size: 0.85rem;
            margin-top: 15px;
            background: rgba(255, 255, 255, 0.01);
        }}
        .ledger-table th {{
            text-align: left;
            padding: 12px 12px;
            border-bottom: 2px solid var(--border-color);
            color: var(--accent-color);
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 0.75rem;
        }}
        .ledger-table td {{
            padding: 10px 12px;
            border-bottom: 1px solid #222;
            vertical-align: top;
            line-height: 1.4;
        }}
        .ledger-table tr:hover {{ background: rgba(255, 255, 255, 0.02); }}

        .anchor-link {{ color: #fff; text-decoration: none; font-weight: bold; border-bottom: 1px dashed #444; }}
        .anchor-link:hover {{ color: var(--accent-color); border-bottom-color: var(--accent-color); }}

        .impact-badge {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 0.7rem;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .impact-live {{ background: #238636; color: #fff; }}
        .impact-design {{ background: #1f6feb; color: #fff; }}
        .impact-stable {{ background: #6e7681; color: #fff; }}
        .impact-archived {{ background: #9a6600; color: #fff; }}

        /* Search Filter Input Box */
        .filter-container {{
            margin-bottom: 15px;
            position: relative;
        }}
        #feat-search {{
            width: 100%;
            padding: 8px 12px;
            background-color: #111;
            border: 1px solid var(--border-color);
            color: var(--text-color);
            font-family: var(--font-stack);
            font-size: 0.8rem;
            border-radius: 4px;
            outline: none;
            transition: border-color 0.2s;
            box-sizing: border-box;
        }}
        #feat-search:focus {{
            border-color: var(--accent-color);
        }}
    </style>
</head>
<body>
<!-- [SOURCE_OF_TRUTH] Compiled from: {REL_SOURCE_MD}. Do NOT edit features.html directly! -->

    <button id="menu-toggle">☰ MENU</button>

    <nav id="sidebar">
        <mission-control></mission-control>
    </nav>

    <main>
        <div id="sys-console">
            <div>[INIT] Mounting Feature DNA Matrix...</div>
        </div>

        <section id="ledger">
            <h2 class="section-title">The Feature DNA Association Matrix</h2>
            {phil_html}

            <div class="filter-container">
                <input type="text" id="feat-search" placeholder="Filter features by ID, name, logic, mechanism, or code (e.g. active, vllm, FEAT-030, cognitive_hub)...">
            </div>

            <table class="ledger-table">
                <thead>
                    <tr>
                        <th style="width: 22%;">Feature ID & Name</th>
                        <th style="width: 26%;">Theoretical / Operational Logic</th>
                        <th style="width: 26%;">Acme Implementation / Mechanism</th>
                        <th style="width: 16%;">Git Link</th>
                        <th style="width: 10%; text-align: center;">Status</th>
                    </tr>
                </thead>
                <tbody id="features-table-body">
{rows_html}
                </tbody>
            </table>
        </section>
    </main>

    <script src="mission-control.js"></script>
    <script src="script.js"></script>
    <script>
        // Live client-side search filter across all columns
        document.addEventListener('DOMContentLoaded', () => {{
            const searchInput = document.getElementById('feat-search');
            const tableBody = document.getElementById('features-table-body');
            if (searchInput && tableBody) {{
                searchInput.addEventListener('input', (e) => {{
                    const query = e.target.value.toLowerCase().trim();
                    const rows = tableBody.getElementsByTagName('tr');
                    for (let row of rows) {{
                        const text = row.innerText.toLowerCase();
                        if (!query || text.includes(query)) {{
                            row.style.display = '';
                        }} else {{
                            row.style.display = 'none';
                        }}
                    }}
                }});
            }}
        }});
    </script>
</body>
</html>
"""


def main():
    if not os.path.exists(SOURCE_MD):
        print(f"Error: {SOURCE_MD} not found.")
        return
        
    with open(SOURCE_MD, 'r') as f:
        content = f.read()
        
    phil_md = parse_philosophy(content)
    features = parse_feature_tracker(content)
    if not features:
        print("Error: No features parsed from FeatureTracker.md.")
        return
        
    full_html = build_full_page(features, phil_md)
    
    with open(OUTPUT_HTML, 'w') as f:
        f.write(full_html)
        
    print(f"✅ Successfully compiled {OUTPUT_HTML} ({len(features)} features) in 5-column ledger layout.")


if __name__ == "__main__":
    main()
