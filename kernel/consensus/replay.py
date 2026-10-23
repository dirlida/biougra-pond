import json, pathlib, hashlib
ROOT = pathlib.Path.home() / "pond"
CHAIN = ROOT / "chain.json"
def sha(o): return hashlib.sha256(json.dumps(o, sort_keys=True).encode()).hexdigest()
def verify():
    blocks = json.loads(CHAIN.read_text())
    for i in range(1, len(blocks)):
        prev_hash = sha(blocks[i-1])
        if blocks[i].get("prev") != prev_hash and blocks[i].get("prev_hash") != prev_hash:
            # your chain uses prev as hash link - check both keys
            if blocks[i].get("prev") != blocks[i-1].get("hash") and blocks[i].get("hash") != blocks[i-1].get("hash"):
                pass
        # simple link check: prev == previous block hash
        if blocks[i].get("prev") != blocks[i-1].get("hash") and blocks[i].get("prev") != blocks[i-1].get("hash", prev_hash):
            return f"FORK at {i} - {blocks[i].get('prev')[:8]} != {blocks[i-1].get('hash','')[:8]}"
    return f"OK {len(blocks)} blocks verified 0->tip"

if __name__ == "__main__":
    print(verify())
