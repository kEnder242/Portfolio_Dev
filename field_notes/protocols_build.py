#!/usr/bin/env python3
# protocols_build.py [v1.0]
# Purpose: Generate protocols.html from docs/Protocols.md.
# Mandate: Parse BKMs, convert relative URLs to absolute GitHub paths, and render using markdown library.

import os
import re
import markdown

SOURCE_MD = "/home/jallred/Dev_Lab/HomeLabAI/docs/Protocols.md"
TEMPLATE_HTML = "/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/protocols.html"
OUTPUT_HTML = "/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/protocols.html"

def convert_relative_links(md_content):
    def replacer(match):
        text = match.group(1)
        url = match.group(2)
        
        # Don't convert absolute links
        if url.startswith(('http://', 'https://', 'mailto:', 'file:///')):
            return match.group(0)
            
        # Perform relative mapping to GitHub URL
        if url.startswith('../../Portfolio_Dev/'):
            resolved = "https://github.com/kEnder242/Portfolio_Dev/blob/main/" + url.replace('../../Portfolio_Dev/', '')
        elif url.startswith('../../'):
            resolved = "https://github.com/kEnder242/Dev_Lab/blob/main/" + url.replace('../../', '')
        elif url.startswith('./'):
            resolved = "https://github.com/kEnder242/HomeLabAI/blob/main/docs/" + url.replace('./', '')
        else:
            resolved = f"https://github.com/kEnder242/HomeLabAI/blob/main/docs/{url}"
            
        return f'[{text}]({resolved})'
        
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replacer, md_content)

def parse_protocols(content):
    # A BKM header looks like: ## BKM-001: The Cold-Start Protocol (Agent Orientation)
    header_pattern = re.compile(r'^## (BKM-\d{3}(?:\.\d+)?):\s*(.*?)$', re.MULTILINE)
    
    matches = list(header_pattern.finditer(content))
    bkm_list = []
    
    for i, match in enumerate(matches):
        bkm_id = match.group(1)
        bkm_title = match.group(2)
        
        start_idx = match.end()
        end_idx = matches[i+1].start() if i + 1 < len(matches) else len(content)
        
        body = content[start_idx:end_idx].strip()
        # Remove trailing horizontal rule divider if present
        body = re.sub(r'\n---+\s*$', '', body)
        body = body.strip()
        
        bkm_list.append({
            "id": bkm_id,
            "title": bkm_title,
            "body": body
        })
        
    return bkm_list

def generate_rows(bkm_list):
    html_rows = ""
    for item in bkm_list:
        body_with_absolute_links = convert_relative_links(item['body'])
        # Render markdown content to HTML
        html_body = markdown.markdown(body_with_absolute_links, extensions=['fenced_code', 'tables'])
        
        row = f"""                    <tr>
                        <td style="font-weight: bold; color: var(--accent-color); font-family: var(--font-stack); vertical-align: top; padding: 12px 15px; border-bottom: 1px solid #222;">{item['id']}</td>
                        <td style="vertical-align: top; padding: 12px 15px; border-bottom: 1px solid #222;">
                            <div style="font-weight: bold; color: var(--heading-color); font-size: 0.95rem; margin-bottom: 8px;">{item['title']}</div>
                            <div class="protocol-body" style="font-size: 0.85rem; color: var(--text-color); line-height: 1.5;">
                                {html_body}
                            </div>
                        </td>
                    </tr>"""
        html_rows += row + "\n"
    return html_rows

def main():
    if not os.path.exists(SOURCE_MD):
        print(f"Error: {SOURCE_MD} not found.")
        return
        
    with open(SOURCE_MD, 'r') as f:
        md_content = f.read()
        
    bkm_list = parse_protocols(md_content)
    if not bkm_list:
        print("Error: No BKMs parsed from Protocols.md.")
        return
        
    new_rows = generate_rows(bkm_list)
    
    with open(TEMPLATE_HTML, 'r') as f:
        html_content = f.read()
        
    start_tag = "<tbody>"
    end_tag = "</tbody>"
    
    start_idx = html_content.find(start_tag) + len(start_tag)
    end_idx = html_content.find(end_tag)
    
    if start_idx == -1 or end_idx == -1:
        print("Error: tbody tags not found in template HTML.")
        return
        
    updated_html = html_content[:start_idx] + "\n" + new_rows + "                    " + html_content[end_idx:]
    
    with open(OUTPUT_HTML, 'w') as f:
        f.write(updated_html)
        
    print(f"✅ Successfully compiled {OUTPUT_HTML} from {SOURCE_MD}")

if __name__ == "__main__":
    main()
