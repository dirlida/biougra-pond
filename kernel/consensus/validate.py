import json, pathlib, hashlib, sys
from datetime import datetime
ROOT = pathlib.Path.home() / "pond"
CHAIN = ROOT / "chain.json"
# fix import for direct run
sys.path.insert(0, str(ROOT))
from kernel.consensus.pow import hash_header, meets_target
from kernel.consensus.merkle import merkle_root

def parse_ts(v):
    if isinstance(v, int): return v
    try: return int(datetime.fromisoformat(v).timestamp())
    except: return 0

def validate_block(block, prev_block=None):
    try:
        idx = block.get("index", block.get("payload",{}).get("index", 0))
        prev = block.get("prev")
        nonce = block.get("nonce", 0)
        diff = block.get("difficulty", 3)
        mr = block.get("merkle_root", "0"*64)
        payload = block.get("payload", {})
        ts = parse_ts(payload.get("ts", 0))
        btc = payload.get("btcHeight", 0)
        cables_hash = payload.get("cables_hash","")
        drones_hash = payload.get("drones_hash","")
        stamp_hash = payload.get("stamp_hash","")
        wallet_h = payload.get("wallet_height",0)

        if prev_block:
            if prev != prev_block.get("hash"):
                return False, f"prev mismatch {prev[:8]} != {prev_block.get('hash','')[:8]}"

        calc_hash = hash_header(prev, mr, payload.get("ts", ts), btc, nonce, diff, idx, cables_hash, drones_hash, stamp_hash, wallet_h)
        if calc_hash != block.get("hash"):
            calc_hash2 = hash_header(prev, mr, payload.get("ts",""), btc, nonce, diff, idx, cables_hash, drones_hash, stamp_hash, wallet_h)
            if calc_hash2 != block.get("hash"):
                return False, f"hash mismatch calc {calc_hash[:8]} != {block.get('hash','')[:8]}"
            calc_hash = calc_hash2

        if not meets_target(calc_hash, diff):
            return False, f"PoW target fail {calc_hash[:8]} diff {diff}"

        import time
        if ts > int(time.time()) + 7200:
            return False, "future block"

        return True, "OK"
    except Exception as e:
        return False, f"exc {e}"

def validate_chain():
    blocks = json.loads(CHAIN.read_text())
    for i in range(1, len(blocks)):
        b = blocks[i]
        if "nonce" not in b:
            continue
        prev = blocks[i-1]
        ok, msg = validate_block(b, prev)
        if not ok:
            return f"FAIL at {i}: {msg}"
    return f"CHAIN OK {len(blocks)} blocks, PoW from first nonce block (old PoT skipped)"

if __name__ == "__main__":
    print(validate_chain())
