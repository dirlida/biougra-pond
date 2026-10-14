# KERNEL LAW v1 ENFORCEMENT - for BIOUGRA POND nested structure
import json, sys
from datetime import datetime, timezone

CANONICAL_FILE = "chain.json"
APPROVAL_THRESHOLD = 615
TIME_RULE_START = 36

def get_ts(block):
    # ts is inside payload
    if "payload" in block and isinstance(block["payload"], dict):
        return block["payload"].get("ts") or block["payload"].get("timestamp") or block["payload"].get("time")
    return block.get("ts") or block.get("timestamp")

def parse_utc_z(ts: str):
    if not isinstance(ts, str):
        raise ValueError(f"ts not string: {ts}")
    if not ts.endswith("Z"):
        raise ValueError(f"ts must be UTC Z, got: {ts}")
    try:
        if "." in ts:
            dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
        return dt.replace(tzinfo=timezone.utc)
    except Exception as e:
        try:
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            return dt
        except:
            raise ValueError(f"Invalid time {ts}: {e}")

def verify():
    data = json.load(open(CANONICAL_FILE))
    if not data:
        print("OK: empty")
        return
    for i in range(1, len(data)):
        prev = data[i-1]
        cur = data[i]
        idx = cur.get("index", i)
        # if payload has index use that
        if "payload" in cur and "index" in cur["payload"]:
            idx = cur["payload"]["index"]
        # also payload may have its own prev chain
        prev_raw = get_ts(prev)
        cur_raw = get_ts(cur)
        if not prev_raw or not cur_raw:
            print(f"FAIL at block {idx}: missing ts - payload keys={list(cur.get('payload', {}).keys()) if 'payload' in cur else list(cur.keys())}")
            sys.exit(1)
        try:
            prev_t = parse_utc_z(prev_raw)
            cur_t = parse_utc_z(cur_raw)
        except Exception as e:
            if idx < TIME_RULE_START:
                continue
            print(f"FAIL at block {idx}: {e}")
            sys.exit(1)

        if idx >= TIME_RULE_START or i >= TIME_RULE_START:
            diff = (cur_t - prev_t).total_seconds()
            if diff < APPROVAL_THRESHOLD:
                print(f"FAIL at block {idx} (i={i}): REFUSED - only {diff:.1f}s since last, need {APPROVAL_THRESHOLD}s - RULE 4 HAMMER")
                sys.exit(1)

        # hash chain check
        expected_prev = cur.get("prev") or cur.get("payload", {}).get("prev")
        actual_prev_hash = prev.get("hash")
        if expected_prev and actual_prev_hash and expected_prev!= actual_prev_hash:
            # allow GENESIS case
            if expected_prev!= "GENESIS" and actual_prev_hash!= "GENESIS":
                if expected_prev!= actual_prev_hash:
                    print(f"FAIL at block {idx}: prev mismatch {expected_prev[:8]} vs {actual_prev_hash[:8]}")
                    sys.exit(1)

    print(f"OK: {len(data)} blocks - KERNEL LAW v1 verified - 615 hammer active - nested payload OK")

if __name__ == "__main__":
    verify()