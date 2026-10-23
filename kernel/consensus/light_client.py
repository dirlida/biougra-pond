import json, pathlib
ROOT=pathlib.Path.home()/"pond"
CHAIN=ROOT/"chain.json"
PUBLIC=ROOT/"embassy"/"public"
def build_headers():
    chain=json.loads(CHAIN.read_text())
    headers=[]
    for b in chain[-500:]:
        headers.append({"index":b.get("index"),"hash":b.get("hash"),"prev":b.get("prev"),"nonce":b.get("nonce",0),"difficulty":b.get("difficulty",0),"merkle_root":b.get("merkle_root","0"*64),"ts":b.get("payload",{}).get("ts"),"btcHeight":b.get("payload",{}).get("btcHeight",0)})
    PUBLIC.mkdir(parents=True, exist_ok=True)
    out=PUBLIC/"headers.json"
    out.write_text(json.dumps(headers, indent=2))
    print(f"light headers {len(headers)} -> {out} {out.stat().st_size} bytes")
if __name__=="__main__": build_headers()
