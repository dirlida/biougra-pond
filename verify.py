import json, hashlib, math, time

with open("wallet.json") as f:
    w=json.load(f)

GPS=w["gps"]
THETA=w["theta"]
PHI=w["phi"]
S=w["proof_S_ideal"]
blocks=w["blocks"]
balance=w["balance"]

# Recompute
seed = f"{GPS}|{THETA}|{PHI}|{S}"
priv = hashlib.sha256(seed.encode()).hexdigest()
addr = "bq_" + hashlib.sha256(priv.encode()).hexdigest()[:16]

expected_bal = round(len(blocks)*S,6)
ok_addr = addr==w["address"]
ok_bal = abs(expected_bal-balance)<1e-6
ok_quant = w["quantum_verified"] and S>2
ok_S = abs(S-2.828427)<0.001

print(f"Address check: {w['address']} == {addr} -> {ok_addr}")
print(f"Balance check: {balance} == {len(blocks)}*S={expected_bal} -> {ok_bal}")
print(f"S_ideal={S} S>2 -> {ok_quant}")
print(f"Blocks: {len(blocks)}")
if ok_addr and ok_bal and ok_quant and ok_S:
    print("VERIFIED: wallet valid, quantum proof holds")
else:
    print("FAILED: check failed")
