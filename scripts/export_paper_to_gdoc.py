#!/usr/bin/env python3
"""
[FEAT-595] Round-Trip Resume Exporter
Compiles Paper AST (PAPER-RESUME_v1.json) and style schema into:
1. Plain text buffer with calculated character ranges for formatting.
2. Structured batch formatting requests for Google Docs API (bolding headers, bolding first 3 words of bullets, italicizing context lines).
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PAPERS_DIR = BASE_DIR / "field_notes" / "data" / "papers"


def compile_paper_to_formatted_doc(paper_path: Path, style_path: Path):
    paper = json.loads(paper_path.read_text(encoding="utf-8"))
    style = json.loads(style_path.read_text(encoding="utf-8")) if style_path.exists() else {}
    
    text_buffer = []
    format_ranges = [] # list of {"start": int, "end": int, "style": "bold" | "italic" | "heading1" | "heading2" | "title"}
    
    cursor = 0
    
    def append_text(txt: str, style_type: str = None):
        nonlocal cursor
        start = cursor
        text_buffer.append(txt)
        cursor += len(txt)
        end = cursor
        if style_type:
            format_ranges.append({"start": start, "end": end, "style": style_type})
        return start, end

    # 1. Author Name (Title)
    author = paper.get("author", "Jason Allred")
    append_text(author + "\n", "title")
    
    # 2. Contact Bar
    contact = paper.get("contact", {})
    contact_line = f"{contact.get('location', '')} | {contact.get('email', '')} | {contact.get('phone', '')} | {contact.get('linkedin', '')} | {contact.get('github', '')}\n\n"
    append_text(contact_line)
    
    # 3. Iterate Sections
    for sec in paper.get("sections", []):
        sec_id = sec.get("section_id", "")
        heading = sec.get("heading", "")
        
        if sec_id == "sec_title":
            # Active Title
            active_node = sec.get("nodes", [{}])[0]
            title_text = active_node.get("text", "")
            append_text(title_text + "\n\n", "bold")
            continue
            
        if heading:
            append_text(heading + "\n", "heading1")
            
        if sec_id == "sec_summary":
            for node in sec.get("nodes", []):
                append_text(node.get("text", "") + "\n\n")
                
        elif sec_id == "sec_skills":
            for node in sec.get("nodes", []):
                cat = node.get("category", "")
                txt = node.get("text", "")
                append_text(f"- {cat}: ", "bold")
                append_text(txt + "\n")
            append_text("\n")
            
        elif sec_id == "sec_experience":
            for role in sec.get("roles", []):
                company = role.get("company", "")
                title = role.get("title", "")
                period = role.get("period", "")
                location = role.get("location", "")
                context_line = role.get("context_line", "")
                
                # Role Header
                append_text(f"{company} – {location}\n", "bold")
                append_text(f"{title} ({period})\n", "bold")
                
                # Context Line (Italicized per Sharghi Recruiter Rubric)
                if context_line:
                    append_text(context_line + "\n", "italic")
                    
                # Bullets
                for bullet in role.get("bullets", []):
                    b_text = bullet.get("text", "")
                    words = b_text.split(" ")
                    lead_in_count = min(3, len(words))
                    lead_in = " ".join(words[:lead_in_count])
                    remainder = " ".join(words[lead_in_count:])
                    
                    append_text("- ")
                    # Bold first 3 words (First 3 Words power verb rule)
                    append_text(lead_in + " ", "bold")
                    append_text(remainder + "\n")
                    
                append_text("\n")
                
        elif sec_id == "sec_education":
            for node in sec.get("nodes", []):
                inst = node.get("institution", "")
                deg = node.get("degree", "")
                period = node.get("period", "")
                append_text(f"- {deg} – {inst} ({period})\n")
            append_text("\n")

    full_text = "".join(text_buffer)
    return {
        "title": f"{author} Resume - Sept2026",
        "full_text": full_text,
        "format_ranges": format_ranges
    }


def main():
    paper_path = PAPERS_DIR / "PAPER-RESUME_v1.json"
    style_path = PAPERS_DIR / "style_resume_v1.json"
    
    doc_payload = compile_paper_to_formatted_doc(paper_path, style_path)
    output_path = PAPERS_DIR / "export_payload_resume_v1.json"
    output_path.write_text(json.dumps(doc_payload, indent=2), encoding="utf-8")
    
    print(f"✅ Compiled Document Payload -> {output_path}")
    print(f"📄 Total Characters: {len(doc_payload['full_text'])}")
    print(f"🎨 Formatting Directives: {len(doc_payload['format_ranges'])} ranges")


if __name__ == "__main__":
    main()
