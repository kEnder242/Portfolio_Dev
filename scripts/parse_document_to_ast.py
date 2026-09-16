#!/usr/bin/env python3
"""
[SPR-82.1] Generic Document Ingestion -> Canonical Two-Tier AST
================================================================
Parses raw Markdown, plain text, or JSON document content into the canonical
two-tier AST schema consumed by Writer Studio (SPRINT_PLAN_SPR_82_0.md §3):

    Root      : { title, bone_collection[], _candidate_pool[], sections[] }
    Section   : { id, heading, bone_collection[], _candidate_pool[], paragraphs[] }
    Paragraph : { id, text, bullet_type, citations[], bone_collection[], _candidate_pool[] }

Tri-Phase Lifecycle alignment (SPR-82.0):
  Phase 1 DISCOVER (this module): detected citation tokens (FEAT-xxx, BKM-xxx,
  WIS-xxx, PHL-xxx, DISC-xxx, LAB-xxx, GEM-xxx, PROTO-xxx, ARXIV:nnnn.nnnnn,
  doi:...) are deposited into `_candidate_pool[]`. `bone_collection[]` starts
  empty at every tier because nothing has been curated yet (Phase 2 CURATE
  promotes bones into `bone_collection[]`).

Usage:
    from parse_document_to_ast import parse_document
    ast = parse_document(markdown_text, title="Staff Resume", source_format="markdown")
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Citation token detectors (DISCOVER phase) — one combined regex preserves
# left-to-right document order; trailing sentence punctuation is stripped
# per token inside detect_citations().
# ---------------------------------------------------------------------------
_ALL_TOKEN = re.compile(
    r"\b(?:PHL|DISC|FEAT|BKM|PROTO|ARXIV|GEM|WIS|LAB)-[A-Za-z0-9_.\-]+"
    r"|\b(?:arXiv|ARXIV):\d{4}\.\d{4,5}"
    r"|\bdoi:[A-Za-z0-9_.\-/]+",
    re.IGNORECASE,
)

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
# Markdown auto-detection probe (MULTILINE: a heading marker anywhere in the text).
_HEADING_MARKER_RE = re.compile(r"^#{1,6}\s+", re.MULTILINE)
_BULLET_RE = re.compile(r"^\s*(?:[-*+]\s+|(?:\d+\.)\s+)(.*)$")
_STAR_BULLET_RE = re.compile(r"^\s*\*\s")
_LEADING_BULLET_RE = re.compile(r"^[•▪◦\-*+]\s|^\d+[.)]\s")

DEFAULT_TITLE = "Untitled Document"
PRE_HEADING_SECTION = "Preamble"


def detect_citations(text: str) -> List[str]:
    """Discover citation tokens in document text (deduplicated, first-seen order).

    A single left-to-right scan preserves document order; trailing sentence
    punctuation ('.', ',', ';', ...) is stripped from each discovered token.
    """
    found: List[str] = []
    seen = set()
    for match in _ALL_TOKEN.finditer(text or ""):
        token = match.group(0).rstrip(".,;:!?)]}\"'")
        if not token:
            continue
        if token not in seen:
            seen.add(token)
            found.append(token)
    return found


def _merge_unique(pool: List[str], discovered: List[str]) -> List[str]:
    """Append discovered tokens to an existing pool, preserving order, no duplicates."""
    out = list(pool)
    seen = set(out)
    for token in discovered:
        if token not in seen:
            seen.add(token)
            out.append(token)
    return out


def _clean_heading(text: str) -> str:
    """Strip markdown heading markers and inline bold/italic/code formatting."""
    cleaned = re.sub(r"^#+\s*", "", text)
    cleaned = re.sub(r"\s+#+\s*$", "", cleaned)
    cleaned = cleaned.replace("**", "").replace("__", "").replace("`", "")
    cleaned = re.sub(r"\*([^*]+)\*", r"\1", cleaned)
    return cleaned.strip()


def _entry(
    text: str,
    bullet_type: str,
    counter: int,
    explicit_citations: Optional[List[str]] = None,
) -> tuple[Dict[str, Any], int]:
    counter += 1
    return (
        {
            "id": f"p-{counter:02d}",
            "bullet_type": bullet_type,
            "text": text,
            "citations": list(explicit_citations or []),
            "bone_collection": [],
            "_candidate_pool": detect_citations(text),
        },
        counter,
    )


def _emit_entries(lines: List[str]) -> List[Dict[str, str]]:
    """Group raw section lines into bullet entries and paragraph blocks.

    - A line starting with '-', '*', '+' or '1.' opens a bullet entry; indented or
      plain continuation lines join it until the next bullet, blank, or heading.
    - Any other non-blank run becomes a paragraph entry.
    """
    entries: List[Dict[str, str]] = []
    i, n = 0, len(lines)
    while i < n:
        stripped = lines[i].strip()
        if not stripped:
            i += 1
            continue
        bullet_match = _BULLET_RE.match(lines[i])
        if bullet_match:
            parts = [bullet_match.group(1).strip()]
            i += 1
            while i < n:
                nxt = lines[i].strip()
                if not nxt or _BULLET_RE.match(lines[i]) or _HEADING_RE.match(lines[i]):
                    break
                if lines[i][0] in (" ", "\t") or _STAR_BULLET_RE.match(lines[i]):
                    parts.append(nxt)
                    i += 1
                else:
                    break
            text = " ".join(part for part in parts if part).strip()
            if text:
                entries.append({"bullet_type": "bullet", "text": text})
            continue
        block = [stripped]
        i += 1
        while i < n:
            nxt = lines[i].strip()
            if not nxt or _BULLET_RE.match(lines[i]) or _HEADING_RE.match(lines[i]):
                break
            block.append(nxt)
            i += 1
        text = " ".join(block).strip()
        if text:
            entries.append({"bullet_type": "paragraph", "text": text})
    return entries


def _entries_to_paragraphs(entries: List[Dict[str, str]], par_counter: int) -> tuple[List[Dict[str, Any]], int]:
    pars: List[Dict[str, Any]] = []
    for raw in entries:
        entry, par_counter = _entry(raw["text"], raw["bullet_type"], par_counter)
        pars.append(entry)
    return pars, par_counter


def parse_markdown(text: str, title: Optional[str] = None, slug: Optional[str] = None) -> Dict[str, Any]:
    """Parse Markdown into the two-tier AST.

    A first-level `# Heading` in the document is consumed as the document title
    (an explicit `title` argument is only a fallback when no H1 exists); every
    other heading (any level) opens a new section in document order. Heading
    levels are preserved as `level` metadata (hierarchy is flattened into the
    canonical single-level `sections[]` collection).
    """
    doc_title = None  # self-describing H1 wins; explicit title is the fallback
    sections: List[Dict[str, Any]] = []
    sec_counter, par_counter = 0, 0
    cur_sec: Optional[Dict[str, Any]] = None
    cur_lines: List[str] = []

    def close_section() -> None:
        nonlocal cur_sec, cur_lines, par_counter
        if cur_sec is None:
            cur_lines = []
            return
        cur_sec["paragraphs"], par_counter = _entries_to_paragraphs(_emit_entries(cur_lines), par_counter)
        sections.append(cur_sec)
        cur_sec = None
        cur_lines = []

    for line in text.splitlines():
        heading_match = _HEADING_RE.match(line)
        if heading_match:
            level = len(heading_match.group(1))
            heading_text = _clean_heading(heading_match.group(2))
            if not heading_text:
                continue
            if doc_title is None and level == 1:
                doc_title = heading_text
                continue
            close_section()
            sec_counter += 1
            cur_sec = {
                "id": f"sec-{sec_counter:02d}",
                "heading": heading_text,
                "level": level,
                "bone_collection": [],
                "_candidate_pool": detect_citations(heading_text),
            }
            continue
        if cur_sec is None:
            if not line.strip():
                continue  # blank lines before the first section must not open a Preamble
            sec_counter += 1
            cur_sec = {
                "id": f"sec-{sec_counter:02d}",
                "heading": PRE_HEADING_SECTION,
                "level": 0,
                "bone_collection": [],
                "_candidate_pool": [],
            }
        cur_lines.append(line)
    close_section()

    if doc_title is None:
        doc_title = (title or "").strip() or (slug or "").strip() or DEFAULT_TITLE
    return {
        "title": doc_title,
        "bone_collection": [],
        "_candidate_pool": [],
        "sections": sections,
    }


def parse_plain_text(text: str, title: Optional[str] = None, slug: Optional[str] = None) -> Dict[str, Any]:
    """Parse plain text into the two-tier AST (single "Overview" section).

    Bullet lines ('-', '*', '+', '1.') become bullet entries; blank-line separated
    runs become paragraph entries. No heading detection is attempted for plain text.
    """
    doc_title = (title or "").strip() or (slug or "").strip() or DEFAULT_TITLE
    pars, _ = _entries_to_paragraphs(_emit_entries(text.splitlines()), 0)
    return {
        "title": doc_title,
        "bone_collection": [],
        "_candidate_pool": [],
        "sections": [
            {
                "id": "sec-01",
                "heading": "Overview",
                "level": 0,
                "bone_collection": [],
                "_candidate_pool": [],
                "paragraphs": pars,
            }
        ],
    }


def _normalize_canonical_ast(data: Dict[str, Any], title: Optional[str] = None, slug: Optional[str] = None) -> Dict[str, Any]:
    """Pass an already-canonical AST through the intake pipeline.

    Explicit `citations` and existing pool/bone entries are preserved; new citation
    tokens discovered in text (Phase 1 DISCOVER) are merged into `_candidate_pool[]`.
    """
    doc_title = (title or "").strip() or str(data.get("title") or "").strip() or (slug or "").strip() or DEFAULT_TITLE
    root_pool = [str(c) for c in (data.get("_candidate_pool") or [])]
    sections: List[Dict[str, Any]] = []
    sec_counter, par_counter = 0, 0
    for sec in data.get("sections") or []:
        if not isinstance(sec, dict):
            raise ValueError("JSON document: every section must be an object")
        sec_counter += 1
        sec_id = str(sec.get("id") or f"sec-{sec_counter:02d}")
        heading = str(sec.get("heading") or "").strip() or f"Section {sec_counter:02d}"
        heading_hits = detect_citations(heading)
        root_pool = _merge_unique(root_pool, heading_hits)
        pars: List[Dict[str, Any]] = []
        for par in sec.get("paragraphs") or []:
            if not isinstance(par, dict):
                raise ValueError("JSON document: every paragraph must be an object")
            text = str(par.get("text") or "").strip()
            if not text:
                continue
            par_counter += 1
            explicit = [str(c) for c in (par.get("citations") or [])]
            bullet_type = par.get("bullet_type")
            if bullet_type not in ("bullet", "paragraph"):
                bullet_type = "bullet" if _LEADING_BULLET_RE.match(text) else "paragraph"
            pars.append({
                "id": str(par.get("id") or f"p-{par_counter:02d}"),
                "bullet_type": bullet_type,
                "text": text,
                "citations": explicit,
                "bone_collection": [str(b) for b in (par.get("bone_collection") or [])],
                "_candidate_pool": _merge_unique(
                    [str(c) for c in (par.get("_candidate_pool") or [])], detect_citations(text)
                ),
            })
        sections.append({
            "id": sec_id,
            "heading": heading,
            "level": sec.get("level", 0),
            "bone_collection": [str(b) for b in (sec.get("bone_collection") or [])],
            "_candidate_pool": _merge_unique(
                [str(c) for c in (sec.get("_candidate_pool") or [])], heading_hits
            ),
            "paragraphs": pars,
        })
    return {
        "title": doc_title,
        "bone_collection": [str(b) for b in (data.get("bone_collection") or [])],
        "_candidate_pool": root_pool,
        "sections": sections,
    }


def _append_json_value(pars: List[Dict[str, Any]], value: Any, par_counter: int) -> int:
    """Render a generic JSON value into paragraph entries (str -> paragraph, list -> bullets)."""
    if isinstance(value, str):
        if value.strip():
            entry, par_counter = _entry(value, "paragraph", par_counter)
            pars.append(entry)
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, str) and item.strip():
                entry, par_counter = _entry(item, "bullet", par_counter)
                pars.append(entry)
            elif isinstance(item, dict):
                for sub in item.values():
                    if isinstance(sub, str) and sub.strip():
                        entry, par_counter = _entry(sub, "bullet", par_counter)
                        pars.append(entry)
    elif value is not None:
        rendered = str(value).strip()
        if rendered:
            entry, par_counter = _entry(rendered, "paragraph", par_counter)
            pars.append(entry)
    return par_counter


def _convert_generic_json(data: Dict[str, Any], title: Optional[str] = None, slug: Optional[str] = None) -> Dict[str, Any]:
    """Convert an arbitrary JSON object into the two-tier AST.

    Every top-level key (except `title`) becomes a section: string values -> paragraph
    entries, list values -> bullet entries, nested objects -> flattened child entries.
    """
    doc_title = (title or "").strip() or str(data.get("title") or "").strip() or (slug or "").strip() or DEFAULT_TITLE
    sections: List[Dict[str, Any]] = []
    sec_counter, par_counter = 0, 0
    for key, value in data.items():
        if key == "title":
            continue
        sec_counter += 1
        heading = str(key).strip() or f"Section {sec_counter:02d}"
        section: Dict[str, Any] = {
            "id": f"sec-{sec_counter:02d}",
            "heading": heading,
            "level": 1,
            "bone_collection": [],
            "_candidate_pool": detect_citations(heading),
            "paragraphs": [],
        }
        if isinstance(value, dict):
            for sub_value in value.values():
                par_counter = _append_json_value(section["paragraphs"], sub_value, par_counter)
        else:
            par_counter = _append_json_value(section["paragraphs"], value, par_counter)
        sections.append(section)
    return {
        "title": doc_title,
        "bone_collection": [],
        "_candidate_pool": [],
        "sections": sections,
    }


def parse_json_document(content: Any, title: Optional[str] = None, slug: Optional[str] = None) -> Dict[str, Any]:
    """Parse a JSON document (string or already-parsed dict) into the two-tier AST.

    Canonical ASTs (containing `sections`) are normalized in place; arbitrary JSON
    objects are converted key-by-key into sections.
    """
    data = content
    if isinstance(content, str):
        data = json.loads(content)  # raises ValueError on malformed JSON
    if not isinstance(data, dict):
        raise ValueError("JSON document root must be an object ({...})")
    if isinstance(data.get("sections"), list):
        return _normalize_canonical_ast(data, title=title, slug=slug)
    return _convert_generic_json(data, title=title, slug=slug)


def parse_document(
    content: Any,
    title: Optional[str] = None,
    slug: Optional[str] = None,
    source_format: Optional[str] = None,
) -> Dict[str, Any]:
    """Parse raw Markdown, plain text, or JSON document content into the canonical two-tier AST.

    Format resolution order: explicit `source_format` hint > JSON detection (content is a
    dict, or a string that json.loads() accepts) > Markdown (heading markers present) >
    plain text.
    """
    fmt = (source_format or "").strip().lower()
    if fmt in ("json", "application/json"):
        return parse_json_document(content, title=title, slug=slug)
    if fmt in ("md", "markdown"):
        if not isinstance(content, str):
            raise ValueError("Markdown content must be a string")
        return parse_markdown(content, title=title, slug=slug)
    if fmt in ("txt", "text", "plain", "plaintext"):
        if not isinstance(content, str):
            raise ValueError("Plain text content must be a string")
        return parse_plain_text(content, title=title, slug=slug)

    if isinstance(content, dict):
        return parse_json_document(content, title=title, slug=slug)
    if isinstance(content, str):
        stripped = content.strip()
        if not stripped:
            raise ValueError("Document content is empty")
        parsed = None
        try:
            parsed = json.loads(stripped)
        except ValueError:
            parsed = None
        if isinstance(parsed, dict):
            return parse_json_document(parsed, title=title, slug=slug)
        if _HEADING_MARKER_RE.search(stripped):
            return parse_markdown(content, title=title, slug=slug)
        return parse_plain_text(content, title=title, slug=slug)
    raise ValueError("Document content must be a string (Markdown/plain text/JSON) or a parsed JSON object")


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse a raw document into the canonical two-tier AST (JSON to stdout).")
    parser.add_argument("file", nargs="?", help="input file (stdin if omitted)")
    parser.add_argument("--title", default=None, help="explicit document title")
    parser.add_argument("--slug", default=None, help="document slug (fallback title)")
    parser.add_argument("--format", default=None, help="source format hint: markdown|text|json")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as fh:
            content = fh.read()
    else:
        content = sys.stdin.read()
    ast = parse_document(content, title=args.title, slug=args.slug, source_format=args.format)
    print(json.dumps(ast, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
