"""
[STORY 70.11] Sanitized Public Benchmark Exporter

Reads internal telemetry data, strips sensitive fields (LAN IPs, session
tokens, absolute paths), and writes a public JSON artifact.

Output: data/public_benchmarks.json
Zero third-party dependencies. Atomic write (.tmp + replace).
"""
import glob
import json
import os
import re
import tempfile

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "public_benchmarks.json")
TELEMETRY_LEDGER = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "HomeLabAI",
    "data",
    "telemetry_ledger.jsonl",
)

LAN_IP_RE = re.compile(r"\b192\.168\.\d{1,3}\.\d{1,3}\b")
SESSION_TOKEN_RE = re.compile(r"\bses_[A-Za-z0-9]{4,}\b")
# Absolute path: starts with "/" (POSIX) or a drive letter (Windows, e.g. C:\\)
ABS_PATH_RE = re.compile(r"(?<![A-Za-z0-9_.-])(?:/[\w~./-]+|(?:[A-Za-z]:[\\/][\w\\/.-]*))")

LAN_REDACTED = "REDACTED_IP"
SESSION_REDACTED = "REDACTED_SESSION"
PATH_REDACTED = "REDACTED_PATH"


def sanitize_text(text):
    """Return *text* with sensitive substrings redacted in place."""
    if not isinstance(text, str):
        return text
    text = LAN_IP_RE.sub(LAN_REDACTED, text)
    text = SESSION_TOKEN_RE.sub(SESSION_REDACTED, text)
    text = ABS_PATH_RE.sub(PATH_REDACTED, text)
    return text


def sanitize_value(value):
    """Recursively redact sensitive data inside a JSON value tree."""
    if isinstance(value, str):
        return sanitize_text(value)
    if isinstance(value, list):
        return [sanitize_value(item) for item in value]
    if isinstance(value, dict):
        return {key: sanitize_value(val) for key, val in value.items()}
    return value


def load_jsonl(path):
    """Yield each parsed JSON record from a JSONL file (skips empty/bad lines)."""
    records = []
    if not os.path.exists(path):
        return records
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records


def load_telemetry():
    """Collect all JSON records from yearly archives plus the telemetry ledger."""
    records = []
    for fpath in sorted(glob.glob(os.path.join(DATA_DIR, "20*.json"))):
        try:
            with open(fpath, encoding="utf-8") as handle:
                data = json.load(handle)
        except (json.JSONDecodeError, OSError):
            continue
        if isinstance(data, list):
            records.extend(data)
        elif isinstance(data, dict):
            records.append(data)
    records.extend(load_jsonl(TELEMETRY_LEDGER))
    return records


def export(records=None):
    """Sanitize *records* (or live telemetry) and atomically write the output."""
    if records is None:
        records = load_telemetry()
    payload = {"benchmarks": [sanitize_value(rec) for rec in records]}

    directory = os.path.dirname(OUTPUT_FILE)
    os.makedirs(directory, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
        os.replace(tmp_path, OUTPUT_FILE)
    except BaseException:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise
    return OUTPUT_FILE


if __name__ == "__main__":
    path = export()
    print(f"Wrote sanitized public benchmarks -> {path}")
