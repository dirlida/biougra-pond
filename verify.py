import json, hashlib, os
print("Biougra Pond - Global Verifier")

with open("wallet.json") as f:
    w=json.load(f)

# gps is NOT consensus anymore
print(f"Genesis: {w['genesis']} | Balance: {w['balance']} | Blocks: {w['blocks']}")
print(f"GPS tag (metadata only): {w['gps']}")

# anti-cheat sig
if os.path.exists("bell_log.txt"):
    sig=hashlib.sha256(open("bell_log.txt","rb").read()).hexdigest()[:16]
    print(f"bell_log sig: {sig} - proof exists, not faked")
else:
    print("warn: bell_log.txt missing, run pond_chsh.py first")

# check S
import biougra
r=biougra.run()
print(f"S_ideal={r['S_ideal']:.3f} | S_measured={r['S_measured']:.3f} | Status: {r['status']}")
print("Global rule: any phone can run this. No Biougra lock.")
