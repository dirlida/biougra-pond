import hashlib, json, time
def sha256d(s): 
    return hashlib.sha256(hashlib.sha256(s.encode()).digest()).hexdigest() if isinstance(s,str) else hashlib.sha256(hashlib.sha256(s).digest()).hexdigest()

def hash_header(prev, merkle_root, ts, btcHeight, nonce, difficulty, index, cables_hash="", drones_hash="", stamp_hash="", wallet_height=0):
    # deterministic header - what PoW secures
    header = f"{index}|{prev}|{merkle_root}|{ts}|{btcHeight}|{nonce}|{difficulty}|{cables_hash}|{drones_hash}|{stamp_hash}|{wallet_height}"
    return hashlib.sha256(header.encode()).hexdigest()

def meets_target(hash_hex, difficulty):
    # difficulty = number of leading zero hex chars, e.g. 4 = "0000"
    return hash_hex.startswith("0"*difficulty)

def mine(prev, merkle_root, ts, btcHeight, difficulty, index, cables_hash="", drones_hash="", stamp_hash="", wallet_height=0, max_nonce=5_000_000):
    # returns nonce, hash
    nonce=0
    while nonce < max_nonce:
        h = hash_header(prev, merkle_root, ts, btcHeight, nonce, difficulty, index, cables_hash, drones_hash, stamp_hash, wallet_height)
        if meets_target(h, difficulty):
            return nonce, h
        nonce+=1
    return None, None

if __name__ == "__main__":
    # test: mine genesis-style
    n,h = mine("0"*64, "0"*64, int(time.time()), 972583, 3, 1314)
    print(f"mined nonce={n} hash={h}")
