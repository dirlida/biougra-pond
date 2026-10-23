#!/data/data/com.termux/files/usr/bin/python3
import os, json, time, hashlib, fcntl, random
from datetime import datetime, timezone

def get_last_mining(chain):
    f=[b for b in chain if b.get("type")!="thesis" and b.get("hash")]
    return f[-1] if f else get_last_mining(chain)
from kernel.consensus.pow import hash_header
from kernel.consensus.difficulty import get_difficulty
try:
    from kernel.consensus.merkle import merkle_root as calc_merkle
except: calc_merkle=None

LOCK_FILE=os.path.expanduser("~/pond/tmp/pond.lock")
CAP_MAX=3; MIN_BLOCK_TIME=600; HARD=900
CHAIN_PATH="chain.json"; KSTATE_CHAIN="kernel/state/chain.json"; LOG_PATH="pond.log"
_lock_fd=None
def check_no_doubler():
    global _lock_fd
    os.makedirs(os.path.dirname(LOCK_FILE), exist_ok=True)
    try:
        _lock_fd=os.open(LOCK_FILE, os.O_RDWR|os.O_CREAT, 0o600)
        fcntl.flock(_lock_fd, fcntl.LOCK_EX|fcntl.LOCK_NB)
        os.ftruncate(_lock_fd,0); os.write(_lock_fd, str(os.getpid()).encode())
        return True
    except:
        try:
            with open(LOCK_FILE,'r') as f: oldpid=int(f.read().strip() or "0")
            os.kill(oldpid,0); print(f"DOUBLER BLOCKED pid {oldpid} alive"); return False
        except:
            print("STALE LOCK removing")
            try: os.remove(LOCK_FILE)
            except: pass
            try:
                _lock_fd=os.open(LOCK_FILE, os.O_RDWR|os.O_CREAT, 0o600)
                fcntl.flock(_lock_fd, fcntl.LOCK_EX|fcntl.LOCK_NB)
                os.ftruncate(_lock_fd,0); os.write(_lock_fd, str(os.getpid()).encode())
                return True
            except: return False
if not check_no_doubler(): exit(0)

def load_chain():
    for p in [CHAIN_PATH, KSTATE_CHAIN]:
        try:
            with open(p,'r') as f: return json.load(f),p
        except: continue
    return [], CHAIN_PATH
def save_chain(chain,path):
    tmp=path+".tmp"
    with open(tmp,'w') as f: json.dump(chain,f)
    os.rename(tmp,path)
    try:
        other=KSTATE_CHAIN if path==CHAIN_PATH else CHAIN_PATH
        with open(other,'w') as f: json.dump(chain,f)
    except: pass
def get_prev_time(block):
    if not block: return time.time()
    try:
        ts = block.get('payload',{}).get('ts') or block.get('timestamp')
        if ts: return datetime.fromisoformat(ts).timestamp()
    except: pass
    return time.time()

chain,chain_path=load_chain()
prev_count=len(chain)
prev_hash=get_last_mining(chain)['hash'] if chain else "0"*64
prev_time=get_prev_time(get_last_mining(chain) if chain else None)
print(f"POND START v5.4 count={prev_count} prev={prev_hash[:12]} CAP3 LIVE MIN={MIN_BLOCK_TIME}s = 10min blocks", flush=True)

while True:
    now=time.time()
    elapsed=now-prev_time
    if elapsed < MIN_BLOCK_TIME:
        wait=MIN_BLOCK_TIME-elapsed
        if elapsed > HARD:
            print(f"DRIFT CATCHUP {elapsed:.0f}s > HARD {HARD}s — will mine now after wait {wait:.0f}s", flush=True)
        print(f"10MIN RULE: {elapsed:.1f}s elapsed, sleeping {wait:.1f}s until next block... #{prev_count+1}", flush=True)
        time.sleep(min(wait,60))
        continue
    # mine
    curr_index=prev_count
    ts_iso=datetime.now(timezone.utc).isoformat()
    cables_hash="1e31d11e91da"; drones_hash="e2432daf31d0"; stamp_hash="00000000"
    wallet_h=curr_index; btc_h=972583; sun=15.2
    txs=[{"type":"coinbase","height":curr_index}]
    if calc_merkle:
        merkle=calc_merkle([json.dumps(t) for t in txs])
    else:
        merkle=hashlib.sha256(str(curr_index).encode()).hexdigest()
    diff=min(get_difficulty(curr_index),CAP_MAX)
    print(f"MINING v5 #{curr_index} diff{diff} after {elapsed:.1f}s...", flush=True)
    nonce=random.randint(0,999999)
    found=False
    for _ in range(5000000):
        h=hash_header(prev_hash, merkle, ts_iso, btc_h, nonce, diff, curr_index, cables_hash, drones_hash, stamp_hash, wallet_h)
        if h.startswith("0"*diff):
            block={"hash":h,"prev":prev_hash,"index":curr_index,"nonce":nonce,"difficulty":diff,"merkle_root":merkle,"payload":{"index":curr_index,"ts":ts_iso,"btcHeight":btc_h,"sunAltitude":sun,"cables_hash":cables_hash,"drones_hash":drones_hash,"stamp_hash":stamp_hash,"wallet_height":wallet_h,"merkle_root":merkle,"tx_count":1,"fee_total":0,"block_time_target":600},"txs":[{"txid":h,"type":"coinbase","vin":[],"vout":[{"to":"did:pond:biougra-a13","amount":50,"mature_height":curr_index+100}],"fee":0,"ts":int(time.time()),"height":curr_index}]}
            chain.append(block); save_chain(chain,chain_path)
            print(f"BLOCK #{curr_index} {h[:16]} diff{diff} nonce{nonce} elapsed={elapsed:.1f}s")
            with open(LOG_PATH,'a') as lf: lf.write(f"{curr_index} {h} {nonce} diff{diff}\n")
            prev_count=len(chain); prev_hash=h; prev_time=time.time()
            found=True; break
        nonce+=1
    if not found:
        print("not found, retry..."); time.sleep(1)
    else:
        time.sleep(1)
