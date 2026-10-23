"""
Insert into pond.py mine_next():

from kernel.consensus.pow import mine, hash_header
from kernel.consensus.difficulty import get_difficulty
from kernel.consensus.merkle import merkle_root
from kernel.modules.wallet.utxo import create_coinbase
import json, pathlib

def mine_next_pow():
    chain = json.loads(Path("chain.json").read_text())
    prev = chain[-1]["hash"]
    index = len(chain)
    difficulty = get_difficulty(index)
    # gather txs
    tx_pool = json.loads(Path("kernel/modules/wallet/tx_pool.json").read_text()).get("pool", [])
    coinbase = create_coinbase("did:pond:biougra-a13", 50, index)
    txs = [coinbase] + tx_pool
    mr = merkle_root(txs)
    # hashes from modules
    cables_hash = hashlib.sha256(Path("kernel/modules/cables/seabed_state.json").read_bytes()).hexdigest()[:12]
    drones_hash = hashlib.sha256(Path("kernel/modules/drones/fleet_state.json").read_bytes()).hexdigest()[:12]
    # ... etc
    payload = {
        "index": index,
        "ts": datetime.utcnow().isoformat()+"+00:00",
        "btcHeight": get_btc_height(),
        "sunAltitude": get_sun(),
        "cables_hash": cables_hash,
        "drones_hash": drones_hash,
        "stamp_hash": "...",
        "wallet_height": index,
        "merkle_root": mr,
        "coinbase": coinbase
    }
    nonce, block_hash = mine(prev, mr, payload["ts"], payload["btcHeight"], difficulty, index, cables_hash, drones_hash, "", index)
    block = {
        "hash": block_hash,
        "prev": prev,
        "index": index,
        "nonce": nonce,
        "difficulty": difficulty,
        "merkle_root": mr,
        "payload": payload
    }
    # append + atomic write
    chain.append(block)
    atomic_write("chain.json", chain)
"""
