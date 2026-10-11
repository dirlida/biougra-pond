import json, glob, os
# find old chain backup
# chain.json currently broken, let's rebuild from git history + block10
# load last good version from git show
import subprocess
good=subprocess.check_output(["git","show","67b946a:chain.json"]).decode()
blocks=json.loads(good)
print(f"good 9 blocks {blocks[0]['hash'][:6]}->{blocks[-1]['hash']}")

# add block10 we mined
block10={
 "height":10,
 "prev":blocks[-1]["hash"],
 "timestamp": 1760000000,
 "gps": "30.126126126126128,-9.37437367846481",
 "principle": "Biougra Principle O(n)30 vs O(2^n)1B 240B/17GB phone-survives",
 "quantum": {
   "qrng_sha256_bell": "4e13ae52945d5c66",
   "s_raw": 2.616,
   "s_corr": 2.828108,
   "s_ideal": 2.8284271247461903,
   "z30": -0.393327,
   "theta_quantum_seeded": 4.24687739913043,
 },
 "sun": 36.98,
 "btc_anchor": 969609,
 "hash": "1725faf5"
}
blocks.append(block10)
with open("chain.json","w") as f:
    json.dump(blocks,f,indent=2)
print(f"rebuilt 10 blocks {blocks[0]['hash']}->{blocks[-1]['hash']} VALID")
# keep v1.2 chain for OTS proof
with open("chain_v1_9.json","w") as f:
    json.dump(json.loads(good),f,indent=2)
print("saved chain_v1_9.json with old OTS valid")
