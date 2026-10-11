#!/usr/bin/env python3
import time, json, os, hashlib, subprocess, random
from datetime import datetime, timezone

BLOCK_TIME = 600  # SACRED - 10min - DO NOT CHANGE
PUSH_EVERY = 5
CHAIN_FILE = "chain.json"

def log(msg):
    print(msg, flush=True)

def load_chain():
    with open(CHAIN_FILE) as f:
        return json.load(f)

def save_chain(chain):
    with open(CHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=2)

def make_hash(payload):
    # hash = sha256 of payload json sorted - matches your genesis
    j = json.dumps(payload, sort_keys=True).encode()
    return hashlib.sha256(j).hexdigest()

def mine_block(chain):
    prev_block = chain[-1]
    prev_hash = prev_block["hash"]
    prev_payload = prev_block.get("payload", {})
    
    # keep your pond metadata, copy from prev
    payload = {
        "pond": prev_payload.get("pond", "BIOUGRA POND"),
        "cityMyth": prev_payload.get("cityMyth", "Marrakech"),
        "lab": prev_payload.get("lab", "Biougra"),
        "gps": prev_payload.get("gps", {"lat": 30.126126126126128, "lon": -9.37437367846481}),
        "gpsStr": prev_payload.get("gpsStr", "30.12613,-9.37437"),
        "sun": str(round(random.uniform(30, 40), 2)),  # simulate sun
        "btcHeight": prev_payload.get("btcHeight", 969609) + random.randint(0,1),
        "prev": prev_hash,
        "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "originTax": prev_payload.get("originTax", "1% LAW"),
        # add quantum entropy
        "entropy": os.urandom(16).hex(),
        "nonce": random.randint(0, 999999)
    }
    block_hash = make_hash(payload)
    block = {
        "hash": block_hash,
        "payload": payload,
        "prev": prev_hash
    }
    return block

def try_push(chain):
    last = 0
    if os.path.exists("LAST.txt"):
        try:
            last = int(open("LAST.txt").read().strip())
        except:
            pass
    current = len(chain) - 1
    if current - last >= PUSH_EVERY:
        log(f" -> pushing {last+1} to {current} to GitHub...")
        try:
            subprocess.run(["git","add","chain.json"], check=True)
            subprocess.run(["git","commit","-m",f"block {current}"], check=True)
            subprocess.run(["git","push"], check=True)
            open("LAST.txt","w").write(str(current))
            log(f" -> pushed to {current} OK")
        except Exception as e:
            log(f" -> push failed: {e}")

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    log(f"Biougra Pond daemon - {BLOCK_TIME}s - auto-push every {PUSH_EVERY} blocks")
    while True:
        try:
            chain = load_chain()
            block = mine_block(chain)
            chain.append(block)
            save_chain(chain)
            ts = datetime.now(timezone.utc).isoformat()
            # next push calc
            last = 0
            if os.path.exists("LAST.txt"):
                try: last = int(open("LAST.txt").read().strip())
                except: pass
            next_push = ((last // PUSH_EVERY)+1)*PUSH_EVERY
            if next_push <= len(chain)-1:
                next_push = len(chain)-1 + PUSH_EVERY - (len(chain)-1-last)%PUSH_EVERY
            mins = (next_push - (len(chain)-1)) * BLOCK_TIME // 60
            log(f"[{ts}] Mined {len(chain)-1} | {block['hash'][:12]} | prev {block['prev'][:12]}")
            log(f" -> next push at block {next_push} (in {mins} min)")
            try_push(chain)
        except Exception as e:
            import traceback
            log(f"ERR: {e}")
            traceback.print_exc()
        time.sleep(BLOCK_TIME)
