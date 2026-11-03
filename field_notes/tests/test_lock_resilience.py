#!/usr/bin/env python3
"""
[BKM-099] / [Story 109.17] Unit Tests for Self-Healing Lock Reaper in can_burn().
Verifies:
1. Dead PID lockfile is reaped and can_burn() proceeds.
2. Expired lockfile (>2 hours old) is reaped regardless of contents.
3. Active PID lockfile is respected and yields can_burn() -> False.
4. Empty/corrupt lockfile is reaped cleanly.
"""

import os
import sys
import time
from pathlib import Path

FIELD_NOTES_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(FIELD_NOTES_DIR))

import utils


def test_dead_pid_reaped(tmp_path, monkeypatch):
    test_lock = tmp_path / "round_table.lock"
    # Write a PID that does not exist
    test_lock.write_text("99999999")
    monkeypatch.setattr(utils, "ROUND_TABLE_LOCK", str(test_lock))
    # Mock VRAM and attendant checks so they pass
    monkeypatch.setattr(utils, "get_system_load", lambda: 0.5)
    monkeypatch.setattr(utils, "get_free_vram_gb", lambda: 16.0)
    monkeypatch.setattr(utils, "get_vram_usage", lambda: 0.1)

    ready, reason = utils.can_burn(check_vram=False)
    assert ready is True
    assert reason == "Nominal"
    # Stale lock must be removed
    assert not test_lock.exists()
    print("TEST_DEAD_PID_REAPED: PASSED")


def test_expired_lock_reaped(tmp_path, monkeypatch):
    test_lock = tmp_path / "round_table.lock"
    test_lock.write_text(str(os.getpid()))
    # Backdate mtime by 3 hours
    three_hours_ago = time.time() - 10800
    os.utime(str(test_lock), (three_hours_ago, three_hours_ago))

    monkeypatch.setattr(utils, "ROUND_TABLE_LOCK", str(test_lock))
    monkeypatch.setattr(utils, "get_system_load", lambda: 0.5)

    ready, reason = utils.can_burn(check_vram=False)
    assert ready is True
    assert reason == "Nominal"
    assert not test_lock.exists()
    print("TEST_EXPIRED_LOCK_REAPED: PASSED")


def test_live_pid_respected(tmp_path, monkeypatch):
    test_lock = tmp_path / "round_table.lock"
    # Current test runner PID is actively alive
    test_lock.write_text(str(os.getpid()))
    monkeypatch.setattr(utils, "ROUND_TABLE_LOCK", str(test_lock))

    ready, reason = utils.can_burn(check_vram=False)
    assert ready is False
    assert reason == "Active Intercom Session (Lock)"
    assert test_lock.exists()
    print("TEST_LIVE_PID_RESPECTED: PASSED")


def test_corrupt_lock_reaped(tmp_path, monkeypatch):
    test_lock = tmp_path / "round_table.lock"
    test_lock.write_text("not_a_pid_garbage_content")
    monkeypatch.setattr(utils, "ROUND_TABLE_LOCK", str(test_lock))
    monkeypatch.setattr(utils, "get_system_load", lambda: 0.5)

    ready, reason = utils.can_burn(check_vram=False)
    assert ready is True
    assert reason == "Nominal"
    assert not test_lock.exists()
    print("TEST_CORRUPT_LOCK_REAPED: PASSED")


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
