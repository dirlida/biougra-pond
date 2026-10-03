import hashlib, math

GPS = (30.12613, -9.37437)
SUN_ELEV = 36.98
BTC_TIP = 969613
CHAIN_HASH = "ab5446ed"

def double_sha256(s: str) -> str:
    return hashlib.sha256(hashlib.sha256(s.encode()).digest()).hexdigest()

def stamp_seed():
    payload = f"{GPS[0]},{GPS[1]}|{SUN_ELEV}|{BTC_TIP}|{CHAIN_HASH}"
    return double_sha256(payload)

def hash_to_angles(h: str):
    a = int(h[:8], 16) / 0xFFFFFFFF * math.pi
    b = int(h[8:16], 16) / 0xFFFFFFFF * math.pi * 2
    return a, b

def build_wallet():
    seed = stamp_seed()
    theta, phi = hash_to_angles(seed)
    print(f"[POND WALLET] seed={seed}")
    print(f"[ANGLES] theta={theta:.4f} phi={phi:.4f}")
    print(f"[PROOF] GPS={GPS} SUN={SUN_ELEV} BTC={BTC_TIP}")
    try:
        from qiskit import QuantumCircuit
        qc = QuantumCircuit(1)
        qc.ry(theta, 0)
        qc.rz(phi, 0)
        qc.measure_all()
        print("\n[QISKIT CIRCUIT]")
        print(qc.draw())
        return qc, seed
    except ImportError:
        prob0 = math.cos(theta/2)**2
        print(f"\n[SIMULATOR] |0> prob: {prob0:.4f} |1> prob: {1-prob0:.4f}")
        print("pip install qiskit for real circuit")
        return None, seed

if __name__ == "__main__":
    build_wallet()

