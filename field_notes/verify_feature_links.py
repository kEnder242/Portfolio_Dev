#!/usr/bin/env python3
# verify_feature_links.py [v1.0]
# [SPR-55 / FEAT Code Mapping] Hard-gate link verifier for FeatureTracker.md **Code:** fields.
# Parses every **Code:** field, resolves the git link against the local repo checkout,
# validates the file exists and that any #Lstart(-Lend) anchor is within the file's line count.
# Report-only (never rewrites links). Exits non-zero on any drift.
#
# Usage: python3 field_notes/verify_feature_links.py [--report /tmp/drift_report.txt]

import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEV_LAB_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../.."))   # /home/jallred/Dev_Lab
TRACKER_MD = os.path.join(BASE_DIR, "../FeatureTracker.md")
DEFAULT_REPORT = os.path.join(DEV_LAB_ROOT, ".omo/evidence/drift_report.txt")

# Repo base mapping: {remote host key -> local checkout root}
REPO_BASES = {
    "github.com/kEnder242/HomeLabAI":   os.path.join(DEV_LAB_ROOT, "HomeLabAI"),
    "github.com/kEnder242/Portfolio_Dev": os.path.join(DEV_LAB_ROOT, "Portfolio_Dev"),
    "gitlab.com/kEnder242/Dev_Lab":     DEV_LAB_ROOT,
}

# Matches https://HOST/OWNER/REPO/blob/BRANCH/path/to/file#L12 or #L12-L34
LINK_RE = re.compile(
    r'https://(?P<host>[^/]+)/(?P<owner>[^/]+)/(?P<repo>[^/]+)/blob/(?P<branch>[^/#]+)/(?P<path>[^#)\s]+)'
    r'(?:#L(?P<start>\d+)(?:-L(?P<end>\d+))?)?'
)


def extract_code_fields(md_text):
    """Return list of (feature_id, code_value) for every **Code:** field."""
    # Split by feature headers
    header_re = re.compile(r'^## \[((?:FEAT|LAB)-\d{3}(?:\.\d+)?)\]', re.MULTILINE)
    matches = list(header_re.finditer(md_text))
    fields = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(md_text)
        body = md_text[m.end():end]
        code_m = re.search(r'\*\*Code:\*\*\s*(.+?)(?=\n\*\*|\n*$)', body, re.DOTALL)
        if code_m:
            fields.append((m.group(1), code_m.group(1).strip()))
    return fields


def validate_field(feat_id, code_value):
    """Validate one Code field. Returns (ok, [issues])."""
    issues = []
    if "none found" in code_value or "documented only" in code_value:
        return True, []  # explicit absence marker, nothing to verify
    link_m = LINK_RE.search(code_value)
    if not link_m:
        return False, [f"{feat_id}: no git link found in Code field: {code_value[:80]!r}"]
    host = link_m.group("host")
    repo = link_m.group("repo")
    rel_path = link_m.group("path")
    start_line = int(link_m.group("start")) if link_m.group("start") else None
    end_line = int(link_m.group("end")) if link_m.group("end") else None

    local_root = REPO_BASES.get(f"{host}/{link_m.group('owner')}/{repo}")
    if local_root is None:
        return False, [f"{feat_id}: unknown repo base for {host}/{repo}"]
    local_file = os.path.join(local_root, rel_path)
    if not os.path.isfile(local_file):
        return False, [f"{feat_id}: file not found: {rel_path} (repo {repo})"]
    with open(local_file, encoding="utf-8", errors="replace") as f:
        line_count = sum(1 for _ in f)
    if start_line is not None and start_line > line_count:
        issues.append(f"{feat_id}: #L{start_line} exceeds {line_count} lines in {rel_path}")
    if end_line is not None:
        if end_line > line_count:
            issues.append(f"{feat_id}: #L{end_line} exceeds {line_count} lines in {rel_path}")
        if start_line and end_line < start_line:
            issues.append(f"{feat_id}: end line {end_line} < start line {start_line} in {rel_path}")
    return (len(issues) == 0, issues)


def main():
    report_path = DEFAULT_REPORT
    if "--report" in sys.argv:
        idx = sys.argv.index("--report")
        if idx + 1 < len(sys.argv):
            report_path = sys.argv[idx + 1]
    if not os.path.exists(TRACKER_MD):
        print(f"❌ Tracker not found: {TRACKER_MD}")
        return 2

    with open(TRACKER_MD, encoding="utf-8") as f:
        md_text = f.read()

    fields = extract_code_fields(md_text)
    total = len(fields)
    verified = 0
    drift = []

    for feat_id, code_value in fields:
        ok, issues = validate_field(feat_id, code_value)
        if ok and not issues:
            verified += 1
        else:
            drift.extend(issues)

    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("FeatureTracker.md link-drift report\n")
        f.write(f"Generated: {__import__('datetime').datetime.now().isoformat()}\n")
        f.write(f"Code fields checked: {total} | verified: {verified} | drift: {len(drift)}\n")
        f.write("=" * 60 + "\n")
        for line in drift:
            f.write(line + "\n")

    print(f"✅ verify_feature_links: {verified}/{total} Code fields verified, {len(drift)} drift")
    if drift:
        print(f"❌ DRIFT FOUND ({len(drift)} issue(s)) — see {report_path}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
