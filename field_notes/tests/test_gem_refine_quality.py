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


def test_prompt_negative_constraints():
    """Verify that nibble_v2 default extraction prompt contains negative guidance against fluff."""
    import inspect
    import nibble_v2

    source = inspect.getsource(nibble_v2.main)
    assert "EXCLUDE" in source or "negative" in source.lower()
    assert "logistics" in source.lower() or "shipping" in source.lower()
