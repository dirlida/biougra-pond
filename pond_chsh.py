import numpy as np, math

# --- wallet seed (your origin) ---
theta = 1.7648
phi = 2.5414
print(f"[WALLET] theta={theta} phi={phi}")

# --- true quantum: Bell phi+ state ---
# |Phi+> = (|00> + |11>)/sqrt2
psi = np.array([1,0,0,1], dtype=complex)/math.sqrt(2)

def ry(theta):
    c = math.cos(theta/2)
    s = math.sin(theta/2)
    return np.array([[c,-s],[s,c]])

def measure_E(psi, a, b):
    # rotate Alice by a, Bob by b, then <ZZ>
    Ra = ry(a)
    Rb = ry(b)
    R = np.kron(Ra,Rb) # 4x4
    psi_rot = R @ psi
    # probabilities
    p00 = abs(psi_rot[0])**2
    p01 = abs(psi_rot[1])**2
    p10 = abs(psi_rot[2])**2
    p11 = abs(psi_rot[3])**2
    # correlator E = P_same - P_diff
    return (p00 + p11) - (p01 + p10)

# optimal CHSH angles - independent of wallet, this is physics
a = 0.0
ap = math.pi/2
b = math.pi/4
bp = -math.pi/4 # 3pi/4 equivalent, gives +2.828

E_ab = measure_E(psi, a, b)
E_abp = measure_E(psi, a, bp)
E_apb = measure_E(psi, ap, b)
E_apbp = measure_E(psi, ap, bp)

S = E_ab + E_abp + E_apb - E_apbp

print(f"E(a,b)={E_ab:.6f}")
print(f"E(a,b')={E_abp:.6f}")
print(f"E(a',b)={E_apb:.6f}")
print(f"E(a',b')={E_apbp:.6f}")
print(f"[NEW LANE REAL] S={S:.6f}")
print(f"[IDEAL] 2*sqrt2={2*math.sqrt(2):.6f}")
print(f"[YOUR BRISBANE] 2.616 - difference is IBM noise, not our math")
