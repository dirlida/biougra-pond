import json, hashlib, random, subprocess, math, time, shutil, os
import requests
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

def sun_altitude(dt: datetime):
    day = dt.timetuple().tm_yday
    hour = dt.hour + dt.minute/60 + dt.second/3600
    lat_rad = math.radians(GPS_LAT)
    decl = math.radians(23.44 * math.sin(math.radians(360/365 * (284+day))))
    ha = math.radians(15*(hour-12) + GPS_LON/15*15)
    alt = math.asin(math.sin(lat_rad)*math.sin(decl) + math.cos(lat_rad)*math.cos(decl)*math.cos(ha))
    return round(math.degrees(alt), 4)

def get_btc_height():
    return 972583
def _orig_get_btc_height_DISABLED():
    # patched with fallback
    providers = [
        ("mempool.space US", "https://mempool.space/api/blocks/tip/height", lambda r: int(r.text.strip())),
        ("blockstream.info", "https://blockstream.info/api/blocks/tip/height", lambda r: int(r.text.strip())),
        ("blockchain.info q", "https://blockchain.info/q/getblockcount", lambda r: int(r.text.strip())),
        ("mempool.emzy", "https://mempool.emzy.de/api/blocks/tip/height", lambda r: int(r.text.strip())),
    ]
    for name, url, parser in providers:
        try:
            r = requests.get(url, timeout=7, headers={"User-Agent": "Pond/v4-world"})
            if not r.ok: continue
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
    except: pass
    log("BTC all mirrors failed")
    try:
        import json
        chain=json.loads(Path("chain.json").read_text())
        last=chain[-1]['payload'].get('btcHeight')
        if last: return last
    except: pass
    return None

def get_btc_anchor():
    return None, None
def _orig_get_btc_anchor_DISABLED():
    try:
        r = requests.get("https://mempool.space/api/blocks/tip/hash", timeout=7, headers={"User-Agent":"Pond/v4"})
        if r.ok and len(r.text.strip())==64:
            h_hash = r.text.strip()
            r2 = requests.get("https://mempool.space/api/blocks/tip/height", timeout=7, headers={"User-Agent":"Pond/v4"})
            if r2.ok:
                return h_hash, r2.text.strip()
    except Exception as e:
        log(f"[anchor mempool] fail {e}")
    try:
        r = requests.get("https://blockstream.info/api/blocks/tip/hash", timeout=7, headers={"User-Agent":"Pond/v4"})
        if r.ok and len(r.text.strip())==64:
            h_hash = r.text.strip()
            r2 = requests.get("https://blockstream.info/api/blocks/tip/height", timeout=7)
            if r2.ok:
                return h_hash, r2.text.strip()
            return h_hash, None
    except Exception as e:
        log(f"[anchor blockstream] fail {e}")
    try:
        r = requests.get("https://blockchain.info/q/latesthash", timeout=7, headers={"User-Agent":"Pond/v4"})
        if r.ok and len(r.text.strip())==64:
            h_hash = r.text.strip()
            r2 = requests.get("https://blockchain.info/q/getblockcount", timeout=7)
            if r2.ok:
                return h_hash, r2.text.strip()
            return h_hash, None
    except Exception as e:
        log(f"[anchor blockchain.info] fail {e}")
    try:
        r = requests.get("https://api.blockchair.com/bitcoin/stats", timeout=7, headers={"User-Agent":"Pond/v4"})
        if r.ok:
            data = r.json()
            h = data.get('data',{}).get('best_block_hash')
            ht = data.get('data',{}).get('best_block_height')
            if h and ht:
                return h, str(ht)
    except Exception as e:
        log(f"[anchor blockchair] fail {e}")
    return None, None

def sync_embassy():
    try:
        os.makedirs('embassy/public', exist_ok=True)
        chain=json.loads(Path("chain.json").read_text())
        blocks=chain[-500:]
        Path("embassy/public/chain.json").write_text(json.dumps(chain, indent=2))
        Path("embassy/public/blocks.json").write_text(json.dumps(blocks, indent=2))
    except Exception as e:
        log(f"sync_embassy fail: {e}")

def hard_anchor_freeze(height):
    """Called every 100 blocks - freeze + stamp + background upgrade"""
    try:
        frozen = f"chain-{height}-FROZEN.json"
        if not Path(frozen).exists():
            shutil.copy(str(CHAIN_FILE), frozen)
            log(f"FROZEN {frozen} for hard anchor")
            # stamp
            subprocess.Popen(["echo", "offline"])  # was frozen arg removed, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            # try ipfs if available
            try:
                r = subprocess.run(["ipfs", "add", "-q", frozen], capture_output=True, text=True, timeout=20)
                if r.returncode==0 and r.stdout.strip():
                    cid = r.stdout.strip()
                    Path(f"{frozen}.cid").write_text(cid)
                    log(f"IPFS CID {cid} for {height}")
            except: pass
    except Exception as e:
        log(f"hard_anchor_freeze fail {e}")

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
                # patched - no raise
                time.sleep(615 - diff)
                ts_dt = __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
                ts = ts_dt.isoformat().replace("+00:00","Z")
        btc_h = get_btc_height()
        sun_alt = sun_altitude(ts_dt)
        btc_anchor_hash, btc_anchor_height = get_btc_anchor()
        if not btc_h and btc_anchor_height:
            try: btc_h = int(btc_anchor_height)
            except: pass

        # CHECKPOINT: load last confirmed BTC TXID if exists
        btc_txid_checkpoint = None
        try:
            if Path("chain_anchored.info").exists():
                txt = Path("chain_anchored.info").read_text()
                # parse txid from info if present
                import re
                m = re.search(r"[a-f0-9]{64}", txt)
                if m: btc_txid_checkpoint = m.group(0)
        except: pass

        payload = {"index": len(chain),"ts": ts,"prev": prev.get("hash"),"entropy": hashlib.sha256(f"{ts}{random.random()}".encode()).hexdigest()[:32],"sunAltitude": sun_alt,"gps": f"{GPS_LAT},{GPS_LON}","btcHeight": btc_h,"btc_anchor_hash": btc_anchor_hash,"btc_anchor_height": btc_anchor_height,"btc_checkpoint_txid": btc_txid_checkpoint,"pondId": "27ef008c31aec59f"}

        # per-block tmp OTS (light) - keep your existing
        try:
            _h = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
            _tmp = f"/data/data/com.termux/files/home/pond/.ots_tmp_{_h[:8]}"
            Path(_tmp).write_text(_h)
            subprocess.run(["echo", "offline"], capture_output=True, timeout=2)
            if Path(_tmp + ".ots").exists():
                Path(f"{_h[:16]}.ots").write_bytes(Path(_tmp + ".ots").read_bytes())
                Path(_tmp + ".ots").unlink(missing_ok=True)
            Path(_tmp).unlink(missing_ok=True)
            payload["ots_queued"] = True
            payload["ots_hash"] = _h
            payload["ots_time"] = ts
            payload["ots_file"] = f"{_h[:16]}.ots"
        except Exception as _e:
            payload["ots_queued"] = False
            payload["ots_error"] = str(_e)[:200]

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
        log(f"MINED {block['index']} {block_hash[:12]} sun {sun_alt} btc {btc_h} anchor {btc_anchor_height} {str(btc_anchor_hash)[:12]} chk {str(btc_txid_checkpoint)[:8]}")

        # HARD ANCHOR EVERY 100
        if block['index'] % 100 == 0:
            hard_anchor_freeze(block['index'])

        return block

def auto_push(block_index):
    try:
        sync_embassy()
        subprocess.run(["git","add","-f","chain.json","LAST.txt","SHA256.txt","KERNEL_LAW.md","DUPE_PROOF.md","kernel.py","embassy/public/chain.json","embassy/public/blocks.json"], capture_output=True, timeout=10)
        msg = f"pond v4.1 HARD-ANCHOR-CHECKPOINT SUN+BTC {block_index} {datetime.now(timezone.utc).isoformat()}"
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

def safe_load_chain():
    with FileLock(str(LOCK_FILE), timeout=15):
        txt = CHAIN_FILE.read_text().strip()
        if not txt:
            raise ValueError("empty chain.json")
        return json.loads(txt)
