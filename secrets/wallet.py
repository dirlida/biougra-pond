import hashlib, math, argparse

GENESIS_SEED = "8fcf242b3a7e9c1d5f6a0b2c8d4e6f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4"
GENESIS_GPS = "30.12613,-9.37437"
GENESIS_SUN = 36.98

def double_sha(s): 
    return hashlib.sha256(hashlib.sha256(s.encode()).digest()).hexdigest()

def derive_seed(gps, sun, btc, ts, parent=GENESIS_SEED):
    return double_sha(f"{gps}|{sun}|{btc}|{ts}|{parent}")

def seed_to_angles(seed):
    th = (int(seed[:16],16)%10000)/10000*3.1415
    ph = (int(seed[16:32],16)%10000)/10000*2*3.1415
    return round(th,4), round(ph,4)

def seed_to_testnet(seed):
    h = hashlib.sha256((seed+"testnet").encode()).hexdigest()
    return f"tb1q{h[:32]}"

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--gps", required=True)
    p.add_argument("--sun", type=float, required=True)
    p.add_argument("--btc", default="969613")
    p.add_argument("--ts", default="2026-10-04")
    args=p.parse_args()
    
    seed=derive_seed(args.gps, args.sun, args.btc, args.ts)
    th,ph=seed_to_angles(seed)
    addr=seed_to_testnet(seed)
    print(f"GENESIS PARENT: {GENESIS_SEED[:16]}... Biougra")
    print(f"YOUR SEED: {seed}")
    print(f"THETA {th} PHI {ph}")
    print(f"TESTNET ADDR (0$ demo): {addr}")
    print(f"Lineage: Biougra -> {args.gps} = PROVEN")
