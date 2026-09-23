#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dna_macro_compiler.py
[FEAT-602 / FEAT-603 / FEAT-604]

Self-Contained DNA Macro Citation & Markdown Grammar Engine.
Parses, serializes, and compiles Markdown papers with embedded DNA macros.
Guarantees papers are readable offline in any markdown viewer without requiring ChromaDB.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
LAB_ROOT = REPO_ROOT.parent
BONES_DIR = REPO_ROOT / "field_notes" / "data" / "bones"
DNA_DIR = REPO_ROOT / "dna"

# Regex matching DNA Macro citations in markdown comments or raw blocks:
# Examples:
#   <!-- [WIS-482:R2 style=paragraph lens=Active] -->
#   <!-- [FEAT-600:R1 style=bullet] -->
#   <!-- [PHL-037:M1 style=callout] -->
#   [WIS-482:R1]
MACRO_COMMENT_PATTERN = re.compile(
    r"<!--\s*\[(?P<id>[A-Z0-9_-]+)(?::(?P<rev>[A-Z0-9_]+))?(?P<attrs_in>[^\]]*)\](?P<attrs_out>[^>]*)-->",
    re.IGNORECASE
)

MACRO_INLINE_PATTERN = re.compile(
    r"^\[(?P<id>[A-Z0-9_-]+)(?::(?P<rev>[A-Z0-9_]+))?(?P<attrs_in>[^\]]*)\](?P<attrs_out>.*)$",
    re.MULTILINE
)


class DNAMacro:
    def __init__(self, card_id: str, revision: str = "R1", style: str = "paragraph", lens: Optional[str] = None, extra_attrs: Optional[Dict[str, str]] = None):
        self.card_id = card_id.upper()
        self.revision = revision.upper()
        self.style = style.lower()
        self.lens = lens
        self.extra_attrs = extra_attrs or {}

    def to_macro_comment(self) -> str:
        attrs = [f"style={self.style}"]
        if self.lens:
            attrs.append(f"lens={self.lens}")
        for k, v in sorted(self.extra_attrs.items()):
            attrs.append(f"{k}={v}")
        attr_str = " " + " ".join(attrs) if attrs else ""
        return f"<!-- [{self.card_id}:{self.revision}{attr_str}] -->"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.card_id,
            "revision": self.revision,
            "style": self.style,
            "lens": self.lens,
            "extra_attrs": self.extra_attrs
        }


def parse_macro_string(macro_str: str) -> Optional[DNAMacro]:
    """Parse a single macro comment or inline macro into a DNAMacro object."""
    m = MACRO_COMMENT_PATTERN.search(macro_str)
    if not m:
        m = MACRO_INLINE_PATTERN.search(macro_str)
    if not m:
        return None

    card_id = m.group("id").strip()
    rev = m.group("rev") or "R1"
    raw_attrs = (m.group("attrs_in") or "") + " " + (m.group("attrs_out") or "")

    style = "paragraph"
    lens = None
    extra_attrs = {}

    for token in raw_attrs.strip().split():
        if "=" in token:
            k, v = token.split("=", 1)
            k = k.strip().lower()
            v = v.strip().strip('"').strip("'")
            if k == "style":
                style = v
            elif k == "lens":
                lens = v
            else:
                extra_attrs[k] = v

    return DNAMacro(card_id=card_id, revision=rev, style=style, lens=lens, extra_attrs=extra_attrs)


def parse_markdown_with_dna_macros(markdown_text: str) -> List[Dict[str, Any]]:
    """
    Parse a full markdown document into an ordered list of vertebrae chunks.
    Each chunk contains the optional DNAMacro and the associated human-readable text.
    """
    lines = markdown_text.splitlines()
    chunks = []
    current_macro: Optional[DNAMacro] = None
    current_text_lines = []

    for line in lines:
        match = MACRO_COMMENT_PATTERN.search(line)
        if match:
            # If we already had an active block, flush it
            if current_macro or current_text_lines:
                raw_body = "\n".join(current_text_lines).strip()
                if raw_body or current_macro:
                    chunks.append({
                        "macro": current_macro.to_dict() if current_macro else None,
                        "text": raw_body
                    })
                current_text_lines = []
            current_macro = parse_macro_string(match.group(0))
        else:
            current_text_lines.append(line)

    if current_macro or current_text_lines:
        raw_body = "\n".join(current_text_lines).strip()
        if raw_body or current_macro:
            chunks.append({
                "macro": current_macro.to_dict() if current_macro else None,
                "text": raw_body
            })

    return chunks


def load_bone_collection(collection_name_or_file: str) -> Optional[Dict[str, Any]]:
    """Load a 1:1 bone collection scratchpad from Portfolio_Dev/field_notes/data/bones/."""
    target = BONES_DIR / collection_name_or_file
    if not target.exists() and not collection_name_or_file.endswith(".json"):
        target = BONES_DIR / f"{collection_name_or_file}.json"
    if not target.exists():
        # Fallback to legacy single file
        legacy = REPO_ROOT / "field_notes" / "data" / "bone_collections.json"
        if legacy.exists():
            try:
                with open(legacy, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for col in data:
                        if col.get("id") == collection_name_or_file or col.get("name") == collection_name_or_file:
                            return col
            except Exception:
                pass
        return None

    try:
        with open(target, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def reconstruct_source_from_bones(bone_data: Dict[str, Any], revision_lens: str = "Original Verbatim") -> str:
    """
    [FEAT-604 / BKM-024]
    Reconstructs the original source text from a 1:1 Bone Collection.
    Guarantees exact mathematical identity:
      Delta(Original Source, Reconstruct(Bones, R1)) == 0
    """
    bones = bone_data.get("bones", [])
    paragraphs = []

    for b in sorted(bones, key=lambda x: x.get("sequence", 0)):
        # Look for target revision or verbatim origin
        text = None
        if revision_lens == "Original Verbatim" and b.get("origin_verbatim"):
            text = b.get("origin_verbatim").strip()
        else:
            for rev in b.get("revisions", []):
                if rev.get("lens") == revision_lens:
                    text = rev.get("text", "").strip()
                    break
            if text is None and b.get("revisions"):
                text = b.get("revisions")[0].get("text", "").strip()
            elif text is None:
                text = b.get("origin_verbatim", "").strip()

        if text:
            paragraphs.append(text)

    return "\n\n".join(paragraphs)


def compile_paper_to_markdown(bone_collections: List[Dict[str, Any]], lens: Optional[str] = None) -> str:
    """
    [FEAT-603]
    Weaves multiple bone collections into a unified composite markdown paper with embedded DNA macros.
    """
    rendered_blocks = []

    for col in bone_collections:
        col_name = col.get("name", "Document Section")
        rendered_blocks.append(f"## {col_name}\n")
        
        for bone in sorted(col.get("bones", []), key=lambda x: x.get("sequence", 0)):
            card_id = bone.get("id", "DNA-000")
            
            # Select matching mutation or revision for the target lens
            body_text = None
            rev_tag = "R1"
            
            if lens:
                for mut in bone.get("mutations", []):
                    if mut.get("lens", "").lower() == lens.lower():
                        body_text = mut.get("text", "").strip()
                        rev_tag = mut.get("id", "M1").upper()
                        break
            
            if not body_text:
                for rev in bone.get("revisions", []):
                    if lens and rev.get("lens", "").lower() == lens.lower():
                        body_text = rev.get("text", "").strip()
                        rev_tag = f"R{rev.get('version', 1)}"
                        break
                if not body_text and bone.get("revisions"):
                    body_text = bone.get("revisions")[0].get("text", "").strip()
                    rev_tag = f"R{bone.get('revisions')[0].get('version', 1)}"
                elif not body_text:
                    body_text = bone.get("origin_verbatim", "").strip()

            macro = DNAMacro(card_id=card_id, revision=rev_tag, lens=lens)
            rendered_blocks.append(f"{macro.to_macro_comment()}\n{body_text}\n")

    return "\n".join(rendered_blocks).strip()


if __name__ == "__main__":
    import sys
    print("[dna_macro_compiler] Ready. Self-contained DNA Macro Citation Engine initialized.")
