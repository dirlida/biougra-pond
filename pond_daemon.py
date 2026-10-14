
# KERNEL LAW v1 - RULE 4 ENFORCEMENT
from datetime import timezone
def kernel_stamp():
    now_utc = datetime.now(timezone.utc)
    ts_z = now_utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    local_tag = now_utc.astimezone().isoformat()
    return ts_z, local_tag
\n# FORWARD FIX 231 - GPS only in genesis block 0, no GPS in blocks 231+ - chain.json history untouched
import json, hashlib, time, subprocess, random, os
from datetime import datetime, timezone
from pathlib import Path

CHAIN="chain.json"
LAST="LAST.txt"

def log(m): print(f"[{datetime.now(timezone.utc).isoformat()}] {m}", flush=True)

def load_chain():
    return json.loads(Path(CHAIN).read_text())

def save_chain(c):
    data = json.dumps(c, indent=2)
    tmp = CHAIN + ".tmp"
    with open(tmp, "w") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, CHAIN)
    tmp2 = LAST + ".tmp"
    with open(tmp2, "w") as f:
        f.write(str(len(c)-1))
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp2, LAST)
    os.sync()

def mine_real_block(chain):
    prev_block=chain[-1]
    prev_hash=prev_block['hash']
    ts=datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
    # keep SAME structure as your valid block 16
    payload={
        "pond": "BIOUGRA POND",
        "cityMyth": "Marrakech",
        "lab": "Biougra",
        # GPS removed for blocks >0 - forward fix from 231
        # gpsStr removed for blocks >0
        "sun": f"{38.97 + random.uniform(-0.5,0.5):.2f}",
        "btcHeight": prev_block['payload'].get('btcHeight',969619)+1,
        "prev": prev_hash,
        "ts": ts,
        "originTax": "1% LAW",
        "entropy": hashlib.sha256(f"{ts}{random.random()}".encode()).hexdigest()[:32],
        "nonce": random.randint(100000, 9999999)
    }
    # hash = sha256(prev + json(payload))
    raw=f"{prev_hash}{json.dumps(payload, sort_keys=True)}"
    h=hashlib.sha256(raw.encode()).hexdigest()
    block={"hash": h, "payload": payload, "prev": prev_hash}
    return block

while True:
    try:
        chain=load_chain()
        # ---- 10min RULE ENFORCER (never mine too fast) ----
        if len(chain)>=1 and len(chain)>=10:
            try:
                last_ts=chain[-1]['payload']['ts']
                dp=datetime.fromisoformat(last_ts.replace('Z','+00:00'))
                dc=datetime.now(timezone.utc)
                diff=(dc-dp).total_seconds()
                if diff < 615:  # 615s safe >590
                    wait=int(615-diff)+2
                    log(f" -> too fast {diff:.0f}s <615 - waiting {wait}s")
                    time.sleep(wait)
                    continue
            except Exception as e:
                log(f"time check err {e}")

        block=mine_real_block(chain)
        chain.append(block)
        save_chain(chain)
        log(f"Mined {len(chain)-1} | {block['hash'][:12]} | prev {block['prev'][:12]} | ts {block['payload']['ts']}")

        if (len(chain)-1) % 5 == 0:
            try:
                subprocess.run(["git","add",CHAIN,LAST], timeout=10)
                subprocess.run(["git","commit","-m",f"block {len(chain)-1}"], timeout=10)
                subprocess.run(["git","push"], timeout=30)
                log(f" -> pushed {len(chain)-1}")
            except Exception as e:
                log(f"push fail {e}")

        time.sleep(615)

    except Exception as e:
        log(f"ERROR {e}")
        import traceback; traceback.print_exc()
        time.sleep(30)
