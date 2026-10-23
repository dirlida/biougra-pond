import json, pathlib, hashlib, time
ROOT=pathlib.Path.home()/"pond"
STATE=ROOT/"kernel"/"modules"/"wallet"/"state.json"
def load_state():
    try: return json.loads(STATE.read_text())
    except: return {"utxo":{},"balances":{},"height":0,"total_supply":0}
def save_state(s):
    s["updated"]=int(time.time())
    STATE.write_text(json.dumps(s, indent=2))
def create_coinbase(to_addr, amount, height):
    txid=hashlib.sha256(f"coinbase-{height}-{to_addr}-{time.time()}".encode()).hexdigest()
    return {"txid":txid,"type":"coinbase","vin":[],"vout":[{"to":to_addr,"amount":amount,"mature_height":height+100}],"fee":0,"ts":int(time.time()),"height":height}
def validate_tx(tx, state):
    utxo=state.get("utxo",{})
    if tx.get("type")=="coinbase": return True,"coinbase"
    total_in=0
    seen=set()
    for inp in tx.get("vin",[]):
        txid=inp.get("txid"); vout=str(inp.get("vout",0)); key=f"{txid}:{vout}"
        if key in seen: return False,f"double spend same tx {key}"
        seen.add(key)
        if txid not in utxo or vout not in utxo[txid]: return False,f"input not found {key}"
        entry=utxo[txid][vout]
        if entry.get("spent"): return False,f"already spent {key}"
        if entry.get("mature_height",0) > state.get("height",0): return False,f"immature {key} matures {entry.get('mature_height')}"
        total_in+=entry.get("amount",0)
    total_out=sum(o.get("amount",0) for o in tx.get("vout",[]))
    fee=total_in-total_out
    if fee<0: return False,f"overspend in={total_in} out={total_out}"
    if fee<1: return False,f"fee low {fee}"
    return True,f"OK in={total_in} out={total_out} fee={fee}"
def apply_txs(txs, height):
    state=load_state(); state["height"]=height; applied=0
    for tx in txs:
        ok,msg=validate_tx(tx, state)
        if not ok:
            print(f"UTXO REJECT {tx.get('txid','?')[:8]} {msg}"); continue
        for inp in tx.get("vin",[]):
            txid=inp.get("txid"); vout=str(inp.get("vout",0))
            if txid in state["utxo"] and vout in state["utxo"][txid]:
                state["utxo"][txid][vout]["spent"]=True
                state["utxo"][txid][vout]["spent_at"]=height
        txid=tx.get("txid")
        if txid not in state["utxo"]: state["utxo"][txid]={}
        for i,out in enumerate(tx.get("vout",[])):
            state["utxo"][txid][str(i)]={"to":out.get("to"),"amount":out.get("amount"),"mature_height":out.get("mature_height",height),"spent":False,"created_at":height}
            to_addr=out.get("to")
            if to_addr not in state["balances"]: state["balances"][to_addr]=0
            state["balances"][to_addr]+=out.get("amount",0)
        if tx.get("type")=="coinbase":
            state["total_supply"]=state.get("total_supply",0)+sum(o.get("amount",0) for o in tx.get("vout",[]))
        applied+=1
    save_state(state)
    return applied
if __name__=="__main__":
    s=load_state()
    print(f"UTXO {len(s.get('utxo',{}))} txs, balances {s.get('balances',{})}, supply {s.get('total_supply')}")
