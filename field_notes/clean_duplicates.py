import glob
import json
import logging
import os
import re
import difflib

# Config
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
logging.basicConfig(level=logging.INFO, format="[CLEAN] %(message)s")


def normalize_text(text):
    return re.sub(r"[^a-z0-9\s]", "", str(text).lower()).strip()


def token_jaccard(s1, s2):
    t1 = set(normalize_text(s1).split())
    t2 = set(normalize_text(s2).split())
    if not t1 or not t2:
        return 0.0
    return len(t1 & t2) / len(t1 | t2)


def are_evidence_duplicates(ev1, ev2):
    n1 = normalize_text(ev1)
    n2 = normalize_text(ev2)
    if not n1 or not n2:
        return False
    if n1 == n2:
        return True
    if len(n1) >= 15 and len(n2) >= 15:
        if n1 in n2 or n2 in n1:
            return True
    if difflib.SequenceMatcher(None, n1, n2).ratio() > 0.75:
        return True
    return token_jaccard(n1, n2) > 0.60


def clean_duplicates():
    logging.info("--- Starting Archive De-Duplication [v2.1 Gem-Specific] ---")

    json_files = glob.glob(os.path.join(DATA_DIR, "*.json"))
    # Only target year or monthly gem files, e.g. 2005.json, 2005_02.json, 2005_2007.json, Unknown.json
    gem_pattern = re.compile(r"^(Unknown|\d{4}(_\w+)?)\.json$")

    total_removed = 0

    for jf in json_files:
        fname = os.path.basename(jf)
        if not gem_pattern.match(fname):
            continue

        try:
            with open(jf, "r") as f:
                data = json.load(f)

            if not isinstance(data, list) or not data:
                continue

            # Verify it's a gem list (items must have summary or evidence)
            if not isinstance(data[0], dict) or ("summary" not in data[0] and "evidence" not in data[0]):
                continue

            original_count = len(data)
            unique_data = []

            for item in data:
                if not isinstance(item, dict):
                    continue
                d = item.get("date")
                if not d:
                    unique_data.append(item)
                    continue

                ev = item.get("evidence", "")
                summ = item.get("summary", "")

                dup_found = False
                for u in unique_data:
                    if d == u.get("date"):
                        # 1. Evidence duplicate
                        if are_evidence_duplicates(ev, u.get("evidence", "")):
                            dup_found = True
                        # 2. Summary similarity
                        elif token_jaccard(summ, u.get("summary", "")) > 0.60 or \
                             difflib.SequenceMatcher(None, summ.lower(), u.get("summary", "").lower()).ratio() > 0.70:
                            dup_found = True

                        if dup_found:
                            # Merge tags and take max rank
                            u["tags"] = list(set(u.get("tags", []) + item.get("tags", [])))
                            u_rank = u.get("rank") or 0
                            i_rank = item.get("rank") or 0
                            if max(u_rank, i_rank) > 0:
                                u["rank"] = max(u_rank, i_rank)
                            if len(summ) > len(u.get("summary", "")):
                                u["summary"] = summ
                            break

                if not dup_found:
                    unique_data.append(item)

            removed = original_count - len(unique_data)

            if removed > 0:
                logging.info(
                    f"File: {fname} | Removed {removed} duplicates ({original_count} -> {len(unique_data)})."
                )
                total_removed += removed
                with open(jf, "w") as f:
                    json.dump(unique_data, f, indent=2)

        except Exception as e:
            logging.error(f"Failed to clean {fname}: {e}")

    logging.info(f"--- De-Duplication Complete. Total removed: {total_removed} ---")


if __name__ == "__main__":
    clean_duplicates()
