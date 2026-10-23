# WALLET RULES - private logic, pond.py reads summary only
# emission: 1 per block for now, supply = height
import json, pathlib
ROOT = pathlib.Path.home() / "pond"
STATE = ROOT / "kernel" / "modules" / "wallet" / "state.json"
def get_supply():
    try:
        chain = json.loads((ROOT / "chain.json").read_text())
        return {"supply": len(chain), "height": len(chain)}
    except:
        return {"supply": 0}
