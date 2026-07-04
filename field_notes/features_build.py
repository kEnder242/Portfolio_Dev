#!/usr/bin/env python3
# features_build.py [v1.0]
# Purpose: Generate features.html from FeatureTracker.md with cross-linking, status styling, and markdown description support.

import os
import re
import markdown

SOURCE_MD = "/home/jallred/Dev_Lab/Portfolio_Dev/FeatureTracker.md"
TEMPLATE_HTML = "/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/features.html"
OUTPUT_HTML = "/home/jallred/Dev_Lab/Portfolio_Dev/field_notes/features.html"

def convert_internal_links(md_content):
    # Convert [FEAT-XXX] references to markdown hash links: [FEAT-XXX](#FEAT-XXX)
    md_content = re.sub(r'\[FEAT-(\d{3}(?:\.\d+)?)\]', r'[FEAT-\1](#FEAT-\1)', md_content)
    # Convert [SCAR #X] references to lookups or just keep them formatted
    return md_content

def parse_feature_block(block):
    # Matches fields like **Logic:** or **Status:** at the start of a line or block
    field_pattern = re.compile(r'(?:^|\n)\*\*([^*:]+):\*\*')
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
        fields[field_name] = field_value
        
    return intro, fields

def parse_feature_tracker(content):
    # Features start with ## [FEAT-XXX] Title
    header_pattern = re.compile(r'^## \[(FEAT-\d{3}(?:\.\d+)?)\]\s*(.*?)$', re.MULTILINE)
    matches = list(header_pattern.finditer(content))
    
    features = []
    for i, match in enumerate(matches):
        feat_id = match.group(1)
        feat_title = match.group(2)
        
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
        # Determine status and class
        status = item['fields'].get('Status', 'UNKNOWN')
        status_upper = status.upper()
        
        if "ACTIVE" in status_upper or "UNITY-ALIGNED" in status_upper:
            status_class = "impact-live"
        elif "DESIGN" in status_upper or "TRANSFORMING" in status_upper:
            status_class = "impact-design"
        elif "ARCHIVED" in status_upper or "DORMANT" in status_upper:
            status_class = "impact-archived"
        else:
            status_class = "impact-stable"
            
        # Build specification column content
        spec_content = f'<div style="font-weight: bold; color: var(--heading-color); font-size: 0.95rem; margin-bottom: 8px;">{item["title"]}</div>'
        
        if item['intro']:
            intro_md = convert_internal_links(item['intro'])
            spec_content += f'<div style="font-size: 0.85rem; color: #aaa; margin-bottom: 10px;">{markdown.markdown(intro_md)}</div>'
            
        for f_name, f_val in item['fields'].items():
            if f_name == 'Status':
                continue
                
            f_val_md = convert_internal_links(f_val)
            f_val_html = markdown.markdown(f_val_md, extensions=['fenced_code', 'tables'])
            
            # Format the output beautifully
            spec_content += f"""
            <div style="margin-bottom: 8px;">
                <span class="field-label">{f_name}</span>
                <div class="feature-body" style="font-size: 0.85rem; color: var(--text-color); line-height: 1.5; margin-left: 10px; margin-top: 4px;">
                    {f_val_html}
                </div>
            </div>"""
            
        row = f"""                    <tr id="{item['id']}">
                        <td style="font-weight: bold; color: var(--accent-color); font-family: var(--font-stack); vertical-align: top; padding: 12px 15px; border-bottom: 1px solid #222;">{item['id']}</td>
                        <td style="vertical-align: top; padding: 12px 15px; border-bottom: 1px solid #222;">
                            {spec_content}
                        </td>
                        <td style="vertical-align: top; padding: 12px 15px; border-bottom: 1px solid #222;">
                            <span class="impact-badge {status_class}">{status}</span>
                        </td>
                    </tr>"""
        html_rows += row + "\n"
        
    return html_rows

def main():
    if not os.path.exists(SOURCE_MD):
        print(f"Error: {SOURCE_MD} not found.")
        return
        
    with open(SOURCE_MD, 'r') as f:
        content = f.read()
        
    features = parse_feature_tracker(content)
    if not features:
        print("Error: No features parsed from FeatureTracker.md.")
        return
        
    new_rows = generate_rows(features)
    
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
