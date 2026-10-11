#!/usr/bin/env python3
import time, json, os, hashlib, subprocess, random
from datetime import datetime, timezone

BLOCK_TIME = 600  # SACRED - 10min
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
    j = json.dumps(payload, sort_keys=True).encode()
    return hashlib.sha256(j).hexdigest()

def mine_block(chain):
    prev_block = chain[-1]
    prev_hash = prev_block["hash"]
    prev_payload = prev_block.get("payload", {})
    payload = {
        "pond": prev_payload.get("pond", "BIOUGRA POND"),
        "cityMyth": prev_payload.get("cityMyth", "Marrakech"),
        "lab": prev_payload.get("lab", "Biougra"),
        "gps": prev_payload.get("gps", {"lat": 30.126126126126128, "lon": -9.37437367846481}),
        "gpsStr": prev_payload.get("gpsStr", "30.12613,-9.37437"),
        "sun": str(round(random.uniform(30, 40), 2)),
        "btcHeight": prev_payload.get("btcHeight", 969609) + random.randint(0,1),
        "prev": prev_hash,
        "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "originTax": prev_payload.get("originTax", "1% LAW"),
        "entropy": os.urandom(16).hex(),
        "nonce": random.randint(0, 999999)
    }
    return {
        "hash": make_hash(payload),
        "payload": payload,
        "prev": prev_hash
    }

def try_push(chain):
    last = 0
    if os.path.exists("LAST.txt"):
        try: last = int(open("LAST.txt").read().strip())
        except: pass
    current = len(chain) - 1
    if current - last < PUSH_EVERY:
        return
    
    log(f" -> trying push {last+1} to {current}...")
    try:
        # these work offline
        subprocess.run(["git","add","chain.json","LAST.txt"], check=False, timeout=5)
        # commit - may fail if nothing to commit, that's ok
        subprocess.run(["git","commit","-m",f"block {current}"], check=False, timeout=5, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # push - IAM PROOF, 15s max, never crash daemon
        result = subprocess.run(["git","push","origin","main"], timeout=15, capture_output=True, text=True)
        if result.returncode == 0:
            open("LAST.txt","w").write(str(current))
            log(f" -> pushed to {current} OK")
            # try push v29 fix too if pending
            subprocess.run(["git","push","origin","main"], timeout=15, capture_output=True)
        else:
            log(f" -> push failed (no net): {result.stderr[:120]}")
            log(f" -> queued, will retry next block, mining continues")
    except subprocess.TimeoutExpired:
        log(f" -> push timeout (iam data dead) - queued, mining continues")
    except Exception as e:
        log(f" -> push error {e} - queued, mining continues")

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    log(f"Biougra Pond daemon - {BLOCK_TIME}s - OFFLINE FIRST - auto-push every {PUSH_EVERY}")
    while True:
        try:
            chain = load_chain()
            block = mine_block(chain)
            chain.append(block)
            save_chain(chain)
            ts = datetime.now(timezone.utc).isoformat()
            last = 0
            if os.path.exists("LAST.txt"):
                try: last = int(open("LAST.txt").read().strip())
                except: pass
            next_push = last + PUSH_EVERY
            if next_push <= len(chain)-1:
                next_push = len(chain)-1 + (PUSH_EVERY - (len(chain)-1-last)%PUSH_EVERY)%PUSH_EVERY
            mins = max(0, (next_push - (len(chain)-1)) * BLOCK_TIME // 60)
            log(f"[{ts}] Mined {len(chain)-1} | {block['hash'][:12]} | prev {block['prev'][:12]}")
            log(f" -> next push at block {next_push} (in {mins} min)")
            try_push(chain)
        except Exception as e:
            import traceback
            log(f"ERR: {e}")
            traceback.print_exc()
        time.sleep(BLOCK_TIME)
