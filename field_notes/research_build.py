#!/usr/bin/env python3
# research_build.py [v1.3]
# Purpose: Generate research.html from RESEARCH_SYNTHESIS.md with ArXiv links.
# Mandate: Move ArXiv links to the number only; remove "arXiv:" prefix.
# CRITICAL: Strip all internal [FEAT-XXX] markers from the HTML output.

import os
import re

# Paths
SOURCE_MD = "/home/jallred/Dev_Lab/HomeLabAI/docs/plans/RESEARCH_SYNTHESIS.md"
TEMPLATE_HTML = "/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/research.html"
OUTPUT_HTML = "/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/research.html"

def parse_markdown_table(content):
    # Extract the main implementation table
    table_pattern = re.compile(r'\| Research Anchor \| Core Architecture \| Role in `ai_engine.py` / HomeLabAI \| Status \|\n\| :--- \| :--- \| :--- \| :--- \|\n(.*?)(?:\n\n|\n$)', re.DOTALL)
    match = table_pattern.search(content)
    if not match:
        return []
    
    rows = match.group(1).strip().split('\n')
    data = []
    for row in rows:
        cells = [c.strip() for c in row.split('|') if c.strip()]
        if len(cells) >= 4:
            anchor_cell = cells[0]
            # Extract Name and ArXiv ID
            name_match = re.search(r'\*\*(.*?)\*\*', anchor_cell)
            arxiv_match = re.search(r'\(arXiv:(.*?)\)', anchor_cell)
            
            name = name_match.group(1) if name_match else anchor_cell
            # Remove any trailing FEAT tags from the name
            name = re.sub(r'\s*\[FEAT-.*?\]', '', name).strip()
            
            arxiv_id = arxiv_match.group(1) if arxiv_match else None
            
            # Implementation cell: Strip FEATs and role-prefixes
            impl_text = cells[2]
            impl_text = re.sub(r'\[FEAT-.*?\]', '', impl_text).strip()
            impl_text = impl_text.replace('**', '')
            
            data.append({
                "name": name,
                "arxiv": arxiv_id,
                "logic": cells[1],
                "implementation": impl_text,
                "status": cells[3]
            })
    return data

def generate_html_rows(research_data):
    html_rows = ""
    for item in research_data:
        # Format the anchor cell: Name (ID) where ID is the link
        anchor_display = item['name']
        if item['arxiv']:
            # Move link to the number; remove "arXiv:" prefix
            anchor_display += f' <a href="https://arxiv.org/abs/{item["arxiv"]}" target="_blank" class="anchor-link" style="font-size: 0.75rem; border-bottom: none; font-weight: normal;">({item["arxiv"]})</a>'
        
        status_class = "impact-stable"
        clean_status = item['status'].replace('**', '')
        if any(x in clean_status for x in ["Live", "100%", "Active"]):
            status_class = "impact-live"
        elif any(x in clean_status for x in ["Design", "Sprint", "Planned"]):
            status_class = "impact-design"
        elif "DEFEATURED" in clean_status:
            status_class = "impact-stable"

        row = f"""                    <tr>
                        <td>{anchor_display}</td>
                        <td>{item['logic']}</td>
                        <td>{item['implementation']}</td>
                        <td><span class="impact-badge {status_class}">{clean_status}</span></td>
                    </tr>"""
        html_rows += row + "\n"
    return html_rows

def main():
    if not os.path.exists(SOURCE_MD):
        print(f"Error: Source {SOURCE_MD} not found.")
        return

    with open(SOURCE_MD, 'r') as f:
        md_content = f.read()

    research_data = parse_markdown_table(md_content)
    if not research_data:
        return

    new_rows = generate_html_rows(research_data)

    if not os.path.exists(TEMPLATE_HTML):
        return

    with open(TEMPLATE_HTML, 'r') as f:
        html_content = f.read()

    start_tag = "<tbody>"
    end_tag = "</tbody>"
    
    start_idx = html_content.find(start_tag) + len(start_tag)
    end_idx = html_content.find(end_tag)
    
    if start_idx == -1 or end_idx == -1:
        return

    updated_html = html_content[:start_idx] + "\n" + new_rows + "                    " + html_content[end_idx:]

    with open(OUTPUT_HTML, 'w') as f:
        f.write(updated_html)
    
    print(f"✅ Successfully updated {OUTPUT_HTML} (ID-ONLY LINKS) from {SOURCE_MD}")

if __name__ == "__main__":
    main()
