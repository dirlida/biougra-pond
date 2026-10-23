import json, pathlib, time, re
from datetime import datetime, timezone
ROOT=pathlib.Path.home()/"pond"
CHAIN=ROOT/"chain.json"
CACHE=ROOT/"kernel"/"state"/"btc_cache.json"
def get_times():
    try:
        local=int(time.time())
        chain_ts=local; btcHeight=972583
        try:
            data=CHAIN.read_bytes()[-2048:]
            m=re.findall(rb'"ts":\s*"([^"]+)"', data)
            if m:
                chain_ts=int(datetime.fromisoformat(m[-1].decode()).timestamp())
            m2=re.findall(rb'"btcHeight":\s*(\d+)', data)
            if m2:
                btcHeight=int(m2[-1])
        except: pass
        if CACHE.exists():
            try: btcHeight=json.loads(CACHE.read_text()).get("btcHeight", btcHeight)
            except: pass
        drift=local-chain_ts
        return {"local":local,"chain":chain_ts,"drift":drift,"btcHeight":btcHeight,"slow":abs(drift)>300,"iso":datetime.now(timezone.utc).isoformat()}
    except:
        return {"local":int(time.time()),"chain":int(time.time()),"drift":0,"btcHeight":972583,"slow":False,"iso":datetime.now(timezone.utc).isoformat()}
if __name__=="__main__":
    print(json.dumps(get_times(), indent=2))
