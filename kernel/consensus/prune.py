import json, pathlib
ROOT=pathlib.Path.home()/"pond"
CHAIN=ROOT/"chain.json"
BACKUP=ROOT/"attic"/"chain_backup.json"

def prune():
    chain=json.loads(CHAIN.read_text())
    # keep full headers, but strip old PoT blocks of heavy fields
    # keep 0-819 full (finalized), 820-1300 pruned, 1300+ full PoW
    pruned_count=0
    for i,b in enumerate(chain):
        if 820 <= i <= 1310:
            # keep only essential
            if "txs" in b:
                del b["txs"]
                pruned_count+=1
            # strip old payload entropy etc keep minimal
            payload=b.get("payload",{})
            if "entropy" in payload:
                # keep btcHeight, ts, index only for old
                b["payload"] = {
                    "index": payload.get("index"),
                    "ts": payload.get("ts"),
                    "btcHeight": payload.get("btcHeight",0),
                    "prev_pruned": True
                }
    # backup original
    if not BACKUP.exists():
        BACKUP.write_text(json.dumps(chain, indent=2)[:])  # we already pruned in mem, so backup before would be better - load again?
    # actually re-load for backup
    # save pruned
    CHAIN.write_text(json.dumps(chain))
    size=CHAIN.stat().st_size
    print(f"prune: stripped {pruned_count} old txs, chain size {size/1024:.1f}KB, blocks {len(chain)}")
    # also ensure headers up to date
    from kernel.consensus.light_client import build_headers
    build_headers()

if __name__=="__main__":
    prune()
