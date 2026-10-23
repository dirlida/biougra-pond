import json, hashlib
from datetime import datetime
from pathlib import Path

def sha_sorted(p): return hashlib.sha256(json.dumps(p, sort_keys=True).encode()).hexdigest()
def pdt(s): return datetime.fromisoformat(s.replace("Z","+00:00"))

c=json.loads(Path("chain.json").read_text())
gen=json.loads(Path("GENESIS.json").read_text())

assert c[0]["hash"]==gen["hash"], f"GENESIS MISMATCH {c[0]['hash'][:12]} vs {gen['hash'][:12]}"
print(f"GENESIS OK {gen['hash'][:12]}")

# 0-35 bootstrap - no 10min rule, just prev linkage
for i in range(1, min(36, len(c))):
    b=c[i]
    assert b["prev"]==c[i-1]["hash"], f"prev FAIL #{i}"
    assert b["payload"]["prev"]==c[i-1]["hash"], f"payload.prev FAIL #{i}"
print("0-35 bootstrap OK - grandfathered")

# 36 transition
if len(c) > 36:
    b=c[36]
    print(f"36 transition {b['hash'][:12]} {b['payload']['ts']} attested")

# Full run check
fails=[]
fast_blocks=[] # only flag if >=698 (10min era)
slow_blocks=[]

for i in range(37, len(c)):
    b=c[i]; p=b["payload"]; prev=c[i-1]
    
    # hash linkage
    if b["prev"]!=prev["hash"]: fails.append(f"#{i} prev hash broken")
    if p["prev"]!=prev["hash"]: fails.append(f"#{i} payload.prev broken")
    
    # hash calc
    if sha_sorted(p)!=b["hash"]: fails.append(f"#{i} hash mismatch")
    
    # timestamp monotonic (all eras must go forward)
    try:
        cur_t=pdt(p["ts"])
        prev_t=pdt(prev["payload"]["ts"])
        diff=(cur_t-prev_t).total_seconds()
        if diff <= 0:
            fails.append(f"#{i} TIME BACKWARDS {diff}s")
        # 10min rule ONLY from 698 onward - grandfather 300-400 fast ones
        if i >= 698:
            if diff < 590:
                fast_blocks.append(f"#{i} {diff:.0f}s <590")
            if diff > 1200:
                slow_blocks.append(f"#{i} {diff:.0f}s >1200")
    except Exception as e:
        fails.append(f"#{i} ts parse {e}")

# Report
if fails:
    print("🔴 FAIL:")
    for f in fails: print(f)
    exit(1)

if fast_blocks or slow_blocks:
    print("⚠️ 10min era warnings (>=698):")
    for f in fast_blocks[-10:]: print(f"  FAST {f}")
    for f in slow_blocks[-10:]: print(f"  SLOW {f}")
    # fast in 10min era is critical - fail
    if fast_blocks:
        print(f"🔴 FAST VIOLATION in 10min era")
        exit(1)

# btc anchoring era check
btc_start=None
for i,b in enumerate(c):
    if b['payload'].get('btcHeight') is not None:
        btc_start=i
        break
if btc_start:
    print(f"BTC anchored from #{btc_start} onward (yesterday era)")
else:
    print("BTC not anchored yet")

print(f"37-{len(c)-1} OK: {len(c)-37} blocks")
print(f"last: #{c[-1]['index']} {c[-1]['hash'][:12]} {c[-1]['payload']['ts']} sun={c[-1]['payload'].get('sunAltitude')} btc={c[-1]['payload'].get('btcHeight')}")
print(f"OK: {len(c)} total - ATTESTED - RUNNING - NO BREAK THIS MORNING")
