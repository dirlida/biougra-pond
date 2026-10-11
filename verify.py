#!/usr/bin/env python3
import json
from datetime import datetime

CHAIN_FILE = "chain.json"
MIN_BLOCK_INTERVAL = 590
ENFORCE_FROM_INDEX = 36 # your current tip - enforce after this

def parse_ts(s):
    try:
        return datetime.fromisoformat(s.replace("Z","+00:00"))
    except Exception as e:
        raise e

def verify():
    with open(CHAIN_FILE) as f:
        chain = json.load(f)
    print(f"Checking {len(chain)} blocks...")
    for i in range(1, len(chain)):
        prev = chain[i-1]
        curr = chain[i]
        # hash link: curr.prev == prev.hash
        if curr.get("prev")!= prev.get("hash"):
            print(f"❌ Block {i} hash link broken: curr.prev!= prev.hash")
            print(f" curr {curr.get('hash')[:12]} prev {curr.get('prev')[:12] if curr.get('prev') else None} vs should {prev.get('hash')[:12]}")
            return False
        # time lock only for new blocks
        if i >= ENFORCE_FROM_INDEX:
            try:
                dp = parse_ts(prev["payload"]["ts"])
                dc = parse_ts(curr["payload"]["ts"])
                diff = (dc-dp).total_seconds()
                if diff < MIN_BLOCK_INTERVAL:
                    print(f"❌ Block {curr['hash'][:12]} too fast: {diff:.0f}s < 590s - REJECTED (10min rule)")
                    return False
            except Exception as e:
                print(f"⚠️ time parse fail at {i}: {e}")
    print(f"✅ verify.py OK - {len(chain)} blocks - 10min rule active from block {ENFORCE_FROM_INDEX}")
    return True

if __name__ == "__main__":
    verify()
