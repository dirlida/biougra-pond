import json, time, hashlib, random
from datetime import datetime, timezone, timedelta
from pathlib import Path

GENESIS_INDEX = 36
CHAIN_FILE = Path("chain.json")
LAST_FILE = Path("LAST.txt")

def log(m): print(f"[{datetime.now(timezone.utc).isoformat()}] {m}", flush=True)

def mine_block(chain, ts_override=None):
    prev = chain[-1]
    if ts_override:
        ts_dt = ts_override
        ts = ts_dt.isoformat().replace("+00:00","Z")
    else:
        ts_dt = datetime.now(timezone.utc)
        ts = ts_dt.isoformat().replace("+00:00","Z")

    payload = {
        "index": len(chain),
        "ts": ts,
        "prev": prev.get("hash"),
        "entropy": hashlib.sha256(f"{ts}{random.random()}".encode()).hexdigest()[:32],
    }
    block_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    block = {
        "index": len(chain),
        "hash": block_hash,
        "prev": prev.get("hash"),
        "payload": payload
    }
    chain.append(block)
    CHAIN_FILE.write_text(json.dumps(chain, indent=2))
    LAST_FILE.write_text(str(len(chain)-1))
    return block

def main():
    while True:
        chain = json.loads(CHAIN_FILE.read_text())
        t36_str=chain[GENESIS_INDEX]['payload']['ts']
        t36=datetime.fromisoformat(t36_str.replace("Z","+00:00"))
        now=datetime.now(timezone.utc)
        expected = GENESIS_INDEX + int((now - t36).total_seconds() // 615)

        actual = len(chain)-1
        if expected > actual:
            log(f"BEHIND: expected {expected} actual {actual} -> catch-up with 615s steps")
            for _ in range(expected - actual):
                last_ts=datetime.fromisoformat(chain[-1]['payload']['ts'].replace('Z','+00:00'))
                next_ts=last_ts + timedelta(seconds=615)
                # FIX: never cap to now, if next_ts > now, stop catch-up and wait
                if next_ts > now + timedelta(seconds=5):
                    log(f" next_ts {next_ts} is in future vs now {now} - stopping catch-up, waiting")
                    break
                block=mine_block(chain, ts_override=next_ts)
                log(f" CATCH-UP Mined {len(chain)-1} | {block['hash'][:12]} | ts {block['payload']['ts']}")
            continue

        # normal 10min heartbeat
        last_ts_str=chain[-1]['payload']['ts']
        dp=datetime.fromisoformat(last_ts_str.replace('Z','+00:00'))
        diff=(now-dp).total_seconds()
        if diff < 615:
            wait=int(615-diff)+2
            log(f" -> too fast {diff:.0f}s <615 - waiting {wait}s")
            time.sleep(wait)
            continue

        block=mine_block(chain)
        log(f"Mined {len(chain)-1} | {block['hash'][:12]} | prev {block['prev'][:12]} | ts {block['payload']['ts']}")
        time.sleep(615)

if __name__ == "__main__":
    main()
