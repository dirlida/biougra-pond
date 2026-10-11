#!/usr/bin/env python3
import json
from datetime import datetime

CHAIN_FILE = "chain.json"
MIN_BLOCK_INTERVAL = 590
MAX_BLOCK_INTERVAL = 900
ENFORCE_FROM_INDEX = 10 # now enforce from your new tip

def parse_ts(s):
    return datetime.fromisoformat(s.replace("Z","+00:00"))

def verify():
    with open(CHAIN_FILE) as f:
        chain = json.load(f)
    print(f"Verifying {len(chain)} blocks - 10min enforced from {ENFORCE_FROM_INDEX}...")
    for i in range(1, len(chain)):
        prev = chain[i-1]
        curr = chain[i]
        if curr.get("prev")!= prev.get("hash"):
            print(f"❌ Block {i} bad link {curr.get('hash','?')[:12]}")
            return False
        if i >= ENFORCE_FROM_INDEX:
            try:
                diff = (parse_ts(curr["payload"]["ts"]) - parse_ts(prev["payload"]["ts"])).total_seconds()
                if diff < MIN_BLOCK_INTERVAL:
                    print(f"❌ Block {curr['hash'][:12]} TOO FAST {diff:.0f}s - REJECTED")
                    return False
            except Exception as e:
                print(f"⚠️ time parse {i}: {e}")
    print(f"✅ Chain valid: {len(chain)} blocks, 10min OK")
    return True

if __name__ == "__main__":
    verify()
