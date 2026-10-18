import time, os, requests
from datetime import datetime, timezone
from kernel import safe_load_chain, mine_and_save, auto_push, log

def post_beacon(height, h, btc_anchor_height=None):
    try:
        tok = os.getenv("TG_TOKEN")
        ch = os.getenv("TG_CHANNEL")
        if not tok or not ch:
            return
        extra = f" | BTC {btc_anchor_height}" if btc_anchor_height else ""
        msg = f"🔵 *POND BEACON v3* | Height: `{height}` | Hash: `{h[:16]}`{extra} | Alive"
        requests.post(f"https://api.telegram.org/bot{tok}/sendMessage",
                      data={"chat_id": ch, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except Exception as e:
        log(f"beacon fail: {e}")

def main():
    log("Pond daemon v3 - BTC soft anchor + FileLock + TG beacon")
    last_pushed = -1
    while True:
        try:
            chain = safe_load_chain()
            now = datetime.now(timezone.utc)
            last_ts = datetime.fromisoformat(chain[-1]['payload']['ts'].replace("Z","+00:00"))
            actual = len(chain)-1
            diff = (now - last_ts).total_seconds()
            if actual != last_pushed:
                import subprocess
                res = subprocess.run(["git","status","--porcelain","chain.json","LAST.txt"], capture_output=True, text=True, timeout=5)
                if res.stdout.strip():
                    log(f"External block {actual} detected, pushing")
                    if auto_push(actual):
                        last_pushed = actual
                        try:
                            payload = chain[-1].get('payload', {})
                            post_beacon(actual, chain[-1]['hash'], payload.get('btc_anchor_height'))
                        except:
                            pass
            if diff < 615:
                wait = int(615 - diff) + 2
                log(f"on-time {actual} {diff:.0f}s ago - waiting {wait}s")
                time.sleep(min(wait, 60))
                continue
            log(f"time to mine: {diff:.0f}s since last - fetching BTC anchor")
            block = mine_and_save()
            log(f"Mined {block['index']} | {block['hash'][:12]} | BTC anchor {block.get('payload',{}).get('btc_anchor_height')}")
            payload = block.get('payload', {})
            post_beacon(block['index'], block['hash'], payload.get('btc_anchor_height'))
            if auto_push(block['index']):
                last_pushed = block['index']
            time.sleep(615)
        except Exception as e:
            log(f"error: {e}")
            import traceback; log(traceback.format_exc()[-500:])
            time.sleep(10)

if __name__ == "__main__":
    main()
