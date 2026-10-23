import json, pathlib, time
ROOT = pathlib.Path.home() / "pond"
POOL = ROOT / "kernel" / "modules" / "wallet" / "tx_pool.json"
MAX_TX_PER_BLOCK = 10
MIN_FEE = 1
def load_pool():
    try:
        j=json.loads(POOL.read_text())
        return j.get("pool", j) if isinstance(j, dict) else j
    except: return []
def score_tx(tx):
    fee=tx.get("fee",0)
    size=len(json.dumps(tx))
    age=time.time()-tx.get("ts", time.time())
    return (fee/max(size,1))*1000+age*0.001
def select_txs_for_block():
    pool=load_pool()
    valid=[t for t in pool if t.get("fee",0)>=MIN_FEE]
    valid.sort(key=score_tx, reverse=True)
    return valid[:MAX_TX_PER_BLOCK]
def remove_mined(txs_mined):
    pool=load_pool()
    mined_ids={t.get("txid") for t in txs_mined}
    remaining=[t for t in pool if t.get("txid") not in mined_ids]
    POOL.write_text(json.dumps({"pool":remaining,"updated":int(time.time())}, indent=2))
    return len(pool)-len(remaining)
if __name__=="__main__":
    sel=select_txs_for_block()
    print(f"mempool {len(load_pool())} -> selected {len(sel)}")
