import json, hashlib
from datetime import datetime
def sha_sorted(p): return hashlib.sha256(json.dumps(p, sort_keys=True).encode()).hexdigest()
def pdt(s): return datetime.fromisoformat(s.replace("Z","+00:00"))
c=json.load(open("chain.json"))
gen=json.load(open("GENESIS.json"))
assert c[0]["hash"]==gen["hash"]
for i in range(1,36):
    b=c[i]
    assert b["prev"]==c[i-1]["hash"]
print("0-35 bootstrap OK")
b=c[36]
print(f"36 transition {b['hash'][:12]} attested")
fails=0
for i in range(37,len(c)):
    b=c[i]; p=b["payload"]; prev=c[i-1]
    assert b["prev"]==prev["hash"], f"prev FAIL #{i}"
    assert p["prev"]==prev["hash"], f"payload.prev FAIL #{i}"
    if pdt(p["ts"]) <= pdt(prev["payload"]["ts"]):
        fails+=1
if fails>0:
    exit(1)
print(f"37-{len(c)-1} OK: {len(c)-37} blocks")
print(f"last: {c[-1]['hash'][:12]} {c[-1]['payload']['ts']}")
print(f"OK: {len(c)} total - ATTESTED - RUNNING")
