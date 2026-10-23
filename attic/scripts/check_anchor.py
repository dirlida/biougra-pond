import os, subprocess, json, sys
from datetime import datetime

FROZEN = "chain-FROZEN-2026-10-18-1748.json"
OTS = FROZEN + ".ots"

def cmd(c):
    try:
        return subprocess.getoutput(c)
    except Exception as e:
        return str(e)

print(f"=== ANCHOR CHECK {datetime.now()} ===")
print(f"File: {FROZEN} exists? {os.path.exists(FROZEN)}")
print(f"OTS: {OTS} exists? {os.path.exists(OTS)}")

if os.path.exists(OTS):
    print("\n--- ots info ---")
    print(cmd(f"ots info {OTS}"))
    print("\n--- ots verify ---")
    print(cmd(f"ots verify {OTS}"))
else:
    print(f"\nNo .ots yet. Create with: ots stamp {FROZEN}")

print("\n--- BTC height check ---")
print(cmd("curl -s https://mempool.space/api/blocks/tip/height"))

print("\n--- chain head ---")
if os.path.exists("chain.json"):
    try:
        with open("chain.json") as f:
            data = json.load(f)
            print(f"blocks: {len(data)}")
            if data:
                print(f"last block: {data[-1]}")
    except Exception as e:
        print(e)
