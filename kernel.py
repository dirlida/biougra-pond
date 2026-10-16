import json, hashlib, random, subprocess, time
from datetime import datetime, timezone
from pathlib import Path
from filelock import FileLock

CHAIN_FILE = Path("chain.json")
LAST_FILE = Path("LAST.txt")
LOCK_FILE = Path(".pond.lock")
LOCK_FILE.touch(exist_ok=True)

def log(m): print(f"[{datetime.now(timezone.utc).isoformat()}] {m}", flush=True)

def safe_load_chain():
    with FileLock(str(LOCK_FILE), timeout=15):
        txt = CHAIN_FILE.read_text().strip()
        if not txt: raise ValueError("empty chain.json")
        return json.loads(txt)

def mine_and_save(ts_override=None):
    """ONLY function in whole repo that writes chain.json/LAST.txt. FileLock protected."""
    with FileLock(str(LOCK_FILE), timeout=15):
        # re-read inside lock
        try:
            chain = json.loads(CHAIN_FILE.read_text())
        except:
            # recover from corrupt
            subprocess.run(["git","checkout","HEAD","--","chain.json"], capture_output=True)
            chain = json.loads(CHAIN_FILE.read_text())
        
        prev = chain[-1]
        ts_dt = ts_override if ts_override else datetime.now(timezone.utc)
        ts = ts_dt.isoformat().replace("+00:00","Z")
        payload = {"index": len(chain),"ts": ts,"prev": prev.get("hash"),"entropy": hashlib.sha256(f"{ts}{random.random()}".encode()).hexdigest()[:32]}
        block_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        block = {"index": len(chain),"hash": block_hash,"prev": prev.get("hash"),"payload": payload}
        chain.append(block)
        
        tmp = CHAIN_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps(chain, indent=2))
        tmp.replace(CHAIN_FILE)
        LAST_FILE.write_text(str(len(chain)-1))
        return block

def auto_push(block_index):
    try:
        subprocess.run(["git","add","-f","chain.json","LAST.txt","kernel.py"], capture_output=True, timeout=10)
        msg = f"pond_daemon v3 LIVE - beacon"
        r = subprocess.run(["git","commit","-m",msg], capture_output=True, text=True, timeout=10)
        if "nothing to commit" in (r.stdout + r.stderr):
            return False
        pr = subprocess.run(["git","push"], capture_output=True, text=True, timeout=30)
        if pr.returncode==0:
            log(f"AUTO-PUSH OK block {block_index}")
            return True
        else:
            log(f"push failed: {pr.stderr[:200]}")
            return False
    except Exception as e:
        log(f"auto_push error: {e}")
        return False
