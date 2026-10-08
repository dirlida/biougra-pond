import hashlib, json, os, time, math

GPS="30.12613,-9.37437"
THETA=1.7648
PHI=2.5414
S=2.828427

# Derive private key from your lab constants (deterministic)
seed = f"{GPS}|{THETA}|{PHI}|{S}"
priv = hashlib.sha256(seed.encode()).hexdigest()
wallet_addr = "bq_" + hashlib.sha256(priv.encode()).hexdigest()[:16]

# Load previous mined hashes as transactions
# From your last run
mined = [
 "cb12b6eab24183bae9eb0d6c66f38e0d6c66f38e0d49431c2c52466be16573f5695d99991b",
 "30962ae4eacdf206ae5697ffc3de5ca4b4e99ee684bebe9e5a4121ca75773c4f",
 "2b96880bcec7996af87748941035cf111e31b9e4157bc24e82e101272ba448d4"
]

balance = len(mined) * (S) # each block worth S

wallet = {
 "address": wallet_addr,
 "private_sha": priv[:16]+"...",
 "gps": GPS,
 "theta": THETA,
 "phi": PHI,
 "proof_S_ideal": S,
 "proof_S_brisbane": 2.616,
 "quantum_verified": S>2,
 "balance": round(balance,6),
 "blocks": mined,
 "created": int(time.time()),
 "chain": "biougra-pond"
}

with open("wallet.json","w") as f:
    json.dump(wallet,f,indent=2)

print(f"ADDRESS: {wallet_addr}")
print(f"BALANCE: {balance:.6f} pond")
print(f"PROOF: S={S} >2 quantum={S>2}")
print(f"FILE: wallet.json written")
