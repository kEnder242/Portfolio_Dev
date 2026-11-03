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
    t1 = set(n1.split())
    t2 = set(n2.split())
    if not t1 or not t2:
        return False
    inter = len(t1 & t2)
    if inter == 0:
        return False
    jaccard = inter / len(t1 | t2)
    if jaccard > 0.60:
        return True
    if jaccard > 0.25 and difflib.SequenceMatcher(None, n1, n2).ratio() > 0.75:
        return True
    return False


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
            by_date = {}

            for item in data:
                if not isinstance(item, dict):
                    continue
                d = item.get("date") or item.get("event_date") or item.get("document_date")
                ev = item.get("evidence", "")
                summ = item.get("summary", "")

                dup_found = False
                candidates = by_date.get(d, []) if d else unique_data
                for u in candidates:
                    u_d = u.get("date") or u.get("event_date") or u.get("document_date")
                    u_ev = u.get("evidence", "")
                    u_summ = u.get("summary", "")

                    same_date = (d and u_d and d == u_d)

                    # 1. Evidence duplicate
                    if are_evidence_duplicates(ev, u_ev):
                        dup_found = True
                    # 2. Summary similarity on exact same date
                    elif same_date and (token_jaccard(summ, u_summ) > 0.55 or
                         difflib.SequenceMatcher(None, summ.lower(), u_summ.lower()).ratio() > 0.70):
                        dup_found = True

                    if dup_found:
                        # Merge tags
                        u["tags"] = sorted(list(set(u.get("tags", []) + item.get("tags", []))))
                        # Take max rank
                        u_rank = u.get("rank") or 0
                        i_rank = item.get("rank") or 0
                        if max(u_rank, i_rank) > 0:
                            u["rank"] = max(u_rank, i_rank)
                        # Keep more detailed summary
                        if len(summ) > len(u_summ):
                            u["summary"] = summ
                        # Preserve highest temporal confidence
                        u_conf = u.get("temporal_confidence") or 0.5
                        i_conf = item.get("temporal_confidence") or 0.5
                        u["temporal_confidence"] = max(u_conf, i_conf)
                        break

                if not dup_found:
                    unique_data.append(item)
                    if d:
                        if d not in by_date:
                            by_date[d] = []
                        by_date[d].append(item)

            removed = original_count - len(unique_data)

            if removed > 0:
                logging.info(
                    f"File: {fname} | Removed {removed} duplicates ({original_count} -> {len(unique_data)})."
                )
                total_removed += removed
                # [BKM-022] Atomic persistence protocol
                tmp_path = jf + ".tmp"
                with open(tmp_path, "w", encoding="utf-8") as f:
                    json.dump(unique_data, f, indent=2)
                os.replace(tmp_path, jf)

        except Exception as e:
            logging.error(f"Failed to clean {fname}: {e}")

    logging.info(f"--- De-Duplication Complete. Total removed: {total_removed} ---")


if __name__ == "__main__":
    clean_duplicates()
