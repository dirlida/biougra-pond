import math
seed_hex = "8fcf242b678b44a7e96f8fd9f7ec570be30880338f3890e9940163e5bdeeee05"
theta=1.7648
phi=2.5414
GPS=(30.12613, -9.37437)
SUN=36.98
BTC=969613
p0=math.cos(theta/2)**2
print(f"[POND WALLET] seed={seed_hex}")
print(f"[ANGLES] theta={theta} phi={phi}")
print(f"[PROOF] GPS={GPS} SUN={SUN} BTC={BTC}")
print(f"[SIMULATOR] |0> prob: {p0:.4f} |1> prob: {1-p0:.4f}")
print(f"[BACKEND] local - no qiskit")
