import json, pathlib, time, hashlib
from datetime import datetime, timezone
ROOT=pathlib.Path.home()/"pond"
CHAIN=ROOT/"chain.json"
import sys
sys.path.insert(0, str(ROOT))
from kernel.consensus.pow import mine
from kernel.consensus.difficulty import get_difficulty
from kernel.consensus.merkle import merkle_root
from kernel.consensus.time_oracle import get_times
from kernel.modules.wallet.utxo import create_coinbase, apply_txs, load_state, validate_tx
from kernel.modules.wallet.fee_market import select_txs_for_block, remove_mined
from kernel.consensus.light_client import build_headers
from kernel.consensus.attestation import get_finalized_height
def load_chain(): return json.loads(CHAIN.read_text())
def save_chain(c):
    tmp=CHAIN.with_suffix(".tmp")
    tmp.write_text(json.dumps(c))
    tmp.rename(CHAIN)
    try: (ROOT/"kernel"/"state"/"chain.json").write_text(json.dumps(c))
    except: pass
def get_module_hash(p):
    q=ROOT/p
    if not q.exists(): return "0"*8
    try: return hashlib.sha256(q.read_bytes()).hexdigest()[:12]
    except: return "0"*8
def mine_loop():
    print("=== POND v5.4 PoW 10MIN PRECISION ===", flush=True)
    print(f"finalized {get_finalized_height()} - 10min blocks - A13 law", flush=True)
    while True:
        try:
            chain=load_chain()
            prev=chain[-1]["hash"]
            index=chain[-1].get("index", len(chain)-1)+1
            diff=get_difficulty(index)
            times=get_times()
            if times.get("drift",0) > 600:
                print(f"[PANIC] drift {times['drift']}s >600 stop", flush=True)
                break
            mem_txs=select_txs_for_block()
            state=load_state()
            valid_mem=[]
            for tx in mem_txs:
                ok,msg=validate_tx(tx, state)
                if ok: valid_mem.append(tx)
                else: print(f"[MEMPOOL REJECT] {tx.get('txid','')[:8]} {msg}", flush=True)
            coinbase=create_coinbase("did:pond:biougra-a13", 50, index)
            txs=[coinbase]+valid_mem
            mr=merkle_root(txs)
            cables_h=get_module_hash("kernel/modules/cables/seabed_state.json")
            drones_h=get_module_hash("kernel/modules/drones/fleet_state.json")
            stamp_h=get_module_hash("kernel/modules/stamp/outbox/summary.json")
            ts_iso=datetime.now(timezone.utc).isoformat()
            print(f"[{index}] diff={diff} mem={len(valid_mem)} mr={mr[:8]} btc={times.get('btcHeight')} drift={times.get('drift')}s target=600s", flush=True)
            nonce,block_hash=mine(prev, mr, ts_iso, times.get("btcHeight",0), diff, index, cables_h, drones_h, stamp_h, index, max_nonce=15_000_000)
            if nonce is None:
                time.sleep(2); continue
            payload={"index":index,"ts":ts_iso,"btcHeight":times.get("btcHeight",0),"sunAltitude":15.2,"cables_hash":cables_h,"drones_hash":drones_h,"stamp_hash":stamp_h,"wallet_height":index,"merkle_root":mr,"tx_count":len(txs),"fee_total":sum(t.get("fee",0) for t in valid_mem),"block_time_target":600}
            block={"hash":block_hash,"prev":prev,"index":index,"nonce":nonce,"difficulty":diff,"merkle_root":mr,"payload":payload,"txs":txs}
            applied=apply_txs(txs, index)
            remove_mined(valid_mem)
            chain.append(block)
            save_chain(chain)
            build_headers()
            print(f"✅ PoW v5.4 10MIN #{index} {block_hash} nonce={nonce} diff={diff} next in 10min", flush=True)
            print(f"[SLEEP] 600s - next block ~10min - A13 battery save", flush=True)
            time.sleep(600)  # 10 min
        except Exception as e:
            import traceback; traceback.print_exc(); print(f"err {e}", flush=True); time.sleep(10)
if __name__=="__main__": mine_loop()
