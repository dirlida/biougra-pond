#!/usr/bin/env python3
"""
Biougra Pond - WakeLock Stable Daemon v1
- Tries Brisbane QPU, fallback to sim_30q_light (auto)
- Mints if S>2.0 and sun_elev>15
- Push retry loop + keeps wakelock
- Termux-only A13 stable
"""
import json, time, subprocess, os, sys
from datetime import datetime

CHAIN="chain.json"

def load_chain():
    with open(CHAIN) as f:
        return json.load(f)

def try_qpu_mint():
    # 1. Try real QPU via pond_new_block.py (no --sim)
    try:
        print(f"[{datetime.now()}] Trying QPU Brisbane...")
        r = subprocess.run(["python", "pond_new_block.py"], capture_output=True, text=True, timeout=120)
        print(r.stdout[-300:])
        if "VALID" in r.stdout or "Block" in r.stdout:
            return "brisbane"
    except Exception as e:
        print(f"QPU fail: {e}")

    # 2. Fallback sim
    print(f"[{datetime.now()}] Fallback to sim_30q_light...")
    r = subprocess.run(["python", "pond_new_block.py", "--sim"], capture_output=True, text=True, timeout=60)
    print(r.stdout[-300:])
    return "sim_30q_light"

def push_retry():
    for _ in range(3):
        try:
            subprocess.run(["git", "add", CHAIN], check=False)
            # only commit if changed
            diff = subprocess.run(["git", "diff", "--cached", "--quiet"])
            if diff.returncode != 0:
                subprocess.run(["git", "commit", "-m", f"daemon block {len(load_chain())-1} {datetime.now().isoformat()} auto"], check=False)
            p = subprocess.run(["git", "push"], capture_output=True, text=True, timeout=60)
            print(p.stdout[-200:], p.stderr[-200:])
            if "main -> main" in p.stderr or "main -> main" in p.stdout or p.returncode==0:
                return True
        except Exception as e:
            print(f"push retry fail {e}")
        time.sleep(10)
    return False

def main_loop():
    print("== POND DAEMON START (wake-lock) ==")
    print("Origin: Biougra Pond 30.12613,-9.37437 | Anywhere validator")
    # acquire wake-lock if termux-wake-lock exists
    try: subprocess.run(["termux-wake-lock"], check=False)
    except: pass

    while True:
        try:
            chain = load_chain()
            print(f"\n[{datetime.now()}] Chain {len(chain)} blocks | last S={chain[-1].get('payload',{}).get('bell_S')}")
            qpu_used = try_qpu_mint()
            push_retry()

            # verify
            subprocess.run(["python", "verify.py"], check=False)

            print(f"Sleep 30m... qpu={qpu_used}")
            time.sleep(30*60)  # 30 min

        except KeyboardInterrupt:
            print("Daemon stop")
            try: subprocess.run(["termux-wake-unlock"], check=False)
            except: pass
            break
        except Exception as e:
            print(f"Loop error {e}")
            time.sleep(60)

if __name__ == "__main__":
    main_loop()
