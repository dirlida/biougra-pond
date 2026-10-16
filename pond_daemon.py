import time
from datetime import datetime, timezone
from kernel import safe_load_chain, mine_and_save, auto_push, log

def main():
    log("Pond daemon v2.3 - single kernel + FileLock - immortal-safe")
    last_pushed = -1
    while True:
        try:
            chain = safe_load_chain()
            now = datetime.now(timezone.utc)
            last_ts = datetime.fromisoformat(chain[-1]['payload']['ts'].replace("Z","+00:00"))
            actual = len(chain)-1
            diff = (now - last_ts).total_seconds()

            # external block detection (hammer pushed chain but git not pushed)
            if actual != last_pushed:
                import subprocess
                res = subprocess.run(["git","status","--porcelain","chain.json","LAST.txt"], capture_output=True, text=True, timeout=5)
                if res.stdout.strip():
                    log(f"External block {actual} detected, pushing")
                    if auto_push(actual):
                        last_pushed = actual

            if diff < 615:
                wait = int(615 - diff) + 2
                log(f"on-time {actual} {diff:.0f}s ago - waiting {wait}s")
                time.sleep(min(wait, 60))
                continue

            log(f"time to mine: {diff:.0f}s since last")
            block = mine_and_save()
            log(f"Mined {block['index']} | {block['hash'][:12]}")
            if auto_push(block['index']):
                last_pushed = block['index']
            time.sleep(615)
        except Exception as e:
            log(f"error: {e}")
            import traceback; log(traceback.format_exc()[-500:])
            time.sleep(10)

if __name__ == "__main__":
    main()
