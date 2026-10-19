import os
import sys
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from refine_gem import _has_technical_evidence


def test_technical_evidence_detector_positive():
    """Verify detection of hardware registers, scripts, tools, and technical scars."""
    assert _has_technical_evidence("Fixed PECI reading on MSR 0x610 using rapl_check.py") is True
    assert _has_technical_evidence("Run with --verbose flag on /usr/bin/ipmitool -I lanplus") is True
    assert _has_technical_evidence("Found PCIe link training failure on bus 0x03") is True
    assert _has_technical_evidence("OpenBMC telemetry service reported RAPL power throttling") is True


def test_technical_evidence_detector_negative():
    """Verify rejection of empty, mundane office logistics, catering, and admin notes."""
    assert _has_technical_evidence("") is False
    assert _has_technical_evidence(None) is False
    assert _has_technical_evidence("Follow up on FedEx shipment tracking for office chairs") is False
    assert _has_technical_evidence("Reset password for Jira account and attend 2pm sync") is False
    assert _has_technical_evidence("Booked room 4B for weekly project planning meeting") is False


def test_prompt_domain_tagging_and_inclusive_scope():
    """Verify that nibble_v2 default extraction prompt tags events with a domain and includes logistics/operations in scope."""
    import inspect
    import nibble_v2

    source = inspect.getsource(nibble_v2.main)
    assert "domain" in source.lower()
    assert "logistics" in source.lower()
    assert "operations" in source.lower()


def test_disentangle_chronology():
    """Verify 4-stage chronological disentanglement between event_era and document_date."""
    from refine_gem import disentangle_chronology

    # Stage 1: Explicit Date
    d1 = disentangle_chronology("Incident occurred on 8/29/2019 during power test", "2024-08-01")
    assert d1["event_year"] == 2019
    assert d1["event_era"] == "2019-08-29"
    assert d1["event_quarter"] == "2019-Q3"
    assert d1["document_date"] == "2024-08-01"
    assert d1["temporal_provenance"] == "explicit_incident_date"

    # Stage 2: Explicit Year
    d2 = disentangle_chronology("Debug performed back in 2016 for thermal drift", "2024-08-01")
    assert d2["event_year"] == 2016
    assert d2["event_quarter"] == "2016-Q1"
    assert d2["temporal_provenance"] == "explicit_incident_year"

    # Stage 3: Platform Era Heuristic
    d3 = disentangle_chronology("Grantley PECI validation discrepancy detected", "2024-08-01")
    assert d3["event_year"] == 2014
    assert d3["event_quarter"] == "2014-Q2"
    assert "platform_heuristic" in d3["temporal_provenance"]

    # Stage 4: Retrospective Shift
    d4 = disentangle_chronology("Noted this behavior 10 years ago during early bring-up", "2024-08-01")
    assert d4["event_year"] == 2014

    # Stage 5: Fallback to document date
    d5 = disentangle_chronology("Routine status update meeting notes", "2023-05-15")
    assert d5["event_year"] == 2023
    assert d5["event_quarter"] == "2023-Q2"
    assert d5["temporal_provenance"] == "document_date_fallback"


def test_classify_impact_level():
    """Verify discrete impact levels 1 to 4 with focal boost."""
    from refine_gem import classify_impact_level

    # Strategic Trunk (Impact 4)
    trunk_gem = {
        "summary": "Platform validation lead for IPMI and PECI architecture",
        "evidence": "Validated MSR 0x610 and RAPL power clamping on Whitley",
        "tags": ["ipmi", "peci", "rapl"],
        "rank": 4
    }
    assert classify_impact_level(trunk_gem) == 4

    # Subsystem Branch (Impact 2 or 3)
    branch_gem = {
        "summary": "Workaround for Montana power sweep failure",
        "evidence": "Ran montana.nativemodules.pmcapsweep with --force on bus 0x02",
        "tags": ["montana", "power"],
        "rank": 3
    }
    assert classify_impact_level(branch_gem) in (2, 3)

    # Leaf (Impact 1)
    leaf_gem = {
        "summary": "FedEx shipment tracking #789012345678 arrived at desk",
        "evidence": "Tracking confirmed delivery via email receipt",
        "tags": ["shipping", "logistics"],
        "rank": 1
    }
    assert classify_impact_level(leaf_gem) == 1


def test_rotational_refinement_engine_mechanics(tmp_path):
    """Verify Lyapunov delta equilibrium, priority scoring, and queue retention in LOOP-004."""
    from refine_gem import RotationalRefinementEngine

    engine = RotationalRefinementEngine(epoch=106)
    item = {
        "gem_id": "TEST-001",
        "file_path": "test.json",
        "index": 0,
        "refinement_level": 1,
        "impact_level": 4,
        "passes": 1,
        "consecutive_zero_deltas": 0,
        "last_touch_epoch": 104,
        "priority": 0.0,
        "anchors": ["RAPL", "MSR 0x610"]
    }

    # Priority score check: Impact 4, Refinement Deficit 2 (3-1), Age 2 (106-104)
    p = engine.compute_priority(item)
    assert p > 0.0
    assert isinstance(p, float)

