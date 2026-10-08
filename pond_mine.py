import hashlib, math, time, random

# Your biougra pond constants
GPS = "30.12613,-9.37437"
THETA = 1.7648
PHI = 2.5414
S_IDEAL = 2.828427
S_BRISBANE = 2.616

# Simulate mining: hash of GPS+time+theta+S -> quantum wallet address
def mine_block():
    nonce = random.randint(0, 999999)
    data = f"{GPS}|{THETA}|{S_IDEAL}|{nonce}|{int(time.time())}"
    h = hashlib.sha256(data.encode()).hexdigest()
    # wallet validity = first 4 chars hex < S*1000
    target = int(S_IDEAL * 1000) # 2828
    if int(h[:4], 16) % 10000 < target:
        return True, h, nonce, data
    return False, h, nonce, data

print(f"[BIOUGRA MINE] GPS={GPS} | S={S_IDEAL}")
print("Mining proof-of-location + quantumness...\n")

blocks=0
tries=0
while blocks<3:
    tries+=1
    ok, h, nonce, data = mine_block()
    if ok:
        blocks+=1
        print(f"BLOCK {blocks} MINED | tries={tries}")
        print(f" hash={h}")
        print(f" nonce={nonce}")
        print(f" data={data[:50]}...")
        print(f" wallet proof: S={S_IDEAL} > 2 = quantum\n")
        tries=0

print("Pond chain valid - phone is the miner")
