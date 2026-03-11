import os, sys, json
sys.path.append(os.path.expanduser("~/Dev_Lab/HomeLabAI/src"))
from nodes.archive_node import stream, wisdom

try:
    where_filter = {"$and": [{"date": {"$gte": "2021-01-01"}}, {"date": {"$lte": "2021-12-31"}}]}
    res = wisdom.get(limit=5, where=where_filter)
    print(f"Count: {len(res.get('ids', []))}")
    print(json.dumps(res.get("metadatas"), indent=2))
except Exception as e:
    print("Error:", e)