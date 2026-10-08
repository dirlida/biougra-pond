import json, hashlib, hmac, os
raw=open("wallet.json","rb").read()
w=json.loads(raw)
S=w.get("proof",{}).get("S_measured",0)
if S < 2.0:
    raise SystemExit("FAIL S<2")
seed=b"biougra-pond-4138350-genesis"
extra=b""
if os.path.exists("bell_log.txt"):
    extra=open("bell_log.txt","rb").read()[:1024]
calc=hmac.new(seed+extra, raw, hashlib.sha256).hexdigest()
print(f"{w['genesis']} {w['balance']} {S} {calc[:24]} {hashlib.sha256(extra).hexdigest()[:16] if extra else 'none'}")
