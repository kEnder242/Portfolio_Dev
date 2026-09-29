#!/usr/bin/env python3
"""
[FEAT-601 / Sprint 94 Story 94.1] DNA Manifest Bridge for VIBE & INSPIRATION Domains

Bridges the canonical bone collections under ``dna/`` into the flat
``field_notes/data/dna_manifest.json`` card catalog that Writer Studio and
Projection Studio read from.

Responsibilities:

1. Ingest ``dna/vibe_data.json`` under the manifest ``"vibe"`` key, guaranteeing
   every card carries a descriptive top-level ``"title"`` and ``"domain"``.
2. Ingest ``dna/inspiration_data.json`` under the manifest ``"inspiration"``
   key, guaranteeing the key always exists (empty list when the source holds no
   records) and every card is titled and domain-tagged.
3. Backfill descriptive top-level ``"title"`` values for the PHL cards so
   dropdowns render names rather than blank rows. ``synthesis.title`` is the
   authoritative carrier; the top-level field is a promoted projection of it.
4. Bar ``RDNA`` / ``RESUME`` cards from acting as active lenses (WIS-484).
   Those domains are ground truth about the author, not stylistic mutations
   that may be applied to a document. The bar is recorded declaratively on
   each card and in a manifest-level policy registry, and is also exposed
   programmatically via :func:`lens_eligible_cards` for the projection engine
   (Story 94.6) to consume.

Design invariants:
    * Idempotent. Re-running merges by card ``id`` and never duplicates cards,
      so the script is safe on a nightly cadence.
    * Non-destructive. Only ``title`` / ``domain`` / lens-bar fields are added;
      every existing comment, field and ordering is preserved.
    * Atomic. The manifest is written to a sibling temp file, fsynced, then
      ``os.replace``-d into position, so a reader never observes a torn file.
    * Byte-stable. The manifest is serialized with the same settings that
      produced it (``indent=2``, ``ensure_ascii=True``), so the diff contains
      only this story's additions.

Usage:
    python3 dna_manifest_bridge.py            # ingest, normalize, write
    python3 dna_manifest_bridge.py --dry-run  # report changes, write nothing
    python3 dna_manifest_bridge.py --verify   # assert post-conditions only
"""

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

BASE_DIR = Path(__file__).resolve().parent.parent
DNA_DIR = BASE_DIR / "dna"
DATA_DIR = BASE_DIR / "field_notes" / "data"

MANIFEST_PATH = DATA_DIR / "dna_manifest.json"
VIBE_SOURCE_PATH = DNA_DIR / "vibe_data.json"
INSPIRATION_SOURCE_PATH = DNA_DIR / "inspiration_data.json"

# Domain label assigned to every ingested card.
VIBE_DOMAIN = "VIBE"
INSPIRATION_DOMAIN = "INSPIRATION"

# Manifest key -> (source bone file, domain label) for the bridged collections.
BRIDGED_SOURCES: Tuple[Tuple[str, Path, str], ...] = (
    ("vibe", VIBE_SOURCE_PATH, VIBE_DOMAIN),
    ("inspiration", INSPIRATION_SOURCE_PATH, INSPIRATION_DOMAIN),
)

# Manifest keys whose cards are backfilled with descriptive titles.
# "wisdom" is retained as the legacy alias of the PHL card set and holds
# separate copies of the same cards, so both keys require the backfill.
TITLE_BACKFILL_KEYS: Tuple[str, ...] = ("philosophy", "wisdom")

# WIS-484: RDNA and RESUME cards are ground truth about the author, not
# stylistic mutations. They are barred from acting as active lenses.
LENS_BARRED_DOMAINS: Tuple[str, ...] = ("RDNA", "RESUME")
LENS_BARRED_KEYS: Tuple[str, ...] = ("rdna", "resume")
LENS_BAR_AUTHORITY = "WIS-484"

# Head-key order shared by every card shape in the manifest, so a newly
# projected title lands beside `id` instead of trailing after `metadata`.
CANONICAL_HEAD: Tuple[str, ...] = ("id", "title", "domain")

# Serialization contract of the existing manifest; verified byte-exact so the
# commit diff shows only this story's additions.
JSON_INDENT = 2
JSON_ENSURE_ASCII = True


# ---------------------------------------------------------------------------
# I/O primitives
# ---------------------------------------------------------------------------
def load_json(path: Path, default: Any = None) -> Any:
    """Load JSON from ``path``; return ``default`` when absent or unparseable."""
    if not path.exists():
        return default
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path} is not valid JSON: {exc}") from exc


def atomic_write_json(path: Path, payload: Any) -> None:
    """
    Serialize ``payload`` to ``path`` atomically.

    Writes a sibling temp file, flushes and fsyncs it to disk, then renames it
    over the target with ``os.replace`` (atomic on POSIX within a filesystem).
    A concurrent reader therefore observes either the pre-write or the
    post-write file, never a truncated one.
    """
    serialized = json.dumps(payload, indent=JSON_INDENT, ensure_ascii=JSON_ENSURE_ASCII)
    path.parent.mkdir(parents=True, exist_ok=True)
    handle_fd, tmp_name = tempfile.mkstemp(
        dir=str(path.parent), prefix=f".{path.name}.", suffix=".tmp"
    )
    try:
        with os.fdopen(handle_fd, "w", encoding="utf-8") as handle:
            handle.write(serialized)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    except BaseException:
        # Never leave a partial temp file behind on failure.
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)
        raise
    # Durably record the rename itself.
    dir_fd = os.open(str(path.parent), os.O_RDONLY)
    try:
        os.fsync(dir_fd)
    finally:
        os.close(dir_fd)


# ---------------------------------------------------------------------------
# Card normalization
# ---------------------------------------------------------------------------
def derive_title(card: Dict[str, Any]) -> str:
    """
    Resolve a descriptive title for ``card``.

    Precedence: an existing non-empty top-level ``title`` wins (a human- or
    agent-authored name outranks a derived one), then ``synthesis.title``,
    then ``origin.source``, then the card ``id`` as a last-resort stable
    identifier. Always returns a non-empty string.
    """
    for candidate in (
        card.get("title"),
        (card.get("synthesis") or {}).get("title"),
        (card.get("origin") or {}).get("source"),
        card.get("id"),
    ):
        if isinstance(candidate, str) and candidate.strip():
            return candidate.strip()
    return "Untitled"


def order_card_keys(card: Dict[str, Any]) -> Dict[str, Any]:
    """
    Reorder a card's head keys to the canonical ``id, title, domain`` prefix.

    Manifest cards are read by humans in diffs and by UI dropdowns, so a newly
    projected ``title`` must not be appended after ``metadata`` where it reads
    as an afterthought. This lifts the canonical head keys to the front and
    preserves the relative order of every remaining key.
    """
    ordered: Dict[str, Any] = {}
    for key in CANONICAL_HEAD:
        if key in card:
            ordered[key] = card[key]
    for key, value in card.items():
        if key not in ordered:
            ordered[key] = value
    return ordered


def normalize_card(card: Dict[str, Any], domain: Optional[str] = None) -> Dict[str, Any]:
    """
    Return ``card`` with a guaranteed descriptive ``title`` (and ``domain``).

    The card is copied, not mutated in place, and every pre-existing field is
    carried through untouched. ``title`` and ``domain`` are ordered to the
    canonical head position so the result matches sibling card shapes such as
    the ``discovery`` and ``rdna`` collections. Passing ``domain=None`` leaves
    any existing domain alone, for keys that do not carry a domain label.
    """
    normalized = dict(card)
    normalized["title"] = derive_title(card)
    if domain is not None:
        normalized["domain"] = domain
    return order_card_keys(normalized)


def ingest_domain(
    manifest: Dict[str, Any],
    key: str,
    source_cards: Iterable[Dict[str, Any]],
    domain: str,
) -> Tuple[int, int]:
    """
    Merge ``source_cards`` into ``manifest[key]`` idempotently.

    Cards are keyed by ``id``; an incoming card replaces the existing entry for
    the same id (bones are re-certified upstream, so the source wins) while
    unknown ids append in source order. Existing ordering is otherwise
    preserved, and the key is always created even when there is nothing to
    ingest, so consumers can rely on its presence.

    Returns ``(added, updated)`` counts.
    """
    incoming = [card for card in (source_cards or []) if isinstance(card, dict)]
    existing = manifest.get(key)
    if not isinstance(existing, list):
        existing = []

    index_by_id: Dict[str, int] = {}
    for position, card in enumerate(existing):
        if isinstance(card, dict) and isinstance(card.get("id"), str):
            index_by_id.setdefault(card["id"], position)

    merged: List[Dict[str, Any]] = list(existing)
    added = 0
    updated = 0
    for card in incoming:
        normalized = normalize_card(card, domain)
        card_id = normalized.get("id")
        if isinstance(card_id, str) and card_id in index_by_id:
            merged[index_by_id[card_id]] = normalized
            updated += 1
        else:
            if isinstance(card_id, str):
                index_by_id[card_id] = len(merged)
            merged.append(normalized)
            added += 1

    manifest[key] = merged
    return added, updated


def backfill_titles(manifest: Dict[str, Any], key: str) -> int:
    """
    Promote ``synthesis.title`` to a top-level ``title`` for every card in
    ``manifest[key]``. Cards that already have a non-empty top-level title are
    left untouched. Returns the number of cards backfilled.
    """
    cards = manifest.get(key)
    if not isinstance(cards, list):
        return 0
    backfilled = 0
    for position, card in enumerate(cards):
        if not isinstance(card, dict):
            continue
        existing = card.get("title")
        if isinstance(existing, str) and existing.strip():
            continue
        cards[position] = normalize_card(card)
        backfilled += 1
    return backfilled


# ---------------------------------------------------------------------------
# WIS-484 lens bar
# ---------------------------------------------------------------------------
def lens_exclusion_policy() -> Dict[str, Any]:
    """
    The manifest-level registry of barred lens domains.

    Downstream consumers read this to learn the rule in one lookup instead of
    hardcoding a domain blacklist of their own.
    """
    return {
        "barred_domains": list(LENS_BARRED_DOMAINS),
        "authority": LENS_BAR_AUTHORITY,
        "rationale": (
            "RDNA and RESUME cards are ground truth about the author. They are "
            "excluded from acting as active lenses, which may only restyle "
            "documents and must never author, overwrite or reframe source truth."
        ),
        "field_contract": {
            "lens_eligible": "False marks a card as barred from lens roles.",
            "lens_barred_by": "DNA anchor asserting the bar (WIS-484).",
            "lens_bar_reason": "Human-readable justification for the bar.",
        },
    }


def bar_lens_roles(manifest: Dict[str, Any]) -> int:
    """
    Stamp the WIS-484 lens bar onto every RDNA and RESUME card.

    The bar is applied by manifest key rather than by the card's ``domain``
    field, because RDNA cards carry no ``domain`` field at all. Returns the
    number of cards stamped.
    """
    reason = lens_exclusion_policy()["rationale"]
    stamped = 0
    for key in LENS_BARRED_KEYS:
        cards = manifest.get(key)
        if not isinstance(cards, list):
            continue
        for card in cards:
            if not isinstance(card, dict):
                continue
            card["lens_eligible"] = False
            card["lens_barred_by"] = LENS_BAR_AUTHORITY
            card["lens_bar_reason"] = reason
            stamped += 1
    return stamped


def lens_eligible_cards(manifest: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Return every card in ``manifest`` permitted to act as an active lens.

    The single enforcement point for WIS-484. A card is eligible unless the
    bridge flagged it ineligible or it resolves to a barred domain.
    """
    barred = {domain.upper() for domain in LENS_BARRED_DOMAINS}
    eligible: List[Dict[str, Any]] = []
    for key, cards in manifest.items():
        if not isinstance(cards, list):
            continue
        for card in cards:
            if not isinstance(card, dict):
                continue
            if card.get("lens_eligible") is False:
                continue
            if str(card.get("domain") or key).upper() in barred:
                continue
            eligible.append(card)
    return eligible


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------
def bridge_manifest(manifest: Dict[str, Any]) -> Dict[str, Dict[str, int]]:
    """
    Apply the full bridge to ``manifest`` in place and return a change report.

    Idempotent: a second application over the same input reports all zeros.
    """
    report: Dict[str, Dict[str, int]] = {}

    for key, source_path, domain in BRIDGED_SOURCES:
        source_cards = load_json(source_path, default=[])
        if not isinstance(source_cards, list):
            source_cards = []
        added, updated = ingest_domain(manifest, key, source_cards, domain)
        report[key] = {"added": added, "updated": updated, "source": len(source_cards)}

    for key in TITLE_BACKFILL_KEYS:
        report[f"titles:{key}"] = {"backfilled": backfill_titles(manifest, key)}

    report["lens_bar"] = {"stamped": bar_lens_roles(manifest)}
    manifest["lens_exclusion_policy"] = lens_exclusion_policy()
    return report


def verify_manifest(manifest: Dict[str, Any]) -> List[str]:
    """
    Assert this story's post-conditions against ``manifest``.

    Returns a list of human-readable failure messages; empty means verified.
    """
    failures: List[str] = []
    barred = {domain.upper() for domain in LENS_BARRED_DOMAINS}

    for key, source_path, domain in BRIDGED_SOURCES:
        cards = manifest.get(key)
        if not isinstance(cards, list):
            failures.append(f"manifest['{key}'] missing or not a list")
            continue
        source_cards = load_json(source_path, default=[]) or []
        if not isinstance(source_cards, list):
            source_cards = []
        if len(cards) != len(source_cards):
            failures.append(f"manifest['{key}'] has {len(cards)} cards, expected {len(source_cards)}")
        ids = [card.get("id") for card in cards if isinstance(card, dict)]
        if len(ids) != len(set(ids)):
            failures.append(f"manifest['{key}'] contains duplicate ids")
        for card in cards:
            if not isinstance(card, dict):
                failures.append(f"manifest['{key}'] contains a non-dict card")
                continue
            if not derive_title(card).strip():
                failures.append(f"{key} card {card.get('id')!r} has no descriptive title")
            if card.get("domain") != domain:
                failures.append(
                    f"{key} card {card.get('id')!r} domain is {card.get('domain')!r}, expected {domain!r}"
                )

    for key in TITLE_BACKFILL_KEYS:
        for card in manifest.get(key) or []:
            if not isinstance(card, dict):
                failures.append(f"{key} contains a non-dict card")
                continue
            title = card.get("title")
            if not isinstance(title, str) or not title.strip():
                failures.append(f"{key} card {card.get('id')!r} has no descriptive title")

    for key in LENS_BARRED_KEYS:
        for card in manifest.get(key) or []:
            if not isinstance(card, dict):
                continue
            if card.get("lens_eligible") is not False:
                failures.append(f"barred card {card.get('id')!r} in {key!r} is still lens eligible")
            if card.get("lens_barred_by") != LENS_BAR_AUTHORITY:
                failures.append(f"barred card {card.get('id')!r} in {key!r} lacks the {LENS_BAR_AUTHORITY} anchor")

    if manifest.get("lens_exclusion_policy") != lens_exclusion_policy():
        failures.append("manifest['lens_exclusion_policy'] is missing or out of sync")

    leaked = [
        card.get("id")
        for card in lens_eligible_cards(manifest)
        if str(card.get("domain") or "").upper() in barred
    ]
    if leaked:
        failures.append(f"{LENS_BAR_AUTHORITY} violation: barred cards offered as lenses: {leaked}")

    return failures


def _format_report(report: Dict[str, Dict[str, int]]) -> str:
    lines = ["DNA Manifest Bridge change report"]
    for stage, counters in report.items():
        detail = ", ".join(f"{name}={value}" for name, value in counters.items())
        lines.append(f"  {stage}: {detail}")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Bridge DNA bone collections into the manifest.")
    parser.add_argument("--dry-run", action="store_true", help="report changes without writing")
    parser.add_argument("--verify", action="store_true", help="verify post-conditions without writing")
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH, help="manifest path override")
    args = parser.parse_args(argv)

    manifest_path: Path = args.manifest
    if not manifest_path.exists():
        print(f"[ERROR] manifest not found: {manifest_path}", file=sys.stderr)
        return 1

    manifest = load_json(manifest_path, default=None)
    if not isinstance(manifest, dict):
        print(f"[ERROR] manifest is not a JSON object: {manifest_path}", file=sys.stderr)
        return 1

    if args.verify:
        failures = verify_manifest(manifest)
        if failures:
            print("[FAIL] manifest verification failed:", file=sys.stderr)
            for failure in failures:
                print(f"  - {failure}", file=sys.stderr)
            return 1
        print(f"[PASS] {manifest_path} satisfies all Story 94.1 post-conditions")
        return 0

    report = bridge_manifest(manifest)

    # Refuse to write a half-satisfied bridge; that would corrupt the catalog.
    failures = verify_manifest(manifest)
    if failures:
        print("[BLOCKER] bridge would not satisfy its own post-conditions:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1

    if args.dry_run:
        print(_format_report(report))
        print("[DRY-RUN] no write performed")
        return 0

    atomic_write_json(manifest_path, manifest)
    print(_format_report(report))
    print(f"[OK] wrote {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
