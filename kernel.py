import json, hashlib, random, subprocess, math, time, shutil, os

import requests
def get_btc_anchor():
    try:
        h = requests.get("https://mempool.space/api/blocks/tip/hash", timeout=5).text.strip()
        ht = requests.get("https://mempool.space/api/blocks/tip/height", timeout=5).text.strip()
        return h, ht
    except:
        return None, None

from datetime import datetime, timezone
from pathlib import Path
from filelock import FileLock

CHAIN_FILE = Path("chain.json")
LAST_FILE = Path("LAST.txt")
SHA_FILE = Path("SHA256.txt")
LOCK_FILE = Path(".pond.lock")
LOCK_FILE.touch(exist_ok=True)

GPS_LAT=30.12613
GPS_LON=-9.37437

def log(m): print(f"[{datetime.now(timezone.utc).isoformat()}] {m}", flush=True)

def safe_load_chain():
    with FileLock(str(LOCK_FILE), timeout=15):
        txt = CHAIN_FILE.read_text().strip()
        if not txt: raise ValueError("empty chain.json")
        return json.loads(txt)

def sun_altitude(dt: datetime):
    day = dt.timetuple().tm_yday
    hour = dt.hour + dt.minute/60 + dt.second/3600
    lat_rad = math.radians(GPS_LAT)
    decl = math.radians(23.44 * math.sin(math.radians(360/365 * (284+day))))
    ha = math.radians(15*(hour-12) + GPS_LON/15*15)
    alt = math.asin(math.sin(lat_rad)*math.sin(decl) + math.cos(lat_rad)*math.cos(decl)*math.cos(ha))
    return round(math.degrees(alt), 4)

def get_btc_height():
    import requests
    providers = [
        ("mempool.space US", "https://mempool.space/api/blocks/tip/height", lambda r: int(r.text.strip())),
        ("blockstream.info", "https://blockstream.info/api/blocks/tip/height", lambda r: int(r.text.strip())),
        ("blockchain.info q", "https://blockchain.info/q/getblockcount", lambda r: int(r.text.strip())),
        ("mempool.emzy", "https://mempool.emzy.de/api/blocks/tip/height", lambda r: int(r.text.strip())),
        ("mempool.space backup", "https://mempool.space/api/blocks/tip/height", lambda r: int(r.text.strip())),
    ]
    for name, url, parser in providers:
        try:
            r = requests.get(url, timeout=7, headers={"User-Agent": "Pond/v4-world"})
            if not r.ok:
                continue
            h = parser(r)
            if h and 700000 < h < 2000000:
                log(f"BTC {h} via {name} ✅")
                return h
        except Exception as e:
            log(f"[{name}] fail {e}")
            continue
    try:
        chain=json.loads(Path("chain.json").read_text())
        last=chain[-1]['payload'].get('btcHeight')
        if last:
            log(f"BTC fallback chain {last}")
            return last
    except:
        pass
    log("BTC all mirrors failed")
    return None

def sync_embassy():
    try:
        os.makedirs('embassy/public', exist_ok=True)
        shutil.copy2('chain.json','embassy/public/chain.json')
        shutil.copy2('chain.json','embassy/public/blocks.json')
    except Exception as e:
        log(f"sync_embassy fail: {e}")

def mine_and_save(ts_override=None):
    with FileLock(str(LOCK_FILE), timeout=15):
        try:
            chain = json.loads(CHAIN_FILE.read_text())
        except:
            subprocess.run(["git","checkout","HEAD","--","chain.json"], capture_output=True)
            chain = json.loads(CHAIN_FILE.read_text())
        prev = chain[-1]
        ts_dt = ts_override if ts_override else datetime.now(timezone.utc)
        ts = ts_dt.isoformat().replace("+00:00","Z")
        if len(chain) >= 698:
            last_ts = datetime.fromisoformat(prev['payload']['ts'].replace("Z","+00:00"))
            diff = (ts_dt - last_ts).total_seconds()
            if diff < 590:
                log(f"TOO FAST {diff}s <590 - WAIT")
                raise ValueError(f"too fast {diff}")
        btc_h = get_btc_height()
        sun_alt = sun_altitude(ts_dt)
        btc_anchor_hash, btc_anchor_height = get_btc_anchor()
        payload = {"index": len(chain),"ts": ts,"prev": prev.get("hash"),"entropy": hashlib.sha256(f"{ts}{random.random()}".encode()).hexdigest()[:32],"sunAltitude": sun_alt,"gps": f"{GPS_LAT},{GPS_LON}","btcHeight": btc_h,"btc_anchor_hash": btc_anchor_hash,"btc_anchor_height": btc_anchor_height,"pondId": "27ef008c31aec59f"}
        block_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        block = {"index": len(chain),"hash": block_hash,"prev": prev.get("hash"),"payload": payload}
        chain.append(block)
        tmp = CHAIN_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps(chain, indent=2))
        tmp.replace(CHAIN_FILE)
        LAST_FILE.write_text(block_hash+"\n")
        sha = hashlib.sha256(CHAIN_FILE.read_bytes()).hexdigest()
        SHA_FILE.write_text(f"{sha}  chain.json\n")
        sync_embassy()
        log(f"MINED {block['index']} {block_hash[:12]} sun {sun_alt} btc {btc_h}")
        return block

def auto_push(block_index):
    try:
        sync_embassy()
        subprocess.run(["git","add","-f","chain.json","LAST.txt","SHA256.txt","KERNEL_LAW.md","DUPE_PROOF.md","kernel.py","embassy/public/chain.json","embassy/public/blocks.json"], capture_output=True, timeout=10)
        msg = f"pond v4 WORLD MIRRORS SUN+BTC {block_index} {datetime.now(timezone.utc).isoformat()}"
        r = subprocess.run(["git","commit","-m",msg], capture_output=True, text=True, timeout=10)
        if "nothing to commit" in (r.stdout + r.stderr):
            return False
        pr = subprocess.run(["git","push"], capture_output=True, text=True, timeout=30)
        if pr.returncode==0:
            log(f"AUTO-PUSH OK {block_index}")
            return True
        else:
            log(f"push fail {pr.stderr[:200]}")
            return False
    except Exception as e:
        log(f"auto_push err {e}")
        return False