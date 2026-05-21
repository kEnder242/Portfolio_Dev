#!/usr/bin/env python3
# research_build.py [v2.0]
# Purpose: Generate research.html from standard-schema RESEARCH_SYNTHESIS.md.
# Mandate: High-Fidelity ArXiv ID-ONLY links. Zero FEAT markers in HTML.
# Schema: | Anchor | ArXiv ID | Logic | Lab Implementation [FEAT] | Status |

import os
import re

# Paths
SOURCE_MD = "/home/jallred/Dev_Lab/HomeLabAI/docs/plans/RESEARCH_SYNTHESIS.md"
TEMPLATE_HTML = "/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/research.html"
OUTPUT_HTML = "/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/research.html"

def parse_standard_table(content):
    # Matches tables with the 5-column standard schema
    header_pattern = r'\| Research Anchor \| ArXiv ID \| Theoretical Logic \| Lab Implementation \[FEAT\] \| Status \|'
    table_regex = re.compile(header_pattern + r'\n\| :--- \| :--- \| :--- \| :--- \| :--- \|\n(.*?)(?:\n\n|\n$)', re.DOTALL)
    
    all_data = []
    for match in table_regex.finditer(content):
        rows = match.group(1).strip().split('\n')
        for row in rows:
            cells = [c.strip() for c in row.split('|') if c.strip()]
            if len(cells) >= 5:
                # 1. Name
                name = cells[0].replace('**', '').strip()
                
                # 2. ArXiv ID
                arxiv_id = cells[1] if cells[1].lower() != "n/a" else None
                
                # 3. Logic
                logic = cells[2]
                
                # 4. Implementation (Strip FEATs)
                impl = re.sub(r'\[FEAT-.*?\]', '', cells[3]).strip()
                impl = impl.replace('**', '')
                
                # 5. Status
                status = cells[4].replace('**', '')
                
                all_data.append({
                    "name": name,
                    "arxiv": arxiv_id,
                    "logic": logic,
                    "implementation": impl,
                    "status": status
                })
    return all_data

def generate_html_rows(research_data):
    html_rows = ""
    for item in research_data:
        anchor_display = item['name']
        if item['arxiv']:
            anchor_display += f' <a href="https://arxiv.org/abs/{item["arxiv"]}" target="_blank" class="anchor-link" style="font-size: 0.75rem; border-bottom: none; font-weight: normal;">({item["arxiv"]})</a>'
        
        status_class = "impact-stable"
        if any(x in item['status'] for x in ["Live", "100%", "Active"]):
            status_class = "impact-live"
        elif any(x in item['status'] for x in ["Design", "Sprint", "Planned"]):
            status_class = "impact-design"

        row = f"""                    <tr>
                        <td>{anchor_display}</td>
                        <td>{item['logic']}</td>
                        <td>{item['implementation']}</td>
                        <td><span class="impact-badge {status_class}">{item['status']}</span></td>
                    </tr>"""
        html_rows += row + "\n"
    return html_rows

def main():
    if not os.path.exists(SOURCE_MD): return
    with open(SOURCE_MD, 'r') as f: md_content = f.read()

    research_data = parse_standard_table(md_content)
    if not research_data: 
        print("Error: No data parsed from standard tables.")
        return
        
    new_rows = generate_html_rows(research_data)

    with open(TEMPLATE_HTML, 'r') as f: html_content = f.read()
    
    start_tag, end_tag = "<tbody>", "</tbody>"
    start_idx = html_content.find(start_tag) + len(start_tag)
    end_idx = html_content.find(end_tag)
    
    if start_idx == -1 or end_idx == -1: return

    updated_html = html_content[:start_idx] + "\n" + new_rows + "                    " + html_content[end_idx:]
    with open(OUTPUT_HTML, 'w') as f: f.write(updated_html)
    print(f"✅ Successfully updated {OUTPUT_HTML} (Standard Schema) from {SOURCE_MD}")

if __name__ == "__main__":
    main()
