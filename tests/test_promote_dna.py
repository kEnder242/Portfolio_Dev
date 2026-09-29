"""
Unit tests for Document-Scoped DNA Promotion Gate (promote_dna.py).
"""

import json
import os
import shutil
import sys
import tempfile
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
from promote_dna import promote_document_dna, get_next_global_id




@pytest.fixture
def test_env():
    """Create isolated sandbox directories for testing promotion."""
    temp_dir = tempfile.mkdtemp()
    dna_dir = os.path.join(temp_dir, "dna")
    papers_dir = os.path.join(temp_dir, "field_notes", "data", "papers")
    os.makedirs(dna_dir, exist_ok=True)
    os.makedirs(papers_dir, exist_ok=True)

    # Seed mock wisdom dataset
    wisdom_data = [
        {"id": "WIS-001", "theme": "General", "paper_order": 1},
        {"id": "WIS-489", "theme": "Architecture", "paper_order": 489},
    ]
    with open(os.path.join(dna_dir, "wisdom_data.json"), "w") as f:
        json.dump(wisdom_data, f, indent=2)

    # Seed mock inspiration dataset
    inspiration_data = [
        {"id": "INS-001", "theme": "Philosophy", "paper_order": 1},
        {"id": "INS-041", "theme": "Spine", "paper_order": 41},
    ]
    with open(os.path.join(dna_dir, "inspiration_data.json"), "w") as f:
        json.dump(inspiration_data, f, indent=2)

    # Seed mock spine
    spine_data = {
        "paper_id": "PAPER-TEST",
        "document_dna": [
            {
                "doc_dna_id": "DOC-TEST-001",
                "theme": "#datacenter #telemetry #debug",
                "title": "Debug Architecture",
                "text": "Extensive enterprise telemetry and hardware debug engineering.",
                "origin_node_id": "node_sum_01",
                "promoted_to_global": None,
                "citations": ["FEAT-586", "FEAT-592"],
            },
            {
                "doc_dna_id": "DOC-TEST-002",
                "theme": "#already_promoted",
                "title": "Already Graduated",
                "text": "Some text",
                "origin_node_id": "node_02",
                "promoted_to_global": "WIS-100",
            },
        ],
    }
    with open(os.path.join(papers_dir, "PAPER-TEST_spine.json"), "w") as f:
        json.dump(spine_data, f, indent=2)

    yield {
        "temp_dir": temp_dir,
        "dna_dir": dna_dir,
        "papers_dir": papers_dir,
    }

    shutil.rmtree(temp_dir)


def test_get_next_global_id():
    wis_items = [{"id": "WIS-001"}, {"id": "WIS-489"}]
    wid, wnum = get_next_global_id(wis_items, "WIS")
    assert wid == "WIS-490"
    assert wnum == 490

    ins_items = [{"id": "INS-001"}, {"id": "INS-041"}]
    iid, inum = get_next_global_id(ins_items, "INS")
    assert iid == "INS-042"
    assert inum == 42


def test_successful_promotion_to_wisdom(test_env):
    res = promote_document_dna(
        paper_id="TEST",
        doc_dna_id="DOC-TEST-001",
        target_domain="WIS",
        dna_dir=test_env["dna_dir"],
        papers_dir=test_env["papers_dir"],
        dry_run=False,
        run_sync=False,
    )

    assert res["status"] == "success"
    assert res["global_id"] == "WIS-490"
    assert res["target_domain"] == "WIS"

    # Verify global dataset updated
    with open(os.path.join(test_env["dna_dir"], "wisdom_data.json")) as f:
        wis = json.load(f)
    assert len(wis) == 3
    card = wis[-1]
    assert card["id"] == "WIS-490"
    assert card["origin"]["source"] == "PAPER-TEST (node_sum_01) -> DOC-TEST-001"
    assert "telemetry" in card["metadata"]["tags"]
    assert "promoted-doc-dna" in card["metadata"]["tags"]

    # Verify spine updated
    with open(os.path.join(test_env["papers_dir"], "PAPER-TEST_spine.json")) as f:
        spine = json.load(f)
    doc_rec = spine["document_dna"][0]
    assert doc_rec["promoted_to_global"] == "WIS-490"
    assert "promoted_at" in doc_rec


def test_successful_promotion_to_inspiration(test_env):
    res = promote_document_dna(
        paper_id="TEST",
        doc_dna_id="DOC-TEST-001",
        target_domain="INS",
        dna_dir=test_env["dna_dir"],
        papers_dir=test_env["papers_dir"],
        dry_run=False,
        run_sync=False,
    )

    assert res["status"] == "success"
    assert res["global_id"] == "INS-042"
    assert res["target_domain"] == "INS"

    with open(os.path.join(test_env["dna_dir"], "inspiration_data.json")) as f:
        ins = json.load(f)
    assert len(ins) == 3
    assert ins[-1]["id"] == "INS-042"


def test_dry_run_leaves_files_untouched(test_env):
    res = promote_document_dna(
        paper_id="TEST",
        doc_dna_id="DOC-TEST-001",
        target_domain="WIS",
        dna_dir=test_env["dna_dir"],
        papers_dir=test_env["papers_dir"],
        dry_run=True,
        run_sync=False,
    )

    assert res["status"] == "success"
    assert res["dry_run"] is True

    # Check files unchanged
    with open(os.path.join(test_env["dna_dir"], "wisdom_data.json")) as f:
        wis = json.load(f)
    assert len(wis) == 2

    with open(os.path.join(test_env["papers_dir"], "PAPER-TEST_spine.json")) as f:
        spine = json.load(f)
    assert spine["document_dna"][0]["promoted_to_global"] is None


def test_reject_already_promoted(test_env):
    with pytest.raises(ValueError, match="already promoted"):
        promote_document_dna(
            paper_id="TEST",
            doc_dna_id="DOC-TEST-002",
            target_domain="WIS",
            dna_dir=test_env["dna_dir"],
            papers_dir=test_env["papers_dir"],
            dry_run=False,
            run_sync=False,
        )


def test_reject_missing_record(test_env):
    with pytest.raises(KeyError, match="not found"):
        promote_document_dna(
            paper_id="TEST",
            doc_dna_id="DOC-NONEXISTENT",
            target_domain="WIS",
            dna_dir=test_env["dna_dir"],
            papers_dir=test_env["papers_dir"],
            dry_run=False,
            run_sync=False,
        )


def test_reject_missing_paper(test_env):
    with pytest.raises(FileNotFoundError, match="Spine file not found"):
        promote_document_dna(
            paper_id="UNKNOWN_PAPER",
            doc_dna_id="DOC-001",
            target_domain="WIS",
            dna_dir=test_env["dna_dir"],
            papers_dir=test_env["papers_dir"],
            dry_run=False,
            run_sync=False,
        )


def test_reject_invalid_domain(test_env):
    with pytest.raises(ValueError, match="Invalid target domain"):
        promote_document_dna(
            paper_id="TEST",
            doc_dna_id="DOC-TEST-001",
            target_domain="INVALID",
            dna_dir=test_env["dna_dir"],
            papers_dir=test_env["papers_dir"],
            dry_run=False,
            run_sync=False,
        )
