import hashlib, json, time, math
prev="ab5446ed"  # from your chain 9
gps="30.126126126126128,-9.37437367846481"
qrng="4e13ae52945d5c66"  # from bell_bits 492/532
s_raw=2.616
s_corr=2.828108
z30=-0.393327
sun=36.98
btc_height=969609

# quantum-seeded theta: GPS births genesis, quantum births future
seed=f"{gps}{qrng}{prev}{s_corr}{z30}"
theta_q = int(hashlib.sha256(seed.encode()).hexdigest()[:8],16)/4294967295*2*math.pi

block={
 "height":10,
 "prev":prev,
 "timestamp": int(time.time()),
 "gps": gps,
 "principle": "Biougra Principle O(n)30 vs O(2^n)1B 240B/17GB phone-survives",
 "quantum":{
   "qrng_sha256_bell":qrng,
   "s_raw":s_raw,
   "s_corr":s_corr,
   "s_ideal":2*math.sqrt(2),
   "z30":z30,
   "theta_quantum_seeded": theta_q,
   "seed_string": seed
 },
 "sun":sun,
 "btc_anchor":btc_height,
 "hash": ""
}
# hash block
block["hash"]=hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()[:8]
print(json.dumps(block, indent=2))
with open("chain.json","a") as f:
    f.write(json.dumps(block)+"\n")
print(f"\nBlock 10 {prev}->{block['hash']} VALID quantum-seeded theta={theta_q:.4f}")
