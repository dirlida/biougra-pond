import time, os, requests, subprocess, traceback
from datetime import datetime, timezone
from kernel import safe_load_chain, mine_and_save, auto_push, log

def post_beacon(height, h):
    try:
        tok = os.getenv("TG_TOKEN"); ch = os.getenv("TG_CHANNEL")
        if not tok or not ch: return
        msg = f"🟢 *POND BEACON v4.2* | Height: `{height}` | Hash: `{h[:16]}`"
        requests.post(f"https://api.telegram.org/bot{tok}/sendMessage", data={"chat_id": ch, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except: pass

def main():
    log("Pond daemon v4.2 - FINAL ZERO-LOCK - kernel handles lock")
    last_pushed = -1
    while True:
        try:
            chain = safe_load_chain()
            now = datetime.now(timezone.utc)
            last_ts = datetime.fromisoformat(chain[-1]['payload']['ts'].replace("Z","+00:00"))
            actual = len(chain)-1
            diff = (now - last_ts).total_seconds()

            if actual != last_pushed:
                res = subprocess.run(["git","status","--porcelain","chain.json","LAST.txt"], capture_output=True, text=True, timeout=5)
                if res.stdout.strip():
                    log(f"External {actual} -> push")
                    if auto_push(actual):
                        last_pushed = actual
                        post_beacon(actual, chain[-1]['hash'])

            if diff < 615:
                wait = int(615-diff)+2
                log(f"on-time {actual} {diff:.0f}s ago wait {wait}s")
                time.sleep(min(wait,60))
                continue

            log(f"MINING {actual+1} - {diff:.0f}s elapsed")
            block = mine_and_save()
            log(f"MINED {block['index']} {block['hash'][:12]}")
            post_beacon(block['index'], block['hash'])
            if auto_push(block['index']):
                last_pushed = block['index']
            time.sleep(615)
        except Exception as e:
            log(f"err {e}")
            log(traceback.format_exc()[-600:])
            time.sleep(10)

if __name__ == "__main__":
    main()
