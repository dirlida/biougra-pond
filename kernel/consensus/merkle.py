import hashlib, json
def sha(s): return hashlib.sha256(s.encode()).hexdigest()
def merkle_root(txs):
    # txs = list of dicts or strings
    if not txs: return "0"*64
    leaves = [sha(json.dumps(t, sort_keys=True) if isinstance(t, dict) else str(t)) for t in txs]
    while len(leaves) > 1:
        if len(leaves) % 2 == 1:
            leaves.append(leaves[-1])
        nxt=[]
        for i in range(0, len(leaves), 2):
            nxt.append(sha(leaves[i]+leaves[i+1]))
        leaves=nxt
    return leaves[0]

if __name__ == "__main__":
    print(merkle_root([{"from":"a","to":"b","amt":1}]))
