import os
import sys
import time

# Add the field_notes directory to sys.path to import mass_scan.
# Robust to cwd: works both from repo root and from the parent of field_notes.
sys.path.append(os.path.abspath("Portfolio_Dev/field_notes"))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mass_scan
from mass_scan import (
    register_pid,
    check_lock,
    atomic_write_text,
    wait_for_roundtable_lock,
    lock_pid_alive,
    MASS_SCAN_PID_FILE,
)


def test_pid_write_is_atomic(tmp_path, monkeypatch):
    pid_file = tmp_path / "p.pid"
    monkeypatch.setattr(mass_scan, "MASS_SCAN_PID_FILE", str(pid_file))
    monkeypatch.setattr(mass_scan, "LAB_RUN_DIR", str(tmp_path))
    register_pid()
    assert int(pid_file.read_text()) == os.getpid()
    assert list(tmp_path.glob("*.tmp")) == []


def test_atomic_write_overwrites(tmp_path):
    target = tmp_path / "x.txt"
    atomic_write_text(str(target), "first")
    atomic_write_text(str(target), "second")
    assert target.read_text() == "second"


def test_atomic_write_no_tmp_residue(tmp_path):
    target = tmp_path / "y.txt"
    atomic_write_text(str(target), "one")
    atomic_write_text(str(target), "two")
    assert list(tmp_path.glob("*.tmp")) == []


def test_check_lock_absent(tmp_path):
    assert check_lock(str(tmp_path / "missing.lock")) is False


def test_check_lock_stale_pid_recovery(tmp_path, monkeypatch):
    lock = tmp_path / "round_table.lock"
    lock.write_text("99999999")  # a PID that is not alive
    monkeypatch.setattr(mass_scan, "lock_pid_alive", lambda pid: False)
    assert check_lock(str(lock)) is False
    assert not lock.exists()


def test_check_lock_live_pid(tmp_path, monkeypatch):
    lock = tmp_path / "round_table.lock"
    lock.write_text(str(os.getpid()))
    monkeypatch.setattr(mass_scan, "lock_pid_alive", lambda pid: True)
    monkeypatch.setattr("os.path.getmtime", lambda p: time.time() - 10)
    assert check_lock(str(lock)) is True


def test_wait_for_lock_timeout(tmp_path):
    lock = tmp_path / "round_table.lock"
    lock.write_text(str(os.getpid()))  # held by a live PID
    assert wait_for_roundtable_lock(str(lock), timeout=0.2) is False


def test_wait_for_lock_clears(tmp_path, monkeypatch):
    lock = tmp_path / "round_table.lock"
    lock.write_text(str(os.getpid()))

    def fake_sleep(seconds):
        lock.unlink(missing_ok=True)

    monkeypatch.setattr("time.sleep", fake_sleep)
    assert wait_for_roundtable_lock(str(lock), timeout=2.0) is True
    assert not lock.exists()