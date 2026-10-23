import time, os, sys
sys.path.insert(0, os.path.expanduser("~/pond/attic/scripts"))
sys.path.insert(0, os.path.expanduser("~/pond/kernel"))
import subprocess, traceback
from datetime import datetime, timezone
from kernel import safe_load_chain, mine_and_save, log

def push_bg(h):
    try:
        subprocess.Popen(["bash","-c", f"cd ~/pond && timeout 8 git add chain.json LAST.txt >/dev/null 2>&1; timeout 8 git commit -m '{h} offline Biougra' >/dev/null 2>&1; timeout 12 git push >/dev/null 2>&1 &"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except: pass

def main():
    log("Pond daemon v4.2.2 OFFLINE PROOF - Biougra A13")
    while True:
        try:
            chain = safe_load_chain()
            now = datetime.now(timezone.utc)
            last = chain[-1]
            last_ts = datetime.fromisoformat(last['payload']['ts'].replace("Z","+00:00"))
            diff = (now - last_ts).total_seconds()
            actual = len(chain)-1
            if diff < 615:
                wait = int(615-diff)+2
                log(f"on-time {actual} {diff:.0f}s ago wait {wait}s")
                time.sleep(min(wait, 30))
                continue
            log(f"MINING {actual+1} - {diff:.0f}s elapsed - offline ok")
            block = mine_and_save()
            log(f"MINED {block['index']} {block['hash'][:12]} btc={block['payload'].get('btcHeight')} offline")
            push_bg(block['index'])
        except Exception as e:
            log(f"ERR {e} {traceback.format_exc()[:600]}")
            time.sleep(30)

if __name__ == "__main__":
    main()
