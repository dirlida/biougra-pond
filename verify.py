# KERNEL LAW v1 ENFORCEMENT
# Block 1eeff99 onward - hammered
import json, sys
from datetime import datetime, timezone

CANONICAL_FILE = "chain.json"
APPROVAL_THRESHOLD = 615
TIME_RULE_START = 36

def parse_utc_z(ts: str):
    if not ts.endswith("Z"):
        raise ValueError(f"ts must be UTC Z, got: {ts}")
    try:
        if "." in ts:
            dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
        return dt.replace(tzinfo=timezone.utc)
    except Exception as e:
        raise ValueError(f"Invalid canonical time format: {ts} - {e}")

def verify():
    try:
        data = json.load(open(CANONICAL_FILE))
    except Exception as e:
        print(f"FAIL: cannot read {CANONICAL_FILE}: {e}")
        sys.exit(1)
    if not data:
        print("OK: empty chain")
        return
    for i in range(1, len(data)):
        prev = data[i-1]
        cur = data[i]
        try:
            prev_t = parse_utc_z(prev["ts"])
            cur_t = parse_utc_z(cur["ts"])
        except Exception as e:
            print(f"FAIL at block {cur.get('index', i)}: {e}")
            sys.exit(1)
        if cur.get("index", i) >= TIME_RULE_START:
            diff = (cur_t - prev_t).total_seconds()
            if diff < APPROVAL_THRESHOLD:
                print(f"FAIL at block {cur.get('index', i)}: REFUSED - only {diff}s since last, need {APPROVAL_THRESHOLD}s - KERNEL LAW RULE 4")
                sys.exit(1)
        if "prev_hash" in cur and "hash" in prev:
            if cur["prev_hash"]!= prev["hash"]:
                print(f"FAIL at block {i}: prev_hash mismatch")
                sys.exit(1)
    print(f"OK: {len(data)} blocks - KERNEL LAW v1 verified - 615 hammer active")

if __name__ == "__main__":
    verify()
